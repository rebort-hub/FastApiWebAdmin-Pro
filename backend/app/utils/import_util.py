#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""ORM 模型自动发现"""

import importlib
import inspect
import os
from functools import lru_cache
from pathlib import Path
from typing import Any
from sqlalchemy import inspect as sa_inspect
from app.config.path_conf import BASE_DIR


class ImportUtil:
    MODEL_FILE_NAMES = {"model.py"}
    EXCLUDE_DIRS = {
        ".git",
        ".venv",
        "__pycache__",
        "alembic",
        "env",
        "logs",
        "static",
        "tests",
        "test",
        "scripts",
        "script",
    }

    @classmethod
    def is_valid_model(cls, obj: Any, base_class: type) -> bool:
        if not (inspect.isclass(obj) and issubclass(obj, base_class) and obj is not base_class):
            return False
        if not getattr(obj, "__tablename__", None):
            return False
        try:
            return len(sa_inspect(obj).columns) > 0
        except Exception:
            return False

    @classmethod
    @lru_cache(maxsize=1)
    def find_models(cls, base_class: type) -> list[Any]:
        models: list[Any] = []
        seen_models: set[Any] = set()
        seen_tables: set[str] = set()
        processed_files: set[str] = set()

        model_files: list[tuple[Path, Path]] = []
        for root, dirs, files in os.walk(BASE_DIR):
            dirs[:] = [d for d in dirs if d not in cls.EXCLUDE_DIRS]
            for file in files:
                if file in cls.MODEL_FILE_NAMES:
                    file_path = Path(root) / file
                    relative_path = file_path.relative_to(BASE_DIR)
                    model_files.append((file_path, relative_path))

        model_files.sort(key=lambda item: str(item[1]))

        for file_path, relative_path in model_files:
            file_key = str(file_path)
            if file_key in processed_files:
                continue
            processed_files.add(file_key)

            module_parts = (*relative_path.parts[:-1], relative_path.stem)
            module_name = ".".join(module_parts)

            try:
                module = importlib.import_module(module_name)
            except ImportError:
                continue
            except Exception:
                continue

            for _, obj in inspect.getmembers(module, inspect.isclass):
                if not cls.is_valid_model(obj, base_class):
                    continue
                if obj in seen_models:
                    continue
                table_name = obj.__tablename__
                if table_name in seen_tables:
                    continue
                seen_models.add(obj)
                seen_tables.add(table_name)
                models.append(obj)

        return models
