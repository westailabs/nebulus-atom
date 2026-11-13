# Project Workflow (Nebulus Standard)

## Branching Strategy

We follow a strict **Gitflow-lite** workflow.

### Permanent Branches (Remote)
- **`main`**: Production-ready code.
- **`develop`**: Integration branch for the next release. **All work merges here.**

### Temporary Branches (Local Only)
These branches should stay on your local machine until the maintainer approves a push or pull request.

- **`feat/name`**: New features (models, services, UI).
- **`fix/description`**: Bug fixes.
- **`docs/description`**: Documentation updates.
- **`chore/description`**: Maintenance, config, refactoring.

## Workflow Steps

1.  **Start**: Checkout `develop` and pull latest (only when a pull has been approved).
    ```bash
    git checkout develop
    git pull origin develop
    ```
2.  **Branch**: Create a specific local branch.
    ```bash
    git checkout -b feat/my-new-feature
    ```
3.  **Work**: Implement changes using **Conventional Commits**.
    ```bash
    git commit -m "feat: add new OpenAI service"
    ```
4.  **Verify**: Run tests/start app to ensure stability.
5.  **Merge**: Switch back to `develop` and merge with `--no-ff` after approval.
    ```bash
    git checkout develop
    git merge --no-ff feat/my-new-feature
    ```
6.  **Push**: Push **only** with explicit authorization, and only `develop` unless asked otherwise.
    ```bash
    git push origin develop
    ```
7.  **Cleanup**: Delete the local branch.
    ```bash
    git branch -d feat/my-new-feature
    ```

## Feature Documentation
All planned features must be documented in `docs/features/` using the `docs/feature_template.md`.
Refer to these documents for branch names, requirements, and verification plans before starting work.
