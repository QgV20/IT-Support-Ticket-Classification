
from pathlib import Path
import re

import pandas as pd

# Thiết lập đường dẫn dự án
ROOT = Path(__file__).resolve().parent.parent.parent
DATA = ROOT / "data"
RESULTS = ROOT / "results"

TRAIN_FILE = DATA / "train.csv"
DEV_FILE = RESULTS / "llm_dev_sample80.csv"
VALIDATION_FILE = RESULTS / "llm_validation_sample160.csv"

TARGET_LABEL = "Administrative rights"

# Các chủ đề cần khảo sát từ kết quả phân tích Ngày 3

TOPIC_PATTERNS = {
    "windows_upgrade": (
        r"\bwindows?\b.*\b(?:upgrade|update)\b"
        r"|\b(?:upgrade|update)\b.*\bwindows?\b"
    ),
    "software_install": (
        r"\b(?:install|installation|software|application)\b"
    ),
    "outlook_email": r"\b(?:outlook|email|mailbox)\b",
    "administrator_privilege": (
        r"\b(?:admin|administrator|privilege|elevated)\b"
    ),
    "password_login": (
        r"\b(?:password|login|log in|sign in)\b"
    ),
    "server_restart": r"\b(?:server|restart|reboot)\b",
    "storage_drive": r"\b(?:storage|disk|drive|space)\b",
    "printer_device": (
        r"\b(?:printer|xerox|laptop|desktop|device)\b"
    ),
}


# Đọc dữ liệu và giữ lại chỉ số dòng gốc
train = pd.read_csv(TRAIN_FILE)

required = {"Document", "Topic_group"}
if not required.issubset(train.columns):
    raise ValueError("train.csv thiếu cột bắt buộc.")

train = train.reset_index().rename(
    columns={"index": "ticket_id"}
)

train = train.dropna(
    subset=["Document", "Topic_group"]
).copy()

# Chuẩn hóa nhẹ để kiểm tra nội dung trùng khớp
def normalize_text(text):
    return re.sub(
        r"\s+", " ", str(text).strip().lower()
    )


train["normalized_document"] = (
    train["Document"].map(normalize_text)
)

# Loại dữ liệu đã sử dụng trong các thực nghiệm cũ
excluded_ids = set()
excluded_texts = set()

for file_path in [DEV_FILE, VALIDATION_FILE]:
    if not file_path.exists():
        raise FileNotFoundError(
            f"Không tìm thấy tập dữ liệu: {file_path}"
        )

    old_data = pd.read_csv(file_path)

    excluded_ids.update(
        old_data["ticket_id"].tolist()
    )

    excluded_texts.update(
        old_data["Document"].map(normalize_text)
    )

# Loại thêm các mẫu HR đã quan sát trước đây
hr_file = RESULTS / "hr_support_samples.csv"

if hr_file.exists():
    hr_data = pd.read_csv(hr_file)

    excluded_texts.update(
        hr_data["Document"].map(normalize_text)
    )

# Loại nội dung xuất hiện trong tập test
for test_name in ["test.csv", "test_sample.csv"]:
    test_file = DATA / test_name

    if test_file.exists():
        test_data = pd.read_csv(test_file)

        excluded_texts.update(
            test_data["Document"].map(normalize_text)
        )

# Bảo đảm dữ liệu khảo sát không trùng các tập đã dùng
study = train[
    ~train["ticket_id"].isin(excluded_ids)
    & ~train["normalized_document"].isin(excluded_texts)
].copy()

study = study.drop_duplicates(
    subset=["normalized_document"]
)

# Đánh dấu các chủ đề xuất hiện trong ticket
for topic, pattern in TOPIC_PATTERNS.items():
    study[topic] = study["normalized_document"].str.contains(
        pattern,
        case=False,
        regex=True,
        na=False,
    )

print("=" * 60)
print("KHẢO SÁT NHÃN ADMINISTRATIVE RIGHTS")
print("=" * 60)

admin = study[
    study["Topic_group"] == TARGET_LABEL
].copy()

print("\nSố ticket còn lại để khảo sát:", len(study))
print("Administrative rights:", len(admin))

# Thống kê số ticket chứa mỗi chủ đề theo từng nhãn
rows = []

for label, group in study.groupby("Topic_group"):
    for topic in TOPIC_PATTERNS:
        count = int(group[topic].sum())

        rows.append({
            "Category": label,
            "Topic": topic,
            "Count": count,
            "Total": len(group),
            "Percentage": round(
                count / len(group) * 100, 2
            ),
        })

topic_stats = pd.DataFrame(rows)

topic_stats.to_csv(
    RESULTS / "admin_topic_distribution.csv",
    index=False,
    encoding="utf-8-sig",
)

# Hiển thị thống kê Administrative rights
admin_stats = topic_stats[
    topic_stats["Category"] == TARGET_LABEL
].sort_values("Count", ascending=False)

print("\nCHỦ ĐỀ TRONG ADMINISTRATIVE RIGHTS")
print(
    admin_stats[
        ["Topic", "Count", "Percentage"]
    ].to_string(index=False)
)

# Lấy mẫu riêng trong từng chủ đề để đọc thủ công
samples = []

for topic in TOPIC_PATTERNS:
    subset = admin[admin[topic]]

    if subset.empty:
        continue

    sample = subset.sample(
        n=min(5, len(subset)),
        random_state=42,
    ).copy()

    sample["Matched_topic"] = topic

    samples.append(
        sample[
            [
                "ticket_id",
                "Document",
                "Topic_group",
                "Matched_topic",
            ]
        ]
    )

if samples:
    sample_df = pd.concat(
        samples,
        ignore_index=True,
    )

    sample_df.to_csv(
        RESULTS / "admin_train_topic_samples.csv",
        index=False,
        encoding="utf-8-sig",
    )

# Kiểm tra nhãn khác trong từng chủ đề
print("\nSO SÁNH MỘT SỐ CHỦ ĐỀ GIỮA CÁC NHÃN")

for topic in [
    "windows_upgrade",
    "outlook_email",
    "administrator_privilege",
    "software_install",
]:
    subset = topic_stats[
        topic_stats["Topic"] == topic
    ].sort_values(
        "Percentage",
        ascending=False
    )

    print(f"\nChủ đề: {topic}")
    print(
        subset[
            ["Category", "Count", "Percentage"]
        ].to_string(index=False)
    )

print("\nĐã lưu kết quả trong thư mục results/")
