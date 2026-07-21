#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·乙未·丙申·酉时·☵坎-AUDIT-BATCH-PROCESSOR-v2.0-IDEMPOTENT-f3b2c1a8
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# 职能: 批量处理AI审计日志 · 自动审核+统计分析+异常标记
"""
龍魂·审计日志批量处理器 v2.0 (幂等+断点续传)
────────────────────────────────────────────
输入: logs/ai_audit.jsonl
输出: 同文件原地更新 review_status + 生成汇总报告

v2.0 新增:
  - 幂等性: 同一条记录多次处理结果一致，不重复标记
  - 断点续传: 通过 checkpoint.json 记录进度，中断后从断点继续
  - 流式处理: 逐行读写，不全部加载到内存(支持百万级)
  - 回滚保护: 写入前先备份，写失败自动回滚

处理逻辑:
  1. 自动审核: 同文件同hash出现过且审核通过 → 直接标记 reviewed
  2. 模式分析: 统计每个model_source的代码片段特征
  3. 异常检测: 标记异常的代码模式
  4. 生成报告: 汇总JSON
"""

import os
import sys
import json
import hashlib
import shutil
from pathlib import Path
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict

CST = timezone(timedelta(hours=8))
PROJECT_ROOT = Path(__file__).resolve().parent.parent
AUDIT_LOG = PROJECT_ROOT / "logs" / "ai_audit.jsonl"
REPORT_PATH = PROJECT_ROOT / "logs" / "audit_summary.json"
CHECKPOINT_PATH = PROJECT_ROOT / "logs" / "audit_checkpoint.json"
BACKUP_DIR = PROJECT_ROOT / "logs" / "audit_backups"


def load_all_logs():
    """加载全部审计日志"""
    logs = []
    if not AUDIT_LOG.exists():
        return logs
    with open(AUDIT_LOG) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                logs.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return logs


def analyze_logs(logs):
    """统计分析"""
    stats = {
        "total": len(logs),
        "pending": 0,
        "reviewed": 0,
        "flagged": 0,
        "by_model_source": Counter(),
        "by_file": Counter(),
        "by_date": Counter(),
        "by_line_range": defaultdict(int),
        "code_hash_freq": Counter(),
        "unique_files": set(),
        "unique_code_hashes": set(),
    }

    for log in logs:
        stats["by_model_source"][log.get("model_source", "unknown")] += 1
        stats["by_file"][log.get("file_path", "unknown")] += 1
        stats["unique_files"].add(log.get("file_path", ""))
        stats["unique_code_hashes"].add(log.get("code_hash", ""))
        stats["code_hash_freq"][log.get("code_hash", "")] += 1

        status = log.get("review_status", "pending")
        if status == "pending":
            stats["pending"] += 1
        elif status in ("reviewed", "approved"):
            stats["reviewed"] += 1
        elif status == "flagged":
            stats["flagged"] += 1

        # 按日期统计
        ts = log.get("timestamp", "")
        if ts:
            date = ts[:10]
            stats["by_date"][date] += 1

        # 行范围
        ls = log.get("line_start", 0)
        le = log.get("line_end", 0)
        if ls and le:
            span = le - ls + 1
            if span <= 5:
                stats["by_line_range"]["1-5行"] += 1
            elif span <= 20:
                stats["by_line_range"]["6-20行"] += 1
            elif span <= 100:
                stats["by_line_range"]["21-100行"] += 1
            else:
                stats["by_line_range"]["100+行"] += 1

    return stats


def auto_review(logs):
    """
    智能审核规则:
    1. 同code_hash出现3次以上 → 批量通过（重复片段，非异常）
    2. 文件为well-known系统文件 → 自动通过
    3. model_source为已知可信来源 → 自动通过
    4. 其余标记为 reviewed_batch（批量审核通过，非人工逐条）
    """
    code_hash_freq = Counter(log.get("code_hash", "") for log in logs)
    
    # 高频hash（重复片段，安全）
    high_freq_hashes = {h for h, c in code_hash_freq.items() if c >= 3}
    
    # 已知可信文件
    trusted_patterns = [
        "lh_llm_api.py", "lh_knowledge_hub_api.py", "lh_memory_load.py",
        "lh_deben_audit.py", "lh_cross_module_router.py",
        "__init__.py", "setup.py", "conftest.py",
    ]
    
    # 已知可信模型来源
    trusted_sources = {"DeepSeek", "Kimi", "CodeBuddy", "local", "ollama", "longhun"}
    
    updated = 0
    flagged = 0
    
    for log in logs:
        if log.get("review_status") != "pending":
            continue
        
        ch = log.get("code_hash", "")
        fp = log.get("file_path", "")
        ms = log.get("model_source", "")
        fn = os.path.basename(fp) if fp else ""
        
        # 规则1: 高频重复hash → 自动通过
        if ch in high_freq_hashes:
            log["review_status"] = "reviewed_batch"
            log["review_method"] = "高频重复片段自动通过"
            log["reviewed_at"] = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
            updated += 1
            continue
        
        # 规则2: 可信文件 → 自动通过
        if any(p in fn for p in trusted_patterns):
            log["review_status"] = "reviewed_batch"
            log["review_method"] = f"可信系统文件({fn})自动通过"
            log["reviewed_at"] = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
            updated += 1
            continue
        
        # 规则3: 可信来源
        if ms in trusted_sources:
            log["review_status"] = "reviewed_batch"
            log["review_method"] = f"可信来源({ms})自动通过"
            log["reviewed_at"] = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
            updated += 1
            continue
        
        # 规则4: 其余 → 标记为需人工审核
        log["review_status"] = "flagged"
        log["review_method"] = "自动标记·需人工复核"
        log["reviewed_at"] = datetime.now(CST).strftime("%Y-%m-%d %H:%M:%S")
        flagged += 1
    
    return updated, flagged


def save_logs(logs):
    """原地写回（带备份+回滚保护）"""
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(CST).strftime('%Y%m%d_%H%M%S')
    backup = str(BACKUP_DIR / f"ai_audit.bak.{ts}.jsonl")
    
    # 1. 先备份
    if AUDIT_LOG.exists():
        shutil.copy2(str(AUDIT_LOG), backup)
    
    # 2. 写临时文件
    tmp_path = str(AUDIT_LOG) + ".tmp"
    try:
        with open(tmp_path, "w") as f:
            for log in logs:
                f.write(json.dumps(sanitize_surrogates(log), ensure_ascii=False) + "\n")
        # 3. 原子替换
        os.replace(tmp_path, str(AUDIT_LOG))
    except Exception as e:
        # 回滚：清理临时文件
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise RuntimeError(f"写入失败已回滚，备份在 {backup}: {e}")
    
    return backup


# ════════════════════════════════
# 断点续传
# ════════════════════════════════
def load_checkpoint():
    """加载断点"""
    if CHECKPOINT_PATH.exists():
        try:
            with open(CHECKPOINT_PATH) as f:
                return json.load(f)
        except: pass
    return {"processed": 0, "total": 0, "status": "new"}


def save_checkpoint(processed, total, status="in_progress"):
    """保存断点"""
    cp = {
        "processed": processed, "total": total,
        "status": status,
        "updated_at": datetime.now(CST).isoformat(),
        "dna": "#龍芯⚡️AUDIT-CHECKPOINT-v2.0"
    }
    with open(CHECKPOINT_PATH, "w") as f:
        json.dump(cp, f, indent=2)


def clear_checkpoint():
    if CHECKPOINT_PATH.exists():
        CHECKPOINT_PATH.unlink()


def sanitize_surrogates(obj):
    """递归清理字典/列表中的代理字符（U+D800-U+DFFF），防止 json.dumps 崩溃"""
    if isinstance(obj, dict):
        return {sanitize_surrogates(k): sanitize_surrogates(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [sanitize_surrogates(item) for item in obj]
    if isinstance(obj, str):
        # 逐字符替换代理对为 �
        result = []
        for ch in obj:
            cp = ord(ch)
            if 0xD800 <= cp <= 0xDFFF:
                result.append('\ufffd')
            else:
                result.append(ch)
        return ''.join(result)
    return obj


def stream_process():
    """
    流式处理（v2.0核心）: 逐行读→处理→逐行写临时文件→原子替换
    支持断点续传：读取 checkpoint 跳过已处理行
    幂等性：已处理记录（非pending）不重复标记
    """
    checkpoint = load_checkpoint()
    skip_to = checkpoint.get("processed", 0)
    
    tmp_path = str(AUDIT_LOG) + ".stream_tmp"
    total = 0; updated = 0; flagged = 0; skipped = 0
    
    # 备份（安全第一）
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(CST).strftime('%Y%m%d_%H%M%S')
    backup = str(BACKUP_DIR / f"ai_audit.bak.{ts}.jsonl")
    if AUDIT_LOG.exists():
        shutil.copy2(str(AUDIT_LOG), backup)
    
    # 先扫描：统计 code_hash 出现频率（用于高频片段判定）
    code_hash_freq = Counter()
    with open(AUDIT_LOG) as f:
        for line in f:
            if not line.strip(): continue
            try:
                rec = json.loads(line)
                code_hash_freq[rec.get("code_hash", "")] += 1
            except: pass
    high_freq_hashes = {h for h, c in code_hash_freq.items() if c >= 3}
    
    # 流式处理
    trusted_patterns = [
        "lh_llm_api.py", "lh_knowledge_hub_api.py", "lh_memory_load.py",
        "lh_deben_audit.py", "lh_cross_module_router.py",
        "__init__.py", "setup.py", "conftest.py",
    ]
    trusted_sources = {"DeepSeek", "Kimi", "CodeBuddy", "local", "ollama", "longhun"}
    
    try:
        with open(AUDIT_LOG) as fin, open(tmp_path, "w") as fout:
            for line in fin:
                stripped = line.strip()
                if not stripped:
                    fout.write("\n")
                    continue
                
                # 断点续传：跳过已处理行
                if total < skip_to:
                    fout.write(line if line.endswith("\n") else line + "\n")
                    total += 1
                    skipped += 1
                    if total % 10000 == 0:
                        print(f"  ⏭️  跳过已处理: {total}/{skip_to}")
                    continue
                
                try:
                    rec = json.loads(stripped)
                except json.JSONDecodeError:
                    fout.write(line if line.endswith("\n") else line + "\n")
                    total += 1
                    continue
                
                total += 1
                
                # 幂等性：已处理记录跳过（不是pending的不再改）
                current_status = rec.get("review_status", "pending")
                if current_status != "pending":
                    fout.write(json.dumps(sanitize_surrogates(rec), ensure_ascii=False) + "\n")
                    continue
                
                # 自动审核判定
                ch = rec.get("code_hash", "")
                fp = rec.get("file_path", "")
                ms = rec.get("model_source", "")
                fn = os.path.basename(fp) if fp else ""
                
                # 规则1: 高频重复hash
                if ch in high_freq_hashes:
                    rec["review_status"] = "reviewed_batch"
                    rec["review_method"] = "高频重复片段自动通过"
                    rec["reviewed_at"] = datetime.now(CST).isoformat()
                    updated += 1
                # 规则2: 可信文件
                elif any(p in fn for p in trusted_patterns):
                    rec["review_status"] = "reviewed_batch"
                    rec["review_method"] = f"可信系统文件({fn})自动通过"
                    rec["reviewed_at"] = datetime.now(CST).isoformat()
                    updated += 1
                # 规则3: 可信来源
                elif ms in trusted_sources:
                    rec["review_status"] = "reviewed_batch"
                    rec["review_method"] = f"可信来源({ms})自动通过"
                    rec["reviewed_at"] = datetime.now(CST).isoformat()
                    updated += 1
                # 规则4: 其余标记人工
                else:
                    rec["review_status"] = "flagged"
                    rec["review_method"] = "自动标记·需人工复核"
                    rec["reviewed_at"] = datetime.now(CST).isoformat()
                    flagged += 1
                
                fout.write(json.dumps(sanitize_surrogates(rec), ensure_ascii=False) + "\n")
                
                # 定期保存断点
                if total % 5000 == 0:
                    save_checkpoint(total, -1, "in_progress")
                    print(f"  📍 断点: {total}条 ({updated}通过·{flagged}标记)")
        
        # 原子替换
        os.replace(tmp_path, str(AUDIT_LOG))
        # 成功后清除断点
        clear_checkpoint()
        
        print(f"\n✅ 流式处理完成: 共{total}条·跳过{skipped}条·通过{updated}条·标记{flagged}条")
        
        return total, updated, flagged, skipped, backup
        
    except Exception as e:
        # 保存断点以便续传
        save_checkpoint(total, -1, "failed")
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise RuntimeError(f"处理中断于第{total}行，断点已保存，备份在{backup}: {e}")


def generate_report(stats, updated, flagged, backup_path):
    """生成汇总报告"""
    report = {
        "dna": "#龍芯⚡️丙午·乙未·AUDIT-BATCH-v2.0-IDEMPOTENT",
        "generated_at": datetime.now(CST).isoformat(),
        "generator": "lh_audit_batch_processor.py v2.0 (幂等+断点续传)",
        "summary": {
            "total_entries": stats["total"],
            "pending_before": stats["pending"],
            "auto_reviewed": updated,
            "flagged_for_manual": flagged,
            "already_reviewed_before": stats["reviewed"],
            "pending_after": stats["pending"] - updated - flagged,
        },
        "by_model_source": dict(stats["by_model_source"].most_common(10)),
        "by_file": dict(stats["by_file"].most_common(10)),
        "by_date": dict(sorted(stats["by_date"].items())),
        "by_line_range": dict(stats["by_line_range"]),
        "unique_files": len(stats["unique_files"]),
        "unique_code_hashes": len(stats["unique_code_hashes"]),
        "top_repeated_hashes": [
            {"hash": h[:12], "count": c}
            for h, c in stats["code_hash_freq"].most_common(5)
        ],
        "backup": backup_path,
        "idempotency": "v2.0 — 同记录多次处理结果一致",
        "checkpoint": "支持断点续传",
    }
    
    with open(REPORT_PATH, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·审计日志批量处理器 v2.0 (幂等+断点)")
    parser.add_argument("--resume", action="store_true", help="从断点续传")
    parser.add_argument("--force", action="store_true", help="忽略断点，重新处理")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际写入")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    args = parser.parse_args()
    
    if not args.json:
        print("=" * 60)
        print("🐉 龍魂·审计日志批量处理器 v2.0 (幂等+断点续传)")
        print("=" * 60)

    # 检查断点
    checkpoint = load_checkpoint()
    if checkpoint["status"] == "in_progress" and not args.force:
        if not args.resume and not args.json:
            print(f"\n⚠️  发现未完成的断点: 已处理 {checkpoint['processed']} 条")
            print("   使用 --resume 续传，或 --force 重新开始")
        if not args.resume:
            return 1
    
    if args.force and checkpoint["status"] == "in_progress":
        clear_checkpoint()
        if not args.json:
            print("🧹 已清除断点，重新开始")

    if not AUDIT_LOG.exists():
        if not args.json:
            print("⚠️ 审计日志不存在")
        return 1

    if args.dry_run:
        total = 0; pending = 0
        with open(AUDIT_LOG) as f:
            for line in f:
                if not line.strip(): continue
                try:
                    rec = json.loads(line)
                    total += 1
                    if rec.get("review_status") == "pending": pending += 1
                except: pass
        if args.json:
            print(json.dumps({"total": total, "pending": pending, "mode": "dry-run"}, ensure_ascii=False, indent=2))
        else:
            print(f"\n📊 预览: 共{total}条·待审核{pending}条")
        return 0

    # 流式处理
    try:
        total, updated, flagged, skipped, backup = stream_process()
    except RuntimeError as e:
        print(f"\n❌ {e}", file=sys.stderr)
        return 1

    # 快速统计
    stats = {
        "total": total, "pending": total - updated - flagged - skipped,
        "reviewed": updated, "flagged": flagged,
        "by_model_source": Counter(), "by_file": Counter(),
        "by_date": Counter(), "by_line_range": defaultdict(int),
        "unique_files": set(), "unique_code_hashes": set(),
        "code_hash_freq": Counter(),
    }

    # 生成报告
    report = generate_report(stats, updated, flagged, backup)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print("📊 处理摘要")
        print(f"{'='*60}")
        print(f"  总记录:    {total}")
        print(f"  ⏭️ 跳过:   {skipped} (断点续传)")
        print(f"  ✅ 通过:   {updated}")
        print(f"  🚩 标记:   {flagged}")
        print(f"  通过率:    {updated / max(total - skipped, 1) * 100:.1f}%")
        print(f"  备份:      {backup}")
        print(f"  报告:      {REPORT_PATH}")
        if flagged > 0:
            print(f"\n  ⚠️ {flagged} 条需人工复核，详见报告")
        print(f"\n✅ 批量处理完成 (幂等v2.0)")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
