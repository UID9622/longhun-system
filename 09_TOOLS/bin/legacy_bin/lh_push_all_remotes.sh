#!/bin/bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·三远程强制推送脚本
# DNA: #龍芯⚡️丙午·乙未·丙申·酉时·䷀乾-PUSH-ALL-REMOTES-SLIM-v1.0-a1b2c3d4

set -e

REPO_DIR="/Users/zuimeidedeyihan/longhun-system"
LOG="/Users/zuimeidedeyihan/longhun-system/logs/push_$(date +%Y%m%d_%H%M%S).log"

exec > >(tee -a "$LOG") 2>&1

echo "=== 龍魂三远程瘦身推送 ==="
echo "开始时间: $(date)"
echo "当前目录: $(pwd)"
echo ""

cd "$REPO_DIR"

echo "=== 推送 GitHub ==="
git push gh-ssh --force orphan_main
echo "✅ GitHub 完成"
echo ""

echo "=== 推送 GitCode ==="
git push gitcode --force orphan_main
echo "✅ GitCode 完成"
echo ""

echo "=== 推送 Gitee ==="
git push gitee --force orphan_main
echo "✅ Gitee 完成"
echo ""

echo "=== 推送 Tags ==="
git push gh-ssh --force --tags
git push gitcode --force --tags  
git push gitee --force --tags
echo "✅ Tags 完成"
echo ""

echo "=== 清理备份 ==="
rm -f .git.fat
echo "✅ 旧 .git 已删除"
echo ""

echo "=== 推送完成 ==="
echo "结束时间: $(date)"
echo "大小: $(du -sh .git | cut -f1)"
