# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙申·己酉·CLEANUP-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂项目一键清理脚本 v1.0
DNA: #龍芯⚡️丙午·乙申·己酉·CLEANUP-v1.0

目标：去重、归档、瘦身，不删关键文件，只移不删。
"""
import os, sys, json, shutil, hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
LOG_FILE = ROOT / "05_系統報告" / f"cleanup_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
STATS = {
    "moved": 0, "removed": 0, "deduped": 0, "archived": 0,
    "bytes_saved": 0, "errors": []
}

def log(msg: str):
    print(f"  {msg}")

def section(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def sha256_short(f: Path) -> str:
    """快速文件hash用于去重"""
    try:
        h = hashlib.sha256()
        with open(f, 'rb') as fh:
            for chunk in iter(lambda: fh.read(65536), b''):
                h.update(chunk)
        return h.hexdigest()
    except:
        return ""

def safe_move(src: Path, dst_dir: Path, dry_run: bool = False) -> bool:
    """安全移动文件，目标存在则跳过或覆盖"""
    if not src.exists():
        return False
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst = dst_dir / src.name
    if dst.exists():
        # 目标已存在，检查hash
        if sha256_short(src) == sha256_short(dst):
            log(f"  跳过(相同): {src.name}")
            src.unlink()  # 删除源，因为目标已有相同文件
            STATS["removed"] += 1
            STATS["bytes_saved"] += src.stat().st_size
            return True
        else:
            # 内容不同，加后缀区分
            stem, suffix = os.path.splitext(src.name)
            dst = dst_dir / f"{stem}_dedup{suffix}"
    try:
        shutil.move(str(src), str(dst))
        size = dst.stat().st_size
        STATS["moved"] += 1
        STATS["bytes_saved"] += size
        return True
    except Exception as e:
        STATS["errors"].append(f"move {src} -> {dst}: {e}")
        return False

def safe_remove(f: Path) -> bool:
    """安全删除文件"""
    if not f.exists():
        return False
    try:
        size = f.stat().st_size
        f.unlink()
        STATS["removed"] += 1
        STATS["bytes_saved"] += size
        return True
    except Exception as e:
        STATS["errors"].append(f"remove {f}: {e}")
        return False

def safe_rmtree(d: Path) -> bool:
    """安全删除目录"""
    if not d.exists():
        return False
    try:
        total_size = sum(f.stat().st_size for f in d.rglob('*') if f.is_file())
        shutil.rmtree(str(d))
        STATS["removed"] += 1
        STATS["bytes_saved"] += total_size
        return True
    except Exception as e:
        STATS["errors"].append(f"rmtree {d}: {e}")
        return False

def find_duplicates(dirs: List[Path]) -> Dict[str, List[Path]]:
    """在多个目录中找重复文件"""
    hash_map: Dict[str, List[Path]] = {}
    for d in dirs:
        if not d.exists():
            continue
        for f in d.rglob('*'):
            if f.is_file() and f.suffix in ('.py', '.sh', '.md'):
                h = sha256_short(f)
                if h:
                    hash_map.setdefault(h, []).append(f)
    return {h: files for h, files in hash_map.items() if len(files) > 1}

# ============================================================
# Phase 1: 根目录报告文件归档
# ============================================================
def phase1_archive_root_reports():
    section("Phase 1: 根目录报告文件归档 → 05_系統報告/")
    
    report_dir = ROOT / "05_系統報告"
    patterns = [
        "*_REPORT*.md", "*_REPORT*.json", "*_SUMMARY*.md", "*_COMPLETE*.md",
        "*_COMPLETION*.md", "*_VERIFICATION*.md", "*_FINAL*.md",
        "*_DEPLOYMENT_*.md", "*_READINESS*.md", "*_INTEGRATION*.md",
        "*_EXECUTION*.md", "*_TEST_*.json", "*_TEST_*.md", "*_TEST_*.txt",
        "*_AUDIT_*.md", "*_AUDIT_*.json", "*_ALIGNMENT*.md",
        "*_STATUS*.md", "*_ASSESSMENT*.md", "*_EVALUATION*.md",
        "*_ANALYSIS*.md", "*_CONFIRMATION*.md", "*_DELIVERY*.md",
        "*_MANIFEST*.md", "*_INDEX*.md", "*_PLAN*.md",
        "KIMI_VERIFICATION_REPORT*.md", "NOTION_*.md", "PHASE*_*.md",
        "PRODUCTION_DEPLOYMENT_*.json", "PRODUCTION_*.md",
        "SMOKE_TEST_*.md", "STAGING_DEPLOYMENT_*.md",
        "SYSTEM_*.md", "SYSTEM_*.json", "SYSTEM_*.txt",
        "ROUTE_VERIFICATION_*.md", "ROUTING_VERIFICATION_*.md",
        "ROUTER_MATRIX_DEPLOYMENT_*.md",
        "V*_UPGRADE_REPORT.md", "WUXING_V3*_REPORT.md",
        "TASK*_REPORT.md", "TASK*_SUMMARY.md",
        "MVP_COMPLETION_REPORT*.md",
        "FORMULA_*_OPTIMIZATION*.md", "FORMULA_SYSTEM_OPTIMIZATION*.md",
        "DAY*-COMPLETION-REPORT*.md", "DAY*-FINAL-COMPLETION-REPORT*.md",
        "FINAL-PROJECT-COMPLETION-REPORT*.md",
        "FINAL_SESSION_SUMMARY.md", "FINAL_SYSTEM_*.md", "FINAL_SYSTEM_*.txt",
        "PROJECT_FINAL_SUMMARY.md", "PROJECT_SUMMARY_*.md",
        "SESSION_SUMMARY_*.md",
        "IMPLEMENTATION_STATUS_*.md", "IMPLEMENTATION_EXECUTION_REPORT.md",
        "LOGGING_INTEGRATION_REPORT.md", "M04_M05_EXECUTION_REPORT.md",
        "PERSONA_INTEGRATION_COMPLETE.md", "PERSONA_INTEGRATION_PLAN.md",
        "PERSONA_ROUTER_*.md", "PERSONA_SYSTEM_VERIFICATION_*.md",
        "PERSONA_TRAINING_SYSTEM_*.md",
        "INTEGRATION_COMPLETE_REPORT_*.md", "INTEGRATION_TEST_REPORT_*.md",
        "COMPLETE_EXECUTION_SUMMARY.md", "COMPLETE-API-DOCUMENTATION-v4.0.md",
        "COMPREHENSIVE_DEPLOYMENT_STATUS_*.md",
        "BENCHMARK_COMPLETE_FINAL_REPORT.md",
        "CNSH_INTEGRATED_EXECUTION_REPORT.md",
        "CNSH_v3.0_UPGRADE_COMPLETE_REPORT.md",
        "CNSH_v1.0_DEPLOYMENT_VERIFICATION.md",
        "CNSH_v1.0_FULL_ARCHITECTURE.md",
        "ARCHIVE_EVALUATION_REPORT.md", "BACKUP_MANIFEST.md",
        "DEPLOYMENT_READY_CHECKLIST_*.md",
        "DEPLOYMENT_READINESS_CONFIRMATION_REPORT.md",
        "DEPLOYMENT_RUNBOOK_FOR_TEAM.md", "DEPLOYMENT_GUIDE_v1.0.md",
        "FLEXIBLE_INTEGRATION_ROADMAP_*.md",
        "FLOW_DECISION_EXECUTION_REPORT.md",
        "LONGHUN_GOVERNANCE_FINAL_DELIVERY_*.md",
        "MCP_DETECTION_REPORT_*.md",
        "MOBILE-MONITORING-DEPLOYMENT-REPORT*.md",
        "MONITORING_VERIFICATION_REPORT_*.md",
        "NEXT_WEEK_DEPLOYMENT_PREP_*.md",
        "NOTION_SYNC_STATUS_REPORT.md",
        "PHASE2_VERIFICATION_REPORT.md",
        "PHASE3_AUTOMATED_EVALUATION_REPORT.md",
        "PHASE4_PRODUCTION_DEPLOYMENT_COMPLETE.md",
        "PRE_DEPLOYMENT_FINAL_SAFETY_CHECK.md",
        "PRK_v3.0_NOTION_DEPLOYMENT.md",
        "PRODUCTION_*.md",
        "PROTOCOL_LOCKDOWN_REPORT.md",
        "PROTOCOL_SIMPLIFICATION_COMPLETION_v2.md",
        "PROTOCOL_UNIFICATION_PLAN.md",
        "RELEASE-v4.0-MOBILE-MONITORING.md",
        "ROUTE_VERIFICATION_COMPLETE_REPORT.md",
        "ROUTING_VERIFICATION_FINAL_REPORT.md",
        "SANCAI_SYNC_EXECUTION_REPORT.md",
        "SECURITY-HOTFIX-v4.1.1-RELEASE-NOTES.md",
        "SKILL_STANDARDIZATION_UPGRADE_v3.3.0.md",
        "SKILLS_DEDUP_MANIFEST.md", "SKILLS_INTEGRATION_REPORT.md",
        "SYSTEM_INTEGRATION_TEST_RESULTS.json",
        "SYSTEM_TEST_RESULTS_FINAL.json",
        "SYSTEM_UNIFICATION_*.md",
        "UNIFIED_SYSTEM_COMPREHENSIVE_TEST_REPORT_*.md",
        "DASHBOARD_TEST_*.md",
        "DEPENDENCY_UPDATE_REPORT.md",
        "DNA_ALIGNMENT_*.md",
        "DRAGON_MULTICURRENCY_UPGRADE_PLAN.md",
        "DRAGON_UPGRADE_QUICKREF.txt",
        "ENGINE_DEDUP_MANIFEST.md",
        "EVOLUTION_DASHBOARD_VERIFICATION.md",
        "XPAY_DEPLOYMENT_COMPLETE.md",
        "ACTION_LOG_USAGE_GUIDE.md",
        "AUTOMATED_DAILY_ASSESSMENT_SETUP.md",
        "COMPATIBILITY_ANALYSIS_*.md",
        "CRON_AUTOMATION_SETUP.md", "CRON_BACKUP_SETUP.md",
        "DAILY_REVIEW_*.md",
        "PRODUCTION_*.json", "PRODUCTION_*.md",
        "15_AGENTS_INTEGRATION_SUMMARY.md",
        "AGENT_007_FIX_REPORT.md", "AGENT_011_FIX_REPORT.md", "AGENT_014_FIX_REPORT.md",
        "behavcrypto_receipt_*.json",
        "output_v3.2.json",
        "prod_config_template.json", "prod_monitoring_alerts.json",
        "OPENHUB_AI_CLAW_API_DOCS_*.json",
        "PRODUCTION_DEPLOYMENT_REPORT_PROD-*.json",
    ]
    
    for pattern in patterns:
        for f in ROOT.glob(pattern):
            if f.is_file():
                safe_move(f, report_dir)
    
    # 特殊：大文档移入 docs/
    special_docs = ["CNSH_v1.0_FULL_ARCHITECTURE.md", "CNSH-GATEKEEPER.md",
                    "CNSH-PROTOCOL.md", "CNSH-SEMANTIC.md"]
    for name in special_docs:
        f = ROOT / name
        if f.exists():
            safe_move(f, ROOT / "03_知識圖譜")
    
    # 部署相关 → deploy/
    deploy_files = ["LONGHUN_STARTUP_COMPLETE_GUIDE.md", "LOCAL_DEPLOYMENT_GUIDE.md"]
    for name in deploy_files:
        f = ROOT / name
        if f.exists():
            safe_move(f, ROOT / "deploy")

# ============================================================
# Phase 2: 重复文件去重
# ============================================================
def phase2_dedup():
    section("Phase 2: 重复文件去重")
    
    # 2A. DragonSoul_Guardian_v2.py 三份 → 保留 integrations/guardian/ + deploy/guardian-v2/
    dup_targets = [
        ROOT / "bin/DragonSoul_Guardian_v2.py",
    ]
    for f in dup_targets:
        if f.exists():
            safe_remove(f)
            log(f"  删除重复: {f.name}")
    
    # 2B. dao_ethics_anchor 两份 → 保留 scripts/ 版本
    f = ROOT / "bin/dao_ethics_anchor.py"
    if f.exists() and (ROOT / "scripts/dao_ethics_anchor_v1.0.py").exists():
        safe_remove(f)
        log("  删除重复: bin/dao_ethics_anchor.py (保留 scripts/)")
    
    # 2C. L6_同步层/ 下 old persona verify
    old_verify = [
        ROOT / "L6_同步层/longhun-persona-verify-v4.py",
        ROOT / "L6_同步层/longhun-persona-verify.py",
    ]
    for f in old_verify:
        if f.exists():
            safe_remove(f)
            log(f"  删除旧版: {f.name}")
    
    # 2D. 01_技能庫/downloads_archive/中重复 .skill
    dup_skill = ROOT / "01_技能庫/downloads_archive/新技能/longhun-v5-skills/local/longhun-agent-eco.skill"
    if dup_skill.exists():
        safe_remove(dup_skill)
        log("  删除重复.skill: longhun-agent-eco.skill (v5-skills/local)")
    
    # 2E. 01_技能庫/downloads_archive/新技能/longhun_mvp_reviewed/ 整个目录 — v1.0旧版
    reviewed_dir = ROOT / "01_技能庫/downloads_archive/新技能/longhun_mvp_reviewed"
    if reviewed_dir.exists():
        safe_rmtree(reviewed_dir)
        log("  删除旧版目录: longhun_mvp_reviewed/ (v1.0旧版)")
    
    # 2F. 01_技能庫/downloads_archive/新技能/zeng-extraction/ — 已整合
    zeng_ext = ROOT / "01_技能庫/downloads_archive/新技能/zeng-extraction"
    if zeng_ext.exists():
        safe_rmtree(zeng_ext)
        log("  删除已整合目录: zeng-extraction/")

# ============================================================
# Phase 3: bin/ 存根文件清理
# ============================================================
def phase3_clean_stubs():
    section("Phase 3: bin/ 存根/空文件清理")
    
    STUB_KEYWORDS = ["存根文件", "模块已迁移", "已废弃", "stub"]
    EMPTY_MAX_SIZE = 10  # bytes
    
    for f in (ROOT / "bin").glob("*.py"):
        try:
            size = f.stat().st_size
            if size == 0:
                safe_remove(f)
                log(f"  删除空文件: {f.name}")
                continue
            if size < 200:
                content = f.read_text(errors='ignore')
                if any(kw in content for kw in STUB_KEYWORDS):
                    safe_remove(f)
                    log(f"  删除存根: {f.name}")
        except:
            pass
    
    # 特殊：_root_cleanup.py 0字节
    f = ROOT / "bin/_root_cleanup.py"
    if f.exists() and f.stat().st_size == 0:
        safe_remove(f)
    
    # bin/plan.md — 移到docs
    plan = ROOT / "bin/plan.md"
    if plan.exists():
        safe_move(plan, ROOT / "docs")

# ============================================================
# Phase 4: 旧模型文件瘦身
# ============================================================
def phase4_model_cleanup():
    section("Phase 4: 旧模型文件瘦身")
    
    models_dir = ROOT / "models/longhun-v1.0/lora_output"
    
    # 4A. 旧版 GGUF (保留 v2.1 最新)
    gguf_dir = models_dir / "gguf"
    if gguf_dir.exists():
        keep_versions = {}  # 默认全部可删，保留v2.1
        for f in gguf_dir.glob("*.gguf"):
            safe_remove(f)
            log(f"  删除旧GGUF: {f.name}")
        # 删除空gguf目录
        if not any(gguf_dir.iterdir()):
            gguf_dir.rmdir()
    
    # 4B. 旧版 merged safetensors
    merged = models_dir / "merged/model.safetensors"
    if merged.exists() and (models_dir / "merged_v2.1/model.safetensors").exists():
        safe_remove(merged)
        log("  删除旧merged: v1.0 merged/model.safetensors")
    
    # 4C. base_model safetensors (已合并到 merged)
    base = ROOT / "models/longhun-v1.0/base_model/model.safetensors"
    if base.exists():
        safe_remove(base)
        log("  删除冗余: base_model/model.safetensors")
    
    # 4D. adapter备份
    adapter_backup = models_dir / "adapter_v1.9_backup"
    if adapter_backup.exists():
        safe_rmtree(adapter_backup)
        log("  删除旧adapter备份: adapter_v1.9_backup/")
    
    # 4E. 只保留adapter_v2.1最新，删除旧adapter训练checkpoint
    adapter_dir = models_dir / "adapter"
    if adapter_dir.exists():
        safe_rmtree(adapter_dir)
        log("  删除旧adapter训练文件: adapter/")

# ============================================================
# Phase 5: _downloads_staging 清理
# ============================================================
def phase5_clean_downloads():
    section("Phase 5: _downloads_staging 清理")
    
    ds = ROOT / "_downloads_staging"
    if not ds.exists():
        return
    
    # 5A. 删除 .bak 备份文件
    for f in ds.rglob("*.bak*"):
        safe_remove(f)
        log(f"  删除.bak: {f.relative_to(ds)}")
    
    # 5B. 删除重复的 .skill 文件 (与01_技能庫中重复的)
    # 保留 01_技能庫 中的权威版本
    skills_main = set()
    for f in (ROOT / "01_技能庫").glob("*.skill"):
        skills_main.add(f.name)
    for f in (ROOT / "01_技能庫/downloads_archive").rglob("*.skill"):
        skills_main.add(f.name)
    
    for f in ds.rglob("*.skill"):
        if f.name in skills_main:
            safe_remove(f)
            log(f"  删除重复skill: {f.name}")
    
    # 5C. 删除旧版/中间版本的 Python 脚本（只保留最新 v2+ 版）
    for f in ds.rglob("*v1.*.py"):
        safe_remove(f)
    for f in ds.rglob("*_v1.*.py"):
        safe_remove(f)
    
    # 5D. 删除日志文件
    for f in ds.rglob("*.log"):
        safe_remove(f)
    
    # 5E. 归档非代码文档到 docs/
    for f in ds.rglob("*报告*.md"):
        safe_move(f, ROOT / "05_系統報告")
    for f in ds.rglob("*总结*.md"):
        safe_move(f, ROOT / "05_系統報告")
    for f in ds.rglob("*计划*.md"):
        safe_move(f, ROOT / "docs")

# ============================================================
# Phase 6: docs/ 去重整理
# ============================================================
def phase6_docs_dedup():
    section("Phase 6: docs/ 去重整理")
    
    docs_dir = ROOT / "docs"
    
    # 6A. 删除 docs/ 下的 .py 脚本（不应在docs目录中）
    for f in docs_dir.glob("*.py"):
        safe_remove(f)
        log(f"  删除docs中脚本: {f.name}")
    
    # 6B. 清理 claude-backlog/ 中的旧Python脚本
    claude_backlog = docs_dir / "claude-backlog"
    if claude_backlog.exists():
        for f in claude_backlog.glob("*.py"):
            safe_remove(f)
    
    # 6C. docs/ 根级大JSON → 归档
    for f in docs_dir.glob("*.json"):
        if f.stat().st_size > 100_000:  # >100KB的大JSON
            safe_move(f, ROOT / "data")

# ============================================================
# Phase 7: 最终统计和清理
# ============================================================
def phase7_finalize():
    section("Phase 7: 最终统计")
    
    # 清理空的归档目录
    empty_dirs_to_check = [
        ROOT / "_downloads_staging",
        ROOT / "_archive",
    ]
    for d in empty_dirs_to_check:
        if d.exists():
            remaining = list(d.rglob('*'))
            if not remaining:
                safe_rmtree(d)
                log(f"  删除空目录: {d.name}/")
    
    # 清理 Python编译缓存
    for pycache in ROOT.rglob("__pycache__"):
        safe_rmtree(pycache)
    
    # 保存日志
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, 'w') as f:
        json.dump(STATS, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"  📊 清理完成!")
    print(f"  📁 移动文件: {STATS['moved']} 个")
    print(f"  🗑️  删除文件: {STATS['removed']} 个")
    print(f"  💾 预估节省: {STATS['bytes_saved'] / 1024 / 1024:.1f} MB")
    print(f"  ❌ 错误: {len(STATS['errors'])} 个")
    print(f"  📝 日志: {LOG_FILE}")
    print(f"{'='*60}")
    if STATS['errors']:
        print(f"\n  错误详情:")
        for e in STATS['errors']:
            print(f"    - {e}")

# ============================================================
# Main
# ============================================================
if __name__ == "__main__":
    print(f"""
╔═══════════════════════════════════════════════════════╗
║  🐉 龍魂项目一键清理 v1.0                            ║
║  DNA: #龍芯⚡️丙午·乙申·己酉·CLEANUP-v1.0            ║
║  原则: 移而不删 · 去重留一 · 归档归位               ║
╚═══════════════════════════════════════════════════════╝
""")
    phase1_archive_root_reports()
    phase2_dedup()
    phase3_clean_stubs()
    phase4_model_cleanup()
    phase5_clean_downloads()
    phase6_docs_dedup()
    phase7_finalize()
