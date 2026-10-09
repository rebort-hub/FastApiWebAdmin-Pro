# 后端分层与扩展规范

## 目录约定

```
backend/
├── env/
│   ├── .env.example      # 配置模板（复制为 .env）
│   └── .env              # 本地/部署唯一配置文件（勿提交）
├── app/static/           # 离线 Swagger/ReDoc 等静态资源
├── app/
│   ├── config/           # path_conf.py + setting.py
│   ├── api/v1/system/    # 系统模块四层
│   ├── plugin/fastadmin*/     # 业务插件
│   ├── shared/
│   │   ├── schemas/      # 跨模块 Pydantic 基类
│   │   └── crud/         # 通用 CRUD 基类
│   └── models/base.py    # ORM 基类
```

## 模块四层

`app/api/v1/system/<module>/`：`controller.py` → `service.py` → `model.py`（ORM+CRUD）→ `schema.py`

## 配置

- **单一文件**：`backend/env/.env`，通过 `ENVIRONMENT=dev|prod|test` 区分环境，无需 `.env.dev` / `.env.prod` 多文件。
- 首次使用：`copy env\.env.example env\.env`（Windows）或 `cp env/.env.example env/.env`。
- 数据库/Redis 支持分项配置或 `SQL_DATABASE_URI` / `REDIS_URI` 整串覆盖。
- API 文档静态资源前缀由 `STATIC_URL` 控制，离线资源在 `backend/static/swagger/`。

## 路由

- 系统：`app/api/v1/system/router.py`
- 插件：`app/core/discover.py` 扫描 `app/plugin/{PLUGIN_PREFIX}*/**/controller.py`（默认 `fea_`）
  - 目录 `fea_project` → 挂载前缀 `/project` → 完整路径 `/api/project/...`
  - 目录 `fea_demo` → `/api/demo/...`
  - 启动时会打印扫描到的 controller、每个 Router 加载结果、容器注册路由数

## 启动

- `AUTO_CREATE_TABLES` / `AUTO_SEED_DATA`：lifespan 自动建表、空表灌种子。
- CLI：`uv run python main.py init`；开发环境删表重建：`uv run python main.py reset`（仅 `ENVIRONMENT=dev`）
- 启动日志走 Loguru（控制台 + `logs/`），可直接看到建表/灌种子成功或失败。

## Schema 演进（Alembic）

- **快速起步**：`AUTO_CREATE_TABLES=true` 时 lifespan 仍会用 `create_all` 补缺失表；空表可继续 `python main.py init` 灌种子。
- **模型变更后**：在 `backend` 目录执行：
  - `uv run python main.py revision -m "说明"` — 对比 ORM 与数据库，生成 `app/alembic/versions/` 脚本（无变更则不生成文件）
  - `uv run python main.py upgrade` — 应用到 `head`
  - `uv run python main.py current` / `history` — 查看版本
- **协作/生产**：建议将 `AUTO_CREATE_TABLES=false`，仅通过迁移改表；首次接入 Alembic 时可在已有库上生成 baseline 迁移并 `stamp` 或手工核对后再 `upgrade`。
- 配置：`alembic.ini`（`script_location=app/alembic`），连接串来自 `env/.env` 的同步 URL（`SQL_DB_URL_SYNC`）。
