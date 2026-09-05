# Lesson 6: Docker Images

An image is a read-only template used to create containers. This lesson explains layers, names, and tags, then teaches you to pull, list, inspect, and remove images.

[← Previous Lesson](05-docker-cli.md)
[Course Home](../README.md)
[Next Lesson →](07-docker-containers.md)

---

## Learning Objectives

After this lesson you will be able to:

- Define an image and explain image layers.
- Read an image reference: `registry/name:tag`.
- Pull images from Docker Hub, including `python:3.12`.
- List local images and identify REPOSITORY, TAG, IMAGE ID, and SIZE.
- Remove images with `docker rmi` and understand when removal is blocked.
- Choose tags deliberately (`latest` vs `3.12` vs `3.12.8`).

---

## Prerequisites

- Lessons 1–5.
- Working Docker install.
- Network access to Docker Hub for pull exercises.

---

## Concept

### Image = snapshot of a filesystem plus metadata

An image contains:

- A stack of **filesystem layers** (the files the container will see).
- **Metadata**: default command, environment variables, exposed ports, architecture, and more.

Images are **immutable**. You do not edit an image in place. You create containers from it, or later you **build** a new image (not in Part 1).

### Layers

Think of layers as stacked transparent sheets. Each layer records a set of file changes relative to the layer below.

```text
┌─────────────────────────┐  top layer: pip packages (example)
├─────────────────────────┤  Python interpreter
├─────────────────────────┤  OS packages
└─────────────────────────┘  base filesystem (e.g. Debian)
```

When ten containers use `python:3.12`, the Python layers are stored **once**. Each container adds a thin **writable layer** on top (Lesson 7). That is why containers are disk-efficient compared with copying a full VM disk per instance.

`docker pull` downloads **only layers you do not already have**. If you already pulled `python:3.12`, pulling `python:3.12` again is quick (the daemon checks and reports "Image is up to date" or downloads changed layers).

### Names and tags

A full reference looks like:

```text
[registry/][namespace/]repository:tag
```

Examples:

| Reference | Registry | Namespace | Repository | Tag |
|-----------|----------|-----------|------------|-----|
| `hello-world` | Docker Hub (default) | `library` (official) | `hello-world` | `latest` (default) |
| `python:3.12` | Docker Hub | `library` | `python` | `3.12` |
| `docker.io/library/python:3.12` | Explicit Hub | `library` | `python` | `3.12` |

If you omit the registry, Docker uses Docker Hub (`docker.io`). If you omit the tag, Docker uses `latest`.

**`latest` does not mean "the newest stable forever" in a reliable way.** It means "the tag named latest." Maintainers choose what it points at. Prefer explicit tags in classwork: `python:3.12` is better than `python` or `python:latest`.

Official images on Hub live under the `library` namespace. You write `python`, not `library/python`. User and organization images look like `username/myapp:1.0`.

### Image ID

Besides names, every image has an **IMAGE ID** (a content hash, shown as a short hex string in `docker images`). Tags are pointers to IDs. Several tags can point to the same ID.

```text
python:3.12     ──►  sha256:abc123...
python:3.12.8   ──►  sha256:abc123...   (if they currently match)
```

Removing by tag removes that name. If other tags still point at the ID, the layers remain.

### Image vs container (again)

```bash
docker images      # templates
docker ps -a       # instances
```

`docker rmi` removes images. `docker rm` removes containers. Mixing them is the most common CLI typo in this course.

---

## Why It Matters

You cannot run a container without an image. Pulling the **wrong tag** is how labs silently use Python 3.11 when the syllabus says 3.12. Understanding layers explains why the first pull is slow and the second is fast, and why `docker system df` can show image size much smaller than "size times number of containers."

---

## Commands/Syntax

### Pull

```bash
docker pull python:3.12
docker pull hello-world
```

`docker pull <image>` downloads the image into the local cache. It does not start a container.

### List

```bash
docker images
docker image ls
```

Columns:

| Column | Meaning |
|--------|---------|
| REPOSITORY | Name (`python`, `hello-world`) |
| TAG | Tag (`3.12`, `latest`) |
| IMAGE ID | Short identifier |
| CREATED | When that image was built (not when you pulled) |
| SIZE | Apparent size (shared layers make totals non-additive) |

### Run uses an image

```bash
docker run --rm python:3.12 python --version
```

If the image is missing, `run` pulls it first. Explicit `pull` is still useful: you can prefetch on campus Wi-Fi before a demo.

### Remove

```bash
docker rmi hello-world
docker image rm hello-world
```

`rmi` is "remove image." You may pass a name:tag or an IMAGE ID.

If a container (even stopped) still uses the image, removal fails. Remove the container first (`docker rm`), then `docker rmi`.

Force (only when you understand why it is blocked):

```bash
docker rmi -f <image>
```

Prefer fixing the real cause (stop/remove containers) over `-f`.

### Inspect an image

```bash
docker inspect python:3.12
```

This prints JSON. To extract architecture:

```bash
docker inspect --format "{{.Architecture}}" python:3.12
```

Same command in PowerShell and bash if you keep double quotes.

### Interactive Python (image in use)

```bash
docker run -it python:3.12
```

`-it` is explained fully in Lesson 7. Here it shows that the image contains a working Python REPL. Exit with `exit()` or Ctrl+D.

**Windows PowerShell:** `-it` works in current Windows Terminal / PowerShell with Docker Desktop. Use Windows Terminal if a legacy console mishandles interactive TTY.

---

## Beginner Example

```bash
docker pull python:3.12
docker images
docker run --rm python:3.12 python --version
```

Read the pull output. You will see layer IDs and "Pull complete" per layer. That is the layer model in action.

Then:

```bash
docker pull python:3.12
```

The second pull should be mostly "Already exists" or "Image is up to date."

---

## Intermediate Example

Compare tags:

```bash
docker pull hello-world
docker pull hello-world:latest
docker images hello-world
```

`hello-world` and `hello-world:latest` are the same default. You should see one repository with tag `latest` (not two copies), unless extra tags exist.

Filter the list:

```bash
docker images python
```

Remove an image you do not need (only if no container uses it):

```bash
docker rmi hello-world
docker images
```

Pull it again when you want it.

---

## Advanced Example

**SIZE is not a simple sum.** Two images that share a base can total less disk than SIZE1 + SIZE2. `docker system df` is the better disk picture.

**Pinning:**

```bash
docker pull python:3.12
docker pull python:3.12-slim
```

- `python:3.12` is a full image (more tools, larger).
- `python:3.12-slim` is a smaller variant. Enough for many scripts; sometimes missing OS packages you might assume exist.

Part 2 may use either. For Part 1, `python:3.12` is the default example.

**Digest** (optional knowledge):

Images also have a digest (`sha256:...`). Tags move; digests do not. Production pinning uses digests. For this course, named tags such as `python:3.12` are enough.

**Architecture:**

```bash
docker inspect --format "{{.Os}}/{{.Architecture}}" python:3.12
```

You want `linux/amd64` or `linux/arm64` matching your engine. Desktop on Apple Silicon typically shows `arm64`.

---

## Practical Example

Lab setup you can reuse for the rest of Part 1:

```bash
docker pull hello-world
docker pull python:3.12
docker images
docker run --rm python:3.12 python --version
docker run --rm hello-world
```

**PowerShell / macOS / Linux:** identical.

If pull fails with a rate-limit error from Hub, Lesson 8 explains free anonymous limits and logging in. For now, retry later or log in with `docker login` if you have a Hub account.

---

## Common Mistakes

1. **`docker rmi` vs `docker rm`.** Image vs container.
2. **Deleting an image while a stopped container still references it.** `docker ps -a` first.
3. **Trusting `latest`.** Always say the tag in reports.
4. **Comparing SIZE column across images as exclusive disk use.** Layers are shared.
5. **Assuming pull installed Python on the host.** Check: `python --version` on the host is unrelated.
6. **Typos in the name.** `phython:3.12` will try to pull a nonexistent repository.

---

## Best Practices

- Pin a tag: `python:3.12` (or a patch tag) for class.
- Prefer official images while learning.
- Pull once, run many times.
- Remove unused images when disk is tight; keep images you use every session.
- Use `docker images` and `docker system df` together.
- Do not force-remove images to "make an error go away" without reading the error.

---

## Exercises

1. **Pull.** `docker pull python:3.12`. Watch layer output. How many layers roughly appeared?
2. **List.** `docker images`. Write down REPOSITORY, TAG, IMAGE ID, SIZE for `python`.
3. **Idempotent pull.** Pull `python:3.12` again. What did Docker print?
4. **One-shot run.** `docker run --rm python:3.12 python --version`. Confirm 3.12.
5. **Hello World image.** Pull `hello-world` if needed, list it, run it, then `docker rmi hello-world` after removing any exited container that uses it (`docker ps -a` then `docker rm`).
6. **Inspect.** `docker inspect python:3.12` and find `Architecture` in the JSON (or use `--format`).
7. **Blocked delete.** Create a container without `--rm`: `docker run --name keep-me python:3.12 python --version`. Try `docker rmi python:3.12`. Read the error. Then `docker rm keep-me` and decide whether you still want to remove the image (you should **keep** `python:3.12` for Lesson 7).
8. **Help.** `docker pull --help` and `docker rmi --help`. Name one flag from each.

---

## Quick Review

- Images are immutable, layered templates.
- Reference format: `name:tag` on Hub by default.
- `pull` fills the cache; `images` lists it; `rmi` deletes from the cache.
- `latest` is a tag name, not a promise.
- Shared layers save disk; SIZE columns are not simply additive.

---

## Summary

You can now fetch and identify images, including `python:3.12`, and you understand tags and layers. Lesson 7 turns those images into containers you start, stop, inspect, and remove.

---

[← Previous Lesson](05-docker-cli.md)
[Course Home](../README.md)
[Next Lesson →](07-docker-containers.md)
