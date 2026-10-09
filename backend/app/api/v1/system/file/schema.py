#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
from app.core.validator import DateTimeStr


class FileCreate(BaseModel):
    id: str
    name: Optional[str] = None
    file_path: Optional[str] = None
    extend_name: Optional[str] = None
    original_name: Optional[str] = None
    content_type: Optional[str] = None
    file_size: Optional[str] = None
    storage_type: Optional[str] = "local"
    file_url: Optional[str] = None
    file_hash: Optional[str] = None
    uploader_id: Optional[str] = None
    uploader_name: Optional[str] = None


class FileOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: Optional[str] = None
    file_path: Optional[str] = None
    extend_name: Optional[str] = None
    original_name: Optional[str] = None
    content_type: Optional[str] = None
    file_size: Optional[str] = None
    storage_type: Optional[str] = None
    file_url: Optional[str] = None
    file_hash: Optional[str] = None
    uploader_id: Optional[str] = None
    uploader_name: Optional[str] = None
    created_at: Optional[DateTimeStr] = None
    updated_at: Optional[DateTimeStr] = None


class FileId(BaseModel):
    id: str


class FileIdList(BaseModel):
    ids: List[str] = Field(default_factory=list)


class FileQuery(BaseModel):
    name: Optional[str] = None
    storage_type: Optional[str] = None
