#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""项目路径常量"""

from pathlib import Path


BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
APP_DIR: Path = BASE_DIR / "app"
ENV_DIR: Path = BASE_DIR / "env"
STATIC_DIR: Path = APP_DIR / "static"
FILES_DIR: Path = APP_DIR / "files"
TEMP_DIR: Path = APP_DIR / "temp"
LOG_DIR: Path = BASE_DIR / "logs"
PLUGIN_DIR: Path = APP_DIR / "plugin"
INITIALIZE_DIR: Path = APP_DIR / "scripts" / "initialize"
ALEMBIC_VERSION_DIR: Path = APP_DIR / "alembic" / "versions"
