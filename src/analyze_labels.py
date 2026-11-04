
from pathlib import Path
import pandas as pd

# Duong dan project
PROJECT_ROOT = Path(__file__).resolve().parent.parent
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

dev_sample.to_csv(
    dev_output,
    index=False,
    encoding="utf-8-sig"
)

# Hiển thị kết quả kiểm tra
print("\nTẬP DỮ LIỆU PHÁT TRIỂN - NGÀY 7")
print("Tổng số ticket:", len(dev_sample))
print(dev_sample["Topic_group"].value_counts())
print("Đã lưu tại:", dev_output)
