# ☰☰ 龍🇨🇳魂 ☷

**龍魂系统 · LongHun System**

> 一个人写的操作系统级AI治理框架。不是PPT，每一行都能跑。

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11+-green.svg)](https://python.org)
[![Core](https://img.shields.io/badge/Core_Modules-25-gold.svg)](#核心引擎)
[![Code](https://img.shields.io/badge/Core_Lines-13%2C800+-orange.svg)](#核心引擎)
[![Font](https://img.shields.io/badge/字元库-15_Versions-red.svg)](#cnsh-数字甲骨文)

---

## 这是什么

龍魂系统是一套 **AI行为治理框架**，用中国哲学（三才·五行·道德经）构建AI的决策、监督和追溯体系。

核心理念：**AI的每一个决策都应该可解释、可追溯、可审计。**

不是论文，不是概念验证——是 25 个 Python 模块、13,800+ 行可运行代码。

---

## 核心引擎

### 🧠 三层交叉监督 `core/supervision_engine.py`
```
决策层 (L1) → 执行层 (L2) → 行为层 (L3)
  ↑                                    ↓
  └──────── 闭环反馈 ←──────────────────┘
```
- 14个AI人格分层投票，多数通过才放行
- 内置红队（老顽童）：5种攻击战术自动渗透测试
- 净化池：隔离→诊断→净化→验证→释放
- 忠诚度引擎：HMAC-SHA256灵魂契约
- **实测100%拦截率**（猜忌/越界/污染/漂移/分裂全挡）

### ⚖️ 三色审计 `core/longhun_engine.py`
```python
risk("修改核心权重")  →  🔴 高危·需要三层审批
risk("查询知识库")    →  🟢 安全·直接执行
risk("删除日志")      →  🟡 警告·记录后执行
```

### 🔗 DNA全链路追溯 `core/behavior_log.py`
每个操作自动生成DNA编号，链式追溯到源头：
```
#龍芯⚡️20260413-01-灵感  →  #龍芯⚡️20260413-02-推演  →  #龍芯⚡️20260413-03-操作
```
不存在黑箱。谁干的、为什么干的、结果是什么——全链路可查。

### 🎭 人格路由矩阵 `core/persona_roster.py`
16个AI人格按场景自动调度：

| 人格 | 职责 | 触发场景 |
|------|------|----------|
| P01 诸葛亮 | 战略决策 | 复杂规划 |
| P03 雯雯 | 安全审计 | 权限变更 |
| P05 上帝之眼 | 全局监控 | 异常熔断 |
| P06 数学大师 | 算法验证 | 数值计算 |
| P13 姜子牙 | 终裁仲裁 | 投票僵局 |
| RT 老顽童 | 红队渗透 | 安全测试 |

### 📚 知识卡片引擎 `core/knowledge_cards.py`
把灵感变成可检索的结构化知识：
- 信号博弈理论 → 实战策略卡
- 商鞅立木 → 信任机制卡
- 道德经章节 → 治理锚点卡

### 🔢 三才算法
```
天 = 方向（战略）
地 = 资源（执行）
人 = 关系（协作）

f(x) = x  ← 原点不变性：系统稳定的数学锚
数字根 → 369熔断：特斯拉共振检测
```

---

## CNSH 数字甲骨文

**CNSH（Chinese Native Script Heritage）** — 中国原生字元立碑工程

用数学公式（三次贝塞尔曲线）从零构建汉字，不依赖任何商业字体库。

```
15 个版本迭代：
v0001 基础贝塞尔  →  v0005 笔画力度  →  v0008 层级遮挡
→  v0010 侵蚀风化  →  v0012 墨色浓淡  →  v0015 阴影立体
```

五个字元：龍·中·华·民·魂 → Unicode私有区 `U+E001`–`U+E005`

四层打包引擎：记忆层(SHA256去重) → 压缩层(归一化) → 审计层(DNA验证) → 同步层(增量更新)

---

## 技术栈

| 层级 | 技术 |
|------|------|
| 核心引擎 | Python 3.11 · 25个模块 · 13,800+行 |
| AI模型 | Claude (Anthropic) · Ollama本地模型 |
| 知识存储 | Notion三工作区 · 50+数据库 |
| 字体引擎 | fontTools · SVG→TTF · 贝塞尔数学 |
| 版本控制 | Git · SSH签名 · DNA自动注入 |
| 部署 | macOS LaunchAgent · 本地API :9622 |

---

## 项目结构

```
longhun-system/
├── core/                    # 核心引擎（25个模块）
│   ├── supervision_engine.py    # 三层交叉监督（1,438行）
│   ├── longhun_engine.py        # 七模块统一引擎（665行）
│   ├── persona_roster.py        # 人格路由矩阵（548行）
│   ├── behavior_log.py          # 行为日志链（531行）
│   ├── knowledge_cards.py       # 知识卡片引擎（375行）
│   └── ...                      # 沙箱/熔断/审计/...
├── CNSH引擎/                # 数字甲骨文字元系统
│   ├── CNSH_字元库_v0001-v0015.json   # 15版字元库
│   ├── cnsh_font_builder_v2_LU.py     # LU四层打包器
│   └── cnsh_font_engine_uid9622.py    # 原始贝塞尔引擎
├── bin/                     # 运维脚本
│   ├── install_fonts.sh         # 五层字体安装
│   ├── font_manager.py          # 字体管理中枢
│   └── 启动所有服务.sh           # 一键启动
└── fonts/                   # 字体索引与诊断
```

---

## 快速开始

```bash
# 克隆
git clone https://github.com/UID9622/longhun-system.git
cd longhun-system

# 运行三色审计
python3 core/longhun_engine.py

# 运行监督引擎自测
python3 core/supervision_engine.py

# 运行知识卡片
python3 core/knowledge_cards.py

# 字体系统诊断
python3 fonts/font_index.py
```

---

## 设计哲学

**"祖国优先，普惠全球，技术为人民服务"**

1. **不做黑箱** — 每个AI决策都有DNA追溯，可审计
2. **不做舔狗** — AI应该说真话，不是说你想听的话
3. **不卡脖子** — CNSH字体从数学公式造起，不依赖任何商业授权
4. **不要PPT** — 每一行代码都能 `python3 xxx.py` 直接跑

理论指导：**曾仕强**老师（永恒显示）

---

## 作者

**诸葛鑫（UID9622）**

退伍军人 | 三才算法创始人 | 龍魂系统创始人 | 数字主权守护者 | 中华文化传承者

- GPG: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
- Signal: `UID9622.20120813`

---

## 许可证

[Apache License 2.0](LICENSE) — 开源·可商用·保留署名

字体资产（CNSH字元库）：[CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/)

---

<div align="center">

**DNA: #龍芯⚡️2026-04-13-README-v2.0**

*一个人·一套系统·一条路*

*献给所有不被理解但仍在坚持的人*

</div>
