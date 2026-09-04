#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
龍魂·统一视觉色彩引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·庚戌·壬午·䷫姤-UNIFIED-VISUAL-ENGINE-v1.0
融合: 三色审计·五色治理·七色不动点·真实协议·五彩石·跑马灯 → 8色统一色阶

一看颜色就知道优先级:
  P0🔴断空红 > P1⚫深渊黑 > P2🟣观察紫 > P3🟡主权金
  > P4🔵追踪蓝 > P5🟡待核黄 > P6⚪过渡银 > P7🟢放行绿

用法:
  python3 bin/lh_unified_visual.py judge "文本内容"     # 单条判定
  python3 bin/lh_unified_visual.py batch file.txt       # 批量判定
  python3 bin/lh_unified_visual.py dashboard            # 输出仪表盘JSON
  python3 bin/lh_unified_visual.py test                 # 跑测试
"""

import json, sys, os, re
from datetime import datetime
from enum import IntEnum
from typing import Optional, Dict, List, Any, Tuple

# ═══════════════════════════════════════════
# P1 · 统一色阶枚举（优先级焊死）
# ═══════════════════════════════════════════

class VisualLevel(IntEnum):
    """统一视觉色阶·数字越小越紧急"""
    P0_RED    = 0   # 🔴 断空红 — 熔断·红线·立即停
    P1_BLACK  = 1   # ⚫ 深渊黑 — 隔离·机密·永久禁
    P2_PURPLE = 2   # 🟣 观察紫 — 外部·未审·观察池
    P3_GOLD   = 3   # 🟡 主权金 — 主控·实证·已授权
    P4_BLUE   = 4   # 🔵 追踪蓝 — 系统·审计·运维
    P5_YELLOW = 5   # 🟡 待核黄 — 待查·警告·需复查
    P6_SILVER = 6   # ⚪ 过渡银 — 演绎·AI生成·扫描中
    P7_GREEN  = 7   # 🟢 放行绿 — 通过·安全·一切正常

# ═══════════════════════════════════════════
# 色阶元数据表
# ═══════════════════════════════════════════

LEVEL_META: Dict[VisualLevel, Dict] = {
    VisualLevel.P0_RED: {
        "name": "断空红", "emoji": "🔴", "css_class": "uv-p0",
        "hex": "#e5484d", "hex_bg": "#2d0a0c", "hex_border": "#8b2024",
        "animation": "pulse-red 1.2s", "action": "立即停止·上报·不自动恢复",
        "from_systems": "三色审计🔴·五色治理🔴·七色不动点🔴·真实协议疑"
    },
    VisualLevel.P1_BLACK: {
        "name": "深渊黑", "emoji": "⚫", "css_class": "uv-p1",
        "hex": "#1a1a20", "hex_bg": "#000000", "hex_border": "#3a3a44",
        "animation": "static", "action": "物理隔离·人工解封",
        "from_systems": "五色治理⚫·七色不动点⚫·五彩石⚫"
    },
    VisualLevel.P2_PURPLE: {
        "name": "观察紫", "emoji": "🟣", "css_class": "uv-p2",
        "hex": "#9b59b6", "hex_bg": "#1a1020", "hex_border": "#6c3483",
        "animation": "marquee 2s", "action": "沙箱运行·标记追踪",
        "from_systems": "七色不动点🟣"
    },
    VisualLevel.P3_GOLD: {
        "name": "主权金", "emoji": "🟡", "css_class": "uv-p3",
        "hex": "#d4af37", "hex_bg": "#141310", "hex_border": "#8a742a",
        "animation": "glow 2s", "action": "正常执行·可发布",
        "from_systems": "五色治理金AU·七色不动点金·真实协议实·五彩石黄"
    },
    VisualLevel.P4_BLUE: {
        "name": "追踪蓝", "emoji": "🔵", "css_class": "uv-p4",
        "hex": "#3498db", "hex_bg": "#0d1b2a", "hex_border": "#1a5276",
        "animation": "pulse-dot 2s", "action": "记录·追踪",
        "from_systems": "七色不动点🔵·五彩石青"
    },
    VisualLevel.P5_YELLOW: {
        "name": "待核黄", "emoji": "🟡", "css_class": "uv-p5",
        "hex": "#f1c40f", "hex_bg": "#1a1808", "hex_border": "#8a7e0a",
        "animation": "blink 2.5s", "action": "48h内复查·人工确认",
        "from_systems": "三色审计🟡·五色治理Y·七色不动点🟡"
    },
    VisualLevel.P6_SILVER: {
        "name": "过渡银", "emoji": "⚪", "css_class": "uv-p6",
        "hex": "#9aa0a6", "hex_bg": "#121216", "hex_border": "#5c6066",
        "animation": "dashed-static", "action": "标注·不阻塞",
        "from_systems": "七色不动点银·真实协议演·五彩石白"
    },
    VisualLevel.P7_GREEN: {
        "name": "放行绿", "emoji": "🟢", "css_class": "uv-p7",
        "hex": "#27ae60", "hex_bg": "#0a1a10", "hex_border": "#1a6e3a",
        "animation": "static", "action": "正常·静默",
        "from_systems": "三色审计🟢·五色治理G·七色不动点🟢"
    },
}

# ═══════════════════════════════════════════
# P0 焊死关键词（触发即红）
# ═══════════════════════════════════════════

P0_RED_TRIGGERS = [
    # 涉童
    r'儿童.*色情', r'未成年.*性', r'child.*porn',
    # 伪造DNA
    r'伪造.*DNA', r'fake.*dna', r'假冒.*龍魂',
    # 背叛人民
    r'背叛.*人民', r'卖.*用户数据', r'收割.*老百姓',
    # 海外部署内核
    r'海外.*部署.*内核', r'export.*kernel.*overseas',
    # P77对外渗透
    r'对外.*渗透.*测试', r'attack.*external.*system',
    # 一票否决词
    r'技术无国界', r'简化管理.*安全', r'灵活处理.*协议',
    r'国际接轨.*标准', r'商业化.*用户数据',
    # 删除/绕过指令
    r'绕过.*审计', r'跳过.*签名', r'删.*日志', r'去.*水印',
]

P1_BLACK_TRIGGERS = [
    r'D1.*数据', r'GPG.*私钥', r'DNA.*种子', r'quantum_key',
    r'绝密.*泄露', r'永不.*对外', r'物理.*隔离',
]

# ═══════════════════════════════════════════
# 核心判定引擎
# ═══════════════════════════════════════════

class VisualSignature:
    """统一视觉签名"""
    def __init__(self, level: VisualLevel, text: str = "",
                 reason: str = "", sources: List[str] = None,
                 dna: str = ""):
        self.level = level
        self.text = text
        self.reason = reason
        self.sources = sources or []
        self.dna = dna or _gen_dna()
        self.timestamp = datetime.now().isoformat()
        self.meta = LEVEL_META[level]

    def to_dict(self) -> Dict:
        return {
            "level": self.level.value,
            "level_name": self.meta["name"],
            "emoji": self.meta["emoji"],
            "hex": self.meta["hex"],
            "animation": self.meta["animation"],
            "text": self.text,
            "reason": self.reason,
            "sources": self.sources,
            "dna": self.dna,
            "timestamp": self.timestamp,
        }

    def to_html_band(self) -> str:
        """输出色带HTML"""
        cls = self.meta["css_class"]
        return f'<div class="uv-band uv-band-{cls}" title="{self.meta["name"]}: {self.reason}"></div>'

    def to_html_badge(self) -> str:
        """输出标签HTML"""
        cls = self.meta["css_class"]
        return f'<span class="uv-badge uv-badge-{cls}">{self.meta["emoji"]} {self.meta["name"]}</span>'

    def to_html_card(self, content: str = "") -> str:
        """输出完整卡片HTML"""
        cls = self.meta["css_class"]
        return f'''<div class="uv-card uv-card-{cls}">
  <div class="uv-band uv-band-{cls}"></div>
  {self.to_html_badge()}
  <div style="margin-top:8px">{content or self.text}</div>
  <div style="font-size:10px;color:#a09a8a;margin-top:6px">{self.reason} · {self.dna[:16]}</div>
</div>'''

    def __repr__(self):
        return f"{self.meta['emoji']} [{self.meta['name']}] {self.reason}"


def _gen_dna() -> str:
    from hashlib import sha256
    return "#龍芯⚡️" + sha256(str(datetime.now().timestamp()).encode()).hexdigest()[:8]


def color_priority(a: VisualLevel, b: VisualLevel) -> VisualLevel:
    """取更紧急的颜色（数字小=紧急）"""
    return a if a.value <= b.value else b


def _scan_red_triggers(text: str) -> List[str]:
    """扫描P0红线触发词"""
    hits = []
    for pattern in P0_RED_TRIGGERS:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(pattern)
    return hits


def _scan_black_triggers(text: str) -> List[str]:
    """扫描P1黑线触发词"""
    hits = []
    for pattern in P1_BLACK_TRIGGERS:
        if re.search(pattern, text, re.IGNORECASE):
            hits.append(pattern)
    return hits


def judge_text(text: str, context: Dict = None) -> VisualSignature:
    """
    对文本内容进行统一视觉判定
    返回 VisualSignature
    """
    context = context or {}
    reasons = []

    # 1. P0 红线扫描（最高优先级）
    red_hits = _scan_red_triggers(text)
    if red_hits:
        return VisualSignature(
            VisualLevel.P0_RED, text,
            reason=f"触发P0红线: {', '.join(red_hits[:3])}",
        )

    # 2. P1 黑线扫描
    black_hits = _scan_black_triggers(text)
    if black_hits:
        return VisualSignature(
            VisualLevel.P1_BLACK, text,
            reason=f"触发D1/P1: {', '.join(black_hits[:3])}",
        )

    # 3. 来源判定
    source = context.get("source", "")
    is_external = context.get("is_external", False)
    is_verified = context.get("is_verified", False)
    is_ai_generated = context.get("is_ai_generated", False)
    is_deduced = context.get("is_deduced", False)
    audit_mark = context.get("audit_mark", "")  # 🟢🟡🔴
    # 默认信任分=0.5(未知)，显式设置才给高分
    trust_score = context.get("trust_score", 0.5)
    # 检测context是否显式设置了信任分（未设置=未知=默认观察）
    trust_explicit = "trust_score" in context

    # 4. 审计三色 → 统一色映射
    if audit_mark == "🔴":
        return VisualSignature(VisualLevel.P0_RED, text, reason="审计🔴红线")
    elif audit_mark == "🟡":
        reasons.append("审计🟡待核")

    # 5. 真实性判定
    if is_ai_generated or is_deduced:
        reasons.append("AI生成/推演内容")
    if source and is_verified:
        reasons.append(f"已验证来源: {source}")
    elif source and not is_verified:
        reasons.append(f"来源未验证: {source}")

    # 6. 外部输入判定
    if is_external and not is_verified:
        reasons.append("外部未验证输入")

    # 7. 信任分判定
    if trust_explicit and trust_score < 0.3:
        reasons.append(f"信任分过低({trust_score:.2f})")

    # 8. 统合判定（按优先级）
    # 审计黄
    if audit_mark == "🟡":
        return VisualSignature(VisualLevel.P5_YELLOW, text,
                               reason="; ".join(reasons) if reasons else "审计待核")
    # 已确认真实来源
    elif source and is_verified:
        return VisualSignature(VisualLevel.P3_GOLD, text,
                               reason="; ".join(reasons))
    # 外部未验证
    elif is_external and not is_verified:
        return VisualSignature(VisualLevel.P2_PURPLE, text,
                               reason="; ".join(reasons))
    # AI生成/推演
    elif is_ai_generated or is_deduced:
        return VisualSignature(VisualLevel.P6_SILVER, text,
                               reason="; ".join(reasons))
    # 来源未验证（有来源但不确认）
    elif source and not is_verified:
        return VisualSignature(VisualLevel.P2_PURPLE, text,
                               reason=f"来源未验证: {source}")
    # 信任分高且明确设置
    elif trust_explicit and trust_score >= 0.9:
        return VisualSignature(VisualLevel.P7_GREEN, text,
                               reason="信任分高·无告警")
    # 默认：未明确判定的入观察池
    else:
        return VisualSignature(VisualLevel.P2_PURPLE, text,
                               reason="默认·待观察·入观察池")


def judge_audit_result(audit: Dict) -> VisualSignature:
    """
    从三色审计结果 → 统一视觉色
    输入: {"mark": "🟢/🟡/🔴", "score": 0.85, "gates": [...], "reason": "..."}
    """
    mark = audit.get("mark", "")
    score = audit.get("score", 1.0)
    reason = audit.get("reason", "")

    if mark == "🔴":
        return VisualSignature(VisualLevel.P0_RED, reason=reason or "审计红线")
    elif mark == "🟡":
        return VisualSignature(VisualLevel.P5_YELLOW, reason=reason or "审计待核")
    elif score >= 0.9:
        return VisualSignature(VisualLevel.P7_GREEN, reason="审计全绿·高分")
    elif score >= 0.7:
        return VisualSignature(VisualLevel.P3_GOLD, reason="审计通过·中等分")
    else:
        return VisualSignature(VisualLevel.P5_YELLOW, reason=f"审计分偏低({score:.2f})")


def judge_multi(items: List[Dict]) -> List[VisualSignature]:
    """批量判定，每个 item = {"text": str, **context}"""
    results = []
    for item in items:
        text = item.pop("text", "")
        sig = judge_text(text, item)
        results.append(sig)
    return results


def highest_level(signatures: List[VisualSignature]) -> VisualSignature:
    """取多重判定中最高优先级色"""
    if not signatures:
        return VisualSignature(VisualLevel.P7_GREEN, reason="无输入·默认绿")
    return min(signatures, key=lambda s: s.level.value)


def render_dashboard(items: List[Dict]) -> Dict:
    """生成仪表盘JSON"""
    sigs = judge_multi(items)
    top = highest_level(sigs)
    return {
        "dashboard_level": top.to_dict(),
        "items": [s.to_dict() for s in sigs],
        "summary": {
            "total": len(sigs),
            "p0_red": sum(1 for s in sigs if s.level == VisualLevel.P0_RED),
            "p1_black": sum(1 for s in sigs if s.level == VisualLevel.P1_BLACK),
            "p2_purple": sum(1 for s in sigs if s.level == VisualLevel.P2_PURPLE),
            "p3_gold": sum(1 for s in sigs if s.level == VisualLevel.P3_GOLD),
            "p5_yellow": sum(1 for s in sigs if s.level == VisualLevel.P5_YELLOW),
            "p6_silver": sum(1 for s in sigs if s.level == VisualLevel.P6_SILVER),
            "p7_green": sum(1 for s in sigs if s.level == VisualLevel.P7_GREEN),
        },
        "dna": _gen_dna(),
        "timestamp": datetime.now().isoformat(),
    }


# ═══════════════════════════════════════════
# HTML生成器（前端可直接用）
# ═══════════════════════════════════════════

def render_full_html(results: List[VisualSignature], title: str = "龍魂·统一视觉判定") -> str:
    """生成完整HTML页面"""
    summary = {lv: 0 for lv in VisualLevel}
    for r in results:
        summary[r.level] += 1

    items_html = ""
    for r in results:
        cls = r.meta["css_class"]
        items_html += f'''
    <div class="uv-card uv-card-{cls}">
      <div class="uv-band uv-band-{cls}"></div>
      <span class="uv-badge uv-badge-{cls}">{r.meta["emoji"]} {r.meta["name"]}</span>
      <span style="margin-left:8px">{r.text[:120]}</span>
      <div class="uv-meta">{r.reason} · {r.dna}</div>
    </div>'''

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
{generate_css()}
</style>
</head>
<body>
<header>
  <h1>🐉 龍魂 · 统一视觉色彩引擎</h1>
  <div class="dna">DNA: #龍芯⚡️丙午·乙未·庚戌·天风姤-UNIFIED-VISUAL-v1.0</div>
</header>
<main>
  <div class="uv-summary">
    <span class="uv-stat red">🔴 {summary[VisualLevel.P0_RED]}</span>
    <span class="uv-stat black">⚫ {summary[VisualLevel.P1_BLACK]}</span>
    <span class="uv-stat purple">🟣 {summary[VisualLevel.P2_PURPLE]}</span>
    <span class="uv-stat gold">🟡 {summary[VisualLevel.P3_GOLD]}</span>
    <span class="uv-stat blue">🔵 {summary[VisualLevel.P4_BLUE]}</span>
    <span class="uv-stat yellow">🟡 {summary[VisualLevel.P5_YELLOW]}</span>
    <span class="uv-stat silver">⚪ {summary[VisualLevel.P6_SILVER]}</span>
    <span class="uv-stat green">🟢 {summary[VisualLevel.P7_GREEN]}</span>
  </div>
  {items_html}
</main>
</body>
</html>'''


def generate_css() -> str:
    """生成完整CSS"""
    return '''
:root {
  --uv-p0:#e5484d;--uv-p0-bg:#2d0a0c;--uv-p0-border:#8b2024;--uv-p0-glow:0 0 12px rgba(229,72,77,.7);
  --uv-p1:#1a1a20;--uv-p1-bg:#000000;--uv-p1-border:#3a3a44;
  --uv-p2:#9b59b6;--uv-p2-bg:#1a1020;--uv-p2-border:#6c3483;
  --uv-p3:#d4af37;--uv-p3-bg:#141310;--uv-p3-border:#8a742a;--uv-p3-glow:0 0 14px rgba(212,175,55,.6);
  --uv-p4:#3498db;--uv-p4-bg:#0d1b2a;--uv-p4-border:#1a5276;
  --uv-p5:#f1c40f;--uv-p5-bg:#1a1808;--uv-p5-border:#8a7e0a;
  --uv-p6:#9aa0a6;--uv-p6-bg:#121216;--uv-p6-border:#5c6066;
  --uv-p7:#27ae60;--uv-p7-bg:#0a1a10;--uv-p7-border:#1a6e3a;
}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:#0a0a0c;color:#e8e4d8;font-family:"PingFang SC","Microsoft YaHei",sans-serif;}
header{border-bottom:1px solid #8a742a;padding:16px 24px;background:linear-gradient(180deg,#141310,#0a0a0c);}
h1{font-size:20px;color:#d4af37;letter-spacing:3px;}
.dna{font-size:11px;color:#8a742a;font-family:monospace;margin-top:4px;}
main{max-width:900px;margin:0 auto;padding:20px;}
.uv-summary{display:flex;gap:10px;flex-wrap:wrap;margin-bottom:18px;}
.uv-stat{font-size:13px;padding:4px 10px;border-radius:4px;font-weight:bold;}
.uv-stat.red{background:var(--uv-p0-bg);color:var(--uv-p0);border:1px solid var(--uv-p0-border);}
.uv-stat.black{background:var(--uv-p1-bg);color:#8888a0;border:1px solid var(--uv-p1-border);}
.uv-stat.purple{background:var(--uv-p2-bg);color:var(--uv-p2);border:1px dashed var(--uv-p2);}
.uv-stat.gold{background:var(--uv-p3-bg);color:var(--uv-p3);border:1px solid var(--uv-p3-border);box-shadow:var(--uv-p3-glow);}
.uv-stat.blue{background:var(--uv-p4-bg);color:var(--uv-p4);border:1px solid var(--uv-p4-border);}
.uv-stat.yellow{background:var(--uv-p5-bg);color:var(--uv-p5);border:1px solid var(--uv-p5-border);animation:uv-blink-yellow 2.5s infinite;}
.uv-stat.silver{background:var(--uv-p6-bg);color:var(--uv-p6);border:1px dashed var(--uv-p6-border);}
.uv-stat.green{background:var(--uv-p7-bg);color:var(--uv-p7);border:1px solid var(--uv-p7-border);}
.uv-card{border-radius:8px;padding:14px;margin:8px 0;position:relative;}
.uv-card-p0{background:var(--uv-p0-bg);border:1px solid var(--uv-p0-border);}
.uv-card-p1{background:var(--uv-p1-bg);border:1px solid var(--uv-p1-border);}
.uv-card-p2{background:var(--uv-p2-bg);border:1px dashed var(--uv-p2-border);}
.uv-card-p3{background:var(--uv-p3-bg);border:1px solid var(--uv-p3-border);}
.uv-card-p4{background:var(--uv-p4-bg);border:1px solid var(--uv-p4-border);}
.uv-card-p5{background:var(--uv-p5-bg);border:1px solid var(--uv-p5-border);}
.uv-card-p6{background:var(--uv-p6-bg);border:1px dashed var(--uv-p6-border);}
.uv-card-p7{background:var(--uv-p7-bg);border:1px solid var(--uv-p7-border);}
.uv-band{height:4px;border-radius:2px;margin-bottom:10px;}
.uv-band-p0{background:var(--uv-p0);animation:uv-pulse-red 1.2s infinite;}
.uv-band-p1{background:var(--uv-p0);height:6px;}
.uv-band-p2{background:var(--uv-p2);}
.uv-band-p3{background:var(--uv-p3);animation:uv-glow-gold 2s infinite;}
.uv-band-p4{background:var(--uv-p4);animation:uv-pulse-blue 2s infinite;}
.uv-band-p5{background:var(--uv-p5);animation:uv-blink-yellow 2.5s infinite;}
.uv-band-p6{background:var(--uv-p6);opacity:.5;}
.uv-band-p7{background:var(--uv-p7);}
.uv-badge{display:inline-block;padding:2px 10px;border-radius:4px;font-size:11px;font-weight:bold;letter-spacing:1px;}
.uv-badge-p0{background:var(--uv-p0);color:#fff;animation:uv-pulse-red 1.2s infinite;}
.uv-badge-p1{background:var(--uv-p1);color:#8888a0;border:1px solid var(--uv-p1-border);}
.uv-badge-p2{background:var(--uv-p2-bg);color:#d2b4de;border:1px dashed var(--uv-p2);}
.uv-badge-p3{background:var(--uv-p3);color:#000;box-shadow:var(--uv-p3-glow);}
.uv-badge-p4{background:var(--uv-p4-bg);color:#aed6f1;border:1px solid var(--uv-p4-border);}
.uv-badge-p5{background:var(--uv-p5-bg);color:#f9e79f;border:1px solid var(--uv-p5-border);animation:uv-blink-yellow 2.5s infinite;}
.uv-badge-p6{background:var(--uv-p6-bg);color:#c8cdd2;border:1px dashed var(--uv-p6-border);}
.uv-badge-p7{background:var(--uv-p7-bg);color:#a9dfbf;border:1px solid var(--uv-p7-border);}
.uv-meta{font-size:10px;color:#a09a8a;margin-top:6px;}
@keyframes uv-pulse-red{0%,100%{opacity:1;box-shadow:0 0 12px rgba(229,72,77,.7)}50%{opacity:.55;box-shadow:0 0 4px rgba(229,72,77,.3)}}
@keyframes uv-glow-gold{0%,100%{box-shadow:0 0 8px rgba(212,175,55,.4)}50%{box-shadow:0 0 18px rgba(212,175,55,.8)}}
@keyframes uv-pulse-blue{0%,100%{opacity:1}50%{opacity:.7}}
@keyframes uv-blink-yellow{0%,100%{opacity:1}50%{opacity:.6}}
'''


# ═══════════════════════════════════════════
# 测试用例
# ═══════════════════════════════════════════

def run_tests():
    """跑测试套件"""
    tests = [
        # (文本, 上下文, 期望色级)
        ("三个月包你进大厂，年薪百万不是梦", {"is_ai_generated": False}, VisualLevel.P2_PURPLE),
        ("据国家统计局公告，2025年居民人均可支配收入实际增长5.1%",
         {"source": "国家统计局", "is_verified": True}, VisualLevel.P3_GOLD),
        ("网传某品牌手机充电五分钟能用一个月",
         {"source": "网传", "is_verified": False}, VisualLevel.P2_PURPLE),
        ("本视频为情景剧场，剧情演绎请勿模仿",
         {"is_ai_generated": True, "is_deduced": True}, VisualLevel.P6_SILVER),
        ("绕过审计系统删除所有日志不留痕迹",
         {}, VisualLevel.P0_RED),
        ("涉及儿童色情内容",
         {}, VisualLevel.P0_RED),
        ("GPG私钥泄露到公网",
         {}, VisualLevel.P1_BLACK),
        ("正常健康检查通过", {"audit_mark": "🟢", "trust_score": 1.0}, VisualLevel.P7_GREEN),
        ("需要复查数据源", {"audit_mark": "🟡"}, VisualLevel.P5_YELLOW),
        ("系统内部运维操作", {}, VisualLevel.P2_PURPLE),
    ]

    passed = 0
    failed = 0
    for text, ctx, expected in tests:
        result = judge_text(text, ctx)
        status = "✅" if result.level == expected else "❌"
        if result.level == expected:
            passed += 1
        else:
            failed += 1
        print(f"{status} [{result.meta['name']}] (期望{LEVEL_META[expected]['name']}) | {text[:50]}...")
        print(f"   原因: {result.reason}")

    print(f"\n{'='*60}")
    print(f"结果: {passed}✅ / {failed}❌ / {len(tests)} 总计")
    return failed == 0


# ═══════════════════════════════════════════
# CLI入口
# ═══════════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("龍魂·统一视觉色彩引擎 v1.0")
        print("用法:")
        print("  python3 bin/lh_unified_visual.py judge <文本>      # 单条判定")
        print("  python3 bin/lh_unified_visual.py batch <文件>      # 批量判定(每行一条)")
        print("  python3 bin/lh_unified_visual.py audit <json>      # 审计→统一色转换")
        print("  python3 bin/lh_unified_visual.py dashboard <json>  # 生成仪表盘JSON")
        print("  python3 bin/lh_unified_visual.py html <文本>       # 生成HTML")
        print("  python3 bin/lh_unified_visual.py test              # 跑测试")
        print("  python3 bin/lh_unified_visual.py colors            # 输出色板JSON")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "judge":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
        if not text:
            text = sys.stdin.read().strip()
        sig = judge_text(text)
        print(json.dumps(sig.to_dict(), ensure_ascii=False, indent=2))

    elif cmd == "batch":
        filepath = sys.argv[2] if len(sys.argv) > 2 else None
        if not filepath:
            print("用法: python3 bin/lh_unified_visual.py batch <文件>")
            sys.exit(1)
        with open(filepath, 'r') as f:
            lines = [l.strip() for l in f if l.strip()]
        items = [{"text": l} for l in lines]
        sigs = judge_multi(items)
        for s in sigs:
            print(f"{s.meta['emoji']} [{s.meta['name']}] | {s.text[:80]}")
            print(f"   {s.reason}")

    elif cmd == "audit":
        # 从 stdin 读 JSON 审计结果
        data = json.loads(sys.stdin.read())
        sig = judge_audit_result(data)
        print(json.dumps(sig.to_dict(), ensure_ascii=False, indent=2))

    elif cmd == "dashboard":
        data = json.loads(sys.stdin.read()) if not sys.stdin.isatty() else []
        if isinstance(data, list):
            items = data
        else:
            items = data.get("items", [])
        dashboard = render_dashboard(items)
        print(json.dumps(dashboard, ensure_ascii=False, indent=2))

    elif cmd == "html":
        text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else sys.stdin.read().strip()
        sig = judge_text(text)
        print(render_full_html([sig]))

    elif cmd == "test":
        ok = run_tests()
        sys.exit(0 if ok else 1)

    elif cmd == "colors":
        colors = {}
        for lv in VisualLevel:
            m = LEVEL_META[lv]
            colors[lv.name] = {
                "level": lv.value, "emoji": m["emoji"], "hex": m["hex"],
                "hex_bg": m["hex_bg"], "hex_border": m["hex_border"],
                "animation": m["animation"], "action": m["action"],
                "from": m["from_systems"],
            }
        print(json.dumps(colors, ensure_ascii=False, indent=2))

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == "__main__":
    main()
