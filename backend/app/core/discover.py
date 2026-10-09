#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""业务插件动态路由发现与注册。"""

import importlib
from functools import lru_cache
from pathlib import Path
from fastapi import APIRouter
from app.config.setting import settings
from app.core.logger import log


@lru_cache
def get_dynamic_router() -> APIRouter:
    
    log.info("开始业务模块路由发现与注册")
    root_router = APIRouter()
    seen_router_ids: set[int] = set()
    plugin_prefix = settings.PLUGIN_PREFIX
    prefix_len = len(plugin_prefix)

    try:
        base_package = importlib.import_module("app.plugin")
        base_dir = Path(next(iter(base_package.__path__)))
        controller_files = sorted(
            p for p in base_dir.rglob("controller.py")
            if p.is_file() and p.relative_to(base_dir).parts[0].startswith(plugin_prefix)
        )
        log.info(
            f"扫描到 {len(controller_files)} 个业务 controller "
            f"(前缀={plugin_prefix!r}): {[str(p.relative_to(base_dir)) for p in controller_files]}"
        )
        if not controller_files:
            plugin_dirs = [p.name for p in base_dir.iterdir() if p.is_dir() and not p.name.startswith("_")]
            log.warning(
                f"未发现匹配 {plugin_prefix}* 的 controller。"
                f"当前 plugin 子目录: {plugin_dirs}；请检查 PLUGIN_PREFIX 与目录命名是否一致"
            )
        container_routers: dict[str, APIRouter] = {}

        for file in controller_files:
            rel_path = file.relative_to(base_dir)
            path_parts = rel_path.parts
            top_module = path_parts[0]
            if not top_module.startswith(plugin_prefix):
                continue
            suffix = top_module[prefix_len:]
            if not suffix:
                log.error(f"跳过无效业务模块目录: {top_module}")
                continue
            mount_prefix = f"/{suffix}"
            if mount_prefix not in container_routers:
                container_routers[mount_prefix] = APIRouter(prefix=mount_prefix)
            container_router = container_routers[mount_prefix]
            module_path = f"app.plugin.{'.'.join(path_parts[:-1])}.controller"

            try:
                module = importlib.import_module(module_path)
                registered = 0
                for attr_name in dir(module):
                    attr_value = getattr(module, attr_name, None)
                    if isinstance(attr_value, APIRouter):
                        router_id = id(attr_value)
                        if router_id not in seen_router_ids:
                            seen_router_ids.add(router_id)
                            container_router.include_router(attr_value)
                            registered += 1
                            log.info(f"加载业务路由: {module_path}.{attr_name} → {mount_prefix}")
                if registered == 0:
                    log.warning(f"模块 {module_path} 未找到顶层 APIRouter")
            except Exception as exc:
                log.exception(f"加载业务模块失败: {module_path} - {exc}")

        for mount_prefix, container_router in sorted(container_routers.items()):
            root_router.include_router(container_router)
            log.info(f"注册业务模块: {mount_prefix} (路由数: {len(container_router.routes)})")

        log.info(f"业务模块路由发现完成: {len(container_routers)} 个业务模块")
    except Exception as exc:
        log.exception(f"业务模块路由发现失败: {exc}")

    return root_router


__all__ = ["get_dynamic_router"]
