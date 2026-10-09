#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import NewType, Dict, Union
import string, random, base64
from app.core.security import (
    CustomOAuth2PasswordRequestForm,
    verify_password,
    create_jwt_token,
    decode_jwt_token,
    get_password_hash,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import CustomException
from redis.asyncio import Redis
from app.utils.tools import get_random_character, generate_captcha
from app.utils.mail import EmailService
from datetime import timedelta
from app.config.setting import settings
from app.api.v1.system.user.model import UserCRUD
from app.api.v1.system.user.model import UserModel
from app.api.v1.system.auth.schema import Auth, EmailCodeIn, ForgetPasswordIn
from app.api.v1.system.auth.schema import JWTPayload, JWTOut
from datetime import datetime
from fastapi import status


CaptchaKey = NewType('CaptchaKey', str)
CaptchaBase64 = NewType('CaptchaBase64', str)


class LoginService:
    """
    登录模块服务层
    """

    @classmethod
    async def authenticate_user(
            cls,
            login_form: CustomOAuth2PasswordRequestForm,
            session: AsyncSession,
            redis: Redis
    ) -> UserModel:
        if settings.CAPTCHA_ENABLE:
            await CaptchaService.check_captcha(key=login_form.captcha_key, captcha=login_form.captcha, redis=redis)

        auth = Auth(session=session)

        user = await UserCRUD(auth).get_by_username(login_form.username)
        if not verify_password(login_form.password, user.password):
            raise CustomException(
                msg="密码错误",
                code=status.HTTP_401_UNAUTHORIZED
            )

        if not user.available:
            raise CustomException(
                msg="用户已被停用",
                code=status.HTTP_403_FORBIDDEN
            )

        user = await UserCRUD(auth).update_last_login(user.id)
        return user

    @classmethod
    async def create_token(cls, username: str) -> JWTOut:
        expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_jwt_token(payload=JWTPayload(
            sub=username,
            is_refresh=False,
            exp=datetime.utcnow() + expires
        ))
        refresh_token = create_jwt_token(payload=JWTPayload(
            sub=username,
            is_refresh=True,
            exp=datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        ))
        return JWTOut(access_token=access_token, refresh_token=refresh_token, expires_in=expires.total_seconds())

    @classmethod
    async def refresh_token(cls, refresh_token: str) -> JWTOut:
        token_payload = decode_jwt_token(refresh_token)
        if not token_payload.is_refresh:
            raise CustomException(
                msg="非法凭证",
                code=status.HTTP_403_FORBIDDEN,
                status_code=status.HTTP_403_FORBIDDEN
            )

        username = token_payload.sub
        return await cls.create_token(username)


class CaptchaService:
    """
    验证码模块服务层
    """

    @classmethod
    async def get_captcha(cls, redis: Redis) -> Dict[str, Union[CaptchaKey, CaptchaBase64]]:
        if not settings.CAPTCHA_ENABLE:
            raise CustomException(msg="未开启验证码服务", code=status.HTTP_404_NOT_FOUND)

        total_strings = string.digits + string.ascii_lowercase
        random_strings = random.sample(list(total_strings), 4)
        captcha_string = "".join(random_strings)

        captcha = generate_captcha(captcha_string)
        captcha_bytes = captcha.getvalue()
        captcha_base64 = base64.b64encode(captcha_bytes).decode()

        captcha_key = get_random_character()

        await redis.setex(
            f"captcha:{captcha_key}",
            settings.CAPTCHA_EXPIRE_SECONDS,
            captcha_string
        )

        return {
            "key": CaptchaKey(captcha_key),
            "img_base": CaptchaBase64(f"data:image/png;base64,{captcha_base64}")
        }

    @classmethod
    async def check_captcha(cls, key: str, captcha: str, redis: Redis) -> bool:
        if not captcha:
            raise CustomException(msg="验证码不能为空")

        captcha_value = await redis.get(f"captcha:{key}")
        if not captcha_value:
            raise CustomException(msg="验证码已过期", code=status.HTTP_410_GONE)

        if captcha != str(captcha_value):
            raise CustomException(msg="验证码错误")

        await redis.delete(f"captcha:{key}")

        return True


class AuthAccountService:
    """账号相关：邮箱验证码、忘记密码。"""

    @classmethod
    async def _resolve_bound_user(cls, account: str, email: str, session: AsyncSession) -> UserModel:
        """严格校验：账号必须存在，且请求邮箱必须等于用户绑定邮箱。"""
        auth = Auth(session=session)
        crud = UserCRUD(auth)
        user = await crud.get_by_username_or_email(account)
        if not user:
            # 兼容只填邮箱的场景
            user = await crud.get_by_email(email)
        if not user:
            raise CustomException(msg="该邮箱未注册或未绑定账号")
        if not user.email:
            raise CustomException(msg="该账号未绑定邮箱，无法通过邮件重置密码")
        if user.email.strip().lower() != email.strip().lower():
            raise CustomException(msg="邮箱与账号绑定邮箱不一致")
        if not user.available:
            raise CustomException(msg="用户已被停用", code=status.HTTP_403_FORBIDDEN)
        return user

    @classmethod
    async def send_email_code(cls, params: EmailCodeIn, session: AsyncSession, redis: Redis) -> None:
        user = await cls._resolve_bound_user(params.username, str(params.mail), session)
        ok = await EmailService.send_email(
            username=user.username,
            title=params.title,
            mail=user.email,
            redis=redis,
        )
        if not ok:
            raise CustomException(msg="验证码发送失败，请检查邮箱配置或稍后重试")

    @classmethod
    async def forget_password(cls, params: ForgetPasswordIn, session: AsyncSession, redis: Redis) -> None:
        user = await cls._resolve_bound_user(params.username, str(params.email), session)
        result = await EmailService.verify_code(
            username=user.username,
            mail=user.email,
            code=params.code,
            redis=redis,
        )
        if not result["status"]:
            raise CustomException(msg=result["msg"])

        await UserCRUD(Auth(session=session)).change_password(
            user.id,
            get_password_hash(params.new_password),
        )
