
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score

# Thiết lập đường dẫn của dự án
ROOT = Path(__file__).resolve().parent.parent.parent
RESULTS = ROOT / "results"

FILE_V3 = RESULTS / "llm_validation_predictions_v3.csv"
FILE_V5 = RESULTS / "llm_validation_predictions_v5.csv"

# Đọc hai file kết quả đã lưu
v3 = pd.read_csv(FILE_V3)
v5 = pd.read_csv(FILE_V5)

required = {
    "ticket_id",
    "Document",
    "Topic_group",
    "llm_prediction",
    "llm_status",
}

# Kiểm tra các cột bắt buộc và dữ liệu đầu vào
for version, df in [("V3", v3), ("V5", v5)]:
    if not required.issubset(df.columns):
        raise ValueError(f"{version} thiếu cột bắt buộc.")

    if len(df) != 160:
        raise ValueError(f"{version} không có đủ 160 ticket.")

    if df["ticket_id"].isna().any():
        raise ValueError(f"{version} có ticket_id bị thiếu.")

    if df["ticket_id"].duplicated().any():
        raise ValueError(f"{version} có ticket_id trùng lặp.")

    if df[["Document", "Topic_group"]].isna().any().any():
        raise ValueError(f"{version} có nội dung hoặc nhãn bị thiếu.")

# Ghép dữ liệu theo ticket_id để so sánh chính xác
comparison = v3[
    [
        "ticket_id",
        "Document",
        "Topic_group",
        "llm_prediction",
        "llm_status",
    ]
].merge(
    v5[
        [
            "ticket_id",
            "Document",
            "Topic_group",
            "llm_prediction",
            "llm_status",
        ]
    ],
    on="ticket_id",
    suffixes=("_v3", "_v5"),
    validate="one_to_one",
)

# Bảo đảm hai phiên bản được chạy trên cùng 160 ticket
if len(comparison) != 160:
    raise ValueError("Hai phiên bản không có cùng 160 ticket.")

for column in ["Document", "Topic_group"]:
    if not (
        comparison[f"{column}_v3"]
        == comparison[f"{column}_v5"]
    ).all():
        raise ValueError(f"Dữ liệu {column} không khớp.")

# Giữ một bản nội dung và nhãn thực tế
comparison = comparison.rename(
    columns={
        "Document_v3": "Document",
        "Topic_group_v3": "Topic_group",
    }
).drop(columns=["Document_v5", "Topic_group_v5"])

# Biểu diễn lỗi xử lý bằng nhãn riêng khi đánh giá
for version in ["v3", "v5"]:
    comparison[f"prediction_{version}"] = (
        comparison[f"llm_prediction_{version}"]
        .fillna("__ERROR__")
    )

    comparison[f"correct_{version}"] = (
        comparison["Topic_group"]
        == comparison[f"prediction_{version}"]
    )

# Xác định các trường hợp thay đổi giữa hai prompt
comparison["changed"] = (
    comparison["prediction_v3"]
    != comparison["prediction_v5"]
)

improved = comparison[
    (~comparison["correct_v3"]) &
    comparison["correct_v5"]
].copy()

regressed = comparison[
    comparison["correct_v3"] &
    (~comparison["correct_v5"])
].copy()

both_correct = comparison[
    comparison["correct_v3"] &
    comparison["correct_v5"]
].copy()

both_wrong = comparison[
    (~comparison["correct_v3"]) &
    (~comparison["correct_v5"])
].copy()

# Tính các chỉ số tổng thể và Recall theo nhãn
labels = sorted(comparison["Topic_group"].unique())
y_true = comparison["Topic_group"]

print("=" * 60)
print("SO SÁNH CHI TIẾT PROMPT V3 VÀ V5")
print("=" * 60)

for version in ["v3", "v5"]:
    y_pred = comparison[f"prediction_{version}"]

    accuracy = accuracy_score(y_true, y_pred)

    macro_f1 = f1_score(
        y_true,
        y_pred,
        labels=labels,
        average="macro",
        zero_division=0,
    )

    admin_recall = recall_score(
        y_true,
        y_pred,
        labels=["Administrative rights"],
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
    print(f"Administrative rights Recall: {admin_recall:.4f}")
    print(f"HR Support Recall: {hr_recall:.4f}")

print("\nTHỐNG KÊ THAY ĐỔI")
print("Dự đoán khác nhau:", int(comparison["changed"].sum()))
print("Cả hai đúng:", len(both_correct))
print("Cả hai sai:", len(both_wrong))
print("V5 sửa đúng so với V3:", len(improved))
print("V5 làm sai so với V3:", len(regressed))

# Thống kê các nhóm nhãn thay đổi số dự đoán đúng
label_rows = []

for label, group in comparison.groupby("Topic_group"):
    correct_v3 = int(group["correct_v3"].sum())
    correct_v5 = int(group["correct_v5"].sum())

    label_rows.append({
        "Category": label,
        "Total": len(group),
        "Correct_V3": correct_v3,
        "Correct_V5": correct_v5,
        "Recall_V3": round(correct_v3 / len(group), 4),
        "Recall_V5": round(correct_v5 / len(group), 4),
        "Net_change": correct_v5 - correct_v3,
    })

label_summary = pd.DataFrame(label_rows)

print("\nTHAY ĐỔI THEO TỪNG NHÃN")
print(label_summary.to_string(index=False))

# Xuất các file phân tích riêng
comparison.to_csv(
    RESULTS / "llm_v3_v5_comparison.csv",
    index=False,
    encoding="utf-8-sig",
)

improved.to_csv(
    RESULTS / "llm_v5_improved_cases.csv",
    index=False,
    encoding="utf-8-sig",
)

regressed.to_csv(
    RESULTS / "llm_v5_regressed_cases.csv",
    index=False,
    encoding="utf-8-sig",
)

label_summary.to_csv(
    RESULTS / "llm_experiments" / "analysis" / "llm_v3_v5_label_summary.csv",
    index=False,
    encoding="utf-8-sig",
)

print("\nĐã lưu kết quả vào thư mục results/")
