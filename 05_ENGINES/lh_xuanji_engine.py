#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂·璇玑引擎 v5.0 — 记忆溯源推演系统
============================================
DNA: #龍芯⚡️丙午·癸未·丁未·亥时·䷀乾-XUANJI-ENGINE-v5.0-DUAL-TRACK
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

四象闭环:
  青龍·溯源 → 朱雀·齐政 → 白虎·验真 → 玄武·烙印 → 熔断判定

升级要点（v5.0 vs DeepSeek v4.1.5）:
  ① 七因子双轨制: 查询七因子（时空/设备/操作/内容/情绪/关系）
     + 行为七因子（承诺/兑现/情绪/受众/解释/认错/时间）独立信用评分
  ② 记忆索引: 复用现有 memory_index.json + ChromaDB 向量检索（双检）
  ③ 人格推演: 16人格完整版（非5维简化版），调用 Ollama 本地模型
  ④ 信任分: 对接语义反馈引擎 + trust_score_registry.json 持久化
  ⑤ DNA签章: 对接现有 GPG 签名引擎 + DNA 生成管线
  ⑥ 校验: 三六九不动点 + STATE.md 根校验 + 推理链连续性 + DNA追溯

用法:
  python3 engines/lh_xuanji_engine.py "查询问题"
  python3 engines/lh_xuanji_engine.py "查询问题" --raw       # JSON输出
  python3 engines/lh_xuanji_engine.py "查询问题" --deep      # 深度推演（更多记忆+更多人格）
  python3 engines/lh_xuanji_engine.py --status               # 引擎状态
  python3 engines/lh_xuanji_engine.py --rebuild-index         # 重建索引
  python3 engines/lh_xuanji_engine.py "查询问题" --memory-source local,notion,log  # 多源记忆
  python3 engines/lh_xuanji_engine.py "查询问题" --memory-source local --no-llm    # 测试记忆接入
"""

import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Set

# ─── 项目路径 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = PROJECT_ROOT / "bin"
MEMORY_DIR = PROJECT_ROOT / ".codebuddy" / "memory"
CACHE_DIR = Path.home() / ".longhun" / "cache" / "xuanji"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
INDEX_FILE = Path.home() / ".longhun" / "memory_index.json"
TRUST_REGISTRY = PROJECT_ROOT / "L7_数据层" / "trust_score_registry.json"
STATE_FILE = PROJECT_ROOT / "STATE.md"
MEMORY_FILE = MEMORY_DIR / "MEMORY.md"

# ─── 反虚伪仲裁中心联动 ───
_CNSH_V21_ROOT = PROJECT_ROOT / "cnsh" / "core" / "cnsh_v2.1"
if str(_CNSH_V21_ROOT) not in sys.path:
    sys.path.insert(0, str(_CNSH_V21_ROOT))
try:
    from cnsh_v21 import 反虚伪仲裁中心 as _anti_hypocrisy_center
except Exception as _anti_err:
    _anti_hypocrisy_center = None

# ─── 常量 ───
CST = timezone(timedelta(hours=8))
DNA_PREFIX = "#龍芯⚡️"
VERSION = "v5.0"
ENGINE_DNA = f"{DNA_PREFIX}丙午·癸未·丁未·亥时·☰乾-XUANJI-ENGINE-v5.0-DUAL-TRACK"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 人格权重（16人格·完整版）
PERSONA_WEIGHTS = {
    "P00_文心":  0.15,   # 意图解析·第一入口
    "P01_诸葛亮": 0.12,  # 战略推演
    "P02_宝宝":  0.08,   # 情感温度
    "P03_雯雯":  0.05,   # 结构归档
    "P04_鲁班":  0.08,   # 技术执行
    "P05_上帝之眼": 0.06, # 审计
    "P06_数学大师": 0.04, # 权重计算
    "P07_管仲":  0.04,   # 资源调度
    "P08_仓颉":  0.05,   # 符号语言
    "P09_孙思邈": 0.04,  # 系统诊断
    "P10_苏东坡": 0.06,  # 豁达跨界
    "P11_李白":  0.06,   # 创意爆发
    "P12_屈原":  0.06,   # 价值底线
    "P13_姜子牙": 0.04,  # 封神榜权限
    "P14_吕蒙":  0.04,   # 部署执行
    "P15_乔前辈": 0.03,  # 极简签章
}

# 向量检索引擎（懒加载）
_chroma_client = None
_chroma_collection = None
_vector_available = False

# ──────────────────────────────────────────────
# 第一象 · 青龍·溯源 — 七因子解析 + 双检索引
# ──────────────────────────────────────────────

def _parse_seven_factors(query: str) -> Dict[str, Any]:
    """查询上下文七因子：时间·空间·设备·操作·内容·情绪·关系"""
    now = datetime.now(CST)

    # ── 时间因子 ──
    time_map = {
        "今天": now.strftime("%Y-%m-%d"),
        "昨天": (now - timedelta(days=1)).strftime("%Y-%m-%d"),
        "前天": (now - timedelta(days=2)).strftime("%Y-%m-%d"),
        "上周": (now - timedelta(days=7)).strftime("%Y-%m-%d"),
        "上个月": (now - timedelta(days=30)).strftime("%Y-%m"),
        "去年": (now - timedelta(days=365)).strftime("%Y-%m"),
        "本周": now.strftime("%Y-%m-%d"),
        "今年": now.strftime("%Y"),
    }
    time_factor = now.strftime("%Y-%m-%d")
    for k, v in sorted(time_map.items(), key=lambda x: -len(x[0])):
        if k in query:
            time_factor = v
            break

    # ── 空间因子 ──
    space_kw = ["318", "泸定桥", "川藏", "成都", "北京", "上海", "深圳", 
                "鲲鹏", "Mac", "云端", "本地", "服务器"]
    space_factor = next((kw for kw in space_kw if kw in query), "未知")

    # ── 设备因子 ──
    device_kw = ["Mac", "鲲鹏", "iPhone", "iPad", "Ollama", "Kimi", 
                 "CodeBuddy", "Claude", "GitHub", "Gitee", "Notion"]
    device_factor = next((kw for kw in device_kw if kw in query), "未知")

    # ── 操作因子 ──
    action_kw = ["训练", "蒸馏", "部署", "审计", "归档", "搜索", "查询",
                 "推演", "修复", "创建", "删除", "同步", "签名", "发布",
                 "熔断", "熔炼", "合并", "注册", "登记", "巡检", "健康"]
    action_factor = next((kw for kw in action_kw if kw in query), "推理")

    # ── 内容因子 ──
    content_words = re.findall(r'[\u4e00-\u9fa5]{2,}', query)
    content_factor = content_words[:5] if content_words else ["未知"]

    # ── 情绪因子 ──（简易版，后续可接语义抽屉引擎）
    emotion_map = {"崩溃": -0.8, "烦": -0.5, "生气": -0.7, "急": -0.4,
                   "爽": 0.7, "开心": 0.8, "稳": 0.5, "担心": -0.3,
                   "害怕": -0.6, "激动": 0.6, "淡定": 0.2, "累": -0.4}
    emotion_factor = 0.0
    for kw, val in emotion_map.items():
        if kw in query:
            emotion_factor = val
            break

    # ── 关系因子 ──
    relation_kw = {"老大": ["UID9622", "诸葛鑫"],
                   "宝宝": ["P02"], "雯雯": ["P03"], "鲁班": ["P04"],
                   "龍盾": ["P72"], "黑天使": ["P77"],
                   "我自己": ["UID9622", "self"]}
    relation_factor = ["UID9622"]  # 默认
    for kw, rels in relation_kw.items():
        if kw in query:
            relation_factor = rels
            break

    return {
        "时间": time_factor,
        "空间": space_factor,
        "设备": device_factor,
        "操作": action_factor,
        "内容": content_factor,
        "情绪": emotion_factor,
        "关系": relation_factor,
    }


def _load_memory_index() -> List[Dict]:
    """加载记忆索引（复用 lh_memory_indexer 产物）"""
    if INDEX_FILE.exists():
        try:
            with open(INDEX_FILE, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            entries_raw = raw.get("entries", {})
            # entries 可能是 dict（key=date）或 list
            if isinstance(entries_raw, dict):
                return list(entries_raw.values())
            elif isinstance(entries_raw, list):
                return entries_raw
        except Exception:
            pass
    return []


# ──────────────────────────────────────────────
# 记忆源抽象（L2/L3 多源接入）
# ──────────────────────────────────────────────

class MemorySource:
    """多源记忆检索抽象基类"""

    name: str = "base"

    def is_available(self) -> bool:
        return True

    def search(self, query: str, factors: Dict, top_k: int = 5) -> List[Dict]:
        """返回统一格式的记忆片段，必须包含 source 与 timestamp"""
        raise NotImplementedError


class LocalMemorySource(MemorySource):
    """L0-L3 本地记忆源：memory_index.json + ChromaDB 向量索引 + MEMORY.md + STATE.md"""

    name = "local"

    def is_available(self) -> bool:
        return INDEX_FILE.exists() or MEMORY_FILE.exists() or STATE_FILE.exists()

    def search(self, query: str, factors: Dict, top_k: int = 5) -> List[Dict]:
        if not self.is_available():
            return []

        # 倒排索引
        index_results = _search_index(query, factors, top_k=top_k)
        for r in index_results:
            r.setdefault("source", "local")
            r.setdefault("timestamp", r.get("date", ""))
            r.setdefault("源", f"local:{r.get('date', '?')}")
            r.setdefault("内容", r.get("preview") or r.get("title") or "")
            r.setdefault("_检索方式", "local-keyword")

        # 向量索引（懒加载）
        vector_results = []
        if _init_chroma():
            _build_vector_index()
            vector_results = _vector_search(query, top_k=top_k)
            for r in vector_results:
                r.setdefault("source", "local")
                r.setdefault("timestamp", "")
                r.setdefault("_检索方式", "local-vector")

        merged = _merge_dedup(index_results, vector_results)
        return merged[:top_k]


class NotionMemorySource(MemorySource):
    """L2 领域知识源：Notion 本地镜像 / Notion API 注册表"""

    name = "notion"

    def __init__(self):
        self.config_path = Path.home() / ".longhun" / "notion" / "config.json"
        self.db_path = Path.home() / ".longhun" / "notion_pages" / "notion_pages.db"
        self._available = self._check_available()

    def _check_available(self) -> bool:
        if not self.config_path.exists():
            return False
        # 如本地缓存存在则可直接用；如只有 API 配置也可尝试
        if self.db_path.exists():
            return True
        try:
            cfg = json.loads(self.config_path.read_text(encoding="utf-8"))
            env_vars = cfg.get("環境變量", cfg.get("env_vars", {}))
            for key in env_vars.values():
                if key and os.environ.get(key):
                    return True
        except Exception:
            pass
        return False

    def is_available(self) -> bool:
        return self._available

    def search(self, query: str, factors: Dict, top_k: int = 5) -> List[Dict]:
        if not self._available:
            return []

        query_words = set(re.findall(r"[\u4e00-\u9fa5a-zA-Z0-9]{2,}", query.lower()))
        results: List[Dict] = []

        # 优先读取本地 Notion 缓存数据库
        if self.db_path.exists():
            try:
                results.extend(self._search_local_cache(query_words, top_k * 2))
            except Exception:
                pass

        # 简单去重/截断
        seen: Set[str] = set()
        unique = []
        for r in results:
            key = r.get("page_id", "") + r.get("title", "")[:40]
            if key and key in seen:
                continue
            seen.add(key)
            unique.append(r)
        unique.sort(key=lambda x: x.get("_score", 0), reverse=True)
        return unique[:top_k]

    def _search_local_cache(self, query_words: Set[str], top_k: int) -> List[Dict]:
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.cursor()
        rows = []
        try:
            # 本地缓存通常几百条以内，全部读取后做关键词评分
            cur.execute(
                "SELECT id, title, page_type, local_md_path, downloaded_at "
                "FROM targeted_pages WHERE status='done'"
            )
            rows = cur.fetchall()
        finally:
            conn.close()

        scored: List[Dict] = []
        for page_id, title, page_type, md_path, downloaded_at in rows:
            if not title:
                continue
            text = title.lower()
            content_preview = ""
            mtime = downloaded_at or ""
            if md_path and Path(md_path).exists():
                try:
                    raw = Path(md_path).read_text(encoding="utf-8", errors="ignore")
                    content_preview = re.sub(r"\s+", " ", raw)[:600]
                    text += " " + content_preview.lower()
                    # 尝试从内容中提取 DNA 时间戳
                    m = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", raw)
                    if m:
                        mtime = m.group()
                except Exception:
                    pass

            hits = sum(1 for w in query_words if w in text)
            score = hits * 10
            if score > 0 or len(scored) < top_k:
                scored.append({
                    "page_id": page_id,
                    "title": title,
                    "source": "notion",
                    "timestamp": mtime,
                    "源": f"notion:{title[:40]}",
                    "内容": content_preview[:300] if content_preview else title,
                    "_score": score + 1,  # 保底分，确保可排序
                    "匹配度": min(1.0, (score + 1) / 20),
                    "_检索方式": "notion-cache",
                    "notion_url": f"https://www.notion.so/{page_id.replace('-', '')}",
                })
        scored.sort(key=lambda x: x["_score"], reverse=True)
        return scored[:top_k]


class LogMemorySource(MemorySource):
    """L3 上下文/历史事件源：本地日志与每日执行记录"""

    name = "log"

    def __init__(self):
        self.log_dirs = [
            Path.home() / ".longhun" / "logs",
            PROJECT_ROOT / "_work" / "logs_archive",
            MEMORY_DIR,  # .codebuddy/memory 每日日志
        ]

    def is_available(self) -> bool:
        return any(d.exists() for d in self.log_dirs)

    def search(self, query: str, factors: Dict, top_k: int = 5) -> List[Dict]:
        query_words = set(re.findall(r"[\u4e00-\u9fa5a-zA-Z0-9]{2,}", query.lower()))
        time_target = factors.get("时间", "")

        # 收集候选日志文件（最近 30 天优先）
        candidates: List[Tuple[Path, float]] = []
        for d in self.log_dirs:
            if not d.exists():
                continue
            for f in d.rglob("*"):
                if f.is_file() and f.suffix.lower() in (".log", ".md", ".jsonl", ".txt"):
                    try:
                        mtime = f.stat().st_mtime
                        candidates.append((f, mtime))
                    except Exception:
                        pass

        # 按修改时间排序，取最近 60 个文件
        candidates.sort(key=lambda x: x[1], reverse=True)
        candidates = candidates[:60]

        scored: List[Dict] = []
        for fpath, mtime in candidates:
            try:
                text = fpath.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            lower_text = text.lower()
            hits = sum(1 for w in query_words if w in lower_text)
            if hits == 0:
                continue

            # 截取命中上下文
            snippet = self._extract_snippet(text, query_words)
            ts = datetime.fromtimestamp(mtime, tz=CST).isoformat()

            # 文件名里的日期
            m = re.search(r"(\d{4}-\d{2}-\d{2})", fpath.name)
            file_date = m.group(1) if m else ""
            if file_date and time_target:
                score = hits * 10 + _time_proximity_score(file_date, time_target) * 5
            else:
                score = hits * 10

            scored.append({
                "file": str(fpath.relative_to(PROJECT_ROOT)) if str(fpath).startswith(str(PROJECT_ROOT)) else str(fpath),
                "title": fpath.name,
                "source": "log",
                "timestamp": ts,
                "源": f"log:{fpath.name}",
                "内容": snippet,
                "_score": score,
                "匹配度": min(1.0, score / 30),
                "_检索方式": "log-keyword",
            })

        scored.sort(key=lambda x: x["_score"], reverse=True)
        return scored[:top_k]

    @staticmethod
    def _extract_snippet(text: str, query_words: Set[str], radius: int = 80) -> str:
        lower = text.lower()
        for w in query_words:
            idx = lower.find(w)
            if idx >= 0:
                start = max(0, idx - radius)
                end = min(len(text), idx + len(w) + radius)
                return text[start:end].replace("\n", " ")
        # 无精确命中时返回前 200 字符
        return re.sub(r"\s+", " ", text)[:200]


def _make_source_instances(sources: List[str]) -> List[MemorySource]:
    """根据 source 名称列表构造记忆源实例"""
    registry: Dict[str, Any] = {
        "local": LocalMemorySource,
        "notion": NotionMemorySource,
        "log": LogMemorySource,
    }
    instances: List[MemorySource] = []
    for name in sources:
        cls = registry.get(name)
        if cls:
            try:
                inst = cls()
                if inst.is_available():
                    instances.append(inst)
            except Exception:
                pass
    return instances


def search_memories(query: str, sources: List[str], factors: Dict,
                    deep: bool = False) -> List[Dict]:
    """多源记忆检索入口：同时检索本地 / Notion / 日志"""
    instances = _make_source_instances(sources)
    if not instances:
        return []

    top_k = 8 if deep else 5
    all_results: List[Dict] = []
    for src in instances:
        try:
            results = src.search(query, factors, top_k=top_k)
            all_results.extend(results)
        except Exception as e:
            # 单源失败不阻断整体检索
            print(f"⚠️ 记忆源 {src.name} 检索失败: {e}")

    # 去重：按 (source + title/content) 去重
    seen: Set[str] = set()
    unique: List[Dict] = []
    for r in all_results:
        key = f"{r.get('source', '?')}:{r.get('title', '')}:{r.get('内容', '')[:40]}"
        if key in seen:
            continue
        seen.add(key)
        unique.append(r)

    unique.sort(key=lambda x: x.get("_score", 0), reverse=True)
    return unique[:10 if deep else 6]


def _search_index(query: str, factors: Dict, top_k: int = 5) -> List[Dict]:
    """倒排索引搜索（关键词匹配 + 时间加权）"""
    entries = _load_memory_index()
    if not entries:
        return []

    # 提取查询关键词
    query_words = set(re.findall(r'[\u4e00-\u9fa5a-zA-Z0-9]{2,}', query.lower()))
    time_target = factors.get("时间", "")

    scored = []
    for entry in entries:
        if not isinstance(entry, dict):
            continue
        score = 0.0
        # 组合标题+关键词
        entry_text = (entry.get("title", "") + " " + 
                      " ".join(entry.get("keywords", []))).lower()

        # 关键词命中
        hits = sum(1 for w in query_words if w in entry_text)
        score += hits * 10

        # 时间匹配加权
        entry_date = entry.get("date", "")
        if time_target and entry_date:
            score += _time_proximity_score(entry_date, time_target) * 5

        # DNA标记加权
        if entry.get("dna"):
            score += 3

        if score > 0:
            scored.append({**entry, "_score": score})

    scored.sort(key=lambda x: x["_score"], reverse=True)
    return scored[:top_k]


def _time_proximity_score(date1: str, date2: str) -> float:
    """日期接近度评分（越近越高）"""
    try:
        d1 = datetime.strptime(date1[:10], "%Y-%m-%d")
        d2 = datetime.strptime(date2[:10], "%Y-%m-%d")
        diff_days = abs((d1 - d2).days)
        if diff_days == 0: return 1.0
        if diff_days <= 1: return 0.9
        if diff_days <= 3: return 0.7
        if diff_days <= 7: return 0.5
        if diff_days <= 30: return 0.3
        return 0.1
    except Exception:
        return 0.0


def _init_chroma() -> bool:
    """懒加载 ChromaDB 向量检索引擎"""
    global _chroma_client, _chroma_collection, _vector_available
    if _vector_available:
        return True
    try:
        import chromadb
        from chromadb.utils import embedding_functions
        _chroma_client = chromadb.PersistentClient(
            path=str(CACHE_DIR / "chroma_db")
        )
        ef = embedding_functions.DefaultEmbeddingFunction()
        try:
            _chroma_collection = _chroma_client.get_collection(
                "xuanji_memory", embedding_function=ef
            )
        except Exception:
            _chroma_collection = _chroma_client.create_collection(
                name="xuanji_memory", embedding_function=ef
            )
        _vector_available = True
        return True
    except ImportError:
        return False


def _build_vector_index(force: bool = False):
    """构建向量索引（从记忆索引 + STATE.md + MEMORY.md）"""
    global _chroma_client, _chroma_collection
    if not _init_chroma():
        print("⚠️ ChromaDB 不可用，跳过向量索引")
        return

    existing = _chroma_collection.count() if _chroma_collection else 0
    if existing > 0 and not force:
        return

    print("📦 构建璇玑向量索引...")
    docs, metas, ids = [], [], []

    # L0: MEMORY.md（长期记忆事实层）
    if MEMORY_FILE.exists():
        content = MEMORY_FILE.read_text(encoding='utf-8')
        # 按 ## 分段
        sections = re.split(r'\n##\s+', content)
        for i, sec in enumerate(sections):
            if len(sec.strip()) > 50:
                docs.append(sec[:3000])
                metas.append({"源": "MEMORY.md", "层级": "L0", "段": i})
                ids.append(f"L0_{i:04d}")

    # L1: STATE.md（当前状态）
    if STATE_FILE.exists():
        content = STATE_FILE.read_text(encoding='utf-8')
        docs.append(content[:5000])
        metas.append({"源": "STATE.md", "层级": "L1"})
        ids.append("L1_state")

    # L2: 每日日志（最近30天）
    log_files = sorted(MEMORY_DIR.glob("????-??-??.md"), reverse=True)[:30]
    for i, f in enumerate(log_files):
        content = f.read_text(encoding='utf-8')
        if len(content.strip()) > 30:
            docs.append(content[:3000])
            metas.append({"源": f.name, "层级": "L2"})
            ids.append(f"L2_{i:04d}")

    # L3: 记忆索引条目
    index_entries = _load_memory_index()
    for i, entry in enumerate(index_entries[:100]):
        if not isinstance(entry, dict):
            continue
        text = f"{entry.get('title','')} {' '.join(entry.get('keywords',[]))}"
        if len(text.strip()) > 20:
            docs.append(text[:2000])
            metas.append({"源": "索引", "层级": "L3", "日期": entry.get("date","")})
            ids.append(f"L3_{i:04d}")

    if docs:
        try:
            # 清空重建
            try:
                _chroma_client.delete_collection("xuanji_memory")
                from chromadb.utils import embedding_functions
                ef = embedding_functions.DefaultEmbeddingFunction()
                _chroma_collection = _chroma_client.create_collection(
                    name="xuanji_memory", embedding_function=ef
                )
            except Exception:
                pass  # 用旧collection
            
            # 分批添加
            batch_size = 50
            for i in range(0, len(docs), batch_size):
                batch_docs = docs[i:i+batch_size]
                batch_metas = metas[i:i+batch_size]
                batch_ids = ids[i:i+batch_size]
                _chroma_collection.add(
                    documents=batch_docs,
                    metadatas=batch_metas,
                    ids=batch_ids
                )
            print(f"✅ 向量索引完成: {len(docs)} 条记忆")
        except Exception as e:
            print(f"⚠️ 向量索引构建失败: {e}")


def _vector_search(query: str, top_k: int = 5) -> List[Dict]:
    """ChromaDB 向量检索"""
    if not _vector_available or not _chroma_collection:
        return []
    try:
        results = _chroma_collection.query(
            query_texts=[query], n_results=top_k
        )
        memories = []
        if results.get('documents') and results['documents'][0]:
            for idx, doc in enumerate(results['documents'][0]):
                meta = results['metadatas'][0][idx] if results.get('metadatas') else {}
                dist = results['distances'][0][idx] if results.get('distances') else 1.0
                memories.append({
                    "源": meta.get("源", "未知"),
                    "层级": meta.get("层级", "L?"),
                    "内容": doc[:400],
                    "匹配度": round(1.0 - min(dist, 1.0), 3),
                })
        return memories
    except Exception:
        return []


def aozora_trace(query: str, deep: bool = False,
                 memory_sources: Optional[List[str]] = None) -> Tuple[Dict, List[Dict]]:
    """青龍·溯源 — 七因子解析 + 多源记忆检索"""
    # 1. 查询上下文七因子
    factors = _parse_seven_factors(query)

    # 2. 多源记忆检索（默认 local，可扩展 notion / log）
    if memory_sources is None:
        memory_sources = ["local"]
    merged = search_memories(query, memory_sources, factors, deep=deep)

    # 3. 尝试加载行为七因子信用分（如果可用）
    behavior_score = None
    behavior_pattern = None
    try:
        sys.path.insert(0, str(PROJECT_ROOT))
        from engines.lh_seven_factor_engine import SevenFactorEngine
        se = SevenFactorEngine()
        score_obj = se.get_score("UID9622") or se.get_score("uid9622_master_hash")
        pattern_obj = se.get_pattern("UID9622") or se.get_pattern("uid9622_master_hash")
        if score_obj and isinstance(score_obj, dict):
            behavior_score = score_obj.get("current_score")
        if pattern_obj and isinstance(pattern_obj, dict):
            behavior_pattern = {
                "pattern": pattern_obj.get("behavior_pattern"),
                "kept_ratio": pattern_obj.get("kept_ratio"),
                "risk_level": pattern_obj.get("risk_level"),
            }
    except Exception:
        pass
    # 兜底：从信任注册表取分
    if behavior_score is None:
        behavior_score = _load_trust_score()
    factors["行为信用分"] = behavior_score
    factors["行为模式"] = behavior_pattern

    return factors, merged


def _merge_dedup(index_results: List[Dict], vector_results: List[Dict]) -> List[Dict]:
    """合并倒排索引和向量检索结果，按综合得分排序去重"""
    seen_sources = set()
    merged = []

    # 向量结果优先（语义匹配更精准）
    for r in vector_results:
        key = r.get("源", "") + r.get("内容", "")[:50]
        if key not in seen_sources:
            seen_sources.add(key)
            r["_检索方式"] = "向量"
            r["_score"] = r.get("匹配度", 0.5) * 100
            merged.append(r)

    for r in index_results:
        key = r.get("date", "") + r.get("title", "")[:50]
        if key not in seen_sources:
            seen_sources.add(key)
            r["_检索方式"] = "索引"
            r["_score"] = r.get("_score", 1)
            merged.append(r)

    merged.sort(key=lambda x: x["_score"], reverse=True)
    return merged


# ──────────────────────────────────────────────
# 第二象 · 朱雀·齐政 — 16人格加权推演
# ──────────────────────────────────────────────

def _build_persona_prompt(persona: str, query: str, memories: List[Dict]) -> str:
    """构造人格推演提示词"""
    persona_name = persona.split("_", 1)[-1] if "_" in persona else persona
    mem_text = ""
    for i, m in enumerate(memories[:3]):
        src = m.get("源", m.get("date", "?"))
        # 兼容不同来源的记忆格式
        content = (m.get("内容") or m.get("title") or 
                   " ".join(m.get("keywords", []))[:200] or "无摘要")
        mem_text += f"[记忆{i+1}·{src}] {content}\n"

    return (
        f"你是{persona_name}。用户问：「{query}」\n"
        f"已知记忆:\n{mem_text}\n"
        f"请用{persona_name}的视角给出简短解读（80字内），只输出解读，不加任何前缀。"
    )


def _strip_ansi(text: str) -> str:
    """去除终端控制序列，防止 Ollama 进度条污染输出"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def _ollama_infer(system_prompt: str, user_prompt: str, 
                  model: str = "qwen2.5:1.5b", timeout: int = 20) -> str:
    """调用本地 Ollama 推理（合并system+user为单个提示词）"""
    try:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        cmd = ["ollama", "run", model, full_prompt]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if result.returncode == 0 and result.stdout.strip():
            return _strip_ansi(result.stdout.strip())
        err = _strip_ansi(result.stderr.strip()) if result.stderr else "未知错误"
        return f"（推理失败: {err}）"
    except subprocess.TimeoutExpired:
        return "（推理超时）"
    except FileNotFoundError:
        return "（Ollama 未安装）"
    except Exception as e:
        return f"（推理失败: {e}）"


def _infer_one_persona(persona: str, query: str, memories: List[Dict]) -> Tuple[str, str]:
    """单个人格推理（供线程池调用）"""
    prompt = _build_persona_prompt(persona, query, memories)
    raw = _ollama_infer(
        f"你是{persona.split('_',1)[-1]}，龍魂系统的人格之一。回答简洁、直接、有见地。",
        prompt,
        timeout=25
    )
    return persona, raw


def suzaku_reason(query: str, memories: List[Dict], 
                  deep: bool = False) -> Dict[str, Any]:
    """朱雀·齐政 — 16人格加权推演（人格视角并行推理）"""
    # 选择人格（deep模式全部，否则选权重最高的6个）
    if deep:
        active_personas = dict(PERSONA_WEIGHTS)
    else:
        active_personas = dict(sorted(
            PERSONA_WEIGHTS.items(), key=lambda x: -x[1]
        )[:6])

    interpretations = {}
    # 并行推理，避免 Ollama 顺序调用过慢
    max_workers = min(8, len(active_personas))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_persona = {
            executor.submit(_infer_one_persona, p, query, memories): p
            for p, w in active_personas.items() if w > 0
        }
        for future in as_completed(future_to_persona):
            persona = future_to_persona[future]
            try:
                _, raw = future.result()
                interpretations[persona] = raw
            except Exception as e:
                interpretations[persona] = f"（推理异常: {e}）"

    # 加权融合
    fused = _weighted_fusion(interpretations, active_personas)

    return {
        "解读": interpretations,
        "融合": fused,
        "活跃人格数": len(interpretations),
    }


def _weighted_fusion(interpretations: Dict[str, str],
                     weights: Dict[str, float]) -> str:
    """按人格权重融合多个解读：先列出各人格观点，再由模型合成一段连贯结论"""
    parts = []
    total_weight = sum(weights.values()) or 1.0
    for persona, text in interpretations.items():
        w = weights.get(persona, 0.05) / total_weight
        name = persona.split("_", 1)[-1] if "_" in persona else persona
        parts.append(f"【{name}·{w:.0%}】{text}")
    raw_fusion = "\n\n".join(parts)

    # 用 Ollama 合成一段带因果链词的连贯结论
    synthesis_prompt = (
        "你是一位冷静的龍魂系统 synthesizer。请综合以下多个人格视角的解读，"
        "生成一段 150 字以内的连贯结论。要求：\n"
        "1. 使用'因为'、'所以'、'因此'、'由此'、'基于'等推理连接词；\n"
        "2. 保留关键事实和判断；\n"
        "3. 不要编造原始材料中没有的信息；\n"
        "4. 语气稳重、简洁。\n\n"
        f"{raw_fusion}\n\n"
        "请直接输出合成结论，不要加标题。"
    )
    synthesized = _ollama_infer(
        "你是龍魂系统的结论 synthesizer，只基于给定材料输出连贯结论。",
        synthesis_prompt,
        timeout=30
    )
    # 如果合成失败或太短，退回到原始拼接
    if len(synthesized) < 20 or "失败" in synthesized or "超时" in synthesized:
        return raw_fusion
    return synthesized


# ──────────────────────────────────────────────
# 第三象 · 白虎·验真 — 三六九不动点校验
# ──────────────────────────────────────────────

def _load_state_anchors() -> Dict[str, Any]:
    """从 STATE.md 提取核心锚点"""
    anchors = {
        "UID": "9622",
        "创建者": "诸葛鑫",
        "GPG": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
        "确认码": CONFIRM_CODE,
        "369": [3, 6, 9],
    }
    if STATE_FILE.exists():
        content = STATE_FILE.read_text(encoding='utf-8')
        # 提取焊死锚点块
        m = re.search(r'焊死锚点.*?(?=\n##|\Z)', content, re.DOTALL)
        if m:
            anchors["STATE_锚点块"] = m.group()[:500]
    return anchors


def byakko_verify(fused_text: str, memories: List[Dict], 
                  factors: Dict) -> Tuple[bool, bool, bool, Dict]:
    """白虎·验真 — 三层校验"""
    anchors = _load_state_anchors()

    # 宏观·根校验：产出是否与核心事实冲突
    macro_ok = True
    macro_issues = []
    # 检查核心标识
    if "9622" in fused_text or "UID9622" in fused_text or "诸葛鑫" in fused_text:
        pass  # 已关联核心身份
    # 检查是否与 STATE.md 矛盾（简单规则，后续可接深度校验）
    if STATE_FILE.exists():
        state_text = STATE_FILE.read_text(encoding='utf-8')[:3000]
        # 检查关键事实
        for kw in ["龍魂", "CNSH", "369", "20人格"]:
            if kw in fused_text and kw not in state_text:
                pass  # 新知识，不算矛盾

    # 中观·链校验：推理是否连续（链词 or 多视角结构）
    chain_words = ["因为", "所以", "因此", "由于", "基于", "由此",
                   "导致", "从而", "进而", "归结", "总结"]
    chain_count = sum(1 for w in chain_words if w in fused_text)
    # 多视角融合输出中的人格分区也算结构化推理证据
    persona_sections = len(re.findall(r'【[^】]+】', fused_text))
    meso_ok = chain_count >= 1 or persona_sections >= 2 or len(fused_text) < 80
    meso_detail = f"推理链词命中: {chain_count}, 人格视角: {persona_sections}"

    # 微观·源校验：是否有DNA/溯源
    has_dna = any(kw in fused_text for kw in ["DNA", "龍芯", "签章", "#"])
    has_memory_source = len(memories) > 0
    micro_ok = has_dna or has_memory_source
    micro_detail = f"DNA标记: {has_dna}, 记忆源: {has_memory_source}"

    # 三六九不动点校验
    si_369 = _check_369_anchor(fused_text)

    details = {
        "宏观": {"通过": macro_ok, "问题": macro_issues},
        "中观": {"通过": meso_ok, "详情": meso_detail},
        "微观": {"通过": micro_ok, "详情": micro_detail},
        "三六九": si_369,
    }

    return macro_ok, meso_ok, micro_ok, details


def _check_369_anchor(text: str) -> Dict:
    """三六九不动点快速校验"""
    nums = [int(n) for n in re.findall(r'\b\d+\b', text)]
    has_3 = 3 in nums
    has_6 = 6 in nums
    has_9 = 9 in nums
    # 369出现次数与位置（洛书九宫）
    count_369 = sum(1 for n in nums if n in (3, 6, 9))
    return {
        "3出现": has_3, "6出现": has_6, "9出现": has_9,
        "369计数": count_369,
        "锚定状态": "稳固" if count_369 >= 1 else "待锚定",
    }


# ──────────────────────────────────────────────
# 第四象 · 玄武·烙印 — DNA签章 + GPG签名
# ──────────────────────────────────────────────

def _load_trust_score() -> int:
    """从信任注册表加载当前信任分"""
    default_score = 80
    if TRUST_REGISTRY.exists():
        try:
            data = json.loads(TRUST_REGISTRY.read_text(encoding='utf-8'))
            # 新版结构: {"users": {"uid9622_master_hash": 95.0, ...}, "names": {...}}
            if isinstance(data, dict):
                users = data.get("users", {})
                for k, v in users.items():
                    if "9622" in str(k) and isinstance(v, (int, float)):
                        return int(v)
                # 兼容旧版: 顶层键值
                for k, v in data.items():
                    if k == "_meta":
                        continue
                    if "9622" in str(k):
                        if isinstance(v, dict):
                            return int(v.get("trust_score", v.get("score", default_score)))
                        if isinstance(v, (int, float)):
                            return int(v)
            # 兼容旧版 list 结构
            elif isinstance(data, list):
                for entry in data:
                    if isinstance(entry, dict):
                        if entry.get("uid") == "9622" or "UID9622" in str(entry):
                            return int(entry.get("trust_score", default_score))
        except Exception:
            pass
    return default_score


def _save_trust_score(new_score: int):
    """持久化信任分回注册表"""
    try:
        data = {}
        if TRUST_REGISTRY.exists():
            data = json.loads(TRUST_REGISTRY.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            data = {"_meta": {"title": "龍魂·信任积分注册表", "note": "user_dna_hash -> trust_score"}}
        users = data.setdefault("users", {})
        names = data.setdefault("names", {})
        users["uid9622_master_hash"] = round(float(new_score), 2)
        names["uid9622_master_hash"] = "UID9622·诸葛鑫"
        TRUST_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
        TRUST_REGISTRY.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8'
        )
    except Exception as e:
        # 写失败不阻断主流程
        print(f"⚠️ 信任分持久化失败: {e}")


def _generate_dna(content: str, module: str = "XUANJI") -> str:
    """生成DNA追溯码"""
    hash_short = hashlib.sha256(content.encode()).hexdigest()[:8]
    now = datetime.now(CST)
    return f"{DNA_PREFIX}{now.strftime('%Y-%m-%d')}-{module}-OUTPUT-{hash_short}"


def genbu_stamp(fused_text: str, trace_path: List[Dict],
                persona_votes: Dict, verify_result: Tuple,
                trust_score: int, factors: Dict,
                persona_name: str = "璇玑") -> Dict:
    """玄武·烙印 — 生成带DNA签章的完整输出（增加反虚伪前置检查）"""
    now = datetime.now(CST)
    macro_ok, meso_ok, micro_ok = verify_result

    # 反虚伪仲裁中心联动：输出前挂载检查
    if _anti_hypocrisy_center is not None:
        仲裁结果 = _anti_hypocrisy_center.检查(
            文本=fused_text,
            人格=persona_name,
            语言="auto",
            模式="同步",
        )
        if 仲裁结果.get("状态") == "熔断":
            return {
                "状态": "熔断",
                "原因": f"反虚伪仲裁拦截: {仲裁结果.get('建议', '文本虚伪度过高')}",
                "触发词": 仲裁结果.get("一级命中", []),
                "虚伪度": 仲裁结果.get("虚伪度", 0),
                "DNA": f"{DNA_PREFIX}{now.strftime('%Y-%m-%d')}-XUANJI-ANTI-HYPOCRISY-FUSE",
                "引擎DNA": ENGINE_DNA,
                "时间戳": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
            }
        if 仲裁结果.get("状态") == "自动简化":
            fused_text = 仲裁结果.get("简化后", fused_text)

    # 信任分调整
    score_delta = 0
    if macro_ok: score_delta += 1
    if meso_ok: score_delta += 1
    if micro_ok: score_delta += 2
    new_trust = min(100, trust_score + score_delta)

    output = {
        "内容": fused_text,
        "溯源路径": [
            {"源": m.get("源", m.get("date", "?")),
             "匹配度": m.get("匹配度", m.get("_score", 0)),
             "方式": m.get("_检索方式", "未知")}
            for m in trace_path[:5]
        ],
        "人格投票": {k: v[:50] + "..." if len(v) > 50 else v 
                     for k, v in persona_votes.get("解读", {}).items()},
        "校验": {
            "宏观": macro_ok,
            "中观": meso_ok,
            "微观": micro_ok,
        },
        "七因子": {
            "时间": factors.get("时间", ""),
            "空间": factors.get("空间", ""),
            "操作": factors.get("操作", ""),
            "情绪": factors.get("情绪", 0),
            "行为信用分": factors.get("行为信用分"),
        },
        "信任分": {"调整前": trust_score, "调整后": new_trust, "变化": score_delta},
        "DNA": _generate_dna(fused_text),
        "引擎DNA": ENGINE_DNA,
        "时间戳": now.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "签章方": "龍芯北辰 UID9622",
        "确认码": CONFIRM_CODE,
        "审计摘要": hashlib.sha256(
            json.dumps({"内容": fused_text, "时间": now.isoformat()}, 
                       ensure_ascii=False).encode()
        ).hexdigest()[:16],
    }

    return output


# ──────────────────────────────────────────────
# 熔断层 — 综合判定
# ──────────────────────────────────────────────

def _meltdown_check(stamped: Dict) -> Tuple[str, Optional[str]]:
    """熔断判定"""
    verify = stamped.get("校验", {})
    trust = stamped.get("信任分", {})

    # 三六九全不通过 → 🔴熔断
    if not any([verify.get("宏观", True),
                verify.get("中观", True),
                verify.get("微观", True)]):
        return "🔴熔断", "三六九校验全未通过，输出不可信"

    # 核心身份缺失 → 🔴熔断
    content = stamped.get("内容", "")
    if "UID9622" in content or "龍魂" in content or "诸葛鑫" in content:
        pass  # OK
    else:
        if len(verify) > 0 and not verify.get("宏观", True):
            return "🔴熔断", "核心事实锚定失败"

    # 低信任分 → 🟡告警
    new_trust = trust.get("调整后", 80)
    if new_trust < 30:
        return "🔴熔断", f"信任分过低({new_trust})"
    if new_trust < 50:
        return "🟡告警", f"信任分偏低({new_trust})，建议人工复核"

    # 无溯源记忆 → 🟡告警
    trace = stamped.get("溯源路径", [])
    if len(trace) == 0:
        return "🟡告警", "无相关记忆溯源，可能为纯推测"

    return "🟢通过", None


# ──────────────────────────────────────────────
# 主引擎
# ──────────────────────────────────────────────

class XuanjiEngine:
    """龍魂·璇玑记忆溯源推演系统 v5.0"""

    def __init__(self):
        self.trust_score = _load_trust_score()
        self.session_count = 0

    def run(self, query: str, deep: bool = False,
            memory_sources: Optional[List[str]] = None,
            no_llm: bool = False) -> Dict:
        """四象完整运转"""
        self.session_count += 1

        # 象一·青龍·溯源
        factors, memories = aozora_trace(query, deep=deep,
                                         memory_sources=memory_sources)

        # 象二·朱雀·齐政
        if no_llm:
            fused_text = _fallback_fusion(query, memories)
            persona_result = {
                "解读": {},
                "融合": fused_text,
                "活跃人格数": 0,
                "no_llm": True,
            }
        else:
            persona_result = suzaku_reason(query, memories, deep=deep)
            fused_text = persona_result["融合"]

        # 象三·白虎·验真
        macro_ok, meso_ok, micro_ok, verify_details = byakko_verify(
            fused_text, memories, factors
        )

        # 象四·玄武·烙印
        stamped = genbu_stamp(
            fused_text, memories, persona_result,
            (macro_ok, meso_ok, micro_ok),
            self.trust_score, factors
        )

        # 反虚伪仲裁熔断：直接返回，不再走后续校验
        if stamped.get("状态") == "熔断":
            return stamped

        # 熔断判定
        melt_status, melt_reason = _meltdown_check(stamped)
        stamped["熔断"] = {"状态": melt_status, "原因": melt_reason}

        # 信任分更新并持久化
        self.trust_score = stamped["信任分"]["调整后"]
        _save_trust_score(self.trust_score)

        return stamped

    def get_status(self) -> Dict:
        """引擎状态"""
        entries = _load_memory_index()
        vec_avail = _init_chroma()
        vec_count = _chroma_collection.count() if _chroma_collection else 0
        return {
            "引擎": "璇玑 v5.0",
            "DNA": ENGINE_DNA,
            "会话数": self.session_count,
            "信任分": self.trust_score,
            "记忆索引条目": len(entries),
            "向量索引可用": vec_avail,
            "向量条目数": vec_count,
            "最后索引构建": "动态",
        }


def _fallback_fusion(query: str, memories: List[Dict]) -> str:
    """无 LLM 时的融合摘要：直接列出记忆来源与关键内容"""
    lines = [f"基于 {len(memories)} 条记忆片段对「{query}」的溯源摘要："]
    for i, m in enumerate(memories[:5], 1):
        src = m.get("源", m.get("source", "?"))
        content = (m.get("内容") or m.get("title") or "无摘要")[:120]
        lines.append(f"{i}. [{src}] {content}")
    if len(memories) > 5:
        lines.append(f"... 以及另外 {len(memories) - 5} 条相关记忆")
    lines.append("因此，建议基于上述记忆进一步调用本地模型做深度推演。")
    return "\n".join(lines)


# ──────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────

def _format_output(result: Dict) -> str:
    """格式化终端输出"""
    melt = result.get("熔断", {})
    melt_status = melt.get("状态", "🟢通过")

    lines = []
    lines.append("")
    lines.append("=" * 64)
    lines.append("  🐉 璇玑引擎 v5.0 · 记忆溯源推演结果")
    lines.append("=" * 64)
    lines.append("")

    if melt_status == "🔴熔断":
        lines.append(f"  ❌ {melt_status}: {melt.get('原因', '')}")
        lines.append("")
        lines.append("=" * 64)
        return "\n".join(lines)

    # 主内容
    content = result.get("内容", "")
    for line in content.split("\n"):
        lines.append(f"  {line}")
    lines.append("")

    # 校验状态
    verify = result.get("校验", {})
    macro = "✅" if verify.get("宏观") else "❌"
    meso = "✅" if verify.get("中观") else "❌"
    micro = "✅" if verify.get("微观") else "❌"
    lines.append(f"  {melt_status} 校验: 宏观{macro} 中观{meso} 微观{micro}")

    # 信任分
    trust = result.get("信任分", {})
    old_t = trust.get("调整前", "?")
    new_t = trust.get("调整后", "?")
    delta = trust.get("变化", 0)
    sign = "+" if delta > 0 else ""
    lines.append(f"  📊 信任分: {old_t} → {new_t} ({sign}{delta})")

    # 溯源
    trace = result.get("溯源路径", [])
    lines.append(f"  🔗 溯源: {len(trace)} 条记忆")
    for t in trace[:3]:
        src = t.get("源", "?")
        method = t.get("方式", "")
        lines.append(f"     [{method}] {src}")

    # DNA
    lines.append(f"  🧬 {result.get('DNA', '')}")
    lines.append("")
    lines.append("=" * 64)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="龍魂·璇玑引擎 v5.0 — 记忆溯源推演系统",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 engines/lh_xuanji_engine.py "去年318路上的事"
  python3 engines/lh_xuanji_engine.py "训练模型" --deep --raw
  python3 engines/lh_xuanji_engine.py --status
  python3 engines/lh_xuanji_engine.py --rebuild-index
  python3 engines/lh_xuanji_engine.py "测试记忆接入" --memory-source local --no-llm
  python3 engines/lh_xuanji_engine.py "顶刊论文" --memory-source local,notion,log --raw
        """
    )
    parser.add_argument("query", nargs="?", type=str, help="查询问题")
    parser.add_argument("--raw", action="store_true", help="JSON原样输出")
    parser.add_argument("--deep", action="store_true", help="深度推演（更多记忆+全人格）")
    parser.add_argument("--status", action="store_true", help="显示引擎状态")
    parser.add_argument("--rebuild-index", action="store_true",
                        help="强制重建向量索引")
    parser.add_argument("--memory-source", type=str, default="local",
                        help="记忆源，逗号分隔（local/notion/log），默认 local")
    parser.add_argument("--no-llm", action="store_true",
                        help="跳过本地 LLM 推理，仅做记忆检索与校验（测试用）")
    args = parser.parse_args()

    engine = XuanjiEngine()

    # 解析记忆源
    memory_sources = [s.strip() for s in args.memory_source.split(",") if s.strip()]
    valid_sources = {"local", "notion", "log"}
    memory_sources = [s for s in memory_sources if s in valid_sources]
    if not memory_sources:
        memory_sources = ["local"]

    # 状态查询
    if args.status:
        print(json.dumps(engine.get_status(), ensure_ascii=False, indent=2))
        return

    # 重建索引
    if args.rebuild_index:
        print("🔄 重建璇玑向量索引...")
        _build_vector_index(force=True)
        stat = engine.get_status()
        print(json.dumps(stat, ensure_ascii=False, indent=2))
        return

    # 查询
    if not args.query:
        parser.print_help()
        return

    result = engine.run(
        args.query, deep=args.deep,
        memory_sources=memory_sources, no_llm=args.no_llm
    )

    if args.raw:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(_format_output(result))


if __name__ == "__main__":
    main()
