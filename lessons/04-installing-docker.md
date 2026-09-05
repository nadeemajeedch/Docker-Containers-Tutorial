# Lesson 4: Installing Docker

This is the first hands-on lesson. You will install Docker, verify the client and daemon, and run `hello-world`. After this lesson, every remaining Part 1 lesson assumes `docker version` shows a Server section.

[← Previous Lesson](03-docker-architecture.md)
[Course Home](../README.md)
[Next Lesson →](05-docker-cli.md)

---

## Learning Objectives

After this lesson you will be able to:

- Choose Docker Desktop vs Docker Engine for your computer.
- Install Docker on Windows, macOS, or Linux following current practice.
- Verify the install with `docker version`, `docker info`, and `docker run hello-world`.
- Fix the most common install failures (daemon not running, PATH, permissions).
- Know what you should not do (legacy Docker Toolbox, random third-party installers).

---

## Prerequisites

- Lessons 1–3 (especially architecture: CLI vs daemon).
- Administrator or sudo rights.
- A network connection to download the installer and to pull `hello-world`.
- Windows 10/11, macOS (Intel or Apple Silicon), or a current Linux distribution.

Hardware notes:

- **Windows:** WSL 2 capable machine (required for current Docker Desktop).
- **Mac:** Apple Silicon (M1/M2/M3/M4) must use the Apple Silicon Desktop build, not the Intel build.
- **RAM:** 8 GB recommended; 4 GB is uncomfortable.

---

## Concept

### What you are installing

You need both:

1. The **`docker` CLI** on your `PATH`.
2. A running **daemon** that the CLI can reach.

On Windows and macOS, **Docker Desktop** provides both. On Linux you may install Desktop **or** Docker Engine (packages from Docker's official repository).

### Current vs obsolete install paths

| Use this | Do not use |
|----------|------------|
| Docker Desktop (Win/Mac, optional Linux) | Docker Toolbox, docker-machine, VirtualBox-based "Docker Quickstart" |
| Docker Engine from Docker's official docs (Linux) | Random `curl \| bash` scripts from blogs |
| WSL 2 backend on Windows | Legacy Hyper-V-only backend unless Desktop requires it |
| Official docs: `https://docs.docker.com/get-started/get-docker/` | Outdated course PDFs that mention boot2docker |

This course follows **Linux containers** everywhere, including Windows (via WSL 2).

### Docker Desktop vs Engine (Linux)

- **Desktop:** best for students. GUI, automatic updates, easy start/stop.
- **Engine:** best for servers and for Linux users who want no extra GUI. You start the daemon with systemd (`sudo systemctl start docker`).

Commands after install are the same.

### What installation does *not* do

- It does not install Python, Node, or your homework stack on the host. Those stay in images.
- It does not sign you into Docker Hub. Pulling public images works without an account. (Hub accounts matter for rate limits and for pushing; Lesson 8.)
- It does not start containers until you run them.

---

## Why It Matters

An unverified install wastes hours later. Five minutes of `docker version` and `hello-world` tells you:

- The CLI is on `PATH`.
- The daemon is running.
- Your user may talk to the daemon.
- Network pull from Hub works.
- Containers can start on this machine.

Part 2 (Python/Jupyter) is impossible until this lesson is green.

---

## Commands/Syntax

Verification set (identical in **PowerShell** and **bash/zsh** unless noted):

```bash
docker --help
docker version
docker info
docker run hello-world
```

| Command | Success looks like |
|---------|-------------------|
| `docker --help` | Usage text, list of commands |
| `docker version` | Client **and** Server blocks |
| `docker info` | Long report, no connection error |
| `docker run hello-world` | "Hello from Docker!" and an explanation of the pull/run flow |

**Linux Engine only** — if you get permission denied on the socket:

```bash
sudo docker version
```

Then follow Docker's post-install steps to add your user to the `docker` group, **log out and back in**, and retry without sudo.

**Do not** use `sudo` on Docker Desktop for Windows or macOS.

Check that the daemon is running:

- **Desktop:** the whale/menu icon should indicate running. Wait until "Engine running" / "Docker Desktop is running."
- **Linux Engine:**

```bash
sudo systemctl status docker
```

(You only need `systemctl` to inspect the service. Do not disable unrelated system services.)

---

## Beginner Example

### Windows (Docker Desktop + WSL 2)

1. Install WSL 2 if needed. In **PowerShell as Administrator**:

```powershell
wsl --install
```

Reboot if Windows asks.

2. Download Docker Desktop for Windows from Docker's official Get Docker page. Run the installer. Enable the WSL 2 backend when asked.

3. Start Docker Desktop. Wait until it reports that the engine is running.

4. Open a **new** PowerShell or Windows Terminal window (PATH updates apply to new sessions):

```powershell
docker version
docker run hello-world
```

5. If `docker` is not recognized, sign out of Windows or reboot once, then retry.

### macOS (Docker Desktop)

1. Download **Docker Desktop for Mac** — Apple Silicon or Intel, matching your machine (Apple menu → About This Mac).
2. Drag Docker to Applications, open it, approve the privileged helper when macOS asks.
3. Wait until the menu bar icon shows Docker is running.
4. Open Terminal:

```bash
docker version
docker run hello-world
```

### Linux (Engine, summary)

Always follow the current instructions on Docker's documentation for your distribution (Ubuntu, Debian, Fedora, etc.). The usual shape is:

1. Uninstall old unofficial `docker` packages if the docs say so.
2. Add Docker's official apt/dnf repository.
3. Install `docker-ce`, `docker-ce-cli`, and `containerd.io`.
4. Start the service.
5. Run `sudo docker run hello-world`.
6. Optional: add your user to the `docker` group as in the official post-install guide, then re-login.

Do not copy decade-old `apt-get install docker.io` blog posts without reading current Docker docs; package names and repos change.

---

## Intermediate Example

Read the `hello-world` output. It is a short architecture lesson:

1. The CLI contacted the daemon.
2. The daemon lacked the image, so it pulled `hello-world` from Docker Hub.
3. The daemon created a container.
4. The daemon ran the container; the process printed the message.
5. The process exited.

Then:

```bash
docker ps
docker ps -a
docker images
```

- `docker ps` is probably empty (nothing still running).
- `docker ps -a` shows the exited `hello-world` container.
- `docker images` shows the `hello-world` image remaining in the cache.

Remove the exited container (replace the ID with yours):

```bash
docker ps -a
docker rm <container_id>
```

You may also use the container name in the `NAMES` column.

The image remains until:

```bash
docker rmi hello-world
```

You can pull it again anytime.

---

## Advanced Example

### Confirm platform and resources

```bash
docker info
```

Check:

- `OSType: linux` (you want Linux containers).
- `Architecture: x86_64` or `aarch64`.
- Enough space under `Docker Root Dir`.

On Windows, in Docker Desktop → Settings, confirm **Use the WSL 2 based engine** is enabled.

### Disk and memory on Desktop

Desktop Settings allow you to cap RAM and CPUs for the Linux engine. If the host has 8 GB RAM, giving Docker 6 GB will starve the rest of the OS. A modest cap (for example 2 GB) is enough for Part 1.

### Corporate proxies and SSL inspection

If `docker pull` fails with TLS or timeout errors on a university network, you may need proxy settings in Desktop (Settings → Resources → Proxies) matching the campus proxy. This is an environment issue, not a Docker bug.

### Apple Silicon

If a pull or run fails with exec format errors, the image may be amd64-only. For Part 1, `hello-world` and `python:3.12` publish multi-arch manifests and should work.

---

## Practical Example

Full first-session script after the installer finishes:

```bash
docker --help
docker version
docker info
docker run hello-world
docker ps -a
docker images
docker pull python:3.12
docker run --rm python:3.12 python --version
```

**PowerShell:** paste the same lines. No changes.

Expected Python output resembles:

```text
Python 3.12.x
```

The patch number (`x`) varies. The `3.12` minor version should match the tag.

If `python --version` on your **host** prints 3.10 and the **container** prints 3.12, that is success: two different Pythons, by design.

---

## Common Mistakes

1. **CLI works, daemon does not.** Desktop not started, or Linux `docker` service stopped.
2. **Old terminal.** Install added `docker` to PATH; existing windows do not see it. Open a new terminal.
3. **Wrong Desktop binary on Mac.** Intel build on Apple Silicon (or the reverse).
4. **Permission denied on Linux socket.** User not in `docker` group, or you forgot to re-login after adding the group.
5. **Using Toolbox / docker-machine.** Uninstall those if present; they conflict with Desktop.
6. **Assuming `sudo docker` on Windows.** PowerShell as your user is correct for Desktop.
7. **Offline exam environment.** `hello-world` must already be pulled, or Hub must be reachable.

---

## Best Practices

- Install from Docker's official documentation only.
- Verify with `docker version` (Server block) and `hello-world` the same day you install.
- Leave Desktop running while you study; starting it takes time.
- Add your Linux user to the `docker` group instead of living on `sudo` — but understand that membership is root-equivalent for the host. That is acceptable on a personal student laptop; it is a policy issue on shared lab servers.
- Keep Desktop reasonably updated; Engine APIs stay backward compatible for the commands in this course.

---

## Exercises

1. **Install** Docker Desktop or Engine using the official docs for your OS.
2. **Verify** `docker version` shows Client and Server. Screenshot or paste both version numbers into your notes.
3. **Help.** Run `docker --help` and `docker run --help`. Write one sentence on the difference.
4. **Hello World.** Run `docker run hello-world`. In your own words, list the steps Docker performed.
5. **Lists.** Run `docker ps`, `docker ps -a`, and `docker images`. Explain why `ps` and `ps -a` differ.
6. **Python probe.** `docker pull python:3.12` then `docker run --rm python:3.12 python --version`.
7. **Info.** From `docker info`, record OSType, Architecture, and whether you have any running containers.
8. **Cleanup.** Remove the exited `hello-world` container with `docker rm`. Confirm with `docker ps -a`. Keep the `python:3.12` image for later lessons.

---

## Quick Review

- Desktop for Win/Mac; Engine or Desktop for Linux.
- Success = CLI on PATH + running daemon + `hello-world` output.
- PowerShell and bash use the same `docker` commands here.
- Toolbox and boot2docker are obsolete.
- `docker version` without a Server section means you are not done.

---

## Summary

You installed the CLI and a daemon, proved they talk, pulled from Docker Hub, and ran your first containers. The rest of Part 1 teaches the command line in depth, then images, container lifecycle, and Hub — on top of this working install.

---

[← Previous Lesson](03-docker-architecture.md)
[Course Home](../README.md)
[Next Lesson →](05-docker-cli.md)
