
from pathlib import Path
import re

import pandas as pd

# Thiết lập đường dẫn của dự án
ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"

TEST_FILE = DATA / "test_sample.csv"

# Các tập đã dùng trong quá trình phát triển prompt
DEVELOPMENT_FILES = [
    RESULTS / "llm_dev_sample80.csv",
    RESULTS / "llm_validation_sample160.csv",
    RESULTS / "hr_support_samples.csv",
]

EXPECTED_LABELS = {
    "Hardware",
    "HR Support",
    "Access",
    "Miscellaneous",
    "Storage",
    "Purchase",
    "Internal Project",
    "Administrative rights",
}


def normalize_text(text: str) -> str:
    """Chuẩn hóa văn bản để kiểm tra nội dung trùng khớp."""
    return re.sub(
        r"\s+",
        " ",
        str(text).strip().lower(),
    )


# Đọc dữ liệu test và kiểm tra cấu trúc
test = pd.read_csv(TEST_FILE)

required = {"Document", "Topic_group"}

if not required.issubset(test.columns):
    raise ValueError("Tập test thiếu cột bắt buộc.")

if test[list(required)].isna().any().any():
    raise ValueError("Tập test có giá trị thiếu.")

if len(test) != 400:
    raise ValueError(
        f"Tập test có {len(test)} ticket, không phải 400."
    )

if set(test["Topic_group"]) != EXPECTED_LABELS:
    raise ValueError("Danh sách nhãn không khớp.")

# Chuẩn hóa nội dung test để kiểm tra trùng
test_texts = test["Document"].map(normalize_text)

duplicate_count = int(test_texts.duplicated().sum())

print("=" * 60)
print("KIỂM TRA TẬP TEST CUỐI CÙNG")
print("=" * 60)

print("\nTổng số ticket:", len(test))
print("Số nhóm nhãn:", test["Topic_group"].nunique())
print("Nội dung trùng trong test:", duplicate_count)

print("\nPHÂN BỐ NHÃN")
print(test["Topic_group"].value_counts().to_string())

# Kiểm tra trùng với những tập phát triển đã lưu
overlap_rows = []

for file_path in DEVELOPMENT_FILES:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy file: {file_path}"
        )

    old = pd.read_csv(file_path)

    if "Document" not in old.columns:
        raise ValueError(
            f"File {file_path.name} thiếu cột Document."
        )

    old_texts = set(
        old["Document"].map(normalize_text)
    )

    overlap = int(test_texts.isin(old_texts).sum())

    overlap_rows.append({
        "Dataset": file_path.name,
        "Overlapping_tickets": overlap,
    })

overlap_df = pd.DataFrame(overlap_rows)

print("\nTRÙNG NỘI DUNG VỚI TẬP PHÁT TRIỂN")
print(overlap_df.to_string(index=False))

# Kiểm tra thêm trùng với dữ liệu train
train = pd.read_csv(DATA / "train.csv")

train_texts = set(
    train["Document"].dropna().map(normalize_text)
)

train_overlap = int(test_texts.isin(train_texts).sum())

print("\nSố ticket trùng nội dung với train.csv:", train_overlap)

# Lưu báo cáo kiểm tra
output_file = RESULTS / "final_test_integrity_check.csv"

if output_file.exists():
    raise FileExistsError(
        "File kiểm tra đã tồn tại, không tự ghi đè."
    )

overlap_df.to_csv(
    output_file,
    index=False,
    encoding="utf-8-sig",
)

print("\nĐã lưu:", output_file)
