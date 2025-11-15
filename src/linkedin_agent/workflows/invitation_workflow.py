from __future__ import annotations

from pathlib import Path

from ..schemas import InvitationRequest, InvitationResponse
from ..services.invitation_service import InvitationService
from ..services.audit_service import AuditService
from ..adapters.candidate_source import CandidateSource
from ..adapters.linkedin_client import LinkedInClient


class InvitationWorkflow:
    def __init__(self, invitation_service: InvitationService, audit_service: AuditService):
        self.invitation_service = invitation_service
        self.audit_service = audit_service

    @classmethod
    def from_settings(cls, settings):
        linkedin_client = None
        if settings.linkedin.access_token:
            linkedin_client = LinkedInClient(
                base_url=settings.linkedin.base_url,
                access_token=settings.linkedin.access_token,
            )
        source = CandidateSource(Path(settings.invitations.dataset_path), linkedin_client)
        invitation_service = InvitationService(source, linkedin_client)
        audit_service = AuditService(Path(settings.storage.excel_path))
        return cls(invitation_service, audit_service)

    def run(self, request: InvitationRequest) -> InvitationResponse:
        normalized_filters = request.filters.normalized()
        candidates = self.invitation_service.filter_candidates(normalized_filters, request.candidates)
        invitations = self.invitation_service.send_invitations(candidates, request.message)
        self.audit_service.log_invitation_batch(normalized_filters, invitations)
        return InvitationResponse(
            total_candidates=len(candidates),
            filters=normalized_filters,
            invitations=invitations,
        )
