#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂分页引擎 · PageHelper 龍魂版                        ║
║  DNA: #龍芯⚡️2026-04-12-PAGEHELPER-v1.0                 ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

灵感来源: Mybatis-PageHelper (MIT · 12.4k星)
龍魂改造: Java → Python · MyBatis → SQLite/Notion/JSONL
保留核心: 透明分页 · 自动count · 多数据源支持

三个数据源全覆盖:
  1. SQLite  → 本地数据库分页
  2. Notion  → API分页 (cursor-based)
  3. JSONL   → 日志文件分页 (流式读取)

老大说接入操作台 → 操作台查数据不再一次性全拉

献给每一个相信技术应该有温度的人。
"""

import json
import math
import sqlite3
import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass, field

SYSTEM_ROOT = Path.home() / "longhun-system"

# ═══════════════════════════════════════════
# 分页结果
# ═══════════════════════════════════════════

@dataclass
class PageInfo:
    """
    分页信息 —— 对标 PageHelper 的 PageInfo<T>

    用法:
        page = PageHelper.paginate(data, page_num=1, page_size=10)
        print(page.items)       # 当前页数据
        print(page.total)       # 总记录数
        print(page.pages)       # 总页数
        print(page.has_next)    # 还有下一页吗
    """
    page_num: int = 1              # 当前页码（从1开始）
    page_size: int = 20            # 每页条数
    total: int = 0                 # 总记录数
    pages: int = 0                 # 总页数
    items: list = field(default_factory=list)  # 当前页数据

    @property
    def has_prev(self) -> bool:
        return self.page_num > 1

    @property
    def has_next(self) -> bool:
        return self.page_num < self.pages

    @property
    def start_row(self) -> int:
        """起始行号（0-based）"""
        return (self.page_num - 1) * self.page_size

    @property
    def end_row(self) -> int:
        """结束行号（不含）"""
        return min(self.start_row + self.page_size, self.total)

    def to_dict(self) -> dict:
        return {
            "页码": self.page_num,
            "每页": self.page_size,
            "总数": self.total,
            "总页": self.pages,
            "本页条数": len(self.items),
            "有上一页": self.has_prev,
            "有下一页": self.has_next,
        }

    def display(self) -> str:
        """可视化分页状态"""
        # 页码导航条
        nav = []
        for p in range(1, self.pages + 1):
            if p == self.page_num:
                nav.append(f"[{p}]")
            elif abs(p - self.page_num) <= 2 or p == 1 or p == self.pages:
                nav.append(str(p))
            elif abs(p - self.page_num) == 3:
                nav.append("...")

        # 去重连续的...
        clean_nav = []
        for n in nav:
            if n == "..." and clean_nav and clean_nav[-1] == "...":
                continue
            clean_nav.append(n)

        nav_str = " ".join(clean_nav)

        lines = [
            f"📄 第{self.page_num}/{self.pages}页 · 共{self.total}条 · 每页{self.page_size}条",
            f"   显示第{self.start_row + 1}-{self.end_row}条",
            f"   {'⬅️ ' if self.has_prev else '  '}{nav_str}{'  ➡️' if self.has_next else ''}",
        ]
        return "\n".join(lines)


# ═══════════════════════════════════════════
# 核心分页器
# ═══════════════════════════════════════════

class PageHelper:
    """
    龍魂分页引擎

    三种分页模式:
    1. 内存分页  → 对list直接切片（小数据量）
    2. SQLite分页 → LIMIT/OFFSET（数据库查询）
    3. JSONL分页  → 流式读取指定行范围（大日志文件）

    用法（像 PageHelper 一样简单）:
        # 内存分页
        page = PageHelper.paginate(my_list, page_num=2, page_size=10)

        # SQLite分页
        page = PageHelper.sql("SELECT * FROM logs", page_num=1, page_size=20,
                              db_path="logs.db")

        # JSONL分页
        page = PageHelper.jsonl("dispatch.jsonl", page_num=3, page_size=50)
    """

    # ── 内存分页 ──

    @staticmethod
    def paginate(data: list, page_num: int = 1, page_size: int = 20,
                 sort_key: Callable = None, reverse: bool = False) -> PageInfo:
        """
        内存列表分页

        data:      完整数据列表
        page_num:  页码（从1开始）
        page_size: 每页条数
        sort_key:  排序函数（可选）
        reverse:   是否倒序
        """
        if sort_key:
            data = sorted(data, key=sort_key, reverse=reverse)
        elif reverse:
            data = list(reversed(data))

        total = len(data)
        pages = max(1, math.ceil(total / page_size))
        page_num = max(1, min(page_num, pages))

        start = (page_num - 1) * page_size
        end = start + page_size
        items = data[start:end]

        return PageInfo(
            page_num=page_num,
            page_size=page_size,
            total=total,
            pages=pages,
            items=items,
        )

    # ── SQLite 分页 ──

    @staticmethod
    def sql(query: str, page_num: int = 1, page_size: int = 20,
            db_path: str = None, params: tuple = ()) -> PageInfo:
        """
        SQLite 分页查询

        自动注入 LIMIT/OFFSET，自动 COUNT(*)
        """
        if db_path is None:
            db_path = str(SYSTEM_ROOT / "data" / "longhun.db")

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        try:
            # 1. 先查总数
            count_query = f"SELECT COUNT(*) as cnt FROM ({query})"
            cursor = conn.execute(count_query, params)
            total = cursor.fetchone()["cnt"]

            # 2. 计算分页
            pages = max(1, math.ceil(total / page_size))
            page_num = max(1, min(page_num, pages))
            offset = (page_num - 1) * page_size

            # 3. 注入 LIMIT/OFFSET
            paged_query = f"{query} LIMIT {page_size} OFFSET {offset}"
            cursor = conn.execute(paged_query, params)
            rows = cursor.fetchall()
            items = [dict(row) for row in rows]

            return PageInfo(
                page_num=page_num,
                page_size=page_size,
                total=total,
                pages=pages,
                items=items,
            )
        finally:
            conn.close()

    # ── JSONL 分页 ──

    @staticmethod
    def jsonl(file_path: str, page_num: int = 1, page_size: int = 20,
              filter_fn: Callable = None, reverse: bool = True) -> PageInfo:
        """
        JSONL 日志文件分页

        file_path:  JSONL文件路径（相对于longhun-system或绝对路径）
        filter_fn:  过滤函数（可选），传入一条记录dict，返回True保留
        reverse:    默认最新的在前面
        """
        p = Path(file_path)
        if not p.is_absolute():
            p = SYSTEM_ROOT / file_path

        if not p.exists():
            return PageInfo(page_num=1, page_size=page_size, total=0, pages=0, items=[])

        # 读取全部行（JSONL通常不会太大）
        records = []
        with open(p, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    if filter_fn is None or filter_fn(record):
                        records.append(record)
                except json.JSONDecodeError:
                    continue

        if reverse:
            records.reverse()

        return PageHelper.paginate(records, page_num=page_num, page_size=page_size)

    # ── Notion 分页 ──

    @staticmethod
    def notion_results(results: list, page_num: int = 1,
                       page_size: int = 20) -> PageInfo:
        """
        Notion API 结果分页

        Notion API 本身有 cursor 分页，这里处理的是
        已经拉取到本地的结果集的二次分页显示
        """
        return PageHelper.paginate(results, page_num=page_num, page_size=page_size)

    # ── 文件列表分页 ──

    @staticmethod
    def files(directory: str = None, pattern: str = "*",
              page_num: int = 1, page_size: int = 20,
              sort_by: str = "mtime") -> PageInfo:
        """
        文件列表分页

        directory: 目录路径
        pattern:   glob模式
        sort_by:   排序方式 (mtime/name/size)
        """
        d = Path(directory) if directory else SYSTEM_ROOT
        files = list(d.glob(pattern))

        # 构造文件信息
        file_infos = []
        for f in files:
            if f.is_file():
                try:
                    stat = f.stat()
                    file_infos.append({
                        "名称": f.name,
                        "路径": str(f),
                        "大小": stat.st_size,
                        "大小显示": _format_size(stat.st_size),
                        "修改时间": datetime.datetime.fromtimestamp(
                            stat.st_mtime).strftime("%Y-%m-%d %H:%M"),
                    })
                except Exception:
                    continue

        # 排序
        sort_keys = {
            "mtime": lambda x: x["修改时间"],
            "name": lambda x: x["名称"],
            "size": lambda x: x["大小"],
        }
        key_fn = sort_keys.get(sort_by, sort_keys["mtime"])

        return PageHelper.paginate(
            file_infos, page_num=page_num, page_size=page_size,
            sort_key=key_fn, reverse=(sort_by == "mtime")
        )

    # ── 记忆文件分页 ──

    @staticmethod
    def memories(keyword: str = "", page_num: int = 1,
                 page_size: int = 10) -> PageInfo:
        """
        记忆文件分页查询
        """
        memory_dir = Path.home() / ".claude" / "projects" / "-Users-zuimeidedeyihan" / "memory"
        if not memory_dir.exists():
            return PageInfo(total=0, pages=0, items=[])

        results = []
        for f in sorted(memory_dir.glob("*.md"), key=lambda x: x.stat().st_mtime, reverse=True):
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                if keyword and keyword not in content:
                    continue
                # 提取前3行作为摘要
                lines = [l for l in content.splitlines() if l.strip()][:3]
                results.append({
                    "文件": f.name,
                    "摘要": " | ".join(lines)[:100],
                    "大小": f"{f.stat().st_size:,} 字节",
                    "修改": datetime.datetime.fromtimestamp(
                        f.stat().st_mtime).strftime("%m-%d %H:%M"),
                })
            except Exception:
                continue

        return PageHelper.paginate(results, page_num=page_num, page_size=page_size)

    # ── 日志分页 ──

    @staticmethod
    def logs(log_name: str = "baobao_dispatch",
             page_num: int = 1, page_size: int = 20,
             filter_fn: Callable = None) -> PageInfo:
        """
        龍魂系统日志分页

        log_name: 日志文件名（不带.jsonl后缀）
        """
        log_path = SYSTEM_ROOT / "logs" / f"{log_name}.jsonl"
        return PageHelper.jsonl(str(log_path), page_num=page_num,
                                page_size=page_size, filter_fn=filter_fn)


def _format_size(size: int) -> str:
    """人话文件大小"""
    if size < 1024:
        return f"{size}B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.1f}KB"
    else:
        return f"{size / (1024 * 1024):.1f}MB"


# ═══════════════════════════════════════════
# CLI 入口
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("🐉 龍魂分页引擎 v1.0 (灵感: Mybatis-PageHelper)")
        print()
        print("用法:")
        print("  python3 page_helper.py demo               # 分页演示")
        print("  python3 page_helper.py logs [页码]         # 查调度日志")
        print("  python3 page_helper.py files [页码]        # 查文件列表")
        print("  python3 page_helper.py memories [关键词]   # 查记忆文件")
        print("  python3 page_helper.py refusal [页码]      # 查拒绝日志")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "demo":
        print("═══════════════════════════════════════")
        print("🐉 分页演示")
        print("═══════════════════════════════════════")

        # 模拟100条数据
        data = [{"id": i, "内容": f"第{i}条记录"} for i in range(1, 101)]

        for pn in [1, 3, 5, 10]:
            page = PageHelper.paginate(data, page_num=pn, page_size=10)
            print(f"\n{page.display()}")
            print(f"   数据: {page.items[0]['内容']} ... {page.items[-1]['内容']}")

    elif cmd == "logs":
        pn = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        page = PageHelper.logs("baobao_dispatch", page_num=pn, page_size=10)
        print(f"\n📋 调度日志")
        print(page.display())
        if page.items:
            for item in page.items:
                t = item.get("时间", "")[:16]
                a = item.get("动作", "")
                ok = "✅" if item.get("授权") else "❌"
                print(f"  {t} {ok} {a}")
        else:
            print("  （暂无日志）")

    elif cmd == "refusal":
        pn = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        page = PageHelper.logs("gentle_refusal", page_num=pn, page_size=10)
        print(f"\n🚫 温柔拒绝日志")
        print(page.display())
        if page.items:
            for item in page.items:
                t = item.get("时间", "")[:16]
                cat = item.get("类别", "")
                tp = item.get("拒绝类型", "")
                print(f"  {t} [{cat}] {tp}")

    elif cmd == "files":
        pn = int(sys.argv[2]) if len(sys.argv) > 2 else 1
        page = PageHelper.files(str(SYSTEM_ROOT / "core"), "*.py",
                                page_num=pn, page_size=10)
        print(f"\n📁 core/ Python文件")
        print(page.display())
        for item in page.items:
            print(f"  {item['修改时间']}  {item['大小显示']:>8s}  {item['名称']}")

    elif cmd == "memories":
        kw = sys.argv[2] if len(sys.argv) > 2 else ""
        page = PageHelper.memories(keyword=kw, page_num=1, page_size=10)
        print(f"\n🧠 记忆文件{f' (关键词: {kw})' if kw else ''}")
        print(page.display())
        for item in page.items:
            print(f"  {item['修改']}  {item['大小']:>12s}  {item['文件']}")
            print(f"           {item['摘要'][:60]}")

    else:
        print(f"未知命令: {cmd}")
