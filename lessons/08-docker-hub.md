# Lesson 8: Docker Hub

Docker Hub is the default public registry. This lesson teaches you to find images, read tags, pull official images, and understand the difference between Hub in the browser and the local cache on your disk.

[← Previous Lesson](07-docker-containers.md)
[Course Home](../README.md)
[Next Lesson →](09-running-python-with-docker.md)

---

## Learning Objectives

After this lesson you will be able to:

- Explain what a registry is and why Docker Hub is the default.
- Search for images and identify **Docker Official Images**.
- Read a Hub page: tags, architectures, short description, pull command.
- Pull by tag (`python:3.12`) and explain `latest`.
- Log in (optional) and know why anonymous pulls may be rate-limited.
- Avoid untrusted images for classwork.

---

## Prerequisites

- Lessons 1–7.
- Working `docker pull` and `docker run`.
- A web browser for Hub pages.
- Optional: a free account at [https://hub.docker.com](https://hub.docker.com).

---

## Concept

### Registries

A **registry** is a server that stores image repositories and serves layers when you pull. Docker Engine speaks the registry API.

**Docker Hub** (`docker.io`) is the default. Other registries exist (GitHub Container Registry, Amazon ECR, Google Artifact Registry, a self-hosted registry). This lesson focuses on Hub because `docker pull python:3.12` goes there unless you specify another host.

```text
docker pull python:3.12
        │
        ▼
https://registry-1.docker.io  (Docker Hub)
        │
        ▼
local image cache
```

A **repository** on Hub is a named collection of tags (`python` with tags `3.12`, `3.12-slim`, `latest`, ...).

### Official images vs everything else

Hub contains:

| Kind | Example | Trust model |
|------|---------|-------------|
| **Docker Official Image** | `python`, `nginx`, `hello-world` | Curated, documented, often multi-arch |
| Verified / publisher images | Vendor-published products | Publisher identity verified by Docker; still read the docs |
| Community images | `someuser/random` | Variable quality; anyone with an account can push |

For Part 1 and Part 2, prefer **Official Images**: `python`, `hello-world`, `nginx` if you experiment with web servers.

Official images appear in the CLI as short names: `python:3.12`, not `library/python:3.12` (both work).

### Tags on Hub

Open the Tags tab on a Hub repo. You will see many tags. For Python:

- `latest` — currently a specific major Python; **it moves**
- `3.12` — latest 3.12.x patch the maintainers published
- `3.12.8` — a patch version (numbers change over time)
- `3.12-slim`, `3.12-alpine` — smaller variants
- `3.12-bookworm` — tied to a Debian release name

Pull what your syllabus states. This course uses `python:3.12`.

### Multi-arch manifests

One tag can point to a **manifest list**: amd64, arm64, and others. Docker Desktop on Apple Silicon pulls the arm64 variant automatically. You usually do not add `--platform` in Part 1.

If you force the wrong platform, you may see emulation (slow) or exec format errors.

### Search

```bash
docker search python
```

Prints Hub search results in the terminal (`NAME`, `DESCRIPTION`, `STARS`, `OFFICIAL`). The browser is better for reading docs. The CLI is useful on servers without a GUI.

Stars are popularity, not a security audit.

### Login

```bash
docker login
```

Enter Hub username and password (or a personal access token if Hub requires it). Login is stored as credentials for the daemon/CLI. You do **not** need to login to pull public official images, but **anonymous pull rate limits** exist. If pulls fail with `toomanyrequests` or 429, wait or log in.

```bash
docker logout
```

Never paste passwords into screenshots or homework submissions.

---

## Why It Matters

Every `docker run` that is not already cached is a Hub (or other registry) operation. Choosing `python:3.12` instead of a random community image is a safety and reproducibility decision. Reading tags prevents "it worked in September" surprises when `latest` moves.

You will not **push** images in Part 1. Consumption — search, evaluate, pull — is the skill.

---

## Commands/Syntax

```bash
docker search python
docker pull python:3.12
docker pull hello-world
docker images
docker run --rm python:3.12 python --version
docker login
docker logout
```

| Command | Purpose |
|---------|---------|
| `docker search <term>` | Search Hub from the CLI |
| `docker pull <name>:<tag>` | Download image layers |
| `docker images` | Confirm the image is local |
| `docker login` | Authenticate to Hub (optional for public pulls) |
| `docker logout` | Remove stored Hub credentials |

Pull from an explicit Hub reference:

```bash
docker pull docker.io/library/python:3.12
```

Equivalent to `docker pull python:3.12`.

Search only official images (if your Docker version supports the filter):

```bash
docker search python --filter is-official=true
```

If the filter is rejected, use unfiltered `docker search` and look at the `OFFICIAL` column.

**PowerShell:** same commands. `docker login` is interactive; the prompt for username/password works in PowerShell. Prefer an access token over a password if Hub's account security settings require it.

---

## Beginner Example

In a browser, open:

`https://hub.docker.com/_/python`

Note:

- The official badge
- The suggested pull command
- The Tags tab

Then:

```bash
docker pull python:3.12
docker images python
docker run --rm python:3.12 python --version
```

Compare the version printed with the tag you pulled. It should be 3.12.x, not 3.11.

Repeat for Hello World:

`https://hub.docker.com/_/hello-world`

```bash
docker pull hello-world
docker run --rm hello-world
```

---

## Intermediate Example

CLI search:

```bash
docker search python
```

Identify the line where `NAME` is `python` and `OFFICIAL` is `[OK]`.

Pull two tags and list:

```bash
docker pull python:3.12
docker pull hello-world:latest
docker images
```

Interpret REPOSITORY + TAG as the Hub coordinates you used.

Remove only what you do not need:

```bash
docker rmi hello-world
```

Keep `python:3.12` if you still use it for practice.

---

## Advanced Example

### Rate limits

Anonymous users share a public IP (a university NAT may look like one user). Many students pulling at once can trigger Hub rate limits. Symptoms: pull fails with a too-many-requests message.

Mitigations:

1. Log in with a free Hub account: `docker login`.
2. Pull once, then work from the cache (`docker images` should already list the image).
3. Avoid deleting and re-pulling the same official image all afternoon.

### Content trust (awareness)

Docker Content Trust (`DOCKER_CONTENT_TRUST=1`) verifies signed official images. It is off by default. You do not need to enable it for Part 1. Know that official images are signed in Docker's publishing process; community images may not be.

### Not every Dockerfile on the internet is Hub

People post Dockerfiles on GitHub. Those are **build recipes**, not registry images. `docker pull` does not build a Dockerfile. Building is a later skill. If a README says "pull `myuser/myapp:1.0`," that image must exist on a registry. If it only has a Dockerfile, you cannot pull it until someone builds and pushes it (or you build it yourself later).

### Alternative registries (recognize the hostname)

```text
docker pull ghcr.io/owner/name:tag
docker pull public.ecr.aws/example/name:tag
```

The first hostname is the registry. No hostname means Hub. Do not pull from random registries for this course.

---

## Practical Example

Evaluate-then-pull checklist for any new image:

1. Browser: is it an Official Image?
2. Read the short description. Does it match your need (Python interpreter vs a random app)?
3. Tags: pick `3.12` or whatever the syllabus says, not an undated `latest` if you can avoid it.
4. Architectures: amd64/arm64 if you are on Apple Silicon or a Raspberry Pi.
5. Pull: `docker pull python:3.12`
6. Prove: `docker run --rm python:3.12 python --version`
7. Record the tag in your lab notes.

**Windows / macOS / Linux:** the pull and run commands do not change.

---

## Common Mistakes

1. **Pulling a similarly named community image** (`python3` from a random user) instead of official `python`.
2. **Assuming Hub search stars equal safety.**
3. **Using `latest` in a report** that must be reproducible next semester.
4. **Confusing Hub's website with `docker images`.** The website is remote; `docker images` is local.
5. **Publishing secrets.** Never put passwords, API keys, or `.env` files in an image you will one day push. Part 1 does not push; keep the habit anyway.
6. **Login to the wrong registry.** Default login is Hub. You do not need a Hub login for Part 1 unless you hit rate limits.
7. **Typos that silently search the wrong repo.** Check `docker images` after pull.

---

## Best Practices

- Official images first.
- Explicit tags (`python:3.12`).
- Pull on a good network, then work offline from cache when possible (the daemon still must run).
- Create a Hub account when rate limits appear; use `docker login`.
- Treat community images like unsolicited executables: only if you have a reason and a source.
- Log out on shared lab computers: `docker logout`.

---

## Exercises

1. **Browser.** Open the official Python image page. Write down one recommended pull command and three tag names you see.
2. **Search.** `docker search python --filter is-official=true` or unfiltered search. Identify the official `python` row.
3. **Pull tag.** `docker pull python:3.12`. Confirm with `docker images`.
4. **Run.** `docker run --rm python:3.12 python --version`.
5. **Hello World Hub page.** Open `_ /hello-world` in the browser. Pull and run with `--rm`.
6. **Compare local vs remote.** After pull, does `docker images` show Hub's entire tag list or only what you pulled? (Only what you pulled.)
7. **Optional login.** Create a free Hub account if you do not have one. `docker login`, then `docker pull python:3.12` again. `docker logout` if you are on a shared computer.
8. **Judgment.** A classmate says "pull `coolhacker/python-fast:latest`, it has more stars." Write three questions you would ask before using it.
9. **Capstone recap.** Repeat the Part 1 capstone from the [course README](../README.md) using only Hub-pulled `python:3.12`.

---

## Quick Review

- Docker Hub is the default registry; `python:3.12` is an official image tag.
- Tags move; pick explicit ones for class.
- `search` and the website find images; `pull` copies them locally.
- Official beats random community images for this course.
- Login is optional until rate limits or pushing (pushing is later).

---

## Summary

You can find, evaluate, and pull images from Docker Hub, which is how `hello-world` and `python:3.12` reached your machine throughout Part 1. You now have the full beginner loop: understand containers, install the engine, use the CLI, manage images and containers, and consume a registry.

**Part 1 is complete.** Part 2 will use this foundation to run Python workflows and Jupyter in containers — Dockerfiles, mounts, and ports on top of the skills you already have.

Continue with [Lesson 9: Running Python with Docker](09-running-python-with-docker.md).

---

[← Previous Lesson](07-docker-containers.md)
[Course Home](../README.md)
[Next Lesson →](09-running-python-with-docker.md)
