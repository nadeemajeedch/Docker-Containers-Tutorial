# Lesson 1: Introduction to Docker

Welcome to Part 1 of the Docker and Containers Tutorial. This lesson explains what Docker is, what a container is, and why both exist. You do not need Docker installed yet. Lesson 4 covers installation.

[Course Home](../README.md)

---

## Learning Objectives

After this lesson you will be able to:

- Define Docker, a container, and an image in one or two sentences each.
- Explain the "works on my machine" problem and how containers address it.
- Describe reproducibility and why it matters in class, research, and production.
- Distinguish an image (the recipe) from a container (a running instance).
- Recognize what Docker is **not** (it is not a virtual machine, not a cloud, not a programming language).

---

## Prerequisites

- None. This is the starting lesson.
- A willingness to learn a few new words: image, container, registry, engine.

---

## Concept

### The problem Docker solves

Software does not run in a vacuum. A Python script needs a Python interpreter. That interpreter needs libraries. Those libraries need a specific operating system. Your classmate's laptop has different versions. The lab computer has different versions. The grader's machine has different versions.

The result is the sentence every instructor hears:

> It works on my machine.

That sentence is not an excuse. It is a description of **environment drift**: two computers that were supposed to be equivalent are not.

You can try to fix drift by writing long setup guides ("install Python 3.12.8, then pip install these twelve packages, then set this environment variable"). Those guides rot. They also fail when two tools need conflicting versions of the same library.

### Containerization

**Containerization** packages an application together with everything it needs to run: the program, its runtime, libraries, configuration, and files. The package is a **container image**. When you start that image, you get a **container**: an isolated process (or group of processes) that sees its own filesystem and its own network identity, but shares the host's operating system kernel.

Analogy:

| Kitchen analogy | Docker |
|-----------------|--------|
| Recipe (ingredients + steps) | Image |
| A meal cooked from that recipe | Container |
| Cookbook shelf / supermarket | Registry (for example Docker Hub) |
| The kitchen and stove | Docker Engine on your computer |

You can cook the same recipe many times. Each meal is a separate container. The recipe does not change when you eat the meal.

### What Docker is

**Docker** is a platform for building, shipping, and running containers. In everyday student use, "Docker" usually means:

1. **Docker Engine** — the software on your computer that actually runs containers.
2. **Docker CLI** — the `docker` command you type in a terminal.
3. **Docker Hub** — a public library of images you can download.

Docker did not invent containers. Linux had isolation features (namespaces, cgroups) for years. Docker made those features **usable**: a simple CLI, a standard image format, and a public registry.

### Images vs containers (learn this now)

This distinction will appear in every later lesson.

- An **image** is a read-only template. It has a name such as `python:3.12` or `hello-world`. It does not run. It sits on disk (or in a registry).
- A **container** is a running (or stopped) instance created from an image. You can have many containers from one image.

```text
Image: python:3.12          (template, read-only)
   |
   +-- Container A          (your interactive Python session)
   +-- Container B          (a script you ran last night, now stopped)
   +-- Container C          (another student's identical environment)
```

### What Docker is not

- Not a virtual machine hypervisor (Lesson 2 explains the difference).
- Not a cloud provider. Docker runs on your laptop and also in clouds, but it is not AWS, Azure, or GCP.
- Not a programming language. You still write Python, Java, Go, or whatever your course uses.
- Not automatic security. A container can still contain vulnerable software. Isolation is not a substitute for updates.

---

## Why It Matters

If you only ever run code on one laptop, Docker can feel optional. It stops being optional as soon as any of these is true:

- A classmate cannot run your project.
- A teaching assistant must grade 80 assignments with the same dependencies.
- A research paper must be reproducible two years later.
- You deploy to a server that is not your laptop.
- Two projects on one machine need different Python or Node versions.

Containers give you **reproducibility**: the same image produces the same runtime behavior on any machine that can run Docker. They also give you **isolation**: experimenting with a database or an old library does not wreck the rest of your laptop.

In industry, containers are the default packaging format for microservices, CI pipelines, and cloud workloads. Learning Docker now is not a niche skill. It is literacy.

---

## Commands/Syntax

You do not need these commands to work yet. They are here so the words become familiar. Lesson 4 installs Docker; Lessons 5–7 explain each option in detail.

Check that Docker exists:

```bash
docker version
```

Run the canonical first container:

```bash
docker run hello-world
```

What `docker run hello-world` does, in order:

1. The CLI talks to the Docker daemon.
2. If the `hello-world` image is not on your machine, Docker **pulls** it from Docker Hub.
3. Docker **creates** a container from that image.
4. Docker **starts** the container.
5. The program inside prints a message and exits.

Pull an image without running it:

```bash
docker pull python:3.12
```

Run a command inside a throwaway container, then delete the container:

```bash
docker run --rm python:3.12 python --version
```

| Piece | Meaning |
|-------|---------|
| `docker` | The CLI |
| `run` | Create and start a container |
| `--rm` | Remove the container when it exits |
| `python:3.12` | Image name and tag |
| `python --version` | Command to run inside the container |

These commands are identical in **PowerShell**, **cmd**, **bash**, and **zsh**.

---

## Beginner Example

Imagine you need Python 3.12 for homework, but your laptop has Python 3.10 for another class.

Without Docker you might install a second Python, fight with `PATH`, and break the first class.

With Docker you leave the laptop Python alone:

```bash
docker run --rm python:3.12 python --version
```

Docker uses the Python **inside the image**, not the Python on your laptop. Your laptop's 3.10 install is untouched.

You have not "installed Python 3.12" on the host. You have **run** Python 3.12 inside a container.

---

## Intermediate Example

A teammate sends you a project and says "just run `app.py`." You try. It fails because they used a library you do not have.

The Docker-oriented workflow is:

1. They publish (or send) an image that already contains the app and its libraries.
2. You run that image.
3. You both see the same behavior.

Until you learn to **build** images (later in the course), you already benefit as a **consumer**: you pull official images such as `python:3.12` and `hello-world` and run them.

List what is running right now:

```bash
docker ps
```

An empty table is normal. `hello-world` starts, prints, and exits, so it does not stay in `docker ps`. Stopped containers appear with:

```bash
docker ps -a
```

---

## Advanced Example

Reproducibility is stronger when you pin **tags**.

```bash
docker pull python:3.12
docker pull python:3.12.8
```

- `python:3.12` is a **moving tag**. It points at the latest 3.12 patch Docker publishes. Next month it might be 3.12.9.
- `python:3.12.8` is more specific. Your lab report can say "we ran `python:3.12.8`."

For class labs, `python:3.12` is usually fine. For a paper or a production deploy, prefer a more specific tag (and later, a digest). Lesson 6 and Lesson 8 return to tags.

---

## Practical Example

Your first mental model of a Docker session:

```text
1. Is Docker installed?     docker version
2. Run a test container     docker run hello-world
3. Get a useful image       docker pull python:3.12
4. Use it once              docker run --rm python:3.12 python --version
5. See leftover containers  docker ps -a
```

On **Windows PowerShell** and on **Linux/macOS**, type those lines as shown. Do not add `sudo` on Windows or macOS Desktop. On some Linux Engine installs, `sudo docker version` is required until your user is in the `docker` group (Lesson 4).

---

## Common Mistakes

1. **Thinking Docker installs software on the host.** `docker run python:3.12` does not add `python` to your Start Menu or `/usr/bin`. The Python lives inside the container.
2. **Confusing image and container.** `docker images` lists templates. `docker ps -a` lists instances.
3. **Expecting `docker ps` to show Hello World.** Hello World exits immediately. Use `docker ps -a`.
4. **Assuming Docker is a VM.** You will see why that is wrong in Lesson 2. Do not start "a Linux VM named Docker" as your mental model.
5. **Skipping the why.** If you only memorize commands, Part 2 (Python/Jupyter) will feel like magic instead of a tool.

---

## Best Practices

- Learn vocabulary first: image, container, registry, engine, CLI, daemon.
- Prefer official images when you are starting (`python`, `hello-world`).
- Use `--rm` for one-shot experiments so stopped containers do not pile up.
- Write down the image tag you used in lab reports (`python:3.12`, not "Python").
- Do not fight your host OS. Let the container provide the runtime.

---

## Exercises

You may complete exercises 1–4 on paper. Exercises 5–6 wait until Lesson 4 if Docker is not installed.

1. **Define.** In your own words (two sentences each): image, container, Docker Engine.
2. **Diagnose.** A classmate says their code runs at home but fails in the lab. List three possible environment differences containers would hide.
3. **Predict.** After `docker run hello-world`, will `docker ps` show a running container? Why or why not?
4. **Map the analogy.** Fill in: recipe = _____, cooked meal = _____, supermarket = _____.
5. **(After install)** Run `docker run hello-world`. Copy the first two paragraphs of output into your notes and explain what each paragraph is telling you.
6. **(After install)** Run `docker run --rm python:3.12 python --version`. Confirm the printed version starts with `3.12`.

---

## Quick Review

- Docker packages apps with their dependencies as **images**.
- A **container** is a running (or stopped) instance of an image.
- Containers fix "works on my machine" by shipping the environment, not just the source code.
- `docker run hello-world` is the standard first proof that Docker works.
- Docker is not a VM, not a cloud, and not a language.

---

## Summary

Docker is a practical way to make software environments portable and reproducible. An image is a template; a container is an instance of that template. The rest of Part 1 teaches you the architecture behind those two words, how to install the engine, and how to run and manage containers with the CLI.

You are not expected to build custom images yet. First, understand and use existing ones.

---

[Course Home](../README.md)
[Next Lesson →](02-containers-vs-virtual-machines.md)
