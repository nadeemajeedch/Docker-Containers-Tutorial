# Lesson 17: Jupyter Project Lab

This capstone for Part 2 uses `examples/jupyter-project` as a complete workspace: custom image, persistent notebooks, and a short analysis you can submit as files on the host.

[← Previous Lesson](16-custom-jupyter-image.md)
[Course Home](../README.md)
[Next Lesson →](18-docker-compose.md)

---

## Learning Objectives

After this lesson you will be able to:

- Build, run, stop, and rebuild the course Jupyter project without notes.
- Keep all `.ipynb` files on the host through a bind mount.
- Create a new notebook that uses numpy, pandas, matplotlib, and scikit-learn.
- Decide when to rebuild the image vs when to just rerun the container.
- Combine Part 1 operations (`ps`, `logs`, `stop`, `rm`) with Part 2 mounts and ports.

---

## Prerequisites

- Lessons 9–16.
- `examples/jupyter-project` in this repository.
- Docker daemon running.

---

## Concept

A **project** in this course means:

```text
Image (environment)     +     Bind-mounted folder (your work)     +     Published port (UI)
course-jupyter:1.0            examples/jupyter-project/notebooks        localhost:8888
```

Git tracks Dockerfiles, requirements, and notebooks. Docker runs the environment. The browser is only a view.

You do **not** need Docker Compose for one container. `docker build` and `docker run` are enough.

---

## Explanation

### When to rebuild

| You changed | Rebuild? |
|-------------|----------|
| A notebook cell | No |
| Files under `notebooks/` | No |
| `requirements.txt` | Yes |
| `Dockerfile` | Yes |
| Base image tag | Yes |

### Suggested notebook workflow

1. Start the container with the mount.
2. In JupyterLab, duplicate `01-check-stack.ipynb` or create `02-study-hours.ipynb`.
3. Save often. Confirm the file appears in `examples/jupyter-project/notebooks` on the host (IDE or `ls`).
4. Stop Jupyter when done. Commit notebooks on the host if you use git.

### Permissions reminder

If Linux cannot save notebooks, check ownership of `notebooks/` (`ls -l`). Docker Desktop on Windows/macOS usually maps ownership for you.

### Connecting the CLI app and Jupyter

`examples/python-docker-project/main.py` is the same study-hours idea as the Jupyter starter notebook. One is a script image; one is an interactive environment. Same libraries, different `CMD`.

---

## Commands/Syntax

Build:

```bash
cd examples/jupyter-project
docker build -t course-jupyter:1.0 .
```

Run (Linux / macOS):

```bash
docker run --rm -p 8888:8888 \
  -v "$PWD/notebooks":/home/jovyan/work \
  --name course-jupyter \
  course-jupyter:1.0
```

Run (PowerShell):

```powershell
docker run --rm -p 8888:8888 `
  -v "${PWD}\notebooks:/home/jovyan/work" `
  --name course-jupyter `
  course-jupyter:1.0
```

Status and logs:

```bash
docker ps
docker logs course-jupyter
docker stop course-jupyter
```

If you started with `-d` and without `--rm`:

```bash
docker start course-jupyter
docker rm course-jupyter
```

From the repository root without `cd` (Linux/macOS):

```bash
docker run --rm -p 8888:8888 \
  -v "$PWD/examples/jupyter-project/notebooks":/home/jovyan/work \
  course-jupyter:1.0
```

The image must already exist. Build still needs the project directory as context.

---

## Beginner Example

Follow `examples/jupyter-project/README.md` from top to bottom: build, run, open `http://localhost:8888`, open `01-check-stack.ipynb`, run all cells, save, Ctrl+C.

Confirm `01-check-stack.ipynb` is still in `notebooks/` on the host.

---

## Intermediate Example

Create `02-study-hours.ipynb` in JupyterLab with:

1. A pandas table of hours vs scores (you may copy numbers from `main.py`).
2. `LinearRegression` from sklearn.
3. A matplotlib scatter plus the fitted line.
4. A markdown cell stating the predicted score after 5 hours.

Save. On the host, open the notebook in a text editor and confirm JSON changed (or just check the timestamp).

Stop the container and run again with the same mount. Open `02-study-hours.ipynb` — outputs may or may not be stored depending on whether you saved after running; the **source cells** must still be there.

---

## Advanced Example

### Detached lab server for a study session

```bash
docker run -d -p 8888:8888 \
  -v "$PWD/notebooks":/home/jovyan/work \
  --name course-jupyter \
  course-jupyter:1.0
```

No `--rm`, so the container remains until `docker rm`. Notebooks still live on the mount either way.

```bash
docker logs course-jupyter
docker stop course-jupyter
docker start course-jupyter
docker rm -f course-jupyter
```

### Second host port for a classmate's copy

```bash
docker run --rm -p 8890:8888 -v "$PWD/notebooks":/home/jovyan/work course-jupyter:1.0
```

Use `http://localhost:8890`. Do not share an empty-token server beyond localhost.

### Rebuild after adding a library

Add `scipy>=1.13,<2.0` to `requirements.txt` only if you need it, rebuild, restart the container. In a notebook `import scipy` should work. Revert if you want to stay on the course default stack.

---

## Practical Example

Part 2 capstone (do in order):

1. `docker run --rm python:3.12 python --version`
2. Bind-mount run `examples/hello-python/hello.py`
3. Build and run `examples/python-docker-project` as `my-python-app`
4. Build `course-jupyter:1.0`
5. Run Jupyter with `notebooks/` mounted
6. Complete or extend `01-check-stack.ipynb`
7. Stop Jupyter; list host `notebooks/`
8. `docker images` and identify `my-python-app` and `course-jupyter:1.0`
9. `docker system df` — note images vs volumes. Do not prune volumes you still need.

---

## Common Mistakes

1. **Building from the wrong directory** so `COPY requirements.txt` fails.
2. **Mounting `$PWD` onto `/home/jovyan/work` when `$PWD` is the repo root.** You will see many folders in Jupyter, not just notebooks. Mount `.../notebooks`.
3. **Two containers publishing 8888.** Stop the old one.
4. **Empty notebooks folder path** because `${PWD}` was wrong in PowerShell. Use a full path if needed.
5. **Submitting only a screenshot** when the instructor asked for the `.ipynb` from the host folder.

---

## Best Practices

- One image tag per assignment version (`course-jupyter:1.0`).
- Notebooks in git; large datasets not in the image.
- Stop Jupyter when you leave the laptop.
- Keep the Jupyter Dockerfile as small as the CLI Dockerfile: pip, user, CMD.
- Re-read `docker logs` before changing the Dockerfile for "it won't open."

---

## Exercises

1. **Cold start.** Close extra terminals. Build and run the Jupyter project from the README.
2. **New notebook.** Create `02-study-hours.ipynb` as in the Intermediate Example.
3. **Host proof.** Screenshot or paste `ls` / `Get-ChildItem` of `notebooks/`.
4. **Stop/start.** If using a named container without `--rm`, `docker stop` then `docker start` and reopen the notebook.
5. **CLI twin.** Run `docker run --rm my-python-app` and compare the predicted score with your notebook.
6. **Cleanup plan.** List images and containers you created in Part 2. Remove **containers** you do not need. Keep images you will use tomorrow, or `docker rmi` them if disk is tight.
7. **Write.** Half a page: how bind mounts plus a custom image replace "install Anaconda on every lab PC."

---

## Quick Review

- Environment = image. Work = bind mount. UI = published port.
- Rebuild for Dockerfile/requirements; not for notebook edits.
- Part 2 capstone is Python CLI image + Jupyter image + persistence.
- Part 3 adds Compose, networking, DS/ML environments, and a GitHub final project.

---

## Summary

Part 2 is complete. You can run Python in Docker, write Dockerfiles, install pinned dependencies, ignore junk in builds, persist files with mounts, and run a custom JupyterLab environment whose notebooks live on your machine.

Part 3 continues with Docker Compose, networking, data science and ML environments, troubleshooting, security, and a final project.

---

[← Previous Lesson](16-custom-jupyter-image.md)
[Course Home](../README.md)
[Next Lesson →](18-docker-compose.md)
