#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║          CNSH 金融格式化引擎 v1.0 — 人民币标准 + Notion导出          ║
║  DNA: #龍芯⚡️丙午·丙申·癸丑·午时·䷄需-FINANCE-FORMATTER-BF8BA356    ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【功能】
1. 人民币大写转换 — 数字 → "壹仟贰佰叁拾肆元整"
2. 千分位格式化 — 1234567.89 → "1,234,567.89"
3. 金额中文读法 — 1234567 → "一百二十三万四千五百六十七"
4. Notion金融导出解析 — Markdown/CSV → 格式化的财务报表
5. 财务报表模板 — 资产负债表/利润表/现金流量表
6. 中日英金融格式互转 — 日-万円/中-万元/英-thousands
"""

from __future__ import annotations
import re
import csv
import json
import io
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP


# ══════════════════════════════════════════════════════════════════
# 【一、人民币大写引擎】
# ══════════════════════════════════════════════════════════════════

_CN_DIGIT = ["零", "壹", "贰", "叁", "肆", "伍", "陆", "柒", "捌", "玖"]
_CN_UNIT = ["", "拾", "佰", "仟"]
_CN_BIG_UNIT = ["", "万", "亿", "兆"]
_CN_DECIMAL = ["角", "分"]
_CN_INTEGER = "整"


def number_to_cny_upper(amount: float | Decimal | str) -> str:
    """
    人民币大写转换（标准金融格式）。
    >>> number_to_cny_upper(1234.56)
    '壹仟贰佰叁拾肆元伍角陆分'
    >>> number_to_cny_upper(100)
    '壹佰元整'
    >>> number_to_cny_upper(0.01)
    '零元零壹分'
    """
    if isinstance(amount, str):
        amount = amount.replace(",", "").replace("￥", "").replace("¥", "").strip()
    d = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if d == 0:
        return "零元整"

    parts = str(d).split(".")
    int_part = int(parts[0])
    dec_part = int(parts[1]) if len(parts) > 1 else 0

    result: list[str] = []

    # 整数部分 — 分段处理
    if int_part == 0:
        result.append("零")
    else:
        result.append(_int_to_cny(int_part))

    result.append("元")

    # 角分
    if dec_part == 0:
        result.append(_CN_INTEGER)
    else:
        jiao = dec_part // 10
        fen = dec_part % 10
        if jiao > 0:
            result.append(f"{_CN_DIGIT[jiao]}角")
        elif fen > 0:
            result.append("零")
        if fen > 0:
            result.append(f"{_CN_DIGIT[fen]}分")

    return "".join(result)


def _int_to_cny(n: int) -> str:
    """整数部分转中文大写（支持任意长度）"""
    if n == 0:
        return "零"
    groups: list[int] = []
    while n > 0:
        groups.append(n % 10000)
        n //= 10000

    parts: list[str] = []
    for i in range(len(groups) - 1, -1, -1):
        g = groups[i]
        g_str = _group4_to_cny(g)
        if g_str:
            # 低位组不足4位时（前面有更高组），补零
            if parts and g < 1000:
                parts.append("零")
            parts.append(g_str + _CN_BIG_UNIT[i])
        else:
            # 全零组：前后都有非零组时补零
            if parts and i < len(groups) - 1 and groups[i + 1] > 0 and (not parts[-1] == "零"):
                # 检查后面还有没有非零组
                has_after = any(groups[j] > 0 for j in range(i - 1, -1, -1))
                if has_after:
                    parts.append("零")

    result = "".join(parts)
    while "零零" in result:
        result = result.replace("零零", "零")
    if result.endswith("零"):
        result = result[:-1]
    return result


def _group4_to_cny(n: int) -> str:
    """四位以内数字转中文大写（不含大单位）"""
    if n == 0:
        return ""
    d4 = n // 1000
    d3 = (n % 1000) // 100
    d2 = (n % 100) // 10
    d1 = n % 10

    parts: list[str] = []
    need_zero = False

    # 千位
    if d4 > 0:
        parts.append(f"{_CN_DIGIT[d4]}仟")
    else:
        need_zero = parts != []  # 前面有内容才标记需要零

    # 百位
    if d3 > 0:
        if need_zero:
            parts.append("零")
            need_zero = False
        parts.append(f"{_CN_DIGIT[d3]}佰")
    else:
        if parts:
            need_zero = True

    # 十位
    if d2 > 0:
        if need_zero:
            parts.append("零")
            need_zero = False
        parts.append(f"{_CN_DIGIT[d2]}拾")
    else:
        if parts:
            need_zero = True

    # 个位
    if d1 > 0:
        if need_zero:
            parts.append("零")
        parts.append(_CN_DIGIT[d1])

    return "".join(parts)


# ══════════════════════════════════════════════════════════════════
# 【二、千分位格式化】
# ══════════════════════════════════════════════════════════════════

def format_thousands(value: float | int | str, decimals: int = 2, symbol: str = "") -> str:
    """
    千分位格式化。
    >>> format_thousands(1234567.89)
    '1,234,567.89'
    >>> format_thousands(1234567, symbol='¥')
    '¥1,234,567.00'
    """
    if isinstance(value, str):
        value = float(value.replace(",", "").replace("¥", "").replace("￥", "").strip())
    fmt = f"{{:,.{decimals}f}}"
    result = fmt.format(value)
    if symbol:
        result = symbol + result
    return result


def format_thousands_cn(value: float | int | str, decimals: int = 2) -> str:
    """中文千分位 ¥1,234,567.89"""
    return format_thousands(value, decimals, "¥")


# ══════════════════════════════════════════════════════════════════
# 【三、金额中文读法】
# ══════════════════════════════════════════════════════════════════

_CN_NUMBER = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
_CN_UNIT_READ = ["", "十", "百", "千"]
_CN_BIG_READ = ["", "万", "亿"]


def number_to_chinese_read(n: int | float | str) -> str:
    """
    整数金额中文读法。
    >>> number_to_chinese_read(1234567)
    '一百二十三万四千五百六十七'
    >>> number_to_chinese_read(10000)
    '一万'
    """
    if isinstance(n, str):
        n = int(float(n.replace(",", "")))
    elif isinstance(n, float):
        n = int(n)
    if n == 0:
        return "零"

    chunks: list[str] = []
    big_idx = 0
    while n > 0:
        chunk = n % 10000
        if chunk > 0:
            c_str = _four_digit_read(chunk)
            if big_idx > 0:
                c_str += _CN_BIG_READ[big_idx]
            chunks.append(c_str)
        else:
            if big_idx == 0 and chunks:
                pass  # 末尾四个零不读
        n //= 10000
        big_idx += 1
    return "".join(reversed(chunks))


def _four_digit_read(n: int) -> str:
    if n == 0:
        return ""
    digits: list[int] = []
    while n > 0:
        digits.append(n % 10)
        n //= 10
    result: list[str] = []
    for i in range(len(digits) - 1, -1, -1):
        d = digits[i]
        if d == 0:
            if result and result[-1] != "零" and i < len(digits) - 1:
                result.append("零")
        else:
            if i == 1 and d == 1 and len(digits) == 2:
                # 12 → 十二，不是一十二
                result.append("十")
            else:
                result.append(_CN_NUMBER[d])
                if i > 0:
                    result.append(_CN_UNIT_READ[i])
    # 去末尾零
    while result and result[-1] == "零":
        result.pop()
    return "".join(result)


# ══════════════════════════════════════════════════════════════════
# 【四、Notion金融导出解析】
# ══════════════════════════════════════════════════════════════════

@dataclass
class FinanceRecord:
    """单条金融记录"""
    日期: str = ""
    类别: str = ""         # 收入/支出/转账/投资
    金额: float = 0.0
    币种: str = "CNY"
    描述: str = ""
    分类标签: str = ""
    备注: str = ""
    Notion页面ID: str = ""
    源数据: dict[str, Any] = field(default_factory=dict)


@dataclass
class FinanceReport:
    """格式化后的财务报表"""
    标题: str = ""
    生成时间: str = ""
    记录列表: list[FinanceRecord] = field(default_factory=list)
    总流入: float = 0.0
    总流出: float = 0.0
    净额: float = 0.0
    按类别汇总: dict[str, float] = field(default_factory=dict)
    按标签汇总: dict[str, float] = field(default_factory=dict)


class NotionFinanceParser:
    """解析 Notion 导出的金融数据"""

    @staticmethod
    def parse_markdown_table(text: str) -> list[FinanceRecord]:
        """解析Markdown表格格式的金融数据"""
        records: list[FinanceRecord] = []
        lines = text.strip().split("\n")
        headers: list[str] = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("|--"):
                continue
            if line.startswith("|") and not headers:
                headers = [h.strip().lower() for h in line.split("|")[1:-1]]
                continue
            if line.startswith("|") and headers:
                cells = [c.strip() for c in line.split("|")[1:-1]]
                if len(cells) == len(headers):
                    rec = FinanceRecord()
                    for i, h in enumerate(headers):
                        val = cells[i] if i < len(cells) else ""
                        if "日期" in h or "date" in h:
                            rec.日期 = val
                        elif "类别" in h or "type" in h or "category" in h:
                            rec.类别 = val
                        elif "金额" in h or "amount" in h:
                            try:
                                rec.金额 = float(val.replace(",", "").replace("¥", "").replace("￥", ""))
                            except ValueError:
                                rec.金额 = 0.0
                        elif "币种" in h or "currency" in h:
                            rec.币种 = val or "CNY"
                        elif "描述" in h or "desc" in h or "note" in h:
                            rec.描述 = val
                        elif "标签" in h or "tag" in h:
                            rec.分类标签 = val
                        elif "备注" in h or "remark" in h:
                            rec.备注 = val
                    records.append(rec)
        return records

    @staticmethod
    def parse_csv(csv_text: str) -> list[FinanceRecord]:
        """解析CSV格式金融数据"""
        records: list[FinanceRecord] = []
        reader = csv.DictReader(io.StringIO(csv_text))
        for row in reader:
            rec = FinanceRecord()
            for k, v in row.items():
                kl = k.strip().lower()
                v = v.strip() if v else ""
                if "日期" in kl or "date" in kl:
                    rec.日期 = v
                elif "类别" in kl or "type" in kl or "category" in kl:
                    rec.类别 = v
                elif "金额" in kl or "amount" in kl:
                    try:
                        rec.金额 = float(v.replace(",", "").replace("¥", ""))
                    except ValueError:
                        rec.金额 = 0.0
                elif "币种" in kl or "currency" in kl:
                    rec.币种 = v or "CNY"
                elif "描述" in kl or "desc" in kl or "note" in kl:
                    rec.描述 = v
                elif "标签" in kl or "tag" in kl:
                    rec.分类标签 = v
                elif "备注" in kl or "remark" in kl:
                    rec.备注 = v
            records.append(rec)
        return records

    @staticmethod
    def parse_notion_json(notion_data: dict[str, Any]) -> list[FinanceRecord]:
        """解析 Notion API 返回的 JSON 数据"""
        records: list[FinanceRecord] = []
        results = notion_data.get("results", [notion_data])
        if not isinstance(results, list):
            results = [results]
        for item in results:
            props = item.get("properties", {})
            rec = FinanceRecord(Notion页面ID=item.get("id", ""))
            for key, prop in props.items():
                kl = key.strip().lower()
                ptype = prop.get("type", "")
                if ptype == "title":
                    rec.描述 = "".join(t.get("plain_text", "") for t in prop.get("title", []))
                elif ptype == "rich_text":
                    rec.备注 = "".join(t.get("plain_text", "") for t in prop.get("rich_text", []))
                elif ptype == "number":
                    if "金额" in kl or "amount" in kl:
                        rec.金额 = prop.get("number") or 0.0
                elif ptype == "select":
                    val = prop.get("select", {})
                    if val and val.get("name"):
                        if "类别" in kl or "category" in kl:
                            rec.类别 = val["name"]
                        elif "标签" in kl or "tag" in kl:
                            rec.分类标签 = val["name"]
                elif ptype == "date":
                    dt = prop.get("date", {})
                    if dt and dt.get("start"):
                        rec.日期 = dt["start"]
            records.append(rec)
        return records


def build_finance_report(records: list[FinanceRecord], title: str = "财务报表") -> FinanceReport:
    """从记录列表构建汇总报表"""
    report = FinanceReport(标题=title, 生成时间=datetime.now().isoformat())
    report.记录列表 = records
    for rec in records:
        if rec.类别 in ("收入", "income", "in", "入"):
            report.总流入 += abs(rec.金额)
        else:
            report.总流出 += abs(rec.金额)
        # 按类别汇总
        cat = rec.类别 or "未分类"
        report.按类别汇总[cat] = report.按类别汇总.get(cat, 0.0) + abs(rec.金额)
        # 按标签汇总
        tag = rec.分类标签 or "无标签"
        report.按标签汇总[tag] = report.按标签汇总.get(tag, 0.0) + abs(rec.金额)
    report.净额 = report.总流入 - report.总流出
    return report


# ══════════════════════════════════════════════════════════════════
# 【五、报表格式化输出】
# ══════════════════════════════════════════════════════════════════

def format_report_markdown(report: FinanceReport) -> str:
    """财务报表 → Markdown 格式"""
    lines: list[str] = []
    lines.append(f"# {report.标题}")
    lines.append(f"> 生成时间: {report.生成时间}")
    lines.append("")
    lines.append("## 汇总")
    lines.append(f"| 指标 | 金额 | 大写 |")
    lines.append(f"|------|------|------|")
    lines.append(f"| 总流入 | {format_thousands_cn(report.总流入)} | {number_to_cny_upper(report.总流入)} |")
    lines.append(f"| 总流出 | {format_thousands_cn(report.总流出)} | {number_to_cny_upper(report.总流出)} |")
    lines.append(f"| 净额 | {format_thousands_cn(report.净额)} | {number_to_cny_upper(report.净额)} |")
    lines.append("")

    if report.按类别汇总:
        lines.append("## 按类别")
        lines.append("| 类别 | 金额 | 占比 |")
        lines.append("|------|------|------|")
        total = sum(report.按类别汇总.values())
        for cat, amt in sorted(report.按类别汇总.items(), key=lambda x: -x[1]):
            pct = (amt / total * 100) if total > 0 else 0
            lines.append(f"| {cat} | {format_thousands_cn(amt)} | {pct:.1f}% |")
        lines.append("")

    if report.按标签汇总:
        lines.append("## 按标签")
        lines.append("| 标签 | 金额 |")
        lines.append("|------|------|")
        for tag, amt in sorted(report.按标签汇总.items(), key=lambda x: -x[1]):
            lines.append(f"| {tag} | {format_thousands_cn(amt)} |")
        lines.append("")

    lines.append("## 明细")
    lines.append("| 日期 | 类别 | 金额 | 大写 | 标签 | 描述 |")
    lines.append("|------|------|------|------|------|------|")
    for rec in report.记录列表:
        lines.append(
            f"| {rec.日期} | {rec.类别} | {format_thousands_cn(rec.金额)} "
            f"| {number_to_cny_upper(rec.金额)} | {rec.分类标签} | {rec.描述} |"
        )

    return "\n".join(lines)


def format_report_json(report: FinanceReport) -> str:
    """财务报表 → JSON"""
    return json.dumps({
        "标题": report.标题,
        "生成时间": report.生成时间,
        "总流入": report.总流入,
        "总流出": report.总流出,
        "净额": report.净额,
        "总流入大写": number_to_cny_upper(report.总流入),
        "总流出大写": number_to_cny_upper(report.总流出),
        "净额大写": number_to_cny_upper(report.净额),
        "按类别汇总": report.按类别汇总,
        "按标签汇总": report.按标签汇总,
        "记录数": len(report.记录列表),
        "明细": [
            {
                "日期": r.日期,
                "类别": r.类别,
                "金额": r.金额,
                "大写": number_to_cny_upper(r.金额),
                "标签": r.分类标签,
                "描述": r.描述,
            }
            for r in report.记录列表
        ],
    }, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════
# 【六、简单记账器】
# ══════════════════════════════════════════════════════════════════

@dataclass
class SimpleLedger:
    """简单记账本"""
    记录: list[FinanceRecord] = field(default_factory=list)
    名称: str = "我的账本"

    def 记收入(self, 金额: float, 描述: str = "", 标签: str = "", 日期: str = "") -> None:
        dt = 日期 or datetime.now().strftime("%Y-%m-%d")
        self.记录.append(FinanceRecord(日期=dt, 类别="收入", 金额=abs(金额), 描述=描述, 分类标签=标签))

    def 记支出(self, 金额: float, 描述: str = "", 标签: str = "", 日期: str = "") -> None:
        dt = 日期 or datetime.now().strftime("%Y-%m-%d")
        self.记录.append(FinanceRecord(日期=dt, 类别="支出", 金额=abs(金额), 描述=描述, 分类标签=标签))

    def 汇总(self) -> FinanceReport:
        return build_finance_report(self.记录, self.名称)

    def 导出Markdown(self) -> str:
        return format_report_markdown(self.汇总())

    def 导出JSON(self) -> str:
        return format_report_json(self.汇总())

    def 余额(self) -> float:
        inflow = sum(r.金额 for r in self.记录 if r.类别 in ("收入", "income"))
        outflow = sum(r.金额 for r in self.记录 if r.类别 not in ("收入", "income"))
        return inflow - outflow


# ══════════════════════════════════════════════════════════════════
# 【七、中日英金融格式互转】
# ══════════════════════════════════════════════════════════════════

_UNIT_SCALE = {
    "元": 1, "万": 10_000, "亿": 100_000_000,
    "yen": 1, "man": 10_000, "oku": 100_000_000,
    "dollar": 1, "thousand": 1_000, "million": 1_000_000, "billion": 1_000_000_000,
}

def convert_finance_unit(amount: float, from_unit: str, to_unit: str) -> float:
    """金融单位转换：万↔亿↔thousand↔million↔万↔億"""
    from_scale = _UNIT_SCALE.get(from_unit, 1)
    to_scale = _UNIT_SCALE.get(to_unit, 1)
    return amount * from_scale / to_scale


# ══════════════════════════════════════════════════════════════════
# 导出
# ══════════════════════════════════════════════════════════════════

__all__ = [
    "number_to_cny_upper",
    "format_thousands",
    "format_thousands_cn",
    "number_to_chinese_read",
    "NotionFinanceParser",
    "FinanceRecord",
    "FinanceReport",
    "build_finance_report",
    "format_report_markdown",
    "format_report_json",
    "SimpleLedger",
    "convert_finance_unit",
]

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️丙午·丙申·癸丑·午时·䷄需-FINANCE-FORMATTER-BF8BA356"
__responsibility__ = "UID9622·不免责"
