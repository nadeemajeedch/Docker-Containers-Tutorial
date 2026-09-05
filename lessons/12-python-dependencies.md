# Lesson 12: Python Dependencies

A Python image without your libraries cannot import NumPy. This lesson covers pip, `requirements.txt`, version pinning, reproducibility, and conflicts — inside Docker, where the host Python (if any) does not matter.

[← Previous Lesson](11-building-python-images.md)
[Course Home](../README.md)
[Next Lesson →](13-dockerignore.md)

---

## Learning Objectives

After this lesson you will be able to:

- Explain why dependencies belong in the **image**, not on the host, for this course.
- Write and pin a `requirements.txt` for numpy, pandas, matplotlib, and scikit-learn.
- Install with `pip install -r requirements.txt` during `docker build`.
- Describe reproducibility: same file, same tags, same install (within the ranges you allow).
- Recognize a dependency conflict and how Docker makes it visible.

---

## Prerequisites

- Lessons 10–11.
- Built `my-python-app` at least once, or be ready to build it now.
- No local virtualenv is required. Docker *is* the isolated environment.

---

## Concept

### pip

**pip** is Python's package installer. Inside a `python:3.12-slim` container it is already available. It downloads wheels from the Python Package Index (PyPI), not from Docker Hub. Two networks appear in a typical build:

1. Docker Hub — `FROM python:3.12-slim`
2. PyPI — `RUN pip install -r requirements.txt`

### requirements.txt

A **requirements file** is a list of packages (and optional version constraints) pip should install:

```text
numpy>=2.0,<3.0
pandas>=2.2,<3.0
matplotlib>=3.9,<4.0
scikit-learn>=1.5,<2.0
```

This is the file in `examples/python-docker-project/requirements.txt`. Each line is a **constraint**. pip chooses versions that satisfy all lines together.

### Why Docker + requirements beats "pip install on my laptop"

| Approach | Problem |
|----------|---------|
| `pip install numpy` on the host | Classmates have different versions; graders may have none |
| "It works in my venv" | The venv is not what you submitted |
| Image with `RUN pip install -r requirements.txt` | The environment is **part of the artifact** |

The Dockerfile copies the requirements file and installs **at build time**. Anyone who builds the same Dockerfile with the same files gets the same importable stack (within the version ranges and the index state at build time).

---

## Explanation

### Version pinning styles

| Style | Example | Meaning |
|-------|---------|---------|
| Unpinned | `numpy` | Any version. Bad for class reports. |
| Lower bound | `numpy>=2.0` | 2.0 or newer, including 3.x someday |
| Range (this course) | `numpy>=2.0,<3.0` | 2.x only |
| Exact (lock) | `numpy==2.1.3` | Only that wheel. Maximum reproducibility, more rebuild friction |

Part 2 uses **ranges** so builds keep working when a patch releases, without jumping a major version. For a paper or a production freeze, generate a fully pinned lock (for example `pip freeze` **from the image** after a successful build) and commit that file.

```bash
docker run --rm my-python-app pip freeze
```

That output is the exact set that was installed **in that image**. Save it as `requirements.lock.txt` if your instructor asks for a freeze.

### Reproducibility layers

1. **Base image tag:** `python:3.12-slim` (not `python:latest`).
2. **Requirements ranges or exact pins.**
3. **Same Dockerfile order** so you actually rebuild what you think you rebuilt.
4. Optional: pin the **index** or use a lock file.

Docker does not freeze PyPI by itself. A rebuild next year may pick newer 2.x wheels if you used `>=2.0,<3.0`. Exact `==` pins close that gap.

### Dependency conflicts

pip tries to find one set of versions that fits every constraint. If pandas needs numpy `>=2` and another package demands numpy `1.x`, the install **fails at build time**. That is a feature: you see the conflict before you run the app.

Typical student conflict: adding packages without ranges until two libraries disagree. Fix by reading the pip error, loosening or tightening pins, or dropping the extra package.

### `--no-cache-dir`

```dockerfile
RUN pip install --no-cache-dir -r requirements.txt
```

pip's HTTP cache would stay in the image layer and waste space. `--no-cache-dir` keeps the layer to the installed packages.

Do not confuse this with Docker's **layer** cache. Docker still caches the `RUN` layer until `requirements.txt` changes.

---

## Commands/Syntax

Install during build (already in the course Dockerfile):

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
```

Inspect what an image contains:

```bash
docker run --rm my-python-app pip list
docker run --rm my-python-app python -c "import numpy, pandas, sklearn; print(numpy.__version__, pandas.__version__, sklearn.__version__)"
```

Install **once in a running container** (ephemeral; lost on `rm`):

```bash
docker run --rm -it python:3.12-slim bash
# inside:
pip install numpy
python -c "import numpy; print(numpy.__version__)"
exit
```

That experiment teaches the wrong long-term habit. Put pip in the Dockerfile so the next `run` still has numpy.

**PowerShell:** same `docker` commands. `pip` on the host is unrelated.

---

## Beginner Example

Prove the official image does **not** include pandas:

```bash
docker run --rm python:3.12-slim python -c "import pandas"
```

You should see `ModuleNotFoundError`.

Prove the project image **does**:

```bash
cd examples/python-docker-project
docker build -t my-python-app .
docker run --rm my-python-app python -c "import pandas as pd; print(pd.__version__)"
```

The difference is the `RUN pip install` layer.

---

## Intermediate Example

Add a dependency:

1. Add a line to `requirements.txt`, for example `scipy>=1.13,<2.0` (optional; rebuild will take longer).
2. Rebuild: `docker build -t my-python-app .`
3. Confirm pip runs again (cache miss on `COPY requirements.txt` or on `RUN`).
4. `docker run --rm my-python-app python -c "import scipy; print(scipy.__version__)"`

Remove the extra line afterward if you want to stay aligned with the course file, then rebuild.

Print a freeze for your lab report:

```bash
docker run --rm my-python-app pip freeze
```

---

## Advanced Example

Conflict demonstration (do this in a copy of the file, or undo afterward):

```text
numpy>=2.0,<3.0
numpy<2.0
```

Rebuild. pip should error. Read the message. Restore the original `requirements.txt`.

Pinning for a submission:

```text
numpy==2.1.3
pandas==2.2.3
matplotlib==3.9.2
scikit-learn==1.5.2
```

Exact numbers go stale; only use them when you have verified those versions install on `python:3.12-slim`. The course repo keeps ranges so the example keeps building as patches release.

Hash-pinning and `pip-tools` exist; they are beyond Part 2. Know that `requirements.txt` is the standard interface Dockerfiles use.

---

## Practical Example

The scientific stack in this course:

| Package | Role in `main.py` |
|---------|-------------------|
| numpy | Arrays for hours and scores |
| pandas | Table printout |
| matplotlib | Scatter plot to `/tmp/study-hours.png` |
| scikit-learn | `LinearRegression` |

All four are listed in `requirements.txt` and installed in the image. The host does not need any of them.

Workflow:

```text
edit requirements.txt  →  docker build  →  docker run
```

Not:

```text
pip install on host  →  hope the container sees it
```

The container will not see host site-packages.

---

## Common Mistakes

1. **Installing on the host and expecting the container to import it.** Different filesystems.
2. **`pip install` in a one-off container** and not recording it in `requirements.txt`.
3. **Unpinned `numpy` in a graded lab** so two builds a month apart differ.
4. **Copying `COPY . .` before pip** so every code edit reinstalls the stack (Lesson 10).
5. **Mixing conda on the host with pip in Docker** without a need. This course is pip-only.
6. **Editing `requirements.txt` but not rebuilding.**

---

## Best Practices

- One `requirements.txt` per image.
- Ranges or exact pins; never rely on "whatever pip felt like."
- `pip install --no-cache-dir -r requirements.txt` in the Dockerfile.
- After a successful class build, save `pip freeze` if the assignment asks for exact versions.
- Keep scientific packages in the **image** for Jupyter too (Lessons 15–16), not in a notebook `!pip install` as the only record.
- Do not copy virtualenv directories into the image (Lesson 13).

---

## Exercises

1. **Missing import.** Run `python:3.12-slim` with `import pandas` and record the error name.
2. **Project image.** `docker run --rm my-python-app pip list` and find numpy, pandas, matplotlib, scikit-learn.
3. **Versions.** Print the four versions with a single `python -c` as in Commands/Syntax.
4. **Read.** Open `examples/python-docker-project/requirements.txt`. For each line, name the package and the allowed major version.
5. **Freeze.** `docker run --rm my-python-app pip freeze` and save the output in your notes (not necessarily committed).
6. **Reason.** In four sentences, explain how Docker + requirements.txt attacks "works on my machine" for a pandas assignment.

---

## Quick Review

- pip installs PyPI packages during **build** via `RUN`.
- `requirements.txt` lists constraints; ranges vs `==` trade freshness vs freeze.
- Host pip is irrelevant to the container.
- Conflicts fail the build; that is earlier and better than a runtime crash.

---

## Summary

Dependencies are part of the image. `requirements.txt` plus `RUN pip install` makes NumPy, Pandas, Matplotlib, and scikit-learn available every time you run `my-python-app`. Next you will stop sending junk (`.git`, venvs, secrets) into that build with `.dockerignore`.

---

[← Previous Lesson](11-building-python-images.md)
[Course Home](../README.md)
[Next Lesson →](13-dockerignore.md)
