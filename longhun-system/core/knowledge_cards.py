#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧬 龍芯知识卡片引擎 · knowledge_cards.py
# DNA追溯码: #龍芯⚡️2026-04-13-知识卡片引擎-v1.0
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
# 理论指导: 曾仕强老师（永恒显示）
# 灵感来源: ChatGPT基础卡片框架 → Claude落地优化
#
# 功能:
#   ① 统一知识卡片结构（7层必填字段）
#   ② RootCheck根检查（来源+DNA+哈希三合一验证）
#   ③ 自动三色状态判定
#   ④ 批量生成 + 导出Notion/Markdown
#   ⑤ 与longhun_engine.py联动（f(x)=x验证+数字根）
#
# 用法:
#   from knowledge_cards import CardEngine
#   engine = CardEngine()
#   card = engine.create("数据结构", "东西怎么摆放才能好找好用", ...)
#   engine.verify(card)  # RootCheck
#
# 献礼: 致敬曾仕强老师 · 致敬每一位守护普通人的人
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import hashlib
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

DNA_TAG = "#龍芯⚡️2026-04-13-知识卡片引擎-v1.0"
GPG_FP = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID = "9622"


# ════════════════════════════════════════════════════════════════
# 知识卡片结构定义
# ════════════════════════════════════════════════════════════════

class Card:
    """
    龍芯知识卡片 · 七层结构

    必填: 名称、一句话、本质、最小实现、边界、来源、DNA
    自动: 哈希、三色状态、创建时间
    """

    def __init__(
        self,
        name: str,
        one_line: str,       # 📌 一句话（初中能懂）
        essence: str,        # 🧠 本质（f(x)=x 不动点）
        minimal: str,        # 🔧 最小实现（能跑的代码/步骤）
        boundary: str,       # ⚠️ 边界（什么时候不能用）
        source: str,         # 🔍 来源（作者/灵感/体系）
        category: str = "",  # 分类标签
        fail_conditions: Optional[List[str]] = None,  # 🛑 失效条件
    ):
        self.name = name
        self.one_line = one_line
        self.essence = essence
        self.minimal = minimal
        self.boundary = boundary
        self.source = source
        self.category = category
        self.fail_conditions = fail_conditions or [
            "无溯源 → 无效",
            "修改不留痕 → 无效",
            "用于欺骗 → 自动拒绝",
        ]

        # 自动生成
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.uid = UID
        self.dna = f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-{name}-v1.0"
        self.hash = self._compute_hash()
        self.status = "🟢"  # 默认可用，root_check后可能变

    def _compute_hash(self) -> str:
        """内容指纹：名称+本质+最小实现 → SHA256前16位"""
        raw = f"{self.name}|{self.essence}|{self.minimal}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "one_line": self.one_line,
            "essence": self.essence,
            "minimal": self.minimal,
            "boundary": self.boundary,
            "source": self.source,
            "category": self.category,
            "fail_conditions": self.fail_conditions,
            "created": self.created,
            "uid": self.uid,
            "dna": self.dna,
            "hash": self.hash,
            "status": self.status,
        }

    def to_markdown(self) -> str:
        """导出为标准Markdown卡片"""
        fc = "\n".join(f"- {f}" for f in self.fail_conditions)
        return f"""# 🧬 {self.name}

## 📌 一句话（初中能懂）
{self.one_line}

## 🧠 本质（f(x)=x 不动点）
{self.essence}

## 🔧 最小实现（能跑）
```
{self.minimal}
```

## ⚠️ 边界（什么时候不能用）
{self.boundary}

## 🔍 溯源
来源: {self.source}

## 🛑 失效条件
{fc}

## 🧬 DNA标记
- UID: {self.uid}
- 时间: {self.created}
- 哈希: {self.hash}
- DNA: {self.dna}

## 🔄 三色状态
{self.status}

---
GPG: {GPG_FP}
"""

    def to_notion_properties(self) -> Dict[str, Any]:
        """生成Notion页面属性（配合花名册数据库或独立知识库）"""
        return {
            "名字": self.name,
            "一句话": self.one_line,
            "做什么": self.essence,
            "功能定位": self.one_line,
            "DNA追溯码": self.dna,
            "确认码": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
            "备注": f"哈希:{self.hash} | 来源:{self.source}",
        }


# ════════════════════════════════════════════════════════════════
# RootCheck · 根检查（来源+DNA+哈希三合一验证）
# ════════════════════════════════════════════════════════════════

def root_check(card: Card) -> Dict[str, Any]:
    """
    根检查：验证卡片完整性

    三条铁律:
      ① 有来源（source不为空）
      ② 有DNA标记（dna不为空）
      ③ 哈希一致（内容没被篡改）

    返回: {"passed": bool, "status": "🟢/🟡/🔴", "issues": [...]}
    """
    issues = []

    # ① 来源检查
    if not card.source or card.source.strip() == "":
        issues.append("❌ 无来源：不知道从哪来的知识不可信")

    # ② DNA检查
    if not card.dna or "龍芯" not in card.dna:
        issues.append("❌ 无DNA标记：没有溯源锚点")

    # ③ 哈希一致性
    current_hash = card._compute_hash()
    if current_hash != card.hash:
        issues.append(f"⚠️ 哈希不一致：内容被修改（期望{card.hash}，实际{current_hash}）")

    # ④ 必填字段完整性
    for field, label in [
        (card.name, "名称"),
        (card.one_line, "一句话"),
        (card.essence, "本质"),
        (card.minimal, "最小实现"),
        (card.boundary, "边界"),
    ]:
        if not field or field.strip() == "":
            issues.append(f"⚠️ 缺失字段：{label}")

    # 判定三色
    if not issues:
        status = "🟢 通过·可用"
        passed = True
    elif any("❌" in i for i in issues):
        status = "🔴 拒绝·不可用"
        passed = False
    else:
        status = "🟡 警告·待验证"
        passed = False

    card.status = status.split()[0]

    return {
        "passed": passed,
        "status": status,
        "issues": issues,
        "hash": current_hash,
        "dna": card.dna,
    }


# ════════════════════════════════════════════════════════════════
# CardEngine · 卡片引擎（批量管理）
# ════════════════════════════════════════════════════════════════

class CardEngine:
    """龍芯知识卡片引擎"""

    def __init__(self):
        self.cards: Dict[str, Card] = {}
        self.output_dir = Path.home() / "longhun-system" / "knowledge"
        self.output_dir.mkdir(exist_ok=True)

    def create(self, name: str, one_line: str, essence: str,
               minimal: str, boundary: str, source: str,
               category: str = "", fail_conditions: Optional[List[str]] = None) -> Card:
        """创建一张卡片并自动验证"""
        card = Card(name, one_line, essence, minimal, boundary, source,
                    category, fail_conditions)
        result = root_check(card)
        self.cards[name] = card
        return card

    def verify_all(self) -> List[Dict]:
        """验证所有卡片"""
        results = []
        for name, card in self.cards.items():
            r = root_check(card)
            r["name"] = name
            results.append(r)
        return results

    def export_markdown(self, filename: str = None) -> Path:
        """导出全部卡片为Markdown文件"""
        if not filename:
            today = datetime.now().strftime("%Y-%m-%d")
            filename = f"{today}_知识卡片集.md"
        out = self.output_dir / filename

        lines = [
            f"# 🧬 龍芯知识卡片集",
            f"> 导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            f"> DNA: {DNA_TAG}",
            f"> 共 {len(self.cards)} 张卡片",
            "",
        ]
        for card in self.cards.values():
            lines.append(card.to_markdown())
            lines.append("")

        lines += [
            "---",
            f"GPG: {GPG_FP}",
            f"创建者: 诸葛鑫（UID9622）",
            f"理论指导: 曾仕强老师（永恒显示）",
        ]

        out.write_text("\n".join(lines), encoding="utf-8")
        return out

    def export_json(self) -> Path:
        """导出全部卡片为JSON（可导入Notion）"""
        today = datetime.now().strftime("%Y-%m-%d")
        out = self.output_dir / f"{today}_知识卡片集.json"
        data = {
            "dna": DNA_TAG,
            "gpg": GPG_FP,
            "exported": datetime.now().isoformat(),
            "cards": [c.to_dict() for c in self.cards.values()],
        }
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return out

    def print_summary(self):
        """打印卡片摘要"""
        print(f"━{'━'*60}")
        print(f"🧬 龍芯知识卡片引擎 · 共 {len(self.cards)} 张")
        print(f"━{'━'*60}")
        for name, card in self.cards.items():
            r = root_check(card)
            print(f"  {r['status'].split()[0]} {name:12s} │ {card.one_line[:35]}")
        print(f"━{'━'*60}")
        print(f"DNA: {DNA_TAG}")


# ════════════════════════════════════════════════════════════════
# 预装卡片 · 计算机基础四根柱
# ════════════════════════════════════════════════════════════════

def load_foundation_cards() -> CardEngine:
    """加载计算机基础四张根卡片"""
    engine = CardEngine()

    engine.create(
        name="数据结构",
        one_line="东西怎么摆放，才能好找好用",
        essence="「存」和「取」的平衡。再复杂的结构，本质都逃不掉这个。",
        minimal='data = [1, 2, 3]\ndata.append(4)  # 存\nprint(data[0])  # 取',
        boundary="数据量大→列表慢，需要排序→要换结构",
        source="计算机基础公开知识 · ChatGPT灵感 · Claude落地",
        category="计算机基础",
    )

    engine.create(
        name="操作系统",
        one_line="管电脑资源的管家",
        essence="资源分配。CPU、内存、文件、设备——谁用？什么时候用？用多少？",
        minimal='ps aux       # 查看进程\nkill -9 PID  # 杀进程',
        boundary="误杀系统进程→系统崩，权限不足→执行失败",
        source="计算机基础公开知识 · ChatGPT灵感 · Claude落地",
        category="计算机基础",
    )

    engine.create(
        name="网络TCP/IP",
        one_line="把数据从A送到B",
        essence="可靠传输。不是「发出去」，是：发到+对方收到+没错。",
        minimal='ping 8.8.8.8  # 最简网络测试',
        boundary="网络通≠服务正常，IP通≠网站能访问",
        source="计算机基础公开知识 · ChatGPT灵感 · Claude落地",
        category="计算机基础",
    )

    engine.create(
        name="哈希/加密",
        one_line="把内容变成指纹",
        essence="唯一映射。同一输入→同一输出，不同输入→基本不同输出。",
        minimal='import hashlib\ndata = "hello"\nhash_value = hashlib.sha256(data.encode()).hexdigest()\nprint(hash_value)',
        boundary="哈希≠加密（不能还原），不能用于隐藏数据",
        source="计算机基础公开知识 · ChatGPT灵感 · Claude落地",
        category="计算机基础",
    )

    return engine


# ════════════════════════════════════════════════════════════════
# 独立运行
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    engine = load_foundation_cards()

    # 打印摘要
    engine.print_summary()

    # 验证全部
    print("\n🔍 RootCheck 根检查:")
    for r in engine.verify_all():
        print(f"  {r['status']} │ {r['name']}")

    # 导出
    md_path = engine.export_markdown()
    json_path = engine.export_json()
    print(f"\n✅ 已导出:")
    print(f"  📄 Markdown: {md_path}")
    print(f"  📦 JSON: {json_path}")
