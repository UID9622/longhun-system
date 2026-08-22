#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
> #龍芯⚡️丙午·丙申·乙卯·丙戌·䷷旅-GITEE-MIRROR-SYNC-v1.0

#!/bin/bash
# Gitee 仓库批量同步脚本
# 将 uid9622 组织的仓库同步到 L7_数据层/gitee-mirror/

set -e

MIRROR_DIR="/Users/zuimeidedeyihan/longhun-system/L7_数据层/gitee-mirror"
ORG="uid9622"

REPOS=(
  "cnsh"
  "cnsh-language"
  "longhun-identity-system"
  "dragon-soul-pack"
  "longhun-terminal"
  "Edu-Coding"
  "UID9622-CNSH"
  "my-chinese-docs"
  "test-project"
  "harmonyos-behavioral-audit"
)

mkdir -p "$MIRROR_DIR"

echo "🐉 开始同步 Gitee 仓库到本地镜像..."

for repo in "${REPOS[@]}"; do
  REPO_DIR="$MIRROR_DIR/$repo"
  if [ -d "$REPO_DIR/.git" ]; then
    echo "🔄 更新 $repo ..."
    cd "$REPO_DIR"
    git pull origin master 2>/dev/null || git pull origin main 2>/dev/null || true
  else
    echo "⬇️ 克隆 $repo ..."
    cd "$MIRROR_DIR"
    git clone "https://gitee.com/$ORG/$repo.git" "$repo" 2>/dev/null || echo "⚠️ $repo 克隆失败，保留现有文件"
  fi
done

echo "✅ Gitee 镜像同步完成"
