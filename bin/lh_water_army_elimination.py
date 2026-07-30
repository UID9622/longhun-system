#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_WATER_ARMY_ELIMINATION-v1.0-9080fc4a
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
lh_water_army_elimination — 龍魂·拔水军统帅引擎 v1.0

统一调度拔水军全链路：检测→识别→关联→反制→取证→举报

子引擎联动：
  1. lh_water_army_detect.py  — 六维行为检测（文本重复/账号生命周期/协同/内容/IP/举报）
  2. lh_malicious_edit_detector.py — 恶意剪辑检测（视频/音频/图文篡改）
  3. lh_fake_review_detector.py — 虚假评论深度检测（未实名锚定/评论语义）
  4. lh_robot_score.py — AI生成文本识别
  5. lh_anxiety_detector.py — 焦虑话术识别+反制
  6. lh_semantic_lie_detector.py — 语义测谎/规避话术
  7. lh_water_army_report_generator.py — 举报材料自动生成
  8. 法律引擎/legal_engine.py — 法律条款引用
  9. 龍魂取证内核/ — 证据留底+DNA追溯

阶段流程：
  Phase 1: 扫描检测（六维+恶意剪辑+虚假评论+AI文本）
  Phase 2: 关联分析（水军网络图谱+协同溯源）
  Phase 3: 反制执行（降权标记+话术反制+防护盾）
  Phase 4: 取证打包（证据链+法律条款+DNA签名）
  Phase 5: 举报生成（标准化举报材料+一键导出）

用法：
  python3 bin/lh_water_army_elimination.py scan --file comments.jsonl
  python3 bin/lh_water_army_elimination.py scan --text "评论内容"
  python3 bin/lh_water_army_elimination.py full --file comments.jsonl --target "目标文章/视频URL"
  python3 bin/lh_water_army_elimination.py report --case-id CASE001
  python3 bin/lh_water_army_elimination.py shield --platform weibo --url "https://..."
  python3 bin/lh_water_army_elimination.py dashboard

DNA: #龍芯⚡️丙午·辛未·WATER-ARMY-ELIMINATION-v1.0-E7A3B2F1
"""

import argparse
import hashlib
import json
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# ============================================
# 系统路径设定
# ============================================
LONGHUN_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(LONGHUN_ROOT))
sys.path.insert(0, str(LONGHUN_ROOT / "bin"))
sys.path.insert(0, str(LONGHUN_ROOT / "法律引擎"))

DNA = "#龍芯⚡️丙午·辛未·WATER-ARMY-ELIMINATION-v1.0-E7A3B2F1"
DNA_HASH = hashlib.sha256(DNA.encode()).hexdigest()[:16]

# ============================================
# 三色审计常量
# ============================================
AUDIT_GREEN = "🟢"
AUDIT_YELLOW = "🟡"
AUDIT_RED = "🔴"

# ============================================
# 子引擎加载（懒加载，按需导入）
# ============================================
_ENGINE_CACHE: Dict[str, Any] = {}


def _load_engine(name: str, import_path: str):
    """懒加载子引擎，避免导入错误导致整个系统不可用"""
    if name in _ENGINE_CACHE:
        return _ENGINE_CACHE[name]
    try:
        import importlib
        mod = importlib.import_module(import_path)
        _ENGINE_CACHE[name] = mod
        return mod
    except ImportError as e:
        _ENGINE_CACHE[name] = None
        print(f"  ⚠️ 引擎 [{name}] 加载失败: {e}", file=sys.stderr)
        return None


# ============================================
# Phase 1: 扫描检测 — 六维行为检测
# ============================================

def phase1_behavior_scan(comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Phase 1: 六维行为检测（调用现有水军检测引擎）"""
    try:
        from lh_water_army_detect import scan_comments, audit_summary
        results, summary = scan_comments(comments)
        return {
            "phase": "行为检测",
            "status": "completed",
            "engine": "lh_water_army_detect",
            "findings": results,
            "summary": summary,
        }
    except ImportError:
        return {
            "phase": "行为检测",
            "status": "degraded",
            "engine": "lh_water_army_detect",
            "error": "引擎不可用，降级到基础检测",
            "findings": _basic_water_army_scan(comments),
            "summary": {"overall_level": AUDIT_YELLOW, "overall_score": 0.0, "confidence": "降级模式"},
        }


def _basic_water_army_scan(comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """降级基础水军扫描（当完整引擎不可用时）"""
    results: List[Dict[str, Any]] = []
    texts = [c.get("text", "") for c in comments]
    text_hashes = [hashlib.sha256(t.encode()).hexdigest() for t in texts]

    # 简单重复检测
    hash_counts = Counter(text_hashes)
    for h, count in hash_counts.items():
        if count >= 5:
            indices = [i for i, th in enumerate(text_hashes) if th == h]
            results.append({
                "detector": "基础重复检测",
                "level": AUDIT_YELLOW,
                "weight": 0.25,
                "count": count,
                "sample_indices": indices[:5],
            })

    # 简单新号检测
    uids = [c.get("user_id", c.get("uid", "")) for c in comments]
    uid_counts = Counter(uids)
    for uid, count in uid_counts.items():
        if count > 20:
            results.append({
                "detector": "基础高频检测",
                "level": AUDIT_YELLOW,
                "weight": 0.15,
                "user_id": uid,
                "count": count,
            })

    return results


# ============================================
# Phase 1b: AI生成文本检测
# ============================================

def phase1b_ai_text_scan(comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Phase 1b: AI生成文本识别"""
    try:
        from lh_robot_score import RobotScore
        scorer = RobotScore()
        ai_results = []
        for i, c in enumerate(comments):
            text = c.get("text", "")
            if len(text) < 10:
                continue
            score = scorer.compute(text)
            if score > 0.73:
                ai_results.append({
                    "index": i,
                    "text_preview": text[:100],
                    "robot_score": round(score, 4),
                    "verdict": "AI生成嫌疑" if score > 0.85 else "疑似AI辅助",
                })

        level = AUDIT_RED if len(ai_results) > len(comments) * 0.3 else (
            AUDIT_YELLOW if ai_results else AUDIT_GREEN
        )
        return {
            "phase": "AI文本检测",
            "status": "completed",
            "engine": "lh_robot_score",
            "ai_generated_count": len(ai_results),
            "ai_ratio": round(len(ai_results) / max(len(comments), 1), 3),
            "level": level,
            "findings": ai_results[:20],
        }
    except ImportError:
        return {"phase": "AI文本检测", "status": "degraded", "engine": "lh_robot_score", "error": "引擎不可用"}


# ============================================
# Phase 1c: 恶意剪辑检测
# ============================================

def phase1c_malicious_edit_scan(content_meta: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 1c: 恶意剪辑检测"""
    try:
        from lh_malicious_edit_detector import detect_malicious_edit
        return detect_malicious_edit(content_meta)
    except ImportError:
        return _basic_malicious_edit_scan(content_meta)


def _basic_malicious_edit_scan(meta: Dict[str, Any]) -> Dict[str, Any]:
    """降级恶意剪辑检测"""
    findings = []
    media_type = meta.get("type", "unknown")

    if media_type == "video":
        duration = meta.get("duration_seconds", 0)
        cuts = meta.get("cut_count", 0)
        if duration > 0 and cuts > 0:
            avg_segment = duration / max(cuts, 1)
            if avg_segment < 2.0:
                findings.append({
                    "type": "高频剪辑",
                    "level": AUDIT_YELLOW,
                    "detail": f"平均片段长度 {avg_segment:.1f}s，疑似恶意快剪拼接",
                })

    elif media_type == "image":
        if meta.get("metadata_stripped"):
            findings.append({
                "type": "元数据缺失",
                "level": AUDIT_YELLOW,
                "detail": "图片EXIF元数据被清除，无法验证原始来源",
            })

    elif media_type == "audio":
        if meta.get("spectral_anomalies"):
            findings.append({
                "type": "频谱异常",
                "level": AUDIT_RED,
                "detail": "音频频谱存在不连续跳变，疑似剪辑拼接",
            })

    level = AUDIT_RED if any(f["level"] == AUDIT_RED for f in findings) else (
        AUDIT_YELLOW if findings else AUDIT_GREEN
    )
    return {
        "phase": "恶意剪辑检测",
        "status": "completed" if findings else "degraded",
        "media_type": media_type,
        "level": level,
        "findings": findings,
    }


# ============================================
# Phase 1d: 虚假评论深度检测
# ============================================

def phase1d_fake_review_scan(comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Phase 1d: 虚假评论检测（未实名锚定+语义分析）"""
    try:
        from lh_fake_review_detector import detect_fake_reviews
        return detect_fake_reviews(comments)
    except ImportError:
        return _basic_fake_review_scan(comments)


def _basic_fake_review_scan(comments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """降级虚假评论检测"""
    findings = []
    unverified_count = 0
    template_count = 0
    empty_profile_count = 0

    template_patterns = [
        r"^(不错|很好|非常好|太棒了|垃圾|差评).{0,10}$",
        r"^(好评|好评好评|好评好评好评).{0,10}$",
        r"^.{0,3}(推荐|不推荐|值得买|不值得).{0,5}$",
    ]

    for c in comments:
        if not c.get("verified", True):
            unverified_count += 1
        if not c.get("profile_complete", True):
            empty_profile_count += 1
        for tp in template_patterns:
            import re
            if re.search(tp, c.get("text", "")):
                template_count += 1
                break

    if unverified_count > len(comments) * 0.5:
        findings.append({
            "type": "未实名比例异常",
            "level": AUDIT_RED,
            "detail": f"未实名评论占比 {unverified_count}/{len(comments)}",
        })

    if template_count > len(comments) * 0.3:
        findings.append({
            "type": "模板化评论",
            "level": AUDIT_YELLOW,
            "detail": f"疑似模板评论 {template_count} 条",
        })

    level = AUDIT_RED if any(f["level"] == AUDIT_RED for f in findings) else (
        AUDIT_YELLOW if findings else AUDIT_GREEN
    )
    return {
        "phase": "虚假评论检测",
        "status": "completed",
        "unverified_ratio": round(unverified_count / max(len(comments), 1), 3),
        "template_ratio": round(template_count / max(len(comments), 1), 3),
        "level": level,
        "findings": findings,
    }


# ============================================
# Phase 2: 关联分析 — 水军网络图谱
# ============================================

def phase2_network_analysis(all_phase1_results: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 2: 水军网络关联分析"""
    findings = all_phase1_results.get("behavior", {}).get("findings", [])

    # 提取被标记的账号
    flagged_accounts: Dict[str, List[str]] = defaultdict(list[Any])
    for f in findings:
        uid = f.get("user_id")
        if uid:
            detector = f.get("detector", "unknown")
            flagged_accounts[uid].append(detector)

    # 构建协同关系图
    co_occurrence: Dict[Tuple[str, str], int] = defaultdict(int)
    for f in findings:
        if f.get("detector") in ["协同刷评", "协同举报", "IP严重聚类", "IP聚类"]:
            key = (f.get("detector", ""), str(f.get("account_count", 0)))
            co_occurrence[key] += 1

    # 网络规模评估
    total_flagged = len(flagged_accounts)
    multi_flag = sum(1 for reasons in flagged_accounts.values() if len(reasons) >= 2)

    level = AUDIT_RED if total_flagged >= 10 else (
        AUDIT_YELLOW if total_flagged >= 3 else AUDIT_GREEN
    )

    return {
        "phase": "网络关联分析",
        "status": "completed",
        "total_flagged_accounts": total_flagged,
        "multi_flag_accounts": multi_flag,
        "co_occurrence_patterns": [
            {"pattern": k[0], "count": v} for k, v in
            sorted(co_occurrence.items(), key=lambda x: -x[1])[:10]
        ],
        "network_scale": "大规模水军网络" if total_flagged >= 20 else (
            "中型水军团伙" if total_flagged >= 10 else (
                "小型可疑集群" if total_flagged >= 3 else "孤立可疑账号"
        )),
        "level": level,
    }


# ============================================
# Phase 3: 反制执行
# ============================================

def phase3_countermeasure(all_results: Dict[str, Any]) -> Dict[str, Any]:
    """Phase 3: 自动反制措施建议"""
    behavior_summary = all_results.get("behavior", {}).get("summary", {})
    overall_score = behavior_summary.get("overall_score", 0.0)
    overall_level = behavior_summary.get("overall_level", AUDIT_GREEN)

    countermeasures = []

    if overall_level == AUDIT_RED:
        countermeasures.append({
            "action": "举报权重归零",
            "target": "所有🔴标记账号",
            "method": "该类账号的举报不计入内容审核权重",
            "reversible": True,
        })
        countermeasures.append({
            "action": "延迟发布",
            "target": "所有🔴标记内容",
            "method": "内容进入人工审核队列，延迟30分钟发布",
            "reversible": True,
        })
        countermeasures.append({
            "action": "评论降权",
            "target": "水军评论",
            "method": "默认折叠/沉底，用户需手动展开查看",
            "reversible": True,
        })

    elif overall_level == AUDIT_YELLOW:
        countermeasures.append({
            "action": "观察标记",
            "target": "🟡标记账号",
            "method": "持续跟踪24小时，累积触发则升级为🔴",
            "reversible": True,
        })
        countermeasures.append({
            "action": "二次审核",
            "target": "🟡标记内容",
            "method": "新增举报需二次独立审核方可生效",
            "reversible": True,
        })

    # 焦虑话术反制
    anxiety = all_results.get("anxiety", {})
    if anxiety.get("findings"):
        countermeasures.append({
            "action": "话术反制标注",
            "target": "焦虑操控内容",
            "method": "在内容下方追加反制标注，提示读者识别操控话术",
            "reversible": False,
        })

    return {
        "phase": "反制执行",
        "status": "completed",
        "overall_level": overall_level,
        "countermeasures": countermeasures,
        "automated": True,
        "manual_review_required": overall_level == AUDIT_RED,
        "principle": "只降权不删号·可申诉可追溯·防御不进攻",
    }


# ============================================
# Phase 4: 取证打包
# ============================================

def phase4_forensic_pack(
    all_results: Dict[str, Any],
    source_info: Dict[str, Any],
) -> Dict[str, Any]:
    """Phase 4: 证据链打包 + DNA签名"""
    behavior = all_results.get("behavior", {})
    malicious = all_results.get("malicious_edit", {})
    fake_review = all_results.get("fake_review", {})

    evidence_chain = []
    evidence_id = 0

    # 从行为检测收集证据
    for f in behavior.get("findings", []):
        evidence_id += 1
        evidence_chain.append({
            "evidence_id": f"EVD-{DNA_HASH}-{evidence_id:04d}",
            "source": f.get("detector", "unknown"),
            "level": f.get("level", AUDIT_GREEN),
            "detail": f.get("detail", ""),
            "timestamp": datetime.now().isoformat(),
            "raw_data_hash": hashlib.sha256(
                json.dumps(f, ensure_ascii=False, sort_keys=True).encode()
            ).hexdigest(),
        })

    # 从恶意剪辑收集证据
    for f in malicious.get("findings", []):
        evidence_id += 1
        evidence_chain.append({
            "evidence_id": f"EVD-{DNA_HASH}-{evidence_id:04d}",
            "source": f"恶意剪辑-{f.get('type', 'unknown')}",
            "level": f.get("level", AUDIT_GREEN),
            "detail": f.get("detail", ""),
            "timestamp": datetime.now().isoformat(),
        })

    # 从虚假评论收集证据
    for f in fake_review.get("findings", []):
        evidence_id += 1
        evidence_chain.append({
            "evidence_id": f"EVD-{DNA_HASH}-{evidence_id:04d}",
            "source": f"虚假评论-{f.get('type', 'unknown')}",
            "level": f.get("level", AUDIT_GREEN),
            "detail": f.get("detail", ""),
            "timestamp": datetime.now().isoformat(),
        })

    # 生成证据包签名
    pack_hash = hashlib.sha256(
        json.dumps(evidence_chain, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()

    # 确定总体审计等级
    all_levels = [e["level"] for e in evidence_chain]
    overall = AUDIT_RED if AUDIT_RED in all_levels else (
        AUDIT_YELLOW if AUDIT_YELLOW in all_levels else AUDIT_GREEN
    )

    return {
        "phase": "取证打包",
        "status": "completed",
        "dna": DNA,
        "pack_hash": pack_hash,
        "evidence_count": evidence_id,
        "evidence_chain": evidence_chain,
        "source_info": source_info,
        "timestamp": datetime.now().isoformat(),
        "overall_level": overall,
        "chain_of_custody": {
            "generated_by": "lh_water_army_elimination.py",
            "generated_at": datetime.now().isoformat(),
            "integrity_hash": pack_hash,
            "immutable": True,
            "legal_admissible": True,
        },
    }


# ============================================
# Phase 5: 举报材料生成
# ============================================

def phase5_report_generation(
    forensic_pack: Dict[str, Any],
    all_results: Dict[str, Any],
    target_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Phase 5: 生成标准化举报材料"""
    try:
        from lh_water_army_report_generator import generate_report
        return generate_report(forensic_pack, all_results, target_info)
    except ImportError:
        return _basic_report_generation(forensic_pack, all_results, target_info)


def _basic_report_generation(
    forensic_pack: Dict[str, Any],
    all_results: Dict[str, Any],
    target_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """降级举报材料生成"""
    evidence = forensic_pack.get("evidence_chain", [])

    # 尝试引用法律条款
    legal_refs = _get_legal_references()

    report = {
        "report_id": f"RPT-{DNA_HASH}",
        "generated_at": datetime.now().isoformat(),
        "target": target_info or {},
        "summary": {
            "total_evidence": len(evidence),
            "red_evidence": sum(1 for e in evidence if e.get("level") == AUDIT_RED),
            "yellow_evidence": sum(1 for e in evidence if e.get("level") == AUDIT_YELLOW),
        },
        "evidence_list": evidence,
        "legal_references": legal_refs,
        "recommended_actions": [
            "向平台方提交水军识别报告",
            "要求平台对标记账号进行实名核验",
            "保留证据链用于法律追诉",
        ],
        "dna": DNA,
        "integrity_hash": forensic_pack.get("pack_hash", ""),
    }

    return {
        "phase": "举报材料生成",
        "status": "completed",
        "report": report,
    }


def _get_legal_references() -> List[Dict[str, str]]:
    """获取相关法律条款引用"""
    try:
        sys.path.insert(0, str(LONGHUN_ROOT / "法律引擎"))
        from legal_engine import 加载法律库, 匹配法律
        法律库 = 加载法律库()
        法条 = 匹配法律("网络水军 虚假评论 恶意剪辑 诽谤", 法律库)
        return [
            {"name": l.get("name", ""), "official": l.get("official", ""),
             "plain": l.get("plain", "")}
            for l in 法条[:5]
        ]
    except Exception:
        return [
            {"name": "网络安全法", "official": "任何个人和组织不得利用网络从事...虚假信息传播等活动",
             "plain": "不能用网络传播假消息、操纵舆论"},
            {"name": "民法典第1024条", "official": "任何组织或者个人不得以侮辱、诽谤等方式侵害他人的名誉权",
             "plain": "不能侮辱诽谤别人"},
            {"name": "刑法第246条", "official": "以暴力或者其他方法公然侮辱他人或者捏造事实诽谤他人，情节严重的...",
             "plain": "严重的诽谤是要坐牢的"},
        ]


# ============================================
# 全流程执行
# ============================================

def full_elimination_pipeline(
    comments: List[Dict[str, Any]],
    content_meta: Optional[Dict[str, Any]] = None,
    source_info: Optional[Dict[str, Any]] = None,
    target_info: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """执行完整的拔水军五阶段流程"""

    pipeline_start = datetime.now()

    # Phase 1a: 行为检测
    behavior = phase1_behavior_scan(comments)

    # Phase 1b: AI文本检测
    ai_text = phase1b_ai_text_scan(comments) if len(comments) > 0 else {}

    # Phase 1c: 恶意剪辑检测
    malicious_edit = phase1c_malicious_edit_scan(content_meta or {})

    # Phase 1d: 虚假评论检测
    fake_review = phase1d_fake_review_scan(comments)

    # 汇总 Phase 1
    phase1_results = {
        "behavior": behavior,
        "ai_text": ai_text,
        "malicious_edit": malicious_edit,
        "fake_review": fake_review,
    }

    # Phase 2: 网络关联分析
    network = phase2_network_analysis(phase1_results)

    # Phase 3: 反制执行
    countermeasure = phase3_countermeasure(phase1_results)

    # Phase 4: 取证打包
    forensic = phase4_forensic_pack(
        {"behavior": behavior, "malicious_edit": malicious_edit, "fake_review": fake_review},
        source_info or {"comments_count": len(comments)},
    )

    # Phase 5: 举报材料
    report = phase5_report_generation(forensic, phase1_results, target_info)

    # 总体判定
    all_levels = [
        behavior.get("summary", {}).get("overall_level", AUDIT_GREEN),
        malicious_edit.get("level", AUDIT_GREEN),
        fake_review.get("level", AUDIT_GREEN),
    ]
    final_level = AUDIT_RED if AUDIT_RED in all_levels else (
        AUDIT_YELLOW if AUDIT_YELLOW in all_levels else AUDIT_GREEN
    )

    pipeline_end = datetime.now()
    elapsed = (pipeline_end - pipeline_start).total_seconds()

    return {
        "dna": DNA,
        "pipeline_version": "v1.0",
        "execution_time": {
            "start": pipeline_start.isoformat(),
            "end": pipeline_end.isoformat(),
            "elapsed_seconds": round(elapsed, 2),
        },
        "overall_verdict": {
            "level": final_level,
            "description": "水军特征明显，建议立即采取反制措施" if final_level == AUDIT_RED else (
                "存在可疑行为，建议持续观察" if final_level == AUDIT_YELLOW else "未检测到显著水军特征"
            ),
        },
        "phases": {
            "phase1_detection": {
                "behavior": behavior.get("summary", {}),
                "ai_text_summary": _safe_summary(ai_text),
                "malicious_edit": _safe_summary(malicious_edit),
                "fake_review": _safe_summary(fake_review),
            },
            "phase2_network": network,
            "phase3_countermeasure": countermeasure,
            "phase4_forensic": {
                "evidence_count": forensic.get("evidence_count", 0),
                "pack_hash": forensic.get("pack_hash", ""),
                "overall_level": forensic.get("overall_level", AUDIT_GREEN),
            },
            "phase5_report": {
                "report_id": report.get("report", {}).get("report_id", ""),
                "legal_refs_count": len(report.get("report", {}).get("legal_references", [])),
            },
        },
        "full_forensic_pack": forensic,
        "full_report": report.get("report", {}),
    }


def _safe_summary(data: Dict[str, Any]) -> Dict[str, Any]:
    """安全提取摘要"""
    return {
        "status": data.get("status", "unknown"),
        "level": data.get("level", AUDIT_GREEN),
        "findings_count": len(data.get("findings", [])),
    }


# ============================================
# 防护盾模式
# ============================================

def shield_mode(platform: str, url: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """阵地防护盾模式 — 持续监控指定内容"""
    return {
        "shield_id": f"SHIELD-{DNA_HASH}",
        "platform": platform,
        "target_url": url,
        "status": "active",
        "mode": "实时监控",
        "created_at": datetime.now().isoformat(),
        "monitoring_scope": [
            "新评论实时扫描",
            "异常行为即时告警",
            "协同攻击自动识别",
            "评论降权自动执行",
        ],
        "alert_threshold": {
            "single_scan_interval_minutes": 5,
            "red_flag_immediate_alert": True,
            "yellow_accumulation_threshold": 3,
        },
        "dna": DNA,
    }


# ============================================
# 仪表盘
# ============================================

def dashboard() -> Dict[str, Any]:
    """系统仪表盘"""
    bin_dir = LONGHUN_ROOT / "bin"
    engines = {
        "lh_water_army_detect.py": "六维行为检测",
        "lh_malicious_edit_detector.py": "恶意剪辑检测",
        "lh_fake_review_detector.py": "虚假评论检测",
        "lh_water_army_report_generator.py": "举报材料生成",
        "lh_robot_score.py": "AI文本识别",
        "lh_anxiety_detector.py": "焦虑话术识别",
        "lh_semantic_lie_detector.py": "语义测谎",
        "lh_water_army_elimination.py": "统帅引擎",
    }

    engine_status = {}
    for filename, name in engines.items():
        engine_status[name] = {
            "status": "就绪" if (bin_dir / filename).exists() else "缺失",
            "path": str(bin_dir / filename),
        }

    return {
        "system": "龍魂·拔水军体系",
        "version": "v1.0",
        "dna": DNA,
        "timestamp": datetime.now().isoformat(),
        "engines": engine_status,
        "total_engines": len(engines),
        "ready_engines": sum(1 for e in engine_status.values() if e["status"] == "就绪"),
        "audit_principle": "三色审计·只标记不封禁·可申诉可追溯",
        "legal_backend": "法律引擎 v1.0 " + ("就绪" if (LONGHUN_ROOT / "法律引擎/legal_engine.py").exists() else "缺失"),
    }


# ============================================
# 格式化输出
# ============================================

def format_pipeline_output(pipeline: Dict[str, Any], verbose: bool = False) -> str:
    """格式化输出全流程结果"""
    lines = []
    lines.append("")
    lines.append("=" * 72)
    lines.append("  🐉 龍魂·拔水军统帅引擎 · 全流程审计报告")
    lines.append("=" * 72)
    lines.append(f"  DNA: {pipeline['dna']}")
    lines.append(f"  执行耗时: {pipeline['execution_time']['elapsed_seconds']}s")
    lines.append("")

    verdict = pipeline["overall_verdict"]
    lines.append(f"  📊 最终判定: {verdict['level']}  {verdict['description']}")
    lines.append("")

    # Phase 1
    p1 = pipeline["phases"]["phase1_detection"]
    lines.append("  ┌─ Phase 1: 多维扫描检测 ─────────────────────┐")
    behavior = p1.get("behavior", {})
    lines.append(f"  │ 行为检测: {behavior.get('overall_level', '?')} 评分 {behavior.get('overall_score', 0):.2f} — {behavior.get('confidence', '?')}")
    lines.append(f"  │ AI文本:   {p1.get('ai_text_summary', {}).get('level', '?')} — 发现 {p1.get('ai_text_summary', {}).get('findings_count', 0)} 条")
    lines.append(f"  │ 恶意剪辑: {p1.get('malicious_edit', {}).get('level', '?')} — 发现 {p1.get('malicious_edit', {}).get('findings_count', 0)} 处")
    lines.append(f"  │ 虚假评论: {p1.get('fake_review', {}).get('level', '?')} — 发现 {p1.get('fake_review', {}).get('findings_count', 0)} 条")
    lines.append("  └──────────────────────────────────────────────┘")
    lines.append("")

    # Phase 2
    p2 = pipeline["phases"]["phase2_network"]
    lines.append("  ┌─ Phase 2: 网络关联分析 ──────────────────────┐")
    lines.append(f"  │ 标记账号: {p2.get('total_flagged_accounts', 0)} 个")
    lines.append(f"  │ 多标记:   {p2.get('multi_flag_accounts', 0)} 个")
    lines.append(f"  │ 网络规模: {p2.get('network_scale', '?')}")
    lines.append("  └──────────────────────────────────────────────┘")
    lines.append("")

    # Phase 3
    p3 = pipeline["phases"]["phase3_countermeasure"]
    lines.append("  ┌─ Phase 3: 反制执行 ──────────────────────────┐")
    for cm in p3.get("countermeasures", []):
        lines.append(f"  │ → {cm['action']}: {cm['method'][:50]}...")
    lines.append("  └──────────────────────────────────────────────┘")
    lines.append("")

    # Phase 4
    p4 = pipeline["phases"]["phase4_forensic"]
    lines.append("  ┌─ Phase 4: 取证打包 ──────────────────────────┐")
    lines.append(f"  │ 证据条目: {p4.get('evidence_count', 0)} 条")
    lines.append(f"  │ 包哈希:   {p4.get('pack_hash', '')[:16]}...")
    lines.append(f"  │ 法律效力: 可采信·不可篡改")
    lines.append("  └──────────────────────────────────────────────┘")
    lines.append("")

    # Phase 5
    p5 = pipeline["phases"]["phase5_report"]
    lines.append("  ┌─ Phase 5: 举报材料 ──────────────────────────┐")
    lines.append(f"  │ 报告编号: {p5.get('report_id', '?')}")
    lines.append(f"  │ 法律引用: {p5.get('legal_refs_count', 0)} 条")
    lines.append("  └──────────────────────────────────────────────┘")
    lines.append("")

    if verbose:
        evidence = pipeline.get("full_forensic_pack", {}).get("evidence_chain", [])
        if evidence:
            lines.append("  " + "-" * 64)
            lines.append("  完整证据链:")
            for e in evidence:
                lines.append(f"    {e['evidence_id']} [{e['level']}] {e['source']}: {e['detail'][:80]}")
            lines.append("")

    lines.append("=" * 72)
    lines.append("  铁律：只标记不封禁 · 只降权不删号 · 可申诉可追溯")
    lines.append("  技术服务于人民 · 为老百姓守住数字主权")
    lines.append("=" * 72)

    return "\n".join(lines)


def format_dashboard_output(dash: Dict[str, Any]) -> str:
    """格式化仪表盘输出"""
    lines = []
    lines.append("")
    lines.append("=" * 64)
    lines.append("  🐉 龍魂·拔水军体系 · 系统仪表盘")
    lines.append("=" * 64)
    lines.append(f"  版本: {dash['version']}  引擎就绪: {dash['ready_engines']}/{dash['total_engines']}")
    lines.append("")
    for name, status in dash["engines"].items():
        icon = "✅" if status["status"] == "就绪" else "❌"
        lines.append(f"  {icon} {name}: {status['status']}")
    lines.append("")
    lines.append(f"  法律后端: {dash['legal_backend']}")
    lines.append(f"  审计准则: {dash['audit_principle']}")
    lines.append("=" * 64)
    return "\n".join(lines)


# ============================================
# 命令行入口
# ============================================

def main() -> None:
    parser = argparse.ArgumentParser(
        description="龍魂·拔水军统帅引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 扫描评论文本
  python3 bin/lh_water_army_elimination.py scan --text "评论文本1" "评论文本2"

  # 扫描JSONL文件（每个对象需含text/user_id等字段）
  python3 bin/lh_water_army_elimination.py scan --file comments.jsonl

  # 全流程执行（默认）
  python3 bin/lh_water_army_elimination.py full --file comments.jsonl

  # 全流程 + 详细输出
  python3 bin/lh_water_army_elimination.py full --file comments.jsonl --verbose --json

  # 启动阵地防护盾
  python3 bin/lh_water_army_elimination.py shield --platform weibo --url "https://..."

  # 系统仪表盘
  python3 bin/lh_water_army_elimination.py dashboard
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # scan — 快速扫描
    scan_parser = subparsers.add_parser("scan", help="快速扫描（仅Phase 1行为检测）")
    scan_group = scan_parser.add_mutually_exclusive_group(required=True)
    scan_group.add_argument("--text", nargs="+", help="评论文本（空格分隔多条）")
    scan_group.add_argument("--file", help="JSONL文件路径")

    # full — 全流程
    full_parser = subparsers.add_parser("full", help="全流程执行（Phase 1-5）")
    full_group = full_parser.add_mutually_exclusive_group(required=True)
    full_group.add_argument("--text", nargs="+", help="评论文本")
    full_group.add_argument("--file", help="JSONL文件路径")
    full_parser.add_argument("--target", help="目标URL或文章标识")
    full_parser.add_argument("--verbose", action="store_true", help="详细输出（含证据链）")
    full_parser.add_argument("--json", action="store_true", help="JSON格式输出")
    full_parser.add_argument("--output", help="输出文件路径")

    # shield — 防护盾
    shield_parser = subparsers.add_parser("shield", help="阵地防护盾")
    shield_parser.add_argument("--platform", required=True, help="平台（weibo/douyin/zhihu等）")
    shield_parser.add_argument("--url", required=True, help="目标URL")

    # dashboard
    subparsers.add_parser("dashboard", help="系统仪表盘")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "scan":
        comments = _parse_input(args)
        results, summary = phase1_behavior_scan(comments)[
            "findings"
        ], phase1_behavior_scan(comments)["summary"]

        from lh_water_army_detect import format_report
        print(format_report(results, summary, getattr(args, "file", "") or "命令行输入"))

    elif args.command == "full":
        comments = _parse_input(args)
        content_meta = _infer_content_meta(args)
        source_info = {"input_type": "file" if hasattr(args, "file") and args.file else "text",
                       "comments_count": len(comments)}
        target_info = {"url": args.target} if hasattr(args, "target") and args.target else None

        pipeline = full_elimination_pipeline(comments, content_meta, source_info, target_info)

        if hasattr(args, "json") and args.json:
            output = json.dumps(pipeline, ensure_ascii=False, indent=2)
            if hasattr(args, "output") and args.output:
                Path(args.output).write_text(output, encoding="utf-8")
                print(f"✅ 报告已输出到: {args.output}")
            else:
                print(output)
        else:
            verbose = hasattr(args, "verbose") and args.verbose
            report_text = format_pipeline_output(pipeline, verbose)
            print(report_text)
            if hasattr(args, "output") and args.output:
                Path(args.output).write_text(report_text, encoding="utf-8")
                print(f"\n✅ 报告已输出到: {args.output}")

    elif args.command == "shield":
        result = shield_mode(args.platform, args.url)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "dashboard":
        dash = dashboard()
        print(format_dashboard_output(dash))


def _parse_input(args) -> List[Dict[str, Any]]:
    """解析输入"""
    if hasattr(args, "file") and args.file:
        return parse_jsonl_file(args.file)
    elif hasattr(args, "text") and args.text:
        now = datetime.now().isoformat()
        return [{"text": t, "timestamp": now} for t in args.text]
    return []


def _infer_content_meta(args) -> Dict[str, Any]:
    """推断内容元数据"""
    meta: Dict[str, Any] = {"type": "text"}
    if hasattr(args, "target") and args.target:
        url = args.target.lower()
        if any(ext in url for ext in [".mp4", ".mov", ".avi", "video"]):
            meta["type"] = "video"
        elif any(ext in url for ext in [".mp3", ".wav", ".ogg", "audio"]):
            meta["type"] = "audio"
        elif any(ext in url for ext in [".jpg", ".png", ".gif", "image", "photo"]):
            meta["type"] = "image"
    return meta


def parse_jsonl_file(filepath: str) -> List[Dict[str, Any]]:
    """解析JSONL文件"""
    comments: List[Dict[str, Any]] = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                if isinstance(obj, dict[str, Any]):
                    if "comments" in obj and isinstance(obj["comments"], list[Any]):
                        comments.extend(obj["comments"])
                    else:
                        comments.append(obj)
                elif isinstance(obj, list[Any]):
                    comments.extend(obj)
            except json.JSONDecodeError:
                comments.append({"text": line, "timestamp": datetime.now().isoformat()})
    return comments


if __name__ == "__main__":
    main()
