#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

info() { echo "[OK] $*"; }

if [[ ! -f "env/.env" ]]; then
  if [[ -f "env/.env.example" ]]; then
    info "未找到 env/.env，从 env/.env.example 复制..."
    cp "env/.env.example" "env/.env"
    info "请编辑 env/.env 后重新运行"
  else
    echo "[ERROR] 未找到 env/.env" >&2
    exit 1
  fi
fi

sync_deps() {
  info "同步依赖 (uv sync)..."
  uv sync
}

init_db() {
  info "初始化数据库..."
  uv run python main.py init
}

start_dev() {
  info "启动服务..."
  uv run python main.py run
}

export_req() {
  info "导出 requirements.txt ..."
  uv export --no-dev -o requirements.txt
}

usage() {
  cat <<EOF
用法: $0 [sync|init|run|export]
  sync   安装/同步依赖 (uv sync)
  init   初始化数据库
  run    启动服务
  export 导出 pip 用 requirements.txt
EOF
}

case "${1:-}" in
  sync) sync_deps ;;
  init) init_db ;;
  run) start_dev ;;
  export) export_req ;;
  *) usage; exit 1 ;;
esac
