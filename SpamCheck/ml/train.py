import os
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.metrics import accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression


BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, "data", "spam.csv")
ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
MODEL_PATH = os.path.join(ARTIFACT_DIR, "spam_model.joblib")


def main():
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    x = df["text"]
    y = df["label"]

    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("spam-classification-local")

    pipeline = Pipeline([
        ("vectorizer", CountVectorizer()),
        ("classifier", LogisticRegression(max_iter=200))
    ])

    with mlflow.start_run():
        mlflow.log_param("model_type", "LogisticRegression")
        mlflow.log_param("vectorizer", "CountVectorizer")
        mlflow.log_param("max_iter", 200)
        mlflow.log_param("data_path", DATA_PATH)
        mlflow.log_param("row_count", len(df))

        pipeline.fit(x, y)

        preds = pipeline.predict(x)
        acc = accuracy_score(y, preds)

        mlflow.log_metric("train_accuracy", acc)

        joblib.dump(pipeline, MODEL_PATH)

        mlflow.log_artifact(DATA_PATH)
        mlflow.log_artifact(MODEL_PATH)

        mlflow.sklearn.log_model(
            sk_model=pipeline,
            name="model",
            registered_model_name="spam-model"
        )

        print(f"Model saved to: {MODEL_PATH}")
        print(f"train_accuracy: {acc:.4f}")


if __name__ == "__main__":
    main()