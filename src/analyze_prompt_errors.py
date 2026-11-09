
from pathlib import Path

import pandas as pd

# Đường dẫn thư mục gốc và thư mục kết quả
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

# Đọc bảng so sánh Prompt V2 và V3
INPUT_FILE = RESULTS / "llm_comparison_v2_v3.csv"

df = pd.read_csv(INPUT_FILE)

# Kiểm tra các cột cần thiết
required_columns = {
    "ticket_id",
    "Document",
    "Topic_group",
    "llm_prediction_v2",
    "llm_prediction_v3",
}

if not required_columns.issubset(df.columns):
    raise ValueError("File so sánh thiếu cột bắt buộc.")

if len(df) != 80 or df["ticket_id"].duplicated().any():
    raise ValueError("Tập so sánh không hợp lệ.")

print("=" * 55)
print("PHÂN TÍCH LỖI PHÂN LOẠI LLM")
print("=" * 55)

# Xác định kết quả đúng/sai của hai phiên bản
df["correct_v2"] = (
    df["Topic_group"] == df["llm_prediction_v2"]
)

df["correct_v3"] = (
    df["Topic_group"] == df["llm_prediction_v3"]
)

# Chia các ticket theo kết quả thay đổi
improved = df[
    (~df["correct_v2"]) & df["correct_v3"]
].copy()

regressed = df[
    df["correct_v2"] & (~df["correct_v3"])
].copy()

both_wrong = df[
    (~df["correct_v2"]) & (~df["correct_v3"])
].copy()

# Tổng hợp các cặp nhãn bị nhầm lẫn
confusions = []

for version in ["v2", "v3"]:
    prediction_col = f"llm_prediction_{version}"

    wrong = df[
        df["Topic_group"] != df[prediction_col]
    ]

    counts = (
        wrong.groupby(
            ["Topic_group", prediction_col],
            dropna=False
        )
        .size()
        .reset_index(name="Count")
    )

    counts["Version"] = version.upper()

    counts = counts.rename(
        columns={
            "Topic_group": "Actual",
            prediction_col: "Predicted",
        }
    )

    confusions.append(counts)

confusion_df = pd.concat(
    confusions,
    ignore_index=True
)

confusion_df = confusion_df[
    ["Version", "Actual", "Predicted", "Count"]
].sort_values(
    ["Version", "Count"],
    ascending=[True, False]
)

# Xuất dữ liệu phục vụ phân tích
improved.to_csv(
    RESULTS / "llm_improved_cases.csv",
    index=False,
    encoding="utf-8-sig",
)

regressed.to_csv(
    RESULTS / "llm_regressed_cases.csv",
    index=False,
    encoding="utf-8-sig",
)

both_wrong.to_csv(
    RESULTS / "llm_both_wrong_cases.csv",
    index=False,
    encoding="utf-8-sig",
)

confusion_df.to_csv(
    RESULTS / "llm_confusion_pairs.csv",
    index=False,
    encoding="utf-8-sig",
)

# Hiển thị thống kê
print("\nTỔNG QUAN")
print("Tổng số ticket:", len(df))
print("V3 sửa đúng:", len(improved))
print("V3 làm sai:", len(regressed))
print("Cả hai cùng sai:", len(both_wrong))

print("\nCÁC NHÓM NHẦM LẪN NHIỀU NHẤT")
for version in ["V2", "V3"]:
    print(f"\nPrompt {version}:")

    subset = confusion_df[
        confusion_df["Version"] == version
    ]

    print(subset.head(10).to_string(index=False))

print("\nĐÃ HOÀN THÀNH PHÂN TÍCH")
print("Kết quả được lưu trong results/")
