#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# 龍魂·六层来源链 / LongHun Six-Layer Source Chain
# DNA追溯码:#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-PUBLISH-WUWU-v1.0
#
# 发布 @uid9622/wuwu-renderer 到 npm
# 用法:
#   export NPM_TOKEN=your_npm_access_token
#   ./scripts/publish_wuwu.sh [dry-run]

set -euo pipefail

DNA="#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-LONGHUN-FONT-PUBLISH-WUWU-v1.0"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_DIR="$(cd "${SCRIPT_DIR}/../packages/wuwu-renderer" && pwd)"

echo "============================================================"
echo "📦 发布 @uid9622/wuwu-renderer 到 npm"
echo "DNA: ${DNA}"
echo "包目录: ${PKG_DIR}"
echo "============================================================"
echo

cd "${PKG_DIR}"

# 优先使用环境变量中的 NPM_TOKEN
if [ -n "${NPM_TOKEN:-}" ]; then
    echo "🔑 使用环境变量 NPM_TOKEN 设置 registry token"
    npm config set //registry.npmjs.org/:_authToken "${NPM_TOKEN}"
fi

# 检查登录状态
if ! npm whoami >/dev/null 2>&1; then
    echo "❌ 未登录 npm。请提供 NPM_TOKEN 环境变量，或先执行 npm login。"
    echo "   示例: export NPM_TOKEN=npm_xxxxxxxx && ./scripts/publish_wuwu.sh"
    exit 1
fi

echo "✅ npm 用户: $(npm whoami)"

if [ "${1:-}" == "dry-run" ]; then
    echo "🧪 执行 npm publish --dry-run"
    npm publish --access public --dry-run
else
    echo "🚀 执行 npm publish --access public"
    npm publish --access public
fi

echo
echo "============================================================"
echo "✅ @uid9622/wuwu-renderer 发布流程完成"
echo "DNA: ${DNA}"
echo "============================================================"
