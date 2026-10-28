from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
df = pd.read_csv(ROOT / "data" / "all_tickets_processed_improved_v3.csv")

print("Kích thước:", df.shape)
print(df.dtypes)
print("\nDữ liệu thiếu:\n", df.isna().sum())
print("\nSố lượng mỗi nhãn:\n", df["Topic_group"].value_counts())
print("\nTỷ lệ (%):\n", (df["Topic_group"].value_counts(normalize=True) * 100).round(1))
print("\nSố từ mỗi văn bản:\n", df["Document"].str.split().str.len().describe())
print("\nSố Document trùng:", df["Document"].duplicated().sum())