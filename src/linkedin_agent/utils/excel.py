from pathlib import Path
import pandas as pd
from typing import List, Dict


def append_rows(path: Path, rows: List[Dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    df_new = pd.DataFrame(rows)
    if path.exists():
        existing = pd.read_excel(path)
        df_new = pd.concat([existing, df_new], ignore_index=True)
    df_new.to_excel(path, index=False)


def append_row(path: Path, row: Dict) -> None:
    append_rows(path, [row])


def read_sheet(path: Path) -> pd.DataFrame:
    return pd.read_excel(path) if path.exists() else pd.DataFrame()
