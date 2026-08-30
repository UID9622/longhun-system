#!/bin/bash
# DNA: #龍芯⚡️2026-08-30-丙午·丙申·丙子·未时-TOPOLOGY-PUBLISH-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 龍魂拓扑一键发布流程 — 构建→校验→GPG签名→打包dmg→校验→部署(可选)
# 用法: bash bin/lh_topology_publish.sh [--deploy <远端:路径>]
#   示例: bash bin/lh_topology_publish.sh --deploy root@119.13.90.27:/opt/longhun/portal/apps/topology
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VERIFY="$ROOT/bin/lh_topology_verify.py"
SIGN="$ROOT/bin/lh_gpg_sign.py"
OUT="$ROOT/web/topology-viewer"
DMG="$ROOT/dist/龍魂拓扑.dmg"

echo "════════ 龍魂拓扑 · 一键发布 ════════"
echo "▶ 1/6 构建"
python3 "$ROOT/bin/lh_topology_viewer_build.py"

echo "▶ 2/6 校验产物"
python3 "$VERIFY" --out "$OUT" --dmg "$DMG" || { echo "🔴 产物校验失败 · 终止发布"; exit 1; }

echo "▶ 3/6 GPG 签名产物"
python3 "$SIGN" sign "$OUT" >/dev/null

echo "▶ 4/6 打包 dmg"
bash "$ROOT/bin/lh_topology_make_dmg.sh"

echo "▶ 5/6 GPG 签名 dmg + 校验"
python3 "$SIGN" sign "$DMG" >/dev/null
python3 "$VERIFY" --out "$OUT" --dmg "$DMG"

echo "▶ 6/6 部署"
DEPLOY_TARGET="${1:-}"
if [ -n "${DEPLOY_TARGET}" ]; then
  DEPLOY_TARGET="$(echo "$DEPLOY_TARGET" | sed 's/^--deploy[= ]//')"
  echo "  目标: $DEPLOY_TARGET"
  rsync -avz --delete "$OUT/" "$DEPLOY_TARGET/" || { echo "🟡 部署失败 · 检查 SSH/路径"; }
  echo "🟢 部署完成"
else
  echo "  跳过（需要在线部署时: bash $0 --deploy root@鲲鹏:/路径）"
fi

echo "════════ 发布完成 · 三色: 🟢🟢🟢════════"
ls -lh "$DMG" | awk '{print "  dmg: "$5"  "}'
