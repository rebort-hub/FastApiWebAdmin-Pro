#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据层"""

from app.models.base import Model, TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, BIGINT, ForeignKey
from app.api.v1.system.association.model import RoleMenusModel, RoleDeptsModel, UserPositionsModel, UserRolesModel
from typing import Dict, List, Sequence
from app.shared.crud.base import CRUDBase
from app.api.v1.system.menu.schema import MenuCreate, MenuUpdate
from app.api.v1.system.auth.schema import Auth
from app.utils.tools import dict_to_search_sql
from sqlalchemy import update

class MenuModel(TimestampMixin, Model):
    __tablename__ = "system_menu"
    __table_args__ = ({'comment': '菜单表'})

    id = Column(BIGINT, primary_key=True, autoincrement=True, unique=True, comment='主键ID', nullable=False)
    name = Column(String(50), nullable=False, comment="菜单名称")
    type = Column(Integer, nullable=False, comment="菜单类型")
    icon = Column(String(50), nullable=False, default="", comment="图标")
    order = Column(Integer, nullable=False, default=1, comment="显示排序")
    permission = Column(String(50), nullable=False, default="", comment="权限标识")
    route_name = Column(String(50), nullable=True, comment="路由名称")
    route_path = Column(String(50), nullable=True, comment="路由路径")
    component_path = Column(String(50), nullable=True, comment="组件路径")
    redirect = Column(String(50), nullable=True, comment="重定向")
    available = Column(Boolean, nullable=False, default=True, comment="是否可用")
    cache = Column(Boolean, nullable=False, default=True, comment="是否缓存")
    hidden = Column(Boolean, nullable=False, default=False, comment="是否隐藏")
    parent_id = Column(
        BIGINT,
        ForeignKey("system_menu.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True, index=True, comment="父级菜单ID"
    )
    parent_name = Column(String(50), nullable=True, comment="父级菜单名称")
    description = Column(Text, nullable=True, comment="备注")

    parent = relationship(
        "MenuModel",
        cascade='all, delete-orphan',
        primaryjoin="MenuModel.parent_id == MenuModel.id",
        uselist=False
    )





class MenuCRUD(CRUDBase[MenuModel, MenuCreate, MenuUpdate]):
    """
    菜单模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        super().__init__(model=MenuModel, auth=auth)

    async def get_by_id(self, id: int) -> MenuModel:
        obj = await self.get(id=id)
        return obj

    async def get_menu_list(self, search: Dict = None, order: List[str] = None) -> Sequence[MenuModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else []
        return await self.list(search=sql_where, order=order)

    async def set_menu_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids)).values(available=available)
        await self.session.execute(sql)
        await self.session.flush()
