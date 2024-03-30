from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
import logging
from datetime import datetime

webserver = Flask(__name__)

# Initialize the logger & add handler to webserver.log
webserver.logger.setLevel(logging.INFO)
handler = logging.FileHandler("webserver.log")
webserver.logger.addHandler(handler)

webserver.tasks_runner = ThreadPool()
webserver.logger.info(f"[{datetime.now()}] ThreadPool initialized")

# webserver.task_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")
webserver.logger.info(f"[{datetime.now()}] Loaded data from CSV file")

webserver.job_counter = 1


from app import routes
