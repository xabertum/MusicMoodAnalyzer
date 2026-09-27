import keras
import numpy as np

from .config import MODEL_PATH

# Orden de clases usado al entrenar (LabelEncoder ordena alfabéticamente por
# defecto, así que el índice de cada clase en la salida del modelo coincide
# con esta lista). Evita depender de scikit-learn en producción solo para
# deserializar 3 nombres de clase: scikit-learn + pandas suman ~150 MB de
# RAM en tiempo de ejecución, un coste inasumible en hosts con poca memoria
# (p. ej. el plan gratuito de Render, limitado a 512 MB).
CLASS_NAMES = ["Alegre", "Neutra", "Triste"]


class ModelService:
    def __init__(self):
        self.model = None

    def load(self):
        self.model = keras.models.load_model(MODEL_PATH)

    def predict(self, X_infer: np.ndarray) -> dict:
        probs = self.model.predict(X_infer, verbose=0)[0]
        probabilities = {cls: float(p) for cls, p in zip(CLASS_NAMES, probs)}
        predicted_class = CLASS_NAMES[int(np.argmax(probs))]
        return {"probabilities": probabilities, "predicted_class": predicted_class}


model_service = ModelService()
