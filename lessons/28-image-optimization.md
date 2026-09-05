# Lesson 28: Image Optimization

Smaller images pull faster on campus Wi-Fi and waste less disk. This lesson shows how to reduce size with better bases, `.dockerignore`, layer order, fewer packages, and **optional** multi-stage builds.

[← Previous Lesson](27-advanced-docker.md)
[Course Home](../README.md)
[Next Lesson →](29-docker-and-github.md)

---

## Learning Objectives

After this lesson you will be able to:

- Compare `python:3.12` vs `python:3.12-slim` for project images.
- Explain how `.dockerignore` and layer order affect size and cache.
- Avoid leaving pip caches and apt lists in layers.
- Describe a multi-stage build at a recognition level.
- Measure size with `docker images` and `docker history`.

---

## Prerequisites

- Lessons 10–13 and 25.
- Multi-stage is **optional / advanced** for the final project.

---

## Concept

Image size is the sum of layers (with sharing across images). You reduce it by:

1. Starting smaller (`slim`)
2. Not copying junk (`.dockerignore`)
3. Not storing caches (`pip --no-cache-dir`)
4. Combining/cleaning `apt` in the **same** `RUN` if you install OS packages
5. Multi-stage: build with compilers, copy only the result into a slim runtime

Scientific wheels from PyPI are already large (numpy). You will not get a 20 MB data-science image. You can still avoid doubling that with venvs and git history.

---

## Explanation

### Better base images

| Tag | Typical use |
|-----|-------------|
| `python:3.12` | Interactive exploration |
| `python:3.12-slim` | Course project images |
| `python:3.12-alpine` | Small, but many scientific packages need extra work |

This course standardizes on **slim** for Compose projects.

### `.dockerignore` and context

A 2 GB `data/` folder in context slows **every** build even if you never `COPY` it. Ignore it, or keep large data outside the build directory.

### Layer ordering

Copy `requirements.txt` first (Lesson 10). That does not always shrink the image, but it avoids **re-downloading** gigabytes of wheels.

### Removing unnecessary packages

If you `apt-get install` compilers to build a wheel, delete them in the same `RUN` or use multi-stage. Course examples use wheels from PyPI and do not need `gcc` for numpy on slim/debian typically.

### Multi-stage (advanced)

```dockerfile
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /install /usr/local
WORKDIR /app
COPY src/ /app/src/
USER nobody
CMD ["python", "src/analyze.py"]
```

Stage `builder` can be larger. The final image copies only installed packages. Optional for this course; the simple single-stage slim Dockerfiles are enough for the final project.

---

## Commands/Syntax

```bash
docker images python
docker images course-jupyter
docker history course-jupyter:1.0
```

Compare sizes after you have built Part 2/3 images.

**PowerShell:** same.

Do not use `docker system prune -a` just to "optimize" during a lab; you will re-pull bases.

---

## Beginner Example

```bash
docker images python
```

Note `3.12` vs `3.12-slim` SIZE if both are pulled. Slim should be smaller. Project images add pip packages on top of slim.

---

## Intermediate Example

```bash
cd examples/python-docker-project
docker build -t my-python-app .
docker history my-python-app
```

Find the `pip install` layer. That layer is the scientific stack. The `COPY . .` layer should be tiny if dockerignore works.

---

## Advanced Example

Sketch a multi-stage file for `src/analyze.py` only (no Jupyter). Jupyter needs many files; multi-stage helps more for **CLI** apps than for JupyterLab images.

You do not have to build the sketch unless you want to.

---

## Practical Example

Optimization checklist for Part 3 projects:

```text
[ ] FROM python:3.12-slim
[ ] pip --no-cache-dir
[ ] .dockerignore includes .git and venvs
[ ] no COPY of notebooks into the image if they are mounted
[ ] docker history looks sane
```

Course Jupyter Dockerfiles do **not** `COPY notebooks/` into the image; Compose mounts them. That keeps rebuilds fast and images smaller.

---

## Common Mistakes

1. Alpine + numpy without reading musl issues.
2. `apt-get install` without `rm -rf /var/lib/apt/lists/*` in the same layer.
3. Multi-stage that copies the entire builder filesystem.
4. Measuring SIZE as exclusive disk (`docker system df` is better for disk).

---

## Best Practices

- Slim + pip no-cache + dockerignore covers 90% of student needs.
- Multi-stage when you compile or ship a tiny CLI.
- Do not copy mounted work into the image.
- Re-read `history` after a surprising size jump.

---

## Exercises

1. Compare `docker images` for `python:3.12` and `python:3.12-slim` (pull slim if needed).
2. `docker history` on a project image; identify the pip layer.
3. Confirm a Jupyter Dockerfile does not `COPY notebooks`.
4. Write three bullets on why venvs should be dockerignored.
5. Optional: write (not necessarily build) a two-stage Dockerfile for `analyze.py`.

---

## Quick Review

- Slim bases, no pip cache, dockerignore, copy requirements first.
- Multi-stage is optional and best for CLI runtimes.
- Jupyter images will never be tiny; avoid extra junk.

---

## Summary

You can shrink and explain image size. Next: putting Docker projects on GitHub so a classmate can clone and compose-up.

---

[← Previous Lesson](27-advanced-docker.md)
[Course Home](../README.md)
[Next Lesson →](29-docker-and-github.md)
