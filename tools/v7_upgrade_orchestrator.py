#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 v7 主干升级编排器

把 `/Users/zuimeidedeyihan/Downloads/Kimi_Agent_终端升级与结构优化 7`
吸收进系统主干：
  - ~/longhun-system/
  - ~/CNSH 软链接
  - ~/.kimi-code/skills/
  - ~/.zshrc / ~/.bashrc

不重复做 v6 已有的事，而是把 v7 新文件整合进来，并复用/升级结构。

DNA:#龍芯⚡️2026-06-20-V7-UPGRADE-ORCHESTRATOR-v1.0
"""

import hashlib
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

V7_ROOT = Path("/Users/zuimeidedeyihan/Downloads/Kimi_Agent_终端升级与结构优化 7").resolve()
MAIN_SYSTEM = Path("/Users/zuimeidedeyihan/longhun-system").expanduser().resolve()
CNSH_LINK = Path("/Users/zuimeidedeyihan/CNSH").expanduser()
USER_SKILLS_DIR = Path("/Users/zuimeidedeyihan/.kimi-code/skills").expanduser().resolve()
MEMORY_SCRIPT_CANDIDATES = [
    Path("/Users/zuimeidedeyihan/.longhun/scripts/longhun_memory_bootstrap.py").expanduser(),
    Path("/Users/zuimeidedeyihan/.longhun/scripts/memory_bootstrap.py").expanduser(),
]
OPS_CONSOLE = MAIN_SYSTEM / "ops-console" / "index.html"
REPORT_PATH = MAIN_SYSTEM / "V7_UPGRADE_REPORT.md"
IMPORT_DIR = MAIN_SYSTEM / "imports" / "v7"


def make_dna(prefix: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")[:-3]
    h = hashlib.sha256((ts + prefix + "v7").encode()).hexdigest()[:12].upper()
    return f"#龍芯⚡️{ts}-V7-UPGRADE-{prefix}-{h}"


def log(msg: str):
    print(f"  {msg}")


def clean_pycache(root: Path):
    removed = 0
    for p in list(root.rglob("__pycache__")) + list(root.rglob("*.pyc")) + list(root.rglob(".DS_Store")):
        try:
            if p.is_dir():
                shutil.rmtree(p)
            else:
                p.unlink()
            removed += 1
        except Exception:
            pass
    log(f"清理垃圾文件/目录: {removed}")


def skill_scope(name: str) -> str:
    if name.startswith("longhun-cloud-"):
        return "cloud"
    if name in ("CNSH-PROTOCOL", "CNSH-SEMANTIC", "dragon-soul-agent", "content_sovereignty_protocol"):
        return "protocol"
    return "local"


def organize_skills():
    skills_dir = V7_ROOT / "skills"
    if skills_dir.exists():
        shutil.rmtree(skills_dir)
    for scope in ("local", "cloud", "protocol"):
        (skills_dir / scope).mkdir(parents=True)

    stats = {"from_flat": 0, "from_package": 0, "merged": 0}

    # 1. 目录包（longhun-v5-skills/）优先，内容通常更完整
    for src_scope in ("local", "cloud"):
        src_dir = V7_ROOT / "longhun-v5-skills" / src_scope
        if not src_dir.exists():
            continue
        for pkg in src_dir.iterdir():
            if not pkg.is_dir():
                continue
            target = skills_dir / src_scope / pkg.name
            if target.exists():
                shutil.rmtree(target)
            shutil.copytree(pkg, target)
            stats["from_package"] += 1

    # 2. 根目录 flat .skill 文件：补充或创建目录
    for skill_file in sorted(V7_ROOT.glob("*.skill")):
        name = skill_file.stem
        scope = skill_scope(name)
        target_dir = skills_dir / scope / name
        target_dir.mkdir(parents=True, exist_ok=True)
        if (target_dir / "SKILL.md").exists():
            # 保留目录包的 SKILL.md，把 flat 文件作为补充
            shutil.copy2(skill_file, target_dir / "SKILL-root.md")
            stats["merged"] += 1
        else:
            shutil.copy2(skill_file, target_dir / "SKILL.md")
            stats["from_flat"] += 1

    # 3. 其他协议级文件
    for py_file in ("content_sovereignty_protocol_v2.1.py",):
        src = V7_ROOT / py_file
        if src.exists():
            target_dir = skills_dir / "protocol" / src.stem
            target_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target_dir / py_file)
            stats["from_flat"] += 1

    log(f"技能整理完成: 目录包 {stats['from_package']}, flat {stats['from_flat']}, 合并 {stats['merged']}")
    return stats


def write_registry():
    skills_dir = V7_ROOT / "skills"
    registry = []
    for scope in ("local", "cloud", "protocol"):
        scope_dir = skills_dir / scope
        if not scope_dir.exists():
            continue
        for skill_dir in sorted(scope_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            desc = ""
            keywords = []
            if skill_md.exists():
                text = skill_md.read_text(encoding="utf-8", errors="ignore")[:2000]
                for line in text.splitlines()[:20]:
                    if line.strip().startswith("description:") or line.strip().startswith(">"):
                        desc = line.split(">", 1)[-1].strip()[:120]
                        break
            registry.append({
                "name": skill_dir.name,
                "scope": scope,
                "path": str(skill_dir.relative_to(V7_ROOT)),
                "description": desc,
                "keywords": keywords,
            })
    reg_file = skills_dir / "registry.json"
    reg_file.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"生成技能注册表: {reg_file} ({len(registry)} 个)")
    return len(registry)


def create_launcher():
    # 直接基于 v6 启动器代码，替换版本与路径
    launcher_src = Path("/Users/zuimeidedeyihan/Downloads/Kimi_Agent_终端升级与结构优化 6/longhun-v6-launcher.py")
    if launcher_src.exists():
        code = launcher_src.read_text(encoding="utf-8")
        code = code.replace("V6_ROOT = Path(__file__).resolve().parent", "V7_ROOT = Path(__file__).resolve().parent")
        code = code.replace("V6_ROOT", "V7_ROOT")
        code = code.replace("龍魂 v6 总控启动器", "龍魂 v7 总控启动器")
        code = code.replace("LAUNCHER-v6.1", "LAUNCHER-v7.0")
        code = code.replace("v6 根目录", "v7 根目录")
        code = code.replace("v6 总控启动器", "v7 总控启动器")
        code = code.replace('prog="longhun-v6-launcher.py"', 'prog="longhun-v7-launcher.py"')
        code = code.replace('description="龍魂 v6 总控启动器"', 'description="龍魂 v7 总控启动器"')
    else:
        # fallback 极简启动器
        code = f'''#!/usr/bin/env python3
# fallback launcher
import subprocess, sys
print("请确认 v6 启动器存在")
'''
    launcher_path = V7_ROOT / "longhun-v7-launcher.py"
    launcher_path.write_text(code, encoding="utf-8")
    launcher_path.chmod(0o755)
    log(f"创建启动器: {launcher_path}")


def import_new_files():
    IMPORT_DIR.mkdir(parents=True, exist_ok=True)
    copied = []
    for name in ("守护进程管理器_逐行注释版.py", "baobao_workflow_v2.0.py", "cnsh_aligner_v2.0.py",
                 "cnsh_editor_engine_v2.0.py", "cnsh_translator_engine_v2.0.py",
                 "longhun_file_audit_foundation_v2.0.py", "longhun_foundation_launcher_v2.0.py",
                 "longhun_lineage_verification_v2.0.py", "longhun_mvp_executor_v2.0.py",
                 "longhun_mvp_launcher_v2.0.py", "longhun_mvp_notion_integration_v2.0.py",
                 "longhun_mvp_setup_integration_v2.0.py", "longhun_script_manager_v2.0.py"):
        src = V7_ROOT / name
        if src.exists():
            dst = IMPORT_DIR / name
            shutil.copy2(src, dst)
            copied.append(name)
    log(f"导入新文件到主干: {len(copied)} 个 -> {IMPORT_DIR}")
    return copied


def update_cnsh_link(report: dict):
    old_target = None
    if CNSH_LINK.is_symlink():
        old_target = os.readlink(str(CNSH_LINK))
        CNSH_LINK.unlink()
    elif CNSH_LINK.exists():
        old_target = str(CNSH_LINK)
        CNSH_LINK.unlink()
    new_target = V7_ROOT / "CNSH"
    CNSH_LINK.symlink_to(new_target, target_is_directory=True)
    report["cnsh_old_target"] = old_target
    report["cnsh_new_target"] = str(new_target)
    log(f"CNSH 软链接更新: {old_target} -> {new_target}")


def sync_skills(report: dict):
    skills_dir = V7_ROOT / "skills"
    installed, skipped = [], []
    for scope in ("local", "cloud", "protocol"):
        scope_dir = skills_dir / scope
        if not scope_dir.exists():
            continue
        for skill_dir in sorted(scope_dir.iterdir()):
            if not skill_dir.is_dir():
                continue
            name = skill_dir.name
            target = USER_SKILLS_DIR / name
            if target.exists():
                skipped.append(name)
                continue
            shutil.copytree(skill_dir, target)
            installed.append(name)
    report["skills_installed"] = installed
    report["skills_skipped"] = skipped
    log(f"同步技能: 新增 {len(installed)}, 跳过 {len(skipped)}")


def update_shell_rc(report: dict):
    old_path = "/Users/zuimeidedeyihan/Downloads/Kimi_Agent_终端升级与结构优化 6"
    new_path = str(V7_ROOT)
    for rc in (Path.home() / ".zshrc", Path.home() / ".bashrc"):
        if not rc.exists():
            continue
        text = rc.read_text(encoding="utf-8")
        # 更新路径
        text = text.replace(old_path, new_path)
        # 别名版本号升级
        text = text.replace("alias lh6=", "alias lh7=")
        text = text.replace("alias longhun6=", "alias longhun7=")
        text = text.replace("alias 龍魂6=", "alias 龍魂7=")
        text = text.replace("lh6 status", "lh7 status")
        text = text.replace("lh6 ops", "lh7 ops")
        text = text.replace("lh6 portal", "lh7 portal")
        text = text.replace("lh6 cnsh", "lh7 cnsh")
        text = text.replace("🐉 龍魂 v6 ·", "🐉 龍魂 v7 ·")
        text = text.replace("龍魂 v6 总控启动器", "龍魂 v7 总控启动器")
        rc.write_text(text, encoding="utf-8")
        log(f"更新 shell 配置: {rc}")
    report["shell_rc_updated"] = True


def run_memory_bootstrap(report: dict):
    script = None
    for cand in MEMORY_SCRIPT_CANDIDATES:
        if cand.exists():
            script = cand
            break
    if not script:
        report["memory_bootstrap"] = "not found"
        log("未找到记忆启动脚本")
        return
    log(f"运行记忆启动器: {script}")
    try:
        result = subprocess.run([sys.executable, str(script)], capture_output=True, text=True, timeout=120)
        report["memory_bootstrap"] = {"returncode": result.returncode, "stdout_tail": result.stdout[-500:], "stderr_tail": result.stderr[-300:]}
        log(f"记忆启动器返回: {result.returncode}")
    except Exception as e:
        report["memory_bootstrap"] = f"error: {e}"
        log(f"记忆启动器异常: {e}")


def write_report(report: dict):
    lines = [
        "# 🐉 龍魂 v7 主干升级报告",
        "",
        f"**DNA**: {report['dna']}",
        f"**时间**: {datetime.now(timezone.utc).isoformat()}",
        f"**v7 包**: {V7_ROOT}",
        "",
        "## 执行摘要",
        "",
        f"- 清理垃圾: 完成",
        f"- 技能整理: 目录包 {report['skill_stats']['from_package']}, flat {report['skill_stats']['from_flat']}, 合并 {report['skill_stats']['merged']}",
        f"- 技能注册表: {report['registry_count']} 个",
        f"- 新文件导入: {len(report['imported_files'])} 个 -> `{IMPORT_DIR}`",
        f"- CNSH 软链接: `{report['cnsh_old_target']}` -> `{report['cnsh_new_target']}`",
        f"- 技能同步: 新增 {len(report['skills_installed'])}, 跳过 {len(report['skills_skipped'])}",
        f"- shell 配置: 已更新",
        "",
        "## 新增技能",
        "",
    ]
    for name in report["skills_installed"]:
        lines.append(f"- `{name}`")
    lines += ["", "## 导入的新文件", ""]
    for name in report["imported_files"]:
        lines.append(f"- `{name}`")
    lines += ["", "## 记忆启动器", "", f"```\n{report['memory_bootstrap']}\n```"]
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    log(f"报告已生成: {REPORT_PATH}")


def main():
    dna = make_dna("MAIN")
    print(f"🐉 龍魂 v7 主干升级编排器启动")
    print(f"   DNA: {dna}")
    print(f"   v7 包: {V7_ROOT}")

    if not V7_ROOT.exists():
        print(f"错误：v7 包不存在: {V7_ROOT}")
        return 1

    report = {"dna": dna}

    clean_pycache(V7_ROOT)
    report["skill_stats"] = organize_skills()
    report["registry_count"] = write_registry()
    create_launcher()
    report["imported_files"] = import_new_files()
    update_cnsh_link(report)
    sync_skills(report)
    update_shell_rc(report)
    run_memory_bootstrap(report)
    write_report(report)

    print("\n✅ 龍魂 v7 主干升级完成")
    print(f"   新启动器: {V7_ROOT / 'longhun-v7-launcher.py'}")
    print(f"   CNSH 指向: {CNSH_LINK} -> {os.readlink(str(CNSH_LINK))}")
    print(f"   报告: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
