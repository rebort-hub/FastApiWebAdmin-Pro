#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import APIRouter, Depends, File, Query, UploadFile
from fastapi.responses import JSONResponse
from app.api.v1.system.auth.schema import Auth
from app.api.v1.system.file.schema import FileId, FileIdList, FileQuery
from app.api.v1.system.file.service import FileService
from app.core.dependencies import AuthPermission
from app.core.params import PaginationQueryParams
from app.core.router_class import OperationLogRoute
from app.utils.response import PaginationResponse, SuccessResponse

FileRouter = APIRouter(route_class=OperationLogRoute)
FileAccessRouter = APIRouter()


@FileRouter.post("/upload", summary="上传文件")
async def upload_file(
    file: UploadFile = File(...),
    folder: str = Query(default=""),
    auth: Auth = Depends(AuthPermission(permissions=["system:file:upload"])),
) -> JSONResponse:
    data = await FileService.upload(file, folder, auth)
    return SuccessResponse(data)


@FileRouter.post("/list", summary="文件列表")
async def file_list(
    params: FileQuery,
    paging_query: PaginationQueryParams = Depends(),
    auth: Auth = Depends(AuthPermission(permissions=["system:file:query"])),
) -> JSONResponse:
    search = {k: v for k, v in params.model_dump().items() if v is not None}
    data = await FileService.get_file_list(search, auth)
    return PaginationResponse(data, page=paging_query.page, page_size=paging_query.page_size)


@FileRouter.get("/statistics", summary="文件统计")
async def file_statistics(
    auth: Auth = Depends(AuthPermission(permissions=["system:file:query"])),
) -> JSONResponse:
    return SuccessResponse(await FileService.get_statistics(auth))


@FileRouter.get("/storage-config", summary="存储配置")
async def storage_config(
    auth: Auth = Depends(AuthPermission(permissions=["system:file:query"])),
) -> JSONResponse:
    return SuccessResponse(await FileService.get_storage_config())


@FileRouter.get("/download/{file_id}", summary="下载文件")
async def download_file(
    file_id: str,
    auth: Auth = Depends(AuthPermission(permissions=["system:file:download"])),
):
    return await FileService.download(file_id, auth)


@FileRouter.post("/deleted", summary="删除文件")
async def delete_file(
    params: FileId,
    auth: Auth = Depends(AuthPermission(permissions=["system:file:delete"])),
) -> JSONResponse:
    await FileService.delete(params, auth)
    return SuccessResponse()


@FileRouter.post("/deleteList", summary="批量删除")
async def delete_file_list(
    params: FileIdList,
    auth: Auth = Depends(AuthPermission(permissions=["system:file:delete"])),
) -> JSONResponse:
    count = await FileService.batch_delete(params, auth)
    return SuccessResponse({"count": count})


@FileAccessRouter.get("/files/{file_path:path}", summary="本地存储文件访问")
async def access_local_file(file_path: str):
    return await FileService.serve_local_file(file_path)
