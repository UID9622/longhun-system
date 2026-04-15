#!/bin/bash
# ☰☰ 龍🇨🇳魂 ☷ · 唯一入口 · UID9622
# DNA: #龍芯⚡️2026-04-08-DRAGON-SOUL-ENTRANCE-v1.0

clear
echo ""
echo "    ☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰☰"
echo "    ☰                                    ☰"
echo "    ☰        🐉 龍 🇨🇳 魂 🐉              ☰"
echo "    ☰                                    ☰"
echo "    ☰☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷☷"
echo ""
echo "    UID9622 · 诸葛鑫 · 龍芯北辰"
echo "    理论指导: 曾仕强老师（永恒显示）"
echo ""

BASE="$HOME/longhun-system"
COMFY_DIR="$HOME/ComfyUI"

check_service() {
    port=$1
    name=$2
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo "    ✅ $name :$port 运行中"
        return 0
    else
        echo "    ❌ $name :$port 未启动"
        return 1
    fi
}

echo "═══════════════════════════════════════"
echo "    世界状态检测"
echo "═══════════════════════════════════════"
check_service 8000 "主引擎"
check_service 8001 "补丁层"
check_service 8002 "知识库API"
check_service 8003 "熔断规则"
check_service 8081 "字体管理"
check_service 8188 "ComfyUI"

echo ""
echo "═══════════════════════════════════════"
echo "    选择你的世界"
echo "═══════════════════════════════════════"
echo ""
echo "    [1] 🌐 打开主控台 (浏览器)"
echo "    [2] 🧠 启动对话 (8000端口)"
echo "    [3] 📊 查看统计看板"
echo "    [4] ☯ 洛书九宫地图"
echo "    [5] 🔍 搜索本地知识库"
echo "    [6] 📚 读取系统记忆"
echo "    [7] 🎬 视频AI (ComfyUI)
    [A] 🀄 字体管理 (15字元库+2字体)
    [C] 🇨🇳 CNSH语言终端
    [T] 🧰 工具箱 (75个脚本)
    [K] 🤖 Kimi终端版 (DeepSeek主·Kimi挂)"
echo "    [8] 🚀 启动全部服务"
echo "    [S] 🛑 停止全部服务"
echo "    [0] 退出"
echo ""
echo "═══════════════════════════════════════"
echo ""

read -p "    选择 [0-9/A/S]: " choice

case $choice in
    1)
        echo "    正在打开主控台..."
        open "http://localhost:8001/static/portal.html"
        ;;
    2)
        echo "    启动对话模式..."
        cd "$BASE" && python3 app.py
        ;;
    3)
        echo "    打开统计看板..."
        open "http://localhost:8001/static/stats_dashboard.html"
        ;;
    4)
        echo "    打开洛书九宫..."
        open "http://localhost:8001/static/luoshu_map.html"
        ;;
    5)
        echo "    知识库搜索: http://localhost:8002/search?q=关键词"
        ;;
    6)
        echo "    系统记忆: $BASE/memory.jsonl"
        echo "    共 $(wc -l < "$BASE/memory.jsonl") 条记录"
        ;;
    A|a)
        echo "    🀄 字体管理中枢..."
        open "http://localhost:8081/"
        ;;
    C|c)
        echo "    🇨🇳 CNSH语言终端..."
        echo "    示例文件:"
        ls -1 ~/longhun-system/cnsh语言/*.cnsh 2>/dev/null | while read f; do
            echo "      - $(basename $f)"
        done
        echo ""
        read -p "    输入要编译的.cnsh文件名: " cnsh_file
        python3 ~/longhun-system/bin/cnsh_cli.py ~/longhun-system/cnsh语言/$cnsh_file
        ;;
    T|t)
        echo "    🧰 启动工具箱..."
        python3 ~/longhun-system/bin/toolbox.py
        ;;
    K|k)
        echo "    🤖 Kimi终端版..."
        echo "    DeepSeek主引擎 · Kimi挂载执行"
        echo "    确认: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
        echo ""
        echo "    [1] Bash快速模式"
        echo "    [2] Python交互模式"
        read -p "    选择 [1/2]: " kimi_mode
        if [ "$kimi_mode" = "1" ]; then
            bash ~/longhun-system/longhun_kimi.sh
        else
            python3 ~/longhun-system/longhun_kimi.py
        fi
        ;;
    7)
        echo "    🎬 龍魂视频AI"
        echo "    1. 启动ComfyUI..."
        cd "$COMFY_DIR" && python3 main.py &
        sleep 3
        echo "    2. 打开浏览器..."
        open "http://127.0.0.1:8188"
        echo ""
        echo "    工作流位置: $COMFY_DIR/workflows/"
        echo "    模型下载: $COMFY_DIR/models/下载模型指引.md"
        ;;
    8)
        echo "    启动全部服务..."
        cd "$BASE" && nohup python3 app_patch.py > /tmp/app_patch.log 2>&1 &
        cd "$BASE" && nohup python3 bin/knowledge_api.py > /tmp/knowledge_api.log 2>&1 &
        cd "$BASE" && nohup python3 bin/fuse_api.py > /tmp/fuse_api.log 2>&1 &
        cd "$BASE" && nohup python3 bin/font_manager.py > /tmp/font_manager.log 2>&1 &
        echo "    ✅ 全部服务已启动"
        sleep 2
        $0
        ;;
    S|s)
        echo "    停止全部服务..."
        pkill -f "python3 app_patch.py" 2>/dev/null
        pkill -f "python3 bin/knowledge_api.py" 2>/dev/null
        pkill -f "python3 bin/fuse_api.py" 2>/dev/null
        pkill -f "python3 main.py" 2>/dev/null
        pkill -f "python3 bin/font_manager.py" 2>/dev/null
        echo "    ✅ 全部服务已停止"
        ;;
    0)
        echo "    龍魂永在 · 后会有期"
        exit 0
        ;;
    *)
        echo "    无效选择"
        ;;
esac

echo ""
read -p "    按回车返回主菜单..."
$0
