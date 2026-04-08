#import necessary libraries
import os
import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
from backend.schemas import PredictFraudRequest,PredictFraudResponse
from fastapi.concurrency import run_in_threadpool

#app creation
app = FastAPI()

#load the model
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
model_path = os.path.join(ROOT_DIR,"models","xgb_pipeline.pkl")
pipe = joblib.load(model_path)


#simple home api
@app.get("/home")
def home():
    return {"message":"This is a home page"}

# 'hour', 'day', 'category', 'amt', 'gender', 'state', 'distance',
#        'city_pop', 'age'


#fraud prediction api
@app.post("/predict_fraud",response_model=PredictFraudResponse)
async def predict_fraud(pred_req : PredictFraudRequest):
    trans_data = pd.DataFrame({
        'hour':pred_req.hour, 
        'day' :pred_req.day,
        'category':pred_req.category,
        'amt':pred_req.amt,
        'gender':pred_req.gender,
        'state':pred_req.state,
        'distance':pred_req.distance,
        'city_pop':pred_req.city_pop,
        'age':pred_req.age
    }, index = [0])

    prediction = await run_in_threadpool(pipe.predict, trans_data)
    response = {
        "prediction":prediction[0], 
        "label": "Fraud" if prediction[0]==1 else "Not Fraud"
    }
    return response

