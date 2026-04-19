from utils.logger import setup_logger
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[2]
log_path = ROOT_DIR / "logs" / "model.log"

logger = setup_logger("model_pipeline", log_path)

#single model trainer

def model_trainer(model_tuple):
    name,model,X_train,y_train = model_tuple
    model.fit(X_train,y_train)
    return name,model

#multi-model training
class Trainer:
    def __init__(self,models: dict,X_train,y_train):
        self.models=models
        self.X_train = X_train
        self.y_train = y_train
  
    
    def train_models_parallel(self):
        trained_models = {}
        logger.info(f"Model Training initiated ...")

        with ProcessPoolExecutor() as executor:
            tasks = [(name,model,self.X_train,self.y_train) 
                     for name,model in self.models.items()]

            results = executor.map(model_trainer,tasks)

            for name,model in results:
                trained_models[name]=model
        
        logger.info(f"Model Training completed ...")
        return trained_models
        