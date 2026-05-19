import os


# rules: 규칙 기반 판별
# ml: 로컬 joblib 모델 사용
# mlflow: MLflow Model Registry 모델 사용
MODEL_MODE = os.getenv("MODEL_MODE", "rules")

# 로컬 모델 파일 경로
LOCAL_MODEL_PATH = os.getenv(
    "LOCAL_MODEL_PATH",
    "ml/artifacts/spam_model.joblib"
)

# MLflow Tracking Server 주소
# 처음에는 로컬 서버를 사용하고, ngrok 실습 후에는 ngrok URL로 바꿀 수 있다.
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:6430"
)

# MLflow Model Registry 모델 주소
# alias는 MLflow UI에서 champion 또는 challenger로 붙인다.
MODEL_URI = os.getenv(
    "MODEL_URI",
    "models:/spam-model@champion"
)