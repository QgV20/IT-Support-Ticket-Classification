
import argparse
import time
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score

from llm_classifier import classify_ticket as classify_v3
from llm_classifier_v2 import classify_ticket as classify_v2

# Đường dẫn thư mục gốc của project
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"
INPUT_FILE = RESULTS / "llm_dev_sample80.csv"

# Hai phiên bản sử dụng cùng mô hình Qwen2.5:3B
MODEL_NAME = "qwen2.5:3b"

CLASSIFIERS = {
    "v2": classify_v2,
    "v3": classify_v3,
}


def main():
    # Cho phép chọn phiên bản khi chạy bằng Terminal
    parser = argparse.ArgumentParser(
        description="Đánh giá Prompt V2 hoặc V3"
    )

    parser.add_argument(
        "--version",
        choices=["v2", "v3"],
        required=True,
        help="Phiên bản prompt cần đánh giá",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Cho phép ghi đè file kết quả đã tồn tại",
    )

    args = parser.parse_args()

    version = args.version
    classifier = CLASSIFIERS[version]

    # Tạo tên file kết quả tương ứng với phiên bản
    output_file = RESULTS / f"llm_dev_predictions_{version}.csv"

    # Bảo vệ các kết quả đã chạy trước đó
    if output_file.exists() and not args.force:
        print(f"File đã tồn tại: {output_file}")
        print("Sử dụng --force nếu muốn chạy lại và ghi đè.")
        return

    # Đọc tập phát triển cố định
    df = pd.read_csv(INPUT_FILE)

    required = {"ticket_id", "Document", "Topic_group"}

    if not required.issubset(df.columns):
        raise ValueError("Dữ liệu thiếu cột bắt buộc.")

    if len(df) != 80:
        raise ValueError("Tập phát triển phải có 80 ticket.")

    if df["ticket_id"].duplicated().any():
        raise ValueError("Phát hiện ticket_id trùng lặp.")

    print("=" * 50)
    print(f"ĐÁNH GIÁ PROMPT {version.upper()}")
    print("Mô hình:", MODEL_NAME)
    print("Số ticket:", len(df))
    print("=" * 50)

    predictions = []
    statuses = []
    durations = []

    # Phân loại lần lượt từng ticket
    for i, document in enumerate(df["Document"], start=1):
        start = time.perf_counter()

        try:
            prediction = classifier(document)
            status = "success"

        except Exception as error:
            prediction = None
            status = "error"
            print(f"Lỗi ticket {i}: {error}")

        elapsed = time.perf_counter() - start

        predictions.append(prediction)
        statuses.append(status)
        durations.append(round(elapsed, 3))

        print(
            f"[{i}/{len(df)}] {prediction} "
            f"| {status} | {elapsed:.2f}s"
        )

    # Lưu kết quả dự đoán
    df["llm_prediction"] = predictions
    df["llm_status"] = statuses
    df["processing_time_seconds"] = durations

    df.to_csv(
        output_file,
        index=False,
        encoding="utf-8-sig",
    )

    # Tính các chỉ số đánh giá
    y_true = df["Topic_group"].astype(str)
    y_pred = df["llm_prediction"].fillna("__ERROR__")

    labels = sorted(y_true.unique())

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

    print(f"\nKẾT QUẢ PROMPT {version.upper()}")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Macro F1: {macro_f1:.4f}")
    print(f"HR Support Recall: {hr_recall:.4f}")
    print("Dự đoán thành công:", statuses.count("success"))
    print("Đã lưu tại:", output_file)


if __name__ == "__main__":
    main()
