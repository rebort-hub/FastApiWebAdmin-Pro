#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.core.params import PaginationQueryParams, RoleQueryParams
from app.core.dependencies import AuthPermission
from app.utils.response import SuccessResponse, PaginationResponse
from app.api.v1.system.role.service import RoleService
from app.api.v1.system.auth.schema import Auth
from app.api.v1.system.role.schema import (    RoleCreate,
    RoleUpdate,
    RoleBatchSetAvailable,
    RolePermissionSetting
)


RoleRouter = APIRouter(route_class=OperationLogRoute)


@RoleRouter.get("/list", summary="查询角色", description="查询角色")
async def get_role_list(
        paging_query: PaginationQueryParams = Depends(),
        role_query: RoleQueryParams = Depends(),
        auth: Auth = Depends(AuthPermission(permissions=["system:role:query"])),
) -> JSONResponse:
    search = role_query.__dict__
    data = await RoleService.get_role_list(search, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@RoleRouter.get("/detail", summary="查询角色详情", description="查询角色详情")
async def get_role_detail(
        id: int = Query(..., description="角色ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:role:query"])),
) -> JSONResponse:
    data = await RoleService.get_role_detail(id, auth)
    return SuccessResponse(data)


@RoleRouter.get("/options", summary="查询角色选项", description="查询角色选项")
async def get_position_options(
        paging_query: PaginationQueryParams = Depends(),
        role_query: RoleQueryParams = Depends(),
        auth: Auth = Depends(AuthPermission(permissions=["system:role:options"])),
) -> JSONResponse:
    search = role_query.__dict__
    data = await RoleService.get_role_options(search, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@RoleRouter.post("/create", summary="创建角色", description="创建角色")
async def create_role(
        role_in: RoleCreate,
        auth: Auth = Depends(AuthPermission(permissions=["system:role:create"])),
) -> JSONResponse:
    data = await RoleService.create_role(role_in, auth)
    return SuccessResponse(data, msg="创建成功")


@RoleRouter.post("/update", summary="修改角色", description="修改角色")
async def update_role(
        role_in: RoleUpdate,
        auth: Auth = Depends(AuthPermission(permissions=["system:role:update"])),
) -> JSONResponse:
    data = await RoleService.update_role(role_in, auth)
    return SuccessResponse(data, msg="修改成功")


@RoleRouter.post("/delete", summary="删除角色", description="删除角色")
async def delete_role(
        id: int = Query(..., description="角色ID"),
        auth: Auth = Depends(AuthPermission(permissions=["system:role:delete"])),
) -> JSONResponse:
    await RoleService.delete_role(id, auth)
    return SuccessResponse(msg="删除成功")


@RoleRouter.post("/batch/enable", summary="批量启用角色", description="批量启用角色")
async def batch_enabled_role(
        data: RoleBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:role:update"])),
) -> JSONResponse:
    await RoleService.set_role_available(data.ids, available=True, auth=auth)
    return SuccessResponse(msg="启用成功")


@RoleRouter.post("/batch/disable", summary="批量停用角色", description="批量停用角色")
async def batch_disable_role(
        data: RoleBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["system:role:update"])),
) -> JSONResponse:
    await RoleService.set_role_available(data.ids, available=False, auth=auth)
    return SuccessResponse(msg="停用成功")


@RoleRouter.get("/permission", summary="查询角色权限", description="查询角色权限")
async def get_role_permission(
    id: int = Query(..., description="角色ID"),
    auth: Auth = Depends(AuthPermission(permissions=["system:role:query"])),
) -> JSONResponse:
    data = await RoleService.get_role_permission(id, auth)
    return SuccessResponse(data)


@RoleRouter.post("/permission/setting", summary="设置角色权限", description="设置角色权限")
async def set_role_permission(
        permission_in: RolePermissionSetting,
        auth: Auth = Depends(AuthPermission(permissions=["system:role:permission"])),
) -> JSONResponse:
    await RoleService.set_role_permission(permission_in, auth)
    return SuccessResponse(msg="授权成功")
