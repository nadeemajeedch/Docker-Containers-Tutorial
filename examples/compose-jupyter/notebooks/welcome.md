# Compose Jupyter workspace

This folder is bind-mounted at `/workspace/notebooks`.

Start from the project directory:

```bash
docker compose up
```

Open `http://localhost:8888`. Files you save here remain on the host after `docker compose down`.
