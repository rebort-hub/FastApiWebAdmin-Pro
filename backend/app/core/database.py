#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from fastapi import FastAPI
from redis.asyncio import from_url as redis_from_url
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config.setting import settings
from app.core.exceptions import CustomException

_engine = None
_async_session_factory: async_sessionmaker[AsyncSession] | None = None


def _get_session_factory() -> async_sessionmaker[AsyncSession]:
    """全局单例"""
    global _engine, _async_session_factory
    if not settings.SQL_DB_ENABLE:
        raise CustomException(
            msg="请先配置SQL数据库链接并启用",
            desc="请启用 app/core/config.py: SQL_DB_ENABLE",
        )
    if _async_session_factory is None:
        _engine = create_async_engine(
            settings.SQL_DB_URL,
            echo=False,
            echo_pool=False,
            pool_pre_ping=True,
            future=True,
        )
        _async_session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=_engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )
    return _async_session_factory


def session_connect() -> AsyncSession:
    
    return _get_session_factory()()


async def dispose_async_engine() -> None:
    global _engine, _async_session_factory
    if _engine is None:
        return
    try:
        await asyncio.wait_for(_engine.dispose(), timeout=3)
    except Exception:
        pass
    finally:
        _engine = None
        _async_session_factory = None


async def redis_connect(app: FastAPI, status: bool) -> None:
   
    from app.core.logger import log

    if not settings.REDIS_ENABLE:
        raise CustomException(
            msg="请先配置Redis数据库链接并启用",
            desc="请启用 app/core/config.py: REDIS_ENABLE",
        )

    if status:
        app.state.redis = redis_from_url(
            settings.REDIS_URL,
            decode_responses=True,
            health_check_interval=30,
        )
        log.info("Redis 连接初始化完成")
        return

    redis = getattr(app.state, "redis", None)
    if redis is None:
        return
    try:
        await asyncio.wait_for(
            redis.aclose(close_connection_pool=True),
            timeout=3,
        )
        log.info("Redis 连接池已关闭")
    except Exception as exc:
        log.warning(f"Redis 关闭异常，忽略以继续退出: {exc}")
    finally:
        app.state.redis = None
