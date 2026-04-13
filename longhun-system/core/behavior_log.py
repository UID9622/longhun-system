#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🧬 龍芯行为日志引擎 · behavior_log.py
# DNA追溯码: #龍芯⚡️2026-04-13-行为日志-v1.0
# GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 创建者: 诸葛鑫（UID9622）
# 理论指导: 曾仕强老师（永恒显示）
# 灵感来源: ChatGPT日志型追溯表方案 → Claude引擎化落地
#
# 核心理念:
#   "灵感可以乱，记录必须准"
#   每一条灵感 = 一条记录
#   每一步操作 = 有痕迹
#   每天 = 有收敛总结
#   最后能还原: 这个东西是怎么一步一步长出来的
#
# 功能:
#   ① 四类记录: 灵感 / 推演 / 操作 / 总结
#   ② 自动DNA生成: #龍芯⚡️YYYYMMDD-序号-类型
#   ③ 链式追溯: 每条记录可挂上级DNA（父链）
#   ④ 三色自动判定: 🟢有来源+一句话 / 🟡缺一句话 / 🔴缺来源
#   ⑤ 每日自动收敛: 一键生成当日总结
#   ⑥ Notion同步: 写入《龍魂·行为日志》数据库
#   ⑦ 本地持久化: JSON + Markdown双存储
#   ⑧ 链路可视化: 从任意一条往上追到起点
#   ⑨ 通心翻译: 所有输出初中能懂
#
# 用法:
#   from behavior_log import BehaviorLog
#   log = BehaviorLog()
#   log.灵感("信任需要成本证明", 行为="想到商鞅立木", 来源="历史案例")
#   log.推演("信号博弈=高成本承诺", 行为="博弈论解释", 上级="01")
#   log.操作("用369模型验证", 行为="做1000次测试", 结果="100%收敛")
#   log.今日总结()
#
# 献礼: 致敬曾仕强老师 · 致敬每一位守护普通人的人
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

DNA_TAG = "#龍芯⚡️2026-04-13-行为日志-v1.0"
GPG_FP = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
UID = "9622"

# 输出目录
BASE_DIR = Path.home() / "longhun-system"
LOG_DIR = BASE_DIR / "behavior_logs"
LOG_DIR.mkdir(exist_ok=True)

# Notion配置
NOTION_TOKEN = os.getenv("NOTION_TOKEN_WORKSPACE", "")

# 四种记录类型
RECORD_TYPES = {
    "灵感": {"icon": "💡", "desc": "随便来的想法·灵光一闪", "通心": "脑子里冒出来的东西"},
    "推演": {"icon": "🔮", "desc": "用理论/逻辑推导·深入分析", "通心": "拿放大镜看清楚"},
    "操作": {"icon": "🔧", "desc": "实际动手做·代码/测试/部署", "通心": "撸起袖子干活"},
    "总结": {"icon": "📋", "desc": "收敛当日成果·形成沉淀", "通心": "今天学到了什么"},
}


# ════════════════════════════════════════════════════════════════
# 单条行为记录
# ════════════════════════════════════════════════════════════════

class BehaviorRecord:
    """
    一条行为记录 · 认知链的最小单元

    必填: 类型 + 一句话
    自动: DNA + 时间 + 三色状态
    可选: 行为 + 结果 + 来源 + 上级DNA + 备注
    """

    def __init__(
        self,
        record_type: str,       # 灵感 / 推演 / 操作 / 总结
        one_line: str,          # 📌 一句话（核心，初中能懂）
        behavior: str = "",     # 🔧 做了什么
        result: str = "",       # 📊 得到什么
        source: str = "",       # 🔍 来自哪里
        parent_dna: str = "",   # 🔗 上级DNA（链式追溯）
        note: str = "",         # 🧾 备注（原始内容）
        seq: int = 1,           # 当日序号
    ):
        self.record_type = record_type
        self.one_line = one_line
        self.behavior = behavior
        self.result = result
        self.source = source
        self.parent_dna = parent_dna
        self.note = note
        self.seq = seq

        # 自动生成
        self.timestamp = datetime.now()
        self.date_str = self.timestamp.strftime("%Y%m%d")
        self.time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        self.dna = f"#龍芯⚡️{self.date_str}-{seq:02d}-{record_type}"
        self.status = self._auto_status()

    def _auto_status(self) -> str:
        """
        三色自动判定:
          🟢 有来源 + 有一句话
          🟡 有一句话但缺来源
          🔴 缺来源
        """
        if not self.source or self.source.strip() == "":
            return "🔴"
        if not self.one_line or self.one_line.strip() == "":
            return "🟡"
        return "🟢"

    def to_dict(self) -> Dict[str, Any]:
        type_info = RECORD_TYPES.get(self.record_type, {})
        return {
            "dna": self.dna,
            "时间": self.time_str,
            "类型": self.record_type,
            "类型图标": type_info.get("icon", "📝"),
            "一句话": self.one_line,
            "通心翻译": self._tongxin(),
            "行为": self.behavior,
            "结果": self.result,
            "来源": self.source,
            "上级DNA": self.parent_dna,
            "状态": self.status,
            "备注": self.note,
            "序号": self.seq,
        }

    def _tongxin(self) -> str:
        """
        通心翻译 · 初中能懂版本

        把专业描述翻译成人话:
          行为链日志 → 每天做了什么的记录本
          DNA追溯 → 每条记录的身份证号
          链式追溯 → 顺着线头往回找
        """
        type_info = RECORD_TYPES.get(self.record_type, {})
        type_plain = type_info.get("通心", self.record_type)
        return f"[{type_plain}] {self.one_line}"

    def to_markdown_line(self) -> str:
        """一行Markdown格式。"""
        type_info = RECORD_TYPES.get(self.record_type, {})
        icon = type_info.get("icon", "📝")
        parent = f" ← `{self.parent_dna}`" if self.parent_dna else ""
        return (
            f"| `{self.dna}` | {self.status} {icon} {self.record_type} "
            f"| {self.one_line} | {self.behavior} | {self.result} "
            f"| {self.source}{parent} |"
        )

    def to_detail_markdown(self) -> str:
        """详细Markdown卡片。"""
        type_info = RECORD_TYPES.get(self.record_type, {})
        icon = type_info.get("icon", "📝")
        lines = [
            f"### {self.status} {icon} {self.one_line}",
            f"",
            f"- **DNA**: `{self.dna}`",
            f"- **类型**: {self.record_type}（{type_info.get('通心', '')}）",
            f"- **时间**: {self.time_str}",
        ]
        if self.behavior:
            lines.append(f"- **行为**: {self.behavior}")
        if self.result:
            lines.append(f"- **结果**: {self.result}")
        if self.source:
            lines.append(f"- **来源**: {self.source}")
        if self.parent_dna:
            lines.append(f"- **上级DNA**: `{self.parent_dna}`")
        if self.note:
            lines.append(f"- **备注**: {self.note}")
        lines.append("")
        return "\n".join(lines)


# ════════════════════════════════════════════════════════════════
# 行为日志引擎
# ════════════════════════════════════════════════════════════════

class BehaviorLog:
    """
    🧬 龍芯行为日志引擎

    核心铁律: "灵感可以乱，记录必须准"

    每天一个日志文件，JSON + Markdown双存储。
    所有记录通过DNA链式串联，从任意一条往上追到起点。

    用法:
        log = BehaviorLog()
        log.灵感("信任需要成本证明", 行为="想到商鞅立木", 来源="历史案例")
        log.推演("信号博弈=高成本承诺", 行为="博弈论解释", 上级="01")
        log.今日总结()
    """

    def __init__(self):
        self.today = datetime.now().strftime("%Y%m%d")
        self.today_dash = datetime.now().strftime("%Y-%m-%d")
        self.records: List[BehaviorRecord] = []
        self.seq = 0

        # 尝试加载今日已有记录
        self._load_today()

    def _next_seq(self) -> int:
        """获取下一个序号。"""
        self.seq += 1
        return self.seq

    def _load_today(self):
        """加载今日已有记录。"""
        json_path = LOG_DIR / f"{self.today_dash}_行为日志.json"
        if json_path.exists():
            try:
                data = json.loads(json_path.read_text(encoding="utf-8"))
                self.seq = data.get("last_seq", 0)
                # 重建记录对象
                for r in data.get("records", []):
                    rec = BehaviorRecord(
                        record_type=r["类型"],
                        one_line=r["一句话"],
                        behavior=r.get("行为", ""),
                        result=r.get("结果", ""),
                        source=r.get("来源", ""),
                        parent_dna=r.get("上级DNA", ""),
                        note=r.get("备注", ""),
                        seq=r.get("序号", 0),
                    )
                    rec.dna = r["dna"]
                    rec.time_str = r["时间"]
                    rec.status = r["状态"]
                    self.records.append(rec)
            except (json.JSONDecodeError, KeyError):
                pass

    def _resolve_parent(self, parent: str) -> str:
        """
        解析上级DNA。
        支持简写: "01" → "#龍芯⚡️20260413-01-灵感"
        支持全写: 直接用
        """
        if not parent:
            return ""
        # 如果是纯数字（简写序号），查找对应记录
        if parent.isdigit():
            seq_num = int(parent)
            for r in self.records:
                if r.seq == seq_num:
                    return r.dna
            # 没找到就拼接（容错）
            return f"#龍芯⚡️{self.today}-{int(parent):02d}"
        # 如果已经是完整DNA
        if parent.startswith("#龍芯"):
            return parent
        return parent

    # ── 四种记录快捷入口 ──────────────────────────────────

    def 灵感(self, one_line: str, 行为: str = "", 结果: str = "",
           来源: str = "", 备注: str = "") -> BehaviorRecord:
        """
        💡 记录一个灵感

        通心翻译: 脑子里冒出来的东西，先记下来再说

        参数:
          one_line: 一句话（核心想法）
          行为: 怎么想到的
          结果: 想到了什么
          来源: 从哪里来的灵感
          备注: 补充说明
        """
        return self._add("灵感", one_line, 行为, 结果, 来源, "", 备注)

    def 推演(self, one_line: str, 行为: str = "", 结果: str = "",
           来源: str = "", 上级: str = "", 备注: str = "") -> BehaviorRecord:
        """
        🔮 记录一次推演

        通心翻译: 拿放大镜看清楚，用理论/逻辑推导

        参数:
          one_line: 一句话（推演结论）
          行为: 用什么方法推演的
          结果: 推演出什么
          来源: 理论依据
          上级: 上级记录的序号或DNA
          备注: 推演过程
        """
        return self._add("推演", one_line, 行为, 结果, 来源, 上级, 备注)

    def 操作(self, one_line: str, 行为: str = "", 结果: str = "",
           来源: str = "", 上级: str = "", 备注: str = "") -> BehaviorRecord:
        """
        🔧 记录一次操作

        通心翻译: 撸起袖子干活，实际动手做

        参数:
          one_line: 一句话（干了什么）
          行为: 具体操作步骤
          结果: 操作结果
          来源: 为什么要做这个
          上级: 上级记录的序号或DNA
          备注: 操作细节
        """
        return self._add("操作", one_line, 行为, 结果, 来源, 上级, 备注)

    def 总结(self, one_line: str, 行为: str = "", 结果: str = "",
           来源: str = "当日记录", 备注: str = "") -> BehaviorRecord:
        """
        📋 记录一条总结

        通心翻译: 今天学到了什么，收敛沉淀

        参数:
          one_line: 一句话（今日核心收获）
          行为: 怎么总结的
          结果: 总结产出
          来源: 默认"当日记录"
          备注: 补充
        """
        return self._add("总结", one_line, 行为, 结果, 来源, "", 备注)

    def _add(self, record_type: str, one_line: str,
             behavior: str, result: str, source: str,
             parent: str, note: str) -> BehaviorRecord:
        """内部添加记录。"""
        seq = self._next_seq()
        parent_dna = self._resolve_parent(parent)

        record = BehaviorRecord(
            record_type=record_type,
            one_line=one_line,
            behavior=behavior,
            result=result,
            source=source,
            parent_dna=parent_dna,
            note=note,
            seq=seq,
        )

        self.records.append(record)
        self._save()  # 每次添加自动保存

        return record

    # ── 英文别名（方便代码调用） ──────────────────────────

    def idea(self, one_line: str, **kwargs) -> BehaviorRecord:
        return self.灵感(one_line, **kwargs)

    def deduce(self, one_line: str, **kwargs) -> BehaviorRecord:
        return self.推演(one_line, **kwargs)

    def action(self, one_line: str, **kwargs) -> BehaviorRecord:
        return self.操作(one_line, **kwargs)

    def summary(self, one_line: str, **kwargs) -> BehaviorRecord:
        return self.总结(one_line, **kwargs)

    # ── 今日自动总结 ──────────────────────────────────────

    def 今日总结(self) -> BehaviorRecord:
        """
        📋 自动生成今日收敛总结

        通心翻译: 把今天所有的灵感、推演、操作打包成一句话

        统计今日各类型数量，生成摘要，自动写入总结记录。
        """
        type_counts = {}
        for r in self.records:
            t = r.record_type
            type_counts[t] = type_counts.get(t, 0) + 1

        total = len(self.records)
        parts = [f"{RECORD_TYPES[t]['icon']}{t}×{c}" for t, c in type_counts.items()]
        summary_line = f"今日共{total}条: {' '.join(parts)}"

        # 提取所有灵感的一句话
        ideas = [r.one_line for r in self.records if r.record_type == "灵感"]
        idea_summary = "、".join(ideas[:5]) if ideas else "无灵感记录"

        # 统计三色
        colors = {"🟢": 0, "🟡": 0, "🔴": 0}
        for r in self.records:
            colors[r.status] = colors.get(r.status, 0) + 1
        color_str = f"🟢{colors['🟢']} 🟡{colors['🟡']} 🔴{colors['🔴']}"

        behavior = f"整合{total}条记录 | {color_str}"
        result = f"核心灵感: {idea_summary}"

        return self.总结(
            summary_line,
            行为=behavior,
            结果=result,
            备注=f"自动生成·{self.today_dash}",
        )

    # ── 链路追溯 ──────────────────────────────────────────

    def 追溯(self, dna_or_seq) -> List[Dict]:
        """
        🔗 从一条记录往上追溯到起点

        通心翻译: 顺着线头往回找，看这个东西是怎么一步步来的

        参数: DNA完整码 或 序号
        返回: 从当前到起点的链路列表
        """
        # 找到起始记录
        target = None
        if isinstance(dna_or_seq, int):
            for r in self.records:
                if r.seq == dna_or_seq:
                    target = r
                    break
        else:
            for r in self.records:
                if r.dna == dna_or_seq or str(dna_or_seq) in r.dna:
                    target = r
                    break

        if not target:
            return [{"error": f"未找到记录: {dna_or_seq}"}]

        # 往上追溯
        chain = []
        current = target
        visited = set()  # 防环

        while current and current.dna not in visited:
            visited.add(current.dna)
            chain.append(current.to_dict())

            if not current.parent_dna:
                break

            # 找上级
            parent = None
            for r in self.records:
                if r.dna == current.parent_dna:
                    parent = r
                    break
            current = parent

        return chain

    def 追溯打印(self, dna_or_seq):
        """可视化打印追溯链路。"""
        chain = self.追溯(dna_or_seq)
        if not chain or "error" in chain[0]:
            print(f"  ⚠️ {chain[0].get('error', '未知错误')}")
            return

        print(f"\n🔗 追溯链路（共{len(chain)}层）")
        print(f"{'─' * 60}")
        for i, node in enumerate(chain):
            indent = "  " * i
            arrow = "→ " if i > 0 else "⭐ "
            icon = node.get("类型图标", "📝")
            print(f"{indent}{arrow}{icon} [{node['类型']}] {node['一句话']}")
            print(f"{indent}   DNA: {node['dna']}")
            if node.get("上级DNA"):
                print(f"{indent}   ← 来自: {node['上级DNA']}")
        print(f"{'─' * 60}")

    # ── 持久化 ──────────────────────────────────────────

    def _save(self):
        """保存到本地（JSON + Markdown）。"""
        self._save_json()
        self._save_markdown()

    def _save_json(self):
        """保存JSON（可增量加载）。"""
        out = LOG_DIR / f"{self.today_dash}_行为日志.json"
        data = {
            "dna": DNA_TAG,
            "gpg": GPG_FP,
            "uid": UID,
            "日期": self.today_dash,
            "last_seq": self.seq,
            "记录数": len(self.records),
            "records": [r.to_dict() for r in self.records],
        }
        out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def _save_markdown(self):
        """保存Markdown（人类可读）。"""
        out = LOG_DIR / f"{self.today_dash}_行为日志.md"

        # 统计
        type_counts = {}
        colors = {"🟢": 0, "🟡": 0, "🔴": 0}
        for r in self.records:
            type_counts[r.record_type] = type_counts.get(r.record_type, 0) + 1
            colors[r.status] = colors.get(r.status, 0) + 1

        lines = [
            f"# 🧬 龍魂行为日志 · {self.today_dash}",
            f"",
            f"> DNA: {DNA_TAG}",
            f"> 记录数: {len(self.records)} | "
            f"🟢{colors['🟢']} 🟡{colors['🟡']} 🔴{colors['🔴']}",
            f"> 通心翻译: 今天做了{len(self.records)}件事的记录本",
            f"",
            f"| DNA | 状态·类型 | 一句话 | 行为 | 结果 | 来源 |",
            f"|-----|----------|--------|------|------|------|",
        ]

        for r in self.records:
            lines.append(r.to_markdown_line())

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 📋 详细记录")
        lines.append("")

        for r in self.records:
            lines.append(r.to_detail_markdown())

        lines += [
            "---",
            f"",
            f"## 🔗 链路关系",
            f"",
        ]

        # 画链路
        roots = [r for r in self.records if not r.parent_dna]
        for root in roots:
            lines.append(f"- **{root.dna}**: {root.one_line}")
            children = [r for r in self.records if r.parent_dna == root.dna]
            for child in children:
                lines.append(f"  - **{child.dna}**: {child.one_line}")
                grandchildren = [r for r in self.records if r.parent_dna == child.dna]
                for gc in grandchildren:
                    lines.append(f"    - **{gc.dna}**: {gc.one_line}")

        lines += [
            "",
            "---",
            f"GPG: {GPG_FP}",
            f"创建者: 诸葛鑫（UID9622）",
            f"理论指导: 曾仕强老师（永恒显示）",
            f"铁律: 灵感可以乱，记录必须准",
        ]

        out.write_text("\n".join(lines), encoding="utf-8")

    # ── Notion同步 ──────────────────────────────────────

    def sync_to_notion(self, record: BehaviorRecord, db_id: str) -> bool:
        """
        写入Notion《龍魂·行为日志》数据库。

        参数:
          record: 要同步的记录
          db_id: Notion数据库ID

        返回: 是否成功
        """
        if not NOTION_TOKEN:
            return False

        import urllib.request
        type_info = RECORD_TYPES.get(record.record_type, {})

        payload = {
            "parent": {"database_id": db_id},
            "properties": {
                "🧬 DNA": {"title": [{"type": "text", "text": {"content": record.dna}}]},
                "📌 类型": {"select": {"name": f"{type_info.get('icon','')} {record.record_type}"}},
                "🧠 一句话": {"rich_text": [{"type": "text", "text": {"content": record.one_line}}]},
                "🔧 行为": {"rich_text": [{"type": "text", "text": {"content": record.behavior}}]},
                "📊 结果": {"rich_text": [{"type": "text", "text": {"content": record.result}}]},
                "🔍 来源": {"rich_text": [{"type": "text", "text": {"content": record.source}}]},
                "🔗 上级DNA": {"rich_text": [{"type": "text", "text": {"content": record.parent_dna}}]},
                "⚖️ 状态": {"select": {"name": record.status}},
                "📅 时间": {"date": {"start": record.timestamp.strftime("%Y-%m-%dT%H:%M:%S")}},
            }
        }

        if record.note:
            payload["properties"]["🧾 备注"] = {
                "rich_text": [{"type": "text", "text": {"content": record.note[:2000]}}]
            }

        try:
            req = urllib.request.Request(
                "https://api.notion.com/v1/pages",
                data=json.dumps(payload).encode(),
                headers={
                    "Authorization": f"Bearer {NOTION_TOKEN}",
                    "Notion-Version": "2022-06-28",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            urllib.request.urlopen(req, timeout=10)
            return True
        except Exception:
            return False

    def sync_all_to_notion(self, db_id: str) -> Dict[str, int]:
        """同步今日全部记录到Notion。"""
        success = 0
        fail = 0
        for r in self.records:
            if self.sync_to_notion(r, db_id):
                success += 1
            else:
                fail += 1
        return {"成功": success, "失败": fail}

    # ── 统计与查看 ──────────────────────────────────────

    def stats(self) -> Dict[str, Any]:
        """今日统计。"""
        type_counts = {}
        colors = {"🟢": 0, "🟡": 0, "🔴": 0}
        for r in self.records:
            type_counts[r.record_type] = type_counts.get(r.record_type, 0) + 1
            colors[r.status] = colors.get(r.status, 0) + 1

        return {
            "日期": self.today_dash,
            "总记录": len(self.records),
            "各类型": type_counts,
            "三色": colors,
            "链路数": sum(1 for r in self.records if r.parent_dna),
            "根节点": sum(1 for r in self.records if not r.parent_dna),
        }

    def print_today(self):
        """打印今日记录摘要。"""
        s = self.stats()
        print(f"\n{'━' * 60}")
        print(f"🧬 龍魂行为日志 · {s['日期']}")
        print(f"{'━' * 60}")
        print(f"  共 {s['总记录']} 条 | "
              f"🟢{s['三色']['🟢']} 🟡{s['三色']['🟡']} 🔴{s['三色']['🔴']} | "
              f"链路{s['链路数']}条")
        print(f"{'─' * 60}")

        for r in self.records:
            type_info = RECORD_TYPES.get(r.record_type, {})
            icon = type_info.get("icon", "📝")
            parent = f" ← {r.parent_dna[-15:]}" if r.parent_dna else ""
            print(f"  {r.status} {icon} #{r.seq:02d} {r.one_line[:40]}{parent}")

        print(f"{'─' * 60}")
        print(f"  DNA: {DNA_TAG}")
        print(f"  铁律: 灵感可以乱，记录必须准")
        print(f"{'━' * 60}")


# ════════════════════════════════════════════════════════════════
# 独立运行 · 演示完整流程
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("━" * 60)
    print("🧬 龍芯行为日志引擎 · 完整演示")
    print(f"DNA: {DNA_TAG}")
    print(f"创建者: UID9622 诸葛鑫 · 理论指导: 曾仕强老师")
    print("━" * 60)

    log = BehaviorLog()

    # ── 演示: 商鞅立木思维链 ──
    print("\n📖 演示: 商鞅立木 → 信号博弈 → 规则可信度")

    r1 = log.灵感(
        "信任需要成本证明",
        行为="想到商鞅立木",
        结果="建立信号博弈理解",
        来源="历史案例",
    )
    print(f"  {r1.status} #{r1.seq:02d} 灵感: {r1.one_line}")

    r2 = log.推演(
        "信号博弈=高成本承诺",
        行为="用博弈论解释",
        结果="信任建立机制明确",
        来源="理论推演",
        上级=str(r1.seq),  # 链接到灵感
    )
    print(f"  {r2.status} #{r2.seq:02d} 推演: {r2.one_line} ← #{r1.seq:02d}")

    r3 = log.操作(
        "用369模型验证信号理论",
        行为="做100次数字根收敛测试",
        结果="100%收敛到{3,6,9}",
        来源="实验验证",
        上级=str(r2.seq),  # 链接到推演
    )
    print(f"  {r3.status} #{r3.seq:02d} 操作: {r3.one_line} ← #{r2.seq:02d}")

    r4 = log.总结(
        "规则可信度来自代价",
        行为="综合灵感+推演+操作",
        结果="进入认知体系",
        来源="综合",
    )
    print(f"  {r4.status} #{r4.seq:02d} 总结: {r4.one_line}")

    # ── 演示: 龍魂系统开发链 ──
    print("\n📖 演示: 龍魂系统开发链")

    r5 = log.灵感(
        "三层监督需要红队测试",
        行为="看到安全体系都有红蓝对抗",
        结果="决定给龍魂系统加老顽童",
        来源="ChatGPT灵感",
    )
    print(f"  {r5.status} #{r5.seq:02d} 灵感: {r5.one_line}")

    r6 = log.操作(
        "开发supervision_engine.py",
        行为="写七模块三层监督引擎",
        结果="1438行代码·老顽童100%防御率",
        来源="Claude落地",
        上级=str(r5.seq),
    )
    print(f"  {r6.status} #{r6.seq:02d} 操作: {r6.one_line} ← #{r5.seq:02d}")

    r7 = log.操作(
        "推送GitHub+GitCode",
        行为="git push origin+gitcode main",
        结果="双平台同步成功",
        来源="执行",
        上级=str(r6.seq),
    )
    print(f"  {r7.status} #{r7.seq:02d} 操作: {r7.one_line} ← #{r6.seq:02d}")

    # ── 追溯链路 ──
    print("\n🔗 追溯演示: 从 #07 往上追")
    log.追溯打印(r7.seq)

    print("\n🔗 追溯演示: 从 #03 往上追")
    log.追溯打印(r3.seq)

    # ── 自动今日总结 ──
    print("\n📋 自动生成今日总结")
    daily = log.今日总结()
    print(f"  {daily.status} #{daily.seq:02d} {daily.one_line}")

    # ── 打印今日摘要 ──
    log.print_today()

    # ── 统计 ──
    s = log.stats()
    print(f"\n📊 统计:")
    print(f"  总记录: {s['总记录']}")
    print(f"  各类型: {s['各类型']}")
    print(f"  链路: {s['链路数']}条 | 根节点: {s['根节点']}个")

    # ── 文件位置 ──
    json_path = LOG_DIR / f"{log.today_dash}_行为日志.json"
    md_path = LOG_DIR / f"{log.today_dash}_行为日志.md"
    print(f"\n📁 已保存:")
    print(f"  📦 JSON: {json_path}")
    print(f"  📄 Markdown: {md_path}")

    print(f"\n{'━' * 60}")
    print(f"🟢 行为日志引擎就绪 · 灵感可以乱，记录必须准")
    print(f"DNA: {DNA_TAG}")
    print(f"{'━' * 60}")
