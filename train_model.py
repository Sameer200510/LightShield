import pandas as pd
import joblib
from lightgbm import LGBMClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from src.lightshield.utils.preprocessor import extract_features

# Load SQL dataset
sql_df = pd.read_csv("dataset/sql.csv")

sql_df = sql_df[["full_query", "label"]]
sql_df.columns = ["payload", "label"]

# Load XSS dataset
xss_df = pd.read_csv("dataset/xss.csv")

xss_df = xss_df[["Sentence", "Label"]]
xss_df.columns = ["payload", "label"]

# Combine datasets
df = pd.concat([sql_df, xss_df], ignore_index=True)

print("Total Samples:", len(df))

# Feature extraction
X = []
for payload in df["payload"]:
    X.append(extract_features(str(payload)))

y = df["label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train model
model = LGBMClassifier()
model.fit(X_train, y_train)

# Evaluate
preds = model.predict(X_test)
acc = accuracy_score(y_test, preds)

print("Model Accuracy:", acc)

# Save model
joblib.dump(model, "src/lightshield/models/ml_model.pkl")
print("Model saved successfully.")