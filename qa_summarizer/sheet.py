from __future__ import annotations

import hashlib
import io
import pandas as pd
import requests
from .utils import extract_sheet_id


def fetch_questions(sheet_url: str, max_questions: int = 1000) -> tuple[pd.DataFrame, str, str]:
    """Download a public sheet as CSV and return DataFrame with a hash for caching."""
    sheet_id = extract_sheet_id(sheet_url)
    csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"
    resp = requests.get(csv_url, timeout=30)
    resp.raise_for_status()
    content = resp.text
    df = pd.read_csv(io.StringIO(content)).loc[:max_questions - 1, ['Timestamp', 'Question']]
    modified_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
    return df, sheet_id, modified_hash
