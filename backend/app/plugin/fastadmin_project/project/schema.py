#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Optional, List
from pydantic import BaseModel, ConfigDict
from app.shared.schemas.base import CustomOutSchema


class Project(BaseModel):
    name: str
    order: Optional[int] = 1
    description: Optional[str] = None


class ProjectCreate(Project):
    ...


class ProjectUpdate(Project):
    id: int
    available: Optional[bool] = True


class ProjectBatchSetAvailable(BaseModel):
    ids: List[int] = []


class ProjectOut(Project, CustomOutSchema):
    available: Optional[bool] = True


class ProjectSimpleOut(ProjectOut):
    ...


class ProjectOptionsOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: Optional[str] = None
    available: Optional[bool] = True
