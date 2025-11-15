from __future__ import annotations

from typing import Any, Iterable, List

from ..adapters.candidate_source import CandidateSource
from ..adapters.linkedin_client import LinkedInClient
from ..utils.filters import apply_filters


class InvitationService:
    def __init__(self, candidate_source: CandidateSource, linkedin_client: LinkedInClient | None = None):
        self.candidate_source = candidate_source
        self.linkedin_client = linkedin_client

    def filter_candidates(
        self,
        filters: dict[str, str],
        explicit_candidates: Iterable[dict[str, Any]] | None = None,
    ) -> List[dict[str, Any]]:
        candidates = list(explicit_candidates) if explicit_candidates is not None else self.candidate_source.fetch_candidates(filters)
        return apply_filters(filters, candidates)

    def send_invitations(self, candidates: List[dict[str, Any]], message: str | None = None) -> List[dict[str, Any]]:
        invitations = []
        for candidate in candidates:
            status = 'pending'
            if self.linkedin_client and self.linkedin_client.is_configured:
                profile_urn = (
                    candidate.get('profileUrn')
                    or candidate.get('profile_urn')
                    or candidate.get('entityUrn')
                )
                if profile_urn:
                    try:
                        status = self.linkedin_client.send_invitation(profile_urn, message)
                    except Exception as exc:  # pragma: no cover
                        status = f'error:{exc.__class__.__name__}'
                else:
                    status = 'missing_profile_urn'
            invitations.append({**candidate, 'status': status})
        return invitations
