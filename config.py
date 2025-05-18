# from dotenv import load_dotenv
# load_dotenv()

# import os
# GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
# SECRET_KEY = 'testkey'  # For testing only, not secure for production


import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///users.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

