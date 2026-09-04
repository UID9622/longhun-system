#!/usr/bin/env bash
# ============================================================
# 龍魂感知层 · 卸载脚本（macOS 版 · P0 默认冻结不硬删）
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-UNINSTALL-MAC-v2.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 安全策略（对齐 P0「不删除只冻结」）：
#   默认 = 冻结归档到 ~/longhun-archive-时间戳（不删任何东西）
#   彻底删除 = 需再输入 DELETE 二次确认
# 用法: bash scripts/uninstall_longhun.sh
# ============================================================
set -euo pipefail

PROJECT_DIR="${HOME}/longhun-system"
STAMP=$(date +%Y%m%d_%H%M%S)
ARCHIVE_DIR="${HOME}/longhun-archive-${STAMP}"

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
ok()   { echo -e "${GREEN}✓${NC} $*"; }
warn() { echo -e "${YELLOW}!${NC} $*"; }
info() { echo -e "→ $*"; }

echo "=============================================="
echo " 龍魂感知层 · 卸载 (macOS) v2.0"
echo "=============================================="
echo ""
echo "本脚本将执行："
echo "  1. 冻结归档整个项目 → ${ARCHIVE_DIR}（默认，不删除）"
echo "  2. 彻底删除项目（需再输 DELETE 二次确认）"
echo ""
echo "⚠️ 卸载是最后手段。想清楚再动手。"
echo ""

read -p "确认开始？输入 F 冻结归档 / 输入 D 彻底删除 / 其他=取消: " action
case "${action}" in
    F|f)
        info "冻结归档模式..."
        if [[ -d "${PROJECT_DIR}" ]]; then
            mv "${PROJECT_DIR}" "${ARCHIVE_DIR}" && ok "项目已冻结 → ${ARCHIVE_DIR}"
            echo "  恢复命令: mv ${ARCHIVE_DIR} ${PROJECT_DIR}"
        else
            warn "项目目录不存在，跳过"
        fi
        ;;
    D|d)
        read -p "彻底删除将不可恢复！输入 DELETE（全大写）确认: " confirm
        if [[ "${confirm}" != "DELETE" ]]; then
            echo "已取消。什么都没删。"
            exit 0
        fi
        # 即使彻底删除也先留冻结副本（P0 不删除只冻结）
        info "先冻结一份..."
        if [[ -d "${PROJECT_DIR}" ]]; then
            mv "${PROJECT_DIR}" "${ARCHIVE_DIR}" && ok "冻结副本 → ${ARCHIVE_DIR}"
        fi
        # 仅当用户再次要求且拥有冻结副本后，才真正清理用户级无关文件（本项目不动）
        info "项目已冻结。如需清除 Python 用户包，可手动执行："
        info "  python3 -m pip uninstall -y numpy sounddevice faster-whisper requests pillow"
        ;;
    *)
        echo "已取消。什么都没发生。"
        exit 0
        ;;
esac

echo ""
echo "卸载/冻结完成。"
echo "冻结位置: ${ARCHIVE_DIR}"
echo "恢复命令: mv ${ARCHIVE_DIR} ${PROJECT_DIR}"
echo ""
echo "DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-UNINSTALL-MAC-DONE"
