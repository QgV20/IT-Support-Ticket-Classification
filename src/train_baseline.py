from pathlib import Path
import time
import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (classification_report, accuracy_score,
                             f1_score, ConfusionMatrixDisplay)

ROOT = Path(__file__).resolve().parent.parent
DATA, RES = ROOT / "data", ROOT / "results"
RES.mkdir(exist_ok=True)

train = pd.read_csv(DATA / "train.csv")
test = pd.read_csv(DATA / "test.csv")
sample = pd.read_csv(DATA / "test_sample.csv")

model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                              max_features=50000, sublinear_tf=True)),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
])
model.fit(train["Document"], train["Topic_group"])
joblib.dump(model, RES / "baseline_tfidf_lr.joblib")

lines = []
for name, d in [("TEST DAY DU", test), ("TEST_SAMPLE (cung bo voi LLM)", sample)]:
    t0 = time.time()
    pred = model.predict(d["Document"])
    ms = (time.time() - t0) / len(d) * 1000
    acc = accuracy_score(d["Topic_group"], pred)
    mf1 = f1_score(d["Topic_group"], pred, average="macro")
    lines.append(f"=== {name} ({len(d)} dong) ===")
    lines.append(f"Accuracy={acc:.4f} | Macro F1={mf1:.4f} | {ms:.3f} ms/dong")
    lines.append(classification_report(d["Topic_group"], pred, digits=3))
    fig, ax = plt.subplots(figsize=(9, 8))
    ConfusionMatrixDisplay.from_predictions(
        d["Topic_group"], pred, xticks_rotation=45, ax=ax, colorbar=False)
    plt.tight_layout()
    plt.savefig(RES / f"confusion_{'full' if name.startswith('TEST DAY') else 'sample'}.png", dpi=150)
    plt.close()

report = "\n".join(lines)
print(report)
(RES / "baseline_report.txt").write_text(report, encoding="utf-8")