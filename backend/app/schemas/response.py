from pydantic import BaseModel

class ModelResponse(BaseModel):
    prediction: str
    fraud_probability: float