import json
import time
import pandas as pd
from utils.logger import setup_logger
from kafka import KafkaProducer
from backend.app.kafka.config import KAFKA_BROKER,TOPIC_NAME
from pathlib import Path

#logger
ROOT_DIR = Path(__file__).resolve().parents[3]
logger = setup_logger("kafka",ROOT_DIR / "logs" / "kafka.log")


#kafka producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer = lambda v: json.dumps(v).encode("utf-8")
)



TOPIC = TOPIC_NAME

#stream data logic

def stream_data(fraud=0):
    logger.info("producer started...")
    try:
        test_data_path = ROOT_DIR / "data" / "fraudTest.csv"
        df = pd.read_csv(test_data_path)
        df = df[df["is_fraud"]==fraud]
        for _,row in df.iterrows():
            data = row.to_dict()
            producer.send(TOPIC,value = data)
            producer.flush()
            logger.info(f"sent to kafka {data}")
            #delay
            time.sleep(0.5)

    except Exception as e:
        print(f"Error: {e}")

    

if __name__=="__main__":
    stream_data(fraud=1)