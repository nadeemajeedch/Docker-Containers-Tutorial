# Lesson 29: Docker and GitHub

Docker does not replace Git. Git stores the recipe; Docker reproduces the environment. This lesson is the workflow from first commit to a classmate's `docker compose up --build`.

[← Previous Lesson](28-image-optimization.md)
[Course Home](../README.md)
[Next Lesson →](30-reproducible-academic-projects.md)

---

## Learning Objectives

After this lesson you will be able to:

- List the files that belong in a GitHub repo for a Dockerized class project.
- Use `.gitignore` vs `.dockerignore` together.
- Follow create → dockerize → test → commit → push → clone → compose.
- Avoid committing `.env` secrets, venvs, and huge binaries.
- Use `examples/github-template` as a starter.

---

## Prerequisites

- A GitHub account (free).
- Git basics (`clone`, `add`, `commit`, `push`).
- Lessons 18 and 20.

---

## Concept

```text
Create project
↓
Dockerize (Dockerfile + compose.yaml + requirements.txt)
↓
Test (compose up / run scripts)
↓
Git commit
↓
Push to GitHub
↓
Another student clones it
↓
Docker Compose reproduces the environment
```

The remote repo should be enough. "Works on my machine" is not a submission.

Template layout (`examples/github-template`):

```text
Dockerfile
compose.yaml
requirements.txt
README.md
.dockerignore
.gitignore
.env.example
notebooks/
data/
src/
tests/
results/
```

---

## Explanation

### What to store on GitHub

| Commit | Do not commit |
|--------|----------------|
| Dockerfile, compose.yaml | `.env` with secrets |
| requirements.txt | `.venv/`, `__pycache__/` |
| .dockerignore, .gitignore | OS junk |
| README with run steps | Huge datasets (document a URL) |
| Small CSV samples | API keys, tokens |
| notebooks (source) | Optional: huge model weights |

### `.gitignore` vs `.dockerignore`

- Git ignore: what is not versioned.
- Docker ignore: what is not sent to `docker build`.

Both should exclude venvs and `.env`. Git **should** track `Dockerfile` and `requirements.txt`; Docker ignore must **not** exclude those.

### README contract

The first commands in README must work after a fresh clone: `docker compose up --build`. Mention host port and any `cp .env.example .env`.

### Branches and MRs

Follow your course's Git workflow. This lesson does not require GitHub Actions. Optional CI that runs `docker compose run` is advanced.

---

## Commands/Syntax

Illustrative Git sequence (run in **your** project folder, not necessarily this course repo):

```bash
git add Dockerfile compose.yaml requirements.txt README.md .dockerignore .gitignore .env.example
git add notebooks data src tests
git status
git commit -m "Add Dockerized Jupyter project"
git push
```

Classmate:

```bash
git clone <url>
cd <project>
cp .env.example .env
docker compose up --build
```

**PowerShell:** `Copy-Item .env.example .env`; Git and Compose commands are the same.

Never `git add .env` if it has secrets. `git status` before every commit.

---

## Beginner Example

Open `examples/github-template` and tick each committed file against the table. Read its README "Reproduce after clone" section.

---

## Intermediate Example

On your GitHub, create a new empty repo (private if the course requires). Copy the template, commit, push, clone into a **second** directory, `docker compose up --build`. If that works, the README is honest.

You do not have to push the whole Docker-Containers-Tutorial course unless you forked it.

---

## Advanced Example

GitHub Actions that builds the image is optional. A minimal workflow would run on a GitHub runner with Docker; many student repos skip CI. If you add CI, still do not put Hub passwords in workflow files; use GitHub Secrets.

---

## Practical Example

Before `git push`:

```text
git status
# .env untracked? good
# .venv untracked? good
# Dockerfile tracked? good
```

If `git status` shows `id_rsa` or `credentials.json`, stop.

---

## Common Mistakes

1. Pushing `.env` "just this once."
2. README that only documents host Anaconda.
3. Dockerignoring `requirements.txt`.
4. Committing `node_modules` or `.venv` because builds felt slow (they get slower for everyone else).
5. LFS missing for a 2 GB CSV.

---

## Best Practices

- Template + README first, then code.
- `git status` as a security tool.
- Small sample data in Git.
- Private repos if the assignment contains unpublished research data.

---

## Exercises

1. List every file in `examples/github-template` and mark commit vs ignore.
2. Write a six-line README "Reproduce" section from memory.
3. Explain `.gitignore` vs `.dockerignore` in four sentences.
4. Run `git status` in this course repo and confirm `.env` files are not staged (there should be none with secrets).
5. Draw the create→clone flowchart.

---

## Quick Review

- Git holds recipes; Docker holds the runtime.
- Commit Docker files and sample data; never secrets or venvs.
- Clone + `compose up --build` is the test of a good repo.

---

## Summary

You can publish a Dockerized project so another student can reproduce it. Next: academic reproducibility patterns for assignments and research labs.

---

[← Previous Lesson](28-image-optimization.md)
[Course Home](../README.md)
[Next Lesson →](30-reproducible-academic-projects.md)
