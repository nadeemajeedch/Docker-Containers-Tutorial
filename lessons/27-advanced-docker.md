# Lesson 27: Advanced Docker

**Optional / advanced.** You can finish the course without memorizing this lesson. It introduces BuildKit, health checks, resource limits, logging, custom networks, and richer Compose — enough to recognize them in docs.

[← Previous Lesson](26-security.md)
[Course Home](../README.md)
[Next Lesson →](28-image-optimization.md)

---

## Learning Objectives

After this lesson you will be able to:

- Recognize BuildKit output and keep it enabled (default on current Docker).
- Read a `HEALTHCHECK` instruction.
- Set memory/CPU limits on `run` and in Compose.
- Know where container logs go (`docker logs`).
- Attach a service to a custom network.
- Identify advanced Compose keys (`depends_on`, `profiles`, `healthcheck`).

---

## Prerequisites

- Lessons 18–21.
- Curiosity; not required for the final project unless your instructor says so.

---

## Concept

The Engine can do more than `build` / `run` / `compose up`:

| Topic | Why it exists |
|-------|----------------|
| BuildKit | Faster, parallel, better cache |
| Healthcheck | Orchestrators know if the process is alive |
| Limits | One container cannot eat the laptop |
| Logging | stdout/stderr via `docker logs` |
| Custom networks | Isolation beyond the default bridge |
| Advanced Compose | depends_on, profiles, restart, healthcheck |

Kubernetes and cloud platforms use the same ideas. This lesson stays on a single Docker Engine.

---

## Explanation

### BuildKit

Current Docker Desktop uses BuildKit by default. Build output looks like `#5 [2/5] WORKDIR /workspace`. You do not pass `--enable-buildkit` on modern installs.

Cache mounts and secret mounts exist (`RUN --mount=type=cache`). **Optional / advanced.** Part 3 Dockerfiles stay simple.

### Health checks

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8888')"
```

Compose:

```yaml
healthcheck:
  test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8888')"]
  interval: 30s
  timeout: 5s
  retries: 3
```

`docker ps` then shows `healthy` / `unhealthy`. Jupyter may need a few seconds before the probe succeeds. **Optional** for class Jupyter.

### Resource limits

```bash
docker run --rm -m 256m --cpus=1 python:3.12-slim python -c "print('ok')"
```

Compose (Compose file version-dependent syntax; this form is widely used):

```yaml
mem_limit: 512m
cpus: 1.0
```

On Desktop, the **app** also has a RAM cap in Settings. Container limits cannot exceed what Desktop gives the Linux VM.

### Logging

The default driver stores stdout/stderr. `docker logs` / `compose logs` read it. Do not log secrets. JSON-file rotation is a daemon setting; optional.

### Custom networks

```bash
docker network create labnet
```

Compose:

```yaml
networks:
  lab:
    driver: bridge
services:
  jupyter:
    networks: [lab]
```

Default project network is enough for this course. Custom networks matter when two stacks must talk (`external: true`). **Optional / advanced.**

### Advanced Compose

You already used `depends_on` (networking demo) and `profiles` (ml-docker). Also: `restart: unless-stopped`, `init: true`, `read_only: true`. Use them when you have a reason.

---

## Commands/Syntax

```bash
docker buildx version
docker run --rm -m 256m python:3.12-slim python -c "print('limited')"
docker network ls
docker compose --help
```

**PowerShell:** same.

---

## Beginner Example

```bash
docker run --rm -m 128m python:3.12-slim python -c "print('hello')"
```

If the command prints `hello`, limits did not break a tiny process. That is enough as a first contact.

---

## Intermediate Example

Add a healthcheck to a **copy** of compose-jupyter, `up -d`, `docker compose ps`. See if `health` appears. Remove it afterward if it flakes on slow machines.

---

## Advanced Example

Cache mount (do not add to course examples unless you maintain it):

```dockerfile
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
```

This is BuildKit-specific. Optional.

---

## Practical Example

For the final project, you may ignore this lesson except:

- Stay on default BuildKit
- Use `profiles` if you have a train + jupyter split
- Set a memory limit if a shared lab PC is tight

---

## Common Mistakes

1. Treating this lesson as required for Part 3 credit when the instructor did not assign it.
2. Healthchecks that run before Jupyter binds the port (false unhealthy).
3. Limits so low that pip or sklearn cannot start.
4. `external` networks without creating them first.

---

## Best Practices

- Default Compose network until you need more.
- Limits on shared machines.
- Healthchecks only if something will read them.
- Keep Dockerfiles readable; extra BuildKit syntax is optional.

---

## Exercises

1. `docker buildx version` (or skip if missing; Desktop usually has it).
2. Run a container with `-m 256m`.
3. `docker network ls` and name the Compose network while a project is up.
4. Read `depends_on` in `examples/networking-demo/compose.yaml`.
5. Label three features in this lesson as "I will use" vs "I will recognize."

---

## Quick Review

- Advanced = optional recognition, not new required tools.
- BuildKit is already on.
- Limits, health, custom networks, extra Compose keys exist.
- Final project can stay simple.

---

## Summary

You can read advanced docs without fear. Next: shrinking images with bases, dockerignore, layer order, and multi-stage builds.

---

[← Previous Lesson](26-security.md)
[Course Home](../README.md)
[Next Lesson →](28-image-optimization.md)
