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

- 后端采用 <a href="https://fastapi.tiangolo.com/zh/">FastAPI</a>（现代、高性能异步框架） + <a href="https://swagger.io/docs/specification/about/">Swagger</a>（自动生成交互式API文档） + <a href="https://docs.pydantic.dev/2.5/">Pydantic</a>（强制类型约束） + <a href="https://docs.sqlalchemy.org/en/20/">SQLAlchemy 2.0</a>；
- 前端采用 <a href="https://cn.vuejs.org/guide/introduction.html">Vue3</a> + <a href="https://antdv.com/docs/vue/introduce-cn">Ant Design Vue</a> + <a href="https://www.typescriptlang.org/">TypeScript</a> + <a href="https://vitejs.dev/">Vite</a> 等主流技术开发；
- 权限认证使用（哈希）密码和 JWT Bearer 令牌的 OAuth2
- RBAC 权限架构设计。支持加载动态权限菜单、按钮级别权限控制、数据级别权限控制，业务模块开发热插拔
- 开箱即用的中后台解决方案，方便企业开发者快速开发，可选择fastapiwebadmin，也可选择当前的FastApiWebAdmin-Pro


演示地址：http://jnstack.cn


管理员账户：

- 账号：admin
- 密码：123456

## 安装和使用

### 获取代码

> git clone https://github.com/rebort-hub/FastApiWebAdmin-Pro.git

### 准备工作

```
Python 3.10 ~ 3.12（推荐 3.12 本地开发）
nodejs >= 20.0（推荐使用最新版）
PgSQL == 14（其他版本均未测试）
Redis（推荐使用最新版）
uv（可选，本地开发推荐，见后端安装依赖）
```

### 后端

1. 安装依赖


   **方式一：uv（推荐本地开发）**

   需先 [安装 uv](https://docs.astral.sh/uv/getting-started/installation/)，在 `backend` 目录执行 **一条命令** 创建虚拟环境并装齐全部依赖（含 pydantic-core、starlette 等传递包）：

   ```shell
   cd backend
   # 创建虚拟环境并激活
   python -m venv .venv
   # 安装依赖
   uv sync
   ```

   Windows 也可双击或运行 `backend/run_win.bat`，选择「安装/同步依赖」。Linux/macOS：`./run_linux.sh sync`。

   日常命令使用 `uv run`（见下方初始化与启动）。新增/升级依赖时：改 `pyproject.toml` → `uv lock` → `uv sync`，并可选 `uv export --no-dev --no-hashes -o requirements.txt` 同步 pip 清单。

   **方式二：pip**

   ```shell
   cd backend
   pip install -r requirements.txt
   ```

2. 配置环境

   ```shell
   cd backend
   copy env\.env.example env\.env   # Linux/macOS: cp env/.env.example env/.env
   ```

   编辑 `backend/env/.env`（**仅此一份**；用 `ENVIRONMENT=dev|prod|test` 区分环境）。数据库、Redis、密钥、`STATIC_URL`（离线文档静态资源）等均在此配置。

   后端分层与插件规范见 [backend/docs/ARCHITECTURE.md](backend/docs/ARCHITECTURE.md)。

3. 创建名为`fastapiwebadmin-pro`的数据库

4. 初始化数据库数据
   
   ```shell
   # 进入后端根目录 backend 下运行
   # 运行命令后会自动生成数据库内的表和数据
   # 如已初始化数据库数据，此命令可不执行
   # uv run python main.py run 或者 python main.py run 
   ```

5. 数据库迁移（模型变更后，在 `backend` 目录）

   ```shell
   uv run python main.py revision -m "说明变更"
   uv run python main.py upgrade
   uv run python main.py current
   ```

   详见 [backend/docs/ARCHITECTURE.md](backend/docs/ARCHITECTURE.md) 中 Alembic 说明。

6. 启动
   
   ```shell
   # 进入后端根目录 backend 下运行
   python3 main.py run
   # 若使用 uv 安装依赖：
   # uv run python main.py run
   ```

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

