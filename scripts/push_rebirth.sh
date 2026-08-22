#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷯井-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ═══════════════════════════════════════════════════════════
# 龍魂 · 仓库推送脚本 v1.0
# 仓库: 6203文件 · 87MB · 全新重建
# Commit: ae86cd2 · DNA #龍芯⚡️丙午·辛未·乙酉·丁亥·䷵归妹-REPO-REBIRTH-v1.0
# ═══════════════════════════════════════════════════════════

set -e
cd /Users/zuimeidedeyihan/longhun-system

echo "🚀 龍魂仓库重建推送开始"
echo "   Pack: 87MB | Files: 6203 | Remotes: 4"
echo ""

# 1. GitHub SSH (主力)
echo "[1/4] 推送 GitHub SSH..."
git push origin main --force && echo "  ✅ GitHub SSH OK" || echo "  ❌ GitHub SSH failed"

# 2. GitHub HTTPS (备用)
echo "[2/4] 推送 GitHub HTTPS..."
git push https-origin main --force && echo "  ✅ GitHub HTTPS OK" || echo "  ❌ GitHub HTTPS failed"

# 3. GitCode (国内)
echo "[3/4] 推送 GitCode..."
git push gitcode main --force && echo "  ✅ GitCode OK" || echo "  ❌ GitCode failed"

# 4. Gitee (国内)
echo "[4/4] 推送 Gitee..."
git push gitee main --force && echo "  ✅ Gitee OK" || echo "  ❌ Gitee failed"

echo ""
echo "🏁 推送完成. git log:"
git log --oneline -1
