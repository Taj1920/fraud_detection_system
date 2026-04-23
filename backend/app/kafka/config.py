import os
from dotenv import load_dotenv
load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
TOPIC_NAME = os.getenv("TOPIC_NAME")
OUTPUT_TOPIC = os.getenv("OUTPUT_TOPIC")
GROUP_ID = os.getenv("GROUP_ID")