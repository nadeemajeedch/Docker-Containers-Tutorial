# Machine learning Docker project

CPU-only linear regression on a tiny CSV. GPU support is optional and not used here.

Lesson: [23](../../lessons/23-docker-for-machine-learning.md)

## Train (default)

```bash
cd examples/ml-docker
docker compose up --build train
```

Expected: MAE and R2 printed, `models/score-model.joblib` written on the host.

Predict (after training):

```bash
docker compose run --rm train python src/predict.py 5 5
```

## Jupyter (optional profile)

```bash
docker compose --profile notebook up --build jupyter
```

Open `http://localhost:8888` and run `notebooks/01-train.ipynb`.

## GPU (optional, advanced)

This project does **not** require NVIDIA Container Toolkit. If you later train a deep-learning model, you would add a GPU-enabled base image and Compose `deploy.resources.reservations.devices`. Skip that unless your lab machines have NVIDIA GPUs and the toolkit installed.

## Windows PowerShell

The `docker compose` commands are the same.
