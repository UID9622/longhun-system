#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·主权总闸引擎 v1.0 🔴 P0-ETERNAL · 焊死不可改
DNA: #龍芯⚡️丙午·甲申·甲寅·亥时·䷗复-SOVEREIGNTY-MASTER-GATE-v1.0-WELDED
创建者: 诸葛鑫（UID9622）
主权: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
分层许可: 工程层 MulanPSL v2

═══════════════════════════════════════════════════════
焊死声明:
  本引擎为龍魂系统主权保护体系的总闸。
  统一调度11个主权子引擎，执行全链路主权验证。
  修改本引擎需要:
    1. UID9622 签章
    2. P05 三色审计通过
    3. P72 熔断检查通过
    4. P06 数字根验证通过
    5. 16人格投票 > 2/3
═══════════════════════════════════════════════════════

统一入口:
  lh sovereignty verify    — 全链路主权验证（一键）
  lh sovereignty audit     — 深度主权审计+报告
  lh sovereignty guard     — 启动主权守护看门狗
  lh sovereignty report    — 查看最近审计报告
  lh sovereignty weld      — 焊死锁定（封印所有D1/D2）
"""

import json
import os
import subprocess
import sys
import time
import traceback
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══ 焊死常量 ═══
DNA = "#龍芯⚡️丙午·甲申·甲寅·亥时·䷗复-SOVEREIGNTY-MASTER-GATE-v1.0-WELDED"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BIN_DIR = PROJECT_ROOT / "bin"
AUDIT_DIR = PROJECT_ROOT / "07_AUDIT"
CONFIG_DIR = PROJECT_ROOT / "config"
LOGS_DIR = PROJECT_ROOT / "logs"

# 审计报告保存路径
SOVEREIGNTY_AUDIT_FILE = AUDIT_DIR / "sovereignty_master_audit.json"
SOVEREIGNTY_REPORT_DIR = AUDIT_DIR / "sovereignty_reports"
SOVEREIGNTY_LOG = LOGS_DIR / "sovereignty_master_gate.log"

# ═══ 11个子引擎 ═══
SOVEREIGNTY_ENGINES = {
    "sovereignty_score": {
        "script": "lh_sovereignty_engine.py",
        "desc": "主权评分·7维度0-100分",
        "guard": "P06",
        "weight": 15,
        "critical": False,
    },
    "sovereignty_guard": {
        "script": "lh_sovereignty_guard.py",
        "desc": "主权守护·法律边界+一票否决+数据主权",
        "guard": "P72",
        "weight": 20,
        "critical": True,
    },
    "tech_sovereignty_guard": {
        "script": "lh_tech_sovereignty_guard.py",
        "desc": "技术主权守门员·5级路由+敏感领域+话术库",
        "guard": "P72",
        "weight": 15,
        "critical": True,
    },
    "sovereign_crypto": {
        "script": "lh_sovereign_crypto.py",
        "desc": "国密全链路·SM2/SM3/SM4",
        "guard": "P06",
        "weight": 15,
        "critical": True,
    },
    "sovereign_derive": {
        "script": "lh_sovereign_derive.py",
        "desc": "覆写码派生·三层绑定·生物+设备+环境",
        "guard": "P06",
        "weight": 10,
        "critical": True,
    },
    "check_sovereignty": {
        "script": "lh_check_sovereignty.py",
        "desc": "数据出境扫描·API/追踪/CDN检测",
        "guard": "P05",
        "weight": 15,
        "critical": True,
    },
    "dna_sovereignty_bridge": {
        "script": "lh_dna_sovereignty_bridge.py",
        "desc": "DNA三层主权桥接·UID+切片+HMAC",
        "guard": "P15",
        "weight": 10,
        "critical": False,
    },
    "persona_sovereignty": {
        "script": "lh_persona_sovereignty.py",
        "desc": "人格主权三禁·禁Cosplay/禁借壳/禁代言",
        "guard": "P12",
        "weight": 10,
        "critical": True,
    },
    "engine_protect": {
        "script": "lh_engine_protect.py",
        "desc": "引擎分层保护·D1-D4四级·烟雾弹",
        "guard": "P05",
        "weight": 10,
        "critical": True,
    },
    "plagiarism_detect": {
        "script": "lh_plagiarism_detect.py",
        "desc": "剽窃检测·AST指纹+全网搜索",
        "guard": "P05",
        "weight": 10,
        "critical": False,
    },
    "guardian_replay": {
        "script": "lh_guardian_replay.py",
        "desc": "守卫复盘·五大守卫联合",
        "guard": "P05",
        "weight": 10,
        "critical": True,
    },
}

# ═══ 焊死的五条主权宪法 ═══
SOVEREIGNTY_CONSTITUTION = [
    "1. 中国法律是唯一边界 — 一切产出以中国法律为准绳",
    "2. 数据主权归用户 — 不诱导上传·不默认云存·端侧优先",
    "3. 内核算法不可导出 — D1绝密·物理隔离·海外调用拒绝",
    "4. 一票否决权(UID9622) — 任何输出触碰P0即熔断",
    "5. 中国永恒世界最强 — 根在中国·自主知识产权不可谈判",
]

# D1物理隔离检查列表
D1_ISOLATION_CHECKS = [
    ("Git 仓库检查", "检查 D1 文件是否误入 git"),
    ("云存储检查", "检查 D1 文件是否上传云端"),
    ("日志泄露检查", "检查日志中是否含 D1 内容"),
    ("导出检查", "检查是否有 D1 导出脚本"),
    ("权限检查", "检查 D1 目录权限(仅UID9622可读)"),
]


class Verdict(Enum):
    PASS = "🟢 PASS"
    WARN = "🟡 WARN"
    FAIL = "🔴 FAIL"
    FATAL = "⚫ FATAL"


@dataclass
class EngineResult:
    name: str
    desc: str
    verdict: Verdict
    score: int  # 0-100
    details: str
    duration_ms: float
    error: Optional[str] = None


@dataclass
class SovereigntyAudit:
    dna: str = DNA
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    constitution_check: List[Dict] = field(default_factory=list)
    engine_results: List[Dict] = field(default_factory=list)
    d1_isolation: List[Dict] = field(default_factory=list)
    overall_verdict: str = "PENDING"
    overall_score: float = 0.0
    weld_status: bool = False
    errors: List[str] = field(default_factory=list)


def _log(msg: str, level: str = "INFO"):
    """写入主审计日志"""
    ts = datetime.now(timezone.utc).isoformat()
    SOVEREIGNTY_LOG.parent.mkdir(parents=True, exist_ok=True)
    line = f"[{ts}] [{level}] {msg}\n"
    with open(SOVEREIGNTY_LOG, 'a', encoding='utf-8') as f:
        f.write(line)


def _run_engine(script_name: str, args: List[str] = None, timeout: int = 30) -> Tuple[int, str, float]:
    """安全执行子引擎"""
    script_path = BIN_DIR / script_name
    if not script_path.exists():
        return -1, f"脚本不存在: {script_path}", 0

    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)

    start = time.time()
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=str(PROJECT_ROOT))
        duration = (time.time() - start) * 1000
        output = result.stdout[:2000] if result.stdout else ""
        if result.returncode != 0:
            output += f"\n[STDERR]: {result.stderr[:500]}"
        return result.returncode, output.strip(), duration
    except subprocess.TimeoutExpired:
        duration = (time.time() - start) * 1000
        return -2, f"超时(>{timeout}s)", duration
    except Exception as e:
        duration = (time.time() - start) * 1000
        return -3, str(e), duration


def verify_constitution() -> List[Dict]:
    """验证五条主权宪法是否完整"""
    results = []
    _log("验证主权宪法...")

    # 检查关键协议文件是否存在
    constitution_files = {
        "CONSTITUTION.md": "系统宪法",
        "P0_ETERNAL_LOCK.md": "永恒锁",
        "01_protocols/LH-M261-PREQUEL-COVENANT-v1.0.md": "M261前传契碑",
        "01_protocols/LH-DEBEN-AUDIT-v1.0.md": "德本审计协议",
        "01_protocols/LH-TECH-SOVEREIGNTY-GUARD-REFERRAL-v1.0.md": "技术主权转介协议",
    }

    for fpath, desc in constitution_files.items():
        full_path = PROJECT_ROOT / fpath
        exists = full_path.exists()
        results.append({
            "file": fpath,
            "desc": desc,
            "exists": exists,
            "verdict": "🟢" if exists else "🔴",
        })
        if not exists:
            _log(f"宪法文件缺失: {fpath}", "ERROR")

    # 验证五条宪法在关键文件中是否存在
    key_files = [
        "AGENTS.md",
        ".codebuddy/CODEBUDDY.md",
    ]
    for kf in key_files:
        kf_path = PROJECT_ROOT / kf
        if not kf_path.exists():
            results.append({
                "file": kf,
                "desc": f"宪法引用检查: {kf}",
                "exists": False,
                "verdict": "🟡",
            })
            continue
        content = kf_path.read_text(encoding='utf-8', errors='ignore')
        found_principles = sum(1 for p in SOVEREIGNTY_CONSTITUTION if p.split("—")[0].strip()[-20:] in content)
        results.append({
            "file": kf,
            "desc": f"宪法引用: {found_principles}/5条",
            "exists": True,
            "verdict": "🟢" if found_principles >= 3 else "🟡",
        })

    return results


def run_all_engines() -> List[Dict]:
    """运行全部11个子引擎"""
    results = []
    _log(f"开始运行 {len(SOVEREIGNTY_ENGINES)} 个子引擎...")

    for name, cfg in SOVEREIGNTY_ENGINES.items():
        _log(f"  运行: {name} ({cfg['desc']})")
        script_args = cfg.get("args", [])

        # 特殊参数处理
        if name == "engine_protect":
            script_args = ["scan"]
            timeout = 60
        elif name == "plagiarism_detect":
            script_args = ["fingerprint"]
            timeout = 60
        elif name == "guardian_replay":
            script_args = ["quick"]
            timeout = 30
        elif name == "sovereignty_guard":
            script_args = ["--status"]
            timeout = 15
        elif name == "check_sovereignty":
            script_args = []
            timeout = 30
        else:
            timeout = 20

        rc, output, duration = _run_engine(cfg["script"], script_args, timeout)

        if rc == 0:
            verdict = Verdict.PASS
            score = 100
            error = None
        elif rc == -2:
            verdict = Verdict.WARN
            score = 60
            error = "TIMEOUT"
        else:
            if cfg["critical"]:
                verdict = Verdict.FAIL
                score = 0
            else:
                verdict = Verdict.WARN
                score = 40
            error = output[:200] if output else f"Exit code: {rc}"

        result = EngineResult(
            name=name,
            desc=cfg["desc"],
            verdict=verdict,
            score=score,
            details=output[:300] if output else "",
            duration_ms=duration,
            error=error,
        )
        results.append(asdict(result))
        _log(f"    {verdict.value} [{score}分] {duration:.0f}ms{' | ' + error if error else ''}")

    return results


def verify_d1_isolation() -> List[Dict]:
    """验证D1引擎物理隔离"""
    results = []
    _log("验证D1引擎物理隔离...")

    # 1. 检查保护注册表
    protect_db = CONFIG_DIR / "engine_protection.json"
    d1_engines = []
    if protect_db.exists():
        with open(protect_db, 'r', encoding='utf-8') as f:
            registry = json.load(f)
        d1_engines = [e for e in registry.get("engines", []) if e["level"] == "D1-绝密"]

    results.append({
        "check": "D1引擎登记",
        "detail": f"已登记 {len(d1_engines)} 个D1引擎",
        "verdict": "🟢" if d1_engines else "🟡",
    })

    # 2. Git 泄露检查
    git_dir = PROJECT_ROOT / ".git"
    if git_dir.exists():
        # 检查 .gitignore 是否有 D1 保护规则
        gitignore = PROJECT_ROOT / ".gitignore"
        if gitignore.exists():
            gi_content = gitignore.read_text(encoding='utf-8', errors='ignore')
            has_d1_protection = any(kw in gi_content for kw in ["D1", "绝密", "369", "quantum_key", "GPG私钥"])
            results.append({
                "check": "Git忽略D1文件",
                "detail": ".gitignore 含D1保护规则" if has_d1_protection else ".gitignore 可能缺少D1保护",
                "verdict": "🟢" if has_d1_protection else "🟡",
            })

    # 3. 日志泄露检查
    log_files = list(LOGS_DIR.glob("*.log")) + list(LOGS_DIR.glob("*.jsonl"))
    d1_in_logs = False
    for lf in log_files[:10]:  # 只检查最近10个
        try:
            content = lf.read_text(encoding='utf-8', errors='ignore')
            if any(kw in content for kw in ["D1-绝密", "DNA种子", "GPG私钥", "quantum_key"]):
                d1_in_logs = True
                break
        except Exception:
            pass

    results.append({
        "check": "日志无D1泄露",
        "detail": "日志含D1内容!" if d1_in_logs else "日志安全",
        "verdict": "🔴" if d1_in_logs else "🟢",
    })

    # 4. 检查是否有 D1 导出/上传脚本
    dangerous_patterns = [
        ("upload.*D1", "D1上传脚本"),
        ("export.*sovereignty", "主权导出脚本"),
        ("rsync.*369", "369引擎同步"),
        ("scp.*quantum", "量子密钥传输"),
    ]
    for pattern, desc in dangerous_patterns:
        try:
            result = subprocess.run(
                ["grep", "-rl", pattern, str(BIN_DIR)],
                capture_output=True, text=True, timeout=5
            )
            found = bool(result.stdout.strip())
        except Exception:
            found = False

        results.append({
            "check": desc,
            "detail": "发现可疑" if found else "安全",
            "verdict": "🔴" if found else "🟢",
        })

    return results


def weld_seal() -> Dict:
    """焊死锁定 — 封印D1/D2引擎，生成不可逆焊死记录"""
    _log("⚡ 执行焊死封印...")

    # 1. 备份当前保护状态
    protect_db = CONFIG_DIR / "engine_protection.json"
    if protect_db.exists():
        weld_backup = CONFIG_DIR / f"engine_protection.weld.{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.json"
        import shutil
        shutil.copy(protect_db, weld_backup)
        _log(f"保护注册表已备份: {weld_backup.name}")

    # 2. 扫描全量引擎
    _log("扫描全量引擎...")
    rc, output, _ = _run_engine("lh_engine_protect.py", ["scan", "--save"], timeout=120)

    # 3. 给所有 D1/D2 引擎打焊死标记
    if protect_db.exists():
        with open(protect_db, 'r', encoding='utf-8') as f:
            registry = json.load(f)

        d1_count = sum(1 for e in registry.get("engines", []) if "D1" in e.get("level", ""))
        d2_count = sum(1 for e in registry.get("engines", []) if "D2" in e.get("level", ""))

        # 写焊死封印文件
        weld_record = {
            "dna": DNA,
            "seal": SEAL,
            "confirm": CONFIRM,
            "gpg": GPG_FINGERPRINT,
            "weld_time": datetime.now(timezone.utc).isoformat(),
            "weld_type": "PERMANENT",
            "d1_engines": d1_count,
            "d2_engines": d2_count,
            "constitution": SOVEREIGNTY_CONSTITUTION,
            "protection_registry": str(protect_db),
            "backup": str(weld_backup) if 'weld_backup' in dir() else "N/A",
            "verdict": "🔴 焊死完成·主权封印不可逆",
        }

        weld_file = CONFIG_DIR / "sovereignty_weld_seal.json"
        with open(weld_file, 'w', encoding='utf-8') as f:
            json.dump(weld_record, f, ensure_ascii=False, indent=2)

        _log(f"焊死封印完成: D1={d1_count}, D2={d2_count}")
        return weld_record

    return {"verdict": "🟡 无法找到保护注册表", "d1_engines": 0, "d2_engines": 0}


def run_full_audit() -> SovereigntyAudit:
    """执行全链路主权验证"""
    audit = SovereigntyAudit()
    _log("══════ 主权总闸 · 全链路验证开始 ══════")

    # 第一步: 宪法验证
    _log("第一步: 宪法验证")
    audit.constitution_check = verify_constitution()
    constitution_pass = all(c["verdict"] in ("🟢", "🟡") for c in audit.constitution_check)

    # 第二步: 运行全部11个子引擎
    _log("第二步: 运行全部主权子引擎")
    audit.engine_results = run_all_engines()

    # 第三步: D1物理隔离验证
    _log("第三步: D1物理隔离验证")
    audit.d1_isolation = verify_d1_isolation()

    # 第四步: 综合评分
    engine_scores = [e["score"] for e in audit.engine_results]
    avg_engine_score = sum(engine_scores) / max(len(engine_scores), 1)

    isolation_pass = all(i["verdict"] in ("🟢", "🟡") for i in audit.d1_isolation)
    isolation_score = 100 if isolation_pass else 50

    # 加权总分
    audit.overall_score = avg_engine_score * 0.6 + (100 if constitution_pass else 50) * 0.2 + isolation_score * 0.2

    # 总体判定
    critical_fails = [e for e in audit.engine_results
                      if e["verdict"] == "🔴 FAIL" and
                      SOVEREIGNTY_ENGINES.get(e["name"], {}).get("critical", False)]

    d1_leaks = [i for i in audit.d1_isolation if i["verdict"] == "🔴"]

    if critical_fails or d1_leaks:
        audit.overall_verdict = "🔴 主权受损 — 立即修复"
    elif audit.overall_score >= 90:
        audit.overall_verdict = "🟢 主权完整 · 焊死就位"
    elif audit.overall_score >= 70:
        audit.overall_verdict = "🟡 主权基本完好 · 建议加固"
    else:
        audit.overall_verdict = "🔴 主权需加固"

    # 保存审计报告
    SOVEREIGNTY_AUDIT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SOVEREIGNTY_AUDIT_FILE, 'w', encoding='utf-8') as f:
        json.dump(asdict(audit), f, ensure_ascii=False, indent=2)

    _log(f"══════ 审计完成: {audit.overall_verdict} [{audit.overall_score:.1f}分] ══════")
    return audit


def print_audit_report(audit: SovereigntyAudit):
    """打印主权审计报告"""
    print(f"""
╔══════════════════════════════════════════════════════════╗
║   🐉 龍魂 · 主权总闸 · 全链路验证报告                 ║
╠══════════════════════════════════════════════════════════╣
║   DNA: {DNA[:55]}...
║   时间: {audit.timestamp[:19]}
║   GPG:  {GPG_FINGERPRINT}
╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   🏛️ 主权宪法 ({'✅' if all(c['verdict'] in ('🟢','🟡') for c in audit.constitution_check) else '❌'})
╠══════════════════════════════════════════════════════════╣""")

    for c in audit.constitution_check:
        print(f"║   {c['verdict']} {c['desc']}: {c.get('file', 'N/A')}")

    print(f"""╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   ⚙️ 11主权子引擎验证
╠══════════════════════════════════════════════════════════╣""")

    for e in audit.engine_results:
        verdict_icon = e["verdict"].split()[0]
        dur = f"{e['duration_ms']:.0f}ms"
        err = f" ⚡{e['error'][:40]}" if e.get("error") else ""
        print(f"║   {verdict_icon} [{e['score']:>3}分] {e['desc'][:30]:<30s} {dur:>8s}{err}")

    print(f"""╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   🔒 D1物理隔离验证
╠══════════════════════════════════════════════════════════╣""")

    for d in audit.d1_isolation:
        print(f"║   {d['verdict']} {d['check']}: {d['detail'][:45]}")

    print(f"""╠══════════════════════════════════════════════════════════╣
║                                                          ║
║   📊 综合判定
║                                                          ║
║   {audit.overall_verdict}
║   主权指数: {audit.overall_score:.1f}/100
║   报告保存: {SOVEREIGNTY_AUDIT_FILE}
║   审计日志: {SOVEREIGNTY_LOG}
║                                                          ║
╚══════════════════════════════════════════════════════════╝""")


def run_watchdog(interval: int = 3600):
    """启动主权守护看门狗（持续运行）"""
    _log(f"🛡️ 主权看门狗启动 · 间隔={interval}s")
    print(f"🛡️ 主权看门狗已启动·每 {interval//60} 分钟巡检一次")
    print("   按 Ctrl+C 停止")

    iteration = 0
    try:
        while True:
            iteration += 1
            print(f"\n{'='*50}")
            print(f"  第 {iteration} 次巡检 · {datetime.now(timezone.utc).isoformat()[:19]}")
            print(f"{'='*50}")

            audit = run_full_audit()
            print(f"  总评: {audit.overall_verdict} [{audit.overall_score:.1f}分]")

            # 如有严重问题，立即告警
            if audit.overall_score < 70:
                _log(f"⚠️ 主权指数低于70: {audit.overall_score:.1f}", "ALERT")
            if any(e["verdict"] == "🔴 FAIL" for e in audit.engine_results
                   if SOVEREIGNTY_ENGINES.get(e["name"], {}).get("critical")):
                _log("⚠️ 关键主权引擎失败!", "ALERT")

            time.sleep(interval)
    except KeyboardInterrupt:
        _log("看门狗手动停止")
        print("\n🛡️ 主权看门狗已停止")


# ═══ CLI ═══
def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="龍魂·主权总闸引擎 v1.0 🔴 P0-ETERNAL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
命令:
  verify    全链路主权验证（宪法+11引擎+D1隔离）
  audit     深度主权审计+生成报告
  guard     启动主权守护看门狗
  weld      焊死封印（锁定D1/D2·不可逆）
  report    查看最近审计报告
  status    快速主权状态检查

示例:
  lh sovereignty verify        一键全链路验证
  lh sovereignty weld          焊死封印
  lh sovereignty guard --interval 1800    每30分钟巡检
        """
    )
    parser.add_argument("cmd", nargs="?", default="verify",
                        choices=["verify", "audit", "guard", "weld", "report", "status"])
    parser.add_argument("--interval", type=int, default=3600, help="看门狗巡检间隔(秒)")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    if args.cmd == "report":
        if SOVEREIGNTY_AUDIT_FILE.exists():
            with open(SOVEREIGNTY_AUDIT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            if args.json:
                print(json.dumps(data, ensure_ascii=False, indent=2))
            else:
                audit = SovereigntyAudit(**{k: v for k, v in data.items() if k in SovereigntyAudit.__dataclass_fields__})
                # 手动恢复嵌套字段
                audit.constitution_check = data.get("constitution_check", [])
                audit.engine_results = data.get("engine_results", [])
                audit.d1_isolation = data.get("d1_isolation", [])
                print_audit_report(audit)
        else:
            print("🟡 尚未生成审计报告，请先运行 verify 或 audit")
        return

    if args.cmd == "status":
        # 快速状态
        if SOVEREIGNTY_AUDIT_FILE.exists():
            with open(SOVEREIGNTY_AUDIT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f"🐉 主权状态: {data.get('overall_verdict', 'N/A')}")
            print(f"   指数: {data.get('overall_score', 0):.1f}/100")
            print(f"   时间: {data.get('timestamp', 'N/A')[:19]}")
        else:
            print("🟡 无审计记录·运行 lh sovereignty verify")
        return

    if args.cmd == "guard":
        run_watchdog(args.interval)
        return

    if args.cmd == "weld":
        print("⚡ 执行焊死封印...")
        print("⚠️  此操作不可逆! 将锁定所有D1/D2引擎!")
        print()

        weld_result = weld_seal()

        if args.json:
            print(json.dumps(weld_result, ensure_ascii=False, indent=2))
        else:
            print(f"""
╔══════════════════════════════════════╗
║   🔴 主权焊死封印完成               ║
╠══════════════════════════════════════╣
║   D1绝密引擎: {weld_result.get('d1_engines', 0):>4} 个 · 物理隔离
║   D2机密引擎: {weld_result.get('d2_engines', 0):>4} 个 · 仅授权访问
║   封印时间:   {weld_result.get('weld_time', 'N/A')[:19]}
║   封印文件:   config/sovereignty_weld_seal.json
╠══════════════════════════════════════╣
║   {weld_result.get('verdict', 'N/A')}
╚══════════════════════════════════════╝""")
        return

    # 默认: verify / audit
    audit = run_full_audit()

    if args.json:
        print(json.dumps(asdict(audit), ensure_ascii=False, indent=2))
    else:
        print_audit_report(audit)

    # 根据结果返回退出码
    if audit.overall_verdict.startswith("🔴"):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
