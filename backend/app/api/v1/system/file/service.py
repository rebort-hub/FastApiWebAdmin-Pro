#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
from typing import Any, Dict, List
from fastapi import UploadFile
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from app.api.v1.system.auth.schema import Auth
from app.api.v1.system.file.model import FileCRUD
from app.api.v1.system.file.schema import FileCreate, FileId, FileIdList, FileOut
from app.config.setting import settings
from app.core.exceptions import CustomException
from app.core.logger import log
from app.utils.storage import LocalStorage, StorageFactory, StorageType


def _file_type(filename: str) -> str:
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext in {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg", "ico"}:
        return "image"
    if ext in {"doc", "docx", "xls", "xlsx", "ppt", "pptx", "pdf", "txt", "md", "csv"}:
        return "document"
    if ext in {"mp4", "avi", "mov", "wmv", "flv", "mkv"}:
        return "video"
    if ext in {"mp3", "wav", "flac", "aac", "ogg"}:
        return "audio"
    if ext in {"zip", "rar", "7z", "tar", "gz"}:
        return "archive"
    return "other"


class FileService:
    @staticmethod
    def _validate_upload(file: UploadFile, content: bytes) -> None:
        max_bytes = settings.UPLOAD_MAX_SIZE_MB * 1024 * 1024
        if len(content) > max_bytes:
            raise CustomException(msg=f"文件大小超过限制（最大 {settings.UPLOAD_MAX_SIZE_MB}MB）")
        ext = file.filename.rsplit(".", 1)[-1].lower() if file.filename and "." in file.filename else ""
        allowed = settings.upload_allowed_ext_list
        if allowed and ext and ext not in allowed:
            raise CustomException(msg=f"不支持的文件类型: {ext}")

    @classmethod
    async def upload(cls, file: UploadFile, folder: str, auth: Auth) -> Dict[str, Any]:
        if not file or not file.filename:
            raise CustomException(msg="请选择上传文件")
        content = await file.read()
        await file.seek(0)
        cls._validate_upload(file, content)

        storage_type = settings.UPLOAD_STORAGE_TYPE or StorageType.LOCAL
        storage = StorageFactory.create(storage_type)
        result = await storage.upload(file, folder)

        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
        uploader_id = str(auth.user.id) if auth.user else None
        uploader_name = auth.user.username if auth.user else None

        file_id = uuid.uuid4().hex
        file_in = FileCreate(
            id=file_id,
            name=result["key"].split("/")[-1],
            file_path=result["key"],
            extend_name=ext,
            original_name=file.filename,
            content_type=file.content_type,
            file_size=str(round(result["size"] / 1024, 2)),
            storage_type=storage_type,
            file_url=result["url"],
            file_hash=result.get("hash"),
            uploader_id=uploader_id,
            uploader_name=uploader_name,
        )
        await FileCRUD(auth).create(file_in)
        return {
            "id": file_id,
            "url": result["url"],
            "name": file.filename,
            "original_name": file.filename,
            "storage_type": storage_type,
            "file_type": _file_type(file.filename or ""),
            "size": result["size"],
        }

    @classmethod
    async def get_file_list(cls, search: Dict, auth: Auth) -> List[Dict]:
        query = dict(search or {})
        if query.get("name"):
            query["original_name"] = ("like", query.pop("name"))
        rows = await FileCRUD(auth).get_file_list(query, order=["-created_at"])
        return [FileOut.model_validate(row).model_dump() for row in rows]

    @classmethod
    async def get_statistics(cls, auth: Auth) -> dict:
        return await FileCRUD(auth).statistics()

    @classmethod
    async def get_storage_config(cls) -> dict:
        return StorageFactory.get_storage_config()

    @classmethod
    async def download(cls, file_id: str, auth: Auth):
        file_info = await FileCRUD(auth).get(id=file_id)
        data = FileOut.model_validate(file_info).model_dump()
        storage_type = data.get("storage_type") or StorageType.LOCAL
        storage_key = data.get("file_path")
        if storage_type != StorageType.LOCAL and data.get("file_url"):
            return RedirectResponse(data["file_url"])
        storage = StorageFactory.create(storage_type)
        if isinstance(storage, LocalStorage) and storage_key:
            local_path = storage.get_file_path(storage_key)
            if local_path.is_file():
                return FileResponse(path=str(local_path), filename=data.get("original_name"))
        if data.get("file_url"):
            return RedirectResponse(data["file_url"])
        return HTMLResponse(content="文件不存在", status_code=404)

    @classmethod
    async def delete(cls, params: FileId, auth: Auth) -> None:
        file_info = await FileCRUD(auth).get(id=params.id)
        data = FileOut.model_validate(file_info).model_dump()
        storage = StorageFactory.create(data.get("storage_type") or StorageType.LOCAL)
        if data.get("file_path"):
            await storage.delete(data["file_path"])
        await FileCRUD(auth).delete_by_id(params.id)

    @classmethod
    async def batch_delete(cls, params: FileIdList, auth: Auth) -> int:
        count = 0
        for file_id in params.ids:
            try:
                await cls.delete(FileId(id=file_id), auth)
                count += 1
            except Exception as exc:
                log.warning(f"删除文件 {file_id} 失败: {exc}")
        return count

    @classmethod
    async def serve_local_file(cls, file_path: str):
        storage = StorageFactory.create(StorageType.LOCAL)
        if not isinstance(storage, LocalStorage):
            return HTMLResponse(content="文件不存在", status_code=404)
        local_file = storage.get_file_path(file_path)
        if not local_file.is_file() or not local_file.resolve().is_relative_to(storage.base_path.resolve()):
            return HTMLResponse(content="文件不存在", status_code=404)
        return FileResponse(path=str(local_file))
