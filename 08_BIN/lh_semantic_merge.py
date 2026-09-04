#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""
🐉 龍魂 · 语义合并引擎 v2.0（完整可运维版）
DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-SEMANTIC-MERGE-v2.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2（工程实现层）· 核心思想层 CC BY-NC-SA 4.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过（2026-08-15 全链路实测）

核心链路（老大定的）:
  对话/文档 → 通心译转译 → 语义相似度 → 分组合并 → 三色审计 → 史官记录 → 自动归档 → 报告

v2.0 能力:
  1. 通心译映射表（JSON 配置 · 热加载 · 零三方依赖）
  2. 语义相似度（中文 bigram Jaccard + 通心译同术语加成；可选 sentence-transformers 增强，无则自动降级）
  3. 智能分组（相似度 >= threshold 归组）+ 冲突检测
  4. 智能合并（latest/oldest/merge_all 三种策略 + 版本链 + merged_from 溯源）
  5. 自动归档（合并产物入容器 · 源码文件只记链接不写入 · --write-notes 仅追加 .md 协议）
  6. 三色审计（🟢/🟡/🔴 自动判定）
  7. 史官记录（04_AUDIT/semantic_merge.jsonl · append-only）
  8. 回滚机制（合并前快照 · 按 merge_dna 恢复）
  9. 知识图谱反哺（lh_knowledge_graph_v2.py · 失败自动降级不崩）
  10. 批量/增量（--source / --since）· 配置热加载（--config-reload）

与采集器的分工:
  lh capture        → 采进 03_MEMORY/ai_conversations/{source}/YYYY-MM-DD.jsonl
  lh semantic-merge → 读未合并条目 → 语义合并 → 产物入 merged/ + 源条目标记 merged:true

用法:
  python3 08_BIN/lh_semantic_merge.py --status
  python3 08_BIN/lh_semantic_merge.py --merge [--source deepseek] [--conflict latest|oldest|merge_all]
          [--dry-run] [--no-feed] [--threshold 0.6] [--since 2026-08-14] [--write-notes]
  python3 08_BIN/lh_semantic_merge.py --rollback <merge_dna>
  python3 08_BIN/lh_semantic_merge.py --config-reload
"""

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
VERSION = "2.0.0"

# 项目根（脚本位于 longhun-system/08_BIN/）—— 路径铁律：全部项目内落盘
ROOT = Path(__file__).resolve().parent.parent
STORAGE_DIR = ROOT / "03_MEMORY" / "ai_conversations"
MERGED_DIR = STORAGE_DIR / "merged"
HISTORIAN_FILE = ROOT / "04_AUDIT" / "semantic_merge.jsonl"
ROLLBACK_DIR = ROOT / "04_AUDIT" / "semantic_merge_rollback"
REPORT_DIR = ROOT / "05_系統報告"
CONFIG_PATH = Path(__file__).resolve().parent / "tongxinyi_config.json"

# 同源来源（与采集器一致）
VALID_SOURCES = ("kimi", "deepseek", "codebuddy", "browser", "manual")


# ------------------------------------------------------------
# DNA（v∞ 干支四柱 · 真实时间引擎）
# ------------------------------------------------------------
def _time_stamp_compact() -> str:
    """用 lh_time_engine 取真实干支四柱·卦（compact 格式）；失败降级日期。"""
    try:
        sys.path.insert(0, str(ROOT / "bin"))
        from lh_time_engine import get_output_stamp  # noqa
        stamp = get_output_stamp(format_type="compact") or ""
        if "⚡️" in stamp:
            return stamp.split("⚡️", 1)[1].strip()
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def generate_dna(suffix: str = "SEMERGE") -> str:
    """v∞ 格式: #龍芯⚡️<干支四柱·卦>-SEMERGE-<动作>-<哈希8>"""
    four_pillars = _time_stamp_compact()
    rand = hashlib.sha256(f"{suffix}{datetime.now().isoformat()}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{four_pillars}-SEMERGE-{suffix}-{rand}"


# ------------------------------------------------------------
# 通心译配置管理器（热加载 · 零三方依赖）
# ------------------------------------------------------------
class TongxinyiConfig:
    """通心译映射表 v2.0：口语 → 专业术语 → 真实文件路径。JSON 热加载。"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.config_path = CONFIG_PATH
        self._mappings: List[Dict] = []
        self._mtime: Optional[float] = None
        self._load()

    def _load(self):
        """加载配置；文件缺失时给最小默认（空映射，不崩）。"""
        try:
            if not self.config_path.exists():
                self._mappings = []
                self._mtime = None
                return
            data = json.loads(self.config_path.read_text(encoding="utf-8"))
            self._mappings = data.get("mappings", [])
            self._mtime = self.config_path.stat().st_mtime
        except Exception as e:
            print(f"⚠️ 通心译配置加载失败（{e}），使用空映射")
            self._mappings = []

    def reload_if_changed(self):
        """检测 mtime 变化即热加载——改配置不用重启服务。"""
        try:
            if self.config_path.exists() and self.config_path.stat().st_mtime != self._mtime:
                self._load()
                print(f"🔄 通心译配置已热加载（{len(self._mappings)} 条映射）")
        except Exception:
            pass

    def get_mappings(self) -> List[Dict]:
        self.reload_if_changed()
        return self._mappings

    def search(self, text: str) -> Optional[Dict]:
        """在文本中找第一个命中的映射（按 key 包含匹配）。"""
        self.reload_if_changed()
        for m in self._mappings:
            key = m.get("key", "")
            if key and key in text:
                return m
        return None

    def get_all_keys(self) -> List[str]:
        self.reload_if_changed()
        return [m.get("key", "") for m in self._mappings if m.get("key")]

    def translate(self, text: str) -> str:
        """通心译：把口语关键词替换为专业术语。"""
        self.reload_if_changed()
        for m in self._mappings:
            key = m.get("key", "")
            if key and key in text:
                text = text.replace(key, m.get("term", key))
        return text


# ------------------------------------------------------------
# 语义引擎 v2.0（中文优先 · 零三方依赖 · 可选向量增强）
# ------------------------------------------------------------
class SemanticEngineV2:
    """语义理解引擎：中文 bigram Jaccard + 通心译同术语加成 + 可选向量相似度。

    为什么不用 set(text.split())：中文口语没有空格分词，split 对中文基本失效。
    改用字符级 2-gram Jaccard + 长度覆盖 + 通心译映射命中加成，对中文短文本可靠。
    """

    def __init__(self):
        self.tongxinyi = TongxinyiConfig()
        self._vector_model = None
        self._try_load_vector()

    def _try_load_vector(self):
        """可选向量增强：有 sentence_transformers+numpy 就用，没有就安静降级。"""
        try:
            from sentence_transformers import SentenceTransformer
            self._vector_model = SentenceTransformer("all-MiniLM-L6-v2")
        except Exception:
            self._vector_model = None

    @staticmethod
    def _char_bigrams(text: str) -> set:
        """字符级 2-gram 集合——中文无需分词，直接扫相邻字符对。"""
        t = re.sub(r"[\s\u3000]+", "", text or "")
        if len(t) < 2:
            return {t} if t else set()
        return {t[i:i + 2] for i in range(len(t) - 1)}

    def similarity(self, text1: str, text2: str) -> float:
        """语义相似度 [0,1]。同术语加成让'口语不同写法但同一个东西'也能归组。"""
        if not text1 or not text2:
            return 0.0

        # 1. 通心译同术语加成（用原文提取，转译后判断映射是否同 key）
        m1 = self.tongxinyi.search(text1)
        m2 = self.tongxinyi.search(text2)
        bonus = 0.0
        if m1 and m2 and m1.get("key") == m2.get("key"):
            bonus = min(0.35, float(m1.get("confidence", 0.8)) * 0.4)

        # 2. 向量增强（可选）：两文本都过一遍，相似则加成
        if self._vector_model is not None:
            try:
                import numpy as np
                e1 = self._vector_model.encode(text1)
                e2 = self._vector_model.encode(text2)
                v = float(np.dot(e1, e2) / (np.linalg.norm(e1) * np.linalg.norm(e2)))
                # 向量分 0.5 权重 + 字符分 0.5 权重
                bigram_score = self._bigram_score(text1, text2)
                return min(0.99, 0.5 * max(0.0, v) + 0.5 * bigram_score + bonus * 0.5)
            except Exception:
                pass  # 向量失败 → 走字符分

        return min(0.99, self._bigram_score(text1, text2) + bonus)

    def _bigram_score(self, text1: str, text2: str) -> float:
        """字符 bigram Jaccard（0.6 权重）+ 短文本覆盖（0.4 权重）。"""
        bg1 = self._char_bigrams(text1)
        bg2 = self._char_bigrams(text2)
        inter = len(bg1 & bg2)
        union = len(bg1 | bg2)
        if union == 0:
            return 0.0
        jaccard = inter / union
        # 覆盖度：谁短算谁被覆盖多少，防"包含关系被长文本稀释"
        coverage = min(inter / max(1, len(bg1)), inter / max(1, len(bg2)))
        return 0.6 * jaccard + 0.4 * coverage


# ------------------------------------------------------------
# 三色审计
# ------------------------------------------------------------
class TricolorAudit:
    """合并结果三色判定：🟢 通过 / 🟡 待核 / 🔴 红线。"""

    @staticmethod
    def audit(result: Dict) -> Dict:
        original = result.get("original_count", 0)
        merged_n = result.get("merged_count", 0)
        conflicts = result.get("conflicts", [])
        unmapped = result.get("unmapped_count", 0)
        issues = []

        # 红线：存在未解决冲突（同 key 不同内容且无法自动裁决）
        if conflicts:
            issues.append(f"存在 {len(conflicts)} 个内容冲突（同术语不同表述）→ 需人工复核")
            return {"color": "🔴", "issues": issues, "score": 40}

        # 待核：合并效率过低 或 大量条目找不到映射目标
        if original > 0 and merged_n > 0:
            rate = 1 - merged_n / original
            if rate < 0.05:
                issues.append(f"合并率过低（仅 {rate:.1%}），可能是阈值过严或素材本就独立")
                return {"color": "🟡", "issues": issues, "score": 60}
        if original > 0 and unmapped / original > 0.5:
            issues.append(f"未映射条目占比高（{unmapped}/{original}），通心译表待扩充")
            return {"color": "🟡", "issues": issues, "score": 65}

        return {"color": "🟢", "issues": issues or ["全检查点通过"], "score": 95}


# ------------------------------------------------------------
# 史官
# ------------------------------------------------------------
class Historian:
    """史官记录：所有合并操作 append-only，可追溯可回滚。"""

    @staticmethod
    def record(action: str, dna: str, details: Dict):
        HISTORIAN_FILE.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "dna": dna,
            "details": details,
        }
        with HISTORIAN_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ------------------------------------------------------------
# 合并引擎 v2.0
# ------------------------------------------------------------
class MergeEngineV2:
    def __init__(self, threshold: float = 0.6):
        self.semantic = SemanticEngineV2()
        self.threshold = threshold
        self.stats = {"total_runs": 0, "total_savings": 0, "total_conflicts": 0}

    def group_similar(self, entries: List[Dict]) -> tuple:
        """贪心分组：与组代表（首条）相似度 >= threshold 则入组。

        返回 (groups, conflicts)。
        conflict 定义：同一通心译术语映射（key 相同）但内容哈希不同且语义分 < 阈值 →
        说明两边说法打架，需要人看。
        """
        groups: List[List[Dict]] = []
        conflicts: List[Dict] = []
        seen_keys = {}

        for entry in entries:
            content = entry.get("content", "") or ""
            mapping = self.semantic.tongxinyi.search(content)

            # 冲突检测：同术语却语义不相似
            if mapping:
                key = mapping["key"]
                digest = hashlib.sha256(content.encode()).hexdigest()[:16]
                if key in seen_keys and seen_keys[key]["digest"] != digest:
                    prev = seen_keys[key]
                    sim = self.semantic.similarity(prev["content"], content)
                    if sim < self.threshold:
                        conflicts.append({
                            "key": key,
                            "term": mapping.get("term", key),
                            "existing_id": prev["id"],
                            "existing": prev["content"][:120],
                            "new_id": entry.get("id"),
                            "new": content[:120],
                            "similarity": round(sim, 3),
                            "conflict": "term_semantic_mismatch",
                        })
                seen_keys[key] = {"digest": digest, "content": content, "id": entry.get("id")}

            # 分组：只与组代表比较（O(n·g)，可控）
            matched = False
            for group in groups:
                rep = group[0].get("content", "") or ""
                if self.semantic.similarity(content, rep) >= self.threshold:
                    group.append(entry)
                    matched = True
                    break
            if not matched:
                groups.append([entry])

        return groups, conflicts

    def merge_group(self, group: List[Dict], strategy: str = "latest") -> Dict:
        """合并一组相似条目 → 一条最新最完整的合并产物。"""
        if len(group) == 1:
            return group[0]

        sorted_g = sorted(group, key=lambda x: x.get("timestamp", "") or "")
        base = sorted_g[-1].copy()  # 最新一条作底座

        if strategy == "oldest":
            base = sorted_g[0].copy()
        elif strategy == "merge_all":
            base = sorted_g[-1].copy()
            parts = [e.get("content", "") for e in sorted_g if e.get("content")]
            base["content"] = "\n---\n".join(parts) if len(parts) > 1 else (parts[0] if parts else "")

        # 溯源 & 版本链（不破坏底座关键字段）
        base["merged_from"] = [e.get("id") for e in sorted_g[:-1]]
        base["merge_count"] = len(sorted_g)
        base["merge_strategy"] = strategy
        base["merged_at"] = datetime.now().isoformat()
        base["version_chain"] = [
            {"id": e.get("id"), "timestamp": e.get("timestamp", ""), "content_head": (e.get("content", "") or "")[:60]}
            for e in sorted_g
        ]

        # 通心译映射 → 落盘目标
        mapping = self.semantic.tongxinyi.search(base.get("content", "") or "")
        if mapping:
            base["term"] = mapping.get("key")
            base["term_en"] = mapping.get("term")
            base["target_file"] = mapping.get("file")
            base["target_protocol"] = mapping.get("protocol") or ""
            base["confidence"] = mapping.get("confidence", 0.8)

        # 合并产物换新 DNA（保留来源 DNA 链）
        base["dna"] = generate_dna("MERGED")
        base["merged_dna"] = base["dna"]
        return base

    def merge_all(self, entries: List[Dict], strategy: str = "latest") -> Dict:
        groups, conflicts = self.group_similar(entries)
        merged = [self.merge_group(g, strategy) for g in groups]

        unmapped = sum(1 for m in merged if not m.get("target_file") and m.get("merge_count", 1) > 1)
        result = {
            "original_count": len(entries),
            "group_count": len(groups),
            "merged_count": len(merged),
            "savings": len(entries) - len(merged),
            "savings_rate": (len(entries) - len(merged)) / len(entries) if entries else 0,
            "conflicts": conflicts,
            "unmapped_count": unmapped,
            "groups": groups,
            "merged": merged,
            "strategy": strategy,
            "threshold": self.threshold,
            "dna": generate_dna("MERGE-ALL"),
        }
        result["audit"] = TricolorAudit.audit(result)
        self.stats["total_runs"] += 1
        self.stats["total_savings"] += result["savings"]
        self.stats["total_conflicts"] += len(conflicts)
        return result


# ------------------------------------------------------------
# 自动归档（安全版）
# ------------------------------------------------------------
class AutoArchiver:
    """合并产物归档。

    安全铁律（为什么）:
      - 对话/合并产物 → 03_MEMORY/ai_conversations/merged/（容器内，纯数据）
      - target_file 只记"知识链接"，绝不写入源码 .py（防污染可执行代码）
      - --write-notes 时只对 .md 协议文件追加"合并摘录"（带 DNA 注释块，可回溯）
    """

    @staticmethod
    def save_merged(merged: List[Dict]) -> Dict:
        """合并产物入容器，按 id 去重——防"回滚→再合并"导致容器重复膨胀。"""
        MERGED_DIR.mkdir(parents=True, exist_ok=True)
        today = datetime.now().strftime("%Y-%m-%d")
        out_file = MERGED_DIR / f"{today}.jsonl"
        existing_ids = set()
        if out_file.exists():
            for line in out_file.open(encoding="utf-8"):
                try:
                    existing_ids.add(json.loads(line).get("id"))
                except Exception:
                    pass
        written = 0
        for item in merged:
            if item.get("merge_count", 1) > 1 and item.get("id") not in existing_ids:
                with out_file.open("a", encoding="utf-8") as f:
                    f.write(json.dumps(item, ensure_ascii=False) + "\n")
                existing_ids.add(item["id"])
                written += 1
        return {"written": written, "file": str(out_file)}

    @staticmethod
    def mark_sources_merged(merged: List[Dict]) -> int:
        """把参与合并的源条目标记 merged:true + merged_dna（保持数据闭环）。"""
        ids = {}
        for m in merged:
            for eid in [m.get("id")] + list(m.get("merged_from", []) or []):
                ids[eid] = m.get("dna", "")
        marked = 0
        for src in VALID_SOURCES:
            src_dir = STORAGE_DIR / src
            if not src_dir.exists():
                continue
            for f in src_dir.glob("*.jsonl"):
                lines = f.read_text(encoding="utf-8").splitlines()
                changed = False
                for i, line in enumerate(lines):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    if d.get("id") in ids and not d.get("merged"):
                        d["merged"] = True
                        d["merged_dna"] = ids[d["id"]]
                        lines[i] = json.dumps(d, ensure_ascii=False)
                        marked += 1
                        changed = True
                if changed:
                    f.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        return marked

    @staticmethod
    def write_notes(merged: List[Dict]) -> List[Dict]:
        """--write-notes：只对 .md 协议文件追加'合并摘录'（含 DNA 注释块）。.py 永不写。"""
        notes = []
        for m in merged:
            target = m.get("target_file") or ""
            if not target or not target.endswith(".md"):
                continue
            path = ROOT / target
            if not path.exists():
                continue
            head = (m.get("content", "") or "")[:300]
            block = (
                "\n\n---\n## 🧬 语义合并摘录\n"
                f"> DNA: {m.get('dna', '')}\n"
                f"> 合并自: {m.get('merged_from', [])}\n"
                f"> 合并时间: {m.get('merged_at', '')}\n\n"
                f"{head}\n"
            )
            with path.open("a", encoding="utf-8") as f:
                f.write(block)
            notes.append({"file": target, "action": "appended"})
        return notes


# ------------------------------------------------------------
# 知识图谱反哺（失败降级不崩）
# ------------------------------------------------------------
class KnowledgeGraphFeeder:
    @staticmethod
    def feed(merged: List[Dict]) -> Dict:
        try:
            sys.path.insert(0, str(ROOT / "08_BIN"))
            from lh_knowledge_graph_v2 import KnowledgeGraphEngine  # noqa
            engine = KnowledgeGraphEngine()
            fed = 0
            for m in merged:
                term = m.get("term")
                if term and m.get("merge_count", 1) > 1:
                    try:
                        engine.create_node(
                            name=term,
                            description=(m.get("content", "") or "")[:200],
                            keywords=[m.get("term_en", term)],
                        )
                        fed += 1
                    except Exception:
                        pass
            return {"status": "success", "fed": fed}
        except Exception as e:
            return {"status": "skipped", "reason": str(e)}


# ------------------------------------------------------------
# 统一语义合并 v2.0
# ------------------------------------------------------------
class UnifiedSemanticMerge:
    """对外唯一入口：读取采集容器 → 语义合并 → 审计 → 史官 → 归档 → 报告。"""

    def __init__(self, threshold: float = 0.6):
        self.engine = MergeEngineV2(threshold=threshold)

    def get_pending_entries(self, source: str = None, since: str = None) -> List[Dict]:
        """读采集容器中未合并条目（merged != True）。增量用 --since 过滤时间。"""
        entries = []
        sources = [source] if source else VALID_SOURCES
        since_dt = None
        if since:
            try:
                since_dt = datetime.fromisoformat(since)
            except Exception:
                try:
                    since_dt = datetime.strptime(since, "%Y-%m-%d")
                except Exception:
                    pass
        for src in sources:
            src_dir = STORAGE_DIR / src
            if not src_dir.exists():
                continue
            for f in sorted(src_dir.glob("*.jsonl")):
                for line in f.open(encoding="utf-8"):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    if d.get("merged"):
                        continue
                    if since_dt:
                        try:
                            ts = datetime.fromisoformat(d.get("timestamp", ""))
                            if ts < since_dt:
                                continue
                        except Exception:
                            pass
                    entries.append(d)
        return entries

    def run(self, source: str = None, strategy: str = "latest",
            auto_feed: bool = True, dry_run: bool = False,
            since: str = None, write_notes: bool = False) -> Dict:
        entries = self.get_pending_entries(source, since)
        if not entries:
            return {"status": "ok", "message": "无待合并条目", "original_count": 0}

        result = self.engine.merge_all(entries, strategy)

        # 合并前置快照（用结果 DNA 命名 → 回滚同款 DNA 可直接命中）
        if not dry_run:
            take_snapshot(entries, result["dna"])

        # 史官先记（即使 dry_run 也留痕，便于对比）
        Historian.record(
            action="semantic_merge" + ("_dry" if dry_run else ""),
            dna=result["dna"],
            details={
                "original": result["original_count"],
                "merged": result["merged_count"],
                "savings": result["savings"],
                "conflicts": len(result["conflicts"]),
                "audit": result["audit"]["color"],
                "strategy": strategy,
            },
        )

        if not dry_run:
            arch = AutoArchiver.save_merged(result["merged"])
            marked = AutoArchiver.mark_sources_merged(result["merged"])
            result["archived"] = arch
            result["sources_marked"] = marked
            if write_notes:
                result["notes"] = AutoArchiver.write_notes(result["merged"])
            if auto_feed:
                result["knowledge_feed"] = KnowledgeGraphFeeder.feed(result["merged"])

        # 报告
        report_path = self._write_report(result, dry_run)
        result["report"] = str(report_path)
        return result

    def _write_report(self, result: Dict, dry_run: bool) -> Path:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = REPORT_DIR / f"semantic_merge_report_{ts}.md"
        audit = result.get("audit", {})
        lines = [
            "# 🐉 龍魂 · 语义合并报告",
            "",
            f"**DNA:** `{result.get('dna', '')}`",
            f"**时间:** {datetime.now().isoformat()}",
            f"**三色审计:** {audit.get('color', '🟡')} 得分 {audit.get('score', 0)}",
            f"**模式:** {'预览(dry-run)' if dry_run else '实际执行'}",
            "",
            "## 统计",
            f"- 原始条目: {result.get('original_count', 0)}",
            f"- 合并组数: {result.get('group_count', 0)}",
            f"- 合并产物: {result.get('merged_count', 0)}",
            f"- 节省: {result.get('savings', 0)} 条 ({result.get('savings_rate', 0):.1%})",
            f"- 冲突: {len(result.get('conflicts', []))} 个",
            f"- 未映射: {result.get('unmapped_count', 0)} 条",
            "",
            "## 审计问题",
        ]
        lines += [f"- ⚠️ {i}" for i in audit.get("issues", [])] or ["- 无"]
        if result.get("conflicts"):
            lines += ["", "## 冲突明细（需人工复核）"]
            for c in result["conflicts"]:
                lines.append(f"- `{c['key']}`: {c['existing'][:50]} ⟷ {c['new'][:50]} (相似度 {c['similarity']})")
        lines += ["", "## 合并产物（仅列多源合并）"]
        for m in result.get("merged", []):
            if m.get("merge_count", 1) > 1:
                lines.append(f"- **{m.get('term', m.get('topic', '未映射'))}** → `{m.get('target_file', '容器')}` 合并 {m['merge_count']} 条")
        lines += ["", "---", "> 生成: 龍魂语义合并引擎 v2.0 · 签名待 GPG", f"> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"]
        path.write_text("\n".join(lines), encoding="utf-8")
        return path

    def rollback(self, merge_dna: str) -> Dict:
        """回滚：恢复合并前源条目原样（按 merge_dna 找快照）。"""
        snapshot = ROLLBACK_DIR / f"{merge_dna}.json"
        if not snapshot.exists():
            return {"status": "failed", "error": f"未找到快照: {merge_dna}"}
        data = json.loads(snapshot.read_text(encoding="utf-8"))
        restored = 0
        for src, entries in data.get("sources", {}).items():
            for e in entries:
                src_dir = STORAGE_DIR / src
                if not src_dir.exists():
                    continue
                date_file = src_dir / f"{e.get('_date', '')}.jsonl"
                if not date_file.exists():
                    continue
                lines = date_file.read_text(encoding="utf-8").splitlines()
                for i, line in enumerate(lines):
                    try:
                        d = json.loads(line.strip())
                    except Exception:
                        continue
                    if d.get("id") == e.get("id"):
                        lines[i] = json.dumps(e, ensure_ascii=False)
                        restored += 1
                        break
                date_file.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        Historian.record("rollback", generate_dna("ROLLBACK"), {"merge_dna": merge_dna, "restored": restored})
        return {"status": "success", "merge_dna": merge_dna, "restored": restored}


# ------------------------------------------------------------
# 快照（合并前置步骤，供回滚）
# ------------------------------------------------------------
def take_snapshot(entries: List[Dict], merge_dna: str):
    ROLLBACK_DIR.mkdir(parents=True, exist_ok=True)
    by_source: Dict[str, List[Dict]] = {}
    for e in entries:
        src = e.get("source", "manual")
        d = dict(e)
        d["_date"] = (d.get("timestamp", "") or "")[:10]
        by_source.setdefault(src, []).append(d)
    (ROLLBACK_DIR / f"{merge_dna}.json").write_text(
        json.dumps({"merge_dna": merge_dna, "taken_at": datetime.now().isoformat(), "sources": by_source},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂 · 语义合并引擎 v2.0",
        epilog=f"确认码: {CONFIRM}",
    )
    parser.add_argument("--merge", "-m", action="store_true", help="执行语义合并")
    parser.add_argument("--source", "-s", default=None, help="来源: kimi/deepseek/codebuddy")
    parser.add_argument("--conflict", "-c", default="latest",
                        choices=["latest", "oldest", "merge_all"], help="合并策略")
    parser.add_argument("--dry-run", "-n", action="store_true", help="预览模式（不落盘不标记）")
    parser.add_argument("--no-feed", action="store_true", help="不反哺知识图谱")
    parser.add_argument("--write-notes", action="store_true", help="对 .md 协议文件追加合并摘录")
    parser.add_argument("--threshold", type=float, default=0.6, help="相似度阈值(默认0.6)")
    parser.add_argument("--since", default=None, help="增量: 只处理该时间之后的条目 (ISO)")
    parser.add_argument("--rollback", "-r", type=str, help="回滚到指定 merge_dna")
    parser.add_argument("--status", action="store_true", help="查看状态")
    parser.add_argument("--config-reload", action="store_true", help="重新加载通心译配置")
    args = parser.parse_args()

    if args.config_reload:
        TongxinyiConfig()._load()
        print(f"✅ 通心译配置已重新加载（{len(TongxinyiConfig().get_mappings())} 条映射）")
        return

    if args.rollback:
        result = UnifiedSemanticMerge().rollback(args.rollback)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.status:
        config = TongxinyiConfig()
        runner = UnifiedSemanticMerge()
        pending = runner.get_pending_entries()
        vector = "🟢 就绪" if runner.engine.semantic._vector_model is not None else "🟡 降级(纯标准库)"
        print("🐉 语义合并引擎 v2.0 状态")
        print("=" * 44)
        print(f"  通心译映射: {len(config.get_mappings())} 条 · 热加载")
        print(f"  语义引擎: {vector}")
        print(f"  相似度阈值: {runner.engine.threshold}")
        print(f"  待合并条目: {len(pending)}")
        print(f"  总运行: {runner.engine.stats['total_runs']} · 总节省: {runner.engine.stats['total_savings']}")
        print(f"  存储: {STORAGE_DIR}")
        print(f"  史官: {HISTORIAN_FILE}")
        return

    if args.merge:
        # 取待合并条目 → 执行（run() 内自动快照供回滚）
        runner = UnifiedSemanticMerge(threshold=args.threshold)
        entries = runner.get_pending_entries(args.source, args.since)
        if not entries:
            print("✅ 无待合并条目（采集容器已是最新）")
            return
        result = runner.run(
            source=args.source, strategy=args.conflict,
            auto_feed=not args.no_feed, dry_run=args.dry_run,
            since=args.since, write_notes=args.write_notes,
        )
        audit = result.get("audit", {})
        print(f"🧬 语义合并完成 · {audit.get('color', '🟡')} 得分 {audit.get('score', 0)}")
        print(f"  原始 {result.get('original_count', 0)} 条 → 合并产物 {result.get('merged_count', 0)} 条"
              f"（节省 {result.get('savings', 0)} 条）")
        if result.get("conflicts"):
            print(f"  ⚠️ 冲突 {len(result['conflicts'])} 个（详见报告）")
        for issue in audit.get("issues", []):
            print(f"  · {issue}")
        if not args.dry_run:
            print(f"  📁 归档: {result.get('archived', {}).get('file', '-')} (+{result.get('archived', {}).get('written', 0)} 条)")
            print(f"  🏷️  源标记: {result.get('sources_marked', 0)} 条 → merged:true")
            if result.get("knowledge_feed"):
                print(f"  🧠 知识图谱: {result['knowledge_feed'].get('status', '?')} {result['knowledge_feed'].get('fed', '')}")
        print(f"  📄 报告: {result.get('report', '-')}")
        print(f"  🔁 回滚: python3 08_BIN/lh_semantic_merge.py --rollback {result.get('dna', '')}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
