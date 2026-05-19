import os
import joblib
import pandas as pd
import mlflow
import mlflow.sklearn

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

from app.config import MLFLOW_TRACKING_URI


BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")

TRAIN_DATA_PATH = os.path.join(DATA_DIR, "train.csv")
TEST_DATA_PATH = os.path.join(DATA_DIR, "test.csv")

ARTIFACT_DIR = os.path.join(BASE_DIR, "artifacts")
MODEL_PATH = os.path.join(ARTIFACT_DIR, "spam_model.joblib")


def main():
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment("spam-classification-local")

    train_df = pd.read_csv(TRAIN_DATA_PATH)
    test_df = pd.read_csv(TEST_DATA_PATH)

    x_train = train_df["text"]
    y_train = train_df["label"]

    x_test = test_df["text"]
    y_test = test_df["label"]

    models = {
        "LogisticRegression": LogisticRegression(max_iter=200),
        "NaiveBayes": MultinomialNB(),
        "DecisionTree": DecisionTreeClassifier(random_state=42),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    }

    best_model = None
    best_model_name = None
    best_test_acc = -1

    for model_name, model in models.items():
        with mlflow.start_run(run_name=model_name):
            pipeline = Pipeline([
                ("vectorizer", CountVectorizer()),
                ("classifier", model),
            ])

            pipeline.fit(x_train, y_train)

            train_preds = pipeline.predict(x_train)
            test_preds = pipeline.predict(x_test)

            train_acc = accuracy_score(y_train, train_preds)
            test_acc = accuracy_score(y_test, test_preds)

            mlflow.log_param("model_name", model_name)
            mlflow.log_param("train_data_path", TRAIN_DATA_PATH)
            mlflow.log_param("test_data_path", TEST_DATA_PATH)
            mlflow.log_param("train_row_count", len(train_df))
            mlflow.log_param("test_row_count", len(test_df))

            mlflow.log_metric("train_accuracy", train_acc)
            mlflow.log_metric("test_accuracy", test_acc)

            mlflow.log_artifact(TRAIN_DATA_PATH)
            mlflow.log_artifact(TEST_DATA_PATH)

            mlflow.sklearn.log_model(
                sk_model=pipeline,
                artifact_path="model",
                registered_model_name="spam-model",
            )

            print(f"[{model_name}]")
            print(f"train_accuracy: {train_acc:.4f}")
            print(f"test_accuracy : {test_acc:.4f}")
            print()

            if test_acc > best_test_acc:
                best_test_acc = test_acc
                best_model = pipeline
                best_model_name = model_name

    joblib.dump(best_model, MODEL_PATH)

    print(f"Best model: {best_model_name}")
    print(f"Best test_accuracy: {best_test_acc:.4f}")
    print(f"Local model saved to: {MODEL_PATH}")


if __name__ == "__main__":
    main()