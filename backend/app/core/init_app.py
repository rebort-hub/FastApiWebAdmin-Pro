#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fastapi import FastAPI, applications
from app.config.setting import settings
from app.utils.tools import import_module
from app.core.exceptions import (
    CustomException,
    CustomExceptionHandler,
    HTTPException,
    HttpExceptionHandler,
    RequestValidationError,
    ValidationExceptionHandler,
    SQLAlchemyError,
    SQLAlchemyExceptionHandler,
    AllExceptionHandler,
)
from app.api import ApiRouter
from contextlib import asynccontextmanager
from app.core.database import dispose_async_engine, redis_connect
from app.scripts.initialize import InitializeData
from starlette.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """应用生命周期"""
    from app.core.logger import log

    log.info("应用启动中...")
    init_data: InitializeData | None = None
    try:
        if settings.SQL_DB_ENABLE:
            init_data = InitializeData()
            init_data.init_db()
            log.info("数据库初始化成功")
    except Exception as exc:
        log.exception(f"数据库初始化失败: {exc}")
        if settings.ENVIRONMENT == "dev":
            log.warning("开发环境将继续启动，请检查数据库配置与种子数据")
        else:
            raise
    finally:
        if init_data is not None:
            init_data.dispose()

    if settings.REDIS_ENABLE:
        await redis_connect(app, status=True)

    log.info("应用启动完成")
    try:
        yield
    finally:
        if settings.REDIS_ENABLE:
            await redis_connect(app, status=False)
        if settings.SQL_DB_ENABLE:
            await dispose_async_engine()
        log.info("应用已关闭")
        from app.core.logger import cleanup_logging

        cleanup_logging()


def register_middlewares(app: FastAPI) -> None:
    """
    注册中间件
    """
    for middleware in settings.MIDDLEWARE[::-1]:
        if not middleware:
            continue
        middleware = import_module(middleware)
        app.add_middleware(middleware)


def register_exceptions(app: FastAPI) -> None:
    """
    异常捕捉
    """
    app.add_exception_handler(CustomException, CustomExceptionHandler)
    app.add_exception_handler(HTTPException, HttpExceptionHandler)
    app.add_exception_handler(RequestValidationError, ValidationExceptionHandler)
    app.add_exception_handler(SQLAlchemyError, SQLAlchemyExceptionHandler)
    app.add_exception_handler(Exception, AllExceptionHandler)


def register_routers(app: FastAPI, prefix: str = "/") -> None:
    """
    注册根路由
    """
    from app.api.v1.system.router import SystemRouter
    from app.core.discover import get_dynamic_router
    from app.core.logger import log

    from app.api.v1.system.file.controller import FileAccessRouter

    if not ApiRouter.routes:
        ApiRouter.include_router(SystemRouter, prefix="/system")
        log.info("已注册系统路由: /system")
        dynamic_router = get_dynamic_router()
        ApiRouter.include_router(dynamic_router)
        log.info(f"已挂载业务动态路由到 {prefix}（动态路由数: {len(dynamic_router.routes)}）")
    app.include_router(ApiRouter, prefix=prefix)
    app.include_router(FileAccessRouter, prefix=prefix)


def reset_api_docs() -> None:
    """
    修复Redoc API文档CDN无法访问的问题
    """

    def swagger_monkey_patch(*args, **kwargs):
        """
        修复Swagger API文档CDN无法访问的问题
        """
        p = settings.swagger_static_prefix
        return get_swagger_ui_html(
            *args, **kwargs,
            swagger_css_url=f"{p}/swagger/swagger-ui/swagger-ui.css",
            swagger_js_url=f"{p}/swagger/swagger-ui/swagger-ui-bundle.js",
            swagger_favicon_url=f"{p}/swagger/favicon.png",
        )

    def redoc_monkey_patch(*args, **kwargs):
        p = settings.swagger_static_prefix
        return get_redoc_html(
            *args, **kwargs,
            redoc_js_url=f"{p}/swagger/redoc/bundles/redoc.standalone.js",
            redoc_favicon_url=f"{p}/swagger/favicon.png",
        )

    applications.get_swagger_ui_html = swagger_monkey_patch
    applications.get_redoc_html = redoc_monkey_patch
