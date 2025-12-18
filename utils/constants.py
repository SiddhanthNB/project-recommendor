import os
import json
from typing import Any
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

def _get_env(key: str, default: Any = None, required: bool = False) -> Any:
    value = os.getenv(key, default)
    if required and (value is None or value == ""):
        raise ValueError(f"Missing required config: {key}")
    return value

PROJECT_NAME = 'project-recommender'

APP_ENV = _get_env("APP_ENV", "production")

CORENEST_API_URL = _get_env("CORENEST_API_URL", required=True)
CORENEST_SECRET_KEY = _get_env("CORENEST_SECRET_KEY", required=True)

# Mongo is deprecated; keep optional to avoid import failures if env vars are absent.
_mongo_user_password = _get_env("MONGO_USER_PASSWORD", default=None, required=False)
MONGO_CLUSTER_URI = _get_env("MONGO_CLUSTER_URI", default="", required=False)
if MONGO_CLUSTER_URI and _mongo_user_password:
    MONGO_CLUSTER_URI = MONGO_CLUSTER_URI.replace("<db_password>", quote_plus(_mongo_user_password))

MONGO_DATABASE_NAME = _get_env("MONGO_DATABASE_NAME", "project_recommendation")
MONGO_COLLECTION_NAME = _get_env("MONGO_COLLECTION_NAME", "recommendations")

GOOGLE_SPREADSHEET_ID = _get_env("GOOGLE_SPREADSHEET_ID", required=True)
GOOGLE_SHEET_NAME = _get_env("GOOGLE_SHEET_NAME", "AI/ML Ideas")

GOOGLE_SERVICE_ACCOUNT_JSON = json.loads(_get_env("GOOGLE_SERVICE_ACCOUNT_JSON", required=True))
