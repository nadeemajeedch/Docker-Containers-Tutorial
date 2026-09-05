# Lesson 2: Containers vs Virtual Machines

Lesson 1 introduced containers as isolated processes that share the host kernel. This lesson compares that model with virtual machines so you can choose the right tool and avoid a common misconception: "Docker is a lightweight VM."

[← Previous Lesson](01-introduction-to-docker.md)
[Course Home](../README.md)
[Next Lesson →](03-docker-architecture.md)

---

## Learning Objectives

After this lesson you will be able to:

- Explain how a virtual machine isolates software versus how a container isolates software.
- State what a **kernel** is and why kernel sharing matters.
- Compare startup time, disk size, density, and isolation strength.
- Decide when a VM is still the better choice.
- Avoid describing Docker as "a virtual machine for apps."

---

## Prerequisites

- Lesson 1: image vs container, the "works on my machine" problem.
- No Docker installation required.

---

## Concept

### What a virtual machine is

A **virtual machine (VM)** emulates a complete computer. A **hypervisor** (VirtualBox, VMware, Hyper-V, KVM) sits on the physical machine and creates virtual CPUs, virtual disks, and virtual NICs. Inside each VM you install a **guest operating system** with its own kernel.

```text
Physical machine
└── Hypervisor
    ├── VM 1: Guest OS kernel + apps
    ├── VM 2: Guest OS kernel + apps
    └── VM 3: Guest OS kernel + apps
```

Each VM believes it is a real computer. Isolation is strong: a crash inside VM 1 does not take down the host kernel, and you can run Windows VMs next to Linux VMs.

The cost is duplication. Every VM carries a full operating system: kernel, init system, drivers, packages. A "small" VM image is often several gigabytes. Booting means booting an OS: tens of seconds is common.

### What a container is

A **container** does not emulate hardware and does not boot a guest kernel. It is a set of isolated processes on the **host** operating system. Isolation comes from Linux (and equivalent Windows) kernel features:

- **Namespaces** — what the process can *see* (process list, network, mounts, hostname, users).
- **cgroups** (control groups) — what the process can *use* (CPU, memory, I/O limits).
- **A root filesystem from the image** — the files the process believes are "the computer," layered on disk (Lesson 6).

```text
Physical machine
└── Host OS kernel
    ├── Container A: app + its files  (no guest kernel)
    ├── Container B: app + its files
    └── Container C: app + its files
```

All containers on a Linux host share **that Linux kernel**. That is why a Linux container runs on Linux (or on a tiny Linux VM that Docker Desktop starts for you on Windows and macOS — more in Lessons 3 and 4).

### Side-by-side

| | Virtual machine | Container |
|---|-----------------|-----------|
| Isolates | A full computer | Processes and their filesystem |
| Guest kernel | Yes, one per VM | No; shares host kernel |
| Typical size | Gigabytes | Megabytes to hundreds of MB |
| Startup | Seconds to minutes | Milliseconds to a few seconds |
| Density | Few VMs per laptop | Many containers per laptop |
| OS mix | Windows VM on Linux host, etc. | Must match kernel family (Linux containers need a Linux kernel) |
| Isolation strength | Very strong (hardware virtualization) | Strong for apps; weaker than a VM against a kernel exploit |
| Mental model | Another computer | A boxed-in process |

### Docker Desktop blurs the picture on Windows and macOS

On Windows and macOS, Docker Desktop runs a **lightweight Linux VM** in the background, then runs **Linux containers inside that VM**. You still use the `docker` CLI on the host. The VM is an implementation detail so that Linux containers have a Linux kernel.

That does **not** make each container a VM. You have one small VM (the Docker Desktop Linux engine) and many containers inside it.

Windows also supports **Windows containers** (sharing the Windows kernel). This course uses **Linux containers**, which is the default and what you need for Python and Jupyter in Part 2.

### Hypervisors vs container engines

- Hypervisor: VirtualBox, Hyper-V, KVM, ESXi.
- Container engine: Docker Engine, containerd, Podman, CRI-O.

They can coexist. Many cloud VMs *run* Docker Engine inside them. Containers did not replace VMs in the datacenter; they layered on top.

---

## Why It Matters

If you treat Docker like VirtualBox, you will:

- Expect a desktop and a boot screen (there is none).
- Wonder why a container "has no kernel of its own."
- Over-provision RAM "because VMs need 4 GB each."
- Be surprised that 20 containers start in a few seconds.

If you treat Docker like a package manager only, you will:

- Forget that processes are isolated (networking, files, users).
- Be surprised that killing the Docker daemon stops your containers.

The accurate model: **a container is an isolated process with its own files, not a tiny computer.**

Density matters in class. One laptop can run a web app, a database, and a cache as three containers using far less RAM than three VMs.

---

## Commands/Syntax

These commands do not compare VMs and containers by themselves, but they make the "process, not a machine" idea concrete.

A container that prints one line and exits is clearly not "booting an OS":

```bash
docker run --rm python:3.12 python --version
```

Start a container, then look at it as a process from Docker's point of view:

```bash
docker run -dit --name vm-compare python:3.12 bash
docker ps
docker inspect vm-compare
```

| Command | What it shows about the model |
|---------|--------------------------------|
| `docker run --rm python:3.12 python --version` | No OS boot; the process starts, prints, exits |
| `docker ps` | A list of processes Docker manages, not a list of VMs |
| `docker inspect` | JSON including `Pid` on the host, mounts, networks — process metadata |

Stop and remove when finished (Lesson 7 covers these fully):

```bash
docker stop vm-compare
docker rm vm-compare
```

**PowerShell vs Linux/macOS:** these commands are the same.

If you also use VirtualBox, do not confuse `VBoxManage list runningvms` with `docker ps`. They list different kinds of objects.

---

## Beginner Example

You need to try nginx (a web server) for 30 seconds.

**VM approach:** download a Linux ISO, create a VM, allocate 2 GB RAM, boot, install nginx, configure, browse, then shut down. Time: 15–45 minutes the first time.

**Container approach:**

```bash
docker run --rm -p 8080:80 nginx:alpine
```

In a few seconds, nginx is serving on port 8080. `--rm` deletes the container when you stop it (Ctrl+C). No guest OS install.

You did not "install Linux." You started a process whose filesystem *looks like* a small Linux userland, sharing your (or Docker Desktop's) kernel.

---

## Intermediate Example

Resource comparison for a typical student laptop (illustrative numbers):

| Workload | Three Ubuntu VMs | Three containers (app, db, cache) |
|----------|------------------|-----------------------------------|
| Disk | ~10–30 GB | ~0.5–2 GB of images, shared layers |
| RAM | 2 GB x 3 = 6 GB plus host | Hundreds of MB plus host |
| Boot | Minutes | Seconds |
| Host leftover after shutdown | Virtual disks remain | Images remain; containers can be removed |

Image **layers** (Lesson 6) mean ten Python containers from `python:3.12` do not store ten copies of Python. VMs usually store ten copies of the guest OS unless you use advanced linked clones.

---

## Advanced Example

**Isolation is not equal.**

If an attacker escapes a container, they may reach the **shared kernel**. Kernel exploits are rare compared to application bugs, but they exist. A VM escape has to break the hypervisor as well.

Practical guidance:

- For untrusted binary code you did not write and cannot audit, a VM (or a dedicated machine) is the more conservative sandbox.
- For your own homework, class servers, and typical microservices, containers are the standard and appropriate isolation level.
- Do not run containers with unnecessary `--privileged` flags (you will not need that flag in Part 1).

Docker is not a security boundary as strong as a VM. It is an **application packaging and isolation** tool with meaningful, but not absolute, isolation.

---

## Practical Example

Decision checklist:

**Choose a container when:**

- You want the same app environment on every laptop.
- Startup should be seconds, not minutes.
- You will run several services on one machine.
- The app targets Linux (or you use Docker Desktop's Linux engine).

**Choose a VM when:**

- You need a different kernel or OS (Windows app on a Linux host without Windows containers).
- You need a full desktop OS for a course (a GUI Ubuntu VM).
- You must isolate untrusted code as strongly as possible.
- The software vendor ships a VM appliance, not an image.

**You will often use both:** a cloud VM (the computer) running Docker Engine (the container runtime).

---

## Common Mistakes

1. **"Docker is a lightweight VM."** Repeat: isolated process plus filesystem, shared kernel.
2. **Allocating VM-sized RAM to every container.** Containers share the host. Start without limits; add limits later if needed.
3. **Expecting Windows Explorer inside a Linux container.** There is no Windows desktop in `python:3.12`.
4. **Thinking macOS Docker runs macOS containers.** Docker Desktop on Mac runs **Linux** containers inside a Linux VM.
5. **Using VirtualBox and Docker Desktop Hyper-V/WSL2 in conflicting ways on old Windows setups.** Modern Docker Desktop + WSL 2 is the path this course recommends (Lesson 4).

---

## Best Practices

- Use containers for applications and services.
- Use VMs (or physical machines) for kernels, desktops, and strong multi-tenant isolation.
- On Windows/Mac, treat the Desktop Linux VM as plumbing, not as "your container."
- Measure: `docker stats` (Lesson 7) shows live CPU and memory per container — typical of processes, not of full OS boots.
- When writing reports, say "container" and "image," not "Docker VM," unless you mean the Desktop helper VM.

---

## Exercises

1. **Sketch.** Draw the two diagrams from this lesson (hypervisor + VMs vs host kernel + containers) from memory.
2. **Explain.** In four sentences, tell a classmate who only knows VirtualBox what a container is *not*.
3. **Predict size.** Why can `hello-world` be a few kilobytes while a Ubuntu VM is gigabytes?
4. **Kernel.** Why can you not run a Linux container on a Windows machine *without* WSL 2 or a helper Linux VM?
5. **Choose.** For each scenario, pick VM, container, or either, and justify in one sentence:
   - Running PostgreSQL for a class project on your laptop
   - Testing a kernel module
   - Shipping a Python grader that 200 students must run identically
   - Running a Windows-only GUI application on a Mac
6. **(After install)** Run `docker run --rm python:3.12 python -c "import os; print(os.getpid())"`. Note that you get a PID from *inside* the container's namespace. Then run `docker run -dit --name pid-demo python:3.12 bash` and `docker inspect --format "{{.State.Pid}}" pid-demo` to see the host PID. Remove with `docker rm -f pid-demo`. You do not need to understand namespaces fully yet — just notice there are two PID views.

---

## Quick Review

- VMs virtualize hardware and boot a guest kernel.
- Containers isolate processes and share the host kernel.
- Containers start faster, use less disk, and pack denser; VMs isolate more strongly and can run different kernels.
- Docker Desktop uses one Linux VM so Linux containers can run on Windows and macOS.
- Docker is not "a VM for each app."

---

## Summary

Virtual machines and containers both isolate software, but at different layers. VMs emulate computers. Containers box in processes. Docker's speed and density come from sharing the kernel. Use that model in every later lesson when you see a container start in under a second.

---

[← Previous Lesson](01-introduction-to-docker.md)
[Course Home](../README.md)
[Next Lesson →](03-docker-architecture.md)
