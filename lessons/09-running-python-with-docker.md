# Lesson 9: Running Python with Docker

Part 2 starts here. You already know how to pull images and run containers. This lesson uses the official `python:3.12` image as a portable Python interpreter: interactive REPL, one-shot commands, and a script that lives on your computer.

[← Previous Lesson](08-docker-hub.md)
[Course Home](../README.md)
[Next Lesson →](10-dockerfile.md)

---

## Learning Objectives

After this lesson you will be able to:

- Run an interactive Python 3.12 REPL inside Docker without installing Python on the host.
- Run one-shot Python commands with `--rm`.
- Explain the path **host → Docker CLI → daemon → container → Python**.
- Run a local `hello.py` inside a container using a bind mount.
- Choose `python:3.12` vs `python:3.12-slim` for interactive work.

---

## Prerequisites

- Part 1 complete, especially Lessons 6–8.
- `docker version` shows a Server section.
- The image `python:3.12` available (`docker pull python:3.12` if needed).
- A text editor.

You do **not** need Python installed on Windows, macOS, or Linux. The interpreter in this lesson is the one inside the image.

---

## Concept

### Host, Docker, container, Python

When you type `docker run -it python:3.12`, four layers take part:

```text
You (host OS)
  └─ docker CLI          parses the command
       └─ Docker daemon  starts a container from python:3.12
            └─ process   /usr/local/bin/python   (inside the container)
```

The Python that prints `>>>` is **not** `python.exe` on Windows and not `/usr/bin/python3` on your Mac or Linux laptop. It is the interpreter packaged in the image.

That is why this works on a machine that has never installed Python:

```bash
docker run --rm python:3.12 python --version
```

and why the version can be 3.12 even if the host has 3.10, or no Python at all.

### Two ways to use official Python images in Part 2

| Goal | Pattern |
|------|---------|
| Explore, teach syntax, run a snippet | `docker run -it python:3.12` |
| Run a **file that lives on your disk** | Bind-mount the folder, then `python hello.py` |
| Repeatable app with dependencies | Dockerfile (Lessons 10–12) |

This lesson covers the first two. Bind mounts are introduced just enough to run `hello.py`. Lesson 14 explains mounts and named volumes in full.

### Official tags you will see

| Tag | Use in this course |
|-----|--------------------|
| `python:3.12` | Default. Full Debian-based image, includes a shell and common tools. |
| `python:3.12-slim` | Smaller. Fine for Dockerfiles. Slightly fewer OS packages. |
| `python:3.12-alpine` | Smallest. Different package manager (`apk`). Skip it until you need it. |

For a REPL, `python:3.12` is the comfortable choice.

---

## Explanation

### Interactive vs one-shot

`docker run -it python:3.12` starts the image **default command**, which is a Python REPL. `-i` keeps stdin open; `-t` gives you a terminal. Together they make typing possible.

`docker run --rm python:3.12 python --version` **replaces** that default command with `python --version`. Python starts, prints, exits. `--rm` deletes the container so `docker ps -a` stays clean.

### Why a script on the host is invisible unless you mount it

A container has its own filesystem (the image plus a writable layer). Your laptop's `hello.py` is not in that filesystem. Options:

1. `docker cp` the file in (Lesson 7). Awkward for editing.
2. **Bind-mount** the host directory into the container (this lesson and Lesson 14).
3. `COPY` the file when you **build** an image (Lesson 10).

For homework you are still editing, bind-mount is the right tool: save in your editor, run in Docker, repeat. No rebuild.

### The mount in one sentence

```text
host path  ──────────────────────────►  path inside the container
./examples/hello-python                 /app
```

Python inside the container reads `/app/hello.py`, which is the same bytes as `examples/hello-python/hello.py` on the host.

---

## Commands/Syntax

```bash
docker run -it python:3.12
docker run --rm python:3.12 python --version
docker run --rm python:3.12 python -c "print(2+2)"
```

Run a host file (Linux / macOS), from the repository root or any convenient directory:

```bash
docker run --rm -v "$PWD":/app -w /app python:3.12 python hello.py
```

| Piece | Meaning |
|-------|---------|
| `--rm` | Delete the container when Python exits |
| `-v "$PWD":/app` | Bind-mount the current directory at `/app` |
| `-w /app` | Working directory inside the container (`WORKDIR` equivalent for `run`) |
| `python:3.12` | Image |
| `python hello.py` | Command: interpreter + script name |

**Windows PowerShell:**

```powershell
docker run --rm -v "${PWD}:/app" -w /app python:3.12 python hello.py
```

If `${PWD}` is empty in an older PowerShell, use a full path:

```powershell
docker run --rm -v "C:\Users\You\Docker-Containers-Tutorial\examples\hello-python:/app" -w /app python:3.12 python hello.py
```

Host path is on the **left** of the colon. Container path is on the **right** and always uses forward slashes for Linux containers.

A sample script is in `examples/hello-python/hello.py`.

---

## Beginner Example

Version check, then a REPL:

```bash
docker pull python:3.12
docker run --rm python:3.12 python --version
docker run -it --rm python:3.12
```

At the `>>>` prompt:

```python
import sys
print(sys.version)
print(2 * 3)
```

Leave with `exit()` or Ctrl+D (Linux/macOS) or Ctrl+Z then Enter on some Windows consoles. Prefer `exit()`.

**PowerShell:** the `docker` lines are identical. Use Windows Terminal if the REPL ignores keystrokes.

---

## Intermediate Example

One-shot code without a file:

```bash
docker run --rm python:3.12 python -c "import sys; print(sys.platform); print(sys.version_info[:2])"
```

`sys.platform` inside the container is `linux` even when your host is Windows or macOS. The process runs on the Linux engine (Lesson 2).

Run the course sample (from `examples/hello-python`):

**Linux / macOS:**

```bash
cd examples/hello-python
docker run --rm -v "$PWD":/app -w /app python:3.12 python hello.py
```

**PowerShell:**

```powershell
cd examples/hello-python
docker run --rm -v "${PWD}:/app" -w /app python:3.12 python hello.py
```

Expected lines:

```text
Hello from Python inside Docker
This file lives on your host and runs in a container.
```

Edit `hello.py` in your editor, save, run the same `docker run` again. No rebuild. That is the edit loop for scripts.

---

## Advanced Example

### slim vs full

```bash
docker run --rm python:3.12-slim python --version
```

`slim` is smaller and usually enough. The full `python:3.12` image is nicer when you need `bash`, `nano`, or extra OS libraries while exploring.

### Reading stdin

```bash
echo 'print("from pipe")' | docker run --rm -i python:3.12 python
```

`-i` without `-t` is correct for pipes. **PowerShell:**

```powershell
"print('from pipe')" | docker run --rm -i python:3.12 python
```

### Confirm the host file is the one that ran

Add a line to `hello.py`, rerun the mount command, see the new output. If you omit `-v`, Docker looks for `hello.py` inside the image, does not find it, and errors. That failure is the lesson: **no mount, no host file.**

---

## Practical Example

Recommended first Part 2 session:

```text
1. docker run --rm python:3.12 python --version
2. docker run -it --rm python:3.12          # try a few expressions
3. cd examples/hello-python
4. docker run --rm -v <host>:/app -w /app python:3.12 python hello.py
5. Change hello.py, repeat step 4
```

Keep the mental model: **the editor is on the host; Python is in the container; the mount is the bridge.**

---

## Common Mistakes

1. **Expecting `python` on the host.** `python hello.py` in PowerShell may fail even while Docker Python works. Call `docker run ... python hello.py`.
2. **Forgetting `-v`.** `python: can't open file 'hello.py'` means the file is not in the container filesystem.
3. **Swapping host and container paths.** Left of `:` is host. Right is container.
4. **Windows backslashes in the container path.** Use `/app`, not `\app`.
5. **Running from the wrong directory.** `$PWD` / `${PWD}` is whatever directory you are in. `cd` first, or pass a full path.
6. **Using `-it` on a non-interactive one-shot.** Harmless often, but `--rm` plus a command is enough for `python --version`.

---

## Best Practices

- Pin `python:3.12` (or a patch tag) in lab notes, not `python:latest`.
- Use `--rm` for throwaway interpreter sessions.
- Bind-mount source you are editing; copy or build when you ship an app (Lesson 10).
- Stay in one working directory so `$PWD` is predictable.
- Do not install Python "just to try Docker." Trying Docker *is* using this image.

---

## Exercises

1. **Version.** `docker run --rm python:3.12 python --version`. Record the full string.
2. **REPL.** `docker run -it --rm python:3.12`. Print `sys.version` and `sys.platform`. Screenshot or copy the output.
3. **Snippet.** `docker run --rm python:3.12 python -c "print(sum(range(10)))"`. Predict the number first.
4. **hello.py.** From `examples/hello-python`, run the bind-mount command for your OS. Confirm both print lines.
5. **Edit loop.** Add `print("edited")` to `hello.py`, rerun, confirm. No `docker build`.
6. **Broken mount.** From that folder, run `docker run --rm -w /app python:3.12 python hello.py` **without** `-v`. Read the error. Then restore `-v`.
7. **Platform.** Explain in two sentences why `sys.platform` is `linux` on a Windows host.

---

## Quick Review

- Official `python:3.12` is a complete interpreter in an image.
- `docker run -it python:3.12` is the REPL; `--rm` plus a command is one-shot.
- Host files need a bind mount (or a later `COPY` in a Dockerfile).
- Path order: `host:container`. PowerShell uses `${PWD}`; bash/zsh uses `"$PWD"`.

---

## Summary

You can run Python without a local install: REPL, `-c`, and scripts via a bind mount. Next you will stop depending on the official image's default command and write a **Dockerfile** so the app, working directory, and startup command travel together.

---

[← Previous Lesson](08-docker-hub.md)
[Course Home](../README.md)
[Next Lesson →](10-dockerfile.md)
