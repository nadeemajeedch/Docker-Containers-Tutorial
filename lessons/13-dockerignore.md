# Lesson 13: .dockerignore

`.dockerignore` tells `docker build` which files **not** to send as part of the build context. It keeps images smaller, builds faster, and reduces the chance of copying secrets or junk.

[← Previous Lesson](12-python-dependencies.md)
[Course Home](../README.md)
[Next Lesson →](14-volumes-and-bind-mounts.md)

---

## Learning Objectives

After this lesson you will be able to:

- Explain the build context and why extra files still cost you even if you never `COPY` them.
- Write a `.dockerignore` for a Python project.
- Exclude `.git`, virtualenvs, `__pycache__`, `.env`, and local artifacts.
- Confirm that ignored files are not in the image.
- Avoid ignoring `requirements.txt` or `main.py` by accident.

---

## Prerequisites

- Lessons 10–12.
- The project in `examples/python-docker-project` (it already contains a `.dockerignore`).

---

## Concept

When you run `docker build -t my-python-app .`, the Docker **client** packs the current directory (the context) and sends it to the **daemon**. `COPY` and `ADD` can only see files inside that packet.

If the directory contains a 2 GB `data/` folder, a `.venv`, or `.git`, that data is uploaded unless ignored — even when the Dockerfile only copies `requirements.txt` and `main.py`. Large contexts make builds slow and can fill disks.

`.dockerignore` sits next to the Dockerfile and uses gitignore-like patterns. Matching files are **omitted from the context**.

```text
project/
  Dockerfile
  .dockerignore     ← filter
  main.py           ← needed
  requirements.txt  ← needed
  .venv/            ← ignore
  .git/             ← ignore
```

This is **not** the same as `.gitignore`. Git ignore controls version control. Docker ignore controls the build context. Keep both. They often list similar entries.

---

## Explanation

### Patterns

```text
.git
.gitignore
__pycache__
*.pyc
.venv
venv
.env
.DS_Store
Thumbs.db
```

| Pattern | Effect |
|---------|--------|
| `.git` | Drop the Git metadata directory |
| `*.pyc` | Drop compiled bytecode files |
| `.venv` / `venv` | Drop virtualenvs (wrong Python, huge) |
| `.env` | Drop local secrets (API keys, passwords) |
| `.DS_Store` / `Thumbs.db` | OS junk |

`**` and trailing slashes work similarly to gitignore. Start simple.

### What you must not ignore

Do **not** ignore:

- `Dockerfile` (the client still reads it from disk, but do not get clever)
- `requirements.txt`
- Application source you `COPY`

If you ignore `*.py`, `COPY . .` will not include `main.py`, and `CMD ["python", "main.py"]` will fail at runtime.

### Secrets

If `.env` is not ignored and you `COPY . .`, those variables are **baked into an image layer**. Deleting the file later and rebuilding without `--no-cache` may still leave the old layer in history. Never copy secrets. Ignore them, pass them at **run** time later (env files, orchestrators). Part 2 does not need Hub tokens inside the image.

### Course file

`examples/python-docker-project/.dockerignore` also ignores `README.md` and `*.png`. README is not required to run `main.py`. Ignoring it is optional documentation hygiene, not a law.

---

## Commands/Syntax

There is no `docker dockerignore` command. You edit a file named `.dockerignore`.

Verify a file did **not** land in the image:

```bash
docker run --rm my-python-app ls -la /app
```

You should see `main.py` and `requirements.txt`. You should **not** see `.git` or `.venv`.

Check context size indirectly: after adding a huge ignored folder, rebuilds should not suddenly upload gigabytes. BuildKit prints transfer size in the `load build context` step.

**PowerShell:** `ls` inside the container is Linux `ls` because the image is Linux:

```powershell
docker run --rm my-python-app ls -la /app
```

Do not use `dir` as the container command unless the image is Windows containers (this course is Linux containers).

Show hidden files on the host so you can edit `.dockerignore`:

- Linux/macOS: `ls -la`
- PowerShell: `Get-ChildItem -Force`

---

## Beginner Example

Open `examples/python-docker-project/.dockerignore` and read each line. Rebuild if you have not since Lesson 11:

```bash
cd examples/python-docker-project
docker build -t my-python-app .
docker run --rm my-python-app ls -la /app
```

Confirm there is no `.git` directory inside `/app`.

---

## Intermediate Example

Create a dummy file that **should** be ignored, and one that **should** copy:

```bash
# from examples/python-docker-project
echo ignored > junk.log
echo keep > notes-for-app.txt
```

Add `*.log` to `.dockerignore` if it is not already there. Rebuild and list `/app`:

```bash
docker build -t my-python-app .
docker run --rm my-python-app ls /app
```

`notes-for-app.txt` should appear (`COPY . .`). `junk.log` should not.

Remove the dummy files from the host when you are done experimenting. You do not need to `docker rmi` unless you want to.

**PowerShell:**

```powershell
Set-Content -Path junk.log -Value ignored
Set-Content -Path notes-for-app.txt -Value keep
docker build -t my-python-app .
docker run --rm my-python-app ls /app
```

---

## Advanced Example

`.dockerignore` does not affect **bind mounts**. Mounts happen at `docker run`, after the image exists. Ignoring `.venv` at build time does not prevent `-v "$PWD":/app` from exposing `.venv` at runtime if it exists on the host.

That is why Jupyter and edit-loop mounts (Lessons 9, 14, 15) still need a clean project folder: what you mount is what the container sees.

Negation patterns (gitignore-style) exist:

```text
*
!requirements.txt
!main.py
!Dockerfile
```

That "ignore everything except" style is easy to get wrong. Prefer an explicit ignore list for this course.

---

## Practical Example

Minimum Python `.dockerignore` worth copying to new homework:

```text
.git
.gitignore
__pycache__
*.pyc
*.pyo
.venv
venv
.env
.DS_Store
Thumbs.db
.ipynb_checkpoints
```

Put it next to the Dockerfile **before** the first build if the repo already has a `.venv` or data dumps.

---

## Common Mistakes

1. **Ignoring `requirements.txt`.** Build copies nothing; pip fails.
2. **Assuming `.gitignore` applies to Docker.** It does not, unless you duplicate the entries.
3. **Copying `.env` into the image** then pushing to Hub. Ignore secrets.
4. **Huge `node_modules` or `data` folders** left unignored. Builds crawl.
5. **Confusing dockerignore with volumes.** Different lifetime, different mechanism.
6. **Windows: file named `.dockerignore.txt`.** Turn on file extensions.

---

## Best Practices

- Add `.dockerignore` when you add the Dockerfile.
- Ignore VCS metadata, venvs, caches, OS junk, and secrets.
- Keep source and `requirements.txt` visible to `COPY`.
- Review `ls` inside a throwaway `docker run` after the first build.
- Do not store credentials in the project tree if you can avoid it.

---

## Exercises

1. **Read.** List every pattern in `examples/python-docker-project/.dockerignore` and why it is there.
2. **Inspect image.** `docker run --rm my-python-app ls -la /app`. Note what is present.
3. **Secret drill.** Explain in three sentences what happens if `.env` is copied into an image layer.
4. **Dummy log.** Add `junk.log`, ignore `*.log`, rebuild, confirm it is absent in `/app`.
5. **Contrast.** Does `.dockerignore` stop a bind mount of `$PWD` from seeing `junk.log` at runtime? Answer before testing, then test with Lesson 14 if you want.

---

## Quick Review

- Context is the directory sent to the daemon; `.dockerignore` filters it.
- Ignore git, venvs, bytecode, secrets, OS junk.
- Do not ignore the source you `COPY`.
- Bind mounts are a run-time concern, not solved by dockerignore.

---

## Summary

`.dockerignore` keeps builds small and images free of venvs and secrets. Combined with a sensible Dockerfile, you now produce a clean Python image. Next you will persist **data and notebooks** with bind mounts and named volumes, so work is not trapped in a disposable container.

---

[← Previous Lesson](12-python-dependencies.md)
[Course Home](../README.md)
[Next Lesson →](14-volumes-and-bind-mounts.md)
