from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
WEBAPP_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = BASE_DIR / "modelo_emocion_atencion.keras"

NUM_FEATURES_PER_FRAME = 65
MAX_SEQ_LEN = 4504

MAX_UPLOAD_SIZE_MB = 50
ALLOWED_EXTENSIONS = {".wav", ".mp3", ".flac", ".ogg", ".m4a"}

TEMP_UPLOAD_DIR = WEBAPP_DIR / "temp_uploads"
STATIC_DIR = WEBAPP_DIR / "static"
