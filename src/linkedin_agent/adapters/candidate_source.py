import json
from pathlib import Path
from typing import Any


class CandidateSource:
    """Charge les candidats depuis un fichier JSON local ou un jeu de données par défaut."""

    def __init__(self, dataset_path: Path, fallback: list[dict[str, Any]] | None = None):
        self.dataset_path = dataset_path
        self._fallback = fallback or []

    def fetch_candidates(self) -> list[dict[str, Any]]:
        if self.dataset_path.exists():
            raw = self.dataset_path.read_text(encoding='utf-8')
            if raw.strip():
                return json.loads(raw)
        return list(self._fallback)
