# Lesson 15: Running Jupyter with Docker

You can run JupyterLab without installing Python or Jupyter on the host. This lesson uses a maintained official Jupyter image, publishes port 8888, bind-mounts your work folder, and explains tokens, browsers, and how to stop cleanly.

[← Previous Lesson](14-volumes-and-bind-mounts.md)
[Course Home](../README.md)
[Next Lesson →](16-custom-jupyter-image.md)

---

## Learning Objectives

After this lesson you will be able to:

- Run JupyterLab from the official `quay.io/jupyter/base-notebook` image (or the equivalent Docker Hub name your docs show).
- Map host port 8888 to container port 8888.
- Bind-mount a host directory so notebooks persist.
- Find the Jupyter URL and token in `docker logs`.
- Stop and start a Jupyter container without losing notebooks.
- Write the command for bash/zsh and for PowerShell.

---

## Prerequisites

- Lessons 7, 9, and 14 (`-p`, `-v`, `--rm`, logs).
- A free host port **8888** (if something else uses 8888, you will map another host port).
- A browser on the host.

---

## Concept

JupyterLab is a web application. Inside the container it listens on **port 8888**. Your browser runs on the **host**. Docker publishes the port:

```text
browser  →  localhost:8888  →  (publish)  →  container:8888  →  JupyterLab
```

Without `-p`, Jupyter is only reachable from inside the container network, not from your browser.

Notebooks are files. If they exist only in the container, `--rm` or `docker rm` deletes them. Bind-mount a host folder at the Jupyter working directory.

Official Jupyter Docker Stacks use user **`jovyan`** and default work directory **`/home/jovyan/work`**.

This lesson uses the maintained image:

```text
quay.io/jupyter/base-notebook:python-3.12
```

Jupyter Docker Stacks moved publishing toward [Quay.io](https://quay.io/repository/jupyter/base-notebook). The image includes Python and JupyterLab. It does **not** include pandas or scikit-learn. Lesson 16 adds those in a custom image. You can still create notebooks and run standard-library Python now.

If a pull from Quay fails on a restricted network, the same family is often available as `jupyter/base-notebook` on Docker Hub. Prefer a **tagged** image (`python-3.12`), not untagged `latest`, when both exist.

---

## Explanation

### Host vs container ports

```bash
docker run -p 8888:8888 ...
```

| Field | Meaning |
|-------|---------|
| Left `8888` | Port on **your computer** (browser uses this) |
| Right `8888` | Port **inside the container** (Jupyter's default) |

If host 8888 is busy:

```bash
docker run -p 8889:8888 ...
```

Then browse `http://localhost:8889`. The container still uses 8888.

`EXPOSE 8888` in a Dockerfile does not publish. `-p` does.

### Token

Jupyter generates a **token** so random visitors on `localhost` cannot use your session. Official images print a URL like:

```text
http://127.0.0.1:8888/lab?token=abc123...
```

in the container logs. Use that URL, or paste the token into the Jupyter login form.

**Do not** put Jupyter on a public network with an empty token. Empty tokens appear in Lesson 16 for **local class machines only**.

### Persistence

```text
-v "$PWD":/home/jovyan/work
```

Files you save in JupyterLab under `work` appear in the host directory you mounted. Create an empty folder for the lab **before** the first run so you know where they go.

### User and permissions

`jovyan` has uid 1000 on many images. If bind-mounted files on Linux end up owned by root or unreadable, Lesson 16's custom image and Docker Desktop on Win/Mac are usually smoother. On Linux you can pass `-e NB_UID=$(id -u)` with Jupyter Stacks when needed (see image docs). Part 2 default: Docker Desktop, mount a folder you own.

### Stopping

Ctrl+C in the attached terminal stops a foreground container. Named + detached:

```bash
docker stop jupyter-lab
docker start jupyter-lab
```

Notebooks on the bind mount survive. The **token** may be in logs from the first start; `docker logs jupyter-lab` still shows it.

---

## Commands/Syntax

Create a work folder, then run.

**Linux / macOS:**

```bash
mkdir -p "$HOME/jupyter-docker-work"
docker pull quay.io/jupyter/base-notebook:python-3.12
docker run --rm -p 8888:8888 \
  -v "$HOME/jupyter-docker-work":/home/jovyan/work \
  --name jupyter-lab \
  quay.io/jupyter/base-notebook:python-3.12
```

**Windows PowerShell:**

```powershell
New-Item -ItemType Directory -Force -Path "$HOME\jupyter-docker-work"
docker pull quay.io/jupyter/base-notebook:python-3.12
docker run --rm -p 8888:8888 `
  -v "${HOME}\jupyter-docker-work:/home/jovyan/work" `
  --name jupyter-lab `
  quay.io/jupyter/base-notebook:python-3.12
```

Line continuation: bash uses `\`. PowerShell uses `` ` ``. Single-line form (both):

```bash
docker run --rm -p 8888:8888 -v "$HOME/jupyter-docker-work":/home/jovyan/work --name jupyter-lab quay.io/jupyter/base-notebook:python-3.12
```

```powershell
docker run --rm -p 8888:8888 -v "${HOME}\jupyter-docker-work:/home/jovyan/work" --name jupyter-lab quay.io/jupyter/base-notebook:python-3.12
```

Read the URL:

```bash
docker logs jupyter-lab
```

If you used `--rm` in the foreground, the logs are already in that terminal. Look for `token=`.

Open `http://localhost:8888` and paste the token if the query string URL does not auto-login.

Detached (prompt returns; container stays up):

```bash
docker run -d -p 8888:8888 -v "$HOME/jupyter-docker-work":/home/jovyan/work --name jupyter-lab quay.io/jupyter/base-notebook:python-3.12
docker logs jupyter-lab
```

Stop:

```bash
docker stop jupyter-lab
```

If you did not use `--rm`, remove later with `docker rm jupyter-lab`. With `--rm`, stop deletes the container; the bind-mounted folder remains.

---

## Beginner Example

Foreground run, watch logs, open the browser, create `Untitled.ipynb`, save, Ctrl+C.

On the host, list the work folder. The notebook should be there.

**PowerShell:** `Get-ChildItem $HOME\jupyter-docker-work`

**bash:** `ls "$HOME/jupyter-docker-work"`

If the folder is empty, you saved outside `work` in the Jupyter file browser, or the mount path was wrong. In JupyterLab, stay under the `work` directory that reflects the mount.

---

## Intermediate Example

Named container without `--rm` so you can stop and start:

**Linux / macOS:**

```bash
docker run -d -p 8888:8888 \
  -v "$HOME/jupyter-docker-work":/home/jovyan/work \
  --name jupyter-lab \
  quay.io/jupyter/base-notebook:python-3.12
docker logs jupyter-lab
```

Use Jupyter. Then:

```bash
docker stop jupyter-lab
docker start jupyter-lab
docker logs jupyter-lab
```

Browse again. The same notebooks should load from the mount.

If `The container name "/jupyter-lab" is already in use`, either `docker start jupyter-lab` or `docker rm -f jupyter-lab` and run again.

---

## Advanced Example

### Different host port

```bash
docker run --rm -p 8889:8888 -v "$HOME/jupyter-docker-work":/home/jovyan/work quay.io/jupyter/base-notebook:python-3.12
```

Copy the URL from logs but **change the port to 8889** if the log still says 8888 (the process inside does not know your host mapping). `http://localhost:8889/?token=...`

### `--mount` form

```bash
docker run --rm -p 8888:8888 \
  --mount type=bind,source="$HOME/jupyter-docker-work",target=/home/jovyan/work \
  quay.io/jupyter/base-notebook:python-3.12
```

PowerShell:

```powershell
docker run --rm -p 8888:8888 --mount "type=bind,source=${HOME}\jupyter-docker-work,target=/home/jovyan/work" quay.io/jupyter/base-notebook:python-3.12
```

### Token in the terminal vs empty token

Official stacks require a token by default. That is the correct default. Lesson 16's sample sets an empty token for **offline local labs** only, so students are not blocked by a token on a single-user laptop. Do not copy empty-token settings onto a shared server.

---

## Practical Example

Minimal mental checklist before every Jupyter session:

```text
1. Work folder exists on the host
2. docker run -p 8888:8888 -v <folder>:/home/jovyan/work <image>
3. Copy URL + token from logs
4. Browser: localhost and the HOST port
5. Save notebooks under work/
6. docker stop (or Ctrl+C)
7. Confirm .ipynb files on the host
```

You still have no pandas in this base image. `import pandas` will fail. That is expected. Lesson 16 installs the scientific stack.

---

## Common Mistakes

1. **Forgetting `-p`.** Browser: connection refused.
2. **Using container port in the browser after mapping 8889:8888.** Use **8889**.
3. **No bind mount.** Notebooks vanish with the container.
4. **Mounting the wrong directory** (home instead of the small work folder).
5. **Copying a `127.0.0.1` URL from logs that shows port 8888** while you published 8889.
6. **PowerShell backslash continuation** mixed with bash `\`.
7. **Port already allocated.** `docker ps` and stop the old Jupyter, or pick another host port.
8. **Installing Jupyter on the host "to make Docker work."** Not required.

---

## Best Practices

- One dedicated host folder per course.
- Always `-p` and always a bind mount for class Jupyter.
- Prefer image tags that include a Python version.
- Treat tokens like passwords in screenshots you submit.
- Stop containers when you finish so port 8888 is free.
- Use `docker logs` before assuming Jupyter is broken.

---

## Exercises

1. **Pull.** `docker pull quay.io/jupyter/base-notebook:python-3.12` (or the Hub equivalent if your instructor specifies it).
2. **Run.** Start Jupyter with `-p 8888:8888` and a bind mount to an empty work folder.
3. **Token.** Copy the login URL from the terminal or `docker logs`.
4. **Notebook.** Create a notebook, `print("hello jupyter in docker")`, save.
5. **Persist.** Stop the container. Confirm the `.ipynb` is on the host. Start again (or `docker run` again with the same mount) and reopen the notebook.
6. **Port.** Run with `-p 8889:8888` and open `localhost:8889`.
7. **Import.** `import pandas` in a cell. Record the error. You will fix it by building a custom image next.

---

## Quick Review

- JupyterLab is a server on container port 8888; `-p` exposes it to the browser.
- Bind-mount `/home/jovyan/work` so notebooks persist.
- Tokens come from logs; host port is the left side of `-p`.
- Base notebook image is enough to learn the workflow; scientific libraries come in Lesson 16.

---

## Summary

You ran JupyterLab in Docker, reached it in a browser, and saved notebooks on the host. Next you will build a **custom** image that already contains JupyterLab, NumPy, Pandas, Matplotlib, and scikit-learn.

---

[← Previous Lesson](14-volumes-and-bind-mounts.md)
[Course Home](../README.md)
[Next Lesson →](16-custom-jupyter-image.md)
