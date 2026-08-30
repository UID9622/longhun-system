#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 知识全息拉取器 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·䷸巽-HARVEST-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 从 Notion、CSDN、本地代码库、Mac备忘录、AI对话记录拉取龍魂相关知识
  - 提取哲学/原则/规则/模式
  - 自动转化为可执行的系统代码骨架
  - 生成知识主权报告

用法：
  lh 知识拉取                    # 全量拉取（所有来源）
  lh 知识拉取 --source notion    # 只拉 Notion
  lh 知识拉取 --source csdn      # 只拉 CSDN
  lh 知识拉取 --source local     # 只拉本地代码库
  lh 知识拉取 --source notes     # 只拉 Mac 备忘录
  lh 知识拉取 --source ai        # 只拉 AI 对话记录
  lh 知识拉取 --dry-run          # 预览模式（不落地）
  lh 知识拉取 --force            # 强制重新拉取（覆盖缓存）
"""

import os
import re
import sys
import json
import time
import hashlib
import subprocess
import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from collections import defaultdict
from dataclasses import dataclass, field

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
CACHE_DIR = PROJECT_ROOT / "data" / "knowledge_cache"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR = PROJECT_ROOT / "data" / "harvested_knowledge"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 龍魂相关关键词（用于过滤和标记）
LONGHUN_KEYWORDS = [
    "龍魂", "龍魂系统", "DragonSoul", "UID9622", "诸葛鑫",
    "君子协议", "耻辱柱", "反虚伪", "掀黑箱", "主权",
    "DNA", "三色审计", "省电积分", "活人证明",
    "CNSH", "龍魂", "鲲鹏", "主权验证", "因果推断",
    "任务编排", "多智能体", "图谱", "神经补全", "熔断",
    "德本审计", "离火运", "三才", "369", "洛书",
]


# ============================================================
# 数据结构
# ============================================================

@dataclass
class KnowledgeItem:
    source: str           # notion/csdn/local/notes/ai
    source_id: str        # 原始ID或路径
    title: str
    content: str
    keywords: List[str] = field(default_factory=list)
    entities: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    hash: str = ""
    is_philosophy: bool = False
    is_code: bool = False
    is_rule: bool = False
    code_snippet: Optional[str] = None
    rule_proposal: Optional[str] = None

    def __post_init__(self):
        if not self.hash:
            self.hash = hashlib.md5(
                f"{self.source}{self.source_id}{self.content[:100]}".encode()
            ).hexdigest()[:16]


# ============================================================
# 基类：拉取器
# ============================================================

class BaseFetcher:
    """拉取器基类"""
    def __init__(self, cache_dir: Path = CACHE_DIR):
        self.cache_dir = cache_dir
        self.cache_file = cache_dir / f"{self.__class__.__name__.lower()}.json"
        self._cache = self._load_cache()

    def _load_cache(self) -> Dict:
        if self.cache_file.exists():
            try:
                return json.loads(self.cache_file.read_text())
            except Exception:
                return {}
        return {}

    def _save_cache(self):
        self.cache_file.write_text(json.dumps(self._cache, ensure_ascii=False, indent=2))

    def _is_cached(self, item_id: str) -> bool:
        return item_id in self._cache

    def _cache_item(self, item_id: str, data: Dict):
        self._cache[item_id] = data
        # 不每项写盘——由 fetch() 结束后统一 save

    def fetch(self, force: bool = False) -> List[KnowledgeItem]:
        raise NotImplementedError

    def get_name(self) -> str:
        return self.__class__.__name__.replace("Fetcher", "").lower()

    @staticmethod
    def _extract_lh_keywords(text: str) -> List[str]:
        words = set()
        for kw in LONGHUN_KEYWORDS:
            if kw in text:
                words.add(kw)
        return sorted(words)


# ============================================================
# 1. Notion 拉取器
# ============================================================

class NotionFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.api_key = os.environ.get("NOTION_API_KEY", "")
        self.database_id = os.environ.get("NOTION_DATABASE_ID", "")
        self._client = None

    def _init_client(self) -> bool:
        if not self.api_key:
            return False
        try:
            from notion_client import Client
            self._client = Client(auth=self.api_key)
            return True
        except ImportError:
            return False
        except Exception:
            return False

    def fetch(self, force: bool = False) -> List[KnowledgeItem]:
        items = []
        if not self._init_client():
            return self._fetch_from_cache()

        if not self.database_id:
            return self._fetch_from_cache()

        try:
            resp = self._client.databases.query(database_id=self.database_id)
            for page in resp.get("results", []):
                page_id = page.get("id", "")
                if not force and self._is_cached(page_id):
                    continue
                props = page.get("properties", {})
                title = self._extract_title(props)
                content = self._extract_content(page)
                item = KnowledgeItem(
                    source="notion",
                    source_id=page_id,
                    title=title,
                    content=content,
                    keywords=self._extract_lh_keywords(content + title),
                )
                items.append(item)
                self._cache_item(page_id, {
                    "title": title, "content": content[:500],
                    "timestamp": datetime.now().isoformat(),
                })
        except Exception as e:
            print(f"⚠️ Notion 拉取失败: {e}")
            items = self._fetch_from_cache()
        return items

    def _fetch_from_cache(self) -> List[KnowledgeItem]:
        items = []
        for page_id, data in self._cache.items():
            if data.get("content"):
                items.append(KnowledgeItem(
                    source="notion_cached",
                    source_id=page_id,
                    title=data.get("title", ""),
                    content=data.get("content", ""),
                    keywords=self._extract_lh_keywords(data.get("content", "")),
                ))
        return items

    @staticmethod
    def _extract_title(props: Dict) -> str:
        for prop in props.values():
            if prop.get("type") == "title" and prop.get("title"):
                return "".join([t.get("plain_text", "") for t in prop["title"]])
        return "未命名页面"

    @staticmethod
    def _extract_content(page: Dict) -> str:
        parts = []
        for prop in page.get("properties", {}).values():
            if prop.get("type") == "rich_text":
                for text in prop.get("rich_text", []):
                    parts.append(text.get("plain_text", ""))
        return "\n".join(parts)


# ============================================================
# 2. CSDN 拉取器
# ============================================================

class CSDNFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.username = os.environ.get("CSDN_USERNAME", "UID9622")

    def fetch(self, force: bool = False) -> List[KnowledgeItem]:
        items = []
        csdn_file = PROJECT_ROOT / "data" / "csdn_articles.json"
        if csdn_file.exists():
            data = json.loads(csdn_file.read_text())
            for article in data.get("articles", []):
                text = article.get("content", "") + article.get("title", "")
                items.append(KnowledgeItem(
                    source="csdn",
                    source_id=article.get("id", ""),
                    title=article.get("title", ""),
                    content=article.get("content", ""),
                    keywords=self._extract_lh_keywords(text),
                ))
        else:
            self._create_example_file()
        return items

    def _create_example_file(self):
        example = {
            "username": self.username,
            "articles": [
                {
                    "id": "example_001",
                    "title": "【示例】龍魂系统：主权级AI执行骨架",
                    "content": """
龍魂系统是一个主权级AI执行骨架，核心原则包括：
1. 不歧视、不迎合、不瞎扯
2. DNA追溯码：所有内容可追溯
3. 君子协议：不走法律，走耻辱柱
4. 三色审计：🟢🟡🔴 自动决策
5. 反虚伪引擎：熔断虚假内容
6. 省电积分：量化算力节省
7. 掀黑箱引擎：审计技术主权
""",
                }
            ],
        }
        csdn_file = PROJECT_ROOT / "data" / "csdn_articles.json"
        csdn_file.write_text(json.dumps(example, ensure_ascii=False, indent=2))
        print(f"📝 CSDN 示例文件已创建: {csdn_file}")


# ============================================================
# 3. 本地代码拉取器
# ============================================================

class LocalFetcher(BaseFetcher):
    def __init__(self, root: Path = PROJECT_ROOT):
        super().__init__()
        self.root = root

    def fetch(self, force: bool = False) -> List[KnowledgeItem]:
        items = []
        for ext in [".py", ".md", ".cnsh", ".sh"]:
            for file_path in self.root.rglob(f"*{ext}"):
                if "data" in file_path.parts or "cache" in file_path.parts or ".git" in file_path.parts:
                    continue
                rel_path = str(file_path.relative_to(self.root))
                if not force and self._is_cached(rel_path):
                    continue
                # 🔴 三关判定(2026-08-30·文件身份协议v1.1): 前8KB含NUL→二进制跳过
                try:
                    with open(file_path, "rb") as f:
                        if b"\x00" in f.read(8192):
                            continue
                except OSError:
                    continue
                try:
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    if not self._is_relevant(content):
                        continue
                    item = KnowledgeItem(
                        source="local",
                        source_id=rel_path,
                        title=file_path.name,
                        content=content,
                        keywords=self._extract_lh_keywords(content),
                        is_code=ext in [".py", ".cnsh", ".sh"],
                        is_rule=ext == ".md" and any(
                            kw in content for kw in ["协议", "规则", "原则"]
                        ),
                    )
                    if ext == ".py":
                        item.code_snippet = self._extract_functions(content)
                    items.append(item)
                    self._cache_item(rel_path, {
                        "title": file_path.name, "content_hash": hashlib.md5(content.encode()).hexdigest()[:8],
                        "timestamp": datetime.now().isoformat(),
                    })
                except Exception:
                    continue
        self._save_cache()  # 批量扫描结束后统一写盘
        return items

    @staticmethod
    def _is_relevant(content: str) -> bool:
        return any(kw in content for kw in LONGHUN_KEYWORDS)

    @staticmethod
    def _extract_functions(content: str) -> str:
        """行级提取 def 签名（O(n)线性，避免灾难性回溯）"""
        lines = content.split("\n")
        funcs = []
        for line in lines:
            m = re.match(r"\s*def\s+(\w+)\s*\([^)]*\)\s*:", line)
            if m:
                funcs.append(line.strip())
                if len(funcs) >= 5:
                    break
        return "\n".join(funcs)


# ============================================================
# 4. Mac 备忘录拉取器
# ============================================================

class NotesFetcher(BaseFetcher):
    def fetch(self, force: bool = False) -> List[KnowledgeItem]:
        items = []
        try:
            script = '''
            tell application "Notes"
                set noteTexts to {}
                repeat with aNote in notes
                    set noteTexts to noteTexts & {name of aNote, body of aNote}
                end repeat
                return noteTexts
            end tell
            '''
            result = subprocess.run(
                ["osascript", "-e", script],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0 and result.stdout:
                data = result.stdout.strip().split(", ")
                for i in range(0, len(data) - 1, 2):
                    title = data[i] if i < len(data) else ""
                    content = data[i + 1] if i + 1 < len(data) else ""
                    if self._is_relevant(content + title):
                        items.append(KnowledgeItem(
                            source="notes",
                            source_id=f"note_{i // 2}",
                            title=title,
                            content=content,
                            keywords=self._extract_lh_keywords(content + title),
                        ))
        except Exception as e:
            print(f"⚠️ Mac 备忘录拉取失败: {e}")
            return self._fetch_from_cache()
        return items

    @staticmethod
    def _is_relevant(text: str) -> bool:
        return any(kw in text for kw in LONGHUN_KEYWORDS)

    def _fetch_from_cache(self) -> List[KnowledgeItem]:
        items = []
        for note_id, data in self._cache.items():
            items.append(KnowledgeItem(
                source="notes_cached",
                source_id=note_id,
                title=data.get("title", ""),
                content=data.get("content", ""),
                keywords=self._extract_lh_keywords(data.get("content", "")),
            ))
        return items


# ============================================================
# 5. AI 对话拉取器
# ============================================================

class AIFetcher(BaseFetcher):
    def __init__(self):
        super().__init__()
        self.ai_log_dirs = [
            Path.home() / ".codebuddy" / "projects",
            Path.home() / "Library" / "Application Support" / "CodeBuddy" / "history",
        ]

    def fetch(self, force: bool = False) -> List[KnowledgeItem]:
        items = []
        for log_dir in self.ai_log_dirs:
            if not log_dir.exists():
                continue
            for log_file in log_dir.rglob("*.jsonl"):
                # 🔴 三关判定(2026-08-30·文件身份协议v1.1): 前8KB含NUL→二进制跳过
                try:
                    with open(log_file, "rb") as f:
                        if b"\x00" in f.read(8192):
                            continue
                except OSError:
                    continue
                try:
                    for line in log_file.read_text(encoding="utf-8", errors="ignore").split("\n"):
                        if not line.strip():
                            continue
                        try:
                            data = json.loads(line)
                        except Exception:
                            continue
                        text = (
                            data.get("content", "")
                            or data.get("text", "")
                            or data.get("message", "")
                            or json.dumps(data)
                        )
                        if not self._is_relevant(text):
                            continue
                        tag = hashlib.md5(text[:100].encode()).hexdigest()[:8]
                        items.append(KnowledgeItem(
                            source="ai",
                            source_id=f"{log_file.stem}_{tag}",
                            title=f"AI对话: {log_file.stem[:30]}",
                            content=text[:5000],
                            keywords=self._extract_lh_keywords(text),
                        ))
                except Exception:
                    continue
        return items



# ============================================================
# 6. 知识分析器（哲学→代码转化核心）
# ============================================================

class KnowledgeAnalyzer:
    """分析拉取的知识，提取哲学、原则、规则，转化为代码"""

    def analyze(self, items: List[KnowledgeItem]) -> Dict[str, Any]:
        return {
            "principles": self._extract_principles(items),
            "rules": self._extract_rules(items),
            "patterns": self._extract_patterns(items),
            "missing": self._detect_missing(items),
            "code_candidates": self._extract_code_candidates(items),
        }

    def _extract_principles(self, items: List[KnowledgeItem]) -> List[Dict]:
        principles = []
        principle_patterns = [
            (r"(不|非)?(歧视|迎合|瞎扯|胡说|编造)", "反虚伪原则"),
            (r"(主权|自主|自治|自持)", "主权原则"),
            (r"(君子|道德|耻辱柱|德)", "君子协议原则"),
            (r"(透明|公开|可追溯|审计)", "透明原则"),
            (r"(最小化|精简|省电|节能)", "省电原则"),
            (r"(不离|不放弃|守护|保护)", "守护原则"),
        ]
        found_names = set()
        # 只采样前5000条（原则在头部项目足够覆盖）
        for item in items[:5000]:
            if len(found_names) >= len(principle_patterns):
                break
            snippet = item.content[:4096]  # 只扫前4KB
            for pattern, name in principle_patterns:
                if name in found_names:
                    continue
                if re.search(pattern, snippet):
                    context = self._extract_context(snippet, pattern)
                    principles.append({
                        "name": name,
                        "source": item.source,
                        "source_id": item.source_id,
                        "context": context,
                        "confidence": 0.8,
                    })
                    found_names.add(name)
                    break
        return principles

    def _extract_rules(self, items: List[KnowledgeItem]) -> List[Dict]:
        rules = []
        # 只采样前3000条 + 标记为规则的
        sample = [i for i in items if i.is_rule] + [i for i in items[:3000] if not i.is_rule]
        for item in sample:
            if len(rules) >= 100:
                break
            if item.is_rule or any(kw in item.content[:4096] for kw in ["规则", "必须", "禁止"]):
                # 行级提取，避免回溯
                for line in item.content[:16384].split("\n"):
                    if any(kw in line for kw in ["必须", "不能", "禁止", "允许", "不得", "应当"]):
                        rules.append({
                            "rule": line.strip()[:200],
                            "source": item.source,
                            "source_id": item.source_id,
                        })
                        if len(rules) >= 100:
                            break
        return rules

    def _extract_patterns(self, items: List[KnowledgeItem]) -> List[Dict]:
        word_counts = defaultdict(int)
        kw_set = set(LONGHUN_KEYWORDS)
        # 只采样前2000条
        for item in items[:2000]:
            for w in re.findall(r'[\u4e00-\u9fff]{2,}', item.content[:4096]):
                if w in kw_set:
                    word_counts[w] += 1
        patterns = []
        for word, count in sorted(word_counts.items(), key=lambda x: x[1], reverse=True)[:20]:
            if count > 2:
                patterns.append({
                    "keyword": word,
                    "frequency": count,
                    "significance": "high" if count > 5 else "medium",
                })
        return patterns

    def _detect_missing(self, items: List[KnowledgeItem]) -> List[str]:
        # 增量扫描而非拼接巨型字符串（避免OOM+CPU爆炸）
        all_content_chunks = []
        total_len = 0
        for item in items:
            chunk = item.content[:4096]  # 只取前4KB
            all_content_chunks.append(chunk)
            total_len += len(chunk)
            if total_len > 1_000_000:  # 最多拼1MB
                break
        all_content = " ".join(all_content_chunks)
        core_concepts = [
            ("反虚伪", ["反虚伪", "虚伪检测", "熔断"], ["反虚伪*", "anti_hypocrisy*", "lh_反虚伪*", "lh_anti*"]),
            ("主权验证", ["主权", "主权验证", "主权评分"], ["主权*", "sovereignty*", "lh_sovereignty*"]),
            ("省电积分", ["省电", "积分", "节能"], ["省电*", "energy*", "lh_energy*", "lh_power*"]),
            ("君子协议", ["君子", "耻辱柱", "违约"], ["君子*", "gentleman*", "lh_gentleman*"]),
            ("掀黑箱", ["掀黑箱", "审计", "黑箱"], ["掀黑箱*", "lh_blackbox*", "lh_openbox*"]),
            ("因果推断", ["因果", "推断", "为什么"], ["因果*", "causal*", "lh_causal*"]),
            ("多智能体", ["多智能体", "协作", "分工"], ["多智能*", "multi_agent*", "lh_multi*"]),
            ("DAG编排", ["DAG", "编排", "多步骤"], ["dag*", "lh_dag*", "编排*"]),
            ("神经补全", ["神经", "补全", "感知", "反思"], ["神经*", "neural*", "lh_neural*"]),
        ]
        # 先扫描文件系统确认哪些模块已有落地文件
        existing = self._check_existing_modules(core_concepts)
        missing = []
        for name, keywords, file_patterns in core_concepts:
            # 已确认存在 → 跳过
            if name in existing:
                continue
            # 关键词未在内容中出现 → 标记缺失
            if not any(kw in all_content for kw in keywords):
                missing.append(name)
        return missing

    @staticmethod
    def _check_existing_modules(core_concepts: List[tuple]) -> set:
        """扫描 bin/ 目录，确认哪些概念已有对应引擎文件落地"""
        existing = set()
        bin_dir = Path.home() / "longhun-system" / "bin"
        if not bin_dir.exists():
            return existing
        # 收集所有文件名（不含后缀）
        all_files = list(bin_dir.glob("*.py")) + list(bin_dir.glob("*.sh")) + list(bin_dir.glob("*.cnsh"))
        file_names = [f.stem.lower() for f in all_files]
        for name, _, patterns in core_concepts:
            for pattern in patterns:
                clean_pattern = pattern.lower().replace("*", "")
                if any(clean_pattern in fn for fn in file_names):
                    existing.add(name)
                    break
        return existing

    def _extract_code_candidates(self, items: List[KnowledgeItem]) -> List[Dict]:
        candidates = []
        for item in items:
            if item.is_code:
                candidates.append({
                    "source": item.source,
                    "source_id": item.source_id,
                    "title": item.title,
                    "code": item.code_snippet or "需要人工提取",
                })
        return candidates

    @staticmethod
    def _extract_context(text: str, pattern: str) -> str:
        match = re.search(r'[^。！？]{0,50}' + pattern + r'[^。！？]{0,50}[。！？]', text)
        if match:
            return match.group(0)
        return "（未提取到完整上下文）"

    def generate_code(self, analysis: Dict) -> Dict[str, str]:
        code_outputs = {}

        # 1. 原则文件
        principle_lines = [
            "# 龍魂系统原则",
            f"# DNA: #龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-PRINCIPLES-UID9622",
            f"# 自动生成于: {datetime.now().isoformat()}",
            "",
        ]
        for p in analysis["principles"]:
            principle_lines.append(f"## {p['name']}")
            principle_lines.append(f"来源: {p['source']} ({p['source_id']})")
            principle_lines.append(f"置信度: {p.get('confidence', '?')}")
            principle_lines.append(f"上下文: {p['context']}")
            principle_lines.append("")
        code_outputs["PRINCIPLES.md"] = "\n".join(principle_lines)

        # 2. 规则文件
        rules_lines = [
            "# 龍魂系统规则",
            f"# 自动生成于: {datetime.now().isoformat()}",
            "",
        ]
        for r in analysis["rules"]:
            rules_lines.append(f"- {r['rule']} (来源: {r['source']})")
        code_outputs["RULES.md"] = "\n".join(rules_lines)

        # 3. 缺失模块及代码骨架
        if analysis["missing"]:
            missing_lines = [
                "# 待补全模块",
                f"# 自动生成于: {datetime.now().isoformat()}",
                "",
            ]
            for m in analysis["missing"]:
                safe_name = re.sub(r'[^a-zA-Z0-9_\u4e00-\u9fff]', '', m)
                missing_lines.append(f"## {m}")
                missing_lines.append(f"- [ ] 待实现")
                missing_lines.append(f"```python")
                missing_lines.append(f"class {safe_name}Engine:")
                missing_lines.append(f"    \"\"\"{m}引擎 · 自动生成骨架\"\"\"")
                missing_lines.append(f"    def __init__(self):")
                missing_lines.append(f"        pass")
                missing_lines.append(f"```")
                missing_lines.append("")
            code_outputs["MISSING_MODULES.md"] = "\n".join(missing_lines)
        else:
            code_outputs["MISSING_MODULES.md"] = (
                f"# 全部模块已落地\n"
                f"# 自动生成于: {datetime.now().isoformat()}\n\n"
                f"✅ 所有核心概念均有对应引擎文件，无需补全。\n"
            )

        # 4. 代码候选
        if analysis["code_candidates"]:
            cc_lines = [
                "# 可复用的代码片段",
                f"# 自动生成于: {datetime.now().isoformat()}",
                "",
            ]
            for c in analysis["code_candidates"]:
                cc_lines.append(f"## {c['title']}")
                cc_lines.append(f"来源: {c['source']}")
                cc_lines.append(f"```python\n{c['code']}\n```")
                cc_lines.append("")
            code_outputs["CODE_CANDIDATES.md"] = "\n".join(cc_lines)

        return code_outputs


# ============================================================
# 7. 主收割机
# ============================================================

class KnowledgeHarvester:
    """知识收割机总控"""

    def __init__(self):
        self.fetchers = [
            NotionFetcher(),
            CSDNFetcher(),
            LocalFetcher(),
            NotesFetcher(),
            AIFetcher(),
        ]
        self.analyzer = KnowledgeAnalyzer()
        self.all_items: List[KnowledgeItem] = []

    def harvest(self, sources: List[str] = None, force: bool = False,
                dry_run: bool = False) -> Dict:
        """执行收割"""
        if sources:
            fetchers = [f for f in self.fetchers if f.get_name() in sources]
        else:
            fetchers = self.fetchers

        print(f"🚀 开始知识收割 ({len(fetchers)} 个来源)...\n")

        total = 0
        for fetcher in fetchers:
            print(f"  📡 拉取: {fetcher.get_name()}")
            try:
                items = fetcher.fetch(force=force)
                self.all_items.extend(items)
                total += len(items)
                print(f"    ✅ 拉取 {len(items)} 条")
            except Exception as e:
                print(f"    ❌ 失败: {e}")

        print(f"\n📊 共拉取 {total} 条知识")

        if dry_run:
            return {
                "total_items": total,
                "sources": [f.get_name() for f in fetchers],
                "items_preview": [
                    {"source": i.source, "title": i.title[:50], "keywords": i.keywords[:5]}
                    for i in self.all_items[:20]
                ],
            }

        # 分析
        print("\n🧠 开始分析...")
        analysis = self.analyzer.analyze(self.all_items)
        print(f"  📌 提取 {len(analysis['principles'])} 条原则")
        print(f"  📌 提取 {len(analysis['rules'])} 条规则")
        print(f"  📌 发现 {len(analysis['patterns'])} 个模式")
        print(f"  📌 检测 {len(analysis['missing'])} 个缺失模块")

        # 生成代码
        print("\n💻 生成代码...")
        code_outputs = self.analyzer.generate_code(analysis)

        for filename, content in code_outputs.items():
            filepath = OUTPUT_DIR / filename
            filepath.write_text(content, encoding="utf-8")
            print(f"  ✅ 生成: {filepath}")

        # 汇总报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_items": total,
            "principles": analysis["principles"],
            "rules": analysis["rules"][:10],
            "patterns": analysis["patterns"][:10],
            "missing": analysis["missing"],
            "code_candidates": len(analysis["code_candidates"]),
            "output_dir": str(OUTPUT_DIR),
            "dna": f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-HARVEST-UID9622",
        }

        report_file = OUTPUT_DIR / "harvest_report.json"
        report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2))

        print(f"\n✅ 收割完成，报告: {report_file}")
        return report


# ============================================================
# 8. 命令行入口
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="龍魂 · 知识全息拉取器")
    parser.add_argument("--source", "-s", action="append",
                        help="指定来源 (notion/csdn/local/notes/ai)")
    parser.add_argument("--dry-run", action="store_true",
                        help="预览模式（不落地）")
    parser.add_argument("--force", action="store_true",
                        help="强制重新拉取")
    parser.add_argument("--list-sources", action="store_true",
                        help="列出所有可用来源")
    args = parser.parse_args()

    if args.list_sources:
        print("可用来源:")
        for name, desc in [
            ("notion", "Notion 数据库（需 NOTION_API_KEY + NOTION_DATABASE_ID）"),
            ("csdn", "CSDN 博客（需 data/csdn_articles.json）"),
            ("local", "本地代码库（自动扫描 .py/.md/.cnsh/.sh）"),
            ("notes", "Mac 备忘录（AppleScript 读取）"),
            ("ai", "AI 对话记录（扫描 CodeBuddy 历史）"),
        ]:
            print(f"  - {name}: {desc}")
        return

    harvester = KnowledgeHarvester()
    result = harvester.harvest(
        sources=args.source,
        force=args.force,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        print("\n📋 预览结果:")
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
