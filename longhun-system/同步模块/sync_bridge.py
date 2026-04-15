#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
sync_bridge.py  —  龍魂三路只读对接桥
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Copyright © 2026 UID9622 诸葛鑫（龍芯北辰）
Licensed under the Apache License, Version 2.0

作者：UID9622 诸葛鑫（龍芯北辰）
创作地：中华人民共和国
GPG指纹：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导：曾仕强老师（永恒显示）
DNA追溯码：#龍芯⚡️20260311-SYNC-BRIDGE-v1.0
确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。

献礼：新中国成立77周年（1949-2026）· 丙午马年
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

架构：Local ←→ Notion ←→ Claude（三路只读，主权在手）

                 ┌─────────────────────────────────────┐
                 │           SyncBridge                │
                 │                                     │
   本地文件系统  ◄──┤  LocalReader    AuditEvent链      ├──► ~/.env 密钥
                 │                                     │
   Notion API   ◄──┤  NotionReader   IntentPacket封装   ├──► 密钥在本地
                 │                                     │
   Claude API   ◄──┤  ClaudeAligner  DNA戳+三色审计     ├──► 密钥在本地
                 └─────────────────────────────────────┘

核心原则：
  ① Local First  — 一切从本地读，不自动上传
  ② 只读默认     — 所有写操作需要二次确认 + AuditEvent
  ③ 密钥在手     — 从 ~/.env 读取，不硬编码，不提交 git
  ④ Append-only  — 审计日志只追加不覆盖
  ⑤ DNA追溯     — 每个操作都有 DNA 戳

用法：
  python3 sync_bridge.py status          # 三路连接状态
  python3 sync_bridge.py read local      # 读本地摘要
  python3 sync_bridge.py read notion     # 读 Notion 页面列表
  python3 sync_bridge.py read claude     # Claude 对齐检测
  python3 sync_bridge.py align           # 三路对齐报告
  python3 sync_bridge.py audit           # 查看 AuditEvent 链
  python3 sync_bridge.py intent "意图"   # IntentPacket 封装 + 大白话流水线
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.request
import urllib.error
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

# ─── 环境 & 常量 ──────────────────────────────────────────────────────────────

BASE     = Path.home() / "longhun-system"
ENV_FILE = BASE / ".env"
AUDIT_DB = BASE / "logs" / "audit_events.jsonl"   # AuditEvent 专用日志（区别于 audit_log.jsonl）
TZ_CN    = timezone(timedelta(hours=8))
GPG_FP   = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM  = "#CONFIRM\U0001f30c9622-ONLY-ONCE\U0001f9ecLK9X-772Z"
DNA_PRE  = "#龍芯⚡️"
UID      = "9622"

BASE.mkdir(exist_ok=True)
(BASE / "logs").mkdir(exist_ok=True)

# ─── .env 加载（密钥永远在本地） ─────────────────────────────────────────────

def load_env() -> dict[str, str]:
    """从 ~/.longhun-system/.env 读取，不污染系统环境变量。"""
    env: dict[str, str] = {}
    if not ENV_FILE.exists():
        return env
    for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" in line:
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip().strip("'\"")
    return env

ENV = load_env()

def get_key(name: str) -> Optional[str]:
    v = ENV.get(name) or os.environ.get(name)
    if not v or v.startswith("sk-ant-填") or v.startswith("填入"):
        return None
    return v

# ─── 工具 ─────────────────────────────────────────────────────────────────────

def now_cn(fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    return datetime.now(tz=TZ_CN).strftime(fmt)

def now_iso() -> str:
    return datetime.now(tz=TZ_CN).isoformat()

def short_hash(text: str, n: int = 8) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:n].upper()

def gen_dna(tag: str, content: str = "") -> str:
    d = datetime.now(tz=TZ_CN).strftime("%Y%m%d")
    h = short_hash((content or now_cn()) + tag)
    return f"{DNA_PRE}{d}-{tag}-{h}-UID{UID}"

def _http_get(url: str, headers: dict) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return -1, str(e).encode()

def _http_post(url: str, headers: dict, data: dict) -> tuple[int, bytes]:
    body = json.dumps(data).encode()
    req  = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return -1, str(e).encode()

# ─── AuditEvent（字段表死锁，只增不改） ──────────────────────────────────────

@dataclass
class AuditEvent:
    """
    L1 架构规范 §4 AuditEvent 完整字段表
    一旦写入 audit_events.jsonl，永不删改（append-only）。
    """
    # ── 必填字段 ──────────────────────────────────────────────────────────────
    event_id:              str   # AE-YYYYMMDD-HHMMSS-序号
    event_type:            str   # 见枚举
    uid:                   str   = UID
    source_kind:           str   = "manual"       # manual/ai/web/doc/repo/meeting
    source_name:           str   = "local"         # Kimi/Claude/Notion/URL/repo名
    contributor_signature: str   = f"UID{UID} 诸葛鑫（龍芯北辰）"
    gpg_fingerprint:       str   = GPG_FP
    confirm_code:          str   = CONFIRM
    timestamp:             str   = field(default_factory=now_iso)
    input_fingerprint:     str   = ""              # SHA256前8位/语义哈希
    evidence:              str   = ""              # 命中证据点
    decision:              str   = "🟢"            # 🟢通过/🟡挂起/🔴熔断
    action_taken:          str   = "记录"          # 记录/挂起/回滚/冻结DNA/请求二次确认
    rollback_point:        str   = "Baseline-v1.0"
    signature:             str   = f"UID{UID} · {now_cn()}"
    dna_stamp:             str   = ""
    # ── 可选扩展 ──────────────────────────────────────────────────────────────
    detail:                str   = ""
    source_url:            str   = ""
    affected_dna:          str   = ""

    def to_dict(self) -> dict:
        return asdict(self)

# event_type 枚举（不可缩减，只可追加）
EVENT_TYPES = {
    "INPUT_RECEIVED",
    "TEXT_TRAP_AUDIT",
    "FUSE_TRIGGERED_TEXT_TRAP",
    "ROLLBACK_TO_BASELINE",
    "DNA_FREEZE_TEMP",
    "DNA_UNFREEZE",
    "MEMORY_COMPRESS",
    "MEMORY_WRITE_LAYER_A",
    "MEMORY_WRITE_LAYER_B",
    "SYNC_REQUESTED",
    "SYNC_CONFIRMED_1",
    "SYNC_CONFIRMED_2",
    "SYNC_EXECUTED",
    "PUBLIC_READY",
    "PUBLIC_CONFIRMED_2",
    "PUBLIC_EXECUTED",
    # 扩展（三路桥接专用）
    "LOCAL_READ",
    "NOTION_READ",
    "CLAUDE_ALIGN",
    "BRIDGE_STATUS",
    "INTENT_PACKET_CREATED",
    "ALIGN_REPORT_GENERATED",
}

_event_counter: dict[str, int] = {}

def new_event(event_type: str, **kwargs) -> AuditEvent:
    """创建并持久化一条 AuditEvent。"""
    assert event_type in EVENT_TYPES, f"未知 event_type: {event_type}，请先在 EVENT_TYPES 注册"
    date_s   = datetime.now(tz=TZ_CN).strftime("%Y%m%d-%H%M%S")
    _event_counter[date_s] = _event_counter.get(date_s, 0) + 1
    event_id = f"AE-{date_s}-{_event_counter[date_s]:03d}"
    dna      = kwargs.pop("dna_stamp", gen_dna(event_type, event_id))
    ev       = AuditEvent(
        event_id=event_id,
        event_type=event_type,
        dna_stamp=dna,
        **kwargs,
    )
    _append_event(ev)
    return ev

def _append_event(ev: AuditEvent) -> None:
    """Append-only 写入 audit_events.jsonl。"""
    with AUDIT_DB.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev.to_dict(), ensure_ascii=False) + "\n")

def read_events(tail: int = 20, event_type: Optional[str] = None) -> list[dict]:
    if not AUDIT_DB.exists():
        return []
    records = []
    for line in AUDIT_DB.read_text(encoding="utf-8").splitlines():
        try:
            r = json.loads(line)
            if event_type and r.get("event_type") != event_type:
                continue
            records.append(r)
        except Exception:
            pass
    return records[-tail:]

# ─── IntentPacket（§2 输入封装） ─────────────────────────────────────────────

@dataclass
class IntentPacket:
    """
    用户意图封装器。
    格式：【我的意图是：...】  +  【外部参考内容如下：...】（可选）
    """
    intent:    str
    reference: str   = ""
    uid:       str   = UID
    timestamp: str   = field(default_factory=now_iso)
    dna:       str   = ""

    def __post_init__(self):
        if not self.dna:
            self.dna = gen_dna("INTENT", self.intent[:40])

    @classmethod
    def parse(cls, raw: str) -> "IntentPacket":
        """解析 【我的意图是：...】【外部参考内容如下：...】 格式。"""
        intent = ""
        ref    = ""
        m = re.search(r"【我的意图是[：:]\s*(.+?)】", raw, re.DOTALL)
        if m:
            intent = m.group(1).strip()
        r = re.search(r"【外部参考内容如下[：:]\s*(.+?)】", raw, re.DOTALL)
        if r:
            ref = r.group(1).strip()
        if not intent:
            intent = raw.strip()
        return cls(intent=intent, reference=ref)

    def to_plain(self) -> str:
        lines = [f"📥 意图: {self.intent}", f"🕐 时间: {self.timestamp}", f"🧬 DNA: {self.dna}"]
        if self.reference:
            lines.append(f"📎 外部参考（隔离处理）: {self.reference[:80]}…")
        return "\n".join(lines)

# ─── ① LocalReader ───────────────────────────────────────────────────────────

class LocalReader:
    """读取本地龍魂系统状态，不写入任何文件。"""

    def read_summary(self) -> dict:
        result: dict[str, Any] = {}

        # 最新质检报告
        latest = BASE / "reports" / "latest.json"
        if latest.exists():
            try:
                r = json.loads(latest.read_text(encoding="utf-8"))
                result["qa_report"] = {
                    "color": r.get("color"),
                    "avg_score": r.get("avg_score"),
                    "issue_count": r.get("issue_count"),
                    "generated_at": r.get("generated_at"),
                    "dna": r.get("report_id"),
                }
            except Exception:
                result["qa_report"] = {"error": "解析失败"}
        else:
            result["qa_report"] = {"error": "尚未生成（python3 longhun_qa_bot.py run）"}

        # 审计日志统计
        audit_log = BASE / "logs" / "audit_log.jsonl"
        if audit_log.exists():
            records = []
            for line in audit_log.read_text(encoding="utf-8").splitlines():
                try:
                    records.append(json.loads(line))
                except Exception:
                    pass
            colors = [r.get("color", "") for r in records]
            result["audit_log"] = {
                "total": len(records),
                "green": colors.count("🟢"),
                "yellow": colors.count("🟡"),
                "red": colors.count("🔴"),
            }
        else:
            result["audit_log"] = {"total": 0}

        # 核心文件清单
        files = ["auditor.py", "longhun_qa_bot.py", "sync_bridge.py",
                 "memory_console.html", "qa_report.html",
                 "bin/intent_detect.sh", "CLAUDE.md"]
        result["files"] = {f: (BASE / f).exists() for f in files}

        # AuditEvent 链统计
        if AUDIT_DB.exists():
            events = read_events(tail=9999)
            result["audit_events"] = {"total": len(events)}
        else:
            result["audit_events"] = {"total": 0}

        ev = new_event("LOCAL_READ", detail="读取本地状态摘要",
                       source_kind="manual", source_name="local",
                       decision="🟢", action_taken="记录")
        result["dna"] = ev.dna_stamp
        return result

# ─── ② NotionReader ──────────────────────────────────────────────────────────

class NotionReader:
    """只读访问 Notion API v1，密钥从 .env 读取。"""

    BASE_URL = "https://api.notion.com/v1"
    VERSION  = "2022-06-28"

    def __init__(self):
        self.token = get_key("NOTION_TOKEN")
        self.ok    = bool(self.token)

    def _headers(self) -> dict:
        return {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": self.VERSION,
            "Content-Type": "application/json",
        }

    def ping(self) -> dict:
        """验证 Token 是否有效。"""
        if not self.ok:
            return {"online": False, "reason": "NOTION_TOKEN 未配置（~/.env）"}
        status, body = _http_get(f"{self.BASE_URL}/users/me", self._headers())
        if status == 200:
            data = json.loads(body)
            return {"online": True, "user": data.get("name", ""), "type": data.get("type", "")}
        return {"online": False, "reason": f"HTTP {status}: {body[:80].decode(errors='replace')}"}

    def search(self, query: str = "", page_size: int = 10) -> list[dict]:
        """搜索 Notion 页面（只读）。"""
        if not self.ok:
            return []
        payload = {"page_size": page_size}
        if query:
            payload["query"] = query
        status, body = _http_post(f"{self.BASE_URL}/search", self._headers(), payload)
        if status != 200:
            return []
        data    = json.loads(body)
        results = data.get("results", [])
        pages   = []
        for r in results:
            obj_type = r.get("object", "")
            if obj_type == "page":
                title = ""
                props = r.get("properties", {})
                for v in props.values():
                    if v.get("type") == "title":
                        t = v.get("title", [])
                        if t:
                            title = "".join(x.get("plain_text", "") for x in t)
                            break
                if not title:
                    title = r.get("url", "?")
                pages.append({"id": r["id"], "title": title,
                              "url": r.get("url", ""),
                              "last_edited": r.get("last_edited_time", "")})
        return pages

    def read_page_text(self, page_id: str) -> str:
        """读取一个 Notion 页面的文字内容（只读）。"""
        if not self.ok:
            return ""
        # 读取 blocks
        status, body = _http_get(
            f"{self.BASE_URL}/blocks/{page_id}/children?page_size=100",
            self._headers()
        )
        if status != 200:
            return f"[HTTP {status}]"
        data   = json.loads(body)
        blocks = data.get("results", [])
        lines  = []
        for b in blocks:
            bt = b.get("type", "")
            rich = b.get(bt, {}).get("rich_text", [])
            text = "".join(x.get("plain_text", "") for x in rich)
            if text:
                lines.append(text)
        return "\n".join(lines)

    def read_summary(self, query: str = "龍魂", limit: int = 5) -> dict:
        """读取 Notion 摘要（只读对齐用）。"""
        ping    = self.ping()
        pages   = self.search(query=query, page_size=limit) if ping["online"] else []
        ev = new_event("NOTION_READ",
                       source_kind="web", source_name="Notion",
                       detail=f"搜索 '{query}' 返回 {len(pages)} 页",
                       decision="🟢" if ping["online"] else "🟡",
                       action_taken="记录")
        return {"ping": ping, "pages": pages, "count": len(pages), "dna": ev.dna_stamp}

# ─── ③ ClaudeAligner ─────────────────────────────────────────────────────────

class ClaudeAligner:
    """
    只读查询 Claude API，用于三路对齐检测。
    密钥从 .env 的 ANTHROPIC_API_KEY 读取，不硬编码。
    """

    URL     = "https://api.anthropic.com/v1/messages"
    MODEL   = "claude-sonnet-4-6"
    VERSION = "2023-06-01"

    def __init__(self):
        self.key = get_key("ANTHROPIC_API_KEY")
        self.ok  = bool(self.key)

    def _headers(self) -> dict:
        return {
            "x-api-key":         self.key or "",
            "anthropic-version": self.VERSION,
            "content-type":      "application/json",
        }

    def ping(self) -> dict:
        if not self.ok:
            return {"online": False, "reason": "ANTHROPIC_API_KEY 未配置（~/.env 中填入 sk-ant-...）"}
        # 发一条最短的测试请求
        status, body = _http_post(self.URL, self._headers(), {
            "model": self.MODEL,
            "max_tokens": 10,
            "messages": [{"role": "user", "content": "ping"}],
        })
        if status == 200:
            return {"online": True, "model": self.MODEL}
        return {"online": False, "reason": f"HTTP {status}: {body[:80].decode(errors='replace')}"}

    def align_check(self, local_summary: dict, notion_pages: list[dict]) -> dict:
        """
        把本地系统摘要 + Notion 页面标题发给 Claude，
        请它做一次对齐检测（只读，结果不写入任何系统）。
        """
        if not self.ok:
            return {"online": False, "reason": "ANTHROPIC_API_KEY 未配置"}

        qa  = local_summary.get("qa_report", {})
        files_ok = sum(1 for v in local_summary.get("files", {}).values() if v)
        notion_titles = [p["title"] for p in notion_pages[:5]]

        prompt = f"""你是龍魂系统的三路对齐检测器。
身份锚定：UID9622 · GPG {GPG_FP} · {CONFIRM}

你需要根据以下信息，输出一份简短的对齐报告（不超过200字）：
  本地最新质检: {qa.get('color','?')} 均分{qa.get('avg_score','?')} · 问题{qa.get('issue_count','?')}个
  本地核心文件完整: {files_ok} 个在线
  Notion页面（标题）: {notion_titles}

请判断：
1. 三路数据是否互相对齐（一致）？
2. 有什么明显缺口或不一致？
3. 建议的下一步行动是什么（一句话）？

输出格式：
  对齐状态: 🟢/🟡/🔴
  缺口: ...
  建议: ...
"""
        status, body = _http_post(self.URL, self._headers(), {
            "model": self.MODEL,
            "max_tokens": 300,
            "messages": [{"role": "user", "content": prompt}],
        })
        if status != 200:
            return {"online": True, "error": f"HTTP {status}"}
        data    = json.loads(body)
        content = data.get("content", [])
        text    = "".join(c.get("text", "") for c in content if c.get("type") == "text")
        ev = new_event("CLAUDE_ALIGN",
                       source_kind="ai", source_name="Claude",
                       detail=f"对齐检测完成 HTTP{status}",
                       decision="🟢", action_taken="记录")
        return {"online": True, "result": text, "dna": ev.dna_stamp}

    def intent_to_code(self, intent: str) -> dict:
        """
        §5 大白话写代码流水线：
        把用户的白话意图转成可执行需求清单 + 最小代码 + DNA戳。
        """
        if not self.ok:
            return {"online": False, "reason": "ANTHROPIC_API_KEY 未配置"}

        prompt = f"""你是龍魂系统的「大白话写代码」助手。
身份锚定：UID9622 · {CONFIRM}

用户的白话意图：
{intent}

请按以下步骤输出（不超过400字）：

Step 1 需求清单
  - 用大白话列出 3-5 条可执行需求

Step 2 最小代码
  - 给出最短能跑的代码或命令（Python/bash均可）
  - 代码必须可以直接运行，不留 TODO

Step 3 三色审计
  - 🟢/🟡/🔴 + 一句话理由

Step 4 DNA戳
  - 自动生成：#龍芯⚡️{datetime.now(tz=TZ_CN).strftime('%Y%m%d')}-CODE-{short_hash(intent)}-UID9622
"""
        status, body = _http_post(self.URL, self._headers(), {
            "model": self.MODEL,
            "max_tokens": 600,
            "messages": [{"role": "user", "content": prompt}],
        })
        if status != 200:
            return {"online": True, "error": f"HTTP {status}"}
        data    = json.loads(body)
        content = data.get("content", [])
        text    = "".join(c.get("text", "") for c in content if c.get("type") == "text")
        ev = new_event("INTENT_PACKET_CREATED",
                       source_kind="manual", source_name="local",
                       detail=f"大白话流水线: {intent[:40]}",
                       decision="🟢", action_taken="记录")
        return {"online": True, "result": text, "dna": ev.dna_stamp}

# ─── SyncBridge（总调度） ─────────────────────────────────────────────────────

class SyncBridge:
    def __init__(self):
        self.local   = LocalReader()
        self.notion  = NotionReader()
        self.claude  = ClaudeAligner()

    def status(self) -> dict:
        """三路连接状态检测。"""
        notion_ping = self.notion.ping()
        claude_ping = self.claude.ping()
        ev = new_event("BRIDGE_STATUS",
                       source_kind="manual", source_name="local",
                       detail=f"Notion:{notion_ping['online']} Claude:{claude_ping['online']}",
                       decision="🟢", action_taken="记录")
        return {
            "local":  {"online": True, "path": str(BASE)},
            "notion": notion_ping,
            "claude": claude_ping,
            "dna":    ev.dna_stamp,
            "ts":     now_cn(),
        }

    def full_align(self) -> dict:
        """三路完整对齐报告。"""
        print("  ① 读取本地状态…")
        local_sum  = self.local.read_summary()
        print("  ② 读取 Notion 摘要…")
        notion_sum = self.notion.read_summary()
        print("  ③ Claude 对齐分析…")
        align      = self.claude.align_check(local_sum, notion_sum.get("pages", []))
        ev = new_event("ALIGN_REPORT_GENERATED",
                       source_kind="manual", source_name="local",
                       detail="三路对齐报告",
                       decision="🟢", action_taken="记录")
        return {
            "local":  local_sum,
            "notion": notion_sum,
            "claude": align,
            "dna":    ev.dna_stamp,
            "ts":     now_cn(),
        }

# ─── 格式化输出 ───────────────────────────────────────────────────────────────

def _print_status(s: dict) -> None:
    local  = s["local"]
    notion = s["notion"]
    claude = s["claude"]
    print(f"""
╔══════════════════════════════════════════════════════════╗
║  🌉 龍魂三路对接桥 · 连接状态                           ║
║  {s['ts']}  ·  {s['dna'][:42]}  ║
╠══════════════════════════════════════════════════════════╣
║  ① 本地（Local）     🟢 在线  {str(local['path'])[:36]}  ║
║  ② Notion            {"🟢 在线  " + str(notion.get('user',''))[:26] if notion['online'] else "🔴 离线  " + str(notion.get('reason',''))[:26]}  ║
║  ③ Claude API        {"🟢 在线  " + str(claude.get('model',''))[:26] if claude['online'] else "🔴 离线  " + str(claude.get('reason',''))[:26]}  ║
╠══════════════════════════════════════════════════════════╣
║  密钥位置: ~/longhun-system/.env（永不离开本地）         ║
║  架构: 只读 · Append-only · DNA追溯 · 主权在手           ║
╚══════════════════════════════════════════════════════════╝
""")
    if not notion["online"]:
        print(f"  Notion 修复：在 ~/.env 确认 NOTION_TOKEN 正确")
    if not claude["online"]:
        print(f"  Claude 修复：在 ~/.env 填入 ANTHROPIC_API_KEY=sk-ant-...")

def _print_local(s: dict) -> None:
    qa = s.get("qa_report", {})
    al = s.get("audit_log", {})
    files = s.get("files", {})
    print(f"""
━━━ 本地状态摘要 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  最新质检: {qa.get('color','?')} 均分 {qa.get('avg_score','?')}  问题 {qa.get('issue_count','?')} 个
  质检时间: {qa.get('generated_at','未运行')}
  审计日志: 共 {al.get('total',0)} 条  🟢{al.get('green',0)} 🟡{al.get('yellow',0)} 🔴{al.get('red',0)}
  AuditEvent: {s.get('audit_events',{}).get('total',0)} 条

  核心文件:""")
    for fname, ok in files.items():
        icon = "✅" if ok else "❌"
        print(f"    {icon} {fname}")
    print(f"\n  DNA: {s.get('dna','')}")

def _print_align(r: dict) -> None:
    print(f"\n━━━ 三路对齐报告 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    _print_local(r["local"])
    notion = r["notion"]
    print(f"\n━━━ Notion ━━━")
    if notion["ping"]["online"]:
        print(f"  🟢 在线 · 用户: {notion['ping'].get('user','')}")
        for p in notion.get("pages", []):
            print(f"    📄 {p['title']}  ({p['last_edited'][:10]})")
    else:
        print(f"  🔴 离线: {notion['ping'].get('reason','')}")
    claude = r["claude"]
    print(f"\n━━━ Claude 对齐分析 ━━━")
    if claude.get("online"):
        print(claude.get("result", "（无结果）"))
    else:
        print(f"  🔴 离线: {claude.get('reason','')}")
    print(f"\n  报告 DNA: {r['dna']}")

# ─── CLI ─────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="龍魂三路只读对接桥 · sync_bridge.py"
    )
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status",  help="三路连接状态（快速检测）")

    p_read = sub.add_parser("read", help="读取某一路数据")
    p_read.add_argument("target", choices=["local", "notion", "claude"],
                        help="local / notion / claude")
    p_read.add_argument("--query", default="龍魂", help="Notion 搜索词（默认: 龍魂）")

    sub.add_parser("align", help="三路完整对齐报告")

    p_audit = sub.add_parser("audit", help="查看 AuditEvent 链")
    p_audit.add_argument("--tail", type=int, default=20, help="最近 N 条")
    p_audit.add_argument("--type", default="", help="过滤 event_type")

    p_intent = sub.add_parser("intent", help="IntentPacket 封装 + 大白话代码流水线")
    p_intent.add_argument("text", nargs="?", default="", help="意图文本或 【我的意图是：...】格式")

    args = parser.parse_args()
    bridge = SyncBridge()

    if args.cmd == "status":
        s = bridge.status()
        _print_status(s)

    elif args.cmd == "read":
        if args.target == "local":
            s = bridge.local.read_summary()
            _print_local(s)
        elif args.target == "notion":
            s = bridge.notion.read_summary(query=args.query)
            ping = s["ping"]
            if ping["online"]:
                print(f"🟢 Notion 在线 · 用户: {ping.get('user','')} · DNA: {s['dna']}")
                for p in s["pages"]:
                    print(f"  📄 {p['title'][:60]}  ({p['last_edited'][:10]})")
            else:
                print(f"🔴 Notion 离线: {ping.get('reason','')}")
        elif args.target == "claude":
            ping = bridge.claude.ping()
            if ping["online"]:
                print(f"🟢 Claude API 在线 · 模型: {ping['model']}")
            else:
                print(f"🔴 Claude API 离线: {ping.get('reason','')}")
                print(f"\n  修复方法：在 ~/longhun-system/.env 填入：")
                print(f"  ANTHROPIC_API_KEY='sk-ant-你的密钥'")

    elif args.cmd == "align":
        print("\n🔍 三路对齐检测中…")
        r = bridge.full_align()
        _print_align(r)

    elif args.cmd == "audit":
        records = read_events(tail=args.tail, event_type=args.type or None)
        if not records:
            print("（AuditEvent 链为空，先运行 status 生成首条记录）")
        else:
            print(f"\n📜 AuditEvent 链（最近 {len(records)} 条）")
            print(f"{'时间':20} {'类型':30} {'决定':5} {'动作':12} DNA前缀")
            print("─" * 90)
            for r in records:
                ts     = r["timestamp"][:19].replace("T", " ")
                etype  = r["event_type"][:28]
                dec    = r["decision"]
                action = r["action_taken"][:10]
                dna    = r.get("dna_stamp", "")[:32]
                print(f"{ts:20} {etype:30} {dec:5} {action:12} {dna}")

    elif args.cmd == "intent":
        raw  = args.text or input("请输入意图（支持 【我的意图是：...】格式）:\n> ")
        pkt  = IntentPacket.parse(raw)
        print(f"\n📥 IntentPacket 已创建:")
        print(pkt.to_plain())
        new_event("INPUT_RECEIVED", source_kind="manual", source_name="local",
                  input_fingerprint=short_hash(pkt.intent),
                  evidence=pkt.intent[:60], decision="🟢", action_taken="记录",
                  detail=pkt.intent[:120])
        if bridge.claude.ok:
            print(f"\n⚡ 大白话写代码流水线（调用 Claude API）…")
            result = bridge.claude.intent_to_code(pkt.intent)
            if result.get("online"):
                print(result.get("result", ""))
                print(f"\n  DNA: {result.get('dna','')}")
            else:
                print(f"  🔴 {result.get('reason','')}")
        else:
            print(f"\n  ⚠️  Claude API 未配置，跳过代码生成。")
            print(f"  在 ~/.env 中填入 ANTHROPIC_API_KEY 后可自动生成代码。")

    else:
        parser.print_help()
        print(f"\n  DNA: #龍芯⚡️20260311-SYNC-BRIDGE-v1.0")
        print(f"  北京时间: {now_cn()}")
        print(f"\n  快速开始：python3 sync_bridge.py status")

if __name__ == "__main__":
    main()
