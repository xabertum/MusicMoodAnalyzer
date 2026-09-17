# Music Emotion Analyzer — Web App

Web local (FastAPI + HTML/JS) para subir una canción y obtener la predicción del
modelo `modelo_emocion_atencion.keras` (Alegre / Neutra / Triste).

## Prerequisitos

- Cualquier Python moderno sirve, incluido 3.14. El modelo se carga con
  **Keras 3 + backend PyTorch** (`KERAS_BACKEND=torch`, fijado en
  `app/__init__.py`) en lugar de TensorFlow, porque TensorFlow todavía no
  publica wheels para Python 3.14. El modelo solo usa capas estándar de Keras
  (`Attention`, `Conv1D`, `Bidirectional`/`LSTM`, etc., sin capas custom atadas
  a TensorFlow), así que se carga igual bajo PyTorch.
- `opensmile` ya trae el binario nativo de openSMILE para Windows vía pip, no
  requiere instalación aparte; decodifica `.mp3`/`.wav`/etc. internamente sin
  necesitar `ffmpeg` instalado por separado.

## Arranque

```bash
cd webapp
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```

Abre `http://localhost:8000/` en el navegador.

(`--reload` es opcional y solo útil en desarrollo: recarga el modelo en cada
guardado de archivo, lo cual es lento — no usarlo en uso diario normal.)

## Cómo funciona

1. El navegador sube el archivo de audio a `POST /api/predict`.
2. El backend extrae características con `opensmile`
   (`FeatureSet.ComParE_2016`, `FeatureLevel.LowLevelDescriptors`) y las ajusta
   (padding/truncado) a la forma `(4504, 65)` que espera el modelo — el mismo
   pipeline usado para reentrenarlo desde el audio crudo de DEAM (ver notebook,
   celda "Paso 4").
3. El modelo devuelve las probabilidades de las 3 clases; el backend responde
   con JSON y el frontend dibuja las barras y resalta la clase ganadora.

## Verificación rápida sin navegador

```bash
curl -X POST http://localhost:8000/api/predict -F "file=@ruta/a/audio.wav"
```

Debería devolver un JSON como:

```json
{"predicted_class": "Alegre", "probabilities": {"Alegre": 0.55, "Neutra": 0.30, "Triste": 0.15}}
```
