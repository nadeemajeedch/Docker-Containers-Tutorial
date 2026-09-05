# Compose Jupyter

Single-service JupyterLab stack for Lessons 18 and 19.

Lessons: [18](../../lessons/18-docker-compose.md), [19](../../lessons/19-python-jupyter-compose.md)

## Run

From this directory:

```bash
docker compose up --build
```

**Windows PowerShell:** the same command.

Open `http://localhost:8888`. Empty token is for local class use only.

Detached:

```bash
docker compose up -d --build
docker compose ps
docker compose logs
docker compose down
```

Notebooks in `./notebooks` persist on the host.
