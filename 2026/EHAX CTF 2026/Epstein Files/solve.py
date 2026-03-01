import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

X_train = train.drop(columns=["In Black Book"])
y_train = train["In Black Book"]


for col in ["Name", "Bio", "Category"]:
    X_train[col] = X_train[col].fillna("")
    test[col] = test[col].fillna("")
X_train["Nationality"] = X_train["Nationality"].fillna("Unknown")
test["Nationality"] = test["Nationality"].fillna("Unknown")

np.random.seed(42)
flip_mask = np.random.rand(len(y_train)) < 0.30
y_train_noisy = y_train.copy()
y_train_noisy[flip_mask] = 1 - y_train_noisy[flip_mask]

preprocessor = ColumnTransformer(
    transformers=[
        ("name_tfidf", TfidfVectorizer(analyzer="char", ngram_range=(2,4)), "Name"),
        ("cat_ohe", OneHotEncoder(handle_unknown="ignore"), ["Category", "Nationality"]),
        ("numeric", "passthrough", ["Flights", "Documents", "Connections"])
    ]
)

clf = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(n_estimators=100, max_depth=4, random_state=42))
])

clf.fit(X_train, y_train_noisy)

preds = clf.predict(test)

flip_fraction = 0.1
flip_indices = np.random.choice(len(preds), size=int(len(preds)*flip_fraction), replace=False)
preds[flip_indices] = 1 - preds[flip_indices]

submission = pd.DataFrame({"In Black Book": preds})
submission.to_csv("submission.csv", index=False)

print("> Trained model")

import requests
import re

url = "http://chall.ehax.in:4529/"

with open('submission.csv', 'r') as f:
    res = requests.post(f"{url}/submit", files={
        'submission': ('submission.csv', f.read(), 'text/csv')
    })

flag = re.findall(r'(EH4X{.+})', res.text)[0]
print("Flag:", flag)