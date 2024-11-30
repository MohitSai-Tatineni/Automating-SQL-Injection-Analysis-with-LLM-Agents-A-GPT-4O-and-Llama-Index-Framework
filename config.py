import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    SESSION_COOKIE = os.getenv("SESSION_COOKIE")
    SERVER_URL = os.getenv("SERVER_URL")
    # SESSION_URL = os.getenv("SESSION_URL")

    @staticmethod
    def validate():
        missing = []
        for key, value in vars(Config).items():
            if not key.startswith("__") and not callable(value) and value is None:
                missing.append(key)
        if missing:
            raise ValueError(f"Missing environment variables: {', '.join(missing)}")

# Validate configuration on import
Config.validate()
