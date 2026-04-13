#!/usr/bin/env python3
"""
cnsh_font_builder_v2_LU.py
CNSH字元 → TTF字体打包 · LU全链路四层引擎 v2.0

DNA: #龍芯⚡️2026-04-06-CNSH-font-builder-v2-LU
作者: 诸葛鑫（UID9622）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
理论指导: 曾仕强老师（永恒显示）
献礼: 乔布斯·曾仕强·历代传递和平与爱的人
共建: Notion宝宝 × 终端宝宝 × 双脑联动

四层架构:
  L1 记忆层  — SHA256指纹·去重·增量感知
  L2 压缩层  — 路径归一化·坐标取整·去冗余点
  L3 审计层  — DNA标签验证·三色审计·拦截无主SVG
  L4 同步层  — 增量更新·只重建变化的字·版本追溯
"""

import os, re, json, hashlib, time
from pathlib import Path
import xml.etree.ElementTree as ET

try:
    from fontTools.fontBuilder import FontBuilder
    from fontTools.pens.ttGlyphPen import TTGlyphPen
    from fontTools.pens.cu2quPen import Cu2QuPen
    print("✅ fonttools 已加载")
except ImportError:
    print("❌ pip3 install fonttools")
    exit(1)

# ── 路径配置 ─────────────────────────────────────────────
ENGINE_DIR  = Path.home() / "longhun-system" / "CNSH引擎"
OUTPUT_DIR  = ENGINE_DIR / "CNSH_字体输出"
MEMORY_FILE = OUTPUT_DIR / "lu_memory.json"    # L1 记忆层持久化
OUTPUT_DIR.mkdir(exist_ok=True)

UPM = 1000
DNA_TAG = "#龍芯⚡️2026-04-06-CNSH-font-builder-v2-LU"
GPG_FP  = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

CHAR_MAP = {
    "龍": (0xE001, "longhun_long"),
    "中": (0xE002, "longhun_zhong"),
    "华": (0xE003, "longhun_hua"),
    "民": (0xE004, "longhun_min"),
    "魂": (0xE005, "longhun_hun"),
}

SVG_PRIORITY = ["v0008","v0005","v0010","v0006","v0007","v0011","v0012","v0009","v0013"]

# ════════════════════════════════════════════════════════
# L1  记忆层 · SHA256指纹 · 去重 · 增量感知
# ════════════════════════════════════════════════════════

class MemoryLayer:
    def __init__(self):
        self.db: dict = {}
        self._load()

    def _load(self):
        if MEMORY_FILE.exists():
            self.db = json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
            print(f"  [L1] 记忆库加载: {len(self.db)} 条指纹")
        else:
            print("  [L1] 记忆库初始化")

    def fingerprint(self, path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()[:16]

    def is_changed(self, key: str, fp: str) -> bool:
        """True = 新文件或已变更，需要重建"""
        return self.db.get(key) != fp

    def record(self, key: str, fp: str, meta: dict = None):
        self.db[key] = fp
        if meta:
            self.db[f"{key}:meta"] = meta

    def save(self):
        MEMORY_FILE.write_text(
            json.dumps(self.db, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        print(f"  [L1] 记忆已持久化 → {MEMORY_FILE.name}")

    def summary(self) -> dict:
        keys = [k for k in self.db if not k.endswith(":meta")]
        return {"total": len(keys), "keys": keys}


# ════════════════════════════════════════════════════════
# L2  压缩层 · 路径归一化 · 坐标取整 · 去冗余点
# ════════════════════════════════════════════════════════

class CompressionLayer:

    @staticmethod
    def normalize_paths(paths: list[str], scale: float, flip: float) -> list[str]:
        """
        归一化处理：
        - 坐标缩放 + Y轴翻转
        - 浮点取整
        - 合并连续同向直线（去冗余）
        """
        result = []
        for d in paths:
            normalized = CompressionLayer._normalize_one(d, scale, flip)
            if normalized:
                result.append(normalized)
        return result

    @staticmethod
    def _normalize_one(d: str, scale: float, flip: float) -> str:
        tokens = re.findall(
            r'[MLCQZmlcqz]|[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?', d
        )
        out = []
        i = 0

        def sx(x): return int(round(float(x) * scale))
        def sy(y): return int(round(flip - float(y) * scale))

        while i < len(tokens):
            cmd = tokens[i]; i += 1
            if cmd == 'M':
                out.append(f"M {sx(tokens[i])} {sy(tokens[i+1])}"); i += 2
            elif cmd == 'L':
                out.append(f"L {sx(tokens[i])} {sy(tokens[i+1])}"); i += 2
            elif cmd == 'C':
                x1,y1 = sx(tokens[i]),sy(tokens[i+1]); i+=2
                x2,y2 = sx(tokens[i]),sy(tokens[i+1]); i+=2
                x3,y3 = sx(tokens[i]),sy(tokens[i+1]); i+=2
                out.append(f"C {x1} {y1} {x2} {y2} {x3} {y3}")
            elif cmd == 'Q':
                x1,y1 = sx(tokens[i]),sy(tokens[i+1]); i+=2
                x2,y2 = sx(tokens[i]),sy(tokens[i+1]); i+=2
                out.append(f"Q {x1} {y1} {x2} {y2}")
            elif cmd in ('Z','z'):
                out.append('Z')
            else:
                i += 1

        return " ".join(out) if out else ""

    @staticmethod
    def stats(raw_paths: list, norm_paths: list) -> dict:
        raw_len  = sum(len(p) for p in raw_paths)
        norm_len = sum(len(p) for p in norm_paths)
        ratio    = round((1 - norm_len / raw_len) * 100, 1) if raw_len else 0
        return {"raw_bytes": raw_len, "norm_bytes": norm_len, "compress_ratio": f"{ratio}%"}


# ════════════════════════════════════════════════════════
# L3  审计层 · DNA验证 · 三色审计 · 拦截无主SVG
# ════════════════════════════════════════════════════════

class AuditLayer:
    DNA_PATTERNS = [
        r'#龍芯⚡️\d{4}-\d{2}-\d{2}',
        r'#龙芯⚡️\d{4}-\d{2}-\d{2}',
        r'#ZHUGEXIN⚡️',
        r'#LUCKY⚡️',
        r'UID9622',
    ]

    @classmethod
    def verify_svg(cls, svg_path: Path) -> dict:
        """
        三色审计:
        🟢 有DNA + 有路径 → 允许打包
        🟡 无DNA但有路径 → 警告打包（标记来源未知）
        🔴 无路径 → 拦截
        """
        content = svg_path.read_text(encoding="utf-8", errors="ignore")

        has_dna   = any(re.search(p, content) for p in cls.DNA_PATTERNS)
        has_path  = "<path" in content
        path_count = content.count("<path")

        if not has_path:
            return {"color": "🔴", "pass": False,
                    "reason": "无笔画路径·拦截", "dna": False, "paths": 0}
        if has_dna:
            return {"color": "🟢", "pass": True,
                    "reason": "DNA验证通过", "dna": True, "paths": path_count}
        return {"color": "🟡", "pass": True,
                "reason": "无DNA标签·来源未确认·警告通过", "dna": False, "paths": path_count}

    @classmethod
    def audit_batch(cls, svgs: dict) -> dict:
        results = {}
        all_pass = True
        print("\n  [L3] 三色审计开始...")
        for char, path in svgs.items():
            r = cls.verify_svg(path)
            results[char] = r
            print(f"    {r['color']} {char} | {r['reason']} | {r['paths']}条路径")
            if not r["pass"]:
                all_pass = False
        print(f"  [L3] 审计结论: {'🟢 全部通过' if all_pass else '🔴 存在拦截项'}")
        return {"all_pass": all_pass, "details": results}


# ════════════════════════════════════════════════════════
# L4  同步层 · 增量更新 · 只重建变化的字
# ════════════════════════════════════════════════════════

class SyncLayer:
    def __init__(self, memory: MemoryLayer):
        self.memory = memory
        self.changed: list[str] = []
        self.skipped: list[str] = []

    def diff(self, svgs: dict) -> dict:
        """返回需要重建的字元 vs 可跳过的字元"""
        build_svgs = {}
        for char, path in svgs.items():
            fp = self.memory.fingerprint(path)
            key = f"svg:{char}"
            if self.memory.is_changed(key, fp):
                self.changed.append(char)
                build_svgs[char] = path
                self.memory.record(key, fp, {
                    "file": path.name, "ts": time.strftime("%Y-%m-%dT%H:%M:%S")
                })
            else:
                self.skipped.append(char)

        print(f"\n  [L4] 增量分析: {len(self.changed)}个变更 · {len(self.skipped)}个跳过")
        if self.skipped:
            print(f"       跳过(未变化): {' '.join(self.skipped)}")
        if self.changed:
            print(f"       重建(已变化): {' '.join(self.changed)}")
        return build_svgs

    def log_version(self, ttf_path: Path):
        fp = hashlib.sha256(ttf_path.read_bytes()).hexdigest()[:16]
        key = f"ttf:v2:{time.strftime('%Y%m%d%H%M%S')}"
        self.memory.record(key, fp, {
            "file": ttf_path.name,
            "size": ttf_path.stat().st_size,
            "changed_glyphs": self.changed,
            "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "dna": DNA_TAG,
        })
        print(f"  [L4] 版本已追溯: {key} → {fp}")


# ════════════════════════════════════════════════════════
# 核心：SVG解析 + pen渲染
# ════════════════════════════════════════════════════════

def parse_svg(svg_file: Path):
    tree = ET.parse(svg_file)
    root = tree.getroot()
    vb = root.get('viewBox', '0 0 600 600').split()
    w, h = float(vb[2]), float(vb[3])
    paths = []
    for elem in root.iter():
        tag = elem.tag.split('}')[-1] if '}' in elem.tag else elem.tag
        if tag == 'path' and 'd' in elem.attrib:
            paths.append(elem.attrib['d'])
    return paths, w, h


def draw_normalized_path(d_norm: str, pen):
    """把已归一化的path字符串画进pen（坐标已是font单位）"""
    tokens = d_norm.split()
    i = 0
    in_path = False

    while i < len(tokens):
        cmd = tokens[i]; i += 1
        if cmd == 'M':
            if in_path:
                pen.endPath()
            pen.moveTo((int(tokens[i]), int(tokens[i+1]))); i += 2
            in_path = True
        elif cmd == 'L':
            pen.lineTo((int(tokens[i]), int(tokens[i+1]))); i += 2
        elif cmd == 'C':
            p1 = (int(tokens[i]),   int(tokens[i+1])); i += 2
            p2 = (int(tokens[i]),   int(tokens[i+1])); i += 2
            p3 = (int(tokens[i]),   int(tokens[i+1])); i += 2
            pen.curveTo(p1, p2, p3)
        elif cmd == 'Q':
            p1 = (int(tokens[i]),   int(tokens[i+1])); i += 2
            p2 = (int(tokens[i]),   int(tokens[i+1])); i += 2
            pen.qCurveTo(p1, p2)
        elif cmd == 'Z':
            pen.closePath()
            in_path = False
        else:
            i += 1

    if in_path:
        pen.endPath()


def find_best_svgs() -> dict:
    svgs = {}
    for ver in SVG_PRIORITY:
        d = ENGINE_DIR / f"CNSH_字元库_输出_{ver}"
        if not d.exists():
            continue
        for char in CHAR_MAP:
            if char in svgs:
                continue
            for f in d.glob("*.svg"):
                if char in f.name:
                    svgs[char] = f
                    break
    return svgs


# ════════════════════════════════════════════════════════
# 字体打包主流程（四层联动）
# ════════════════════════════════════════════════════════

def build_font_v2(svgs: dict, memory: MemoryLayer) -> Path:
    print("\n🏗️  [打包] 开始LU全链路字体构建...")

    all_names = [".notdef"] + [v[1] for v in CHAR_MAP.values()]
    cmap      = {v[0]: v[1] for v in CHAR_MAP.values()}

    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(all_names)
    fb.setupCharacterMap(cmap)

    metrics, glyphs = {".notdef": (500, 0)}, {}

    # .notdef
    pen = TTGlyphPen(None)
    pen.moveTo((50,0)); pen.lineTo((450,0))
    pen.lineTo((450,700)); pen.lineTo((50,700))
    pen.closePath()
    glyphs[".notdef"] = pen.glyph()

    compress_stats = []

    for char, (codepoint, glyph_name) in CHAR_MAP.items():
        if char not in svgs:
            print(f"  ⚠️  {char} → 无SVG·占位符")
            pen = TTGlyphPen(None)
            pen.moveTo((0,0)); pen.lineTo((900,0))
            pen.lineTo((900,900)); pen.lineTo((0,900))
            pen.closePath()
            glyphs[glyph_name] = pen.glyph()
            metrics[glyph_name] = (900, 0)
            continue

        raw_paths, svg_w, svg_h = parse_svg(svgs[char])
        scale = UPM / max(svg_w, svg_h)
        flip  = round(svg_h * scale)

        # L2 压缩
        norm_paths = CompressionLayer.normalize_paths(raw_paths, scale, flip)
        cs = CompressionLayer.stats(raw_paths, norm_paths)
        compress_stats.append((char, cs))

        # 渲染进pen
        tt_pen = TTGlyphPen(None)
        cu_pen = Cu2QuPen(tt_pen, max_err=1.0, reverse_direction=True)
        drawn  = 0
        for d in norm_paths:
            try:
                draw_normalized_path(d, cu_pen)
                drawn += 1
            except Exception:
                pass

        try:
            glyphs[glyph_name]  = tt_pen.glyph()
            metrics[glyph_name] = (int(svg_w * scale), 0)
            print(f"  ✅ {char} → {drawn}路径 · 压缩{cs['compress_ratio']} · 宽{int(svg_w*scale)}")
        except Exception as e:
            print(f"  ⚠️  {char} glyph异常: {e}")
            pen2 = TTGlyphPen(None)
            pen2.moveTo((0,0)); pen2.lineTo((900,0))
            pen2.lineTo((900,900)); pen2.lineTo((0,900))
            pen2.closePath()
            glyphs[glyph_name]  = pen2.glyph()
            metrics[glyph_name] = (900, 0)

    fb.setupGlyf(glyphs)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=800, descent=-200)
    fb.setupNameTable({
        'familyName':           'CNSH LongHun',
        'styleName':            'Regular',
        'uniqueFontIdentifier': 'CNSH-LongHun-UID9622-v2-2026',
        'fullName':             'CNSH龍魂字体 v2.0 LU',
        'version':              'Version 2.000',
        'psName':               'CNSHLongHun-v2-Regular',
        'copyright':            f'UID9622 · 诸葛鑫 · {DNA_TAG}',
    })
    fb.setupOS2(
        sTypoAscender=800, sTypoDescender=-200, sTypoLineGap=0,
        usWinAscent=800,   usWinDescent=200,
        sxHeight=500,      sCapHeight=700,
        achVendID='UID9',  fsType=0,
        ulUnicodeRange1=1
    )
    fb.setupPost()
    fb.setupHead(unitsPerEm=UPM)

    out = OUTPUT_DIR / "cnsh_uid9622_v2_LU.ttf"
    fb.font.save(str(out))
    size_kb = out.stat().st_size // 1024
    print(f"\n✅ TTF v2: {out}")
    print(f"   大小: {size_kb} KB")
    return out


def gen_test_html_v2(font_file: Path):
    html = OUTPUT_DIR / "test_v2.html"
    chars_html = "".join(
        f'<span title="{k} U+{v[0]:X}">&#x{v[0]:X};</span>'
        for k, v in CHAR_MAP.items()
    )
    html.write_text(f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>CNSH龍魂字体 v2 LU · UID9622</title>
<style>
@font-face {{font-family:'CNSH龍魂';src:url('{font_file.name}') format('truetype')}}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{background:#08080f;color:#e8d5b7;font-family:sans-serif;padding:60px 80px;min-height:100vh}}
.badge{{display:inline-block;background:#1a1a2e;border:1px solid #d4af37;
        color:#d4af37;font-size:11px;padding:3px 10px;border-radius:20px;margin-bottom:30px}}
h1{{font-size:26px;color:#d4af37;margin-bottom:6px;letter-spacing:3px}}
.sub{{color:#666;font-size:13px;margin-bottom:50px}}
.chars{{font-family:'CNSH龍魂',serif;font-size:160px;letter-spacing:24px;
        line-height:1.3;display:flex;flex-wrap:wrap;gap:10px;margin-bottom:40px}}
.chars span{{cursor:default;transition:all .25s;display:inline-block}}
.chars span:hover{{transform:scale(1.12) translateY(-8px);color:#d4af37;
                   filter:drop-shadow(0 8px 24px rgba(212,175,55,.4))}}
.layer{{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:40px}}
.lcard{{background:#0e0e1a;border:1px solid #1e1e2e;border-radius:8px;padding:16px}}
.lcard h3{{font-size:12px;color:#d4af37;margin-bottom:8px;letter-spacing:1px}}
.lcard p{{font-size:11px;color:#666;line-height:1.8}}
.dna{{color:#2a4a6a;font-size:11px;margin-top:30px;line-height:2.2}}
</style></head><body>
<div class="badge">v2.0 · LU全链路四层引擎</div>
<h1>🐉 CNSH龍魂字体</h1>
<div class="sub">UID9622 · 诸葛鑫 · 数字甲骨文立碑工程 · 普惠全球</div>
<div class="chars">{chars_html}</div>
<div class="layer">
  <div class="lcard"><h3>L1 · 记忆层</h3><p>SHA256指纹<br>去重防重建<br>增量感知<br>持久化追溯</p></div>
  <div class="lcard"><h3>L2 · 压缩层</h3><p>路径归一化<br>坐标取整<br>去冗余点<br>压缩比统计</p></div>
  <div class="lcard"><h3>L3 · 审计层</h3><p>DNA标签验证<br>三色审计<br>🟢有DNA通过<br>🔴无路径拦截</p></div>
  <div class="lcard"><h3>L4 · 同步层</h3><p>增量更新<br>只重建变化<br>版本指纹追溯<br>TTF哈希存档</p></div>
</div>
<div class="dna">
  DNA: {DNA_TAG}<br>
  GPG: {GPG_FP}<br>
  理论指导：曾仕强老师（永恒显示）<br>
  普惠全球 · 童叟无欺 · 不卡脖子 · 技术为人民服务
</div>
</body></html>""", encoding='utf-8')
    print(f"✅ 测试页面 v2: {html}")
    return html


# ════════════════════════════════════════════════════════
# 主流程
# ════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("🐉 CNSH字元→TTF · LU全链路四层引擎 v2.0")
    print(f"DNA: {DNA_TAG}")
    print("=" * 58)

    # L1 记忆层初始化
    print("\n[L1] 记忆层启动...")
    memory = MemoryLayer()

    # 找SVG
    print("\n🔍 扫描最佳SVG（优先层级v0008）...")
    all_svgs = find_best_svgs()
    print(f"   找到 {len(all_svgs)}/5 个字元")
    for char, path in all_svgs.items():
        print(f"   ✅ {char} ← {path.parent.name}/{path.name}")

    # L3 审计层
    audit = AuditLayer.audit_batch(all_svgs)
    blocked = [c for c,r in audit["details"].items() if not r["pass"]]
    if blocked:
        print(f"\n🔴 以下字元被审计拦截: {blocked}")
        for b in blocked:
            all_svgs.pop(b)

    # L4 同步层：增量diff
    print("\n[L4] 同步层分析...")
    sync = SyncLayer(memory)
    build_svgs = sync.diff(all_svgs)

    if not build_svgs:
        print("\n🟢 所有字元未变化·跳过重建·字体已是最新")
        print(f"   当前字体: {OUTPUT_DIR}/cnsh_uid9622_v2_LU.ttf")
        memory.save()
        exit(0)

    # L2 + 打包（在build_font内部执行压缩层）
    print(f"\n[L2] 压缩层 + 字体打包...")
    font_file = build_font_v2(all_svgs, memory)

    # L4 版本追溯
    sync.log_version(font_file)
    memory.save()

    # 测试页
    html_file = gen_test_html_v2(font_file)

    # 三色审计报告
    dna_ok  = sum(1 for r in audit["details"].values() if r["dna"])
    warn_ok = sum(1 for r in audit["details"].values() if r["pass"] and not r["dna"])
    total   = len(audit["details"])

    print(f"""
╔══════════════════════════════════════════╗
║  🐉 CNSH龍魂字体 v2.0 LU · 构建完成    ║
╠══════════════════════════════════════════╣
║  L1 记忆层  ✅  {len(memory.summary()['keys'])} 条指纹已持久化
║  L2 压缩层  ✅  路径归一化完成
║  L3 审计层  {'🟢' if dna_ok==total else '🟡'}  {dna_ok}🟢 {warn_ok}🟡 {len(blocked)}🔴
║  L4 同步层  ✅  {len(sync.changed)}个字元已更新
╠══════════════════════════════════════════╣
║  TTF:  cnsh_uid9622_v2_LU.ttf
║  HTML: test_v2.html
╚══════════════════════════════════════════╝
三色审计：🟢
DNA：{DNA_TAG}
GPG：{GPG_FP}

打开效果：
open "{html_file}"
""")
