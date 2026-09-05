# Custom Jupyter project

JupyterLab image with NumPy, Pandas, Matplotlib, and scikit-learn.

Lessons: [15](../../lessons/15-running-jupyter-with-docker.md), [16](../../lessons/16-custom-jupyter-image.md), [17](../../lessons/17-jupyter-project.md)

## Files

- `Dockerfile` — JupyterLab on `python:3.12-slim`
- `requirements.txt` — JupyterLab plus the scientific stack
- `notebooks/` — bind-mounted into the container so work is saved on the host
- `.dockerignore` — keeps the build context small

## Build

From this directory:

```bash
docker build -t course-jupyter:1.0 .
```

**Windows PowerShell:** the same command.

## Run (Linux / macOS)

```bash
docker run --rm -p 8888:8888 \
  -v "$PWD/notebooks":/home/jovyan/work \
  --name course-jupyter \
  course-jupyter:1.0
```

Open a browser at `http://localhost:8888`. This image starts JupyterLab with an empty token for local class use. Do not expose it to the public internet.

## Run (Windows PowerShell)

```powershell
docker run --rm -p 8888:8888 `
  -v "${PWD}\notebooks:/home/jovyan/work" `
  --name course-jupyter `
  course-jupyter:1.0
```

If `${PWD}` does not resolve in your PowerShell version, use a full path:

```powershell
docker run --rm -p 8888:8888 -v "C:\path\to\examples\jupyter-project\notebooks:/home/jovyan/work" --name course-jupyter course-jupyter:1.0
```

## Persistence

Notebooks you save in JupyterLab appear under `notebooks/` on the host. Stopping the container does not delete those files.

## Stop

In the terminal that is attached to `docker run`, press Ctrl+C. If you started it detached (`-d`), run:

```bash
docker stop course-jupyter
```
