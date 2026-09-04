#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-09-04-EXEC-RECAP-VIZ-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 协议: CC BY-NC-SA 4.0（核心思想层）
"""龍魂·执行复盘可视化系统 v1.0 · Execution Recap & Visualization

每次执行自动生成复盘：思维导图/决策状态图/执行链路图/时间线（Mermaid）+
DNA + 干支时间戳 + 系统快照 + 代码锚点。终端/浏览器/GitHub 均可查看。

命令（lh recap <sub>）:
  generate [--cmd x] [--args …] [--rc N] [--id ID] [--meta-json <b64>] [--auto] [--silent]
  view [id]                      # 最近一次或指定复盘
  list [--limit N]               # 复盘清单
  locate <关键词>                # 定位: 复盘文档+代码锚点(文件:行)+上下文
  codemap <id>                   # 代码调用链路图(引擎import链·Mermaid)
  snapshot <id>                  # 查看某次执行后系统快照
  diff <id1> <id2>               # 对比两次执行状态差异
  rollback <id> [--dry-run]      # 回滚预览(影响清单·不实际回滚)
  export <id> --format html|md|json   # 导出(html=可折叠/搜索高亮)
  search <关键词> [--limit N]    # 全库搜索·相关度排序
  timeline [--from YYYY-MM-DD] [--to …] [--mermaid]
  stats                          # 复盘统计
  diagnose <id>                  # AI 规则诊断报告(瓶颈/异常/建议)
  suggest <描述>                 # 推荐相似执行模式
  template list|show <名>|use <名>   # 模板系统
  config [--set k=v]             # 查看/修改配置
  protect <id>|unprotect <id>    # 永久保留(清理豁免)
  archive [--dry-run]            # 季度归档+过期清理(keep_days)
  qr <id>                        # 生成复盘二维码 png
  share <id> [--port N]          # 一键分享: 本地 HTML + 短链 + 二维码
  anchor <cmd> <file>            # 手动登记代码锚点(供 codemap/locate)

设计: 零三方(仅二维码走已装的 qrcode 可选) · 数据主权全本地 ~/.longhun/recap/ ·
去重: 同 id 不重生成 · 异步: lh.py 钩子 Popen 后台生成不阻塞主命令 ·
知识库: 完成即存 lh brain(静默·失败不阻塞) + 本地 kg 节点文件.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIN = Path(__file__).resolve().parent
HOME_LH = Path(os.environ.get("LH_RECAP_HOME") or (Path.home() / ".longhun"))
RECAP_DIR = HOME_LH / "recap"
RECAPS_DIR = RECAP_DIR / "recaps"
ARCHIVE_DIR = RECAP_DIR / "archive"
TPL_DIR = RECAP_DIR / "templates"
QR_DIR = RECAP_DIR / "qr"
CONFIG_FILE = RECAP_DIR / "config.json"
INDEX_FILE = RECAP_DIR / "index.json"
PROTECT_FILE = RECAP_DIR / "protect.json"
KG_FILE = RECAP_DIR / "kg_nodes.jsonl"
LOCK_FILE = RECAP_DIR / ".index.lock"

TOP = "诸葛鑫 | UID9622 · 龍芯北辰"
DEFAULT_TPL = "default"
AUTO_KEEP_DAYS = 90
RISK_WORDS = ("临时", "绕过", "风险", "hack", "workaround", "降级", "重试", "超时", "占位")
# 代码锚点: 命令 → 引擎文件（locate/codemap 用）
CMD_ANCHOR = {
    "topo": ("08_BIN/lh_topo.py", "拓扑引擎·verify/list/render"),
    "publish": ("08_BIN/lh_publish.py", "统一发布工具链·PR状态机"),
    "brain": ("08_BIN/lh_brain.py", "超级大脑记忆引擎"),
    "github": ("08_BIN/lh_github_perms.py", "GitHub社区联动·权限自检"),
    "fork": ("08_BIN/lh_fork_tracker.py", "fork追踪引擎"),
    "codeql": ("08_BIN/lh_codeql_listener.py", "CodeQL自动响应闭环"),
    "codeql-autofix": ("08_BIN/lh_codeql_autofix.py", "CodeQL自动修复引擎"),
    "codeql-dashboard": ("08_BIN/lh_codeql_autofix.py", "CodeQL状态面板"),
    "evolve": ("08_BIN/lh_persona_evolve.py", "人格按任务触发+经验累积"),
    "memory": ("08_BIN/lh_memory_arch.py", "记忆分层架构"),
    "military": ("08_BIN/lh_military.py", "军事调度引擎"),
    "skill": ("08_BIN/lh_skill_scheduler.py", "技能调度器"),
    "search": ("08_BIN/lh_search_engine.py", "搜索引擎"),
    "dh": ("08_BIN/lh_dh_dispatch.py", "数字人调动网关"),
    "mcp": ("08_BIN/lh_mcp_cmd.py", "鲲鹏MCP命令引擎"),
    "cnsh": ("08_BIN/cnsh.py", "CNSH统一CLI"),
    "fast-index": ("08_BIN/lh_index_fast.py", "快索引引擎"),
    "gate": ("bin/lh_gate.py", "操盘网关"),
    "agent": ("08_BIN/lh_persona_gate.py", "人格网关·命令统一执行器"),
    "model": ("08_BIN/lh_model_cmd.py", "AI模型统一入口"),
    "bench": ("08_BIN/lh_bench.py", "模型性能基准"),
    "recap": ("08_BIN/lh_recap.py", "本复盘引擎"),
}
DEFAULT_CONFIG = {
    "schema": "longhun-recap-config-v1", "enabled": True, "min_duration_ms": 800,
    "auto_always": False,
    "generate_for": ["topo", "bench", "publish", "agent", "dh", "brain", "model",
                     "github", "codeql", "fork", "evolve", "memory", "military",
                     "speak", "search", "mcp", "cnsh", "fast-index", "skill"],
    "skip_for": ["health", "status", "stats", "prstate", "list", "view", "help",
                 "recap", "recap-gen", "prstate"],
    "keep_days": 90, "template": "default", "qr_on_generate": False,
    "html_on_generate": False, "brain_save": True,
    "updated_at": datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
}
VALID_CFG_KEYS = {"enabled": bool, "auto_always": bool, "qr_on_generate": bool,
                  "html_on_generate": bool, "brain_save": bool, "min_duration_ms": int,
                  "keep_days": int, "template": str, "generate_for": list,
                  "skip_for": list}
MERMAID_MARK = "```mermaid"


# ─────────────────────────── 基础工具 ───────────────────────────
def _now() -> datetime:
    return datetime.now()


def _iso(dt: datetime | None = None) -> str:
    return (dt or _now()).strftime("%Y-%m-%dT%H:%M:%S")


def _today() -> str:
    return _now().strftime("%Y-%m-%d")


def _js(o) -> str:
    return json.dumps(o, ensure_ascii=False)


def _w(path: Path, s: str) -> None:
    path.write_text(s, encoding="utf-8")


def _r(path: Path, default=""):
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return default


def _lock():
    import fcntl
    LOCK_FILE.parent.mkdir(parents=True, exist_ok=True)
    f = LOCK_FILE.open("a+")
    try:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
    except Exception:
        pass
    return f


def _unlock(f) -> None:
    try:
        import fcntl
        fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except Exception:
        pass
    try:
        f.close()
    except Exception:
        pass


# ─────────────────────────── 配置 ───────────────────────────
def _load_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    if CONFIG_FILE.exists():
        try:
            cfg.update(json.loads(_r(CONFIG_FILE, "{}") or "{}"))
        except Exception:
            pass
    return cfg


def _save_config(cfg: dict) -> None:
    cfg["updated_at"] = _now().strftime("%Y-%m-%dT%H:%M:%S%z")
    _w(CONFIG_FILE, json.dumps(cfg, ensure_ascii=False, indent=2))


def cmd_config(argv) -> int:
    cfg = _load_config()
    i, set_pairs = 0, []
    while i < len(argv):
        if argv[i] == "--set" and i + 1 < len(argv):
            kv = argv[i + 1]
            if "=" in kv:
                set_pairs.append(kv.split("=", 1))
            i += 2
        else:
            i += 1
    if not set_pairs:
        print(json.dumps(cfg, ensure_ascii=False, indent=2))
        return 0
    for k, v in set_pairs:
        if k not in VALID_CFG_KEYS:
            print(f"🔴 未知配置键 {k}（合法: {', '.join(VALID_CFG_KEYS)}）")
            return 2
        typ = VALID_CFG_KEYS[k]
        try:
            if typ is bool:
                nv = str(v).lower() in ("1", "true", "yes", "on")
            elif typ is int:
                nv = int(v)
            elif typ is list:
                nv = [x.strip() for x in str(v).split(",") if x.strip()]
            else:
                nv = v
            cfg[k] = nv
            print(f"✅ config.{k} = {_js(nv)}")
        except Exception as e:
            print(f"🔴 {k}={v} 无效: {e}")
            return 2
    _save_config(cfg)
    return 0


# ─────────────────────────── DNA / 时间戳 ───────────────────────────
def dna_stamp(module: str, action: str) -> tuple[str, str]:
    """返回 (DNA, stamp)。优先调 lh_dna_stamp.py，失败本地降级。"""
    try:
        out = subprocess.run([sys.executable, str(BIN / "lh_dna_stamp.py"),
                              "--module", module, "--action", action, "--json"],
                             capture_output=True, text=True, timeout=25,
                             cwd=str(ROOT))
        d = json.loads((out.stdout or "").strip().splitlines()[-1])
        return d["dna"], d["stamp"]
    except Exception:
        pass
    ts = int(time.time())
    h = hashlib.sha256(f"{module}-{action}-UID9622-{ts}".encode()).hexdigest()[:8].upper()
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-{module}-{action}-{h}"
    return dna, f"🐉{_now().strftime('%Y')}·辰时·䷀乾·🟢"


# ─────────────────────────── 快照采集 ───────────────────────────
def _snapshot() -> dict:
    snap = {"ts": _iso(), "topo_root": "n/a", "topo_nodes": "n/a",
            "memorial_root": "n/a", "shame_count": "n/a", "recap_count": _index_count()}
    try:
        tf = HOME_LH / "topo" / "topo_index.json"
        if tf.exists():
            t = json.loads(_r(tf, "{}"))
            snap["topo_root"] = t.get("root_hash", "n/a")
            snap["topo_nodes"] = (t.get("stats") or {}).get("total_nodes", "n/a")
    except Exception:
        pass
    try:
        mf = ROOT / "07_AUDIT" / "contributor_memorial.json"
        if mf.exists():
            m = json.loads(_r(mf, "{}"))
            for k, v in m.items():
                if isinstance(v, str) and (k.lower() in ("root", "root_hash", "merkle",
                                                         "merkle_root", "hash") or "root" in k.lower()):
                    snap["memorial_root"] = v
                    break
            if snap["memorial_root"] == "n/a":
                snap["memorial_root"] = str(m.get("merkle", m.get("root_hash", "n/a")))
    except Exception:
        pass
    try:
        sw = HOME_LH / "shame_wall"
        if sw.exists():
            n = sum(1 for p in sw.iterdir() if p.is_file() and not p.name.endswith((".db", "-shm", "-wal")))
            snap["shame_count"] = str(n)
    except Exception:
        pass
    return snap


def _index_count() -> int:
    try:
        return len(_load_index().get("entries", []))
    except Exception:
        return 0


# ─────────────────────────── 索引 / 结构化 JSON ───────────────────────────
def _load_index() -> dict:
    if not INDEX_FILE.exists():
        return {"schema": "longhun-recap-index-v1", "entries": []}
    try:
        return json.loads(_r(INDEX_FILE, "{}"))
    except Exception:
        return {"schema": "longhun-recap-index-v1", "entries": []}


def _index_save(idx: dict) -> None:
    _w(INDEX_FILE, json.dumps(idx, ensure_ascii=False, indent=1))


def _find_entry(eid: str) -> dict | None:
    eid_l = eid.lower()
    entries = _load_index().get("entries", [])
    for e in entries:
        if e["id"].lower() == eid_l:
            return e
    for e in entries:  # 前缀匹配兜底
        if e["id"].lower().startswith(eid_l):
            return e
    return None


def _recap_paths(eid: str) -> tuple[Path, Path]:
    return RECAPS_DIR / f"{eid}.md", RECAPS_DIR / f"{eid}.json"


def _load_json(eid: str) -> dict:
    try:
        return json.loads(_r(RECAPS_DIR / f"{eid}.json", "{}"))
    except Exception:
        return {}


def _fmt_dur(ms) -> str:
    try:
        ms = float(ms)
    except Exception:
        return str(ms)
    if ms >= 60000:
        return f"{ms/60000:.1f}min"
    if ms >= 1000:
        return f"{ms/1000:.1f}s"
    return f"{int(ms)}ms"


# ─────────────────────────── 分词(CJK bigram·搜索用) ───────────────────────────
def _cjk(ch: str) -> bool:
    o = ord(ch)
    return 0x4E00 <= o <= 0x9FFF or 0x3400 <= o <= 0x4DBF or 0x9F80 <= o <= 0x9FFF


def _tokens(text: str) -> set[str]:
    t, n = set(), re.findall(r"[A-Za-z0-9_\-\.]+", text.lower())
    t.update(n)
    for tok in n:
        if len(tok) > 3:
            for i in range(1, len(tok)):
                t.add(tok[:i])
    parts = re.findall(r"[\u4e00-\u9fff]+", text)
    for p in parts:
        if len(p) == 1:
            t.add(p)
        for i in range(len(p) - 1):
            t.add(p[i:i + 2])
        for i in range(len(p) - 2):
            t.add(p[i:i + 3])
    return t


# ─────────────────────────── 代码锚点 ───────────────────────────
def _engine_for(cmd: str) -> str:
    if cmd in CMD_ANCHOR:
        return CMD_ANCHOR[cmd][0]
    return ""


def _anchor_line(file: str, kw: str) -> int:
    """在文件里实时定位关键词首次出现行（locate 用）。"""
    try:
        fp = ROOT / file if not file.startswith("bin") else ROOT / file
        if not fp.exists():
            fp = ROOT / "08_BIN" / Path(file).name
        if not fp.exists():
            return 0
        lines = _r(fp, "").splitlines()
        for i, ln in enumerate(lines, 1):
            if kw in ln:
                return i
    except Exception:
        pass
    return 0


def _rg_code(query: str, limit: int = 3) -> list[dict]:
    """实时在 08_BIN 检索关键词 → 代码锚点列表(文件:行:片段)。"""
    out = []
    try:
        r = subprocess.run(["rg", "-n", "--no-heading", "-m", "1",
                            re.escape(query), str(BIN)],
                           capture_output=True, text=True, timeout=8)
        for ln in (r.stdout or "").splitlines()[:limit]:
            if ":" not in ln:
                continue
            fp, no, *rest = ln.split(":", 2)
            out.append({"file": "08_BIN/" + Path(fp).name,
                        "line": int(no), "snippet": (rest[0] if rest else "")[:90]})
    except Exception:
        pass
    return out


def _imports_of(file: str) -> list[str]:
    """静态提取引擎文件的 lh_* import（codemap 调用链用）。"""
    imps = []
    try:
        fp = ROOT / file if not file.startswith("bin") else ROOT / file
        if not fp.exists():
            fp = ROOT / "08_BIN" / Path(file).name
        if not fp.exists():
            return imps
        for ln in _r(fp, "").splitlines():
            m = re.search(r"(?:import|from)\s+([a-zA-Z_][\w.]*lh[\w.]*)", ln)
            if m:
                n = m.group(1).split(".")[0]
                if n not in imps:
                    imps.append(n)
    except Exception:
        pass
    return imps[:8]


# ─────────────────────────── Mermaid 生成 ───────────────────────────
def _san(text: str, maxlen: int = 40) -> str:
    t = re.sub(r"[\[\]\(\)\{\}#\|\`]", "", str(text))
    t = t.replace("\n", " ").replace("::", ":")
    return t[:maxlen]


def mm_mindmap(root_cmd: str, nodes: list[dict]) -> str:
    """思维导图: 根(命令) → 执行各阶段。"""
    lines = ["mindmap", f"  root(({_san(root_cmd, 24)}))"]
    groups: dict[str, list[str]] = {}
    order: list[str] = []
    for n in nodes:
        g = n.get("group", "执行")
        if g not in groups:
            groups[g] = []
            order.append(g)
        groups[g].append(n.get("label", ""))
    for g in order:
        lines.append(f"  {_san(g, 10)}")
        for lbl in groups[g]:
            lines.append(f"    {_san(lbl, 30)}")
    return "\n".join(lines)


def mm_state(decisions: list[dict], rc) -> str:
    """决策与状态图: 快照→执行→成败; 决策逐条状态。"""
    ok = "ok" if str(rc) in ("0", "None", "") else "fail"
    L = ["stateDiagram-v2", "    [*] --> snap_pre", "    snap_pre: 📸 执行前快照捕获",
         "    snap_pre --> running: 执行开始"]
    okid, faid = "done_ok", "done_fail"
    L.append(f"    running --> {okid}: 退出码 {rc if str(rc) not in ('None','') else 0}")
    L.append(f"    running --> {faid}: 异常/非零")
    if ok == "ok":
        L += [f"    {okid} --> [*]", f"    {okid}: ✅ 完成·进入复盘"]
    else:
        L += [f"    {faid} --> diag", "    diag: 🔧 建议 lh recap diagnose", f"    diag --> [*]",
              f"    {faid}: ❌ 失败需复盘"]
    if decisions:
        L.append("    note right of running: 决策检查")
    for i, d in enumerate(decisions):
        st = d.get("state", "note")
        em = {"ok": "✅", "fail": "🔴", "note": "🟡"}.get(st, "🟡")
        L.append(f"    state d{i} {{ {em} {_san(d.get('text','决策'),44)} }}")
    return "\n".join(L)


def mm_chain(cmd: str, file: str, anchors: list[dict], extra: list[str] | None = None) -> str:
    """执行链路图 flowchart LR: lh.py 触发 → 引擎 → (快照/复盘)。含代码锚点。"""
    steps = anchors or []
    if not steps:
        steps = [{"file": file or "08_BIN/lh_recap.py", "note": "执行主体"}]
    L = ["flowchart LR", "    S[lh 命令触发] --> A0"]
    L.append(f"    A0[\"{_san(cmd, 18)} 执行\"] --> E0")
    first = True
    for i, a in enumerate(steps):
        fp, no = a.get("file", "?"), a.get("line")
        note = _san(a.get("note", "阶段"), 22)
        nm = f"A{i+1}"
        L.append(f"    E{i}[\"{note}\\n{Path(fp).name}{':'+str(no) if no else ''}\"] --> {nm}")
        L.append(f"    {nm}[\"🏁 {_san(a.get('outcome','进行'),14)}\"]")
    L.append("    subgraph R[复盘生成]")
    L.append("      R0[🧠 快照] --> R1[✍️ 渲染] --> R2[📌 DNA戳]")
    L.append("    end")
    L.append(f"    E{len(steps)-1 if steps else 0} --> R0")
    return "\n".join(L)


def mm_timeline(cmd: str, start_iso: str, dur_ms: float) -> str:
    """时间线图: 相对步进（入口→主体→收尾→复盘）。"""
    half = int(dur_ms / 2) if dur_ms else 0
    L = ["timeline", f"    title {_san(cmd, 30)} · 执行轨迹"]
    L.append(f"    入口({start_iso[11:19]}) : 命令触发")
    L.append(f"    执行({_fmt_dur(dur_ms)}) : 主进程运行 {int(dur_ms or 0)}ms")
    L.append("    收尾 : 快照捕获 · 复盘生成")
    L.append("    结果 : lh recap view 可回溯")
    return "\n".join(L)


# ─────────────────────────── AI 诊断(规则) ───────────────────────────
def _diagnose(d: dict) -> dict:
    rc = d.get("rc")
    dur = float(d.get("dur_ms") or 0)
    cmd = d.get("cmd", "")
    diag: dict = {"color": "🟢", "lines": [], "suggest": ""}
    if str(rc) not in ("0", "None", ""):
        diag["color"] = "🔴"
        diag["lines"].append(f"异常: 退出码 {rc} → 建议 `lh {cmd} --help` 或查看对应报告/日志定位")
    elif rc is None:
        diag["lines"].append("状态: 未知退出码（手动登记）· 建议复核")
    # 快照变化
    snap = d.get("snapshot") or {}
    if snap:
        diag["lines"].append(f"快照: topo_root={snap.get('topo_root')} · "
                             f"铭碑={snap.get('memorial_root')} · 耻辱墙={snap.get('shame_count')}")
    # 决策风险词
    risk = []
    for dec in d.get("decisions", []):
        txt = str(dec.get("text", ""))
        if any(w in txt for w in RISK_WORDS):
            risk.append(txt[:40])
    if risk:
        diag["color"] = "🟡"
        diag["lines"].append(f"⚠️ 风险决策 {len(risk)} 条: {'; '.join(risk[:3])} — 已登记供人工复核(耻辱墙终审权在 lh judge)")
    # 耗时
    avg = 0
    ent = _load_index().get("entries", [])
    same = [e for e in ent if e.get("cmd") == cmd]
    if len(same) > 1:
        avg = sum(float(e.get("dur_ms") or 0) for e in same) / len(same)
        if dur > avg * 2 > 0:
            diag["lines"].append(f"🟡 耗时瓶颈: {_fmt_dur(dur)} vs 同命令均值 {_fmt_dur(avg)} (>2x) → 建议拆分/并行/检查轮询等待")
    if avg:
        diag["lines"].append(f"耗时: {_fmt_dur(dur)}（同命令 {len(same)} 次均值 {_fmt_dur(avg)}）")
    else:
        diag["lines"].append(f"耗时: {_fmt_dur(dur)}")
    # 建议
    sug_map = {"publish": "lh publish status 看发布进度", "topo": "lh topo list 核对图谱",
               "github": "lh github test-perms 复测权限", "brain": "lh brain search 关键词 查记忆",
               "codeql": "lh codeql status 看检查进度", "mcp": "lh mcp health --remote 验连通",
               "bench": "lh bench list 查看基准结果", "model": "lh model status 看模型状态"}
    diag["suggest"] = sug_map.get(cmd, f"lh recap locate {cmd} 定位相关代码")
    if not diag["lines"]:
        diag["lines"].append("未发现明显异常·建议保持现状")
    return diag


# ─────────────────────────── 模板渲染 ───────────────────────────
def _template(name: str) -> str:
    fp = TPL_DIR / f"{name}.md"
    if fp.exists():
        return _r(fp)
    return _r(TPL_DIR / f"{DEFAULT_TPL}.md")


def _render(d: dict) -> str:
    cfg = _load_config()
    tpl = _template(d.get("template") or cfg.get("template") or DEFAULT_TPL)
    nodes = d.get("nodes") or []
    decs = d.get("decisions") or []
    args_s = " ".join(d.get("args") or [])
    mm_nodes = "\n".join(f"       {_san(n.get('label',''), 30)}" for n in nodes) or "       (无)"
    sd = mm_state(decs, d.get("rc"))
    anchors = d.get("anchors") or []
    chain = mm_chain(d.get("cmd", ""), d.get("engine", ""), anchors)
    tl = mm_timeline(d.get("cmd", ""), d.get("start_iso") or _iso(), float(d.get("dur_ms") or 0))
    snap = d.get("snapshot") or {}
    diag = d.get("diag") or _diagnose(d)
    anchors_txt = "\n".join(
        f"- `{a.get('file')}{':'+str(a.get('line')) if a.get('line') else ''}` — {a.get('note','')}"
        for a in anchors) or "- (无代码锚点·可 `lh recap anchor <cmd> <file>` 登记)"
    dec_txt = "\n".join(
        f"- {'✅' if dec.get('state')=='ok' else '🔴' if dec.get('state')=='fail' else '🟡'} {dec.get('text','')}"
        for dec in decs) or "- (无)"
    out_txt = (d.get("output") or "").strip() or "- (无)"
    vals = {
        "EXEC_ID": d.get("id", ""), "DNA": d.get("dna", ""), "TIMESTAMP": d.get("stamp", ""),
        "COLOR": diag.get("color", "🟢"), "TEMPLATE": d.get("template", ""), "MODE": d.get("mode", "manual"),
        "COMMAND": d.get("cmd", ""), "ARGS": f"`{args_s}`" if args_s else "—",
        "DURATION": _fmt_dur(d.get("dur_ms") or 0), "RC": str(d.get("rc", "")),
        "SUMMARY": d.get("summary", ""), "ROOT_CMD": d.get("cmd", ""),
        "ARGS_TXT": _san(args_s, 50) or "无参数", "NODES_MM": mm_nodes,
        "DECISIONS_SD": sd, "CHAIN_FL": chain, "TIMELINE_TL": tl,
        "SNAP_TOPO": snap.get("topo_root", "n/a"), "SNAP_MEMORIAL": snap.get("memorial_root", "n/a"),
        "SNAP_SHAME": snap.get("shame_count", "n/a"), "SNAP_RECAP_COUNT": snap.get("recap_count", "n/a"),
        "CODE_ANCHORS": anchors_txt, "DIAGNOSE": "\n".join(f"- {x}" for x in diag.get("lines", []))
        + (f"\n- 💡 建议: {diag.get('suggest','')}" if diag.get("suggest") else ""),
        "DECISIONS": dec_txt, "OUTPUT": out_txt,
    }
    body = tpl
    for k, v in vals.items():
        body = body.replace("{{" + k + "}}", str(v))
    if body.count(MERMAID_MARK) < 3:  # 自定义模板丢图 → 底部自动补全
        body += ("\n\n## 自动补全 · 三图\n\n```mermaid\n" + mm_mindmap(d.get("cmd", ""), nodes)
                 + "\n```\n\n```mermaid\n" + sd + "\n```\n\n```mermaid\n" + chain + "\n```\n")
    return body


# ─────────────────────────── generate 核心 ───────────────────────────
def _make_id(cmd: str) -> str:
    h = hashlib.sha256(f"{cmd}-{_now().timestamp()}".encode()).hexdigest()[:4]
    return f"recap-{_now().strftime('%Y%m%d%H%M%S')}-{h}"


def cmd_generate(argv) -> int:
    flags = {"cmd": "", "args": [], "rc": None, "id": "", "auto": False, "silent": False,
             "meta": None, "nodes": [], "decisions": [], "out": "", "template": "",
             "dur": 0, "start": ""}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--dur", "--start") and i + 1 < len(argv):
            flags[a[2:]], i = argv[i + 1], i + 1
        elif a == "--cmd" and i + 1 < len(argv):
            flags["cmd"], i = argv[i + 1], i + 1
        elif a == "--args":
            j = i + 1
            while j < len(argv) and not argv[j].startswith("--"):
                flags["args"].append(argv[j])
                j += 1
            i = j - 1
        elif a == "--rc" and i + 1 < len(argv):
            flags["rc"], i = argv[i + 1], i + 1
        elif a in ("--id", "--template") and i + 1 < len(argv):
            flags[a[2:]], i = argv[i + 1], i + 1
        elif a == "--meta-json" and i + 1 < len(argv):
            try:
                flags["meta"] = json.loads(base64.b64decode(argv[i + 1]).decode("utf-8"))
            except Exception:
                try:
                    flags["meta"] = json.loads(argv[i + 1])
                except Exception:
                    flags["meta"] = None
            i += 1
        elif a in ("--auto", "--silent"):
            flags[a[2:]] = True
        elif a == "--nodes" and i + 1 < len(argv):   # 逗号分隔文本节点
            flags["nodes"] = [x.strip() for x in argv[i + 1].split(",") if x.strip()]
            i += 1
        elif a == "--out" and i + 1 < len(argv):
            flags["out"], i = argv[i + 1], i + 1
        i += 1

    cmd = flags["cmd"] or "manual"
    if flags["auto"] and not cmd:
        return 0
    # 去重: 同 id 已存在 → 不重复生成
    eid = flags["id"] or _make_id(cmd)
    if _find_entry(eid):
        if not flags["silent"]:
            print(f"⏭️ 复盘已存在: {eid}（去重·不重复生成）")
        return 0

    meta = flags["meta"] or {}
    if flags["dur"]:
        meta["dur_ms"] = flags["dur"]
    if flags["start"]:
        meta["start_iso"] = flags["start"]
    nodes = flags["nodes"] or meta.get("nodes") or []
    decisions = flags["decisions"] or meta.get("decisions") or []
    if not nodes:
        eng = _engine_for(cmd)
        nodes = [
            {"label": f"执行 {cmd}", "file": eng or "08_BIN/lh_recap.py",
             "note": "命令主体", "group": "执行", "outcome": "运行"},
            {"label": "快照捕获", "file": "08_BIN/lh_recap.py", "note": "图谱哈希/铭碑/耻辱墙",
             "group": "收尾", "outcome": "捕获"},
            {"label": "复盘生成", "file": "08_BIN/lh_recap.py", "note": "三图+DNA+模板",
             "group": "收尾", "outcome": "成文"},
        ]
    if not decisions:
        rc_s = str(flags["rc"])
        decisions = [{"text": f"退出码 {rc_s if rc_s not in ('None','') else 0} → {'成功' if rc_s in ('0','') else '失败'}",
                      "state": "ok" if rc_s in ("0", "") else "fail"}]
    # 锚点补行号
    anchors = []
    for n in nodes:
        fp = n.get("file", "")
        if fp:
            anchors.append({"file": fp, "line": n.get("line") or 0,
                            "note": n.get("note", n.get("label", ""))})
    if not anchors:
        eng = _engine_for(cmd)
        if eng:
            anchors = [{"file": eng, "line": 0, "note": "命令主体"}]
    # 快照(execute 后)
    snap = _snapshot()
    dna, stamp = dna_stamp("recap", re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]", "", cmd)[:10] or "exec")
    diag = _diagnose({"rc": flags["rc"], "dur_ms": meta.get("dur_ms") or 0, "cmd": cmd,
                      "snapshot": snap, "decisions": decisions})
    d = {"schema": "longhun-recap-v1", "id": eid, "dna": dna, "stamp": stamp,
         "iso": _iso(), "start_iso": meta.get("start_iso", _iso()),
         "cmd": cmd, "args": flags["args"] or meta.get("args", []),
         "rc": flags["rc"], "dur_ms": meta.get("dur_ms") or 0,
         "mode": "auto" if flags["auto"] else "manual",
         "color": diag["color"], "snapshot": snap, "nodes": nodes,
         "decisions": decisions, "anchors": anchors,
         "output": flags["out"] or meta.get("out", ""),
         "diag": diag, "engine": _engine_for(cmd) or "08_BIN/lh_recap.py",
         "template": flags["template"] or _load_config().get("template", DEFAULT_TPL),
         "summary": f"{cmd} 执行完成 · rc={flags['rc'] if str(flags['rc']) not in ('None','') else 0} · {_fmt_dur(meta.get('dur_ms') or 0)}"}
    d["summary"] = f"{cmd} 执行{'完成 ✅' if str(flags['rc']) in ('0','') else '异常 🔴'} · {_fmt_dur(meta.get('dur_ms') or 0)} · {len(nodes)} 节点 · {len(decisions)} 决策 · DNA: {dna}"
    body = _render(d)
    RECAPS_DIR.mkdir(parents=True, exist_ok=True)
    _w(RECAPS_DIR / f"{eid}.md", body)
    _w(RECAPS_DIR / f"{eid}.json", _js(d))
    # 索引 append（去重）
    f = _lock()
    try:
        idx = _load_index()
        if not any(e["id"] == eid for e in idx.get("entries", [])):
            idx.setdefault("entries", []).insert(0, {
                "id": eid, "cmd": cmd, "args": flags["args"] or meta.get("args", []),
                "rc": flags["rc"], "dur_ms": meta.get("dur_ms") or 0,
                "dna": dna, "stamp": stamp, "iso": d["iso"], "color": diag["color"],
                "snapshot": snap, "template": d["template"]})
            _index_save(idx)
    finally:
        _unlock(f)
    # 知识库桥接: kg 节点 + brain(静默)
    try:
        _w_kg_line(d)
    except Exception:
        pass
    if _load_config().get("brain_save", True):
        try:
            note = f"复盘 {eid}: {cmd} {'✅' if str(flags['rc']) in ('0','') else '🔴'} {_fmt_dur(meta.get('dur_ms') or 0)} {dna}"
            subprocess.run([sys.executable, str(BIN / "lh_brain.py"), "save",
                            "--note", note, "--kw", f"recap,{cmd}", "--source", "recap", "--silent"],
                           cwd=str(ROOT), check=False, capture_output=True, timeout=20)
        except Exception:
            pass
    cfg = _load_config()
    if cfg.get("html_on_generate"):
        try:
            _write_html(d)
        except Exception:
            pass
    if not flags["silent"]:
        print(f"✅ 复盘已生成: {eid} · {diag['color']} · {len(nodes)} 节点 · {len(decisions)} 决策 · DNA: {dna}")
        print(f"📄 {RECAPS_DIR / eid}.md")
    return 0


def _w_kg_line(d: dict) -> None:
    RECAP_DIR.mkdir(parents=True, exist_ok=True)
    node = {"type": "recap", "id": d["id"], "dna": d["dna"], "cmd": d["cmd"],
            "rc": d["rc"], "iso": d["iso"], "color": d["color"],
            "links": ["brain-memory", "code-anchor"]}
    with KG_FILE.open("a", encoding="utf-8") as f:
        f.write(_js(node) + "\n")


# ─────────────────────────── view / list ───────────────────────────
def cmd_view(argv) -> int:
    eid = argv[0] if argv else ""
    if eid and eid.startswith("--"):
        eid = ""
    if not eid:
        idx = _load_index().get("entries", [])
        if not idx:
            print("暂无复盘。跑一个复杂命令后自动生成，或 `lh recap generate --cmd topo --rc 0` 手动生成")
            return 0
        eid = idx[0]["id"]
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}（lh recap list）")
        return 2
    fp = RECAPS_DIR / f"{ent['id']}.md"
    if not fp.exists():
        print(f"🔴 复盘文档缺失 {fp}")
        return 2
    print(f"═══ 🔄 {ent['id']} · {ent.get('cmd')} · {ent.get('color')} ═══")
    print(_r(fp))
    return 0


def cmd_list(argv) -> int:
    limit = 10
    i = 0
    while i < len(argv):
        if argv[i] == "--limit" and i + 1 < len(argv):
            limit = int(argv[i + 1]); i += 1
        i += 1
    entries = _load_index().get("entries", [])
    if not entries:
        print("暂无复盘记录")
        return 0
    print(f"{'ID':<34} {'命令':<18} {'RC':<4} {'耗时':<8} 结论")
    for e in entries[:limit]:
        print(f"{e['id']:<34} {e.get('cmd','')[:16]:<18} {str(e.get('rc',''))[:3]:<4} "
              f"{_fmt_dur(e.get('dur_ms') or 0):<8} {e.get('color','')}")
    print(f"\n共 {len(entries)} 条 · 更多: lh recap list --limit {limit + 10}")
    return 0


# ─────────────────────────── locate / search ───────────────────────────
def _corpus(e: dict) -> str:
    j = _load_json(e["id"]) or {}
    return " ".join([str(e.get("cmd", "")), " ".join(e.get("args") or []),
                     j.get("summary", ""),
                     " ".join(str(n.get("label", "")) for n in j.get("nodes", [])),
                     " ".join(str(dc.get("text", "")) for dc in j.get("decisions", [])),
                     " ".join(str(a.get("note", "")) + a.get("file", "") for a in j.get("anchors", []))])


def _rank(q: str) -> list[dict]:
    qt = _tokens(q)
    hits = []
    for e in _load_index().get("entries", []):
        txt = _corpus(e)
        tt = _tokens(txt)
        score = len(qt & tt)
        if score:
            hits.append({"id": e["id"], "cmd": e.get("cmd"), "rc": e.get("rc"),
                         "score": score, "iso": e.get("iso", "")})
    hits.sort(key=lambda x: -x["score"])
    return hits


def cmd_search(argv) -> int:
    q, limit = "", 5
    i = 0
    while i < len(argv):
        if argv[i] == "--limit" and i + 1 < len(argv):
            limit = int(argv[i + 1]); i += 1
        else:
            q = argv[i]
        i += 1
    if not q:
        print("用法: lh recap search <关键词>")
        return 1
    hits = _rank(q)
    if not hits:
        print(f"未在 {_index_count()} 条复盘中命中「{q}」")
        return 0
    print(f"🔎 「{q}」命中 {len(hits)} 条复盘（相关度排序）:")
    for h in hits[:limit]:
        j = _load_json(h["id"]) or {}
        print(f"  {h['score']}分  {h['id']} · {h['cmd']} · {h['iso'][:16]} · rc={h.get('rc')}")
        for n in j.get("nodes", [])[:2]:
            print(f"      ↳ {n.get('label','')} [{n.get('file','')}]")
    return 0


def cmd_locate(argv) -> int:
    q = " ".join(argv) if argv else ""
    if not q:
        print("用法: lh recap locate <关键词>（返回复盘文档路径+代码锚点+上下文）")
        return 1
    print(f"📍 locate「{q}」")
    hits = _rank(q)
    if hits:
        h = hits[0]
        j = _load_json(h["id"]) or {}
        print(f"  复盘: {RECAPS_DIR / (h['id'] + '.md')} · {h['cmd']} · {h['iso'][:16]}")
        ctx = []
        for n in j.get("nodes", []):
            if q in str(n.get("label", "")) or q in str(n.get("note", "")):
                ctx.append(n)
        for dc in j.get("decisions", []):
            if q in str(dc.get("text", "")):
                ctx.append({"label": f"决策: {dc.get('text','')[:60]}", "file": j.get("engine", "")})
        for a in j.get("anchors", []):
            if q in str(a.get("note", "")) or q in a.get("file", ""):
                ctx.append({"label": a.get("note", ""), "file": a.get("file")})
        for c in ctx[:5]:
            f = c.get("file", "")
            line = c.get("line") or _anchor_line(f, q)
            lnk = f"{f}:{line}" if line else f
            print(f"    ⛓️ {c.get('label','')[:70]} → {lnk}")
    else:
        print(f"  复盘库无命中「{q}」")
    print("  💻 代码锚点（实时检索 08_BIN）:")
    codes = _rg_code(q)
    if codes:
        for c in codes[:4]:
            print(f"    🧬 08_BIN/{Path(c['file']).name}:{c['line']}  {c.get('snippet','')}")
    else:
        print("    (08_BIN 未直接命中·可换更短关键词)")
    return 0


# ─────────────────────────── codemap ───────────────────────────
def cmd_codemap(argv) -> int:
    eid = argv[0] if argv else ""
    if not eid:
        print("用法: lh recap codemap <execution-id>")
        return 1
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}")
        return 2
    j = _load_json(ent["id"]) or {}
    engine = j.get("engine") or _engine_for(ent.get("cmd", ""))
    files = [engine] if engine else []
    for a in j.get("anchors", []):
        if a.get("file") not in files:
            files.append(a["file"])
    print(f"🧬 代码调用链路 · {ent['id']}（{ent.get('cmd')}）\n")
    L = ["flowchart LR"]
    L.append("    T[lh.py 触发]")
    seen, prev = set(), None
    for i, fp in enumerate(files):
        name = f"F{i}"
        L.append(f"    {name}[\"{Path(fp).name}\"]")
        seen.add(fp)
        if prev is not None:
            L.append(f"    {prev} --> {name}")
        prev = name
    # import 链扩展: 主引擎 import 的 lh_* 引擎
    if engine:
        imps = _imports_of(engine)
        for jj, im in enumerate(imps):
            L.append(f"    I{jj}[\"{im}\"]")
            L.append(f"    F0 --> I{jj}")
    L.append(f"    {prev} --> R[🧠 lh_recap.py 复盘]")
    print("\n".join(L))
    print("\n  💻 涉及代码文件:")
    for fp in files:
        print(f"    - {fp}")
    return 0


# ─────────────────────────── snapshot / diff / rollback ───────────────────────────
def _fmt_snap(s: dict | None) -> str:
    s = s or {}
    return (f"topo_root={s.get('topo_root','n/a')} · topo_nodes={s.get('topo_nodes','n/a')} · "
            f"铭碑={s.get('memorial_root','n/a')} · 耻辱墙={s.get('shame_count','n/a')} · "
            f"复盘数={s.get('recap_count','n/a')} @ {s.get('ts','')}")


def cmd_snapshot(argv) -> int:
    eid = argv[0] if argv else ""
    if not eid:
        print("用法: lh recap snapshot <execution-id>")
        return 1
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}")
        return 2
    j = _load_json(ent["id"]) or {}
    snap = j.get("snapshot") or ent.get("snapshot") or {}
    print(f"📸 执行前状态快照 · {ent['id']}（{ent.get('cmd')} · {ent.get('iso','')[:16]}）")
    print("  " + _fmt_snap(snap))
    return 0


def cmd_diff(argv) -> int:
    if len(argv) < 2:
        print("用法: lh recap diff <id1> <id2>")
        return 1
    a, b = _find_entry(argv[0]), _find_entry(argv[1])
    if not a or not b:
        print("🔴 未找到复盘（lh recap list）")
        return 2
    ja, jb = _load_json(a["id"]) or {}, _load_json(b["id"]) or {}
    sa, sb = ja.get("snapshot") or a.get("snapshot") or {}, jb.get("snapshot") or b.get("snapshot") or {}
    print(f"📊 状态对比\n  A: {a['id']} · {a.get('cmd')} · {a.get('iso','')[:16]}\n  B: {b['id']} · {b.get('cmd')} · {b.get('iso','')[:16]}")
    keys = sorted(set(sa) | set(sb))
    shown = 0
    for k in keys:
        if k == "ts":
            continue
        va, vb = sa.get(k, "—"), sb.get(k, "—")
        if va == vb:
            continue
        print(f"  🔴 {k:<14} {str(va):<18} → {vb}")
        shown += 1
    if not shown:
        print("  ✅ 两快照一致·无系统状态差异")
    return 0


def cmd_rollback(argv) -> int:
    eid = argv[0] if argv else ""
    dry = "--dry-run" in argv
    if not eid or eid.startswith("--"):
        print("用法: lh recap rollback <execution-id> [--dry-run]")
        return 1
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}")
        return 2
    j = _load_json(ent["id"]) or {}
    snap = j.get("snapshot") or {}
    cur = _snapshot()
    print(f"↩️ 回滚预览 · {ent['id']}（{ent.get('cmd')}）[{'dry-run' if dry else '影响评估'}]")
    print(f"  执行后状态: {_fmt_snap(snap)}")
    print(f"  当前状态:   {_fmt_snap(cur)}")
    changes = []
    for k in ("topo_root", "memorial_root", "shame_count"):
        if snap.get(k) and cur.get(k) and snap[k] != cur[k]:
            changes.append((k, snap[k], cur[k]))
    if not changes:
        print("  ✅ 与执行后快照一致·回滚无实质影响（无需动作）")
        return 0
    print(f"  🟡 检出 {len(changes)} 处系统状态漂移:")
    acts = []
    for k, va, vb in changes:
        print(f"    - {k}: {va} → {vb}")
        if k == "topo_root":
            acts.append("拓扑根哈希变化→建议 `lh topo list` 复核图谱源文件")
        elif k == "shame_count":
            acts.append("耻辱墙计数变化→`lh judge` 查看(终审人工)")
    if acts:
        print("  影响清单（dry-run·不实际回滚）:")
        for x in acts:
            print(f"    ⚠️ {x}")
    print("  ℹ️ 龍魂原则: 数据不删除只冻结·回滚以复核/校正替代物理回滚")
    return 0


# ─────────────────────────── export(html) ───────────────────────────
def _md_to_html(body: str) -> str:
    """极简 md→html（标题/表格/代码/列表/引用）。Mermaid 原样保留给 JS 渲染。"""
    lines, in_code, code_buf, html = body.splitlines(), False, [], []
    for ln in lines:
        if ln.strip().startswith("```"):
            if in_code:
                lang = "mermaid" if code_buf and code_buf[0].strip().lower() in ("mermaid",) else ""
                first = code_buf[0] if code_buf else ""
                rest = code_buf[1:] if lang and len(code_buf) > 1 else code_buf
                if lang:
                    html.append(f'<div class="mermaid">{chr(10).join(rest)}</div>')
                else:
                    html.append("<pre><code>" + chr(10).join(code_buf) + "</code></pre>")
                code_buf, in_code = [], False
            else:
                in_code, code_buf = True, []
            continue
        if in_code:
            code_buf.append(ln); continue
        s = ln.strip()
        if not s:
            continue
        if s.startswith("## "):
            html.append(f"<h2>{s[3:]}</h2>")
        elif s.startswith("# "):
            html.append(f"<h1>{s[2:]}</h1>")
        elif s.startswith("> "):
            html.append(f"<blockquote>{s[2:]}</blockquote>")
        elif s.startswith("- ") or s.startswith("* "):
            html.append(f"<li>{s[2:]}</li>")
        elif s.startswith("|"):
            html.append("<tr>" + "".join(f"<td>{c.strip()}</td>" for c in s.split("|")[1:-1]) + "</tr>")
        else:
            html.append(f"<p>{s}</p>")
    if code_buf:
        html.append("<pre><code>" + chr(10).join(code_buf) + "</code></pre>")
    return "\n".join(html)


def _write_html(d: dict) -> Path:
    body = _render(d)
    html_body = _md_to_html(body)
    tpl = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🔄 龍魂执行复盘 · {d['id']}</title>
<style>
 body{{font-family:-apple-system,'PingFang SC','Microsoft YaHei',sans-serif;max-width:900px;margin:0 auto;padding:20px;background:#0f1115;color:#e6e6e6;line-height:1.6}}
 h1{{font-size:1.4em}} h2{{margin-top:28px;padding:6px 10px;background:#1c2129;border-left:4px solid #c9a86a;cursor:pointer}}
 h2:hover{{background:#262d38}} h2::after{{content:' ▾';color:#888}}
 h2.collapsed::after{{content:' ▸'}}
 section.collapsed .body{{display:none}}
 .body{{padding:8px 4px}}
 table{{border-collapse:collapse;margin:8px 0;width:100%}} td,th{{border:1px solid #333;padding:5px 10px;font-size:.92em}}
 pre{{background:#1c2129;padding:10px;border-radius:6px;overflow-x:auto}} code{{font-family:ui-monospace,Menlo,monospace}}
 blockquote{{border-left:3px solid #c9a86a;margin:8px 0;padding:4px 12px;color:#bbb}}
 #q{{width:70%;padding:8px;border:1px solid #444;border-radius:6px;background:#1c2129;color:#eee}}
 mark{{background:#7a5a2e;color:#fff;border-radius:2px;padding:0 2px}}
 .meta{{color:#999;font-size:.85em}} .mermaid{{text-align:center;margin:12px 0}}
</style></head><body>
<h1>🔄 龍魂执行复盘 · {d['id']}</h1>
<p class="meta">DNA: {d['dna']}<br>时间戳: {d['stamp']} · 归属名: {TOP}</p>
<div><input id="q" placeholder="🔍 搜索本页(高亮)…"><button onclick="docSearch()">搜索</button>
<button onclick="toggleAll()">全部折叠/展开</button></div>
{html_body}
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<script>
 mermaid.initialize({{startOnLoad:true,theme:'dark',securityLevel:'loose'}});
 document.querySelectorAll('h2').forEach(function(h){{h.onclick=function(){{this.classList.toggle('collapsed');this.parentElement.classList.toggle('collapsed')}}}});
 function toggleAll(){{document.querySelectorAll('section').forEach(function(s){{s.classList.toggle('collapsed')}})}};
 function docSearch(){{var t=document.getElementById('q').value.trim();document.querySelectorAll('mark').forEach(function(m){{m.outerHTML=m.textContent}});if(!t)return;var re=new RegExp(t.replace(/[.*+?^${{}}()|[\\]\\\\]/g,'\\\\$&'),'gi');var w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);var n;while(n=w.nextNode()){{if(n.nodeType===3&&re.test(n.nodeValue)){{var p=n.parentNode;if(p&&p.tagName!=='MARK'){{var sp=document.createElement('span');var s2=document.createElement('mark');var rest=n.nodeValue;var m;sp.appendChild(document.createTextNode(''));while((m=re.exec(rest))){{sp.appendChild(document.createTextNode(rest.slice(0,m.index)));s2=document.createTextNode(m[0]);var mk=document.createElement('mark');mk.appendChild(s2);sp.appendChild(mk);rest=rest.slice(m.index+m[0].length)}}sp.appendChild(document.createTextNode(rest));p.replaceChild(sp,n)}}}}}}}}
</script>
</body></html>"""
    html_f = RECAPS_DIR / f"{d['id']}.html"
    _w(html_f, tpl)
    return html_f


def cmd_export(argv) -> int:
    eid, fmt = "", "html"
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ("--format", "-f") and i + 1 < len(argv):
            fmt, i = argv[i + 1], i + 1
        elif a.startswith("--") and "=" in a and "format" in a:
            fmt = a.split("=", 1)[1]
        else:
            eid = a
        i += 1
    if not eid:
        print("用法: lh recap export <execution-id> --format html|md|json")
        return 1
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}")
        return 2
    fmt = (fmt or "html").lower()
    if fmt == "json":
        src = RECAPS_DIR / f"{ent['id']}.json"
        print(_r(src))
        return 0
    if fmt == "md":
        print(_r(RECAPS_DIR / f"{ent['id']}.md"))
        return 0
    d = _load_json(ent["id"]) or {"id": ent["id"]}
    try:
        fp = _write_html(d)
    except Exception as e:
        print(f"🔴 HTML 导出失败: {e}")
        return 2
    print(f"✅ HTML 已导出: {fp}")
    print(f"   file://{fp}")
    return 0


# ─────────────────────────── timeline / stats ───────────────────────────
def cmd_timeline(argv) -> int:
    frm, to, mm = "", "", False
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--from" and i + 1 < len(argv):
            frm, i = argv[i + 1], i + 1
        elif a == "--to" and i + 1 < len(argv):
            to, i = argv[i + 1], i + 1
        elif a == "--mermaid":
            mm = True
        i += 1
    frm = frm or (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    to = to or datetime.now().strftime("%Y-%m-%d")
    entries = [e for e in _load_index().get("entries", [])
               if frm <= e.get("iso", "")[:10] <= to]
    entries.sort(key=lambda e: e.get("iso", ""))
    if not entries:
        print(f"时间段 {frm} ~ {to} 无复盘")
        return 0
    if mm:
        L = ["timeline", f"    title 执行复盘 {frm} → {to}"]
        cur = ""
        for e in entries:
            day = e["iso"][:10]
            if day != cur:
                cur = day
                L.append(f"    {day}")
            L[-1] += f" : {_san(e.get('cmd',''),18)}({e.get('id','')[-6:]})"
        print("\n".join(L))
        return 0
    print(f"📅 执行时间线 {frm} ~ {to}（{len(entries)} 次）")
    for e in entries:
        st = e.get("iso", "")[11:19]
        mark = "🟢" if str(e.get("rc")) in ("0", "") else "🔴"
        print(f"  {e['iso'][:10]} {st}  {mark} {e.get('cmd','')} {_fmt_dur(e.get('dur_ms') or 0)} · {e['id']}")
    return 0


def cmd_stats(argv) -> int:
    entries = _load_index().get("entries", [])
    if not entries:
        print("暂无复盘统计")
        return 0
    total = len(entries)
    durs = [float(e.get("dur_ms") or 0) for e in entries]
    avg = sum(durs) / total if durs else 0
    ok = sum(1 for e in entries if str(e.get("rc")) in ("0", ""))
    fail = total - ok
    top = Counter(e.get("cmd", "?") for e in entries).most_common(5)
    this_week = sum(1 for e in entries if e.get("iso", "")[:10] >= _today())
    print(f"📊 复盘统计 · 共 {total} 条")
    print(f"  成功率: {ok}/{total} ({ok / total * 100:.0f}%) · 失败 {fail}")
    print(f"  平均耗时: {_fmt_dur(avg)}")
    print(f"  最常执行节点:")
    for c, n in top:
        print(f"    {c}: {n} 次")
    print(f"  本周(今日起7天): {this_week} 次 · 库位置: {RECAP_DIR}")
    return 0


# ─────────────────────────── diagnose / suggest ───────────────────────────
def cmd_diagnose(argv) -> int:
    eid = argv[0] if argv else ""
    if not eid:
        print("用法: lh recap diagnose <execution-id>")
        return 1
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}")
        return 2
    d = _load_json(ent["id"]) or ent
    diag = _diagnose(d)
    print(f"🔬 AI 诊断报告 · {ent['id']}（{ent.get('cmd')}）{diag['color']}")
    for x in diag.get("lines", []):
        print(f"  {x}")
    if diag.get("suggest"):
        print(f"  💡 建议: {diag['suggest']}")
    return 0


def cmd_suggest(argv) -> int:
    q = " ".join(argv) if argv else ""
    if not q:
        print("用法: lh recap suggest <描述>（如「发布一次公告」「跑一次拓扑验证」）")
        return 1
    hits = _rank(q)
    if not hits:
        print(f"历史复盘无「{q}」相近模式")
        return 0
    print(f"🧩 相似执行模式推荐（基于历史 {_index_count()} 条复盘）:")
    for h in hits[:3]:
        e = _find_entry(h["id"]) or {}
        print(f"  • {h['cmd']}（相关度 {h['score']}·{h['iso'][:10]}）rc={e.get('rc')} "
              f"耗时 {_fmt_dur(e.get('dur_ms') or 0)} {e.get('color','')}")
        print(f"    复盘: {h['id']} · 查看 lh recap view {h['id']}")
    return 0


# ─────────────────────────── template ───────────────────────────
def cmd_template(argv) -> int:
    if not argv:
        print("用法: lh recap template list|show <名>|use <名>")
        return 1
    sub = argv[0]
    tpls = sorted(p.stem for p in TPL_DIR.glob("*.md")) if TPL_DIR.exists() else []
    if sub == "list":
        cur = _load_config().get("template", DEFAULT_TPL)
        print(f"📋 可用模板（当前: {cur}）:")
        for t in tpls:
            star = " ⭐" if t == cur else ""
            print(f"  - {t}{star}")
        print("  自定义: 复制模板到 ~/.longhun/recap/templates/<名>.md（变量见 default.md）")
        return 0
    if sub == "use" and len(argv) > 1:
        name = argv[1]
        if name not in tpls:
            print(f"🔴 模板不存在: {name}（lh recap template list）")
            return 2
        cfg = _load_config()
        cfg["template"] = name
        _save_config(cfg)
        print(f"✅ 当前模板 → {name}")
        return 0
    if sub == "show" and len(argv) > 1:
        fp = TPL_DIR / f"{argv[1]}.md"
        if not fp.exists():
            print(f"🔴 模板不存在: {argv[1]}")
            return 2
        print(_r(fp))
        return 0
    print("用法: lh recap template list|show <名>|use <名>")
    return 1


# ─────────────────────────── protect / archive ───────────────────────────
def _protect_list() -> list[str]:
    try:
        return json.loads(_r(PROTECT_FILE, "[]") or "[]")
    except Exception:
        return []


def cmd_protect(argv) -> int:
    if not argv:
        print("用法: lh recap protect <id> | unprotect <id>")
        return 1
    eid = argv[0] if not argv[0].startswith("un") else ""
    op = "unprotect" if argv and argv[0].startswith("un") else "protect"
    eid = argv[0][3:].lstrip("-") if op == "unprotect" else (argv[0] if argv else "")
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}")
        return 2
    pl = _protect_list()
    if op == "protect":
        if ent["id"] not in pl:
            pl.append(ent["id"])
            _w(PROTECT_FILE, _js(pl))
        print(f"🔒 已永久保留: {ent['id']}（清理豁免）")
    else:
        if ent["id"] in pl:
            pl.remove(ent["id"])
            _w(PROTECT_FILE, _js(pl))
        print(f"🔓 已解除保留: {ent['id']}")
    return 0


def _quarter(dt: datetime) -> str:
    return f"{dt.year}-Q{(dt.month - 1) // 3 + 1}"


def cmd_archive(argv) -> int:
    dry = "--dry-run" in argv
    cfg = _load_config()
    keep = int(cfg.get("keep_days", AUTO_KEEP_DAYS))
    cutoff = _now() - timedelta(days=keep)
    protected = set(_protect_list())
    moved = []
    for e in _load_index().get("entries", []):
        if e["id"] in protected:
            continue
        try:
            dt = datetime.strptime(e["iso"][:19], "%Y-%m-%dT%H:%M:%S")
        except Exception:
            continue
        if dt < cutoff:
            q = _quarter(dt)
            dest = ARCHIVE_DIR / q
            md, js = _recap_paths(e["id"])
            if not dry:
                dest.mkdir(parents=True, exist_ok=True)
                for src in (md, js):
                    if src.exists():
                        shutil.move(str(src), str(dest / src.name))
            moved.append((e["id"], q, e.get("cmd", ""), e.get("iso", "")))
    if not moved:
        print(f"✅ 无过期复盘（keep_days={keep}·截止 {cutoff.date()}）" + ("[dry-run]" if dry else ""))
        return 0
    print(f"{'📦 归档预览' if dry else '📦 归档执行'}（keep_days={keep}）:")
    for eid, q, cmd, iso in moved:
        print(f"  - {eid} {cmd} {iso[:10]} → archive/{q}/")
    if dry:
        print("  未实际移动（--dry-run）")
    else:
        summ = ARCHIVE_DIR / "ARCHIVE-SUMMARY.md"
        rows = "\n".join(f"- {eid} · {cmd} · {iso[:10]}" for eid, _, cmd, iso in moved)
        _w(summ, (f"# 🗄️ 复盘归档摘要\n\n> 生成 {_iso()} · {len(moved)} 条归档\n\n{rows}\n"))
        # 从索引移除已归档
        f = _lock()
        try:
            idx = _load_index()
            ids = {eid for eid, *_ in moved}
            idx["entries"] = [e for e in idx["entries"] if e["id"] not in ids]
            _index_save(idx)
        finally:
            _unlock(f)
        print(f"  归档摘要: {summ}")
    return 0


# ─────────────────────────── qr / share ───────────────────────────
def _qr_png(eid: str, url: str) -> Path | None:
    try:
        import qrcode  # 已装可选
        img = qrcode.make(url)
        QR_DIR.mkdir(parents=True, exist_ok=True)
        fp = QR_DIR / f"{eid}.png"
        img.save(fp)
        return fp
    except Exception:
        return None


def cmd_qr(argv) -> int:
    eid = argv[0] if argv else ""
    if not eid:
        print("用法: lh recap qr <execution-id>")
        return 1
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}")
        return 2
    md = RECAPS_DIR / f"{ent['id']}.md"
    url = md.as_uri()
    fp = _qr_png(ent["id"], url)
    if fp:
        print(f"✅ 二维码: {fp}（扫码打开 {url}）")
        print(f"   DNA: {ent.get('dna')}")
    else:
        print(f"🟡 二维码库不可用·直接打开: {url}")
    return 0


def cmd_share(argv) -> int:
    eid, port = "", 8769
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--port" and i + 1 < len(argv):
            port = int(argv[i + 1]); i += 1
        elif not a.startswith("--"):
            eid = a
        i += 1
    if not eid:
        print("用法: lh recap share <execution-id> [--port N]")
        return 1
    ent = _find_entry(eid)
    if not ent:
        print(f"🔴 未找到复盘 {eid}")
        return 2
    d = _load_json(ent["id"]) or {"id": ent["id"], "cmd": ent.get("cmd")}
    try:
        html_f = _write_html(d)
    except Exception as ex:
        print(f"🔴 导出失败: {ex}")
        return 2
    url = f"http://127.0.0.1:{port}/recaps/{ent['id']}.html"
    fp = _qr_png(ent["id"], url)
    # 启动一次性静态服务(后台)
    try:
        subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1",
                          "--directory", str(RECAP_DIR)],
                         cwd=str(ROOT), stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL)
    except Exception:
        pass
    print(f"🔗 短链分享: {ent['id']}")
    print(f"   地址: {url}")
    print(f"   DNA: {ent.get('dna')}")
    print(f"   二维码: {fp if fp else '(qrcode 不可用·直接访问地址)'}")
    print(f"   ⏸ 服务已后台启动·完成后: lsof -nP -i :{port} | grep LISTEN | awk '{{print $2}}' | xargs kill")
    return 0


# ─────────────────────────── anchor 手动登记 ───────────────────────────
_EXTRA_ANCHOR_FILE = RECAP_DIR / "extra_anchors.json"


def cmd_anchor(argv) -> int:
    if len(argv) < 2:
        print("用法: lh recap anchor <cmd> <file[:line]>")
        return 1
    cmd, ref = argv[0], argv[1]
    fp, line = ref, 0
    if ":" in ref and ref.rsplit(":", 1)[1].isdigit():
        fp, line = ref.rsplit(":", 1)
        line = int(line)
    extra = {}
    if _EXTRA_ANCHOR_FILE.exists():
        try:
            extra = json.loads(_r(_EXTRA_ANCHOR_FILE, "{}"))
        except Exception:
            extra = {}
    extra[cmd] = {"file": fp, "line": line}
    _w(_EXTRA_ANCHOR_FILE, _js(extra))
    print(f"✅ 锚点已登记: {cmd} → {fp}:{line or '?'}（本会话生效·引擎内建见 lh_recap.py CMD_ANCHOR）")
    return 0


def _engine_for_extra(cmd: str) -> str:
    try:
        extra = json.loads(_r(_EXTRA_ANCHOR_FILE, "{}"))
        if cmd in extra:
            return extra[cmd].get("file", "")
    except Exception:
        pass
    return ""


# ─────────────────────────── 主分发 ───────────────────────────
USAGE = """🔄 lh recap — 龍魂执行复盘可视化
  generate       生成复盘(自动钩子或手动)  lh recap generate --cmd topo --rc 0
  view [id]      查看复盘(默认最近)        lh recap view
  list           复盘清单                  lh recap list
  locate <词>    定位(复盘+代码锚点)       lh recap locate "决策"
  codemap <id>   代码调用链路图            lh recap codemap <id>
  snapshot <id>  执行快照                  lh recap snapshot <id>
  diff <a> <b>   状态差异                  lh recap diff <id1> <id2>
  rollback <id>  回滚预览(--dry-run)       lh recap rollback <id> --dry-run
  export <id>    导出 html/md/json         lh recap export <id> --format html
  search <词>    全库搜索·排序             lh recap search 图谱
  timeline       时间线[--from][--to][--mermaid]
  stats          统计
  diagnose <id>  AI 诊断报告
  suggest <描述> 推荐相似执行
  template       list|show|use
  config         [--set k=v]
  protect <id> / unprotect <id>
  archive        [--dry-run] 季度归档+清理
  qr <id>        二维码
  share <id>     分享(本地短链+二维码)
  anchor <cmd> <file[:line]>  登记代码锚点
"""


def main() -> int:
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    sub = argv[0]
    rest = argv[1:]
    if sub in ("generate", "gen"):
        return cmd_generate(rest)
    if sub == "view":
        return cmd_view(rest)
    if sub == "list":
        return cmd_list(rest)
    if sub == "locate":
        return cmd_locate(rest)
    if sub == "codemap":
        return cmd_codemap(rest)
    if sub == "snapshot":
        return cmd_snapshot(rest)
    if sub == "diff":
        return cmd_diff(rest)
    if sub == "rollback":
        return cmd_rollback(rest)
    if sub == "export":
        return cmd_export(rest)
    if sub == "search":
        return cmd_search(rest)
    if sub == "timeline":
        return cmd_timeline(rest)
    if sub == "stats":
        return cmd_stats(rest)
    if sub == "diagnose":
        return cmd_diagnose(rest)
    if sub == "suggest":
        return cmd_suggest(rest)
    if sub == "template":
        return cmd_template(rest)
    if sub == "config":
        return cmd_config(rest)
    if sub in ("protect", "unprotect"):
        return cmd_protect(rest)
    if sub == "archive":
        return cmd_archive(rest)
    if sub == "qr":
        return cmd_qr(rest)
    if sub == "share":
        return cmd_share(rest)
    if sub == "anchor":
        return cmd_anchor(rest)
    print(USAGE)
    return 1


if __name__ == "__main__":
    sys.exit(main())
