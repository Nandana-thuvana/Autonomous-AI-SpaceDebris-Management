import os
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


def train():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_PATH = os.path.join(BASE_DIR, "debris_dataset.csv")
    MODEL_PATH = os.path.join(BASE_DIR, "debris_model.pkl")

    df = pd.read_csv(CSV_PATH)

    print("Original class distribution:\n", df["label"].value_counts())

    # ✅ Balance the dataset
    debris_df = df[df["label"] == 1]
    sat_df = df[df["label"] == 0].sample(n=len(debris_df), random_state=42)

    balanced_df = pd.concat([debris_df, sat_df])

    print("\nBalanced class distribution:\n", balanced_df["label"].value_counts())

    # Features and label
    X = balanced_df.drop("label", axis=1)
    y = balanced_df["label"]

    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Model
    model = RandomForestClassifier(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    print("\n✅ Model trained on balanced data!")

    # Evaluation
    y_pred = model.predict(X_test)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    # Save model
    joblib.dump(model, MODEL_PATH)
    print(f"\n✅ Model saved at: {MODEL_PATH}")


if __name__ == "__main__":
    train()
