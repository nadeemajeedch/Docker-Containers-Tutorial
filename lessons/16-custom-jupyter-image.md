# Lesson 16: Custom Jupyter Image

The base Jupyter image has no pandas. This lesson builds `examples/jupyter-project`: JupyterLab plus NumPy, Pandas, Matplotlib, and scikit-learn on `python:3.12-slim`.

[← Previous Lesson](15-running-jupyter-with-docker.md)
[Course Home](../README.md)
[Next Lesson →](17-jupyter-project.md)

---

## Learning Objectives

After this lesson you will be able to:

- Read the custom Jupyter Dockerfile and explain `USER`, `EXPOSE`, `ENV`, and `CMD`.
- Build `course-jupyter:1.0` from `examples/jupyter-project`.
- Run it with port 8888 and a bind mount of `notebooks/`.
- Import numpy, pandas, matplotlib, and sklearn in a notebook.
- Contrast this image with `quay.io/jupyter/base-notebook`.

---

## Prerequisites

- Lessons 10–15.
- Disk space for pip packages (first build downloads wheels).
- Port 8888 free, or use another host port.

---

## Concept

Two ways to get a scientific Jupyter:

| Approach | How | Tradeoff |
|----------|-----|----------|
| Jupyter Docker Stacks (`scipy-notebook`, etc.) | Pull a large official stack | Fast to start; less control; image size |
| **Custom image (this lesson)** | `FROM python:3.12-slim` + `requirements.txt` | You choose packages and Python tag; you maintain the Dockerfile |

This course builds a small custom image so the skills from Lessons 10–13 transfer to Jupyter.

Project layout:

```text
examples/jupyter-project/
├── Dockerfile
├── requirements.txt
├── .dockerignore
├── notebooks/
│   ├── 01-check-stack.ipynb
│   └── welcome.md
└── README.md
```

Notebooks stay on the host via a bind mount. They are **not** the thing you bake into the image (you could `COPY` them, but then editing would need rebuilds). The image is the **runtime**. The mount is the **work**.

---

## Explanation

Course Dockerfile (abbreviated comments here; the file itself has no comments):

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /home/jovyan/work

RUN useradd --create-home --uid 1000 --shell /bin/bash jovyan \
    && chown -R jovyan:jovyan /home/jovyan

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

USER jovyan
WORKDIR /home/jovyan/work

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token="]
```

| Piece | Why |
|-------|-----|
| `python:3.12-slim` | Same family as the CLI app; pip-based |
| `useradd jovyan` | Matches Jupyter Stacks naming; not root |
| `pip install -r requirements.txt` | jupyterlab, numpy, pandas, matplotlib, scikit-learn |
| `USER jovyan` | Container process is not root |
| `EXPOSE 8888` | Documents the port |
| `--ip=0.0.0.0` | Listen on all interfaces so `-p` works (not only localhost *inside* the container) |
| `--no-browser` | No browser inside the container |
| `--ServerApp.token=` | **Empty token for local student use.** Do not publish this port to the internet. |

Why `--ip=0.0.0.0`? If Jupyter binds to `127.0.0.1` *inside* the container, port publish on the host still cannot reach it. Listening on `0.0.0.0` is the standard pattern for services in containers.

`requirements.txt` includes `jupyterlab>=4.2,<5.0` and the four scientific libraries with the same ranges as the CLI project.

---

## Commands/Syntax

From `examples/jupyter-project`:

```bash
docker build -t course-jupyter:1.0 .
```

**Linux / macOS run:**

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

Browse `http://localhost:8888`. Empty token means the UI should open without a login form. If a token form appears, check that you ran **this** image, not `base-notebook`.

Override `CMD` to debug:

```bash
docker run --rm -it --user root course-jupyter:1.0 bash
```

You rarely need root. To list packages as jovyan:

```bash
docker run --rm course-jupyter:1.0 pip list
```

That replaces `CMD` with `pip list` and will not start Jupyter (useful check after build).

---

## Beginner Example

```bash
cd examples/jupyter-project
docker build -t course-jupyter:1.0 .
docker run --rm course-jupyter:1.0 pip list
```

Confirm `jupyterlab`, `numpy`, `pandas`, `matplotlib`, `scikit-learn` appear.

Then run with `-p` and the notebooks mount, open `01-check-stack.ipynb`, run all cells.

---

## Intermediate Example

Rebuild after a requirements change:

1. Add a comment or bump a range in `requirements.txt` only when you mean to.
2. `docker build -t course-jupyter:1.0 .`
3. First layers cache; `pip install` reruns if the requirements file changed.

Change a notebook, save, **do not rebuild**. The notebook is on the bind mount. Rebuild is for environment changes, not for cell edits.

---

## Advanced Example

### Restore a token for a shared machine

Change `CMD` to omit the empty token flag so Jupyter generates one:

```dockerfile
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser"]
```

Rebuild, then `docker logs` for the token (Lesson 15).

### Pin Jupyter exactly

```text
jupyterlab==4.2.5
```

Use when the class must freeze UI behavior. Rebuild and record the pin in the lab report.

### Image vs stack

`jupyter/scipy-notebook` already has the scientific stack. Pulling it is valid. You would still bind-mount `work`. This course builds a custom image so you practice Dockerfiles, `USER`, `EXPOSE`, and pip on a slim base.

---

## Practical Example

Session recipe (also in `examples/jupyter-project/README.md`):

```text
cd examples/jupyter-project
docker build -t course-jupyter:1.0 .
docker run --rm -p 8888:8888 -v <pwd>/notebooks:/home/jovyan/work --name course-jupyter course-jupyter:1.0
# browser http://localhost:8888
# Ctrl+C when done
```

Keep `course-jupyter:1.0` on disk so the next session skips the long pip layer.

---

## Common Mistakes

1. **`--ip=127.0.0.1`.** Browser on the host cannot connect.
2. **Forgetting `-p 8888:8888`.**
3. **Bind-mounting the project root over `/usr` or the whole home** and hiding the installed libraries. Mount **`notebooks`** onto `/home/jovyan/work` only.
4. **Empty token on a cloud VM with an open firewall.** Use a token or do not publish the port.
5. **Rebuilding because a notebook changed.** Unnecessary.
6. **Running `jupyter` on the host** and wondering why the custom packages are missing. Use the container URL.

---

## Best Practices

- Tag images (`course-jupyter:1.0`).
- Mount only the notebooks directory.
- Put packages in `requirements.txt`, not in a notebook `!pip install` as the sole record.
- Non-root `USER` for the server process.
- Empty tokens only on localhost, single-user laptops.
- `.dockerignore` so notebooks checkpoints do not bloat the **build** (they still persist via the mount).

---

## Exercises

1. **Read.** Open `examples/jupyter-project/Dockerfile`. Write one sentence each for `USER`, `EXPOSE`, `--ip=0.0.0.0`, and empty token.
2. **Build.** `docker build -t course-jupyter:1.0 .` from that directory.
3. **pip list.** `docker run --rm course-jupyter:1.0 pip list` and tick the five packages.
4. **Run.** Bind-mount `notebooks`, publish 8888, open JupyterLab.
5. **Notebook.** Run `01-check-stack.ipynb` cells. Confirm versions print and the plot renders.
6. **Persist.** Add a markdown cell, save, stop the container, confirm the `.ipynb` on the host changed.
7. **Contrast.** One paragraph: base-notebook vs `course-jupyter:1.0`.

---

## Quick Review

- Custom image = slim Python + pip stack + JupyterLab CMD.
- Bind-mount notebooks; bake dependencies.
- `--ip=0.0.0.0` and `-p 8888:8888` make the browser work.
- Empty token is a local-dev shortcut, not a production setting.

---

## Summary

You built and ran `course-jupyter:1.0` with a scientific Python stack. Lesson 17 is the project lab: use that repo as a template for a complete, persistent Jupyter workspace.

---

[← Previous Lesson](15-running-jupyter-with-docker.md)
[Course Home](../README.md)
[Next Lesson →](17-jupyter-project.md)
