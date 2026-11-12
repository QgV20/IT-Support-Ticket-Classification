
from pathlib import Path

import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    recall_score,
)

# Thiết lập đường dẫn
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

FILE_V2 = RESULTS / "llm_dev_predictions_v2.csv"
FILE_V3 = RESULTS / "llm_dev_predictions_v3.csv"

# Đọc kết quả hai phiên bản
v2 = pd.read_csv(FILE_V2)
v3 = pd.read_csv(FILE_V3)

required = {
    "ticket_id", "Document", "Topic_group",
    "llm_prediction"
}

for name, data in [("V2", v2), ("V3", v3)]:
    if not required.issubset(data.columns):
        raise ValueError(f"File {name} thiếu cột.")

    if len(data) != 80 or data["ticket_id"].duplicated().any():
        raise ValueError(f"Dữ liệu {name} không hợp lệ.")

# Ghép kết quả theo ID của từng ticket
comparison = v2[
    ["ticket_id", "Document", "Topic_group", "llm_prediction"]
].merge(
    v3[
        ["ticket_id", "Document", "Topic_group", "llm_prediction"]
    ],
    on="ticket_id",
    suffixes=("_v2", "_v3"),
    validate="one_to_one",
)

# Kiểm tra hai mô hình dùng đúng cùng dữ liệu
if len(comparison) != 80:
    raise ValueError("Hai phiên bản không có cùng 80 ticket.")

for column in ["Document", "Topic_group"]:
    if not (
        comparison[f"{column}_v2"]
        == comparison[f"{column}_v3"]
    ).all():
        raise ValueError(f"Dữ liệu {column} không khớp.")

# Chuẩn hóa tên cột
comparison = comparison.rename(
    columns={
        "Document_v2": "Document",
        "Topic_group_v2": "Topic_group",
    }
).drop(columns=["Document_v3", "Topic_group_v3"])

# Tính đúng/sai cho từng phiên bản
comparison["correct_v2"] = (
    comparison["Topic_group"]
    == comparison["llm_prediction_v2"]
)

comparison["correct_v3"] = (
    comparison["Topic_group"]
    == comparison["llm_prediction_v3"]
)

# Thống kê số ticket cải thiện và suy giảm
improved = (
    (~comparison["correct_v2"]) &
    comparison["correct_v3"]
).sum()

regressed = (
    comparison["correct_v2"] &
    (~comparison["correct_v3"])
).sum()

both_correct = (
    comparison["correct_v2"] &
    comparison["correct_v3"]
).sum()

both_wrong = (
    (~comparison["correct_v2"]) &
    (~comparison["correct_v3"])
).sum()

# Tính chỉ số đánh giá
labels = sorted(comparison["Topic_group"].unique())
y_true = comparison["Topic_group"]

print("=" * 55)
print("SO SÁNH PROMPT V2 VÀ V3")
print("=" * 55)

for version in ["v2", "v3"]:
    y_pred = comparison[
        f"llm_prediction_{version}"
    ].fillna("__ERROR__")

    accuracy = accuracy_score(y_true, y_pred)

    macro_f1 = f1_score(
        y_true,
        y_pred,
        labels=labels,
        average="macro",
        zero_division=0,
    )

    hr_recall = recall_score(
        y_true,
        y_pred,
        labels=["HR Support"],
        average="macro",
        zero_division=0,
    )

    print(f"\nPROMPT {version.upper()}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")
    print(f"HR Support Recall: {hr_recall:.4f}")

print("\nPHÂN TÍCH SỰ THAY ĐỔI")
print("Cả hai đúng:", both_correct)
print("Cả hai sai:", both_wrong)
print("V2 sai, V3 đúng:", improved)
print("V2 đúng, V3 sai:", regressed)

# Thống kê Recall của từng nhãn
rows = []

for label in labels:
    subset = comparison[
        comparison["Topic_group"] == label
    ]

    rows.append({
        "Category": label,
        "Total": len(subset),
        "Correct_V2": int(subset["correct_v2"].sum()),
        "Correct_V3": int(subset["correct_v3"].sum()),
        "Recall_V2": round(subset["correct_v2"].mean(), 4),
        "Recall_V3": round(subset["correct_v3"].mean(), 4),
    })

label_results = pd.DataFrame(rows)

print("\nRECALL THEO TỪNG NHÃN")
print(label_results.to_string(index=False))

# Lưu kết quả so sánh
comparison.to_csv(
    RESULTS / "llm_comparison_v2_v3.csv",
    index=False,
    encoding="utf-8-sig",
)

label_results.to_csv(
    RESULTS / "llm_experiments" / "analysis" / "llm_recall_by_label.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nĐã lưu kết quả so sánh vào results/")
