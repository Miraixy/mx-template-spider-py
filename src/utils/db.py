from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from src.conf import config
from src.log import logger

# 创建对象的基类:
Base = declarative_base()

# 初始化数据库连接:
engine = create_engine(config.DATABASE_URL)
Base.metadata.create_all(engine)

connection = engine.connect()
logger.info(f"Connected to database {config.DATABASE_URL}")

# 创建DBSession类型:
try:
    db: Session = sessionmaker(bind=engine)()
except Exception as e:
    logger.error("Failed to create DBSession: {}".format(e))
    raise


# 初始化数据库
def database_init():
    Base.metadata.create_all(engine, checkfirst=True)
    # 创建对象的基类:
    logger.success("Database initialized.")
