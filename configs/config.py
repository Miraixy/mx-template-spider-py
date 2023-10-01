from typing import Literal


class Config:
    """Configuration"""

    def __getitem__(self, key):
        return self.__getattribute__(key)

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    UVICORN_LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "WARNING"
    DATABASE_URL: str = "sqlite:///./test.sqlite3.db"
    DEBUG: bool = True
    OUTPUT_DIR: str = "outputs"

    ENTRY_URL: str = "https://www.baidu.com/"
    ALLOW_CORS: bool = False
    MAX_CONNECTIONS: int = 5


class DevConfig(Config):
    """Development environment configuration"""

    LOG_LEVEL = "DEBUG"
    UVICORN_LOG_LEVEL = "DEBUG"
    DATABASE_URL = "sqlite:///./test.sqlite3.db"
    DEBUG = True


class ProdConfig(Config):
    """Production environment configuration"""

    LOG_LEVEL = "WARNING"
    UVICORN_LOG_LEVEL = "WARNING"
    DEBUG = False
