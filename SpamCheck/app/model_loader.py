import joblib
import mlflow
import mlflow.sklearn

from app.config import (
    MODEL_MODE,
    LOCAL_MODEL_PATH,
    MLFLOW_TRACKING_URI,
    MODEL_URI,
)


_model = None


def load_model():
    global _model

    if _model is None:
        if MODEL_MODE == "mlflow":
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            _model = mlflow.sklearn.load_model(MODEL_URI)
        else:
            _model = joblib.load(LOCAL_MODEL_PATH)

    return _model