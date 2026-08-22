#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂车载系统 · 实战部署脚本 v1.0（鲲鹏/边缘节点）
# DNA: #龍芯⚡️丙午·丙申·丁巳·丙午·䷃蒙-CAR-DEPLOY-v1.0-UID9622
# 用法: sudo ./deploy_car_system.sh [install|upgrade|rollback|status|uninstall]
# 零外部依赖：仅 python3 + systemd + curl
set -euo pipefail

# ========== 可调参数（环境变量覆盖） ==========
APP_NAME="${APP_NAME:-longhun-car-index}"
APP_DIR="${APP_DIR:-/opt/longhun/car}"
DATA_DIR="${LONGHUN_CAR_DIR:-/opt/longhun/car/data}"
PORT="${PORT:-8080}"
PY_BIN="${PY_BIN:-python3}"
SCRIPT_SRC="${SCRIPT_SRC:-./${0%/*}/../../05_ENGINES/lh_car_cloud_index.py}"
BACKUP_KEEP="${BACKUP_KEEP:-7}"                 # 备份保留份数
HEALTH_RETRIES="${HEALTH_RETRIES:-10}"          # 健康检查重试
HEALTH_INTERVAL="${HEALTH_INTERVAL:-2}"         # 秒

C_G='🟢'; C_Y='🟡'; C_R='🔴'
log()  { echo "[$(date '+%F %T')] $*"; }
ok()   { log "$C_G $*"; }
warn() { log "$C_Y $*"; }
die()  { log "$C_R $*"; exit 1; }

# ========== 前置检查清单 ==========
preflight() {
    log "① 前置检查（六项，缺一不部署）"
    [ "$(id -u)" = "0" ] || die "需 root 运行（systemd 安装）"
    command -v "$PY_BIN" >/dev/null || die "未找到 python3"
    "$PY_BIN" -c 'import sqlite3,http.server' || die "python3 标准库不完整"
    [ -f "$SCRIPT_SRC" ] || die "服务脚本不存在: $SCRIPT_SRC"
    [ -n "${LONGHUN_CONFIRM_CODE:-}" ] || die "确认码未设置: export LONGHUN_CONFIRM_CODE=..."
    [ "${#LONGHUN_CONFIRM_CODE}" -ge 16 ] || die "确认码长度 <16，不合规"
    ok "前置检查通过"
}

# ========== 备份（升级/回滚共用） ==========
backup() {
    log "② 备份现有版本与数据"
    mkdir -p "$APP_DIR/backups"
    local ts; ts="$(date +%Y%m%d-%H%M%S)"
    if [ -d "$APP_DIR/current" ] || [ -d "$DATA_DIR" ]; then
        tar czf "$APP_DIR/backups/backup-$ts.tar.gz" \
            --ignore-failed-read "$APP_DIR/current" "$DATA_DIR" 2>/dev/null || true
        ok "备份完成: backup-$ts.tar.gz"
    fi
    # 只保留最近 N 份
    ls -1t "$APP_DIR/backups"/backup-*.tar.gz 2>/dev/null | tail -n +$((BACKUP_KEEP+1)) | xargs -r rm -f
}

# ========== 安装/升级 ==========
install_service() {
    log "③ 部署服务文件（原子切换 current 软链思路的目录版）"
    mkdir -p "$APP_DIR/releases" "$DATA_DIR"
    local rel="$APP_DIR/releases/$(date +%Y%m%d-%H%M%S)"
    mkdir -p "$rel"
    cp "$SCRIPT_SRC" "$rel/index_server.py"
    chmod 644 "$rel/index_server.py"

    cat > "$rel/environment" <<EOF
LONGHUN_CAR_DIR=$DATA_DIR
LONGHUN_CONFIRM_CODE=$LONGHUN_CONFIRM_CODE
EOF
    chmod 600 "$rel/environment"   # 确认码只进环境文件，权限600

    cat > /etc/systemd/system/$APP_NAME.service <<EOF
[Unit]
Description=LongHun Car Index Service v2.1
After=network.target

[Service]
Type=simple
EnvironmentFile=$rel/environment
ExecStart=$PY_BIN $rel/index_server.py
Restart=always
RestartSec=3
# 性能与资源护栏（见运维手册性能调优节）
LimitNOFILE=65535
MemoryMax=512M
CPUQuota=50%
NoNewPrivileges=true
ProtectSystem=full
ReadWritePaths=$DATA_DIR

[Install]
WantedBy=multi-user.target
EOF

    # 记录当前 release 供回滚
    [ -d "$APP_DIR/current" ] && readlink -f "$APP_DIR/current/index_server.py" > "$APP_DIR/.previous_release" 2>/dev/null || true
    rm -rf "$APP_DIR/current"
    ln -sfn "$rel" "$APP_DIR/current" 2>/dev/null || cp -r "$rel" "$APP_DIR/current"

    systemctl daemon-reload
    systemctl enable "$APP_NAME" >/dev/null 2>&1 || true
    systemctl restart "$APP_NAME"
    ok "服务已启动（release: $rel）"
}

# ========== 健康检查（部署验收闸门） ==========
health_check() {
    log "④ 健康检查（/health 连续 $HEALTH_RETRIES 次，全绿才算部署成功）"
    local i=1
    while [ $i -le $HEALTH_RETRIES ]; do
        if curl -sf "http://127.0.0.1:$PORT/health" | grep -q '🟢'; then
            ok "健康检查通过（第 $i 次）"
            return 0
        fi
        sleep "$HEALTH_INTERVAL"; i=$((i+1))
    done
    die "健康检查失败——执行回滚: $0 rollback"
}

# ========== 冒烟测试（带确认码的业务验证） ==========
smoke_test() {
    log "⑤ 冒烟测试（三问：能写吗？能查吗？坏人进得来吗？）"
    local H="X-LongHun-Confirm: $LONGHUN_CONFIRM_CODE"
    # 无确认码必须 403
    local code; code=$(curl -s -o /dev/null -w '%{http_code}' -X POST "http://127.0.0.1:$PORT/api/vehicle/register" \
        -H 'Content-Type: application/json' -d '{"vehicle_id":"smoke"}')
    [ "$code" = "403" ] || die "冒烟失败：无确认码未拦截（$code）"
    # 正常注册
    curl -sf -X POST "http://127.0.0.1:$PORT/api/vehicle/register" -H "$H" \
        -H 'Content-Type: application/json' -d '{"vehicle_id":"smoke-test","model":"deploy"}' | grep -q '🟢' \
        || die "冒烟失败：车辆注册"
    # 状态可查
    curl -sf "http://127.0.0.1:$PORT/api/status" | grep -q '🟢' || die "冒烟失败：status"
    ok "冒烟测试通过"
}

# ========== 回滚 ==========
rollback() {
    log "回滚到上一个 release"
    local prev; prev=$(cat "$APP_DIR/.previous_release" 2>/dev/null || true)
    [ -n "$prev" ] && [ -f "$prev" ] || die "无可用回滚版本"
    rm -rf "$APP_DIR/current"
    ln -sfn "$(dirname "$prev")" "$APP_DIR/current" 2>/dev/null || cp -r "$(dirname "$prev")" "$APP_DIR/current"
    systemctl restart "$APP_NAME"
    ok "已回滚: $prev"
}

case "${1:-install}" in
    install|upgrade) preflight; backup; install_service; health_check; smoke_test
        ok "🐉 部署完成。状态: systemctl status $APP_NAME";;
    rollback) rollback; health_check;;
    status)    systemctl status "$APP_NAME" --no-pager || true
        curl -sf "http://127.0.0.1:$PORT/api/status" && echo || warn "服务未响应";;
    uninstall) systemctl disable --now "$APP_NAME" || true
        rm -f /etc/systemd/system/$APP_NAME.service; systemctl daemon-reload
        warn "服务已卸载（数据保留在 $DATA_DIR）";;
    *) die "未知命令: $1（install|upgrade|rollback|status|uninstall）";;
esac
