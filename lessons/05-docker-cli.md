# Lesson 5: Docker CLI

The Docker command-line interface is the `docker` program. This lesson teaches how commands are structured, how to get help, how to inspect the engine, and how to read disk usage. You will use this interface in every later lesson.

[← Previous Lesson](04-installing-docker.md)
[Course Home](../README.md)
[Next Lesson →](06-docker-images.md)

---

## Learning Objectives

After this lesson you will be able to:

- Parse a Docker command into `docker`, a command (or command group), flags, and arguments.
- Use `docker --help` and `docker <command> --help` instead of memorizing every flag.
- Interpret `docker version` and `docker info`.
- List running and stopped containers; list images.
- Read disk usage with `docker system df` and clean safely with `docker system prune`.
- Recognize the modern grouped CLI (`docker container ls`) next to classic aliases (`docker ps`).

---

## Prerequisites

- Lesson 4 completed: `docker version` shows a Server section.
- Comfort typing in PowerShell or bash/zsh.

---

## Concept

### Anatomy of a command

```text
docker [global options] command [command options] [arguments]
```

Examples:

```bash
docker version
docker --help
docker ps -a
docker run --rm python:3.12 python --version
```

| Piece | Example | Role |
|-------|---------|------|
| Binary | `docker` | The CLI |
| Command | `run`, `ps`, `version` | What you want |
| Command options (flags) | `--rm`, `-a` | Modify behavior |
| Arguments | `python:3.12`, `python --version` | Image name, command inside the container |

Flags can be short (`-a`) or long (`--all`). They are not the same as arguments. `docker ps -a` means "list all containers." There is no extra argument.

### Classic commands vs grouped commands

Docker now groups objects:

```text
docker image ls
docker container ls
docker system df
```

Older, still fully supported aliases:

```text
docker images    (same family as docker image ls)
docker ps        (same family as docker container ls)
```

This course teaches **both**. Many tutorials and exam questions still use `docker ps` and `docker images`. The grouped forms are easier to discover with `--help`.

```bash
docker --help
docker image --help
docker container --help
docker system --help
```

### Help is a skill

Do not memorize fifty flags. Memorize this:

```bash
docker --help
docker run --help
docker ps --help
```

`--help` works on groups and on leaf commands. Read the `Usage:` line first. Then scan flags you need.

### Global vs command flags

```bash
docker --version
```

This is a **global** flag on the `docker` binary (prints CLI version only — not a substitute for `docker version`).

```bash
docker ps --all
```

`--all` belongs to `ps`. Putting it in the wrong place fails:

```bash
docker --all ps
```

That is invalid. Order matters: global options, then command, then command options.

### Exit codes

The CLI returns exit code `0` on success. Non-zero means failure. In bash/zsh:

```bash
docker version
echo $?
```

In **PowerShell**:

```powershell
docker version
echo $LASTEXITCODE
```

You rarely need this in Part 1, but it explains why scripts stop after a failed `docker pull`.

---

## Why It Matters

Every Docker skill is a CLI skill until you adopt a GUI. Desktop's dashboard is fine for clicking a container to stop it. It will not be available on most servers, CI systems, or exam lock-down accounts. If you can `docker --help` your way out of a forgotten flag, you are independent.

---

## Commands/Syntax

### Discovery and engine

```bash
docker --help
docker version
docker info
```

| Command | Purpose |
|---------|---------|
| `docker --help` | List top-level commands and global flags |
| `docker version` | Client and Server versions (and API versions) |
| `docker info` | Daemon configuration, counts of images/containers, storage driver |

### List objects

```bash
docker ps
docker ps -a
docker images
```

| Command | Purpose |
|---------|---------|
| `docker ps` | Running containers only |
| `docker ps -a` | All containers, including exited |
| `docker ps --all` | Same as `-a` |
| `docker images` | Local images |

Modern equivalents:

```bash
docker container ls
docker container ls -a
docker image ls
```

### Disk and cleanup

```bash
docker system df
docker system prune
```

| Command | Purpose |
|---------|---------|
| `docker system df` | Disk used by images, containers, volumes, build cache |
| `docker system prune` | Remove dangling data (see warnings below) |

`prune` asks for confirmation. Type `y` to proceed.

To skip the prompt (scripts only; know what you are deleting):

```bash
docker system prune -f
```

`-f` / `--force` skips the yes/no question. **Linux/macOS and PowerShell: same flag.**

A stronger cleanup (still not everything):

```bash
docker system prune -a
```

`-a` also removes unused images, not only dangling ones. You will re-pull images you still need. Do not run `-a` in the middle of a lab unless you understand the cost.

`docker system prune` does **not** delete:

- Running containers
- Images used by remaining containers (without `-a`, unused named images often remain)
- Named volumes, unless you add `--volumes` (do **not** add `--volumes` until you study volumes; you can destroy data)

Part 1 recommendation: use `docker system df` often and `docker system prune` (no `-a`, no `--volumes`) to clear leftover stopped containers and dangling images.

### Formatting (preview)

```bash
docker ps --format "table {{.ID}}\t{{.Names}}\t{{.Status}}"
```

Go templates power `--format`. Optional in Part 1. Useful when the default table is too wide.

**PowerShell note:** double quotes work as shown. If a later lesson uses single quotes around a template, PowerShell may treat the string differently. This course uses double quotes in `--format` examples so they work in both shells.

---

## Beginner Example

Spend five minutes only on help:

```bash
docker --help
```

Find `run`, `images`, `ps`, `pull`, `version`, `info`, `system` in the list.

Then:

```bash
docker version
```

Confirm you still have a Server section (daemon up).

Then:

```bash
docker ps
docker ps -a
docker images
```

Empty tables are valid. They mean "nothing running," "no containers exist," or "no local images" — not "Docker is broken."

---

## Intermediate Example

Compare classic and grouped commands:

```bash
docker ps -a
docker container ls -a

docker images
docker image ls
```

The tables should match (maybe column order or headers differ slightly). Pick one style and stay consistent in your notes. This course uses `docker ps` and `docker images` in most examples because they are short and ubiquitous, and mentions the grouped form so you are not surprised.

Disk check:

```bash
docker system df
```

Example output (numbers will differ):

```text
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          2         1         180MB     20MB
Containers      3         0         12kB      12kB
Local Volumes   0         0         0B        0B
Build Cache     0         0         0B        0B
```

**RECLAIMABLE** is what prune can free if you accept its defaults.

---

## Advanced Example

Read `docker info` with intent. Useful keys for students:

```text
Containers: 3 (running how many?)
Images: 2
Server Version
Storage Driver: overlay2
Operating System
OSType: linux
Architecture
CPUs / Total Memory
Docker Root Dir
Username (Hub login, if any)
```

If `Containers` is high and `Running` is 0, you have exited containers occupying table space (`docker ps -a`) and a little disk. Prune or `docker rm` them.

Client/server mismatch: a very old CLI talking to a new daemon (or the reverse) can fail. `docker version` prints both. After a Desktop update, if commands break, restart Desktop and open a new terminal.

**Windows PowerShell vs Unix shells — line continuation:**

Long commands in this course stay on one line when possible.

Linux/macOS bash/zsh continuation is a backslash:

```bash
docker ps \
  -a
```

PowerShell continuation is a backtick:

```powershell
docker ps `
  -a
```

Do not copy a bash backslash into PowerShell and expect it to continue the line. For Part 1, prefer single-line commands.

---

## Practical Example

A healthy "start of study session" checklist:

```bash
docker version
docker info
docker ps -a
docker images
docker system df
```

If `version` fails on Server, start Docker Desktop (or `sudo systemctl start docker` on Linux Engine) and retry **before** debugging `run`.

Cleanup at the end of a messy experiment day:

```bash
docker ps -a
docker system prune
```

Read the warning. Confirm you do not need those stopped containers. Then `y`.

---

## Common Mistakes

1. **`docker ps` looks empty after Hello World.** Use `-a`. Exited containers are hidden by default.
2. **Running `prune` when you meant `df`.** `df` is read-only. `prune` deletes.
3. **`docker system prune -a --volumes` as a reflex.** That combination is aggressive. Not for Part 1 daily use.
4. **Wrong flag position.** `docker -a ps` is not `docker ps -a`.
5. **Trusting a GUI count over the CLI in screenshots for homework.** Graders use the CLI. You should too.
6. **PowerShell wrapping.** If you paste a command with Unix `\` continuation, PowerShell will error. Use one line.

---

## Best Practices

- `--help` before guessing.
- `docker version` when anything "cannot connect."
- Prefer `docker system df` before prune so you know what you will free.
- Learn both `ps` and `container ls`.
- Keep a personal cheatsheet; this repo also has `cheatsheet.md`.
- Do not alias `docker` to `sudo docker` blindly on shared servers.

---

## Exercises

1. **Help map.** Run `docker --help`. List eight commands you will use in Part 1.
2. **Nested help.** Run `docker container --help` and `docker image --help`. Name two subcommands from each.
3. **Version.** Record Client Version, Server Version, and OS/Arch from `docker version`.
4. **Info.** From `docker info`, write OSType, Architecture, Storage Driver, Docker Root Dir.
5. **Tables.** Show that `docker ps` and `docker container ls` agree. Show that `docker images` and `docker image ls` agree.
6. **Disk.** Run `docker system df`. Note Images SIZE vs RECLAIMABLE.
7. **Prune dry-run mindset.** Run `docker system prune` and read the warning. Answer `n` this time unless you intend to clean. (Choosing `n` is a valid exercise outcome.)
8. **Shell note.** Write one sentence in your notes about line continuation in your shell (backslash vs backtick vs "I will use one line").

---

## Quick Review

- `docker` + command + flags + args.
- `--help` is hierarchical.
- `version` and `info` inspect the engine; `ps` / `images` inspect objects; `system df` / `prune` inspect and clean disk.
- `ps` is running only; `ps -a` is all.
- Classic and grouped CLIs coexist.

---

## Summary

The CLI is a client for the daemon. Help, version, info, listing, and system disk commands are the foundation. With those reflexes, you are ready to study images as objects — layers, names, and tags — in Lesson 6.

---

[← Previous Lesson](04-installing-docker.md)
[Course Home](../README.md)
[Next Lesson →](06-docker-images.md)
