#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·引擎分层保护引擎 v1.0
DNA: #龍芯⚡️丙午·甲申·壬子·亥时·䷗复-ENGINE-PROTECT-v1.0
创建者: 诸葛鑫（UID9622）
分层许可: 工程层 MulanPSL v2

四层保护:
  D1 绝密 🔴 — 内核算法·永不外泄·物理隔离
  D2 机密 🟠 — 核心引擎·仅UID9622+授权AI访问
  D3 内部 🟡 — 公开外壳·含烟雾弹·剽窃可检测
  D4 公开 🟢 — 自由分发·署名即可

功能:
  classify — 对所有引擎自动分层分类
  seal     — 给引擎打保护标记+DNA指纹
  scan     — 扫描是否有未保护引擎
  fog      — 为D3引擎生成烟雾弹版本（公开用）
  report   — 生成保护状态报告
"""

import hashlib
import json
import os
import re
import sys
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

# ═══ 常量 ═══
DNA = "#龍芯⚡️丙午·甲申·壬子·亥时·䷗复-ENGINE-PROTECT-v1.0"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROTECT_DB = PROJECT_ROOT / "config" / "engine_protection.json"
AUDIT_LOG = PROJECT_ROOT / "logs" / "engine_protection.log"

# 引擎目录
ENGINE_DIRS = [
    "engines", "04_ENGINES", "05_ENGINES",
    "核心引擎", "引擎", "bin"
]


class ProtectionLevel(Enum):
    """保护等级"""
    D1 = "D1-绝密"     # 永不公开·物理隔离
    D2 = "D2-机密"     # 仅授权访问
    D3 = "D3-内部"     # 公开外壳·烟雾弹
    D4 = "D4-公开"     # 自由分发


# ═══ D1 关键字（自动识别） ═══
D1_KEYWORDS = [
    "369不动点", "sn=369", "log369", "perm369",
    "DNA种子", "GPG私钥", "quantum_key", "quantum_seed",
    "内核算法", "CORE_ALGORITHM", "NEVER_EXPORT",
    "洛书引擎", "luoshu_369", "行为密码学核心",
    "七因子指纹", "seven_factor_core",
    "主权密钥", "sovereignty_key", "主权种子",
    "confirm_code", "CONFIRM_CODE",
]

# ═══ D2 关键字 ═══
D2_KEYWORDS = [
    "主权", "sovereignty", "防篡改", "anti_tamper",
    "熔断", "circuit_breaker", "meltdown",
    "审计引擎", "audit_engine", "identity_verify",
    "GPG签名", "gpg_sign", "DNA追溯", "dna_chain",
    "人格路由", "persona_router", "人格编排",
    "七因子", "seven_factor", "行为密码",
    "德本审计", "deben_audit", "离火运",
    "CNSH编译器", "cnsh_compiler",
]

# ═══ D3 关键字（可以公开但有烟雾弹） ═══
D3_KEYWORDS = [
    "创新引擎", "innovation", "自然路由", "natural_router",
    "知识蒸馏", "knowledge_distill", "AI安全", "safeai",
    "语义抽屉", "semantic_drawer", "术桥接", "通心译",
    "经济引擎", "xpay", "许愿池",
    "视频工坊", "video", "数字人", "digital_human",
    "搜索", "search_engine", "健康检查", "health_check",
]


def _compute_fingerprint(filepath: Path) -> str:
    """计算文件SHA256指纹"""
    try:
        content = filepath.read_bytes()
        return hashlib.sha256(content).hexdigest()[:16]
    except Exception:
        return "ERROR"


def _extract_dna(filepath: Path) -> Optional[str]:
    """从文件头提取DNA"""
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f):
                if i > 20:
                    break
                m = re.search(r'DNA:\s*(.+)', line)
                if m:
                    return m.group(1).strip()
    except Exception:
        pass
    return None


def _classify_engine(filepath: Path) -> ProtectionLevel:
    """根据内容和路径自动分类引擎"""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return ProtectionLevel.D4

    # 检查文件头是否已有保护标记
    if "D1-绝密" in content[:500] or "PROTECTION:D1" in content[:500]:
        return ProtectionLevel.D1
    if "D2-机密" in content[:500] or "PROTECTION:D2" in content[:500]:
        return ProtectionLevel.D2
    if "D3-内部" in content[:500] or "PROTECTION:D3" in content[:500]:
        return ProtectionLevel.D3

    # 自动分类
    relpath = str(filepath)

    # D1 检测
    for kw in D1_KEYWORDS:
        if kw in content:
            return ProtectionLevel.D1

    # D2 检测
    for kw in D2_KEYWORDS:
        if kw in content:
            return ProtectionLevel.D2

    # D3 检测
    for kw in D3_KEYWORDS:
        if kw in content:
            return ProtectionLevel.D3

    # 默认
    if "bin/" in relpath and "lh_" in relpath:
        return ProtectionLevel.D2  # bin工具默认D2
    if "engines/" in relpath:
        return ProtectionLevel.D3  # 引擎默认D3

    return ProtectionLevel.D4


def scan_engines(dirs: List[str] = None) -> List[Dict]:
    """扫描所有引擎并分类"""
    if dirs is None:
        dirs = ENGINE_DIRS

    results = []
    scanned = set()

    for d in dirs:
        dpath = PROJECT_ROOT / d
        if not dpath.exists():
            continue

        for root, _, files in os.walk(dpath):
            for f in files:
                if not f.endswith('.py'):
                    continue
                fpath = Path(root) / f
                fpath_abs = str(fpath.resolve())
                if fpath_abs in scanned:
                    continue
                scanned.add(fpath_abs)

                level = _classify_engine(fpath)
                dna = _extract_dna(fpath)
                fp = _compute_fingerprint(fpath)

                results.append({
                    "path": str(fpath.relative_to(PROJECT_ROOT)),
                    "level": level.value,
                    "dna": dna or "MISSING",
                    "fingerprint": fp,
                    "has_seal": SEAL[:10] in fpath.read_text(encoding='utf-8', errors='ignore')[:500] if fpath.exists() else False,
                })

    return results


def seal_engine(filepath: Path, level: ProtectionLevel, dry_run: bool = False) -> Dict:
    """给引擎打保护标记"""
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return {"status": "error", "reason": str(e)}

    # 保护标记模板
    protect_header = f"""# ═══ 龍魂引擎保护标记 ═══
# PROTECTION:{level.value} | 签发: {datetime.now(timezone.utc).isoformat()}
# 主权: {SEAL}
# DNA: {DNA}
# 指纹: {_compute_fingerprint(filepath)}
# 规则: 01_protocols/LH-ENGINE-PROTECTION-v1.0.md
# ═══════════════════════════════
"""

    # 检查是否已有保护标记
    if "PROTECTION:D" in content[:1000]:
        # 更新已有标记
        content = re.sub(
            r'# ═══ 龍魂引擎保护标记 ═══.*?# ═══════════════════════════════',
            protect_header.strip(),
            content,
            flags=re.DOTALL
        )
    else:
        # 在文件头后插入
        lines = content.split('\n')
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith('#') or line.startswith('"""') or line.startswith("'''"):
                continue
            if line.strip() == '':
                insert_at = i
                continue
            insert_at = max(0, i - 1)
            break

        new_lines = lines[:insert_at]
        new_lines.extend(protect_header.strip().split('\n'))
        new_lines.append('')
        new_lines.extend(lines[insert_at:])
        content = '\n'.join(new_lines)

    if not dry_run:
        filepath.write_text(content, encoding='utf-8')
        _log(f"SEALED {filepath.name} -> {level.value}")

    return {"status": "sealed", "level": level.value, "file": str(filepath)}


def _log(msg: str):
    """写审计日志"""
    ts = datetime.now(timezone.utc).isoformat()
    log_line = f"[{ts}] {msg}\n"
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
        f.write(log_line)


def generate_fog_version(filepath: Path, output_path: Optional[Path] = None) -> Dict:
    """
    为D3引擎生成烟雾弹版本
    - 保留接口签名和注释
    - 核心逻辑替换为迷雾占位符
    - 外部看起来完整，内部不可执行
    """
    try:
        content = filepath.read_text(encoding='utf-8', errors='ignore')
    except Exception as e:
        return {"status": "error", "reason": str(e)}

    lines = content.split('\n')
    fog_lines = []
    in_function = False
    indent_level = 0

    for line in lines:
        stripped = line.strip()

        # 保留注释和文档字符串
        if stripped.startswith('#') or stripped.startswith('"""') or stripped.startswith("'''"):
            fog_lines.append(line)
            continue

        # 保留 import 语句
        if stripped.startswith('import ') or stripped.startswith('from '):
            fog_lines.append(line)
            continue

        # 保留类/函数定义签名
        if re.match(r'(class|def)\s+\w+', stripped):
            fog_lines.append(line)
            in_function = True
            indent_level = len(line) - len(line.lstrip())
            continue

        # 函数体内部：替换为迷雾
        if in_function:
            current_indent = len(line) - len(line.lstrip())
            if stripped == '':
                fog_lines.append(line)
            elif current_indent <= indent_level and not stripped.startswith('#'):
                in_function = False
                fog_lines.append(line)
            else:
                # 迷雾替换
                fog_lines.append(' ' * current_indent + '# 🌀 烟雾弹 · 核心逻辑已保护 · 详见Notion知识库')
                in_function = False  # 只替换第一行，保留结构
        else:
            fog_lines.append(line)

    fog_content = '\n'.join(fog_lines)

    if output_path is None:
        output_path = filepath.parent / f"{filepath.stem}_fog{filepath.suffix}"

    output_path.write_text(fog_content, encoding='utf-8')
    return {"status": "fogged", "output": str(output_path)}


def save_registry(results: List[Dict]):
    """保存保护注册表"""
    PROTECT_DB.parent.mkdir(parents=True, exist_ok=True)
    registry = {
        "version": "1.0",
        "dna": DNA,
        "updated": datetime.now(timezone.utc).isoformat(),
        "total_engines": len(results),
        "by_level": {},
        "engines": results,
    }
    for r in results:
        lv = r["level"]
        registry["by_level"][lv] = registry["by_level"].get(lv, 0) + 1

    with open(PROTECT_DB, 'w', encoding='utf-8') as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    return registry


def print_report(registry: Dict):
    """打印保护报告"""
    print(f"""
╔══════════════════════════════════════════╗
║   🐉 龍魂 · 引擎分层保护报告 v1.0      ║
╠══════════════════════════════════════════╣
║  DNA: {DNA[:40]}...
║  更新: {registry['updated'][:19]}
║  引擎总数: {registry['total_engines']}
╠══════════════════════════════════════════╣""")

    for lv in ["D1-绝密", "D2-机密", "D3-内部", "D4-公开"]:
        count = registry["by_level"].get(lv, 0)
        icon = {"D1-绝密": "🔴", "D2-机密": "🟠", "D3-内部": "🟡", "D4-公开": "🟢"}.get(lv, "⚪")
        desc = {
            "D1-绝密": "永不外泄·物理隔离",
            "D2-机密": "仅授权访问·GPG加密",
            "D3-内部": "公开外壳·烟雾弹保护",
            "D4-公开": "自由分发·署名即可",
        }.get(lv, "")
        print(f"║  {icon} {lv}: {count:>5} 个 · {desc}")

    print("╚══════════════════════════════════════════╝")

    # D1 列出
    d1_engines = [e for e in registry["engines"] if e["level"] == "D1-绝密"]
    if d1_engines:
        print(f"\n🔴 D1-绝密引擎 ({len(d1_engines)}个):")
        for e in d1_engines[:10]:
            print(f"   {e['path']}")
        if len(d1_engines) > 10:
            print(f"   ... 还有 {len(d1_engines)-10} 个")

    # 缺失DNA的
    missing_dna = [e for e in registry["engines"] if e["dna"] == "MISSING"]
    if missing_dna:
        print(f"\n🟡 缺失DNA标记 ({len(missing_dna)}个):")
        for e in missing_dna[:5]:
            print(f"   {e['path']}")
        if len(missing_dna) > 5:
            print(f"   ... 还有 {len(missing_dna)-5} 个")


# ═══ CLI ═══
def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·引擎分层保护引擎 v1.0")
    sub = parser.add_subparsers(dest="cmd")

    # scan
    p_scan = sub.add_parser("scan", help="扫描所有引擎并分类")
    p_scan.add_argument("--dirs", nargs="*", help="指定目录")
    p_scan.add_argument("--json", action="store_true", help="JSON输出")
    p_scan.add_argument("--save", action="store_true", help="保存注册表")

    # seal
    p_seal = sub.add_parser("seal", help="给引擎打保护标记")
    p_seal.add_argument("file", help="文件路径")
    p_seal.add_argument("--level", choices=["D1","D2","D3","D4"], default="D3")
    p_seal.add_argument("--dry-run", action="store_true")

    # fog
    p_fog = sub.add_parser("fog", help="生成烟雾弹版本")
    p_fog.add_argument("file", help="源文件路径")
    p_fog.add_argument("--output", help="输出路径")

    # report
    p_report = sub.add_parser("report", help="查看保护报告")

    # seal-all
    p_seal_all = sub.add_parser("seal-all", help="批量保护所有引擎")
    p_seal_all.add_argument("--dry-run", action="store_true")
    p_seal_all.add_argument("--level", help="指定级别(不指定则自动分类)")

    args = parser.parse_args()

    if args.cmd == "scan":
        results = scan_engines(args.dirs)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        if args.save:
            registry = save_registry(results)
            print_report(registry)
        elif not args.json:
            registry = {"engines": results, "total_engines": len(results),
                       "by_level": {}, "dna": DNA, "version": "1.0",
                       "updated": datetime.now(timezone.utc).isoformat()}
            for r in results:
                lv = r["level"]
                registry["by_level"][lv] = registry["by_level"].get(lv, 0) + 1
            print_report(registry)
        return

    if args.cmd == "seal":
        fpath = PROJECT_ROOT / args.file if not args.file.startswith('/') else Path(args.file)
        if not fpath.exists():
            print(f"❌ 文件不存在: {fpath}")
            sys.exit(1)
        level_map = {"D1": ProtectionLevel.D1, "D2": ProtectionLevel.D2,
                     "D3": ProtectionLevel.D3, "D4": ProtectionLevel.D4}
        result = seal_engine(fpath, level_map[args.level], args.dry_run)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.cmd == "fog":
        fpath = PROJECT_ROOT / args.file if not args.file.startswith('/') else Path(args.file)
        output = Path(args.output) if args.output else None
        result = generate_fog_version(fpath, output)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if args.cmd == "report":
        if PROTECT_DB.exists():
            with open(PROTECT_DB, 'r', encoding='utf-8') as f:
                registry = json.load(f)
            print_report(registry)
        else:
            print("🟡 尚未生成保护注册表，请先运行 scan --save")
        return

    if args.cmd == "seal-all":
        results = scan_engines()
        sealed = 0
        for r in results:
            fpath = PROJECT_ROOT / r["path"]
            if not fpath.exists():
                continue
            if args.level:
                level_map = {"D1": ProtectionLevel.D1, "D2": ProtectionLevel.D2,
                             "D3": ProtectionLevel.D3, "D4": ProtectionLevel.D4}
                level = level_map[args.level]
            else:
                level_map2 = {
                    "D1-绝密": ProtectionLevel.D1, "D2-机密": ProtectionLevel.D2,
                    "D3-内部": ProtectionLevel.D3, "D4-公开": ProtectionLevel.D4
                }
                level = level_map2.get(r["level"], ProtectionLevel.D3)
            result = seal_engine(fpath, level, args.dry_run)
            if result["status"] == "sealed":
                sealed += 1

        print(f"✅ 已保护 {sealed}/{len(results)} 个引擎")
        registry = save_registry(results)
        print_report(registry)
        return

    # 默认: 扫描+报告
    results = scan_engines()
    registry = save_registry(results)
    print_report(registry)


if __name__ == "__main__":
    main()
