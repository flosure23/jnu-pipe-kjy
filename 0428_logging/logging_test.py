import logging

# 로거 생성
logger = logging.getLogger()

# 로그 출력 기준 설정
logger.setLevel(logging.INFO)

# 로그 출력 형식 설정
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# 콘솔 출력 핸들러
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# 파일 출력 핸들러
file_handler = logging.FileHandler("my.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

for i in range(10):
    logger.info(f"{i}번째 방문입니다.")