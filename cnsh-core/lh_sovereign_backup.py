#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 私云归藏备份
DNA: #龍芯⚡️2026-06-29-LONGHUN-SOVEREIGN-BACKUP-v1.0

把核心主权数据打包、用 GPG 对称加密，存到本地备份目录。
云端只做可断开的镜像，本地才是根。
"""
import argparse
import json
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from cnsh_unified import 系统路径, DNA工具

# 备份来源：核心主权数据
DEFAULT_SOURCES = [
    "~/.longhun/memory",
    "~/.longhun/multi-ai-gateway",
    "~/.dragonsoul",
    "~/.cnsh",
    "~/.龍魂",
    "~/_work/dragon_knowledge.db",
    "~/longhun-system/cnsh-core",
]

BACKUP_ROOT = 系统路径.龍魂系统根目录() / "backups" / "sovereign"
REPORT_PATH = 系统路径.工作数据目录() / "sovereign_backup_report.json"


def 生成DNA(标签: str) -> str:
    return DNA工具.生成(f"SOVEREIGN-BACKUP-{标签}", "1.0")


def 打包并加密(来源列表: list[Any], 输出目录: Path, 密码: str) -> dict[str, Any]:
    输出目录 = Path(输出目录)
    输出目录.mkdir(parents=True, exist_ok=True)
    时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    包名 = f"longhun-sovereign-{时间戳}.tar.gz"
    包路径 = 输出目录 / 包名
    加密路径 = 输出目录 / f"{包名}.gpg"

    # 1. 收集存在的来源
    存在来源 = []
    for s in 来源列表:
        p = Path(s).expanduser()
        if p.exists():
            存在来源.append(str(p))
        else:
            print(f"⚠️ 来源不存在，跳过: {p}")

    if not 存在来源:
        return {"成功": False, "原因": "没有可用的备份来源"}

    # 2. tar.gz 打包（用 bsdtar 兼容语法，遇到无权限目录跳过）
    try:
        result = subprocess.run(
            ["tar", "-czf", str(包路径), "--exclude", ".DS_Store", "--exclude", "__pycache__", "--exclude", "node_modules"] + 存在来源,
            check=False,
            capture_output=True,
            text=True,
        )
        # bsdtar 可能部分报错但仍生成文件
        if not 包路径.exists():
            return {"成功": False, "原因": f"打包后未生成文件: {result.stderr}"}
    except subprocess.CalledProcessError as e:
        return {"成功": False, "原因": f"打包失败: {e.stderr}"}

    # 3. GPG 对称加密
    try:
        subprocess.run(
            [
                "gpg", "--batch", "--yes", "--passphrase-fd", "0",
                "--symmetric", "--cipher-algo", "AES256",
                "--output", str(加密路径), str(包路径),
            ],
            input=密码,
            check=True,
            capture_output=True,
            text=True,
        )
        # 删除未加密的 tar.gz
        包路径.unlink()
    except subprocess.CalledProcessError as e:
        return {"成功": False, "原因": f"加密失败: {e.stderr}"}

    大小 = 加密路径.stat().st_size
    dna = 生成DNA(时间戳)
    return {
        "成功": True,
        "包路径": str(加密路径),
        "大小": 大小,
        "来源数": len(存在来源),
        "时间": datetime.now(timezone.utc).isoformat(),
        "dna": dna,
    }


def 解密(加密文件: Path, 输出目录: Path, 密码: str) -> dict[str, Any]:
    加密文件 = Path(加密文件)
    输出目录 = Path(输出目录)
    输出目录.mkdir(parents=True, exist_ok=True)
    解密包 = 输出目录 / 加密文件.name.replace(".gpg", "")
    try:
        subprocess.run(
            [
                "gpg", "--batch", "--yes", "--passphrase-fd", "0",
                "--decrypt", "--output", str(解密包), str(加密文件),
            ],
            input=密码,
            check=True,
            capture_output=True,
            text=True,
        )
        return {"成功": True, "解密包": str(解密包)}
    except subprocess.CalledProcessError as e:
        return {"成功": False, "原因": f"解密失败: {e.stderr}"}


def 清理旧备份(输出目录: Path, 保留份数: int = 7):
    files = sorted(
        [f for f in Path(输出目录).glob("longhun-sovereign-*.tar.gz.gpg")],
        key=lambda p: p.stat().st_mtime,
    )
    if len(files) > 保留份数:
        for f in files[:-保留份数]:
            f.unlink()
            print(f"🗑 清理旧备份: {f.name}")


def 主函数():
    parser = argparse.ArgumentParser(description="龍魂私云归藏备份")
    parser.add_argument("--password", "-p", help="加密密码（未提供则尝试环境变量 LONGHUN_BACKUP_PASSWORD）")
    parser.add_argument("--output", "-o", default=str(BACKUP_ROOT), help="备份输出目录")
    parser.add_argument("--sources", "-s", nargs="+", default=DEFAULT_SOURCES, help="备份来源")
    parser.add_argument("--decrypt", "-d", help="解密指定 .gpg 文件")
    parser.add_argument("--decrypt-output", default=str(BACKUP_ROOT / "decrypted"), help="解密输出目录")
    parser.add_argument("--keep", type=int, default=7, help="保留最近几份备份")
    args = parser.parse_args()

    密码 = args.password or os.environ.get("LONGHUN_BACKUP_PASSWORD")
    if not 密码:
        print("❌ 必须提供 --password 或设置环境变量 LONGHUN_BACKUP_PASSWORD")
        sys.exit(1)

    if args.decrypt:
        result = 解密(args.decrypt, args.decrypt_output, 密码)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    result = 打包并加密(args.sources, args.output, 密码)
    if result["成功"]:
        清理旧备份(Path(args.output), args.keep)
        print(f"✅ 备份成功")
        print(f"  文件: {result['包路径']}")
        print(f"  大小: {result['大小'] / 1024 / 1024:.2f} MB")
        print(f"  来源: {result['来源数']} 个")
        print(f"  DNA: {result['dna']}")
    else:
        print(f"❌ 备份失败: {result['原因']}")
        sys.exit(1)

    # 写报告
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    import os
    主函数()
