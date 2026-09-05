# Lesson 11: Building Python Images

Lesson 10 explained Dockerfile instructions. This lesson builds the image, runs it, changes the app, and rebuilds. The project lives in `examples/python-docker-project`.

[← Previous Lesson](10-dockerfile.md)
[Course Home](../README.md)
[Next Lesson →](12-python-dependencies.md)

---

## Learning Objectives

After this lesson you will be able to:

- Run `docker build -t my-python-app .` from a project directory.
- Explain build context, tags, and layer cache.
- Run the resulting image with `docker run --rm my-python-app`.
- Override `CMD` for a one-off command.
- Modify `main.py`, rebuild, and see what was cached vs rebuilt.

---

## Prerequisites

- Lesson 10.
- Docker install from Part 1.
- Network access the first time you build (base image and pip packages).
- Ability to `cd` into `examples/python-docker-project`.

---

## Concept

`docker build` reads a Dockerfile, sends a **build context** (a directory tree) to the daemon, and produces an image. You tag that image so you can run it by name.

```text
project folder (context)
   ├── Dockerfile
   ├── requirements.txt
   └── main.py
            │
            ▼  docker build -t my-python-app .
      image my-python-app:latest
            │
            ▼  docker run --rm my-python-app
      container runs CMD: python main.py
```

`-t my-python-app` names the image `my-python-app:latest` if you omit a tag. Prefer an explicit tag when you care about versions: `-t my-python-app:1.0`.

The final `.` is not decoration. It is the context path: "use the current directory."

---

## Explanation

### What the daemon receives

Everything in the context directory can be `COPY`d, unless `.dockerignore` excludes it (Lesson 13). Large extra files slow the build even if you never copy them, because the client still sends the context.

### Cache

Each Dockerfile instruction is a layer. If the instruction and its inputs have not changed, Docker **reuses** the layer. That is why the first build downloads `python:3.12-slim` and pip packages, and the second build of the same tree is much faster.

If you change `main.py` only:

- `FROM` — cache hit
- `WORKDIR` — cache hit
- `COPY requirements.txt` — cache hit
- `RUN pip install` — cache hit
- `COPY . .` — **cache miss** (source changed)
- `CMD` — rerun as metadata on the new layer

If you change `requirements.txt`, `pip install` runs again.

### Tagging

```bash
docker build -t my-python-app .
docker build -t my-python-app:1.0 .
```

You can apply both (two `-t` flags) so `latest` and `1.0` point at the same build.

### Where to run the command

Run `docker build` from the directory that contains the Dockerfile, **or** pass `-f` and a context:

```bash
docker build -t my-python-app -f examples/python-docker-project/Dockerfile examples/python-docker-project
```

Beginners should `cd` into the project. `-f` is for later, when one repo has several Dockerfiles.

---

## Commands/Syntax

**Linux / macOS and PowerShell** (same build/run lines):

```bash
cd examples/python-docker-project
docker build -t my-python-app .
docker run --rm my-python-app
```

Useful variants:

```bash
docker build -t my-python-app:1.0 .
docker images my-python-app
docker run --rm my-python-app python --version
docker run --rm -it my-python-app bash
```

| Command | Meaning |
|---------|---------|
| `docker build -t NAME .` | Build, tag `NAME:latest`, context is `.` |
| `docker run --rm my-python-app` | Run `CMD` from the Dockerfile |
| `docker run --rm my-python-app python --version` | Replace `CMD` |
| `docker images my-python-app` | Confirm the tag exists |

No `--rm` on `build`. `--rm` applies to **containers** at run time. Build containers are handled by BuildKit.

Progress output may say `#1 [internal] load build definition`. That is BuildKit, the current Docker builder. You do not need extra flags for this course.

---

## Beginner Example

From `examples/python-docker-project`:

```bash
docker build -t my-python-app .
docker run --rm my-python-app
```

First build: pulling `python:3.12-slim` (if missing), copying `requirements.txt`, pip installing numpy/pandas/matplotlib/scikit-learn, copying the app.

Run output includes:

- `Hello from the Python Docker project`
- numpy and pandas versions
- a small hours/score table
- a predicted score
- a note about `/tmp/study-hours.png` **inside the container**

That PNG is in the container's ephemeral filesystem. It disappears when the container is removed (`--rm`). Lesson 14 shows how to keep files on the host.

---

## Intermediate Example

Prove `CMD` override and an interactive shell:

```bash
docker run --rm my-python-app python --version
docker run --rm -it my-python-app bash
```

In bash (full `python:3.12-slim` still has bash):

```bash
pwd
ls
python -c "import sklearn; print(sklearn.__version__)"
exit
```

`pwd` should be `/app`. `ls` should list `main.py` and `requirements.txt`.

Rebuild after a code change:

1. Edit `main.py` (for example, change the hello string).
2. `docker build -t my-python-app .`
3. Watch which steps say `CACHED`.
4. `docker run --rm my-python-app` and confirm the new string.

---

## Advanced Example

Tag both a version and latest:

```bash
docker build -t my-python-app:1.0 -t my-python-app:latest .
docker images my-python-app
```

Build with a different Dockerfile name (do this only if you renamed the file):

```bash
docker build -t my-python-app -f Dockerfile .
```

Show cache busting: add a blank line to `requirements.txt` or bump a version, rebuild, and notice `pip install` is not cached.

Apple Silicon vs Intel: the official Python image is multi-arch. A classmate on the other CPU family who **only** has your image file (not a rebuild) might need `--platform`. In class, each student **builds on their own machine**, which is the simple, correct approach.

---

## Practical Example

Full student loop:

```text
cd examples/python-docker-project
docker build -t my-python-app .
docker run --rm my-python-app
# edit main.py
docker build -t my-python-app .
docker run --rm my-python-app
```

**PowerShell:** `cd examples\python-docker-project` then the same `docker` commands. Backslashes are only for the host `cd`.

If build fails on `pip install`, read the pip error (network, typo in `requirements.txt`). If it fails on `COPY`, you are probably not in the project directory (context does not contain `requirements.txt`).

---

## Common Mistakes

1. **`docker build` without `.` or a path.** Usage error. The context is required.
2. **Building from the repo root by accident.** `COPY requirements.txt .` fails if that file is not in the context root.
3. **Expecting `docker run python:3.12` to use your Dockerfile.** You must run the **tag you built** (`my-python-app`).
4. **Forgetting to rebuild** after edits. The old image is unchanged until the next `build`.
5. **Tag typo.** `docker run mypythonapp` pulls from Hub if the local name does not exist. Use `docker images` to see local tags.
6. **Thinking `--rm` on run deletes the image.** It deletes the container. The image `my-python-app` remains.

---

## Best Practices

- `cd` to the project, then `docker build -t project-name .`
- Tag names you can remember (`my-python-app`, `course-jupyter:1.0`).
- Rebuild after every Dockerfile or dependency change; after code changes too unless you bind-mount (Lesson 14).
- Read the `CACHED` lines. They tell you whether your layer order is working.
- Do not publish this student image to Hub until you know what secrets you might have copied (Lesson 13).

---

## Exercises

1. **Build.** From `examples/python-docker-project`, `docker build -t my-python-app .`. Confirm success.
2. **List.** `docker images my-python-app`. Note IMAGE ID and SIZE.
3. **Run.** `docker run --rm my-python-app`. Copy the predicted score into your notes.
4. **Override.** `docker run --rm my-python-app python --version`.
5. **Edit.** Change the first `print` in `main.py`. Rebuild and rerun. Confirm cache hits on `pip install`.
6. **Wrong context.** From the **repository root**, run `docker build -t oops .` and explain why this is the wrong context for this project (no course Dockerfile there, or the wrong one). Then build from the project directory again.
7. **Shell.** `docker run --rm -it my-python-app bash` and run `ls /app`.

---

## Quick Review

- `docker build -t name .` turns a Dockerfile plus context into an image.
- `.` is the context; `COPY` can only see files inside it (minus dockerignore).
- Cache reuses unchanged layers; copy requirements before source.
- `docker run --rm my-python-app` runs `CMD`; extra args override `CMD`.

---

## Summary

You built and ran `my-python-app` from `examples/python-docker-project`. Next you will treat `requirements.txt` as a reproducibility tool: pinning, pip, and what happens when dependencies conflict.

---

[← Previous Lesson](10-dockerfile.md)
[Course Home](../README.md)
[Next Lesson →](12-python-dependencies.md)
