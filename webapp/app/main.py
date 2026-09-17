import uuid
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import ALLOWED_EXTENSIONS, MAX_UPLOAD_SIZE_MB, STATIC_DIR, TEMP_UPLOAD_DIR
from .feature_extraction import extract_features
from .model_service import model_service
from .schemas import PredictionResponse

app = FastAPI(title="Music Emotion Analyzer")


@app.on_event("startup")
def on_startup():
    TEMP_UPLOAD_DIR.mkdir(exist_ok=True)
    model_service.load()


@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.post("/api/predict", response_model=PredictionResponse)
def predict(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(400, f"Formato no soportado: {ext or 'desconocido'}")

    tmp_path = TEMP_UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
    try:
        size = 0
        max_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
        with open(tmp_path, "wb") as f:
            while chunk := file.file.read(1024 * 1024):
                size += len(chunk)
                if size > max_bytes:
                    raise HTTPException(413, "Archivo demasiado grande")
                f.write(chunk)

        try:
            X_infer = extract_features(str(tmp_path))
        except Exception as e:
            raise HTTPException(422, f"No se pudo procesar el archivo de audio: {e}")

        result = model_service.predict(X_infer)
        return PredictionResponse(**result)
    finally:
        tmp_path.unlink(missing_ok=True)
