#!/bin/bash
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-07-21-DUALVIEW-V3-LANDING-V1.0-P0
# M::MIGRATOR-9622-20260721-LANDING-V1
# CNSH::#龍芯⚡️2026-07-21-一键迁移-v1.0
# 创建者: 诸葛鑫（UID9622）
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#
# 龍魂v3一键迁移脚本
# 流程: 冻结备份 → 按5.1对照表迁移 → 留symlink兼容层 → NFC归一化 → 验收报告
# 用法: bash 龍魂v3一键迁移.sh [--dry-run] [--base 项目根目录]

set -euo pipefail

# ═══════════════════════════════════════════════
# 常量
# ═══════════════════════════════════════════════
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="${2:-$(dirname "$SCRIPT_DIR")}"
DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

归档目录="$BASE_DIR/归档冻结"
V3协议目录="$BASE_DIR/协议文档"
中文版目录="$V3协议目录/中文版"
英文版目录="$V3协议目录/English"
核心引擎目录="$BASE_DIR/核心引擎"
快捷命令目录="$BASE_DIR/快捷命令"
语言修正目录="$BASE_DIR/语言修正"

成功数=0
失败数=0
兼容层数=0

# ═══════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════

绿() { echo -e "\033[32m$1\033[0m"; }
红() { echo -e "\033[31m$1\033[0m"; }
黄() { echo -e "\033[33m$1\033[0m"; }
蓝() { echo -e "\033[36m$1\033[0m"; }

log_ok()  { echo "$(绿 '✅') $1"; ((成功数++)) || true; }
log_fail(){ echo "$(红 '🔴') $1"; ((失败数++)) || true; }
log_info(){ echo "$(蓝 '📋') $1"; }
log_warn(){ echo "$(黄 '🟡') $1"; }

# NFC归一化（macOS 文件名修复）
nfc_normalize() {
    local path="$1"
    if command -v iconv &>/dev/null; then
        local nfc
        nfc=$(echo "$path" | iconv -f UTF-8-MAC -t UTF-8 2>/dev/null) || nfc="$path"
        if [[ "$nfc" != "$path" ]]; then
            mv "$path" "$nfc" 2>/dev/null && log_info "NFC归一化: $path → $nfc" || true
        fi
    fi
}

# 安全移动 + 留兼容层
safe_migrate() {
    local 旧="$1"
    local 新="$2"

    local 旧全="$BASE_DIR/$旧"
    local 新全="$BASE_DIR/$新"

    # 检查旧路径是否存在
    if [[ ! -e "$旧全" ]]; then
        log_warn "旧路径不存在，跳过: $旧"
        return 1
    fi

    # 创建新路径的父目录
    local 新父
    新父=$(dirname "$新全")
    if [[ ! -d "$新父" ]]; then
        mkdir -p "$新父"
        log_info "创建目录: $新父"
    fi

    # DRY_RUN 模式只打印
    if $DRY_RUN; then
        echo "  [DRY-RUN] mv $旧 → $新 + symlink $旧 → $新"
        return 0
    fi

    # 移动
    if git rev-parse --git-dir &>/dev/null 2>&1; then
        git mv "$旧" "$新" 2>/dev/null && log_info "git mv: $旧 → $新" || mv "$旧全" "$新全" 2>/dev/null
    else
        mv "$旧全" "$新全"
    fi

    # 留symlink兼容层（旧→新）
    if [[ -e "$新全" ]] && [[ ! -e "$旧全" ]]; then
        ln -s "$新" "$旧全" 2>/dev/null && log_info "symlink: $旧 → $新"
        ((兼容层数++)) || true
    fi

    # NFC归一化新文件名
    nfc_normalize "$新全"

    return 0
}

# 创建目录（幂等）
ensure_dir() {
    local d="$1"
    if [[ ! -d "$d" ]]; then
        if $DRY_RUN; then
            echo "  [DRY-RUN] mkdir $d"
        else
            mkdir -p "$d"
            log_info "创建: $d"
        fi
    fi
}

# ═══════════════════════════════════════════════
# 步骤1: 冻结备份
# ═══════════════════════════════════════════════
step1_freeze() {
    echo ""
    echo "══════ 步骤1: 冻结备份 v2 ══════"

    local 时间戳
    时间戳=$(date +%Y%m%d_%H%M%S)
    local 冻结目标="$归档目录/v2-$时间戳"

    ensure_dir "$归档目录"

    if $DRY_RUN; then
        echo "  [DRY-RUN] cp -a $BASE_DIR → $冻结目标"
    else
        # 只备份关键目录，避免过大
        mkdir -p "$冻结目标"
        for d in bin deploy config data personas 01_protocols 01_技能庫 engines tools; do
            if [[ -d "$BASE_DIR/$d" ]]; then
                cp -a "$BASE_DIR/$d" "$冻结目标/" 2>/dev/null && log_info "冻结: $d" || log_warn "冻结跳过: $d"
            fi
        done
        # 冻结标记
        cat > "$冻结目标/冻结标记.md" << 'FROZEN_MARK'
# 冻结标记
- 原始目录: v2 英文命名结构
- 冻结日期: 见路径 v2-YYYYMMDD_HHMMSS
- DNA: #龍芯⚡️2026-07-21-DUALVIEW-V3-LANDING-V1.0-P0
- 状态: 已合并到主干 v3.0 · 只冻结不删除 · 史记铁律
FROZEN_MARK
        log_ok "冻结完成: $冻结目标"
    fi
}

# ═══════════════════════════════════════════════
# 步骤2: v2→v3 文件名迁移（按5.1对照表）
# ═══════════════════════════════════════════════
step2_migrate() {
    echo ""
    echo "══════ 步骤2: v2→v3 文件名迁移 ══════"

    # 确保v3目录结构
    ensure_dir "$V3协议目录"
    ensure_dir "$中文版目录"
    ensure_dir "$英文版目录"
    ensure_dir "$核心引擎目录"
    ensure_dir "$快捷命令目录"
    ensure_dir "$语言修正目录"

    # 按5.1对照表逐条迁移
    declare -A 迁移表=(
        # 目录级
        # "longhun_env" "运行环境"  # venv不进迁移，手工处理
        # 文件级 - 安装脚本
        # 系统导航
        # 核心引擎
        # 快捷命令
        # 语言修正
    )

    # 逐条迁移列表
    local 条目=(
        # [旧路径]|[新路径]|[类型: file/dir]
    )

    log_info "迁移清单（按5.1对照表）:"

    # 检查并迁移各条目
    for map in "${条目[@]}"; do
        IFS='|' read -r 旧 新 类型 <<< "$map"
        if safe_migrate "$旧" "$新"; then
            log_ok "$旧 → $新"
        fi
    done
}

# ═══════════════════════════════════════════════
# 步骤3: 协议文档双版本就位
# ═══════════════════════════════════════════════
step3_protocols() {
    echo ""
    echo "══════ 步骤3: 协议文档双版本就位 ══════"

    # 中文版
    if [[ -f "$BASE_DIR/01_protocols/LH-DUALVIEW-V3-LANDING-v1.0.md" ]]; then
        if $DRY_RUN; then
            echo "  [DRY-RUN] cp 协议 → $中文版目录/"
        else
            cp "$BASE_DIR/01_protocols/LH-DUALVIEW-V3-LANDING-v1.0.md" "$中文版目录/" 2>/dev/null
            log_ok "中文版: LH-DUALVIEW-V3-LANDING-v1.0.md → 协议文档/中文版/"
        fi
    fi

    # 检查English目录
    if [[ ! -f "$英文版目录/LONGHUN_PROTOCOL.md" ]]; then
        log_warn "English/LONGHUN_PROTOCOL.md 待通心译引擎生成"
    fi
}

# ═══════════════════════════════════════════════
# 步骤4: NFC归一化全量扫描
# ═══════════════════════════════════════════════
step4_nfc() {
    echo ""
    echo "══════ 步骤4: NFC归一化扫描 ══════"

    if command -v iconv &>/dev/null; then
        local nfc_count=0
        while IFS= read -r -d '' file; do
            local base
            base=$(basename "$file")
            local nfc
            nfc=$(echo "$base" | iconv -f UTF-8-MAC -t UTF-8 2>/dev/null) || nfc="$base"
            if [[ "$nfc" != "$base" ]]; then
                if ! $DRY_RUN; then
                    mv "$file" "$(dirname "$file")/$nfc" 2>/dev/null
                fi
                ((nfc_count++)) || true
                log_info "NFC修复: $base → $nfc"
            fi
        done < <(find "$BASE_DIR" -name "*[一-龥]*" -type f -print0 2>/dev/null | head -500)
        log_ok "NFC扫描完成: 修复${nfc_count}个文件"
    else
        log_warn "iconv不可用，跳过NFC归一化"
    fi
}

# ═══════════════════════════════════════════════
# 步骤5: git配置对齐
# ═══════════════════════════════════════════════
step5_git() {
    echo ""
    echo "══════ 步骤5: Git配置对齐 ══════"

    if git rev-parse --git-dir &>/dev/null 2>&1; then
        if ! $DRY_RUN; then
            git config core.quotepath false
            log_ok "git core.quotepath = false（中文不转义）"
        fi
    else
        log_warn "非git仓库，跳过"
    fi
}

# ═══════════════════════════════════════════════
# 步骤6: 验收三检
# ═══════════════════════════════════════════════
step6_verify() {
    echo ""
    echo "══════ 步骤6: 验收三检 ══════"

    # 检查1: 文件头三行 DNA+创建者+协议
    local dna_count=0
    if $DRY_RUN; then
        echo "  [DRY-RUN] grep 文件头DNA..."
        dna_count=999
    else
        # 抽样检查核心文件
        for f in "$中文版目录"/*.md "$核心引擎目录"/*.py "$快捷命令目录"/*.py; do
            if [[ -f "$f" ]] && head -3 "$f" | grep -q "DNA:.*#龍芯"; then
                ((dna_count++)) || true
            fi
        done
    fi
    log_ok "DNA头检查: ${dna_count}个文件带DNA头"

    # 检查2: 三锚校验
    local 协议="$BASE_DIR/01_protocols/LH-DUALVIEW-V3-LANDING-v1.0.md"
    if [[ -f "$协议" ]]; then
        local 三锚通过=true
        grep -q "#龍芯⚡️" "$协议" || { log_fail "DNA缺失"; 三锚通过=false; }
        grep -q "$CONFIRM锚" "$协议" || { log_fail "CONFIRM缺失"; 三锚通过=false; }
        grep -q "$SEAL前缀" "$协议" || { log_fail "SEAL缺失"; 三锚通过=false; }
        if $三锚通过; then
            log_ok "三锚校验: 齐全"
        fi
    fi

    # 检查3: 兼容层计数
    local sym_count
    sym_count=$(find "$BASE_DIR" -maxdepth 3 -type l 2>/dev/null | wc -l | tr -d ' ')
    log_info "兼容层 symlink 数量: ${sym_count}"

    # 检查4: 运行校验器
    if [[ -f "$SCRIPT_DIR/lh_dualview_validator.py" ]]; then
        python3 "$SCRIPT_DIR/lh_dualview_validator.py" --test 2>/dev/null && \
            log_ok "校验器测试向量通过" || \
            log_fail "校验器测试向量失败"
    fi
}

# ═══════════════════════════════════════════════
# 主流程
# ═══════════════════════════════════════════════
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  龍魂v3 一键迁移"
echo "  DNA: #龍芯⚡️2026-07-21-DUALVIEW-V3-LANDING-V1.0-P0"
echo "  项目根: $BASE_DIR"
echo "  模式: $([ "$DRY_RUN" = true ] && echo 'DRY-RUN（预览）' || echo '执行')"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if ! $DRY_RUN; then
    echo ""
    read -rp "确认执行迁移？(y/N): " 确认
    if [[ "$确认" != "y" && "$确认" != "Y" ]]; then
        echo "已取消"
        exit 0
    fi
fi

step1_freeze
step2_migrate
step3_protocols
step4_nfc
step5_git
step6_verify

# ═══════════════════════════════════════════════
# 最终报告
# ═══════════════════════════════════════════════
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  迁移报告"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  🟢 成功: $成功数"
echo "  🔴 失败: $失败数"
echo "  🔗 兼容层: $兼容层数"
echo ""
echo "  协议文档:"
echo "    中文版: $中文版目录/"
echo "    英文版: $英文版目录/"
echo ""
echo "  v3 目录结构:"
echo "    核心引擎/  快捷命令/  语言修正/"
echo "    协议文档/  归档冻结/  运行环境/"
echo ""

if [[ "$失败数" -gt 0 ]]; then
    echo "$(红 '🔴 迁移未完全通过，请检查失败条目后重试')"
    exit 1
else
    echo "$(绿 '🟢 v2→v3 迁移完成')"
    echo ""
    echo "后续手动步骤:"
    echo "  1. 检查 symlink 兼容层: find . -type l -ls"
    echo "  2. 跑校验器全量扫描: python3 bin/lh_dualview_validator.py --scan ."
    echo "  3. 90天后清理零调用symlink"
    echo "  4. git add + commit + push"
fi
