import os

from dotenv import load_dotenv


load_dotenv()


BROKER_HOST = os.getenv('BROKER_HOST', '')

BROKER_TOPIC = os.getenv('BROKER_TOPIC', '')
