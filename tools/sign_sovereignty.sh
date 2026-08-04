#!/bin/bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# ============================================================
# 龍魂主权文件批量 GPG 签章脚本
# ============================================================
# 指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创作者: UID9622（诸葛鑫·Lucky）
# 日期: 2026-07-12
# 用法: bash tools/sign_sovereignty.sh
# ============================================================

set +e  # 不因单文件失败而中断全部签章
cd "$(dirname "$0")/.."

FILES=(
  "sovereignty/CREATOR_LEGACY_WILL_SOVEREIGN_HANDOVER_v1.0.md"
  "sovereignty/VALUES_BASE_CHINESE_ROOT_v1.0.md"
  "sovereignty/KEY_VAULT_HANDOVER_v1.0.md"
  "sovereignty/CREATOR_VISION_DOWNWARD_LEGACY_v1.0.md"
  "sovereignty/EMOTION_ABSORBER_ONE_PERSONA_ONE_DNA_v1.0.md"
)

echo "🔐 龍魂主权文件 GPG 签章"
echo "========================================"
echo "指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
echo "文件数: ${#FILES[@]}"
echo "========================================"

SIGNED=0
SKIPPED=0

for f in "${FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "  ⚠️  跳过（不存在）: $f"
    ((SKIPPED++))
    continue
  fi
  echo ""
  echo "▶ 签章: $f"
  gpg --armor --detach-sign --default-key A2D0092CEE2E5BA87035600924C3704A8CC26D5F "$f"
  echo "  ✅ ${f}.asc"
  
  echo "▶ 验证:"
  gpg --verify "${f}.asc" "$f" 2>&1 | grep -E "Good signature|指纹|Primary key" || true
  ((SIGNED++))
done

echo ""
echo "========================================"
echo "签章完成: ${SIGNED} 份 | 跳过: ${SKIPPED} 份"
echo "DNA: #龍芯⚡️丙午·丙申·丙辰·午时·离-SOVEREIGNTY-SEAL-v1.0"
echo "GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
echo ""
echo "验证所有签名:"
echo "  for f in sovereignty/*.md; do gpg --verify \"\${f}.asc\" \"\$f\"; done"
