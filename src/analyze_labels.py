
from pathlib import Path
import pandas as pd

# Duong dan project
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_ROOT / "data" / "train.csv"
RESULTS_DIR = PROJECT_ROOT / "results"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

# Doc du lieu
df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")

required_columns = {"Document", "Topic_group"}
missing = required_columns - set(df.columns)

if missing:
    raise ValueError(f"Missing columns: {missing}")

print("=" * 55)
print("TRAIN DATASET ANALYSIS")
print("=" * 55)

print(f"\nTotal tickets: {len(df)}")
print(f"Missing documents: {df['Document'].isna().sum()}")
print(f"Missing labels: {df['Topic_group'].isna().sum()}")

# Chuan hoa cot nhan de thong ke
df["Topic_group"] = df["Topic_group"].astype("string").str.strip()

# Phan bo nhan
distribution = (
    df["Topic_group"]
    .value_counts(dropna=False)
    .rename_axis("Category")
    .reset_index(name="Count")
)

distribution["Percentage"] = (
    distribution["Count"] / len(df) * 100
).round(2)

print("\nCATEGORY DISTRIBUTION")
print(distribution.to_string(index=False))

distribution.to_csv(
    RESULTS_DIR / "label_distribution.csv",
    index=False,
    encoding="utf-8-sig"
)

# Phan tich do dai ticket
df["word_count"] = (
    df["Document"]
    .fillna("")
    .astype(str)
    .str.split()
    .str.len()
)

length_stats = (
    df.groupby("Topic_group", dropna=False)["word_count"]
    .agg(["count", "mean", "median", "min", "max"])
    .round(2)
)

print("\nTICKET LENGTH BY CATEGORY")
print(length_stats.to_string())

length_stats.to_csv(
    RESULTS_DIR / "ticket_length_stats.csv",
    encoding="utf-8-sig"
)

# Lay mau HR Support de nghien cuu
hr_tickets = df[
    df["Topic_group"] == "HR Support"
].copy()

print(f"\nHR Support tickets: {len(hr_tickets)}")

hr_samples = hr_tickets.sample(
    n=min(20, len(hr_tickets)),
    random_state=42
)

hr_samples[["Document", "Topic_group"]].to_csv(
    RESULTS_DIR / "hr_support_samples.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nHR SUPPORT SAMPLES")
for i, document in enumerate(hr_samples["Document"], 1):
    print(f"\n{i}. {str(document)[:300]}")

print("\nAnalysis completed.")
print("Results saved to results/")
