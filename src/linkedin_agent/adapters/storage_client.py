from pathlib import Path
from typing import List, Dict

from ..utils import excel as excel_utils


class StorageClient:
    def __init__(self, path: Path):
        self.path = path

    def append_records(self, records: List[Dict]) -> None:
        excel_utils.append_rows(self.path, records)

    def read_records(self):
        return excel_utils.read_sheet(self.path)
