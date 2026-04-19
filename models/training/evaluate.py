from utils.logger import setup_logger
from sklearn.metrics import confusion_matrix,accuracy_score,precision_score,recall_score,f1_score
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[2]
log_path = ROOT_DIR / "logs" / "model.log"
logger = setup_logger("model_pipeline", log_path)

def model_evaluate(model,X_train,X_test,y_train,y_test,model_name="model"):
    logger.info("Evaluation started...")
    #prediction
    y_pred = model.predict(X_test)

    #evaluation metrics
    cm = confusion_matrix(y_test,y_pred)

    train_score = model.score(X_train,y_train)
    test_score = model.score(X_test,y_test)

    accuracy= accuracy_score(y_test,y_pred)
    precision = precision_score(y_test,y_pred)
    recall = recall_score(y_test,y_pred)
    f1 = f1_score(y_test,y_pred)
    logger.info("Evaluation finished...")
    metrics = {"model_name":model_name,
            "confuison_matrix":cm.tolist(),
            "train_data_score":train_score,
            "test_data_score":test_score,
            "accuracy":accuracy,
            "precision":precision,
            "recall":recall,
            "f1":f1}
    logger.info(f"{metrics}")
    return metrics




