# Contributing

## Git workflow

- Branch off `develop`.
- Use conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).
- Merge with `--no-ff`. Never commit straight to `main` or `develop`.
- Keep feature branches local until the maintainer approves a push or pull request.

## Checks

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
ruff check nebulus_atom/ nebulus_swarm/ tests/
ruff format --check nebulus_atom/ nebulus_swarm/ tests/
pytest tests/ -v --tb=short
```

More context for coding agents is in `AGENTS.md`.
