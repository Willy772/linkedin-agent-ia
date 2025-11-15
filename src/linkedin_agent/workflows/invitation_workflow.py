from pathlib import Path

from ..schemas import InvitationRequest, InvitationResponse
from ..services.invitation_service import InvitationService
from ..services.audit_service import AuditService
from ..adapters.candidate_source import CandidateSource


class InvitationWorkflow:
    def __init__(self, invitation_service: InvitationService, audit_service: AuditService):
        self.invitation_service = invitation_service
        self.audit_service = audit_service

    @classmethod
    def from_settings(cls, settings):
        source = CandidateSource(Path(settings.invitations.dataset_path))
        invitation_service = InvitationService(source)
        audit_service = AuditService(Path(settings.storage.excel_path))
        return cls(invitation_service, audit_service)

    def run(self, request: InvitationRequest) -> InvitationResponse:
        normalized_filters = request.filters.normalized()
        candidates = self.invitation_service.filter_candidates(normalized_filters, request.candidates)
        invitations = self.invitation_service.send_invitations(candidates)
        self.audit_service.log_invitation_batch(normalized_filters, invitations)
        return InvitationResponse(
            total_candidates=len(candidates),
            filters=normalized_filters,
            invitations=invitations,
        )
