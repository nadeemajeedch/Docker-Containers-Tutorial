# Lesson 19: Python and Jupyter with Compose

This lesson applies Compose to the workflow you already know: a custom Jupyter image, port 8888, and a notebooks bind mount. The example is `examples/compose-jupyter`.

[← Previous Lesson](18-docker-compose.md)
[Course Home](../README.md)
[Next Lesson →](20-environment-variables.md)

---

## Learning Objectives

After this lesson you will be able to:

- Read the Compose file that builds Jupyter from a local Dockerfile.
- Start, use, and stop Jupyter without memorizing `docker run` flags.
- Exec a Python command inside the running Jupyter service.
- Explain why the mount path is `/workspace/notebooks` in this example.
- Switch between foreground and detached Compose for lab sessions.

---

## Prerequisites

- Lesson 18.
- Lessons 16–17 (custom Jupyter image).
- Port 8888 free, or be ready to change the host port.

---

## Concept

Part 2 started Jupyter with a long `docker run`. The same application as Compose:

```yaml
services:
  jupyter:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/workspace/notebooks
```

`build: .` uses `examples/compose-jupyter/Dockerfile`, which is the Part 2 Jupyter image with **WORKDIR `/workspace/notebooks`** so it matches the YAML the assignment prompt uses.

The scientific stack is still in `requirements.txt` (numpy, pandas, matplotlib, scikit-learn, jupyterlab).

---

## Explanation

### Why a different workdir than Lesson 16?

Lesson 16 used `/home/jovyan/work` to match Jupyter Docker Stacks. Part 3 examples use `/workspace/...` because many academic templates and the Compose snippet in this course's outline use that prefix. Both are correct. **The Compose volume target must match the process working directory** or you will save files you cannot find.

### Service name

The service is called `jupyter`. That name is what you pass to `docker compose logs jupyter` and `docker compose exec jupyter ...`. It is also the DNS name if another service in the same Compose file needs to call it (Lesson 21).

### Rebuild

Change `requirements.txt` → `docker compose up --build`. Change a notebook → do **not** rebuild; it is on the bind mount.

---

## Commands/Syntax

**Linux / macOS and PowerShell:**

```bash
cd examples/compose-jupyter
docker compose up --build
```

Detached session:

```bash
docker compose up -d --build
docker compose ps
docker compose logs -f jupyter
```

Ctrl+C stops following logs, not the container (because of `-d`). Then:

```bash
docker compose exec jupyter python -c "import pandas as pd; print(pd.__version__)"
docker compose down
```

---

## Beginner Example

Foreground:

```bash
cd examples/compose-jupyter
docker compose up --build
```

Browser: `http://localhost:8888`. Empty token (local class image). Create `compose-check.ipynb`, `print("hello compose")`, save, Ctrl+C. Confirm the file under `examples/compose-jupyter/notebooks`.

---

## Intermediate Example

Compare with Part 2:

```bash
# Part 2 style (from examples/jupyter-project)
docker run --rm -p 8888:8888 -v "$PWD/notebooks":/home/jovyan/work course-jupyter:1.0
```

Same idea, different mount target and no Compose project network. After this lesson, prefer Compose for anything you will give to a classmate.

---

## Advanced Example

Run a one-off Python script **in this image** without Jupyter:

```bash
docker compose run --rm jupyter python -c "import sklearn; print('ok')"
```

`compose run` starts a **new** container from the service definition. It does not attach to the already running Jupyter unless you use `exec`. Use `run --rm` for scripts; use `exec` when Jupyter is already up and you want a second process in **that** container.

---

## Practical Example

Lab-day recipe:

```text
cd examples/compose-jupyter
docker compose up -d --build
# browser localhost:8888
docker compose logs jupyter
# work...
docker compose down
```

If 8888 is busy, Lesson 20 shows `JUPYTER_PORT` and `.env`. For now, `docker ps` and stop the other container.

---

## Common Mistakes

1. **Mounting `./notebooks` to `/home/jovyan/work` while WORKDIR is `/workspace/notebooks`.** Files "disappear." Align paths.
2. **`compose run jupyter` while `up` already published 8888.** Port conflict. Use `exec` or `down` first.
3. **Editing Dockerfile but `up` without `--build`.** Old image.
4. **PowerShell `cd` to the wrong examples folder.**

---

## Best Practices

- One Compose service named `jupyter` for class notebooks.
- Bind-mount only the folders students should edit.
- `down` at the end of class.
- Keep `CMD` in the Dockerfile; keep ports/volumes in Compose.

---

## Exercises

1. Start Compose Jupyter and import pandas in a notebook.
2. `exec` `python --version` while it is running.
3. Change the first markdown cell of `notebooks/welcome.md` on the host; refresh Jupyter and confirm.
4. `down`, `up -d`, confirm the notebook still exists.
5. Write three sentences comparing `docker run` (Lesson 16) and `docker compose up`.

---

## Quick Review

- `build` + `ports` + `volumes` replace the long `docker run`.
- Mount target must match the image workdir.
- `exec` vs `run`: existing container vs new container.
- Rebuild for environment changes, not for notebook edits.

---

## Summary

Jupyter for class is now a Compose file plus a Dockerfile. Next: environment variables, `.env` files, and what must never go on GitHub.

---

[← Previous Lesson](18-docker-compose.md)
[Course Home](../README.md)
[Next Lesson →](20-environment-variables.md)
