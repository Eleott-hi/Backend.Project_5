from dotenv import load_dotenv
import os

load_dotenv()

STORE_SERVICE = os.getenv("STORE_SERVICE")
KAFKA_SERVICE = os.getenv("KAFKA_SERVICE")