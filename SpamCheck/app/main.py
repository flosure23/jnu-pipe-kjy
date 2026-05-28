import logging
import traceback

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.config import (
    MODEL_MODE,
    LOW_CONFIDENCE_THRESHOLD,
)
from app.spam import check_spam_rules, check_spam_ml
from app.model_loader import get_model_info
from app.issue import create_github_issue, update_issue_state


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | %(levelname)s | "
        "%(filename)s:%(lineno)d (%(funcName)s) | "
        "%(message)s"
    ),
)

logger = logging.getLogger("spamcheck")

app = FastAPI(title="SpamCheck Web")

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()


class ClassifyRequest(BaseModel):
    text: str


@app.post("/classify")
async def classify(payload: ClassifyRequest):
    text = payload.text

    logger.info(
        f"CALL /classify | mode={MODEL_MODE} | text='{text}' | len={len(text)}"
    )

    try:
        if text == "crash":
            raise RuntimeError("의도적 장애 추가")

        if MODEL_MODE in ["ml", "mlflow"]:
            label, score = check_spam_ml(text)

            update_issue_state(
                text=text,
                label=label,
                score=score,
                threshold=LOW_CONFIDENCE_THRESHOLD,
            )

        else:
            label, score = check_spam_rules(text)

        logger.info(
            f"OK /classify | mode={MODEL_MODE} | label={label} score={score}"
        )

        return {
            "label": label,
            "score": score,
            "model_info": get_model_info(),
        }

    except Exception as e:
        logger.exception(
            f"FAIL /classify | mode={MODEL_MODE} | text='{text}' "
            f"| error={type(e).__name__}: {e}"
        )

        tb = traceback.format_exc()

        title = f"[Local Error] /classify failed: {type(e).__name__}"

        body = (
            "## Summary\n"
            f"- environment: local uvicorn server\n"
            f"- mode: `{MODEL_MODE}`\n"
            f"- endpoint: /classify\n"
            f"- input(text, short): `{text}`\n"
            f"- input length: {len(text)}\n\n"
            "## Exception\n"
            f"- type: `{type(e).__name__}`\n"
            f"- message: `{str(e)}`\n\n"
            "## Traceback (line info)\n"
            f"```text\n{tb}\n```"
        )

        create_github_issue(title, body, logger)

        return {
            "label": "Internal Server Error",
            "score": -1,
            "model_info": get_model_info(),
        }