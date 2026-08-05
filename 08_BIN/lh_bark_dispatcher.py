#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-07-12-BARK-DISPATCHER-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════╗
║   🐉 龍魂·Bark 通知调度器 v1.0 — 全通道·DNA嵌入·审计·知识矩阵入库            ║
║   Bark Dispatcher · DNA → Audit → Annotate → Store → Send               ║
╠══════════════════════════════════════════════════════════════════════════╣
║   DNA: #龍芯⚡️2026-07-12-BARK-DISPATCHER-v1.0                            ║
║   通道: 每日早报 | Git推送 | 自愈报告 | 审计告警 | 备份状态 | 知识变更         ║
║   铁律: 不修改原文 · 下方备注 · DNA嵌入 · 三色审计 · 来源可溯 · 责任自负        ║
║   来源: UID9622 授权 · P02 龍芯设计 · P05 上帝之眼审计 · P15 乔前辈验收        ║
╚══════════════════════════════════════════════════════════════════════════╝

用法:
    python3 bin/lh_bark_dispatcher.py --type daily --content "..." --source "鲲鹏"
    python3 bin/lh_bark_dispatcher.py --type git   --content "commit msg" --source "GitHub"
    python3 bin/lh_bark_dispatcher.py --type heal  --content "修复报告" --source "自愈引擎"
    python3 bin/lh_bark_dispatcher.py --type audit --content "审计结果" --source "三色审计"

管道流程:
    原始内容 → DNA生成 → 三色审计 → 来源标注 → 知识矩阵入库 → Bark推送
"""

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# ═══════════════════════════════════════════════════════════
# 路径配置
# ═══════════════════════════════════════════════════════════

项目根 = Path(__file__).parent.parent
知识矩阵目录 = 项目根 / "articles" / "bark-notifications"
登记册路径 = 项目根 / "L7_数据层" / "dna_registry.jsonl"
索引路径 = 项目根 / "L7_数据层" / "dna_registry_index.json"
审计日志 = 项目根 / "audit" / "bark_audit.log"

# ═══════════════════════════════════════════════════════════
# Bark 配置
# ═══════════════════════════════════════════════════════════

BARK_KEY = os.environ.get("BARK_KEY", "BoWn76MNipaRA8RwrWqksP")
BARK_SERVER = os.environ.get("BARK_SERVER", "")

if BARK_SERVER:
    BARK_URL = f"{BARK_SERVER}/push"  # 自建 POST /push
else:
    BARK_URL = f"https://api.day.app/{BARK_KEY}"  # 官方 API

# ═══════════════════════════════════════════════════════════
# 天干地支·卦象映射（用于DNA生成）
# ═══════════════════════════════════════════════════════════

天干 = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
地支 = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
卦象 = ["䷀乾", "䷁坤", "䷂屯", "䷃蒙", "䷄需", "䷅讼", "䷆师", "䷇比",
        "䷈小畜", "䷉履", "䷊泰", "䷋否", "䷌同人", "䷍大有", "䷎谦", "䷏豫",
        "䷐随", "䷑蛊", "䷒临", "䷓观", "䷔噬嗑", "䷕贲", "䷖剥", "䷗复",
        "䷘无妄", "䷙大畜", "䷚颐", "䷛大过", "䷜坎", "䷝离", "䷞咸", "䷟恒",
        "䷠遁", "䷡大壮", "䷢晋", "䷣明夷", "䷤家人", "䷥睽", "䷦蹇", "䷧解",
        "䷨损", "䷩益", "䷪夬", "䷫姤", "䷬萃", "䷭升", "䷮困", "䷯井",
        "䷰革", "䷱鼎", "䷲震", "䷳艮", "䷴渐", "䷵归妹", "䷶丰", "䷷旅",
        "䷸巽", "䷹兑", "䷺涣", "䷻节", "䷼中孚", "䷽小过", "䷾既济", "䷿未济"]


def 生成DNA(消息类型: str, 内容哈希: str) -> str:
    """为消息生成唯一DNA签名"""
    now = datetime.now()
    年干 = 天干[now.year % 10]
    月干 = 天干[(now.year * 12 + now.month) % 10]
    月支 = 地支[(now.month - 1) % 12]
    日支 = 地支[now.day % 12]
    时辰 = 地支[(now.hour + 1) // 2 % 12]
    卦 = 卦象[now.day % 64]
    hex8 = 内容哈希[:8].upper()

    类型标记 = {
        "daily": "DAILY-REPORT",
        "git": "GIT-PUSH",
        "heal": "SELF-HEAL",
        "audit": "AUDIT-ALERT",
        "backup": "BACKUP",
        "knowledge": "KG-CHANGE",
        "custom": "CUSTOM",
    }.get(消息类型, "NOTIFY")

    return f"#龍芯⚡️{年干}午·{月干}{月支}·{日支}·{时辰}时·{卦}-BARK-{类型标记}-{hex8}"


def 三色审计(内容: str, 消息类型: str) -> Tuple[str, str]:
    """
    三色审计 · 不修改原文 · 只追加审计备注
    返回: (审计色, 审计备注)
    """
    issues = []
    warnings = []

    # 🔴 红线词检测
    红线词 = ["攻击", "漏洞利用", "后门植入", "数据窃取", "隐私泄露",
             "破解", "盗版", "非法", "恶意代码", "0day"]
    for word in 红线词:
        if word in 内容:
            issues.append(f"🔴 检测到敏感词: {word}")

    # 🟡 黄线词检测
    黄线词 = ["密码", "密钥", "token", "secret", "password", "api_key",
             "私钥", "凭据", "access_key"]
    for word in 黄线词:
        if word.lower() in 内容.lower():
            warnings.append(f"🟡 可能含敏感信息: {word}")

    # 消息类型风险评估
    高风险类型 = ["audit"]  # 审计类消息需额外检查
    if 消息类型 in 高风险类型 and len(内容) > 500:
        warnings.append("🟡 审计消息较长，建议确认后发送")

    if issues:
        审计色 = "red"
        审计备注 = "🔴 红线阻断 · 以下内容被标记:\n" + "\n".join(issues)
        if warnings:
            审计备注 += "\n\n🟡 附加警告:\n" + "\n".join(warnings)
    elif warnings:
        审计色 = "yellow"
        审计备注 = "🟡 黄线警告 · 已标注:\n" + "\n".join(warnings)
    else:
        审计色 = "green"
        审计备注 = "🟢 三色审计通过 · 可安全发送"

    return 审计色, 审计备注


def 来源标注(来源: str) -> str:
    """生成来源标注信息"""
    return f"""---
来源: {来源}
时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
作者: UID9622 · 诸葛鑫
授权链: UID9622 → P02 龍芯 → Bark调度器
责任声明: 本文由龍魂系统自动生成，UID9622授权发送。如有错误，接受批评改正。
---"""


def 入库知识矩阵(dna: str, 消息类型: str, 标题: str, 原文: str,
               审计色: str, 审计备注: str, 来源: str) -> Path:
    """
    将消息存入知识矩阵 · 不修改原文 · 下方追加备注
    格式:
        [DNA头]
        [来源标注]
        [原文]
        ---
        [审计备注]
        [责任声明]
    """
    知识矩阵目录.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_title = 标题.replace("/", "-").replace(" ", "_")[:60]
    file_name = f"{date_str}-BARK-{消息类型}-{safe_title}.md"
    file_path = 知识矩阵目录 / file_name

    来源块 = 来源标注(来源)
    短DNA = dna[:64] if len(dna) > 64 else dna

    内容块 = f"""{dna}

{来源块}

---

## 📋 {标题}

{原文}

---

## 🔍 审计记录

**审计结果**: {审计色}
**审计时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**审计备注**:
{审计备注}

---

## 📝 备注

> 本文由龍魂Bark通知调度器自动生成并入库。
> DNA: {短DNA}
> 入库时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> 入库类型: bark-notification/{消息类型}
>
> **责任声明**: 龍魂系统对推送内容负责。如有错误或不当，接受批评并立即改正。
> 本文为系统自动生成的通知记录，不修改原文，仅追加审计与来源信息。

---
*由龍魂Bark调度器 v1.0 生成 · UID9622授权*
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(内容块)

    return file_path


def 注册DNA(dna: str, 消息类型: str, 标题: str, 文件路径: str, 来源: str):
    """将DNA注册到登记册"""
    登记册路径.parent.mkdir(parents=True, exist_ok=True)

    entry = {
        "dna": dna,
        "type": f"BARK_{消息类型.upper()}",
        "title": 标题,
        "file": str(文件路径),
        "source": 来源,
        "uid": "UID9622",
        "timestamp": datetime.now().isoformat(),
        "parent_dna": "",
        "immutable": True,
    }

    with open(登记册路径, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    # 更新索引
    _更新索引(dna, 消息类型, 标题, str(文件路径))


def _更新索引(dna: str, 消息类型: str, 标题: str, 文件路径: str):
    """更新DNA索引文件"""
    索引路径.parent.mkdir(parents=True, exist_ok=True)

    if 索引路径.exists():
        with open(索引路径, "r", encoding="utf-8") as f:
            索引 = json.load(f)
    else:
        索引 = {"entries": [], "by_type": {}, "count": 0}

    索引["entries"].append({
        "dna": dna,
        "timestamp": datetime.now().isoformat(),
        "type": f"BARK_{消息类型.upper()}",
        "title": 标题,
        "file": 文件路径,
    })

    索引["by_type"][f"BARK_{消息类型.upper()}"] = \
        索引["by_type"].get(f"BARK_{消息类型.upper()}", 0) + 1
    索引["count"] = len(索引["entries"])

    with open(索引路径, "w", encoding="utf-8") as f:
        json.dump(索引, f, ensure_ascii=False, indent=2)


def 发送Bark(标题: str, 内容: str, 审计色: str, dna: str) -> bool:
    """通过Bark API推送到iPhone"""
    短DNA = dna.split("-")[-1][:8] if "-" in dna else dna[:8]
    审计图标 = {"red": "🔴", "yellow": "🟡", "green": "🟢"}.get(审计色, "🟢")

    full_title = f"{审计图标} {标题}"

    # 截断过长内容（Bark有长度限制）
    body = 内容
    if len(body) > 4000:
        body = body[:3900] + f"\n\n... (截断，完整内容已入库 DNA:{短DNA})"

    payload = json.dumps({
        "title": full_title,
        "body": body,
        "group": "龍魂系统",
        "sound": "alarm",
        "autoCopy": True,
        "url": f"longhun://notification/{短DNA}",
    }, ensure_ascii=False).encode("utf-8")

    try:
        req = urllib.request.Request(
            BARK_URL,
            data=payload,
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("code") == 200:
                return True
            else:
                print(f"[BARK] 发送失败: {result.get('message', 'unknown')}", file=sys.stderr)
                return False
    except Exception as e:
        print(f"[BARK] 发送异常: {e}", file=sys.stderr)
        return False


def 记录审计日志(dna: str, 消息类型: str, 审计色: str, 来源: str, bark_result: bool):
    """记录审计日志"""
    审计日志.parent.mkdir(parents=True, exist_ok=True)
    with open(审计日志, "a", encoding="utf-8") as f:
        f.write(json.dumps({
            "timestamp": datetime.now().isoformat(),
            "dna": dna,
            "type": 消息类型,
            "audit_color": 审计色,
            "source": 来源,
            "bark_sent": bark_result,
        }, ensure_ascii=False) + "\n")


# ═══════════════════════════════════════════════════════════
# 主调度函数
# ═══════════════════════════════════════════════════════════

def dispatch(消息类型: str, 标题: str, 内容: str, 来源: str = "龍魂系统",
            dry_run: bool = False) -> Dict[str, Any]:
    """
    核心调度管道:
    原始内容 → DNA生成 → 三色审计 → 来源标注 → 知识矩阵入库 → Bark推送

    返回调度结果字典
    """
    # Step 1: 生成DNA
    内容哈希 = hashlib.sha256(内容.encode("utf-8")).hexdigest()
    dna = 生成DNA(消息类型, 内容哈希)

    # Step 2: 三色审计
    审计色, 审计备注 = 三色审计(内容, 消息类型)

    # Step 3: 🔴红线阻断
    if 审计色 == "red":
        result = {
            "status": "blocked",
            "dna": dna,
            "audit_color": 审计色,
            "audit_remark": 审计备注,
            "message": "🔴 红线阻断 · 消息未发送",
        }
        # 即使阻断也入库记录
        if not dry_run:
            file_path = 入库知识矩阵(dna, 消息类型, 标题, 内容, 审计色, 审计备注, 来源)
            注册DNA(dna, 消息类型, 标题, str(file_path), 来源)
            记录审计日志(dna, 消息类型, 审计色, 来源, False)
        return result

    # Step 4: 知识矩阵入库（不修改原文，下方追加备注）
    file_path = None
    if not dry_run:
        file_path = 入库知识矩阵(dna, 消息类型, 标题, 内容, 审计色, 审计备注, 来源)
        注册DNA(dna, 消息类型, 标题, str(file_path), 来源)

    # Step 5: Bark推送
    bark_sent = False
    if not dry_run:
        bark_sent = 发送Bark(标题, 内容, 审计色, dna)
        记录审计日志(dna, 消息类型, 审计色, 来源, bark_sent)

    return {
        "status": "sent" if bark_sent else ("stored" if not dry_run else "dry_run"),
        "dna": dna,
        "audit_color": 审计色,
        "audit_remark": 审计备注,
        "bark_sent": bark_sent,
        "knowledge_file": str(file_path) if file_path else None,
        "message": f"{'✅ 已推送' if bark_sent else '📁 已入库（推送失败）'}" if not dry_run else "🧪 干运行完成",
    }


# ═══════════════════════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·Bark通知调度器 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--type", required=True,
                       choices=["daily", "git", "heal", "audit", "backup", "knowledge", "custom"],
                       help="消息类型")
    parser.add_argument("--title", required=True, help="消息标题")
    parser.add_argument("--content", default="", help="消息内容（或从stdin读取）")
    parser.add_argument("--source", default="龍魂系统", help="消息来源")
    parser.add_argument("--stdin", action="store_true", help="从stdin读取内容")
    parser.add_argument("--dry-run", action="store_true", help="干运行，不实际发送")
    parser.add_argument("--json", action="store_true", help="JSON格式输出")

    args = parser.parse_args()

    # 获取内容
    content = args.content
    if args.stdin:
        content = sys.stdin.read().strip()
    if not content:
        print("错误: 需要提供内容 (--content 或 --stdin)", file=sys.stderr)
        sys.exit(1)

    # 执行调度
    result = dispatch(args.type, args.title, content, args.source, args.dry_run)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"DNA:    {result['dna']}")
        print(f"审计:    {result['audit_color']}")
        print(f"状态:    {result['message']}")
        if result.get("knowledge_file"):
            print(f"入库:    {result['knowledge_file']}")

    sys.exit(0 if result["status"] != "blocked" else 1)


if __name__ == "__main__":
    main()
