from linkedin_agent.adapters.candidate_source import CandidateSource
from linkedin_agent.services.invitation_service import InvitationService


class DummyLinkedInClient:
    def __init__(self):
        self.is_configured = True
        self.sent_to = []

    def send_invitation(self, profile_urn, message=None):
        self.sent_to.append((profile_urn, message))
        return 'sent'


def test_filter_candidates_by_school(sample_candidates):
    data, dataset_path = sample_candidates
    service = InvitationService(CandidateSource(dataset_path))
    results = service.filter_candidates({'school': 'ESIGELEC'}, data)
    assert len(results) == 1
    assert results[0]['full_name'] == 'Alice Dupont'


def test_send_invitations_with_linkedin_client(sample_candidates):
    data, dataset_path = sample_candidates
    linkedin_client = DummyLinkedInClient()
    for candidate in data:
        candidate['profileUrn'] = f"urn:li:person:{candidate['full_name'].replace(' ', '').lower()}"
    service = InvitationService(CandidateSource(dataset_path, linkedin_client), linkedin_client)
    invitations = service.send_invitations(data, message='Hello')
    assert invitations[0]['status'] == 'sent'
    assert linkedin_client.sent_to[0][1] == 'Hello'
