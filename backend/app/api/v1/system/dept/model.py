#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据层"""

from app.models.base import Model, TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, BIGINT, ForeignKey
from app.api.v1.system.association.model import RoleMenusModel, RoleDeptsModel, UserPositionsModel, UserRolesModel
from typing import Dict, List, Sequence
from app.shared.crud.base import CRUDBase
from app.api.v1.system.dept.schema import DeptCreate, DeptUpdate
from app.api.v1.system.auth.schema import Auth
from app.utils.tools import dict_to_search_sql
from sqlalchemy import update

class DeptModel(TimestampMixin, Model):
    __tablename__ = "system_dept"
    __table_args__ = ({'comment': '部门表'})

    id = Column(BIGINT, primary_key=True, autoincrement=True, unique=True, comment='主键ID', nullable=False)
    name = Column(String(40), nullable=False, comment="部门名称")
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    available = Column(Boolean, nullable=False, default=True, comment="是否可用")
    parent_id = Column(
        BIGINT,
        ForeignKey("system_dept.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True, index=True, comment="父级部门ID"
    )
    description = Column(Text, nullable=True, comment="备注")

    parent = relationship("DeptModel", cascade='all, delete-orphan', uselist=False)




class DeptCRUD(CRUDBase[DeptModel, DeptCreate, DeptUpdate]):
    """
    部门模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        super().__init__(model=DeptModel, auth=auth)

    async def get_by_id(self, id: int) -> DeptModel:
        obj = await self.get(id=id)
        return obj

    async def get_dept_list(self, search: Dict = None, order: List[str] = None) -> Sequence[DeptModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else []
        return await self.list(search=sql_where, order=order)

    async def set_dept_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids)).values(available=available)
        await self.session.execute(sql)
        await self.session.flush()
