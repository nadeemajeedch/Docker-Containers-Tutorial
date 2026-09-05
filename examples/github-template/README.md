# GitHub-ready academic project template

Copy this folder when you start a course project you will push to GitHub.

Lessons: [29](../../lessons/29-docker-and-github.md), [30](../../lessons/30-reproducible-academic-projects.md), [31](../../lessons/31-final-project.md)

## Reproduce after clone

```bash
docker compose up --build
```

Open `http://localhost:8888`.

## What to commit

Commit: `Dockerfile`, `compose.yaml`, `requirements.txt`, `.dockerignore`, `.gitignore`, `.env.example`, `README.md`, `src/`, `notebooks/`, `data/` (if the dataset is small and redistributable), `tests/`.

Do **not** commit: `.env` with secrets, `.venv`, model weights that are huge unless the assignment requires them, API keys.

## Workflow

```text
Create project
↓
Dockerize (Dockerfile + compose.yaml)
↓
Test locally (compose up / run scripts)
↓
Git commit
↓
Push to GitHub
↓
Classmate clones
↓
docker compose up --build
```
