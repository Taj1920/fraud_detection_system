import pandas as pd
from fastapi import APIRouter
from backend.app.services.inference_service import model_prediction
from backend.app.schemas.transaction import Transaction 
from backend.app.schemas.response import ModelResponse 
from pathlib import Path

router = APIRouter()

# ROOT_DIR = Path(__file__).resolve().parents[3]
# test_data_path = ROOT_DIR / "data" / "fraudTest.csv"
# df = pd.read_csv(test_data_path,index_col=0)


@router.post("/predict",response_model=ModelResponse)
def predict(data: Transaction):
    result =  model_prediction(data.model_dump())
    return result


@router.get("/sample_transactions")
def sample_transactions(n_samples: int = 10):
    pass