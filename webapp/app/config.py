from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
WEBAPP_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "modelo_emocion_atencion.keras"

NUM_FEATURES_PER_FRAME = 65
MAX_SEQ_LEN = 4504

# ComParE_2016 LLDs use a 10ms frame step, so MAX_SEQ_LEN frames correspond to
# ~45s of audio (matching the ~45s DEAM training excerpts). We only ever use
# the first MAX_SEQ_LEN frames anyway (see feature_extraction.py), so there is
# no point decoding/analyzing a whole multi-minute song: reading only this
# many seconds upfront keeps memory and CPU bounded regardless of how long the
# uploaded file is (important on memory-constrained hosts, e.g. Render's free
# tier, capped at 512MB).
MAX_AUDIO_DURATION_SECONDS = 50.0

MAX_UPLOAD_SIZE_MB = 50
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}

TEMP_UPLOAD_DIR = WEBAPP_DIR / "temp_uploads"
STATIC_DIR = WEBAPP_DIR / "static"
