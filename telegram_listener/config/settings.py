import os

from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class Settings(BaseModel):
    API_ID: int
    API_HASH: str
    PHONE_NUMBER: str
    DJANGO_API_URL: str
    DJANGO_API_TOKEN: str | None = None


def get_settings() -> Settings:
    return Settings(
        API_ID=int(os.getenv("API_ID")),
        API_HASH=os.getenv("API_HASH"),
        PHONE_NUMBER=os.getenv("PHONE_NUMBER"),
        DJANGO_API_URL=os.getenv("DJANGO_API_URL"),
        DJANGO_API_TOKEN=os.getenv("DJANGO_API_TOKEN"),
    )
