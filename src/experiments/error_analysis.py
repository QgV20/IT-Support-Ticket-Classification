from pathlib import Path
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent.parent
DATA, RES = ROOT / "data", ROOT / "results"

model = joblib.load(RES / "baseline_tfidf_lr.joblib")
test = pd.read_csv(DATA / "test.csv")

test["pred"] = model.predict(test["Document"])
test["confidence"] = model.predict_proba(test["Document"]).max(axis=1)
errors = test[test["pred"] != test["Topic_group"]].copy()
errors.to_csv(RES / "misclassified_test.csv", index=False)
print(f"Số ticket sai: {len(errors)} / {len(test)}")

# Các cặp nhãn hay bị nhầm nhất (nhãn thật -> nhãn dự đoán)
pairs = (errors.groupby(["Topic_group", "pred"]).size()
         .sort_values(ascending=False).head(8))
print("\nTop cặp nhầm lẫn:\n", pairs)

# Xem ví dụ của 3 cặp nhầm nhiều nhất
for (true, pred), _ in pairs.head(3).items():
    print(f"\n--- Thật: {true} | Dự đoán: {pred} ---")
    ex = errors[(errors["Topic_group"] == true) & (errors["pred"] == pred)].head(5)
    for _, r in ex.iterrows():
        print(f"[{r['confidence']:.2f}] {r['Document'][:200]}")

# Độ tin cậy trung bình giữa dự đoán đúng và sai
test["correct"] = test["pred"] == test["Topic_group"]
print("\nConfidence trung bình:\n", test.groupby("correct")["confidence"].mean())

# Từ khóa nổi bật nhất của từng nhãn
vec = model.named_steps["tfidf"]
clf = model.named_steps["clf"]
terms = vec.get_feature_names_out()
print("\nTop 8 từ khóa mỗi nhãn:")
for i, label in enumerate(clf.classes_):
    top = clf.coef_[i].argsort()[-8:][::-1]
    print(f"{label}: {', '.join(terms[top])}")