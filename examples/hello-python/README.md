# hello-python

Minimal script for [Lesson 9](../../lessons/09-running-python-with-docker.md) and [Lesson 14](../../lessons/14-volumes-and-bind-mounts.md).

**Linux / macOS:**

```bash
docker run --rm -v "$PWD":/app -w /app python:3.12 python hello.py
```

**Windows PowerShell:**

```powershell
docker run --rm -v "${PWD}:/app" -w /app python:3.12 python hello.py
```

There is no Dockerfile here on purpose. The official `python:3.12` image runs the host file through a bind mount.
