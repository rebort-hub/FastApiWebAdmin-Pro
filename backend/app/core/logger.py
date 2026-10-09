#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Loguru 日志"""

import atexit
import logging
import sys
import time
from loguru import logger
from app.config.path_conf import LOG_DIR

_handler_ids: list[int] = []
_atexit_registered = False


class InterceptHandler(logging.Handler):
    """将 uvicorn 标准库日志转发到 Loguru。"""

    def emit(self, record: logging.LogRecord) -> None:
        if record.name.startswith("loguru"):
            return
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def cleanup_logging() -> None:
    global _handler_ids
    for handler_id in list(_handler_ids):
        try:
            logger.remove(handler_id)
        except ValueError:
            pass
    _handler_ids.clear()
    try:
        logger.remove()
    except ValueError:
        pass


def setup_logging() -> None:
    global _handler_ids, _atexit_registered
    cleanup_logging()

    console_fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )
    file_fmt = (
        "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
        "{name}:{function}:{line} | {message}"
    )

    _handler_ids.append(
        logger.add(
            sys.stdout,
            format=console_fmt,
            level="INFO",
            colorize=True,
            enqueue=False,
        )
    )

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    day = time.strftime("%Y-%m-%d")
    _handler_ids.append(
        logger.add(
            LOG_DIR / f"info_{day}.log",
            format=file_fmt,
            rotation="00:00",
            retention="3 days",
            enqueue=False,
            encoding="UTF-8",
            level="INFO",
        )
    )
    _handler_ids.append(
        logger.add(
            LOG_DIR / f"error_{day}.log",
            format=file_fmt,
            rotation="00:00",
            retention="3 days",
            enqueue=False,
            encoding="UTF-8",
            level="ERROR",
            backtrace=True,
            diagnose=True,
        )
    )

    intercept = InterceptHandler()
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uv_logger = logging.getLogger(name)
        uv_logger.handlers = [intercept]
        uv_logger.propagate = False

    if not _atexit_registered:
        atexit.register(cleanup_logging)
        _atexit_registered = True


log = logger
