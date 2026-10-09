#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, Sequence
from sqlalchemy import Column, String, select, delete, func
from app.api.v1.system.auth.schema import Auth
from app.api.v1.system.file.schema import FileCreate
from app.models.base import Model, TimestampMixin
from app.shared.crud.base import CRUDBase
from app.utils.tools import dict_to_search_sql


class FileModel(TimestampMixin, Model):
    __tablename__ = "system_file"
    __table_args__ = {"comment": "文件信息表"}

    id = Column(String(64), primary_key=True, comment="文件ID")
    name = Column(String(255), nullable=True, comment="存储文件名")
    file_path = Column(String(512), nullable=True, comment="存储 key")
    extend_name = Column(String(64), nullable=True, index=True, comment="扩展名")
    original_name = Column(String(255), nullable=True, comment="原始文件名")
    content_type = Column(String(128), nullable=True, comment="MIME")
    file_size = Column(String(32), nullable=True, comment="大小(KB)")
    storage_type = Column(String(32), nullable=True, default="local", comment="存储类型")
    file_url = Column(String(1000), nullable=True, comment="访问 URL")
    file_hash = Column(String(64), nullable=True, comment="MD5")
    uploader_id = Column(String(32), nullable=True, comment="上传者 ID")
    uploader_name = Column(String(64), nullable=True, comment="上传者")


class FileCRUD(CRUDBase[FileModel, FileCreate, None]):
    def __init__(self, auth: Auth) -> None:
        super().__init__(model=FileModel, auth=auth)

    async def get_file_list(self, search: Dict = None, order: List[str] = None) -> Sequence[FileModel]:
        sql_where = dict_to_search_sql(self.model, search) if search else []
        return await self.list(search=sql_where, order=order or ["-created_at"])

    async def delete_by_id(self, file_id: str) -> None:
        sql = delete(self.model).where(self.model.id == file_id)
        await self.session.execute(sql)
        await self.session.flush()

    async def statistics(self) -> dict:
        total = await self.session.scalar(select(func.count()).select_from(self.model))
        rows = await self.session.execute(select(self.model.file_size))
        total_size = 0.0
        for size in rows.scalars().all():
            try:
                total_size += float(size or 0)
            except (TypeError, ValueError):
                pass
        return {"total_count": total or 0, "total_size_kb": round(total_size, 2)}
