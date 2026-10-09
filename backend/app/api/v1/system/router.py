#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter
from app.api.v1.system.auth.controller import AuthRouter
from app.api.v1.system.menu.controller import MenuRouter
from app.api.v1.system.dept.controller import DeptRouter
from app.api.v1.system.position.controller import PositionRouter
from app.api.v1.system.role.controller import RoleRouter
from app.api.v1.system.user.controller import UserRouter
from app.api.v1.system.log.controller import LogRouter
from app.api.v1.system.file.controller import FileRouter


SystemRouter = APIRouter()

SystemRouter.include_router(AuthRouter, prefix="/auth", tags=["系统认证"])
SystemRouter.include_router(MenuRouter, prefix="/menu", tags=["菜单模块"])
SystemRouter.include_router(DeptRouter, prefix="/dept", tags=["部门模块"])
SystemRouter.include_router(PositionRouter, prefix="/position", tags=["岗位模块"])
SystemRouter.include_router(RoleRouter, prefix="/role", tags=["角色模块"])
SystemRouter.include_router(UserRouter, prefix="/user", tags=["用户模块"])
SystemRouter.include_router(LogRouter, prefix="/log", tags=["操作日志"])
SystemRouter.include_router(FileRouter, prefix="/file", tags=["文件管理"])
