
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score


ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"

MODEL_FILE = RESULTS / "baseline_tfidf_lr.joblib"
TEST_FILE = DATA / "test_sample.csv"
OUTPUT_FILE = RESULTS / "baseline_predictions_400.csv"


def main():
    """Xuất dự đoán từ mô hình baseline đã huấn luyện."""

    # Bảo vệ kết quả đã lưu
    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"File đã tồn tại: {OUTPUT_FILE}"
        )

    if not MODEL_FILE.exists():
        raise FileNotFoundError(
            f"Không tìm thấy mô hình: {MODEL_FILE}"
        )

    # Đọc đúng tập dữ liệu đã dùng để đánh giá LLM
    test = pd.read_csv(TEST_FILE)

    if len(test) != 400:
        raise ValueError("Tập kiểm thử phải có 400 ticket.")

    if test[["Document", "Topic_group"]].isna().any().any():
        raise ValueError("Dữ liệu kiểm thử có giá trị thiếu.")

    # Chỉ tải mô hình từ nguồn đáng tin cậy của nhóm
    model = joblib.load(MODEL_FILE)
    predictions = model.predict(test["Document"])

    accuracy = accuracy_score(
        test["Topic_group"], predictions
    )
    macro_f1 = f1_score(
        test["Topic_group"],
        predictions,
        average="macro",
    )

    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")

    # Chỉ lưu nếu mô hình khớp báo cáo chính thức
    if (
        round(accuracy, 4) != 0.8575
        or round(macro_f1, 4) != 0.8611
    ):
        raise ValueError(
            "Mô hình không khớp kết quả baseline gốc."
        )

    result = test[["Document", "Topic_group"]].copy()
    result["baseline_prediction"] = predictions
    result["baseline_correct"] = (
        result["Topic_group"]
        == result["baseline_prediction"]
    )

    result.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print("Correct:", int(result["baseline_correct"].sum()))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
