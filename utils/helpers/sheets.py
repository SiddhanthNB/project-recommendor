from typing import Any, List

from google.oauth2 import service_account
from googleapiclient.discovery import build

import utils.constants as constants

SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def get_sheets_client():
    credentials = service_account.Credentials.from_service_account_info(
        constants.GOOGLE_SERVICE_ACCOUNT_JSON, scopes=SHEETS_SCOPES
    )
    service = build("sheets", "v4", credentials=credentials, cache_discovery=False)
    return service.spreadsheets()


def ensure_header(spreadsheets, spreadsheet_id: str, sheet_name: str, header: List[str]) -> None:
    range_name = f"{sheet_name}!A1:{chr(ord('A') + len(header) - 1)}1"
    result = spreadsheets.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    if not result.get("values"):
        spreadsheets.values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body={"values": [header]},
        ).execute()


def append_rows(spreadsheets, spreadsheet_id: str, sheet_name: str, rows: List[List[Any]]) -> None:
    if not rows:
        return
    spreadsheets.values().append(
        spreadsheetId=spreadsheet_id,
        range=f"{sheet_name}!A1",
        valueInputOption="RAW",
        insertDataOption="INSERT_ROWS",
        body={"values": rows},
    ).execute()
