#!/usr/bin/env python3
"""
龍魂联动感知引擎 · Cross-Module Awareness Engine
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DNA: #龍芯⚡️2026-07-07-CROSS-MODULE-AWARENESS-ENGINE-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

核心能力：
  每次AI操作/脚本执行后，自动扫描上下游依赖，发现孤立模块、
  缺少消费方的新数据、未注册的导航链接等"事不关己"断点。

哲学基础：
  责任塌缩模型 §4.3 — 责任心不是被动等待指令，是主动发现下游断点。
  S_责任 = Σ R_i × W_i → 联动缺失 = R 塌缩 = 系统失温。

用法：
  python3 bin/lh_cross_module_awareness.py                    # 全面扫描
  python3 bin/lh_cross_module_awareness.py --changed file.py  # 单文件变更触发
  python3 bin/lh_cross_module_awareness.py --auto-fix         # 扫描并自动修复
  python3 bin/lh_cross_module_awareness.py --check portal     # 仅检查portal联动
"""

import json
import os
import sys
import re
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Any

# ─── 常量 ───
PROJECT_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = PROJECT_ROOT / "L1_内核层" / "kernel" / "cross_module_registry.json"
PORTAL_INDEX = PROJECT_ROOT / "L5_服务层" / "services" / "portal" / "portal" / "index.html"
PORTAL_DATA_DIR = PROJECT_ROOT / "L5_服务层" / "services" / "portal" / "portal" / "data"
BIN_DIR = PROJECT_ROOT / "bin"

# ─── 颜色 ───
class Colors:
    RED = '\033[91m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def color(s: str, c: str) -> str:
    return f"{c}{s}{Colors.RESET}"

# ─── 加载注册表 ───
def load_registry() -> Optional[dict[str, Any]]:
    if not REGISTRY_PATH.exists():
        print(color(f"❌ 注册表不存在: {REGISTRY_PATH}", Colors.RED))
        return None
    with open(REGISTRY_PATH, 'r') as f:
        return json.load(f)

# ─── 读取文件 ───
def read_file_safe(path: Path) -> Optional[str]:
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception:
        return None

# ─── RULE-001: 新数据文件→portal消费检查 ───
def check_portal_data_consumers(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """检查 portal/data/ 下每个JSON文件在 index.html 中是否有消费"""
    issues = []
    
    if not PORTAL_INDEX.exists():
        return [{"rule": "RULE-001", "severity": "🔴", "msg": f"portal/index.html 不存在"}]
    
    html_content = read_file_safe(PORTAL_INDEX)
    if html_content is None:
        return [{"rule": "RULE-001", "severity": "🔴", "msg": "无法读取 portal/index.html"}]
    
    # 找到所有 portal/data/ 下的 JSON 文件
    data_files = []
    if PORTAL_DATA_DIR.exists():
        data_files = list(PORTAL_DATA_DIR.glob("*.json"))
    
    for data_file in data_files:
        rel_path = f"data/{data_file.name}"
        # 检查 HTML 中是否引用了此数据文件
        if rel_path not in html_content:
            # 在 registry 中查找该文件的消费方定义
            full_data_path = str(PORTAL_DATA_DIR / data_file.name).replace(str(PROJECT_ROOT) + "/", "")
            deps = registry.get("dependency_graph", {}).get(full_data_path, {})
            
            if deps:
                # registry 中有定义，但 HTML 中没找到 → 缺口
                issues.append({
                    "rule": "RULE-001",
                    "severity": "🔴",
                    "msg": f"portal/data/{data_file.name} 在registry有消费方定义，但portal/index.html中未引用",
                    "auto_fix": True,
                    "fix_description": f"需要在 portal/index.html 中补充 loadJSON('data/{data_file.name}') 引用和对应渲染函数"
                })
    
    # 检查 registry 中注册的 portal data 是否都在 HTML 中有消费
    for dep_key, dep_val in registry.get("dependency_graph", {}).items():
        if "portal/data/" in dep_key and dep_key.endswith(".json"):
            fname = dep_key.split("/")[-1]
            for consumer in dep_val.get("consumed_by", []):
                if consumer.get("file") == "L5_服务层/services/portal/portal/index.html" and consumer.get("required"):
                    pattern = consumer.get("pattern", "")
                    # 去掉 regex 转义，让子串匹配正常工作（persona_report\.json → persona_report.json）
                    pattern_plain = pattern.replace("\\.", ".")
                    if pattern and pattern_plain not in html_content:
                        issues.append({
                            "rule": "RULE-001",
                            "severity": "🔴",
                            "msg": f"portal/index.html 缺少对 {fname} 的引用（期望模式: {pattern}）",
                            "section": consumer.get("section", ""),
                            "auto_fix": consumer.get("auto_fix_ref") is not None
                        })
    
    return issues

# ─── RULE-002: 统计栏更新检查 ───
def check_stats_bar(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """检查统计栏是否列出了所有统计元素"""
    issues = []
    
    html_content = read_file_safe(PORTAL_INDEX)
    if html_content is None:
        return []
    
    expected_stats = registry.get("portal_sections", {}).get("stat_elements", [])
    for stat_id in expected_stats:
        if f'id="{stat_id}"' not in html_content and f"id='{stat_id}'" not in html_content:
            issues.append({
                "rule": "RULE-002",
                "severity": "🟡",
                "msg": f"portal统计栏缺少元素: id={stat_id}",
                "auto_fix": True
            })
    
    return issues

# ─── RULE-003: 新增API端点→消费方注册检查 ───
def check_api_consumers(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """检查注册表中API是否有消费方"""
    issues = []
    
    for dep_key, dep_val in registry.get("dependency_graph", {}).items():
        if dep_key.startswith("API:"):
            consumers = dep_val.get("consumed_by", [])
            if not consumers:
                issues.append({
                    "rule": "RULE-003",
                    "severity": "🟡",
                    "msg": f"API端点 {dep_key} 在registry中无消费方注册",
                    "auto_fix": False
                })
    
    return issues

# ─── RULE-004: bin/脚本注册检查 ───
def extract_script_desc(script_path: Path) -> str:
    """从脚本文件提取描述"""
    try:
        content = Path(script_path).read_text(encoding='utf-8')[:2000]
        lines = content.split('\n')
        # 跳过 shebang 和 coding
        start = 0
        for i, line in enumerate(lines):
            ls = line.strip()
            if ls.startswith('#!') or 'coding' in ls or ls == '':
                start = i + 1
                continue
            break
        remaining = '\n'.join(lines[start:])
        # 多行 docstring
        m = re.match(r'["\']{3}\s*\n?(.+?)["\']{3}', remaining, re.DOTALL)
        if m:
            return m.group(1).strip().split('\n\n')[0].replace('\n', ' ')[:120]
        # 单行注释
        for l in lines[start:start+5]:
            ls = l.strip()
            if ls.startswith('# ') and len(ls) > 3 and not ls.startswith('# -*-'):
                return ls[2:].strip()[:120]
        return ''
    except Exception:
        return ''

def check_bin_registry(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """检查 bin/ 下脚本是否在注册表中"""
    issues = []
    
    bin_dir = PROJECT_ROOT / "bin"
    if not bin_dir.exists():
        return []
    
    registered = registry.get("registered_bin_scripts", [])
    registered_names = {r.get("name", "") for r in registered}
    
    for script in sorted(bin_dir.glob("*.py")):
        script_name = script.name
        if script_name.startswith("_"):
            continue
        if script_name in registered_names:
            continue
        
        issues.append({
            "rule": "RULE-004",
            "severity": "🟡",
            "msg": f"bin/{script_name} 未在registered_bin_scripts中注册",
            "auto_fix": True,
            "fix_description": f"自动注册 bin/{script_name}",
            "file": str(script)
        })
    
    for script in sorted(bin_dir.glob("*.sh")):
        script_name = script.name
        if script_name.startswith("_"):
            continue
        if script_name in registered_names:
            continue
        
        issues.append({
            "rule": "RULE-004",
            "severity": "🟡",
            "msg": f"bin/{script_name} 未在registered_bin_scripts中注册",
            "auto_fix": True,
            "fix_description": f"自动注册 bin/{script_name}",
            "file": str(script)
        })
    
    return issues

# ─── RULE-007: portal新section→导航栏注册检查 ───
def check_portal_nav(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """检查 portal section 是否都在导航栏有链接"""
    issues = []
    
    html_content = read_file_safe(PORTAL_INDEX)
    if html_content is None:
        return []
    
    sections = registry.get("portal_sections", {}).get("current_sections", [])
    nav_map = registry.get("portal_sections", {}).get("nav_links_map", {})
    
    for section in sections:
        if section in nav_map:
            nav_text = nav_map[section]
            # 检查导航栏是否有这个链接
            if f'href="{section}"' not in html_content:
                issues.append({
                    "rule": "RULE-007",
                    "severity": "🔴",
                    "msg": f"portal导航栏缺少section链接: {section} ({nav_text})",
                    "auto_fix": True,
                    "fix_description": f'在<nav>中补充: <a href="{section}">{nav_text}</a>'
                })
    
    return issues

# ─── RULE-008: init函数执行检查 ───
def check_init_functions(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """检查 portal 中定义的 init 函数是否都在初始化时被调用"""
    issues = []
    
    html_content = read_file_safe(PORTAL_INDEX)
    if html_content is None:
        return []
    
    data_loaders = registry.get("portal_sections", {}).get("data_loaders", {})
    
    for data_path, init_func in data_loaders.items():
        func_name = init_func.replace("()", "")
        # 检查 init 函数是否在初始化链中被调用
        # 函数定义存在
        if f"function {func_name}" in html_content or f"async function {func_name}" in html_content:
            # 检查是否在初始化链中被调用
            # 在 initTheme() 后面的初始化链中查找
            init_chain_pattern = r'initTheme\(\);(.*?)}'
            init_chain_match = re.search(r'initTheme\(\);\s*((?:.|\n)*?)(?=//.*?init)', html_content)
            if init_chain_match:
                init_block = init_chain_match.group(1)
                if func_name not in init_block:
                    issues.append({
                        "rule": "RULE-008",
                        "severity": "🔴",
                        "msg": f"portal/index.html 定义了 {func_name}() 但初始化链中未调用",
                        "auto_fix": True,
                        "fix_description": f"在initTheme()后的初始化链中补充 {func_name}()"
                    })
    
    return issues

# ─── RULE-010: 执行权限检查 ───
def check_exec_permissions(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """检查 bin/ 下脚本执行权限"""
    issues = []
    
    for script in sorted(BIN_DIR.glob("*.py")):
        if not os.access(script, os.X_OK):
            issues.append({
                "rule": "RULE-010",
                "severity": "🟢",
                "msg": f"bin/{script.name} 缺少执行权限",
                "auto_fix": True,
                "fix_description": f"chmod +x {script}",
                "file": str(script)
            })
    
    for script in sorted(BIN_DIR.glob("*.sh")):
        if not os.access(script, os.X_OK):
            issues.append({
                "rule": "RULE-010",
                "severity": "🟢",
                "msg": f"bin/{script.name} 缺少执行权限",
                "auto_fix": True,
                "fix_description": f"chmod +x {script}",
                "file": str(script)
            })
    
    return issues

# ─── 消费方一致性检查（RULE-009） ───
def check_consumer_consistency(registry: dict[str, Any]) -> list[dict[str, Any]]:
    """检查数据消费者引用的一致性"""
    issues = []
    
    for dep_key, dep_val in registry.get("dependency_graph", {}).items():
        if not dep_key.endswith(".json"):
            continue
        
        # 读取源数据文件
        data_path = PROJECT_ROOT / dep_key
        if not data_path.exists():
            continue
        
        try:
            data_content = json.load(open(data_path, 'r'))
        except Exception:
            continue
        
        # 获取顶层字段
        top_keys = set(data_content.keys()) if isinstance(data_content, dict) else set()
        
        # 检查每个消费者
        for consumer in dep_val.get("consumed_by", []):
            consumer_file = PROJECT_ROOT / consumer["file"]
            if not consumer_file.exists():
                continue
            
            consumer_content = read_file_safe(consumer_file)
            if consumer_content is None:
                continue
            
            # 检查消费者是否引用了已废弃的字段（这里做简化检查）
            # 对于 portal/index.html，检查 data.xxx 引用
            if consumer_file.suffix == ".html" or consumer_file.suffix == ".js":
                # 提取所有 data.xxx 引用
                data_refs = set(re.findall(r'\bdata\.([a-zA-Z_]\w*)', consumer_content))
                # 提取所有可能是字段名的引用
                field_refs = set(re.findall(r'r\.([a-zA-Z_]\w*)', consumer_content))
                
                # 对于那些不在 top_keys 中的引用，标记潜在不一致
                for ref in field_refs:
                    if ref not in top_keys and ref not in ["code", "name", "role"]:
                        # 可能是旧字段引用
                        pass  # 需要更精确的上下文分析，暂时标记为低优先级
    
    return issues

# ─── 自动修复 ───
def auto_fix_issues(issues: list[dict[str, Any]]) -> int:
    """对可自动修复的问题执行修复"""
    fixed_count = 0
    new_registrations = []  # RULE-004 积累新注册的脚本
    
    for issue in issues:
        if not issue.get("auto_fix"):
            continue
        
        if issue.get("rule") == "RULE-004":
            # bin脚本自动注册
            filepath = issue.get("file", "")
            script_name = os.path.basename(filepath)
            desc = extract_script_desc(filepath) if filepath else ''
            new_registrations.append({
                "name": script_name,
                "description": desc,
                "added": datetime.now().isoformat(),
                "dna": f"#龍芯⚡️2026-07-07-AUTO-REGISTER-BIN-v1.0"
            })
            print(f"  ✅ {color('[已注册]', Colors.GREEN)} bin/{script_name}")
            fixed_count += 1
        
        elif issue.get("rule") == "RULE-010":
            # 执行权限修复
            filepath = issue.get("file")
            if filepath and os.path.exists(filepath):
                try:
                    os.chmod(filepath, 0o755)
                    print(f"  ✅ {color('[已修复]', Colors.GREEN)} {issue['msg']}")
                    fixed_count += 1
                except Exception as e:
                    print(f"  ❌ 修复失败: {e}")
        
        elif issue.get("rule") in ("RULE-001", "RULE-002", "RULE-007", "RULE-008"):
            # portal HTML 修复 → 需要更复杂的文本编辑
            print(f"  📝 {color('[需手动]', Colors.YELLOW)} {issue.get('fix_description', issue['msg'])}")
    
    # RULE-004: 持久化新注册到 JSON
    if new_registrations:
        registry_path = PROJECT_ROOT / "L1_内核层" / "kernel" / "cross_module_registry.json"
        try:
            reg = json.load(open(registry_path, 'r'))
            existing = reg.get("registered_bin_scripts", [])
            existing_names = {r["name"] for r in existing}
            for nr in new_registrations:
                if nr["name"] not in existing_names:
                    existing.append(nr)
            reg["registered_bin_scripts"] = existing
            reg["_meta"]["last_updated"] = datetime.now().isoformat()
            json.dump(reg, open(registry_path, 'w'), ensure_ascii=False, indent=2)
            print(f"  📋 {color('[持久化]', Colors.GREEN)} {len(new_registrations)} 个脚本写入 cross_module_registry.json")
        except Exception as e:
            print(f"  ❌ 持久化失败: {e}")
    
    return fixed_count

# ─── 主扫描函数 ───
def scan_all(registry: dict[str, Any], auto_fix: bool = False, changed_file: Optional[str] = None) -> dict[str, Any]:
    """执行全部联动感知扫描"""
    all_issues = []
    
    checks = [
        ("RULE-001: portal数据消费检查", check_portal_data_consumers),
        ("RULE-002: 统计栏更新检查", check_stats_bar),
        ("RULE-003: API消费方注册检查", check_api_consumers),
        ("RULE-004: bin脚本注册检查", check_bin_registry),
        ("RULE-007: portal导航栏检查", check_portal_nav),
        ("RULE-008: init函数调用检查", check_init_functions),
        ("RULE-010: 执行权限检查", check_exec_permissions),
    ]
    
    result = {
        "scan_time": datetime.now().isoformat(),
        "dna": "#龍芯⚡️2026-07-07-CROSS-MODULE-AWARENESS-SCAN-v1.0",
        "total_issues": 0,
        "critical": 0,
        "warnings": 0,
        "info": 0,
        "fixed": 0,
        "issues": [],
        "health_score": 100
    }
    
    for check_name, check_func in checks:
        try:
            issues = check_func(registry)
            all_issues.extend(issues)
        except Exception as e:
            all_issues.append({
                "rule": "SCAN-ERROR",
                "severity": "🟡",
                "msg": f"{check_name} 执行异常: {e}"
            })
    
    # 统计
    result["total_issues"] = len(all_issues)
    for issue in all_issues:
        sev = issue.get("severity", "🟡")
        if sev == "🔴":
            result["critical"] += 1
        elif sev == "🟡":
            result["warnings"] += 1
        else:
            result["info"] += 1
    
    result["issues"] = all_issues
    
    # 健康度
    result["health_score"] = max(0, 100 - result["critical"] * 20 - result["warnings"] * 5 - result["info"] * 2)
    
    # 自动修复
    if auto_fix:
        result["fixed"] = auto_fix_issues(all_issues)
    
    return result

# ─── 打印报告 ───
def print_report(result: dict[str, Any]) -> None:
    print()
    print(color("╔══════════════════════════════════════════════════╗", Colors.PURPLE))
    print(color("║     🧬 龍魂联动感知引擎 · 扫描报告               ║", Colors.PURPLE))
    print(color("╠══════════════════════════════════════════════════╣", Colors.PURPLE))
    
    health = result["health_score"]
    health_color = Colors.GREEN if health >= 80 else Colors.YELLOW if health >= 50 else Colors.RED
    health_icon = "🟢" if health >= 80 else "🟡" if health >= 50 else "🔴"
    
    print(f"║  联动健康度: {color(str(health), health_color)}/100 {health_icon}                ║")
    print(f"║  严重: {result['critical']} | 警告: {result['warnings']} | 信息: {result['info']}        ║")
    if result.get("fixed", 0) > 0:
        print(f"║  已自动修复: {result['fixed']} 项                          ║")
    print(color("╠══════════════════════════════════════════════════╣", Colors.PURPLE))
    
    if result["total_issues"] == 0:
        print(color("║  ✅ 无断点·所有模块联动正常                       ║", Colors.GREEN))
    else:
        for issue in result["issues"]:
            sev = issue.get("severity", "🟡")
            rule = issue.get("rule", "")
            msg = issue.get("msg", "")
            icon = "🔴" if sev == "🔴" else "🟡" if sev == "🟡" else "🟢"
            print(f"║  {icon} [{rule}] {msg}")
            if issue.get("fix_description"):
                print(f"║     → 修复: {issue['fix_description']}")
    
    print(color("╚══════════════════════════════════════════════════╝", Colors.PURPLE))
    print(f"  DNA: {result['dna']}")
    print()

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="龍魂联动感知引擎")
    parser.add_argument("--auto-fix", action="store_true", help="自动修复可修复的问题")
    parser.add_argument("--changed", type=str, help="单文件变更触发检查")
    parser.add_argument("--check", type=str, choices=["portal", "all"], default="all", help="检查范围")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")
    
    args = parser.parse_args()
    
    registry = load_registry()
    if registry is None:
        sys.exit(1)
    
    result = scan_all(registry, auto_fix=args.auto_fix, changed_file=args.changed)
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)
    
    # 退出码
    if result["critical"] > 0:
        sys.exit(2)  # 有严重断点
    elif result["warnings"] > 0:
        sys.exit(1)  # 有警告
    else:
        sys.exit(0)  # 通过

if __name__ == "__main__":
    main()
