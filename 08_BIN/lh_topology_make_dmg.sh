#!/bin/bash
# DNA: #龍芯⚡️2026-08-30-丙午·丙申·丙子·未时-TOPOLOGY-DMG-v1.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 将龍魂拓扑可视化应用封装为 macOS dmg（零第三方依赖·osacompile+hdiutil）
# 用法: bash bin/lh_topology_make_dmg.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$ROOT/web/topology-viewer"
WORK="$(mktemp -d)"
APP="$WORK/龍魂拓扑.app"
DMG_OUT="$ROOT/dist/龍魂拓扑.dmg"
VOLNAME="龍魂拓扑"

trap 'rm -rf "$WORK" 2>/dev/null || true' EXIT

echo "🟡 0/4 准备资源…"
[ -f "$SRC/index.html" ] || { echo "🔴 缺少 $SRC/index.html · 先跑 lh_topology_viewer_build.py"; exit 1; }
mkdir -p "$ROOT/dist"

echo "🟡 1/4 写入应用壳…"
mkdir -p "$WORK/build"
cat > "$WORK/build/launcher.applescript" <<'EOF'
on run
    set appPath to POSIX path of (path to me)
    set htmlPath to appPath & "Contents/Resources/index.html"
    do shell script "open '" & htmlPath & "'"
end run
EOF
osacompile -o "$WORK/build/longhun-topology.app" "$WORK/build/launcher.applescript"
mv "$WORK/build/longhun-topology.app" "$APP"

echo "🟡 2/4 注入资源…"
mkdir -p "$APP/Contents/Resources"
cp "$SRC/index.html" "$SRC/sw.js" "$SRC/manifest.webmanifest" "$SRC/icon.svg" "$SRC"/icon-*.png "$APP/Contents/Resources/"
cat > "$APP/Contents/Info.plist" <<'PLIST'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>龍魂拓扑</string>
  <key>CFBundleDisplayName</key><string>龍魂拓扑</string>
  <key>CFBundleIdentifier</key><string>cn.uid9622.longhun.topology</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundleExecutable</key><string>applet</string>
  <key>CFBundlePackageType</key><string>APPL</string>
</dict>
</plist>
PLIST
chmod +x "$APP/Contents/MacOS/applet"

echo "🟡 3/4 写入三端说明…"
cat > "$WORK/三端使用说明.txt" <<'EOF'
==========================================
 龍魂拓扑 · 神经网络全览 · v1.1
 归属名：诸葛鑫 | UID9622 · 龍芯北辰
 License: MulanPSL v2 (工程实现层)
==========================================

【macOS】
  双击「龍魂拓扑.app」→ 自动在浏览器打开拓扑总览。
  可拖入「应用程序」文件夹。

【iOS（iPhone / iPad）】
  1. 将 web/topology-viewer 目录部署到任意 https 站点（如 uid9622.cn）
     或局域网内 http 服务
  2. Safari 打开 index.html
  3. 点「分享」按钮 →「添加到主屏幕」→ 桌面生成龍魂拓扑图标
  4. 首次打开联网后，Service Worker 完成离线缓存，之后离线可用

【鸿蒙 HarmonyOS（手机 / 平板 / 车机）】
  1. 同上，浏览器打开 index.html
  2. 浏览器菜单 →「添加到桌面」
  3. 首次联网打开后离线可用

【数据与隐私】
  全部数据内嵌单页。不联网、不上传、不收集、不追踪任何数据。
  数据源：.codebuddy/longhun_neural_net.json（v4.0 拓扑）
  版本：v1.1（审计修复：真离线缓存 · PNG 图标 · 错误边界）

【工程流程（完整链）】
  1 构建   python3 bin/lh_topology_viewer_build.py
  2 校验   python3 bin/lh_topology_verify.py
  3 打包   bash bin/lh_topology_make_dmg.sh
  4 发布   bash bin/lh_topology_publish.sh [--deploy 目标]

DNA: #龍芯⚡️2026-08-30-TOPOLOGY-VIEWER-v1.1-BUILD-UID9622
EOF
cp "$WORK/三端使用说明.txt" "$APP/Contents/Resources/"

echo "🟡 4/4 打包 dmg…"
mkdir -p "$WORK/payload"
mv "$APP" "$WORK/payload/"
mv "$WORK/三端使用说明.txt" "$WORK/payload/"
hdiutil create -volname "$VOLNAME" -srcfolder "$WORK/payload" -ov -format UDZO "$DMG_OUT" >/dev/null
rm -rf "$WORK"
echo "🟢 完成 → $DMG_OUT"
ls -lh "$DMG_OUT" | awk '{print "   大小: "$5}'
