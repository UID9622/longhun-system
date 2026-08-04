# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 产物创建标准作业程序（SOP）

> DNA: #龍芯⚡️丙午·癸未·丁未-ARTIFACT-CREATION-SOP-v1.0
> 适用范围：所有 AI 生成的源码、脚本、配置、文档、模型产物
> 生效日期：2026-07-29

---

## 目的

杜绝碎片化、垃圾文件、信息断裂。无论 AI 产出什么，都必须走同一套流水线：**创建 → 签名 → 索引 → 同步**。最终全部可归集到鲲鹏统一入口调用。

---

## 四步流水线（焊死）

| 步骤 | 动作 | 命令/位置 | 不做会怎样 |
|:---|:---|:---|:---|
| **1. 落文件** | 按规范命名、加 DNA 头部注释、写入 `bin/`/`engines/`/`scripts/`/`config/`/`01_protocols/` 等对应目录 | — | 文件散乱，找不到 |
| **2. GPG 签名** | 每个 `.py`/`.sh`/`.md`/`.json` 产物必须有 `.asc`  detached 签名 | `gpg --detach-sign --armor -o <file>.asc <file>` | 无法追溯，无法验证未被篡改 |
| **3. 本地索引** | 更新 `STATE.md` 和/或 `MEMORY.md` 的当前变量区 | 手动追加到 STATE.md §当前变量 | 状态断裂，新 AI 不知道已有产物 |
| **4. 双向同步** | 自动同步到 Notion 与鲲鹏 | `python3 scripts/sync_second_brain.py` / `bin/lh_push_all.sh` | 信息只存在本地，其他端看不到 |

---

## 文件命名与 DNA 规范

### DNA 头部注释模板

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
<中文名>
DNA: #龍芯⚡️<干支>·<模块名>-v<版本号>
功能：<一句话说明>
"""
```

### 命名规则

- Python 脚本：`lh_<功能>.py`
- 引擎：`engines/lh_<功能>_engine.py`
- 配置：`config/<功能>_rules.json`
- 协议：`01_protocols/LH-<主题>-v<版本号>.md`
- 禁止出现：`test_xxx.py`、`temp_xxx`、`新建文件夹`、`未命名` 等无意义名称

---

## 目录归属

| 产物类型 | 放入目录 | 示例 |
|:---|:---|:---|
| 可执行工具/CLI | `bin/` | `bin/lh_mac_translator.py` |
| 业务引擎 | `engines/` | `engines/lh_auto_intent.py` |
| 一次性/辅助脚本 | `scripts/` | `scripts/organize_photos.py` |
| 配置文件 | `config/` | `config/organize_rules.json` |
| 协议/规范 | `01_protocols/` | `01_protocols/LH-ARTIFACT-CREATION-SOP-v1.0.md` |
| 论文/文章 | `papers/` 或 `articles/` | `papers/xxx.md` |

---

## 签名清单

每个产物交付后，必须存在：

```
<file>.py
<file>.py.asc
```

验证命令：

```bash
gpg --verify <file>.asc <file>
```

---

## 同步命令

```bash
# 1. 本地记忆索引
python3 bin/lh_memory_load.py

# 2. 推送所有变更到鲲鹏
bin/lh_push_all.sh

# 3. 同步到 Notion
python3 scripts/sync_second_brain.py
```

---

## 禁止行为

- ❌ 不签名就交付
- ❌ 不更新 STATE.md 就结束任务
- ❌ 把产物扔在 `~/Downloads`、`~/Desktop`、`/tmp` 不管
- ❌ 创建临时文件后不清理
- ❌ 同一功能重复造轮子，不复用现有引擎

---

## 签章

| 签章方 | 确认 |
|:---|:---|
| 创世者 | UID9622 |
| DNA | #龍芯⚡️丙午·癸未·丁未-ARTIFACT-CREATION-SOP-v1.0 |
| 生效 | 2026-07-29 |
