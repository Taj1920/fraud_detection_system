import os
import mysql.connector
from mysql.connector import Error
from pathlib import Path
from utils.logger import setup_logger
from dotenv import load_dotenv
load_dotenv()

#config
DB_HOST=os.getenv("DB_HOST")
DB_USER=os.getenv("DB_USER")
DB_PASSWORD=os.getenv("DB_PASSWORD")
DB_NAME=os.getenv("DB_NAME")
DB_PORT=os.getenv("DB_PORT")


#logger
ROOT_DIR = Path(__file__).resolve().parents[3]
log_file = ROOT_DIR / "logs" / "app.log"
logger = setup_logger("database",log_file)



def get_connection():
    try:
        conn= mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return conn
    
    except Error as e:
        logger.error("DB connection error")
        raise
        return None