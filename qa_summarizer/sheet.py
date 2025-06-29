from __future__ import annotations

import os
import pandas as pd
import gspread


def _get_client() -> gspread.Client:
    creds = os.getenv('GS_CREDENTIALS', 'credentials.json')
    token = os.getenv('GS_TOKEN', 'authorized_user.json')
    return gspread.oauth(credentials_filename=creds, authorized_user_filename=token)


def fetch_questions(sheet_url: str, max_questions: int = 1000) -> tuple[pd.DataFrame, str, str]:
    """Fetch sheet data via OAuth and return DataFrame with last update time."""
    gc = _get_client()
    sh = gc.open_by_url(sheet_url)
    sheet_id = sh.id
    values = sh.sheet1.get_all_values()
    df = pd.DataFrame(values[1:], columns=values[0]).loc[:max_questions - 1, ['Timestamp', 'Question']]
    modified_time = sh.get_lastUpdateTime()
    return df, sheet_id, modified_time
