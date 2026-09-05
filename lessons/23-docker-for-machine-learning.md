# Lesson 23: Docker for Machine Learning

ML in this course means: train a small model in a container, write the artifact to a mounted folder, optionally open Jupyter. **GPU is optional and not required.**

[← Previous Lesson](22-docker-for-data-science.md)
[Course Home](../README.md)
[Next Lesson →](24-debugging.md)

---

## Learning Objectives

After this lesson you will be able to:

- Run `examples/ml-docker` training with Compose.
- Persist a `joblib` model on the host via a bind mount.
- Run a predict command against that model.
- Start Jupyter with a Compose **profile**.
- Explain why GPU extra images are optional.

---

## Prerequisites

- Lesson 22.
- No NVIDIA GPU required.

---

## Concept

Training is a **batch job**. Jupyter is an **interactive server**. They can share one image and different Compose services.

```yaml
services:
  train:
    build: .
    command: ["python", "src/train.py"]
  jupyter:
    build: .
    profiles: ["notebook"]
```

`docker compose up train` runs training. Jupyter starts only with `--profile notebook`, so a CI machine can train without publishing 8888.

Data: `data/scores.csv`. Output: `models/score-model.joblib`.

CPU `LinearRegression` is enough to learn the Docker workflow. Deep learning frameworks are large; add them later with extra requirements and, if needed, a CUDA base image.

---

## Explanation

`src/train.py` splits data, fits, prints MAE and R2, dumps the model. `src/predict.py` loads the file.

If you train without the `models/` mount, the joblib file dies with the container. The Compose file mounts `./models`.

GPU (optional, advanced): NVIDIA Container Toolkit, a CUDA image, and Compose device reservations. Skip unless your lab documents it. This example never calls CUDA.

---

## Commands/Syntax

```bash
cd examples/ml-docker
docker compose up --build train
```

Predict:

```bash
docker compose run --rm train python src/predict.py 5 5
```

Jupyter:

```bash
docker compose --profile notebook up --build jupyter
```

**PowerShell:** same commands.

```bash
docker compose down
```

---

## Beginner Example

Run `train`. Confirm MAE/R2 print and `models/score-model.joblib` exists on the host.

---

## Intermediate Example

```bash
docker compose run --rm train python src/predict.py 5 5
```

You should see a predicted score. Change hours, run again — no retrain needed if the model file remains.

---

## Advanced Example

Enable the notebook profile and run `notebooks/01-train.ipynb`. Compare notebook R2 with the script (same `random_state=42` should be close; the notebook fits in-process and may not write joblib unless you add that cell).

Optional GPU note for reports: "We did not use a GPU; training is sklearn on CPU."

---

## Practical Example

Course project split:

| Job | Service | Mounts |
|-----|---------|--------|
| Train | `train` | data, src, models |
| Explore | `jupyter` profile | notebooks + the same data/models |

Do not bake trained weights into the image unless the assignment says to ship a frozen model.

---

## Common Mistakes

1. **Expecting GPU speed on this example.** There is no GPU path.
2. **Forgetting to mount `models/`.**
3. **Starting Jupyter without `--profile notebook`.** Service is ignored.
4. **Committing huge `.pt` / `.h5` files** in later projects without LFS or a download script.

---

## Best Practices

- CPU baseline first.
- Model artifacts on a mount or object storage, not in Docker layers, unless tiny and required.
- Profiles for optional interactive services.
- Pin sklearn in `requirements.txt`.

---

## Exercises

1. `docker compose up --build train` and copy MAE and R2.
2. Predict `5 5`.
3. Delete the joblib on the host, predict, read the error, retrain.
4. Start Jupyter with the profile; open the notebook.
5. One paragraph: GPU optional vs required for *this* assignment.

---

## Quick Review

- Train service vs Jupyter profile.
- Persist models with a bind mount.
- GPU is optional; this project is CPU sklearn.
- `compose run` for predict.

---

## Summary

You trained and predicted inside Docker without a local ML install. Next: a structured troubleshooting guide for everything that breaks in Parts 1–3.

---

[← Previous Lesson](22-docker-for-data-science.md)
[Course Home](../README.md)
[Next Lesson →](24-debugging.md)
