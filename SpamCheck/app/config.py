import os


# rules: 규칙 기반 판별
# ml: 로컬 joblib 모델 사용
# mlflow: MLflow Model Registry 모델 사용
MODEL_MODE = os.getenv("MODEL_MODE", "rules")

# 로컬 모델 파일 경로
LOCAL_MODEL_PATH = os.getenv(
    "LOCAL_MODEL_PATH",
    "ml/artifacts/spam_model.joblib",
)

# MLflow Tracking Server 주소
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:6430",
)

# MLflow Model Registry 모델 주소
# 예: models:/spam-model-new@champion
MODEL_URI = os.getenv(
    "MODEL_URI",
    "models:/spam-model-new@champion",
)

# 낮은 confidence 판단 기준
LOW_CONFIDENCE_THRESHOLD = float(
    os.getenv("LOW_CONFIDENCE_THRESHOLD", "0.65")
)

# 낮은 confidence가 몇 번 누적되면 이슈를 만들지
LOW_CONFIDENCE_LIMIT = int(
    os.getenv("LOW_CONFIDENCE_LIMIT", "5")
)