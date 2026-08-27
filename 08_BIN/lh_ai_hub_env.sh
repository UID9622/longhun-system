#!/usr/bin/env zsh
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·AI产出归集环境 v1.0                                   ║
# ║  DNA: #龍芯⚡️丙午·丙申·戊午·亥时·AI-HUB-ENV-V1.0-HUB    ║
# ║  创建者: 诸葛鑫（UID9622）                                   ║
# ║  协议: MulanPSL v2（工程层·允许商业使用）                     ║
# ║  用法: source ~/longhun-system/bin/lh_ai_hub_env.sh          ║
# ╚══════════════════════════════════════════════════════════════╝

# ── 焊死路径 ──
export AI_OUTPUT_HUB="$HOME/ai-outputs"
export AI_INDEX_DIR="$AI_OUTPUT_HUB/_index"
export AI_SHARED_DIR="$AI_OUTPUT_HUB/_shared"

# ── 各工具输出子目录 ──
export CODEBUDDY_OUTPUT_DIR="$AI_OUTPUT_HUB/codebuddy"
export CLAUDE_OUTPUT_DIR="$AI_OUTPUT_HUB/claude"
export KIMI_OUTPUT_DIR="$AI_OUTPUT_HUB/kimi"
export GROK_OUTPUT_DIR="$AI_OUTPUT_HUB/grok"
export COPILOT_OUTPUT_DIR="$AI_OUTPUT_HUB/copilot"

# ── 确保目录存在 ──
for d in "$AI_OUTPUT_HUB" "$AI_INDEX_DIR" "$AI_SHARED_DIR" \
         "$CODEBUDDY_OUTPUT_DIR" "$CLAUDE_OUTPUT_DIR" \
         "$KIMI_OUTPUT_DIR" "$GROK_OUTPUT_DIR" "$COPILOT_OUTPUT_DIR"; do
    [[ -d "$d" ]] || mkdir -p "$d"
done

# ── 快速命令 ──

# ai-hub: 查看归集状态
alias ai-hub='python3 ~/longhun-system/bin/lh_ai_indexer.py report'

# ai-scan: 扫描指定工具目录归集到hub
# 用法: ai-scan ~/some/output --tool kimi
ai-scan() {
    python3 ~/longhun-system/bin/lh_ai_indexer.py scan "$1" --tool "${2:-shared}"
}

# ai-find: 搜索归集内容
# 用法: ai-find "关键词" [--tool kimi]
ai-find() {
    python3 ~/longhun-system/bin/lh_ai_indexer.py search "$@"
}

# ai-stats: 查看统计
alias ai-stats='python3 ~/longhun-system/bin/lh_ai_indexer.py stats'

# ai-rebuild: 强制重建索引
alias ai-rebuild='python3 ~/longhun-system/bin/lh_ai_indexer.py force'

# ai-to: 将当前产出快速归集到指定工具目录
# 用法: ai-to kimi ./my_output.md
ai-to() {
    local tool="$1"
    local src="$2"
    local dest="$AI_OUTPUT_HUB/${tool:-shared}"
    if [[ -z "$src" ]]; then
        echo "用法: ai-to <工具名> <文件或目录>"
        echo "工具: codebuddy | claude | kimi | grok | copilot | shared"
        return 1
    fi
    mkdir -p "$dest"
    if [[ -f "$src" ]]; then
        cp "$src" "$dest/" && echo "✅ $src → $dest/"
    elif [[ -d "$src" ]]; then
        cp -r "$src"/* "$dest/" 2>/dev/null && echo "✅ $src/* → $dest/"
    else
        echo "❌ 找不到: $src"
        return 1
    fi
    ai-rebuild
}

# ai-open: 打开归集目录
alias ai-open='open "$AI_OUTPUT_HUB"'

# ── 自动钩子：每当产出到 longhun-system/output 时自动归集 ──
# （在 lh 命令中调用，此处声明环境变量）

# ── 欢迎信息（v1.1·仅交互式终端显示·计数走缓存·不刷屏不卡终端）──
# 修复: ①非交互shell(zsh -c/脚本/管道)不再刷横幅 ②12MB索引只在变化后重算一次
# 彻底静音: export AI_HUB_SILENT=1
if [[ "$AI_HUB_SILENT" != "1" && "$-" == *i* ]]; then
    count=0
    if [[ -f "$AI_INDEX_DIR/master_index.json" ]]; then
        count_cache="$AI_INDEX_DIR/.count_cache"
        # 索引没变 → 直接读缓存；变了才重新解析（一次）
        if [[ -f "$count_cache" && "$AI_INDEX_DIR/master_index.json" -ot "$count_cache" ]]; then
            count=$(cat "$count_cache" 2>/dev/null || echo 0)
        else
            count=$(python3 -c "import json;print(json.load(open('$AI_INDEX_DIR/master_index.json')).get('entry_count',0))" 2>/dev/null || echo 0)
            echo "$count" > "$count_cache" 2>/dev/null
        fi
    fi
    echo "🐉 AI归集Hub就绪 | 索引: ${count:-0} 文件 | 工具: $(ls -d $AI_OUTPUT_HUB/*/ 2>/dev/null | wc -l | tr -d ' ') 个"
fi
