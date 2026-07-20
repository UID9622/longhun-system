#!/bin/bash
# DNA: #龍芯⚡️2026-07-21-SUMMARY-CRAWLER-SPLIT-V1.0-P0-SIGN
# GPG签章脚本 · 在终端手动执行一次即可
# 用法: bash bin/lh_sign_crawler.sh

set -e

cd "$(dirname "$0")/.."

FILES=(
  "01_protocols/LH-SUMMARY-CRAWLER-TRAFFIC-SPLIT-v1.0.md"
  "bin/lh_summary_crawler.py"
  "bin/lh_summary_crawler_test.py"
)

echo "龍魂摘要爬虫协议 v1.0 · GPG签章"
echo "指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
echo ""

for f in "${FILES[@]}"; do
  echo "签章: $f"
  gpg --detach-sign --armor --local-user A2D0092CEE2E5BA87035600924C3704A8CC26D5F "$f"
  echo "  → ${f}.asc"
done

echo ""
echo "🟢 3个文件签章完成"

# 对commit也签名
echo ""
echo "重新签名最近一次 commit..."
git commit --amend -S --no-edit 2>&1 || echo "commit签名需gpg-agent已缓存passphrase"

# SHA-256 清单
echo ""
echo "生成 SHA-256 完整性清单..."
sha256sum "${FILES[@]}" > .codebuddy/crawler_v1.0.MANIFEST.sha256
cat .codebuddy/crawler_v1.0.MANIFEST.sha256

echo ""
echo "=== 全部完成 ==="
echo "DNA: #龍芯⚡️2026-07-21-SUMMARY-CRAWLER-SPLIT-V1.0-P0"
echo "GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
