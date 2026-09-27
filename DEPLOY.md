# Desplegar la demo (Render.com)

Este repo incluye un `Dockerfile` en la raíz listo para desplegar la web app
(FastAPI + Keras/PyTorch + openSMILE) en cualquier proveedor con soporte
Docker. La forma recomendada y gratuita es **Render.com**:

## Pasos

1. Crea una cuenta en [render.com](https://render.com) (puedes registrarte con
   tu cuenta de GitHub).
2. En el dashboard: **New → Web Service**.
3. Conecta tu cuenta de GitHub y selecciona el repositorio
   `xabertum/MusicMoodAnalyzer`.
4. **Importante**: en el desplegable de **Language/Runtime**, elige
   **Docker** (no "Python 3"). Si Render detecta el `Dockerfile` de la raíz
   correctamente, los campos "Build Command" y "Start Command" desaparecen —
   no hacen falta, el propio `Dockerfile` define cómo arrancar la app.
5. Configuración del servicio:
   - **Branch**: `main`
   - **Instance Type**: **Free**
   - El resto de campos por defecto
6. **Create Web Service**. Render construirá la imagen (puede tardar varios
   minutos por el tamaño de las dependencias: PyTorch, openSMILE, etc.) y
   publicará la app en una URL del tipo
   `https://music-mood-analyzer.onrender.com`.

⚠️ En el plan gratuito, el servicio "duerme" tras 15 minutos sin tráfico y
tarda ~1 minuto en despertar en la siguiente visita.

## Notas técnicas

- El contenedor escucha en el puerto indicado por la variable de entorno
  `$PORT` si existe (como hace Render), y si no en el `7860` por defecto
  (convención de Hugging Face Spaces, donde este mismo `Dockerfile` también
  funciona sin cambios si en el futuro se prefiere esa alternativa).
- PyTorch se instala desde el índice CPU-only
  (`https://download.pytorch.org/whl/cpu`) para evitar arrastrar las
  librerías CUDA de NVIDIA (~550 MB de más) que no se usan en un despliegue
  sin GPU.

## Probar la imagen en local

```bash
docker build -t music-mood-analyzer .
docker run --rm -p 7860:7860 music-mood-analyzer
# abre http://localhost:7860
```
