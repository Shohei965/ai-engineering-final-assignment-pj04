from __future__ import annotations

import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from .utils import extract_sheet_id


def get_sheet_client() -> gspread.Client:
    cred_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE')
    if not cred_file or not os.path.exists(cred_file):
        raise RuntimeError('Service account credentials not found. Set GOOGLE_SERVICE_ACCOUNT_FILE')
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets.readonly',
        'https://www.googleapis.com/auth/drive.readonly',
    ]
    creds = Credentials.from_service_account_file(cred_file, scopes=scopes)
    return gspread.authorize(creds)


def fetch_questions(sheet_url: str, max_questions: int = 1000) -> tuple[pd.DataFrame, str, str]:
    sheet_id = extract_sheet_id(sheet_url)
    client = get_sheet_client()
    spreadsheet = client.open_by_key(sheet_id)

    # Get modified time from Drive API
    meta = client.request('get', f'https://www.googleapis.com/drive/v3/files/{sheet_id}?fields=modifiedTime')
    modified_time = meta.get('modifiedTime', '')

    worksheet = spreadsheet.sheet1
    records = worksheet.get_all_records()[:max_questions]
    df = pd.DataFrame(records, columns=['Timestamp', 'Question'])
    return df, sheet_id, modified_time
