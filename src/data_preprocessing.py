from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = 42
MIN_WORDS = 3
LLM_SAMPLE_SIZE = 400

def load_clean():
    df = pd.read_csv(DATA / "all_tickets_processed_improved_v3.csv")
    df = df.dropna(subset=["Document", "Topic_group"])
    df["Document"] = df["Document"].str.strip()
    df = df.drop_duplicates(subset="Document")
    df = df[df["Document"].str.split().str.len() >= MIN_WORDS]
    return df.reset_index(drop=True)

def split_and_save():
    df = load_clean()
    train, test = train_test_split(
        df, test_size=0.2, stratify=df["Topic_group"], random_state=SEED)
    # Mẫu nhỏ để chạy LLM, lấy từ tập test, giữ nguyên tỷ lệ nhãn
    sample, _ = train_test_split(
        test, train_size=LLM_SAMPLE_SIZE, stratify=test["Topic_group"], random_state=SEED)
    train.to_csv(DATA / "train.csv", index=False)
    test.to_csv(DATA / "test.csv", index=False)
    sample.to_csv(DATA / "test_sample.csv", index=False)
    print(f"train={len(train)}, test={len(test)}, test_sample={len(sample)}")

if __name__ == "__main__":
    split_and_save()