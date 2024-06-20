import os

from dotenv import load_dotenv

load_dotenv()

USER = os.environ.get("POSTGRES_USER")
PASSWORD = os.environ.get("POSTGRES_PASSWORD")
HOST = os.environ.get("POSTGRES_HOST")
PORT = os.environ.get("POSTGRES_PORT")
NAME = os.environ.get("POSTGRES_NAME")
