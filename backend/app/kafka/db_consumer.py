import json
from kafka import KafkaConsumer
from backend.app.db.crud import insert_prediction
from backend.app.kafka.config import OUTPUT_TOPIC,KAFKA_BOOTSTRAP_SERVERS
from pathlib import Path
from utils.logger import setup_logger


#logger
ROOT_DIR = Path(__file__).resolve().parents[3]
log_file = ROOT_DIR / "logs" / "kafka.log"
logger = setup_logger("db_consumer",log_file)

consumer = KafkaConsumer(
    OUTPUT_TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_deserializer=lambda x: json.loads(x.decode("utf-8")),
    auto_offset_reset="earliest",
    enable_auto_commit=False
)


for msg in consumer:
    data = msg.value

    try:
        insert_prediction(data)

        consumer.commit()   # commit only after DB success

        logger.info(f"Inserted into DB: {data}")

    except Exception as e:
        logger.error(f"Error: {e}")
        raise