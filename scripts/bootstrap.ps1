param([switch]$withDev)

python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
if ($withDev) { pip install -e ".[dev]" }
Copy-Item -Path .env.example -Destination .env -ErrorAction SilentlyContinue
Write-Host 'Bootstrap terminé.'
