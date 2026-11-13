
from pathlib import Path
import re

import pandas as pd

# Thiết lập đường dẫn
ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"

# Biểu thức tìm yêu cầu liên quan nâng cấp Windows
WINDOWS_PATTERN = (
    r"\bwindows?\b.*\b(?:upgrade|update)\b"
    r"|\b(?:upgrade|update)\b.*\bwindows?\b"
)


def normalize_text(text: str) -> str:
    """Chuẩn hóa nội dung để loại các bản trùng lặp."""
    return re.sub(r"\s+", " ", str(text).strip().lower())


# Đọc dữ liệu train và giữ chỉ số dòng gốc
train = pd.read_csv(DATA / "train.csv")

train = train.reset_index().rename(
    columns={"index": "ticket_id"}
)

train = train.dropna(
    subset=["Document", "Topic_group"]
).copy()

train["normalized_document"] = (
    train["Document"].map(normalize_text)
)

# Loại các ticket đã dùng để phát triển và kiểm định
excluded_ids = set()
excluded_texts = set()

for filename in [
    "llm_dev_sample80.csv",
    "llm_validation_sample160.csv",
    "hr_support_samples.csv",
]:
    path = RESULTS / filename

    if not path.exists():
        raise FileNotFoundError(f"Thiếu file: {path}")

    old = pd.read_csv(path)

    if "ticket_id" in old.columns:
        excluded_ids.update(old["ticket_id"].tolist())

    excluded_texts.update(
        old["Document"].map(normalize_text)
    )

# Loại nội dung đã xuất hiện trong các tập test
for filename in ["test.csv", "test_sample.csv"]:
    path = DATA / filename

    if not path.exists():
        raise FileNotFoundError(f"Thiếu file: {path}")

    old = pd.read_csv(path)

    excluded_texts.update(
        old["Document"].map(normalize_text)
    )

study = train[
    ~train["ticket_id"].isin(excluded_ids)
    & ~train["normalized_document"].isin(excluded_texts)
].copy()

study = study.drop_duplicates(
    subset=["normalized_document"]
)

# Chọn các ticket khớp dấu hiệu Windows upgrade
matches = study[
    study["normalized_document"].str.contains(
        WINDOWS_PATTERN,
        regex=True,
        na=False,
    )
]

print("=" * 60)
print("SO SÁNH WINDOWS UPGRADE GIỮA CÁC NHÃN")
print("=" * 60)

# Đọc mẫu từ hai nhóm cần đối chiếu
for label in ["Administrative rights", "Hardware"]:
    group = matches[
        matches["Topic_group"] == label
    ]

    print(f"\nNHÃN: {label}")
    print("Số ticket khớp:", len(group))

    sample = group.sample(
        n=min(5, len(group)),
        random_state=2026,
    )

    for _, row in sample.iterrows():
        print(f"\nTicket ID: {row['ticket_id']}")
        print(f"Nội dung: {str(row['Document'])[:300]}")

print("\nĐã hoàn thành đối chiếu mẫu.")
