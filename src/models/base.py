import json
from datetime import datetime

from sqlalchemy import (  # noqa: F401
    Boolean,
    Column,
    DateTime,
    Double,
    Integer,
    String,
    Text,
)

from src.utils.db import Base, db


# 定义 DB_Base 模型
class DB_Base(Base):
    __tablename__ = "base"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")
    # 在此添加表结构信息:
    # ...

    extra_info = Column(String(length=1024), comment="额外信息")
    last_update_time = Column(DateTime, default=datetime.now, comment="数据最后更新时间(db)")
    created_time = Column(DateTime, default=datetime.now, comment="数据创建时间(db)")

    def get_extra_info(self):
        try:
            if json.loads(str(self.extra_info)):
                return json.loads(str(self.extra_info))
        except:
            return {}
        return {}

    def update_extra_info(self, data: dict):
        self.update(self, extra_info=json.dumps(self.get_extra_info().update(data)))

    @classmethod
    def add(cls, data: "DB_Base"):
        """新增 Base 资源"""

        data.last_update_time = datetime.now()
        data.created_time = datetime.now()
        db.add(data)
        db.commit()

    @classmethod
    def get_by_id(cls, _id: int):
        """根据 id 查询 Base 资源"""

        return db.query(cls).filter(cls.id == _id).first()

    @classmethod
    def get_all(cls, limit: int = 0):
        """获取所有 Base 资源"""

        if limit > 0:
            return db.query(cls).limit(limit).all()
        return db.query(cls).all()

    @classmethod
    def update(cls, data: "DB_Base", **kwargs):
        """更新 Base 资源"""

        if "id" in kwargs:
            del kwargs["id"]
        if "created_time" in kwargs:
            del kwargs["created_time"]
        if "last_update_time" in kwargs:
            del kwargs["last_update_time"]
        data.last_update_time = datetime.now()
        db.query(cls).filter(cls.id == data.id).update(dict(**kwargs))
        db.commit()

    @classmethod
    def delete(cls, data: "DB_Base"):
        """删除 Base 资源"""

        db.query(cls).filter(cls.id == data.id).delete()
        db.commit()

    @classmethod
    def auto_insert(cls, **kwargs):
        """自动插入 Base 资源(不存在则新增)"""

        if "id" in kwargs:
            base = cls.get_by_id(kwargs["id"])
            if base:
                cls.update(base, **kwargs)
                return base
        base = cls(**kwargs)
        cls.add(base)
        return base

