import logging
import logging.config

logging.config.dictConfig({
    "version": 1,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple"
        }
    },
    "formatters": {
        "simple": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO"
    }
})

logger = logging.getLogger(__name__)

for i in range(10):
    logger.info(f"{i}번째 방문입니다.")