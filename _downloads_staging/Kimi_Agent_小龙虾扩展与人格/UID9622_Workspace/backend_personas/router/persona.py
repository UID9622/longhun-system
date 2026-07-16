#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
北辰·路由官 P-AK-ROUTER
功能：统一入口 → 关键词识别 → Agent / Skill / IPA 节点 路由决策
      把老大的一句话分发给正确的智能代理或技能，并留下 DNA 与审计。
DNA: #ROUTER-AGENT-CONFIG-20251214-001
"""
import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from core import AuditMark, DNATracer, Messenger, SecurityFilter, TelemetryCollector, TricolorAudit, load_config, setup_logging, workspace_root


PERSONA_CODE = "ROUTER"
PERSONA_NAME = "北辰·路由官 P-AK-ROUTER"
AGENT_DNA = "#ROUTER-AGENT-CONFIG-20251214-001"

CONFIG = load_config()
WORKSPACE = Path(CONFIG.get("workspace", workspace_root()))
LOG_FILE = Path(CONFIG.get("logs_dir", WORKSPACE / "logs")) / "router.log"
DEFAULT_REGISTRY = Path(__file__).parent / "registry.json"
DATA_DIR = WORKSPACE / "data" / "router"


def load_registry(path: Path) -> Dict[str, Any]:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {}


def save_registry(path: Path, data: Dict[str, Any]):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def score_keywords(text: str, keywords: List[str]) -> int:
    """简单关键词匹配打分，支持部分匹配。"""
    text = text.lower()
    score = 0
    for kw in keywords:
        kw = kw.lower()
        score += text.count(kw)
        # 全词匹配额外加分
        if re.search(r"\b" + re.escape(kw) + r"\b", text):
            score += 2
    return score


def route(text: str, registry: Dict[str, Any]) -> Tuple[str, Dict[str, Any], List[Dict[str, Any]]]:
    """
    返回 (target_type, target_entry, ranked_list)
    target_type: 'agent' | 'skill' | 'ipa_node' | 'default'
    """
    candidates = []
    for group in ["agents", "skills", "ipa_nodes"]:
        for entry in registry.get(group, []):
            keywords = entry.get("keywords", [])
            s = score_keywords(text, keywords)
            if s > 0:
                candidates.append({
                    "type": group.rstrip("s"),  # agent/skill/ipa_node
                    "group": group,
                    "score": s,
                    **entry,
                })
    candidates.sort(key=lambda x: x["score"], reverse=True)

    if candidates:
        winner = candidates[0]
        return winner["type"], winner, candidates

    default = registry.get("default", {"code": "BAOBAO", "name": "宝宝·构建师"})
    return "default", {"type": "default", "score": 0, **default}, candidates


def ensure_uid(uid: str) -> bool:
    return uid.endswith("9622")


def build_report(query: str, source: str, device: str, target_type: str, winner: Dict[str, Any], ranked: List[Dict[str, Any]], dna: str) -> Dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "query": SecurityFilter.sanitize(query),
        "source": source,
        "device": device,
        "routed_to_type": target_type,
        "routed_to": winner.get("name") or winner.get("id"),
        "code": winner.get("code") or winner.get("id"),
        "score": winner.get("score", 0),
        "ranked": [
            {
                "type": r.get("type"),
                "name": r.get("name") or r.get("id"),
                "code": r.get("code") or r.get("id"),
                "score": r.get("score", 0),
            }
            for r in ranked[:5]
        ],
        "dna": dna,
    }


def scan_skill_directories() -> List[Dict[str, Any]]:
    """
    扫描已安装技能目录，生成技能注册表条目。
    技能目录：~/.kimi-code/skills / ~/.agents/skills
    """
    roots = [
        Path.home() / ".kimi-code" / "skills",
        Path.home() / ".agents" / "skills",
    ]
    skills = []
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        for skill_dir in root.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            skill_id = skill_dir.name
            if skill_id in seen:
                continue
            seen.add(skill_id)
            text = skill_md.read_text(encoding="utf-8", errors="ignore")
            lines = [l.strip() for l in text.splitlines() if l.strip()]
            name = skill_id
            when_keywords = []
            # 第一行非注释标题作为名字
            if lines:
                first = lines[0]
                if first.startswith("#"):
                    name = first.lstrip("#").strip().split("—")[0].split("-")[0].strip()
            # 提取 WHEN: 后面的关键词
            for line in lines[:20]:
                m = re.search(r"WHEN[:：]\s*(.+)", line, re.I)
                if m:
                    when_text = m.group(1)
                    # 分割关键词
                    kws = [k.strip(",. ·｜|/、") for k in re.split(r"[,，/|｜、]", when_text) if k.strip()]
                    when_keywords.extend(kws)
                    break
            # 如果没提取到，用技能 id 拆词兜底
            if not when_keywords:
                when_keywords = [skill_id.replace("longhun-", "").replace("-", " ")]
            skills.append({
                "id": skill_id,
                "name": name,
                "path": str(skill_md),
                "keywords": when_keywords[:12],
            })
    return skills


def cmd_scan(registry_path: Path, logger):
    logger.info(AuditMark.tag(AuditMark.BLUE, PERSONA_NAME, "开始扫描本地技能目录"))
    registry = load_registry(registry_path)
    skills = scan_skill_directories()
    registry["skills"] = skills
    registry.setdefault("default", {"code": "BAOBAO", "name": "宝宝·构建师"})
    save_registry(registry_path, registry)
    logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, f"技能注册表已更新：{len(skills)} 个技能"))
    return skills


def main():
    parser = argparse.ArgumentParser(description=PERSONA_NAME)
    parser.add_argument("--query", "-q", required=False, help="要路由的输入文本")
    parser.add_argument("--source", default="cli", help="来源平台 (cli/notion/web)")
    parser.add_argument("--device", default="MacBook", help="来源设备")
    parser.add_argument("--uid", default="UID9622", help="用户身份标识")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="路由注册表路径")
    parser.add_argument("--dispatch", action="store_true", help="向目标 Agent 邮箱发送路由消息")
    parser.add_argument("--report", action="store_true", help="生成 JSON 路由报告")
    parser.add_argument("--scan-skills", action="store_true", help="扫描技能目录并更新注册表")
    parser.add_argument("--verbose", action="store_true", help="详细日志")
    args = parser.parse_args()

    logger = setup_logging("router", LOG_FILE, verbose=args.verbose)
    dna = DNATracer(PERSONA_CODE, AGENT_DNA)
    audit = TricolorAudit(Path(CONFIG.get("audit_dir", WORKSPACE / "logs" / "audit")))

    registry_path = Path(args.registry)

    if args.scan_skills:
        with TelemetryCollector(PERSONA_CODE, PERSONA_NAME, operation_type="SCAN_SKILLS", source=args.source, device=args.device) as telemetry:
            skills = cmd_scan(registry_path, logger)
            telemetry.set_metrics({"skills_scanned": len(skills)})
        return

    if not args.query:
        parser.print_help()
        return

    with TelemetryCollector(PERSONA_CODE, PERSONA_NAME, operation_type="ROUTE", source=args.source, device=args.device, query=args.query) as telemetry:
        if not ensure_uid(args.uid):
            msg = f"UID 不匹配：{args.uid}，拒绝路由"
            logger.error(AuditMark.tag(AuditMark.RED, PERSONA_NAME, msg))
            audit.red(PERSONA_NAME, "UID拒绝", {"uid": args.uid, "query": SecurityFilter.sanitize(args.query)})
            telemetry.finish("error", {"reason": "uid_mismatch"})
            sys.exit(1)

        query = args.query
        registry = load_registry(registry_path)
        # 缺省注册表兜底
        if not registry.get("agents"):
            registry["agents"] = [
                {"code": "WENWEN", "name": "雯雯·技术整理师", "keywords": ["整理", "分类", "归档", "去重", "文档", "笔记", "扫描", "索引"]},
                {"code": "SCOUT", "name": "侦察兵·信息猎手", "keywords": ["搜索", "收集", "情报", "监控", "发现", "巡逻", "抓取", "rss"]},
                {"code": "GUARDIAN", "name": "上帝之眼·守护者", "keywords": ["安全", "审计", "检查", "守护", "风险", "熔断", "权限", "合规", "审查"]},
                {"code": "BAOBAO", "name": "宝宝·构建师", "keywords": ["构建", "搭建", "生成", "项目", "代码", "脚本", "创建", "写文件", "makefile", "部署"]},
                {"code": "WENXIN", "name": "文心·同步专家", "keywords": ["同步", "备份", "复制", "镜像", "增量", "全量", "冲突", "一致性", "回滚"]},
                {"code": "ROUTER", "name": "北辰·路由官", "keywords": ["路由", "分发", "调度", "选择", "哪个", "应该找谁", "匹配"]},
            ]
        registry.setdefault("default", {"code": "BAOBAO", "name": "宝宝·构建师"})

        target_type, winner, ranked = route(query, registry)
        route_dna = dna.generate("ROUTE")

        target_code = winner.get("code") or winner.get("id") or registry["default"]["code"]
        target_name = winner.get("name") or winner.get("id") or registry["default"]["name"]

        logger.info(AuditMark.tag(
            AuditMark.GREEN if target_type != "default" else AuditMark.YELLOW,
            PERSONA_NAME,
            f"[{target_type.upper()}] {target_name} (score={winner.get('score', 0)})",
        ))
        audit.green(PERSONA_NAME, "路由决策", {
            "query": SecurityFilter.sanitize(query),
            "target_type": target_type,
            "target_code": target_code,
            "target_name": target_name,
            "score": winner.get("score", 0),
            "dna": route_dna,
        })

        telemetry.route(target_type, target_code, target_name, winner.get("score", 0), query=SecurityFilter.sanitize(query), dna=route_dna)
        telemetry.set_metrics({
            "matched": target_type != "default",
            "score": winner.get("score", 0),
            "candidates": len(ranked),
        })

        if args.dispatch:
            messenger = Messenger(Path(CONFIG.get("mailbox", WORKSPACE / "mailbox")))
            msg_id = messenger.send(
                sender=PERSONA_CODE,
                recipient=target_code,
                event="ROUTE",
                payload={
                    "query": SecurityFilter.sanitize(query),
                    "source": args.source,
                    "device": args.device,
                    "routed_by": PERSONA_NAME,
                    "dna": route_dna,
                },
            )
            logger.info(AuditMark.tag(AuditMark.BLUE, PERSONA_NAME, f"已派发消息 {msg_id} -> {target_code}"))

        report = build_report(query, args.source, args.device, target_type, winner, ranked, route_dna)
        if args.report:
            DATA_DIR.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            report_path = DATA_DIR / f"route_report_{ts}.json"
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.info(AuditMark.tag(AuditMark.GREEN, PERSONA_NAME, f"报告已保存: {report_path}"))

        # 控制台输出简洁结果，方便其他脚本调用
        print(json.dumps({
            "target_type": target_type,
            "target_code": target_code,
            "target_name": target_name,
            "score": winner.get("score", 0),
            "dna": route_dna,
        }, ensure_ascii=False))


if __name__ == "__main__":
    main()
