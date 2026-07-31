# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_FULL_SYSTEM_AUDIT-v1.0-85f78724
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂全系统大排查脚本 v1.0
检查：对冲冲突 / 孤立文件 / 注册表缺失 / 重复文件 / 依赖断裂
源头： #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
import json, os, sys, hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime

ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
CONFIRM_HASH = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"

# 核心目录（需要严格审计的）
CORE_DIRS = [
    "01_protocols", "01_技能庫", "02_執行記錄", "02_rules",
    "03_知識圖譜", "03_compiler", "04_決策日誌", "05_系統報告", "06_技術文檔",
    "L1_内核层", "L2_技能层", "L5_服务层", "L6_集成层", "L7_数据层",
    "L8_治理层", "L9_子系统",
    "bin", "scripts", "agents",
    "docs", "tools", "assets", "config", "deploy",
]

# 排除模式
EXCLUDE_PATTERNS = [
    "__pycache__", ".venv", "node_modules", ".git/", ".obsidian",
    ".codebuddy", "*.pyc", "*.DS_Store", "*.log", "*.pid", "*.zip",
    "dist/", "logs/", "tts_outputs/", "brain/", "baobao-guardian/",
    "train/", "_archive/", "_archives/", "_archived_reports/",
    ".longhun/", ".playwright-mcp/", ".snapshots/", ".mypy_cache/",
    ".pytest_cache/", ".claude/", ".github/", ".git.bak-",
    "voice-twin/tts_outputs/", ".vscode/",
]

def should_include(filepath):
    rel = str(filepath.relative_to(ROOT))
    for pat in EXCLUDE_PATTERNS:
        if pat in rel:
            return False
    return True

def get_file_hash(filepath):
    try:
        with open(filepath, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()[:12]
    except:  # noqa
        return "NO_READ"

def find_all_files():
    """返回所有应审计文件"""
    all_files = []
    for f in ROOT.rglob("*"):
        if f.is_file() and should_include(f):
            all_files.append(f)
    return all_files

def check_confirm_hash(files):
    """检查CONFIRM签名"""
    with_confirm = set()
    without_confirm = []
    for fp in files:
        try:
            content = fp.read_text(encoding='utf-8', errors='ignore')
            if CONFIRM_HASH in content:
                with_confirm.add(str(fp.relative_to(ROOT)))
            else:
                without_confirm.append(str(fp.relative_to(ROOT)))
        except:  # noqa
            without_confirm.append(str(fp.relative_to(ROOT)))
    return with_confirm, without_confirm

def check_registry_coverage(files):
    """检查注册表覆盖"""
    registry_path = ROOT / "L7_数据层/persona_knowledge/registry.json"
    if not registry_path.exists():
        return {}, set()
    
    reg = json.loads(registry_path.read_text())
    dep_graph = reg.get("dependency_graph", {})
    routes = reg.get("ipa_routes", {})
    
    registered_files = set(dep_graph.keys())
    registered_nodes = {r["local_path"] for r in routes if "local_path" in r}
    all_registered = registered_files | registered_nodes
    
    # 规范化比较
    actual_files = {str(f.relative_to(ROOT)) for f in files if f.suffix in ('.py', '.md', '.json')}
    
    in_registry_not_actual = all_registered - actual_files  # 注册了但文件不存在
    actual_not_in_registry = actual_files - all_registered  # 文件存在但未注册
    
    return {"in_registry_not_actual": in_registry_not_actual, 
            "actual_not_in_registry": actual_not_in_registry,
            "total_registered": len(all_registered),
            "total_actual": len(actual_files)}, all_registered

def find_duplicate_names(files):
    """找同名文件（可能对冲）"""
    name_map = defaultdict(list)
    for fp in files:
        name_map[fp.name].append(str(fp.relative_to(ROOT)))
    return {k: v for k, v in name_map.items() if len(v) > 1}

def find_root_clutter():
    """根目录文件碎片"""
    root_files = {}
    for f in ROOT.iterdir():
        if f.is_file() and not f.name.startswith('.'):
            root_files[f.name] = {
                'ext': f.suffix,
                'size': f.stat().st_size,
                'has_confirm': CONFIRM_HASH in f.read_text(encoding='utf-8', errors='ignore') if f.suffix in ('.md', '.py', '.json', '.txt', '.yaml', '.toml') else 'N/A'
            }
    return root_files

def find_isolated_producers(files, registry):
    """找出依赖图中无消费者的生产者"""
    reg_path = ROOT / "L7_数据层/persona_knowledge/registry.json"
    if not reg_path.exists():
        return {}
    
    reg = json.loads(reg_path.read_text())
    dep_graph = reg.get("dependency_graph", {})
    
    all_consumed = set()
    for fpath, info in dep_graph.items():
        for consumer in info.get("consumed_by", []):
            all_consumed.add(consumer.get("file", ""))
    
    producers = set(dep_graph.keys())
    isolated = producers - {dep_graph[p]["produced_by"][0] if dep_graph[p].get("produced_by") else "" for p in producers}
    
    return {"producers_without_consumers": isolated}

def find_dependency_conflicts(files_with_confirm):
    """找依赖冲突 — 同模块多版本"""
    version_files = defaultdict(list)
    for fp in files_with_confirm:
        name = fp.split('/')[-1]
        if 'v2.0' in name or 'v3.0' in name or 'v1.0' in name:
            base = name.split('_v')[0] if '_v' in name else name
            version_files[base].append(fp)
    return {k: v for k, v in version_files.items() if len(v) > 1}

def generate_report():
    print("=" * 70)
    print("🐉 龍魂全系统大排查报告")
    print(f"源头: {CONFIRM_HASH}")
    print(f"时间: {datetime.now().isoformat()}")
    print("=" * 70)
    
    # 1. 文件清单
    print("\n## 1. 文件总览")
    all_files = find_all_files()
    py_files = [f for f in all_files if f.suffix == '.py']
    md_files = [f for f in all_files if f.suffix == '.md']
    json_files = [f for f in all_files if f.suffix == '.json']
    html_files = [f for f in all_files if f.suffix == '.html']
    other_files = [f for f in all_files if f.suffix not in ('.py', '.md', '.json', '.html')]
    
    print(f"总文件数: {len(all_files)}")
    print(f"  .py: {len(py_files)}")
    print(f"  .md: {len(md_files)}")
    print(f"  .json: {len(json_files)}")
    print(f"  .html: {len(html_files)}")
    print(f"  其他: {len(other_files)}")
    
    # 2. CONFIRM签名覆盖
    print("\n## 2. CONFIRM签名覆盖")
    with_confirm, without_confirm = check_confirm_hash(all_files)
    pct = len(with_confirm) / len(all_files) * 100 if all_files else 0
    print(f"有CONFIRM: {len(with_confirm)} ({pct:.1f}%)")
    print(f"无CONFIRM: {len(without_confirm)} ({100-pct:.1f}%)")
    
    # 核心目录无CONFIRM
    print("\n### 核心目录中无CONFIRM签名文件:")
    core_without = [f for f in without_confirm if any(f.startswith(d) for d in CORE_DIRS)]
    for f in sorted(core_without):
        print(f"  ⚠️ {f}")
    
    # 3. 注册表覆盖
    print("\n## 3. 注册表覆盖")
    cov, registered = check_registry_coverage(all_files)
    print(f"注册表条目: {cov['total_registered']}")
    print(f"应注册文件: {cov['total_actual']}")
    
    if cov['in_registry_not_actual']:
        print(f"\n🔴 注册了但文件不存在 ({len(cov['in_registry_not_actual'])}):")
        for f in sorted(cov['in_registry_not_actual']):
            print(f"  💀 {f}")
    
    if cov['actual_not_in_registry']:
        core_unreg = [f for f in cov['actual_not_in_registry'] if any(f.startswith(d) for d in CORE_DIRS)]
        print(f"\n🟡 文件存在但未注册 (核心目录 {len(core_unreg)}):")
        for f in sorted(core_unreg):
            print(f"  📄 {f}")
    
    # 4. 根目录文件碎片
    print("\n## 4. 根目录文件碎片评估")
    root_files = find_root_clutter()
    non_core_root = {k: v for k, v in root_files.items() 
                     if k not in ['AGENTS.md', 'CONSTITUTION.md', 'CNSH-PROTOCOL.md',
                                   'CNSH-GATEKEEPER.md', 'CNSH-SEMANTIC.md',
                                   'README.md', 'ATTRIBUTION.md', 'CHANGELOG.md',
                                   'CLAUDE.md', 'LICENSE', 'SECURITY.md', 'CONTRIBUTING.md',
                                   'P0_ETERNAL_LOCK.md', 'MASTER_REGISTRY.md',
                                   'BACKUP_MANIFEST.md', 'STANDARD.md',
                                   'COMMIT_MESSAGE_STANDARD.md', '__init__.py',
                                   'requirements-base.txt', 'prod_config_template.json',
                                   'prod_monitoring_alerts.json',
                                   'CNSH_v1.0_FULL_ARCHITECTURE.md',
                                   'CNSH_v1.0_DEPLOYMENT_VERIFICATION.md',
                                   'CNSH_v3.0_UPGRADE_COMPLETE_REPORT.md',
                                   'CNSH_INTEGRATED_EXECUTION_REPORT.md',
                                   '15_AGENTS_INTEGRATION_SUMMARY.md']}
    
    # 分类根目录文件
    report_files = [k for k in non_core_root if 'REPORT' in k or 'report' in k.lower() or 'COMPLETION' in k or 'COMPLETE' in k or 'SUMMARY' in k or 'FINAL' in k or 'STATUS' in k]
    plan_files = [k for k in non_core_root if 'PLAN' in k or 'SETUP' in k or 'GUIDE' in k or 'CHECKLIST' in k or 'RUNBOOK' in k or 'REFERENCE' in k]
    other_root = [k for k in non_core_root if k not in report_files and k not in plan_files]
    
    print(f"📊 根目录非核心文件: {len(non_core_root)} 个")
    print(f"  🗂️ 一次性报告类: {len(report_files)} 个")
    print(f"  📋 计划/指南类: {len(plan_files)} 个")
    print(f"  ❓ 其他: {len(other_root)} 个")
    
    # 5. 同名文件（可能对冲）
    print("\n## 5. 同名文件（可能对冲/冗余）")
    dupes = find_duplicate_names(all_files)
    # 只显示核心目录中的重复
    interesting_dupes = 0
    for name, paths in sorted(dupes.items()):
        core_paths = [p for p in paths if any(p.startswith(d) for d in CORE_DIRS)]
        if len(core_paths) > 1 or (len(paths) > 2 and len(core_paths) > 0):
            interesting_dupes += 1
            print(f"\n  🔄 同名: {name} ({len(paths)}个)")
            for p in paths:
                marker = "⭐" if any(p.startswith(d) for d in CORE_DIRS) else "  "
                print(f"    {marker} {p}")
    if interesting_dupes == 0:
        print("  ✅ 核心目录无同名冲突")
    
    # 6. 多版本冲突
    print("\n## 6. 多版本并存（需确认正本）")
    versions = find_dependency_conflicts(with_confirm)
    for base, paths in sorted(versions.items()):
        print(f"\n  📚 {base} ({len(paths)}个版本):")
        for p in paths:
            print(f"    {p}")
    
    # 7. 独立脚本分析
    print("\n## 7. 独立脚本/模块分析")
    scripts_dir = ROOT / "scripts"
    if scripts_dir.exists():
        script_files = list(scripts_dir.rglob("*.py"))
        standalone = []
        for sf in script_files:
            try:
                content = sf.read_text()
                has_main = 'if __name__' in content
                imports = [l for l in content.split('\n') if l.strip().startswith('from ') or l.strip().startswith('import ')]
                standalone.append({
                    'file': str(sf.relative_to(ROOT)),
                    'has_main': has_main,
                    'imports': len(imports),
                    'has_confirm': CONFIRM_HASH in content
                })
            except:  # noqa
                pass
        print(f"  scripts/ 目录 .py 文件: {len(standalone)} 个")
        with_main = sum(1 for s in standalone if s['has_main'])
        print(f"  有 __main__ 入口: {with_main} 个")
        without_main = sum(1 for s in standalone if not s['has_main'])
        print(f"  无入口（纯库/未挂载）: {without_main} 个")
    
    # 8. 总结
    print("\n" + "=" * 70)
    print("## 总结")
    total = len(all_files)
    confirm_count = len(with_confirm)
    core_orphans = len(core_without)
    root_clutter = len(non_core_root)
    
    print(f"""
| 指标 | 数值 | 状态 |
|------|------|------|
| 总文件数 | {total} | — |
| CONFIRM签名覆盖 | {confirm_count}/{total} ({pct:.1f}%) | {'🟢' if pct > 80 else '🟡' if pct > 50 else '🔴'} |
| 核心目录无签名 | {core_orphans} | {'🟡' if core_orphans > 0 else '🟢'} |
| 注册表缺失文件 | {len(cov.get('in_registry_not_actual', set()))} | {'🔴' if cov.get('in_registry_not_actual') else '🟢'} |
| 未注册核心文件 | {len(core_unreg) if 'core_unreg' in dir() else 'N/A'} | — |
| 根目录碎片文件 | {len(non_core_root)} | {'🔴' if len(non_core_root) > 30 else '🟡' if len(non_core_root) > 10 else '🟢'} |
| 同名可能冲突 | {interesting_dupes} | {'🟡' if interesting_dupes > 0 else '🟢'} |
| 多版本并存 | {len(versions)} 组 | — |
""")
    
    return {
        'total': total,
        'confirm': confirm_count,
        'core_orphans': core_orphans,
        'root_clutter': root_clutter,
        'dupes': interesting_dupes,
        'versions': len(versions),
    }

if __name__ == '__main__':
    report = generate_report()
