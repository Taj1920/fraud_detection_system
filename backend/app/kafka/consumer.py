import json
import requests
from kafka import KafkaConsumer,KafkaProducer
from backend.app.kafka.config import KAFKA_BOOTSTRAP_SERVERS,TOPIC_NAME,OUTPUT_TOPIC,GROUP_ID
from utils.logger import setup_logger
from pathlib import Path

#logger
ROOT_DIR = Path(__file__).resolve().parents[3]
logger = setup_logger("kafka",ROOT_DIR / "logs" / "kafka.log")


#kafka consumer
consumer = KafkaConsumer(
    TOPIC_NAME,
    bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS,
    group_id = GROUP_ID,
    value_deserializer = lambda x: json.loads(x.decode("utf-8")),
    enable_auto_commit = False
)

#kafka prediciton result producer
producer = KafkaProducer(
    bootstrap_servers = KAFKA_BOOTSTRAP_SERVERS,
    value_serializer = lambda v:json.dumps(v).encode("utf-8")
)

for message in consumer:
    data = message.value
    logger.info(f"message: {data}")
    try:
        response = requests.post("http://127.0.0.1:8000/predict",json = data)
        data = response.json()

        producer.send(OUTPUT_TOPIC,value=data)
        producer.flush() #force sends buffer messages

        consumer.commit()# msg successfully processed

        logger.info(f"sent prediction: {data}")

    except Exception as e:

        logger.error(f" An error occured: {e}")
        raise
    