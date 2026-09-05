# Cheatsheet: Dockerfiles

[Course Home](../README.md) · [Python cheatsheet](python-docker.md) · [Jupyter cheatsheet](jupyter-docker.md)

Lessons: [10](../lessons/10-dockerfile.md) · [11](../lessons/11-building-python-images.md) · [13](../lessons/13-dockerignore.md)

---

## Build and run

```bash
docker build -t my-python-app .
docker build -t my-python-app:1.0 -t my-python-app:latest .
docker run --rm my-python-app
docker run --rm my-python-app python --version
```

`.` is the **build context**. Run these from the directory that contains the Dockerfile, or pass `-f` and a context path.

---

## Instruction map

| Instruction | When it runs | Notes |
|-------------|--------------|--------|
| `FROM` | Build | Base image; pin a tag |
| `WORKDIR` | Build | Creates the directory if needed |
| `COPY` | Build | From context into the image; prefer over `ADD` |
| `ADD` | Build | Extra tar/URL behavior; avoid unless needed |
| `RUN` | **Build** | `pip install`, `useradd` |
| `CMD` | **Start** | Default command; easy to override |
| `ENTRYPOINT` | **Start** | Fixed program; `run` args append |
| `ENV` | Build + start | Persisted environment |
| `EXPOSE` | Docs only | Does not publish; use `docker run -p` |
| `USER` | Build + start | Later steps and the main process |
| `ARG` | Build | `docker build --build-arg`; not in the runtime env unless copied to `ENV` |

Exec form (preferred for `CMD`):

```dockerfile
CMD ["python", "main.py"]
```

---

## Course Python Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Copy `requirements.txt` **before** `COPY . .` so pip layers cache when you only edit `main.py`.

---

## .dockerignore (minimum)

```text
.git
__pycache__
*.pyc
.venv
venv
.env
.DS_Store
Thumbs.db
.ipynb_checkpoints
```

Does not affect bind mounts at `docker run`.

---

## Cache

- Unchanged instructions reuse layers (`CACHED` in build output).
- Changing `requirements.txt` reinstalls pip packages.
- Changing only `main.py` should reuse `RUN pip install`.
