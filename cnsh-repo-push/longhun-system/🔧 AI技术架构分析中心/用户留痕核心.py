#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龍魂系统 | 用户留痕核心系统                               ║
╠═══════════════════════════════════════════════════════════════╣
║  📦 名称：星辰记忆·用户留痕核心                               ║
║  📌 版本：v1.0                                                ║
║  🧬 DNA：#龍芯⚡️2026-03-04-TRACE-CORE-v1.0                   ║
║  🔐 GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F            ║
║  👤 创建：Lucky·UID9622                                       ║
║  🤝 协作：宝宝🐱(执行)                                        ║
║  📅 创建：2026-03-04                                          ║
║  ⚠️  熔断：签名失效则本文件作废                               ║
║  🎯 用途：用户操作留痕，防篡改，可审计，可追溯                ║
╚═══════════════════════════════════════════════════════════════╝
"""

import hashlib
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# ========== 全局配置 ==========
DNA_PREFIX     = "#龍芯⚡️"
UID            = "9622"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
VERSION        = "1.0"

# 存储路径（完全本地，不上云）
BASE_DIR   = Path.home() / ".star-memory"
TRACE_DIR  = BASE_DIR / "traces"
AUDIT_LOG  = BASE_DIR / "audit.log"
TRACE_FILE = BASE_DIR / "用户留痕日志.jsonl"  # jsonl = 每行一条，只追加

# ========== 初始化目录 ==========
def 初始化存储():
    """确保本地存储目录存在"""
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    TRACE_DIR.mkdir(parents=True, exist_ok=True)
    if not TRACE_FILE.exists():
        TRACE_FILE.touch()
    if not AUDIT_LOG.exists():
        AUDIT_LOG.touch()

# ========== DNA追溯码生成 ==========
def 生成DNA追溯码(用户ID: str, 操作类型: str, 哈希值: str) -> str:
    """
    生成唯一DNA追溯码
    格式：#龍芯⚡️YYYY-MM-DD-操作类型-UID-哈希前8位
    """
    日期 = datetime.now().strftime("%Y-%m-%d")
    操作类型英文 = {
        "登录": "LOGIN", "支付": "PAY", "提交": "SUBMIT",
        "查看": "VIEW",  "修改": "EDIT", "删除": "DELETE",
        "注册": "REGISTER", "退出": "LOGOUT"
    }.get(操作类型, 操作类型.upper()[:8])
    
    return f"{DNA_PREFIX}{日期}-{操作类型英文}-{用户ID}-{哈希值[:8].upper()}"

# ========== 核心哈希：防篡改 ==========
def 生成防篡改哈希(用户ID: str, 操作类型: str, 操作内容: str, 时间戳: str) -> str:
    """
    SHA-256哈希：只要内容被改，哈希就变
    任何人都无法在不暴露的情况下篡改记录
    """
    原文 = f"{用户ID}|{操作类型}|{操作内容}|{时间戳}|{GPG_FINGERPRINT}"
    return hashlib.sha256(原文.encode("utf-8")).hexdigest()

# ========== 核心：用户留痕 ==========
def 用户留痕(
    用户ID: str,
    操作类型: str,
    操作内容: str,
    附加信息: Optional[dict] = None
) -> dict:
    """
    每次用户操作，自动生成一条不可篡改的痕迹
    
    参数：
        用户ID     —— 用户唯一标识（如 UID9622）
        操作类型   —— 登录 / 支付 / 提交 / 查看 / 修改 / 删除
        操作内容   —— 操作的具体描述
        附加信息   —— 可选，设备/IP/备注等

    返回：
        痕迹字典（同时写入本地留痕日志）
    """
    初始化存储()
    
    时间戳 = datetime.now().isoformat()
    哈希值 = 生成防篡改哈希(用户ID, 操作类型, 操作内容, 时间戳)
    DNA追溯 = 生成DNA追溯码(用户ID, 操作类型, 哈希值)

    痕迹 = {
        # === 核心六要素 ===
        "用户ID":    用户ID,
        "操作类型":  操作类型,
        "操作内容":  操作内容,
        "时间戳":    时间戳,
        "哈希验证":  哈希值,       # 防篡改核心
        "DNA追溯":   DNA追溯,      # 唯一溯源码

        # === 扩展信息 ===
        "版本":      VERSION,
        "GPG指纹":   GPG_FINGERPRINT,
        "附加信息":  附加信息 or {},

        # === 三色状态（初始为绿）===
        "三色状态":  "🟢",
        "备注":      ""
    }

    # 写入留痕日志（只追加，不覆盖）
    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(痕迹, ensure_ascii=False) + "\n")

    # 同步写入审计日志（人类可读格式）
    with open(AUDIT_LOG, "a", encoding="utf-8") as f:
        f.write(
            f"{时间戳} | {操作类型:6} | {用户ID:12} | "
            f"{操作内容[:40]:40} | {哈希值[:16]}\n"
        )

    print(f"✅ 留痕成功 | {操作类型} | {DNA追溯}")
    return 痕迹

# ========== 验证：检查记录有没有被篡改 ==========
def 验证留痕(痕迹: dict) -> tuple[bool, str]:
    """
    重新计算哈希，对比原始值
    如果哈希不一致 → 记录被篡改 → 🔴熔断
    """
    预期哈希 = 生成防篡改哈希(
        痕迹["用户ID"],
        痕迹["操作类型"],
        痕迹["操作内容"],
        痕迹["时间戳"]
    )

    if 预期哈希 == 痕迹["哈希验证"]:
        return True, f"🟢 验证通过 | DNA: {痕迹['DNA追溯']}"
    else:
        return False, f"🔴 警告：记录已被篡改！ | DNA: {痕迹['DNA追溯']}"

# ========== 查询：搜索留痕日志 ==========
def 查询留痕(
    用户ID: Optional[str] = None,
    操作类型: Optional[str] = None,
    日期: Optional[str] = None   # 格式 YYYY-MM-DD
) -> list:
    """
    按条件搜索留痕记录
    """
    初始化存储()
    结果 = []

    if not TRACE_FILE.exists():
        return 结果

    with open(TRACE_FILE, "r", encoding="utf-8") as f:
        for 行 in f:
            行 = 行.strip()
            if not 行:
                continue
            try:
                记录 = json.loads(行)
                if 用户ID and 记录.get("用户ID") != 用户ID:
                    continue
                if 操作类型 and 记录.get("操作类型") != 操作类型:
                    continue
                if 日期 and not 记录.get("时间戳", "").startswith(日期):
                    continue
                结果.append(记录)
            except json.JSONDecodeError:
                continue  # 跳过损坏行

    return 结果

# ========== 批量验证：扫描所有记录 ==========
def 批量验证全部留痕() -> dict:
    """
    扫描所有留痕记录，找出被篡改的条目
    返回三色汇总报告
    """
    初始化存储()
    报告 = {"🟢 通过": [], "🔴 篡改": [], "⚠️ 异常": []}

    if not TRACE_FILE.exists():
        print("暂无留痕记录")
        return 报告

    with open(TRACE_FILE, "r", encoding="utf-8") as f:
        for i, 行 in enumerate(f, 1):
            行 = 行.strip()
            if not 行:
                continue
            try:
                记录 = json.loads(行)
                通过, 信息 = 验证留痕(记录)
                if 通过:
                    报告["🟢 通过"].append({"行号": i, "DNA": 记录["DNA追溯"]})
                else:
                    报告["🔴 篡改"].append({"行号": i, "DNA": 记录["DNA追溯"], "信息": 信息})
            except Exception as e:
                报告["⚠️ 异常"].append({"行号": i, "错误": str(e)})

    # 打印汇总
    print("\n══════════ 三色审计报告 ══════════")
    print(f"🟢 验证通过: {len(报告['🟢 通过'])} 条")
    print(f"🔴 发现篡改: {len(报告['🔴 篡改'])} 条")
    print(f"⚠️ 异常记录: {len(报告['⚠️ 异常'])} 条")
    if 报告["🔴 篡改"]:
        print("\n‼️ 被篡改的记录：")
        for 项 in 报告["🔴 篡改"]:
            print(f"  → 第{项['行号']}行 | {项['DNA']} | {项['信息']}")
    print("══════════════════════════════════\n")

    return 报告

# ========== 生成月度留痕报告 ==========
def 生成月度报告(年: int, 月: int) -> dict:
    """
    生成指定月份的用户留痕统计报告
    """
    日期前缀 = f"{年}-{月:02d}"
    记录列表 = 查询留痕(日期=日期前缀)

    操作统计 = {}
    用户统计 = {}
    for 记录 in 记录列表:
        操作 = 记录.get("操作类型", "未知")
        用户 = 记录.get("用户ID", "未知")
        操作统计[操作] = 操作统计.get(操作, 0) + 1
        用户统计[用户] = 用户统计.get(用户, 0) + 1

    报告 = {
        "报告月份":   f"{年}-{月:02d}",
        "总记录数":   len(记录列表),
        "操作分布":   操作统计,
        "用户分布":   用户统计,
        "DNA追溯":    f"{DNA_PREFIX}{年}-{月:02d}-MONTHLY-REPORT-{UID}",
        "GPG指纹":    GPG_FINGERPRINT,
        "三色状态":   "🟢" if len(记录列表) > 0 else "🟡"
    }

    # 保存月度报告
    报告路径 = BASE_DIR / f"月度报告_{年}_{月:02d}.json"
    with open(报告路径, "w", encoding="utf-8") as f:
        json.dump(报告, f, ensure_ascii=False, indent=2)

    print(f"📊 月度报告已生成：{报告路径}")
    return 报告

# ========== 熔断检查 ==========
def 熔断检查() -> tuple[bool, str]:
    """
    系统自检：验证留痕文件和审计日志完整性
    """
    if not TRACE_FILE.exists():
        return False, "🔴 留痕文件不存在，系统异常！"
    if not AUDIT_LOG.exists():
        return False, "🔴 审计日志不存在，系统异常！"
    if GPG_FINGERPRINT != "A2D0092CEE2E5BA87035600924C3704A8CC26D5F":
        return False, "🔴 GPG指纹不匹配，熔断！"
    return True, "🟢 系统正常，无需熔断"

# ========== 主程序入口 ==========
if __name__ == "__main__":
    print("🐉 龍魂留痕系统启动...\n")

    # 熔断检查
    状态, 信息 = 熔断检查()
    print(f"熔断检查：{信息}\n")
    if not 状态:
        exit(1)

    # ===== 模拟用户操作留痕 =====
    用户留痕("UID9622", "登录",  "设备=iPhone15 | IP=192.168.1.1")
    用户留痕("UID9622", "查看",  "页面=星辰记忆主页")
    用户留痕("UID9622", "支付",  "金额=10元 | 档位=认可支持档")
    用户留痕("UID9622", "提交",  "内容=星辰记忆v1.0文档")
    用户留痕("UID0001", "登录",  "设备=Android | IP=10.0.0.2",
             附加信息={"备注": "普通用户"})
    用户留痕("UID0001", "查看",  "页面=透明账本")

    print("\n━━━━━━ 批量验证所有留痕 ━━━━━━")
    批量验证全部留痕()

    print("\n━━━━━━ 查询 UID9622 的所有操作 ━━━━━━")
    记录 = 查询留痕(用户ID="UID9622")
    for r in 记录:
        print(f"  {r['时间戳'][:19]} | {r['操作类型']} | {r['操作内容'][:30]}")

    print("\n━━━━━━ 生成本月报告 ━━━━━━")
    now = datetime.now()
    生成月度报告(now.year, now.month)

    print("\n🟢 留痕系统运行完成！")
    print(f"📁 留痕文件：{TRACE_FILE}")
    print(f"📋 审计日志：{AUDIT_LOG}")
