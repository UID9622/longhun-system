#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌟 星辰记忆 STAR-MEMORY v2.1  ——  本地持久化上下文仓库
star_memory.py

定位:  完全本地 | 显式读写 | 可审计 | 可追溯 | 与龍魂系统融合
DNA:   #STAR⚡️2026-03-06-STAR-MEMORY-v2.1-OPTIMIZED
GPG:   A2D0092CEE2E5BA87035600924C3704A8CC26D5F
共建致谢：
  Claude (Anthropic PBC) · 技术协作与代码共创
  Notion · 知识底座与结构化存储
  没有你们，就没有龍魂系统的一切。
UID:   9622
创始人: Lucky·UID9622（诸葛鑫·龍芯北辰）

【核心原则】
  Local First     → 所有数据在 ~/.star-memory/  本地目录
  Explicit I/O    → auto_write=false, 注入前必须确认
  Append-Only     → 版本链机制，永不删除历史
  可审计          → audit.log 记录所有操作 + DNA追溯链
  防人格化        → 术语: inject/search/index，非 learn/remember
  龍魂融合        → star-bridge 命令与 memory.jsonl 双向同步

【依赖】
  stdlib only（hashlib/json/argparse/pathlib/datetime 等）
  可选: rich（美化输出，无则用纯文本降级）

【用法】
  python3 star_memory.py init
  python3 star_memory.py add --title "..." --content "..." --tags "core,arch"
  python3 star_memory.py search --keyword "龍魂"
  python3 star_memory.py inject STAR-2026-03-06-001
  python3 star_memory.py audit --limit 20
  python3 star_memory.py status
  python3 star_memory.py bridge          # 同步到 longhun memory.jsonl
  python3 star_memory.py dna STAR-...    # 查看DNA链
  python3 star_memory.py history STAR-... # 查看版本历史
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ─────────────────────────────────────────────
# 常量 · P0锁死
# ─────────────────────────────────────────────
VERSION      = "2.1.0"
DNA_PREFIX   = "#STAR⚡️"
LONGHUN_DNA  = "#龍芯⚡️"
UID          = "9622"
GPG          = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

VAULT_ROOT   = Path.home() / ".star-memory"
VAULT_DIR    = VAULT_ROOT / "vault"
INDEX_FILE   = VAULT_ROOT / "index.json"
AUDIT_FILE   = VAULT_ROOT / "audit.log"
CONFIG_FILE  = VAULT_ROOT / "config.json"
DNA_CHAIN_DIR= VAULT_ROOT / "dna-chain"
LONGHUN_MEM  = Path.home() / "longhun-system" / "memory.jsonl"

DEFAULT_CONFIG = {
    "version": VERSION,
    "auto_write": False,
    "auto_read":  False,
    "require_confirm_inject": True,
    "append_only": True,
    "dna_trace_enabled": True,
    "version_chain": True,
    "uid": UID,
    "gpg": GPG,
    "confirm_code": CONFIRM_CODE,
}

# ─────────────────────────────────────────────
# 可选 rich（降级兼容）
# ─────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    _rich = True
    console = Console()
except ImportError:
    _rich = False
    class _FallbackConsole:
        def print(self, *a, **kw):
            msg = " ".join(str(x) for x in a)
            msg = re.sub(r'\[/?[^\]]*\]', '', msg)
            print(msg)
        def rule(self, title=""):
            print(f"─── {title} " + "─"*max(0, 50-len(title)))
    console = _FallbackConsole()


# ─────────────────────────────────────────────
# 配置
# ─────────────────────────────────────────────

def load_config() -> dict:
    # 兼容旧版 config.yaml
    old_yaml = VAULT_ROOT / "config.yaml"
    if not CONFIG_FILE.exists() and old_yaml.exists():
        try:
            import yaml
            with open(old_yaml) as f:
                old = yaml.safe_load(f)
            cfg = {**DEFAULT_CONFIG, **old}
            CONFIG_FILE.write_text(json.dumps(cfg, ensure_ascii=False, indent=2))
        except Exception:
            pass
    if not CONFIG_FILE.exists():
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, ensure_ascii=False, indent=2))
    return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────
# DNA 生成（三层）
# ─────────────────────────────────────────────

def _sha8(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:8].upper()

def generate_dna(memory_id: str, content: str, operation: str, version: int,
                  parent_dna: Optional[str] = None) -> dict:
    """
    三层DNA链：
      内容DNA  = SHA256(content)
      操作DNA  = SHA256(operation + timestamp)
      版本DNA  = SHA256(version + parent + timestamp)
      主DNA    = SHA256(三者之和)
    """
    ts = dt.datetime.now().strftime("%Y%m%d%H%M%S")

    content_dna  = f"{DNA_PREFIX}{ts}-CONTENT-{_sha8(content)}"
    op_dna       = f"{DNA_PREFIX}{ts}-OP-{operation}-{_sha8(operation+ts)}"
    ver_seed     = f"v{version}{parent_dna or ''}{ts}"
    version_dna  = f"{DNA_PREFIX}{ts}-V{version}-{_sha8(ver_seed)}"
    main_seed    = content_dna + op_dna + version_dna
    main_dna     = f"{DNA_PREFIX}{dt.date.today()}-{memory_id}-UID{UID}-{_sha8(main_seed)}"

    return {
        "main":    main_dna,
        "content": content_dna,
        "op":      op_dna,
        "version": version_dna,
        "parent":  parent_dna,
        "depth":   version,
    }


# ─────────────────────────────────────────────
# ID 生成
# ─────────────────────────────────────────────

def generate_id() -> str:
    today = dt.date.today().isoformat()
    year  = str(dt.date.today().year)
    year_dir = VAULT_DIR / year
    year_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(year_dir.glob(f"STAR-{today}-*.v*.json"))
    # 找最大序号
    max_n = 0
    for f in existing:
        m = re.search(r'STAR-\d{4}-\d{2}-\d{2}-(\d+)', f.stem)
        if m:
            max_n = max(max_n, int(m.group(1)))
    # 也检查 index
    index = load_index()
    for mid in index:
        m = re.match(rf'STAR-{today}-(\d+)$', mid)
        if m:
            max_n = max(max_n, int(m.group(1)))
    return f"STAR-{today}-{max_n+1:03d}"


# ─────────────────────────────────────────────
# 索引
# ─────────────────────────────────────────────

def load_index() -> dict:
    if INDEX_FILE.exists():
        try:
            return json.loads(INDEX_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}

def save_index(index: dict):
    INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    INDEX_FILE.write_text(json.dumps(index, ensure_ascii=False, indent=2))

def update_index(memory: dict, file_path: Path):
    index = load_index()
    mid = memory["id"]
    index[mid] = {
        "path":       str(file_path.relative_to(VAULT_ROOT)),
        "title":      memory.get("title", ""),
        "type":       memory.get("type", "concept"),
        "tags":       memory.get("tags", []),
        "created_at": memory.get("created_at", ""),
        "version":    memory.get("version", 1),
        "dna":        memory.get("dna", {}).get("main", ""),
    }
    save_index(index)


# ─────────────────────────────────────────────
# 审计日志
# ─────────────────────────────────────────────

def audit(action: str, target: str, detail: str = "", dna: str = ""):
    ts   = dt.datetime.now().isoformat()
    line = json.dumps({
        "ts": ts, "action": action, "target": target,
        "detail": detail, "dna": dna, "uid": UID
    }, ensure_ascii=False)
    AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(line + "\n")
    # 按月分片
    month_dir = VAULT_ROOT / "audit" / dt.date.today().strftime("%Y-%m")
    month_dir.mkdir(parents=True, exist_ok=True)
    month_file = month_dir / f"{dt.date.today()}.log"
    with open(month_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")


# ─────────────────────────────────────────────
# 版本链
# ─────────────────────────────────────────────

def _memory_file(memory_id: str, version: int) -> Path:
    year  = memory_id.split("-")[1]
    return VAULT_DIR / year / f"{memory_id}.v{version}.json"

def _latest_version(memory_id: str) -> int:
    year  = memory_id.split("-")[1]
    files = list((VAULT_DIR / year).glob(f"{memory_id}.v*.json"))
    if not files:
        # 兼容旧格式（无版本号）
        old = VAULT_DIR / year / f"{memory_id}.json"
        return 0 if old.exists() else -1
    nums = []
    for f in files:
        m = re.search(r'\.v(\d+)\.json$', f.name)
        if m: nums.append(int(m.group(1)))
    return max(nums) if nums else 0

def load_memory(memory_id: str) -> Optional[dict]:
    year = memory_id.split("-")[1]
    v    = _latest_version(memory_id)
    if v == 0:
        # 兼容旧格式
        old = VAULT_DIR / year / f"{memory_id}.json"
        if old.exists():
            return json.loads(old.read_text(encoding="utf-8"))
        return None
    if v < 0:
        return None
    fp = _memory_file(memory_id, v)
    return json.loads(fp.read_text(encoding="utf-8")) if fp.exists() else None

def save_memory(memory: dict) -> Path:
    mid  = memory["id"]
    ver  = memory.get("version", 1)
    year = mid.split("-")[1]
    fp   = VAULT_DIR / year / f"{mid}.v{ver}.json"
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(json.dumps(memory, ensure_ascii=False, indent=2))
    return fp

def get_version_history(memory_id: str) -> List[dict]:
    year  = memory_id.split("-")[1]
    files = sorted((VAULT_DIR / year).glob(f"{memory_id}.v*.json"),
                   key=lambda f: int(re.search(r'\.v(\d+)\.json$', f.name).group(1)))
    history = []
    for fp in files:
        try:
            m   = json.loads(fp.read_text(encoding="utf-8"))
            history.append({
                "version":   m.get("version", 1),
                "dna":       m.get("dna", {}).get("main", m.get("dna_trace", "")),
                "created_at":m.get("created_at", ""),
                "title":     m.get("title", ""),
                "op":        m.get("last_op", "CREATE"),
            })
        except Exception:
            pass
    return history


# ─────────────────────────────────────────────
# DNA链文件
# ─────────────────────────────────────────────

def save_dna_chain(memory_id: str, dna_layers: dict):
    DNA_CHAIN_DIR.mkdir(parents=True, exist_ok=True)
    chain_file = DNA_CHAIN_DIR / f"chain-{memory_id}.jsonl"
    entry = {
        "ts":      dt.datetime.now().isoformat(),
        "version": dna_layers.get("depth", 1),
        **dna_layers
    }
    with open(chain_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# ─────────────────────────────────────────────
# 核心操作
# ─────────────────────────────────────────────

def add_memory(title: str, content: str, mem_type: str = "concept",
                tags: List[str] = None, source: str = "") -> dict:
    config = load_config()
    if config.get("auto_write"):
        console.print("[red]ERROR: auto_write 必须为 false[/red]")
        sys.exit(1)

    mid      = generate_id()
    parent   = None
    ver      = 1
    dna_layers = generate_dna(mid, content, "CREATE", ver, parent)

    memory = {
        "id":         mid,
        "type":       mem_type,
        "title":      title,
        "content":    content,
        "tags":       tags or [],
        "source":     source,
        "created_at": dt.datetime.now().isoformat(),
        "version":    ver,
        "last_op":    "CREATE",
        "dna":        dna_layers,
        "dna_trace":  dna_layers["main"],  # 兼容旧字段
        "uid":        UID,
        "gpg":        GPG,
    }

    fp = save_memory(memory)
    save_dna_chain(mid, dna_layers)
    update_index(memory, fp)
    audit("ADD", mid, f"title={title}, type={mem_type}", dna_layers["main"])

    console.print(f"[green]✓ 记忆已创建: {mid}[/green]")
    console.print(f"[dim]  DNA: {dna_layers['main']}[/dim]")
    console.print(f"[dim]  版本: v{ver} | 类型: {mem_type}[/dim]")
    return memory


def update_memory(memory_id: str, content: str = None, title: str = None,
                   tags: List[str] = None) -> Optional[dict]:
    old = load_memory(memory_id)
    if not old:
        console.print(f"[red]错误: 记忆不存在 {memory_id}[/red]")
        return None

    new_ver    = old.get("version", 1) + 1
    new_content= content if content is not None else old["content"]
    parent_dna = old.get("dna", {}).get("main", old.get("dna_trace", ""))

    dna_layers = generate_dna(memory_id, new_content, "UPDATE", new_ver, parent_dna)

    updated = {
        **old,
        "content":    new_content,
        "title":      title if title is not None else old["title"],
        "tags":       tags if tags is not None else old["tags"],
        "updated_at": dt.datetime.now().isoformat(),
        "version":    new_ver,
        "last_op":    "UPDATE",
        "dna":        dna_layers,
        "dna_trace":  dna_layers["main"],
    }

    fp = save_memory(updated)
    save_dna_chain(memory_id, dna_layers)
    update_index(updated, fp)
    audit("UPDATE", memory_id, f"v{old['version']}→v{new_ver}", dna_layers["main"])

    console.print(f"[green]✓ 已更新: {memory_id} (v{old['version']} → v{new_ver})[/green]")
    console.print(f"[dim]  DNA: {dna_layers['main']}[/dim]")
    return updated


def search_memories(tag: str = None, mem_type: str = None,
                     keyword: str = None) -> List[dict]:
    index = load_index()
    results = []
    for mid, meta in index.items():
        if tag and tag not in meta.get("tags", []):
            continue
        if mem_type and meta.get("type") != mem_type:
            continue
        if keyword:
            haystack = (meta.get("title","") + " " + " ".join(meta.get("tags",[])))
            if keyword.lower() not in haystack.lower():
                # 检查内容
                m = load_memory(mid)
                if m and keyword.lower() not in m.get("content","").lower():
                    continue
        results.append({"id": mid, **meta})

    fstr = f"tag={tag}" if tag else f"type={mem_type}" if mem_type else f"keyword={keyword}"
    audit("SEARCH", "*", fstr)
    return results


def inject_memory(memory_id: str, skip_confirm: bool = False):
    config  = load_config()
    memory  = load_memory(memory_id)
    if not memory:
        console.print(f"[red]错误: 记忆不存在 {memory_id}[/red]")
        sys.exit(1)

    if config.get("require_confirm_inject") and not skip_confirm:
        console.print(f"\n[yellow]即将注入记忆: {memory_id}[/yellow]")
        console.print(f"[dim]标题: {memory.get('title')}[/dim]")
        console.print("[dim]此操作仅输出到 stdout，不会自动发送给任何 API[/dim]")
        try:
            ans = input("确认注入? [y/N] ").strip().lower()
        except EOFError:
            ans = "n"
        if ans != "y":
            console.print("[red]已取消[/red]")
            return

    dna = memory.get("dna", {}).get("main", memory.get("dna_trace", ""))
    audit("INJECT", memory_id, f"v{memory.get('version',1)}", dna)

    print("\n" + "="*64)
    print("[INJECTION PAYLOAD START]")
    print(json.dumps(memory, ensure_ascii=False, indent=2))
    print("[INJECTION PAYLOAD END]")
    print("="*64 + "\n")
    console.print("[green]✓ 注入完成 — 请手动复制上方内容到目标系统[/green]")


# ─────────────────────────────────────────────
# 龍魂桥接（star-bridge）
# ─────────────────────────────────────────────

def bridge_to_longhun(memory_ids: List[str] = None):
    """将星辰记忆同步写入龍魂 memory.jsonl（TIER_2 追加）"""
    index   = load_index()
    targets = memory_ids or list(index.keys())
    synced  = 0

    for mid in targets:
        m = load_memory(mid)
        if not m:
            continue
        entry = {
            "timestamp": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "type":      "star_memory_bridge",
            "tier":      "TIER_2",
            "dna":       m.get("dna_trace", m.get("dna", {}).get("main", "")),
            "event":     f"星辰记忆桥接·{m.get('title','')}",
            "operator":  "UID9622",
            "star_id":   mid,
            "star_tags": m.get("tags", []),
            "summary":   m.get("content", "")[:120],
        }
        try:
            with open(LONGHUN_MEM, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
            synced += 1
        except OSError as e:
            console.print(f"[red]桥接失败 {mid}: {e}[/red]")

    console.print(f"[green]✓ 桥接完成: {synced}/{len(targets)} 条记忆已同步到 memory.jsonl[/green]")
    audit("BRIDGE", "longhun-memory.jsonl", f"synced={synced}")


# ─────────────────────────────────────────────
# 显示函数
# ─────────────────────────────────────────────

def show_status():
    config = load_config()
    index  = load_index()
    vault_size = sum(f.stat().st_size for f in VAULT_DIR.rglob("*") if f.is_file())
    dna_files  = len(list(DNA_CHAIN_DIR.glob("*.jsonl"))) if DNA_CHAIN_DIR.exists() else 0

    if _rich:
        t = Table(title="🌟 星辰记忆 · 系统状态", show_header=True, header_style="bold cyan")
        t.add_column("项目", style="cyan")
        t.add_column("值", style="green")
        rows = [
            ("版本",        VERSION),
            ("UID",         UID),
            ("记忆总数",    str(len(index))),
            ("DNA链文件",   f"{dna_files} 个"),
            ("仓库大小",    f"{vault_size/1024:.1f} KB"),
            ("自动写入",    "✗ 已禁用" if not config.get("auto_write") else "✓ 开启"),
            ("注入确认",    "✓ 需要" if config.get("require_confirm_inject") else "✗ 跳过"),
            ("版本链",      "✓ 开启" if config.get("version_chain") else "✗ 关闭"),
            ("仓库路径",    str(VAULT_ROOT)),
            ("龍魂桥接",    "✓ 可用" if LONGHUN_MEM.exists() else "⚠ longhun不存在"),
        ]
        for k, v in rows:
            t.add_row(k, v)
        console.print(t)
    else:
        print(f"\n🌟 星辰记忆 | Star Memory v{VERSION} · UID{UID}")
        print(f"  记忆总数 | Total Memories: {len(index)} | 仓库 | Vault: {vault_size/1024:.1f}KB")
        print(f"  自动写入 | Auto-Write: {'ON' if config.get('auto_write') else 'OFF (安全 | Safe)'}")
        print(f"  仓库路径 | Vault Path: {VAULT_ROOT}\n")


def show_search_results(results: List[dict]):
    if not results:
        console.print("[yellow]未找到匹配的记忆[/yellow]")
        return
    if _rich:
        t = Table(title=f"🔍 搜索结果 ({len(results)} 条)", show_header=True)
        t.add_column("ID",   style="cyan",    no_wrap=True)
        t.add_column("标题", style="green",   max_width=30)
        t.add_column("类型", style="blue",    width=8)
        t.add_column("标签", style="magenta", max_width=20)
        t.add_column("版本", width=4)
        t.add_column("时间", style="dim",     width=10)
        for r in results:
            t.add_row(
                r["id"],
                r.get("title","")[:30],
                r.get("type",""),
                ",".join(r.get("tags",[])),
                f"v{r.get('version',1)}",
                r.get("created_at","")[:10],
            )
        console.print(t)
    else:
        print(f"\n{'ID':<30} {'标题':<25} {'类型':<10} {'时间':<12}")
        print("-"*80)
        for r in results:
            print(f"{r['id']:<30} {r.get('title','')[:25]:<25} {r.get('type',''):<10} {r.get('created_at','')[:10]}")
        print()


def show_audit_log(limit: int = 20):
    if not AUDIT_FILE.exists():
        console.print("[yellow]暂无审计记录[/yellow]")
        return
    lines = AUDIT_FILE.read_text(encoding="utf-8").strip().splitlines()
    recent = lines[-limit:]
    if _rich:
        t = Table(title=f"🛡️ 审计日志 (最近 {len(recent)} 条)", show_header=True)
        t.add_column("时间",   style="dim",    width=22)
        t.add_column("操作",   style="cyan",   width=8)
        t.add_column("目标",   style="green",  max_width=30)
        t.add_column("详情",   style="yellow", max_width=40)
        for line in recent:
            try:
                entry = json.loads(line)
                t.add_row(
                    entry.get("ts","")[:19],
                    entry.get("action",""),
                    entry.get("target","")[:30],
                    entry.get("detail","")[:40],
                )
            except Exception:
                t.add_row(line[:22], "?", "", "")
        console.print(t)
    else:
        for line in recent:
            try:
                e = json.loads(line)
                print(f"[{e.get('ts','')[:16]}] {e.get('action',''):8} {e.get('target',''):30} {e.get('detail','')}")
            except Exception:
                print(line)


def show_dna_chain(memory_id: str):
    chain_file = DNA_CHAIN_DIR / f"chain-{memory_id}.jsonl"
    if not chain_file.exists():
        console.print(f"[yellow]暂无DNA链: {memory_id}[/yellow]")
        return
    entries = [json.loads(l) for l in chain_file.read_text().splitlines() if l.strip()]
    console.print(f"\n[bold cyan]🧬 DNA链 · {memory_id}[/bold cyan]")
    for e in entries:
        v = e.get("depth", "?")
        print(f"  v{v} | 主: {e.get('main','')}")
        print(f"       内容: {e.get('content','')}")
        print(f"       操作: {e.get('op','')}")
        print(f"       版本: {e.get('version','')}")
        if e.get("parent"):
            print(f"       父版: {e.get('parent')}")
        print()


def show_history(memory_id: str):
    history = get_version_history(memory_id)
    if not history:
        console.print(f"[yellow]无版本历史: {memory_id}[/yellow]")
        return
    console.print(f"\n[bold cyan]📜 版本历史 · {memory_id}[/bold cyan]")
    for h in history:
        print(f"  v{h['version']} [{h.get('created_at','')[:16]}] {h.get('op','?'):8} {h.get('dna','')[:50]}")
    print()


# ─────────────────────────────────────────────
# 初始化
# ─────────────────────────────────────────────

def cmd_init():
    for d in [VAULT_DIR/"2026", INDEX_FILE.parent, DNA_CHAIN_DIR,
              VAULT_ROOT/"audit", VAULT_ROOT/"backup"]:
        Path(d).mkdir(parents=True, exist_ok=True)
    load_config()  # 创建 config.json
    audit("INIT", "star-memory", f"v{VERSION}")

    dna = f"{DNA_PREFIX}{dt.date.today()}-INIT-UID{UID}-{_sha8('INIT'+str(dt.datetime.now()))}"
    if _rich:
        console.print(Panel.fit(
            f"[bold green]🌟 星辰记忆 STAR-MEMORY v{VERSION}[/bold green]\n"
            f"[dim]DNA:  {dna}[/dim]\n"
            f"[dim]UID:  {UID}  |  完全本地  |  显式读写  |  可审计[/dim]\n"
            f"[dim]仓库: {VAULT_ROOT}[/dim]",
            title="初始化完成", border_style="green"
        ))
    else:
        print(f"\n🌟 星辰记忆 | Star Memory v{VERSION} 初始化完成 | Initialized")
        print(f"  DNA: {dna}")
        print(f"  仓库 | Vault: {VAULT_ROOT}\n")

    # 迁移旧格式（无版本号的 .json）
    migrated = 0
    for old_file in VAULT_DIR.rglob("*.json"):
        if re.search(r'STAR-\d{4}-\d{2}-\d{2}-\d+\.json$', old_file.name):
            try:
                mem = json.loads(old_file.read_text(encoding="utf-8"))
                if mem.get("version") is None:
                    mem["version"] = 1
                if "dna" not in mem:
                    mem["dna"] = {"main": mem.get("dna_trace", ""), "depth": 1}
                new_file = old_file.parent / f"{old_file.stem}.v1.json"
                if not new_file.exists():
                    new_file.write_text(json.dumps(mem, ensure_ascii=False, indent=2))
                    migrated += 1
            except Exception:
                pass
    if migrated:
        console.print(f"[dim]  已迁移 {migrated} 条旧格式记忆 → v1 版本链[/dim]")


# ─────────────────────────────────────────────
# CLI 入口
# ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="star_memory",
        description="🌟 星辰记忆 STAR-MEMORY v2.1 — 本地持久化上下文仓库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""示例:
  python3 star_memory.py init
  python3 star_memory.py add --title "核心理念" --content "本地主权AI" --tags "core"
  python3 star_memory.py search --keyword "龍魂"
  python3 star_memory.py inject STAR-2026-03-06-001
  python3 star_memory.py update STAR-2026-03-06-001 --content "新内容"
  python3 star_memory.py dna STAR-2026-03-06-001
  python3 star_memory.py history STAR-2026-03-06-001
  python3 star_memory.py bridge
  python3 star_memory.py audit --limit 20
  python3 star_memory.py status"""
    )
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("init",   help="初始化仓库（首次使用）")
    sub.add_parser("status", help="查看系统状态")

    a = sub.add_parser("add",  help="添加新记忆")
    a.add_argument("--title",   "-t", required=True)
    a.add_argument("--content", "-c", required=True)
    a.add_argument("--type",          default="concept", help="concept/fact/task/insight")
    a.add_argument("--tags",          default="", help="标签，逗号分隔")
    a.add_argument("--source",        default="")

    u = sub.add_parser("update", help="更新记忆（生成新版本，不删除旧版本）")
    u.add_argument("id")
    u.add_argument("--content", "-c")
    u.add_argument("--title",   "-t")
    u.add_argument("--tags",          default=None)

    s = sub.add_parser("search", help="搜索记忆")
    s.add_argument("--tag",     "-g")
    s.add_argument("--type",    "-T")
    s.add_argument("--keyword", "-k")

    i = sub.add_parser("inject", help="显式注入记忆（输出到 stdout）")
    i.add_argument("id")
    i.add_argument("--yes", "-y", action="store_true", help="跳过确认")

    d = sub.add_parser("dna",     help="查看DNA追溯链")
    d.add_argument("id")

    h = sub.add_parser("history", help="查看版本历史")
    h.add_argument("id")

    au = sub.add_parser("audit",  help="查看审计日志")
    au.add_argument("--limit", "-n", type=int, default=20)

    br = sub.add_parser("bridge", help="同步到龍魂 memory.jsonl（TIER_2）")
    br.add_argument("ids", nargs="*", help="指定记忆ID（留空=全部）")

    return p


def main():
    parser = build_parser()
    args   = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return

    if args.cmd == "init":
        cmd_init()

    elif args.cmd == "status":
        show_status()

    elif args.cmd == "add":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        add_memory(args.title, args.content, args.type, tags, args.source)

    elif args.cmd == "update":
        tags = ([t.strip() for t in args.tags.split(",") if t.strip()]
                if args.tags is not None else None)
        update_memory(args.id, args.content, args.title, tags)

    elif args.cmd == "search":
        results = search_memories(args.tag, args.type, args.keyword)
        show_search_results(results)

    elif args.cmd == "inject":
        inject_memory(args.id, skip_confirm=args.yes)

    elif args.cmd == "dna":
        show_dna_chain(args.id)

    elif args.cmd == "history":
        show_history(args.id)

    elif args.cmd == "audit":
        show_audit_log(args.limit)

    elif args.cmd == "bridge":
        bridge_to_longhun(args.ids if args.ids else None)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
