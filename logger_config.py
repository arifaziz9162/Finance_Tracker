import logging

# file handler and stream handler setup
logger = logging.getLogger("Finance_Tracker_Logger")
logger.setLevel(logging.DEBUG)

if not logger.hasHandlers():
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("finance_tracker.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)