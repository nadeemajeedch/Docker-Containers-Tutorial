# Lesson 31: Final Project

**Reproducible Data Science Environment with Docker + JupyterLab**

This is the course capstone. Use `examples/final-project` as a starter, then make it yours. Another student must clone your GitHub repo and reproduce the environment with Compose.

[← Previous Lesson](30-reproducible-academic-projects.md)
[Course Home](../README.md)
[Next Lesson →](../cheatsheet/complete-docker-cheatsheet.md)

---

## Learning Objectives

After this lesson you will be able to:

- Deliver a GitHub repo that builds an image, runs JupyterLab, persists notebooks, mounts data, and documents a DS workflow.
- Meet the numbered requirements below.
- Self-score against the rubric before you submit.

---

## Prerequisites

- Parts 1–3 through Lesson 30.
- GitHub account.
- Docker working (`docker compose version`).

---

## Concept

You ship an **environment** (Dockerfile + requirements + Compose) and **work** (notebooks, src, data, results). The grader is a classmate with Docker, not a clone of your laptop.

Starter: `examples/final-project`

---

## Explanation

### Requirements

You must:

1. **Build a Docker image** from a Dockerfile (`python:3.12-slim` or equivalent official pin).
2. **Install dependencies** with `requirements.txt` (include JupyterLab, NumPy, Pandas, Matplotlib, scikit-learn).
3. **Launch JupyterLab** via Docker Compose on a published port (default 8888).
4. **Persist notebooks** with a bind mount (`./notebooks:/workspace/notebooks`).
5. **Mount data** (`./data` → `/workspace/data`).
6. **Use Docker Compose** (`compose.yaml`) as the primary start method.
7. **Perform a Data Science workflow**: load a table, summarize or model, produce at least one figure saved under `results/`.
8. **Document** the project in `README.md` (reproduce steps, ports, layout).
9. **Push to GitHub** (public or private per instructor).
10. **Enable another student to reproduce** with clone + `docker compose up --build` (and `cp .env.example .env` if needed).

### Project structure

```text
your-final/
├── README.md
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .dockerignore
├── .gitignore
├── .env.example
├── notebooks/
├── data/
├── src/
├── tests/
└── results/
```

You may start by copying `examples/final-project`. Replace the study-hours CSV with your own small dataset if the instructor allows, or keep it and extend the analysis.

### Step-by-step instructions

1. Copy the starter (or the github-template) into your own folder/repo.
2. Pin packages in `requirements.txt`.
3. Confirm Dockerfile: non-root user, `CMD` Jupyter with `--ip=0.0.0.0`.
4. Confirm `compose.yaml` mounts notebooks, data, src, tests, results.
5. `docker compose up --build` and open the host port.
6. Complete `notebooks/01-analysis.ipynb` (or your own notebook): load CSV, fit or describe, save a PNG to `/workspace/results`.
7. Run the script path: `docker compose --profile script run --rm analyze` (starter) or equivalent.
8. Run tests if present: `docker compose run --rm jupyter python tests/test_analyze.py`.
9. Fill README and `SUBMISSION.md`.
10. `git status` — no `.env` secrets, no venv. Commit, push.
11. Clone into a **new** directory (or ask a classmate) and reproduce.

### Expected results

- Jupyter opens on `http://localhost:8888` (or your documented port).
- Notebook runs without `ModuleNotFoundError`.
- A figure exists in `results/` on the **host** after the workflow.
- Script path prints a numeric result (starter: predicted score after 5 hours).
- Fresh clone does not require Anaconda.

### Submission checklist

```text
[ ] Dockerfile builds
[ ] requirements.txt includes the scientific stack + JupyterLab
[ ] docker compose up --build starts Jupyter
[ ] notebooks persist on the host
[ ] data is mounted and used
[ ] results figure on the host
[ ] README reproduce section works on a clean clone
[ ] .env.example present; .env not committed
[ ] .dockerignore and .gitignore present
[ ] GitHub URL submitted per instructor
[ ] No secrets in the repo
[ ] Token warning if Jupyter has empty token (localhost only)
```

### Evaluation rubric

| Criterion | Weight | Excellent | Adequate | Missing |
|-----------|--------|-----------|----------|---------|
| Image builds from pinned official base | 10% | Slim/pin documented | Builds | Fails |
| Dependencies in requirements.txt | 10% | Pinned/ranged, complete | Present | pip in notebook only |
| Compose + Jupyter port | 15% | compose.yaml, documented port | Works locally | docker run only |
| Persistence (notebooks, data, results) | 15% | All three mounted | Notebooks only | Lost on down |
| DS workflow | 20% | Clear notebook + figure + src | Notebook only | No analysis |
| Documentation | 15% | Clone-and-run README | Partial | None |
| GitHub hygiene | 10% | No secrets, gitignore | Minor junk | Secrets or venv |
| Reproducibility test | 5% | Second-directory clone works | Author machine only | Cannot clone |

Instructors may rescale. Use this as a self-check.

### Extension challenges (optional)

- Add a Compose **profile** for a headless train/analyze service.
- Pin exact versions with a freeze file.
- Add a second container (Lesson 21) that only fetches data.
- Multi-stage CLI image for `src/analyze.py` (Lesson 28).
- Healthcheck (Lesson 27).
- Replace empty Jupyter token with a token from logs (safer).
- GPU-enabled extra service — **only** if hardware and instructor allow; not required.

---

## Commands/Syntax

Starter:

```bash
cd examples/final-project
cp .env.example .env
docker compose up --build
```

**PowerShell:** `Copy-Item .env.example .env`

Headless:

```bash
docker compose --profile script run --rm analyze
docker compose run --rm jupyter python tests/test_analyze.py
```

---

## Beginner Example

Run the starter unchanged. Confirm Jupyter, notebook, `results/notebook-plot.png` after you save from the notebook, and script output.

---

## Intermediate Example

Change the CSV (add a row), rerun analyze, confirm the prediction moves. Commit the data change. Rebuild is **not** required for CSV edits (mount). Rebuild **is** required if you add `seaborn` to requirements.

---

## Advanced Example

Publish a private GitHub repo, add a classmate as collaborator, have them clone and `compose up` without you narrating. Fix README holes they hit. That is the real exam.

---

## Practical Example

Your submission is the **repo URL** plus a short note (port, any extra step). Screenshots without a working Compose file do not satisfy requirement 10.

---

## Common Mistakes

1. Only `docker run` documented, no Compose.
2. Notebooks not mounted.
3. Figure written to a non-mounted path.
4. Secrets in GitHub.
5. README assumes `C:\Users\YourName\...` paths.
6. Empty token on a cloud VM.

---

## Best Practices

- Starter first, then customize.
- Clone test before the deadline.
- Rubric as a checklist, not afterthought.
- Keep the DS story small and correct rather than a huge model that does not run.

---

## Exercises

The project **is** the exercise. Minimum:

1. Starter runs.
2. README filled.
3. GitHub pushed.
4. Clone test.
5. Checklist ticked.
6. Rubric self-score written in `SUBMISSION.md`.

---

## Quick Review

- Ten numbered requirements.
- Starter in `examples/final-project`.
- Success = classmate compose-up.
- Extensions are optional.

---

## Summary

The course ends when someone else can reproduce your DS environment from GitHub. You now have beginner fundamentals, Python/Jupyter images, Compose, networking, DS/ML examples, debugging, security, and a final project pattern.

[Part 1 CLI cheatsheet](../cheatsheet.md) · [Complete cheatsheet](../cheatsheet/complete-docker-cheatsheet.md)

---

[← Previous Lesson](30-reproducible-academic-projects.md)
[Course Home](../README.md)
[Next Lesson →](../cheatsheet/complete-docker-cheatsheet.md)
