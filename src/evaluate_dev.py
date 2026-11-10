
import argparse
import time
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, recall_score

from llm_classifier_v2 import classify_ticket as classify_v2
from llm_classifier import classify_ticket as classify_v3
from llm_classifier_v4 import classify_ticket as classify_v4
from llm_classifier_v5 import classify_ticket as classify_v5

# Thiết lập đường dẫn của dự án
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

MODEL_NAME = "qwen2.5:3b"

CLASSIFIERS = {
    "v2": classify_v2,
    "v3": classify_v3,
    "v4": classify_v4,
    "v5": classify_v5,
}

DATASETS = {
    "dev80": RESULTS / "llm_dev_sample80.csv",
    "validation160": RESULTS / "llm_validation_sample160.csv",
}

EXPECTED_SIZES = {
    "dev80": 80,
    "validation160": 160,
}


def main():
    # Đọc các tham số từ Terminal
    parser = argparse.ArgumentParser(
        description="Đánh giá các phiên bản Prompt V2, V3, V4 và V5"
    )

    parser.add_argument(
        "--version",
        choices=["v2", "v3", "v4", "v5"],
        required=True,
        help="Phiên bản prompt cần đánh giá",
    )

    parser.add_argument(
        "--dataset",
        choices=["dev80", "validation160"],
        required=True,
        help="Tập dữ liệu dùng để đánh giá",
    )

    parser.add_argument(
        "--force",
        action="store_true",
        help="Cho phép ghi đè kết quả đã tồn tại",
    )

    args = parser.parse_args()

    version = args.version
    dataset = args.dataset

    classifier = CLASSIFIERS[version]
    input_file = DATASETS[dataset]

    # Giữ nguyên quy ước tên file của Tuần 1
    if dataset == "dev80":
        output_file = (
            RESULTS / f"llm_dev_predictions_{version}.csv"
        )
    else:
        output_file = (
            RESULTS / f"llm_validation_predictions_{version}.csv"
        )

    # Không ghi đè những kết quả đã được lưu
    if output_file.exists() and not args.force:
        print(f"File kết quả đã tồn tại: {output_file}")
        print("Không ghi đè. Dùng --force nếu muốn chạy lại.")
        return

    # Đọc và kiểm tra dữ liệu
    df = pd.read_csv(input_file)

    required_columns = {
        "ticket_id",
        "Document",
        "Topic_group",
    }

    if not required_columns.issubset(df.columns):
        raise ValueError("Tập dữ liệu thiếu cột bắt buộc.")

    if len(df) != EXPECTED_SIZES[dataset]:
        raise ValueError("Số lượng ticket không đúng.")

    if df["ticket_id"].duplicated().any():
        raise ValueError("Phát hiện ticket_id trùng lặp.")

    if df[list(required_columns)].isna().any().any():
        raise ValueError("Tập dữ liệu có giá trị thiếu.")

    if df["Document"].duplicated().any():
        raise ValueError("Phát hiện nội dung ticket trùng lặp.")

    if df["Topic_group"].nunique() != 8:
        raise ValueError("Tập dữ liệu phải có 8 nhóm nhãn.")

    if not (
        df["Topic_group"].value_counts()
        == EXPECTED_SIZES[dataset] // 8
    ).all():
        raise ValueError("Phân bố nhãn không cân bằng.")

    print("=" * 55)
    print(f"ĐÁNH GIÁ PROMPT {version.upper()}")
    print("Mô hình:", MODEL_NAME)
    print("Tập dữ liệu:", dataset)
    print("Số ticket:", len(df))
    print("=" * 55)

    predictions = []
    statuses = []
    durations = []

    # Phân loại từng ticket bằng phiên bản đã chọn
    for i, document in enumerate(df["Document"], start=1):
        start = time.perf_counter()

        try:
            prediction = classifier(str(document))
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

    # Lưu dự đoán của từng ticket
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
    print("File kết quả:", output_file)


if __name__ == "__main__":
    main()
