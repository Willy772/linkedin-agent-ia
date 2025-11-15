from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any, Dict, List

from .linkedin_client import LinkedInAuthError, LinkedInClient

logger = logging.getLogger(__name__)


class CandidateSource:
    """Charge les candidats depuis LinkedIn ou un fichier local de secours."""

    def __init__(self, dataset_path: Path, linkedin_client: LinkedInClient | None = None):
        self.dataset_path = dataset_path
        self.linkedin_client = linkedin_client

    def fetch_candidates(self, filters: Dict[str, str]) -> List[Dict[str, Any]]:
        if self.linkedin_client and self.linkedin_client.is_configured:
            try:
                return self.linkedin_client.search_people(filters)
            except LinkedInAuthError as exc:
                logger.warning('LinkedInAuthError, utilisation du dataset local : %s', exc)
        return self._load_local_dataset()

    def _load_local_dataset(self) -> List[Dict[str, Any]]:
        if not self.dataset_path.exists():
            return []
        raw = self.dataset_path.read_text(encoding='utf-8').strip()
        if not raw:
            return []
        return json.loads(raw)
