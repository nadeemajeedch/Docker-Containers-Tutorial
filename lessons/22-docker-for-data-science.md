# Lesson 22: Docker for Data Science

A data-science environment is an image plus bind-mounted notebooks, data, source, and results. This lesson uses `examples/data-science-docker` so a classmate can clone and reproduce the stack without installing Anaconda.

[← Previous Lesson](21-docker-networking.md)
[Course Home](../README.md)
[Next Lesson →](23-docker-for-machine-learning.md)

---

## Learning Objectives

After this lesson you will be able to:

- Describe a reproducible DS layout: `Dockerfile`, `compose.yaml`, `requirements.txt`, `notebooks/`, `data/`, `src/`, `results/`.
- Start JupyterLab with data and results mounted.
- Run a headless analysis script in the same image.
- Explain how another student reproduces the environment.
- Keep datasets on mounts, libraries in the image.

---

## Prerequisites

- Lessons 16–20.
- Comfort with pandas at a "read a CSV" level (the analysis is tiny).

---

## Concept

Install-on-each-laptop fails for class: different pandas, missing BLAS, broken PATH. Docker pins Python and pip packages. Git holds notebooks and small CSVs. Compose wires mounts.

```text
Image          JupyterLab + numpy + pandas + matplotlib + scikit-learn
notebooks/     bind mount — what you submit as thinking
data/          bind mount — inputs (tiny CSV here)
src/           bind mount — .py you can also run headless
results/       bind mount — figures and outputs
```

Libraries stay in the **image**. Data and notebooks stay on the **host**.

---

## Explanation

`examples/data-science-docker/compose.yaml` mounts four directories and sets `STUDENT_NAME` from `.env`. Jupyter listens on 8888; host port is `${JUPYTER_PORT:-8888}`.

`src/analyze.py` reads `/workspace/data/study_hours.csv` and writes `/workspace/results/study-hours.png`. Those paths are **container** paths. Because of mounts, the PNG appears in `results/` on the host.

Reproduction for a classmate:

```text
git clone ...
cd examples/data-science-docker
cp .env.example .env
docker compose up --build
```

They do not install Python. They need Docker and the repo.

---

## Commands/Syntax

```bash
cd examples/data-science-docker
cp .env.example .env
docker compose up --build
```

**PowerShell:** `Copy-Item .env.example .env` then the same `docker compose` line.

Headless:

```bash
docker compose run --rm jupyter python src/analyze.py
```

Then `ls results` (PowerShell: `Get-ChildItem results`).

Stop Jupyter: Ctrl+C or `docker compose down`.

---

## Beginner Example

Start Compose, open `http://localhost:8888`, run `notebooks/01-explore.ipynb`. Confirm `STUDENT_NAME` and the scatter plot.

---

## Intermediate Example

Without the browser:

```bash
docker compose run --rm jupyter python src/analyze.py
```

Expected: a table, a predicted score after 5 hours, `wrote /workspace/results/study-hours.png`. Open that PNG on the host.

---

## Advanced Example

Give a classmate **only** this folder (zip or a small Git repo). Their first run is `docker compose up --build`. If they already have `python:3.12-slim` cached, the slow step is pip. That is expected once per machine.

If the CSV were huge, you would **not** commit it; you would document a download URL and a script. This course CSV is tiny and is committed on purpose.

---

## Practical Example

When an assignment says "use pandas 2.x and sklearn 1.5+":

1. Pin ranges in `requirements.txt` (already done).
2. Put the grader's expected paths in the README (`/workspace/data/...`).
3. Mount `results/` so figures survive `down`.

---

## Common Mistakes

1. **Writing plots only to `/tmp`.** Not mounted; gone after `--rm`.
2. **`pip install` in a notebook as the only dependency record.** Put packages in `requirements.txt` and rebuild.
3. **Committing `.env` with secrets.** This example has none; keep it that way.
4. **Host Python vs container Python** when debugging imports.

---

## Best Practices

- Same image for notebooks and scripts.
- Small sample data in Git; large data documented.
- `results/` gitignored except `.gitkeep` if outputs are generated (this example keeps `.gitkeep`).
- README with the exact `compose up` line.

---

## Exercises

1. `cp .env.example .env` and `docker compose up --build`.
2. Run the explore notebook.
3. Run `src/analyze.py` via `compose run` and open the PNG.
4. Change your name in `.env`, recreate the container, confirm the notebook print.
5. Write the clone-and-run steps for a classmate in five lines.

---

## Quick Review

- Image = libraries. Mounts = notebooks, data, results.
- Compose is how others reproduce.
- Headless `compose run` uses the same image as Jupyter.

---

## Summary

You have a cloneable DS environment. Next: a small ML train/predict workflow, still CPU-only.

---

[← Previous Lesson](21-docker-networking.md)
[Course Home](../README.md)
[Next Lesson →](23-docker-for-machine-learning.md)
