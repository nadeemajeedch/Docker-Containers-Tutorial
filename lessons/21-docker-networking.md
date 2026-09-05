# Lesson 21: Docker Networking

Containers have their own network namespaces. This lesson covers bridge networks, published ports, Compose DNS, and the rule that saves hours of debugging: **`localhost` inside a container is not `localhost` on the host.**

[← Previous Lesson](20-environment-variables.md)
[Course Home](../README.md)
[Next Lesson →](22-docker-for-data-science.md)

---

## Learning Objectives

After this lesson you will be able to:

- Explain bridge networks and published ports (`-p` / Compose `ports`).
- Contrast host `localhost` with container `localhost`.
- Reach one Compose service from another using the **service name**.
- State that Compose provides DNS on the project network.
- Use `examples/networking-demo`.

---

## Prerequisites

- Lessons 7, 18, and 20.
- `python:3.12-slim` available (Compose will pull it).

---

## Concept

### Isolation

Each container has its own network stack: its own interfaces, its own `127.0.0.1`. Two containers on the same **user-defined bridge** (Compose creates one per project) can talk using **container or service names**. They cannot see the host's loopback.

```text
Host
  localhost:8000  ----publish----►  web container :8000
                                      ▲
                                      │  DNS name "web"
                                      │
                                   client container
                                   localhost:8000  is the CLIENT, not web
```

### Bridge

The default Docker network type for Compose projects is a **bridge**. Containers on that bridge get private IPs. You rarely type those IPs. You use names.

### Ports

`-p 8000:8000` maps **host** 8000 to **container** 8000. Your browser uses the host side. Another container should **not** use `localhost:8000` to reach that service; it should use `http://servicename:8000`.

---

## Explanation

### Host vs container

| You are | `localhost` means |
|---------|-------------------|
| Browser / PowerShell / macOS Terminal | Your computer |
| Process inside container A | Container A only |
| Process inside container B | Container B only |

Jupyter published as `-p 8888:8888` is opened as `http://localhost:8888` **on the host**. A second container does not use that URL unless you add extra host networking (out of scope; avoid `network_mode: host` in class).

### Compose DNS

On the default project network, the service key is a hostname. In `examples/networking-demo`, `client` fetches `http://web:8000/index.html`.

### Isolation between projects

Two Compose projects get two networks. Service `web` in project A is not visible to project B unless you attach a shared external network (advanced, Lesson 27).

---

## Commands/Syntax

```bash
cd examples/networking-demo
docker compose up --abort-on-container-exit
docker compose down
```

`--abort-on-container-exit` stops the stack when `client` finishes so the demo does not leave `web` running forever.

Inspect networks (optional):

```bash
docker network ls
docker compose up -d
docker network inspect networking-demo_default
docker compose down
```

The network name includes the project directory. **PowerShell:** same commands.

Publish without Compose (reminder):

```bash
docker run --rm -p 8000:8000 python:3.12-slim python -m http.server 8000
```

That still does not make `localhost:8000` work *inside another container*.

---

## Beginner Example

```bash
cd examples/networking-demo
docker compose up --abort-on-container-exit
```

You should see HTTP `200` and the HTML paragraph. Open `http://localhost:8000` in a **host** browser. Then `docker compose down`.

---

## Intermediate Example

Exec into a running `web` (start with `up -d` first) and see both views:

```bash
docker compose up -d
docker compose exec web python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/index.html'); print('loopback in web: ok')"
docker compose run --rm client
docker compose down
```

Loopback works **inside web** because the server is in that container. `client` must use `http://web:8000`.

---

## Advanced Example

Create a user-defined bridge without Compose:

```bash
docker network create classnet
docker run -d --name web --network classnet python:3.12-slim python -m http.server 8000
docker run --rm --network classnet python:3.12-slim python -c "import urllib.request; print(urllib.request.urlopen('http://web:8000').status)"
docker rm -f web
docker network rm classnet
```

`--name web` becomes the DNS name on `classnet`. This is what Compose does for you.

**Optional / advanced:** `network_mode: host` shares the host stack. It breaks port publish semantics and is not used in this course.

---

## Practical Example

Jupyter + a database later: the notebook would connect to `postgres:5432` (service name), **not** `localhost:5432`. Your GUI client on the host would use `localhost:5432` **if** Compose published `5432:5432`.

Remember both URLs: host tools vs container tools.

---

## Common Mistakes

1. **`localhost` inside container B to reach container A.** Use the service name.
2. **Publishing the wrong side of `-p`.** Left = host, right = container.
3. **Assuming two Compose projects share DNS.** They do not, by default.
4. **Firewall confusion on campus Wi-Fi** vs Docker networks. Docker bridge is local to the engine.
5. **Using the host port number from another container** (`http://web:8000` uses the **container** port).

---

## Best Practices

- Compose service names as hostnames.
- Publish ports only for things humans or host tools must reach.
- Do not publish a database port unless you need a host GUI.
- Document two URLs in READMEs: browser vs container-to-container.

---

## Exercises

1. Run `examples/networking-demo` and copy the client output.
2. With `web` up, open `http://localhost:8000` on the host.
3. Explain in writing why `http://localhost:8000` from `client` would fail.
4. `docker network ls` while the demo is up; find the project network.
5. Draw the diagram in Concept from memory.

---

## Quick Review

- Bridge + DNS names for container-to-container.
- `-p` is for the host.
- `localhost` is per network namespace.
- Compose project network is isolated by default.

---

## Summary

You can publish ports for browsers and use service names between containers. Next: a full data-science folder another student can clone and reproduce with Compose.

---

[← Previous Lesson](20-environment-variables.md)
[Course Home](../README.md)
[Next Lesson →](22-docker-for-data-science.md)
