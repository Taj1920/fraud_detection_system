import joblib
import pandas as pd
from pathlib import Path
from backend.services.feature_engineering import engineer_features,extract_features
from backend.services.rules_engine import apply_rules
from utils.logger import setup_logger

#model path
ROOT_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = ROOT_DIR / "models" / "artifacts" / "best_model" / "model.pkl"

#logger
LOG_FILE = ROOT_DIR / "logs" / "prediction.log"
logger = setup_logger("prediction",LOG_FILE)

def load_best_model(model_path):
    model = joblib.load(model_path)
    return model

#load best model
model = load_best_model(MODEL_PATH)

def model_prediction(inp_data):
    try:
        logger.info(f"User input: {inp_data}")
        logger.info("preprocessing...")
        #convert to dataframe
        df = pd.DataFrame(inp_data if isinstance(inp_data,list) else [inp_data])
        #feature engineering
        df = engineer_features(df)
        #extract features
        df = extract_features(df)

        #predict fraud
        logger.info("model predicting...")
        prediction = model.predict(df)[0]

        #predict probability
        prob = model.predict_proba(df)[0][1]

        #rules engine
        prediction = apply_rules(df,prediction,prob)

        logger.info(f"predicted: {prediction}, fraud_probablity: {prob}")

        return {"prediction":prediction,"fraud_probablity":prob}
    except Exception as e:
        logger.error(f"Error during prediction {str(e)}")
        raise 


if __name__=="__main__":
    test_path = ROOT_DIR / "data" / "fraudTest.csv"
    df = pd.read_csv(test_path)
    sam = df[df["is_fraud"]==0].sample().to_dict(orient="records")
    print(sam)
    print(model_prediction(sam))



 