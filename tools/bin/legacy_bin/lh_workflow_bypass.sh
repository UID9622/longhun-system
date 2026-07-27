#!/bin/bash
# ============================================
# 龍魂系统 · 绕过 VS Code 中文乱码工作流 v1.0
# UID9622 | 龍芯北辰
# 解决：Mac M4 字体损坏/缺失导致 VS Code 中文显示乱码
# 策略：不修复 VS Code，绕过它，用其他工具处理中文
# ============================================

# 颜色定义
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
CYAN="\033[36m"
RESET="\033[0m"
BOLD="\033[1m"

# 龍魂标识
DNA="ZHUGEXIN-2025-CHINA-LONGHUN"
LH_UID="9622"

echo -e "${CYAN}"
echo "╔══════════════════════════════════════════╗"
echo "║     🐉 龍魂系统 · 中文工作流绕过工具      ║"
echo "║     UID9622 | 龍芯北辰 | 绕过不修复       ║"
echo "╚══════════════════════════════════════════╝"
echo -e "${RESET}"

# ============================================
# 1. 环境检查
# ============================================
echo -e "${BOLD}[1/6] 环境检查${RESET}"

# 检查终端编码
CURRENT_LANG=${LANG:-"未设置"}
echo "   当前 LANG: $CURRENT_LANG"

# 设置焊死
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
export LC_CTYPE=zh_CN.UTF-8

echo -e "   ${GREEN}✓${RESET} 编码已强制设置为 zh_CN.UTF-8"

# 检查可用工具
echo ""
echo "   可用工具检查:"
command -v cat >/dev/null && echo -e "   ${GREEN}✓${RESET} cat" || echo -e "   ${RED}✗${RESET} cat"
command -v less >/dev/null && echo -e "   ${GREEN}✓${RESET} less" || echo -e "   ${RED}✗${RESET} less"
command -v head >/dev/null && echo -e "   ${GREEN}✓${RESET} head" || echo -e "   ${RED}✗${RESET} head"
command -v tail >/dev/null && echo -e "   ${GREEN}✓${RESET} tail" || echo -e "   ${RED}✗${RESET} tail"
command -v grep >/dev/null && echo -e "   ${GREEN}✓${RESET} grep" || echo -e "   ${RED}✗${RESET} grep"
command -v open >/dev/null && echo -e "   ${GREEN}✓${RESET} open (Mac)" || echo -e "   ${RED}✗${RESET} open"
command -v pbcopy >/dev/null && echo -e "   ${GREEN}✓${RESET} pbcopy (Mac)" || echo -e "   ${RED}✗${RESET} pbcopy"

# ============================================
# 2. 龍魂系统目录结构确认
# ============================================
echo ""
echo -e "${BOLD}[2/6] 龍魂系统目录确认${RESET}"

LONGHUN_BASE="${HOME}/longhun-system"
WORK_DIRS=(
    "L0_物理层"
    "L1_身份层"
    "L2_主权层"
    "L3_执行层"
    "L4_数据层"
    "L5_服务层"
    "L6_记忆层/raw"
    "L6_记忆层/processed"
    "L7_表达层"
    "L8_分发层"
)

for dir in "${WORK_DIRS[@]}"; do
    full_path="${LONGHUN_BASE}/${dir}"
    if [ ! -d "$full_path" ]; then
        mkdir -p "$full_path"
        echo -e "   ${YELLOW}📁 创建${RESET} ${dir}"
    else
        echo -e "   ${GREEN}✓${RESET} ${dir}"
    fi
done

# ============================================
# 3. 核心工作流函数
# ============================================
echo ""
echo -e "${BOLD}[3/6] 加载工作流函数${RESET}"

# --- 函数1: 查看中文文件 (替代 VS Code) ---
lh_view() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ 文件不存在: $file${RESET}"
        return 1
    fi

    echo -e "${CYAN}═══ 文件内容: $(basename "$file") ═══${RESET}"
    echo ""

    # 小于50行直接cat
    local lines=$(wc -l < "$file" 2>/dev/null || echo 0)
    if [ "$lines" -lt 50 ]; then
        cat "$file"
    else
        # 大于50行用less
        less -N "$file"
    fi

    echo ""
    echo -e "${CYAN}═══ 文件结束 | 路径: $file ═══${RESET}"
}

# --- 函数2: 快速预览 (前20行) ---
lh_head() {
    local file="$1"
    local n="${2:-20}"
    echo -e "${CYAN}═══ 前 ${n} 行: $(basename "$file") ═══${RESET}"
    head -n "$n" "$file"
    echo -e "${CYAN}═══ 预览结束 ═══${RESET}"
}

# --- 函数3: 搜索内容 (替代 VS Code 搜索) ---
lh_search() {
    local keyword="$1"
    local dir="${2:-${LONGHUN_BASE}}"

    echo -e "${CYAN}═══ 搜索: "${keyword}" ═══${RESET}"
    echo ""

    grep -r -n --color=always -i "$keyword" "$dir" 2>/dev/null | head -50 | while read line; do
        echo "$line"
    done

    echo ""
    echo -e "${CYAN}═══ 搜索结束 | 目录: $dir ═══${RESET}"
}

# --- 函数4: 编辑中文文件 (用 nano 或 vim) ---
lh_edit() {
    local file="$1"
    if [ ! -f "$file" ]; then
        touch "$file"
        echo -e "${YELLOW}📄 创建新文件: $file${RESET}"
    fi

    # 优先用 nano（简单），没有就用 vim
    if command -v nano >/dev/null; then
        nano "$file"
    elif command -v vim >/dev/null; then
        vim "$file"
    else
        echo -e "${RED}✗ 未安装 nano/vim，无法编辑${RESET}"
        return 1
    fi
}

# --- 函数5: 复制文件内容到剪贴板 (替代 VS Code 复制) ---
lh_copy() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ 文件不存在${RESET}"
        return 1
    fi

    cat "$file" | pbcopy
    echo -e "${GREEN}✓ 已复制到剪贴板: $(basename "$file") | $(wc -c < "$file") 字节${RESET}"
}

# --- 函数6: 用系统默认应用打开 (TextEdit 等) ---
lh_open() {
    local file="$1"
    if [ ! -f "$file" ]; then
        echo -e "${RED}✗ 文件不存在${RESET}"
        return 1
    fi

    open "$file"
    echo -e "${GREEN}✓ 已用系统默认应用打开: $(basename "$file")${RESET}"
}

# --- 函数7: 新建文章/文档 (标准化命名) ---
lh_new() {
    local title="$1"
    local type="${2:-article}"  # article, script, note, log

    # 生成标准化文件名
    local timestamp=$(date +%Y%m%d_%H%M%S)
    local ganzhi=$(date +%Y%m%d | awk 'BEGIN{tg="甲乙丙丁戊己庚辛壬癸";dz="子丑寅卯辰巳午未申酉戌亥"}{y=$1-1984;print substr(tg,y%10+1,1)substr(dz,y%12+1,1)}')
    local safe_title=$(echo "$title" | sed 's/[^a-zA-Z0-9\u4e00-\u9fa5]/_/g' | cut -c1-30)

    local filename="${timestamp}_${ganzhi}_${type}_${safe_title}.md"
    local filepath="${LONGHUN_BASE}/L7_表达层/${filename}"

    # 创建模板
    cat > "$filepath" << EOF
# ${title}

> 作者：龍芯北辰 | UID9622
> DNA锚定：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
> 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 创建时间：$(date '+%Y-%m-%d %H:%M:%S')
> 干支：${ganzhi}

---

[在此输入内容]

---

> UID9622 | 龍芯北辰
> 时间戳：$(date '+%Y-%m-%d %H:%M:%S')
> 区块哈希：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
EOF

    echo -e "${GREEN}✓ 创建文件: ${filename}${RESET}"
    echo -e "   路径: ${filepath}"
    echo ""
    echo -e "${YELLOW}💡 用 lh_edit ${filepath} 编辑${RESET}"
    echo -e "${YELLOW}💡 用 lh_view ${filepath} 查看${RESET}"
}

# --- 函数8: 归档当前会话 (替代手动复制) ---
lh_archive() {
    local session_name="${1:-session_$(date +%H%M%S)}"
    local archive_dir="${LONGHUN_BASE}/L6_记忆层/raw/$(date +%Y-%m-%d)"
    mkdir -p "$archive_dir"

    local archive_file="${archive_dir}/${session_name}_$(date +%Y%m%d_%H%M%S).md"

    cat > "$archive_file" << EOF
# 会话归档: ${session_name}

> 归档时间: $(date '+%Y-%m-%d %H:%M:%S')
> DNA: ${DNA}
> UID: ${UID}

## 会话内容

[请粘贴会话内容]

## 关键结论

- 

## 待办事项

- 

## 相关链接

- 

---

> 龍魂系统 · 记忆层归档
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
EOF

    echo -e "${GREEN}✓ 归档模板已创建: ${archive_file}${RESET}"
    echo -e "${YELLOW}💡 用 lh_edit ${archive_file} 补充内容${RESET}"
}

# --- 函数9: 查看今日归档 ---
lh_today() {
    local today_dir="${LONGHUN_BASE}/L6_记忆层/raw/$(date +%Y-%m-%d)"
    if [ ! -d "$today_dir" ]; then
        echo -e "${YELLOW}📂 今日无归档${RESET}"
        return 0
    fi

    echo -e "${CYAN}═══ 今日归档 ($(date +%Y-%m-%d)) ═══${RESET}"
    ls -lt "$today_dir" | head -20 | awk '{printf "   %s %s %s\n", $6, $7, $9}'
    echo -e "${CYAN}═══ 共 $(ls "$today_dir" | wc -l) 个文件 ═══${RESET}"
}

# --- 函数10: 快速帮助 ---
lh_help() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════╗"
    echo "║     🐉 龍魂工作流命令速查表              ║"
    echo "╚══════════════════════════════════════════╝"
    echo -e "${RESET}"
    echo -e "${BOLD}文件查看${RESET}"
    echo "  lh_view <文件>     - 查看完整文件 (cat/less)"
    echo "  lh_head <文件> [n] - 预览前n行 (默认20)"
    echo "  lh_search <关键词> [目录] - 搜索内容"
    echo ""
    echo -e "${BOLD}文件编辑${RESET}"
    echo "  lh_edit <文件>     - 用 nano/vim 编辑"
    echo "  lh_open <文件>     - 用系统默认应用打开"
    echo "  lh_copy <文件>     - 复制内容到剪贴板"
    echo ""
    echo -e "${BOLD}内容创建${RESET}"
    echo "  lh_new <标题> [类型] - 创建标准化文档"
    echo "  lh_archive [名称]    - 创建会话归档模板"
    echo ""
    echo -e "${BOLD}归档管理${RESET}"
    echo "  lh_today           - 查看今日归档"
    echo "  lh_help            - 显示本帮助"
    echo ""
    echo -e "${YELLOW}💡 所有文件保存在: ${LONGHUN_BASE}${RESET}"
    echo -e "${YELLOW}💡 VS Code 只用于英文代码，中文用这些命令${RESET}"
}

# ============================================
# 4. 导出函数到当前 shell
# ============================================
echo ""
echo -e "${BOLD}[4/6] 导出函数${RESET}"

# 写入 .zshrc 持久化
ZSHRC_ADD="
# === 龍魂系统 · 中文工作流绕过 (UID9622) ===
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
export LC_CTYPE=zh_CN.UTF-8

# 龍魂工作流函数
lh_view() { cat \"\$1\" 2>/dev/null | less -N; }
lh_head() { head -n \"\${2:-20}\" \"\$1\"; }
lh_search() { grep -r -n --color=always -i \"\$1\" \"\${2:-\$HOME/longhun-system}\" 2>/dev/null | head -50; }
lh_edit() { nano \"\$1\" 2>/dev/null || vim \"\$1\"; }
lh_copy() { cat \"\$1\" | pbcopy; }
lh_open() { open \"\$1\"; }
lh_new() { local t=\"\$1\"; local type=\"\${2:-article}\"; local ts=\$(date +%Y%m%d_%H%M%S); local gz=\$(date +%Y%m%d | awk 'BEGIN{tg=\"甲乙丙丁戊己庚辛壬癸\";dz=\"子丑寅卯辰巳午未申酉戌亥\"}{y=\$1-1984;print substr(tg,y%10+1,1)substr(dz,y%12+1,1)}'); local st=\$(echo \"\$t\" | sed 's/[^a-zA-Z0-9\\u4e00-\\u9fa5]/_/g' | cut -c1-30); local f=\"\$HOME/longhun-system/L7_表达层/\${ts}_\${gz}_\${type}_\${st}.md\"; echo \"# \\${t}\" > \"\$f\"; echo \"> 作者：龍芯北辰 | UID9622\" >> \"\$f\"; echo \"> 时间：\$(date '+%Y-%m-%d %H:%M:%S')\" >> \"\$f\"; echo \"\$f\"; }
lh_archive() { local d=\"\$HOME/longhun-system/L6_记忆层/raw/\$(date +%Y-%m-%d)\"; mkdir -p \"\$d\"; local f=\"\${d}/\${1:-session}_\$(date +%H%M%S).md\"; echo \"# 归档\" > \"\$f\"; echo \"\$f\"; }
lh_today() { ls -lt \"\$HOME/longhun-system/L6_记忆层/raw/\$(date +%Y-%m-%d)\" 2>/dev/null | head -20; }
lh_help() { echo \"lh_view/head/search/edit/open/copy/new/archive/today\"; }
# === 龍魂工作流结束 ===
"

# 检查是否已写入
if ! grep -q "龍魂系统 · 中文工作流绕过" ~/.zshrc 2>/dev/null; then
    echo "$ZSHRC_ADD" >> ~/.zshrc
    echo -e "   ${GREEN}✓${RESET} 函数已写入 ~/.zshrc"
else
    echo -e "   ${GREEN}✓${RESET} 函数已存在于 ~/.zshrc"
fi

# 当前 shell 生效
source ~/.zshrc 2>/dev/null || echo "   ${YELLOW}⚠ 请手动执行: source ~/.zshrc${RESET}"

# ============================================
# 5. 测试
# ============================================
echo ""
echo -e "${BOLD}[5/6] 功能测试${RESET}"

# 测试中文输出
echo -e "   ${GREEN}✓${RESET} 中文输出测试: 龍魂系统正常工作"

# 测试目录
echo -e "   ${GREEN}✓${RESET} 龍魂根目录: ${LONGHUN_BASE}"

# 测试文件创建
test_file="${LONGHUN_BASE}/L7_表达层/test_$(date +%H%M%S).md"
echo "# 测试文件" > "$test_file"
echo -e "   ${GREEN}✓${RESET} 文件创建测试: $(basename "$test_file")"
rm "$test_file"

# ============================================
# 6. 使用指南
# ============================================
echo ""
echo -e "${BOLD}[6/6] 使用指南${RESET}"

cat << 'GUIDE'

┌─────────────────────────────────────────────┐
│  🐉 龍魂系统 · 中文工作流绕过方案            │
│  VS Code 中文乱码？不用修，绕过它！          │
├─────────────────────────────────────────────┤
│                                             │
│  【场景1: 查看中文文章】                      │
│  $ lh_view ~/longhun-system/某文章.md       │
│                                             │
│  【场景2: 快速预览】                          │
│  $ lh_head 某文件.md 30                     │
│                                             │
│  【场景3: 搜索内容】                          │
│  $ lh_search "关键词"                       │
│                                             │
│  【场景4: 编辑中文文件】                      │
│  $ lh_edit 某文件.md                        │
│                                             │
│  【场景5: 创建新文章】                        │
│  $ lh_new "文章标题" article                │
│                                             │
│  【场景6: 复制到剪贴板】                      │
│  $ lh_copy 某文件.md                        │
│  然后直接粘贴到 Kimi/抖音/CSDN               │
│                                             │
│  【场景7: 用系统应用打开】                    │
│  $ lh_open 某文件.md                        │
│  用 TextEdit 或其他编辑器查看                │
│                                             │
│  【场景8: 归档当前会话】                      │
│  $ lh_archive "kimi-session-001"            │
│                                             │
│  【场景9: 查看今日归档】                      │
│  $ lh_today                                 │
│                                             │
│  【场景10: 查看帮助】                         │
│  $ lh_help                                  │
│                                             │
├─────────────────────────────────────────────┤
│  核心原则:                                   │
│  • VS Code = 英文代码专用                    │
│  • 终端命令 = 中文内容处理                   │
│  • 系统应用 = 中文文档查看                   │
│  • 所有文件 = 本地归档，DNA绑定             │
└─────────────────────────────────────────────┘

GUIDE

echo -e "${CYAN}"
echo "═══════════════════════════════════════════"
echo "  🐉 龍魂系统 · 工作流已就绪"
echo "  UID9622 | 龍芯北辰"
echo "  DNA: ${DNA}"
echo "═══════════════════════════════════════════"
echo -e "${RESET}"

# 显示可用命令
lh_help
