import os
import json
import time
import pandas as pd
from utils.logger import logging
from kafka import KafkaProducer
from config import KAFKA_BROKER,TOPIC_NAME

#kafka producer

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer = lambda v: json.dumps(v).encode("utf-8")
)

TOPIC = TOPIC_NAME

#stream data logic

def stream_data():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        ROOT_DIR = os.path.dirname(BASE_DIR)
        test_data_path = os.path.join(ROOT_DIR,"data","fraudTest.csv")
        df = pd.read_csv(test_data_path)
        for _,row in df.iterrows():
            data = row.to_dict()
            producer.send(TOPIC,value = data)
            logging.info(f"sent to kafka {data}")
            #delay
            time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")

    

if __name__=="__main__":
    stream_data()