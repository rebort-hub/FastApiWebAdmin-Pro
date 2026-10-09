#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""应用入口"""

import os
from typing import Annotated, Optional
import typer
import uvicorn
from fastapi import FastAPI
from app.config.setting import get_settings, settings

shell_app = typer.Typer()


def _alembic():
    """热重载强依赖该包。"""
    from alembic import command
    from alembic.config import Config

    return command, Config("alembic.ini")


def _reload_settings(environment: Optional[str] = None) -> None:
    if environment:
        os.environ["ENVIRONMENT"] = environment
    get_settings.cache_clear()


def create_app() -> FastAPI:
    from starlette.staticfiles import StaticFiles

    from app.core.init_app import (
        lifespan,
        register_middlewares,
        register_exceptions,
        register_routers,
        reset_api_docs,
    )
    from app.core.logger import setup_logging

    setup_logging()
    app = FastAPI(**settings.get_backend_app_attributes, lifespan=lifespan)

    register_exceptions(app)

    if settings.STATIC_ENABLE:
        app.mount(settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT))

    if settings.TEMP_ENABLE:
        app.mount(settings.TEMP_URL, app=StaticFiles(directory=settings.TEMP_ROOT))
    register_routers(app, prefix=settings.API_PREFIX)

    register_middlewares(app)

    reset_api_docs()

    return app


@shell_app.command()
def run():
    """启动服务"""
    try:
        typer.echo(f"启动 {settings.TITLE} (reload={settings.RELOAD}) ...")
        from app.core.logger import setup_logging

        setup_logging()
        uvicorn.run(
            app="main:create_app",
            host=settings.SERVER_HOST,
            port=settings.SERVER_PORT,
            reload=settings.RELOAD,
            factory=True,
            log_config=None,
            h11_max_incomplete_event_size=16 * 1024,
        )
    finally:
        from app.core.logger import cleanup_logging

        cleanup_logging()


@shell_app.command()
def init():
    """初始化数据"""
    from app.core.logger import setup_logging
    from app.scripts.initialize import InitializeData

    setup_logging()
    InitializeData().run()


@shell_app.command(name="reset")
def db_reset(
    env: Annotated[
        Optional[str],
        typer.Option("--env", help="运行环境，仅 dev 允许重置"),
    ] = None,
    yes: Annotated[bool, typer.Option("--yes", "-y", help="跳过确认提示")] = False,
):
    """删表重建并导入种子数据（仅 ENVIRONMENT=dev）"""
    _reload_settings(env)
    cfg = get_settings()
    if not cfg.SQL_DB_ENABLE:
        typer.echo("SQL_DB_ENABLE=False，无法重置数据库", err=True)
        raise typer.Exit(1)
    if cfg.ENVIRONMENT != "dev":
        typer.echo("reset 仅允许在 dev 环境执行，请设置 ENVIRONMENT=dev", err=True)
        raise typer.Exit(1)
    if not yes and not typer.confirm("将删除所有表并重建，是否继续？"):
        raise typer.Exit()
    from app.core.logger import setup_logging
    from app.scripts.initialize import InitializeData

    setup_logging()
    InitializeData().reset_db()
    typer.echo("数据库重置完成，默认账号: admin / 123456")


@shell_app.command(name="revision")
def alembic_revision(
    message: Annotated[str, typer.Option("-m", "--message", help="迁移描述")] = "迁移脚本",
    env: Annotated[
        Optional[str],
        typer.Option("--env", help="运行环境 dev|prod|test，会写入 ENVIRONMENT 并重新加载配置"),
    ] = None,
):
    """根据模型变更生成 Alembic 迁移脚本"""
    _reload_settings(env)
    command, cfg = _alembic()
    command.revision(cfg, autogenerate=True, message=message)
    typer.echo("迁移脚本已生成，请检查 app/alembic/versions/ 后执行 upgrade")


@shell_app.command(name="upgrade")
def alembic_upgrade(
    revision: Annotated[str, typer.Option("-r", "--revision", help="目标版本")] = "head",
    env: Annotated[Optional[str], typer.Option("--env", help="运行环境")] = None,
):
    """应用 Alembic 迁移"""
    _reload_settings(env)
    command, cfg = _alembic()
    command.upgrade(cfg, revision)
    typer.echo(f"迁移已应用至 {revision}")


@shell_app.command(name="downgrade")
def alembic_downgrade(
    revision: Annotated[str, typer.Option("-r", "--revision", help="目标版本")] = "-1",
    env: Annotated[Optional[str], typer.Option("--env", help="运行环境")] = None,
):
    """回滚 Alembic 迁移"""
    _reload_settings(env)
    if not typer.confirm(f"确定回滚至 {revision} 吗？"):
        raise typer.Exit()
    command, cfg = _alembic()
    command.downgrade(cfg, revision)
    typer.echo("迁移已回滚")


@shell_app.command(name="current")
def alembic_current(
    env: Annotated[Optional[str], typer.Option("--env", help="运行环境")] = None,
):
    """查看当前数据库迁移版本"""
    _reload_settings(env)
    command, cfg = _alembic()
    command.current(cfg)


@shell_app.command(name="history")
def alembic_history(
    verbose: Annotated[bool, typer.Option("-v", "--verbose", help="显示详情")] = False,
    env: Annotated[Optional[str], typer.Option("--env", help="运行环境")] = None,
):
    """查看迁移历史"""
    _reload_settings(env)
    command, cfg = _alembic()
    command.history(cfg, verbose=verbose)


if __name__ == "__main__":
    shell_app()
