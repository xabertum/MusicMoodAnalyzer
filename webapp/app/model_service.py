import pickle

import keras
import numpy as np

from .config import LABEL_ENCODER_PATH, MODEL_PATH


class ModelService:
    def __init__(self):
        self.model = None
        self.label_encoder = None

    def load(self):
        self.model = keras.models.load_model(MODEL_PATH)
        with open(LABEL_ENCODER_PATH, "rb") as f:
            self.label_encoder = pickle.load(f)

    def predict(self, X_infer: np.ndarray) -> dict:
        probs = self.model.predict(X_infer, verbose=0)[0]
        classes = self.label_encoder.classes_
        probabilities = {cls: float(p) for cls, p in zip(classes, probs)}
        predicted_class = str(classes[int(np.argmax(probs))])
        return {"probabilities": probabilities, "predicted_class": predicted_class}


model_service = ModelService()
