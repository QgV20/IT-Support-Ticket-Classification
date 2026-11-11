
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import classification_report


# Thiết lập đường dẫn dự án
ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results"

INPUT_FILE = RESULTS / "llm_final_predictions_v3_400.csv"
OUTPUT_FILE = RESULTS / "llm_confusion_final_v3_400.png"

LABELS = [
    "Access",
    "Administrative rights",
    "HR Support",
    "Hardware",
    "Internal Project",
    "Miscellaneous",
    "Purchase",
    "Storage",
]

ERROR_LABEL = "__ERROR__"


def main():
    """Phân tích Confusion Matrix của Prompt V3 trên test400."""

    # Không ghi đè biểu đồ đã tạo trước đó
    if OUTPUT_FILE.exists():
        raise FileExistsError(
            f"Biểu đồ đã tồn tại: {OUTPUT_FILE}"
        )

    df = pd.read_csv(INPUT_FILE)

    # Kiểm tra dữ liệu đầu vào
    required = {
        "Topic_group",
        "llm_prediction",
        "llm_status",
    }

    if not required.issubset(df.columns):
        raise ValueError("File kết quả thiếu cột bắt buộc.")

    if len(df) != 400:
        raise ValueError("Tập kết quả phải có đúng 400 ticket.")

    true_labels = df["Topic_group"]
    predicted_labels = df["llm_prediction"].fillna(ERROR_LABEL)

    if not true_labels.isin(LABELS).all():
        raise ValueError("Nhãn thực tế không hợp lệ.")

    if not predicted_labels.isin(
        LABELS + [ERROR_LABEL]
    ).all():
        raise ValueError("Nhãn dự đoán không hợp lệ.")

    # Tạo ma trận với 8 hàng nhãn thật và 9 cột dự đoán
    # Cột thứ chín ghi nhận các dự đoán bị lỗi
    matrix = pd.crosstab(
        pd.Categorical(true_labels, categories=LABELS),
        pd.Categorical(
            predicted_labels,
            categories=LABELS + [ERROR_LABEL],
        ),
        dropna=False,
    )

    if int(matrix.to_numpy().sum()) != 400:
        raise ValueError("Confusion Matrix không đủ 400 ticket.")

    print("=" * 60)
    print("LLM V3 - CONFUSION MATRIX - TEST400")
    print("=" * 60)

    print("\nCONFUSION MATRIX")
    print(matrix.to_string())

    print("\nCLASSIFICATION REPORT")
    print(
        classification_report(
            true_labels,
            predicted_labels,
            labels=LABELS,
            zero_division=0,
            digits=3,
        )
    )

    # Chỉ lấy những dự đoán sai để tìm cặp nhãn phổ biến
    errors = df.loc[
        true_labels != predicted_labels
    ].copy()

    errors["predicted_label"] = predicted_labels.loc[
        errors.index
    ]

    confusion_pairs = (
        errors.groupby(
            ["Topic_group", "predicted_label"]
        )
        .size()
        .sort_values(ascending=False)
    )

    print("\nTOP 12 CAP NHAN NHAM LAN")
    print(confusion_pairs.head(12).to_string())

    # Hiển thị đầy đủ 8 nhãn thật và 9 nhãn dự đoán
    fig, ax = plt.subplots(figsize=(13, 8))

    values = matrix.to_numpy()

    image = ax.imshow(values, cmap="Blues")

    ax.set_xticks(np.arange(len(matrix.columns)))
    ax.set_yticks(np.arange(len(matrix.index)))

    ax.set_xticklabels(
        matrix.columns,
        rotation=45,
        ha="right",
    )
    ax.set_yticklabels(matrix.index)

    ax.set_xlabel("Predicted label")
    ax.set_ylabel("True label")
    ax.set_title("Qwen2.5:3B Zero-shot V3 - Test400")

    # Ghi số lượng ticket lên từng ô
    threshold = values.max() / 2

    for i in range(values.shape[0]):
        for j in range(values.shape[1]):
            value = int(values[i, j])

            ax.text(
                j,
                i,
                str(value),
                ha="center",
                va="center",
                color=(
                    "white"
                    if value > threshold
                    else "black"
                ),
                fontsize=9,
            )

    fig.colorbar(image, ax=ax, label="Ticket count")
    fig.tight_layout()

    # Chỉ lưu một biểu đồ mới
    fig.savefig(
        OUTPUT_FILE,
        dpi=150,
        bbox_inches="tight",
    )

    plt.close(fig)

    print("\nSaved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
