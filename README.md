<div align="center">
  <p align="center">
    <img src="frontend/public/logo.png" height="150" alt="logo"/>
  </p>
  <p align="center">
    <a href="https://github.com/rebort-hub/FastApiWebAdmin-Pro.git"><img src="https://github.com/rebort-hub/FastApiWebAdmin-Pro/badge/star.svg?theme=dark"></a>
    <a href="https://github.com/rebort-hub/FastApiWebAdmin-Pro.git"><img src="https://github.com/rebort-hub/FastApiWebAdmin-Pro.git?style=social"></a>
    <a href="https://github.com/rebort-hub/FastApiWebAdmin-Pro/blob/master/LICENSE"><img src="https://img.shields.io/badge/License-Apache-orange"></a>
    <img src="https://img.shields.io/badge/Python-3.10~3.12-blue">
    <img src="https://img.shields.io/badge/NodeJS-≥20.0-blue">
  </p>
</div>

## 介绍

<b>FastApiWebAdmin-Pro</b> 是一套全部开源的快速开发平台，提供免费使用

## 🛠️ 技术栈概览

| 类型 | 技术选型 | 描述 |
|------|----------|------|
| **后端框架** | FastAPI / Uvicorn / Pydantic 2.0 / Alembic | 现代、高性能的异步框架，强制类型约束，数据迁移 |
| **ORM** | SQLAlchemy 2.0 | 强大的 ORM 库 |
| **定时任务** | APScheduler | 轻松实现定时任务 |
| **权限认证** | PyJWT | 实现 JWT 认证 |
| **前端框架** | Vue3 / Vite / Pinia / TypeScript | 快速开发 Web 应用 |
| **Web UI** | Ant Design Vue‌ | 企业级 UI 组件库 |
| **数据库** | MySQL / PostgreSQL |
| **缓存** | Redis | 高性能缓存数据库 |
| **文档** | Swagger / Redoc | 自动生成 API 文档 |
| **部署** | Docker / Nginx / Docker Compose | 容器化部署方案 |


## 📌 内置功能模块

| 模块 | 功能 | 描述 |
|------|------|------|
| 📊 **首页 ** | Token使用统计 | Toekn使用趋势统计 |
| ⚙️ **系统管理** | 用户、角色、菜单、部门、岗位、字典、配置、公告 | 核心系统管理功能 |
| 👀 **监控管理** | 在线用户、服务器监控、缓存监控 | 系统运行状态监控 |
| 📋 **任务管理** | 定时任务 | 异步任务调度管理 |
| 📝 **日志管理** | 操作日志 | 用户行为审计 |
| 📁 **文件管理** | 文件存储 | 统一文件管理 |


- 权限认证使用（哈希）密码和 JWT Bearer 令牌的 OAuth2
- RBAC 权限架构设计。支持加载动态权限菜单、按钮级别权限控制、数据级别权限控制，业务模块开发热插拔
- 开箱即用的中后台解决方案，方便企业开发者快速开发，可选择fastapiwebadmin，也可选择当前的FastApiWebAdmin-Pro


演示地址：http://jnstack.cn


管理员账户：

- 账号：admin
- 密码：123456

# 后端分层与扩展规范

## 目录约定

```
backend/
├── env/
│   ├── .env.example      # 配置模板（复制为 .env）
│   └── .env              # 本地/部署唯一配置文件
├── app/static/           # 离线 Swagger/ReDoc 等静态资源
├── app/
│   ├── config/           # path_conf.py + setting.py
│   ├── api/v1/system/    # 系统模块四层
│   ├── plugin/fastadmin*/     # 业务插件模块【所有业务模块基于这个目录下进行开发，严格遵循】
│   ├── shared/
│   │   ├── schemas/      # 跨模块 Pydantic 基类
│   │   └── crud/         # 通用 CRUD 基类
│   └── models/base.py    # ORM 基类
```

## 模块四层

`controller.py` → `service.py` → `model.py`（ORM+CRUD）→ `schema.py`

案例：fastadmin_project-项目管理业务模块

## 安装和使用

### 获取代码

> git clone https://github.com/rebort-hub/FastApiWebAdmin-Pro.git

### 准备工作

```
Python 3.10 ~ 3.12（推荐 3.12 本地开发）
nodejs >= 20.0（推荐使用最新版）
PgSQL == 14（其他版本均未测试）
Redis（推荐使用最新版）
uv（本地开发推荐）
```

### 后端

1. 安装依赖


   **方式一：uv（推荐本地开发）**

   需先 [安装 uv](https://docs.astral.sh/uv/getting-started/installation/)，在 `backend` 目录执行 **一条命令** 创建虚拟环境并装齐全部依赖（含 pydantic-core、starlette 等传递包）：

   ```shell
   cd backend
      # 创建虚拟环境（推荐）
   python -m venv .venv
      # 激活虚拟环境
      # macOS/Linux
   source .venv/bin/activate
      # Windows
   .venv\Scripts\activate
      # windows 用户
      # 安装依赖
   uv sync
     # 安装依赖(linux&mac)
   pip install -r requirements
   ```

   Windows 也可双击或运行 `backend/run_win.bat`，选择「安装/同步依赖」。Linux/macOS：`./run_linux.sh sync`。

   日常命令使用 `uv run`（见下方初始化与启动）。
   
   新增/升级依赖时：改 `pyproject.toml` → `uv lock` → `uv sync`，并可选 `uv export --no-dev --no-hashes -o requirements.txt` 同步 pip 清单。


2. 配置环境

   ```shell
   cd backend
   copy env\.env.example env\.env   # Linux/macOS: cp env/.env.example env/.env
   ```
   
3. 创建名为`fastapiwebadmin-pro`的数据库

4. 初始化数据库数据并启动后端
   
   ```shell
      # 进入后端根目录 backend 下运行
      # 运行命令后会自动生成数据库内的表和数据
      # 如已初始化数据库数据，此命令可不执行
      # Linux环境，Mac使用如下方式启动
   python3 main.py run
      # 若使用 uv 安装依赖，启动方式如下，windows环境下默认方式：
   uv run python main.py run
   ```

5. 数据库迁移（模型变更后，在 `backend` 目录）

- **快速起步**：`AUTO_CREATE_TABLES=true` 时 lifespan 仍会用 `create_all` 补缺失表；空表可继续 `python main.py init` 灌种子。
- **模型变更后**：在 `backend` 目录执行：
  - `uv run python main.py revision -m "说明"` — 对比 ORM 与数据库，生成 `app/alembic/versions/` 脚本（无变更则不生成文件）
  - `uv run python main.py upgrade` — 应用到 `head`
  - `uv run python main.py current` / `history` — 查看版本
  - `uv run python main.py reset` / `reset` — 运行此命令，会直接把本地数据库中的表全部删除清空，重新初始化，注意，只用于本地开发环境

- **协作/生产**：将 `AUTO_CREATE_TABLES=false`，仅通过迁移改表；首次接入 Alembic 时可在已有库上生成 baseline 迁移并 `stamp` 或手工核对后再 `upgrade`。
- 配置：`alembic.ini`（`script_location=app/alembic`），连接串来自 `env/.env` 的同步 URL（`SQL_DB_URL_SYNC`）。


### 前端

1. 安装依赖
   
   ```shell
   cd frontend
   pnpm install
   ```

2. 运行
   
   ```shell
   pnpm run dev
   ```

3. 打包
   
   ```shell
   pnpm exec vite build   # 仅打包
   pnpm run build    # 会先跑 vue-tsc
   pnpm run typecheck
   ```

### 访问项目

- 前端地址：http://127.0.0.1:5180
- 账号：`admin`密码：`123456`
- 接口地址：http://127.0.0.1:8085/docs

