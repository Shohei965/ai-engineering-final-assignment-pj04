import json
from pathlib import Path
from typing import Any, Dict, List


CACHE_DIR = Path('.cache')
CACHE_DIR.mkdir(exist_ok=True)


def load_cache(sheet_id: str, modified_time: str) -> List[Dict[str, Any]] | None:
    cache_file = CACHE_DIR / f'{sheet_id}_{modified_time}.json'
    if cache_file.exists():
        with cache_file.open('r', encoding='utf-8') as f:
            return json.load(f)
    return None


def save_cache(sheet_id: str, modified_time: str, data: List[Dict[str, Any]]) -> None:
    cache_file = CACHE_DIR / f'{sheet_id}_{modified_time}.json'
    with cache_file.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
