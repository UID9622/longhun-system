#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·子仓库同步脚本 v1.0
# DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☰乾-SUBREPO-SYNC-v1.0-c1d2e3f4
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

set -e
BASE="/Users/zuimeidedeyihan/longhun-system/_work/repos"
LOG="/Users/zuimeidedeyihan/longhun-system/logs/subrepo_sync_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG") 2>&1

echo "=== 龍魂子仓库同步 ==="
echo "时间: $(date)"
echo ""

# 1. 删除 typo 仓库
echo "1/4 清理 typo..."
rm -rf "$BASE/onghun-system" 2>/dev/null && echo "✅ onghun-system 已删除" || echo "⚠️ onghun-system 不存在或已删除"

# 2. 主仓库备份同步（用cp替代fetch避免大流量）
echo ""
echo "2/4 同步主仓库备份..."
cd "$BASE/longhun-system"
# 直接从主仓库复制瘦身后的 .git
rm -rf .git
cp -r /Users/zuimeidedeyihan/longhun-system/.git .git
git reset --hard HEAD 2>&1 | tail -1
echo "✅ longhun-system 备份大小: $(du -sh .git | cut -f1)"

# 3. 批量 pull 其他仓库
echo ""
echo "3/4 拉取其他仓库..."
repos="ai-truth-protocol cnsh-runtime CNSH ecny-global-system longhun-anti-colonial longhun-calendar longhun-kimi-skills longhun-memory-bootstrap LonghunFont uid9622-open-blueprint wuwu-renderer longhun-identity-system"
for repo in $repos; do
    echo -n "  $repo ... "
    if [ -d "$BASE/$repo" ]; then
        (cd "$BASE/$repo" && git pull --ff-only 2>&1 | tail -1) || echo "⚠️ pull失败"
    else
        echo "❌ 目录不存在"
    fi
done

# 4. 修复 identity-system 分支
echo ""
echo "4/4 修复 identity-system 分支..."
cd "$BASE/longhun-identity-system"
git checkout main 2>/dev/null && git pull 2>&1 | tail -1 || echo "⚠️ 分支切换失败"

echo ""
echo "=== 同步完成 ==="
echo "时间: $(date)"
echo ""
echo "=== 子仓库一览 ==="
for d in "$BASE"/*/; do
    name=$(basename "$d")
    size=$(du -sh "$d/.git" 2>/dev/null | cut -f1)
    branch=$(cd "$d" && git branch --show-current 2>/dev/null || echo "?")
    echo "  $name: $size ($branch)"
done
