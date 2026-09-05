# Cheatsheet: Troubleshooting

[Course Home](../README.md) · Lesson: [24](../lessons/24-debugging.md)

Walk this order before changing a Dockerfile:

```text
docker --help
docker version          # need Server section
docker ps / docker compose ps
docker logs / docker compose logs
docker inspect / docker compose config
```

---

## Problem → first check

| Problem | First check | Typical fix |
|---------|-------------|-------------|
| `docker: command not found` | New terminal; Desktop installed | Lesson 4 |
| Cannot connect to daemon | Desktop whale / `docker version` Server | Start Desktop; wait |
| Permission denied (Linux socket) | `id` / docker group | Log out after adding group |
| Port already allocated | `docker ps` | `compose down` or `JUPYTER_PORT=8889` |
| Container Exited | `docker logs` | Read traceback; missing `-it`; bad CMD |
| `COPY failed` | Current directory | `cd` to Dockerfile context |
| `ModuleNotFoundError` | `requirements.txt`; image rebuilt? | `compose up --build` |
| Empty bind mount | Path order; quotes; `$PWD` | Host left, container right, `/` in container |
| Windows volume spec | Backslash in container path | `/workspace/notebooks` |
| Jupyter login | `compose logs` for `token=` | Use **host** port in the URL |
| `localhost` fails from another container | Lesson 21 | Use **service name** |
| `docker-compose: not found` | Hyphen vs space | `docker compose version` |
| Compose: no config file | Wrong directory | `cd` to `compose.yaml` |
| Profile service missing | `profiles:` in YAML | `--profile notebook` |

---

## PowerShell vs bash

- Continuation: PowerShell `` ` ``, bash `\`
- Bind mount: `"${PWD}:/app"` vs `"$PWD":/app`
- Copy env: `Copy-Item .env.example .env` vs `cp .env.example .env`

---

## Compose debug

```bash
docker compose config
docker compose ps
docker compose logs -f
```
