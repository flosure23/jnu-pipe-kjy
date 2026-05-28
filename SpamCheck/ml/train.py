import os
import time
from pathlib import Path

import joblib
import pandas as pd
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

TRAIN_DATA_PATH = DATA_DIR / "train.csv"
TEST_DATA_PATH = DATA_DIR / "test.csv"

ARTIFACT_DIR = BASE_DIR / "artifacts"
MODEL_PATH = ARTIFACT_DIR / "spam_model.joblib"

DEFAULT_TRACKING_URI = (BASE_DIR.parent / "mlruns").resolve().as_uri()
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI") or DEFAULT_TRACKING_URI

MLFLOW_EXPERIMENT_NAME = os.getenv(
    "MLFLOW_EXPERIMENT_NAME",
    "spam-classification-server",
)

MLFLOW_REGISTERED_MODEL_NAME = os.getenv(
    "MLFLOW_REGISTERED_MODEL_NAME",
    "spam-model",
)

MLFLOW_MODEL_ALIAS = os.getenv(
    "MLFLOW_MODEL_ALIAS",
    "champion",
)


def wait_until_model_version_ready(
    client: MlflowClient,
    model_name: str,
    version: str,
    max_wait_seconds: int = 30,
) -> None:
    """
    MLflow Model Registry에 새 모델 버전이 등록된 직후에는
    상태가 READY가 아닐 수 있으므로 잠깐 기다린다.
    """
    for _ in range(max_wait_seconds):
        model_version = client.get_model_version(model_name, version)

        if getattr(model_version, "status", "READY") == "READY":
            return

        time.sleep(1)


def set_model_alias(model_name: str, version: str, alias: str) -> None:
    """
    특정 모델 버전에 alias를 붙인다.
    예: spam-model-new의 version 12를 champion으로 지정
    """
    client = MlflowClient()

    wait_until_model_version_ready(
        client=client,
        model_name=model_name,
        version=str(version),
    )

    client.set_registered_model_alias(
        name=model_name,
        alias=alias,
        version=str(version),
    )


def get_current_alias_test_accuracy(
    model_name: str,
    alias: str,
) -> float:
    """
    현재 champion alias가 붙어 있는 모델의 test_accuracy를 가져온다.
    아직 champion이 없거나 정보를 못 읽으면 -1.0으로 처리한다.
    """
    client = MlflowClient()

    try:
        current_version = client.get_model_version_by_alias(
            name=model_name,
            alias=alias,
        )

        run = client.get_run(current_version.run_id)
        test_accuracy = run.data.metrics.get("test_accuracy")

        if test_accuracy is None:
            return -1.0

        return float(test_accuracy)

    except Exception as e:
        print(
            f"[PROMOTION] current {alias} not found "
            f"or test_accuracy unavailable: {type(e).__name__}: {e}"
        )
        return -1.0


def promote_if_better(
    model_name: str,
    new_version: str,
    new_test_accuracy: float,
    alias: str = "champion",
) -> None:
    """
    새 모델의 test_accuracy가 현재 champion보다 좋을 때만 alias를 교체한다.
    """
    current_test_accuracy = get_current_alias_test_accuracy(
        model_name=model_name,
        alias=alias,
    )

    print(f"[PROMOTION] current {alias} test_accuracy = {current_test_accuracy}")
    print(f"[PROMOTION] new candidate test_accuracy = {new_test_accuracy}")

    if new_test_accuracy > current_test_accuracy:
        set_model_alias(
            model_name=model_name,
            version=str(new_version),
            alias=alias,
        )
        print(f"[PROMOTION] version {new_version} promoted to {alias}")
    else:
        print(f"[PROMOTION] {alias} unchanged")


def train_and_log_model(
    model_name: str,
    model,
    x_train,
    y_train,
    x_test,
    y_test,
    train_df: pd.DataFrame,
    test_df: pd.DataFrame,
):
    """
    모델 하나를 학습하고 MLflow에 metric, param, artifact, model을 기록한다.
    """
    with mlflow.start_run(run_name=model_name):
        run_id = mlflow.active_run().info.run_id

        pipeline = Pipeline([
            ("vectorizer", CountVectorizer()),
            ("classifier", model),
        ])

        pipeline.fit(x_train, y_train)

        train_preds = pipeline.predict(x_train)
        test_preds = pipeline.predict(x_test)

        train_acc = accuracy_score(y_train, train_preds)
        test_acc = accuracy_score(y_test, test_preds)

        mlflow.log_param("model_type", model_name)
        mlflow.log_param("train_data_path", str(TRAIN_DATA_PATH))
        mlflow.log_param("test_data_path", str(TEST_DATA_PATH))
        mlflow.log_param("train_row_count", len(train_df))
        mlflow.log_param("test_row_count", len(test_df))

        mlflow.log_metric("train_accuracy", train_acc)
        mlflow.log_metric("test_accuracy", test_acc)

        mlflow.log_artifact(str(TRAIN_DATA_PATH))
        mlflow.log_artifact(str(TEST_DATA_PATH))

        mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="model",
        )

        print(f"[{model_name}]")
        print(f"run_id        : {run_id}")
        print(f"train_accuracy: {train_acc:.4f}")
        print(f"test_accuracy : {test_acc:.4f}")
        print()

        return {
            "model_name": model_name,
            "pipeline": pipeline,
            "run_id": run_id,
            "train_accuracy": train_acc,
            "test_accuracy": test_acc,
        }


def main():
    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    print(f"MLFLOW_TRACKING_URI: {MLFLOW_TRACKING_URI}")
    print(f"MLFLOW_EXPERIMENT_NAME: {MLFLOW_EXPERIMENT_NAME}")
    print(f"MLFLOW_REGISTERED_MODEL_NAME: {MLFLOW_REGISTERED_MODEL_NAME}")
    print(f"MLFLOW_MODEL_ALIAS: {MLFLOW_MODEL_ALIAS}")
    print()

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
        "RandomForest": RandomForestClassifier(
            n_estimators=100,
            random_state=42,
        ),
    }

    best_result = None

    for model_name, model in models.items():
        result = train_and_log_model(
            model_name=model_name,
            model=model,
            x_train=x_train,
            y_train=y_train,
            x_test=x_test,
            y_test=y_test,
            train_df=train_df,
            test_df=test_df,
        )

        if best_result is None:
            best_result = result
        elif result["test_accuracy"] > best_result["test_accuracy"]:
            best_result = result

    if best_result is None:
        raise RuntimeError("No model was trained.")

    best_model_name = best_result["model_name"]
    best_model = best_result["pipeline"]
    best_run_id = best_result["run_id"]
    best_test_acc = best_result["test_accuracy"]

    joblib.dump(best_model, MODEL_PATH)

    print(f"Best model: {best_model_name}")
    print(f"Best test_accuracy: {best_test_acc:.4f}")
    print(f"Local model saved to: {MODEL_PATH}")

    if MLFLOW_REGISTERED_MODEL_NAME and best_run_id:
        model_uri = f"runs:/{best_run_id}/model"

        print(f"Registering best model from: {model_uri}")

        model_version = mlflow.register_model(
            model_uri=model_uri,
            name=MLFLOW_REGISTERED_MODEL_NAME,
        )

        print(
            f"Registered model: {MLFLOW_REGISTERED_MODEL_NAME} "
            f"version {model_version.version}"
        )

        if MLFLOW_MODEL_ALIAS:
            promote_if_better(
                model_name=MLFLOW_REGISTERED_MODEL_NAME,
                new_version=str(model_version.version),
                new_test_accuracy=best_test_acc,
                alias=MLFLOW_MODEL_ALIAS,
            )
    else:
        print(
            "[PROMOTION] skipped: "
            "MLFLOW_REGISTERED_MODEL_NAME or best_run_id is missing"
        )


if __name__ == "__main__":
    main()