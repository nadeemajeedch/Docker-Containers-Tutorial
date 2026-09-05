# Docker CLI Cheatsheet (Part 1)

Companion to the [course home](README.md). Full explanations live in the lessons. Commands work in **PowerShell**, **bash**, and **zsh** unless a path example says otherwise.

---

## Engine and help

```bash
docker --help
docker version
docker info
docker run --help
```

[Lesson 5](lessons/05-docker-cli.md) · [Lesson 3](lessons/03-docker-architecture.md)

---

## Images

```bash
docker pull python:3.12
docker pull hello-world
docker images
docker image ls
docker rmi hello-world
docker inspect python:3.12
```

[Lesson 6](lessons/06-docker-images.md)

---

## Containers

```bash
docker run hello-world
docker run --rm python:3.12 python --version
docker run -it python:3.12
docker run -dit --name py-lab python:3.12 bash

docker ps
docker ps -a

docker start py-lab
docker stop py-lab
docker restart py-lab
docker rm py-lab
docker rm -f py-lab

docker logs py-lab
docker logs -f py-lab
docker exec py-lab python --version
docker exec -it py-lab bash
docker inspect py-lab
docker rename py-lab python-lab
docker stats
docker stats --no-stream py-lab
```

Copy files (Linux/macOS host paths):

```bash
docker cp py-lab:/tmp/file.txt ./file.txt
docker cp ./file.txt py-lab:/tmp/file.txt
```

Copy files (PowerShell host paths):

```powershell
docker cp py-lab:/tmp/file.txt .\file.txt
docker cp .\file.txt py-lab:/tmp/file.txt
```

[Lesson 7](lessons/07-docker-containers.md)

---

## Hub

```bash
docker search python
docker pull python:3.12
docker login
docker logout
```

[Lesson 8](lessons/08-docker-hub.md)

---

## Disk

```bash
docker system df
docker system prune
```

Do not add `--volumes` in Part 1. Be cautious with `-a`.

[Lesson 5](lessons/05-docker-cli.md)

---

## First-hour script

```bash
docker version
docker run hello-world
docker pull python:3.12
docker run --rm python:3.12 python --version
docker run -it python:3.12
```

[Lesson 4](lessons/04-installing-docker.md)

---

## rm vs rmi

| Command | Deletes |
|---------|---------|
| `docker rm` | Containers |
| `docker rmi` | Images |

---

Part 2:

- [Python in Docker](cheatsheet/python-docker.md)
- [Dockerfiles](cheatsheet/dockerfile.md)
- [Jupyter in Docker](cheatsheet/jupyter-docker.md)

Part 3:

- [Docker Compose](cheatsheet/docker-compose.md)
- [Networking](cheatsheet/networking.md)
- [Troubleshooting](cheatsheet/troubleshooting.md)
- [Best practices](cheatsheet/best-practices.md)
- [Complete cheatsheet](cheatsheet/complete-docker-cheatsheet.md)

[Course Home](README.md)
[Lesson index](lessons/README.md)
