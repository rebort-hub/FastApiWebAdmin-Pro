#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Union, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime
from app.api.v1.system.user.schema import UserPermissionOut
from sqlalchemy.ext.asyncio import AsyncSession


class AuthUser(UserPermissionOut):
    ...


class Auth(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    user: Optional[AuthUser] = None
    check_data_scope: bool = False
    session: AsyncSession


class JWTPayload(BaseModel):
    sub: str
    is_refresh: bool
    exp: Union[datetime, int]


class RefreshTokenPayload(BaseModel):
    refresh_token: str


class JWTOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    expires_in: int


class CaptchaOut(BaseModel):
    key: str
    img_base: str


class EmailCodeIn(BaseModel):
    username: str = Field(..., min_length=1, max_length=150, description="用户名或绑定邮箱")
    title: str = Field(..., min_length=1, max_length=32, description="邮件标题")
    mail: EmailStr = Field(..., description="用户绑定邮箱")


class ForgetPasswordIn(BaseModel):
    username: str = Field(..., min_length=1, max_length=150, description="用户名或绑定邮箱")
    email: EmailStr = Field(..., description="用户绑定邮箱")
    code: str = Field(..., min_length=4, max_length=16, description="邮箱验证码")
    new_password: str = Field(..., min_length=6, max_length=128, description="新密码（前端 MD5）")
