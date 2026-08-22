#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
公开工具箱完整性检查器
DNA: #龍芯⚡️丙午·甲午·辛未·甲午·䷖剥-LONGHUN-PUBLIC-TOOLBOX-VALIDATOR-v1.0

检查项：
1. PUBLIC_TOOLBOX_README.md 中所有相对链接指向的文件/目录存在
2. 核心模块速览中的目录存在
3. 快速开始中引用的示例文件存在
4. _quarantine 隔离区存在且包含外部导入目录
5. 公开文件中无明显硬编码密钥/Token
6. CNSH 示例脚本可运行
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "PUBLIC_TOOLBOX_README.md"

SECRET_PATTERNS = [
    re.compile(r"api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.IGNORECASE),
    re.compile(r"token\s*[:=]\s*['\"][^'\"]{8,}['\"]", re.IGNORECASE),
    re.compile(r"password\s*[:=]\s*['\"][^'\"]{6,}['\"]", re.IGNORECASE),
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"Bearer\s+[a-zA-Z0-9_\-\.]{20,}"),
]


def check_links():
    """检查 README 中所有相对 markdown 链接"""
    text = README.read_text(encoding="utf-8", errors="ignore")
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", text)
    broken = []
    checked = set()
    for label, target in links:
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        # 锚点
        if "#" in target:
            target = target.split("#", 1)[0]
        if not target:
            continue
        path = ROOT / target
        key = str(path)
        if key in checked:
            continue
        checked.add(key)
        if not path.exists():
            broken.append((label, target))
    return broken


def check_core_modules():
    """检查核心模块速览中提到的目录"""
    modules = [
        "dev-env/chinese-editor",
        "cnsh-core",
        "01_技能库",
        "scripts",
        "multicurrency",
        "xpay",
        "sovereignty",
        "01_技能库/longhun-zeng-digital-human",
        "_quarantine",
    ]
    missing = [m for m in modules if not (ROOT / m).exists()]
    return missing


def check_quickstart_files():
    files = [
        "dev-env/chinese-editor/examples/hello.cnsh",
    ]
    missing = [f for f in files if not (ROOT / f).exists()]
    return missing


def check_quarantine():
    q = ROOT / "_quarantine"
    if not q.exists():
        return ["_quarantine 目录不存在"]
    expected = q / "Kimi_Agent_龍魂協議自動化完成"
    if not expected.exists():
        return ["_quarantine/Kimi_Agent_龍魂協議自動化完成 不存在"]
    return []


def check_secrets():
    """扫描公开README和中文编辑器包中的疑似密钥"""
    suspects = []
    scan_files = [
        README,
        ROOT / "dev-env/chinese-editor/README.md",
        ROOT / "dev-env/chinese-editor/pyproject.toml",
        ROOT / "dev-env/chinese-editor/src/longhun_chinese_editor/cli.py",
        ROOT / "dev-env/chinese-editor/src/longhun_chinese_editor/runtime.py",
        ROOT / "dev-env/chinese-editor/src/longhun_chinese_editor/editor.py",
    ]
    for f in scan_files:
        if not f.exists():
            continue
        text = f.read_text(encoding="utf-8", errors="ignore")
        for pat in SECRET_PATTERNS:
            for m in pat.finditer(text):
                line = text[: m.start()].count("\n") + 1
                suspects.append(f"{f.relative_to(ROOT)}:{line}: {m.group(0)[:60]}")
    return suspects


def check_examples_run():
    """运行 CNSH 示例"""
    examples_dir = ROOT / "dev-env/chinese-editor/examples"
    results = []
    for ex in ["hello.cnsh", "loops.cnsh", "test_full.cnsh"]:
        path = examples_dir / ex
        if not path.exists():
            results.append((ex, False, "文件不存在"))
            continue
        proc = subprocess.run(
            [sys.executable, str(ROOT / "dev-env/chinese-editor/scripts/cnsh_runtime.py"), str(path)],
            capture_output=True,
            text=True,
        )
        results.append((ex, proc.returncode == 0, proc.stderr or proc.stdout[-200:]))
    return results


def main():
    print("🐉 龍魂公开工具箱完整性检查")
    print("-" * 50)

    broken_links = check_links()
    print(f"🔗 README 相对链接: {len(broken_links)} 个失效")
    for label, target in broken_links[:20]:
        print(f"   ❌ [{label}] -> {target}")
    if len(broken_links) > 20:
        print(f"   ... 还有 {len(broken_links) - 20} 个")

    missing_modules = check_core_modules()
    print(f"\n📦 核心模块目录缺失: {len(missing_modules)} 个")
    for m in missing_modules:
        print(f"   ❌ {m}")

    missing_qs = check_quickstart_files()
    print(f"\n🚀 快速开始文件缺失: {len(missing_qs)} 个")
    for f in missing_qs:
        print(f"   ❌ {f}")

    quarantine_issues = check_quarantine()
    print(f"\n🛡️ 隔离区检查问题: {len(quarantine_issues)} 个")
    for issue in quarantine_issues:
        print(f"   ❌ {issue}")

    secrets = check_secrets()
    print(f"\n🔑 疑似硬编码密钥: {len(secrets)} 处")
    for s in secrets[:10]:
        print(f"   ⚠️  {s}")
    if len(secrets) > 10:
        print(f"   ... 还有 {len(secrets) - 10} 处")

    examples = check_examples_run()
    print(f"\n📜 CNSH 示例运行:")
    for name, ok, detail in examples:
        print(f"   {'✅' if ok else '❌'} {name}")
        if not ok:
            print(f"      {detail}")

    all_ok = (
        not broken_links
        and not missing_modules
        and not missing_qs
        and not quarantine_issues
        and not secrets
        and all(ok for _, ok, _ in examples)
    )

    print("-" * 50)
    if all_ok:
        print("✅ 公开工具箱完整性检查通过")
        return 0
    else:
        print("🔴 公开工具箱完整性检查未通过，请修复上述问题")
        return 1


if __name__ == "__main__":
    sys.exit(main())
