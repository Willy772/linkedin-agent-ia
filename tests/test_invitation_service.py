from linkedin_agent.adapters.candidate_source import CandidateSource
from linkedin_agent.services.invitation_service import InvitationService


def test_filter_candidates_by_school(sample_candidates):
    _, dataset_path = sample_candidates
    service = InvitationService(CandidateSource(dataset_path))
    results = service.filter_candidates({'school': 'ESIGELEC'}, None)
    assert len(results) == 1
    assert results[0]['full_name'] == 'Alice Dupont'


def test_send_invitations_appends_status(sample_candidates):
    data, dataset_path = sample_candidates
    service = InvitationService(CandidateSource(dataset_path))
    invitations = service.send_invitations(data)
    assert invitations[0]['status'] == 'queued'
