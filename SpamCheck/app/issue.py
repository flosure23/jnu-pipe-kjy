import logging
from datetime import datetime

import os
import requests

from app.config import LOW_CONFIDENCE_LIMIT

logger = logging.getLogger("spamcheck")

_state = {
    "low_confidence_count": 0,
    "samples": [],
    "issue_created": False,
}


def create_github_issue(title: str, body: str, logger: logging.Logger) -> None:
    repo = os.getenv("GH_REPO")
    token = os.getenv("GH_TOKEN")

    if not repo or not token:
        logger.warning("GH_REPO/GH_TOKEN not set; skipping GitHub issue creation.")
        return

    url = f"https://api.github.com/repos/{repo}/issues"

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
    }

    payload = {
        "title": title,
        "body": body,
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)

        if response.status_code >= 300:
            logger.warning(
                f"Failed to create issue: status={response.status_code}, body={response.text[:200]}"
            )
        else:
            issue_url = response.json().get("html_url")
            logger.info(f"GitHub issue created: {issue_url}")

    except Exception as e:
        logger.exception(f"GitHub issue creation failed: {type(e).__name__}: {e}")


def update_issue_state(
    text: str,
    label: str,
    score: float,
    threshold: float,
):
    """
    낮은 confidence 예측이 누적되면 drift 의심 상황으로 보고
    GitHub Issue를 1회 생성한다.
    """
    if score < threshold:
        _state["low_confidence_count"] += 1
        _state["samples"].append({
            "text": text,
            "label": label,
            "score": round(float(score), 4),
            "time": datetime.now().isoformat(timespec="seconds"),
        })

        logger.info(
            f"LOW CONFIDENCE | count={_state['low_confidence_count']} "
            f"threshold={threshold} label={label} score={score}"
        )

    if (
        _state["low_confidence_count"] >= LOW_CONFIDENCE_LIMIT
        and not _state["issue_created"]
    ):
        create_drift_issue()
        _state["issue_created"] = True

    return _state


def create_drift_issue():
    """
    최근 low confidence 샘플을 GitHub Issue 본문에 담아 생성한다.
    """
    samples = _state["samples"][-5:]

    title = "[MLOps] Drift suspected (low confidence accumulation)"

    body = (
        "## Drift Detection Report\n\n"
        "Low-confidence predictions accumulated.\n\n"
        f"- count: {_state['low_confidence_count']}\n"
        f"- threshold: {LOW_CONFIDENCE_LIMIT}\n\n"
        "## Recent Samples\n\n"
    )

    for sample in samples:
        body += (
            f"- ({sample['score']}) "
            f"{sample['text']} "
            f"→ predicted: {sample['label']} "
            f"at {sample['time']}\n"
        )

    body += (
        "\n## Action\n\n"
        "- Please review data\n"
        "- Decide whether retraining is needed\n"
        "- If needed, add reviewed samples to train.csv or test.csv\n"
    )

    create_github_issue(title, body, logger)