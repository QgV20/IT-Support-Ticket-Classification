
from pathlib import Path

import pandas as pd


# Thiết lập đường dẫn của dự án
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

BASELINE_FILE = RESULTS / "baseline_predictions_400.csv"
LLM_FILE = RESULTS / "llm_final_predictions_v3_400.csv"

OUTPUT_FILE = RESULTS / "baseline_llm_comparison_400.csv"


def main():
    """So sánh dự đoán Baseline và LLM trên 400 ticket."""

    # Không ghi đè kết quả đã tồn tại
    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"File kết quả đã tồn tại: {OUTPUT_FILE}"
        )

    baseline = pd.read_csv(BASELINE_FILE)
    llm = pd.read_csv(LLM_FILE)

    required_baseline = {
        "Document", "Topic_group", "baseline_prediction"
    }
    required_llm = {
        "Document", "Topic_group",
        "llm_prediction", "llm_status"
    }

    if not required_baseline.issubset(baseline.columns):
        raise ValueError("File baseline thiếu cột bắt buộc.")

    if not required_llm.issubset(llm.columns):
        raise ValueError("File LLM thiếu cột bắt buộc.")

    if len(baseline) != 400 or len(llm) != 400:
        raise ValueError("Hai file phải có đúng 400 ticket.")

    # Đảm bảo hai file có cùng ticket theo đúng thứ tự
    original_columns = ["Document", "Topic_group"]

    if not baseline[original_columns].equals(
        llm[original_columns]
    ):
        raise ValueError(
            "Hai file không khớp nội dung hoặc thứ tự."
        )

    # Ticket LLM gặp lỗi được tính là dự đoán sai
    llm_predictions = llm["llm_prediction"].fillna("__ERROR__")

    # Tạo bảng kết quả chung, không sao chép nội dung ticket
    result = pd.DataFrame({
        "row_id": range(1, 401),
        "Topic_group": baseline["Topic_group"],
        "baseline_prediction": baseline["baseline_prediction"],
        "llm_prediction": llm_predictions,
        "llm_status": llm["llm_status"],
    })

    result["baseline_correct"] = (
        result["Topic_group"] == result["baseline_prediction"]
    )

    result["llm_correct"] = (
        result["Topic_group"] == result["llm_prediction"]
    )

    # Phân nhóm trường hợp dự đoán
    def classify_case(row):
        if row["baseline_correct"] and row["llm_correct"]:
            return "both_correct"
        if row["baseline_correct"]:
            return "baseline_only"
        if row["llm_correct"]:
            return "llm_only"
        return "both_wrong"

    result["comparison_case"] = result.apply(
        classify_case, axis=1
    )

    counts = result["comparison_case"].value_counts()

    # Kiểm tra tính nhất quán với kết quả đã xác minh
    if result["baseline_correct"].sum() != 343:
        raise ValueError("Baseline không khớp 343/400.")

    if result["llm_correct"].sum() != 164:
        raise ValueError("LLM không khớp 164/400.")

    print("=" * 55)
    print("SO SANH BASELINE VA LLM - TEST400")
    print("=" * 55)

    for case in [
        "both_correct",
        "baseline_only",
        "llm_only",
        "both_wrong",
    ]:
        print(f"{case}: {counts.get(case, 0)}")

    print("\nTICKET CHI LLM DU DOAN DUNG")

    llm_only = result[
        result["comparison_case"] == "llm_only"
    ]

    print(
        llm_only[
            [
                "row_id",
                "Topic_group",
                "baseline_prediction",
                "llm_prediction",
            ]
        ].to_string(index=False)
    )

    # Lưu đúng một file tổng hợp phục vụ phân tích
    result.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print("\nSaved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
