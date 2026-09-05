# Cheatsheet: Best Practices

[Course Home](../README.md) · Lessons: [25](../lessons/25-best-practices.md) · [26](../lessons/26-security.md) · [28](../lessons/28-image-optimization.md)

---

## Images

- Official bases: `python:3.12-slim` for projects
- Never rely on `python:latest` for graded work
- `COPY requirements.txt` then `RUN pip install --no-cache-dir`
- Then `COPY` source
- `.dockerignore`: `.git`, `.venv`, `.env`, `__pycache__`, checkpoints

---

## Runtime

- Bind-mount notebooks, data, results
- Libraries live in the image
- Non-root `USER` for Jupyter
- Publish only needed ports
- No `--privileged`
- Empty Jupyter token: localhost only

---

## GitHub

- Commit: Dockerfile, compose.yaml, requirements.txt, README, dockerignore, gitignore, `.env.example`
- Do not commit: `.env` secrets, venvs, huge binaries
- README first command: `docker compose up --build`

---

## Pre-push

```text
[ ] pinned FROM
[ ] requirements pinned or ranged
[ ] .dockerignore
[ ] no secrets in git status
[ ] compose README
[ ] mounts for work
[ ] non-root server
```
