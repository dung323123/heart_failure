import os
from dotenv import load_dotenv

# Load biến môi trường từ file .env
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://dungduhau:m7lNjMGLn3mzAAAx@heartprediction.ursbr.mongodb.net/")
DATABASE_NAME = os.getenv("DATABASE_NAME", "heart_prediction")
