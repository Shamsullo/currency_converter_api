from pydantic import Field
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(..., env='DATABASE_URL')
    cb_api_key: str = Field(..., env='CB_API_KEY')


settings = Settings()
