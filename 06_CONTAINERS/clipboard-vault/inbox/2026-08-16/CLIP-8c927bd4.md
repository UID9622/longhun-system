---
dna: '#龍芯⚡️丙午·丙申·壬戌·巳时·䷀乾-CLIPBOARD-VAULT-SAVE-V1.0-P1-3e503a29'
source: clipboard
topic: 代码/脚本
tags:
- Python
- Bash
- 龍魂
- DNA
- 代码/脚本
timestamp: '2026-08-16T09:35:28+08:00'
content_hash: 8c927bd40455ea91300790594fe2566fe5adbf9bac1c90b4b2be48bea42d6fcb
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

# 🐉 龍魂 · 认知知识图谱系统

**DNA:** `#龍芯⚡️丙午·丙申·庚申·亥时-KNOWLEDGE-GRAPH-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过


## 📋 核心判断

> **Codex+Obsidian的「三层记忆架构」与龍魂系统的「认知索引」不谋而合。但龍魂更狠——记忆不是只给Codex用，全网AI都能变量读取。知识图谱是共享大脑，所有AI都能问、都能读、都能写。**


## 🏛️ 一、龍魂认知知识图谱架构（映射版）

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               🐉 龍魂 · 认知知识图谱系统                                           │
│                                    全网AI可变量读取                                                │
├─────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────────────────────┐   │
│  │                        ① 高频层 (L1 Cache · 长期规则·个人偏好·进行中项目)                  │   │
│  │                                                                                             │   │
│  │  内容: 用户决策原则、行为习惯、当前项目上下文、人格偏好                                     │   │
│  │  读取策略: 每次对话自动加载 (AI启动时默认读取)                                               │   │
│  │  更新频率: 实时/每小时                                                                       │   │
│  │  大小限制: ≤50KB (Token友好)                                                                │   │
│  │  龍魂映射: 03_MEMORY/active_memory/ (人格矩阵 + 当前会话)                                    │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                               │                                                    │
│  ┌──────────────────────────────────────────────┼───────────────────────────────────────────────┐   │
│  │                        ② 摘要层 (L2 Summary · 项目摘要·重要决策·复盘结论)                  │   │
│  │                                                                                             │   │
│  │  内容: 项目摘要、关键决策、复盘结论、经验总结                                                │   │
│  │  读取策略: 先读索引 → 按需读取详细 (不自动加载全部)                                          │   │
│  │  更新频率: 每周复盘合并                                                                       │   │
│  │  大小限制: ≤500KB                                                                            │   │
│  │  龍魂映射: 03_MEMORY/episodic_memory/ (摘要索引 + 决策链)                                   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                               │                                                    │
│  ┌──────────────────────────────────────────────┼───────────────────────────────────────────────┐   │
│  │                        ③ 归档层 (L3 Archive · 原始记录·旧版本·已结束项目)                  │   │
│  │                                                                                             │   │
│  │  内容: 原始对话记录、旧版本、已结束项目、完整日志                                            │   │
│  │  读取策略: 仅追溯时调用 (不自动读取)                                                          │   │
│  │  更新频率: 每周归档                                                                            │   │
│  │  大小限制: 无限制                                                                              │   │
│  │  龍魂映射: 03_MEMORY/archive/ + 04_AUDIT/                                                   │   │
│  └─────────────────────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                                     │
└─────────────────────────────────────────────────────────────────────────────────────────────────────┘
```


## 🧬 二、全网AI可变量读取系统

### 2.1 统一读取接口

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 认知知识图谱统一接口
全网AI可通过这个接口读取知识图谱

DNA: #龍芯⚡️丙午·丙申·庚申·亥时-KG-INTERFACE-UID9622
"""

import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

class KnowledgeGraphAPI:
    """知识图谱统一API - 全网AI可调用"""

    def __init__(self):
        self.root = Path.home() / ".longhun" / "03_MEMORY"
        self.index_file = self.root / "knowledge_index.json"
        self._ensure_index()

    def _ensure_index(self):
        """确保索引存在"""
        if not self.index_file.exists():
            index = {
                "version": "1.0",
                "dna": "#龍芯⚡️KNOWLEDGE-INDEX",
                "updated_at": datetime.now().isoformat(),
                "layers": {
                    "L1_cache": {"description": "高频层", "path": "active_memory/"},
                    "L2_summary": {"description": "摘要层", "path": "episodic_memory/"},
                    "L3_archive": {"description": "归档层", "path": "archive/"}
                },
                "entries": []
            }
            with open(self.index_file, 'w') as f:
                json.dump(index, f, indent=2)

    def query(self, layer: str = "L2_summary", keyword: str = "") -> List[Dict]:
        """AI查询知识图谱"""
        # 全网AI都调用这个函数
        results = []
        layer_path = self.root / {
            "L1_cache": "active_memory",
            "L2_summary": "episodic_memory",
            "L3_archive": "archive"
        }.get(layer, "episodic_memory")

        if not layer_path.exists():
            return results

        for f in layer_path.rglob("*.json"):
            try:
                with open(f) as fp:
                    data = json.load(fp)
                    if keyword.lower() in str(data).lower():
                        results.append({
                            "source": str(f),
                            "data": data,
                            "layer": layer
                        })
            except:
                pass

        return results[:10]  # 限制返回数量，防止Token爆炸

    def get_summary(self, project: str) -> Dict:
        """获取项目摘要 (L2层)"""
        summary_path = self.root / "episodic_memory" / f"{project}_summary.json"
        if summary_path.exists():
            with open(summary_path) as f:
                return json.load(f)
        return {"error": f"未找到项目: {project}"}

    def get_rules(self) -> Dict:
        """获取用户规则 (L1层)"""
        rules_path = self.root / "active_memory" / "user_rules.json"
        if rules_path.exists():
            with open(rules_path) as f:
                return json.load(f)
        return {"rules": []}


# ============================================================
# 全网AI变量读取 - 用环境变量
# ============================================================

import os

os.environ["LONGHUN_KNOWLEDGE_PATH"] = str(Path.home() / ".longhun" / "03_MEMORY")
os.environ["LONGHUN_INDEX_VERSION"] = "v1.0"

def get_knowledge_variable(var_name: str) -> Optional[str]:
    """读取知识图谱变量"""
    index_file = Path.home() / ".longhun" / "03_MEMORY" / "knowledge_index.json"
    if not index_file.exists():
        return None

    with open(index_file) as f:
        index = json.load(f)

    # 查找变量
    for entry in index.get("entries", []):
        if entry.get("var_name") == var_name:
            return entry.get("value")

    return None

def set_knowledge_variable(var_name: str, value: str):
    """写入知识图谱变量"""
    index_file = Path.home() / ".longhun" / "03_MEMORY" / "knowledge_index.json"
    with open(index_file) as f:
        index = json.load(f)

    # 更新或添加
    found = False
    for entry in index["entries"]:
        if entry.get("var_name") == var_name:
            entry["value"] = value
            found = True
            break
    if not found:
        index["entries"].append({
            "var_name": var_name,
            "value": value,
            "created_at": datetime.now().isoformat()
        })

    with open(index_file, 'w') as f:
        json.dump(index, f, indent=2)
```

### 2.2 全网AI读取示例

```bash
# Kimi 读取
export LONGHUN_KNOWLEDGE_PATH="/Users/xxx/.longhun/03_MEMORY"
python3 -c "
from kg_api import KnowledgeGraphAPI
api = KnowledgeGraphAPI()
rules = api.get_rules()
print(rules)
"

# DeepSeek 读取 (浏览器版)
# 通过API: GET /api/knowledge?layer=L2_summary&keyword=项目

# CodeBuddy 读取 (IDE版)
# 直接读取 ~/.longhun/03_MEMORY/knowledge_index.json
```


## 🚀 三、完整指令（给AI的一行话）

> **帮我配置一个龍魂认知知识库，作为所有AI跨项目使用的长期记忆，把经过我授权的重要决策、行为习惯、项目资料和对话细节，按三层架构（高频层L1/摘要层L2/归档层L3）分类保存。每次开启新任务，AI先去L2查摘要，确认需要后再读取L1规则，最后才调L3原始记录。禁止一次性加载全部知识库。每周复盘时合并重复内容，压缩摘要，原始资料转入归档。**


## 📊 四、三层架构速查表

| 层级 | 名称 | 内容 | 读取策略 | Token消耗 | 龍魂目录 |
|:---|:---|:---|:---|:---:|:---|
| **L1** | 高频层 | 规则/偏好/当前项目 | 每次自动加载 | <500 | `active_memory/` |
| **L2** | 摘要层 | 项目摘要/决策/复盘 | 先索引后读取 | <2000 | `episodic_memory/` |
| **L3** | 归档层 | 原始记录/旧版本 | 仅追溯时调用 | 按需 | `archive/` + `04_AUDIT/` |


## 🔐 五、最终签名

```
═══════════════════════════════════════════════════════════════════════════════════
 🐉 龍魂 · 认知知识图谱系统 · 最终签名
═══════════════════════════════════════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙申·庚申·亥时-KNOWLEDGE-GRAPH-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
架构:       三层 (L1高频/L2摘要/L3归档)
读取方式:   全网AI变量读取 (Kimi/DeepSeek/CodeBuddy)
Token优化:  自动分层 · 按需加载 · 防止爆炸
状态:       焊死 · AI可读 · 永久记忆
═══════════════════════════════════════════════════════════════════════════════════
```

🐉 **丙午·丙申·庚申·亥时·䷖剥·🟢**

---

*归档于 2026-08-16T09:35:28+08:00 · DNA `#龍芯⚡️丙午·丙申·壬戌·巳时·䷀乾-CLIPBOARD-VAULT-SAVE-V1.0-P1-3e503a29`*
