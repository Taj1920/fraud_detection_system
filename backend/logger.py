import logging
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BASE_DIR)
file_path = os.path.join(ROOT_DIR,"logs","app.logs")
#configuration
logging.basicConfig(
    filename=file_path,
    filemode="w",
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%s %H:%M:%S"
)