from typing import Any, Iterable, List

from ..adapters.candidate_source import CandidateSource
from ..utils.filters import apply_filters


class InvitationService:
    def __init__(self, candidate_source: CandidateSource):
        self.candidate_source = candidate_source

    def filter_candidates(self, filters: dict[str, str], explicit_candidates: Iterable[dict[str, Any]] | None = None) -> List[dict[str, Any]]:
        candidates = list(explicit_candidates) if explicit_candidates is not None else self.candidate_source.fetch_candidates()
        return apply_filters(filters, candidates)

    def send_invitations(self, candidates: List[dict[str, Any]]) -> List[dict[str, Any]]:
        invitations = []
        for candidate in candidates:
            invitations.append({**candidate, 'status': 'queued'})
        return invitations
