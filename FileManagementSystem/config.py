import json
import os
from dotenv import load_dotenv

load_dotenv()  # loads .env in dev, does nothing in prod

class CONFIG(dict):
    def __init__(self):
        data = read_json("config.json")

        user = os.getenv("DB_USER")
        password = os.getenv("DB_PASSWORD")

        if not user or not password:
            raise RuntimeError("DB_USER or DB_PASSWORD not set")

        data["SQL_ADDRESS"] = (
            f"postgresql://{user}:{password}"
            f"@{data['DB_HOST']}:{data['DB_PORT']}/{data['DB_NAME']}"
        )

        jwt_secret = os.getenv("JWT_SECRET_KEY")
        if not jwt_secret:
            raise RuntimeError("JWT_SECRET_KEY not set")
        data["JWT_SECRET_KEY"] = jwt_secret

        super().__init__(data)


def read_json(file):
    with open(file) as f:
        return json.load(f)
