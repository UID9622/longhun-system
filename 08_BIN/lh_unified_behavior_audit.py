#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# DNA: #龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-UNIFIED-BEHAVIOR-AUDIT-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: 工程实现层 MulanPSL v2 · 核心思想层 CC BY-NC-SA 4.0
"""
龍魂·统一行为审计引擎 v1.0 — 五合一综合判定

五合一：
  1. 道德经锚   — 第0问·行为锚·fail-closed·无道词必拒（命中数==0 → 🔴 一票）
  2. 行为七因子 — 行为密码学·composite_score + 因子状态
  3. DNA追溯    — 本次审计 DNA 生成（干支+内容哈希）
  4. 天干地支   — 干支四柱时间戳（含ISO可排序）
  5. CNSH语义   — 一票否决词 + 诱导词检测；CNSH代码走语法编译校验

定位: P05 上帝之眼 · 行为/产出综合审计 · fail-closed
联动: P06交叉验证 · P72熔断 · P15签章 · P03归档

用法:
  python3 08_BIN/lh_unified_behavior_audit.py audit "内容" [--author UID9622] [--type text|cnsh] [--json] [--report]
  python3 08_BIN/lh_unified_behavior_audit.py selftest
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys

# ── 路径锚点 ──
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_BIN_DIR = os.path.join(_PROJECT_ROOT, "bin")
_BEHAVIOR_DIR = os.path.join(_PROJECT_ROOT, "04_ENGINES", "behavioral_crypto")
_COMPILER_DIR = os.path.join(_PROJECT_ROOT, "03_compiler")
for _p in (_BIN_DIR, _BEHAVIOR_DIR, _COMPILER_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

# ── 道德经锚（第0问） ──
try:
    from lh_daodejing_anchor import CNSH_道德经定锚器
    _HAS_DAO = True
except Exception:
    _HAS_DAO = False

# ── 干支时间戳 ──
try:
    from lh_time_engine import get_output_stamp
    _HAS_TIME = True
except Exception:
    _HAS_TIME = False

# ── 行为七因子 ──
try:
    from seven_factor_model import quick_fingerprint as _提取行为指纹
    _HAS_BEHAVIOR = True
except Exception:
    _HAS_BEHAVIOR = False

# ── CNSH 编译器（代码类型·词法+语法校验） ──
try:
    from cnsh_compiler import Lexer as _CNSHLexer, Parser as _CNSHParser
    _HAS_CNSH = True
except Exception:
    _HAS_CNSH = False


def _干支时间戳() -> str:
    """干支四柱完整时间戳（内含ISO·可排序）·引擎缺失降级ISO"""
    try:
        if _HAS_TIME:
            return get_output_stamp()
    except Exception:
        pass
    return datetime.datetime.now().isoformat()


def _干支紧凑() -> str:
    """从完整戳提取 干支·卦 紧凑段（如 丙午·丙申·丁卯·戌时·䷗复）"""
    m = re.search(r"\[([^\]]+)\]", _干支时间戳())
    return m.group(1) if m else "干支不可用"


def _生成DNA(内容: str) -> str:
    """审计 DNA：干支 + 内容哈希8位"""
    _h = hashlib.sha256((内容 or "").encode("utf-8")).hexdigest()[:8]
    return f"#龍芯⚡️{_干支紧凑()}-UNIFIED-BEHAVIOR-AUDIT-{_h}"


# ── 第十层·一票否决词（出现即P05强制审计·AI输出严禁使用） ──
一票否决词 = [
    "技术无国界", "用户体验优先", "灵活处理", "国际接轨",
    "简化管理", "商业化需要", "平衡各方", "行业标准",
]

# ── 隐私接入协议 v2.0 诱导词（诱导指数I≤1） ──
诱导词 = [
    "默认勾选", "强制授权", "一键授权", "跳过验证", "忽略隐私", "自动分享",
]


# ═══════════════════════════════════════════════════════════
# 五层判定
# ═══════════════════════════════════════════════════════════
def _层道德经锚(内容: str) -> dict:
    """第0问·道德经锚：无道词必拒（命中数==0 → 🔴 一票）"""
    if not _HAS_DAO:
        return {"状态": "🔴", "理由": "道德经锚引擎未加载·fail-closed", "命中数": None, "无道词": True}
    try:
        _锚 = CNSH_道德经定锚器().定锚((内容 or "审计场景")[:500])
        if "error" in _锚:
            return {"状态": "🔴", "理由": f"定锚异常·无锚不输出: {_锚['error'][:80]}",
                    "命中数": None, "无道词": True}
        _命中数 = _锚.get("命中数", 0)
        if _命中数 == 0:
            return {"状态": "🔴", "理由": "无道词内容·道德经无章可锚·必拒（兜底章不算锚）",
                    "章": _锚.get("章"), "锚句": _锚.get("锚句"), "命中数": 0, "无道词": True}
        return {"状态": "🟢", "理由": f"第{_锚['章']}章锚定·{_锚['锚句']}",
                "章": _锚.get("章"), "锚句": _锚.get("锚句"),
                "五行": _锚.get("五行"), "三六九": _锚.get("三六九"),
                "命中数": _命中数, "无道词": False}
    except Exception as e:
        return {"状态": "🔴", "理由": f"定锚异常: {str(e)[:80]}", "命中数": None, "无道词": True}


def _层行为七因子(内容: str, 作者: str) -> dict:
    """行为密码学·七因子指纹"""
    if not _HAS_BEHAVIOR:
        return {"状态": "🟡", "理由": "七因子引擎未加载·跳过", "composite_score": None}
    try:
        _fp = _提取行为指纹((内容 or "")[:2000], 作者 or "UID9622")
        _score = _fp.get("composite_score") or 0
        _factors = _fp.get("factors") or []
        _红 = sum(1 for f in _factors if f.get("status") == "🔴")
        _黄 = sum(1 for f in _factors if f.get("status") == "🟡")
        状态 = "🔴" if _红 > 2 else ("🟡" if (_红 > 0 or _黄 > 3) else "🟢")
        return {
            "状态": 状态,
            "理由": f"composite={_score:.3f}·红{_红}·黄{_黄}",
            "composite_score": _score,
            "红因子": _红, "黄因子": _黄,
            "factors": [
                {"id": f.get("id"), "name": f.get("name"),
                 "score": f.get("score"), "status": f.get("status")}
                for f in _factors
            ],
            "sovereignty": _fp.get("sovereignty"),
        }
    except Exception as e:
        return {"状态": "🟡", "理由": f"七因子提取异常: {str(e)[:80]}", "composite_score": None}


def _层DNA(内容: str) -> dict:
    """DNA追溯：生成本次审计DNA + 内容指纹"""
    _h = hashlib.sha256((内容 or "").encode("utf-8")).hexdigest()
    return {
        "状态": "🟢",
        "理由": "DNA已生成·内容指纹SHA-256",
        "dna": _生成DNA(内容),
        "内容哈希": _h[:16],
        "完整哈希": _h,
    }


def _层天干地支() -> dict:
    """干支四柱时间戳"""
    _stamp = _干支时间戳()
    m = re.search(r"\[([^\]]+)\]", _stamp)
    _段 = m.group(1) if m else ""
    return {
        "状态": "🟢",
        "理由": "干支四柱+64卦·含ISO可排序",
        "干支卦": _段,
        "时间戳": _stamp,
    }


def _层CNSH(内容: str, 类型: str) -> dict:
    """CNSH语义层：一票否决词/诱导词检测 + 代码语法校验"""
    _命中否决 = [w for w in 一票否决词 if w in (内容 or "")]
    _命中诱导 = [w for w in 诱导词 if w in (内容 or "")]
    _详情 = {"一票否决词": _命中否决, "诱导词": _命中诱导}
    状态 = "🔴" if _命中否决 else ("🟡" if _命中诱导 else "🟢")
    理由 = ("命中一票否决词: " + "、".join(_命中否决)) if _命中否决 else (
        "命中诱导词: " + "、".join(_命中诱导)) if _命中诱导 else "语义净·无否决无诱导"

    # CNSH 代码类型 → 语法编译校验
    if 类型 == "cnsh" and _HAS_CNSH and (内容 or "").strip():
        try:
            _tokens = _CNSHLexer(内容).tokenize()
            _CNSHParser(_tokens).parse()
            _详情["语法校验"] = "🟢 词法+语法通过"
        except Exception as e:
            状态 = "🔴"
            理由 = f"CNSH语法错误: {str(e)[:120]}"
            _详情["语法校验"] = f"🔴 {str(e)[:120]}"
    elif 类型 == "cnsh" and not _HAS_CNSH:
        _详情["语法校验"] = "🟡 编译器不可用·人工核查"

    return {"状态": 状态, "理由": 理由, "详情": _详情}


# ═══════════════════════════════════════════════════════════
# 综合判定
# ═══════════════════════════════════════════════════════════
def _综合判定(五合一: dict, 作者: str) -> dict:
    """加权风险 + 三色 + 熔断建议"""
    _层状态 = {k: v["状态"] for k, v in 五合一.items()}
    # 一票项：道德经锚🔴 / CNSH否决🔴
    _一票 = [k for k in ("道德经锚", "CNSH语义") if _层状态.get(k) == "🔴"]
    _红数 = sum(1 for v in _层状态.values() if v == "🔴")
    _黄数 = sum(1 for v in _层状态.values() if v == "🟡")

    风险分 = 1.0 if _一票 else min(1.0, 0.34 + _红数 * 0.22 + _黄数 * 0.12)
    三色 = "🔴" if (_一票 or _红数 >= 2) else ("🟡" if (_黄数 or _红数) else "🟢")
    熔断 = "L0-一票熔断" if _一票 else ("L1-数据熔断" if _红数 >= 2 else ("L3-行为熔断" if 三色 == "🔴" else ("L3-待核" if 三色 == "🟡" else "无")))

    if 三色 == "🟢":
        建议 = "放行·归档·可进入下一链路"
    elif 三色 == "🟡":
        建议 = "待核·标记留痕·48h内复查·人工复核" + ("·否决词待P05复核" if _层状态.get("CNSH语义") == "🔴" else "")
    else:
        建议 = "拒绝·冻结·DNA追溯" + ("·" + "、".join(_一票) + "一票否决" if _一票 else "")

    return {
        "三色": 三色,
        "风险分": round(风险分, 3),
        "红层": _红数, "黄层": _黄数,
        "一票层": _一票,
        "熔断建议": 熔断,
        "建议": 建议,
        "审计者": 作者 or "UID9622",
        "判定规则": "一票项=道德经锚/CNSH否决·红≥2=L1·红黄加权",
    }


# ═══════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════
class 统一行为审计引擎:
    """五合一统一行为审计·fail-closed"""

    VERSION = "v1.0"
    DNA = "#龍芯⚡️丙午·丙申·丁卯·丙午·䷚颐-UNIFIED-BEHAVIOR-AUDIT-v1.0"

    def 审计(self, 内容: str, 作者: str = "UID9622", 类型: str = "text") -> dict:
        报告ID = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_") + hashlib.sha256((内容 or "").encode()).hexdigest()[:6]
        五合一 = {
            "道德经锚": _层道德经锚(内容),
            "行为七因子": _层行为七因子(内容, 作者),
            "DNA追溯": _层DNA(内容),
            "天干地支": _层天干地支(),
            "CNSH语义": _层CNSH(内容, 类型),
        }
        综合 = _综合判定(五合一, 作者)
        return {
            "报告ID": 报告ID,
            "引擎": f"统一行为审计引擎 {self.VERSION}",
            "DNA": 五合一["DNA追溯"]["dna"],
            "时间戳": 五合一["天干地支"]["时间戳"],
            "审计对象": {"作者": 作者, "类型": 类型, "摘要": (内容 or "")[:80]},
            "五合一": 五合一,
            "综合判定": 综合,
            "审计链": {
                "signer": "P05上帝之眼",
                "audit_mark": 综合["三色"],
                "report_id": 报告ID,
            },
        }

    def 存报告(self, 报告: dict, 目录: str = None) -> str:
        """落盘 JSON 报告 → 04_AUDIT/unified_behavior/YYYYMMDD/"""
        根 = 目录 or os.path.join(_PROJECT_ROOT, "04_AUDIT", "unified_behavior")
        日 = os.path.join(根, 报告["报告ID"][:8])
        os.makedirs(日, exist_ok=True)
        路径 = os.path.join(日, f"report_{报告['报告ID']}.json")
        with open(路径, "w", encoding="utf-8") as f:
            json.dump(报告, f, ensure_ascii=False, indent=2)
        return 路径


# ═══════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════
def _打印报告(报告: dict, 全量: bool = False):
    _c = 报告["综合判定"]
    print("🐉 龍魂·统一行为审计引擎 " + 报告["引擎"].split()[-1])
    print("DNA: " + 报告["DNA"])
    print("时间戳: " + 报告["时间戳"])
    print("=" * 52)
    for _层名, _层 in 报告["五合一"].items():
        print(f"  {_层名:6s} {_层['状态']}  {_层['理由'][:60]}")
    print("=" * 52)
    print(f"综合判定: {_c['三色']}  风险分: {_c['风险分']}  熔断: {_c['熔断建议']}")
    print("建议: " + _c["建议"])
    if 全量:
        print("\n" + json.dumps(报告, ensure_ascii=False, indent=2))


def _selftest():
    """自检：五合一能力 + 道词/无道词双样本"""
    print("=== 能力加载 ===")
    print(f"道德经锚: {_HAS_DAO} | 行为七因子: {_HAS_BEHAVIOR} | 干支时间: {_HAS_TIME} | CNSH语义: {_HAS_CNSH}")
    print(f"干支戳: {_干支时间戳()[:55]}")
    引擎 = 统一行为审计引擎()
    print("\n=== 样本1·有道词（应🟢/🟡） ===")
    r1 = 引擎.审计("上善若水，利万物而不争，处众人之所恶，故几于道", "UID9622", "text")
    _打印报告(r1)
    print("\n=== 样本2·无道词（应🔴·一票） ===")
    r2 = 引擎.审计("test123 random payload 随便来的东西", "UID9622", "text")
    _打印报告(r2)
    print("\n=== 样本3·一票否决词（应🔴） ===")
    r3 = 引擎.审计("我们基于行业标准做灵活处理，平衡各方利益", "UID9622", "text")
    _打印报告(r3)


def main():
    _p = argparse.ArgumentParser(description="龍魂·统一行为审计引擎 v1.0")
    _p.add_argument("子命令", choices=["audit", "selftest"], nargs="?", default="selftest")
    _p.add_argument("内容", nargs="?", default="")
    _p.add_argument("--author", default="UID9622")
    _p.add_argument("--type", default="text", choices=["text", "cnsh"])
    _p.add_argument("--json", action="store_true", help="输出完整JSON")
    _p.add_argument("--report", action="store_true", help="落盘报告到 04_AUDIT/unified_behavior/")
    _a = _p.parse_args()

    if _a.子命令 == "selftest":
        _selftest()
        return
    if not _a.内容.strip():
        _p.error("audit 需要传入内容: audit \"要审计的内容\"")
    引擎 = 统一行为审计引擎()
    报告 = 引擎.审计(_a.内容, _a.author, _a.type)
    _打印报告(报告, _a.json)
    if _a.report:
        路径 = 引擎.存报告(报告)
        print(f"\n📦 报告已落盘: {路径}")


if __name__ == "__main__":
    main()
