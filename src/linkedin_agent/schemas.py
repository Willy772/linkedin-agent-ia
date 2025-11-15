from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str


class InvitationFilters(BaseModel):
    school: Optional[str] = None
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None

    def normalized(self) -> Dict[str, str]:
        data = {}
        for key, value in self.model_dump().items():
            if value:
                data[key] = str(value).strip()
        return data


class InvitationRequest(BaseModel):
    filters: InvitationFilters = Field(default_factory=InvitationFilters)
    candidates: List[Dict[str, Any]] | None = None
    message: Optional[str] = None


class InvitationResponse(BaseModel):
    total_candidates: int
    filters: Dict[str, str]
    invitations: List[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
