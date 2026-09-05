# Lesson 26: Security

Docker isolation is not a force field. This lesson introduces **least privilege**, secrets, image trust, scanning, exposed ports, and why `--privileged` is not a class default.

[← Previous Lesson](25-best-practices.md)
[Course Home](../README.md)
[Next Lesson →](27-advanced-docker.md)

---

## Learning Objectives

After this lesson you will be able to:

- Run long-lived processes as a non-root user.
- Keep secrets out of images and Git.
- Prefer official/pinned images and explain image trust.
- Describe what vulnerability scanning is for (without treating a scanner as a homework requirement).
- Publish only the ports you need.
- Avoid `--privileged` and host network mode in this course.

---

## Prerequisites

- Lessons 13, 20, 21, and 25.
- This is an **introduction**, not a pentest course.

---

## Concept

A container shares the host kernel (Lesson 2). If malware runs as **root** in a container with extra capabilities, the blast radius is larger. Class policy:

- Do not run untrusted images.
- Do not pass `--privileged`.
- Do not expose Jupyter on a public IP with an empty token.
- Do not bake API keys into layers.

Least privilege: the process gets only the files, ports, and user it needs.

---

## Explanation

### Non-root

Part 3 Jupyter Dockerfiles create `jovyan` and `USER jovyan`. The server cannot write arbitrary host paths except where you bind-mounted (and the mount's permissions allow).

### Secrets

If a key is in a Dockerfile `ENV` or a `COPY`d `.env`, it lives in the image history. `docker history` and Hub copies will show or include it.

Pass configuration at **run** time. For class, prefer no real cloud keys at all.

### Image trust

Pull official tags you chose (`python:3.12-slim`). Do not run `docker run coolhacker/python-fast` from a forum. Content trust (`DOCKER_CONTENT_TRUST`) exists; optional, advanced. Pinning a digest is stronger than a moving tag; optional for this course.

### Vulnerability scanning

Tools such as Docker Scout (where available) or other scanners report known CVEs in packages. **Optional / advanced.** For class: keep base images reasonably current, pin dependencies, do not ignore pip audit warnings if your instructor asks you to run them.

This course does not require you to install a scanner.

### Exposed ports

Every `-p` is a door on the host. Publish Jupyter only on localhost-style lab machines. Do not port-forward 8888 through a campus firewall to the world with `--ServerApp.token=`.

`EXPOSE` does not open the host. `-p` and Compose `ports` do.

### Privileged containers

`--privileged` turns off most isolation. Never use it to "fix" a mount. Fix the mount.

---

## Commands/Syntax

See the user inside a running service:

```bash
docker compose exec jupyter whoami
docker compose exec jupyter id
```

Inspect published ports:

```bash
docker ps
```

Do **not** run:

```bash
docker run --privileged ...
```

in this course.

**PowerShell:** same `docker` / `compose` commands.

---

## Beginner Example

```bash
cd examples/compose-jupyter
docker compose up -d --build
docker compose exec jupyter whoami
docker compose down
```

Expect `jovyan`, not `root`.

---

## Intermediate Example

Imagine you accidentally committed a Hub password. Treat it as leaked: change the password on Hub, `git` history rewrite is hard on shared remotes — rotation matters more than clever git tricks for a class key. Add `.env` to `.gitignore`.

---

## Advanced Example

Optional: after building, some Desktop versions offer Scout quick views. If the UI is absent, skip. Do not install random third-party scanners in the Agent/platform environment; on your laptop, follow your instructor.

Pin by digest (advanced):

```dockerfile
FROM python:3.12-slim@sha256:...
```

You look up the digest on Hub. Optional; tags are enough for Part 3 assignments unless specified.

---

## Practical Example

Jupyter security for this course:

| Setting | Class laptop | Shared server |
|---------|--------------|---------------|
| Empty token | Acceptable on localhost only | No |
| `-p 8888:8888` | Yes | Bind to localhost or use a reverse proxy + token |
| `USER jovyan` | Yes | Yes |
| `--privileged` | No | No |

---

## Common Mistakes

1. Empty token + public cloud VM + open 8888.
2. `COPY .env` .
3. Running as root because pip was root at **build** time (build vs runtime users differ).
4. `--privileged` to fix permissions.
5. Pulling unverified images for "speed."

---

## Best Practices

- Non-root `USER` for servers.
- Secrets never in Git or image layers.
- Official pinned bases.
- Minimal published ports.
- No privileged mode.
- Tokens on any machine that is not a single-user localhost.

---

## Exercises

1. `whoami` in compose-jupyter.
2. List three secrets that must not appear in `git log -p`.
3. Explain `EXPOSE` vs `ports:` in four sentences.
4. Why is `--privileged` the wrong fix for "permission denied on the bind mount"?
5. Write a two-line warning you would put in a README about Jupyter tokens.

---

## Quick Review

- Least privilege: user, ports, capabilities.
- Secrets at run time, not in layers.
- Official images; optional scanning.
- Empty token is localhost-only.

---

## Summary

Security here is boring on purpose: non-root, no secrets in Git, no open Jupyter, no privileged. Next: advanced Engine features, clearly labeled optional.

---

[← Previous Lesson](25-best-practices.md)
[Course Home](../README.md)
[Next Lesson →](27-advanced-docker.md)
