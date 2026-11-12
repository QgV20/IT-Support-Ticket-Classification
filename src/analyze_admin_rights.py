
from pathlib import Path

import pandas as pd

# Thiết lập đường dẫn
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

VERSIONS = ["v2", "v3", "v4"]
TARGET_LABEL = "Administrative rights"

frames = {}

# Đọc và kiểm tra kết quả từng phiên bản
for version in VERSIONS:
    file_path = (
        RESULTS / f"llm_validation_predictions_{version}.csv"
    )

    df = pd.read_csv(file_path)

    required = {
        "ticket_id",
        "Document",
        "Topic_group",
        "llm_prediction",
        "llm_status",
    }

    if not required.issubset(df.columns):
        raise ValueError(
            f"File {version} thiếu cột bắt buộc."
        )

    if len(df) != 160 or df["ticket_id"].duplicated().any():
        raise ValueError(
            f"Dữ liệu {version} không hợp lệ."
        )

    frames[version] = df.set_index("ticket_id").sort_index()

# Kiểm tra ba phiên bản sử dụng cùng tập ticket
reference = frames["v2"]

for version in ["v3", "v4"]:
    other = frames[version]

    if not reference.index.equals(other.index):
        raise ValueError("ticket_id không khớp.")

    for column in ["Document", "Topic_group"]:
        if not reference[column].equals(other[column]):
            raise ValueError(
                f"Dữ liệu {column} không khớp."
            )

# Lấy 20 ticket Administrative rights
admin = reference[
    reference["Topic_group"] == TARGET_LABEL
][["Document", "Topic_group"]].copy()

if len(admin) != 20:
    raise ValueError(
        "Số ticket Administrative rights phải bằng 20."
    )

# Ghép dự đoán và trạng thái từng phiên bản
for version in VERSIONS:
    admin[f"prediction_{version}"] = (
        frames[version]
        .loc[admin.index, "llm_prediction"]
        .fillna("__ERROR__")
    )

    admin[f"status_{version}"] = (
        frames[version]
        .loc[admin.index, "llm_status"]
    )

    admin[f"correct_{version}"] = (
        admin[f"prediction_{version}"]
        == TARGET_LABEL
    )

# Phân tích sự khác biệt giữa các phiên bản
admin["v3_v4_changed"] = (
    admin["prediction_v3"] != admin["prediction_v4"]
)

print("=" * 60)
print("PHÂN TÍCH ADMINISTRATIVE RIGHTS")
print("=" * 60)

print("\nTổng số ticket:", len(admin))

# Thống kê phân bố nhãn dự đoán
for version in VERSIONS:
    print(f"\nDỰ ĐOÁN CỦA PROMPT {version.upper()}")

    counts = admin[
        f"prediction_{version}"
    ].value_counts(dropna=False)

    print(counts.to_string())

    print(
        "Số dự đoán đúng:",
        int(admin[f"correct_{version}"].sum())
    )

    print(
        "Số xử lý lỗi:",
        int((admin[f"status_{version}"] != "success").sum())
    )

print("\nV3 VÀ V4 DỰ ĐOÁN KHÁC NHAU:")
print(int(admin["v3_v4_changed"].sum()))

# Xuất bảng chi tiết để đọc từng ticket
admin_output = (
    RESULTS / "llm_admin_rights_analysis.csv"
)

admin.reset_index().to_csv(
    admin_output,
    index=False,
    encoding="utf-8-sig",
)

# Lưu bảng tổng hợp phân bố dự đoán
summary_rows = []

for version in VERSIONS:
    counts = admin[
        f"prediction_{version}"
    ].value_counts(dropna=False)

    for predicted, count in counts.items():
        summary_rows.append({
            "Version": version.upper(),
            "Actual": TARGET_LABEL,
            "Predicted": predicted,
            "Count": int(count),
        })

summary = pd.DataFrame(summary_rows)

summary.to_csv(
    RESULTS / "llm_experiments" / "analysis" / "llm_admin_rights_summary.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nĐã lưu:")
print(admin_output)
print(RESULTS / "llm_experiments" / "analysis" / "llm_admin_rights_summary.csv")
