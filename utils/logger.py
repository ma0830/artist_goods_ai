'''
Created on 2025/09/04

@author: 81901
'''
# utils/logger.py
import logging

LOG_FILE = "app.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    encoding="utf-8"
)

def log_event(message: str):
    logging.info(message)

def log_error(message: str):
    logging.error(message)
