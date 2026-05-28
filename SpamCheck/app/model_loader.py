import joblib
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

from app.config import (
    MODEL_MODE,
    LOCAL_MODEL_PATH,
    MLFLOW_TRACKING_URI,
    MODEL_URI,
)


_model = None
_model_info = None


def get_model_info():
    global _model_info

    if _model_info is None:
        if MODEL_MODE == "mlflow":
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

            try:
                info = mlflow.models.get_model_info(MODEL_URI)
                run = MlflowClient().get_run(info.run_id)

                _model_info = {
                    "run_id": info.run_id,
                    "model_type": run.data.params.get("model_type"),
                    "test_accuracy": run.data.metrics.get("test_accuracy"),
                }

            except Exception:
                _model_info = {
                    "run_id": "unknown",
                    "model_type": None,
                    "test_accuracy": None,
                }
        else:
            _model_info = {
                "run_id": "local",
                "model_type": "local_or_rules",
                "test_accuracy": None,
            }

    return _model_info


def load_model():
    global _model

    if _model is None:
        if MODEL_MODE == "mlflow":
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            _model = mlflow.sklearn.load_model(MODEL_URI)
        else:
            _model = joblib.load(LOCAL_MODEL_PATH)

    return _model