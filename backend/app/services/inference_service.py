import mlflow
import numpy as np
import pandas as pd
from pathlib import Path
from backend.app.services.feature_engineering import engineer_features,extract_features
from backend.app.services.rules_engine import apply_rules
from utils.logger import setup_logger


#logger
ROOT_DIR = Path(__file__).resolve().parents[3]
LOG_FILE = ROOT_DIR / "logs" / "prediction.log"
logger = setup_logger("prediction",LOG_FILE)

def load_best_model():
    mlflow.set_tracking_uri("http://mlflow:5000")
    model = mlflow.pyfunc.load_model("models:/fraud_detection_model/Production")
    return model

#load best model
model = load_best_model()

def model_prediction(inp_data):
    try:
        logger.info(f"User input: {inp_data}")
        logger.info("preprocessing...")
        #convert to dataframe
        df = pd.DataFrame(inp_data if isinstance(inp_data,list) else [inp_data])
        trans_num = df["trans_num"][0]
        #feature engineering
        df = engineer_features(df)
        #extract features
        df = extract_features(df)
        #predict fraud
        logger.info("model predicting...")
        probs = model.predict(df)
        prob = probs[0][1]
        pred_class = np.argmax(probs,axis=1)[0]

        #rules engine
        prediction = apply_rules(df,pred_class,prob)

        logger.info(f"trans_num: {trans_num} predicted: {prediction}, fraud_probability: {prob}")

        return {"trans_num":trans_num,"prediction":prediction,"fraud_probability":float(prob)}
    except Exception as e:
        logger.error(f"Error during prediction {str(e)}")
        raise 


if __name__=="__main__":
    test_path = ROOT_DIR / "data" / "fraudTest.csv"
    df = pd.read_csv(test_path)
    sam = df[df["is_fraud"]==0].sample().to_dict(orient="records")
    print(sam)
    print(model_prediction(sam))



 