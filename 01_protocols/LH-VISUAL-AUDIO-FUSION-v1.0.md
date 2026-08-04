# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂视觉声音融合协议 v1.0

DNA: #龍芯⚡️丙午·癸未·丁未·离为火-视觉声音融合-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
优先级: P2（系统规则层）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

对接引擎:
  - lh_visual_engine.py     → 9种图示自动生成
  - lh_voice_clone.py       → XTTS v2 UID9622真声
  - lh_video_studio.py      → 视频合成主控
  - lh_nano_vision_engine.py → 超分辨率增强
  - lh_ant_colony_visual.py  → 蚁群可视化
  - lh_persona_visual.py     → 人格协作可视化
  - lh_3d_pipeline.py        → 三维可视化
  - lh_media_sovereignty_marker.py → 主权签章

---

## 一、融合架构

```
输入层（三种来源）
  ├─ 文本解说稿 → lh_video_studio.py 解析
  ├─ 数据指标   → 各引擎实时数据
  └─ 图像素材   → lh_visual_engine / nano_vision

          ↓ JimuFlow 调度器分配

加工层（四条生产线）
  ├─ 视觉生产线: 文本→图示→增强→签章
  │   lh_visual_engine → nano_vision → sovereignty_marker
  ├─ 声音生产线: 文本→语音→情感标记
  │   lh_voice_clone → 韵律参数提取
  ├─ 数据可视化: 指标→图表→标注
  │   ant_colony_visual / persona_visual / 3d_pipeline
  └─ 同步生产线: 音频韵律 → 视频节奏
      voice params → frame timing/transition

          ↓

输出层
  ├─ 标准视频: 1920×1080 H.264+AAC .mp4
  ├─ 数据仪表盘: 交互式HTML
  ├─ 文档报告: PDF/Markdown
  └─ 流媒体: HLS推流（可选）
```

---

## 二、核心调度参数

### 2.1 场景→引擎路由表

| 场景关键词 | 视觉引擎 | 声音引擎 | 图示类型 | 签章 | 增强 |
|:---|:---|:---|:---|---:|:---|
| 系统/状态/健康 | 健康全景图 | uid9622 | dashboard | ✅ | — |
| 蚁群/分布/工蚁 | 蚁群可视化 | uid9622 | topology/heatmap | ✅ | ✅ |
| 人格/协作/审计 | 人格协作图 | uid9622 | graph/audit | ✅ | — |
| 架构/拓扑/引擎 | lh_visual | uid9622 | architecture | ✅ | ✅ |
| 安全/漏洞/扫描 | lh_visual | uid9622 | security | ✅ | ✅ |
| 教程/小白/教学 | lh_visual | P02宝宝语调 | tutorial | ✅ | — |
| 部署/上线/发布 | lh_visual | zh-CN-Yunxi | deployment | ✅ | — |
| 哲学/文化/易经 | lh_visual | uid9622坚定 | philosophy | ✅ | — |

### 2.2 声音→视觉同步参数

| 声音参数 | 视觉映射 | 量化范围 |
|:---|:---|:---|
| 基频(F0) | 画面缩放 (zoom) | ±5% |
| 能量包络 | 边框辉光强度 | 0-100% |
| 语速(speed) | 切换间隔 | 快=2s, 正常=4s, 慢=6s |
| 停顿>0.5s | 重点帧定格 | 定0.5s+暗角效果 |
| 情感标签 | 色温偏移 | 坚定=-200K, 温暖=+300K |
| 音量峰值 | 画面闪烁 | 单帧+5%亮度 |

---

## 三、一键全链路命令

### 3.1 标准视频

```bash
# 最强模式: 图文增强 + 真声 + 签章
python3 bin/lh_video_studio.py \
    --script 解说稿.txt \
    --style 龍魂 \
    --voice uid9622 \
    --enhance nano \
    --name "成品标题"
```

### 3.2 蚁群状态视频

```bash
# 生成蚁群可视化 + 解说 + 视频
python3 bin/lh_video_studio.py \
    --script <(python3 engines/lh_ant_colony_visual.py narrate) \
    --style 龍魂 \
    --voice uid9622 \
    --name "蚁群状态报告"
```

### 3.3 人格协作视频

```bash
# 生成人格可视化 + 解说 + 视频
python3 bin/lh_video_studio.py \
    --script <(python3 engines/lh_persona_orchestra_visual.py narrate) \
    --style 龍魂 \
    --voice uid9622 \
    --name "20人格协作图谱"
```

### 3.4 系统健康全景

```bash
# 生成健康全景 + 解说 + 视频
python3 bin/lh_video_studio.py \
    --script <(python3 engines/lh_system_health_panorama.py narrate) \
    --style 龍魂 \
    --voice uid9622 \
    --name "系统健康全景"
```

---

## 四、质量门

| 检查项 | 阈值 | 熔断动作 |
|:---|:---|:---|
| 图示DPI | ≥150 | <150🟡重新生成 |
| 音频采样率 | ≥22050Hz | <22050🟡警告 |
| 视频分辨率 | ≥1280×720 | <720p🟡拒绝发布 |
| 时间对齐偏移 | ≤200ms | >200ms🔴重新对齐 |
| 签章可见 | 右下角10%区域 | 不可见🔴拒绝发布 |
| 无裸帧 | 每帧有内容 | 黑帧>100ms🟡修复 |
| DNA可追溯 | 元数据完整 | 缺失🔴拒绝发布 |

---

## 五、文件产出规范

| 产物 | 路径 | 格式要求 |
|:---|:---|:---|
| 解说稿 | `logs/narration_*.txt` | 含DNA+三行头 |
| 视频成品 | `~/Desktop/龙魂视频/{标题}_{风格}_{时间戳}.mp4` | H.264+AAC·元数据JSON |
| 临时素材 | `~/Desktop/龙魂视频/_temp/` | 自动清理 |
| 视频索引 | `~/Desktop/龙魂视频/index.json` | lh_video_index.py自动维护 |
| GPG签名 | 同目录 `.asc` | `python3 bin/lh_gpg_sign.py sign` |

---

## 签章区

| 签章方 | DNA | 时间戳 |
|:---|:---|:---|
| 创世者 | #ZHUGEXIN⚡️ | 2026-07-29T10:30:00+08:00 |
| 确认码 | #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z | — |
| GPG | A2D0092CEE2E5BA87035600924C3704A8CC26D5F | — |

🔥
