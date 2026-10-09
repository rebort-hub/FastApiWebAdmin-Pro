#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List
from app.api.v1.system.auth.schema import Auth
from app.plugin.fastadmin_project.project.model import ProjectCRUD
from app.plugin.fastadmin_project.project.schema import (
    ProjectCreate,
    ProjectUpdate,
    ProjectOut,
    ProjectSimpleOut,
    ProjectOptionsOut,
)


class ProjectService:
    """项目管理服务层"""

    @classmethod
    async def get_project_detail(cls, id: int, auth: Auth) -> Dict:
        obj = await ProjectCRUD(auth).get_by_id(id)
        return ProjectSimpleOut.model_validate(obj).model_dump()

    @classmethod
    async def get_project_list(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await ProjectCRUD(auth).get_project_list(search, order=["order"])
        return [ProjectOut.model_validate(obj).model_dump() for obj in data]

    @classmethod
    async def create_project(cls, project_in: ProjectCreate, auth: Auth) -> Dict:
        obj = await ProjectCRUD(auth).create(obj_in=project_in)
        return ProjectOut.model_validate(obj).model_dump()

    @classmethod
    async def update_project(cls, project_in: ProjectUpdate, auth: Auth) -> Dict:
        obj = await ProjectCRUD(auth).update(id=project_in.id, obj_in=project_in)
        return ProjectOut.model_validate(obj).model_dump()

    @classmethod
    async def delete_project(cls, id: int, auth: Auth) -> None:
        await ProjectCRUD(auth).delete(ids=[id])

    @classmethod
    async def set_project_available(cls, ids: List[int], available: bool, auth: Auth) -> None:
        await ProjectCRUD(auth).set_project_available(ids=ids, available=available)

    @classmethod
    async def get_project_options(cls, search: Dict, auth: Auth) -> List[Dict]:
        data = await ProjectCRUD(auth).get_project_list(search, order=["order"])
        return [ProjectOptionsOut.model_validate(obj).model_dump() for obj in data]
