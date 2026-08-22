# 🐉 龍魂 · 故事工厂 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·辛酉·巳时·䷀乾-STORY-FACTORY-UID9622`

> 小说/剧本 → AI 连续剧资产流水线。角色不动点、素材货架制、人格声线、DNA 水印，全部本地可控。  
> **v1.3 更新：F5-TTS 本地声音克隆接入，EP01 装配器可用 UID9622 官方声线；视频输出固定到 `~/Pictures/龍魂素材仓库/videos/`。**
> **v1.2 更新：MeloTTS 本地中文 TTS 接入，EP01 装配器可用本地神经声线；不再依赖 macOS `say` 或在线 API。**

---

## 一、设计理念

1. **角色 = 不动点**：一张锚点图锁脸，全剧不换脸。
2. **素材 = 货架制**：一物一码，生成一次，终身复用。
3. **人格 = 可激活资产**：角色卡锁脸，人格锁味儿。
4. **输出 = 带 DNA**：每张图、每段音、每个镜头都带龍魂水印与来源码。
5. **低算力优先**：720p 试播、1080p 定稿、高光镜头单独 4K。

---

## 二、快速开始

```bash
# 进入工厂目录（必须在 .venv 中，故事工厂依赖 mlx_lm / Pillow 等）
cd ~/longhun-system/08_BIN/story_factory
source ../../.venv/bin/activate

# 一键安装开源工具链
bash setup_tools.sh

# 索引素材仓库
python3 lh_warehouse_indexer.py

# 初始化项目（例如：坏蛋项目）
python3 lh_story_factory.py init 坏蛋

# 创建角色卡
python3 lh_story_factory.py character 坏蛋 create \
  --code HD-002 \
  --name 三眼 \
  --role 双花红棍 \
  --face 寸头浓眉眉心竖印 \
  --height 185cm \
  --build 魁梧 \
  --age 25 \
  --mark 眉心竖印怒时泛红 \
  --costume 黑色劲装皮夹克 \
  --persona P-SY-001 \
  --seed 123456

# 列出角色
python3 lh_story_factory.py character 坏蛋 list

# 注册素材到货架
python3 lh_story_factory.py asset 坏蛋 register \
  --code S-01-01-001 \
  --category S \
  --name 金刀 \
  --path assets/坏蛋/props/S-01-01-001.png

# 注入龍魂水印
python3 lh_story_factory.py watermark \
  --input assets/坏蛋/characters/HD-002.png \
  --output output/HD-002_watermarked.png
```

---

## 三、目录结构

```
story_factory/
├── lh_story_factory.py          # 主控 CLI（项目/角色/素材/人格/水印）
├── lh_script_writer.py          # 编剧大脑：本地模型 + Kimi K3 API 双后端
├── lh_story_pipeline.py         # 故事流水线：分镜表 → 语音 + 视频 + DNA 清单
├── lh_ep01_assembler.py         # EP01「雪夜初见」低成本本地装配器
├── lh_voice_engine.py           # 语音引擎（GPT-SoVITS / 系统 say 兜底）
├── lh_melotts_tts.py            # MeloTTS 本地中文 TTS 包装器
├── lh_kokoro_tts.py             # Kokoro 本地 TTS 包装器
├── lh_f5tts_clone.py            # F5-TTS 本地声音克隆包装器（UID9622官方声线）
├── lh_video_engine.py           # 视频引擎（AnimateDiff / zoompan 兜底）
├── lh_animatediff_generate.py   # ComfyUI+AnimateDiff-Evolved 真实运动生成
├── install_comfy_deps.py        # 安全安装 ComfyUI 依赖（保护现有 torch）
├── install_melotts_deps.py      # 安全安装 MeloTTS 依赖（保护 torch/numpy）
├── patch_melotts_for_zh.py      # MeloTTS 中文懒加载补丁（无需系统 MeCab）
├── download_models.py           # HF 镜像下载 SD 1.5 + motion module
├── lh_warehouse.py              # 素材仓库查找工具
├── lh_warehouse_indexer.py      # 素材仓库索引器
├── lh_watermark.py              # 可见水印注入
├── lh_kimi_distiller.py         # Kimi K3 蒸馏器：批量造训练数据
├── setup_tools.sh               # 开源工具链一键安装
├── configs/
│   ├── personas.json        # 默认人格声线库
│   ├── tools.json           # 推荐开源工具链
│   ├── warehouse.json       # 素材仓库根目录配置
│   └── warehouse_index.json # 素材索引（由 indexer 生成）
├── assets/
│   └── {project}/
│       ├── project.json     # 项目元数据 + DNA
│       ├── characters/      # 角色卡 JSON
│       ├── props/           # 道具图
│       ├── scenes/          # 场景图
│       └── voices/          # 声音样本
└── output/                  # 水印/语音/视频/分镜表/流水线清单输出
```

---

## 四、一条龙：编剧大脑 → 分镜表 → 成片

### 双后端编剧大脑

```bash
# 本地模型（离线，数据主权）
python3 lh_script_writer.py \
  --project 坏蛋 \
  --theme "谢文东与三眼在雨夜老街初次相遇" \
  --shots 3 \
  --assets "ENV-02_老街雨夜.png,HD-001_谢文东_少年锚点图.png,HD-002_三眼_锚点图.png" \
  --backend local

# Kimi K3 API（在线，质量更高；需环境变量 KIMI_API_KEY）
python3 lh_script_writer.py \
  --project 坏蛋 \
  --theme "三眼雨夜持刀救谢文东" \
  --shots 3 \
  --assets "ENV-02_老街雨夜.png,HD-002_三眼_锚点图.png" \
  --backend kimi \
  --max-tokens 2048

# 自动选择：有 KIMI_API_KEY 就用 K3，否则本地
python3 lh_script_writer.py \
  --project 坏蛋 \
  --theme "谢文东收服李爽的第一场酒局" \
  --shots 3 \
  --backend auto
```

### EP01 低成本本地装配（推荐）

```bash
# 1. 安装 MeloTTS 或 F5-TTS（首次，二选一即可）
python3 install_melotts_deps.py
# 或：pip install -e third_party/F5-TTS

# 2. 生成 EP01 完整成片（本地神经声线 + 图片运镜）
python3 lh_ep01_assembler.py \
  --backend-voice melotts \
  --backend-video zoompan

# 2b. 使用 UID9622 官方克隆声线（需已准备 voice_samples/uid9622/*.wav）
python3 lh_ep01_assembler.py \
  --backend-voice f5tts \
  --backend-video zoompan

# 3. 输出位置（固定，不深）
#    主目录: ~/Pictures/龍魂素材仓库/videos/EP01_雪夜初见/final/EP01_雪夜初见_成片_v1.mp4
#    快捷入口: ~/Movies/龍魂成片/EP01_雪夜初见/final/EP01_雪夜初见_成片_v1.mp4
```

**实测：** 33 镜、154 秒成片、MPS 加速，约 10 分钟完成；音频带人格 speed 差异。f5tts 每句约 10-15s（含模型加载），全片约 30-40 分钟。

### 运行流水线（语音 + 视频）

```bash
python3 lh_story_pipeline.py \
  --project 坏蛋 \
  --script output/scripts/坏蛋_script_*.json \
  --backend-video ffmpeg \
  --backend-voice system
```

输出：`output/voice/`、`output/video/`、`output/pipelines/` 带 DNA 清单。

### 真实运动镜头（AnimateDiff）

```bash
# 单镜头生成（MPS 加速，Apple Silicon 可用）
python3 lh_animatediff_generate.py \
  --image ~/Pictures/龍魂素材仓库/ENV-02_老街雨夜.png \
  --prompt "night street, neon lights, falling rain, cinematic atmosphere" \
  --shot E01-S01

# EP01 装配器切换真实视频后端
python3 lh_ep01_assembler.py \
  --backend-voice system \
  --backend-video animatediff

# 低算力测试：先用 zoompan 快速看节奏，再切 animatediff 出定稿
python3 lh_ep01_assembler.py --backend-video zoompan   # 快，图片运镜
python3 lh_ep01_assembler.py --backend-video animatediff  # 慢，真实运动
```

**语音后端对比：**
| 后端 | 依赖 | 联网 | 质量 | 速度 |
|---|---|---|---|---|
| `system` | macOS `say` | 否 | 机械 | 极快 |
| `melotts` | MeloTTS 本地 | 否 | 自然中文 | 中（MPS 约 10s/句） |
| `f5tts` | F5-TTS 本地 | 否（首次下载约1.6GB） | 克隆用户音色 | 中（每句约10-15s含加载） |
| `kokoro` | Kokoro ONNX | 否 | 自然多语言 | 快 |
| `edge` | edge-tts | 是 | 自然 | 中 |

**诚实边界：**
- MPS 生成 1.5s@384px 镜头约 30-90s；全片 30 镜约 15-45 分钟。
- 当前分辨率 384×384（低算力优先），后续可上 512/720。
- 人物脸在动态中可能漂移，高光特写建议仍用 zoompan 或单独修脸。

---

## 五、路线 B：用 Kimi K3 蒸馏本地编剧模型

```bash
# 1. 用 K3 批量生成 10 个主题的分镜表样本
python3 lh_kimi_distiller.py \
  --project 坏蛋 \
  --output-dir output/distill \
  --max-tokens 2048 \
  --sleep 1

# 2. 生成后的文件
#    output/distill/坏蛋_kimi_raw_*.jsonl    原始分镜表（可人工审稿）
#    output/distill/坏蛋_kimi_train_*.jsonl  训练样本（可合并进训练池）

# 3. 合并进 longhun-small-instruct-v1.3 训练数据（示例）
cat output/distill/坏蛋_kimi_train_*.jsonl >> \
  ../../models/longhun-small-instruct-v1.3/data/train.jsonl

# 4. 重新训练
#    cd ../../ && .venv/bin/python3 08_BIN/lh_lora_trainer_instruct.py train --lr 1e-5
```

---

## 六、推荐开源工具链

### 图像生成 + 角色一致性
- **ComfyUI** + **IPAdapter FaceID Plus V2**
- 角色卡中的 reference image 作为 IPAdapter 输入，weight 建议 0.85

### 视频生成
- **ComfyUI + AnimateDiff-Evolved**（SD 1.5，本地 MPS/CPU 可跑，真实运动）
- **CogVideoX** / **HunyuanVideo**（高清长镜头，后续接入）

### 语音合成 / 克隆
- **MeloTTS**（本地中文，零 API，MPS/CPU 可跑，已接入 EP01 装配器）
- **Kokoro**（本地轻量，多语言，已接入）
- **GPT-SoVITS**（中文首选，需要 CUDA，macOS 仅占位）
- **OpenVoice** / **F5-TTS**（轻量备选）

### 水印 / 来源存证
- 本模块内置可见水印
- **C2PA Python SDK** 用于元数据签名
- **stegano** 用于轻量隐写

---

## 七、低算力原则

1. 试播期：720p，单镜头 2-4 秒
2. 角色/场景首件定调，不逐集重 roll
3. 复用 > 重新生成
4. 高光镜头单独上 4K，普通镜头 1080p

---

## 八、版权与合规

- 本工具链只做技术验证与原创化改编。
- 未授权前不商用、不复制原著原文。
- 不复刻真人脸、不输出武器设计参数。
