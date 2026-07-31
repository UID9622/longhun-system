# -*- coding: utf-8 -*-
"""
龍魂民生系统 · 通用服务基类（焊死底座）

所有民生审计服务（合同审计 / 四绝开店 / P0电子签·照片审计）继承此基类，统一：
  - DNA追溯码生成（干支风格·唯一标识·不可伪造）
  - 三色审计（🔴红=风险/红线  🟢绿=通过/可信  🔵蓝=信息/提示）
  - 可信度分层（🟢真实公开 / 🔵龍魂示例库 / 🟡推演分析 / 🟣用户贡献 / 🔴红线）
  - 报告基类（to_json / render_html）+ 确认码（#CONFIRM🌌...-ONLY-ONCE🧬）
  - 本地持久化（SQLite·不上云·数据主权）
  - 不可删审计日志（append-only·data/<name>_audit_log/）

⚠️ 铁律：
  - 任何结论须挂 data_source（来源标注）+ derivation（推演标注），不允许黑箱。
  - 降级能力（缺真实数据源/缺联网）必须显式标 🟡 并在 notes 说明，不得伪装 🟢。
  - 审计日志 append-only，只增不删（对应 li/unlink 锁死）。
DNA #龍魂⚡️丙午·辛未·P0-BASE-v1
"""

import hashlib
import json
import os
import sqlite3
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Optional, Any

# ============================================================
# 干支 / 时辰 / DNA 追溯码
# ============================================================

GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
JIAZI = [GAN[i % 10] + ZHI[i % 12] for i in range(60)]
# 公历月 -> 近似月地支（仅作追溯码标识，非命理推演）
MONTH_ZHI = ["", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]
# 24h -> 12时辰
SHICHEN = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


def _gan_zhi_year(y: int) -> str:
    return GAN[(y - 4) % 10] + ZHI[(y - 4) % 12]


def make_dna(module: str, action: str, gua: str = "讼", applicant: str = "") -> str:
    """生成运行时 DNA 追溯码。

    格式: #龍魂⚡️<年干支>·<月支>月·<日干支>·<时辰>时·<卦>-<module>-<action>-<hash8>
    注: 日干支用日期稳定哈希映射到六十甲子，作为唯一追溯标识，非命理推演用途。
    """
    now = datetime.now()
    y = _gan_zhi_year(now.year)
    m = MONTH_ZHI[now.month]
    d = JIAZI[abs(hash(now.strftime("%Y-%m-%d"))) % 60]
    sc = SHICHEN[min(now.hour // 2, 11)]
    h = hashlib.sha256(
        f"{module}{action}{now.isoformat()}{applicant}".encode("utf-8")
    ).hexdigest()[:8]
    return f"#龍魂⚡️{y}·{m}月·{d}·{sc}时·{gua}-{module}-{action}-{h}"


# ============================================================
# 可信度分层
# ============================================================

class TrustTier(Enum):
    REAL = "🟢真实公开数据"
    LIBRARY = "🔵龍魂示例库"
    INFERENCE = "🟡推演分析"
    USER = "🟣用户贡献"
    RED_LINE = "🔴红线"


# ============================================================
# 三色审计（焊死）
# ============================================================

class ColorAudit:
    """三色审计容器。🔴红=风险/红线，🟢绿=通过/可信，🔵蓝=信息/提示。"""

    def __init__(self):
        self.red: List[Dict] = []
        self.green: List[Dict] = []
        self.blue: List[Dict] = []

    def add_red(self, item: str, level: str = "high", detail: str = "") -> None:
        self.red.append({"item": item, "level": level, "detail": detail})

    def add_green(self, item: str, detail: str = "") -> None:
        self.green.append({"item": item, "detail": detail})

    def add_blue(self, item: str, detail: str = "") -> None:
        self.blue.append({"item": item, "detail": detail})

    def from_dict(self, d: Dict[str, Any]) -> None:
        for k in ("red", "green", "blue"):
            for it in d.get(k, []):
                getattr(self, k).append(it)

    def summary(self) -> Dict[str, Any]:
        return {"red": len(self.red), "green": len(self.green), "blue": len(self.blue)}

    def verdict(self) -> str:
        """综合判定: 有高危红=不可信🔴; 有红=可疑🟡; 否则可信🟢。"""
        if any(r.get("level") == "high" for r in self.red):
            return "不可信🔴"
        if self.red:
            return "可疑🟡"
        return "可信🟢"

    def to_dict(self) -> Dict[str, Any]:
        return {"red": self.red, "green": self.green, "blue": self.blue}


# ============================================================
# 数据来源 / 推演标注（杜绝黑箱·焊死）
# ============================================================

@dataclass
class SourceRef:
    tier: TrustTier
    source_url: str          # 来源标注（URL/路径/API名/库名）
    reliability: str         # high / medium / low
    fetch_time: str          # ISO 时间
    notes: str               # 备注（强制非空）
    ref_policy: str = ""     # 引用法规/政策依据（政策类强制）

    def validate(self) -> bool:
        assert self.source_url, "❌ 来源URL不能为空（来源标注缺失）"
        assert self.notes, "❌ 备注不能为空（备注规范缺失）"
        if self.tier in (TrustTier.LIBRARY, TrustTier.RED_LINE) and not self.ref_policy:
            # 龍魂库/红线类建议带依据；不强报错，记录即可
            pass
        return True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "tier": self.tier.value,
            "source_url": self.source_url,
            "reliability": self.reliability,
            "fetch_time": self.fetch_time,
            "notes": self.notes,
            "ref_policy": self.ref_policy,
        }


# ============================================================
# 报告基类
# ============================================================

@dataclass
class MinshengReport:
    dna_trace: str
    applicant: str
    version: str
    audit_level: str = "P0"
    color_audit: ColorAudit = field(default_factory=ColorAudit)
    data_sources: List[SourceRef] = field(default_factory=list)
    extra_sections: List[str] = field(default_factory=list)   # 子类注入HTML区块
    meta_extra: Dict[str, Any] = field(default_factory=dict)
    confirm_code: str = ""

    def generate_confirm_code(self) -> str:
        base = f"{self.dna_trace}{self.applicant}{datetime.now().isoformat()}"
        self.confirm_code = f"#CONFIRM🌌{hashlib.sha256(base.encode()).hexdigest()[:8]}-ONLY-ONCE🧬"
        return self.confirm_code

    def add_source(self, src: SourceRef) -> None:
        src.validate()
        self.data_sources.append(src)

    def validate(self) -> bool:
        assert self.dna_trace.startswith("#龍魂"), "❌ DNA追溯码格式错误"
        assert self.data_sources, "❌ 缺少数据来源（来源标注缺失·黑箱）"
        for s in self.data_sources:
            s.validate()
        return True

    def to_json(self) -> Dict[str, Any]:
        self.validate()
        return {
            "meta": {
                "dna_trace": self.dna_trace,
                "applicant": self.applicant,
                "version": self.version,
                "audit_level": self.audit_level,
                "audit_time": datetime.now().isoformat(),
                "verdict": self.color_audit.verdict(),
                **self.meta_extra,
            },
            "color_audit": self.color_audit.to_dict(),
            "data_sources": [s.to_dict() for s in self.data_sources],
            "confirm_code": self.confirm_code or self.generate_confirm_code(),
        }

    # ---------- HTML 渲染（暗色龍魂金·响应式） ----------
    def render_html(self) -> str:
        self.validate()
        v = self.color_audit.verdict()
        v_color = {"不可信🔴": "#ff4d4f", "可疑🟡": "#ffc53d", "可信🟢": "#52c41a"}.get(v, "#ffc53d")
        src_rows = "".join(
            f"<tr><td>{s.tier.value}</td><td>{s.source_url}</td>"
            f"<td>{s.reliability}</td><td>{s.notes}</td><td>{s.ref_policy or '—'}</td></tr>"
            for s in self.data_sources
        )
        sections = "\n".join(self.extra_sections)
        return f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>龍魂审计 · {self.audit_level}</title>
<style>
:root{{--gold:#d4af37;--bg:#0e0e10;--card:#1a1a1f;--line:#333;--fg:#e8e8e8}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--bg);color:var(--fg);
font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif}}
.wrap{{max-width:960px;margin:0 auto;padding:24px}}
h1{{color:var(--gold);border-bottom:2px solid var(--gold);padding-bottom:8px}}
h2{{color:var(--gold);margin-top:28px;border-left:4px solid var(--gold);padding-left:10px}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px;margin:12px 0}}
.kv{{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px dashed #2a2a2a}}
.verdict{{font-size:24px;font-weight:700;text-align:center;padding:14px;border-radius:10px;
background:#000;color:{v_color};border:2px solid {v_color}}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{border:1px solid var(--line);padding:6px 8px;text-align:left}}
th{{background:#222;color:var(--gold)}}
.r{{color:#ff4d4f}} .g{{color:#52c41a}} .b{{color:#4ea1ff}}
.tag{{display:inline-block;background:#222;border:1px solid var(--line);border-radius:6px;
padding:2px 8px;margin:2px;font-size:12px}}
</style></head><body><div class="wrap">
<h1>龍魂{self.audit_level}级审计报告</h1>
<div class="card"><div class="kv"><span>DNA追溯码</span><b>{self.dna_trace}</b></div>
<div class="kv"><span>申请人</span><span>{self.applicant}</span></div>
<div class="kv"><span>报告版本</span><span>{self.version}</span></div>
<div class="kv"><span>审计时间</span><span>{datetime.now().isoformat(timespec='seconds')}</span></div>
<div class="kv"><span>确认码</span><b>{self.confirm_code or '（未生成）'}</b></div></div>
<div class="verdict">{v}</div>
<div class="card"><h2>三色审计</h2>
<span class="r">🔴 红 {self.color_audit.summary()['red']}</span> &nbsp;
<span class="g">🟢 绿 {self.color_audit.summary()['green']}</span> &nbsp;
<span class="b">🔵 蓝 {self.color_audit.summary()['blue']}</span>
{'<ul>'+''.join(f'<li class="r">🔴 [{r.get("level","")}] {r["item"]} {r.get("detail","")}</li>' for r in self.color_audit.red)+'</ul>' if self.color_audit.red else '<p class="g">无红色风险</p>'}
{'<ul>'+''.join(f'<li class="g">🟢 {g["item"]} {g.get("detail","")}</li>' for g in self.color_audit.green)+'</ul>' if self.color_audit.green else ''}
{'<ul>'+''.join(f'<li class="b">🔵 {b["item"]} {b.get("detail","")}</li>' for b in self.color_audit.blue)+'</ul>' if self.color_audit.blue else ''}
</div>
{sections}
<div class="card"><h2>数据来源声明</h2>
<table><tr><th>可信度</th><th>来源</th><th>可靠性</th><th>备注</th><th>依据</th></tr>{src_rows}</table>
<p style="color:#888;font-size:12px">本报告依据《中华人民共和国电子签名法》/《民法典》及龍魂P0焊死底座生成，
结论仅供参考，最终决策由申请人自行做出。</p></div>
</div></body></html>"""


# ============================================================
# 持久化基类（SQLite·本地·数据主权）+ 不可删日志
# ============================================================

class BaseMinshengService:
    """民生服务基类：本地持久化 + append-only 审计日志。"""

    def __init__(self, name: str, db_path: Optional[Path] = None,
                 log_dir: Optional[Path] = None):
        self.name = name
        base = Path(__file__).resolve().parent
        self.db = db_path or (base / "data" / f"{name}.db")
        self.log_dir = log_dir or (base / "data" / f"{name}_audit_log")
        os.makedirs(self.db.parent, exist_ok=True)
        os.makedirs(self.log_dir, exist_ok=True)
        self._init_db()

    def _init_db(self) -> None:
        conn = sqlite3.connect(self.db)
        conn.execute("""CREATE TABLE IF NOT EXISTS reports (
            dna TEXT PRIMARY KEY, payload TEXT, confirmed INTEGER DEFAULT 0,
            confirm_code TEXT, confirm_time TEXT, created TEXT)""")
        conn.commit()
        conn.close()

    def persist(self, report_json: Dict[str, Any]) -> None:
        dna = report_json["meta"]["dna_trace"]
        conn = sqlite3.connect(self.db)
        conn.execute(
            "INSERT OR REPLACE INTO reports (dna, payload, created) VALUES (?,?,?)",
            (dna, json.dumps(report_json, ensure_ascii=False), datetime.now().isoformat()))
        conn.commit()
        conn.close()
        # 同步写不可删日志
        self.append_audit_log(f"PERSIST dna={dna} verdict={report_json['meta'].get('verdict')}")

    def load(self, dna: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db)
        row = conn.execute("SELECT payload, confirmed, confirm_code, confirm_time "
                           "FROM reports WHERE dna=?", (dna,)).fetchone()
        conn.close()
        if not row:
            return None
        payload = json.loads(row[0])
        payload.setdefault("confirm", {})["confirmed"] = bool(row[1])
        if row[2]:
            payload["confirm"]["code"] = row[2]
        if row[3]:
            payload["confirm"]["confirm_time"] = row[3]
        return payload

    def confirm(self, dna: str, confirm_code: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db)
        if not conn.execute("SELECT 1 FROM reports WHERE dna=?", (dna,)).fetchone():
            conn.close()
            return None
        conn.execute(
            "UPDATE reports SET confirmed=1, confirm_code=?, confirm_time=? WHERE dna=?",
            (confirm_code, datetime.now().isoformat(), dna))
        conn.commit()
        conn.close()
        self.append_audit_log(f"CONFIRM dna={dna} code={confirm_code[:20]}")
        return self.load(dna)

    def append_audit_log(self, entry: str) -> None:
        """不可删审计日志：按日追加，只增不删。"""
        today = datetime.now().strftime("%Y-%m-%d")
        log_path = self.log_dir / f"{today}.log"
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().isoformat(timespec='seconds')}] {entry}\n")


if __name__ == "__main__":
    # 自测：基类可实例化、DNA/三色/报告渲染跑通
    svc = BaseMinshengService("__base_selftest__")
    dna = make_dna("BASE", "selftest", gua="乾")
    rep = MinshengReport(dna_trace=dna, applicant="自检", version="v1", audit_level="P0")
    rep.color_audit.add_green("基类自检通过")
    rep.add_source(SourceRef(TrustTier.LIBRARY, "龍魂基类自测", "high",
                             datetime.now().isoformat(), "自测来源"))
    rep.generate_confirm_code()
    j = rep.to_json()
    h = rep.render_html()
    svc.persist(j)
    back = svc.load(dna)
    assert back and back["meta"]["dna_trace"] == dna
    assert "<html" in h
    print("✅ 基类自测通过 | DNA:", dna, "| verdict:", rep.color_audit.verdict())
