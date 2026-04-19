import joblib
import os
from pathlib import Path
import pandas as pd

# import sys
# sys.path.append(os.path.abspath(r".."))
from backend.services.feature_engineering import engineer_features,extract_features

from models.training.train import Trainer
from models.training.evaluate import model_evaluate
from utils.logger import setup_logger

from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from imblearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer


#Root dir
ROOT_DIR = Path(__file__).resolve().parents[2]
#dataset paths
train_path = ROOT_DIR / "data" / "fraudTrain.csv"
test_path = ROOT_DIR / "data" / "fraudTest.csv"

#log file path
log_path = ROOT_DIR / "logs" / "model.log"
logger = setup_logger("model_pipeline",log_path)

#model save paths
MODELS_DIR = Path(__file__).resolve().parents[1]
ARTIFACTS_DIR = MODELS_DIR / "artifacts"
MODELS_ARTIFACTS = ARTIFACTS_DIR / "models"
BEST_MODEL_DIR = ARTIFACTS_DIR / "best_model"
# create folders
MODELS_ARTIFACTS.mkdir(parents=True, exist_ok=True)
BEST_MODEL_DIR.mkdir(parents=True, exist_ok=True)



def load_dataset(file_path):
    df = pd.read_csv(file_path)
    return df


def pipeline():
    logger.info("model pipeline initiated")

    #1. load datasets
    logger.info("Ingesting Data...")
    train = load_dataset(train_path)
    test = load_dataset(test_path)

    #2. feature engineering
    logger.info("Performing Feature engineering...")
    train = engineer_features(train)
    test = engineer_features(test)

    #3. feature extraction
    logger.info("Extracting Features...")
    train = extract_features(train)
    test = extract_features(test)

    #4. Divide data into training and testing
    logger.info("created train and test datasets...")
    X_train = train.drop("is_fraud",axis=1)
    y_train = train.is_fraud
    X_test = test.drop("is_fraud",axis=1)
    y_test = test.is_fraud

    #5.--- Preprocessing pipeline---

    logger.info("preprocessing data...")
    #Divide numerical and categorical columns
    numeric_cols = X_train.select_dtypes(include="number").columns
    cat_cols = X_train.select_dtypes(include="str").columns

    preprocessor = ColumnTransformer([
            ("scaler",StandardScaler(),numeric_cols),
            ("encoder",OneHotEncoder(handle_unknown="ignore"),cat_cols)
    ])

    #6. ---Models---
    logger.info("xg boost model initialized...")
    xgb = Pipeline([
        ("preprocessor",preprocessor),
        ("smote",SMOTE()),
        ("model",XGBClassifier(n_estimators=300,max_depth=6,random_state=42))
    ])

    logger.info("random forest model initialized...")
    rf = Pipeline([
        ("preprocessor",preprocessor),
        ("smote",SMOTE()),
        ("model",RandomForestClassifier(n_estimators=100,max_depth=5,random_state=42))
    ])

    models = {"xgb":xgb,"RF":rf}

    #7. model training
    trainer = Trainer(models,X_train,y_train)
    trained_models = trainer.train_models_parallel()

    #8. model evaluation
    metrics_result = {}
    for name,model in trained_models.items():
        metrics_result[name] = model_evaluate(model,X_train,X_test,y_train,y_test,model_name=name)
        #model serialization
        logger.info(f"saving {name} in artifacts/models...")
        joblib.dump(model,f"{MODELS_ARTIFACTS}/{name}.pkl")


    #9. Serialize best model
    logger.info(f"Finding best model...")
    best_model_name = max(metrics_result,key = lambda x: metrics_result[x]['f1'])
    best_model = trained_models[best_model_name]
    logger.info(f"Best model {best_model_name}.. saving in artifacts/best_model...")
    joblib.dump(best_model,f"{BEST_MODEL_DIR}/model.pkl")

    logger.info("model pipeline finished successfully...")

    return metrics_result


if __name__=="__main__":
    pipeline()