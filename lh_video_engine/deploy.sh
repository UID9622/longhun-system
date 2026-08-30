#!/bin/bash
# deploy.sh · 龍魂视频引擎 · 一键部署
# DNA: #龍芯⚡️2026-08-22-VIDEO-ENGINE-DEPLOY-v1.1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
set -e
ENG=~/longhun-system/lh_video_engine
cd "$ENG"
echo "🎬 龍魂视频引擎 · 一键部署开始"

# 1. 创建目录
echo "1️⃣ 创建目录..."
mkdir -p schemas characters/beichen/refs output

# 2. 检查依赖
echo "2️⃣ 检查依赖..."
if which ffmpeg >/dev/null 2>&1; then echo "  ✅ ffmpeg"; else echo "  ⚠️  ffmpeg 未安装 —— 请运行: brew install ffmpeg"; fi
if which python3 >/dev/null 2>&1; then echo "  ✅ python3"; else echo "  ❌ python3 未安装"; exit 1; fi
if say -v Tingting "ok" 2>/dev/null; then echo "  ✅ say (macOS TTS·Tingting)"; else echo "  ❌ say 不可用"; exit 1; fi
if which whisper >/dev/null 2>&1; then echo "  ✅ whisper (字级对齐增强)"; else echo "  🟡 whisper 未安装——将使用插值对齐"; fi

# 3. 校验 8 个核心模块在位
echo "3️⃣ 校验核心模块..."
for m in engine script_parser character_registry tts_pipeline \
         visual_track lip_sync subtitle_gen timeline_composer; do
  if [ -f "$m.py" ]; then echo "  ✅ $m.py"; else echo "  ❌ 缺失 $m.py —— 请将 8 个 py 放入 $ENG"; exit 1; fi
done

# 4. 写入 JSON Schema
echo "4️⃣ 写入 JSON Schema..."
python3 -c "
import json, sys
sys.path.insert(0, '$ENG')
from script_parser import SCRIPT_SCHEMA
with open('$ENG/schemas/script_schema.json', 'w', encoding='utf-8') as f:
    json.dump(SCRIPT_SCHEMA, f, ensure_ascii=False, indent=2)
print('  ✅ script_schema.json 写入完成')
"

# 5. 初始化角色注册表
echo "5️⃣ 初始化角色注册表..."
python3 -c "
from character_registry import CharacterRegistry, BEICHEN_PROFILE
reg = CharacterRegistry()
if not reg.load('beichen'):
    reg.register(BEICHEN_PROFILE)
print('  ✅ 北辰角色已注册')
"

# 6. 快速测试
echo "6️⃣ 快速测试剧本解析..."
python3 -c "
from script_parser import ScriptParser
import json
result = ScriptParser.parse('欢迎。我们先看代码执行结果。接下来由北辰讲解。')
print('  ✅ 剧本解析 OK | 共', result['segment_count'], '个 Segment')
print(json.dumps(result['segments'][0], ensure_ascii=False, indent=2))
"

echo ""
echo "✅ 龍魂视频引擎部署完成"
echo ""
echo "🚀 使用示例:"
echo "   cd $ENG"
echo "   python3 engine.py --script 你的解说稿.txt --output my_video"
echo ""
echo "🟡 口型同步增强（如需）:"
echo "   cd ~ && git clone https://github.com/Rudrabha/Wav2Lip.git"
echo "   python3 engine.py --wav2lip_dir ~/Wav2Lip ..."
echo ""
echo "DNA: #龍芯⚡️2026-08-22-VIDEO-ENGINE-DEPLOY-v1.1-UID9622"
