# Lesson 3: Docker Architecture

You now know what a container is and how it differs from a VM. This lesson names the parts of Docker you will touch every day: the CLI, the daemon, the Engine, Docker Desktop, images, containers, and registries.

[← Previous Lesson](02-containers-vs-virtual-machines.md)
[Course Home](../README.md)
[Next Lesson →](04-installing-docker.md)

---

## Learning Objectives

After this lesson you will be able to:

- Sketch Docker's client–server architecture.
- Define Docker CLI, Docker daemon (`dockerd`), Docker Engine, and Docker Desktop.
- Explain the path of a command such as `docker run hello-world`.
- Place images, containers, and registries in that architecture.
- Know where your data lives (local image cache vs a registry).

---

## Prerequisites

- Lessons 1 and 2.
- No installation required yet; Lesson 4 installs the pieces named here.

---

## Concept

### Client and server

Docker uses a **client–server** design.

- The **client** is the `docker` program you run in a terminal (the **Docker CLI**).
- The **server** is the **Docker daemon** (`dockerd`), a background process that builds, runs, and manages images and containers.

They talk over an API (REST over a Unix socket on Linux, or a named pipe / TCP endpoint in other setups). You rarely call the API yourself. The CLI does it.

```text
You
 └─ docker CLI  ──(API)──►  Docker daemon (dockerd)
                               ├─ images on disk
                               ├─ containers (processes)
                               └─ talks to registries (pull/push)
```

If the daemon is not running, the CLI prints an error such as "Cannot connect to the Docker daemon." The CLI is not enough by itself.

### Docker Engine

**Docker Engine** is the product name for the runtime stack on a machine: the daemon, the API, and related components such as **containerd** (the low-level container runtime Docker uses). In conversation, "install the Engine" on Linux means installing this stack without the Desktop GUI.

You do not need to configure containerd by hand in Part 1. Remember the name so log messages do not look like a second mysterious Docker.

### Docker Desktop

**Docker Desktop** is the application for Windows and macOS (also available on Linux). It includes:

- Docker Engine (inside a Linux VM / WSL 2 distro on Windows and Mac)
- The `docker` CLI on your host
- A GUI dashboard
- Optional tools (Kubernetes, Docker Compose) that Part 1 does not require

Desktop is how most students install Docker. Linux servers and many cloud VMs install **Engine only**, with no GUI.

| | Docker Desktop | Docker Engine (Linux package) |
|---|----------------|-------------------------------|
| Typical user | Students on Windows/Mac | Linux servers, some Linux laptops |
| GUI | Yes | No |
| Linux containers on Win/Mac | Yes (via WSL 2 or a VM) | Not applicable (already Linux) |
| CLI | `docker` | `docker` |
| Daemon | Managed by Desktop | `dockerd` via systemd |

The commands you type are the same. The difference is how the daemon is installed and started.

### Images, containers, registries

Three object types, three places:

| Object | What it is | Where it lives |
|--------|------------|----------------|
| **Image** | Read-only template (layers) | Local disk cache, and/or a **registry** |
| **Container** | Instance of an image | Only on a machine running the daemon |
| **Registry** | Server that stores and serves images | Docker Hub, GitHub Container Registry, a private registry |

**Docker Hub** (`https://hub.docker.com`) is the default public registry. When you `docker pull python:3.12` with no extra hostname, the daemon asks Docker Hub.

```text
Docker Hub (registry)
        │  docker pull
        ▼
Local image cache  ── docker run ──►  Container (process)
```

`docker run` will **pull** automatically if the image is missing locally. That is why `docker run hello-world` works on a fresh install (network required).

### High-level flow of `docker run hello-world`

1. You type `docker run hello-world`.
2. The CLI sends a "create and start container" request to the daemon.
3. The daemon checks the local cache for the `hello-world` image (tag `latest` if you omit a tag).
4. On a miss, the daemon **pulls** from Docker Hub.
5. The daemon creates a container (writable layer + metadata) and starts the process.
6. The process prints to stdout; the CLI streams that output to your terminal.
7. The process exits. The container exists in **exited** state until you remove it.

### Other moving parts you will hear about

- **runc** — starts the container process. Docker uses it via containerd.
- **BuildKit** — builds images from Dockerfiles (Part 2+). Not needed to *run* images.
- **Compose** — multi-container projects via YAML. Out of scope for Part 1.

Ignore these for hands-on work until later. They explain log lines; they are not extra tools you must start.

---

## Why It Matters

Almost every beginner error is an architecture error in disguise:

| Symptom | Usual cause |
|---------|-------------|
| `Cannot connect to the Docker daemon` | Desktop/Engine not running, or your user cannot access the socket |
| Pull is slow or fails | Registry (network, Hub rate limits, wrong name) |
| `docker` not found | CLI not installed or not on `PATH` |
| Image is "there" on Hub but `docker images` is empty | You never pulled; Hub is remote |
| Container "vanished" | You looked at `docker ps` (running only) instead of `docker ps -a` |

Once you see CLI vs daemon vs registry, these errors become readable.

---

## Commands/Syntax

These commands inspect the architecture. They work the same in **PowerShell** and **bash/zsh**.

CLI vs daemon versions:

```bash
docker version
```

You should see a **Client** section and a **Server** section. If Client exists but Server fails, the CLI is installed and the daemon is not reachable.

Rich daemon snapshot (OS, runtime, images, containers):

```bash
docker info
```

List images in the **local cache** (not "everything on Hub"):

```bash
docker images
```

Equivalent modern form:

```bash
docker image ls
```

Help for the CLI as a whole:

```bash
docker --help
```

Help for one command:

```bash
docker run --help
```

**Linux note:** if you installed Engine with the distribution packages and skipped the `docker` group, prefix with `sudo`:

```bash
sudo docker version
```

**Windows PowerShell / macOS Desktop:** do not use `sudo`. Start Docker Desktop and wait until it says it is running.

---

## Beginner Example

Read `docker version` as two programs:

```text
Client: Docker Engine - Community
 ...
Server: Docker Engine - Community
 ...
```

- Client = CLI (talks to you).
- Server = daemon (talks to images and containers).

If you open a terminal **before** Docker Desktop has finished starting, Client may print and Server may error. Wait, then retry. That single experiment teaches the architecture better than a diagram.

---

## Intermediate Example

Where is the image?

```bash
docker images
docker pull python:3.12
docker images
```

The first list may not include `python`. After `pull`, it does. Docker Hub still has the image too. **Pull copies layers into the local cache.** Deleting your laptop cache does not delete Hub. Deleting Hub (you cannot) would not delete your local copy until you `docker rmi`.

Run without an explicit pull:

```bash
docker run --rm hello-world
```

If `hello-world` is absent locally, the daemon pulls, then runs. `docker images` afterward shows `hello-world`.

---

## Advanced Example

`docker info` fields worth reading once:

| Field | Why it matters |
|-------|----------------|
| `Server Version` | Engine version |
| `Storage Driver` | How image layers are stored (often `overlay2`) |
| `Cgroup Driver` / `Cgroup Version` | How resource limits are enforced |
| `OSType` / `Architecture` | `linux` / `x86_64` or `aarch64` (Apple Silicon is `aarch64`) |
| `Docker Root Dir` | Where images and container data live on disk |
| `Name` | Daemon hostname |

Apple Silicon (`arm64`) vs Intel/AMD (`amd64`) is an architecture detail: many Hub images publish both. If an image is amd64-only, Desktop may emulate it (slower) or fail. Prefer images that list `arm64` when you are on Apple Silicon. Lesson 8 returns to this when reading Hub tags.

Inspect how the CLI reaches the daemon (Linux):

```bash
docker context ls
```

The default context typically uses the Unix socket `unix:///var/run/docker.sock`. You do not need to change this in Part 1.

---

## Practical Example

Keep this map next to your terminal:

```text
docker --help          What can the CLIENT do?
docker version         CLIENT + SERVER both alive?
docker info            SERVER details
docker images          LOCAL image cache
docker ps / docker ps -a    CONTAINERS on this daemon
docker pull            REGISTRY -> local cache
docker run             cache (and maybe pull) -> container
```

**Windows PowerShell:** same commands. If `docker` is not recognized, Docker Desktop is not installed or "Use Docker Desktop" / PATH was not refreshed — open a **new** terminal after installing (Lesson 4).

---

## Common Mistakes

1. **Assuming the GUI is required.** Desktop's GUI is optional. The daemon and CLI are the real engine. Linux servers have no Desktop and work fine.
2. **Confusing Hub with the local cache.** `docker images` is not a search of Hub.
3. **Killing the terminal and thinking the daemon died.** The CLI is short-lived. The daemon is a background service. Closing the terminal does not stop Desktop.
4. **Two CLIs.** Rare, but possible if old Docker Toolbox and Desktop both exist. `docker version` shows which server you hit. Uninstall Toolbox on modern Windows.
5. **Editing files "in Docker" without knowing which layer.** Images are immutable; containers have a writable layer. Lesson 6 and 7.

---

## Best Practices

- Confirm **Server** in `docker version` before blaming a `run` command.
- Learn both spellings: `docker images` and `docker image ls` (the second is the newer grouped CLI).
- Treat Docker Hub as remote storage, your disk as a cache.
- On laptops, start Desktop once and leave it running while you work.
- Do not expose the Docker daemon TCP port to the internet. The default local socket is the correct beginner setup.

---

## Exercises

1. **Label the diagram.** Draw CLI, daemon, local cache, container, and Hub. Draw arrows for `pull` and `run`.
2. **Vocab matching.** Match: `dockerd`, `docker`, Docker Desktop, Docker Hub, image, container.
3. **Predict the error.** The daemon is stopped. You run `docker ps`. What fails: parsing the command, or connecting to the server?
4. **(After install)** Run `docker version` and write down Client version and Server version.
5. **(After install)** Run `docker info` and write down OSType, Architecture, and Docker Root Dir.
6. **(After install)** Run `docker --help` and list five top-level commands you recognize from this lesson.

---

## Quick Review

- The **CLI** (`docker`) is the client. The **daemon** (`dockerd`) is the server.
- **Docker Engine** is the runtime stack. **Docker Desktop** wraps Engine plus a GUI (and a Linux VM on Win/Mac).
- **Images** live in a registry and in a local cache. **Containers** live only on a daemon host.
- `docker version` proves both sides are talking.

---

## Summary

Docker is a client talking to a daemon that manages images and containers and that pulls from registries. Desktop is the friendly installer for that architecture on Windows and macOS. With the parts named, installation (Lesson 4) and the CLI (Lesson 5) will make sense instead of feeling like unrelated commands.

---

[← Previous Lesson](02-containers-vs-virtual-machines.md)
[Course Home](../README.md)
[Next Lesson →](04-installing-docker.md)
