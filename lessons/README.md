# Lessons

Start here if you are new: [01 — Introduction to Docker](01-introduction-to-docker.md)

[Course Home](../README.md)

---

## Part 1 — Foundations (Beginner)

1. [Introduction to Docker](01-introduction-to-docker.md) — Docker, containers, reproducibility, "works on my machine"
2. [Containers vs Virtual Machines](02-containers-vs-virtual-machines.md) — isolation, kernels, density, when to use each
3. [Docker Architecture](03-docker-architecture.md) — CLI, daemon, Engine, Desktop, registries
4. [Installing Docker](04-installing-docker.md) — install, verify, Hello World
5. [Docker CLI](05-docker-cli.md) — command structure, help, version, info, disk usage
6. [Docker Images](06-docker-images.md) — layers, tags, pull, list, remove
7. [Docker Containers](07-docker-containers.md) — lifecycle, run, logs, exec, inspect, copy, cleanup
8. [Docker Hub](08-docker-hub.md) — registries, official images, tags, search

```text
Concepts (1-3) --> Install (4) --> CLI (5) --> Images (6) --> Containers (7) --> Hub (8)
```

---

## Part 2 — Python, Dockerfiles, Volumes, Jupyter (Beginner to Intermediate)

9. [Running Python with Docker](09-running-python-with-docker.md) — REPL, scripts, bind-mount `hello.py`
10. [Dockerfiles](10-dockerfile.md) — FROM, WORKDIR, COPY, RUN, CMD, and related instructions
11. [Building Python images](11-building-python-images.md) — `docker build`, tags, cache, `my-python-app`
12. [Python dependencies](12-python-dependencies.md) — pip, requirements.txt, pinning
13. [.dockerignore](13-dockerignore.md) — build context, secrets, venvs
14. [Volumes and bind mounts](14-volumes-and-bind-mounts.md) — `-v`, `--mount`, named volumes
15. [Running Jupyter with Docker](15-running-jupyter-with-docker.md) — port 8888, token, persistence
16. [Custom Jupyter image](16-custom-jupyter-image.md) — JupyterLab plus the scientific stack
17. [Jupyter project lab](17-jupyter-project.md) — capstone workspace

```text
Python (9) --> Dockerfile (10-13) --> Mounts (14) --> Jupyter (15-17)
```

---

## Part 3 — Compose, Networking, DS/ML, Advanced, Final Project

18. [Docker Compose](18-docker-compose.md) — `compose.yaml`, up/down/ps/logs/exec
19. [Python and Jupyter with Compose](19-python-jupyter-compose.md) — class Jupyter via Compose
20. [Environment variables](20-environment-variables.md) — `-e`, `--env-file`, `.env`, secrets
21. [Docker networking](21-docker-networking.md) — bridges, ports, service DNS, localhost
22. [Docker for data science](22-docker-for-data-science.md) — cloneable Jupyter + data + results
23. [Docker for machine learning](23-docker-for-machine-learning.md) — CPU train/predict, optional GPU note
24. [Debugging](24-debugging.md) — problem, cause, diagnosis, solution
25. [Best practices](25-best-practices.md) — pins, cache, dockerignore, non-root
26. [Security](26-security.md) — least privilege, secrets, ports, no privileged
27. [Advanced Docker](27-advanced-docker.md) — optional: BuildKit, healthchecks, limits
28. [Image optimization](28-image-optimization.md) — slim bases, history, optional multi-stage
29. [Docker and GitHub](29-docker-and-github.md) — clone-and-compose workflow
30. [Reproducible academic projects](30-reproducible-academic-projects.md) — assignment and research layout
31. [Final project](31-final-project.md) — reproducible DS environment capstone

```text
Compose (18-20) --> Networks (21) --> DS/ML (22-23) --> Debug/practice/security (24-26)
--> Advanced/optimize (27-28) --> GitHub/academic (29-30) --> Final (31)
```

Examples: [examples/](../examples/README.md)

---

## Reference

- [Part 1 CLI cheatsheet](../cheatsheet.md)
- [Python in Docker](../cheatsheet/python-docker.md)
- [Dockerfiles](../cheatsheet/dockerfile.md)
- [Jupyter in Docker](../cheatsheet/jupyter-docker.md)
- [Docker Compose](../cheatsheet/docker-compose.md)
- [Networking](../cheatsheet/networking.md)
- [Troubleshooting](../cheatsheet/troubleshooting.md)
- [Best practices](../cheatsheet/best-practices.md)
- [Complete cheatsheet](../cheatsheet/complete-docker-cheatsheet.md)
- [Part 2 preview](part-2-preview.md)
