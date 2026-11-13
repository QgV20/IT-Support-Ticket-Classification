
from pathlib import Path
import pandas as pd

# Duong dan project
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "train.csv"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Doc du lieu
df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")

required_columns = {"Document", "Topic_group"}
missing = required_columns - set(df.columns)

if missing:
    raise ValueError(f"Missing columns: {missing}")

print("=" * 55)
print("TRAIN DATASET ANALYSIS")
print("=" * 55)

print(f"\nTotal tickets: {len(df)}")
print(f"Missing documents: {df['Document'].isna().sum()}")
print(f"Missing labels: {df['Topic_group'].isna().sum()}")

# Chuan hoa cot nhan de thong ke
df["Topic_group"] = df["Topic_group"].astype("string").str.strip()

# Phan bo nhan
distribution = (
    df["Topic_group"]
    .value_counts(dropna=False)
    .rename_axis("Category")
    .reset_index(name="Count")
)

distribution["Percentage"] = (
    distribution["Count"] / len(df) * 100
).round(2)

print("\nCATEGORY DISTRIBUTION")
print(distribution.to_string(index=False))

distribution.to_csv(
    RESULTS_DIR / "label_distribution.csv",
    index=False,
    encoding="utf-8-sig"
)

# Phan tich do dai ticket
df["word_count"] = (
    df["Document"]
    .fillna("")
    .astype(str)
    .str.split()
    .str.len()
)

length_stats = (
    df.groupby("Topic_group", dropna=False)["word_count"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)

print("\nTICKET LENGTH BY CATEGORY")
print(length_stats.to_string())

length_stats.to_csv(
    RESULTS_DIR / "ticket_length_stats.csv",
    encoding="utf-8-sig"
)

# Lay mau HR Support de nghien cuu
hr_tickets = df[
    df["Topic_group"] == "HR Support"
].copy()

print(f"\nHR Support tickets: {len(hr_tickets)}")

hr_samples = hr_tickets.sample(
    n=min(20, len(hr_tickets)),
    random_state=42
)

hr_samples[["Document", "Topic_group"]].to_csv(
    RESULTS_DIR / "hr_support_samples.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nHR SUPPORT SAMPLES")
for i, document in enumerate(hr_samples["Document"], 1):
    print(f"\n{i}. {str(document)[:300]}")

print("\nAnalysis completed.")
print("Results saved to results/")

# ==========================================
# TẠO TẬP DỮ LIỆU PHÁT TRIỂN
# ==========================================

# Giữ lại chỉ số dòng gốc để có thể đối chiếu kết quả
dev_source = df.reset_index().rename(
    columns={"index": "ticket_id"}
)

# Loại bỏ các mẫu HR Support đã xem trong Ngày 5
hr_sample_file = RESULTS_DIR / "hr_support_samples.csv"

if hr_sample_file.exists():
    inspected = pd.read_csv(hr_sample_file)
    dev_source = dev_source[
        ~dev_source["Document"].isin(inspected["Document"])
    ]

# Loại bỏ các ticket trùng nội dung với tập test_sample
test_sample_file = PROJECT_ROOT / "data" / "test_sample.csv"
test_sample = pd.read_csv(test_sample_file)

dev_source = dev_source[
    ~dev_source["Document"].isin(test_sample["Document"])
]

# Loại bỏ dữ liệu thiếu và ticket trùng nội dung
dev_source = dev_source.dropna(
    subset=["Document", "Topic_group"]
).drop_duplicates(subset=["Document"])

# Lấy ngẫu nhiên 10 ticket cho mỗi nhóm nhãn
# random_state=42 giúp tái lập kết quả khi chạy lại
groups = []

for category in sorted(dev_source["Topic_group"].unique()):
    group = dev_source[
        dev_source["Topic_group"] == category
    ]

    # Kiểm tra mỗi nhóm có đủ số lượng mẫu hay không
    if len(group) < 10:
        raise ValueError(
            f"Không đủ 10 ticket cho nhóm {category}"
        )

    groups.append(
        group.sample(n=10, random_state=42)
    )

# Gộp các nhóm và sắp xếp theo vị trí dòng gốc
dev_sample = pd.concat(groups).sort_values("ticket_id")

# Chỉ giữ các cột cần thiết cho thực nghiệm
dev_sample = dev_sample[
    ["ticket_id", "Document", "Topic_group"]
]

# Lưu tập phát triển vào thư mục results
dev_output = RESULTS_DIR / "llm_dev_sample80.csv"

# Chỉ tạo tập phát triển nếu file chưa tồn tại
if not dev_output.exists():
    dev_sample.to_csv(
        dev_output,
        index=False,
        encoding="utf-8-sig"
    )
    print("Đã tạo tập phát triển 80 ticket.")
else:
    print("Tập phát triển 80 ticket đã tồn tại, không ghi đè.")

# Hiển thị kết quả kiểm tra
print("\nTẬP DỮ LIỆU PHÁT TRIỂN - NGÀY 7")
print("Tổng số ticket:", len(dev_sample))
print(dev_sample["Topic_group"].value_counts())
print("Đã lưu tại:", dev_output)



# ==========================================
# TUẦN 2 - NGÀY 2: TẠO TẬP KIỂM ĐỊNH V4
# ==========================================

# Đọc tập phát triển 80 ticket đã sử dụng
dev_file = RESULTS_DIR / "llm_dev_sample80.csv"
old_dev = pd.read_csv(dev_file)

# Lấy lại dữ liệu train cùng chỉ số dòng gốc
validation_source = df.reset_index().rename(
    columns={"index": "ticket_id"}
)

# Loại những ticket đã sử dụng trong tập phát triển
validation_source = validation_source[
    ~validation_source["ticket_id"].isin(
        old_dev["ticket_id"]
    )
]

# Loại những mẫu HR Support đã xem trước đó
hr_file = RESULTS_DIR / "hr_support_samples.csv"

if hr_file.exists():
    old_hr = pd.read_csv(hr_file)

    validation_source = validation_source[
        ~validation_source["Document"].isin(
            old_hr["Document"]
        )
    ]

# Loại những ticket xuất hiện trong các tập test
for filename in ["test.csv", "test_sample.csv"]:
    test_file = PROJECT_ROOT / "data" / filename

    if test_file.exists():
        test_data = pd.read_csv(test_file)

        validation_source = validation_source[
            ~validation_source["Document"].isin(
                test_data["Document"]
            )
        ]

# Loại dữ liệu thiếu và nội dung trùng nhau
validation_source = validation_source.dropna(
    subset=["Document", "Topic_group"]
).drop_duplicates(subset=["Document"])

# Lấy 20 ticket của mỗi nhóm nhãn
validation_groups = []

for category in sorted(
    validation_source["Topic_group"].unique()
):
    group = validation_source[
        validation_source["Topic_group"] == category
    ]

    if len(group) < 20:
        raise ValueError(
            f"Không đủ 20 ticket cho nhóm {category}"
        )

    validation_groups.append(
        group.sample(
            n=20,
            random_state=2026
        )
    )

# Gộp và sắp xếp dữ liệu
validation_sample = pd.concat(
    validation_groups
).sort_values("ticket_id")

validation_sample = validation_sample[
    ["ticket_id", "Document", "Topic_group"]
]

# Kiểm tra tập kiểm định không trùng tập phát triển cũ
assert len(validation_sample) == 160

assert not set(validation_sample["ticket_id"]) & set(
    old_dev["ticket_id"]
)

# Lưu tập kiểm định mới
validation_output = (
    RESULTS_DIR / "llm_validation_sample160.csv"
)


# Kiểm tra tập kiểm định trước khi lưu
if validation_output.exists():
    # Đọc kết quả đã lưu để đối chiếu với dữ liệu tái tạo
    saved_validation = pd.read_csv(validation_output)

    expected = validation_sample.reset_index(drop=True)
    actual = saved_validation.reset_index(drop=True)

    if not expected.equals(actual):
        raise ValueError(
            "Tập validation160 đã lưu khác với dữ liệu "
            "được tái tạo. Không ghi đè kết quả cũ."
        )

    print(
        "Tập validation160 đã tồn tại và khớp "
        "với dữ liệu tái tạo. Không ghi đè."
    )
else:
    # Chỉ tạo file khi chưa tồn tại
    validation_sample.to_csv(
        validation_output,
        index=False,
        encoding="utf-8-sig"
    )

    print("Đã tạo tập validation160 mới.")

# Hiển thị thống kê tập kiểm định
print("\nTẬP KIỂM ĐỊNH PROMPT")
print("Tổng số ticket:", len(validation_sample))
print(validation_sample["Topic_group"].value_counts())
print("Đường dẫn:", validation_output)
