# AGENTS.md

## Project overview

Nebulus Atom is a privacy-first, self-hosted AI coding assistant and autonomous software engineering agent. It is a Python CLI (Typer, Rich, Textual, Streamlit) that talks to local or OpenAI-compatible LLM servers for code assistance, GitHub issue automation, and multi-agent orchestration (`nebulus_swarm`, including the Overlord control plane).

This repository is licensed under the MIT License; see [LICENSE](LICENSE). Current product version is documented on the README badge (v2.6.0 at the time of this file). Prefer that over `pyproject.toml`, which may lag.

Longer notes: `AI_DIRECTIVES.md` (OOP/SOLID and operational guardrails), `WORKFLOW.md` (git process), `CONTEXT.md` (architectural context), `docs/AI_INSIGHTS.md` (lessons learned).

## Setup and commands

Python 3.12+ is required (`requires-python = ">=3.12"`).

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt   # pytest, ruff, pre-commit, coverage

cp .env.example .env                  # then edit locally; never commit it

# Run the CLI
python3 -m nebulus_atom.main start
# After an editable install, the console scripts are also:
#   nebulus-atom   # or: mn
```

Entry point: `nebulus_atom/main.py` (`[project.scripts]` maps `nebulus-atom` and `mn` to `nebulus_atom.main:app`).

Environment variable names (values belong in `.env`, not here): `NEBULUS_BASE_URL`, `NEBULUS_API_KEY`, `NEBULUS_MODEL`, `NEBULUS_TIMEOUT`, `NEBULUS_STREAMING`, `COMPOSE_PROJECT_NAME`. The historical docs default for the LLM server is `http://localhost:5000/v1`; always prefer what is configured in `.env`.

```bash
# Tests
pytest tests/ -v --tb=short

# Lint / format (ruff is the project linter; also used in CI)
ruff check nebulus_atom/ nebulus_swarm/ tests/
ruff format --check nebulus_atom/ nebulus_swarm/ tests/

# Pre-commit (if installed)
pre-commit run --all-files
```

There is no root Makefile. Docker files (`Dockerfile`, `docker-compose.yml`, `docker-compose.swarm.yml`) exist for container/swarm workflows; use them when working on those paths.

## Build, test, and lint

- Tests live in `tests/`. CI (`.github/workflows/unittests.yml`) runs on `main` and `develop`: `ruff check`, `ruff format --check`, then `pytest tests/ -v --tb=short --cov=nebulus_atom --cov=nebulus_swarm`.
- Docs deploy (`.github/workflows/docs.yml`) runs `mkdocs gh-deploy` on pushes to `main` only. Do not trigger or alter that workflow unless asked.
- Test counts in the README and older notes differ (the README badge, tree comment, and Overlord tables are not always in sync). Trust a fresh `pytest` run over a badge.
- Add or update tests for the code you change. Keep the suite green before calling work done.

## Code style

- Python 3.12+, type hints on new functions, Google-style docstrings on public modules.
- Strict MVC: `nebulus_atom/models/`, `views/`, `controllers/`, `services/`. Do not bury business logic in the CLI entry point.
- Follow `AI_DIRECTIVES.md`. Prefer the smallest change that works.
- Ruff is configured via pre-commit (`ruff` and `ruff-format`). Do not run a surprise repo-wide reformat unless asked; CI already checks formatting.

## Git workflow

- Branch off `develop`. Conventional commits (`feat:`, `fix:`, `docs:`, `chore:`).
- Merge with `--no-ff`. Never commit straight to `main` or `develop`.
- Keep feature branches local until Jason approves a push or pull request. Do not push, publish, or open a PR unless he asked for that specific action.
- `main` and `develop` have diverged in this repo; do not merge them unless he asks.
- The default integration remote is `origin` (`git@github.com:westailabs/nebulus-atom.git`), not a `nebulus-atom` remote name.

## Security and privacy

- Never commit secrets, tokens, or `.env` files. Name environment variables only; never print values.
- Never read vault files or `~/.config/neo4j-shared.env`.
- No proprietary O'Reilly data in this repo or in agent context. Pattern-level problems only.
- Ask before installing packages, changing remotes, merging, pushing, or restarting services.

## Agent boundaries

- Implement, fix, and test. Do not invent project priorities or expand scope.
- When user-facing features, version badges, or key metrics change, update `README.md` first. The GitHub wiki is a separate repo; older notes disagree on the local path (`/tmp/nebulus-atom-wiki` vs `nebulus-atom.wiki/`) and on whether wiki default is `master` or `main`. Do not clone, commit, or push the wiki unless asked.
- Record durable lessons in `docs/AI_INSIGHTS.md`.

Overlord (meta-orchestrator under `nebulus_swarm/overlord/`) is an active part of this tree. Useful CLI groups include `overlord`, `queue`, `dispatch`, and `focus`. Some roadmap phases were still marked planned in prior notes (Gantry visual control plane, observability); check the code before treating a phase as done or missing.

## Nebulus shared services

- Shared RAG in the West AI Labs ecosystem is `shared-rag` on port **8002**. The old **shared** ChromaDB on port 8001 is retired.
- Atom may still use the `chromadb` Python package for **its own** semantic code search / RAG. That is local product memory, not the retired shared service.
- Gantry integration and Overlord routing are optional companions, not a requirement to work on the CLI.

## Key files and directories

| Path | Purpose |
|------|---------|
| `nebulus_atom/main.py` | CLI entry point |
| `nebulus_atom/` | Core agent (MVC) |
| `nebulus_swarm/overlord/` | Meta-orchestrator and control plane |
| `nebulus_swarm/` | Swarm, minions, dashboard, reviewer |
| `tests/` | Pytest suite |
| `requirements.txt` / `requirements-dev.txt` | Runtime and test/lint deps |
| `pyproject.toml` | Packaging, console scripts, pytest/coverage config |
| `docker-compose.yml` / `docker-compose.swarm.yml` | Container workflows |

## Generated or restricted files

- Do not commit `.env`, `.venv/`, `.nebulus_atom/`, or `site/`.
- `.gemini/` is gitignored except for `.gemini/settings.json`, which should be committed so Gemini CLI reads `AGENTS.md`.
- `.aider.conf.yml` should read `AGENTS.md` and `CONTEXT.md`. There is no `rules/ai_behavior.md` in this tree; do not resurrect that path.
