import json
from pathlib import Path
import typer

from .config import load_settings
from .schemas import InvitationFilters, InvitationRequest
from .workflows.invitation_workflow import InvitationWorkflow

cli = typer.Typer(help='Workflow CLI pour envoyer des invitations LinkedIn basées sur des filtres.')


def _build_request(
    school: str | None,
    title: str | None,
    company: str | None,
    location: str | None,
    candidates_file: Path | None,
) -> InvitationRequest:
    filters = InvitationFilters(school=school, title=title, company=company, location=location)
    candidates = None
    if candidates_file:
        data = json.loads(candidates_file.read_text(encoding='utf-8'))
        if not isinstance(data, list):
            raise typer.BadParameter('Le fichier de candidats doit contenir une liste de profils.')
        candidates = data
    return InvitationRequest(filters=filters, candidates=candidates)


@cli.command('send-invitations')
def send_invitations(
    config: Path | None = typer.Option(None, '--config', '-c', help='Chemin vers un fichier YAML de configuration.'),
    school: str | None = typer.Option(None, help="Filtrer par école (ex: ESIGELEC)."),
    title: str | None = typer.Option(None, help="Filtrer par titre de poste."),
    company: str | None = typer.Option(None, help="Filtrer par entreprise."),
    location: str | None = typer.Option(None, help="Filtrer par localisation (ex: Ile-de-France)."),
    candidates_file: Path | None = typer.Option(None, help='Fichier JSON contenant des candidats à la place de la source par défaut.'),
):
    """Lance la préparation d'invitations et journalise le suivi dans Excel."""

    settings = load_settings(config)
    workflow = InvitationWorkflow.from_settings(settings)
    request = _build_request(school, title, company, location, candidates_file)
    response = workflow.run(request)
    typer.echo(f"{response.total_candidates} invitation(s) préparée(s).")
    typer.echo(f"Journal Excel: {settings.storage.excel_path}")


if __name__ == '__main__':
    cli()
