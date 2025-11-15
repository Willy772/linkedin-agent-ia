from linkedin_agent.schemas import InvitationFilters, InvitationRequest
from linkedin_agent.services.audit_service import AuditService
from linkedin_agent.services.invitation_service import InvitationService
from linkedin_agent.adapters.candidate_source import CandidateSource
from linkedin_agent.workflows.invitation_workflow import InvitationWorkflow


def test_workflow_filters_and_logs(sample_candidates, tmp_path):
    _, dataset_path = sample_candidates
    excel_path = tmp_path / 'audit.xlsx'
    workflow = InvitationWorkflow(
        InvitationService(CandidateSource(dataset_path)),
        AuditService(excel_path),
    )
    request = InvitationRequest(filters=InvitationFilters(school='ESIGELEC'), message='Bonjour')
    response = workflow.run(request)
    assert response.total_candidates == 1
    assert excel_path.exists()
