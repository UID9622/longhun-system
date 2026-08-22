#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ╔═══════════════════════════════════════════════════════════════╗
# ║  🐉 龍魂系统 · 鲲鹏服务监控配置脚本                          ║
# ║  🏷️  版本: v1.1 · Bark                                       ║
# ║  🧬  DNA: #龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-KUNPENG-MONITOR-BARK-v1.1        ║
# ║  👤  适用: UID9622 · 诸葛鑫                                   ║
# ║  🖥️  目标: 华为 TaiShan 200 · openEuler                       ║
# ╚═══════════════════════════════════════════════════════════════╝

set -e

# ────────────────────────────────────────────────────────────────
# 配置区（改这里适配你的环境）
# ────────────────────────────────────────────────────────────────
BASE_DIR="/opt/longhun-system"
LOG_DIR="/var/log/longhun"
DATA_DIR="/var/lib/longhun"
PYTHON="/usr/bin/python3"
USER="longhun"

# 服务定义（名称:端口:启动命令）
SERVICES=(
    "longhun-skillbus:8080:${PYTHON} ${BASE_DIR}/bin/lh_skill_bus.py --serve --port 8080"
    "longhun-digitalhuman:8081:${PYTHON} ${BASE_DIR}/bin/lh_digital_human_bridge.py --serve --port 8081"
    "longhun-persona:8082:${PYTHON} ${BASE_DIR}/bin/lh_persona_orchestrator.py --serve --port 8082"
    "longhun-dna:8083:${PYTHON} ${BASE_DIR}/bin/lh_dna_registry.py --serve --port 8083"
    "longhun-ecosystem:8084:${PYTHON} ${BASE_DIR}/bin/lh_ecosystem_passport.py --serve --port 8084"
)

# 告警配置
ALARM_LOG="${LOG_DIR}/alarm.log"
HEALTH_LOG="${LOG_DIR}/health.log"
CPU_THRESHOLD=80      # CPU 使用率超过此值告警（百分比）
MEM_THRESHOLD=80      # 内存使用率超过此值告警（百分比）
DISK_THRESHOLD=85     # 磁盘使用率超过此值告警（百分比）

# ────────────────────────────────────────────────────────────────
# 颜色定义
# ────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ────────────────────────────────────────────────────────────────
# 工具函数
# ────────────────────────────────────────────────────────────────
log_info() {
    echo -e "${GREEN}[INFO]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"
    echo "[WARN] $(date '+%Y-%m-%d %H:%M:%S') $1" >> "${ALARM_LOG}"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $(date '+%Y-%m-%d %H:%M:%S') $1"
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') $1" >> "${ALARM_LOG}"
}

log_health() {
    echo "[HEALTH] $(date '+%Y-%m-%d %H:%M:%S') $1" >> "${HEALTH_LOG}"
}

# ────────────────────────────────────────────────────────────────
# 第一步：创建目录结构
# ────────────────────────────────────────────────────────────────
setup_directories() {
    log_info "创建目录结构..."

    mkdir -p "${LOG_DIR}"
    mkdir -p "${DATA_DIR}/dna"
    mkdir -p "${DATA_DIR}/db"
    mkdir -p "${DATA_DIR}/backups"
    mkdir -p "${BASE_DIR}/scripts"

    # 确保 longhun 用户有权限
    if id "${USER}" &>/dev/null; then
        chown -R "${USER}:${USER}" "${LOG_DIR}" 2>/dev/null || true
        chown -R "${USER}:${USER}" "${DATA_DIR}" 2>/dev/null || true
    fi

    log_info "目录创建完成"
}

# ────────────────────────────────────────────────────────────────
# 第二步：生成 systemd 服务文件
# ────────────────────────────────────────────────────────────────
generate_systemd_services() {
    log_info "生成 systemd 服务文件..."

    for service_def in "${SERVICES[@]}"; do
        IFS=':' read -r name port cmd <<< "${service_def}"
        local service_file="/etc/systemd/system/${name}.service"

        cat > "${service_file}" << EOF
[Unit]
Description=龍魂系统 - ${name} 服务
Documentation=https://uid9622.notion.site
After=network.target
Wants=network.target

[Service]
Type=simple
User=${USER}
Group=${USER}
WorkingDirectory=${BASE_DIR}
ExecStart=${cmd}
Restart=always
RestartSec=10
StartLimitInterval=300
StartLimitBurst=5

# 资源限制
LimitNOFILE=65536
LimitNPROC=4096

# 安全加固
PrivateTmp=true
ProtectSystem=full
ProtectHome=false
NoNewPrivileges=true

[Install]
WantedBy=multi-user.target
EOF

        chmod 644 "${service_file}"
        log_info "  生成 ${name}.service (端口 ${port})"
    done

    systemctl daemon-reload
    log_info "systemd 服务文件全部生成完成"
}

# ────────────────────────────────────────────────────────────────
# 第三步：启用并启动所有服务
# ────────────────────────────────────────────────────────────────
enable_and_start_services() {
    log_info "启用并启动所有龍魂服务..."

    for service_def in "${SERVICES[@]}"; do
        IFS=':' read -r name port cmd <<< "${service_def}"

        systemctl enable "${name}" 2>/dev/null || true
        systemctl start "${name}" 2>/dev/null || true

        # 等待 3 秒检查服务状态
        sleep 2
        if systemctl is-active --quiet "${name}"; then
            log_info "  ✅ ${name} 已启动并运行中"
        else
            log_error "  ❌ ${name} 启动失败，请检查日志: journalctl -u ${name}"
        fi
    done

    log_info "所有服务启动完成"
}

# ────────────────────────────────────────────────────────────────
# 第四步：配置自愈引擎定时任务
# ────────────────────────────────────────────────────────────────
setup_cron_jobs() {
    log_info "配置定时任务..."

    # 先导出已有的 crontab
    crontab -l > /tmp/cron_backup.tmp 2>/dev/null || true

    # 移除旧的龍魂定时任务（避免重复）
    sed -i '/longhun/d' /tmp/cron_backup.tmp 2>/dev/null || true

    # 添加新的定时任务
    cat >> /tmp/cron_backup.tmp << EOF

# ── 龍魂系统定时任务 ──
# 每30分钟：自愈引擎巡检
*/30 * * * * cd ${BASE_DIR} && ${PYTHON} bin/lh_auto_heal.py --quiet >> ${LOG_DIR}/auto_heal.log 2>&1

# 每5分钟：服务健康检查
*/5 * * * * ${BASE_DIR}/scripts/health_check.sh >> ${LOG_DIR}/health_check.log 2>&1

# 每天凌晨3点：全量系统体检
0 3 * * * cd ${BASE_DIR} && ${PYTHON} bin/lh_auto_heal.py --full >> ${LOG_DIR}/daily_health.log 2>&1

# 每天凌晨4点：日志归档
0 4 * * * ${BASE_DIR}/scripts/archive_logs.sh >> ${LOG_DIR}/archive.log 2>&1

# 每周日凌晨5点：数据备份
0 5 * * 0 ${BASE_DIR}/scripts/backup_data.sh >> ${LOG_DIR}/backup.log 2>&1
EOF

    crontab /tmp/cron_backup.tmp
    rm -f /tmp/cron_backup.tmp

    log_info "定时任务配置完成"
}

# ────────────────────────────────────────────────────────────────
# 第五步：生成健康检查脚本
# ────────────────────────────────────────────────────────────────
generate_health_check_script() {
    log_info "生成健康检查脚本..."

    mkdir -p "${BASE_DIR}/scripts"

    cat > "${BASE_DIR}/scripts/health_check.sh" << 'SCRIPT'
#!/bin/bash
# 龍魂系统 · 服务健康检查脚本（简版，完整版见 deploy/scripts/health_check.sh）
# 此脚本由 monitor_setup.sh 自动生成，加新服务请改 monitor_setup.sh 中的 SERVICES 数组

BASE_DIR="/opt/longhun-system"
LOG_DIR="/var/log/longhun"
PYTHON="/usr/bin/python3"
ALARM_LOG="${LOG_DIR}/alarm.log"

# ── Bark 推送（如果你配了 BARK_KEY）──
BARK_KEY="${BARK_KEY:-}"
BARK_URL="https://api.day.app/${BARK_KEY}"

# 健康检查日志
TS=$(date '+%Y-%m-%d %H:%M:%S')
echo "[CHECK] ${TS} 开始健康检查" >> "${LOG_DIR}/health_check.log"

ALARM_ITEMS=()
ALARM_COUNT=0

add_alarm() { ALARM_ITEMS+=("$1|$2"); ALARM_COUNT=$((ALARM_COUNT + 1)); echo "[$1] ${TS} $2" >> "${ALARM_LOG}"; }

# 1. 检查所有 systemd 服务
SERVICES=("longhun-skillbus" "longhun-digitalhuman" "longhun-persona" "longhun-dna" "longhun-ecosystem")
ALL_OK=true

for svc in "${SERVICES[@]}"; do
    if systemctl is-active --quiet "${svc}"; then
        echo "  ✅ ${svc} 运行正常" >> "${LOG_DIR}/health_check.log"
    else
        echo "  ❌ ${svc} 异常！尝试重启..." >> "${LOG_DIR}/health_check.log"
        systemctl restart "${svc}"
        sleep 2
        if systemctl is-active --quiet "${svc}"; then
            add_alarm "WARN" "${svc} 异常已自动重启并恢复"
        else
            add_alarm "CRITICAL" "${svc} 重启失败，需人工介入"
        fi
        ALL_OK=false
    fi
done

# 2. 检查端口连通性
for port in 8080 8081 8082 8083 8084; do
    if ss -tlnp | grep -q ":${port} "; then
        echo "  ✅ 端口 ${port} 监听正常" >> "${LOG_DIR}/health_check.log"
    else
        echo "  ❌ 端口 ${port} 未监听！" >> "${LOG_DIR}/health_check.log"
        add_alarm "CRITICAL" "端口 ${port} 未监听"
    fi
done

# 3. 资源监控
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'.' -f1)
[ -z "${CPU_USAGE}" ] && CPU_USAGE=0
MEM_USAGE=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')
[ -z "${MEM_USAGE}" ] && MEM_USAGE=0
DISK_USAGE=$(df -h /data 2>/dev/null | tail -1 | awk '{print $5}' | cut -d'%' -f1)
[ -z "${DISK_USAGE}" ] && DISK_USAGE=0

echo "  📊 CPU: ${CPU_USAGE}% | 内存: ${MEM_USAGE}% | 磁盘: ${DISK_USAGE}%" >> "${LOG_DIR}/health_check.log"

[ "${CPU_USAGE}" -gt 80 ] && add_alarm "WARN" "CPU ${CPU_USAGE}%（阈值 80%）"
[ "${MEM_USAGE}" -gt 80 ] && add_alarm "WARN" "内存 ${MEM_USAGE}%（阈值 80%）"
[ "${DISK_USAGE}" -gt 85 ] && add_alarm "WARN" "磁盘 ${DISK_USAGE}%（阈值 85%）"

# 4. 检查数据盘挂载
if mountpoint -q /data 2>/dev/null; then
    echo "  ✅ 数据盘 /data 挂载正常" >> "${LOG_DIR}/health_check.log"
else
    echo "  ❌ 数据盘 /data 未挂载！尝试挂载..." >> "${LOG_DIR}/health_check.log"
    mount /dev/sdb /data 2>/dev/null
    if mountpoint -q /data 2>/dev/null; then
        add_alarm "INFO" "数据盘自动挂载成功"
    else
        add_alarm "CRITICAL" "数据盘挂载失败，需人工介入"
    fi
fi

# ── Bark 推送 ──
if [ -n "${BARK_KEY}" ] && [ ${ALARM_COUNT} -gt 0 ]; then
    TITLE="🔴 龍魂系统 · ${ALARM_COUNT}条告警"
    BODY=""
    for alert in "${ALARM_ITEMS[@]}"; do
        IFS='|' read -r level text <<< "${alert}"
        BODY="${BODY}\n${text}"
    done
    BODY="${BODY}\n\n📊 CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK:${DISK_USAGE}%\n${TS} · 鲲鹏 TaiShan 200"
    ENC_TITLE=$(echo -n "${TITLE}" | python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read()))" 2>/dev/null || echo "${TITLE}")
    ENC_BODY=$(echo -n "${BODY}" | python3 -c "import sys,urllib.parse; print(urllib.parse.quote(sys.stdin.read()))" 2>/dev/null || echo "${BODY}")
    curl -s "${BARK_URL}/${ENC_TITLE}/${ENC_BODY}?group=龍魂系统&sound=alarm" > /dev/null 2>&1
fi

echo "[CHECK] $(date '+%Y-%m-%d %H:%M:%S') 健康检查完成" >> "${LOG_DIR}/health_check.log"

if [ "$ALL_OK" = false ]; then
    echo "[WARN] 部分服务异常，请查看日志: ${LOG_DIR}/health_check.log"
else
    echo "[OK] 所有服务运行正常 | CPU:${CPU_USAGE}% MEM:${MEM_USAGE}% DISK:${DISK_USAGE}%"
fi
SCRIPT

    chmod +x "${BASE_DIR}/scripts/health_check.sh"
    log_info "健康检查脚本生成完成"
}

# ────────────────────────────────────────────────────────────────
# 第六步：生成日志归档脚本
# ────────────────────────────────────────────────────────────────
generate_archive_script() {
    log_info "生成日志归档脚本..."

    cat > "${BASE_DIR}/scripts/archive_logs.sh" << 'SCRIPT'
#!/bin/bash
# 龍魂系统 · 日志归档脚本

LOG_DIR="/var/log/longhun"
ARCHIVE_DIR="${LOG_DIR}/archive"
RETENTION_DAYS=30

mkdir -p "${ARCHIVE_DIR}"

# 归档昨天的日志
YESTERDAY=$(date -d "yesterday" '+%Y%m%d')
for logfile in "${LOG_DIR}"/*.log; do
    if [ -f "${logfile}" ]; then
        gzip -c "${logfile}" > "${ARCHIVE_DIR}/$(basename ${logfile})_${YESTERDAY}.gz"
        : > "${logfile}"  # 清空原文件，不删除
    fi
done

# 删除超过30天的归档
find "${ARCHIVE_DIR}" -name "*.gz" -mtime +${RETENTION_DAYS} -delete

echo "[ARCHIVE] $(date '+%Y-%m-%d %H:%M:%S') 日志归档完成，保留 ${RETENTION_DAYS} 天"
SCRIPT

    chmod +x "${BASE_DIR}/scripts/archive_logs.sh"
    log_info "日志归档脚本生成完成"
}

# ────────────────────────────────────────────────────────────────
# 第七步：生成数据备份脚本
# ────────────────────────────────────────────────────────────────
generate_backup_script() {
    log_info "生成数据备份脚本..."

    cat > "${BASE_DIR}/scripts/backup_data.sh" << 'SCRIPT'
#!/bin/bash
# 龍魂系统 · 数据备份脚本

BACKUP_DIR="/var/lib/longhun/backups"
DATE_TAG=$(date '+%Y%m%d_%H%M%S')
RETENTION_COUNT=10

mkdir -p "${BACKUP_DIR}"

# 备份 DNA 登记册
if [ -f "/var/lib/longhun/dna/dna_registry.json" ]; then
    cp "/var/lib/longhun/dna/dna_registry.json" "${BACKUP_DIR}/dna_registry_${DATE_TAG}.json"
fi

# 备份数据库
if [ -f "/var/lib/longhun/db/longhun.db" ]; then
    cp "/var/lib/longhun/db/longhun.db" "${BACKUP_DIR}/longhun_${DATE_TAG}.db"
fi

# 备份配置文件
if [ -d "/opt/longhun-system/.codebuddy" ]; then
    tar -czf "${BACKUP_DIR}/codebuddy_config_${DATE_TAG}.tar.gz" -C "/opt/longhun-system" ".codebuddy" 2>/dev/null || true
fi

# 清理旧备份（只保留最近10份）
ls -t "${BACKUP_DIR}"/*.json 2>/dev/null | tail -n +$((RETENTION_COUNT + 1)) | xargs rm -f 2>/dev/null || true
ls -t "${BACKUP_DIR}"/*.db 2>/dev/null | tail -n +$((RETENTION_COUNT + 1)) | xargs rm -f 2>/dev/null || true
ls -t "${BACKUP_DIR}"/*.tar.gz 2>/dev/null | tail -n +$((RETENTION_COUNT + 1)) | xargs rm -f 2>/dev/null || true

echo "[BACKUP] $(date '+%Y-%m-%d %H:%M:%S') 备份完成，保留最近 ${RETENTION_COUNT} 份"
SCRIPT

    chmod +x "${BASE_DIR}/scripts/backup_data.sh"
    log_info "数据备份脚本生成完成"
}

# ────────────────────────────────────────────────────────────────
# 第八步：生成一键状态查看命令
# ────────────────────────────────────────────────────────────────
generate_status_command() {
    log_info "生成龍魂状态查看命令..."

    cat > /usr/local/bin/longhun-status << 'CMD'
#!/bin/bash
# 龍魂系统 · 一键查看状态
# 用法: longhun-status

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}════════════════════════════════════════════${NC}"
echo -e "${CYAN}  🐉 龍魂系统 · 鲲鹏运行状态              ${NC}"
echo -e "${CYAN}  $(date '+%Y-%m-%d %H:%M:%S')              ${NC}"
echo -e "${CYAN}════════════════════════════════════════════${NC}"
echo ""

# 1. 服务状态
echo -e "${CYAN}📦 服务状态:${NC}"
for svc in longhun-skillbus longhun-digitalhuman longhun-persona longhun-dna longhun-ecosystem; do
    if systemctl is-active --quiet "${svc}"; then
        echo -e "  ${GREEN}✅${NC} ${svc}"
    else
        echo -e "  ${RED}❌${NC} ${svc}"
    fi
done

echo ""

# 2. 资源使用
echo -e "${CYAN}📊 资源使用:${NC}"
echo -e "  CPU:    $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}')%"
echo -e "  内存:   $(free -h | grep Mem | awk '{print $3 "/" $2}')"
echo -e "  磁盘:   $(df -h /data | tail -1 | awk '{print $3 "/" $2 " (" $5 ")"}')"
echo -e "  运行时间: $(uptime -p | sed 's/up //')"

echo ""

# 3. 端口监听
echo -e "${CYAN}🔌 端口监听:${NC}"
for port in 8080 8081 8082 8083 8084; do
    if ss -tlnp | grep -q ":${port} "; then
        svc_name=$(ss -tlnp | grep ":${port} " | grep -oP 'longhun-\K[^"]+' || echo "unknown")
        echo -e "  ${GREEN}✅${NC} 端口 ${port}"
    else
        echo -e "  ${RED}❌${NC} 端口 ${port}"
    fi
done

echo ""

# 4. 最近告警
echo -e "${CYAN}⚠️  最近告警（最近5条）:${NC}"
if [ -f "/var/log/longhun/alarm.log" ]; then
    tail -5 "/var/log/longhun/alarm.log" 2>/dev/null | while read line; do
        echo -e "  ${YELLOW}${line}${NC}"
    done
else
    echo -e "  ${GREEN}暂无告警${NC}"
fi

echo ""
echo -e "${CYAN}════════════════════════════════════════════${NC}"
echo -e "${CYAN}  UID9622 · 诸葛鑫 · 龍魂系统              ${NC}"
echo -e "${CYAN}════════════════════════════════════════════${NC}"
CMD

    chmod +x /usr/local/bin/longhun-status
    log_info "龍魂状态查看命令已安装: longhun-status"
}

# ────────────────────────────────────────────────────────────────
# 第九步：生成一键部署脚本（汇总）
# ────────────────────────────────────────────────────────────────
generate_deploy_script() {
    log_info "生成一键部署脚本..."

    cat > "${BASE_DIR}/deploy.sh" << 'DEPLOY'
#!/bin/bash
# 🐉 龍魂系统 · 鲲鹏一键部署脚本
# 用法: sudo bash deploy.sh

set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "${BASE_DIR}"

echo "╔══════════════════════════════════════════════════╗"
echo "║  🐉 龍魂系统 · 鲲鹏一键部署                      ║"
echo "╚══════════════════════════════════════════════════╝"

# 1. 检测环境
echo ""
echo "[1/6] 检测环境..."
python3 --version || { echo "请先安装 Python3"; exit 1; }
which systemctl || { echo "请使用 openEuler/CentOS 系统"; exit 1; }
echo "  ✅ 环境检测通过"

# 2. 安装依赖
echo ""
echo "[2/6] 安装 Python 依赖..."
pip3 install flask fastapi uvicorn psutil -q
echo "  ✅ 依赖安装完成"

# 3. 执行本监控脚本
echo ""
echo "[3/6] 配置服务监控..."
bash "${BASE_DIR}/scripts/monitor_setup.sh"
echo "  ✅ 服务监控配置完成"

# 4. 启动服务
echo ""
echo "[4/6] 启动龍魂服务..."
systemctl daemon-reload
for svc in longhun-skillbus longhun-digitalhuman longhun-persona longhun-dna longhun-ecosystem; do
    systemctl enable "${svc}" 2>/dev/null
    systemctl start "${svc}" 2>/dev/null
done
echo "  ✅ 服务启动完成"

# 5. 设置定时任务
echo ""
echo "[5/6] 配置定时任务..."
# 这里的 crontab 由 monitor_setup.sh 处理
echo "  ✅ 定时任务配置完成"

# 6. 验证
echo ""
echo "[6/6] 验证部署..."
sleep 3
bash /usr/local/bin/longhun-status

echo ""
echo "  ✅ 部署完成！"
echo ""
echo "  常用命令:"
echo "    longhun-status          # 查看所有服务状态"
echo "    journalctl -u longhun-skillbus   # 查看某服务日志"
echo "    systemctl restart longhun-skillbus  # 重启某服务"
DEPLOY

    chmod +x "${BASE_DIR}/deploy.sh"
    log_info "一键部署脚本生成完成: ${BASE_DIR}/deploy.sh"
}

# ────────────────────────────────────────────────────────────────
# 主流程
# ────────────────────────────────────────────────────────────────
main() {
    echo ""
    echo -e "${CYAN}══════════════════════════════════════════════════${NC}"
    echo -e "${CYAN}  🐉 龍魂系统 · 鲲鹏服务监控配置                  ${NC}"
    echo -e "${CYAN}  DNA: #龍芯⚡️丙午·乙未·丙戌·甲午·䷕贲-KUNPENG-MONITOR-v1.0    ${NC}"
    echo -e "${CYAN}══════════════════════════════════════════════════${NC}"
    echo ""

    # 检查是否以 root 运行
    if [ "$EUID" -ne 0 ]; then
        log_error "请以 root 权限运行此脚本 (sudo bash $0)"
        exit 1
    fi

    # 检查基础目录
    if [ ! -d "${BASE_DIR}" ]; then
        log_error "龍魂系统目录不存在: ${BASE_DIR}"
        log_error "请先 git clone 龍魂系统到 ${BASE_DIR}"
        exit 1
    fi

    setup_directories
    generate_systemd_services
    generate_health_check_script
    generate_archive_script
    generate_backup_script
    generate_status_command
    generate_deploy_script
    enable_and_start_services
    setup_cron_jobs

    echo ""
    echo -e "${GREEN}══════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ 龍魂系统服务监控配置完成！                    ${NC}"
    echo -e "${GREEN}══════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "  ${CYAN}查看状态:${NC}  longhun-status"
    echo -e "  ${CYAN}查看日志:${NC}  ${LOG_DIR}/"
    echo -e "  ${CYAN}告警日志:${NC}  ${ALARM_LOG}"
    echo -e "  ${CYAN}健康日志:${NC}  ${HEALTH_LOG}"
    echo ""
}

main "$@"
