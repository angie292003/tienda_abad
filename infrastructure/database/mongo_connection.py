import os
from pathlib import Path

import certifi
from dotenv import load_dotenv
from pymongo import MongoClient


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "tienda_abad")

if not MONGO_URI:
    raise ValueError("No se encontró MONGO_URI en el archivo .env")


client = MongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where()
)

db = client[MONGO_DB]