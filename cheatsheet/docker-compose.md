# Cheatsheet: Docker Compose

[Course Home](../README.md) · [Complete cheatsheet](complete-docker-cheatsheet.md)

Lessons: [18](../lessons/18-docker-compose.md) · [19](../lessons/19-python-jupyter-compose.md)

Use `docker compose` (space), not `docker-compose` (hyphen).

---

## Daily commands

```bash
docker compose version
docker compose up
docker compose up -d
docker compose up --build
docker compose up -d --build
docker compose ps
docker compose logs
docker compose logs -f jupyter
docker compose exec jupyter python --version
docker compose run --rm jupyter python src/analyze.py
docker compose down
docker compose config
```

Same in **PowerShell**.

---

## Minimal compose.yaml

```yaml
services:
  jupyter:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/workspace/notebooks
```

| Key | Meaning |
|-----|---------|
| `services` | Named containers |
| `build` | Build from Dockerfile in that path |
| `ports` | `host:container` |
| `volumes` | Bind mounts or named volumes |
| `environment` | Env vars in the container |
| `env_file` | File loaded into the container |
| `profiles` | Optional services |
| `depends_on` | Start order (not a full health wait) |

---

## Profiles

```bash
docker compose --profile notebook up jupyter
docker compose --profile script run --rm analyze
```

---

## Project name

```bash
docker compose -p course-jupyter up -d
docker compose -p course-jupyter down
```

---

## Reminders

- Run Compose from the directory that contains `compose.yaml`.
- `down` does not delete bind-mounted notebooks.
- `exec` needs a running service; `run` starts a new container.
