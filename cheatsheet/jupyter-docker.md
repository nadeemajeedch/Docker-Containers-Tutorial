# Cheatsheet: Jupyter in Docker

[Course Home](../README.md) · [Python cheatsheet](python-docker.md) · [Dockerfile cheatsheet](dockerfile.md)

Lessons: [15](../lessons/15-running-jupyter-with-docker.md) · [16](../lessons/16-custom-jupyter-image.md) · [17](../lessons/17-jupyter-project.md)

---

## Official base (token in logs)

**Linux / macOS:**

```bash
mkdir -p "$HOME/jupyter-docker-work"
docker pull quay.io/jupyter/base-notebook:python-3.12
docker run --rm -p 8888:8888 \
  -v "$HOME/jupyter-docker-work":/home/jovyan/work \
  --name jupyter-lab \
  quay.io/jupyter/base-notebook:python-3.12
```

**PowerShell:**

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\jupyter-docker-work"
docker run --rm -p 8888:8888 `
  -v "${HOME}\jupyter-docker-work:/home/jovyan/work" `
  --name jupyter-lab `
  quay.io/jupyter/base-notebook:python-3.12
```

Open the URL with `token=` from the terminal or:

```bash
docker logs jupyter-lab
```

Browser: `http://localhost:8888` (host port is the **left** number in `-p`).

If Quay is blocked, try `jupyter/base-notebook` on Docker Hub with a version tag your instructor specifies.

This base image may **not** include pandas. Use the custom image below for the course stack.

---

## Custom course image

```bash
cd examples/jupyter-project
docker build -t course-jupyter:1.0 .
```

**Linux / macOS:**

```bash
docker run --rm -p 8888:8888 \
  -v "$PWD/notebooks":/home/jovyan/work \
  --name course-jupyter \
  course-jupyter:1.0
```

**PowerShell:**

```powershell
docker run --rm -p 8888:8888 `
  -v "${PWD}\notebooks:/home/jovyan/work" `
  --name course-jupyter `
  course-jupyter:1.0
```

Browse `http://localhost:8888`. The sample `CMD` uses an **empty token for local class use only**.

Includes JupyterLab, NumPy, Pandas, Matplotlib, scikit-learn.

---

## Ports

| Flag | Meaning |
|------|---------|
| `-p 8888:8888` | Host 8888 → container 8888 |
| `-p 8889:8888` | Browser uses **8889** |

`EXPOSE` in a Dockerfile does not publish a port.

Jupyter must listen on `0.0.0.0` inside the container (`--ip=0.0.0.0`).

---

## Persist / stop

- Notebooks: bind-mount a host folder to `/home/jovyan/work`.
- Foreground: Ctrl+C.
- Detached: `docker stop course-jupyter` then `docker start course-jupyter`.
- `--rm` deletes the **container**, not the bind-mounted host files.

---

## Do not

- Run Jupyter without `-p` and expect the host browser to work.
- Keep the only copy of a notebook in an unmounted `--rm` container.
- Expose an empty-token Jupyter server on the public internet.
- Mount the entire repository over interpreter paths; mount `notebooks/` onto `work`.
