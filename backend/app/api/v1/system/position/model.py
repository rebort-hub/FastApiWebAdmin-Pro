#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据层"""

from app.models.base import Model, CustomMixin, TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, BIGINT, ForeignKey
from app.api.v1.system.association.model import RoleMenusModel, RoleDeptsModel, UserPositionsModel, UserRolesModel
from typing import Dict, List, Sequence
from app.shared.crud.base import CRUDBase
from app.api.v1.system.position.schema import PositionCreate, PositionUpdate
from app.api.v1.system.auth.schema import Auth
from app.utils.tools import dict_to_search_sql
from sqlalchemy import update

class PositionModel(CustomMixin, Model):
    __tablename__ = "system_position"
    __table_args__ = ({'comment': '岗位表'})

    name = Column(String(40), nullable=False, comment="岗位名称")
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    available = Column(Boolean, default=True, nullable=False, comment="是否可用")

    users = relationship(
        "UserModel",
        secondary=UserPositionsModel.__tablename__,
        back_populates='positions',
        lazy="joined",
        uselist=True
    )






class PositionCRUD(CRUDBase[PositionModel, PositionCreate, PositionUpdate]):
    """
    岗位模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        super().__init__(model=PositionModel, auth=auth)

    async def get_by_id(self, id: int) -> PositionModel:
        obj = await self.get(id=id)
        return obj

    async def get_position_list(self, search: Dict = None, order: List[str] = None) -> Sequence[PositionModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else None
        return await self.list(search=sql_where, order=order)

    async def set_position_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids)).values(available=available)
        await self.session.execute(sql)
        await self.session.flush()
