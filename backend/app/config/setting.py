#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""系统配置"""

from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Union
from urllib.parse import quote_plus
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from app.config.path_conf import ENV_DIR, FILES_DIR, STATIC_DIR, TEMP_DIR


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        """优先读取 env"""
        return init_settings, dotenv_settings, env_settings, file_secret_settings

    # ---------- 环境----------
    ENVIRONMENT: Literal["dev", "prod", "test"] = "dev"

    DEBUG: bool = True
    RELOAD: bool = False
    DEMO: bool = False
    DEMO_WHITE_LIST_PATH: List[str] = Field(
        default_factory=lambda: [
            "/api/system/auth/login",
            "/api/system/auth/token/refresh",
            "/api/system/auth/captcha/get",
            "/api/system/auth/email/code",
            "/api/system/auth/forget-password",
        ]
    )

    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8085
    API_PREFIX: str = "/api"

    TITLE: str = "FastApiWebAdmin-Pro 专业版"
    VERSION: str = "2.0.0"
    DESCRIPTION: Optional[str] = None
    DOCS_URL: Optional[str] = "/docs"
    OPENAPI_URL: str = "/openapi.json"
    REDOC_URL: Optional[str] = "/redoc"
    OPENAPI_PREFIX: str = ""

    CORS_ORIGIN_ENABLE: bool = True
    ALLOW_ORIGINS: List[str] = Field(default_factory=lambda: ["*"])
    ALLOW_METHODS: List[str] = Field(default_factory=lambda: ["*"])
    ALLOW_HEADERS: List[str] = Field(default_factory=lambda: ["*"])
    ALLOW_CREDENTIALS: bool = True

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    STATIC_ENABLE: bool = True
    STATIC_URL: str = "/static"
    TEMP_ENABLE: bool = False
    TEMP_URL: str = "/temp"

    SQL_DB_ENABLE: bool = True
    DATABASE_TYPE: Literal["postgres", "mysql"] = "postgres"
    DATABASE_HOST: str = "127.0.0.1"
    DATABASE_PORT: int = 5432
    DATABASE_USER: str = "postgres"
    DATABASE_PASSWORD: str = "Rebort"
    DATABASE_NAME: str = "fastapiwebadmin-pro"
    SQL_DATABASE_URI: Optional[str] = None

    REDIS_ENABLE: bool = True
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    REDIS_DB: int = 0
    REDIS_URI: Optional[str] = None

    AUTO_CREATE_TABLES: bool = True
    AUTO_SEED_DATA: bool = True
    PLUGIN_PREFIX: str = "fastadmin_"

    CAPTCHA_ENABLE: bool = True
    CAPTCHA_EXPIRE_SECONDS: int = 60

    # ---------- 邮件（忘记密码邮箱验证码） ----------
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 465
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_FROM_ADDR: str = ""
    EMAIL_FROM_NAME: str = ""
    EMAIL_USE_SSL: bool = True
    EMAIL_CODE_EXPIRE_SECONDS: int = 120

    REQUEST_LOG_RECORD: bool = True
    OPERATION_LOG_RECORD: bool = True
    OPERATION_RECORD_METHOD: List[str] = Field(
        default_factory=lambda: ["POST", "PUT", "PATCH", "DELETE"]
    )
    IGNORE_OPERATION_FUNCTION: List[str] = Field(
        default_factory=lambda: ["get_captcha_for_login"]
    )

    # ---------- 文件上传 / 对象存储 ----------
    UPLOAD_STORAGE_TYPE: str = "local"
    UPLOAD_MAX_SIZE_MB: int = 100
    UPLOAD_ALLOWED_EXTENSIONS: str = (
        "jpg,jpeg,png,gif,bmp,webp,svg,ico,"
        "pdf,doc,docx,xls,xlsx,ppt,pptx,txt,md,csv,"
        "zip,rar,7z,mp4,mp3,wav"
    )
    UPLOAD_LOCAL_PATH: str = ""
    UPLOAD_URL_PREFIX: str = "/api/files"

    ALIYUN_OSS_ACCESS_KEY: str = ""
    ALIYUN_OSS_SECRET_KEY: str = ""
    ALIYUN_OSS_BUCKET: str = ""
    ALIYUN_OSS_ENDPOINT: str = ""
    ALIYUN_OSS_DOMAIN: str = ""

    TENCENT_COS_SECRET_ID: str = ""
    TENCENT_COS_SECRET_KEY: str = ""
    TENCENT_COS_BUCKET: str = ""
    TENCENT_COS_REGION: str = ""
    TENCENT_COS_DOMAIN: str = ""

    QINIU_ACCESS_KEY: str = ""
    QINIU_SECRET_KEY: str = ""
    QINIU_BUCKET: str = ""
    QINIU_DOMAIN: str = ""

    MINIO_ENDPOINT: str = ""
    MINIO_ACCESS_KEY: str = ""
    MINIO_SECRET_KEY: str = ""
    MINIO_BUCKET: str = ""
    MINIO_SECURE: bool = False

    @property
    def upload_local_dir(self) -> str:
        return self.UPLOAD_LOCAL_PATH or str(FILES_DIR)

    @property
    def upload_allowed_ext_list(self) -> List[str]:
        return [x.strip().lower() for x in self.UPLOAD_ALLOWED_EXTENSIONS.split(",") if x.strip()]

    @property
    def STATIC_ROOT(self) -> Path:
        return STATIC_DIR

    @property
    def TEMP_ROOT(self) -> Path:
        return TEMP_DIR

    @property
    def SQL_DB_URL(self) -> str:
        if self.SQL_DATABASE_URI:
            return self.SQL_DATABASE_URI
        pwd = quote_plus(self.DATABASE_PASSWORD)
        if self.DATABASE_TYPE == "postgres":
            return (
                f"postgresql+asyncpg://{self.DATABASE_USER}:{pwd}"
                f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            )
        return (
            f"mysql+asyncpg://{self.DATABASE_USER}:{pwd}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def SQL_DB_URL_SYNC(self) -> str:
        if self.SQL_DATABASE_URI:
            url = self.SQL_DATABASE_URI
            return url.replace("+asyncpg", "").replace("+asyncmy", "+pymysql")
        pwd = quote_plus(self.DATABASE_PASSWORD)
        if self.DATABASE_TYPE == "postgres":
            return (
                f"postgresql+psycopg2://{self.DATABASE_USER}:{pwd}"
                f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
            )
        return (
            f"mysql+pymysql://{self.DATABASE_USER}:{pwd}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def REDIS_URL(self) -> str:
        if self.REDIS_URI:
            return self.REDIS_URI
        auth = ""
        if self.REDIS_USER or self.REDIS_PASSWORD:
            auth = f"{self.REDIS_USER}:{quote_plus(self.REDIS_PASSWORD)}@"
        return f"redis://{auth}{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"

    @property
    def swagger_static_prefix(self) -> str:
        return self.STATIC_URL.rstrip("/")

    @property
    def MIDDLEWARE(self) -> List[Optional[str]]:
        return [
            "app.core.middlewares.CustomCORSMiddleware" if self.CORS_ORIGIN_ENABLE else None,
            "app.core.middlewares.RequestLogMiddleware" if self.REQUEST_LOG_RECORD else None,
            "app.core.middlewares.DemoEnvMiddleware" if self.DEMO else None,
        ]

    @property
    def get_backend_app_attributes(self) -> Dict[str, Union[str, bool, None]]:
        return {
            "debug": self.DEBUG,
            "title": self.TITLE,
            "version": self.VERSION,
            "description": self.DESCRIPTION,
            "docs_url": self.DOCS_URL,
            "openapi_url": self.OPENAPI_URL,
            "redoc_url": self.REDOC_URL,
            "openapi_prefix": self.OPENAPI_PREFIX,
        }

    @property
    def get_cors_middleware_attributes(self) -> Dict[str, Union[List[str], bool]]:
        return {
            "allow_origins": self.ALLOW_ORIGINS,
            "allow_methods": self.ALLOW_METHODS,
            "allow_headers": self.ALLOW_HEADERS,
            "allow_credentials": self.ALLOW_CREDENTIALS,
        }


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
