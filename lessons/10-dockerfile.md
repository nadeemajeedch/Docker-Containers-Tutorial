# Lesson 10: Dockerfiles

A Dockerfile is a text file that describes how to build an image. This lesson explains every instruction you need for Part 2, then walks through a complete Python example line by line.

[← Previous Lesson](09-running-python-with-docker.md)
[Course Home](../README.md)
[Next Lesson →](11-building-python-images.md)

---

## Learning Objectives

After this lesson you will be able to:

- Explain what a Dockerfile is and how it relates to `docker build`.
- Read and write `FROM`, `WORKDIR`, `COPY`, `ADD`, `RUN`, `CMD`, `ENTRYPOINT`, `ENV`, `EXPOSE`, `USER`, and `ARG`.
- Explain the example Python Dockerfile used in `examples/python-docker-project`.
- Choose `CMD` vs `ENTRYPOINT` for a student project.
- Avoid treating `ADD` as a synonym for `COPY` without a reason.

---

## Prerequisites

- Lessons 6, 7, and 9.
- Comfort with a text editor and with `docker run`.
- You do not need to build yet. Lesson 11 is `docker build`. Read this lesson first so the build output makes sense.

---

## Concept

An **image** is a stack of layers (Lesson 6). A **Dockerfile** is the recipe that creates those layers.

```text
Dockerfile  --docker build-->  image  --docker run-->  container
```

Each instruction typically adds a layer (or metadata). Order matters: Docker caches layers from the top down. Changing an early line rebuilds that line and everything below it. Lesson 11 uses that fact; here you learn what the lines mean.

The file is usually named `Dockerfile` with no extension, placed in the project root.

---

## Explanation

### Instruction catalog

| Instruction | Role | Typical Python use |
|-------------|------|--------------------|
| `FROM` | Base image. First instruction (except optional comments/`ARG` before it). | `FROM python:3.12-slim` |
| `WORKDIR` | Set working directory; creates it if needed. Later `RUN`/`COPY`/`CMD` are relative to it. | `WORKDIR /app` |
| `COPY` | Copy files from the **build context** (usually the project folder) into the image. | `COPY requirements.txt .` |
| `ADD` | Like `COPY`, plus extra features (local tar auto-extract, remote URL). Prefer `COPY` unless you need those extras. | Rare in this course |
| `RUN` | Execute a command **at build time**. Result is baked into the image. | `RUN pip install ...` |
| `CMD` | Default command **when the container starts**, if the user did not pass one. | `CMD ["python", "main.py"]` |
| `ENTRYPOINT` | Command that always runs; `docker run` args are appended (exec form). | Wrappers, CLI tools |
| `ENV` | Environment variable persisted in the image. | `ENV PYTHONUNBUFFERED=1` |
| `EXPOSE` | Documents a port. Does **not** publish it. Publishing is `docker run -p`. | `EXPOSE 8888` (Jupyter) |
| `USER` | Run later instructions and the container process as that user. | Non-root Jupyter user |
| `ARG` | Build-time variable (`docker build --build-arg`). Not kept unless you also `ENV`. | Python version, extra flags |

Comments start with `#`.

### Exec form vs shell form

```dockerfile
CMD ["python", "main.py"]
CMD python main.py
```

The first is **exec form** (JSON array): no shell, clear signal handling, preferred.

The second is **shell form**: runs via `/bin/sh -c`. Needed when you want shell features (`$VAR`, pipes). For `python main.py`, use exec form.

The same distinction applies to `ENTRYPOINT` and `RUN` (`RUN ["pip", "install", "x"]` vs `RUN pip install x`). `RUN pip install ...` in shell form is normal and readable.

### `CMD` vs `ENTRYPOINT`

- `CMD` = default. Easy to override: `docker run my-python-app python --version` replaces the `CMD`.
- `ENTRYPOINT` = the program. `docker run myimage --help` appends `--help` to the entrypoint.

For `main.py`, `CMD ["python", "main.py"]` is the student-friendly choice. Jupyter images often use an entrypoint script; you will still pass flags after the image name.

### `COPY` vs `ADD`

Use **`COPY`** unless you are extracting a local tar or have a documented reason for `ADD`. `ADD` with a URL looks convenient and is harder to cache and debug. This course uses `COPY`.

### Complete example (this course)

File: `examples/python-docker-project/Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

Line by line:

1. **`FROM python:3.12-slim`** — start from official Python 3.12 on a slim Debian base. Smaller than `python:3.12`, enough for pip packages in this project.
2. **`WORKDIR /app`** — create `/app` if needed and use it as the current directory.
3. **`COPY requirements.txt .`** — copy only the dependency list first. `.` means `/app` because of `WORKDIR`.
4. **`RUN pip install --no-cache-dir -r requirements.txt`** — install packages **during build**. `--no-cache-dir` avoids storing pip's download cache in the image layer.
5. **`COPY . .`** — copy the rest of the project (including `main.py`) into `/app`.
6. **`CMD ["python", "main.py"]`** — when someone runs the image with no extra command, start `main.py`.

Why copy `requirements.txt` before `COPY . .`? If you only change `main.py`, Docker can reuse the `pip install` layer. If `requirements.txt` and the app were copied together, every code edit would reinstall NumPy. Lesson 11 shows this in a rebuild.

---

## Commands/Syntax

You write a Dockerfile; you do not "run" it. The related CLI is:

```bash
docker build -t my-python-app .
```

`.` is the **build context**: the directory sent to the daemon. `COPY` paths are relative to that context, not to your home folder.

```bash
docker run --rm my-python-app
```

runs the image and therefore the `CMD`.

Override `CMD`:

```bash
docker run --rm my-python-app python --version
```

Dockerfile instructions are not shell commands. Do not type `FROM python:3.12-slim` in PowerShell.

---

## Beginner Example

Smallest useful Python Dockerfile:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY hello.py .
CMD ["python", "hello.py"]
```

This has no `pip` step. It is enough for `hello.py` with the standard library only.

The course project adds `requirements.txt` because NumPy is not in the standard library. The official image does **not** include pandas or scikit-learn until you `RUN pip install`.

---

## Intermediate Example

Environment, port documentation, and a non-root user (pattern you will see again in Jupyter):

```dockerfile
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

ARG APP_USER=appuser
RUN useradd --create-home --uid 1000 ${APP_USER}

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
USER appuser

EXPOSE 8000
CMD ["python", "main.py"]
```

| Line | Why |
|------|-----|
| `PYTHONUNBUFFERED=1` | Prints show up immediately in `docker logs` |
| `PYTHONDONTWRITEBYTECODE=1` | Skip `.pyc` files in the image |
| `ARG` + `useradd` | Avoid running as root when you do not need it |
| `EXPOSE 8000` | Documents intent; still requires `-p` at run time |

The example in `examples/python-docker-project` stays simpler: no `USER`, no `EXPOSE`. That is acceptable for a CLI program that prints and exits.

---

## Advanced Example

`ENTRYPOINT` plus `CMD` as default arguments:

```dockerfile
ENTRYPOINT ["python", "main.py"]
CMD ["--help"]
```

`docker run myimage` runs `python main.py --help`. `docker run myimage --quiet` runs `python main.py --quiet`.

Build-time version pin:

```dockerfile
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim
```

```bash
docker build --build-arg PYTHON_VERSION=3.12 -t my-python-app .
```

`ARG` before `FROM` is a special case: it only applies to the `FROM` line unless redeclared after `FROM`.

---

## Practical Example

Open `examples/python-docker-project/Dockerfile` and match each line to the table in this lesson. Then open `main.py` and `requirements.txt`. You should be able to answer, without building yet:

- Which image supplies the `python` binary?
- Where will `main.py` live inside the image?
- When does `pip install` run: build or container start?
- What process starts if you `docker run` with no extra args?

Answers: `python:3.12-slim`; `/app/main.py`; **build**; `python main.py`.

Lesson 11 builds and runs this project.

---

## Common Mistakes

1. **Putting application code in `RUN`.** `RUN` is for build steps (apt, pip). App startup belongs in `CMD` or `ENTRYPOINT`.
2. **`EXPOSE` and thinking the port is published.** Always `docker run -p`.
3. **`COPY . .` before `pip install`.** Slow rebuilds on every edit.
4. **Using `ADD` for a single file** out of habit. Use `COPY`.
5. **Shell-form `CMD python main.py` then extra quotes problems.** Prefer exec form.
6. **Editing the Dockerfile but expecting a running container to change.** You must rebuild, then run a new container.
7. **Windows: saving `Dockerfile.txt`.** The file name should be `Dockerfile`. Show extensions in Explorer if needed.

---

## Best Practices

- One Dockerfile per image, in the project root, named `Dockerfile`.
- Pin the base tag (`3.12-slim`, not `python:latest`).
- `COPY` dependency files, `RUN pip`, then `COPY` source.
- Exec-form `CMD` for Python apps.
- Prefer `COPY` over `ADD`.
- Comments only when they explain *why*, not when they repeat the instruction.
- Keep the default user as needed; do not enable `--privileged`.

---

## Exercises

1. **Label.** Print the six-line course Dockerfile. Write one sentence per instruction.
2. **Predict.** If you change `CMD` to `CMD ["python", "--version"]`, what happens on `docker run --rm my-python-app`? (You will verify in Lesson 11.)
3. **COPY vs ADD.** When would `ADD` be justified? When must you still prefer `COPY`?
4. **CMD vs RUN.** Why is `RUN python main.py` the wrong way to start the app at container runtime?
5. **EXPOSE.** Does `EXPOSE 8888` make Jupyter reachable on the host? How do you actually publish a port?
6. **Read.** Open `examples/python-docker-project/Dockerfile` in your editor. Confirm it matches this lesson.

---

## Quick Review

- A Dockerfile is a layer recipe consumed by `docker build`.
- `FROM` / `WORKDIR` / `COPY` / `RUN` / `CMD` are the core Python set.
- `ADD`, `ENTRYPOINT`, `ENV`, `EXPOSE`, `USER`, `ARG` extend that set.
- `pip install` belongs in `RUN` (build). `python main.py` belongs in `CMD` (run).
- Copy requirements before source so dependency layers cache.

---

## Summary

You can read a Dockerfile as a sequence of layers and metadata. The course Python image starts from `python:3.12-slim`, installs pinned pip packages, copies the app, and defaults to `python main.py`. Lesson 11 turns that file into an image with `docker build`.

---

[← Previous Lesson](09-running-python-with-docker.md)
[Course Home](../README.md)
[Next Lesson →](11-building-python-images.md)
