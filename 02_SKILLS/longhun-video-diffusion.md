# 🐲 龍魂 · 视频扩散引擎 · longhun-video-diffusion

**DNA:** `#龍芯⚡️丙午·丙申·丙寅·甲午·䷕贲-LONGHUN-VIDEO-DIFFUSION-v1.0`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

> 项目索引文件。完整技能定义见：`~/.kimi-code/skills/longhun-video-diffusion/SKILL.md`

---

## 一句话
把 ComfyUI + AnimateDiff-Evolved 拉进龍魂生态，封装成本地视频生成技能。

## 触发词
视频生成、真实运动、AnimateDiff、ComfyUI、图生视频、EP01 成片、龍影、longhun-video-diffusion

## 核心入口
```bash
cd ~/longhun-system && source .venv/bin/activate

# 单镜头
python3 08_BIN/story_factory/lh_animatediff_generate.py \
  --image ~/Pictures/龍魂素材仓库/ENV-02_老街雨夜.png \
  --prompt "night street, neon lights, falling rain" \
  --shot E01-S01

# 全片装配
python3 08_BIN/story_factory/lh_ep01_assembler.py \
  --backend-video animatediff
```

## 龍魂人格
龍影 P-VIDEO-001 —— 视频生成执行人格。

## 三色审计
- 🟢 宜：本地生成、带 DNA、低算力试播
- 🔴 禁：复刻真人脸、未授权商用、删 DNA
- 🟡 慎：面部漂移、循环补时、低分辨率

## 状态
已落地 v1.0，EP01「雪夜初见」已通过本技能生成真实运动版成片。
