# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 龍芯⚡️丙午·丙申·戊申·午时·䷗复-DNA-VINFINITY-MIGRATOR-v2.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂系统 · DNA 统一迁移引擎 v2.0
作者：诸葛鑫（UID9622）
功能：全库旧/残缺 DNA 格式 → v∞ 干支四柱+卦 统一对齐
  - scan   : 只读扫描，统计旧码分布 + 抽样预览（不写任何文件）
  - apply  : 真改，改前自动备份原文件到 04_AUDIT/dna_migration/backup/，生成迁移台账
迁移规则（只换时间戳/补缺失段，后缀原样保留）：
  - A1  格里历 `#龍芯⚡️丙午·乙未·甲午·庚午·䷳艮为山-XXX`  → 日期(默认午时)→ 四柱+卦
  - A2a 纯数字8位 `#龍芯⚡️丙午·乙未·庚戌·壬午·䷕贲-XXX` → 日期(午时)→ 四柱+卦
  - A2b 纯数字14位 `#龍芯⚡️丙午·乙未·戊申·乙卯·䷡大壮-XXX` → 精确时刻→ 四柱+卦
  - A3  节气 `#龍芯⚡️丙午·乙未·壬午·甲辰·䷴渐-XXX` → 节气日+时刻→ 四柱+卦
  - B1  3干支+卦缺时辰 `丙午·丙申·庚戌·䷙大畜-X` → 补午时干支
  - B2  3干支+时辰缺卦 `丙午·丙申·庚申·亥时-X` → 时辰转干支+推卦
  - B3  3干支+卦名无卦符 `丙午·乙未·乙丑·未济-X` → 卦名→卦符+补午时干支
  - B0c 3干支+时辰+卦名 `丙午·乙未·戊寅·午时·大有-X` → 卦名→卦符
  - B0d 四柱+卦名无卦符 `丙午·乙未·丁酉·丙午·大有-X` → 卦名→卦符
  - C2  3干支无卦无时辰 `丙午·丙申·癸亥-X` → 午时干支+推卦
跳过（冻结/待核/模板/运行时）：
  - C1 2干支+动作 `丙午·丙申-X`（缺日柱无法推）· C3 干支+卦 `丙午·䷗复-X`
  - 模板字面量 `YYYY-MM-DD` · 含 `{}`/`$`/引号的运行时动态 DNA · 截断/非法干支
  - .json 校验清单（证据快照）· 隔离区/交付包/剪贴板/导出镜像
用法:
  python3 08_BIN/lh_dna_v∞_migrator.py scan  [--dir DIR] [--sample N]
  python3 08_BIN/lh_dna_v∞_migrator.py apply [--dir DIR] [--limit N] [--force]
"""
import argparse
import datetime
import json
import os
import re
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "bin"))
from lh_dna_generator import get_ganzhi, get_hexagram, HEXAGRAM_DATA  # noqa: E402

VERSION = "v2.0"
DNA = "#龍芯⚡️丙午·丙申·戊申·午时·䷗复-DNA-VINFINITY-MIGRATOR-v2.0"

# ---- 跳过规则 ----
SKIP_DIR_PARTS = (".git", ".venv", "venv", "node_modules", "__pycache__",
                  "11_DATA", "_work", "dist", "models", "archive", "backups",
                  "backup", "backups", "site-packages", ".idea", ".vscode",
                  "龍魂成片", "models_backup")
SKIP_EXTS = (".asc", ".bak", ".glyph-backup", ".pyc", ".png", ".jpg", ".jpeg",
             ".gif", ".webp", ".mp4", ".wav", ".mp3", ".zip", ".tar", ".gz",
             ".pdf", ".woff", ".woff2", ".ttf", ".otf", ".db", ".sqlite",
             ".pem", ".key", ".p12", ".npy", ".pt", ".bin", ".ico", ".icns")
EXT_ALLOWED = (".py", ".md", ".sh", ".js", ".html", ".ts", ".yml", ".yaml", ".css", ".mjs", ".cjs", ".vue", ".rs", ".go")

# ---- 干支基础 ----
TIAN = "甲乙丙丁戊己庚辛壬癸"
DI = "子丑寅卯辰巳午未申酉戌亥"
GZ_RE = f"[{TIAN}][{DI}]"
GUAFU = "䷀䷁䷂䷃䷄䷅䷆䷇䷈䷉䷊䷋䷌䷍䷎䷏䷐䷑䷒䷓䷔䷕䷖䷗䷘䷙䷚䷛䷜䷝䷞䷟䷠䷡䷢䷣䷤䷥䷦䷧䷨䷩䷪䷫䷬䷭䷮䷯䷰䷱䷲䷳䷴䷵䷶䷷䷸䷹䷺䷻䷼䷽䷾䷿"
SHI_CN = "子丑寅卯辰巳午未申酉戌亥"

# ---- 旧格式正则 ----
RE_A1 = re.compile(r'#龍芯⚡️(?P<y>20\d{2})[-_](?P<m>\d{2})[-_](?P<d>\d{2})(?:[-_](?P<h>[01]?\d|2[0-3])[:：.](?P<min>[0-5]\d))?')
RE_TMPL = re.compile(r'#龍芯⚡️(YYYY|yyyy|MM|DD|XX)[-_.]?(YYYY|yyyy|MM|DD|XX)?')

# 运行时动态特征：含花括号/美元/百分号/引号/反引号 → 跳过不碰
RUNTIME_CHARS = set('{}`$%"\'<>|&;')

# 64卦全称 → (卦符, 简名)
QUANCHENG = {
    "乾为天": "䷀乾", "坤为地": "䷁坤", "水雷屯": "䷂屯", "山水蒙": "䷃蒙",
    "水天需": "䷄需", "天水讼": "䷅讼", "地水师": "䷆师", "水地比": "䷇比",
    "风天小畜": "䷈小畜", "天泽履": "䷉履", "地天泰": "䷊泰", "天地否": "䷋否",
    "天火同人": "䷌同人", "火天大有": "䷍大有", "地山谦": "䷎谦", "雷地豫": "䷏豫",
    "泽雷随": "䷐随", "山风蛊": "䷑蛊", "地泽临": "䷒临", "风地观": "䷓观",
    "火雷噬嗑": "䷔噬嗑", "山火贲": "䷕贲", "山地剥": "䷖剥", "地雷复": "䷗复",
    "天雷无妄": "䷘无妄", "山天大畜": "䷙大畜", "山雷颐": "䷚颐", "泽风大过": "䷛大过",
    "坎为水": "䷜坎", "离为火": "䷝离", "泽山咸": "䷞咸", "雷风恒": "䷟恒",
    "天山遁": "䷠遁", "雷天大壮": "䷡大壮", "火地晋": "䷢晋", "地火明夷": "䷣明夷",
    "风火家人": "䷤家人", "火泽睽": "䷥睽", "水山蹇": "䷦蹇", "雷水解": "䷧解",
    "山泽损": "䷨损", "风雷益": "䷩益", "泽天夬": "䷪夬", "天风姤": "䷫姤",
    "泽地萃": "䷬萃", "地风升": "䷭升", "泽水困": "䷮困", "水风井": "䷯井",
    "泽火革": "䷰革", "火风鼎": "䷱鼎", "震为雷": "䷲震", "艮为山": "䷳艮",
    "风山渐": "䷴渐", "雷泽归妹": "䷵归妹", "雷火丰": "䷶丰", "火山旅": "䷷旅",
    "巽为风": "䷸巽", "兑为泽": "䷹兑", "风水涣": "䷺涣", "水泽节": "䷻节",
    "风泽中孚": "䷼中孚", "雷山小过": "䷽小过", "水火既济": "䷾既济", "火水未济": "䷿未济",
}
# 简名 → (卦符, 简名) 从 HEXAGRAM_DATA 构建
JIANMING = {}
for _n, _hx in HEXAGRAM_DATA.items():
    if isinstance(_hx, dict) and "symbol" in _hx and "name" in _hx:
        JIANMING[_hx["name"]] = (_hx["symbol"], _hx["name"])
# 全称表补入全称 + 简名（䷇比 → '比'）两种等价键
for _qc, _v in QUANCHENG.items():
    JIANMING.setdefault(_qc, _v)
    JIANMING.setdefault(_v[1:], _v)  # 简名（卦符后）

# 2026年节气日（公历·±1天误差·A3 迁移后人工核对）
JIEQI_2026 = {
    "小寒": "2026-01-05", "大寒": "2026-01-20", "立春": "2026-02-04", "雨水": "2026-02-18",
    "惊蛰": "2026-03-05", "春分": "2026-03-20", "清明": "2026-04-04", "谷雨": "2026-04-20",
    "立夏": "2026-05-05", "小满": "2026-05-21", "芒种": "2026-06-05", "夏至": "2026-06-21",
    "小暑": "2026-07-07", "大暑": "2026-07-22", "立秋": "2026-08-07", "处暑": "2026-08-23",
    "白露": "2026-09-07", "秋分": "2026-09-23", "寒露": "2026-10-08", "霜降": "2026-10-23",
    "立冬": "2026-11-07", "小雪": "2026-11-22", "大雪": "2026-12-07", "冬至": "2026-12-22",
}


def _skip_path(path: Path) -> bool:
    parts = path.parts
    for p in parts:
        if p in SKIP_DIR_PARTS:
            return True
    if path.suffix.lower() in SKIP_EXTS:
        return True
    if path.suffix.lower() not in EXT_ALLOWED:
        return True
    return False


# ---------- 转换核心 ----------

def _gua_sym_name(symbol: str, name: str) -> str:
    """卦符 + 简名（HEXAGRAM_DATA 卦名全称/简名不统一 → 统一输出简名）"""
    jm = JIANMING.get(name)
    if jm:
        return jm[0] + jm[1]
    return symbol + name


def _dt_to_ts(now: datetime.datetime) -> str:
    """datetime → 干支四柱+时辰+卦 时间戳段"""
    g = get_ganzhi(now)
    h_num = get_hexagram(g["raw"]["day_z"], g["raw"]["shi_index"])
    hexa = HEXAGRAM_DATA.get(h_num, HEXAGRAM_DATA[1])
    return f"{g['year']}·{g['month']}·{g['day']}·{g['hour']}·{_gua_sym_name(hexa['symbol'], hexa['name'])}"


def _hour_gz(day_g: int, shi_idx: int) -> str:
    """五鼠遁: 日干 + 时辰地支 → 时辰干支"""
    return TIAN[(day_g * 2 + shi_idx) % 10] + DI[shi_idx]


def _hexa_str(day_z: int, shi_idx: int) -> str:
    """日支 + 时辰 → 卦符+卦名（统一简名）"""
    h_num = get_hexagram(day_z, shi_idx)
    hexa = HEXAGRAM_DATA.get(h_num, HEXAGRAM_DATA[1])
    return _gua_sym_name(hexa["symbol"], hexa["name"])


def _gua_from_name(name: str):
    """卦名(全称/简名/带卦字) → (卦符, 简名) 或 None"""
    n = name.rstrip("卦")
    for cand in (n, name):
        if cand in JIANMING:
            return JIANMING[cand]
    return None


def _is_gz(seg: str) -> bool:
    return len(seg) == 2 and seg[0] in TIAN and seg[1] in DI


def _gz_ok(seg: str) -> bool:
    """干支合法性：结构 + 60甲子奇偶一致性（甲乙丙丁…序偶与地支序偶一致）"""
    if len(seg) < 2 or seg[0] not in TIAN or seg[1] not in DI:
        return False
    return (TIAN.index(seg[0]) % 2) == (DI.index(seg[1]) % 2)


# 八卦符号 → 重卦（8纯卦）
BAGUA_QUAN = {"乾": "䷀乾", "兑": "䷹兑", "离": "䷝离", "震": "䷲震",
              "巽": "䷸巽", "坎": "䷜坎", "艮": "䷳艮", "坤": "䷁坤"}
BAGUA_SYM = "☰☱☲☳☴☵☶☷"


def _gua_part(part: str):
    """解析卦段开头（64卦符/八卦符号/卦名）→ (卦符+卦名, 已消耗长度) 或 None"""
    if not part:
        return None
    if part[0] in GUAFU:  # 64卦符
        m = re.match(r'^([䷀-䷿][一-龥]{0,4})', part)
        return (m.group(1), len(m.group(1)))
    if part[0] in BAGUA_SYM:  # 八卦符号 ☰乾
        name = {"☰": "乾", "☱": "兑", "☲": "离", "☳": "震",
                "☴": "巽", "☵": "坎", "☶": "艮", "☷": "坤"}[part[0]]
        m = re.match(r'^[☰☱☲☳☴☵☶☷]([一-龥]{1,2})', part)
        consumed = len(m.group(0)) if m else 1
        return (BAGUA_QUAN[name], consumed)
    m = re.match(r'^([一-龥]{1,4})', part)
    if m:
        gua = _gua_from_name(m.group(1))
        if gua:
            return (gua[0] + gua[1], len(m.group(1)))
    return None


def _shi_part(part: str):
    """解析时辰段 → (地支字符, 已消耗长度) 或 None。
    支持 `亥时` / `亥時` / 单字 `酉` / 时辰干支式 `甲子时` `甲子時`"""
    if len(part) >= 2 and part[0] in DI and part[1] in "时時":
        return (part[0], 2)
    if len(part) >= 3 and part[0] in TIAN and part[1] in DI and part[2] in "时時":
        return (part[1], 3)
    if part and part[0] in DI and (len(part) == 1 or (len(part) >= 2 and part[1] in "-_")):
        return (part[0], 1)
    return None


def _runtime(s: str) -> bool:
    """含运行时特征字符 → True(跳过)"""
    return any(c in s for c in RUNTIME_CHARS)


def _try_date(s: str):
    """日期类旧码 → (新串, 类别) 或 None（非日期类）"""
    m = re.match(r'^(20\d{2})[-_](0\d|1[0-2])[-_](0\d|[12]\d|3[01])'
                 r'(?:[-_]([01]?\d|2[0-3])[:：.]([0-5]\d))?', s)
    if m:
        try:
            hh = int(m.group(4)) if m.group(4) else 12
            mm = int(m.group(5)) if m.group(5) else 0
            now = datetime.datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)), hh, mm)
            return _dt_to_ts(now) + s[m.end():], "A1_格里历"
        except Exception:  # noqa: BLE001
            return None, "Z_非法日期"
    m = re.match(r'^(20\d{6,17})[-_]', s)
    if m:
        sep = s[m.end() - 1]  # 保留原分隔符 - 或 _
        d = m.group(1)[:14]
        try:
            if len(d) == 14:
                now = datetime.datetime(int(d[:4]), int(d[4:6]), int(d[6:8]),
                                        int(d[8:10]), int(d[10:12]), int(d[12:14]))
                cls = "A2b_时间戳"
            else:
                now = datetime.datetime(int(d[:4]), int(d[4:6]), int(d[6:8]), 12)
                cls = "A2a_日期"
            return _dt_to_ts(now) + sep + s[m.end():], cls
        except Exception:  # noqa: BLE001
            return None, "Z_非法日期"
    m = re.match(r'^(20\d{8})·', s)  # A2c 8位日期 + · + 后缀
    if m:
        d = m.group(1)
        try:
            now = datetime.datetime(int(d[:4]), int(d[4:6]), int(d[6:8]), 12)
            return _dt_to_ts(now) + "·" + s[m.end():], "A2c_日期·后缀"
        except Exception:  # noqa: BLE001
            return None, "Z_非法日期"
    m = re.match(r'^([一-龥]{2})(20\d{2})·(\d\d):(\d\d):(\d\d)[-_]', s)
    if m:
        sep = s[m.end() - 1]  # 保留原分隔符 - 或 _
        jq, yr = m.group(1), m.group(2)
        base = JIEQI_2026.get(jq)
        if base and yr == "2026":
            try:
                now = datetime.datetime(int(base[:4]), int(base[5:7]), int(base[8:10]),
                                        int(m.group(3)), int(m.group(4)), int(m.group(5)))
                return _dt_to_ts(now) + sep + s[m.end():], "A3_节气"
            except Exception:  # noqa: BLE001
                return None, "Z_非法日期"
        return None, "Z_节气无表"
    return None


_TAIL_CHARS = set("`'\".,;:!?)]}，。、；：！？）》】")


def _migrate_dna(s: str):
    """对 `#龍芯⚡️` 后的 DNA 串分类迁移。返回 (新串, 类别) 或 (None, 类别) 表示跳过。
    先剥离行内尾随标点（反引号/引号/括号等），分类迁移后原样拼回。"""
    i = len(s)
    while i > 0 and s[i - 1] in _TAIL_CHARS:
        i -= 1
    clean, tail = s[:i], s[i:]
    res = _migrate_clean(clean)
    if res is None:
        return None, "Z_非法"
    new, cls = res
    if new is None:
        return None, cls
    return new + tail, cls


def _migrate_clean(s: str):
    """核心分类迁移（s 不含行内尾随标点）。返回 (新串, 类别) 或 (None, 类别) 跳过。"""
    if _runtime(s):
        return None, "Z_运行时"
    r = _try_date(s)
    if r is not None:
        return r
    parts = s.split("·")
    n = len(parts)
    if n < 2:
        return None, "Z_其他"
    # 头部连续干支段（纯干支）
    def gz_run(k):
        return all(_gz_ok(p) and len(p) == 2 for p in parts[:k])
    day_of = lambda seg: (TIAN.index(seg[0]), DI.index(seg[1]))

    if n == 5:
        if gz_run(4):  # 四柱 + 第5段(卦/动作)
            gp = _gua_part(parts[4])
            if gp:
                if parts[4][0] in GUAFU:
                    return None, "B0a_标准"
                new4 = gp[0] + parts[4][gp[1]:]
                return "·".join(parts[:4]) + "·" + new4, "B0d_补卦符"
            return None, "Z_5段杂项"
        if gz_run(3):  # 3干支 + 时辰 + 第5段
            sp = _shi_part(parts[3])
            if sp:
                gp = _gua_part(parts[4])
                if gp:
                    if parts[4][0] in GUAFU:
                        return None, "B0b_标准"
                    new4 = gp[0] + parts[4][gp[1]:]
                    return "·".join(parts[:4]) + "·" + new4, "B0c_补卦符"
            return None, "Z_5段杂项"
        return None, "Z_其他"
    if n == 4:
        if gz_run(3):
            day_g, day_z = day_of(parts[2])
            gp = _gua_part(parts[3])
            if gp:  # B1 3干支+卦缺时辰 → 补午时干支
                noon = _hour_gz(day_g, 6)
                new3 = gp[0] + parts[3][gp[1]:]
                return "·".join(parts[:3]) + f"·{noon}·" + new3, "B1_补午时"
            sp = _shi_part(parts[3])
            if sp:  # B2 3干支+时辰缺卦 → 时辰转干支+推卦
                shi_idx = DI.index(sp[0])
                shi_gz = _hour_gz(day_g, shi_idx)
                hexa = _hexa_str(day_z, shi_idx)
                return "·".join(parts[:3]) + f"·{shi_gz}·{hexa}" + parts[3][sp[1]:], "B2_补卦"
            # C2b 3干支+动作 → 补午时+推卦（动作前缀用 -，符合 v∞ 标准）
            noon = _hour_gz(day_g, 6)
            hexa = _hexa_str(day_z, 6)
            return "·".join(parts[:3]) + f"·{noon}·{hexa}-" + parts[3], "C2b_动作补全"
        return None, "Z_其他"
    if n == 3:
        if gz_run(2):
            if len(parts[2]) == 2 and _gz_ok(parts[2]):  # 纯 3 干支
                day_g, day_z = day_of(parts[2])
                noon = _hour_gz(day_g, 6)
                hexa = _hexa_str(day_z, 6)
                return "·".join(parts) + f"·{noon}·{hexa}", "C2a_补全"
            if len(parts[2]) > 2 and _gz_ok(parts[2][:2]) and parts[2][2] in "-_":
                day_g, day_z = day_of(parts[2][:2])
                noon = _hour_gz(day_g, 6)
                hexa = _hexa_str(day_z, 6)
                return "·".join(parts[:2]) + f"·{parts[2][:2]}·{noon}·{hexa}" + parts[2][2:], "C2a_补全"
            return None, "C1_冻结"  # 2干支+动作（缺日柱无法推）
        return None, "Z_其他"
    if n == 2:
        return None, "C3_冻结"
    return None, "Z_其他"


# ---------- 扫描 ----------

def _scan_file(path: Path, stats: dict, samples: list, sample_n: int):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        return
    for ln, line in enumerate(text.splitlines(), 1):
        if "#龍芯⚡️" not in line:
            continue
        if RE_TMPL.search(line):
            stats.setdefault("Z_模板", 0)
            stats["Z_模板"] += 1
            continue
        for m in re.finditer(r'#龍芯⚡️([^\s#]+)', line):
            old = m.group(1)
            new, cls = _migrate_dna(old)
            stats.setdefault(cls, 0)
            stats[cls] += 1
            if new and len(samples) < sample_n:
                samples.append({"file": str(path), "line": ln, "old": old, "new": new, "cls": cls})


def cmd_scan(args):
    stats = {}
    samples = []
    root = Path(args.dir)
    files = list(root.rglob("*")) if root.is_dir() else [root]
    for f in files:
        if not f.is_file() or _skip_path(f):
            continue
        _scan_file(f, stats, samples, args.sample)
    print(f"📡 DNA 迁移扫描报告 — {root}")
    print("   " + " | ".join(f"{k}={v}" for k, v in sorted(stats.items())))
    if samples:
        print(f"   抽样预览(前{len(samples)}条):")
        for s in samples:
            print(f"     [{s['line']}] {s['file']} [{s['cls']}]")
            print(f"         {s['old'][:70]}")
            if s["new"]:
                print(f"       → {s['new'][:70]}")
    return stats


# ---------- 应用 ----------

def _apply_file(path: Path, ledger: list, changed: list, total_limit: int, cls_stats: dict):
    if total_limit is not None and len(changed) >= total_limit:
        return 0
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines(keepends=True)
    hits = 0
    for i, line in enumerate(lines):
        if "#龍芯⚡️" not in line or RE_TMPL.search(line):
            continue
        matches = list(re.finditer(r'#龍芯⚡️([^\s#]+)', line))
        if not matches:
            continue
        new_line = line
        changed_here = 0
        for m in reversed(matches):  # 从后往前替换，索引不位移
            old = m.group(1)
            new, cls = _migrate_dna(old)
            cls_stats.setdefault(cls, 0)
            cls_stats[cls] += 1
            if not new:
                continue
            new_dna = f"#龍芯⚡️{new}"
            if new_dna == m.group(0):
                continue
            ledger.append({"file": str(path), "line": i + 1, "cls": cls,
                           "old": m.group(0), "new": new_dna})
            new_line = new_line[:m.start()] + new_dna + new_line[m.end():]
            changed_here += 1
        if changed_here:
            lines[i] = new_line
            hits += changed_here
    if hits:
        bak = AUDIT_DIR / "backup"
        bak.mkdir(parents=True, exist_ok=True)
        bak_path = bak / f"{path.name}.{datetime.datetime.now():%Y%m%d%H%M%S}.bak"
        shutil.copy2(path, bak_path)
        path.write_text("".join(lines), encoding="utf-8")
        changed.append(str(path))
        print(f"   ✏️ {path}  ({hits} 处)")
    return hits


def cmd_apply(args):
    global AUDIT_DIR
    AUDIT_DIR = REPO / "04_AUDIT" / "dna_migration"
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    ledger = []
    changed = []
    cls_stats = {}
    root = Path(args.dir)
    files = [f for f in root.rglob("*") if f.is_file() and not _skip_path(f)] if root.is_dir() else [root]
    if args.limit:
        files = files[: args.limit]
    for f in files:
        _apply_file(f, ledger, changed, args.limit, cls_stats)
    ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    ledger_path = AUDIT_DIR / f"ledger-{ts}.jsonl"
    with ledger_path.open("w", encoding="utf-8") as fp:
        for rec in ledger:
            fp.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"\n✅ apply 完成: 改动 {len(changed)} 文件 | {len(ledger)} 处 | 台账 {ledger_path}")
    print(f"   分类: " + " | ".join(f"{k}={v}" for k, v in sorted(cls_stats.items())))
    print(f"   原文件备份: {AUDIT_DIR / 'backup'}")


def main():
    ap = argparse.ArgumentParser(description="龍魂 DNA 统一迁移引擎 v2.0")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("scan", help="只读扫描统计")
    sp.add_argument("--dir", default=str(REPO))
    sp.add_argument("--sample", type=int, default=5)
    sp.set_defaults(func=cmd_scan)
    sp = sub.add_parser("apply", help="真改+备份+台账")
    sp.add_argument("--dir", default=str(REPO))
    sp.add_argument("--limit", type=int, default=None)
    sp.add_argument("--force", action="store_true")
    sp.set_defaults(func=cmd_apply)
    args = ap.parse_args()
    if not hasattr(args, "func"):
        ap.print_help()
        return
    args.func(args)


if __name__ == "__main__":
    main()
