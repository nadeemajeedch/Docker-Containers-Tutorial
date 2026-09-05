# Lesson 24: Debugging and Troubleshooting

When Docker fails, guesswork wastes time. This lesson uses **Problem → Cause → Diagnosis → Solution** for the failures students actually hit.

[← Previous Lesson](23-docker-for-machine-learning.md)
[Course Home](../README.md)
[Next Lesson →](25-best-practices.md)

---

## Learning Objectives

After this lesson you will be able to:

- Diagnose CLI, daemon, permission, port, exit, build, pip, volume, Windows path, Jupyter token, network, and Compose failures.
- Choose `docker version`, `ps`, `logs`, `inspect`, and `compose logs` in a sensible order.
- Fix Windows path and line-continuation mistakes.
- Avoid "reinstall Docker" as the first step.

---

## Prerequisites

- Parts 1–3 through Lesson 23.
- Cheatsheet: [troubleshooting](../cheatsheet/troubleshooting.md).

---

## Concept

Order of checks:

```text
1. Is the CLI on PATH?           docker --help
2. Is the daemon up?             docker version  (Server section)
3. Is the container running?     docker ps / docker compose ps
4. What did it print?            docker logs / compose logs
5. What did it mount/publish?    docker inspect / compose config
```

Most bugs are one of: daemon down, wrong directory, wrong path side of `-v`, port taken, process exited, or a Dockerfile cache/pip error.

---

## Explanation

Each item below is Problem → Cause → Diagnosis → Solution.

### Docker command not found

- **Cause:** Docker not installed, or terminal opened before PATH updated.
- **Diagnosis:** `docker --help` fails. Desktop not in Applications / Start Menu.
- **Solution:** Lesson 4 install. Open a **new** terminal. Windows: Docker Desktop running.

### Docker daemon not running

- **Cause:** Desktop still starting; Linux `docker` service stopped.
- **Diagnosis:** `docker version` has Client but no Server. Error contains `Cannot connect to the Docker daemon`.
- **Solution:** Start Desktop and wait. Linux Engine: start the docker service (you may need an instructor for systemd). Retry `docker version`.

### Permission errors (Linux)

- **Cause:** User not in `docker` group; socket is root-only.
- **Diagnosis:** `permission denied` on `/var/run/docker.sock`.
- **Solution:** Official post-install: add user to `docker` group, **log out and in**. Lab servers: follow site policy; `sudo docker` is a workaround on a personal VM only.

### Port already in use

- **Cause:** Another Jupyter/Compose project bound 8888.
- **Diagnosis:** `Bind for 0.0.0.0:8888 failed: port is already allocated`. `docker ps` shows the occupant.
- **Solution:** `docker compose down` in that project, or `docker stop <name>`, or set `JUPYTER_PORT=8889`.

### Container exits immediately

- **Cause:** Main process ended (Python finished, missing file, REPL with no TTY).
- **Diagnosis:** `docker ps -a` Status `Exited`. `docker logs <name>`.
- **Solution:** Read the traceback. For Jupyter, check `CMD` and `--ip=0.0.0.0`. For `python:3.12` detached, use `bash` or a long command (Lesson 7).

### Build failures

- **Cause:** Wrong context, missing `COPY` source, syntax error, base pull failed.
- **Diagnosis:** Build output stops on a `COPY` or `FROM` line.
- **Solution:** `cd` to the directory with the Dockerfile. Confirm filenames. Network for Hub. `--no-cache` only after you understand the error (Lesson 27).

### Python dependency errors

- **Cause:** Package not in `requirements.txt`; conflict; build used old cache after you edited requirements but Compose `up` without `--build`.
- **Diagnosis:** `ModuleNotFoundError` at run; pip conflict at build.
- **Solution:** Add the package, `docker compose up --build`. Do not `pip install` only inside a running container if you need it tomorrow.

### Volume mounting problems

- **Cause:** Host path wrong; swapped host/container; directory did not exist; shadowed image files.
- **Diagnosis:** `ls` inside the container (`compose exec`) vs host. Empty mount.
- **Solution:** Quote `"$PWD"`. PowerShell `${PWD}`. Create the host folder first. Align WORKDIR and volume target (Lesson 19).

### Windows path problems

- **Cause:** Backslashes in the **container** path; bash `\` continuation pasted into PowerShell; `${PWD}` empty.
- **Diagnosis:** Errors about invalid volume spec; file not found.
- **Solution:** Container paths use `/workspace/notebooks`. PowerShell continuation is backtick. Use a full `C:\...` host path if needed. Shared drives enabled in Desktop if an older setting requires it.

### Jupyter token issues

- **Cause:** Official image requires a token; logs ignored; empty-token custom image vs base-notebook mix-up; host port mismatch.
- **Diagnosis:** Browser login page; `docker logs` / `compose logs` for `token=`.
- **Solution:** Paste the URL from logs. If you mapped `8889:8888`, use localhost **8889**. Course custom images may use empty token **only on localhost**.

### Networking problems

- **Cause:** `localhost` inside container B; wrong port side; two projects.
- **Diagnosis:** Connection refused from a second container; browser works.
- **Solution:** Service name + **container** port (Lesson 21).

### Compose problems

- **Cause:** Old `docker-compose` hyphen; no `compose.yaml` in `.`; profile not enabled; project name clash.
- **Diagnosis:** `docker compose version` fails; `no configuration file`; service not started.
- **Solution:** Install Compose plugin. `cd` correctly. `--profile notebook` for ML Jupyter. `docker compose ls`.

---

## Commands/Syntax

```bash
docker version
docker ps -a
docker logs <container>
docker inspect <container>
docker compose ps
docker compose logs
docker compose config
```

`compose config` prints the **resolved** YAML (after `.env` interpolation). Use it when ports look wrong.

**PowerShell:** same.

---

## Beginner Example

Simulate daemon-down thinking: if Desktop is running, `docker version` shows Server. If you unpause that check when a command fails, you avoid debugging `run` for five minutes.

---

## Intermediate Example

Port conflict drill: start `examples/compose-jupyter` with `up -d`. In another terminal start it again or start `data-science-docker` on 8888. Read the error. `docker ps`. `down` one project.

---

## Advanced Example

```bash
cd examples/data-science-docker
docker compose config
```

Confirm `JUPYTER_PORT` interpolation. Change `.env`, `config` again.

---

## Practical Example

Keep [cheatsheet/troubleshooting.md](../cheatsheet/troubleshooting.md) open during labs. Walk the five-step order before changing the Dockerfile.

---

## Common Mistakes

1. Reinstalling Docker for a port clash.
2. Ignoring `logs`.
3. Fixing the host Python instead of the image.
4. Mixing bash and PowerShell continuation.

---

## Best Practices

- Logs before rebuilds.
- One stack on 8888 at a time.
- `compose config` for env/port confusion.
- Minimal reproduction: smallest command that still fails.

---

## Exercises

1. Write the five-step diagnosis order from memory.
2. Force a port clash (then `down`).
3. Run `docker compose config` in `data-science-docker`.
4. Pair each of these with a diagnosis command: daemon down, exited container, missing module.
5. Record your OS-specific path gotcha (Windows vs macOS vs Linux).

---

## Quick Review

- CLI → daemon → ps → logs → inspect/config.
- Port, mount, and `localhost` bugs are the usual suspects.
- Compose plugin and correct directory are required for Part 3.

---

## Summary

You have a playbook instead of superstition. Next: best practices that prevent many of these failures.

---

[← Previous Lesson](23-docker-for-machine-learning.md)
[Course Home](../README.md)
[Next Lesson →](25-best-practices.md)
