# Data science Docker environment

JupyterLab plus a small pandas/sklearn workflow. Another student can clone this folder (or the whole course repo), run Compose, and get the same stack.

Lessons: [22](../../lessons/22-docker-for-data-science.md), [30](../../lessons/30-reproducible-academic-projects.md)

## Reproduce

```bash
cd examples/data-science-docker
cp .env.example .env
docker compose up --build
```

Open `http://localhost:8888`. Run `notebooks/01-explore.ipynb`.

Headless script (no browser):

```bash
docker compose run --rm jupyter python src/analyze.py
```

Plots land in `results/` on the host because that directory is bind-mounted.

## Layout

```text
Dockerfile
compose.yaml
requirements.txt
.env.example
notebooks/
data/
src/
results/
```

Copy `.env.example` to `.env` for local settings. Do not commit `.env` if it ever contains secrets. This example only has a display name and a port.

## Windows PowerShell

`docker compose` commands are the same. Copy the env file with:

```powershell
Copy-Item .env.example .env
docker compose up --build
```
