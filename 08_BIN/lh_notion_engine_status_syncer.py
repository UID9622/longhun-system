#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · Notion 引擎状态同步器 v2.0
DNA: #龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-NOTION-ENGINE-STATUS-SYNCER-v2.0-7D5E8F9A
创建者: 诸葛鑫 (UID9622)
协议: CC BY-NC-SA 4.0

基于 Notion 数据库 Schema v2.0 生成导入就绪数据：
  - 决策归档（为什么存在这个引擎）
  - 毫秒级响应分级与 SLA
  - 自动化标签与触发方式
  - 完整性审计与健康分
  - 三色风险标签

用法:
  python3 bin/lh_notion_engine_status_syncer.py              # dry-run 生成同步文件
  python3 bin/lh_notion_engine_status_syncer.py --execute    # 调用 Notion API（需 token）
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

CST = timezone(timedelta(hours=8))

DNA = "#龍芯⚡️丙午·丙申·癸酉·庚申·䷒临-NOTION-ENGINE-STATUS-SYNCER-v2.0-7D5E8F9A"
SCHEMA_VERSION = "2.0.1"

ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT / "data" / "notion_sync" / "engines"
REGISTRY_FILE = OUTPUT_DIR / "engine_registry.json"
INTEGRITY_FILE = OUTPUT_DIR / "integrity_report.json"
JSONL_FILE = OUTPUT_DIR / "notion_import.jsonl"
CSV_FILE = OUTPUT_DIR / "notion_import.csv"
SYNC_PLAN_FILE = OUTPUT_DIR / "sync_plan.json"
SCHEMA_FILE = OUTPUT_DIR / "notion_db_schema_v2.json"

# CSV 列定义（与 Schema v2.0 对齐）
CSV_COLUMNS = [
    "id", "name", "filename", "path", "dna", "description",
    "category", "subcategory", "content_type", "type", "status", "priority",
    "decision_archive", "decision_log", "archive_date", "owner",
    "response_level", "response_ms", "sla",
    "automation_tags", "automation_ready", "triggers",
    "ops_tags", "tested", "documented", "audited", "audit_notes", "health_score",
    "function_count", "class_count", "import_count", "lines", "size_bytes",
    "last_scan", "last_verify", "last_run", "runlog_summary", "last_exit_code", "last_job_id",
    "next_audit", "dependency_risk",
    "functions", "classes", "imports",
    "code_url", "doc_url",
]


def _now() -> str:
    return datetime.now(CST).isoformat()


def _today() -> str:
    return datetime.now(CST).strftime("%Y-%m-%d")


def _next_audit_date() -> str:
    return (datetime.now(CST) + timedelta(days=7)).strftime("%Y-%m-%d")


def _log(msg: str, level: str = "INFO"):
    markers = {"INFO": "📋", "OK": "✅", "WARN": "🟡", "ERROR": "🔴", "SKIP": "⏭️", "SYNC": "🔄"}
    print(f"[{datetime.now(CST).strftime('%H:%M:%S')}] {markers.get(level, 'ℹ️')} {msg}")


def load_json(path: Path) -> Optional[Dict[str, Any]]:
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_integrity_index(integrity_report: Optional[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """建立 path -> integrity result 索引"""
    idx: Dict[str, Dict[str, Any]] = {}
    if not integrity_report:
        return idx
    for result in integrity_report.get("results", []):
        path = result.get("path", "")
        if path:
            idx[path] = result
    return idx


# lh-ctl 命令名 → 注册表引擎文件名（stem）映射
CMD_TO_ENGINE = {
    "search": "lh_search_engine",
    "video": "lh_video_studio",
    "distill": "lh_k3_distill_v39",
    "audit": "lh_sg_auditor",
}


def build_runlog_index(job_history_path: Path) -> Dict[str, Dict[str, Any]]:
    """读取 lh-ctl 运行历史，按引擎 stem 取最新记录。"""
    idx: Dict[str, Dict[str, Any]] = {}
    if not job_history_path.exists():
        return idx
    with open(job_history_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                continue
            cmd = rec.get("command", "")
            engine_name = CMD_TO_ENGINE.get(cmd, cmd)
            # 保留时间最新的记录
            prev = idx.get(engine_name)
            if prev is None or rec.get("started_at", "") > prev.get("started_at", ""):
                idx[engine_name] = rec
    return idx


def compute_content_type(engine: Dict[str, Any]) -> List[str]:
    """推断内容类型"""
    tags = []
    etype = engine.get("type", "")
    path = engine.get("path", "").lower()
    name = engine.get("name", "").lower()

    if etype == "engine":
        tags.append("核心引擎")
    elif etype == "script":
        tags.append("工具脚本")
    elif etype == "skill":
        tags.append("技能库")

    if name.startswith("test_") or name.endswith("_test") or "/tests/" in path:
        tags.append("测试")
    elif name in ("__init__",):
        tags.append("模块入口")
    elif ".md" in path or "readme" in name:
        tags.append("文档")
    elif "config" in name or "settings" in name or ".yaml" in path or ".json" in path:
        tags.append("配置")
    elif "template" in name or "example" in name:
        tags.append("模板")

    ops = engine.get("ops_tags", [])
    if "核心引擎" in ops:
        tags.append("核心引擎")
    if "技能库" in ops:
        tags.append("技能库")

    return list(set(tags)) if tags else ["未分类"]


def compute_decision(engine: Dict[str, Any]) -> Tuple[str, str]:
    """决策归档状态 + 决策记录摘要"""
    status = engine.get("status", "active")
    dna = engine.get("dna", "")
    description = engine.get("description", "")
    path = engine.get("path", "")
    category = engine.get("category", "")
    subcategory = engine.get("subcategory", "")

    if status == "deprecated":
        archive = "已归档"
    elif dna and dna != "未注册" and description and description != "（无描述）":
        archive = "已归档"
    else:
        archive = "待归档"

    decision_log = (
        f"[{category} > {subcategory}] "
        f"该引擎负责 {description[:40] if description else '（待补充功能描述）'}，"
        f"位于 {path}。"
        f"决策：纳入龍魂引擎注册表统一管理；"
        f"下次审计：{_next_audit_date()}。"
    )
    return archive, decision_log


def compute_response(engine: Dict[str, Any]) -> Tuple[str, int, str]:
    """响应等级 / 预计响应(ms) / SLA"""
    path = engine.get("path", "").lower()
    name = engine.get("name", "").lower()
    imports = [i.lower() for i in engine.get("imports", [])]
    ops_tags = engine.get("ops_tags", [])

    # API / 网关 / 实时推理 → 毫秒级
    if any(k in path for k in ["api", "gateway", "router", "realtime", "stream"]):
        return "毫秒级", 10, "P99<10ms"
    if any(k in name for k in ["api", "gateway", "router", "server"]):
        return "毫秒级", 10, "P99<10ms"
    if "flask" in imports or "fastapi" in imports or "aiohttp" in imports:
        return "毫秒级", 50, "P99<100ms"

    # 模型训练 / 大数据处理 → 分钟级
    if any(k in path for k in ["train", "distill", "lora", "data", "backup"]):
        return "分钟级", 60000, "无SLA"
    if any(k in name for k in ["train", "distill", "backup", "sync"]):
        return "分钟级", 60000, "无SLA"
    if "torch" in imports or "mlx" in imports or "transformers" in imports:
        return "分钟级", 60000, "无SLA"

    # 检测 / 审计 / 工具脚本 → 秒级
    if any(k in path for k in ["audit", "detect", "scan", "check"]):
        return "秒级", 500, "P99<1s"

    # 有网络依赖 → 秒级
    if "有网络依赖" in ops_tags:
        return "秒级", 300, "P99<1s"

    # 默认：秒级
    return "秒级", 100, "P99<1s"


def compute_automation(engine: Dict[str, Any]) -> Tuple[List[str], bool, List[str]]:
    """自动化标签 / 自动化就绪 / 触发方式"""
    path = engine.get("path", "").lower()
    name = engine.get("name", "").lower()
    ops_tags = engine.get("ops_tags", [])
    imports = [i.lower() for i in engine.get("imports", [])]

    tags = []
    triggers = []

    # 扫描/审计类 → 自动扫描 + 自动审计
    if any(k in name for k in ["discovery", "audit", "scan", "labeler", "mapper", "syncer", "checker"]):
        tags.extend(["自动扫描", "自动审计"])
        triggers.append("Cron")

    # 训练/部署类 → CI/CD + 自动部署
    if any(k in name for k in ["train", "deploy", "distill", "export"]):
        tags.extend(["CI/CD", "自动部署"])
        triggers.append("Webhook")

    # 备份类 → 自动备份
    if any(k in name for k in ["backup", "sync"]):
        tags.append("自动备份")
        triggers.append("Cron")

    # 守护/健康类 → Cron
    if any(k in name for k in ["daemon", "health", "monitor", "watch"]):
        triggers.append("Cron")

    # API 类 → API + Webhook
    if any(k in path for k in ["api", "gateway"]):
        triggers.extend(["API", "Webhook"])

    # 默认触发方式
    if not triggers:
        triggers.append("Manual")

    # 自动化就绪：没有关键 TODO/FIXME、不是实验性、有描述
    ready = (
        "待修复" not in ops_tags
        and "已废弃" not in ops_tags
        and "实验性" not in ops_tags
        and engine.get("description", "") not in ("", "（无描述）")
    )

    tags = list(set(tags)) if tags else ["待评估"]
    triggers = list(set(triggers))
    return tags, ready, triggers


def compute_dependency_risk(engine: Dict[str, Any]) -> str:
    """依赖风险等级"""
    ops_tags = engine.get("ops_tags", [])
    imports = engine.get("imports", [])

    if "有网络依赖" in ops_tags:
        return "高"
    if "有系统调用" in ops_tags:
        return "中"
    if len(imports) > 15:
        return "中"
    if len(imports) <= 5:
        return "低"
    return "中"


def compute_health_and_audit(engine: Dict[str, Any],
                             integrity_result: Optional[Dict[str, Any]]) -> Tuple[bool, str, int, str]:
    """已通过审计 / 审计备注 / 健康分 / 最后验证时间"""
    if not integrity_result:
        return False, "未执行完整性检查", 50, ""

    passed = integrity_result.get("passed", False)
    issues = integrity_result.get("issues", [])
    severity = integrity_result.get("severity", "unknown")

    audit_notes_parts = []
    for issue in issues:
        audit_notes_parts.append(f"[{issue.get('severity', '?')}] {issue.get('message', '')}")
    audit_notes = "；".join(audit_notes_parts) if audit_notes_parts else "无问题"

    # 健康分：100 - 扣分
    score = 100
    if not passed:
        if severity == "critical":
            score -= 30
        elif severity == "high":
            score -= 20
        else:
            score -= 10
    score -= len(issues) * 5
    score = max(0, min(100, score))

    # 最后验证时间：用 integrity_report 生成时间
    last_verify = integrity_result.get("scanned_at", "")

    return passed, audit_notes, score, last_verify


def _to_notion_properties(engine: Dict[str, Any],
                          integrity_result: Optional[Dict[str, Any]],
                          runlog_result: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """将引擎条目转换为 Notion 数据库 properties 格式（Schema v2.0）"""
    content_type = compute_content_type(engine)
    decision_archive, decision_log = compute_decision(engine)
    response_level, response_ms, sla = compute_response(engine)
    auto_tags, auto_ready, triggers = compute_automation(engine)
    audited, audit_notes, health_score, last_verify = compute_health_and_audit(engine, integrity_result)
    dep_risk = compute_dependency_risk(engine)

    tested = "未测试" not in engine.get("ops_tags", [])
    documented = engine.get("description", "") not in ("", "（无描述）")

    scanned_at = engine.get("scanned_at", "")
    scanned_date = scanned_at[:10] if scanned_at else _today()
    verify_date = last_verify[:10] if last_verify else scanned_date

    code_url = f"https://github.com/uid9622/longhun-system/tree/main/{engine.get('path', '')}"
    doc_url = ""
    if engine.get("path", "").endswith(".py"):
        doc_url = f"https://uid9622.cn/docs/{engine.get('name', '')}"

    props = {
        # 基础身份
        "名称": {"title": [{"text": {"content": str(engine.get("name", ""))}}]},
        "引擎ID": {"rich_text": [{"text": {"content": str(engine.get("id", ""))}}]},
        "分类": {"select": {"name": str(engine.get("category", "未分类"))}},
        "子分类": {"select": {"name": str(engine.get("subcategory", "未分类"))}},
        "内容类型": {"multi_select": [{"name": t} for t in content_type]},
        "类型": {"select": {"name": str(engine.get("type", "unknown"))}},
        "状态": {"select": {"name": str(engine.get("status", "active"))}},
        "优先级": {"number": int(engine.get("priority", 0))},
        "说明": {"rich_text": [{"text": {"content": str(engine.get("description", "")[:2000])}}]},
        "DNA": {"rich_text": [{"text": {"content": str(engine.get("dna", "未注册"))}}]},
        "路径": {"rich_text": [{"text": {"content": str(engine.get("path", ""))}}]},
        "代码链接": {"url": code_url if engine.get("path") else None},
        "文档链接": {"url": doc_url or None},

        # 决策归档
        "决策归档": {"select": {"name": decision_archive}},
        "决策记录": {"rich_text": [{"text": {"content": decision_log}}]},
        "归档时间": {"date": {"start": _today()}},
        "责任人": {"rich_text": [{"text": {"content": "UID9622"}}]},

        # 性能 / 毫秒级响应
        "响应等级": {"select": {"name": response_level}},
        "预计响应(ms)": {"number": response_ms},
        "性能要求": {"select": {"name": sla}},

        # 自动化
        "自动化标签": {"multi_select": [{"name": t} for t in auto_tags]},
        "自动化就绪": {"checkbox": auto_ready},
        "触发方式": {"multi_select": [{"name": t} for t in triggers]},

        # 运维 / 审计
        "运维标签": {"multi_select": [{"name": tag} for tag in engine.get("ops_tags", [])]},
        "已测试": {"checkbox": tested},
        "已文档化": {"checkbox": documented},
        "已通过审计": {"checkbox": audited},
        "审计备注": {"rich_text": [{"text": {"content": audit_notes[:2000]}}]},
        "健康分": {"number": health_score},

        # 规模
        "函数数": {"number": len(engine.get("functions", []))},
        "类数": {"number": len(engine.get("classes", []))},
        "导入数": {"number": len(engine.get("imports", []))},
        "行数": {"number": int(engine.get("lines", 0))},
        "体积(bytes)": {"number": int(engine.get("size_bytes", 0))},

        # 时间
        "最后扫描": {"date": {"start": scanned_date}},
        "最后验证": {"date": {"start": verify_date}},
        "下次审计": {"date": {"start": _next_audit_date()}},

        # 依赖 / 元数据
        # 注意：函数/类/导入模块改为 rich_text，防止 Notion multi_select 选项爆炸导致
        # database schema has exceeded the maximum size
        "依赖风险": {"select": {"name": dep_risk}},
        "重要函数": {"rich_text": [{"text": {"content": ", ".join(engine.get("functions", [])[:30])}}]},
        "重要类": {"rich_text": [{"text": {"content": ", ".join(engine.get("classes", [])[:30])}}]},
        "导入模块": {"rich_text": [{"text": {"content": ", ".join(engine.get("imports", [])[:30])}}]},
    }

    # 运行日志摘要（由 lh-ctl 写入）
    if runlog_result:
        started = runlog_result.get("started_at", "")
        summary = runlog_result.get("summary", "")
        exit_code = runlog_result.get("exit_code")
        job_id = runlog_result.get("job_id", "")
        if started:
            props["最后运行"] = {"date": {"start": started[:10]}}
        if summary:
            props["运行日志摘要"] = {"rich_text": [{"text": {"content": summary[:2000]}}]}
        if exit_code is not None:
            props["最后退出码"] = {"number": int(exit_code)}
        if job_id:
            props["最后任务ID"] = {"rich_text": [{"text": {"content": job_id}}]}

    # 剔除空值属性（Notion API 拒绝空 date/None url）
    cleaned: Dict[str, Any] = {}
    for k, v in props.items():
        if "url" in v and v.get("url") is None:
            continue
        if v.get("date", {}).get("start") == "":
            continue
        cleaned[k] = v
    return cleaned


def _to_flat_row(engine: Dict[str, Any],
                 integrity_result: Optional[Dict[str, Any]],
                 runlog_result: Optional[Dict[str, Any]]) -> Dict[str, str]:
    """将引擎条目展平为 CSV 行"""
    content_type = compute_content_type(engine)
    decision_archive, decision_log = compute_decision(engine)
    response_level, response_ms, sla = compute_response(engine)
    auto_tags, auto_ready, triggers = compute_automation(engine)
    audited, audit_notes, health_score, last_verify = compute_health_and_audit(engine, integrity_result)
    dep_risk = compute_dependency_risk(engine)

    tested = "未测试" not in engine.get("ops_tags", [])
    documented = engine.get("description", "") not in ("", "（无描述）")

    scanned_at = engine.get("scanned_at", "")
    scanned_date = scanned_at[:10] if scanned_at else _today()
    verify_date = last_verify[:10] if last_verify else scanned_date

    last_run = ""
    runlog_summary = ""
    last_exit_code = ""
    last_job_id = ""
    if runlog_result:
        started = runlog_result.get("started_at", "")
        last_run = started[:10] if started else ""
        runlog_summary = runlog_result.get("summary", "")
        exit_code = runlog_result.get("exit_code")
        last_exit_code = "" if exit_code is None else str(exit_code)
        last_job_id = runlog_result.get("job_id", "")

    return {
        "id": str(engine.get("id", "")),
        "name": str(engine.get("name", "")),
        "filename": str(engine.get("filename", "")),
        "path": str(engine.get("path", "")),
        "dna": str(engine.get("dna", "")),
        "description": str(engine.get("description", "")).replace("\n", " "),
        "category": str(engine.get("category", "")),
        "subcategory": str(engine.get("subcategory", "")),
        "content_type": "|".join(content_type),
        "type": str(engine.get("type", "")),
        "status": str(engine.get("status", "")),
        "priority": str(engine.get("priority", "")),
        "decision_archive": decision_archive,
        "decision_log": decision_log,
        "archive_date": _today(),
        "owner": "UID9622",
        "response_level": response_level,
        "response_ms": str(response_ms),
        "sla": sla,
        "automation_tags": "|".join(auto_tags),
        "automation_ready": str(auto_ready),
        "triggers": "|".join(triggers),
        "ops_tags": "|".join(engine.get("ops_tags", [])),
        "tested": str(tested),
        "documented": str(documented),
        "audited": str(audited),
        "audit_notes": audit_notes,
        "health_score": str(health_score),
        "function_count": str(len(engine.get("functions", []))),
        "class_count": str(len(engine.get("classes", []))),
        "import_count": str(len(engine.get("imports", []))),
        "lines": str(engine.get("lines", "")),
        "size_bytes": str(engine.get("size_bytes", "")),
        "last_scan": scanned_date,
        "last_verify": verify_date,
        "last_run": last_run,
        "runlog_summary": runlog_summary,
        "last_exit_code": last_exit_code,
        "last_job_id": last_job_id,
        "next_audit": _next_audit_date(),
        "dependency_risk": dep_risk,
        "functions": "|".join(engine.get("functions", [])),
        "classes": "|".join(engine.get("classes", [])),
        "imports": "|".join(engine.get("imports", [])),
        "code_url": f"https://github.com/uid9622/longhun-system/tree/main/{engine.get('path', '')}",
        "doc_url": "",
    }


def build_sync_payload(engines: List[Dict[str, Any]],
                       integrity_index: Dict[str, Dict[str, Any]],
                       runlog_index: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    """构建同步载荷"""
    _log("构建 Notion 同步载荷 (Schema v2.0)...", "SYNC")

    records: List[Dict[str, Any]] = []
    for eng in engines:
        path = eng.get("path", "")
        name = eng.get("name", "")
        integrity_result = integrity_index.get(path)
        runlog_result = runlog_index.get(name)
        record = dict(eng)
        record["external_id"] = eng.get("id")
        record["properties"] = _to_notion_properties(eng, integrity_result, runlog_result)
        records.append(record)

    payload = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "schema_version": SCHEMA_VERSION,
        "schema_file": str(SCHEMA_FILE),
        "generated_at": _now(),
        "total_records": len(records),
        "database_title": "龍魂引擎注册表 v2",
        "records": records,
    }

    _log(f"载荷构建完成: {len(records)} 条记录", "OK")
    return payload


def write_jsonl(engines: List[Dict[str, Any]], path: Path):
    """写入 JSONL 文件"""
    with open(path, "w", encoding="utf-8", newline="") as f:
        for eng in engines:
            record = {
                "external_id": eng.get("external_id"),
                "name": eng.get("name"),
                "properties": eng.get("properties"),
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_csv(engines: List[Dict[str, Any]],
              integrity_index: Dict[str, Dict[str, Any]],
              runlog_index: Dict[str, Dict[str, Any]],
              path: Path):
    """写入 CSV 文件"""
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for eng in engines:
            path = eng.get("path", "")
            name = eng.get("name", "")
            writer.writerow(_to_flat_row(eng, integrity_index.get(path), runlog_index.get(name)))


def save_outputs(payload: Dict[str, Any],
                 integrity_index: Dict[str, Dict[str, Any]],
                 runlog_index: Dict[str, Dict[str, Any]],
                 dry_run: bool):
    """保存 JSONL、CSV 和同步计划"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    plan = {
        "dna": DNA,
        "version": SCHEMA_VERSION,
        "schema_version": SCHEMA_VERSION,
        "schema_file": str(SCHEMA_FILE),
        "generated_at": _now(),
        "dry_run": dry_run,
        "total_records": payload["total_records"],
        "output_files": {
            "jsonl": str(JSONL_FILE),
            "csv": str(CSV_FILE),
        },
        "notion_api_called": False,
        "notion_api_status": "skipped (dry-run)" if dry_run else "pending",
        "records": [{"external_id": r["external_id"], "name": r["name"]} for r in payload["records"]],
    }

    if dry_run:
        _log(f"[DRY-RUN] 不写入文件: {JSONL_FILE}", "SKIP")
        _log(f"[DRY-RUN] 不写入文件: {CSV_FILE}", "SKIP")
    else:
        write_jsonl(payload["records"], JSONL_FILE)
        _log(f"已保存: {JSONL_FILE}", "OK")

        write_csv(payload["records"], integrity_index, runlog_index, CSV_FILE)
        _log(f"已保存: {CSV_FILE}", "OK")

    with open(SYNC_PLAN_FILE, "w", encoding="utf-8") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    _log(f"已保存: {SYNC_PLAN_FILE}", "OK")


def _notion_post(url: str, token: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """向 Notion API 发送 POST 请求并返回响应。"""
    import urllib.request
    import urllib.error

    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return {"ok": True, "status": resp.status, "data": json.loads(resp.read().decode("utf-8"))}
    except urllib.error.HTTPError as e:
        err = e.read().decode("utf-8")
        return {"ok": False, "status": e.code, "error": err}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)}


def call_notion_api(payload: Dict[str, Any], limit: Optional[int] = None) -> bool:
    """调用 Notion API 逐条创建页面（支持限流与断点续传）。"""
    import time

    token = os.environ.get("NOTION_INTEGRATION_TOKEN") or os.environ.get("NOTION_TOKEN")
    database_id = os.environ.get("NOTION_DATABASE_ID")

    if not token:
        _log("未设置 NOTION_INTEGRATION_TOKEN 环境变量，无法调用真实 API", "ERROR")
        return False
    if not database_id:
        _log("未设置 NOTION_DATABASE_ID 环境变量，无法调用真实 API", "ERROR")
        return False

    records = payload["records"]
    if limit is not None:
        records = records[:limit]

    _log(f"准备向 Notion 数据库 {database_id} 同步 {len(records)} 条记录...", "SYNC")

    url = "https://api.notion.com/v1/pages"
    results: List[Dict[str, Any]] = []
    success = 0
    failed = 0

    for idx, record in enumerate(records, 1):
        page_payload = {
            "parent": {"database_id": database_id},
            "properties": record["properties"],
        }
        # 可选：添加外部ID到页面内容，方便后续查询/去重
        # page_payload["children"] = [...]

        result = _notion_post(url, token, page_payload)
        result["external_id"] = record.get("external_id")
        result["name"] = record.get("name")
        result["seq"] = idx
        results.append(result)

        if result["ok"]:
            success += 1
        else:
            failed += 1
            _log(f"[{idx}/{len(records)}] 失败 {record.get('external_id')}: {result.get('error', '')[:120]}", "ERROR")

        if idx % 10 == 0 or idx == len(records):
            _log(f"进度 {idx}/{len(records)} · 成功 {success} · 失败 {failed}", "OK" if failed == 0 else "WARN")

        # Notion 速率限制：保守 0.35s/请求 ≈ 2.86 req/s
        if idx < len(records):
            time.sleep(0.35)

    report = {
        "dna": DNA,
        "database_id": database_id,
        "generated_at": _now(),
        "total": len(records),
        "success": success,
        "failed": failed,
        "results": results,
    }
    report_path = OUTPUT_DIR / "notion_sync_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    _log(f"同步报告已保存: {report_path}", "OK")

    if failed == 0:
        _log(f"全部 {success} 条记录同步成功", "OK")
        return True
    else:
        _log(f"同步完成：成功 {success} / 失败 {failed}", "WARN")
        return False


def main():
    parser = argparse.ArgumentParser(description="龍魂 Notion 引擎状态同步器 v2.0")
    parser.add_argument("--registry", type=Path, default=REGISTRY_FILE,
                        help="输入注册表路径")
    parser.add_argument("--integrity", type=Path, default=INTEGRITY_FILE,
                        help="输入完整性报告路径")
    parser.add_argument("--dry-run", action="store_true", default=True,
                        help="默认开启：仅生成同步文件，不调用 Notion API")
    parser.add_argument("--execute", action="store_false", dest="dry_run",
                        help="尝试调用 Notion API（需要环境变量）")
    parser.add_argument("--limit", type=int, default=None,
                        help="限制同步记录数（用于测试）")
    args = parser.parse_args()

    print(f"\n{DNA}\n")

    if not args.registry.exists():
        _log(f"注册表不存在: {args.registry}", "ERROR")
        sys.exit(1)

    with open(args.registry, "r", encoding="utf-8") as f:
        registry = json.load(f)

    engines = registry.get("engines", [])
    if not engines:
        _log("注册表为空", "WARN")
        sys.exit(0)

    integrity_report = load_json(args.integrity)
    if not integrity_report:
        _log(f"未找到完整性报告: {args.integrity}，审计字段将使用默认值", "WARN")
    else:
        _log(f"已加载完整性报告: {len(integrity_report.get('results', []))} 条", "OK")

    # 加载 lh-ctl 运行日志摘要
    job_history_path = Path.home() / ".longhun" / "state" / "job_history.jsonl"
    runlog_index = build_runlog_index(job_history_path)
    if runlog_index:
        _log(f"已加载运行日志: {len(runlog_index)} 个引擎", "OK")

    integrity_index = build_integrity_index(integrity_report)
    payload = build_sync_payload(engines, integrity_index, runlog_index)

    print("\n📊 同步计划:")
    print(f"  记录总数: {payload['total_records']}")
    print(f"  目标数据库: 龍魂引擎注册表 v2")
    print(f"  Schema: {SCHEMA_FILE.name}")
    print(f"  模式: {'DRY-RUN' if args.dry_run else 'EXECUTE'}")
    print(f"\n📝 前 3 条记录预览:")
    for r in payload["records"][:3]:
        print(f"  - {r['external_id']}: {r['name']}")

    save_outputs(payload, integrity_index, runlog_index, args.dry_run)

    if not args.dry_run:
        success = call_notion_api(payload, limit=args.limit)
        if not success:
            _log("Notion API 调用未执行或失败", "WARN")
    else:
        _log("DRY-RUN 模式：已生成同步计划，未调用 Notion API", "OK")

    _log("完成", "OK")


if __name__ == "__main__":
    main()
