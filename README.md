# Analizador de Emoción Musical (CNN + BiLSTM + Attention)

Clasifica canciones en **Alegre**, **Neutra** o **Triste** a partir de sus
características acústicas, usando un modelo de deep learning entrenado sobre el
dataset [DEAM](https://cvml.unige.ch/databases/DEAM/) (1802 canciones anotadas en
valencia/activación).

Incluye:

- El **notebook de entrenamiento** (`Music_Clasificator_CNN.ipynb`): carga de
  anotaciones DEAM, extracción de características de audio con `openSMILE`
  (`ComParE_2016`, descriptores de bajo nivel), balanceo de clases, y
  arquitectura CNN + BiLSTM con Attention.
- Los **artefactos entrenados** (`modelo_emocion_atencion.keras`,
  `label_encoder.pkl`), listos para servir en producción.
- Una **web app local** (`webapp/`, FastAPI + HTML/JS) para subir una canción y
  ver la predicción con un gráfico de barras interactivo.

## Cómo funciona

1. Subes un archivo de audio (`.wav`, `.mp3`, `.flac`, `.ogg`, `.m4a`).
2. El backend extrae un fragmento representativo y calcula sus características
   acústicas con `openSMILE` (mismo pipeline usado en entrenamiento, para evitar
   desajustes entre entrenamiento y producción).
3. El modelo (CNN + BiLSTM + Attention) procesa la secuencia de características
   y devuelve una probabilidad por clase.
4. La web muestra la emoción predominante y el desglose de probabilidades.

Todo el análisis ocurre en local: el audio no se envía a ningún servicio externo.

## Estructura del repositorio

```
.
├── Music_Clasificator_CNN.ipynb   # Notebook de entrenamiento (Google Colab)
├── modelo_emocion_atencion.keras  # Modelo entrenado
├── label_encoder.pkl              # LabelEncoder de las 3 clases
└── webapp/                        # Web app FastAPI + HTML/JS
    ├── app/                       # Backend (carga de modelo, extracción de
    │                              # features, endpoints)
    └── static/                    # Frontend (index.html, script.js, style.css)
```

Los datasets crudos de DEAM (`DEAM_Annotations/`, `DEAM_Features/`,
`DEAM_audio/`) no se incluyen en el repositorio por su tamaño; son necesarios
solo para reentrenar el modelo desde el notebook, no para usar la web app.

## Arrancar la web app

```bash
cd webapp
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```

Abre `http://localhost:8000/` en el navegador. Más detalle en
[`webapp/README.md`](webapp/README.md).

## Modelo

- **Arquitectura:** CNN (Conv1D) + BiLSTM con capa de Attention, implementada
  en Keras 3 (backend PyTorch).
- **Entrada:** secuencia de características `openSMILE ComParE_2016`
  (descriptores de bajo nivel) extraídas del audio crudo, forma `(4504, 65)`.
- **Salida:** probabilidades para 3 clases (Alegre / Neutra / Triste).
- **Entrenamiento:** dataset DEAM, con balanceo de clases y soft labels
  derivadas de centroides Valencia/Activación.
