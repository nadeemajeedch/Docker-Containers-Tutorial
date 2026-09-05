# Python Docker project

Sample app for Part 2 of the Docker and Containers Tutorial.

It runs a small NumPy / Pandas / scikit-learn demo inside an image built from this folder.

## Files

- `Dockerfile` — image recipe
- `requirements.txt` — pip dependencies
- `.dockerignore` — files excluded from the build context
- `main.py` — application entrypoint

Lessons: [10](../../lessons/10-dockerfile.md), [11](../../lessons/11-building-python-images.md), [12](../../lessons/12-python-dependencies.md), [13](../../lessons/13-dockerignore.md)

## Build and run

From this directory:

**Linux / macOS:**

```bash
docker build -t my-python-app .
docker run --rm my-python-app
```

**Windows PowerShell:**

```powershell
docker build -t my-python-app .
docker run --rm my-python-app
```

Expected output includes NumPy and Pandas versions, a small table, and a predicted exam score.

## Rebuild after edits

Change `main.py` or `requirements.txt`, then build again:

```bash
docker build -t my-python-app .
docker run --rm my-python-app
```

Docker reuses unchanged layers. Editing `requirements.txt` invalidates the `pip install` layer and everything after it.

## Run a one-off command in the image

```bash
docker run --rm my-python-app python --version
```

The image `CMD` is replaced by `python --version` for that run.
