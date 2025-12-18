import datetime as dt
import logging
from typing import Any, Dict, List

from pymongo import MongoClient

import utils.constants as constants
from utils.helpers.sheets import append_rows, ensure_header, get_sheets_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HEADER = ["generated_at", "project_title", "brief_description", "stack", "steps", "data_sources"]


def _require(value: Any, name: str) -> Any:
    if not value:
        raise ValueError(f"Missing required config: {name}")
    return value


def _format_timestamp(value: Any) -> str:
    if isinstance(value, dt.datetime):
        return value.isoformat()
    return str(value) if value is not None else dt.datetime.now(dt.timezone.utc).isoformat()


def _coerce_list(value: Any) -> List[str]:
    if not value:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, str):
        return [value]
    return [str(value)]


def _format_stack(stack: Any) -> str:
    if stack is None:
        return ""
    if isinstance(stack, str):
        return stack.strip()
    return ", ".join(_coerce_list(stack))


def _format_steps(steps: Any) -> str:
    if isinstance(steps, str):
        return steps.strip()
    steps_list = _coerce_list(steps)
    return "\n".join(f"{idx + 1}) {step}" for idx, step in enumerate(steps_list))


def _format_links(links: Any) -> str:
    links_list = _coerce_list(links)
    return "\n".join(link.strip() if isinstance(link, str) else str(link) for link in links_list)


def _build_rows(docs: List[Dict[str, Any]]) -> List[List[str]]:
    rows: List[List[str]] = []
    for doc in docs:
        response = doc.get("response") or {}
        created_ts = _format_timestamp(doc.get("created_at") or doc.get("updated_at"))
        rows.append(
            [
                created_ts,
                response.get("project_title", ""),
                response.get("brief_description", ""),
                _format_stack(response.get("stack")),
                _format_steps(response.get("steps")),
                _format_links(response.get("link_to_data_source")),
            ]
        )
    return rows


def _get_mongo_docs() -> List[Dict[str, Any]]:
    mongo_uri = _require(constants.MONGO_CLUSTER_URI, "MONGO_CLUSTER_URI")
    db_name = constants.MONGO_DATABASE_NAME
    collection_name = constants.MONGO_COLLECTION_NAME

    with MongoClient(mongo_uri) as client:
        collection = client[db_name][collection_name]
        docs = list(collection.find())
        logger.info(f"Fetched {len(docs)} documents from MongoDB: {db_name}.{collection_name}")
        return docs


def _get_sheets_client():
    # Backward compatibility; prefer using sheets_helper directly.
    return get_sheets_client()


def _ensure_header(spreadsheets, spreadsheet_id: str, sheet_name: str) -> None:
    ensure_header(spreadsheets, spreadsheet_id, sheet_name, HEADER)


def _append_rows(spreadsheets, spreadsheet_id: str, sheet_name: str, rows: List[List[str]]) -> None:
    if not rows:
        logger.info("No rows to append; exiting")
        return
    append_rows(spreadsheets, spreadsheet_id, sheet_name, rows)
    logger.info("Appended %s rows to sheet %s", len(rows), sheet_name)


def run_migration():
    spreadsheet_id = _require(constants.GOOGLE_SPREADSHEET_ID, "GOOGLE_SPREADSHEET_ID")
    sheet_name = constants.GOOGLE_SHEET_NAME

    docs = _get_mongo_docs()
    rows = _build_rows(docs)

    spreadsheets = _get_sheets_client()
    _ensure_header(spreadsheets, spreadsheet_id, sheet_name)
    _append_rows(spreadsheets, spreadsheet_id, sheet_name, rows)
