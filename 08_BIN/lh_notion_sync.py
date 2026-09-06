#!/usr/bin/env python3
# DNA: #龍芯⚡️2026-09-05-NOTION-SYNC-UNIFIED-v1.3-FILL-KEYWORDS
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 协议: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""📡 龍魂通用 Notion 公开化同步引擎 v1.3(可运维·可观测·可扩展)
================================================================
目标: 将 10 个可公开数据模块批量接入 Notion 公开数据库(可审计·可追溯·可展示)
架构: 复用 lh_health_sync.py 已验证基建(token三级链/直连/幂等/建库) · 模块注册表驱动
v1.2 六维工程升级(2026-09-05·老大指令): 视图层+参数扩展+属性标准化+路由增强+公式字段+CLI子命令
v1.3 关键字主题回填(2026-09-05): _kw_extract 关键字提取(替代 kind 通用标签) + sync --fill
     回填既有行(模块列 diff→PATCH·永不建新行·语义键=来源文件防内容指纹变化误判重复)

模块(10): health✅(独立引擎) · report✅(health_sync覆盖) · shamewall · topo ·
  pipeline · sense · feedback · ledger(安全) · model · deploy · memory(记忆外接大脑)

用法:
  init [--module M|all]            # 建库(幂等·自动带 5 标准属性+4 公式字段)
  sync [--module M|all] [--since YYYY-MM-DD] [--since-file F] [--dry-run] [--quiet]
       [--limit N] [--retry N] [--batch-size N] [--format table|json]
       [--fill]  # 回填既有行(主题/摘要 diff→PATCH·永不建新·语义键=来源文件防重复)
  status [--json]                  # 状态(json 含标准列/引擎版本)
  list                             # 本地数据源清单
  dashboard                        # 终端 Markdown 综合看板
  serve [--port 8780]              # Web 仪表盘 127.0.0.1:8780 (/api/state JSON)
  route list / route test <M>      # 路由注册表(pre/post_hook·filter·transform·on_error)
  diff <M> [--format table|json]   # 本地 vs Notion 差异
  verify <M>                       # 数据哈希一致性(防篡改比对)
  rollback <M> --to <ts> [--yes]   # 归档同步时间>ts 的行(默认清单+备份)
  clean <M> --older-than <days> [--yes]
  经 lh: lh sync <M|all|serve|dashboard|route|diff|verify|rollback|clean|status>
失败即写耻辱墙(sync-failure 事件)。同步状态: ~/.longhun/notion_sync_state.json
"""
import argparse
import contextlib
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

# 复用 lh_health_sync 已验证基建(token/_api/建库/幂等/直连/2022-06-28 header)
import lh_health_sync as hs  # noqa: E402

STATE_P = Path.home() / ".longhun" / "notion_sync_state.json"
CFG_P = Path.home() / ".longhun" / "notion_sync_config.json"


def _h(s):
    return hashlib.sha256(str(s).encode("utf-8")).hexdigest()[:12].upper()


def _dna(mod, rec, tag=""):
    ts = str(rec.get("ts") or rec.get("date") or rec.get("time") or rec.get("created_at") or "")[:10]
    raw = f"NOTION|{mod}|{ts}|{tag}|{json.dumps(rec, ensure_ascii=False, sort_keys=True)}"
    return f"#龍芯⚡️{ts or 'SYNC'}-{mod.upper()}-{_h(raw)}"


# ─────────────────────────── 状态持久化 ───────────────────────────

def _load_state():
    if STATE_P.is_file():
        try:
            return json.loads(STATE_P.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {}


def _save_state(st):
    STATE_P.parent.mkdir(parents=True, exist_ok=True)
    STATE_P.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _load_cfg():
    if CFG_P.is_file():
        try:
            return json.loads(CFG_P.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            pass
    return {"version": "1.0", "parent_page": hs.PARENT_PAGE, "databases": {}}


def _save_cfg(cfg):
    CFG_P.parent.mkdir(parents=True, exist_ok=True)
    CFG_P.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# ─────────────────────────── 耻辱墙告警 ───────────────────────────

def _shame_sync_failure(mod, detail):
    try:
        sw_p = Path.home() / ".longhun" / "shame_wall" / "shame_wall.json"
        if sw_p.is_file():
            sw = json.loads(sw_p.read_text(encoding="utf-8"))
        else:
            sw = {"version": "1.0", "生成时间": datetime.now().isoformat(),
                  "总记录数": 0, "记录": []}
        sw.setdefault("记录", []).append({
            "date": datetime.now().strftime("%Y-%m-%d"), "time": datetime.now().isoformat(),
            "type": "sync_failure", "color": "🔴", "bad": 1, "warn": 0,
            "severity": "error", "reason": f"Notion同步失败[{mod}]: {detail}"})
        sw["生成时间"] = datetime.now().isoformat()
        sw["总记录数"] = len(sw["记录"])
        sw_p.write_text(json.dumps(sw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return True
    except Exception:  # noqa: BLE001
        return False


# ─────────────────────────── 模块注册表 ───────────────────────────
# 每模块: key → {name库名, icon, schema建库, load()→记录list,
#               props(rec)→Notion properties, dedup(rec)→去重key,
#               title(rec)→标题字符串, 提示sourcetip}
# 注: health/report 走 lh_health_sync.py(已独立) · model/deploy/feedback 数据源待采集 → 建库预留

MODULES = {}

# v1.1 (2026-09-06): 预留模块已全部解锁转真实模块注册(老大批准) → 空
PRE_REGISTERED = {}

# ─────────── 优化三/五: 属性标准化 + 公式字段（v1.2 全模块统一） ───────────
# 5 个标准属性: 每条写入 Notion 的记录自动带（跨模块可查询/可审计）
# 4 个公式字段: 由 Notion 侧实时计算(不占本地数据源)
ENGINE_VERSION = 1.0
STD_SCHEMA = {
    "同步时间": {"date": {}},
    "同步版本": {"number": {"format": "number"}},
    "来源系统": {"select": {"options": [
        {"name": "龙魂系统", "color": "green"}, {"name": "其他", "color": "gray"}]}},
    "数据哈希": {"rich_text": {}},
    "同步状态": {"select": {"options": [
        {"name": "成功", "color": "green"}, {"name": "失败", "color": "red"},
        {"name": "待重试", "color": "yellow"}]}},
}
FORMULA_SCHEMA = {
    "记录年龄（天）": {"formula": {"expression":
        'dateBetween(now(), prop("同步时间"), "days")'}},
    "是否久未同步": {"formula": {"expression":
        'if(prop("记录年龄（天）") > 7, "🟡", "🟢")'}},
    "数据来源简写": {"formula": {"expression":
        'replace(prop("来源系统"), "龙魂系统", "LH")'}},
    "同步状态图标": {"formula": {"expression":
        'if(prop("同步状态") == "成功", "✅", "❌")'}},
}


def _extend_schema(schema: dict) -> dict:
    """模块 schema → 追加 5 标准属性 + 4 公式字段(仅缺失列·幂等)"""
    out = dict(schema)
    for k, v in {**STD_SCHEMA, **FORMULA_SCHEMA}.items():
        if k not in out:
            out[k] = v
    return out


def _ensure_std_columns(db_id: str, tok: str, verbose=False) -> bool:
    """幂等补列: 已建老库缺 5 标准属性/4 公式 → PATCH database 补上
    逐列降级: 个别列被 Notion 拒(如公式表达式校验失败)不拖累其余列"""
    try:
        code, body = hs._api("GET", f"/databases/{db_id}", tok=tok)
        if code != 200:
            return False
        have = set((body or {}).get("properties") or {})
        all_cols = {**STD_SCHEMA, **FORMULA_SCHEMA}
        missing = [k for k in all_cols if k not in have]
        if not missing:
            return True
        ok_n = bad_n = 0
        for col in missing:
            code2, b2 = hs._api("PATCH", f"/databases/{db_id}",
                                {"properties": {col: all_cols[col]}}, tok=tok)
            if code2 in (200, 201):
                ok_n += 1
            else:
                bad_n += 1
                if verbose:
                    print(f"    🟡 补列失败 [{col}]: {str(b2)[:120]}")
        return bad_n == 0
    except Exception:  # noqa: BLE001
        return False


def _hash_rec(rec) -> str:
    """数据哈希: 记录规范化内容的 SHA256(防篡改验证·verify 用)"""
    try:
        return "lh1:" + hashlib.sha256(
            json.dumps(rec, ensure_ascii=False, sort_keys=True, default=str)
            .encode("utf-8")).hexdigest()
    except Exception:  # noqa: BLE001
        return "lh1:ERROR"


def _std_props(props: dict, rec) -> dict:
    """写入行自动填充 5 标准属性(无需每个模块手改 props)"""
    props = dict(props or {})
    now = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    props["同步时间"] = {"date": {"start": now}}
    props["同步版本"] = {"number": ENGINE_VERSION}
    props["来源系统"] = hs._sel("龙魂系统")
    props["数据哈希"] = hs._txt(_hash_rec(rec), 1990)
    props["同步状态"] = hs._sel("成功")
    return props


# ─────────── 优化四: 全局路由钩子(模块级 hooks 写在模块 dict 里) ───────────
GLOBAL_HOOKS = {"pre": {}, "post": {}, "on_error": {}}


def _reg(mod):
    def deco(f):
        MODULES[mod] = f()
        return f
    return deco


@_reg("shamewall")
def _m_shamewall():
    src = Path.home() / ".longhun" / "shame_wall" / "shame_wall.json"
    schema = {
        "标题": {"title": {}},
        "事件时间": {"date": {}},
        "事件类型": {"select": {"options": [
            {"name": "topo_change", "color": "green"}, {"name": "topo_changed", "color": "green"},
            {"name": "audit", "color": "yellow"}, {"name": "plagiarism", "color": "red"},
            {"name": "health_alert", "color": "red"}, {"name": "sync_failure", "color": "red"},
            {"name": "其他", "color": "gray"}]}},
        "严重程度": {"select": {"options": [
            {"name": "🔴 error", "color": "red"}, {"name": "🟡 warning", "color": "yellow"},
            {"name": "🟢 info", "color": "green"}, {"name": "其他", "color": "gray"}]}},
        "描述": {"rich_text": {}},
        "DNA追溯码": {"rich_text": {}},
        "责任主体": {"rich_text": {}},
        "已处理": {"checkbox": {}},
    }
    return {"db": "shamewall", "name": "🗂️ 龍魂耻辱墙事件", "icon": "🗂️", "schema": schema,
            "src": src, "sourcetip": "~/.longhun/shame_wall/shame_wall.json",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            "load": lambda: json.loads(src.read_text(encoding="utf-8")).get("记录", []),
            "dedup": lambda r: f"SW|{r.get('time') or r.get('date') or r.get('日期')}|{r.get('type') or r.get('类型')}|{str(r.get('reason') or r.get('详情') or '')[:60]}",
            "title": lambda r: f"{str(r.get('time') or r.get('date') or r.get('日期'))[:19]} · {r.get('type') or r.get('类型')} · {r.get('severity','')}",
            "props": lambda r: {
                "标题": {"title": [{"text": {"content":
                    f"{str(r.get('time') or r.get('date') or r.get('日期'))[:19]} · {r.get('type') or r.get('类型')}"}}]},
                "事件时间": {"date": {"start": str(r.get('time') or r.get('date') or r.get('日期'))[:19].replace(' ', 'T')}},
                "事件类型": hs._sel(str(r.get('type') or '其他')[:40]),
                "严重程度": hs._sel({"error": "🔴 error", "warning": "🟡 warning",
                                      "info": "🟢 info"}.get(str(r.get('severity') or ''), "其他")),
                "描述": hs._txt(str(r.get('reason') or r.get('detail') or ''), 1990),
                "DNA追溯码": hs._txt(""), "责任主体": hs._txt(str(r.get('actor') or '')[:120]),
                "已处理": {"checkbox": bool(r.get('resolved', r.get('severity') not in ('error', 'warning')))},
            }}


@_reg("topo")
def _m_topo():
    src = ROOT / "docs" / "topology" / "对外交付_legion_topo.json"
    schema = {
        "标题": {"title": {}},
        "节点名称": {"rich_text": {}},
        "所属分组": {"select": {"options": []}},
        "类型": {"select": {"options": [
            {"name": "document", "color": "blue"}, {"name": "article", "color": "purple"},
            {"name": "report", "color": "yellow"}, {"name": "asset", "color": "green"},
            {"name": "endpoint", "color": "orange"}, {"name": "其他", "color": "gray"}]}},
        "状态": {"select": {"options": [
            {"name": "🟢 可用", "color": "green"}, {"name": "🟡 待关注", "color": "yellow"},
            {"name": "🔴 不可用", "color": "red"}, {"name": "其他", "color": "gray"}]}},
        "DNA追溯码": {"rich_text": {}},
        "描述": {"rich_text": {}},
        "注册时间": {"date": {}},
    }
    def load():
        t = json.loads(src.read_text(encoding="utf-8"))
        out = []
        for g in t.get("groups", []):
            for a in g.get("assets", []):
                row = dict(a)
                row["_group"] = g.get("name", "")
                out.append(row)
        return out
    return {"db": "topo", "name": "🗺️ 龍魂知识图谱节点", "icon": "🗺️", "schema": schema,
            "src": src, "sourcetip": "docs/topology/对外交付_legion_topo.json",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            "load": load,
            "dedup": lambda r: r.get("dna", "") or f"TOPO|{r.get('name')}",
            # 一 DNA 可能对应多资产(如 C入口/D发布共享文档站DNA) → 组合 DNA+分组+名称 唯一化
            "dna_key": lambda r: f"{r.get('dna','') or 'TOPO'}|{r.get('_group','')}|{r.get('name','')}",
            "title": lambda r: f"{r.get('_group','')}/{r.get('name','')}",
            "props": lambda r: {
                "标题": {"title": [{"text": {"content": str(r.get("name", ""))[:200]}}]},
                "节点名称": hs._txt(r.get("name", "")),
                "所属分组": hs._sel(r.get("_group", "未分组")[:40]),
                "类型": hs._sel(str(r.get("type") or "其他")[:40]),
                "状态": hs._sel(str(r.get("status") or "🟡 待关注")[:30]),
                "DNA追溯码": hs._txt(r.get("dna", "")),
                "描述": hs._txt(r.get("desc", "")[:1990]),
                "注册时间": {"date": {"start": str(r.get("registered_at") or "")[:19].replace(' ', 'T')}},
            }}


@_reg("pipeline")
def _m_pipeline():
    src = Path.home() / ".longhun" / "pipeline" / "records.jsonl"
    schema = {
        "标题": {"title": {}},
        "执行时间": {"date": {}},
        "意图": {"rich_text": {}},
        "领域": {"select": {"options": []}},
        "人格": {"select": {"options": []}},
        "黑白双审": {"select": {"options": [
            {"name": "是", "color": "green"}, {"name": "否", "color": "gray"}]}},
        "三色终裁": {"select": {"options": [
            {"name": "🟢", "color": "green"}, {"name": "🟡", "color": "yellow"},
            {"name": "🔴", "color": "red"}]}},
        "数字根": {"number": {}},
        "DNA追溯码": {"rich_text": {}},
    }
    def load():
        out = []
        if src.is_file():
            for line in src.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    with contextlib.suppress(Exception):
                        out.append(json.loads(line))
        return out
    return {"db": "pipeline", "name": "⚙️ 龍魂执行日志", "icon": "⚙️", "schema": schema,
            "src": src, "sourcetip": "~/.longhun/pipeline/records.jsonl",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            "load": load,
            "dedup": lambda r: f"PL|{r.get('ts')}|{str(r.get('input'))[:80]}",
            "title": lambda r: f"{str(r.get('ts'))[:16]} · {str(r.get('input'))[:40]}",
            "props": lambda r: {
                "标题": {"title": [{"text": {"content":
                    f"{str(r.get('ts'))[:16]} · {str(r.get('input'))[:40]}"}}]},
                "执行时间": {"date": {"start": str(r.get("ts"))[:19].replace(' ', 'T')}},
                "意图": hs._txt(str(r.get("input") or "")[:1990]),
                "领域": hs._sel(str(r.get("domain") or "其他")[:40]),
                "人格": hs._sel(str(r.get("persona") or "P04")[:60]),
                "黑白双审": hs._sel("是" if r.get("duel") else "否"),
                "三色终裁": hs._sel(str(r.get("color") or "🟡")[:3]),
                "数字根": {"number": int(r.get("dr") or 0)},
                "DNA追溯码": hs._txt(""),
            }}


@_reg("sense")
def _m_sense():
    src = Path.home() / ".longhun" / "sense_memory" / "sense_memory.jsonl"
    schema = {
        "标题": {"title": {}},
        "感知时间": {"date": {}},
        "类型": {"select": {"options": [
            {"name": "image", "color": "blue"}, {"name": "audio", "color": "purple"},
            {"name": "video", "color": "green"}, {"name": "text", "color": "yellow"},
            {"name": "其他", "color": "gray"}]}},
        "识别结果": {"rich_text": {}},
        "置信度": {"number": {}},
        "审计结果": {"select": {"options": [
            {"name": "🟢", "color": "green"}, {"name": "🟡", "color": "yellow"},
            {"name": "🔴", "color": "red"}]}},
        "DNA追溯码": {"rich_text": {}},
    }
    def load():
        out = []
        if src.is_file():
            for line in src.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    with contextlib.suppress(Exception):
                        out.append(json.loads(line))
        return out
    return {"db": "sense", "name": "👁️ 龍魂感知记录", "icon": "👁️", "schema": schema,
            "src": src, "sourcetip": "~/.longhun/sense_memory/sense_memory.jsonl",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            "load": load,
            "dedup": lambda r: r.get("dna", "") or f"SENSE|{r.get('ts')}",
            "title": lambda r: f"{str(r.get('ts'))[:16]} · {r.get('type')} · conf {r.get('confidence','')}",
            "props": lambda r: {
                "标题": {"title": [{"text": {"content":
                    f"{str(r.get('ts'))[:16]} · {r.get('type')} · {r.get('confidence','')}"}}]},
                "感知时间": {"date": {"start": str(r.get("ts"))[:19].replace(' ', 'T')}},
                "类型": hs._sel(str(r.get("type") or "其他")[:40]),
                "识别结果": hs._txt(str(r.get("text") or "")[:1990]),
                "置信度": {"number": float(r.get("confidence") or 0)},
                "审计结果": hs._sel(str(r.get("audit") or r.get("color") or "🟡")[:3]),
                "DNA追溯码": hs._txt(r.get("dna", "")),
            }}


@_reg("ledger")
def _m_ledger():
    """🧾 龙魂公开账本 — 老大已确认白名单字段(2026-09-06)
    公开: 日期/类型/科目/金额(模糊)/状态/审计色/DNA · 隐藏: note原文/witness/extra/hash"""
    src = Path.home() / ".longhun" / "ledger" / "transactions.jsonl"
    schema = {
        "标题": {"title": {}},
        "交易日期": {"date": {}},
        "交易类型": {"select": {"options": [
            {"name": "T1", "color": "green"}, {"name": "T2", "color": "green"},
            {"name": "T3", "color": "blue"}, {"name": "T9", "color": "purple"},
            {"name": "其他", "color": "gray"}]}},
        "借方科目": {"rich_text": {}},
        "贷方科目": {"rich_text": {}},
        "金额": {"rich_text": {}},
        "状态": {"select": {"options": [
            {"name": "🟢 GREEN", "color": "green"}, {"name": "🟡 YELLOW", "color": "yellow"},
            {"name": "🔴 RED", "color": "red"}]}},
        "审计结果": {"select": {"options": [
            {"name": "🟢", "color": "green"}, {"name": "🟡", "color": "yellow"},
            {"name": "🔴", "color": "red"}]}},
        "DNA追溯码": {"rich_text": {}},
    }
    def load():
        out = []
        if src.is_file():
            for line in src.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    try:
                        r = json.loads(line)
                        # 仅公开状态正常的交易(非敏感note可带·金额已是模糊文本)
                        out.append(r)
                    except Exception:  # noqa: BLE001
                        pass
        return out
    return {"db": "ledger", "name": "🧾 龍魂公开账本", "icon": "🧾", "schema": schema,
            "src": src, "sourcetip": "~/.longhun/ledger/transactions.jsonl(公开字段白名单)",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            "load": load,
            "dedup": lambda r: r.get("dna", "") or f"LEDGER|{r.get('date')}|{r.get('seq')}",
            "dna_key": lambda r: r.get("dna", "") or f"LEDGER|{r.get('date')}|{r.get('seq')}",
            "title": lambda r: f"{r.get('date')} · {r.get('tx_type')} · {r.get('dr_code')}→{r.get('cr_code')}",
            "props": lambda r: {
                "标题": {"title": [{"text": {"content":
                    f"{r.get('date')} · {r.get('tx_type')} · {r.get('dr_code')}→{r.get('cr_code')}"}}]},
                "交易日期": {"date": {"start": str(r.get("date"))[:10]}},
                "交易类型": hs._sel(str(r.get("tx_type") or "其他")[:40]),
                "借方科目": hs._txt(str(r.get("dr_code") or "")[:40]),
                "贷方科目": hs._txt(str(r.get("cr_code") or "")[:40]),
                "金额": hs._txt(str(r.get("amount") or "")[:60]),
                "状态": hs._sel(str(r.get("status") or "🟡 YELLOW")[:30]),
                "审计结果": hs._sel(str(r.get("extra", {}).get("audit_color") or "🟡")[:3]),
                "DNA追溯码": hs._txt(""),
            }}


@_reg("model")
def _m_model():
    """🤖 龙魂模型基线 — 数据源由 lh_notion_collect.py 采集(ollama list + 服务状态)"""
    src_dir = Path.home() / ".longhun" / "model_state"
    schema = {
        "标题": {"title": {}},
        "采集日期": {"date": {}},
        "模型名称": {"rich_text": {}},
        "模型ID": {"rich_text": {}},
        "大小": {"rich_text": {}},
        "修改时间": {"rich_text": {}},
        "服务": {"rich_text": {}},
        "DNA追溯码": {"rich_text": {}},
    }
    def latest_file():
        fs = sorted(src_dir.glob("*.json")) if src_dir.is_dir() else []
        return fs[-1] if fs else None
    def load():
        f = latest_file()
        if not f:
            return []
        data = json.loads(f.read_text(encoding="utf-8"))
        models = data.get("models", [])
        for m in models:
            m["_date"] = f.stem
            m["_service"] = str(data.get("service", {}).get("runner", ""))[:80]
        return models
    return {"db": "model", "name": "🤖 龍魂模型基线", "icon": "🤖", "schema": schema,
            "src": src_dir, "sourcetip": "~/.longhun/model_state/*.json(采集器lh_notion_collect.py)",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            "load": load,
            "dedup": lambda r: f"MODEL|{r.get('name')}|{r.get('_date')}",
            "title": lambda r: f"{r.get('name','')} · {r.get('_date','')}",
            "props": lambda r: {
                "标题": {"title": [{"text": {"content": f"{r.get('name','')}"}}]},
                "采集日期": {"date": {"start": str(r.get("_date", ""))[:10]}},
                "模型名称": hs._txt(r.get("name", "")),
                "模型ID": hs._txt(r.get("id", "")),
                "大小": hs._txt(str(r.get("size", ""))[:40]),
                "修改时间": hs._txt(str(r.get("modified", ""))[:40]),
                "服务": hs._txt(str(r.get("_service", ""))[:80]),
                "DNA追溯码": hs._txt(""),
            }}


@_reg("deploy")
def _m_deploy():
    """🛰️ 龙魂运维状态 — 采集器拉取 Mac launchd + 鲲鹏 systemd"""
    src_dir = Path.home() / ".longhun" / "deploy_status"
    schema = {
        "标题": {"title": {}},
        "采集日期": {"date": {}},
        "主机": {"select": {"options": [
            {"name": "Mac", "color": "blue"}, {"name": "Kunpeng", "color": "orange"},
            {"name": "其他", "color": "gray"}]}},
        "服务名": {"rich_text": {}},
        "状态": {"rich_text": {}},
        "PID": {"rich_text": {}},
        "DNA追溯码": {"rich_text": {}},
    }
    def latest_file():
        fs = sorted(src_dir.glob("*.json")) if src_dir.is_dir() else []
        return fs[-1] if fs else None
    def load():
        f = latest_file()
        if not f:
            return []
        data = json.loads(f.read_text(encoding="utf-8"))
        svcs = data.get("services", [])
        for s in svcs:
            s["_date"] = f.stem
        return svcs
    return {"db": "deploy", "name": "🛰️ 龍魂运维状态", "icon": "🛰️", "schema": schema,
            "src": src_dir, "sourcetip": "~/.longhun/deploy_status/*.json(Mac launchd+鲲鹏 systemd)",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            "load": load,
            "dedup": lambda r: f"DEPLOY|{r.get('host')}|{r.get('label') or r.get('service')}|{r.get('_date')}",
            "title": lambda r: f"{r.get('host','')}/{r.get('label') or r.get('service','')}",
            "props": lambda r: {
                "标题": {"title": [{"text": {"content":
                    f"{r.get('host','')}/{r.get('label') or r.get('service','')}"}}]},
                "采集日期": {"date": {"start": str(r.get("_date", ""))[:10]}},
                "主机": hs._sel(str(r.get("host") or "其他")[:30]),
                "服务名": hs._txt(str(r.get("label") or r.get("service") or "")[:120]),
                "状态": hs._txt(str(r.get("status") or "")[:40]),
                "PID": hs._txt(str(r.get("pid") or "")[:40]),
                "DNA追溯码": hs._txt(""),
            }}


@_reg("feedback")
def _m_feedback():
    """🗣️ 龙魂社区反馈 — feedback_*.jsonl(社区反馈/虚伪检测记录·滚动累积)"""
    src_dir = Path.home() / ".longhun" / "feedback"
    schema = {
        "标题": {"title": {}},
        "反馈时间": {"date": {}},
        "来源": {"select": {"options": [
            {"name": "社区", "color": "blue"}, {"name": "虚伪检测", "color": "red"},
            {"name": "审计", "color": "yellow"}, {"name": "其他", "color": "gray"}]}},
        "人格/模块": {"rich_text": {}},
        "反馈内容": {"rich_text": {}},
        "结果": {"rich_text": {}},
        "虚伪度": {"number": {}},
        "状态": {"select": {"options": [
            {"name": "🔴 熔断", "color": "red"}, {"name": "🟡 待标注", "color": "yellow"},
            {"name": "🟢 通过", "color": "green"}, {"name": "其他", "color": "gray"}]}},
        "DNA追溯码": {"rich_text": {}},
    }
    def load():
        out = []
        if src_dir.is_dir():
            for f in sorted(src_dir.glob("feedback_*.jsonl")):
                for line in f.read_text(encoding="utf-8").splitlines():
                    if line.strip():
                        try:
                            r = json.loads(line)
                            r["_date"] = (r.get("时间") or "")[:10]
                            out.append(r)
                        except Exception:  # noqa: BLE001
                            pass
        return out
    return {"db": "feedback", "name": "🗣️ 龍魂社区反馈", "icon": "🗣️", "schema": schema,
            "src": src_dir, "sourcetip": "~/.longhun/feedback/feedback_*.jsonl",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            "load": load,
            "dedup": lambda r: f"FB|{(r.get('时间') or '')[:19]}|{str(r.get('人格') or '')[:30]}",
            "title": lambda r: f"{(r.get('时间') or '')[:16]} · {r.get('人格') or '匿名'}",
            "props": lambda r: {
                "标题": {"title": [{"text": {"content":
                    f"{(r.get('时间') or '')[:16]} · {r.get('人格') or '匿名'}"}}]},
                "反馈时间": {"date": {"start": str(r.get("时间") or "")[:19].replace(' ', 'T')}},
                "来源": hs._sel("虚伪检测" if "虚伪" in str(r.get("格式", {}).get("输出", ""))
                                or r.get("虚伪度") is not None else "其他"),
                "人格/模块": hs._txt(str(r.get("人格") or "")[:60]),
                "反馈内容": hs._txt(str(r.get("原始文本") or "")[:1980]),
                "结果": hs._txt(str(r.get("检测结果") or "")[:1980]),
                "虚伪度": {"number": int(r.get("虚伪度") or 0)},
                "状态": hs._sel(str(r.get("状态") or "其他")[:30]),
                "DNA追溯码": hs._txt(""),
            }}


# ─────────────────────────── 蒸馏辅助 ───────────────────────────

def _md_strip(text, maxlen=1990):
    """markdown → 去模板头/代码块/页脚后的纯文本(截断 maxlen)"""
    s = str(text or "")
    # 去掉头部 > 引用块(模板 DNA 头/声明)只留一行 DNA 信息
    lines = s.splitlines()
    body, in_code = [], False
    for ln in lines:
        st = ln.strip()
        if st.startswith("```"):
            in_code = not in_code
            continue
        if in_code or st.startswith("```"):
            continue
        body.append(ln)
    s = "\n".join(body)
    # 去页脚常见模板
    for mark in ("确认码:", "GPG:", "三色:", "License:", "协议:", "v63 · 2026-09-04",
                 "> v63"):
        s = s.split(mark)[0]
    s = s.replace("**", "").replace("##", "#").replace("###", "#")
    s = re.sub(r"[#>*|]", "", s)
    s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"\n{3,}", "\n\n", s).strip()
    return s[:maxlen]


def _md_topics(text, maxn=6):
    """提取 markdown 中 ## 小节标题(至多 maxn 个·用于主题列·滤纯标签小节)"""
    out, seen = [], set()
    for ln in str(text or "").splitlines():
        m = re.match(r"^#{1,3}\s+(.+)$", ln.strip())
        if m:
            t = m.group(1).strip().replace("**", "")
            parts = [p.strip() for p in re.split(r"[·|,，、]", t) if p.strip()]
            keep = [p for p in parts if p.casefold() not in _KW_STOP]
            if not keep:
                continue  # 纯模板小节(基本信息/决策理由…)整节丢弃
            t2 = " · ".join(keep)
            if t2 and t2 not in seen:
                seen.add(t2)
                out.append(t2)
        if len(out) >= maxn:
            break
    return " · ".join(out)


# ─────────── 关键字提取(记忆主题填充·老大 2026-09-05 指令) ───────────
_KW_STOP = {
    "工作日志", "年轮事件", "速记", "复盘", "基本信息", "决策理由", "决策详情",
    "待办事项", "说明", "评分", "公式引用", "测试结果", "完成的工程", "新增文件",
    "关键发现", "流水线", "扩展内容", "集成内容", "归属名", "结论", "描述",
    "the", "and", "for", "with", "from", "that", "this",
    "code", "note", "data", "file", "text", "time", "list", "done", "task",
    "action", "result", "info", "date", "root",
}
_KW_TITLE_DATE = re.compile(r"^\d{4}[-_]?\d{2}[-_]?\d{2}$")


def _kw_extract(text, maxn=6):
    """从 markdown/正文提取可检索关键字: 标题行·加粗短语·英文技术词
    (记忆主题列用·替代"工作日志"式通用标签·纯 stdlib 无三方分词)"""
    txt = str(text or "")
    if not txt.strip():
        return ""
    cands, seen = [], set()

    def push(s):
        s = str(s).strip().strip("·|,，。:：-–— ")
        s = re.sub(r"^[#>*`\d.\s]+", "", s)
        s = re.sub(r"[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F]", "", s)
        s = re.sub(r"[（(][^）)]*[)）]", "", s).strip()
        s = re.sub(r"\s+", " ", s)
        if not s or len(s) < 2:
            return
        k = s.casefold()
        if k in seen:
            return
        if k in _KW_STOP or s.lower() in _KW_STOP:
            return
        if _KW_TITLE_DATE.fullmatch(s):
            return
        seen.add(k)
        cands.append(s[:24])

    # ① 标题行(##/#·去 emoji/编号/括号说明)
    for ln in txt.splitlines():
        m = re.match(r"^#+\s+(.+)$", ln.strip())
        if m:
            push(m.group(1))
        if len(cands) >= maxn:
            break
    # ② 加粗短语 **xxx**
    for m in re.findall(r"\*\*([^*\n|]{2,20})\*\*", txt):
        push(m)
        if len(cands) >= maxn:
            break
    # ③ 英文技术词/编号(停用过滤)
    if len(cands) < maxn:
        for w in re.findall(r"[A-Za-z][A-Za-z0-9._/#+-]{1,19}", txt):
            if w.casefold() not in _KW_STOP and not w.isdigit():
                push(w)
            if len(cands) >= maxn:
                break
    return " · ".join(cands[:maxn])


def _mem_topics(ents, maxn=6):
    """每日记忆主题合成: 逐 entry(标题有语义优先·正文关键字补充)"""
    out, seen = [], set()

    def push(s):
        s = str(s).strip()
        k = s.casefold()
        if s and len(s) >= 2 and k not in seen:
            seen.add(k)
            out.append(s[:26])

    for e in ents[:10]:
        if len(out) >= maxn:
            break
        t = str(e.get("title") or "")
        x = str(e.get("text") or "")
        if t and not _KW_TITLE_DATE.fullmatch(t):
            push(t)
        for kw in _kw_extract(x, 3).split(" · "):
            push(kw)
        if len(out) >= maxn:
            break
    return " · ".join(out[:maxn])


def _date_of(name, text=""):
    """从文件名或正文提取 YYYY-MM-DD(决策/复盘 ID 形 20260606203509 → 2026-06-06)"""
    s = str(name) + " " + str(text)
    m = re.search(r"(\d{4})[-_]?(\d{2})[-_]?(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    return datetime.now().strftime("%Y-%m-%d")


@_reg("memory")
def _m_memory():
    """🧠 龍魂记忆外接大脑 — 老大承诺: Notion=龍魂+未来所有人的记忆外接大脑
    三源蒸馏入库(每源独立_蒸馏+过滤规则·见下):
    ① calmem 日历记忆(每日聚合: 五源含执行复盘·一天一条·只取 entries 前 8 条各截 300 字)
    ② 决策日志 DECISION-*.md(全量 _md_strip 截 1500 字·只取首个有效小节标题作主题)
    ③ 执行复盘(recap) — 不单列: 已含于 calmem 五源聚合(避免重复噪音·sourcetip 注明)
    蒸馏边界: _md_strip=去模板头/代码块/页脚纯文本(截断 maxlen·≤1990 Notion 富文本上限);
              _md_topics=仅提取 ## 小节标题(滤纯模板节·至多 maxn 个)
    数据主权: 只推脱敏摘要/标题/日期/DNA → 原文仍在本地(可追溯·敏感不上云)"""
    calmem_dir = Path.home() / ".longhun" / "calendar_memory" / "days"
    decide_dir = ROOT / "04_決策日誌"
    schema = {
        "标题": {"title": {}},
        "记忆日期": {"date": {}},
        "记忆类型": {"select": {"options": [
            {"name": "每日记忆", "color": "blue"}, {"name": "决策日志", "color": "purple"},
            {"name": "执行复盘", "color": "green"}, {"name": "其他", "color": "gray"}]}},
        "主题": {"rich_text": {}},
        "摘要": {"rich_text": {}},
        "来源文件": {"rich_text": {}},
        "DNA追溯码": {"rich_text": {}},
    }
    def load():
        out = []
        # ① calmem 每日聚合(一天一条: 各源 title 合并)
        if calmem_dir.is_dir():
            for f in sorted(calmem_dir.glob("*.json")):
                try:
                    d = json.loads(f.read_text(encoding="utf-8"))
                except Exception:  # noqa: BLE001
                    continue
                date = d.get("date") or f.stem
                ents = d.get("entries", [])
                title = f"📅 {date} · {len(ents)} 条记忆"
                tops = _mem_topics(ents, 6)  # 关键字主题(替代 kind 通用标签)
                summ = "\n".join([_md_strip(str(e.get('title') or '') + " " +
                                            str(e.get('text') or ''), 300)
                                  for e in ents[:8]])
                out.append({
                    "_date": date, "_kind": "每日记忆", "_key": "calmem",
                    "title": title, "topics": tops, "summary": summ,
                    "src": str(f).replace(str(Path.home()), "~"),
                    "_dna": f"MEM|{date}|calmem|{d.get('root_hash','')[:8]}"})
        # ② 决策日志 DECISION-*.md
        if decide_dir.is_dir():
            for f in sorted(decide_dir.glob("DECISION-*.md")):
                txt = f.read_text(encoding="utf-8")
                date = _date_of(f.name, txt)
                topic = _md_topics(txt, 1)  # 只取首个有效小节标题(滤模板节)
                title = f"📜 {date} · {f.stem[:40]}"
                out.append({"_date": date, "_kind": "决策日志", "_key": "decision",
                            "title": title, "topics": topic,
                            "summary": _md_strip(txt, 1500),
                            "src": str(f).replace(str(ROOT), ""),
                            "_dna": f"MEM|{date}|decision|{f.stem[:36]}"})
        out.sort(key=lambda r: r["_date"], reverse=True)
        return out
    return {"db": "memory", "name": "🧠 龍魂记忆外接大脑", "icon": "🧠", "schema": schema,
            "src": f"{calmem_dir} / {decide_dir}",
            "sourcetip": "~/.longhun/calendar_memory/days + 04_決策日誌",
            "title_col": "标题", "dedup_col": "DNA追溯码",
            # 语义键: 同来源文件视为同一行(内容升级走 fill 更新·不重复建行)
            "fill_key_col": "来源文件", "fill_key_src": "src",
            "load": load,
            "dedup": lambda r: r["_dna"],
            "title": lambda r: r["title"][:60],
            "props": lambda r: {
                "标题": {"title": [{"text": {"content": r["title"][:200]}}]},
                "记忆日期": {"date": {"start": r["_date"]}},
                "记忆类型": hs._sel(r["_kind"]),
                "主题": hs._txt(r.get("topics", "")[:500]),
                "摘要": hs._txt(r.get("summary", "")[:1990]),
                "来源文件": hs._txt(r.get("src", "")[:500]),
                "DNA追溯码": hs._txt(""),
            }}


# ─────────────────────────── init 建库 ───────────────────────────

def cmd_init(module=None, quiet=False):
    tok = hs.get_token()
    if not tok:
        print("🔴 NOTION_TOKEN 不可用(env/vault/mcp.json 均失败)")
        return 1
    cfg = _load_cfg()
    dbs = cfg.setdefault("databases", {})
    if not quiet:
        print("📡 初始化龍魂 Notion 公开数据库…")
    mods = list(MODULES) if module in (None, "all", "") else [module]
    if module in PRE_REGISTERED:
        print(f"  🟡 {module}: {PRE_REGISTERED[module][2]}")
        return 0
    errs = 0
    for key in mods:
        m = MODULES.get(key)
        if not m:
            print(f"  ❌ 未知模块: {key}")
            errs += 1
            continue
        if dbs.get(m["db"]):
            code, _ = hs._api("GET", f"/databases/{dbs[m['db']]}", tok=tok)
            if code == 200:
                # 优化三/五: 老库幂等补标准属性+公式字段
                ok = _ensure_std_columns(dbs[m["db"]], tok)
                if not quiet:
                    extra = " · 已补标准列✅" if ok else " · 🔴 补列失败"
                    print(f"  ⏭️  已存在 {m['db']}: {dbs[m['db']]}{extra}")
                continue
        payload = {"parent": {"type": "page_id", "page_id": hs.PARENT_PAGE},
                   "icon": {"type": "emoji", "emoji": m["icon"]},
                   "title": [{"type": "text", "text": {"content": m["name"]}}],
                   "properties": _extend_schema(m["schema"])}
        code, body = hs._api("POST", "/databases", payload, tok=tok)
        if code in (200, 201):
            db_id = body.get("id", "")
            dbs[m["db"]] = db_id
            if not quiet:
                print(f"  ✅ {m['name']}: {db_id}")
        else:
            errs += 1
            print(f"  🔴 {m['db']} 建库失败: HTTP {code} "
                  f"{json.dumps(body, ensure_ascii=False)[:160]}")
    _save_cfg(cfg)
    if not quiet:
        print("  📝 配置: ~/.longhun/notion_sync_config.json")
        print("  ✅ init 完成 · 用 status 查看库链接 · ledger 需老大确认后解锁")
    return 1 if errs else 0


# ─────────────────────────── sync 推送 ───────────────────────────

def _fmt_date(v):
    s = str(v or "")[:19].replace("Z", "")
    return s


def cmd_sync(module=None, since="", dry_run=False, quiet=False, limit=0,
             retry=3, batch_size=50, fmt="table", since_file="", fill=False):
    tok = hs.get_token()
    if not tok:
        print("🔴 NOTION_TOKEN 不可用")
        return 1
    if since_file:
        try:
            p = Path(since_file)
            if p.is_file():
                since = p.read_text(encoding="utf-8").strip().splitlines()[0].strip()[:10]
        except Exception:  # noqa: BLE001
            print(f"  🟡 since-file 读取失败: {since_file}")
    cfg = _load_cfg()
    dbs = cfg.get("databases", {})
    if module in PRE_REGISTERED:
        print(f"  🟡 {module} 未解锁: {PRE_REGISTERED[module][2]}")
        return 2
    mods = list(MODULES) if module in (None, "all", "") else [module]
    st = _load_state()
    total_pushed = total_skip = total_failed = total_updated = 0
    json_report = {"cmd": "sync", "time": datetime.now().astimezone().isoformat(),
                   "dry_run": dry_run, "fill": fill, "modules": {}}
    for key in mods:
        m = MODULES.get(key)
        if not m:
            print(f"  ❌ 未知模块: {key}")
            continue
        db_id = dbs.get(m["db"])
        if not db_id:
            print(f"  🟡 [{key}] 库未初始化 · 先跑 init --module {key}")
            continue
        # 优化三: 老库幂等补标准列(失败则该模块跳过·写行会 400)
        if not dry_run and not _ensure_std_columns(db_id, tok):
            msg = "标准属性/公式字段补列失败(检查 token 权限)"
            print(f"  🔴 [{key}] {msg}")
            _shame_sync_failure(key, msg)
            continue
        records = []
        try:
            records = m["load"]()
        except Exception as e:  # noqa: BLE001
            print(f"  🔴 [{key}] 数据源读取失败: {e} ({m.get('sourcetip')})")
            _shame_sync_failure(key, f"数据源读取失败: {e}")
            continue
        if since:
            records = [r for r in records if str(r.get("ts") or r.get("date")
                                                 or r.get("time") or "")[:10] >= since]
        # 优化四: filter 路由(按条件过滤)
        if m.get("filter"):
            try:
                records = [r for r in records if m["filter"](r)]
            except Exception as e:  # noqa: BLE001
                print(f"  🟡 [{key}] filter 执行异常: {e}")
        if limit:
            records = records[:limit]
        # 回填通道: --fill 时拉全库已存在行(dna→page·fill_key_col→page)做字段 diff
        exist_map = sem_map = None
        if fill and not dry_run:
            exist_map, sem_map = {}, {}
            fkc = m.get("fill_key_col")
            for pg in _query_pages(db_id, tok, cap=3000):
                rowp = pg["props"]
                dval = str(rowp.get("DNA追溯码") or "").strip()
                if dval:
                    exist_map.setdefault(dval, (pg["id"], rowp))
                if fkc:
                    sv = str(rowp.get(fkc) or "").strip()[:80]
                    if sv:
                        sem_map.setdefault(sv, (pg["id"], rowp))
        pushed = skipped = failed = updated = 0
        # 优化四: pre_hook(同步前·模块级优先·全局兜底)
        try:
            pre = m.get("pre_hook") or GLOBAL_HOOKS["pre"].get(key)
            if pre:
                pre({"key": key, "records": records, "db_id": db_id,
                     "tok": tok, "dry_run": dry_run})
        except Exception as e:  # noqa: BLE001
            print(f"  🟡 [{key}] pre_hook 异常: {e}")
        src_total = len(records)
        for idx, rec in enumerate(records, 1):
            try:
                # 优化四: transform(推送前动态改写)
                if m.get("transform"):
                    rec = m["transform"](rec) or rec
                if m.get("dna_key"):
                    dna = m["dna_key"](rec)
                else:
                    dna = rec.get("dna", "") or _dna(key, rec, m["dedup"](rec))
                if not dna:
                    dna = _dna(key, rec, m["dedup"](rec))
                if fill:
                    # --fill 回填: 只更新既有行(按 dna 或语义键) · 永不建新行 · 防内容指纹变化误判重复
                    hit = None
                    if exist_map is not None:
                        if dna in exist_map:
                            hit = exist_map[dna]
                        elif sem_map:
                            sk = str(rec.get(m.get("fill_key_src") or "") or "")[:80]
                            if sk and sk in sem_map:
                                hit = sem_map[sk]
                    if not hit:  # dry-run 或库中无此行 → 保守跳过(回填不做新增)
                        skipped += 1
                        continue
                    pid, rowp = hit
                    props = m["props"](rec)
                    if "DNA追溯码" in props:
                        props["DNA追溯码"] = hs._txt(dna)
                    props = _std_props(props, rec)
                    ups = _prop_diffs(rowp, props)
                    cur_dna = str(rowp.get("DNA追溯码") or "").strip()
                    if cur_dna and cur_dna != dna:
                        ups["DNA追溯码"] = hs._txt(dna)  # 主键对齐(内容指纹演进)
                    if ups:
                        ups["同步时间"] = props["同步时间"]
                        ups["数据哈希"] = props["数据哈希"]
                        c, _ = hs._api("PATCH", f"/pages/{pid}",
                                       {"properties": ups}, tok=tok)
                        if c in (200, 201):
                            updated += 1
                        else:
                            failed += 1
                            if not quiet:
                                print(f"  🟡 [{key}] 回填失败 {m['title'](rec)[:40]}")
                    else:
                        skipped += 1
                    continue
                if hs._query_exists(db_id, "DNA追溯码", dna, tok):
                    skipped += 1
                    continue
                props = m["props"](rec)
                if "DNA追溯码" in props:
                    props["DNA追溯码"] = hs._txt(dna)
                # 优化三: 自动填充 5 标准属性
                props = _std_props(props, rec)
                if dry_run:
                    if quiet:
                        pass
                    elif idx <= batch_size:
                        print(f"  [dry-run] [{key}] 将推送: {m['title'](rec)[:60]}")
                    pushed += 1
                    continue
                pid, err = "", ""
                for attempt in range(max(1, int(retry))):
                    pid, err = hs._create_row(db_id, props, tok=tok)
                    if pid:
                        break
                    time.sleep(0.4 * (attempt + 1))
                if pid:
                    pushed += 1
                    st.setdefault(key, {})
                    seen = st[key].setdefault("synced_keys", [])
                    if dna not in seen:
                        seen.append(dna)
                    if batch_size and idx % batch_size == 0 and not quiet:
                        print(f"    …{key} 已推 {pushed}/{src_total}")
                else:
                    failed += 1
                    msg = f"推送失败: {err}"
                    print(f"  🟡 [{key}] {msg}")
                    on_err = m.get("on_error") or GLOBAL_HOOKS["on_error"].get(key)
                    if on_err:
                        with contextlib.suppress(Exception):
                            on_err(rec, err)
            except Exception as e:  # noqa: BLE001
                failed += 1
                print(f"  🟡 [{key}] 记录处理失败: {e}")
        # 优化四: post_hook(同步后)
        try:
            post = m.get("post_hook") or GLOBAL_HOOKS["post"].get(key)
            if post:
                post({"key": key, "pushed": pushed, "skipped": skipped,
                      "failed": failed, "dry_run": dry_run})
        except Exception as e:  # noqa: BLE001
            print(f"  🟡 [{key}] post_hook 异常: {e}")
        tag = "dry-run" if dry_run else "实际推送"
        if not quiet or pushed or failed or updated:
            print(f"  {key}: 新增 {pushed} · 已同步 {skipped} · "
                  f"{'回填 ' + str(updated) + ' · ' if updated else ''}"
                  f"失败 {failed} · 源 {src_total} 条 ({tag})")
        if not dry_run:
            cell = st.setdefault(key, {})
            cell["last_sync"] = datetime.now().astimezone().isoformat()
            cell.setdefault("errors", 0)
            cell["errors"] = int(cell.get("errors", 0)) + failed
            cell["stats"] = {"source": src_total, "pushed": pushed,
                             "skipped": skipped, "updated": updated,
                             "failed": failed}
        json_report["modules"][key] = {"db": m["db"], "source": src_total,
                                       "pushed": pushed, "skipped": skipped,
                                       "updated": updated, "failed": failed}
        total_pushed += pushed
        total_skip += skipped
        total_updated += updated
        total_failed += failed
    if not dry_run:
        _save_state(st)
    if fmt == "json":
        json_report["summary"] = {"pushed": total_pushed, "skipped": total_skip,
                                  "updated": total_updated,
                                  "failed": total_failed}
        print(json.dumps(json_report, ensure_ascii=False, indent=2))
        return 0 if not total_failed else 3
    return 0 if not total_failed else 3


# ─────────────────────────── status / list ───────────────────────────

def cmd_status(json_out=False):
    cfg = _load_cfg()
    st = _load_state()
    dbs = cfg.get("databases", {})
    out = {"config": str(CFG_P), "state": str(STATE_P), "modules": {}}
    for key in list(MODULES) + list(PRE_REGISTERED):
        db_id = dbs.get(key, "")
        meta = {"id": db_id,
                "url": f"https://www.notion.so/{db_id.replace('-', '')}" if db_id else ""}
        if key in PRE_REGISTERED:
            meta["status"] = "🟡 未解锁"
            meta["note"] = PRE_REGISTERED[key][2]
        else:
            meta["status"] = "🟢" if db_id else "❌"
            src = MODULES[key].get("src", "")
            meta["source"] = str(src)
        meta["last_sync"] = st.get(key, {}).get("last_sync", "")
        meta["synced"] = len(st.get(key, {}).get("synced_keys", []))
        meta["errors"] = st.get(key, {}).get("errors", 0)
        meta["stats"] = st.get(key, {}).get("stats", {})
        out["modules"][key] = meta
    out["engine_version"] = ENGINE_VERSION
    out["std_attrs"] = list(STD_SCHEMA) + list(FORMULA_SCHEMA)
    if json_out:
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    print("📡 龍魂 Notion 公开化 · 同步状态")
    for key, meta in out["modules"].items():
        if key in PRE_REGISTERED:
            print(f"  {meta['status']} {key}: {meta['note']}")
        else:
            print(f"  {meta['status']} {key}: {meta['url'] or '未初始化'} "
                  f"· 已同步 {meta['synced']} · 最后 {str(meta['last_sync'])[:19]}")
    print("  公开化提示: 打开数据库页面 → Share → Publish(手动一步)")
    return 0


def cmd_list(module=None):
    cfg = _load_cfg()
    dbs = cfg.get("databases", {})
    tok = hs.get_token()
    mods = list(MODULES) if module in (None, "all", "") else [module]
    for key in mods:
        m = MODULES.get(key)
        if not m:
            continue
        print(f"[{key}] 本地数据源: {m.get('sourcetip')}")
        try:
            recs = m["load"]()
            print(f"  记录 {len(recs)} 条")
            db_id = dbs.get(m["db"])
            done = 0
            if tok and db_id:
                for r in recs:
                    dna = r.get("dna", "") or ""
                    if dna and hs._query_exists(db_id, "DNA追溯码", dna, tok):
                        done += 1
            print(f"  已同步(按dna) {done} 条")
        except Exception as e:  # noqa: BLE001
            print(f"  读取失败: {e}")
    return 0


# ─────────────────────────── 优化六: 运维子命令 ───────────────────────────

def _prop_plain(page, name):
    """从 query 结果页提取某属性 plain_text(rich_text/title/select/date/number/formula)"""
    p = (page.get("properties") or {}).get(name) or {}
    t = p.get("type", "")
    try:
        if t in ("rich_text", "title"):
            return "".join(x.get("plain_text", "") for x in p.get(t, []) or [])
        if t == "select":
            return (p.get("select") or {}).get("name", "")
        if t == "date":
            return (p.get("date") or {}).get("start", "")
        if t == "number":
            return str(p.get("number") or "")
        if t == "formula":
            inner = p.get("formula") or {}
            v = inner.get(inner.get("type", ""))
            return str(v or "") if v is not None else ""
        if t == "checkbox":
            return str(bool(p.get("checkbox")))
    except Exception:  # noqa: BLE001
        pass
    return ""


def _query_pages(db_id, tok, cap=2000):
    """分页拉全库行 → [{id, created_time, props:{col:value-str}}]"""
    out, cursor, guard = [], None, 0
    while guard < 100:
        body = {"page_size": 100, "start_cursor": cursor or None}
        body = {k: v for k, v in body.items() if v is not None}
        if cursor:
            body["start_cursor"] = cursor
        code, data = hs._api("POST", f"/databases/{db_id}/query", body, tok=tok)
        if code != 200 or not isinstance(data, dict):
            return out
        rows = data.get("results")
        for pg in (rows if isinstance(rows, list) else []):
            out.append({"id": pg.get("id", ""),
                        "created_time": (pg.get("created_time") or "")[:19].replace("T", " "),
                        "props": {k: _prop_plain(pg, k) for k in pg.get("properties", {})}})
            if len(out) >= cap:
                return out
        if not data.get("has_more"):
            return out
        cursor = data.get("next_cursor")
        guard += 1
    return out


def _page_dna(page, key=""):
    return page["props"].get("DNA追溯码", "") or page["props"].get("dna", "")


def _plain_of(v):
    """属性值 → 归一纯文本(兼容 Notion API dict 与 _query_pages 已归一 str)"""
    if not isinstance(v, dict):
        return str(v or "")
    for k in ("rich_text", "title"):
        if k in v and isinstance(v[k], list):
            return "".join(
                str(x.get("text", {}).get("content", "")
                    if isinstance(x.get("text"), dict)
                    else x.get("plain_text", ""))
                for x in v[k])
    if "select" in v:
        return str((v["select"] or {}).get("name", ""))
    if "date" in v:
        d = v["date"]
        return str(d.get("start", "") if isinstance(d, dict) else (d or ""))
    if "number" in v:
        return str(v["number"])
    if "formula" in v:
        f = v["formula"]
        return str(f.get("string", "") if isinstance(f, dict) else (f or ""))
    return str(v)


def _prop_diffs(rowp, props):
    """回填判定: 模块自有列(非 DNA/标准 5/公式)本地与行值差异 → {col: props值}"""
    skips = set(STD_SCHEMA) | set(FORMULA_SCHEMA) | {"DNA追溯码"}
    out = {}
    for k, v in (props or {}).items():
        if k in skips or not isinstance(v, dict):
            continue
        nv = _plain_of(v)
        ov = _plain_of(rowp.get(k)) if isinstance(rowp, dict) else ""
        if (nv or "") != (ov or ""):
            out[k] = v
    return out


def cmd_route(action="list", module=""):
    """route list / route test <module>: 路由注册表查看与预处理器冒烟"""
    if action == "test":
        if module not in MODULES:
            print(f"  ❌ 未知模块: {module}")
            return 1
        m = MODULES[module]
        print(f"📡 route test [{module}] · {m['name']}")
        print(f"  路由: filter={'✔' if m.get('filter') else '—'} · "
              f"transform={'✔' if m.get('transform') else '—'} · "
              f"pre_hook={'✔' if (m.get('pre_hook') or GLOBAL_HOOKS['pre'].get(module)) else '—'} · "
              f"post_hook={'✔' if (m.get('post_hook') or GLOBAL_HOOKS['post'].get(module)) else '—'} · "
              f"on_error={'✔' if (m.get('on_error') or GLOBAL_HOOKS['on_error'].get(module)) else '—'}")
        try:
            recs = m["load"]()
            if m.get("filter"):
                recs = [r for r in recs if m["filter"](r)]
            samples = recs[:3] if recs else []
            print(f"  数据源加载 {len(recs)} 条(过 filter 后) · 样本:")
            for r in samples:
                if m.get("transform"):
                    r = m["transform"](r) or r
                dna = m.get("dna_key")(r) if m.get("dna_key") else _dna(module, r, m["dedup"](r))
                print(f"    - {m['title'](r)[:50]} · DNA={str(dna)[:44]}")
            print("  ✅ route test 通过(预处理器正常)")
        except Exception as e:  # noqa: BLE001
            print(f"  🔴 route test 失败: {e}")
            return 2
        return 0
    # list
    cfg = _load_cfg()
    dbs = cfg.get("databases", {})
    print("📡 模块路由注册表")
    for key, m in MODULES.items():
        hooks = []
        if m.get("pre_hook") or GLOBAL_HOOKS["pre"].get(key):
            hooks.append("pre")
        if m.get("post_hook") or GLOBAL_HOOKS["post"].get(key):
            hooks.append("post")
        if m.get("on_error") or GLOBAL_HOOKS["on_error"].get(key):
            hooks.append("on_error")
        f = m.get("filter") and "filter" or ""
        t = m.get("transform") and "transform" or ""
        dbn = dbs.get(m["db"], "")
        print(f"  {key:12s} db=…{dbn[-8:]:8s} " if dbn else f"  {key:12s} db=未初始化   ",
              end="")
        print(f"hooks=[{','.join(hooks) or '—'}] filter={f or '—'} transform={t or '—'}")
    return 0


def cmd_diff(module, fmt="table"):
    """diff <module>: 本地 dedup 集合 vs Notion DNA追溯码集合 → 差异清单"""
    if module not in MODULES:
        print(f"  ❌ 未知模块: {module}")
        return 1
    cfg = _load_cfg()
    tok = hs.get_token()
    m = MODULES[module]
    db_id = cfg.get("databases", {}).get(m["db"])
    if not tok or not db_id:
        print(f"  🔴 token/库不可用({m['db']})")
        return 2
    local, remotes, dedups = [], [], set()
    try:
        for r in m["load"]():
            d = m.get("dna_key")(r) if m.get("dna_key") else _dna(module, r, m["dedup"](r))
            dedups.add(str(d))
            local.append((str(d), m["title"](r)))
    except Exception as e:  # noqa: BLE001
        print(f"  🔴 本地源读取失败: {e}")
        return 3
    for pg in _query_pages(db_id, tok):
        d = _page_dna(pg, module)
        if d:
            remotes.append((d, pg["created_time"]))
    remote_set = {d for d, _ in remotes}
    only_local = [x for x in local if x[0] not in remote_set]
    only_remote = [x for x in remotes if x[0] not in dedups]
    same = [x for x in local if x[0] in remote_set]
    if fmt == "json":
        print(json.dumps({"module": module, "local": len(local), "notion": len(remotes),
                          "in_both": len(same), "only_local": len(only_local),
                          "only_remote": len(only_remote)},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"📡 diff [{module}] · 本地 {len(local)} · Notion {len(remotes)} · "
          f"一致 {len(same)}")
    print(f"  仅本地(将推送) {len(only_local)} 条:")
    for d, t in only_local[:15]:
        print(f"    + {d[:48]} · {t[:40]}")
    if len(only_local) > 15:
        print(f"    … 共 {len(only_local)}")
    print(f"  仅 Notion(幽灵行·源已删) {len(only_remote)} 条:")
    for d, ct in only_remote[:15]:
        print(f"    - {d[:48]} · created {ct}")
    if len(only_remote) > 15:
        print(f"    … 共 {len(only_remote)}")
    return 0


def cmd_verify(module):
    """verify <module>: 数据哈希比对(本地重算 vs Notion 库内) → 一致性"""
    if module not in MODULES:
        print(f"  ❌ 未知模块: {module}")
        return 1
    cfg = _load_cfg()
    tok = hs.get_token()
    m = MODULES[module]
    db_id = cfg.get("databases", {}).get(m["db"])
    if not tok or not db_id:
        print(f"  🔴 token/库不可用({m['db']})")
        return 2
    try:
        records = m["load"]()
    except Exception as e:  # noqa: BLE001
        print(f"  🔴 本地源读取失败: {e}")
        return 3
    local_dna = {}
    for r in records:
        d = m.get("dna_key")(r) if m.get("dna_key") else _dna(module, r, m["dedup"](r))
        local_dna[str(d)] = _hash_rec(r)
    rows = _query_pages(db_id, tok)
    ok = bad = unverifiable = 0
    bad_samples = []
    for pg in rows:
        d = _page_dna(pg, module)
        if not d:
            unverifiable += 1
            continue
        if d not in local_dna:
            unverifiable += 1  # Notion 有·本地源已无(无法重算·不判坏)
            continue
        want = local_dna[d]
        got = pg["props"].get("数据哈希", "")
        if not got or not got.startswith("lh1:"):
            unverifiable += 1  # 补列前旧行无哈希·待下轮回填(非坏)
            continue
        if got == want:
            ok += 1
        else:
            bad += 1
            if len(bad_samples) < 5:
                bad_samples.append({"dna": d[:48], "want": want[:32],
                                    "got": (got or "")[:32]})
    total = ok + bad
    rate = round(ok / total * 100, 1) if total else 100.0
    line = (f"📡 verify [{module}] · Notion {len(rows)} 行 · 可比对 {total} · "
            f"一致 {ok}({rate}%) · 不一致 {bad} · 无法比对 {unverifiable}")
    print(line)
    for s in bad_samples:
        print(f"    🔴 {s['dna']} want={s['want']} got={s['got']}")
    if not bad and total:
        print("  ✅ 数据哈希全部一致(防篡改通过)")
    # 可运维: 每次 verify 落盘 ~/.longhun/notion_sync_verify.log(追加·可审计)
    try:
        vlog = Path.home() / ".longhun" / "notion_sync_verify.log"
        vlog.parent.mkdir(parents=True, exist_ok=True)
        with vlog.open("a", encoding="utf-8") as fh:
            fh.write(f"{datetime.now().isoformat()} | {module} | 行{len(rows)} | "
                     f"一致{ok} | 不一致{bad} | 无法比对{unverifiable} | "
                     f"{'PASS' if not bad else 'FAIL'}\n")
    except Exception:  # noqa: BLE001
        pass
    return 0 if not bad else 4


def cmd_rollback(module, to_ts, yes=False):
    """rollback <module> --to <ts>: 归档 同步时间>ts 的行(默认只列清单+备份)"""
    ts = (to_ts or "").strip()[:19].replace("T", " ")
    if not ts:
        print("  🔴 需要 --to <YYYY-MM-DD[THH:MM:SS]>")
        return 1
    cfg = _load_cfg()
    tok = hs.get_token()
    m = MODULES.get(module)
    db_id = cfg.get("databases", {}).get(module) if not m else cfg.get("databases", {}).get(m["db"])
    if not tok or not db_id:
        print(f"  🔴 token/库不可用({module})")
        return 2
    hits = []
    for pg in _query_pages(db_id, tok):
        when = pg["props"].get("同步时间") or pg["created_time"]
        if when and str(when)[:19].replace("T", " ") > ts:
            hits.append({"page_id": pg["id"], "同步时间": str(when)[:19],
                         "标题": pg["props"].get("标题", "")[:60],
                         "DNA追溯码": _page_dna(pg, module)[:60]})
    backup_dir = Path.home() / ".longhun" / "notion_rollback"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d%H%M%S")
    bfile = backup_dir / f"{module}-rollback-{stamp}.json"
    bfile.write_text(json.dumps({"module": module, "to": ts, "count": len(hits),
                                 "hits": hits}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"📡 rollback [{module}] 至 {ts} · 命中 {len(hits)} 行(同步时间>ts)")
    for h in hits[:20]:
        print(f"    {h['同步时间']} · {h['标题']} · {h['DNA追溯码']}")
    if len(hits) > 20:
        print(f"    … 共 {len(hits)}")
    print(f"  备份: {bfile}")
    if not hits:
        return 0
    if not yes:
        print("  🟡 未执行 · 加 --yes 才归档(archived=true)")
        return 0
    done = 0
    for h in hits:
        try:
            code, _ = hs._api("PATCH", f"/pages/{h['page_id']}",
                              {"archived": True}, tok=tok)
            if code in (200, 201):
                done += 1
        except Exception:  # noqa: BLE001
            pass
    print(f"  ✅ 已归档 {done}/{len(hits)} (失败=权限不足·Notion content 需授权)")
    return 0 if done == len(hits) else 5


def cmd_clean(module, older_days, yes=False):
    """clean <module> --older-than <days>: 归档 同步时间 早于 N 天的行"""
    try:
        days = int(older_days or 0)
    except ValueError:
        print("  🔴 --older-than 需整数天数")
        return 1
    cfg = _load_cfg()
    tok = hs.get_token()
    m = MODULES.get(module)
    db_id = cfg.get("databases", {}).get(module) if not m else cfg.get("databases", {}).get(m["db"])
    if not tok or not db_id:
        print(f"  🔴 token/库不可用({module})")
        return 2
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")
    hits = []
    for pg in _query_pages(db_id, tok):
        when = pg["props"].get("同步时间") or pg["created_time"]
        if when and str(when)[:19].replace("T", " ") < cutoff:
            hits.append({"page_id": pg["id"], "同步时间": str(when)[:19],
                         "标题": pg["props"].get("标题", "")[:60],
                         "DNA追溯码": _page_dna(pg, module)[:60]})
    print(f"📡 clean [{module}] 早于 {days} 天(cutoff {cutoff}) · 命中 {len(hits)} 行")
    for h in hits[:20]:
        print(f"    {h['同步时间']} · {h['标题']}")
    if len(hits) > 20:
        print(f"    … 共 {len(hits)}")
    if not hits:
        return 0
    if not yes:
        print("  🟡 未执行 · 加 --yes 才归档")
        return 0
    done = 0
    for h in hits:
        try:
            code, _ = hs._api("PATCH", f"/pages/{h['page_id']}",
                              {"archived": True}, tok=tok)
            if code in (200, 201):
                done += 1
        except Exception:  # noqa: BLE001
            pass
    print(f"  ✅ 已归档 {done}/{len(hits)}")
    return 0 if done == len(hits) else 5


# ─────────────────────────── 优化一: 视图层 serve/dashboard ───────────────────────────

_VIEW_CACHE = {"t": 0.0, "data": None}  # 源计数 5 分钟缓存(serve 轻量)


def _src_count(key):
    try:
        n = len(MODULES[key]["load"]())
        return n
    except Exception:  # noqa: BLE001
        return -1


def _state_view():
    """dashboard/serve 共用: 全模块状态聚合(源计数带缓存)"""
    now = time.time()
    if _VIEW_CACHE["data"] and now - _VIEW_CACHE["t"] < 300:
        return _VIEW_CACHE["data"]
    cfg = _load_cfg()
    st = _load_state()
    dbs = cfg.get("databases", {})
    mods, total_synced, total_src, total_err = [], 0, 0, 0
    for key in list(MODULES) + list(PRE_REGISTERED):
        cell = st.get(key, {})
        src = 0
        if key in MODULES:
            src = _src_count(key)
            if src >= 0:
                total_src += src
        synced = len(cell.get("synced_keys", []))
        errs = int(cell.get("errors", 0))
        total_synced += synced
        total_err += errs
        db_id = dbs.get(key, "")
        mods.append({
            "module": key, "name": MODULES[key]["name"] if key in MODULES else "",
            "db": db_id, "url": f"https://www.notion.so/{db_id.replace('-','')}" if db_id else "",
            "source": src, "synced": synced,
            "rate": round(min(100.0, (synced / src * 100) if src else 0.0), 1),
            "errors": errs, "last_sync": cell.get("last_sync", ""),
            "stats": cell.get("stats", {}),
            "published": "待手动 Publish"})
    view = {"time": datetime.now().astimezone().isoformat(),
            "engine_version": ENGINE_VERSION, "modules": mods,
            "total": {"source": total_src, "synced": total_synced,
                      "errors": total_err},
            "std_attrs": list(STD_SCHEMA) + list(FORMULA_SCHEMA)}
    _VIEW_CACHE["data"] = view
    _VIEW_CACHE["t"] = now
    return view


def cmd_dashboard():
    """dashboard: 终端 Markdown 综合看板"""
    v = _state_view()
    print("📡 龍魂 Notion 同步看板 · 引擎 v{} · {}".format(
        v["engine_version"], v["time"][:19]))
    print()
    print("| 模块 | 源记录 | 已同步 | 同步率 | 错误 | 最后同步 |")
    print("|:---|---:|---:|---:|---:|:---|")
    for m in v["modules"]:
        print(f"| {m['module']} | {m['source'] if m['source']>=0 else '—'} | "
              f"{m['synced']} | {m['rate']}% | {m['errors']} | "
              f"{str(m['last_sync'])[:16] or '—'} |")
    print()
    print(f"合计: 源 {v['total']['source']} · 已同步 {v['total']['synced']} · "
          f"错误 {v['total']['errors']}")
    print("标准属性: " + " · ".join(v["std_attrs"]))
    print("提示: 打开 Notion 数据库 → Share → Publish 即可公开浏览")
    return 0


_DASH_HTML = """<!DOCTYPE html>
<html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>🐉 龍魂 Notion 同步仪表盘</title>
<style>
body{font-family:-apple-system,'PingFang SC',sans-serif;background:#0d1117;color:#e6edf3;margin:0;padding:24px}
h1{font-size:22px;color:#58a6ff} h1 small{color:#8b949e;font-weight:400;font-size:13px}
.card{background:#161b22;border:1px solid #30363d;border-radius:10px;padding:16px 18px;margin-bottom:14px}
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:8px 10px;border-bottom:1px solid #21262d}
th{color:#8b949e;font-weight:600}
.bar{background:#21262d;border-radius:6px;overflow:hidden;min-width:90px}
.bar i{display:block;height:8px;background:linear-gradient(90deg,#2ea043,#58a6ff)}
.ok{color:#3fb950}.warn{color:#d29922}.err{color:#f85149}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:10px;margin-bottom:14px}
.k{color:#8b949e;font-size:12px;display:block}
.big{font-size:26px;font-weight:700}
footer{color:#484f58;font-size:12px;margin-top:18px}
</style></head><body>
<h1>🐉 龍魂 · Notion 记忆/公开化同步仪表盘 <small id="ts"></small></h1>
<div class="grid">
  <div class="card"><span class="k">源记录(本地)</span><span class="big" id="src">—</span></div>
  <div class="card"><span class="k">已同步</span><span class="big ok" id="syn">—</span></div>
  <div class="card"><span class="k">错误事件</span><span class="big err" id="err">—</span></div>
  <div class="card"><span class="k">引擎版本</span><span class="big" id="ver">—</span></div>
</div>
<div class="card"><table><thead><tr><th>模块</th><th>库名</th><th>源记录</th>
<th>已同步</th><th>同步率</th><th>错误</th><th>最后同步</th></tr></thead>
<tbody id="rows"></tbody></table></div>
<div class="card" id="std" style="font-size:12px;color:#8b949e"></div>
<footer>🐉 lh sync serve · 127.0.0.1 本机绑定 · 数据来自 notion_sync_state.json + 本地源实时</footer>
<script>
async function load(){try{
 const r=await fetch('/api/state');const v=await r.json();
 document.title='🐉 龍魂 Notion 同步仪表盘';
 ts.textContent=v.time;ver.textContent='v'+v.engine_version;
 src.textContent=v.total.source;syn.textContent=v.total.synced;err.textContent=v.total.errors;
 std.textContent='标准属性: '+v.std_attrs.join(' · ');
 rows.innerHTML=v.modules.map(m=>{const pct=Math.max(0,Math.min(100,m.rate));
  return `<tr><td>${m.module}</td><td style="color:#8b949e">${m.name}</td>
  <td>${m.source<0?'—':m.source}</td><td>${m.synced}</td>
  <td><div class="bar"><i style="width:${pct}%"></i></div>${pct}%</td>
  <td class="${m.errors>0?'err':'ok'}">${m.errors}</td>
  <td style="color:#8b949e">${(m.last_sync||'—').slice(0,16)}</td></tr>`}).join('');
 }catch(e){rows.innerHTML=`<tr><td colspan="7" class="err">加载失败: ${e}</td></tr>`}}
load();setInterval(load,30000);
</script></body></html>"""


def cmd_serve(port=8780):
    """serve: 本地 Web 仪表盘 http://127.0.0.1:{port} · / 仪表盘 · /api/state JSON
    (默认 8780: 8769-8775 段已被 lh_antenna_8ga 等常驻守护占用·勿撞)"""
    import http.server

    class H(http.server.BaseHTTPRequestHandler):
        def log_message(self, format, *a):  # noqa: A002 — 静默(节能)
            pass

        def do_GET(self):
            if self.path.startswith("/api/state"):
                body = json.dumps(_state_view(), ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
            elif self.path in ("/", "/index.html"):
                body = _DASH_HTML.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
            else:
                self.send_response(404)
                body = b"not found"
                self.send_header("Content-Type", "text/plain")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    print(f"📡 龍魂 Notion 同步仪表盘: http://127.0.0.1:{port}  (Ctrl-C 退出)")
    try:
        http.server.ThreadingHTTPServer(("127.0.0.1", port), H).serve_forever()
    except OSError as e:
        print(f"  🟡 端口 {port} 不可用: {e} · 换 --port 如 8771")
    return 0


# ─────────────────────────── main ───────────────────────────

def main():
    # 🔧 argv 归一: 支持 `lh_notion_sync.py <模块|all>` 裸模块形态(与 `lh sync <模块>` 网关透传一致)
    #   argparse subparsers 只认命令 → 裸模块名先转 sync --module
    if sys.argv[1:] and sys.argv[1] in MODULES or (sys.argv[1:] and sys.argv[1] == "all"):
        sys.argv = [sys.argv[0], "sync", "--module", sys.argv[1]] + sys.argv[2:]
    ap = argparse.ArgumentParser(description="📡 龍魂通用 Notion 公开化同步 v1.2 (lh sync)")
    sub = ap.add_subparsers(dest="cmd")
    i = sub.add_parser("init", help="建库(幂等·含标准属性+公式字段) · --module 指定模块或 all")
    i.add_argument("--module", default="all")
    i.add_argument("--quiet", action="store_true")
    s = sub.add_parser("sync", help="推送未同步记录(--module M|all)")
    s.add_argument("--module", default="all")
    s.add_argument("--since", default="", help="只推 >= YYYY-MM-DD 的记录")
    s.add_argument("--since-file", default="", help="从文件读起始时间戳")
    s.add_argument("--dry-run", action="store_true")
    s.add_argument("--quiet", action="store_true")
    s.add_argument("--limit", type=int, default=0, help="每模块最多同步 N 条(测试/分批)")
    s.add_argument("--retry", type=int, default=3, help="推送失败重试 N 次(默认 3)")
    s.add_argument("--fill", action="store_true",
                   help="回填已存在行: 主题/摘要与本地关键字不一致时 PATCH 更新(如记忆主题列填充)")
    s.add_argument("--batch-size", type=int, default=50, help="进度输出批次(默认 50)")
    s.add_argument("--format", choices=["table", "json"], default="table",
                   help="输出格式(脚本集成用 json)")
    st = sub.add_parser("status", help="库链接/同步状态(--json)")
    st.add_argument("--json", action="store_true")
    lp = sub.add_parser("list", help="本地数据源清单")
    lp.add_argument("--module", default="all")
    sub.add_parser("dashboard", help="终端 Markdown 综合看板")
    sv = sub.add_parser("serve", help="本地 Web 仪表盘(默认 127.0.0.1:8780)")
    sv.add_argument("--port", type=int, default=8780)
    rt = sub.add_parser("route", help="路由注册表: list / test <module>")
    rt_sub = rt.add_subparsers(dest="route_cmd")
    rt_sub.add_parser("list", help="列出所有模块路由配置")
    rt_test = rt_sub.add_parser("test", help="测试某模块预处理器")
    rt_test.add_argument("module", nargs="?", default="")
    d1 = sub.add_parser("diff", help="diff <module>: 本地 vs Notion 差异清单")
    d1.add_argument("module")
    d1.add_argument("--format", choices=["table", "json"], default="table")
    v1 = sub.add_parser("verify", help="verify <module>: 数据哈希一致性比对")
    v1.add_argument("module")
    rb = sub.add_parser("rollback", help="rollback <module> --to <ts>: 归档同步时间>ts 的行")
    rb.add_argument("module")
    rb.add_argument("--to", default="")
    rb.add_argument("--yes", action="store_true", help="确认归档(archived=true)")
    cl = sub.add_parser("clean", help="clean <module> --older-than <days>: 归档早于 N 天的行")
    cl.add_argument("module")
    cl.add_argument("--older-than", type=int, default=0)
    cl.add_argument("--yes", action="store_true")
    args = ap.parse_args()
    # 兼容 lh sync <module|all> 形态: argv[1] 若是模块名 → 自动转为 sync --module
    if args.cmd in MODULES or args.cmd in PRE_REGISTERED or args.cmd == "all":
        return cmd_sync(module=args.cmd if args.cmd != "all" else "all")
    if args.cmd == "init":
        return cmd_init(module=args.module, quiet=args.quiet)
    if args.cmd == "sync":
        return cmd_sync(module=args.module, since=args.since, since_file=args.since_file,
                        dry_run=args.dry_run, quiet=args.quiet, limit=args.limit,
                        retry=args.retry, batch_size=args.batch_size, fmt=args.format,
                        fill=args.fill)
    if args.cmd == "status":
        return cmd_status(json_out=args.json)
    if args.cmd == "list":
        return cmd_list(module=args.module)
    if args.cmd == "dashboard":
        return cmd_dashboard()
    if args.cmd == "serve":
        return cmd_serve(port=args.port)
    if args.cmd == "route":
        if args.route_cmd == "test":
            return cmd_route("test", args.module)
        return cmd_route("list")
    if args.cmd == "diff":
        return cmd_diff(args.module, fmt=args.format)
    if args.cmd == "verify":
        return cmd_verify(args.module)
    if args.cmd == "rollback":
        return cmd_rollback(args.module, args.to, yes=args.yes)
    if args.cmd == "clean":
        return cmd_clean(args.module, args.older_than, yes=args.yes)
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
