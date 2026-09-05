# Lesson 20: Environment Variables

Containers need configuration: ports, student names, API endpoints. **Environment variables** are the standard channel. This lesson covers `-e`, `--env-file`, Compose `environment` / `env_file`, `.env` files, and secrets you must not commit.

[← Previous Lesson](19-python-jupyter-compose.md)
[Course Home](../README.md)
[Next Lesson →](21-docker-networking.md)

---

## Learning Objectives

After this lesson you will be able to:

- Pass variables with `-e` / `--env` and `--env-file`.
- Use Compose `environment` and `env_file`.
- Distinguish Compose's project `.env` (interpolation) from a file mounted into the container.
- List what must never be committed to GitHub.
- Change the Jupyter host port with `${JUPYTER_PORT:-8888}`.

---

## Prerequisites

- Lessons 7 and 18.
- Optional: `examples/data-science-docker` (has `.env.example`).

---

## Concept

An environment variable is a key/value pair visible to a process (`os.environ` in Python).

**Host → container**

```bash
docker run --rm -e STUDENT_NAME=ada python:3.12 python -c "import os; print(os.environ['STUDENT_NAME'])"
```

`--env` is the same as `-e`.

**File of variables**

```bash
docker run --rm --env-file .env.example python:3.12 python -c "import os; print(os.environ.get('STUDENT_NAME'))"
```

`--env-file` does not require Compose.

---

## Explanation

### Three layers (easy to mix up)

| Mechanism | Who reads it | Typical use |
|-----------|--------------|-------------|
| `-e KEY=value` | Container process | One-off overrides |
| `--env-file file` or Compose `env_file` | Container process | Lists of non-secret config |
| Compose project `.env` next to `compose.yaml` | **Compose**, for `${VAR}` interpolation in the YAML | `JUPYTER_PORT=8889` |

A project `.env` is **not** automatically copied into the container unless you also list those keys under `environment` or `env_file`.

### Compose interpolation

```yaml
ports:
  - "${JUPYTER_PORT:-8888}:8888"
environment:
  STUDENT_NAME: ${STUDENT_NAME:-anonymous}
```

`${JUPYTER_PORT:-8888}` means: use `JUPYTER_PORT` if set (shell or project `.env`), otherwise 8888.

### Secrets

**Never commit:**

- Passwords, API keys, tokens, private `.pem` files
- Cloud credentials
- `.env` files that contain any of the above

**Do commit:**

- `.env.example` with **dummy** values and comments
- `compose.yaml` that references `${VAR}` without putting the secret in Git

This course's `.env.example` files only have a display name and a port. Still treat real keys as secrets.

`.gitignore` in the templates ignores `.env`.

### Not a substitute for `requirements.txt`

Do not pass library versions as ad-hoc env vars instead of pinning pip. Env vars configure **runtime**; dependencies belong in the image.

---

## Commands/Syntax

```bash
docker run --rm -e STUDENT_NAME=ada python:3.12 python -c "import os; print(os.environ['STUDENT_NAME'])"
docker run --rm --env STUDENT_NAME=ada python:3.12 python -c "import os; print(os.environ['STUDENT_NAME'])"
```

**PowerShell** quoting:

```powershell
docker run --rm -e STUDENT_NAME=ada python:3.12 python -c "import os; print(os.environ['STUDENT_NAME'])"
```

Compose (from `examples/data-science-docker`):

```bash
cp .env.example .env
# edit STUDENT_NAME in .env
docker compose up --build
```

**PowerShell:** `Copy-Item .env.example .env`

Inside a notebook, `os.environ.get("STUDENT_NAME")` should match.

---

## Beginner Example

```bash
docker run --rm -e GREETING=hello python:3.12 python -c "import os; print(os.environ['GREETING'])"
```

Prints `hello`. No Compose required.

---

## Intermediate Example

```bash
cd examples/data-science-docker
cp .env.example .env
```

Set `STUDENT_NAME=sam` and `JUPYTER_PORT=8888` in `.env`. `docker compose up --build`. In `01-explore.ipynb` the first cell prints `STUDENT_NAME`.

Change `JUPYTER_PORT=8889` if 8888 is taken, `down`, `up` again, browse `http://localhost:8889`.

---

## Advanced Example

`env_file` with `required: false` (Compose spec) lets classmates run without copying `.env` first; defaults in YAML still apply. If you write `env_file: .env` without that, Compose errors when the file is missing.

Do **not** `COPY .env` in a Dockerfile. That bakes secrets into layers (Lesson 13). Pass env at **run** / Compose time.

---

## Practical Example

Safe GitHub layout:

```text
compose.yaml
.env.example      # committed
.env              # gitignored, local only
```

README says: `cp .env.example .env` then edit.

---

## Common Mistakes

1. **Committing `.env` with a token.** Rotate the token; add `.gitignore`.
2. **Setting a var in project `.env` and expecting `os.environ` inside the container** without listing it under `environment`.
3. **Spaces around `=` in env files.** `KEY=value` not `KEY = value`.
4. **Using env vars for secrets in `docker history` / `docker inspect`.** They are visible to anyone who can inspect the container. For real secrets, later tools (Compose secrets, vaults) exist; for class, keep secrets off the machine when possible.
5. **PowerShell `$VAR` expansion** eating Compose interpolation. Quote or use a `.env` file.

---

## Best Practices

- `.env.example` committed; `.env` ignored.
- Defaults in YAML (`${VAR:-default}`).
- No secrets in Dockerfiles.
- Prefer env for config, images for code and libraries.
- Empty Jupyter tokens are **not** secrets; they are a local-dev shortcut (Lesson 26).

---

## Exercises

1. `-e` one-off print as in Beginner Example.
2. Copy `.env.example` in `examples/data-science-docker`, set your name, confirm in the notebook.
3. Change `JUPYTER_PORT` and open the matching `localhost` port.
4. List five strings that must never appear in a public GitHub repo.
5. Explain in four sentences the difference between Compose interpolation `.env` and `env_file`.

---

## Quick Review

- `-e` / `--env` / `--env-file` inject container env.
- Compose `.env` interpolates YAML; `environment` / `env_file` reach the process.
- Commit examples, not secrets.
- Ports can be parameterized with `${JUPYTER_PORT:-8888}`.

---

## Summary

You can configure containers without rebuilding images, and you know what GitHub must never see. Next: how containers talk on networks, and why `localhost` inside a container is not your laptop.

---

[← Previous Lesson](19-python-jupyter-compose.md)
[Course Home](../README.md)
[Next Lesson →](21-docker-networking.md)
