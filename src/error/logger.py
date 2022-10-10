import os
import logging

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
LOG_PATH = f"{BASE_PATH}/log/base_loger.log"
logging.basicConfig(level=logging.INFO, filename=LOG_PATH,
                    format="%(asctime)s :: %(levelname)s :: %(message)s")
