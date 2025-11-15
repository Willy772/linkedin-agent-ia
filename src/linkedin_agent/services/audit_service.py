from datetime import datetime
from pathlib import Path
from typing import Dict, List

from ..adapters.storage_client import StorageClient


class AuditService:
    def __init__(self, storage_path: Path):
        self.storage = StorageClient(storage_path)

    def log_invitation_batch(self, filters: Dict[str, str], invitations: List[Dict]) -> None:
        timestamp = datetime.utcnow().isoformat()
        if invitations:
            records = [self._build_record(timestamp, filters, invite) for invite in invitations]
        else:
            records = [self._build_record(timestamp, filters, {})]
        self.storage.append_records(records)

    @staticmethod
    def _build_record(timestamp: str, filters: Dict[str, str], invite: Dict) -> Dict:
        record = {
            'timestamp': timestamp,
            'full_name': invite.get('full_name'),
            'school': invite.get('school'),
            'title': invite.get('title'),
            'company': invite.get('company'),
            'location': invite.get('location'),
        }
        for key, value in filters.items():
            record[f'filter_{key}'] = value
        record['status'] = invite.get('status', 'pending')
        return record
