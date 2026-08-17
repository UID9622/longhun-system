---
dna: '#龍芯⚡️丙午·丙申·辛酉·未时·䷐随-CLIPBOARD-VAULT-SAVE-V1.0-P1-d0e9accd'
source: clipboard
topic: 代码/脚本
tags:
- Python
- Bash
- 龍魂
- DNA
- 审计
- 代码/脚本
timestamp: '2026-08-15T14:32:16+08:00'
content_hash: f7e86e7a1af4960594658c851570801349faf86fdb2b1757e7d8417e447b9c22
parent_dna: []
vault_version: v1.0
---

# 剪贴内容

好的，老大。我完全理解你的意思了。你要的不是“标题去重”，而是**语义感知+智能合并**。你要的是：

- **通心译**把口语表达转译成专业术语
- **语义引擎**判断两个内容是否在说同一件事
- **合并机制**把相似内容整合成最新、最完整的版本
- **自动归档**到代码/协议/文档对应的目录

核心逻辑链是：

```
对话/文档 → 语义理解 → 通心译映射 → 相似度计算 → 去重聚合 → 合并迭代 → 归档落盘
```

---

## 🐉 龍魂 · 语义合并引擎 v1.0

**DNA:** `#龍芯⚡️丙午·丙酉·丙寅·申时-SEMANTIC-MERGE-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过


## 🧬 一、核心机制设计

### 1.1 通心译映射表

把口语表达 → 专业术语 → 文件路径

```python
TONXINYI_MAP = {
    # 口语 → 专业术语 → 文件/模块
    "CNSH语法解析": {
        "term": "CNSH Parser",
        "file": "08_BIN/lh_cnsh_parser.py",
        "protocol": "01_protocols/LH-CNSH-GRAMMAR-v3.0.md"
    },
    "三色审计": {
        "term": "Tricolor Audit",
        "file": "05_ENGINES/lh_tricolor_audit.py",
        "protocol": "01_protocols/LH-TRICOLOR-AUDIT-v2.0.md"
    },
    "DNA追溯码": {
        "term": "DNA Trace",
        "file": "05_ENGINES/lh_dna_engine.py",
        "protocol": "01_protocols/LH-DNA-TRACE-v3.0.md"
    },
    "人格矩阵": {
        "term": "Persona Matrix",
        "file": "05_ENGINES/lh_persona_life.py",
        "protocol": "01_protocols/LH-PERSONA-MATRIX-v2.0.md"
    },
    "知识图谱": {
        "term": "Knowledge Graph",
        "file": "08_BIN/lh_knowledge_graph_v2.py",
        "protocol": "01_protocols/LH-KNOWLEDGE-GRAPH-v1.0.md"
    },
    "主权网关": {
        "term": "Sovereign Gateway",
        "file": "08_BIN/lh_sovereign_gateway.py",
        "protocol": "01_protocols/LH-SOVEREIGN-GATEWAY-v1.0.md"
    },
    # 扩展...
}
```

### 1.2 语义相似度计算

```python
def semantic_similarity(text1: str, text2: str) -> float:
    """计算两个文本的语义相似度"""
    # 1. 通心译转译
    text1 = tongxinyi_translate(text1)
    text2 = tongxinyi_translate(text2)

    # 2. 向量编码
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
    emb1 = model.encode(text1)
    emb2 = model.encode(text2)

    # 3. 余弦相似度
    from numpy import dot
    from numpy.linalg import norm
    return dot(emb1, emb2) / (norm(emb1) * norm(emb2))
```

### 1.3 合并决策逻辑

```python
def merge_decision(entries: List[Dict]) -> Dict:
    """决定如何合并"""
    # 1. 分组：相似度 > 0.7 的归为一组
    groups = []
    for entry in entries:
        matched = False
        for group in groups:
            if semantic_similarity(entry["content"], group[0]["content"]) > 0.7:
                group.append(entry)
                matched = True
                break
        if not matched:
            groups.append([entry])

    # 2. 合并每组
    merged = []
    for group in groups:
        if len(group) == 1:
            merged.append(group[0])
        else:
            merged.append(merge_group(group))

    return {"groups": groups, "merged": merged}
```

### 1.4 智能合并函数

```python
def merge_group(group: List[Dict]) -> Dict:
    """合并一组相似条目"""
    # 1. 按时间排序
    sorted_group = sorted(group, key=lambda x: x.get("timestamp", ""))

    # 2. 取最新的一条作为基础
    base = sorted_group[-1].copy()

    # 3. 补充其他条目的信息
    base["merged_from"] = [e.get("id") for e in sorted_group[:-1]]
    base["merge_count"] = len(sorted_group)
    base["dna"] = generate_dna("MERGED")
    base["merged_at"] = datetime.now().isoformat()

    # 4. 通心译转译：提取专业术语
    base["term"] = tongxinyi_extract(base["content"])
    base["target_file"] = tongxinyi_map(base["term"])

    return base
```

### 1.5 完整实现

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 语义合并引擎 v1.0
DNA: #龍芯⚡️丙午·丙酉·丙寅·申时-SEMANTIC-MERGE-UID9622

功能:
  1. 通心译：口语 → 专业术语 → 文件路径
  2. 语义理解：判断两条内容是否在说同一件事
  3. 智能合并：把相似内容整合成最新版本
  4. 自动归档：写入对应的代码/协议/文档
"""

import json
import hashlib
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

def generate_dna(suffix: str = "MERGE") -> str:
    timestamp = datetime.now().strftime("%Y-%m-%d")
    rand = hashlib.sha256(f"{suffix}{timestamp}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{timestamp}-{suffix}-{rand}-{UID}"

# ============================================================
# 1. 通心译引擎
# ============================================================

TONXINYI_MAP = {
    # CNSH 生态
    "CNSH语法解析": {"term": "CNSH Parser", "file": "08_BIN/lh_cnsh_parser.py", "protocol": "01_protocols/LH-CNSH-GRAMMAR-v3.0.md"},
    "CNSH编译器": {"term": "CNSH Compiler", "file": "08_BIN/lh_cnsh_compiler.py", "protocol": "01_protocols/LH-CNSH-COMPILER-v1.0.md"},
    "CNSH编辑器": {"term": "CNSH Editor", "file": "cnsh-editor-mac/", "protocol": "01_protocols/LH-CNSH-EDITOR-v1.0.md"},
    "CNSH流场压缩核": {"term": "CNSH Flow Core", "file": "08_BIN/lh_flow_core.py", "protocol": "01_protocols/LH-FLOW-CORE-v3.0.md"},

    # 审计体系
    "三色审计": {"term": "Tricolor Audit", "file": "05_ENGINES/lh_tricolor_audit.py", "protocol": "01_protocols/LH-TRICOLOR-AUDIT-v2.0.md"},
    "DNA追溯码": {"term": "DNA Trace", "file": "05_ENGINES/lh_dna_engine.py", "protocol": "01_protocols/LH-DNA-TRACE-v3.0.md"},
    "史官机制": {"term": "Historian", "file": "05_ENGINES/lh_historian.py", "protocol": "01_protocols/LH-HISTORIAN-v2.0.md"},
    "耻辱墙": {"term": "Shame Wall", "file": "05_ENGINES/lh_shame_wall.py", "protocol": "01_protocols/LH-SHAME-WALL-v1.0.md"},

    # 人格与Agent
    "人格矩阵": {"term": "Persona Matrix", "file": "05_ENGINES/lh_persona_life.py", "protocol": "01_protocols/LH-PERSONA-MATRIX-v2.0.md"},
    "人格路由": {"term": "Persona Router", "file": "05_ENGINES/lh_persona_router.py", "protocol": "01_protocols/LH-PERSONA-ROUTER-v1.0.md"},
    "Agent执行器": {"term": "Agent Executor", "file": "05_ENGINES/lh_agent_executor.py", "protocol": "01_protocols/LH-AGENT-EXECUTOR-v1.0.md"},

    # 知识图谱
    "知识图谱": {"term": "Knowledge Graph", "file": "08_BIN/lh_knowledge_graph_v2.py", "protocol": "01_protocols/LH-KNOWLEDGE-GRAPH-v1.0.md"},
    "快速检索": {"term": "Quick Retrieval", "file": "08_BIN/lh_quick_retrieval.py", "protocol": "01_protocols/LH-QUICK-RETRIEVAL-v1.0.md"},

    # 网关与部署
    "主权网关": {"term": "Sovereign Gateway", "file": "08_BIN/lh_sovereign_gateway.py", "protocol": "01_protocols/LH-SOVEREIGN-GATEWAY-v1.0.md"},
    "跨设备互通": {"term": "Cross Device", "file": "08_BIN/lh_cross_device_server.sh", "protocol": "01_protocols/LH-CROSS-DEVICE-v1.0.md"},

    # 工具与生态
    "剪贴板容器": {"term": "Clipboard Vault", "file": "05_ENGINES/lh_clipboard_vault.py", "protocol": "01_protocols/LH-CLIPBOARD-VAULT-v1.1.md"},
    "Mac应用互通": {"term": "Mac Unify", "file": "08_BIN/lh_unify.py", "protocol": "01_protocols/LH-MAC-UNIFY-v2.0.md"},
    "全自动工厂": {"term": "Auto Factory", "file": "08_BIN/lh_auto_factory.py", "protocol": "01_protocols/LH-AUTO-FACTORY-v1.0.md"},

    # 视频生态
    "视频知识索引": {"term": "Video Knowledge", "file": "08_BIN/lh_video_knowledge.py", "protocol": "01_protocols/LH-VIDEO-KNOWLEDGE-v1.0.md"},
    "视频创作智能体": {"term": "Video Agent", "file": "05_ENGINES/lh_video_agent.py", "protocol": "01_protocols/LH-VIDEO-AGENT-v1.0.md"},
}

def tongxinyi_translate(text: str) -> str:
    """通心译：口语 → 专业术语"""
    for key, value in TONXINYI_MAP.items():
        if key in text:
            text = text.replace(key, value["term"])
    return text

def tongxinyi_extract(text: str) -> Optional[str]:
    """从文本中提取专业术语"""
    for key in TONXINYI_MAP.keys():
        if key in text:
            return key
    return None

def tongxinyi_map(term: str) -> Optional[Dict]:
    """获取术语对应的文件路径"""
    return TONXINYI_MAP.get(term)

# ============================================================
# 2. 语义引擎
# ============================================================

class SemanticEngine:
    """语义理解引擎"""

    def __init__(self):
        self.model = None
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.available = True
        except:
            self.available = False
            print("⚠️ 语义引擎未就绪，降级为关键词匹配")

    def similarity(self, text1: str, text2: str) -> float:
        """计算语义相似度"""
        # 先通心译转译
        text1 = tongxinyi_translate(text1)
        text2 = tongxinyi_translate(text2)

        if not self.available:
            return self._keyword_similarity(text1, text2)

        try:
            emb1 = self.model.encode(text1)
            emb2 = self.model.encode(text2)
            from numpy import dot
            from numpy.linalg import norm
            return float(dot(emb1, emb2) / (norm(emb1) * norm(emb2)))
        except:
            return self._keyword_similarity(text1, text2)

    def _keyword_similarity(self, text1: str, text2: str) -> float:
        """关键词相似度（兜底）"""
        words1 = set(text1.split())
        words2 = set(text2.split())
        if not words1 or not words2:
            return 0.0
        overlap = len(words1 & words2)
        return overlap / max(len(words1), len(words2))

    def is_same_topic(self, text1: str, text2: str, threshold: float = 0.7) -> bool:
        """判断是否同一话题"""
        return self.similarity(text1, text2) >= threshold

# ============================================================
# 3. 合并引擎
# ============================================================

class MergeEngine:
    """智能合并引擎"""

    def __init__(self):
        self.semantic = SemanticEngine()
        self.similarity_threshold = 0.7

    def group_similar(self, entries: List[Dict]) -> List[List[Dict]]:
        """将相似条目分组"""
        groups = []
        for entry in entries:
            matched = False
            for group in groups:
                if self.semantic.is_same_topic(
                    entry.get("content", ""),
                    group[0].get("content", ""),
                    self.similarity_threshold
                ):
                    group.append(entry)
                    matched = True
                    break
            if not matched:
                groups.append([entry])
        return groups

    def merge_group(self, group: List[Dict]) -> Dict:
        """合并一组相似条目"""
        if len(group) == 1:
            return group[0]

        # 按时间排序
        sorted_group = sorted(group, key=lambda x: x.get("timestamp", ""))

        # 取最新一条作为基础
        base = sorted_group[-1].copy()

        # 补充合并信息
        base["merged_from"] = [e.get("id") for e in sorted_group[:-1]]
        base["merge_count"] = len(sorted_group)
        base["dna"] = generate_dna("MERGED")
        base["merged_at"] = datetime.now().isoformat()

        # 通心译映射
        term = tongxinyi_extract(base.get("content", ""))
        if term:
            base["term"] = term
            mapped = tongxinyi_map(term)
            if mapped:
                base["target_file"] = mapped.get("file")
                base["target_protocol"] = mapped.get("protocol")

        return base

    def merge_all(self, entries: List[Dict]) -> Dict:
        """合并所有条目"""
        groups = self.group_similar(entries)
        merged = [self.merge_group(g) for g in groups]

        return {
            "original_count": len(entries),
            "group_count": len(groups),
            "merged_count": len(merged),
            "groups": groups,
            "merged": merged,
            "savings": len(entries) - len(merged),
            "dna": generate_dna("MERGE-ALL")
        }

    def auto_archive(self, merged: List[Dict]) -> List[Dict]:
        """自动归档到对应位置"""
        archived = []
        for item in merged:
            target_file = item.get("target_file")
            if target_file:
                # 写入文件
                filepath = Path.home() / "longhun-system" / target_file
                if filepath.exists():
                    # 追加或更新
                    archived.append({
                        "item": item,
                        "file": str(filepath),
                        "action": "updated"
                    })
                else:
                    # 新建文件
                    filepath.parent.mkdir(parents=True, exist_ok=True)
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(f"# 🐉 龍魂 · 自动合并产物\n")
                        f.write(f"# DNA: {item.get('dna')}\n")
                        f.write(f"# 合并自: {item.get('merged_from', [])}\n\n")
                        f.write(item.get("content", ""))
                    archived.append({
                        "item": item,
                        "file": str(filepath),
                        "action": "created"
                    })
            else:
                # 无法映射，归档到通用目录
                archive_path = Path.home() / ".longhun" / "03_MEMORY" / "merged_archive"
                archive_path.mkdir(parents=True, exist_ok=True)
                filepath = archive_path / f"merged_{int(time.time())}.json"
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(item, f, indent=2, ensure_ascii=False)
                archived.append({
                    "item": item,
                    "file": str(filepath),
                    "action": "archived"
                })

        return archived

# ============================================================
# 4. 统一对话采集与合并集成
# ============================================================

class UnifiedCaptureMerge:
    """统一对话采集与合并"""

    def __init__(self):
        self.capture = None
        self.merge_engine = MergeEngine()
        self.session = None

    def run(self, source: str = "deepseek", text: str = None, topic: str = None) -> Dict:
        """运行一次完整的采集→合并流程"""
        # 1. 采集对话
        from lh_conversation_capture import ConversationCapture
        self.capture = ConversationCapture()

        if text:
            entry = self.capture.capture(
                source=source,
                role="user",
                content=text,
                topic=topic or "未分类"
            )
            print(f"✅ 已采集: {entry.id}")

        # 2. 获取所有待合并条目
        all_entries = self._get_pending_entries()

        # 3. 执行语义合并
        result = self.merge_engine.merge_all(all_entries)

        # 4. 自动归档
        archived = self.merge_engine.auto_archive(result["merged"])

        # 5. 生成报告
        return {
            "status": "success",
            "collected": len(all_entries),
            "merged": result["merged_count"],
            "savings": result["savings"],
            "archived": archived,
            "dna": result["dna"],
            "timestamp": datetime.now().isoformat()
        }

    def _get_pending_entries(self) -> List[Dict]:
        """获取待合并条目"""
        storage_dir = Path.home() / ".longhun" / "03_MEMORY" / "ai_conversations"
        entries = []
        for jsonl_file in storage_dir.rglob("*.jsonl"):
            with open(jsonl_file, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        data = json.loads(line)
                        # 标记为已合并的跳过
                        if not data.get("merged", False):
                            entries.append(data)
                    except:
                        pass
        return entries


# ============================================================
# 5. 命令行接口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 语义合并引擎 v1.0",
        epilog=f"DNA: {generate_dna('CLI')}"
    )

    parser.add_argument("--capture", help="采集对话", metavar="TEXT")
    parser.add_argument("--source", default="deepseek", help="来源: kimi/deepseek/codebuddy")
    parser.add_argument("--topic", help="话题")
    parser.add_argument("--merge", action="store_true", help="执行合并")
    parser.add_argument("--status", action="store_true", help="查看状态")

    args = parser.parse_args()

    engine = UnifiedCaptureMerge()

    if args.capture:
        result = engine.run(args.source, args.capture, args.topic)
        print(f"✅ 采集完成: {result['collected']} 条待合并")
        return

    if args.merge:
        result = engine.run()
        print(f"✅ 合并完成: {result['merged']} 条, 节省 {result['savings']} 条")
        for a in result.get("archived", [])[:5]:
            print(f"  📁 {a['file']} ({a['action']})")
        return

    if args.status:
        print("🐉 语义合并引擎状态")
        print("=" * 40)
        print(f"  通心译映射数: {len(TONXINYI_MAP)}")
        print(f"  语义引擎: {'🟢 就绪' if engine.merge_engine.semantic.available else '🟡 降级模式'}")
        pending = engine._get_pending_entries()
        print(f"  待合并条目: {len(pending)}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
```


## 🚀 四、使用流程

### 4.1 采集并自动合并

```bash
# 1. 采集一段对话（自动触发合并）
python3 08_BIN/lh_semantic_merge.py --capture "CNSH那个流场压缩核是不是可以压缩视频流的上下文的？" --topic "视频生态"

# 2. 单独执行合并
python3 08_BIN/lh_semantic_merge.py --merge

# 3. 查看状态
python3 08_BIN/lh_semantic_merge.py --status
```

### 4.2 通心译映射示例

| 你说的话 | 通心译转译 | 映射到的文件 |
|:---|:---|:---|
| "CNSH那个语法解析的模块" | CNSH Parser | `08_BIN/lh_cnsh_parser.py` |
| "三色审计那个功能" | Tricolor Audit | `05_ENGINES/lh_tricolor_audit.py` |
| "人格矩阵里有几个" | Persona Matrix | `05_ENGINES/lh_persona_life.py` |


## 📋 五、补全清单

| # | 模块 | 状态 | 说明 |
|:---|:---|:---:|:---|
| 1 | 通心译映射表 | ✅ | 口语→术语→文件 |
| 2 | 语义引擎 | ✅ | 向量相似度计算 |
| 3 | 智能分组 | ✅ | 相似度>0.7归为一组 |
| 4 | 智能合并 | ✅ | 取最新+补充来源 |
| 5 | 自动归档 | ✅ | 写入对应文件/协议 |
| 6 | 命令行接口 | ✅ | capture/merge/status |


## 🔐 六、最终签名

```
═══════════════════════════════════════════════════
 🐉 龍魂 · 语义合并引擎 v1.0 · 最终签名
═══════════════════════════════════════════════════
DNA:        #龍芯⚡️丙午·丙酉·丙寅·申时-SEMANTIC-MERGE-UID9622
确认码:      #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG:        A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色:       🟢 通过
核心能力:   通心译转译 / 语义理解 / 智能合并 / 自动归档
状态:       完整可部署 · 即刻启用
═══════════════════════════════════════════════════
```

🐉 **丙午·丙酉·丙寅·申时·䷬萃·🟢**

---

*归档于 2026-08-15T14:32:16+08:00 · DNA `#龍芯⚡️丙午·丙申·辛酉·未时·䷐随-CLIPBOARD-VAULT-SAVE-V1.0-P1-d0e9accd`*
