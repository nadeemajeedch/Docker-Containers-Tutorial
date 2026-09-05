# Cheatsheet: Docker Networking

[Course Home](../README.md) · [Complete cheatsheet](complete-docker-cheatsheet.md)

Lesson: [21](../lessons/21-docker-networking.md)

---

## The rule

**`localhost` inside a container is not `localhost` on the host.**

| Who | How to reach Jupyter on 8888 |
|-----|------------------------------|
| Browser on the host | `http://localhost:8888` if you published `-p 8888:8888` |
| Another Compose service | `http://jupyter:8888` (service name + **container** port) |
| Process inside the Jupyter container | `http://127.0.0.1:8888` |

---

## Ports

```bash
docker run -p 8888:8888 ...
```

```yaml
ports:
  - "8888:8888"
  - "${JUPYTER_PORT:-8888}:8888"
```

Left = host. Right = container.

---

## Compose DNS

On the default project network, the YAML service key is a hostname.

Demo: `examples/networking-demo` — client uses `http://web:8000`.

```bash
cd examples/networking-demo
docker compose up --abort-on-container-exit
docker compose down
```

---

## Inspect

```bash
docker network ls
docker compose up -d
docker network inspect <project>_default
docker compose down
```

Two Compose projects do **not** share DNS unless you add an external network (advanced).
