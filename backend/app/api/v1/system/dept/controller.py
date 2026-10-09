#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.core.params import PaginationQueryParams
from app.core.dependencies import AuthPermission
from app.api.v1.system.dept.service import DeptService
from app.api.v1.system.user.service import UserService
from app.api.v1.system.auth.schema import Auth
from app.utils.response import SuccessResponse, PaginationResponse
from app.api.v1.system.dept.schema import (    DeptCreate,
    DeptUpdate,
    DeptBatchSetAvailable
)


DeptRouter = APIRouter(route_class=OperationLogRoute)


@DeptRouter.get("/list", summary="查询部门", description="查询部门")
async def get_dept_list(
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:query"])),
) -> JSONResponse:
    data = await DeptService.get_dept_list(auth)
    return SuccessResponse(data)


@DeptRouter.get("/detail", summary="查询部门详情", description="查询部门详情")
async def get_dept_detail(
        id: int = Query(..., description="部门ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:query"])),
) -> JSONResponse:
    data = await DeptService.get_dept_detail(id, auth)
    return SuccessResponse(data)


@DeptRouter.get("/options", summary="查询部门选项", description="查询部门选项")
async def get_dept_options(
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:options"])),
) -> JSONResponse:
    data = await DeptService.get_dept_options(auth)
    return SuccessResponse(data)


@DeptRouter.get("/users", summary="查询部门所属用户", description="按部门查询所属用户列表")
async def get_dept_users(
        paging_query: PaginationQueryParams = Depends(),
        dept_id: int = Query(..., description="部门ID"),
        username: Optional[str] = Query(None, description="用户名"),
        name: Optional[str] = Query(None, description="姓名"),
        available: Optional[bool] = Query(None, description="状态"),
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:query"])),
) -> JSONResponse:
    search = {
        "dept_id": dept_id,
        "username": ("like", username),
        "name": ("like", name),
        "available": available,
    }
    data = await UserService.get_user_list(search, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@DeptRouter.post("/create", summary="创建部门", description="创建部门")
async def create_dept(
        dept_in: DeptCreate,
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:create"])),
) -> JSONResponse:
    data = await DeptService.create_dept(dept_in, auth)
    return SuccessResponse(data, msg="创建成功")


@DeptRouter.post("/update", summary="修改部门", description="修改部门")
async def update_dept(
        dept_in: DeptUpdate,
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:update"])),
) -> JSONResponse:
    data = await DeptService.update_dept(dept_in, auth)
    return SuccessResponse(data, msg="修改成功")


@DeptRouter.post("/delete", summary="删除部门", description="删除部门")
async def delete_dept(
        id: int = Query(..., description="部门ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:delete"])),
) -> JSONResponse:
    await DeptService.delete_dept(id, auth)
    return SuccessResponse(msg="删除成功")


@DeptRouter.post("/batch/enable", summary="批量启用菜单", description="批量启用菜单")
async def batch_enabled_dept(
        data: DeptBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:update"])),
) -> JSONResponse:
    await DeptService.enable_dept(data.ids, auth)
    return SuccessResponse(msg="启用成功")


@DeptRouter.post("/batch/disable", summary="批量停用菜单", description="批量停用菜单")
async def batch_disable_dept(
        data: DeptBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:dept:update"])),
) -> JSONResponse:
    await DeptService.disable_dept(data.ids, auth)
    return SuccessResponse(msg="停用成功")
