# DNA: #龍芯⚡️丙午·丙申·癸巳·戌时·䷬萃-PATHS-REGISTRY-V1.0-P04-LAND
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 功能: 龍魂统一路径注册中心 v1.0.1 —— 防"同名不同路径=自毁"
#   P04 鲁班商讨结论(2026-08-24): 全系统目录名散乱(软链/双名/坏链)，
#   需要一个唯一真相源：逻辑名→权威路径映射 + 软链健康扫描 + resolve 接口。
#   与 lh_path_audit.py(文件归类审计)互补：本文件管"目录注册与解析"。

import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────
# 1. 逻辑名 → 权威相对路径（唯一真相源·以 ROOT 为基准）
#    软链别名（bin/engines/docs 等）统一解析到这里的权威路径
# ─────────────────────────────────────────────
REGISTRY = {
    # L0 层
    "protocols":    "01_protocols",       # 协议/白皮书
    "skills":       "02_SKILLS",          # 技能定义（01_技能庫 软链→此）
    "knowledge":    "03_KNOWLEDGE_GRAPH", # 知识图谱（03_知識圖譜 软链→此）
    "layers":       "03_LAYERS",          # 九层架构（layers 软链→此）
    "compiler":     "03_compiler",        # CNSH 编译器
    "audit":        "07_AUDIT",           # 审计（audit 软链→此）
    "bin":          "08_BIN",             # 可执行（bin 软链→此）
    "state":        "08_STATE",
    "tools":        "09_TOOLS",           # tools 软链→此
    "portal":       "10_PORTAL",          # portal 软链→此
    "data":         "11_DATA",
    "docs":         "12_DOCS",            # docs 软链→此
    "tests":        "13_TESTS",           # tests 软链→此
    "labs":         "15_LABS",
    "config":       "20_CONFIG",
    "task_engine":  "25_TASK_ENGINE",
    "houtu_os":     "06_HOUTU_OS",        # 03_后土OS 软链→此
    "services":     "04_SERVICES",        # services 软链→此
    "engines":      "05_ENGINES",         # engines 软链→此
    # 业务目录
    "exchange":     "exchange",           # 数字人民币跨境结算桥 :8899
    "personas":     "personas",           # 人格定义
    "deploy":       "deploy",             # 部署脚本
    "brand":        "brand",
    "web_apps":     "web_apps",
    "rust":         "rust",
    "sandbox":      "sandbox_runtime",
    "config_legacy": "config",            # 旧 config/（与 20_CONFIG 并存·待归一化）
}

# ─────────────────────────────────────────────
# 2. 软链别名表：别名 → 权威路径（自动扫描填充，手动覆盖纠错）
# ─────────────────────────────────────────────
def _scan_symlinks() -> dict:
    """扫描 ROOT 顶层软链：别名 → (目标, 是否自指向, 目标是否存在)
    v1.0.1 修复: 原用 resolve().name 判定自指向，会把"同名目录软链"
    (如 L0_物理层→layers/L0_物理层) 误判为坏链。改用 readlink 原始目标
    + strict=False 不跟随解析，真实自指向=目标解析后仍指回软链自身。"""
    result = {}
    for child in ROOT.iterdir():
        if child.is_symlink() and child.is_dir():
            raw = os.readlink(child)                     # 原始目标字符串
            target_abs = Path(raw) if raw.startswith("/") else child.parent / raw
            resolved = target_abs.resolve(strict=False)  # 不跟随到断点也不抛错
            self_loop = Path(os.path.abspath(child)) == resolved
            result[child.name] = {
                "target": raw,                           # 原始目标（可读）
                "self_loop": self_loop,                  # 🔴 真·自指向坏链
                "target_exists": resolved.exists(),      # 🔴 断链
                "is_alias": target_abs.name in {v for v in REGISTRY.values()},
            }
    return result


def root() -> Path:
    """系统根目录"""
    return ROOT


def resolve(name: str) -> Path:
    """逻辑名 → 权威绝对路径（不存在则尝试按原名返回 ROOT/name）"""
    rel = REGISTRY.get(name, name)
    p = ROOT / rel
    return p


# ─────────────────────────────────────────────
# 3. 软链健康检查（P09 目录归一化地基）
# ─────────────────────────────────────────────
def scan_symlinks() -> dict:
    return _scan_symlinks()


def verify() -> dict:
    """输出软链健康报告：🔴 坏链 / 🟡 别名 / 🟢 正常"""
    links = _scan_symlinks()
    bad_self = [k for k, v in links.items() if v["self_loop"]]
    bad_missing = [k for k, v in links.items() if not v["target_exists"]]
    aliases_ok = [k for k, v in links.items()
                  if not v["self_loop"] and v["target_exists"]]
    return {
        "total_symlinks": len(links),
        "self_loops": bad_self,          # 🔴 自指向=坏链，需修
        "broken": bad_missing,           # 🔴 目标不存在=断链，需修
        "healthy_aliases": aliases_ok,   # 🟢 正常别名
    }


def report() -> str:
    r = verify()
    lines = [
        f"龍魂路径注册中心 v1.0.1 · {ROOT}",
        f"注册逻辑名: {len(REGISTRY)} 个",
        f"顶层软链总数: {r['total_symlinks']}",
        f"🔴 自指向坏链({len(r['self_loops'])}): {', '.join(r['self_loops']) or '无'}",
        f"🔴 断链({len(r['broken'])}): {', '.join(r['broken']) or '无'}",
        f"🟢 正常别名({len(r['healthy_aliases'])}): {', '.join(r['healthy_aliases']) or '无'}",
    ]
    return "\n".join(lines)


# ─────────────────────────────────────────────
# 4. CLI
# ─────────────────────────────────────────────
def main():
    args = sys.argv[1:]
    if not args or args[0] == "--report":
        print(report())
    elif args[0] == "--json":
        print(json.dumps(verify(), ensure_ascii=False, indent=2))
    elif args[0] == "resolve" and len(args) >= 2:
        for name in args[1:]:
            p = resolve(name)
            print(f"{name} -> {p}")
    elif args[0] == "--verify":
        r = verify()
        # 🔴 有坏链/断链 → 退出码 1（供 CI/pre-commit 检测）
        if r["self_loops"] or r["broken"]:
            print(report())
            sys.exit(1)
        print("✅ 软链全部健康")
    else:
        print(__doc__)
        sys.exit(2)


if __name__ == "__main__":
    main()
