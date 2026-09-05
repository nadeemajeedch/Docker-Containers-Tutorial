# Docker and Containers Tutorial

A complete beginner-to-expert course on Docker and containers.

**Part 1** teaches you what Docker is, why containers exist, how the engine works, and how to run and manage containers from the command line.

**Part 2** teaches you to run Python in Docker, write Dockerfiles, install dependencies, persist files with volumes, and run JupyterLab without a local Python install.

**Part 3** teaches Docker Compose, networking, data science and machine learning environments, troubleshooting, security, image optimization, GitHub workflows, academic reproducibility, and a final project.

This course is written for university students and self-learners. Every lesson starts from first principles, then builds to practical commands you will use every day.

---

## Description

"It works on my machine" is one of the most expensive sentences in software.

Docker packages an application together with its runtime, libraries, and files into a **container image**. Anyone with Docker can run that image and get the same behavior: on a laptop, in a lab, or on a server.

Part 1 answers:

- What is Docker, and what problem does it solve?
- How is a container different from a virtual machine?
- What are the Docker Engine, CLI, daemon, and Docker Desktop?
- How do you install Docker and prove that it works?
- How do you pull images, run containers, and clean up afterward?
- What is Docker Hub, and how do tags and official images work?

Part 1 does not use Dockerfiles or Compose. First you become fluent with images, containers, and the CLI. Part 2 adds Dockerfiles, pip dependencies, mounts, and Jupyter. Part 3 adds Compose, networking, DS/ML stacks, and a GitHub capstone.

---

## Learning Objectives

By the end of Part 1 you will be able to:

1. Explain Docker, containerization, and reproducibility in plain language.
2. Compare containers with virtual machines and choose the right tool.
3. Describe Docker architecture: client, daemon, images, containers, and registries.
4. Install Docker Desktop or Docker Engine and verify the installation.
5. Use the Docker CLI, including `--help`, `version`, and `info`.
6. Pull, list, tag-identify, and remove images.
7. Create, start, stop, inspect, and remove containers.
8. View logs, copy files, rename containers, and run commands inside a running container.
9. Find and pull images from Docker Hub with an understanding of tags and official images.
10. Clean unused data with `docker system df` and `docker system prune`.

By the end of Part 2 you will be able to:

1. Run the official `python:3.12` interpreter interactively and as one-shot commands.
2. Run a host `hello.py` inside a container with a bind mount.
3. Read and write a Dockerfile (`FROM`, `WORKDIR`, `COPY`, `RUN`, `CMD`, and related instructions).
4. Build and tag a custom Python image (`docker build -t my-python-app .`).
5. Install pinned pip dependencies from `requirements.txt` during the build.
6. Use `.dockerignore` so venvs, `.git`, and secrets stay out of the image.
7. Persist work with bind mounts and named volumes (`-v` and `--mount`).
8. Run JupyterLab in Docker on port 8888 with notebooks saved on the host.
9. Build a custom Jupyter image with NumPy, Pandas, Matplotlib, and scikit-learn.

By the end of Part 3 you will be able to:

1. Describe multi-container apps in `compose.yaml` and use `docker compose up/down/ps/logs/exec`.
2. Pass configuration with `-e`, `--env-file`, and Compose `.env` without committing secrets.
3. Explain bridge networks, published ports, and why `localhost` inside a container is not the host.
4. Reproduce a data-science environment from Git with Jupyter, data mounts, and results mounts.
5. Train a small CPU ML model in Compose and persist the artifact (GPU optional, not required).
6. Diagnose common Docker failures with a logs-first playbook.
7. Apply image, security, and GitHub hygiene checklists.
8. Complete the final project so a classmate can clone and `docker compose up --build`.

---

## Prerequisites

- A computer you can install software on (Windows 10/11, macOS, or Linux).
- Administrator or sudo access for installation.
- Comfort using a terminal:
  - **Windows:** PowerShell or Windows Terminal
  - **macOS / Linux:** Terminal (bash or zsh)
- Curiosity. No prior Docker, Linux sysadmin, or cloud experience is required.

Optional but helpful:

- Basic familiarity with files and folders
- A free [Docker Hub](https://hub.docker.com/) account (needed later for publishing; not required to pull public images)

---

## Beginner Roadmap

```text
BEGINNER
↓
Docker Fundamentals          Lessons 1-8
↓
Python + Docker              Lesson 9
↓
Dockerfiles                  Lessons 10-13
↓
Volumes                      Lesson 14
↓
Jupyter                      Lessons 15-17
↓
INTERMEDIATE
↓
Docker Compose               Lessons 18-19
↓
Environment variables        Lesson 20
↓
Networking                   Lesson 21
↓
Data Science                 Lesson 22
↓
Machine Learning             Lesson 23
↓
ADVANCED
↓
Debugging / best practices   Lessons 24-25
↓
Security                     Lesson 26
↓
Optimization / advanced      Lessons 27-28
↓
GitHub + Reproducibility     Lessons 29-30
↓
FINAL PROJECT                Lesson 31
```

Study path:

1. Read the concept, then type every command yourself. Do not only read them.
2. Complete the exercises at the end of each lesson before moving on.
3. Keep a personal command log. Writing commands by hand is part of learning.
4. When something fails, read the error. Docker error messages are usually specific.
5. Finish Part 1 before Part 2, and Part 2 before Part 3. Compose and Jupyter assume you can already build images and use mounts.

---

## Lesson Navigation

| # | Lesson | What you will learn |
|---|--------|---------------------|
| 1 | [Introduction to Docker](lessons/01-introduction-to-docker.md) | What Docker is, why containers exist, reproducibility |
| 2 | [Containers vs Virtual Machines](lessons/02-containers-vs-virtual-machines.md) | Isolation models, kernel sharing, when to use each |
| 3 | [Docker Architecture](lessons/03-docker-architecture.md) | CLI, daemon, Engine, Desktop, images, containers, registries |
| 4 | [Installing Docker](lessons/04-installing-docker.md) | Desktop vs Engine, install, verify, Hello World |
| 5 | [Docker CLI](lessons/05-docker-cli.md) | Command structure, help, version, info, system commands |
| 6 | [Docker Images](lessons/06-docker-images.md) | Layers, tags, pull, list, remove images |
| 7 | [Docker Containers](lessons/07-docker-containers.md) | Lifecycle, run, start, stop, logs, exec, inspect, cp |
| 8 | [Docker Hub](lessons/08-docker-hub.md) | Registries, official images, tags, search, pull |
| 9 | [Running Python with Docker](lessons/09-running-python-with-docker.md) | REPL, one-shot commands, bind-mount scripts |
| 10 | [Dockerfiles](lessons/10-dockerfile.md) | FROM, WORKDIR, COPY, RUN, CMD, and related instructions |
| 11 | [Building Python images](lessons/11-building-python-images.md) | `docker build`, tags, layer cache |
| 12 | [Python dependencies](lessons/12-python-dependencies.md) | pip, requirements.txt, pinning |
| 13 | [.dockerignore](lessons/13-dockerignore.md) | Build context, secrets, venvs |
| 14 | [Volumes and bind mounts](lessons/14-volumes-and-bind-mounts.md) | `-v`, `--mount`, named volumes |
| 15 | [Running Jupyter with Docker](lessons/15-running-jupyter-with-docker.md) | Port 8888, token, notebook persistence |
| 16 | [Custom Jupyter image](lessons/16-custom-jupyter-image.md) | JupyterLab plus the scientific stack |
| 17 | [Jupyter project lab](lessons/17-jupyter-project.md) | Capstone workspace |
| 18 | [Docker Compose](lessons/18-docker-compose.md) | `compose.yaml`, up, down, logs, exec |
| 19 | [Python and Jupyter with Compose](lessons/19-python-jupyter-compose.md) | Class Jupyter via Compose |
| 20 | [Environment variables](lessons/20-environment-variables.md) | `-e`, `--env-file`, `.env`, secrets |
| 21 | [Docker networking](lessons/21-docker-networking.md) | Bridge, ports, service DNS, localhost |
| 22 | [Docker for data science](lessons/22-docker-for-data-science.md) | Cloneable Jupyter + data + results |
| 23 | [Docker for machine learning](lessons/23-docker-for-machine-learning.md) | CPU train/predict; GPU optional |
| 24 | [Debugging](lessons/24-debugging.md) | Problem → cause → diagnosis → solution |
| 25 | [Best practices](lessons/25-best-practices.md) | Pins, cache, dockerignore, non-root |
| 26 | [Security](lessons/26-security.md) | Least privilege, secrets, ports |
| 27 | [Advanced Docker](lessons/27-advanced-docker.md) | Optional BuildKit, healthchecks, limits |
| 28 | [Image optimization](lessons/28-image-optimization.md) | Slim bases, history, optional multi-stage |
| 29 | [Docker and GitHub](lessons/29-docker-and-github.md) | Clone-and-compose workflow |
| 30 | [Reproducible academic projects](lessons/30-reproducible-academic-projects.md) | Assignment and research layout |
| 31 | [Final project](lessons/31-final-project.md) | Reproducible DS environment |

Extra:

- [Lesson index](lessons/README.md)
- [Part 1 CLI cheatsheet](cheatsheet.md)
- [Python in Docker](cheatsheet/python-docker.md)
- [Dockerfiles](cheatsheet/dockerfile.md)
- [Jupyter in Docker](cheatsheet/jupyter-docker.md)
- [Docker Compose](cheatsheet/docker-compose.md)
- [Networking](cheatsheet/networking.md)
- [Troubleshooting](cheatsheet/troubleshooting.md)
- [Best practices](cheatsheet/best-practices.md)
- [Complete cheatsheet](cheatsheet/complete-docker-cheatsheet.md)
- [Examples](examples/README.md)
- [Part 2 preview](lessons/part-2-preview.md)

---

## Quick Start

After Docker is installed (Lesson 4):

**Linux / macOS (bash or zsh):**

```bash
docker version
docker run hello-world
docker pull python:3.12
docker run --rm python:3.12 python --version
```

**Windows PowerShell:**

```powershell
docker version
docker run hello-world
docker pull python:3.12
docker run --rm python:3.12 python --version
```

Those four commands are the same on all platforms. Differences appear later with file paths, line continuation, and volume mounts. Lessons call out PowerShell vs Linux/macOS whenever the syntax diverges.

Expected: `hello-world` prints a success message, and the Python container prints a 3.12.x version string, then exits.

---

## Exercises

Work through these in order. Full instructions live in the lessons.

| Exercise | Lesson | Skill |
|----------|--------|--------|
| Install Docker and run `docker version` | 4 | Installation |
| Run `docker run hello-world` and explain the output | 1, 4 | First container |
| Pull `python:3.12` and list images | 6, 8 | Images |
| Run `python:3.12` with `--rm` and print the version | 6, 7 | Ephemeral containers |
| Start an interactive Python container with `-it` | 7 | Interactive mode |
| Create a named container, stop it, start it, inspect it | 7 | Lifecycle |
| View logs and run `docker exec` inside a running container | 7 | Debug |
| Copy a file out of a container with `docker cp` | 7 | Files |
| Rename a container | 7 | Management |
| Remove stopped containers and unused images | 5, 7 | Cleanup |
| Find an official image on Docker Hub and pull a specific tag | 8 | Registry |
| Run `python:3.12` interactively and with `--rm` | 9 | Python in Docker |
| Bind-mount and run `examples/hello-python/hello.py` | 9, 14 | Host scripts |
| Build `my-python-app` from `examples/python-docker-project` | 10, 11 | Dockerfiles |
| Inspect pip packages in that image | 12 | Dependencies |
| Confirm `.dockerignore` excludes junk from the image | 13 | Build context |
| Persist a file with a bind mount and with a named volume | 14 | Volumes |
| Run JupyterLab on port 8888 with a work folder mount | 15 | Jupyter |
| Build and run `course-jupyter:1.0` | 16, 17 | Custom Jupyter |
| Start Jupyter with `docker compose up` | 18, 19 | Compose |
| Configure a port or name with `.env` | 20 | Environment |
| Fetch a page via Compose service DNS | 21 | Networking |
| Run the data-science example notebook and script | 22 | Data science |
| Train and predict in `examples/ml-docker` | 23 | Machine learning |
| Diagnose a port clash with logs and `ps` | 24 | Debugging |
| Complete the GitHub clone-and-compose checklist | 29 | GitHub |
| Submit the final project | 31 | Capstone |

Part 1 capstone (after Lesson 8):

1. Pull `python:3.12`.
2. Run a container named `py-lab` that stays running (`docker run -dit --name py-lab python:3.12 bash`).
3. Confirm it is running with `docker ps`.
4. Execute `python --version` inside it with `docker exec`.
5. Copy a small file into the container with `docker cp`.
6. Inspect the container and find its image ID.
7. Stop, then remove the container.
8. Run `docker system df` and decide whether you need `docker system prune`.

Part 2 capstone (after Lesson 17):

1. Bind-mount run `examples/hello-python/hello.py`.
2. Build and run `examples/python-docker-project` as `my-python-app`.
3. Build `course-jupyter:1.0` from `examples/jupyter-project`.
4. Run JupyterLab with `notebooks/` mounted and port 8888 published.
5. Run `01-check-stack.ipynb` (numpy, pandas, matplotlib, sklearn).
6. Stop the container and confirm the notebook is still on the host.

Part 3 capstone (Lesson 31):

1. Copy or fork `examples/final-project`.
2. `docker compose up --build` and run the analysis notebook.
3. Produce a figure under `results/` on the host.
4. Push to GitHub without secrets.
5. Clone into a second directory and reproduce.

---

## Part 1 Overview

Part 1 is **foundations**.

| Part 1 | Part 2 |
|--------|--------|
| What containers are | Dockerfiles |
| Docker architecture | `docker build` |
| Installation and CLI | pip and `requirements.txt` |
| Images, containers, Hub | `.dockerignore` |
| Lifecycle and cleanup | Bind mounts and named volumes |
| Official `python:3.12` as a consumer | Custom Python and Jupyter images |

---

## Part 2 Overview

Part 2 is **Python, images you build, persistence, and Jupyter**.

| Topic | Lessons | Example |
|-------|---------|---------|
| Run Python without a host install | 9 | `examples/hello-python` |
| Dockerfile instructions | 10 | `examples/python-docker-project/Dockerfile` |
| Build, tag, cache | 11 | `docker build -t my-python-app .` |
| numpy, pandas, matplotlib, scikit-learn | 12 | `requirements.txt` |
| Filter the build context | 13 | `.dockerignore` |
| Persist files | 14 | `-v` and `--mount` |
| JupyterLab on port 8888 | 15 | `quay.io/jupyter/base-notebook` |
| Custom Jupyter stack | 16–17 | `examples/jupyter-project` |

See [Part 2 preview](lessons/part-2-preview.md) and [examples/](examples/README.md).

---

## Part 3 Overview

Part 3 is **Compose, networking, DS/ML environments, operations, and the final project**.

| Topic | Lessons | Example |
|-------|---------|---------|
| Compose | 18–19 | `examples/compose-jupyter` |
| Environment variables | 20 | `.env.example` in DS/final projects |
| Networking | 21 | `examples/networking-demo` |
| Data science | 22 | `examples/data-science-docker` |
| Machine learning (CPU) | 23 | `examples/ml-docker` |
| Debugging | 24 | [troubleshooting cheatsheet](cheatsheet/troubleshooting.md) |
| Best practices and security | 25–26 | checklists in those lessons |
| Advanced / optimization (optional) | 27–28 | labeled optional in-lesson |
| GitHub and academic layout | 29–30 | `examples/github-template` |
| Final project | 31 | `examples/final-project` |

Not in this course: Kubernetes, production public Jupyter, required GPUs.

---

## How to Use This Repository

1. Clone or download the repository.
2. Start at [Lesson 1](lessons/01-introduction-to-docker.md) or open the [lesson index](lessons/README.md).
3. Keep [the Part 1 cheatsheet](cheatsheet.md) nearby once you reach Lesson 5. Later sheets: [Python](cheatsheet/python-docker.md), [Dockerfile](cheatsheet/dockerfile.md), [Jupyter](cheatsheet/jupyter-docker.md), [Compose](cheatsheet/docker-compose.md), [networking](cheatsheet/networking.md), [troubleshooting](cheatsheet/troubleshooting.md), [best practices](cheatsheet/best-practices.md), [complete](cheatsheet/complete-docker-cheatsheet.md).
4. Type commands in your own terminal. Reading is not a substitute for running them.
5. After Part 1, continue with [Lesson 9](lessons/09-running-python-with-docker.md). After Part 2, continue with [Lesson 18](lessons/18-docker-compose.md).

GitHub renders every `.md` file. GitHub Pages can publish the same files as a course site.

---

## License

This course is released under the MIT License. See `LICENSE`.
