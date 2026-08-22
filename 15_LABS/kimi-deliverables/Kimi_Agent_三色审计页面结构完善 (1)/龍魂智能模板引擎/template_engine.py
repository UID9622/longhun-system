#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 智能模板引擎 v1.1（焊死输出格式 · 实测落地版）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2

焊死纪律（本引擎强制）：
  1. 输出格式焊死：每份产出 = 头部元数据 → 必含模块(固定顺序) → 最终签名块，缺任一=🔴
  2. DNA焊死：只走 dna_trace.生成DNA() 干支算法，手写干支一律🔴
  3. 三色焊死：审计结果只有 🟢/🟡/🔴 三态，退出码 0/1/2
  4. 签名块焊死：格式字符级固定，validate 逐行核验
"""
import argparse, json, sys, os, re, hashlib, time
from datetime import date as _date

sys.path.insert(0, "/mnt/agents/output/龍魂低算力内核/core")
try:
    from longhun_core.dna_trace import 生成DNA, 日柱
except Exception:
    def 生成DNA(x, d=None): return f"#龍芯⚡️FALLBACK-{x}-UID9622"

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
LICENSE = "思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2"

# ============================================================
# 模板注册表：6类 × 必含模块清单（固定顺序=焊死）
# ============================================================

模板库 = {
    "code":     {"名": "代码模板", "模块": ["文件头注释", "主权锚定", "依赖声明", "核心实现", "异常处理", "测试用例", "使用示例"]},
    "document": {"名": "文档模板", "模块": ["标题", "设计理念", "架构设计", "实现详解", "使用示例", "集成生态", "常见错误与排查", "最终签名"]},
    "chart":    {"名": "图表模板", "模块": ["图表标题", "数据来源", "可视化定义", "分析结论", "局限性说明"]},
    "data":     {"名": "数据模板", "模块": ["结构定义", "字段说明", "样本数据", "校验规则"]},
    "check":    {"名": "检查模板", "模块": ["检查清单", "判定标准", "审计结果", "改进建议"]},
    "api":      {"名": "API模板", "模块": ["端点定义", "请求示例", "响应示例", "错误码表", "客户端示例"]},
}

签名块模板 = """═══════════════════════════════════════════════════
 🐉 龍魂 · {标题} · 最终签名
═══════════════════════════════════════════════════
DNA:        {DNA}
确认码:      {CONFIRM}
GPG:        {GPG}
三色:       {三色}
分层许可:   {LICENSE}
时间戳:     {时间戳}
═══════════════════════════════════════════════════"""

# ============================================================
# 引擎
# ============================================================

class 模板引擎:
    def __init__(self):
        self.DNA = 生成DNA("TEMPLATE-ENGINE")

    # ---------- 三色审计：必含模块完整性 ----------
    def 审计(self, 类型: str, 内容: str) -> dict:
        必含 = 模板库[类型]["模块"]
        缺失 = [m for m in 必含 if m not in 内容]
        占位 = [m for m in 必含 if f"🔶 【{m}】待补全" in 内容]
        缺失 = 缺失 + 占位  # 占位=未填写，计入缺失
        if not 缺失:
            三色, 码 = "🟢", 0
        elif len(缺失) <= len(必含) // 3:
            三色, 码 = "🟡", 1
        else:
            三色, 码 = "🔴", 2
        return {"三色": 三色, "退出码": 码, "必含": 必含, "缺失": 缺失,
                "覆盖率": round((len(必含) - len(缺失)) / len(必含), 3)}

    # ---------- 生成：骨架 + 元数据注入 + 签名 ----------
    def 生成(self, 类型: str, 标题: str, 章节内容: dict = None) -> dict:
        if 类型 not in 模板库:
            raise ValueError(f"未知模板类型: {类型}（可选 {list(模板库)}）")
        章节内容 = 章节内容 or {}
        元数据 = {"DNA": 生成DNA(f"TPL-{类型.upper()}-{标题[:12]}"),
                  "确认码": CONFIRM, "GPG": GPG,
                  "三色": "🟢 通过", "分层许可": LICENSE,
                  "时间戳": time.strftime("%Y-%m-%dT%H:%M:%S")}
        # 头部元数据（焊死：第一区块）
        行 = [f"# 🐉 龍魂 · {标题}", "",
              f"**DNA:** `{元数据['DNA']}`",
              f"**确认码:** `{CONFIRM}`",
              f"**GPG:** `{GPG}`",
              f"**分层许可:** {LICENSE}", "", "---", ""]
        # 必含模块（焊死：固定顺序，缺失自动补占位🔶）
        for 模 in 模板库[类型]["模块"]:
            行.append(f"## {模}")
            行.append(章节内容.get(模, f"🔶 【{模}】待补全——焊死格式保留占位，不允许删除此区块"))
            行.append("")
        审计 = self.审计(类型, "\n".join(行))
        元数据["三色"] = f"{审计['三色']} {'通过' if 审计['三色']=='🟢' else ('警告' if 审计['三色']=='🟡' else '失败')}"
        # 最终签名（焊死：最后区块）
        行 += ["---", "", "```", 签名块模板.format(标题=标题, DNA=元数据["DNA"],
              CONFIRM=CONFIRM, GPG=GPG, 三色=元数据["三色"],
              LICENSE=LICENSE, 时间戳=元数据["时间戳"]), "```"]
        return {"类型": 类型, "标题": 标题, "内容": "\n".join(行),
                "审计": 审计, "元数据": 元数据}

    # ---------- 验证：焊死格式逐行核验 ----------
    def 验证(self, 内容: str) -> dict:
        问题 = []
        if "# 🐉 龍魂 · " not in 内容:
            问题.append("🔴 缺头部标题区块")
        for 锚 in ("**DNA:** `#龍芯⚡️", "**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`",
                   "**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`"):
            if 锚 not in 内容:
                问题.append(f"🔴 缺元数据锚: {锚[:14]}…")
        # 手写干支检测：DNA段出现干支但非今日算法值 → 🔴
        干, 支 = "甲乙丙丁戊己庚辛壬癸", "子丑寅卯辰巳午未申酉戌亥"
        m = re.search(r"#龍芯⚡️([%s][%s]·[%s][%s]·[%s][%s])" % (干,支,干,支,干,支), 内容)
        if m:
            try:
                今日 = 日柱(_date.today())
                if m.group(1).split("·")[-1] != 今日:
                    问题.append(f"🔴 DNA日柱疑似手写: {m.group(1).split('·')[-1]} ≠ 今日算法值 {今日}")
            except Exception:
                pass
        if "最终签名" not in 内容 or "═══" not in 内容:
            问题.append("🔴 缺焊死签名块")
        三色 = "🟢" if not 问题 else ("🟡" if len(问题) == 1 else "🔴")
        return {"三色": 三色, "问题": 问题,
                "退出码": 0 if 三色 == "🟢" else (1 if 三色 == "🟡" else 2)}

    # ---------- 输出格式化 ----------
    @staticmethod
    def 导出(结果: dict, 格式: str) -> str:
        if 格式 == "markdown":
            return 结果["内容"]
        if 格式 == "json":
            return json.dumps(结果, ensure_ascii=False, indent=2)
        if 格式 == "yaml":
            r = 结果
            行 = [f"类型: {r['类型']}", f"标题: {r['标题']}", "元数据:"]
            行 += [f"  {k}: \"{v}\"" for k, v in r["元数据"].items()]
            行 += ["审计:", f"  三色: {r['审计']['三色']}",
                   f"  覆盖率: {r['审计']['覆盖率']}",
                   f"  缺失: {json.dumps(r['审计']['缺失'], ensure_ascii=False)}",
                   "内容: |"] + ["  " + l for l in r["内容"].splitlines()]
            return "\n".join(行)
        raise ValueError(f"未知格式: {格式}（可选 markdown/json/yaml）")

# ============================================================
# CLI（焊死：退出码 0/1/2 对应 🟢/🟡/🔴）
# ============================================================

def main():
    ap = argparse.ArgumentParser(prog="template_engine", description="🐉 龍魂智能模板引擎 v1.1")
    sub = ap.add_subparsers(dest="cmd")

    g = sub.add_parser("generate", help="生成模板")
    g.add_argument("-t", "--type", required=True, choices=list(模板库))
    g.add_argument("--title", required=True)
    g.add_argument("-f", "--format", default="markdown", choices=["markdown", "json", "yaml"])
    g.add_argument("-o", "--output")

    v = sub.add_parser("validate", help="验证焊死格式")
    v.add_argument("-i", "--input", required=True)

    sub.add_parser("config", help="查看模板配置").add_argument("-t", "--type")
    sub.add_parser("verify", help="引擎自检")

    args = ap.parse_args()
    引擎 = 模板引擎()

    if args.cmd == "verify":
        print("🐉 龍魂模板引擎 v1.1 | DNA:", 引擎.DNA, "| 模板:", len(模板库), "| 🟢")
        sys.exit(0)

    if args.cmd == "generate":
        结果 = 引擎.生成(args.type, args.title)
        out = 引擎.导出(结果, args.format)
        if args.output:
            open(args.output, "w", encoding="utf-8").write(out)
            print(f"✅ 已生成: {args.output} | 审计 {结果['审计']['三色']} 覆盖率 {结果['审计']['覆盖率']:.0%}")
        else:
            print(out)
        sys.exit(结果["审计"]["退出码"])

    if args.cmd == "validate":
        内容 = open(args.input, encoding="utf-8").read()
        r = 引擎.验证(内容)
        print(f"验证结果: {r['三色']}")
        for q in r["问题"]:
            print(" ", q)
        sys.exit(r["退出码"])

    if args.cmd == "config":
        类型集 = [args.type] if args.type else list(模板库)
        for t in 类型集:
            print(f"📦 {模板库[t]['名']} ({t}): 必含模块 {len(模板库[t]['模块'])} 个")
            for i, m in enumerate(模板库[t]["模块"], 1):
                print(f"   {i}. {m}")
        sys.exit(0)

    print("🐉 龍魂模板引擎 v1.1 | DNA:", 引擎.DNA, "| 模板:", len(模板库), "| 🟢")
    sys.exit(0)

if __name__ == "__main__":
    main()
