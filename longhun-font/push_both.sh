#!/bin/bash
# 龍魂·双仓推送脚本
# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-PUSH-BOTH-v1.0
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 用法：./push_both.sh

set -e

echo "🚀 推送到 GitHub（origin 镜像）..."
git push origin main

echo "🚀 推送到 Gitee（gitee 镜像）..."
git push gitee main

echo "✅ 双仓同步完成"
