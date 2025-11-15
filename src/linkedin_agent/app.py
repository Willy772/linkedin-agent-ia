from flask import Flask, jsonify, request
from pydantic import ValidationError

from .config import get_settings
from .schemas import HealthResponse, InvitationRequest
from .workflows.invitation_workflow import InvitationWorkflow

app = Flask(__name__)


def _workflow() -> InvitationWorkflow:
    settings = get_settings()
    return InvitationWorkflow.from_settings(settings)


@app.get('/health')
def health():
    return jsonify(HealthResponse(status='ok').model_dump())


@app.post('/invitations')
def create_invitations():
    payload = request.get_json(silent=True) or {}
    try:
        invitation_request = InvitationRequest.model_validate(payload)
    except ValidationError as exc:
        return jsonify({'errors': exc.errors()}), 400

    workflow = _workflow()
    response = workflow.run(invitation_request)
    return jsonify(response.model_dump())
