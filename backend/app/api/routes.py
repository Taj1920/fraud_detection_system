from fastapi import APIRouter
from backend.services.inference_service import model_prediction
from backend.app.schemas.transaction import Transaction 
from backend.app.schemas.response import ModelResponse 


router = APIRouter()


@router.post("/predict",response_model=ModelResponse)
def predict(data: Transaction):
    result =  model_prediction(data.model_dump())
    return result