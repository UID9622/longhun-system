#!/bin/bash
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 龍魂·视频自动化生产线 v1.0 — 部署脚本
# DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VIDEO-DEPLOY-v1.0
# 创建者: 诸葛鑫（UID9622）· 协议: CC BY-NC-SA 4.0
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

set -euo pipefail

HONG_SE='\033[0;31m'
LV_SE='\033[0;32m'
JIN_SE='\033[0;33m'
WU_SE='\033[0m'

JIAO_BEN_MU_LU="$(cd "$(dirname "$0")" && pwd)"
XI_TONG_MU_LU="$(dirname "$JIAO_BEN_MU_LU")"

echo "============================================"
echo "  龍魂·视频自动化生产线 v1.0 — 部署"
echo "  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-VIDEO-DEPLOY-v1.0"
echo "  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
echo "============================================"
echo ""

# ━━━━━ 第一步：环境检查 ━━━━━
echo -e "${JIN_SE}[1/6] 环境检查...${WU_SE}"
PYTHON3=$(which python3 || echo "")
if [ -z "$PYTHON3" ]; then
    echo -e "${HONG_SE}  ✗ python3 未安装${WU_SE}"
    exit 1
fi
PYTHON_BAN_BEN=$($PYTHON3 --version 2>&1 | awk '{print $2}')
echo -e "${LV_SE}  ✓ python3 ${PYTHON_BAN_BEN}${WU_SE}"

# 检查必要文件
WEN_JIAN_LIE=(
    "engines/lh_visual_engine.py"
    "engines/lh_voice_engine.py"
    "engines/lh_avatar_engine.py"
    "bin/lh_video_pipeline.py"
    "config/video_presets.yaml"
    "01_protocols/LH-VIDEO-PRODUCTION-v1.0.md"
)

QUE_SHI=0
for wen_jian in "${WEN_JIAN_LIE[@]}"; do
    if [ ! -f "$XI_TONG_MU_LU/$wen_jian" ]; then
        echo -e "${HONG_SE}  ✗ 缺少: $wen_jian${WU_SE}"
        QUE_SHI=1
    fi
done

if [ $QUE_SHI -eq 1 ]; then
    echo -e "${HONG_SE}  必要文件缺失，请先确认所有文件已创建${WU_SE}"
    exit 1
fi
echo -e "${LV_SE}  ✓ 所有必要文件就绪${WU_SE}"

# ━━━━━ 第二步：创建目录 ━━━━━
echo ""
echo -e "${JIN_SE}[2/6] 创建输出目录...${WU_SE}"
mkdir -p "$XI_TONG_MU_LU/output/videos"
mkdir -p "$XI_TONG_MU_LU/models/voice"
mkdir -p "$XI_TONG_MU_LU/models/avatar"
mkdir -p "$XI_TONG_MU_LU/logs"
echo -e "${LV_SE}  ✓ 输出目录已创建${WU_SE}"

# ━━━━━ 第三步：安装Python依赖 ━━━━━
echo ""
echo -e "${JIN_SE}[3/6] 安装Python依赖...${WU_SE}"
# 基础依赖（不包含实际ML框架，待模型就绪再加）
# 优先使用当前 python3 对应的 pip，避免系统 pip3 与 venv 不一致
python3 -m pip install pyyaml pypinyin 2>/dev/null && echo -e "${LV_SE}  ✓ pyyaml pypinyin${WU_SE}" || echo -e "${JIN_SE}  ⚠ pyyaml/pypinyin已安装或跳过${WU_SE}"

# ━━━━━ 第四步：自检 ━━━━━
echo ""
echo -e "${JIN_SE}[4/6] 运行自检...${WU_SE}"

ZI_JIAN_TONG_GUO=0
ZI_JIAN_SHI_BAI=0

echo "  --- 视觉引擎 ---"
if python3 "$XI_TONG_MU_LU/engines/lh_visual_engine.py" selftest 2>&1 | tail -3; then
    ZI_JIAN_TONG_GUO=$((ZI_JIAN_TONG_GUO + 1))
else
    ZI_JIAN_SHI_BAI=$((ZI_JIAN_SHI_BAI + 1))
fi

echo "  --- 声音引擎 ---"
if python3 "$XI_TONG_MU_LU/engines/lh_voice_engine.py" selftest 2>&1 | tail -3; then
    ZI_JIAN_TONG_GUO=$((ZI_JIAN_TONG_GUO + 1))
else
    ZI_JIAN_SHI_BAI=$((ZI_JIAN_SHI_BAI + 1))
fi

echo "  --- 数字人引擎 ---"
if python3 "$XI_TONG_MU_LU/engines/lh_avatar_engine.py" selftest 2>&1 | tail -3; then
    ZI_JIAN_TONG_GUO=$((ZI_JIAN_TONG_GUO + 1))
else
    ZI_JIAN_SHI_BAI=$((ZI_JIAN_SHI_BAI + 1))
fi

echo "  --- 视频管线 ---"
if python3 "$XI_TONG_MU_LU/bin/lh_video_pipeline.py" selftest 2>&1 | tail -3; then
    ZI_JIAN_TONG_GUO=$((ZI_JIAN_TONG_GUO + 1))
else
    ZI_JIAN_SHI_BAI=$((ZI_JIAN_SHI_BAI + 1))
fi

echo ""
echo -e "  自检结果: ${LV_SE}${ZI_JIAN_TONG_GUO}通过${WU_SE} / ${HONG_SE}${ZI_JIAN_SHI_BAI}失败${WU_SE}"

if [ $ZI_JIAN_SHI_BAI -gt 0 ]; then
    echo -e "${HONG_SE}  自检未全绿，请修复后再部署${WU_SE}"
    exit 1
fi

# ━━━━━ 第五步：安装 Git Hook ━━━━━
echo ""
echo -e "${JIN_SE}[5/6] 安装 Git Hook（DNA水印检查）...${WU_SE}"

GIT_HOOK_LU="$XI_TONG_MU_LU/.git/hooks/pre-commit"
if [ -d "$XI_TONG_MU_LU/.git/hooks" ]; then
    cat > "$GIT_HOOK_LU" << 'HOOK_EOF'
#!/bin/bash
# 龍魂·视频管线提交检查
# 检查视频产出文件是否有DNA水印

while IFS= read -r -d '' f; do
    if [[ "$f" == output/videos/* ]]; then
        echo "⚠️ 检测到视频产出文件: $f"
        echo "  请确认: DNA水印 ✅  GPG签名 ✅  老大已审 ✅"
    fi
done < <(git diff --cached --name-only --diff-filter=ACM -z)
exit 0
HOOK_EOF
    chmod +x "$GIT_HOOK_LU"
    echo -e "${LV_SE}  ✓ Git Hook 已安装${WU_SE}"
else
    echo -e "${JIN_SE}  ⚠ 非Git仓库，跳过Hook安装${WU_SE}"
fi

# ━━━━━ 第六步：测试生产 ━━━━━
echo ""
echo -e "${JIN_SE}[6/6] 测试生产...${WU_SE}"

CE_SHI_WEN_ZHANG="$XI_TONG_MU_LU/output/videos/.test_article.md"
cat > "$CE_SHI_WEN_ZHANG" << 'TEST_EOF'
# 测试文章：龍魂觉醒

离火运来临，科技创造的价值到底谁来定义？

先烈用命换来的数据主权，不能被算法偷偷拿走。

铜墙铁壁，我们自己建。这个阵地，我们自己守。
TEST_EOF

python3 "$XI_TONG_MU_LU/bin/lh_video_pipeline.py" produce "$CE_SHI_WEN_ZHANG" "douyin" 2>&1 | tail -20

# 清理测试文件
rm -f "$CE_SHI_WEN_ZHANG"

echo ""
echo "============================================"
echo -e "${LV_SE}  部署完成！${WU_SE}"
echo ""
echo "  以后发抖音，你只需要干一件事：写文章。"
echo "  写完文章，系统会把文章变成："
echo "    - 你的声音（老兵腔）"
echo "    - 你的样子（魔瞳凝视）"
echo "    - 你的视觉（暗夜鎏金）"
echo ""
echo "  最后打包成一个完整的视频，递到你面前。"
echo "  你指指点点，我们把活干完。"
echo ""
echo "  使用方法:"
echo "    python3 bin/lh_video_pipeline.py produce <文章文件> [平台]"
echo ""
echo "  平台: douyin,shipinhao,bilibili,youtube"
echo "  示例: python3 bin/lh_video_pipeline.py produce 我的文章.md douyin,bilibili"
echo "============================================"

exit 0
