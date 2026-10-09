@echo off
setlocal EnableDelayedExpansion

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

if not exist "env\.env" (
    if exist "env\.env.example" (
        echo [INFO] 未找到 env\.env，正在从 env\.env.example 复制...
        copy "env\.env.example" "env\.env" >nul
        echo [INFO] 请编辑 env\.env 后重新运行
    ) else (
        echo [ERROR] 未找到 env\.env，请先配置 env\.env.example
        pause
        exit /b 1
    )
)

:menu
cls
echo ========================================
echo   FastApiWebAdmin-Pro - uv 开发脚本
echo ========================================
echo.
echo  0. 安装/同步依赖 (uv sync)
echo  1. 初始化数据库 (uv run python main.py init)
echo  2. 启动服务 (uv run python main.py run)
echo  3. 重置数据库 (uv run python main.py reset) 仅 dev
echo  5. 导出 pip 依赖 (uv export --no-dev -o requirements.txt)
echo  9. 退出
echo.
set /p option="请选择操作: "

if "%option%"=="0" goto sync_deps
if "%option%"=="1" goto init_db
if "%option%"=="2" goto start_dev
if "%option%"=="3" goto reset_db
if "%option%"=="5" goto export_req
if "%option%"=="9" exit /b 0
goto menu

:sync_deps
echo.
echo [INFO] 同步依赖...
uv sync
pause
goto menu

:init_db
echo.
echo [INFO] 初始化数据库...
uv run python main.py init
pause
goto menu

:start_dev
echo.
echo [INFO] 启动服务...
uv run python main.py run
pause
goto menu

:reset_db
echo.
echo [WARN] 将删除所有表并重建（仅 dev 环境）...
uv run python main.py reset
pause
goto menu

:export_req
echo.
echo [INFO] 导出 requirements.txt ...
uv export --no-dev -o requirements.txt
pause
goto menu
