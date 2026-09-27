# syntax=docker/dockerfile:1

# Docker image for running the Music Emotion Analyzer web app (FastAPI + Keras/PyTorch + openSMILE).
#
# Designed to work as-is on Hugging Face Spaces (Docker SDK): the app listens on
# port 7860, which is the port Spaces expects. It also works locally:
#
#   docker build -t music-mood-analyzer .
#   docker run --rm -p 7860:7860 music-mood-analyzer
#   # open http://localhost:7860
#
FROM python:3.11-slim

WORKDIR /code

# Model artifacts + webapp source (paths are resolved relative to this layout
# by webapp/app/config.py, so keep the model files at the repo root).
COPY modelo_emocion_atencion.keras label_encoder.pkl ./
COPY webapp ./webapp

# Install the CPU-only PyTorch wheel first: the default PyPI wheel bundles the
# NVIDIA CUDA runtime (~550 MB) even though we never use a GPU here. The CPU
# wheel is ~150-190 MB and is all Render's (or any CPU-only host's) free tier
# needs. `pip install -r` afterwards leaves it in place since "torch" (no
# version pin) is already satisfied.
RUN pip install --no-cache-dir --index-url https://download.pytorch.org/whl/cpu --timeout 120 --retries 5 torch \
    && pip install --no-cache-dir --timeout 120 --retries 5 -r webapp/requirements.txt

# Keras 3 loads the model with the PyTorch backend (no TensorFlow wheel
# dependency), matching how the model was trained/exported.
ENV KERAS_BACKEND=torch
ENV PYTHONUNBUFFERED=1

WORKDIR /code/webapp

EXPOSE 7860

# Render (and most PaaS providers) inject a $PORT env var; default to 7860
# (Hugging Face Spaces' expected port) when it's not set, e.g. local `docker run`.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-7860}"]
