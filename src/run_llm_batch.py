
from pathlib import Path
import sys
import time

import pandas as pd

# Import classifier from the same src directory
from llm_classifier import classify_ticket, MODEL_NAME


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = PROJECT_ROOT / "data" / "test_sample.csv"
OUTPUT_DIR = PROJECT_ROOT / "results"
OUTPUT_FILE = OUTPUT_DIR / "llm_predictions.csv"

# Số ticket xử lý trong một lần chạy
MAX_TICKETS = 10


def main():
    if not INPUT_FILE.exists():
        print(f"Dataset not found: {INPUT_FILE}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_FILE)

    print("Dataset columns:", df.columns.tolist())
    print("Total tickets:", len(df))

    if "Document" not in df.columns:
        raise ValueError(
            "Required column 'Document' not found."
        )

    if "Topic_group" not in df.columns:
        print(
            "Warning: Topic_group not found. "
            "Predictions can run, but labels cannot be evaluated."
        )

    # Keep the original rows and columns
    df = df.head(MAX_TICKETS).copy()

    predictions = []
    statuses = []
    processing_times = []

    print("=" * 50)
    print("LLM BATCH CLASSIFICATION")
    print("Model:", MODEL_NAME)
    print("Number of tickets:", len(df))
    print("=" * 50)

    for index, document in enumerate(df["Document"], start=1):
        start_time = time.perf_counter()

        try:
            prediction = classify_ticket(document)
            status = "success"

        except Exception as error:
            prediction = None
            status = f"error: {type(error).__name__}"
            print(f"Error on ticket {index}: {error}")

        elapsed = time.perf_counter() - start_time

        predictions.append(prediction)
        statuses.append(status)
        processing_times.append(round(elapsed, 3))

        print(
            f"[{index}/{len(df)}] "
            f"Prediction: {prediction} | "
            f"Status: {status} | "
            f"Time: {elapsed:.2f}s"
        )

    df["llm_prediction"] = predictions
    df["llm_status"] = statuses
    df["processing_time_seconds"] = processing_times

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig",
    )

    print("\nClassification completed.")
    print("Successful predictions:",
          sum(status == "success" for status in statuses))
    print("Total tickets:", len(df))
    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
