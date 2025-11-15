from __future__ import annotations

import logging
from typing import Any, Dict

import httpx

logger = logging.getLogger(__name__)


class LinkedInAuthError(RuntimeError):
    """Raised when LinkedIn credentials are missing or invalid."""


class LinkedInApiError(RuntimeError):
    """Raised when LinkedIn returns a non-success status code."""


class LinkedInClient:
    def __init__(
        self,
        base_url: str,
        access_token: str | None,
        client: httpx.Client | None = None,
    ) -> None:
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self._client = client or httpx.Client(base_url=self.base_url, timeout=10.0)

    @property
    def is_configured(self) -> bool:
        return bool(self.access_token)

    def search_people(self, filters: Dict[str, str]) -> list[dict[str, Any]]:
        response = self._client.get(
            '/peopleSearch',
            headers=self._auth_headers(),
            params=self._build_search_params(filters),
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise LinkedInApiError(f'Erreur LinkedIn search_people: {exc.response.text}') from exc

        data = response.json()
        return [self._normalize_profile(elem) for elem in data.get('elements', [])]

    def send_invitation(self, profile_urn: str, message: str | None = None) -> str:
        payload = {
            'invitee': {
                'com.linkedin.voyager.growth.invitation.InviteeProfile': {
                    'profileUrn': profile_urn,
                }
            },
            'message': message or 'Bonjour, connectons-nous sur LinkedIn.',
        }
        response = self._client.post(
            '/invitations',
            headers=self._auth_headers(),
            json=payload,
        )
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            if exc.response.status_code in (401, 403):
                raise LinkedInAuthError('Token LinkedIn invalide ou expiré.') from exc
            raise LinkedInApiError(f'Erreur LinkedIn send_invitation: {exc.response.text}') from exc
        return 'sent'

    def _auth_headers(self) -> Dict[str, str]:
        if not self.access_token:
            raise LinkedInAuthError('Aucun access token LinkedIn configuré.')
        return {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0',
            'Content-Type': 'application/json',
        }

    @staticmethod
    def _build_search_params(filters: Dict[str, str]) -> Dict[str, str]:
        params: Dict[str, str] = {
            'q': 'peopleSearch',
            'count': '25',
        }
        keywords = []
        if title := filters.get('title'):
            keywords.append(title)
        if company := filters.get('company'):
            params['currentCompany'] = company
        if location := filters.get('location'):
            params['geoRegion'] = location
        if school := filters.get('school'):
            params['schools'] = school
        if keywords:
            params['keywords'] = ' '.join(keywords)
        return params

    @staticmethod
    def _normalize_profile(raw: Dict[str, Any]) -> Dict[str, Any]:
        profile = {
            'full_name': raw.get('localizedFirstName', '') + ' ' + raw.get('localizedLastName', ''),
            'title': raw.get('headline'),
            'location': raw.get('locationName'),
            'company': raw.get('companyName'),
            'school': raw.get('schoolName'),
            'profileUrn': raw.get('entityUrn') or raw.get('profileUrn'),
        }
        return {k: v for k, v in profile.items() if v}
