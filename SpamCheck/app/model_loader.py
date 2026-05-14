import joblib
import mlflow
import mlflow.sklearn

from app.config import LOCAL_MODEL_PATH, MLFLOW_TRACKING_URI, MODEL_URI


_model = None


def load_model():
    global _model

    if _model is None:
        if MODEL_URI:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            _model = mlflow.sklearn.load_model(MODEL_URI)
        else:
            _model = joblib.load(LOCAL_MODEL_PATH)

    return _model