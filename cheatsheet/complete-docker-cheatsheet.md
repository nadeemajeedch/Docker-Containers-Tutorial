# Complete Docker Cheatsheet

Course-wide index. Full explanations live in the lessons.

[Course Home](../README.md)

---

## Part 1 — Engine and CLI

See also: [Part 1 sheet](../cheatsheet.md)

```bash
docker --help
docker version
docker info
docker pull python:3.12
docker images
docker run --rm python:3.12 python --version
docker run -it --rm python:3.12
docker ps
docker ps -a
docker start / stop / restart / rm / rmi
docker logs
docker exec
docker inspect
docker cp
docker rename
docker stats --no-stream
docker system df
docker system prune
```

---

## Part 2 — Python, Dockerfile, Jupyter

See also: [python-docker](python-docker.md) · [dockerfile](dockerfile.md) · [jupyter-docker](jupyter-docker.md)

```bash
docker build -t my-python-app .
docker run --rm my-python-app
docker run --rm -v "$PWD":/app -w /app python:3.12 python hello.py
docker run --rm -p 8888:8888 -v "$PWD/notebooks":/home/jovyan/work course-jupyter:1.0
```

PowerShell bind mount: `-v "${PWD}:/app"`

---

## Part 3 — Compose, networks, projects

See also: [compose](docker-compose.md) · [networking](networking.md) · [troubleshooting](troubleshooting.md) · [best practices](best-practices.md)

```bash
docker compose version
docker compose up --build
docker compose up -d
docker compose ps
docker compose logs
docker compose exec jupyter python --version
docker compose down
```

**localhost in a container is not localhost on the host.** Use Compose service names between containers.

```bash
docker run --rm -e STUDENT_NAME=ada python:3.12 python -c "import os; print(os.environ['STUDENT_NAME'])"
docker volume ls
docker network ls
```

---

## Examples

| Path | Topic |
|------|--------|
| `examples/hello-python` | Bind-mount script |
| `examples/python-docker-project` | Dockerfile app |
| `examples/jupyter-project` | Custom Jupyter `docker run` |
| `examples/compose-jupyter` | Compose Jupyter |
| `examples/networking-demo` | Service DNS |
| `examples/data-science-docker` | DS environment |
| `examples/ml-docker` | Train + optional Jupyter |
| `examples/github-template` | GitHub skeleton |
| `examples/final-project` | Capstone starter |
