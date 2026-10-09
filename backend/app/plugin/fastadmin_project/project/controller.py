#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse
from app.core.router_class import OperationLogRoute
from app.core.params import PaginationQueryParams, ProjectQueryParams
from app.core.dependencies import AuthPermission
from app.api.v1.system.auth.schema import Auth
from app.utils.response import SuccessResponse, PaginationResponse
from app.plugin.fastadmin_project.project.service import ProjectService
from app.plugin.fastadmin_project.project.schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectBatchSetAvailable,
)


ProjectRouter = APIRouter(route_class=OperationLogRoute, tags=["项目管理"])


@ProjectRouter.get("/list", summary="查询项目", description="查询项目列表")
async def get_project_list(
        paging_query: PaginationQueryParams = Depends(),
        project_query: ProjectQueryParams = Depends(),
        auth: Auth = Depends(AuthPermission(permissions=["project:query"])),
) -> JSONResponse:
    data = await ProjectService.get_project_list(project_query.__dict__, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@ProjectRouter.get("/detail", summary="查询项目详情", description="查询项目详情")
async def get_project_detail(
        id: int = Query(..., description="项目ID"),
        auth: Auth = Depends(AuthPermission(permissions=["project:query"])),
) -> JSONResponse:
    data = await ProjectService.get_project_detail(id, auth)
    return SuccessResponse(data)


@ProjectRouter.get("/options", summary="查询项目选项", description="查询项目下拉选项")
async def get_project_options(
        paging_query: PaginationQueryParams = Depends(),
        project_query: ProjectQueryParams = Depends(),
        auth: Auth = Depends(AuthPermission(permissions=["project:options"])),
) -> JSONResponse:
    data = await ProjectService.get_project_options(project_query.__dict__, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@ProjectRouter.post("/create", summary="创建项目", description="创建项目")
async def create_project(
        project_in: ProjectCreate,
        auth: Auth = Depends(AuthPermission(permissions=["project:create"])),
) -> JSONResponse:
    data = await ProjectService.create_project(project_in, auth)
    return SuccessResponse(data, msg="创建成功")


@ProjectRouter.post("/update", summary="修改项目", description="修改项目")
async def update_project(
        project_in: ProjectUpdate,
        auth: Auth = Depends(AuthPermission(permissions=["project:update"])),
) -> JSONResponse:
    data = await ProjectService.update_project(project_in, auth)
    return SuccessResponse(data, msg="修改成功")


@ProjectRouter.post("/delete", summary="删除项目", description="删除项目")
async def delete_project(
        id: int = Query(..., description="项目ID"),
        auth: Auth = Depends(AuthPermission(permissions=["project:delete"])),
) -> JSONResponse:
    await ProjectService.delete_project(id, auth)
    return SuccessResponse(msg="删除成功")


@ProjectRouter.post("/batch/enable", summary="批量启用项目", description="批量启用项目")
async def batch_enable_project(
        data: ProjectBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["project:update"])),
) -> JSONResponse:
    await ProjectService.set_project_available(data.ids, available=True, auth=auth)
    return SuccessResponse(msg="启用成功")


@ProjectRouter.post("/batch/disable", summary="批量停用项目", description="批量停用项目")
async def batch_disable_project(
        data: ProjectBatchSetAvailable,
        auth: Auth = Depends(AuthPermission(permissions=["project:update"])),
) -> JSONResponse:
    await ProjectService.set_project_available(data.ids, available=False, auth=auth)
    return SuccessResponse(msg="停用成功")
