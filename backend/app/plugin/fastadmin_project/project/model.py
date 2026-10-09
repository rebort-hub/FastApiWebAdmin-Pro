#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据层"""

from typing import Dict, List, Sequence
from sqlalchemy import Column, String, Integer, Boolean, update
from app.models.base import Model, CustomMixin
from app.shared.crud.base import CRUDBase
from app.api.v1.system.auth.schema import Auth
from app.utils.tools import dict_to_search_sql
from app.plugin.fastadmin_project.project.schema import ProjectCreate, ProjectUpdate


class ProjectModel(CustomMixin, Model):
    __tablename__ = "project_info"
    __table_args__ = ({"comment": "项目信息表"})

    name = Column(String(100), nullable=False, comment="项目名称")
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    available = Column(Boolean, default=True, nullable=False, comment="是否可用")


class ProjectCRUD(CRUDBase[ProjectModel, ProjectCreate, ProjectUpdate]):
    """项目管理数据查询层"""

    def __init__(self, auth: Auth) -> None:
        super().__init__(model=ProjectModel, auth=auth)

    async def get_by_id(self, id: int) -> ProjectModel:
        return await self.get(id=id)

    async def get_project_list(self, search: Dict = None, order: List[str] = None) -> Sequence[ProjectModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else None
        return await self.list(search=sql_where, order=order)

    async def set_project_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids)).values(available=available)
        await self.session.execute(sql)
        await self.session.flush()
