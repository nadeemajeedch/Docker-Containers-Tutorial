# Final project starter: reproducible data science with Docker

Starter for [Lesson 31](../../lessons/31-final-project.md). Clone-and-run for another student:

```bash
cd examples/final-project
cp .env.example .env
docker compose up --build
```

Open `http://localhost:8888`, run `notebooks/01-analysis.ipynb`.

Headless analysis:

```bash
docker compose --profile script run --rm analyze
```

Tiny test:

```bash
docker compose run --rm jupyter python tests/test_analyze.py
```

Do not commit secrets. `.env` is gitignored; `.env.example` is not.
