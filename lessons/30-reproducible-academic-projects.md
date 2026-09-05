# Lesson 30: Reproducible Academic Projects

Docker is a tool for **assignments, labs, and research** that must run the same way next semester. This lesson maps course work onto a folder layout and a README contract.

[← Previous Lesson](29-docker-and-github.md)
[Course Home](../README.md)
[Next Lesson →](31-final-project.md)

---

## Learning Objectives

After this lesson you will be able to:

- Choose a project skeleton for programming, DS, ML, or Jupyter labs.
- Explain what "reproducible" means for a grader vs a paper.
- Keep `notebooks/`, `data/`, `src/`, `tests/`, and `results/` distinct.
- Write a README a classmate can follow without you in the room.
- Point to `examples/data-science-docker`, `ml-docker`, and `github-template`.

---

## Prerequisites

- Lessons 22, 23, and 29.

---

## Concept

Recommended skeleton:

```text
student-project/
├── README.md
├── Dockerfile
├── compose.yaml
├── requirements.txt
├── .dockerignore
├── notebooks/
├── data/
├── src/
├── tests/
└── results/
```

| Folder | Role |
|--------|------|
| `notebooks/` | Exploration, figures for humans |
| `data/` | Inputs (cite the source in README) |
| `src/` | Importable / scriptable code |
| `tests/` | Small checks the grader can run |
| `results/` | Generated outputs; often gitignored except `.gitkeep` |

Programming assignments might skip `notebooks/`. DS/ML labs usually keep all five.

---

## Explanation

### What graders need

1. How to start (`docker compose up --build`)
2. Which notebook or script is the "answer"
3. Python/package versions (from `requirements.txt` + base tag)
4. Where outputs appear (`results/`)

### What papers need (stricter)

Pin more tightly (`==` versions or a lock file), record the image tag or digest, and freeze random seeds (the ML example uses `random_state=42`). Data provenance belongs in README.

### Jupyter labs

Students edit notebooks on a mount. The image is the lab PC. Instructors rebuild the image when the stack changes, not when a student edits a cell.

### Research

Do not put human-subject data in a public GitHub repo. Use a private repo or data-use agreements. Docker still helps by freezing the **code environment** even if data stays offline.

---

## Commands/Syntax

Headless grader-friendly:

```bash
docker compose run --rm jupyter python src/analyze.py
docker compose run --rm jupyter python tests/test_analyze.py
```

Interactive:

```bash
docker compose up --build
```

Same on PowerShell.

---

## Beginner Example

Compare `examples/github-template` (empty folders) with `examples/data-science-docker` (filled CSV + notebook). The skeleton is the same. Filling the folders is the assignment.

---

## Intermediate Example

Write a README section:

```text
## Reproduce
1. Install Docker (see course Lesson 4)
2. cp .env.example .env
3. docker compose up --build
4. Open http://localhost:8888
5. Run notebooks/01-explore.ipynb
```

If any step needs a secret, stop and use `.env.example` instead of pasting the secret.

---

## Advanced Example

For a paper, add a `VERSIONS.md` with `docker compose run --rm jupyter pip freeze` captured on the day you submit. Optional. Ranges in `requirements.txt` are enough for most courses.

---

## Practical Example

| Work type | Start from |
|-----------|------------|
| Programming homework | `python-docker-project` + tests |
| DS lab | `data-science-docker` |
| ML mini-project | `ml-docker` |
| New GitHub repo | `github-template` |
| Course final | `final-project` + Lesson 31 |

---

## Common Mistakes

1. Notebooks that only work with files on `C:\Users\You\Downloads`.
2. No `src/` — logic trapped in an unsaved notebook.
3. Results committed as 50 MB PNGs every commit (gitignore `results/*`).
4. README that assumes the grader has your conda env name.

---

## Best Practices

- Stable container paths (`/workspace/data`).
- Seeds for stochastic methods.
- Cite data.
- Tests even if they are one assertion.
- Private GitHub when data cannot be public.

---

## Exercises

1. Draw the skeleton from memory.
2. Map each folder in `examples/final-project` to the table.
3. Write a grader-oriented Reproduce section for that example.
4. List three differences between a lab and a paper in pinning strictness.
5. Decide whether your next assignment's data can be public.

---

## Quick Review

- Same skeleton for DS/ML/academic GitHub.
- Image = env; mounts = work; README = contract.
- Graders run Compose; they do not install Anaconda.

---

## Summary

You have a layout and a social contract for reproducible coursework. Lesson 31 is the assessed capstone: a full DS environment another student can clone.

---

[← Previous Lesson](29-docker-and-github.md)
[Course Home](../README.md)
[Next Lesson →](31-final-project.md)
