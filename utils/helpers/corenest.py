import json
from pathlib import Path
from typing import Any, Dict, List

import requests

import utils.constants as constants
from config.logger import logger


def _load_prompt(path: str) -> str:
    try:
        return Path(path).read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompt file not found: {path}")


def _dispatch_request(url: str, method: str = "post", payload: Dict[str, Any] | None = None, timeout: int = 60) -> Any:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {constants.CORENEST_SECRET_KEY}",
    }
    response = requests.request(method=method, url=url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()
    try:
        return response.json()
    except json.JSONDecodeError:
        return response.text


def ping() -> bool:
    url = f"{constants.CORENEST_API_URL.rstrip('/')}/ping"
    try:
        return _dispatch_request(url, method="get") == "pong"
    except Exception as exc:
        logger.warning("CoreNest ping failed: %s", exc)
        return False


def generate_ideas() -> List[Dict[str, Any]]:
    """Call CoreNest completions API using local prompts and return the ideas list."""
    system_prompt = _load_prompt("utils/prompts/system_prompt.txt")
    user_prompt = _load_prompt("utils/prompts/user_prompt.txt")
    url = f"{constants.CORENEST_API_URL.rstrip('/')}/completions"
    payload = {
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "structured_output": True,
    }

    logger.info("Sending request to CoreNest completions API at %s", url)
    raw = _dispatch_request(url, method="post", payload=payload)

    data = raw.get("result") if isinstance(raw, dict) else raw
    if isinstance(data, dict) and "content" in data:
        data = data["content"]

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            raise ValueError("CoreNest returned string content that was not valid JSON.")

    if not isinstance(data, list):
        raise ValueError("Expected CoreNest to return a JSON array of ideas in result.content")

    return data
