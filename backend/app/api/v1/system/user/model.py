#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据层"""

from app.models.base import Model, CustomMixin, TimestampMixin
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, BIGINT, ForeignKey
from app.api.v1.system.association.model import RoleMenusModel, RoleDeptsModel, UserPositionsModel, UserRolesModel
from typing import Dict, List, Optional, Sequence
from app.shared.crud.base import CRUDBase
from app.api.v1.system.user.schema import UserCreate, UserUpdate
from app.api.v1.system.auth.schema import Auth
from app.utils.tools import dict_to_search_sql
from datetime import datetime
from sqlalchemy import update
from app.api.v1.system.role.model import RoleCRUD
from app.api.v1.system.position.model import PositionCRUD


class UserModel(CustomMixin, Model):
    __tablename__ = "system_user"
    __table_args__ = {"comment": "用户表", "quote": True}

    username = Column(String(150), nullable=False, comment="用户名")
    password = Column(String(128), nullable=False, comment="密码")
    name = Column(String(40), nullable=False, comment="姓名")
    mobile = Column(String(20), nullable=True, comment="手机号")
    email = Column(String(255), nullable=True, comment="邮箱")
    gender = Column(Integer, default=1, nullable=False, comment="性别")
    avatar = Column(String(255), nullable=True, comment="头像", default="https://gw.alipayobjects.com/zos/rmsportal/BiazfanxmamNRoxxVxka.png")
    available = Column(Boolean, default=True, nullable=False, comment="是否可用")
    is_superuser = Column(Boolean, default=False, nullable=False, comment="是否超管")
    last_login = Column(DateTime, nullable=True, comment="最近登录时间")
    dept_id = Column(
        BIGINT,
        ForeignKey('system_dept.id', ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True, index=True, comment="部门ID"
    )

    dept = relationship('DeptModel', primaryjoin="UserModel.dept_id == DeptModel.id", lazy="select", uselist=False)
    roles = relationship("RoleModel", secondary=UserRolesModel.__tablename__, lazy="joined", uselist=True)
    positions = relationship("PositionModel", secondary=UserPositionsModel.__tablename__, lazy="joined", uselist=True)




class UserCRUD(CRUDBase[UserModel, UserCreate, UserUpdate]):
    """
    用户模块数据查询层
    """
    def __init__(self, auth: Auth) -> None:
        self.auth = auth
        super().__init__(model=UserModel, auth=auth)

    async def get_by_id(self, id: int) -> UserModel:
        obj = await self.get(id=id)
        return obj

    async def get_by_username(self, username: str) -> UserModel:
        obj = await self.get(username=username)
        return obj

    async def get_by_email(self, email: str) -> Optional[UserModel]:
        from sqlalchemy import select, func

        sql = select(self.model).where(func.lower(self.model.email) == email.strip().lower())
        result = await self.session.execute(sql)
        return result.scalars().unique().first()

    async def get_by_username_or_email(self, account: str) -> Optional[UserModel]:
        from sqlalchemy import select, func, or_

        value = account.strip()
        sql = select(self.model).where(
            or_(
                self.model.username == value,
                func.lower(self.model.email) == value.lower(),
            )
        )
        result = await self.session.execute(sql)
        return result.scalars().unique().first()

    async def get_user_list(self, search: Dict = None) -> Sequence[UserModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else []
        return await self.list(search=sql_where)

    async def update_last_login(self, id: int) -> UserModel:
        obj = await self.update(id, obj_in={"last_login": datetime.now()})
        return obj

    async def set_user_available(self, ids: List[int], available: bool) -> None:
        sql = update(self.model).where(self.model.id.in_(ids)).values(available=available)
        await self.session.execute(sql)
        await self.session.flush()

    async def set_user_roles(self, user_ids: List[int], role_ids: List[int]) -> None:
        users = await self.get_user_list(search={"id": ("in", user_ids)})
        roles = await RoleCRUD(self.auth).get_role_list(search={"id": ("in", role_ids)})

        for user in users:
            user.roles.clear()
            for role in roles:
                user.roles.append(role)

        await self.session.flush()

    async def set_user_positions(self, user_ids: List[int], position_ids: List[int]) -> None:
        user_objs = await self.get_user_list(search={"id": ("in", user_ids)})
        position_objs = await PositionCRUD(self.auth).get_position_list(search={"id": ("in", position_ids)})

        for user_obj in user_objs:
            user_obj.positions.clear()
            for position_obj in position_objs:
                user_obj.positions.append(position_obj)

        await self.session.flush()

    async def change_password(self, id: int, password_hash: str):
        obj = await self.update(id, obj_in={"password": password_hash})
        return obj
