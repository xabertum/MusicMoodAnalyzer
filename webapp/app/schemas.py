from pydantic import BaseModel


class PredictionResponse(BaseModel):
    predicted_class: str
    probabilities: dict[str, float]
