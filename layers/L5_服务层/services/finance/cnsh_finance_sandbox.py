# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║           CNSH 金融爬虫沙箱 v1.0 — 数据摄取 + 变量化管理               ║
║  DNA: #龍芯⚡️2026-07-06-FINANCE-SANDBOX-v1.0                       ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F                     ║
║  三色审计: 🟢 通过                                                   ║
╚══════════════════════════════════════════════════════════════════════╝

【设计意图】
金融数据爬取 → 自动注入沙箱变量 → 变量可用 CNSH 语法直接操作。
不再需要手动定义金融变量，爬虫爬回来自动注册为 CNSH 变量。

【数据源】
- 新浪财经：A 股行情
- Binance：数字货币价格
- 更多数据源按需扩展

【安全边界】
- 只读爬取，不修改任何系统文件
- 爬取结果在沙箱内隔离
- 支持频率限制防止被封
- 所有数据变量自动绑 DNA 追溯码
"""

from __future__ import annotations
import json
import os
import re
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Any
from dataclasses import dataclass, field
from datetime import datetime


# ══════════════════════════════════════════════════════════════════
# 【一、数据模型】
# ══════════════════════════════════════════════════════════════════

@dataclass
class FinanceVar:
    """金融变量定义"""
    中文名: str
    英文名: str
    cns类型: str           # 整数/小数/文本
    值: Any
    数据源: str            # sina/binance/...
    原始代码: str          # 股票代码/币对
    爬取时间: float = field(default_factory=time.time)
    DNA: str = ""

    def to_sandbox_entry(self) -> tuple[str, str, object, str, bool]:
        """转为 VarSandbox.register_batch 格式"""
        return (self.中文名, self.cns类型, self.值, self.英文名, False)


@dataclass
class FinanceCrawlRule:
    """爬取规则"""
    名称: str
    类型: str              # 股票/指数/汇率/数字货币
    代码: str
    数据源: str            # sina/binance
    间隔秒: int = 5        # 最小请求间隔
    重试次数: int = 3
    超时秒数: int = 10


# ══════════════════════════════════════════════════════════════════
# 【二、爬虫引擎】
# ══════════════════════════════════════════════════════════════════

class FinanceCrawler:
    """
    金融数据爬虫引擎。
    安全、频率控制、自动变量化。
    """

    def __init__(self):
        self.规则列表: list[FinanceCrawlRule] = []
        self.最后请求时间: dict[str, float] = {}
        self.爬取变量: list[FinanceVar] = []

    def add_rule(self, rule: FinanceCrawlRule):
        """添加爬取规则"""
        self.规则列表.append(rule)

    def _rate_limit(self, source: str):
        """频率限制：确保两次请求间隔 ≥ 规则要求"""
        now = time.time()
        if source in self.最后请求时间:
            elapsed = now - self.最后请求时间[source]
            # 找到该源的最大间隔
            max_interval = 5
            for r in self.规则列表:
                if r.数据源 == source and r.间隔秒 > max_interval:
                    max_interval = r.间隔秒
            if elapsed < max_interval:
                time.sleep(max_interval - elapsed)
        self.最后请求时间[source] = time.time()

    def crawl_stock_sina(self, code: str) -> dict[str, object] | None:
        """
        从新浪财经爬取 A 股行情。

        返回字段：
          名称, 今开, 昨收, 现价, 最高, 最低,
          买一价, 卖一价, 成交量, 成交额,
          涨跌额, 涨跌幅, 日期, 时间
        """
        self._rate_limit("sina")
        try:
            market = "sh" if code.startswith("6") else "sz"
            full_code = f"{market}{code}"
            url = f"http://hq.sinajs.cn/list={full_code}"

            req = urllib.request.Request(url, headers={
                "Referer": "http://finance.sina.com.cn",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Accept": "*/*",
            })
            with urllib.request.urlopen(req, timeout=8) as resp:
                text = resp.read().decode("gbk", errors="replace")

            match = re.search(r'"(.+)"', text)
            if not match:
                return None

            fields = match.group(1).split(",")
            if len(fields) < 32:
                return None

            return {
                "名称": fields[0].strip(),
                "今开": self._safe_float(fields[1]),
                "昨收": self._safe_float(fields[2]),
                "现价": self._safe_float(fields[3]),
                "最高": self._safe_float(fields[4]),
                "最低": self._safe_float(fields[5]),
                "买一": self._safe_float(fields[6]),
                "卖一": self._safe_float(fields[7]),
                "成交量": self._safe_int(fields[8]),
                "成交额": self._safe_float(fields[9]),
                "日期": fields[30].strip(),
                "时间": fields[31].strip() if len(fields) > 31 else "",
            }
        except Exception as e:
            return {"错误": f"新浪爬取异常: {e}"}

    def crawl_crypto_binance(self, symbol: str) -> dict[str, object] | None:
        """
        从 Binance 拉取数字货币 Ticker。

        返回字段：价格
        """
        self._rate_limit("binance")
        try:
            symbol_u = symbol.upper().replace("/", "")
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol_u}"
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0",
            })
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())
            return {"价格": float(data["price"])}
        except Exception as e:
            return {"错误": f"Binance 爬取异常: {e}"}

    def crawl_crypto_okx(self, symbol: str) -> dict[str, object] | None:
        """
        从 OKX 拉取数字货币 Ticker。

        返回字段：价格
        """
        self._rate_limit("okx")
        try:
            symbol_u = symbol.upper().replace("/", "-")
            url = f"https://www.okx.com/api/v5/market/ticker?instId={symbol_u}"
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "application/json",
            })
            with urllib.request.urlopen(req, timeout=8) as resp:
                data = json.loads(resp.read().decode())
            if data.get("code") == "0" and data.get("data"):
                return {"价格": float(data["data"][0]["last"])}
            return {"错误": f"OKX 返回异常: {data.get('msg', '未知')}"}
        except Exception as e:
            return {"错误": f"OKX 爬取异常: {e}"}

    def to_sandbox_vars(self, data: dict[str, object], prefix: str, source: str) -> list[FinanceVar]:
        """将爬取数据转为沙箱变量列表"""
        vars_list = []
        for key, val in data.items():
            if key == "错误":
                continue
            var_type = "小数" if isinstance(val, float) else ("整数" if isinstance(val, int) else "文本")
            vars_list.append(FinanceVar(
                中文名=f"{prefix}{key}",
                英文名=f"{prefix}{key}",
                cns类型=var_type,
                值=val,
                数据源=source,
                原始代码=prefix.strip("_"),
            ))
        return vars_list

    async def crawl_and_register(self, rules: list[FinanceCrawlRule]) -> list[FinanceVar]:  # pyright: ignore[reportReturnType]
        """爬取所有规则并返回金融变量列表"""
        all_vars: list[FinanceVar] = []

        for rule in rules:
            data = None
            prefix = ""  # pyright: ignore[reportUnusedVariable]

            if rule.数据源 == "sina" and rule.类型 == "股票":
                data = self.crawl_stock_sina(rule.代码)
                prefix = f"股票_{rule.代码}_"
            elif rule.数据源 == "binance" and rule.类型 == "数字货币":
                data = self.crawl_crypto_binance(rule.代码)
                prefix = f"币_{rule.代码}_"
            elif rule.数据源 == "okx" and rule.类型 == "数字货币":
                data = self.crawl_crypto_okx(rule.代码)
                prefix = f"币_{rule.代码}_"

            if data and "错误" not in data:
                vars_list = self.to_sandbox_vars(data, prefix, rule.数据源)
                for v in vars_list:
                    生成DNA(v)
                all_vars.extend(vars_list)

        self.爬取变量 = all_vars
        return all_vars

    @staticmethod
    def _safe_float(s: str) -> float:
        try:
            return float(s)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def _safe_int(s: str) -> int:
        try:
            return int(float(s))
        except (ValueError, TypeError):
            return 0


# ══════════════════════════════════════════════════════════════════
# 【三、DNA 生成】
# ══════════════════════════════════════════════════════════════════

def 生成DNA(var: FinanceVar):
    """为金融变量生成 DNA 追溯码"""
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    raw = f"{var.中文名}-{var.数据源}-{var.爬取时间}"
    h = hashlib.sha256(raw.encode()).hexdigest()[:8]
    var.DNA = f"#龍芯⚡️{date_str}-FINANCE-VAR-{h.upper()}"


# ══════════════════════════════════════════════════════════════════
# 【四、快速使用】
# ══════════════════════════════════════════════════════════════════

async def quick_crawl_stock(code: str) -> list[FinanceVar]:
    """快速爬取单只股票"""
    crawler = FinanceCrawler()
    rule = FinanceCrawlRule(
        名称=f"A股-{code}",
        类型="股票",
        代码=code,
        数据源="sina",
    )
    vars_list = await crawler.crawl_and_register([rule])
    return vars_list


async def quick_crawl_crypto(symbol: str, source: str = "binance") -> list[FinanceVar]:
    """快速爬取数字货币"""
    crawler = FinanceCrawler()
    rule = FinanceCrawlRule(
        名称=f"币-{symbol}",
        类型="数字货币",
        代码=symbol,
        数据源=source,
    )
    vars_list = await crawler.crawl_and_register([rule])
    return vars_list


# ══════════════════════════════════════════════════════════════════
# 导出
# ══════════════════════════════════════════════════════════════════

__all__ = [
    "FinanceVar",
    "FinanceCrawlRule",
    "FinanceCrawler",
    "quick_crawl_stock",
    "quick_crawl_crypto",
    "生成DNA",
]

__version__ = "1.0.0"
__author__ = "UID9622 · 诸葛鑫 · 龍芯北辰"
__dna__ = "#龍芯⚡️2026-07-06-FINANCE-SANDBOX-v1.0"
__responsibility__ = "UID9622·不免责"
