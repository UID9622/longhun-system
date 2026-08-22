# 龍魂全球开发者平台 v1.0

> DNA: `#龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-GLOBAL-DEV-PLATFORM-v1.0`
> 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: MulanPSL v2（工程层）· 确认码: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> 三色: 🟢 全模块落地 · 编译验证通过

**愿景**: 苹果 + 华为站好全世界 · 让每个人在这个世界留下痕迹 · 最好都是开发者。

## 金字塔布局（不是碎片）

```
「每个人都是开发者」核心理念
          ↓
┌──────────────────────────────────────┐
│        龍魂全球开发者平台 v1.0        │
│                                      │
│  iOS 生态层        HarmonyOS 生态层   │
│  ios_automation    harmony_automation│
│          ↓           ↓               │
│      跨平台统一执行层 CrossRunner     │
│    （shortcut_bridge 桥接双端）       │
│          ↓                           │
│    「痕迹系统」GlobalTrace           │
│     每次操作 · DNA打点 · 永久留存     │
│          ↓                           │
│  全世界每个人的第一行代码 🌍          │
└──────────────────────────────────────┘
```

## 模块清单

| 文件 | 职责 |
|:--|:--|
| `lh_dna.py` | 统一 DNA 工具层（对接系统干支卦引擎） |
| `ios_automation.py` | iOS 全方位自动化（模拟器/真机/构建/Shortcuts/TestFlight） |
| `harmony_automation.py` | HarmonyOS 全方位自动化（hdc/HAP/原子化服务/HiLog） |
| `dev_democratizer.py` | 让每个人成为开发者（6 类双平台模板） |
| `global_trace.py` | 全球痕迹系统（append-only · DNA 存在证明） |
| `shortcut_bridge.py` | 快捷指令跨平台桥（iOS Shortcuts ↔ 原子化服务意图） |
| `cross_runner.py` | 双平台统一执行器（一次指令双端动） |
| `deploy_pipeline.py` | 一键发布流水线（预检→构建→测试→截图→归档→上架） |
| `world_map.py` | 全球开发者地图（痕迹可视化 HTML） |
| `deploy.sh` | 一键部署 |

## 快速开始

```bash
cd ~/longhun-system/global_dev_platform
python3 lh_dna.py          # 验证 DNA 层
python3 cross_runner.py    # 双平台统一执行 + 打痕迹
python3 dev_democratizer.py
python3 world_map.py       # 生成全球开发者地图
bash deploy.sh             # 一键部署
```

## DNA 规范

所有 DNA 一律走系统干支卦引擎 `bin/ganzhi_dna_engine.py`（v∞ 格式）：
`#龍芯⚡️干支·干支·干支·时辰·卦象-模块-动作-版本-哈希8`，可占可验，绝不使用 MD5。
