# Cheatsheet: Python in Docker

[Course Home](../README.md) · [Dockerfile cheatsheet](dockerfile.md) · [Jupyter cheatsheet](jupyter-docker.md)

Lessons: [9](../lessons/09-running-python-with-docker.md) · [11](../lessons/11-building-python-images.md) · [12](../lessons/12-python-dependencies.md) · [14](../lessons/14-volumes-and-bind-mounts.md)

Commands are the same in **PowerShell** and **bash/zsh** except where paths are shown.

---

## Interpreter (official image)

```bash
docker pull python:3.12
docker run --rm python:3.12 python --version
docker run -it --rm python:3.12
docker run --rm python:3.12 python -c "print(2+2)"
```

---

## Run a host script (bind mount)

**Linux / macOS** (from the folder that contains `hello.py`):

```bash
docker run --rm -v "$PWD":/app -w /app python:3.12 python hello.py
```

**PowerShell:**

```powershell
docker run --rm -v "${PWD}:/app" -w /app python:3.12 python hello.py
```

Sample file: `examples/hello-python/hello.py`

---

## Build and run the course app

```bash
cd examples/python-docker-project
docker build -t my-python-app .
docker run --rm my-python-app
docker run --rm my-python-app python --version
docker run --rm my-python-app pip list
docker run --rm my-python-app pip freeze
```

---

## Dependencies

In a Dockerfile:

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

Course packages: numpy, pandas, matplotlib, scikit-learn (see `examples/python-docker-project/requirements.txt`).

Host `pip install` does **not** change the container.

---

## Persist a file

Named volume:

```bash
docker volume create py-work
docker run --rm -v py-work:/work python:3.12 python -c "open('/work/note.txt','w').write('hi\n')"
docker run --rm -v py-work:/work python:3.12 cat /work/note.txt
docker volume ls
docker volume rm py-work
```

`--mount` bind:

```bash
docker run --rm --mount type=bind,source="$PWD",target=/app -w /app python:3.12 python hello.py
```

PowerShell `--mount`:

```powershell
docker run --rm --mount "type=bind,source=${PWD},target=/app" -w /app python:3.12 python hello.py
```

---

## Reminders

- `python` in these commands is inside the image, not the host.
- Rebuild after Dockerfile or `requirements.txt` changes.
- Do not keep the only copy of homework in a `--rm` container without a mount.
