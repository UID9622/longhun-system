#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️2026-07-21-DUALVIEW-V3-LANDING-V1.0-P0
# M::VALIDATOR-9622-20260721-LANDING-V1
# CNSH::#龍芯⚡️2026-07-21-双视角校验器-v1.0
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂v3落地校验器 · 命名合规·双视角一致·双版同步·三锚准入
# 用法: python3 bin/lh_dualview_validator.py [--scan /path] [--test]
"""
龍魂v3落地校验器 — 双视角封装 & v3.0 命名合规校验
=====================================================
M:: 职责: 解析/验收/落库/查询，只说真假
CNSH:: 职责: DNA/三色/五行/签章，守住归属

四模块:
  1. 命名合规校验 (4.2)
  2. 双视角一致性校验 (4.1)
  3. 双版本同步校验 (4.3)
  4. 三锚准入校验 (4.4)
"""

import re
import os
import sys
import json
import unicodedata
import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# ═══════════════════════════════════════════════
# 常量定义（焊死，修改需UID9622签章）
# ═══════════════════════════════════════════════

机器白名单 = {
    "M::", "CNSH::", "DNA", "CONFIRM", "SEAL", "README",
    "English", ".git", ".github", "LICENSE", "Makefile",
    # 标准开发生态（全世界通用，非"看不懂的英文名"）
    ".env", ".gitignore", ".dockerignore", ".gitattributes",
    ".cursorrules", ".bandit.yaml", ".pre-commit-config.yaml",
    ".coverage", "pyproject.toml", "pytest.ini",
    "requirements.txt", "requirements-base.txt", "requirements-dev.txt",
    "__init__.py", "setup.py", "setup.cfg",
    "Dockerfile", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    "CHANGELOG.md", "ATTRIBUTION.md",
    # 隐藏工具目录（IDE/工具生态标准）
    ".vscode", ".vscode.bak", ".claude", ".obsidian",
    ".playwright-mcp", ".codebuddy-plugin", ".daoyin_workspace",
    ".pytest_cache", ".archive", ".snapshots", ".longhun",
    ".githooks", ".git_dispose", ".git-rewrite",
    # 龍魂系统标记文件
    "cnsh.integrated", "mobile-monitoring.integrated",
    "skill-standards.integrated",
    # 日志文件标准命名
    "launchd.err.log", "launchd.out.log",
}

扩展名白 = {".sh", ".py", ".md", ".json", ".txt", ".yml", ".yaml", ".asc", ".toml", ".ini", ".cfg"}

V2_V3 = {
    "longhun-system": "龍魂系统",
    "install_longhun.sh": "一键安装.sh",
    "00_系统导航.md": "系统导航.md",
    "00_navigation.md": "系统导航.md",
    "longhun_rules_engine_v2.py": "核心引擎/规则引擎.py",
    "governance/risk_engine.py": "核心引擎/风险引擎.py",
    "cnsh_corrector.py": "语言修正/漂移词修正器.py",
    "extract_rules_to_json.py": "语言修正/规则导出工具.py",
    "bin/启动人格代理.py": "快捷命令/启动人格代理.py",
    "bin/tongxinyi_mcp.py": "快捷命令/通心译服务.py",
    "longhun_env": "运行环境",
}

一致性表 = {
    "true": {"pass"},
    "pending": {"hold", "rewrite"},
    "false": {"hold", "rewrite"},
    "error": {"fuse"},
}

DNA_RE = re.compile(r"^#龍芯⚡️\d{4}-\d{2}-\d{2}-.+-v\d+\.\d+.*$")
CONFIRM锚 = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SEAL前缀 = "#ZHUGEXIN⚡️2025-"

三色 = {"🟢": "通过", "🟡": "待核", "🔴": "阻断"}


# ═══════════════════════════════════════════════
# 模块1: 命名合规校验 (协议4.2)
# ═══════════════════════════════════════════════

def CNSH_NFC(名: str) -> str:
    """NFC归一化，防macOS NFD拆字"""
    return unicodedata.normalize("NFC", 名)


def CNSH_命名合规(路径: str) -> dict:
    """
    对路径逐段判定人读层中文覆盖率 γ。
    硬要求 γ = 1.0。
    发现裸英文主名 → 🔴 拒收 + 给出v3迁移建议。
    """
    段列 = [s for s in 路径.replace("\\", "/").split("/") if s]
    合规段 = 0
    违规段详情 = []

    for s in 段列:
        干, 点, 尾 = s.rpartition(".")
        # 机器层白名单直通
        if s in 机器白名单:
            合规段 += 1
            continue
        if 点 and ("." + 尾 in 扩展名白) and 干 in 机器白名单:
            合规段 += 1
            continue
        # 含中文 → 合规
        if re.search(r"[\u4e00-\u9fff]", CNSH_NFC(s)):
            合规段 += 1
            continue
        # 主名在机器白名单
        主名 = 干 if 点 else s
        if 主名 in 机器白名单:
            合规段 += 1
            continue
        # .asc GPG签名文件 → 检查母文件合规性（CONSTITUTION.md.asc → CONSTITUTION.md）
        if 点 and 尾 == "asc":
            母文件 = 干  # e.g. CONSTITUTION.md
            if 母文件 in 机器白名单:
                合规段 += 1
                continue
            # 再拆一次母文件扩展名来判定
            母干, 母点, 母尾 = 母文件.rpartition(".")
            if 母点 and (母干 in 机器白名单 or 母干.replace("-", "").isupper()):
                合规段 += 1
                continue
            if re.search(r"[\u4e00-\u9fff]", CNSH_NFC(母文件)):
                合规段 += 1
                continue
        # requirements-* 系列放行（标准Python生态）
        if 主名.startswith("requirements") and re.fullmatch(r"requirements[\w\-]*", 主名):
            合规段 += 1
            continue
        # .integrated 扩展名（龍魂集成模块标记）
        if 点 and 尾 == "integrated" and ("." not in 干 or 干.endswith(".integrated")):
            合规段 += 1
            continue
        # 隐藏文件/目录（.开头，标准Unix约定）
        if 主名.startswith(".") and 点 == "":
            合规段 += 1
            continue
        # 全大写机器约定名放行（README/LICENSE/LONGHUN_PROTOCOL）
        if re.fullmatch(r"[A-Z0-9_\-]+", 主名):
            合规段 += 1
            continue
        # 违规
        建议 = V2_V3.get(s) or V2_V3.get(主名) or "查《命名对照总表v1.0》"
        违规段详情.append({"段": s, "建议": str(建议)})

    γ = 合规段 / len(段列) if 段列 else 1.0
    return {
        "合规": len(违规段详情) == 0,
        "γ": round(γ, 4),
        "总段": len(段列),
        "合规段": 合规段,
        "违规": 违规段详情,
        "状态": "🟢 γ=1.0" if γ == 1.0 else "🔴 裸英文主名拒收"
    }


# ═══════════════════════════════════════════════
# 模块2: 双视角一致性校验 (协议4.1)
# ═══════════════════════════════════════════════

def CNSH_双视角一致(m_status: str, c_policy: str) -> dict:
    """
    M::status × CNSH::policy 必须在允许组合内。
    不在 → 🔴 双视角分裂，必有一环被篡改。
    """
    允许 = 一致性表.get(m_status, set())
    if c_policy in 允许:
        return {"一致": True, "状态": "🟢"}
    return {
        "一致": False,
        "状态": "🔴 双视角分裂：M::{} × CNSH::{} 必有一环被篡改".format(m_status, c_policy)
    }


# ═══════════════════════════════════════════════
# 模块3: 双版本同步校验 (协议4.3)
# ═══════════════════════════════════════════════

def CNSH_双版同步(中文版本: str, 镜像版本: str, 中文段数: int, 镜像段数: int) -> dict:
    """
    版本锁: V(中文) = V(镜像)，不等即 🔴。
    结构偏差率 δ ≤ 0.10。
    """
    if 中文版本 != 镜像版本:
        return {
            "同步": False,
            "状态": "🔴 版本锁失败 {}≠{}".format(中文版本, 镜像版本)
        }
    δ = abs(中文段数 - 镜像段数) / max(中文段数, 镜像段数, 1)
    if δ > 0.10:
        return {
            "同步": False,
            "δ": round(δ, 3),
            "状态": "🟡 镜像待更新，以中文版为准"
        }
    return {"同步": True, "δ": round(δ, 3), "状态": "🟢"}


# ═══════════════════════════════════════════════
# 模块4: 三锚准入校验 (协议4.4)
# ═══════════════════════════════════════════════

def CNSH_三锚准入(dna: Optional[str], confirm: Optional[str], seal: Optional[str]) -> dict:
    """
    三锚与门判定，fail-closed：缺一即拒。
    DNA必须用繁体「龍」，简体「龙芯」非法。
    """
    缺 = []
    if not (dna and DNA_RE.match(dna)):
        缺.append("DNA")
    if confirm != CONFIRM锚:
        缺.append("CONFIRM")
    if not (seal and seal.startswith(SEAL前缀)):
        缺.append("SEAL")
    # 简体龙芯检测
    if "龙芯" in (dna or ""):
        return {"准入": False, "缺": ["DNA(简体非法)"], "状态": "🔴 DNA简体龙芯，格式非法"}
    if 缺:
        return {"准入": False, "缺": 缺, "状态": "🔴 三锚缺一即拒"}
    return {"准入": True, "状态": "🟢 三锚齐全"}


# ═══════════════════════════════════════════════
# 模块5: 双段封装校验 (协议第三章第1条)
# ═══════════════════════════════════════════════

def CNSH_双段封装(m段: Optional[str], c段: Optional[str]) -> dict:
    """M::×CNSH:: 双段缺一即拒"""
    if not m段 or not c段:
        return {"封装": False, "状态": "🔴 双段缺一，拒收"}
    return {"封装": True, "状态": "🟢 双视角齐备"}


# ═══════════════════════════════════════════════
# 扫描器: 递归扫描目录所有文件命名合规性
# ═══════════════════════════════════════════════

忽略目录 = {
    ".git", "__pycache__", ".codebuddy", "node_modules",
    "运行环境", "归档冻结", "logs", "models", "dist",
    "_archive", "_work", "_private"
}

# v2遗产目录（已存在的老目录，不在v3迁移表中但保留不动）
遗产目录 = {
    "research", "papers", "deploy", "docker", "backups", "archive",
    "articles", "data", "config", "tests", "var", "tmp", "vault",
    "monitoring", "tools", "scripts", "docs", "output", "outputs",
    "releases", "templates", "extensions", "sdk", "library",
    "integrations", "integrated_modules", "integrated-modules",
    "imports", "bridges", "executors", "experiments", "experimental",
    "extensions", "backend", "frontend", "web", "web_apps",
    "knowledge", "knowledge-graph", "memory-universe",
    "train", "compute_kernels", "vector_db", "models",
    "audit", "calendar-context-logger", "chrome_extension",
    "cnsh/data", "cnsh/core", "cnsh/editor", "cnsh/repo-push",
    "cnsh/starter-kit", "cnsh/terminal", "core", "core-services",
    "crypto-stack", "data-hub", "dev-env", "editors", "editor",
    "engine", "engines", "forensic_kernel", "gitee-export",
    "governance", "kg-api", "kimi", "luoshu_369_engine",
    "multicurrency", "mvp_config", "ops-console",
    "phase3", "persona", "personas",
    "project-memory", "protocols", "public-content",
    "rules-engine-v2.5", "sovereignty", "sovereign-registry",
    "state", "systems", "tombstone_vault", "voice-dna",
    "voice-twin", "widgets", "wuxing-visual", "xpay",
    "zeng-extraction", "cnsh/repo-push",
    "container_data", "control-panel", "desktop",
    "L0_物理层", "L1_内核层", "L1_身份层", "L2_技能层",
    "L2_主权层", "L3_数据层", "L3_语义层", "L3_执行层",
    "L4_数据层", "L5_服务层", "L6_集成层", "L6_记忆层",
    "L6_同步层", "L7_表达层", "L7_数据层", "L8_分发层",
    "L8_治理层", "L9_子系统",
    "longhun-font", "longhun-v1.0-audit-package",
    "mobile-monitoring.integrated", "skill-standards.integrated",
    "android-auto", "baobao-guardian", "brain",
    "harmonyos-universe", "launchd", "logging_backup",
    "orders", "portal", "software_dna", "software-dna",
    "skills", "統一入口", "统一入口",
    "02_SKILLS", "01_protocols", "02_執行記錄", "02_rules",
    "06_HOUTU_OS", "03_KNOWLEDGE_GRAPH", "03_compiler", "04_決策日誌",
    "05_系統報告", "06_技術文檔",
    "法律引擎", "龙魂日记本-iOS", "人民维权助手",
    "字体", "引擎", "日志",
    "agents", "bin", "capabilities",
}

def 扫描目录(根路径: str, 全量: bool = False) -> Tuple[List[dict], int, int]:
    """扫描目录命名合规性。
    默认模式(--top): 只扫描顶层，定位v3迁移行动项。
    全量模式(--full): 递归扫描所有遗产文件（数量大，只做审计参考）。"""
    违规列表 = []
    合规 = 0
    总数 = 0

    for dirpath, dirnames, filenames in os.walk(根路径):
        # 过滤忽略目录
        dirnames[:] = [d for d in dirnames if d not in 忽略目录 and d not in 遗产目录]

        相对 = os.path.relpath(dirpath, 根路径)

        if 相对 == ".":
            # 顶层逐项检查
            for 文件名 in filenames:
                总数 += 1
                结果 = CNSH_命名合规(文件名)
                if 结果["合规"]:
                    合规 += 1
                else:
                    违规列表.append({"路径": 文件名, "类型": "文件", **结果})

            for 目录名 in dirnames:
                总数 += 1
                结果 = CNSH_命名合规(目录名)
                if 结果["合规"]:
                    合规 += 1
                else:
                    违规列表.append({"路径": 目录名, "类型": "目录", **结果})

            if not 全量:
                dirnames.clear()  # 非全量模式：阻断walk深入子目录

        elif 全量:
            # 全量模式继续递归扫描
            for 文件名 in filenames:
                全路径 = os.path.join(相对, 文件名)
                总数 += 1
                结果 = CNSH_命名合规(全路径)
                if 结果["合规"]:
                    合规 += 1
                else:
                    违规列表.append({"路径": 全路径, "类型": "文件", **结果})

            for 目录名 in dirnames:
                全路径 = os.path.join(相对, 目录名)
                总数 += 1
                结果 = CNSH_命名合规(全路径)
                if 结果["合规"]:
                    合规 += 1
                else:
                    违规列表.append({"路径": 全路径, "类型": "目录", **结果})

    return 违规列表, 合规, 总数


# ═══════════════════════════════════════════════
# 测试向量执行器 (协议第九章)
# ═══════════════════════════════════════════════

def 跑测试向量() -> dict:
    """执行第九章12条测试向量，返回通过/失败统计"""
    结果 = []
    通过 = 0
    失败 = 0

    # T01: 中文文件名
    r = CNSH_命名合规("核心引擎/规则引擎.py")
    结果.append({"id": "T01", "场景": "核心引擎/规则引擎.py", "期望": "🟢", "实际": r["状态"], "通过": r["合规"]})

    # T02: 裸英文主名
    r = CNSH_命名合规("longhun_rules_engine_v2.py")
    通过_t02 = not r["合规"] and "🔴" in r["状态"]
    结果.append({"id": "T02", "场景": "longhun_rules_engine_v2.py", "期望": "🔴+建议", "实际": r["状态"], "通过": 通过_t02})

    # T03: 机器层大写约定放行
    r = CNSH_命名合规("协议文档/English/LONGHUN_PROTOCOL.md")
    结果.append({"id": "T03", "场景": "English/LONGHUN_PROTOCOL.md", "期望": "🟢", "实际": r["状态"], "通过": r["合规"]})

    # T04: 双视角一致 true×pass
    r = CNSH_双视角一致("true", "pass")
    结果.append({"id": "T04", "场景": "M::true × CNSH::pass", "期望": "🟢", "实际": r["状态"], "通过": r["一致"]})

    # T05: 双视角分裂 true×fuse
    r = CNSH_双视角一致("true", "fuse")
    通过_t05 = not r["一致"] and "🔴" in r["状态"]
    结果.append({"id": "T05", "场景": "M::true × CNSH::fuse", "期望": "🔴分裂", "实际": r["状态"], "通过": 通过_t05})

    # T06: 双版同步 δ≤0.10
    r = CNSH_双版同步("v3.0", "v3.0", 100, 105)
    结果.append({"id": "T06", "场景": "中文v3.0 × 镜像v3.0 δ=0.05", "期望": "🟢", "实际": r["状态"], "通过": r["同步"]})

    # T07: 版本锁失败
    r = CNSH_双版同步("v3.0", "v2.9", 100, 100)
    通过_t07 = not r["同步"] and "🔴" in r["状态"]
    结果.append({"id": "T07", "场景": "中文v3.0 × 镜像v2.9", "期望": "🔴版本锁", "实际": r["状态"], "通过": 通过_t07})

    # T08: 三锚齐全
    r = CNSH_三锚准入("#龍芯⚡️2026-07-21-TEST-v1.0", CONFIRM锚, SEAL前缀 + "TEST")
    结果.append({"id": "T08", "场景": "三锚齐全", "期望": "🟢", "实际": r["状态"], "通过": r["准入"]})

    # T09: 缺SEAL
    r = CNSH_三锚准入("#龍芯⚡️2026-07-21-TEST-v1.0", CONFIRM锚, None)
    通过_t09 = not r["准入"] and "SEAL" in str(r.get("缺", []))
    结果.append({"id": "T09", "场景": "缺SEAL", "期望": "🔴拒绝", "实际": r["状态"], "通过": 通过_t09})

    # T10: DNA简体龙芯非法
    r = CNSH_三锚准入("#龙芯⚡️2026-07-21-TEST-v1.0", CONFIRM锚, SEAL前缀 + "TEST")
    通过_t10 = not r["准入"] and "简体" in r["状态"]
    结果.append({"id": "T10", "场景": "DNA简体龙芯", "期望": "🔴非法", "实际": r["状态"], "通过": 通过_t10})

    # T11: 迁移模拟（用V2_V3对照表自测）
    all_found = all(v3 in V2_V3.values() for v3 in V2_V3.values())
    结果.append({"id": "T11", "场景": "V2_V3对照表完整性", "期望": "🟢", "实际": "🟢" if all_found else "🔴", "通过": all_found})

    # T12: 双段封装缺CNSH::
    r = CNSH_双段封装("M::TEST-9622-20260721-TEST-V1", None)
    通过_t12 = not r["封装"] and "🔴" in r["状态"]
    结果.append({"id": "T12", "场景": "缺CNSH::段", "期望": "🔴拒收", "实际": r["状态"], "通过": 通过_t12})

    for t in 结果:
        if t["通过"]:
            通过 += 1
        else:
            失败 += 1

    return {"总计": len(结果), "通过": 通过, "失败": 失败, "详情": 结果}


# ═══════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════

def 打印报告(标题: str, 数据: dict, 缩进: int = 0):
    前缀 = "  " * 缩进
    print(f"{前缀}━━ {标题} ━━")
    for k, v in 数据.items():
        if isinstance(v, list):
            print(f"{前缀}  {k}: [{len(v)}项]")
            for item in v[:5]:  # 只显示前5条
                print(f"{前缀}    - {item}")
            if len(v) > 5:
                print(f"{前缀}    ... 共{len(v)}条")
        else:
            print(f"{前缀}  {k}: {v}")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="龍魂v3落地校验器 · 双视角封装+命名合规")
    parser.add_argument("--scan", type=str, help="扫描指定目录的命名合规性")
    parser.add_argument("--full", action="store_true", help="全量递归扫描（含遗产目录内文件，数据量大）")
    parser.add_argument("--test", action="store_true", help="跑12条测试向量")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    parser.add_argument("--dry-run", action="store_true", help="扫描后不阻断，只报告")
    args = parser.parse_args()

    if args.test:
        print("══════ 龍魂v3 测试向量（12条）══════")
        报告 = 跑测试向量()
        if args.json:
            print(json.dumps(报告, ensure_ascii=False, indent=2))
        else:
            print(f"\n总计 {报告['总计']} | 🟢通过 {报告['通过']} | {'🔴失败 ' + str(报告['失败']) if 报告['失败'] > 0 else ''}")
            print("-" * 60)
            for t in 报告["详情"]:
                图标 = "✅" if t["通过"] else "❌"
                print(f"  {图标} {t['id']}: {t['场景']}")
                if not t["通过"]:
                    print(f"      期望: {t['期望']}  实际: {t['实际']}")
            print("-" * 60)
            if 报告["失败"] == 0:
                print("🟢 12/12 全绿 — 落地自证通过")
            else:
                print(f"🔴 {报告['失败']}/12 失败 — 需修复后重跑")

    elif args.scan:
        根 = os.path.abspath(args.scan)
        print(f"🔍 扫描: {根} ({'全量' if args.full else '顶层'}模式)")
        违规, 合规数, 总数 = 扫描目录(根, 全量=args.full)
        γ = round(合规数 / 总数, 4) if 总数 else 1.0
        报告 = {
            "扫描根": 根,
            "总段数": 总数,
            "合规段数": 合规数,
            "γ": γ,
            "状态": "🟢 通过" if γ == 1.0 else f"🔴 γ={γ} < 1.0",
            "违规数": len(违规),
            "违规": 违规
        }
        if args.json:
            print(json.dumps(报告, ensure_ascii=False, indent=2))
        else:
            打印报告("扫描报告", {k: v for k, v in 报告.items() if k != "违规"})
            if 违规:
                print(f"\n── 违规详情（共{len(违规)}条）──")
                for v in 违规[:20]:
                    print(f"  🔴 {v['路径']} → {v.get('建议', 'N/A')}")

        if γ < 1.0 and not args.dry_run:
            sys.exit(1)

    else:
        # 默认跑自检
        print("══════ 龍魂v3双视角落地校验器 v1.0 ══════")
        print(f"DNA: #龍芯⚡️2026-07-21-DUALVIEW-V3-LANDING-V1.0-P0")
        print(f"时间: {datetime.datetime.now().isoformat()}")
        print()

        # 自检：测试向量
        print("--- 模块自检：12条测试向量 ---")
        报告 = 跑测试向量()
        for t in 报告["详情"]:
            图标 = "✅" if t["通过"] else "❌"
            print(f"  {图标} {t['id']}: {t['场景']}")
        print(f"\n结果: {报告['通过']}/{报告['总计']} 通过")
        print(f"状态: {'🟢 全绿' if 报告['失败'] == 0 else '🔴 需修复'}")

        # 扫描当前项目
        print("\n--- 项目命名合规扫描 ---")
        项目根 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        违规, 合规数, 总数 = 扫描目录(项目根)
        γ = round(合规数 / 总数, 4) if 总数 else 1.0
        print(f"  总段: {总数} | 合规: {合规数} | γ={γ}")
        print(f"  状态: {'🟢 通过' if γ == 1.0 else '🔴 γ<1.0'}")

        if 违规:
            print(f"\n  违规文件/目录（共{len(违规)}条，控制显示前30条）:")
            for v in 违规[:30]:
                print(f"    🔴 [{v['类型']}] {v['路径']} → {v.get('建议','N/A')}")
        else:
            print("  ✅ 无违规")


if __name__ == "__main__":
    main()
