#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 安装定时任务 · macOS launchd 定时器
# DNA: #龍芯⚡️2026-03-18-定时任务-v1.0
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 作者: UID9622 诸葛鑫（龍芯北辰）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 定时计划：
#   每天 08:00 → 一键同步（Notion+Git）
#   每天 22:00 → 新文件整理 + 清理垃圾
#   每周一 09:00 → 全套运行
#   开机时 → 启动所有服务
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PLIST_DIR="$HOME/Library/LaunchAgents"
BIN="$HOME/longhun-system/bin"
mkdir -p "$PLIST_DIR"

通知() {
    osascript -e "display notification \"$2\" with title \"⏰ 定时任务\" subtitle \"$1\"" 2>/dev/null
}

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  ⏰ 安装定时任务"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ── 1. 每天08:00 同步 ─────────────────────
cat > "$PLIST_DIR/com.longhun.sync.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.sync</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$BIN/一键同步.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>8</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$HOME/longhun-system/logs/定时同步输出.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/longhun-system/logs/定时同步错误.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
PLIST
echo "  ✅ 每天08:00 → 一键同步"

# ── 2. 每天22:00 整理+清理 ───────────────
cat > "$PLIST_DIR/com.longhun.cleanup.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.cleanup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>-c</string>
        <string>bash $BIN/新文件整理.sh &amp;&amp; bash $BIN/清理垃圾.sh</string>
    </array>
    <key>StartCalendarInterval</key>
    <dict>
        <key>Hour</key>
        <integer>22</integer>
        <key>Minute</key>
        <integer>0</integer>
    </dict>
    <key>StandardOutPath</key>
    <string>$HOME/longhun-system/logs/定时整理输出.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/longhun-system/logs/定时整理错误.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
PLIST
echo "  ✅ 每天22:00 → 新文件整理 + 清理垃圾"

# ── 3. 开机自动启动服务 ───────────────────
cat > "$PLIST_DIR/com.longhun.startup.plist" << PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.longhun.startup</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$BIN/启动所有服务.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>$HOME/longhun-system/logs/开机启动输出.log</string>
    <key>StandardErrorPath</key>
    <string>$HOME/longhun-system/logs/开机启动错误.log</string>
</dict>
</plist>
PLIST
echo "  ✅ 开机自动 → 启动所有服务"

# ── 4. 加载所有定时任务 ───────────────────
echo ""
echo "  【加载定时任务到系统】"
for plist in com.longhun.sync com.longhun.cleanup com.longhun.startup; do
    launchctl unload "$PLIST_DIR/${plist}.plist" 2>/dev/null
    launchctl load "$PLIST_DIR/${plist}.plist" 2>/dev/null
    if [ $? -eq 0 ]; then
        echo "  ✅ $plist 已激活"
    else
        echo "  🟡 $plist 加载警告（可能需要重启生效）"
    fi
done

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  定时任务安装完成"
echo ""
echo "  时间表："
echo "  · 08:00 每天 → 自动同步Notion+Git"
echo "  · 22:00 每天 → 整理文件+清垃圾"
echo "  · 开机时      → 启动龍魂服务"
echo ""
echo "  查看状态: launchctl list | grep longhun"
echo "  卸载全部: bash $BIN/卸载定时任务.sh"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
通知 "定时任务已安装" "08:00同步 22:00整理 开机启动服务"
