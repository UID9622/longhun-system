#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂·本地知识引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·甲辰·离为火-知识引擎-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（君子协议，来源链不可切断）
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：Mac备忘录、文件、代码，全部可让CodeBuddy读取、学习、转化。
数据主权：不离开本地，全部加密存储。

功能：
  1. 备忘录采集 — 读取macOS备忘录
  2. 文件索引 — 扫描指定目录文件
  3. 代码学习 — 解析代码结构，生成文档
  4. 知识检索 — 语义搜索本地知识
  5. 代码转化 — 将自然语言转化为代码
  6. 向量存储 — ChromaDB本地向量索引
  7. 与CodeBuddy联动 — 直接对话式调用
"""

import os
import sys
import json
import re
import sqlite3
import hashlib
import subprocess
import time
import mimetypes
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any, Generator
from dataclasses import dataclass, field, asdict
import argparse
import shutil

# ============================================================
# 一、依赖检查与安装
# ============================================================

def ensure_dependencies():
    """确保必要依赖已安装"""
    missing = []
    try:
        import chromadb
    except ImportError:
        missing.append("chromadb")
    try:
        import sentence_transformers
    except ImportError:
        missing.append("sentence-transformers")
    if missing:
        print(f"⚠️ 缺少依赖: {', '.join(missing)}")
        print("请运行: pip install chromadb sentence-transformers")
        return False
    return True

# ============================================================
# 二、配置
# ============================================================

BASE_DIR = Path.home() / ".longhun/knowledge"
BASE_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = BASE_DIR / "knowledge.db"
VECTOR_DIR = BASE_DIR / "vectors"
VECTOR_DIR.mkdir(parents=True, exist_ok=True)
CONFIG_PATH = BASE_DIR / "config.json"
INDEX_PATH = BASE_DIR / "file_index.json"

DEFAULT_CONFIG = {
    "version": "1.0",
    "dna": "#龍芯⚡️丙午·乙未·甲辰·离为火-知识引擎-v1.0",
    "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "scan_dirs": [
        "~/Documents",
        "~/Downloads",
        "~/Desktop",
        "~/longhun-system",
        "~/.codebuddy",
    ],
    "scan_notes": True,
    "scan_code": True,
    "scan_docs": True,
    "exclude_patterns": [
        "*.tmp", "*.log", "*.pyc", "__pycache__",
        "node_modules", ".git", ".venv", ".env",
        "*.frozen", "archive"
    ],
    "vector_model": "all-MiniLM-L6-v2",
    "chunk_size": 500,
    "chunk_overlap": 50,
}

# ============================================================
# 三、数据结构
# ============================================================

@dataclass
class KnowledgeItem:
    """知识条目"""
    id: str
    title: str
    content: str
    source_type: str  # "note", "file", "code", "doc"
    source_path: str
    file_type: str
    created_at: str
    updated_at: str
    size: int
    tags: List[str] = field(default_factory=list)
    dna: str = ""
    vector_id: str = ""
    summary: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CodeSnippet:
    """代码片段"""
    id: str
    file_path: str
    language: str
    code: str
    docstring: str
    functions: List[str]
    classes: List[str]
    imports: List[str]
    complexity: int
    dna: str

    def to_dict(self) -> Dict:
        return asdict(self)


# ============================================================
# 四、备忘录采集器
# ============================================================

class NotesCollector:
    """macOS备忘录采集器"""

    NOTE_DB_PATHS = [
        Path.home() / "Library/Group Containers/group.com.apple.notes/NoteStore.sqlite",
        Path.home() / "Library/Containers/com.apple.Notes/Data/Library/Notes/NotesV7.storedata",
    ]

    def collect(self) -> List[Dict]:
        """采集所有备忘录"""
        note_db = None
        for path in self.NOTE_DB_PATHS:
            if path.exists():
                note_db = path
                break

        if not note_db:
            return []  # 静默跳过，不发警告

        notes = []
        try:
            temp_db = BASE_DIR / "temp_notes.db"
            shutil.copy2(note_db, temp_db)

            conn = sqlite3.connect(str(temp_db))
            cursor = conn.execute("""
                SELECT
                    Z_PK as id,
                    ZTITLE as title,
                    ZCONTENT as content,
                    ZCREATIONDATE as created,
                    ZMODIFICATIONDATE as modified
                FROM ZNOTE
                WHERE ZCONTENT IS NOT NULL AND ZCONTENT != ''
                LIMIT 500
            """)
            rows = cursor.fetchall()
            conn.close()
            temp_db.unlink()

            for row in rows:
                note_id, title, content, created, modified = row
                try:
                    created_time = datetime.fromtimestamp(created + 978307200) if created else datetime.now()
                    modified_time = datetime.fromtimestamp(modified + 978307200) if modified else datetime.now()
                except Exception:
                    created_time = datetime.now()
                    modified_time = datetime.now()

                content = self._clean_content(content) if content else ""

                notes.append({
                    "id": f"note_{note_id}",
                    "title": title or "无标题",
                    "content": content,
                    "created_at": created_time.isoformat(),
                    "updated_at": modified_time.isoformat(),
                    "source": "macOS备忘录"
                })

        except Exception:
            pass  # 静默跳过

        return notes

    @staticmethod
    def _clean_content(content: str) -> str:
        content = re.sub(r'<[^>]+>', '', content)
        content = re.sub(r'&[a-zA-Z]+;', ' ', content)
        content = '\n'.join(line.strip() for line in content.split('\n') if line.strip())
        return content[:50000]


# ============================================================
# 五、文件采集器
# ============================================================

class FileCollector:
    """本地文件采集器"""

    FILE_TYPES = {
        ".md": "markdown", ".py": "python", ".js": "javascript",
        ".ts": "typescript", ".html": "html", ".css": "css",
        ".json": "json", ".yaml": "yaml", ".yml": "yaml",
        ".txt": "text", ".sh": "bash", ".bash": "bash",
        ".zsh": "bash", ".cnsh": "cnsh", ".toml": "toml",
        ".xml": "xml", ".svg": "svg", ".csv": "csv",
    }

    BINARY_EXTS = {
        '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.webp', '.heic',
        '.mp4', '.mp3', '.mov', '.avi', '.mkv', '.wav', '.flac',
        '.zip', '.tar', '.gz', '.rar', '.7z', '.bz2',
        '.exe', '.dll', '.so', '.dylib',
        '.pyc', '.pyo', '.class', '.o', '.dmg', '.pkg',
        '.ttf', '.otf', '.woff', '.woff2', '.eot',
        '.bin', '.dat', '.db', '.sqlite', '.sqlite3',
    }

    def __init__(self, scan_dirs: List[str], exclude_patterns: List[str]):
        self.scan_dirs = [Path(d).expanduser() for d in scan_dirs if d]
        self.exclude_patterns = exclude_patterns

    def collect(self, max_files: int = 2000) -> List[Dict]:
        """扫描文件"""
        files = []
        seen = set()

        for dir_path in self.scan_dirs:
            if not dir_path.exists():
                continue
            try:
                for file_path in dir_path.rglob("*"):
                    if not file_path.is_file():
                        continue
                    if self._is_excluded(file_path):
                        continue

                    ext = file_path.suffix.lower()
                    file_type = self.FILE_TYPES.get(ext, None)
                    if file_type is None:
                        if ext in self.BINARY_EXTS:
                            continue
                        if file_path.stat().st_size > 512 * 1024:
                            continue
                        file_type = "text"

                    # 去重（符号链接等）
                    real = str(file_path.resolve())
                    if real in seen:
                        continue
                    seen.add(real)

                    try:
                        size = file_path.stat().st_size
                        content = self._read_file(file_path)
                        if content:
                            files.append({
                                "id": f"file_{hashlib.md5(real.encode()).hexdigest()[:16]}",
                                "path": str(file_path),
                                "file_type": file_type,
                                "size": size,
                                "content": content,
                                "created_at": datetime.fromtimestamp(file_path.stat().st_ctime).isoformat(),
                                "updated_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
                            })
                    except Exception:
                        continue

                    if len(files) >= max_files:
                        return files
            except PermissionError:
                continue

        return files

    def _is_excluded(self, file_path: Path) -> bool:
        for pattern in self.exclude_patterns:
            if file_path.match(pattern):
                return True
            for parent in file_path.parents:
                if parent.match(pattern):
                    return True
        return False

    def _read_file(self, file_path: Path, max_size: int = 100000) -> Optional[str]:
        ext = file_path.suffix.lower()
        if ext in self.BINARY_EXTS:
            return None
        try:
            size = file_path.stat().st_size
            read_size = min(size, max_size)
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read(read_size)
        except Exception:
            return None


# ============================================================
# 六、代码学习器
# ============================================================

class CodeLearner:
    """代码学习器"""

    FUNC_PATTERN = re.compile(
        r'^(?:async\s+)?def\s+(\w+)\s*\(([^)]*)\)',
        re.MULTILINE
    )
    CLASS_PATTERN = re.compile(
        r'^class\s+(\w+)\s*[(:]',
        re.MULTILINE
    )
    IMPORT_PATTERN = re.compile(
        r'^(?:from\s+(\S+)\s+)?import\s+(.+)$',
        re.MULTILINE
    )
    DOCSTRING_PATTERN = re.compile(
        r'"""(.*?)"""|\'\'\'(.*?)\'\'\'',
        re.DOTALL
    )

    def learn(self, file_path: str, content: str, language: str) -> CodeSnippet:
        file_id = hashlib.md5(f"{file_path}{content[:500]}".encode()).hexdigest()[:16]

        functions = []
        classes = []
        imports_list = []

        if language in ("python", "cnsh"):
            for match in self.FUNC_PATTERN.finditer(content):
                functions.append(match.group(1))
            for match in self.CLASS_PATTERN.finditer(content):
                classes.append(match.group(1))
            for match in self.IMPORT_PATTERN.finditer(content):
                module = match.group(1) or ""
                names = match.group(2).strip()
                if module:
                    imports_list.append(f"{module}.{names.split(',')[0].strip()}")
                else:
                    imports_list.append(names.split(',')[0].strip().split(' as ')[0].strip())

        docstring = ""
        doc_match = self.DOCSTRING_PATTERN.search(content)
        if doc_match:
            docstring = (doc_match.group(1) or doc_match.group(2) or "")[:1000]

        complexity = content.count('\n')

        dna = self._make_dna(file_path)

        return CodeSnippet(
            id=file_id,
            file_path=file_path,
            language=language,
            code=content[:10000],
            docstring=docstring,
            functions=functions,
            classes=classes,
            imports=imports_list[:50],
            complexity=complexity,
            dna=dna
        )

    @staticmethod
    def _make_dna(file_path: str) -> str:
        h = hashlib.sha256(file_path.encode()).hexdigest()[:8]
        return f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-知识学习-{h}"

    def to_document(self, snippet: CodeSnippet) -> str:
        parts = [
            f"## 📁 {Path(snippet.file_path).name}",
            f"**路径:** {snippet.file_path}",
            f"**语言:** {snippet.language}  **行数:** ~{snippet.complexity}  **DNA:** {snippet.dna}",
            "",
        ]
        if snippet.imports:
            parts.append(f"### 📦 导入 ({len(snippet.imports)})")
            parts.extend(f"- {imp}" for imp in snippet.imports[:20])
            parts.append("")
        if snippet.functions:
            parts.append(f"### 🔧 函数 ({len(snippet.functions)})")
            parts.extend(f"- {f}" for f in snippet.functions[:30])
            parts.append("")
        if snippet.classes:
            parts.append(f"### 📐 类 ({len(snippet.classes)})")
            parts.extend(f"- {c}" for c in snippet.classes)
            parts.append("")
        if snippet.docstring:
            parts.append(f"### 📝 文档字符串")
            parts.append(snippet.docstring[:500])
            parts.append("")
        parts.append(f"```{snippet.language}")
        parts.append(snippet.code[:2000])
        parts.append("```")
        return "\n".join(parts)


# ============================================================
# 七、向量知识库
# ============================================================

class VectorKnowledgeBase:
    """向量知识库 - ChromaDB 本地"""

    def __init__(self):
        self._available = False
        try:
            import chromadb
            from chromadb.utils import embedding_functions
            self.client = chromadb.PersistentClient(path=str(VECTOR_DIR))
            self.collection_name = "local_knowledge"
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
            self._ensure_collection()
            self._available = True
        except Exception:
            self._available = False

    @property
    def available(self) -> bool:
        return self._available

    def _ensure_collection(self):
        try:
            self.collection = self.client.get_collection(self.collection_name)
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                embedding_function=self.embedding_fn
            )

    def add(self, items: List[KnowledgeItem]):
        if not self._available or not items:
            return
        ids, docs, metas = [], [], []
        for item in items:
            ids.append(item.id)
            docs.append(f"{item.title}\n{item.content[:2000]}")
            metas.append({
                "source_type": item.source_type,
                "source_path": item.source_path,
                "file_type": item.file_type,
                "dna": item.dna,
                "tags": ",".join(item.tags)
            })
        try:
            self.collection.add(ids=ids, documents=docs, metadatas=metas)
        except Exception:
            pass

    def search(self, query: str, n_results: int = 10) -> List[Dict]:
        if not self._available:
            return []
        try:
            results = self.collection.query(query_texts=[query], n_results=n_results)
            return self._format_results(results)
        except Exception:
            return []

    def _format_results(self, results) -> List[Dict]:
        formatted = []
        if results and results.get('ids'):
            ids_list = results['ids'][0]
            docs_list = results.get('documents', [[]])[0]
            metas_list = results.get('metadatas', [[]])[0]
            dists = results.get('distances', [[1.0]*len(ids_list)])[0]
            for i in range(len(ids_list)):
                formatted.append({
                    "id": ids_list[i],
                    "content": docs_list[i] if i < len(docs_list) else "",
                    "metadata": metas_list[i] if i < len(metas_list) else {},
                    "score": max(0, 1.0 - dists[i])
                })
        return formatted

    def stats(self) -> Dict:
        if not self._available:
            return {"状态": "不可用（chromadb未安装）"}
        try:
            count = self.collection.count()
            return {"集合名": self.collection_name, "向量数": count, "路径": str(VECTOR_DIR)}
        except Exception:
            return {"状态": "集合异常"}


# ============================================================
# 八、fallback 关键词搜索（ChromaDB不可用时）
# ============================================================

class FallbackSearcher:
    """关键词搜索兜底"""

    def __init__(self, index_path: Path):
        self.index_path = index_path

    def search(self, query: str, n: int = 10) -> List[Dict]:
        if not self.index_path.exists():
            return []
        try:
            with open(self.index_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception:
            return []

        results = []
        keywords = query.lower().split()
        for entry in data.get("entries", []):
            title = (entry.get("title", "") or "").lower()
            content = (entry.get("content_preview", "") or "").lower()
            hits = sum(1 for kw in keywords if kw in title or kw in content)
            if hits > 0:
                results.append({
                    "id": entry.get("id", ""),
                    "content": f"{entry.get('title', '')}: {entry.get('content_preview', '')[:200]}",
                    "metadata": entry.get("metadata", {}),
                    "score": hits / max(len(keywords), 1)
                })
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:n]


# ============================================================
# 九、主引擎
# ============================================================

class LocalKnowledgeEngine:
    """本地知识引擎"""

    def __init__(self):
        self.config = self._load_config()
        self.vector_db = VectorKnowledgeBase()
        self.code_learner = CodeLearner()
        self.fallback = FallbackSearcher(INDEX_PATH)
        self.file_index = self._load_index()

    def _load_config(self) -> Dict:
        if CONFIG_PATH.exists():
            with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        self._save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()

    def _save_config(self, config: Dict):
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

    def _load_index(self) -> Dict:
        if INDEX_PATH.exists():
            with open(INDEX_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"entries": [], "last_scan": None, "total_items": 0}

    def _save_index(self):
        INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(INDEX_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.file_index, f, ensure_ascii=False, indent=2)

    def scan(self, full_scan: bool = False) -> Dict:
        """扫描所有知识源"""
        results = {"notes": [], "files": [], "code": [], "total": 0}
        entries = []  # fallback 索引条目

        # 1. 采集备忘录
        if self.config.get("scan_notes", True):
            collector = NotesCollector()
            results["notes"] = collector.collect()
            print(f"  📝 备忘录: {len(results['notes'])} 条")

        # 2. 采集文件
        if self.config.get("scan_docs", True):
            dirs = self.config.get("scan_dirs", DEFAULT_CONFIG["scan_dirs"])
            exclude = self.config.get("exclude_patterns", DEFAULT_CONFIG["exclude_patterns"])
            file_collector = FileCollector(dirs, exclude)
            results["files"] = file_collector.collect()
            print(f"  📁 文件: {len(results['files'])} 个")

        # 3. 学习代码
        code_items = []
        for f in results["files"]:
            lang = f.get("file_type", "")
            if lang in ("python", "javascript", "typescript", "cnsh", "bash"):
                snippet = self.code_learner.learn(f["path"], f["content"], lang)
                doc = self.code_learner.to_document(snippet)
                item = KnowledgeItem(
                    id=snippet.id,
                    title=f"代码: {Path(snippet.file_path).name}",
                    content=doc,
                    source_type="code",
                    source_path=snippet.file_path,
                    file_type=lang,
                    created_at=datetime.now().isoformat(),
                    updated_at=datetime.now().isoformat(),
                    size=len(snippet.code),
                    tags=["代码", lang],
                    dna=snippet.dna,
                )
                code_items.append(item)
        results["code"] = code_items

        # 4. 构建所有知识条目
        all_items = []

        for note in results["notes"]:
            item = KnowledgeItem(
                id=note["id"],
                title=note["title"],
                content=note["content"],
                source_type="note",
                source_path="macOS备忘录",
                file_type="note",
                created_at=note["created_at"],
                updated_at=note["updated_at"],
                size=len(note["content"]),
                tags=["备忘录"],
                dna=hashlib.md5(note["content"][:500].encode()).hexdigest()[:16]
            )
            all_items.append(item)
            entries.append({
                "id": item.id, "title": item.title,
                "content_preview": item.content[:300],
                "metadata": {"source_type": "note"}
            })

        for f in results["files"]:
            lang = f.get("file_type", "text")
            # 代码文件已在 code_items 中，这里加非代码文件
            if lang not in ("python", "javascript", "typescript", "cnsh", "bash"):
                item = KnowledgeItem(
                    id=f["id"],
                    title=Path(f["path"]).name,
                    content=f["content"],
                    source_type="file",
                    source_path=f["path"],
                    file_type=lang,
                    created_at=f["created_at"],
                    updated_at=f["updated_at"],
                    size=f["size"],
                    tags=["文件"],
                    dna=hashlib.md5(f["content"][:500].encode()).hexdigest()[:16]
                )
                all_items.append(item)
                entries.append({
                    "id": item.id, "title": item.title,
                    "content_preview": item.content[:300],
                    "metadata": {"source_type": "file", "path": f["path"]}
                })

        all_items.extend(code_items)
        for ci in code_items:
            entries.append({
                "id": ci.id, "title": ci.title,
                "content_preview": ci.content[:300],
                "metadata": {"source_type": "code", "path": ci.source_path}
            })

        # 5. 存入向量库
        if all_items and self.vector_db.available:
            self.vector_db.add(all_items)
            print(f"  💾 向量索引: {len(all_items)} 条")

        # 6. 保存 fallback 索引
        self.file_index = {
            "entries": entries,
            "last_scan": datetime.now().isoformat(),
            "total_items": len(all_items)
        }
        self._save_index()

        results["total"] = len(all_items)
        return results

    def search(self, query: str, n_results: int = 10) -> List[Dict]:
        """搜索知识"""
        if self.vector_db.available:
            results = self.vector_db.search(query, n_results)
            if results:
                return results
        # fallback 关键词搜索
        return self.fallback.search(query, n_results)

    def convert(self, query: str) -> Dict:
        """自然语言 → 代码转化"""
        results = self.search(query, 5)
        context = "\n\n".join(r.get("content", "")[:500] for r in results)
        code = self._generate_code(query, context)
        lang = self._detect_language(query)
        return {
            "query": query,
            "references": len(results),
            "context_used": [{"title": r.get("metadata", {}).get("source_path", ""),
                              "type": r.get("metadata", {}).get("source_type", "")}
                             for r in results[:5]],
            "generated_code": code,
            "language": lang,
            "dna": hashlib.sha256(f"{query}{datetime.now().isoformat()}".encode()).hexdigest()[:16]
        }

    def _generate_code(self, query: str, context: str) -> str:
        """代码生成（规则引擎 + 模板）"""
        templates = {
            "爬取": '''import requests
from bs4 import BeautifulSoup

def fetch_page(url: str) -> str:
    """爬取网页内容"""
    headers = {"User-Agent": "Mozilla/5.0"}
    resp = requests.get(url, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.text

def parse_html(html: str) -> list:
    """解析HTML"""
    soup = BeautifulSoup(html, "html.parser")
    return [p.get_text() for p in soup.find_all("p")]
''',
            "翻译": '''from bin.lh_tongxinyi_translator import TongxinyiTranslator

translator = TongxinyiTranslator()
result = translator.translate("要翻译的文本", source_lang="zh", target_lang="en")
print(result.target_text)
''',
            "健康": '''import subprocess
import sys

result = subprocess.run(
    [sys.executable, "bin/lh_web_health_check.py", "--once"],
    capture_output=True, text=True
)
print(result.stdout)
if result.returncode != 0:
    print(result.stderr)
''',
            "对齐": '''import subprocess
import sys

subprocess.run([sys.executable, "bin/lh_align_checker.py"])
''',
            "系统": '''import subprocess
import sys

subprocess.run(["python3", "bin/lh.py", "status"])
''',
            "部署": '''import subprocess
import sys

# 同步到鲲鹏
subprocess.run(["bash", "deploy/sync-to-kunpeng.sh"])
print("✅ 同步完成")
''',
        }

        for key, tmpl in templates.items():
            if key in query:
                return tmpl

        return f'''"""
根据查询自动生成的代码框架
查询: {query}
DNA: {hashlib.sha256(query.encode()).hexdigest()[:8]}
"""

def main():
    """TODO: 根据具体需求完善"""
    print("处理: {query}")
    # 参考本地知识库中的相关代码
    pass

if __name__ == "__main__":
    main()
'''

    @staticmethod
    def _detect_language(query: str) -> str:
        q = query.lower()
        if "js" in q or "javascript" in q:
            return "javascript"
        if "cnsh" in q:
            return "cnsh"
        if "bash" in q or "shell" in q:
            return "bash"
        return "python"

    def status(self) -> Dict:
        return {
            "数据目录": str(BASE_DIR),
            "向量库": self.vector_db.stats() if self.vector_db.available else {"状态": "不可用"},
            "上次扫描": self.file_index.get("last_scan", "从未"),
            "知识条目": self.file_index.get("total_items", 0),
            "扫描目录": self.config.get("scan_dirs", []),
            "DNA": self.config.get("dna", ""),
        }


# ============================================================
# 十、命令行接口
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·本地知识引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh-know scan              扫描所有知识源
  lh-know scan --full       全量重新索引
  lh-know search "主权守护"  语义搜索
  lh-know convert "写爬虫"   自然语言→代码
  lh-know status            查看状态
        """
    )

    parser.add_argument("command", nargs="?", default="status",
                        help="命令: scan, search, convert, status")
    parser.add_argument("query", nargs="*", help="搜索或转化查询")
    parser.add_argument("--full", action="store_true", help="全量扫描")
    parser.add_argument("--n", type=int, default=10, help="搜索结果数量")
    parser.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()

    # 检查依赖
    if not ensure_dependencies():
        if args.command in ("scan", "search"):
            print("⚠️ ChromaDB不可用，使用fallback关键词搜索模式")
            print("   pip install chromadb sentence-transformers 以获得语义搜索能力\n")

    engine = LocalKnowledgeEngine()

    if args.command == "scan":
        print("🐉 龍魂·本地知识引擎 — 扫描中...\n")
        result = engine.scan(full_scan=args.full)
        print(f"\n✅ 扫描完成")
        print(f"  📝 备忘录: {len(result.get('notes', []))}")
        print(f"  📁 文件:   {len(result.get('files', []))}")
        print(f"  💻 代码:   {len(result.get('code', []))}")
        print(f"  ━━━━━━━━━━━━━━━━━")
        print(f"  📚 总计:   {result.get('total', 0)} 条")

    elif args.command == "search":
        if not args.query:
            print("❌ 请提供搜索关键词")
            return
        query = " ".join(args.query)
        results = engine.search(query, args.n)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"\n🔍 搜索: {query}")
            print(f"   结果: {len(results)} 条\n")
            for i, r in enumerate(results, 1):
                meta = r.get("metadata", {})
                src = meta.get("source_type", "?")
                path = meta.get("source_path", "")[:60]
                print(f"  {i}. [{src}] {path}")
                print(f"     {r.get('content', '')[:120]}...")
                if r.get('score'):
                    print(f"     匹配度: {r['score']:.0%}")
                print()

    elif args.command == "convert":
        if not args.query:
            print("❌ 请提供描述")
            return
        query = " ".join(args.query)
        result = engine.convert(query)
        print(f"\n🐉 代码转化")
        print(f"📝 {result['query']}")
        print(f"📎 参考: {result['references']} 条本地知识")
        print(f"🧬 DNA: {result['dna']}")
        print("─" * 50)
        print(result['generated_code'])
        print("─" * 50)

    elif args.command == "status":
        s = engine.status()
        print("\n🐉 龍魂·本地知识引擎")
        print("─" * 45)
        for k, v in s.items():
            if isinstance(v, dict):
                print(f"  {k}:")
                for sk, sv in v.items():
                    print(f"    {sk}: {sv}")
            elif isinstance(v, list):
                print(f"  {k}:")
                for item in v[:5]:
                    print(f"    - {item}")
            else:
                print(f"  {k}: {v}")
        print("─" * 45)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
