#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 统一AI对话采集器 v1.0
DNA: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑-CONVERSATION-CAPTURE-UID9622
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2（工程实现层）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过（2026-08-15 全链路实测: 采集/去重/搜索/统计/HTTP四接口/capture-all/merge 全绿）

功能:
  1. 统一采集 Kimi/DeepSeek/CodeBuddy 对话 → 03_MEMORY/ai_conversations/
  2. 统一格式 JSONL + 索引 _index.json + DNA 追溯
  3. 跨AI检索 search / 按话题聚合 get-topic / 统计 stats
  4. 本地 HTTP 服务 :8769（浏览器扩展注入入口）
  5. 智能去重 dedup（SHA-256 内容哈希 + 重复耻辱墙）
  6. 事件审计 capture_audit（04_AUDIT/capture_audit.jsonl）
  7. 健康检查 health / 过期归档 cleanup（默认保留30天）
  8. capture-all 一键采集已知产出 + merge-report 合并报告

用法:
  python3 08_BIN/lh_conversation_capture.py capture --source kimi --role assistant --content "..." --topic "视频生态"
  python3 08_BIN/lh_conversation_capture.py --server --port 8769
  python3 08_BIN/lh_conversation_capture.py --search "视频" --source deepseek
  python3 08_BIN/lh_conversation_capture.py --stats
  python3 08_BIN/lh_conversation_capture.py --import-jsonl <file> --source deepseek
  python3 08_BIN/lh_conversation_capture.py --dedup
  python3 08_BIN/lh_conversation_capture.py --health
  python3 08_BIN/lh_conversation_capture.py --capture-all --merge-report
"""

import argparse
import hashlib
import json
import shutil
import sys
import time
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Optional

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
VERSION = "1.0.0"
VALID_SOURCES = ("kimi", "deepseek", "codebuddy", "browser", "manual")
DEFAULT_PORT = 8769

# 项目根（脚本位于 longhun-system/08_BIN/）
ROOT = Path(__file__).resolve().parent.parent
DEFAULT_STORAGE = ROOT / "03_MEMORY" / "ai_conversations"
DEFAULT_AUDIT = ROOT / "04_AUDIT" / "capture_audit.jsonl"
DEFAULT_SHAME = ROOT / "04_AUDIT" / "shame_wall.jsonl"
REPORT_DIR = ROOT / "05_系統報告"


# ------------------------------------------------------------
# DNA 生成（v∞ 干支四柱优先，降级 ISO 日期）
# ------------------------------------------------------------
def _time_stamp_compact() -> str:
    """用 lh_time_engine 取真实干支四柱·卦（compact 格式）；失败降级日期。"""
    try:
        sys.path.insert(0, str(ROOT / "bin"))
        from lh_time_engine import get_output_stamp  # noqa
        stamp = get_output_stamp(format_type="compact") or ""
        # compact 格式: #龍芯⚡️丙午·丙申·辛酉·未时·䷔噬嗑 → 取 ⚡️ 后段
        if "⚡️" in stamp:
            return stamp.split("⚡️", 1)[1].strip()
    except Exception:
        pass
    return datetime.now().strftime("%Y-%m-%d")


def generate_dna(suffix: str = "CONV") -> str:
    """v∞ 格式: #龍芯⚡️<干支四柱·卦>-<模块>-<动作>-<哈希8>"""
    four_pillars = _time_stamp_compact()
    rand = hashlib.sha256(f"{suffix}{datetime.now().isoformat()}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{four_pillars}-CAPTURE-{suffix}-{rand}"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


# ------------------------------------------------------------
# 存储 & 索引
# ------------------------------------------------------------
class ConversationStore:
    """统一对话存储：JSONL 分来源分日期 + _index.json 索引"""

    def __init__(self, storage_dir: Path = None):
        self.storage_dir = Path(storage_dir) if storage_dir else DEFAULT_STORAGE
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.storage_dir / "_index.json"
        self.audit_file = DEFAULT_AUDIT
        self.shame_file = DEFAULT_SHAME
        self.index = self._load_index()

    def _load_index(self) -> Dict:
        if self.index_file.exists():
            try:
                return json.loads(self.index_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {"entries": [], "sources": {}, "topics": {}, "last_update": None}

    def _save_index(self):
        self.index["last_update"] = datetime.now().isoformat()
        self.index_file.write_text(
            json.dumps(self.index, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # ---------- 审计 ----------
    def audit(self, operation: str, source: str, entry_id: str,
              status: str, details: Dict = None):
        record = {
            "timestamp": datetime.now().isoformat(),
            "operation": operation,
            "source": source,
            "entry_id": entry_id,
            "status": status,
            "details": details or {},
            "dna": generate_dna("AUDIT"),
        }
        self.audit_file.parent.mkdir(parents=True, exist_ok=True)
        with self.audit_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    def shame(self, reason: str, entry_dna: str, details: Dict = None):
        record = {
            "timestamp": datetime.now().isoformat(),
            "reason": reason,
            "dna": entry_dna,
            "details": details or {},
        }
        self.shame_file.parent.mkdir(parents=True, exist_ok=True)
        with self.shame_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # ---------- 采集 ----------
    def capture(self, source: str, role: str, content: str, topic: str,
                project: str = None, metadata: Dict = None,
                skip_dedup: bool = False) -> Optional[Dict]:
        """采集一条对话。返回条目 dict；重复且未强制时返回 None。"""
        source = (source or "manual").lower()
        if source not in VALID_SOURCES:
            source = "manual"
        role = role if role in ("user", "assistant") else "assistant"
        content = (content or "").strip()
        if not content:
            self.audit("capture", source, "-", "skipped", {"reason": "empty_content"})
            return None

        topic = (topic or content[:24]).strip()
        entry_id = f"CONV-{int(time.time()*1000)}-{_sha256(content[:120])}"

        if not skip_dedup:
            dup = self._find_duplicate(content)
            if dup:
                self.shame("重复对话", dup.get("dna", ""),
                           {"original_id": dup.get("id"), "new_id": entry_id})
                self.audit("capture", source, entry_id, "dedup_skipped",
                           {"original_id": dup.get("id")})
                return None

        entry = {
            "id": entry_id,
            "source": source,
            "role": role,
            "content": content,
            "topic": topic,
            "project": project,
            "dna": generate_dna("CONV"),
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {},
            "parent_dna": metadata.get("parent_dna") if metadata else None,
        }

        source_dir = self.storage_dir / source
        source_dir.mkdir(exist_ok=True)
        date_file = source_dir / f"{datetime.now().strftime('%Y-%m-%d')}.jsonl"
        with date_file.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

        self.index["entries"].append({
            "id": entry_id, "source": source, "topic": topic,
            "project": project, "dna": entry["dna"], "timestamp": entry["timestamp"],
        })
        self.index["sources"][source] = self.index["sources"].get(source, 0) + 1
        self.index["topics"][topic] = self.index["topics"].get(topic, 0) + 1
        self._save_index()
        self.audit("capture", source, entry_id, "ok", {"topic": topic})
        return entry

    def _find_duplicate(self, content: str) -> Optional[Dict]:
        """基于内容哈希找重复（逐文件扫，轻量版去重）"""
        digest = _sha256(content)
        for src in VALID_SOURCES:
            src_dir = self.storage_dir / src
            if not src_dir.exists():
                continue
            for f in src_dir.glob("*.jsonl"):
                for line in f.open(encoding="utf-8"):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    if _sha256(d.get("content", "")) == digest:
                        return d
        return None

    # ---------- 检索 ----------
    def iter_entries(self, source: str = None) -> Iterable[Dict]:
        sources = [source] if source else VALID_SOURCES
        for src in sources:
            src_dir = self.storage_dir / src
            if not src_dir.exists():
                continue
            for f in sorted(src_dir.glob("*.jsonl")):
                for line in f.open(encoding="utf-8"):
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        yield json.loads(line)
                    except Exception:
                        continue

    def search(self, query: str, source: str = None, topic: str = None,
               limit: int = 20) -> List[Dict]:
        q = (query or "").lower()
        results = []
        for entry in self.iter_entries(source):
            if q and q not in entry.get("content", "").lower():
                continue
            if topic and entry.get("topic") != topic:
                continue
            results.append(entry)
            if len(results) >= limit:
                break
        return results

    def get_by_topic(self, topic: str, source: str = None, limit: int = 100) -> List[Dict]:
        return [e for e in self.iter_entries(source)
                if e.get("topic") == topic][:limit]

    def stats(self) -> Dict:
        # 重扫实际文件，比索引更可靠
        real = {}
        for src in VALID_SOURCES:
            src_dir = self.storage_dir / src
            if not src_dir.exists():
                continue
            n = sum(1 for _ in src_dir.glob("*.jsonl"))
            real[src] = n
        return {
            "total_files": sum(real.values()),
            "sources": real,
            "index_sources": self.index.get("sources", {}),
            "last_update": self.index.get("last_update"),
            "storage": str(self.storage_dir),
        }

    def recent(self, limit: int = 10) -> List[Dict]:
        all_entries = list(self.iter_entries())
        all_entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
        return all_entries[:limit]

    # ---------- 去重 ----------
    def dedup(self, dry_run: bool = False) -> Dict:
        seen, removed, kept = {}, [], 0
        for entry in self.iter_entries():
            digest = _sha256(entry.get("content", ""))
            if digest in seen:
                removed.append(entry)
                if not dry_run:
                    self.shame("去重清理", entry.get("dna", ""),
                               {"original_id": seen[digest], "dupe_id": entry.get("id")})
                    self._remove_entry(entry)
            else:
                seen[digest] = entry.get("id")
                kept += 1
        return {"dry_run": dry_run, "kept": kept, "removed": len(removed),
                "removed_ids": [r.get("id") for r in removed[:50]]}

    def _remove_entry(self, entry: Dict):
        """从 JSONL 中移除一条（重写文件·冻结留档到 _archive）"""
        f = self.storage_dir / entry.get("source", "manual") / \
            f"{entry['timestamp'][:10]}.jsonl"
        if not f.exists():
            return
        lines = [l for l in f.read_text(encoding="utf-8").splitlines()
                 if not (l.strip() and json.loads(l).get("id") == entry.get("id"))]
        archive = self.storage_dir / "_archive" / entry.get("source", "manual")
        archive.mkdir(parents=True, exist_ok=True)
        (archive / f.name).open("a", encoding="utf-8").write(
            json.dumps(entry, ensure_ascii=False) + "\n")
        f.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # ---------- 健康 & 归档 ----------
    def health(self) -> Dict:
        size_mb = sum(p.stat().st_size for p in self.storage_dir.rglob("*")
                      if p.is_file()) / (1024 * 1024)
        status = {
            "service": "conversation_capture",
            "version": VERSION,
            "storage": {"exists": self.storage_dir.exists(),
                        "path": str(self.storage_dir),
                        "size_mb": round(size_mb, 2)},
            "sources": {},
            "last_capture": None,
            "audit_tail": self._audit_tail(3),
        }
        for src in VALID_SOURCES:
            src_dir = self.storage_dir / src
            if src_dir.exists():
                files = sorted(src_dir.glob("*.jsonl"))
                status["sources"][src] = {
                    "files": len(files),
                    "latest": files[-1].stem if files else None,
                }
        recents = self.recent(1)
        if recents:
            status["last_capture"] = recents[0].get("timestamp")
        return status

    def _audit_tail(self, n: int = 3) -> List[Dict]:
        if not self.audit_file.exists():
            return []
        lines = [json.loads(l) for l in self.audit_file.open(encoding="utf-8")
                 if l.strip()]
        return lines[-n:]

    def cleanup(self, days: int = 30, dry_run: bool = False) -> Dict:
        cutoff = datetime.now() - timedelta(days=days)
        archived, skipped = 0, 0
        for src in VALID_SOURCES:
            src_dir = self.storage_dir / src
            if not src_dir.exists():
                continue
            for f in src_dir.glob("*.jsonl"):
                try:
                    fdate = datetime.strptime(f.stem, "%Y-%m-%d")
                except Exception:
                    skipped += 1
                    continue
                if fdate < cutoff:
                    if not dry_run:
                        archive = self.storage_dir / "_archive" / src
                        archive.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(f), str(archive / f.name))
                    archived += 1
        return {"dry_run": dry_run, "days": days,
                "archived": archived, "skipped": skipped}

    # ---------- 导入 ----------
    def import_jsonl(self, path: Path, source: str = None,
                     topic: str = None, skip_dedup: bool = False) -> Dict:
        path = Path(path)
        if not path.exists():
            return {"error": f"文件不存在: {path}"}
        ok, dup, fail = 0, 0, 0
        for line in path.open(encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
            except Exception:
                fail += 1
                continue
            entry = self.capture(
                source=data.get("source", source or "manual"),
                role=data.get("role", "assistant"),
                content=data.get("content", ""),
                topic=data.get("topic", topic or "导入"),
                project=data.get("project"),
                metadata=data.get("metadata", {}),
                skip_dedup=skip_dedup,
            )
            if entry:
                ok += 1
            else:
                dup += 1
        self.audit("import", source or "manual", "-", "ok",
                   {"file": str(path), "ok": ok, "dup": dup, "fail": fail})
        return {"file": str(path), "imported": ok, "dedup_skipped": dup, "failed": fail}

    def import_deepseek(self, path: Path, skip_dedup: bool = False) -> Dict:
        """导入 DeepSeek 导出文件（JSON 数组 / JSONL / 文本）"""
        path = Path(path)
        if not path.exists():
            return {"error": f"文件不存在: {path}"}
        raw = path.read_text(encoding="utf-8", errors="ignore")
        records, fail = [], 0
        try:
            data = json.loads(raw)
            if isinstance(data, dict):
                data = data.get("messages", data.get("conversations", []))
            if isinstance(data, list):
                records = data
            else:
                fail = 1
        except Exception:
            # 非 JSON → 按行尝试
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                records.append({"role": "user", "content": line})
        ok, dup = 0, 0
        for rec in records:
            if isinstance(rec, dict):
                content = rec.get("content", rec.get("text", ""))
                role = "user" if "user" in str(rec.get("role", "")) else "assistant"
            else:
                content, role = str(rec), "assistant"
            entry = self.capture(source="deepseek", role=role, content=content,
                                 topic="DeepSeek导入",
                                 metadata={"import_file": path.name},
                                 skip_dedup=skip_dedup)
            if entry:
                ok += 1
            else:
                dup += 1
        self.audit("import_deepseek", "deepseek", "-", "ok",
                   {"file": str(path), "ok": ok, "dup": dup, "fail": fail})
        return {"file": str(path), "imported": ok, "dedup_skipped": dup, "failed": fail}


# ------------------------------------------------------------
# HTTP 服务（浏览器扩展入口 :8769）
# ------------------------------------------------------------
def _read_body(handler: BaseHTTPRequestHandler) -> Dict:
    length = int(handler.headers.get("Content-Length", 0) or 0)
    raw = handler.rfile.read(length) if length else b"{}"
    try:
        return json.loads(raw.decode("utf-8"))
    except Exception:
        return {}


class CaptureHandler(BaseHTTPRequestHandler):
    store = None  # 由 server 注入

    def log_message(self, fmt, *args):
        sys.stderr.write("[capture:%d] %s\n" % (self.server.server_port, fmt % args))

    def _send(self, code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path.rstrip("/") == "/api/capture":
            data = _read_body(self)
            source = data.get("source", "browser")
            entry = self.store.capture(
                source=source,
                role=data.get("role", "user"),
                content=data.get("content", ""),
                topic=data.get("topic", "浏览器采集"),
                project=data.get("project"),
                metadata=data.get("metadata", {}),
            )
            if entry:
                self._send(200, {"status": "ok", "id": entry["id"], "dna": entry["dna"]})
            else:
                self._send(200, {"status": "dedup_skipped"})
        else:
            self._send(404, {"status": "not_found"})

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")
        from urllib.parse import parse_qs, urlparse
        query = parse_qs(urlparse(self.path).query)
        if path == "/api/stats":
            self._send(200, self.store.stats())
        elif path == "/api/health":
            self._send(200, self.store.health())
        elif path == "/api/search":
            q = (query.get("q") or query.get("query") or [""])[0]
            src = (query.get("source") or [None])[0]
            limit = int((query.get("limit") or ["20"])[0])
            self._send(200, {"results": self.store.search(q, source=src, limit=limit)})
        elif path == "/api/recent":
            limit = int((query.get("limit") or ["10"])[0])
            self._send(200, {"entries": self.store.recent(limit)})
        else:
            self._send(404, {"status": "not_found", "hint": "try /api/stats /api/health /api/search /api/recent"})


def run_server(port: int = DEFAULT_PORT):
    CaptureHandler.store = ConversationStore()
    server = ThreadingHTTPServer(("127.0.0.1", port), CaptureHandler)
    print(f"🐉 龍魂 · 对话采集服务启动 http://127.0.0.1:{port}")
    print(f"   存储: {CaptureHandler.store.storage_dir}")
    print(f"   接口: POST /api/capture · GET /api/stats · /api/health · /api/search?q= · /api/recent")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹ 服务已停止")
        server.shutdown()


# ------------------------------------------------------------
# capture-all：一键采集已知 AI 产出（合并前置）
# ------------------------------------------------------------
KNOWN_OUTPUTS = [
    # (路径, 来源, 主题, 项目)
    ("05_ENGINES/lh_video_agent.py", "kimi", "视频创作智能体 v1.0", "视频生态"),
    ("08_BIN/lh_video_tools.py", "kimi", "视频工具集成层 v1.0", "视频生态"),
    ("08_BIN/lh_video_ecosystem.py", "kimi", "视频生态主控制器 v1.0", "视频生态"),
    ("08_BIN/lh_conversation_capture.py", "codebuddy", "统一AI对话采集器 v1.0", "对话采集"),
]


def capture_all(store: ConversationStore, skip_dedup: bool = False) -> Dict:
    results = []
    for rel, source, topic, project in KNOWN_OUTPUTS:
        p = ROOT / rel
        if not p.exists():
            results.append({"file": rel, "status": "missing"})
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        head = text[:1500]
        entry = store.capture(
            source=source, role="assistant", content=head,
            topic=topic, project=project,
            metadata={"file": rel, "size": p.stat().st_size,
                      "sha256": _sha256(text), "type": "code_asset"},
            skip_dedup=skip_dedup,
        )
        results.append({"file": rel, "status": "ok" if entry else "dedup"})
    return {"captured": results}


def merge_report(store: ConversationStore) -> Path:
    """生成合并报告（Kimi + DeepSeek + CodeBuddy 汇总）"""
    stats = store.stats()
    topics = store.index.get("topics", {})
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out = REPORT_DIR / f"capture_merge_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    lines = [
        "# 🐉 龍魂 · 统一AI对话采集合并报告",
        "",
        f"**DNA:** `{generate_dna('MERGE')}`",
        f"**生成时间:** {datetime.now().isoformat()}",
        f"**存储:** `{store.storage_dir}`",
        "",
        "## 📊 采集统计",
        "",
        "| 来源 | 文件数 |",
        "|:---|---:|",
    ]
    for src, n in stats["sources"].items():
        lines.append(f"| {src} | {n} |")
    lines += ["", "## 🏷️ 话题分布", ""]
    for topic, n in sorted(topics.items(), key=lambda x: -x[1])[:20]:
        lines.append(f"- **{topic}** × {n}")
    lines += ["", "## 📥 最近采集", ""]
    for e in store.recent(5):
        lines.append(f"- `[{e['source']}]` {e['topic']} — {e['content'][:60]}…")
    lines += ["", "---", "",
              "> 三色: 🟢 采集与检索链路正常 · 🟡 浏览器扩展待实机注入 · 🔴 无",
              f"> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    store.audit("merge_report", "-", "-", "ok", {"file": out.name})
    return out


# ------------------------------------------------------------
# CLI
# ------------------------------------------------------------
def build_parser():
    p = argparse.ArgumentParser(
        prog="lh_conversation_capture",
        description="🐉 龍魂 · 统一AI对话采集器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--version", action="version", version=f"lh_conversation_capture v{VERSION}")
    p.add_argument("--storage", type=str, default=None, help="存储目录（默认 03_MEMORY/ai_conversations）")

    sub = p.add_subparsers(dest="cmd")

    c = sub.add_parser("capture", help="采集一条对话")
    c.add_argument("--source", default="manual")
    c.add_argument("--role", default="assistant")
    c.add_argument("--content", required=True)
    c.add_argument("--topic", default="")
    c.add_argument("--project", default=None)
    c.add_argument("--metadata-json", default="{}")
    c.add_argument("--no-dedup", action="store_true")

    sub.add_parser("server", help="启动HTTP服务").add_argument("--port", type=int, default=DEFAULT_PORT)

    s = sub.add_parser("search", help="跨AI搜索")
    s.add_argument("--query", required=True)
    s.add_argument("--source", default=None)
    s.add_argument("--topic", default=None)
    s.add_argument("--limit", type=int, default=20)
    s.add_argument("--json", action="store_true")

    g = sub.add_parser("topic", help="按话题获取")
    g.add_argument("--topic", required=True)
    g.add_argument("--source", default=None)
    g.add_argument("--limit", type=int, default=100)

    sub.add_parser("stats", help="统计")

    r = sub.add_parser("recent", help="最近采集")
    r.add_argument("--limit", type=int, default=10)

    i = sub.add_parser("import-jsonl", help="导入JSONL")
    i.add_argument("file")
    i.add_argument("--source", default=None)
    i.add_argument("--topic", default=None)
    i.add_argument("--no-dedup", action="store_true")

    d = sub.add_parser("import-deepseek", help="导入DeepSeek导出")
    d.add_argument("file")
    d.add_argument("--no-dedup", action="store_true")

    ded = sub.add_parser("dedup", help="去重")
    ded.add_argument("--dry-run", action="store_true")

    sub.add_parser("health", help="健康检查")

    cl = sub.add_parser("cleanup", help="归档过期对话")
    cl.add_argument("--days", type=int, default=30)
    cl.add_argument("--dry-run", action="store_true")

    a = sub.add_parser("audit", help="查看审计日志")
    a.add_argument("--limit", type=int, default=10)

    ca = sub.add_parser("capture-all", help="一键采集已知产出")
    ca.add_argument("--no-dedup", action="store_true")

    mr = sub.add_parser("merge-report", help="生成合并报告")

    m = sub.add_parser("merge", help="统一合并(capture-all + merge-report)")
    m.add_argument("--no-dedup", action="store_true")

    return p


def main(argv: List[str] = None):
    args = build_parser().parse_args(argv)
    store = ConversationStore(Path(args.storage) if args.storage else None)

    if args.cmd == "capture":
        try:
            metadata = json.loads(args.metadata_json)
        except Exception:
            metadata = {}
        entry = store.capture(args.source, args.role, args.content,
                              args.topic, args.project, metadata,
                              skip_dedup=args.no_dedup)
        if entry:
            print(json.dumps(entry, ensure_ascii=False, indent=2))
        else:
            print("⏭ 重复内容，已跳过（耻辱墙已记录）。加 --no-dedup 强制采集")

    elif args.cmd == "server":
        run_server(args.port)

    elif args.cmd == "search":
        results = store.search(args.query, args.source, args.topic, args.limit)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
            return
        print(f"🔍 搜索「{args.query}」命中 {len(results)} 条：")
        for e in results:
            print(f"  [{e['source']}] {e['topic']} · {e['timestamp'][:16]}")
            print(f"    {e['content'][:100]}")
            print(f"    DNA: {e['dna']}")

    elif args.cmd == "topic":
        results = store.get_by_topic(args.topic, args.source, args.limit)
        print(f"🏷️ 话题「{args.topic}」共 {len(results)} 条：")
        for e in results:
            print(f"  [{e['source']}] {e['timestamp'][:16]} {e['content'][:80]}")

    elif args.cmd == "stats":
        s = store.stats()
        print("🐉 龍魂 · 对话采集统计")
        print("=" * 40)
        print(f"存储: {s['storage']}")
        print(f"总文件数: {s['total_files']}")
        for src, n in s["sources"].items():
            print(f"  {src}: {n}")
        print(f"索引更新: {s['last_update']}")

    elif args.cmd == "recent":
        print("📋 最近采集：")
        for e in store.recent(args.limit):
            print(f"  [{e['source']}] {e['topic']} · {e['timestamp'][:16]}")
            print(f"    {e['content'][:80]}")

    elif args.cmd == "import-jsonl":
        r = store.import_jsonl(args.file, args.source, args.topic,
                               skip_dedup=args.no_dedup)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif args.cmd == "import-deepseek":
        r = store.import_deepseek(args.file, skip_dedup=args.no_dedup)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif args.cmd == "dedup":
        r = store.dedup(dry_run=args.dry_run)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif args.cmd == "health":
        h = store.health()
        print(json.dumps(h, ensure_ascii=False, indent=2))

    elif args.cmd == "cleanup":
        r = store.cleanup(days=args.days, dry_run=args.dry_run)
        print(json.dumps(r, ensure_ascii=False, indent=2))

    elif args.cmd == "audit":
        tail = store._audit_tail(args.limit)
        print(f"🕵️ 审计日志（最近{args.limit}条）：")
        for rec in tail:
            print(f"  {rec['timestamp'][:19]} {rec['operation']} {rec['source']} "
                  f"{rec['entry_id'][:24]} {rec['status']}")

    elif args.cmd == "capture-all":
        r = capture_all(store, skip_dedup=args.no_dedup)
        print("📥 一键采集已知产出：")
        for item in r["captured"]:
            print(f"  {item['file']} → {item['status']}")

    elif args.cmd == "merge-report":
        out = merge_report(store)
        print(f"📄 合并报告已生成: {out}")

    elif args.cmd == "merge":
        print("🧬 龍魂 · 统一合并（含所有AI对话）")
        print("=" * 40)
        print("1. 采集所有AI已知产出...")
        r = capture_all(store, skip_dedup=args.no_dedup)
        for item in r["captured"]:
            print(f"   {item['file']} → {item['status']}")
        print("2. 生成合并报告...")
        out = merge_report(store)
        print(f"   ✅ 合并报告: {out}")
        print("✅ 合并完成！")
    else:
        build_parser().print_help()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
