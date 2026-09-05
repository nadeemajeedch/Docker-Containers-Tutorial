FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /workspace

RUN useradd --create-home --uid 1000 --shell /bin/bash jovyan \
    && mkdir -p /workspace/notebooks /workspace/data /workspace/src /workspace/tests /workspace/results \
    && chown -R jovyan:jovyan /workspace /home/jovyan

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
    && rm /tmp/requirements.txt

USER jovyan
WORKDIR /workspace

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--ServerApp.token="]
