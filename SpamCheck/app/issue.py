import os
import logging
import requests


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