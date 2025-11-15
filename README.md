# LinkedIn Agent IA

Agent IA Python focalisé sur l’envoi d’invitations LinkedIn en fonction de critères (école, titre, entreprise, localisation) et sur la génération d’un fichier Excel de suivi. L’architecture reste modulaire pour ajouter d’autres tâches plus tard.

## Fonctionnalités actuelles
- API Flask exposant `POST /invitations` pour filtrer les profils et préparer les invitations.
- CLI Typer (`typer linkedin_agent.cli send-invitations ...`) pour tester les filtres en local.
- Source de données candidates basée sur un fichier JSON (modifiable) et service de log Excel.
- Suivi détaillé des invitations dans `data/outputs/invitations.xlsx` avec horodatage + critères utilisés.
- Tests Pytest + pipeline CI GitHub Actions (lint, format, tests) pour garantir la qualité.

## Stack
- Python 3.11
- Flask + Uvicorn/Gunicorn possibles pour le déploiement
- Pandas/OpenPyXL pour le suivi Excel
- Typer pour la CLI

## Prérequis
```bash
python -m venv .venv
source .venv/bin/activate  # ou .\.venv\Scripts\Activate.ps1
pip install -e .
cp .env.example .env
```

## Configuration
- `config/settings.yaml` : chemins, options Flask, dataset.
- `.env` : surcharge possible (`INVITATION_DATASET_PATH`, etc.).
- `data/inputs/candidates.sample.json` : exemple de base de prospects.

## Lancer en local
```bash
# API Flask
flask --app linkedin_agent.app run --debug

# Workflow via CLI
typer linkedin_agent.cli send-invitations \
  --school "ESIGELEC" \
  --location "Ile-de-France"
```

`POST /invitations` attend un corps JSON :
```json
{
  "filters": {
    "school": "ESIGELEC",
    "title": "Ingénieur",
    "company": "Startup",
    "location": "Ile-de-France"
  },
  "candidates": [
    {"full_name": "Alice", "school": "ESIGELEC", "title": "Ingénieur", "company": "Startup", "location": "Ile-de-France"}
  ]
}
```

La réponse contient `total_candidates`, `filters` normalisés et la liste des invitations préparées.

## CI/CD
`make ci` exécute lint (`ruff`), formatage (`black`) et tests (`pytest`). Le workflow `.github/workflows/ci.yml` rejoue la même suite sur GitHub Actions.

## Roadmap
1. Ajouter la connexion à l’API LinkedIn ou à un agent Hugging Face gratuit.
2. Étendre l’agent à la génération de posts ou à la veille d’offres.
3. Automatiser les validations humaines (boutons e-mail) dans une future itération.
