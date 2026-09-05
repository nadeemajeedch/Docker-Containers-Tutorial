# Lesson 14: Volumes and Bind Mounts

Container filesystems are ephemeral. Delete the container and the writable layer is gone. This lesson explains bind mounts and named volumes so notebooks, source code, and data live on disk you control.

[← Previous Lesson](13-dockerignore.md)
[Course Home](../README.md)
[Next Lesson →](15-running-jupyter-with-docker.md)

---

## Learning Objectives

After this lesson you will be able to:

- Describe the container writable layer and why it is a poor place for homework.
- Use bind mounts (`-v` / `--mount type=bind`) to edit host files from a container.
- Use named volumes (`-v name:/path` / `--mount type=volume`) for Docker-managed persistence.
- Choose bind mounts for source and notebooks, named volumes for databases and generated data.
- Read `docker volume ls`, `docker volume inspect`, and `docker volume rm`.
- Write the same mount on Linux/macOS and Windows PowerShell.

---

## Prerequisites

- Lessons 7, 9, and 11.
- `python:3.12` image pulled.
- `examples/hello-python/hello.py` available.

---

## Concept

### Three places files can live

```text
1. Image layers          read-only, created at build
2. Container writable    ephemeral, deleted with docker rm
3. Mounts                host folder (bind) or Docker volume (named)
```

`docker run --rm` deletes the container, so anything written only in (2) is lost. The PNG in Lesson 11 (`/tmp/study-hours.png`) was an example of (2).

**Bind mount:** a host directory or file is visible at a path inside the container. Both sides see the same bytes. Ideal for source code and Jupyter notebooks you edit.

**Named volume:** Docker creates a directory it owns (on Linux, under Docker Root Dir; on Desktop, inside the Linux VM). The container sees it at a path you choose. The host path is not a folder you usually open in Explorer / Finder. Ideal for databases and caches.

**Anonymous volume:** a volume without a name. Harder to find later. Prefer named volumes.

### `-v` vs `--mount`

Both work. `--mount` is more explicit. `-v` is shorter and common in tutorials.

```bash
docker run --rm -v "$PWD":/app -w /app python:3.12 python hello.py

docker run --rm --mount type=bind,source="$PWD",target=/app -w /app python:3.12 python hello.py
```

Named volume:

```bash
docker run --rm -v mydata:/data python:3.12 python -c "open('/data/hi.txt','w').write('hi')"

docker run --rm --mount type=volume,source=mydata,target=/data python:3.12 python -c "print(open('/data/hi.txt').read())"
```

---

## Explanation

### Bind mount rules

| Side | Path rules |
|------|------------|
| Host (left of `:`) | Your OS path. PowerShell: `C:\Users\...` or `${PWD}`. bash: `"$PWD"` or `/home/you/proj`. |
| Container (right of `:`) | Linux path for this course: `/app`, `/home/jovyan/work`. Forward slashes. |

If the host path does not exist, Docker **may create an empty directory** (behavior has varied; do not rely on it). Create the folder yourself.

Bind-mounting over a path that had files in the **image** hides those image files for that container. The image is not deleted; the mount shadows the path.

### Named volume rules

```bash
docker volume create mydata
docker volume ls
docker volume inspect mydata
docker volume rm mydata
```

`docker run -v mydata:/data` creates `mydata` if it does not exist. `docker volume rm` fails if a container still uses the volume.

`docker system prune` without `--volumes` does **not** delete named volumes. That is why Lesson 5 told you not to prune volumes casually.

### What should not live only in the container

- Homework `.py` files
- Jupyter `.ipynb` notebooks
- Datasets you cannot download again
- Reports and figures you must submit

Those belong on a **bind mount** (or in git on the host). Use a named volume for a local Postgres data directory or similar — not for files you must zip and upload to a learning-management system.

---

## Commands/Syntax

### Bind mount, `-v`

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

### Bind mount, `--mount`

**Linux / macOS:**

```bash
docker run --rm --mount type=bind,source="$PWD",target=/app -w /app python:3.12 python hello.py
```

**PowerShell:**

```powershell
docker run --rm --mount "type=bind,source=${PWD},target=/app" -w /app python:3.12 python hello.py
```

Quoting the whole `--mount` value is the safe PowerShell habit.

### Named volume

```bash
docker volume create py-work
docker run --rm -v py-work:/work python:3.12 python -c "open('/work/note.txt','w').write('saved in a volume\n')"
docker run --rm -v py-work:/work python:3.12 python -c "print(open('/work/note.txt').read())"
docker volume inspect py-work
```

`--mount` form:

```bash
docker run --rm --mount type=volume,source=py-work,target=/work python:3.12 python -c "print(open('/work/note.txt').read())"
```

These volume commands are the same in PowerShell.

### Inspect a running container's mounts

```bash
docker run -dit --name mount-demo -v py-work:/work python:3.12 bash
docker inspect --format "{{json .Mounts}}" mount-demo
docker rm -f mount-demo
```

---

## Beginner Example

Lose a file on purpose, then do it the durable way.

Ephemeral (file dies with `--rm`):

```bash
docker run --rm python:3.12 python -c "open('/tmp/lost.txt','w').write('gone soon')"
```

There is no second container that can read `/tmp/lost.txt`.

Bind mount (file lives on the host):

**Linux / macOS:**

```bash
cd examples/hello-python
docker run --rm -v "$PWD":/app -w /app python:3.12 python -c "open('/app/from-container.txt','w').write('still here\n')"
cat from-container.txt
```

**PowerShell:**

```powershell
cd examples/hello-python
docker run --rm -v "${PWD}:/app" -w /app python:3.12 python -c "open('/app/from-container.txt','w').write('still here\n')"
Get-Content from-container.txt
```

`from-container.txt` remains after the container is gone. You may delete that demo file from the host when finished.

---

## Intermediate Example

Named volume survives new containers:

```bash
docker volume create py-work
docker run --rm -v py-work:/work python:3.12 python -c "open('/work/note.txt','w').write('hello volume\n')"
docker run --rm -v py-work:/work python:3.12 cat /work/note.txt
```

Second `run` is a **new** container. The volume still has `note.txt`.

List and inspect:

```bash
docker volume ls
docker volume inspect py-work
```

On Docker Desktop you will not typically browse that directory in Finder/Explorer. Use `docker run ... ls /work` or `docker cp` if you need a copy on the host. For class files you must submit, prefer a **bind mount**.

---

## Advanced Example

### Read-only bind mount

```bash
docker run --rm -v "$PWD":/app:ro -w /app python:3.12 python hello.py
```

`:ro` prevents the container from writing to the mount. Useful when you only want to execute code, not let it modify the homework folder.

PowerShell:

```powershell
docker run --rm -v "${PWD}:/app:ro" -w /app python:3.12 python hello.py
```

`--mount` equivalent:

```bash
docker run --rm --mount type=bind,source="$PWD",target=/app,readonly -w /app python:3.12 python hello.py
```

### Shadowing

```bash
docker run --rm -v "$PWD":/usr/local/lib/python3.12/site-packages python:3.12 python -c "import encodings"
```

Do **not** do this for real. Mounting over interpreter internals breaks Python. It illustrates: mounts win over image files at that path.

### Cleanup

```bash
docker volume rm py-work
```

If a container is using it, stop and remove that container first.

---

## Practical Example

Decision table for Part 2:

| Data | Mechanism | Example |
|------|-----------|---------|
| `hello.py` you are editing | Bind mount | Lesson 9 and this lesson |
| Jupyter notebooks | Bind mount | Lesson 15 `-v "$PWD":/home/jovyan/work` |
| pip packages | Image layer (`RUN pip`) | Lessons 11–12 |
| Plot written to `/tmp` in a `--rm` container | Lost | Mount `/tmp` or write to the bind-mounted folder |
| Local database files | Named volume | Later courses / Compose |

Jupyter in the next lesson is this lesson plus `-p 8888:8888`.

---

## Common Mistakes

1. **Saving notebooks only inside a `--rm` container** with no mount. Work vanishes.
2. **Swapping host and container paths.**
3. **Windows path on the container side.** Always `/app`, not `C:\app`.
4. **Unquoted `$PWD` with spaces** in the path. Quote it: `"$PWD":/app`.
5. **Named volume when you needed a zip-able folder.** You cannot easily email Docker's internal volume directory.
6. **`docker volume rm` on the wrong name.** `docker volume ls` first.
7. **Assuming `.dockerignore` applies to bind mounts.** It does not.

---

## Best Practices

- Bind-mount source and notebooks.
- Named volumes for engine-managed state.
- Quote paths.
- Use `--mount` when the `-v` syntax gets ambiguous (commas, multiple options).
- Never store the only copy of an assignment inside a container writable layer.
- Document the host path in your lab notes so you know where Jupyter saved the file.

---

## Exercises

1. **Ephemeral.** Write a file to `/tmp` in a `--rm` container. Explain why a second container cannot read it.
2. **Bind hello.** Run `hello.py` with `-v` as in Lesson 9.
3. **Bind `--mount`.** Same run with `--mount type=bind,...`.
4. **Write back.** Create `from-container.txt` via Python on a bind mount. Open it on the host.
5. **Named volume.** Create `py-work`, write `note.txt`, run a **new** container that prints it.
6. **Inspect.** `docker volume inspect py-work`. What is `Mountpoint`? (On Desktop it is a path inside the Linux VM.)
7. **PowerShell / bash.** Write the bind-mount command for **your** shell in your notes without looking.
8. **Cleanup.** `docker volume rm py-work` after no container uses it.

---

## Quick Review

- Writable layer dies with the container; mounts persist.
- Bind mount = host folder. Named volume = Docker-managed store.
- `-v host:container` and `--mount type=bind,source=...,target=...` are both valid.
- Homework and notebooks: bind mounts.

---

## Summary

You can persist files with bind mounts and named volumes, and you know which to use for classwork. Lesson 15 uses a bind mount plus port `8888` so JupyterLab runs in Docker while notebooks save on your computer.

---

[← Previous Lesson](13-dockerignore.md)
[Course Home](../README.md)
[Next Lesson →](15-running-jupyter-with-docker.md)
