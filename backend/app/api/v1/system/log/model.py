#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据层"""

from app.models.base import Model, CustomMixin, TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, BIGINT, ForeignKey

class OperationLogModel(CustomMixin, Model):
    __tablename__ = "system_operation_log"
    __table_args__ = ({'comment': '操作日志表'})

    request_path = Column(String(255), nullable=True, comment="请求路径")
    request_method = Column(String(10), nullable=True, comment="请求方式")
    request_payload = Column(Text, nullable=True, comment="请求体")
    request_ip = Column(String(50), nullable=True, comment="请求IP地址")
    request_os = Column(String(64), nullable=True, comment="操作系统")
    request_browser = Column(String(64), nullable=True, comment="浏览器")
    response_code = Column(Integer, nullable=True, comment="响应状态码")
    response_json = Column(Text, nullable=True, comment="响应体")



from typing import Dict, List, Sequence
from app.shared.crud.base import CRUDBase
from app.api.v1.system.log.schema import OperationLogCreate
from app.api.v1.system.auth.schema import Auth
from app.utils.tools import dict_to_search_sql


class OperationLogCRUD(CRUDBase[OperationLogModel, OperationLogCreate, None]):
    """
    日志模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        super().__init__(model=OperationLogModel, auth=auth)

    async def get_log_list(self, search: Dict = None, order: List[str] = None) -> Sequence[OperationLogModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else []
        return await self.list(search=sql_where, order=order)
