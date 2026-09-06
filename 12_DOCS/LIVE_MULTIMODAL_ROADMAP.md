---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-LIVE-MULTIMODAL-ROADMAP-v1.0`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·多模态实时交互接入路线图 v1.0

> DNA: #龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-LIVE-MULTIMODAL-ROADMAP-v1.0
> 目标：让语音、视觉、实时流都能走统一的龍魂审计流水线，数据根留本地。

---

## 一、设计原则（焊死）

1. **本地优先**：所有音频/视频/截图先在本地处理，原始流不上云。
2. **隐私主权**：敏感内容（人脸、证件、个人文件）只做本地特征提取，不存储原图。
3. **先审后发**：任何模态输入都必须先过 `SafeAI → KFPP → CSDN → Judge` 序列执行引擎。
4. **按钮触发**：所有实时功能都是“按住说话 / 点击截图 / 开启直播”，不会后台偷录。
5. **可审计**：每次多模态会话生成 DNA 签章，留存日志在 `.longhun/live_sessions/`。

---

## 二、语音接入方案

### 2.1 输入：ASR（语音 → 文本）

| 方案 | 实现 | 适用场景 |
|---|---|---|
| 本地 Whisper | `whisper.cpp` 或 `faster-whisper` | 日常对话、长音频 |
| Ollama 语音扩展 | 本地部署语音模型 | 离线、隐私极高 |
| macOS 原生 | `Dictation` / `say` 配套 | 快速原型、系统级可用 |

**入口命令：**
```bash
lh listen              # 按住说话，松手后自动转文字并走序列审计
lh voice --file a.wav  # 对已有音频做 ASR + 审计
```

### 2.2 输出：TTS（文本 → 语音）

| 方案 | 实现 | 说明 |
|---|---|---|
| macOS `say` | 系统自带 | 零依赖，快速反馈 |
| Piper | 本地轻量 TTS | 可切换人格音色 |
| Edge-TTS 本地代理 | `lh_local_ai_relay.py` | 可选，默认不走外网 |

**入口命令：**
```bash
lh speak "审计通过"    # 用默认人格音色播报
lh speak --persona 宝宝 "哥哥，这段内容是安全的哦"
```

---

## 三、视觉接入方案

### 3.1 输入源

| 输入源 | 工具 | 处理 |
|---|---|---|
| 屏幕截图 | `mss` / `PIL` | OCR + 安全审计 |
| 摄像头帧 | `OpenCV` / `AVFoundation` | 人脸模糊 + 物体识别 + 审计 |
| 本地图片 | 文件路径 | OCR + 内容审核 |
| 浏览器画面 | 观澜浏览器协议 | 网页内容实时抓取 |

### 3.2 OCR / 内容理解

- **中文优先**：`longhun-ocr`（笔画/结构/龍字检测）
- **国际兜底**：`OpenCV + Tesseract`
- **场景识别**：本地轻量 CLIP / YOLO 模型（证件、截图、二维码等）

**入口命令：**
```bash
lh watch               # 实时监控屏幕，触发异常时告警
lh screenshot          # 截屏并审计
lh ocr /path/to/img    # 图片 OCR + 内容审计
```

### 3.3 隐私保护

- 人脸默认打码（本地高斯模糊）。
- 证件、银行卡等敏感区域触发 `P0_ETERNAL_LOCK` 级本地加密。
- 视觉特征向量本地存储，原图可选“阅后即焚”。

---

## 四、实时交互方案

### 4.1 架构

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────────────┐
│ 麦克风/摄像头 │ ──→ │ 本地特征提取  │ ──→ │ SafeAI → KFPP → CSDN → Judge │
└─────────────┘     └──────────────┘     └─────────────────────────────┘
                                                   │
                    ┌──────────────┐              ▼
                    │ 人格音色 TTS  │ ←──── 序列执行结果
                    └──────────────┘
```

### 4.2 参考实现：`bin/lh_live.py`

- 使用 `PyAudio` 捕获麦克风块（每 2-5 秒一段）。
- 使用 `OpenCV` 捕获摄像头帧（可选，默认关闭）。
- 每段音频先做 ASR → 文本 → 序列执行引擎。
- 若结果 ≥ L2，立即语音播报告警；若 L4，立即中断会话并留证。
- 会话结束后生成 `live_session_<dna>.json` 审计报告。

**入口命令：**
```bash
lh live                # 启动实时语音交互
lh live --camera       # 同时开启摄像头（需确认）
lh live --screen       # 同时监控屏幕（需确认）
```

### 4.3 Web 实时方案（可选第二阶段）

- 浏览器 `MediaDevices.getUserMedia()` 采集音视频。
- WebSocket 推到本地 `lh_live_server.py`（localhost only）。
- 服务端调用 ASR/OCR + 序列执行引擎，结果回推浏览器。
- 全部不经过公网，适合桌面端可视化面板。

---

## 五、统一命令入口

| 命令 | 功能 | 触发流水线 |
|---|---|---|
| `lh listen` | 语音输入 | SafeAI → KFPP → CSDN → Judge |
| `lh speak "..."` | 语音播报 | 仅 TTS |
| `lh watch` | 屏幕/摄像头监控 | 每帧走 SafeAI |
| `lh screenshot` | 截屏审计 | SafeAI + OCR |
| `lh live` | 实时音视频交互 | 分段走完整流水线 |

自然语言路由同步增加触发词：
- “听一下”、“语音输入”、“按住说话” → `lh listen`
- “看一下屏幕”、“截个图” → `lh screenshot`
- “开直播”、“实时对话” → `lh live`

---

## 六、第一阶段 MVP（30 天）

1. **Week 1**：`bin/lh_listen.py`（Whisper ASR + 序列执行）。
2. **Week 2**：`bin/lh_screenshot.py`（截屏 + OCR + 序列执行）。
3. **Week 3**：`bin/lh_live.py`（PyAudio 实时块 + SafeAI 拦截）。
4. **Week 4**：接入 `lh.py` 菜单、自然语言路由、GPG 签名、鲲鹏同步。

---

## 七、风险与熔断

| 风险 | 对策 |
|---|---|
| 麦克风/摄像头后台偷录 | 必须按住/点击触发，状态栏显示 🟢 录制中 |
| 语音误识别导致误审 | ASR 结果带置信度，<0.8 时要求重说 |
| 视觉敏感信息泄露 | 本地人脸/证件脱敏，原图 7 天自动清理 |
| 实时流被 prompt 注入 | 每段输入都过 SafeAI L4 熔断 |

---

## 八、接口约定

所有多模态模块输出统一 JSON：

```json
{
  "session_id": "live-20260729-001",
  "input_type": "voice|screen|camera|text",
  "input_preview": "...",
  "pipeline_result": { "final_level": "PASS", "results": [...] },
  "dna": "#龍芯⚡️...",
  "timestamp": "2026-07-29T08:16:41+08:00"
}
```

---

> 本路线图为可执行方案，不是纯设想。下一步优先落地 `lh_listen.py` 和 `lh_screenshot.py`。
>
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

```json
{
  "dna": "#龍芯⚡️丙午·乙未·甲辰·庚午·䷔噬-LIVE-MULTIMODAL-ROADMAP-v1.0",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
