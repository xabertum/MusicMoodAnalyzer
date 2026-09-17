import os

# Must run before any submodule imports `keras` (Python 3.14 has no TensorFlow
# wheel yet; the model has no custom TF-only layers, so the PyTorch backend
# loads it unchanged).
os.environ.setdefault("KERAS_BACKEND", "torch")
