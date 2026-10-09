#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import TypeVar, List, Dict
from pathlib import Path
import orjson
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.config.setting import settings
from app.config.path_conf import INITIALIZE_DIR
from app.core.logger import log
from app.models.base import Model
from app.utils.import_util import ImportUtil
from app.database.database import create_tables, table_is_empty


ModelType = TypeVar("ModelType", bound=Model)


class InitializeData:
    """
    初始化数据：建表 + 空表灌种子数据
    """

    SCRIPT_DIR: Path = INITIALIZE_DIR

    def __init__(self) -> None:
        self.engine = create_engine(settings.SQL_DB_URL_SYNC, echo=False, future=True)
        self.DBSession = sessionmaker(bind=self.engine)

    def dispose(self) -> None:
        """释放同步连接池，避免热重载子进程无法退出。"""
        if self.engine is not None:
            self.engine.dispose()
            self.engine = None

    def init_db(self) -> None:
        if not settings.SQL_DB_ENABLE:
            log.warning("SQL_DB_ENABLE=False，跳过数据库初始化")
            return

        log.info("开始数据库初始化...")
        create_tables()
        if settings.AUTO_SEED_DATA:
            self.__seed_if_empty()
        log.info("默认账号: admin / 123456")
        log.info("数据库初始化完成")

    def reset_db(self) -> None:
        """删表重建并强制导入种子（CLI `main.py reset`）。"""
        from app.database.database import drop_all_tables

        if not settings.SQL_DB_ENABLE:
            log.warning("SQL_DB_ENABLE=False，跳过重置")
            return

        log.info("正在重置数据库（删表 → 建表 → 种子数据）...")
        drop_all_tables()
        ImportUtil.find_models.cache_clear()
        ImportUtil.find_models(Model)
        Model.metadata.create_all(bind=self.engine)
        log.info("数据表已重建")
        self.__seed_if_empty(force=True)
        try:
            from alembic import command
            from alembic.config import Config

            command.stamp(Config("alembic.ini"), "head")
            log.info("Alembic 版本已标记为 head")
        except Exception as exc:
            log.warning(f"Alembic stamp 跳过: {exc}")
        log.info("默认账号: admin / 123456")
        log.info("数据库重置完成")

    def run(self) -> None:
        """CLI `main.py init`：建表并对仍为空的表灌种子数据。"""
        if not settings.SQL_DB_ENABLE:
            log.warning("SQL_DB_ENABLE=False，跳过数据库初始化")
            return
        log.info("开始数据库初始化（CLI）...")
        ImportUtil.find_models(Model)
        Model.metadata.create_all(bind=self.engine)
        log.info("数据表检查/创建完成")
        self.__seed_if_empty(force=False)
        log.info("默认账号: admin / senqi1010")
        log.info("数据库初始化完成")

    def __seed_if_empty(self, force: bool = False) -> None:
        models = self.__sort_models_by_fk(ImportUtil.find_models(Model))
        for model in models:
            table_name = model.__tablename__
            if not force and not table_is_empty(table_name):
                log.info(f"跳过 {table_name} 初始化（表已有数据）")
                continue
            data = self.__get_data(table_name)
            if not data:
                log.info(f"跳过 {table_name}，无初始化数据文件")
                continue
            session = self.DBSession()
            try:
                objs = [model(**item) for item in data]
                session.add_all(objs)
                session.commit()
                self.__update_sequence(model, len(objs))
                log.info(f"已写入 {table_name} 初始化数据（{len(objs)} 条）")
            except Exception as exc:
                session.rollback()
                log.error(f"初始化 {table_name} 失败: {exc}")
                raise
            finally:
                session.close()

    @staticmethod
    def __sort_models_by_fk(models: List[ModelType]) -> List[ModelType]:
        """按外键依赖拓扑排序，避免关联表早于主表灌种子。"""
        by_table = {model.__tablename__: model for model in models}
        original = [model.__tablename__ for model in models]
        deps: Dict[str, set[str]] = {}
        for model in models:
            name = model.__tablename__
            needed: set[str] = set()
            for column in model.__table__.columns:
                for fk in column.foreign_keys:
                    ref = fk.column.table.name
                    if ref != name and ref in by_table:
                        needed.add(ref)
            deps[name] = needed

        ordered: List[str] = []
        remaining = set(by_table)
        while remaining:
            ready = [name for name in original if name in remaining and deps[name] <= set(ordered)]
            if not ready:
                ready = [name for name in original if name in remaining]
            name = ready[0]
            ordered.append(name)
            remaining.remove(name)
        return [by_table[name] for name in ordered]

    def __get_data(self, filename: str) -> List[Dict]:
        try:
            json_path = Path.joinpath(self.SCRIPT_DIR, "data", f"{filename}.json")
            with open(json_path, "r", encoding="utf-8") as f:
                return orjson.loads(f.read())
        except FileNotFoundError:
            return []

    def __update_sequence(self, model: ModelType, max_rows: int) -> None:
        table_name = model.__tablename__
        sequence_name = None
        for col in model.__table__.columns:
            if col.autoincrement is True:
                sequence_name = f"{table_name}_{col.name}_seq"
                break
        if not sequence_name:
            return
        session = self.DBSession()
        try:
            new_value = max_rows + 1
            session.execute(text(f'ALTER SEQUENCE "{sequence_name}" RESTART WITH {new_value}'))
            session.commit()
        except Exception as exc:
            session.rollback()
            log.warning(f"更新序列 {sequence_name} 跳过: {exc}")
        finally:
            session.close()
