#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""数据库表结构初始化"""

from sqlalchemy import create_engine, inspect as sa_inspect, text
from app.config.setting import settings
from app.core.logger import log
from app.models.base import Model
from app.utils.import_util import ImportUtil


def _sync_db_url() -> str:
    return settings.SQL_DB_URL_SYNC


def drop_all_tables() -> None:
    """删除 ORM 模型对应的所有表（开发 reset 使用，慎用）。"""
    if not settings.SQL_DB_ENABLE:
        log.warning("SQL_DB_ENABLE=False，跳过删表")
        return

    ImportUtil.find_models.cache_clear()
    ImportUtil.find_models(Model)
    engine = create_engine(_sync_db_url(), future=True)
    try:
        Model.metadata.drop_all(bind=engine)
        with engine.connect() as conn:
            conn.execute(text("DROP TABLE IF EXISTS alembic_version"))
            conn.commit()
        log.warning("已删除所有业务表及 alembic_version")
    except Exception as exc:
        log.error(f"删表失败: {exc}")
        raise
    finally:
        engine.dispose()


def create_tables() -> None:
    if not settings.SQL_DB_ENABLE:
        return
    if not settings.AUTO_CREATE_TABLES:
        log.info("AUTO_CREATE_TABLES=False，跳过自动建表")
        return

    ImportUtil.find_models(Model)
    engine = create_engine(_sync_db_url(), future=True)
    try:
        Model.metadata.create_all(bind=engine)
        log.info("数据表检查/创建完成")
    except Exception as exc:
        log.error(f"数据表创建失败: {exc}")
        raise
    finally:
        engine.dispose()


def table_is_empty(table_name: str) -> bool:
    engine = create_engine(_sync_db_url(), future=True)
    try:
        with engine.connect() as conn:
            if table_name not in sa_inspect(conn).get_table_names():
                return True
            result = conn.execute(text(f'SELECT COUNT(*) FROM "{table_name}"'))
            return (result.scalar() or 0) == 0
    except Exception:
        return True
    finally:
        engine.dispose()
