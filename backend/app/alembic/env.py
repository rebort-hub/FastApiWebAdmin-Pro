#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Alembic 迁移"""

from logging.config import fileConfig
from alembic import context
from sqlalchemy import MetaData, engine_from_config, pool
from app.config.path_conf import ALEMBIC_VERSION_DIR
from app.config.setting import get_settings
from app.models.base import Model
from app.utils.import_util import ImportUtil

ALEMBIC_VERSION_DIR.mkdir(parents=True, exist_ok=True)

alembic_config = context.config
alembic_config.set_main_option("sqlalchemy.url", get_settings().SQL_DB_URL_SYNC)

if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

ImportUtil.find_models.cache_clear()
if Model.metadata.tables:
    Model.metadata = MetaData()

found_models = ImportUtil.find_models(Model)
target_metadata = Model.metadata
print(f"自动发现 {len(found_models)} 个模型，{len(target_metadata.tables)} 张表")


def _process_revision_directives(context, revision, directives) -> None:
    if not directives:
        return
    script = directives[0]
    if script.upgrade_ops.is_empty():
        directives[:] = []
        print("未检测到模型变更，不生成迁移文件")


def run_migrations_offline() -> None:
    url = alembic_config.get_main_option("sqlalchemy.url")
    if not url:
        raise ValueError("数据库 URL 未配置，请检查 env/.env")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            transaction_per_migration=True,
            process_revision_directives=_process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
