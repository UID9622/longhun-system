#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 龍魂·永恒对齐审计器 lh_align v1.0
道生一，一生二，二生三，三生万物。——《道德经》第42章
扫任何仓库/目录，输出三色对齐报告：
  🔴 手写干支DNA（年份干支与算法不符 / 格式非法）
  🔴 旧时间戳DNA格式（#龍芯⚡️YYYY-MM-DD- 或 #ZHUGEXIN⚡️）
  🟡 缺对齐锚文件 LONGHUN_ALIGN.md
  🟡 确认码格式错误
  🟢 全部合规
用法: python3 lh_align.py <目录> [--json]
"""
import os, re, sys, json, datetime

天干 = "甲乙丙丁戊己庚辛壬癸"; 地支 = "子丑寅卯辰巳午未申酉戌亥"
干支表 = [天干[i%10] + 地支[i%12] for i in range(60)]

def 今日干支(date=None):
    d = date or datetime.date.today()
    offset = (d - datetime.date(1900,1,1)).days
    return 干支表[(10 + offset) % 60]

旧格式 = re.compile(r'#龍芯⚡️\d{4}-\d{2}-\d{2}-|#ZHUGEXIN⚡️')
干支DNA = re.compile(r'#龍芯⚡️([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])·([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])·([甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥])·(\S{1,4})卦')
确认码正确 = '#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z'
确认码模糊 = re.compile(r'#CONFIRM\S{0,40}9622\S{0,40}')

def 扫文件(path):
    问题 = []
    try:
        文本 = open(path, encoding='utf-8', errors='ignore').read()
    except Exception:
        return 问题
    for m in 旧格式.finditer(文本):
        问题.append(("🔴", "旧时间戳/旧前缀DNA格式", m.group(0)[:50]))
    for m in 干支DNA.finditer(文本):
        日柱 = m.group(3)
        # 无法确定书写日期，但可检测「年月日干支互斥」等非法组合：此处校验干支字符合法性即可，标注待核
        for g in m.groups()[:3]:
            if g not in 干支表:
                问题.append(("🔴", "非法干支组合(六十甲子之外)", g))
        if 日柱 != 今日干支():
            问题.append(("🟡", f"日柱[{日柱}]≠今日算法值[{今日干支()}]·若非历史存档即手写嫌疑", m.group(0)[:60]))
    for m in 确认码模糊.finditer(文本):
        if m.group(0) != 确认码正确 and 'ONLY-ONCE' in m.group(0):
            问题.append(("🟡", "确认码格式偏离标准", m.group(0)[:50]))
    return 问题

def 审计(目录):
    报告 = {"目录": 目录, "扫描文件": 0, "🔴": 0, "🟡": 0, "🟢文件": 0, "明细": []}
    锚 = os.path.join(目录, "LONGHUN_ALIGN.md")
    if not os.path.exists(锚):
        报告["明细"].append({"文件": "(仓库根)", "级别": "🟡", "问题": "缺对齐锚文件 LONGHUN_ALIGN.md——每个AI窗口开局无锚可读", "证据": ""})
        报告["🟡"] += 1
    for dp, _, fns in os.walk(目录):
        if any(x in dp for x in ('.git', 'node_modules', '__pycache__')): continue
        for fn in fns:
            if not fn.endswith(('.py','.md','.sh','.yaml','.yml','.txt','.js','.ts','.html')): continue
            p = os.path.join(dp, fn)
            报告["扫描文件"] += 1
            问题 = 扫文件(p)
            if not 问题: 报告["🟢文件"] += 1
            for 级别, 描述, 证据 in 问题:
                报告["明细"].append({"文件": os.path.relpath(p, 目录), "级别": 级别, "问题": 描述, "证据": 证据})
                报告[级别] += 1
    报告["三色"] = "🔴" if 报告["🔴"] else ("🟡" if 报告["🟡"] else "🟢")
    return 报告

if __name__ == "__main__":
    目录 = sys.argv[1] if len(sys.argv) > 1 else "."
    r = 审计(目录)
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(f"🐉 对齐审计: {r['目录']} | 扫描 {r['扫描文件']} 文件 | 三色 {r['三色']}")
        print(f"   🔴 {r['🔴']} · 🟡 {r['🟡']} · 🟢文件 {r['🟢文件']}")
        for d in r["明细"][:20]:
            print(f"   {d['级别']} {d['文件']}: {d['问题']} [{d['证据']}]")
    sys.exit(2 if r["🔴"] else (1 if r["🟡"] else 0))
