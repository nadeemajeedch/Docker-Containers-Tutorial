# Lesson 7: Docker Containers

A container is a runnable instance of an image. This lesson covers the container lifecycle and the commands you will use constantly: run, start, stop, logs, exec, inspect, copy, rename, stats, and remove.

[← Previous Lesson](06-docker-images.md)
[Course Home](../README.md)
[Next Lesson →](08-docker-hub.md)

---

## Learning Objectives

After this lesson you will be able to:

- Describe the container lifecycle: created, running, paused, stopped (exited), removed.
- Use `docker run` with `--rm`, `-it`, `-d`, `--name`, and `-p`.
- Start, stop, restart, and remove containers.
- Read logs, execute commands inside a running container, and inspect metadata.
- Copy files with `docker cp` and rename containers.
- Watch live resource use with `docker stats`.
- Clean up containers without deleting images you still need.

---

## Prerequisites

- Lessons 1–6.
- `python:3.12` image present (`docker pull python:3.12`).
- Lesson 4 verification still passing.

---

## Concept

### Lifecycle

```text
docker run
   │
   ▼
 created ──► running ──► exited (stopped)
                │              │
                │              ├── docker start ──► running
                │              └── docker rm    ──► gone
                │
                ├── docker stop  ──► exited
                ├── docker kill  ──► exited (faster, SIGKILL)
                └── docker rm -f ──► gone (stop + remove)
```

Important states for Part 1:

| State | Meaning | Visible in |
|-------|---------|------------|
| Running | Process is alive | `docker ps` and `docker ps -a` |
| Exited | Process finished or was stopped | `docker ps -a` only |
| Removed | Metadata and writable layer deleted | nowhere |

An **exited** container is not an image. It still has a writable layer, logs, and a name. That is why `hello-world` leftovers show up in `docker ps -a`.

### `run` vs `start`

- `docker run` = **create** a new container from an image, then **start** it.
- `docker start` = start an **existing** stopped container (same writable layer, same name).

If you `run` twice, you get **two** containers (unless names collide). If you `run`, `stop`, `start`, you have **one** container.

### The writable layer

The image is read-only. Each container gets a thin writable layer. Files you create inside the container live there. `docker rm` deletes that layer. **Data only in the writable layer is lost when the container is removed.** (Named volumes are the durable option; they are not the focus of Part 1.)

### Foreground, detached, interactive

| Style | Typical flags | Behavior |
|-------|---------------|----------|
| Foreground | default `docker run` | Your terminal is attached to the process; Ctrl+C usually stops it |
| Interactive TTY | `-it` | You type into a shell or REPL |
| Detached | `-d` | Container runs in the background; your prompt returns |
| Auto-remove | `--rm` | Container is deleted when it exits |

`-i` keeps STDIN open. `-t` allocates a terminal. You almost always use them together: `-it`.

### Naming

Without `--name`, Docker assigns a random name (`funny_einstein`). Use `--name py-lab` for anything you will start twice or exec into.

Names must be unique among containers (running or stopped) until you `docker rm` the old one.

---

## Why It Matters

Images are inert. All real work happens in containers: servers, REPLs, one-shot scripts, graders. If you cannot stop a runaway container, read its logs, or exec into it, you cannot debug. Part 2's Jupyter workflow is this lesson plus a port mapping and a volume — not a new universe.

---

## Commands/Syntax

### Create and start

```bash
docker run hello-world
docker run --rm python:3.12 python --version
docker run -it python:3.12
docker run -dit --name py-lab python:3.12
```

| Flag | Long form | Meaning |
|------|-----------|---------|
| `--rm` | | Remove container on exit |
| `-i` | `--interactive` | Keep STDIN open |
| `-t` | `--tty` | Allocate a pseudo-TTY |
| `-d` | `--detach` | Run in the background |
| `--name` | | Assign a name |
| `-p` | `--publish` | Map host port to container port (`8080:80`) |

`-dit` is `-d -i -t`: detached but ready for later `docker exec -it`.

The `python:3.12` image's default command is a Python REPL. In detached mode without a TTY, that REPL may exit immediately because it has no input. **Keeping a Python container alive** for labs:

```bash
docker run -dit --name py-lab python:3.12 python -c "import time; time.sleep(3600)"
```

or start a shell:

```bash
docker run -dit --name py-lab python:3.12 bash
```

The official `python` image includes bash. A sleeping or bash process stays running so you can `exec` into it.

### List

```bash
docker ps
docker ps -a
```

### Stop, start, restart

```bash
docker stop py-lab
docker start py-lab
docker restart py-lab
```

`stop` sends SIGTERM, waits, then SIGKILL. Default wait is 10 seconds.

```bash
docker stop -t 5 py-lab
```

`-t 5` waits 5 seconds.

### Remove containers

```bash
docker rm py-lab
```

Fails if the container is running. Stop first, or:

```bash
docker rm -f py-lab
```

`-f` force-removes a running container.

**Not the same as** `docker rmi` (images).

### Logs

```bash
docker logs py-lab
docker logs --tail 50 py-lab
docker logs -f py-lab
```

| Flag | Meaning |
|------|---------|
| `--tail 50` | Last 50 lines |
| `-f` | Follow (like `tail -f`); Ctrl+C stops following, **not** the container |

`logs` works on running and exited containers.

### Execute inside a running container

```bash
docker exec py-lab python --version
docker exec -it py-lab bash
```

`exec` requires a **running** container. It starts an **additional** process in that container's namespaces. It is not SSH, but it feels similar.

Exit an interactive exec session with `exit`. That does **not** stop the container (unlike exiting a foreground `docker run -it` that *is* the main process).

### Inspect

```bash
docker inspect py-lab
docker inspect --format "{{.State.Status}}" py-lab
docker inspect --format "{{.State.Pid}}" py-lab
docker inspect --format "{{.Image}}" py-lab
```

`inspect` works on containers and on images. Pass a container name or ID here.

### Copy files

```bash
docker cp py-lab:/etc/hostname ./hostname-from-container
docker cp ./notes.txt py-lab:/tmp/notes.txt
```

**Linux/macOS:** paths as shown.

**Windows PowerShell:** use PowerShell paths on the host side:

```powershell
docker cp py-lab:/etc/hostname .\hostname-from-container
docker cp .\notes.txt py-lab:/tmp/notes.txt
```

Container paths always use **forward slashes** and Linux layout (`/tmp/...`) for Linux containers.

`docker cp` works with running or stopped containers.

### Rename

```bash
docker rename py-lab python-lab
```

Renames an existing container. Does not require a restart.

### Stats

```bash
docker stats
docker stats py-lab
```

Live CPU, memory, net, and disk I/O. Ctrl+C leaves the view; containers keep running.

One-shot (no stream) — useful in scripts and PowerShell:

```bash
docker stats --no-stream
```

### Help reminders

```bash
docker run --help
docker exec --help
docker logs --help
```

---

## Beginner Example

One-shot, then gone:

```bash
docker run --rm python:3.12 python --version
docker ps -a
```

No leftover container from that run.

Hello World leftover cleanup:

```bash
docker run hello-world
docker ps -a
docker rm <id_or_name>
```

Interactive REPL (foreground):

```bash
docker run -it --rm python:3.12
```

You should see `>>>`. Try:

```python
print("hello from a container")
```

Then `exit()` or Ctrl+D. `--rm` deletes the container.

**PowerShell:** the same `docker run -it --rm python:3.12` command. If the REPL does not accept input, use Windows Terminal and confirm Docker Desktop is running.

---

## Intermediate Example

Named container you can stop and start:

```bash
docker run -dit --name py-lab python:3.12 bash
docker ps
docker exec py-lab python --version
docker exec -it py-lab python -c "print(2+2)"
docker logs py-lab
docker stop py-lab
docker ps -a
docker start py-lab
docker exec py-lab python --version
docker stop py-lab
docker rm py-lab
```

If `bash` is not available in some slim tags, use `python:3.12` (full) as specified, not `slim`.

Inspect after start:

```bash
docker run -dit --name py-lab python:3.12 bash
docker inspect --format "{{.State.Status}}" py-lab
docker inspect --format "{{.Config.Image}}" py-lab
```

You want `running` and `python:3.12`.

---

## Advanced Example

### Port publishing (preview for Part 2)

```bash
docker run --rm -p 8080:80 nginx:alpine
```

`-p 8080:80` means host port 8080 maps to container port 80. Browse `http://localhost:8080`. Ctrl+C stops the foreground container; `--rm` removes it.

You do not need nginx for Part 1 fluency, but `-p` is the flag Jupyter will use later.

### Copy a file in and read it back

Linux/macOS:

```bash
echo "lab note" > /tmp/lab-note.txt
docker run -dit --name py-lab python:3.12 bash
docker cp /tmp/lab-note.txt py-lab:/tmp/lab-note.txt
docker exec py-lab cat /tmp/lab-note.txt
docker cp py-lab:/tmp/lab-note.txt ./lab-note-copy.txt
docker rm -f py-lab
```

PowerShell:

```powershell
Set-Content -Path .\lab-note.txt -Value "lab note"
docker run -dit --name py-lab python:3.12 bash
docker cp .\lab-note.txt py-lab:/tmp/lab-note.txt
docker exec py-lab cat /tmp/lab-note.txt
docker cp py-lab:/tmp/lab-note.txt .\lab-note-copy.txt
docker rm -f py-lab
```

### Stats and inspect together

```bash
docker run -dit --name py-lab python:3.12 bash
docker stats --no-stream py-lab
docker inspect py-lab
docker rm -f py-lab
```

### Restart policy (awareness only)

```bash
docker run -dit --name py-lab --restart unless-stopped python:3.12 bash
```

`--restart unless-stopped` restarts the container if the daemon restarts, unless you explicitly stopped it. Optional. Remove with `docker rm -f py-lab` when done.

---

## Practical Example

Capstone sequence (also listed in the course README):

```bash
docker pull python:3.12
docker run -dit --name py-lab python:3.12 bash
docker ps
docker exec py-lab python --version
docker inspect --format "{{.Image}}" py-lab
docker logs py-lab
docker rename py-lab python-lab
docker ps
docker stop python-lab
docker start python-lab
docker stop python-lab
docker rm python-lab
docker system df
```

If you created files with `docker cp`, include those steps between `exec` and `rename`.

Do **not** `docker rmi python:3.12` yet if you still need it for Lesson 8 exercises.

---

## Common Mistakes

1. **`docker rm` on a running container without `-f`.** Stop first or use `-f`.
2. **`docker exec` on an exited container.** Start it, or use `run` instead.
3. **Exiting `exec -it bash` and thinking the container stopped.** Only the exec process ended. `docker ps` still shows it.
4. **Exiting `docker run -it` main process and wondering why the container exited.** That process *was* the container's PID 1.
5. **Detached Python REPL exits immediately.** Give it `bash` or a long-running command.
6. **Name already in use.** `docker ps -a` — a stopped container still holds the name. `docker rm` it or pick another name.
7. **`docker rmi` when you meant `docker rm`.**
8. **`logs -f` vs `stats`:** Ctrl+C stops the *view*, not always what beginners expect; `logs -f` does not stop the container.
9. **Windows paths with backslashes inside the container.** Use `/tmp/file` in the container, backslashes only on the host path in PowerShell.

---

## Best Practices

- Name containers you will reuse (`--name`).
- Use `--rm` for throwaway experiments.
- Prefer `stop` then `rm` over reflexive `rm -f` until you are sure.
- `docker ps -a` before assuming something "vanished."
- `exec` for debugging; do not install a permanent SSH server in the container for Part 1.
- Copy files with `docker cp` for small one-off transfers; use volumes later for real projects.
- `docker stats --no-stream` when you need a snapshot for a report.

---

## Exercises

1. **Hello lifecycle.** Run `hello-world` without `--rm`. Find it with `docker ps -a`. Remove it with `docker rm`.
2. **One-shot Python.** `docker run --rm python:3.12 python --version`.
3. **Interactive.** `docker run -it --rm python:3.12`. Print `2+2` in the REPL. Exit.
4. **Named lab.** `docker run -dit --name py-lab python:3.12 bash`. Confirm `docker ps`.
5. **Exec.** `docker exec py-lab python --version` and `docker exec -it py-lab bash` (type `exit` after `uname -a`).
6. **Logs.** `docker logs py-lab`. Then `docker logs --tail 10 py-lab`.
7. **Inspect.** Status, PID, and image via `docker inspect --format`.
8. **Copy.** Create a small host file, `docker cp` it in, `exec cat` it, `docker cp` it out.
9. **Rename.** `docker rename py-lab python-lab`. Verify with `docker ps`.
10. **Stop/start.** `docker stop python-lab`, `docker ps -a`, `docker start python-lab`, `docker exec python-lab python --version`.
11. **Stats.** `docker stats --no-stream python-lab`.
12. **Cleanup.** `docker stop python-lab` (if needed) and `docker rm python-lab`. Confirm `docker ps -a` no longer lists it. Run `docker images` and confirm `python:3.12` is still there.
13. **Mistake recovery.** Intentionally `docker run --name py-lab ...` twice. Read the name-conflict error. Fix it.

---

## Quick Review

- `run` creates and starts; `start` restarts an existing container.
- `ps` vs `ps -a`; `rm` vs `rmi`.
- `-it` interactive, `-d` detached, `--rm` ephemeral, `--name` stable identity.
- `logs`, `exec`, `inspect`, `cp`, `rename`, `stats` are the daily debug toolkit.
- Removing a container deletes its writable layer, not the image.

---

## Summary

You can now manage a container through its whole life. That is the core operational skill of Part 1. Lesson 8 places images in their public home — Docker Hub — so you know what you are pulling and how tags and official images work.

---

[← Previous Lesson](06-docker-images.md)
[Course Home](../README.md)
[Next Lesson →](08-docker-hub.md)
