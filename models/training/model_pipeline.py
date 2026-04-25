import joblib
import json
from pathlib import Path
import pandas as pd

from backend.app.services.feature_engineering import engineer_features,extract_features
from models.training.train import Trainer
from models.training.evaluate import model_evaluate
from utils.logger import setup_logger

from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from imblearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient

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

#mlflow config
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("fraud_detection")

def load_dataset(file_path):
    df = pd.read_csv(file_path,index_col=0)
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
    cat_cols = X_train.select_dtypes(include="object").columns

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
        ("model",RandomForestClassifier(n_estimators=100,max_depth=5,random_state=42,verbose=1))
    ])

    models = {"xgb":xgb,"RF":rf}

    #7. model training
    logger.info("Models Training paralelly...")
    trainer = Trainer(models,X_train,y_train)
    trained_models = trainer.train_models_parallel()
    logger.info("Models Training finished...")

    #8. model evaluation
    metrics_result = {}
    run_ids = {}
    for name,model in trained_models.items():
        with mlflow.start_run(run_name=name) as run:
            run_id = run.info.run_id
            run_ids[name]=run_id
            logger.info(f"logging {name} to mlflow...")

            #Evaluate model
            metrics = model_evaluate(model,X_train,X_test,y_train,y_test,model_name=name)
            metrics_result[name] = metrics

            #log metrics to mlflow
            for metric_name,value in metrics.items():
                #log numeric
                if isinstance(value,(int,float)):
                    mlflow.log_metric(metric_name,value)
                #log string
                elif isinstance(value,str):
                    mlflow.log_param(metric_name,value)
                #log large objects as artifacts
                else:
                    with open("temp.json","w") as file:
                        json.dump(value,file)
                    mlflow.log_artifact("temp.json")



            #log params
            if name=="xgb":
                mlflow.log_param("model","XGBoost")
            else:
                mlflow.log_param("model","RandomForest")

            #log model to mlflow
            mlflow.sklearn.log_model(model,"model",pyfunc_predict_fn="predict_proba")

            #model serialization
            logger.info(f"saving {name} in artifacts/models...")
            joblib.dump(model,f"{MODELS_ARTIFACTS}/{name}.pkl")


    #9. Serialize best model
    logger.info(f"Finding best model...")
    best_model_name = max(metrics_result,key = lambda x: metrics_result[x]['f1'])
    best_model = trained_models[best_model_name]
    best_run_id = run_ids[best_model_name]

    #log best model to mlflow
    client = MlflowClient()
    logger.info(f"logging best model {best_model_name} and params to mlflow")
    client.log_param(best_run_id,"best_model",best_model_name)
    for metric_name,value in metrics_result[best_model_name].items():
            #log numeric
            if isinstance(value,(int,float)):
                client.log_metric(best_run_id,f"best_{metric_name}",value)
            #log string
            elif isinstance(value,str):
                client.log_param(best_run_id,f"best_{metric_name}",value)
            #log large objects as artifacts
            else:
                with open("temp.json","w") as file:
                    json.dump(value,file)
                client.log_artifact(best_run_id,"temp.json")

    #register best model in mlflow
    model_uri = f"runs:/{best_run_id}/model"
    registered_model = mlflow.register_model(model_uri=model_uri,
                            name="fraud_detection_model")
    version = registered_model.version
    #promote to production
    client.transition_model_version_stage(
    name="fraud_detection_model",
    version=version,
    stage="Production"
    )

    logger.info(f"Model v{version} moved to Production")


    logger.info(f"Best model {best_model_name}.. saving in artifacts/best_model...")
    joblib.dump(best_model,f"{BEST_MODEL_DIR}/model.pkl")

    logger.info("model pipeline finished successfully...")

    return metrics_result


if __name__=="__main__":
    pipeline()