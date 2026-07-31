#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂操作日志记录器
==================
每次改动系统后，用本脚本把来源、去向、逻辑、责任写入日志。

用法示例：
    python3 bin/log_operation.py \
        --dna#龍芯⚡️2026-06-18-EXAMPLE-FILE1-v1.0" \
        --source "用户说：我要……" \
        --changes "a.py,b.py" \
        --logic "1. xxx\n2. yyy" \
        --responsibility "方向：用户，执行：Kimi"

DNA:#龍芯⚡️2026-06-18-LONGHUN-OPERATION-LOGGER-v1.0
"""
import os
import sys
import argparse
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_PATH = os.path.join(ROOT, "02_执行记录", "龍魂操作日志.md")


def 读取最新序号():
    """从日志中读取已有操作序号，返回下一个序号。"""
    if not os.path.exists(LOG_PATH):
        return 1
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        import re
        nums = re.findall(r"## \d{4}-\d{2}-\d{2} · 操作 (\d{3})", content)
        if nums:
            return max(int(n) for n in nums) + 1
    except Exception:
        pass
    return 1


def 记录(参数):
    序号 = 读取最新序号()
    时间 = datetime.now().strftime("%Y-%m-%d %H:%M")
    日期 = datetime.now().strftime("%Y-%m-%d")
    改动列表 = "\n".join(f"  - `{c.strip()}`" for c in 参数.changes.split(",") if c.strip())

    条目 = f"""
## {日期} · 操作 {序号:03d}：{参数.title}

- **时间**：{时间}
- **DNA**：{参数.dna}
- **用户意图**：
  > {参数.source}
- **改动文件**：
{改动列表}
- **设计逻辑**：
{参数.logic}
- **责任**：
  - 方向：用户（UID9622 · 龍芯北辰 · 诸葛鑫）
  - 执行：Kimi AI 助手

---
"""
    # 在日志末尾（最后宣誓之前）插入新条目
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        # 找到 "## 日志管理原则" 或文件末尾
        marker = "## 日志管理原则"
        if marker in content:
            idx = content.find(marker)
            new_content = content[:idx] + 条目 + "\n" + content[idx:]
        else:
            new_content = content + 条目
    else:
        header = """# 龍魂系统 · 操作日志

> 本日志记录龍魂系统的每一次改动来源、去向、逻辑与责任。
> 全部公开透明，无黑箱，不免责，可追溯。
> DNA 编号：#龍芯⚡️2026-06-18-LONGHUN-OPERATION-LOG-v1.0

---

## 操作记录格式

每条记录包含：
- **时间**：改动发生的时间
- **DNA**：本次操作的唯一追溯码
- **来源**：为什么做这件事（用户原话/意图）
- **改动**：改了哪些文件/模块
- **逻辑**：为什么这么设计
- **责任**：谁定的方向，谁执行

---

"""
        new_content = header + 条目

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"✅ 已记录操作 {序号:03d} 到 {LOG_PATH}")


def main():
    parser = argparse.ArgumentParser(description="记录龍魂系统操作日志")
    parser.add_argument("--title", required=True, help="操作标题")
    parser.add_argument("--dna", required=True, help="DNA 追溯码")
    parser.add_argument("--source", required=True, help="用户意图/来源")
    parser.add_argument("--changes", required=True, help="改动文件，逗号分隔")
    parser.add_argument("--logic", required=True, help="设计逻辑，支持换行")
    parser.add_argument("--responsibility", default="方向：用户，执行：Kimi", help="责任归属")
    args = parser.parse_args()
    记录(args)


if __name__ == "__main__":
    main()
