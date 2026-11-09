
from pathlib import Path

import pandas as pd
from sklearn.metrics import f1_score

# Thiết lập đường dẫn kết quả
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

versions = ["v2", "v3", "v4"]
frames = {}

# Đọc và kiểm tra kết quả từng phiên bản
for version in versions:
    path = RESULTS / f"llm_validation_predictions_{version}.csv"
    df = pd.read_csv(path)

    required = {
        "ticket_id",
        "Document",
        "Topic_group",
        "llm_prediction",
        "llm_status",
    }

    if not required.issubset(df.columns):
        raise ValueError(f"{version} thiếu cột dữ liệu.")

    if len(df) != 160 or df["ticket_id"].duplicated().any():
        raise ValueError(f"{version} có dữ liệu không hợp lệ.")

    frames[version] = df.set_index("ticket_id").sort_index()

# Đảm bảo ba phiên bản được đánh giá trên cùng ticket
reference = frames["v2"]

for version in ["v3", "v4"]:
    other = frames[version]

    if not reference.index.equals(other.index):
        raise ValueError("Danh sách ticket_id không khớp.")

    for column in ["Document", "Topic_group"]:
        if not reference[column].equals(other[column]):
            raise ValueError(f"Nội dung {column} không khớp.")

# Đối chiếu dự đoán theo từng ticket
comparison = reference[
    ["Document", "Topic_group"]
].copy()

for version in versions:
    comparison[f"prediction_{version}"] = (
        frames[version]["llm_prediction"].fillna("__ERROR__")
    )

    comparison[f"correct_{version}"] = (
        comparison["Topic_group"]
        == comparison[f"prediction_{version}"]
    )

# Tính thay đổi giữa V3 và V4
changed = (
    comparison["prediction_v3"]
    != comparison["prediction_v4"]
)

improved = (
    (~comparison["correct_v3"])
    & comparison["correct_v4"]
)

regressed = (
    comparison["correct_v3"]
    & (~comparison["correct_v4"])
)

print("=" * 55)
print("SO SÁNH KẾT QUẢ VALIDATION 160")
print("=" * 55)

print("V3 và V4 dự đoán khác nhau:", int(changed.sum()))
print("V4 sửa đúng so với V3:", int(improved.sum()))
print("V4 làm sai so với V3:", int(regressed.sum()))

# So sánh Recall của từng nhãn
rows = []

for category, group in comparison.groupby("Topic_group"):
    row = {"Category": category, "Total": len(group)}

    for version in versions:
        row[f"Recall_{version.upper()}"] = round(
            group[f"correct_{version}"].mean(), 4
        )

    rows.append(row)

recall_df = pd.DataFrame(rows)

print("\nRECALL THEO TỪNG NHÃN")
print(recall_df.to_string(index=False))

# So sánh Macro F1 để xác nhận số liệu
y_true = comparison["Topic_group"]
labels = sorted(y_true.unique())

print("\nMACRO F1 KIỂM TRA")

for version in versions:
    score = f1_score(
        y_true,
        comparison[f"prediction_{version}"],
        labels=labels,
        average="macro",
        zero_division=0,
    )
    print(f"{version.upper()}: {score:.4f}")

# Lưu các kết quả phục vụ báo cáo
comparison.reset_index().to_csv(
    RESULTS / "llm_validation_comparison.csv",
    index=False,
    encoding="utf-8-sig",
)

recall_df.to_csv(
    RESULTS / "llm_validation_recall_by_label.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nĐã lưu kết quả vào results/")
