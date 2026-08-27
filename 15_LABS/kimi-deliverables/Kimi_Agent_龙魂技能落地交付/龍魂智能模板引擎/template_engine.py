#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂 · 智能模板引擎 v1.0 (焊死格式)
规矩 (记忆37):
  - 头部元数据: DNA(生成器输出, 禁手写) + 确认码 + GPG
  - 必含模块固定顺序, 缺区块自动补 🔶占位, 不许删除
  - 字符级固定签名块
  - 三色只有 🟢🟡🔴, 退出码 0/1/2
  - 交付前必跑 validate 核验
用法:
  python3 template_engine.py render <类型> <输出文件>   # 交互式/程序调用见 build_document()
  python3 template_engine.py validate <文件>            # 核验, 退出码 0=🟢 1=🟡 2=🔴
"""
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "bin"))
from lh_dna_generator import generate  # noqa: E402

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
PLACEHOLDER = "🔶 占位待补"

# 六类产出 × 必含模块固定顺序 (焊死, 顺序不可乱, 缺了自动补🔶)
TEMPLATES = {
    "文档": ["核心判断", "正文", "检查清单", "常见QA", "未验证备注", "最终签名"],
    "代码": ["文件头注释", "实现", "锚点断言", "未验证备注", "最终签名"],
    "图表": ["核心判断", "图体", "数据口径", "未验证备注", "最终签名"],
    "数据": ["核心判断", "数据体", "来源与口径", "未验证备注", "最终签名"],
    "检查": ["核心判断", "检查项", "实测记录", "未验证备注", "最终签名"],
    "API":  ["核心判断", "接口契约", "请求响应示例", "错误码", "未验证备注", "最终签名"],
}


def header(dna: str, tricolor: str = "🟢", doc_type: str = "") -> str:
    return (
        f"**DNA:** `{dna}`\n"
        f"**确认码:** `{CONFIRM}`\n"
        f"**GPG:** `{GPG}`\n"
        f"**三色:** {tricolor}\n"
        f"**类型:** {doc_type}\n"
        f"**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2\n"
    )


def signature_block(dna: str, title: str, stats: dict) -> str:
    lines = "\n".join(f"{k}:\t{v}" for k, v in stats.items())
    return (
        "```\n"
        "═══════════════════════════════════════════════════\n"
        f" 🐉 龍魂 · {title} · 最终签名\n"
        "═══════════════════════════════════════════════════\n"
        f"DNA:\t{dna}\n"
        f"确认码:\t{CONFIRM}\n"
        f"GPG:\t{GPG}\n"
        f"{lines}\n"
        "═══════════════════════════════════════════════════\n"
        "```"
    )


def build_document(doc_type: str, title: str, sections: dict, stats: dict,
                   action: str, version: str = "v1.0", tricolor: str = "🟢") -> str:
    """sections: {模块名: 内容}; 缺模块自动补🔶占位"""
    if doc_type not in TEMPLATES:
        raise ValueError(f"未知类型 {doc_type}, 只认: {list(TEMPLATES)}")
    dna = generate(datetime.now(), action, version)
    parts = [f"# 🐉 龍魂 · {title}\n", header(dna, tricolor, doc_type)]
    for module in TEMPLATES[doc_type]:
        if module == "最终签名":
            parts.append(f"\n## 🔐 最终签名\n\n{signature_block(dna, title, stats)}")
            continue
        body = sections.get(module)
        if body is None or not str(body).strip():
            body = PLACEHOLDER  # 缺区块自动补, 不许删除
        parts.append(f"\n## {module}\n\n{body}")
    return "\n".join(parts) + "\n"


def validate(path: str) -> int:
    """核验焊死格式; 打印问题; 返回退出码"""
    p = Path(path)
    if not p.exists():
        print(f"🔴 文件不存在: {path}")
        return 2
    text = p.read_text(encoding="utf-8")
    problems, warnings = [], []

    # 1. 头部元数据
    for field, pat in [("DNA", r"\*\*DNA:\*\*"), ("确认码", re.escape(CONFIRM)),
                       ("GPG", GPG), ("三色", r"\*\*三色:\*\*")]:
        if not re.search(pat, text):
            problems.append(f"缺头部字段: {field}")

    # 2. DNA 手写干支检测: 纯「时辰名」(如'亥时'无干) 或无卦名 = 旧手写格式
    dna_lines = re.findall(r"#龍芯⚡️([^\s`\"]+)", text)
    for d in dna_lines:
        if "䷞" not in d and not re.search(r"[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]时", d):
            problems.append(f"疑手写干支DNA(无卦名/时柱无干): {d[:60]}")

    # 3. 类型识别 (从头部元数据) + 模块顺序核验
    m = re.search(r"\*\*类型:\*\*\s*(\S+)", text)
    doc_type = m.group(1) if m and m.group(1) in TEMPLATES else None
    if doc_type is None:
        problems.append("头部缺类型字段或类型非法")
    if doc_type:
        pos = -1
        for m in TEMPLATES[doc_type]:
            hit = re.search(rf"^##\s*\S*\s*{re.escape(m)}\s*$", text, re.M)
            if not hit:
                problems.append(f"缺模块: {m}")
            elif hit.start() < pos:
                problems.append(f"模块顺序错位: {m}")
            else:
                pos = hit.start()

    # 4. 占位符与未验证标注
    if PLACEHOLDER in text:
        warnings.append(f"存在{PLACEHOLDER}占位区块 (允许存在, 不许删除)")
    if "🟡" not in text:
        warnings.append("全文无🟡待验标注 —— 若有未实测项必须标注")

    # 5. 签名块
    if "最终签名" not in text or "═══" not in text:
        problems.append("缺字符级签名块")

    for w in warnings:
        print(f"🟡 {w}")
    for pr in problems:
        print(f"🔴 {pr}")
    if problems:
        print(f"🔴 核验失败 ({len(problems)}项): {p.name}")
        return 2
    if warnings:
        print(f"🟡 核验通过带警告 ({len(warnings)}项): {p.name}")
        return 1
    print(f"🟢 核验通过: {p.name}")
    return 0


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "validate":
        sys.exit(validate(sys.argv[2]))
    print(__doc__)
    sys.exit(0)
