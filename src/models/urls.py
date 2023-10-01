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


class DB_Url(Base):
    __tablename__ = "url"

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键")

    # 在此添加表结构信息:
    value = Column(String(length=1024), comment="url 值")
    domain = Column(String(length=1024), comment="域名")
    title = Column(String(length=1024), comment="标题")
    visited_cnt = Column(Integer, default=0, comment="访问次数")
    task_finished = Column(Boolean, default=False, comment="任务是否完成")
    is_error = Column(Boolean, default=False, comment="是否任务错误")
    output = Column(Text(length=1024), comment="输出内容")

    extra_info = Column(String(length=1024), comment="额外信息")
    last_update_time = Column(DateTime, default=datetime.now, comment="数据最后更新时间(db)")
    created_time = Column(DateTime, default=datetime.now, comment="数据创建时间(db)")

    def update_visited_cnt(self):
        self.visited_cnt += 1
        self.update(self, visited_cnt=self.visited_cnt)

    def update_task_finished(self):
        self.task_finished = True
        self.update(self, task_finished=self.task_finished)

    def update_is_error(self):
        self.is_error = True
        self.update(self, is_error=self.is_error)

    @classmethod
    def get_available(cls, allow_domain: str = "*", limit: int = 0):
        """获取所有可用的 url 资源"""

        condition = {
            "task_finished": False,
            "is_error": False,
            "domain": allow_domain,
        }

        if allow_domain == "*":
            condition.pop("domain")

        if limit:
            return db.query(cls).filter_by(**condition).limit(limit).all()
        return db.query(cls).filter_by(**condition).all()

    @classmethod
    def get_by_url(cls, value: str):
        """根据 url 获取 url 资源"""
        return db.query(cls).filter(cls.value == value).first()


    # region 通用方法

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
    def add(cls, data: "DB_Url"):
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
    def update(cls, data: "DB_Url", **kwargs):
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
    def delete(cls, data: "DB_Url"):
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

    # endregion
