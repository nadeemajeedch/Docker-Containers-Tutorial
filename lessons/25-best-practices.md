# Lesson 25: Best Practices

This lesson gathers the habits that keep images small, builds fast, and class projects reproducible. It is not a new tool. It is how you use the tools you already have.

[← Previous Lesson](24-debugging.md)
[Course Home](../README.md)
[Next Lesson →](26-security.md)

---

## Learning Objectives

After this lesson you will be able to:

- Choose official, pinned base images instead of `latest`.
- Order Dockerfile instructions for cache hits.
- Keep `.dockerignore` complete.
- Run as a non-root user when the process does not need root.
- Separate libraries (image) from notebooks and data (mounts).
- Apply a short checklist before you push a project.

---

## Prerequisites

- Lessons 10–23.
- Optional: [best-practices cheatsheet](../cheatsheet/best-practices.md).

---

## Concept

A good student image is:

- **Small enough** to pull on campus Wi-Fi
- **Pinned** so next month's build is still the same stack
- **Cached** so editing `main.py` does not reinstall NumPy
- **Free of secrets and venvs**
- **Runnable by a classmate** with `docker compose up --build`

Best practices are constraints that make those five true.

---

## Explanation

### Official base images and pins

Use `python:3.12-slim`, not `python:latest`, not a random `someone/python`. Slim is smaller than the full Debian image and enough for pip wheels in this course. Alpine is smaller still but can break scientific wheels; skip it unless you know you need it.

### Small images

- `slim` base
- `--no-cache-dir` on pip
- No compilers in the final image unless you compile (Lesson 28 multi-stage)
- `.dockerignore` so context is not gigabytes

### Layer caching

```dockerfile
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
```

Dependencies change rarely; source changes often. That order is the whole trick.

### `.dockerignore`

Ignore `.git`, `.venv`, `__pycache__`, `.env`, OS junk, notebook checkpoints. Do not ignore `requirements.txt` or application source.

### Non-root

`USER jovyan` after `pip install` (pip in this course runs as root during build, then the server drops privilege). Jupyter and class web apps do not need root at runtime.

### Reproducibility

Pin base tags and pip ranges or exact versions. Document `docker compose up --build` in README. Keep data paths stable (`/workspace/data/...`).

### Minimal images vs convenience

Full `python:3.12` is easier to explore (`bash`, extra OS tools). Slim is better to ship. This course uses slim for project images and full `python:3.12` for REPL demos.

---

## Commands/Syntax

Sanity checks on an image you built:

```bash
docker images my-python-app
docker history my-python-app
docker run --rm my-python-app whoami
```

`whoami` should not be `root` on the Jupyter images (`jovyan`). The CLI `my-python-app` example from Part 2 still runs as root unless you added `USER`; Part 3 Jupyter examples do not.

Rebuild after a practice change:

```bash
docker compose up --build
```

---

## Beginner Example

Open `examples/python-docker-project/Dockerfile` and `examples/data-science-docker/Dockerfile`. Tick: pinned `FROM`, requirements copied first, `--no-cache-dir`, `.dockerignore` present.

---

## Intermediate Example

Deliberately put `COPY . .` before `pip install` in a scratch copy of a Dockerfile, change `main.py`, rebuild twice, and watch pip rerun. Restore the correct order. That experiment is the cache lesson.

---

## Advanced Example

`docker history` shows layer sizes. A huge last layer often means you copied too much (missing dockerignore) or stored pip cache.

Resource limits (also Lesson 27) keep a runaway notebook from freezing the laptop:

```bash
docker run --rm -m 512m python:3.12-slim python -c "print('ok')"
```

Compose:

```yaml
mem_limit: 512m
```

Optional for class; useful on shared lab PCs.

---

## Practical Example

Pre-push checklist:

```text
[ ] FROM uses a pinned tag
[ ] requirements.txt pinned or ranged
[ ] .dockerignore present
[ ] no .env secrets in git status
[ ] README has compose up --build
[ ] notebooks/data on mounts, not only in the image
[ ] USER is non-root for long-running servers
```

---

## Common Mistakes

1. `FROM python:latest`
2. Installing build tools and never removing them (Lesson 28)
3. Copying `.venv` into the image
4. Running Jupyter as root because "it worked"
5. README that only says "install Anaconda"

---

## Best Practices

This whole lesson is the list. If you remember only four: pin tags, copy requirements first, dockerignore, non-root for servers.

---

## Exercises

1. Run the pre-push checklist on `examples/data-science-docker`.
2. `docker history` on `course-jupyter:1.0` or a Part 3 image you built.
3. `whoami` in the data-science Jupyter service (`compose exec jupyter whoami`).
4. Rewrite a bad one-line Dockerfile (`FROM python` + `COPY . .` + `RUN pip install -r requirements.txt`) into a good one.
5. Add one item to the checklist that your instructor cares about (tests, license, data citation).

---

## Quick Review

- Official + pinned + slim for projects.
- Cache = requirements then source.
- Ignore junk; never ignore needed source.
- Non-root for Jupyter.
- README is part of the environment.

---

## Summary

Best practices are how Part 3 projects stay teachable. Next: security — least privilege, secrets, and why empty tokens must not face the internet.

---

[← Previous Lesson](24-debugging.md)
[Course Home](../README.md)
[Next Lesson →](26-security.md)
