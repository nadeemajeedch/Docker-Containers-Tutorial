# Lesson 18: Docker Compose

Part 3 starts here. You already build images and run containers by hand. **Docker Compose** describes a whole application — one or more services, ports, volumes, and networks — in a YAML file, then starts it with one command.

[← Previous Lesson](17-jupyter-project.md)
[Course Home](../README.md)
[Next Lesson →](19-python-jupyter-compose.md)

---

## Learning Objectives

After this lesson you will be able to:

- Explain what Compose is and when to use `compose.yaml` instead of a long `docker run`.
- Read modern Compose syntax (`services`, `build`, `ports`, `volumes`).
- Run `docker compose up`, `up -d`, `ps`, `logs`, `exec`, and `down`.
- Map Compose fields to flags you already know (`-p`, `-v`, `--name`).
- Use the course example in `examples/compose-jupyter`.

---

## Prerequisites

- Parts 1 and 2 complete (especially Lessons 11, 14, 16).
- Docker Desktop or Engine with the **Compose plugin** (`docker compose version`). This course uses `docker compose` (space), not the old `docker-compose` (hyphen) binary.

---

## Concept

A Compose file is a declarative description of containers. The current filename is **`compose.yaml`** (also accepted: `compose.yml`, `docker-compose.yml`). This course uses `compose.yaml`.

```yaml
services:
  jupyter:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/workspace/notebooks
```

| Key | Meaning | Rough `docker run` equivalent |
|-----|---------|------------------------------|
| `services` | Named containers in this app | each `docker run` |
| `build: .` | Build from Dockerfile in this directory | `docker build` then run that image |
| `ports` | Publish host:container | `-p 8888:8888` |
| `volumes` | Bind mounts or named volumes | `-v ./notebooks:/workspace/notebooks` |

Compose also creates a **project network** so services can reach each other by **service name** (Lesson 21).

The **project name** defaults to the directory name. Containers are named like `compose-jupyter-jupyter-1`.

---

## Explanation

### One service vs many

Lesson 17 used a single `docker run`. Compose is still useful for one service: the flags live in Git, classmates do not have to copy a command. Multi-container apps (web + database, train + jupyter) are the real payoff. Lesson 23's ML example has two services.

### Lifecycle

```text
docker compose up        build if needed, start, attach logs
docker compose up -d     same, detached
docker compose ps        containers in this project
docker compose logs      logs for the project
docker compose exec      run a command in a running service
docker compose down      stop and remove project containers (and the default network)
```

`down` does **not** delete bind-mounted host files. It does not delete images unless you add `--rmi`. Named volumes are kept unless you add `-v` (dangerous if you stored data there).

### `up --build`

```bash
docker compose up --build
```

Rebuilds images before starting. Use it after Dockerfile or `requirements.txt` changes.

### Plugin vs hyphen

```bash
docker compose version
```

If this fails but `docker-compose` (hyphen) works, you have the old standalone tool. Install/update Docker Desktop or the Compose plugin. This course documents **`docker compose`**.

---

## Commands/Syntax

From `examples/compose-jupyter`:

```bash
cd examples/compose-jupyter
docker compose version
docker compose up --build
```

**Windows PowerShell:** the same commands. Line continuation is not required here.

Other commands:

```bash
docker compose up -d --build
docker compose ps
docker compose logs
docker compose logs -f jupyter
docker compose exec jupyter python --version
docker compose down
```

| Command | Purpose |
|---------|---------|
| `up` | Create and start |
| `up -d` | Detached |
| `up --build` | Rebuild images |
| `ps` | Project containers |
| `logs` / `logs -f` | Logs / follow |
| `exec SERVICE CMD` | Extra process in a **running** service |
| `down` | Stop and remove project containers |

Foreground `up`: Ctrl+C stops the attached services (Compose stops them). Detached: use `down` or `stop`.

---

## Beginner Example

```bash
cd examples/compose-jupyter
docker compose up --build
```

Open `http://localhost:8888`. Create a notebook under the Jupyter file browser, save, Ctrl+C, then:

```bash
ls notebooks
```

**PowerShell:** `Get-ChildItem notebooks`

The file is on the host because of the bind mount in `compose.yaml`.

---

## Intermediate Example

Detached workflow:

```bash
docker compose up -d --build
docker compose ps
docker compose logs jupyter
docker compose exec jupyter python -c "import sklearn; print(sklearn.__version__)"
docker compose down
```

`exec` fails if the service is not running. Start with `up -d` first.

---

## Advanced Example

Override the Compose file name:

```bash
docker compose -f compose.yaml ps
```

Set the project name explicitly (avoids clashes if two folders are named the same):

```bash
docker compose -p course-jupyter up -d
docker compose -p course-jupyter down
```

Scale is an advanced topic (replicas). Jupyter is **not** something you scale with `--scale` on one port. Skip scaling until you have a stateless HTTP API.

---

## Practical Example

Translate Lesson 16's `docker run` into Compose (already done in `examples/compose-jupyter`):

```bash
docker run --rm -p 8888:8888 -v "$PWD/notebooks":/workspace/notebooks course-jupyter:1.0
```

becomes `build`, `ports`, and `volumes` in YAML. Prefer the YAML in a shared repo so nobody forgets `-v`.

---

## Common Mistakes

1. **`docker-compose` vs `docker compose`.** Use the plugin form in this course.
2. **Running Compose from the wrong directory.** It looks for `compose.yaml` in `.`
3. **Assuming `down` deletes notebooks.** Bind mounts stay on the host.
4. **`exec` before the container is healthy.** `ps` first.
5. **Two projects both publishing 8888.** Stop the other stack or change the host port (Lesson 20).

---

## Best Practices

- Name the file `compose.yaml`.
- Pin what you can in the Dockerfile; keep Compose for wiring.
- `up --build` after dependency changes.
- `down` at the end of a lab so ports free up.
- Commit `compose.yaml`; do not commit secrets (Lesson 20).

---

## Exercises

1. **Version.** `docker compose version`. Record the version.
2. **Up.** From `examples/compose-jupyter`, `docker compose up --build`. Open Jupyter.
3. **Persist.** Save a notebook, Ctrl+C, confirm it on the host.
4. **Detached.** `up -d`, `ps`, `logs`, `exec jupyter python --version`, `down`.
5. **Map.** Write a table of three Compose keys and their `docker run` flags.

---

## Quick Review

- Compose YAML describes services, ports, volumes, networks.
- `up` / `up -d` / `ps` / `logs` / `exec` / `down` are the daily set.
- `docker compose` (space) is current.
- `down` removes containers, not bind-mounted homework.

---

## Summary

You can start a documented multi-flag container with `docker compose up`. Next you will run the Python/Jupyter stack specifically through Compose and compare it to Part 2's `docker run`.

---

[← Previous Lesson](17-jupyter-project.md)
[Course Home](../README.md)
[Next Lesson →](19-python-jupyter-compose.md)
