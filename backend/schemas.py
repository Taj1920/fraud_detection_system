#pydantic schemas
from pydantic import BaseModel


#predict fraud request body
class PredictFraudRequest(BaseModel):
    hour: int
    day: int
    category: str
    amt: float
    gender: str
    state: str
    distance: float
    city_pop: int
    age:  int

#predict fraud response body

class PredictFraudResponse(BaseModel):
    prediction: int
    label: str