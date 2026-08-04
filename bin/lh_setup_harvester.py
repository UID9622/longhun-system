#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 知识拉取器一键配置引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·乙巳·辛巳·☴巽-SETUP-HARVEST-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

功能：
  - 自动检查/创建 .env 文件
  - 交互式填入 NOTION_API_KEY、NOTION_DATABASE_ID、CSDN_USERNAME
  - 自动安装 notion-client（可选）
  - 执行知识拉取
  - 自动打开 MISSING_MODULES.md 供审查
  - 生成审计日志

用法：
  lh 配置拉取器

确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict

# ============================================================
# 配置
# ============================================================

PROJECT_ROOT = Path.home() / "longhun-system"
ENV_FILE = PROJECT_ROOT / ".env"
HARVESTER_SCRIPT = PROJECT_ROOT / "bin" / "lh_knowledge_harvester.py"
OUTPUT_DIR = PROJECT_ROOT / "data" / "harvested_knowledge"
MISSING_MODULE_FILE = OUTPUT_DIR / "MISSING_MODULES.md"


# ============================================================
# 核心功能
# ============================================================

def ensure_env_file() -> Dict[str, str]:
    """检查 .env 文件，缺失则创建并提示用户填写"""
    env_vars: Dict[str, str] = {}

    if ENV_FILE.exists():
        for line in ENV_FILE.read_text().split("\n"):
            line = line.strip()
            if line and not line.startswith('#'):
                key, _, value = line.partition('=')
                env_vars[key.strip()] = value.strip().strip('"').strip("'")

    required = {
        "NOTION_API_KEY": "Notion API 密钥 (https://www.notion.so/my-integrations)",
        "NOTION_DATABASE_ID": "Notion 数据库 ID (从数据库 URL 获取)",
        "CSDN_USERNAME": "CSDN 用户名",
    }

    changed = False
    for key, desc in required.items():
        if key not in env_vars or not env_vars[key]:
            value = input(f"\n🔑 请输入 {key} ({desc}): ").strip()
            if value:
                env_vars[key] = value
                changed = True
            else:
                print(f"⚠️ {key} 未填写，相关来源将跳过")

    if changed:
        lines = [
            "# 龍魂系统环境变量",
            f"# 生成时间: {datetime.now().isoformat()}",
            "",
        ]
        for key, value in env_vars.items():
            lines.append(f'{key}="{value}"')
        ENV_FILE.write_text("\n".join(lines) + "\n")
        print(f"\n✅ .env 文件已更新: {ENV_FILE}")

    return env_vars


def install_dependencies() -> bool:
    """安装 notion-client（可选）"""
    try:
        import notion_client  # noqa: F401
        print("✅ notion-client 已安装")
        return True
    except ImportError:
        ans = input("\n📦 是否安装 notion-client (用于 Notion API 拉取)？ [y/N]: ").strip().lower()
        if ans in ('y', 'yes'):
            print("⏳ 正在安装 notion-client...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "notion-client"],
                    check=True,
                )
                print("✅ notion-client 安装成功")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ 安装失败: {e}")
                return False
        else:
            print("⏭️ 跳过 notion-client 安装")
            return False


def run_harvester() -> bool:
    """执行知识拉取"""
    if not HARVESTER_SCRIPT.exists():
        print(f"❌ 未找到拉取器: {HARVESTER_SCRIPT}")
        return False

    print("\n🚀 开始执行知识拉取...\n")
    try:
        subprocess.run(
            [sys.executable, str(HARVESTER_SCRIPT), "--force"],
            check=True,
        )
        print("\n✅ 知识拉取完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ 知识拉取失败: {e}")
        return False


def review_missing_modules():
    """打开 MISSING_MODULES.md 供审查"""
    if not MISSING_MODULE_FILE.exists():
        print(f"\n⚠️ 未找到 MISSING_MODULES.md，可能未生成或拉取失败")
        return

    print(f"\n📄 已生成缺失模块建议: {MISSING_MODULE_FILE}")

    try:
        if sys.platform == 'darwin':
            subprocess.run(['open', str(MISSING_MODULE_FILE)])
        elif sys.platform == 'win32':
            os.startfile(str(MISSING_MODULE_FILE))
        else:
            subprocess.run(['xdg-open', str(MISSING_MODULE_FILE)])
        print("✅ 已用默认编辑器打开文件")
    except Exception:
        print(f"⚠️ 请手动查看: {MISSING_MODULE_FILE}")
        content = MISSING_MODULE_FILE.read_text()
        lines = content.split("\n")
        print("\n--- 文件预览 (前20行) ---")
        for line in lines[:20]:
            print(line.rstrip())
        if len(lines) > 20:
            print(f"... (共 {len(lines)} 行)")


def generate_audit_log():
    """生成审计日志"""
    log_dir = PROJECT_ROOT / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = log_dir / f"harvester_setup_{ts}.log"
    log_file.write_text("\n".join([
        "🐉 龙魂知识拉取器配置日志",
        f"时间: {datetime.now().isoformat()}",
        f"DNA: #龍芯⚡️{ts}-SETUP-UID9622",
        f"NOTION_API_KEY: {'已设置' if os.getenv('NOTION_API_KEY') else '未设置'}",
        f"NOTION_DATABASE_ID: {'已设置' if os.getenv('NOTION_DATABASE_ID') else '未设置'}",
        f"CSDN_USERNAME: {'已设置' if os.getenv('CSDN_USERNAME') else '未设置'}",
        f"拉取器脚本: {'存在' if HARVESTER_SCRIPT.exists() else '不存在'}",
        f"输出目录: {OUTPUT_DIR}",
        f"MISSING_MODULES: {'存在' if MISSING_MODULE_FILE.exists() else '不存在'}",
        "",
    ]))
    print(f"\n📋 审计日志已保存: {log_file}")


# ============================================================
# 主入口
# ============================================================

def main():
    print("🐉 龍魂 · 知识拉取器一键配置\n")
    print("确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z\n")

    # 1. 补全环境变量
    env_vars = ensure_env_file()
    for key, value in env_vars.items():
        os.environ[key] = value

    # 2. 安装依赖
    install_dependencies()

    # 3. 执行拉取
    if not run_harvester():
        print("\n⚠️ 知识拉取可能未完整执行，请检查错误信息")
        generate_audit_log()
        sys.exit(1)

    # 4. 审查缺失模块
    review_missing_modules()

    # 5. 审计日志
    generate_audit_log()

    print("\n🎉 全部完成！接下来请查看 MISSING_MODULES.md，按建议补全代码。")
    print("   🛠️  您也可以手动运行: lh 知识拉取 --source notion/csdn/local/notes/ai")


if __name__ == "__main__":
    main()
