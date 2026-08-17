#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂系统 · DNA 追溯码权威生成器
DNA格式（现行规范 v2.0，2026-07-19基线扩展）:
    #龍芯⚡️{年干支}·{月干支}·{日干支}·{时辰}·{卦符卦名}-{动作标签}-{版本}-{日序号}-{哈希8}
铁律:
    1. 干支四柱与卦名一律以本脚本输出为准，禁止手写。
    2. 旧格式DNA冻结不改写（P0：不删除只冻结）。
    3. 每个DNA全局唯一：日序号(持久化) + 内容哈希8位 双锚定。
    4. 注册表统一归类，支持 recover 凭DNA恢复全文。
归属: 龍魂系统 · UID9622 · 诸葛鑫·龍芯北辰
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""

import argparse
import datetime
import gzip
import hashlib
import json
import os
import random
import string
import sys

TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
SHENG_XIAO = ["鼠", "牛", "虎", "兔", "龍", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]

MONTH_DI_ZHI = {
    1: "寅", 2: "卯", 3: "辰", 4: "巳", 5: "午", 6: "未",
    7: "申", 8: "酉", 9: "戌", 10: "亥", 11: "子", 12: "丑",
}

WU_HU_DUN = {
    "甲": "丙", "乙": "戊", "丙": "庚", "丁": "壬", "戊": "甲",
    "己": "丙", "庚": "戊", "辛": "庚", "壬": "壬", "癸": "甲",
}

HEXAGRAM_NAMES = [
    "乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
    "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
    "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
    "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
    "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
    "损", "益", "夬", "姤", "萃", "升", "困", "井",
    "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
    "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济",
]

CATEGORIES = ["protocol", "script", "doc", "paper", "asset", "log", "intel", "other"]

MASTER_UID = "9622"
CONFIRM_PREFIX = "#CONFIRM🌌9622-ONLY-ONCE🧬"


def _jdn(y, m, d):
    """公历日期 -> 儒略日数 (JDN)"""
    a = (14 - m) // 12
    y2 = y + 4800 - a
    m2 = m + 12 * a - 3
    return d + (153 * m2 + 2) // 5 + 365 * y2 + y2 // 4 - y2 // 100 + y2 // 400 - 32045


def year_ganzhi(year):
    """年柱（立春近似=公历年）"""
    return TIAN_GAN[(year - 4) % 10] + DI_ZHI[(year - 4) % 12]


def month_ganzhi(year, month):
    """月柱：五虎遁，正月建寅"""
    yg = TIAN_GAN[(year - 4) % 10]
    first_idx = TIAN_GAN.index(WU_HU_DUN[yg])
    return TIAN_GAN[(first_idx + month - 1) % 10] + MONTH_DI_ZHI[month]


def day_ganzhi(date):
    """日柱：idx = (JDN + 49) % 60，锚点 2000-01-01 = 戊午(54)"""
    idx = (_jdn(date.year, date.month, date.day) + 49) % 60
    return TIAN_GAN[idx % 10] + DI_ZHI[idx % 12]


def shichen(hour):
    """时辰地支：23:00-00:59 为子时"""
    return DI_ZHI[((hour + 1) // 2) % 12] + "时"


def ganzhi_full(dt):
    return {
        "year": year_ganzhi(dt.year),
        "month": month_ganzhi(dt.year, dt.month),
        "day": day_ganzhi(dt.date()),
        "hour": shichen(dt.hour),
        "shengxiao": SHENG_XIAO[(dt.year - 4) % 12],
        "iso": dt.isoformat(timespec="seconds"),
    }


def _hash_hex(payload):
    """国密SM3优先，不可用回退SHA256"""
    data = payload.encode("utf-8")
    try:
        h = hashlib.new("sm3")
        h.update(data)
        return h.hexdigest()
    except (ValueError, TypeError):
        return hashlib.sha256(data).hexdigest()


def hexagram(hash_hex):
    """hash首字节 % 64 -> ䷀乾 … ䷿未济（确定性可复现）"""
    idx = int(hash_hex[:2], 16) % 64
    return chr(0x4DC0 + idx) + HEXAGRAM_NAMES[idx]


# ============================================================
# 注册表（统一归类 / 拓展 / 压缩 / 恢复）
# ============================================================

def _default_registry_dir():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "registry")


def _registry_path(rdir):
    return os.path.join(rdir, "dna_registry.json")


def _counter_path(rdir):
    return os.path.join(rdir, "counter.json")


def _load_json(path, default):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return default


def _save_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)  # 原子写入，防中断损坏


def _next_seq(rdir, day_key):
    """当日单调递增序号（持久化，机器级不重复）"""
    cpath = _counter_path(rdir)
    counter = _load_json(cpath, {})
    day = counter.get(day_key, {"seq": 0})
    day["seq"] += 1
    counter[day_key] = day
    _save_json(cpath, counter)
    return day["seq"]


def _confirm_code():
    rand = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return CONFIRM_PREFIX + rand


# ============================================================
# 核心命令
# ============================================================

def cmd_generate(args, rdir):
    dt = args.dt
    gz = ganzhi_full(dt)
    day_key = dt.date().isoformat()
    seq = _next_seq(rdir, day_key)

    payload = "{}|{}|{}|{}|{:04d}".format(args.title, args.action, args.version, gz["iso"], seq)
    hfull = _hash_hex(payload)
    h8 = hfull[:8]
    gua = hexagram(hfull)

    dna = "#龍芯⚡️{}·{}·{}·{}·{}-{}-{}-{:04d}-{}".format(
        gz["year"], gz["month"], gz["day"], gz["hour"], gua,
        args.action, args.version, seq, h8)

    sha256 = ""
    if args.file and os.path.exists(args.file):
        sha256 = hashlib.sha256(open(args.file, "rb").read()).hexdigest()

    entry = {
        "dna": dna,
        "title": args.title,
        "action": args.action,
        "version": args.version,
        "category": args.category,
        "file_path": os.path.abspath(args.file) if args.file else "",
        "sha256": sha256,
        "created_iso": gz["iso"],
        "ganzhi": gz,
        "confirm_code": _confirm_code(),
        "uid": MASTER_UID,
    }
    reg = _load_json(_registry_path(rdir), {})
    if dna in reg:  # 理论不可能（序号唯一），防御性检查
        print("❌ DNA冲突（不应发生），请检查counter.json", file=sys.stderr)
        return 2
    reg[dna] = entry
    _save_json(_registry_path(rdir), reg)

    print(dna)
    print(entry["confirm_code"])
    return 0


def cmd_verify(args, rdir):
    reg = _load_json(_registry_path(rdir), {})
    e = reg.get(args.dna)
    if not e:
        print("❌ 未注册: " + args.dna)
        return 1
    print("✅ 已注册 | {} | {} | {}".format(e["title"], e["category"], e["created_iso"]))
    if e.get("file_path") and os.path.exists(e["file_path"]):
        now = hashlib.sha256(open(e["file_path"], "rb").read()).hexdigest()
        print("   文件完整性: " + ("✅ 一致" if now == e["sha256"] else "⚠️ 文件已变更"))
    return 0


def cmd_recover(args, rdir):
    reg = _load_json(_registry_path(rdir), {})
    e = reg.get(args.dna)
    if not e:
        print("❌ 未注册: " + args.dna)
        return 1
    print(json.dumps(e, ensure_ascii=False, indent=2))
    fp = e.get("file_path", "")
    if fp and os.path.exists(fp):
        print("\n===== 全文恢复 =====")
        with open(fp, "r", encoding="utf-8", errors="replace") as f:
            print(f.read())
    elif fp:
        print("\n⚠️ 原文件不在本机: " + fp)
    return 0


def cmd_register(args, rdir):
    """把已有文件/旧DNA登记进注册表（旧DNA冻结不改写，仅登记）"""
    reg = _load_json(_registry_path(rdir), {})
    if args.dna in reg:
        print("⚠️ 已存在: " + args.dna)
        return 0
    sha256 = ""
    if args.file and os.path.exists(args.file):
        sha256 = hashlib.sha256(open(args.file, "rb").read()).hexdigest()
    reg[args.dna] = {
        "dna": args.dna,
        "title": args.title,
        "action": "",
        "version": "",
        "category": args.category,
        "file_path": os.path.abspath(args.file) if args.file else "",
        "sha256": sha256,
        "created_iso": datetime.datetime.now().isoformat(timespec="seconds"),
        "ganzhi": ganzhi_full(datetime.datetime.now()),
        "confirm_code": "",
        "uid": MASTER_UID,
        "legacy": True,
    }
    _save_json(_registry_path(rdir), reg)
    print("✅ 已登记(legacy): " + args.dna)
    return 0


def cmd_list(args, rdir):
    reg = _load_json(_registry_path(rdir), {})
    items = list(reg.values())
    if args.category:
        items = [e for e in items if e.get("category") == args.category]
    for e in sorted(items, key=lambda x: x.get("created_iso", "")):
        print("{}  |  {}  |  {}".format(e["dna"], e["title"], e.get("category", "")))
    print("\n共 {} 条".format(len(items)))
    return 0


def cmd_compress(args, rdir):
    """注册表快照 gzip 归档（压缩存储）"""
    rpath = _registry_path(rdir)
    if not os.path.exists(rpath):
        print("❌ 注册表为空")
        return 1
    ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
    adir = os.path.join(rdir, "archive")
    os.makedirs(adir, exist_ok=True)
    out = os.path.join(adir, "dna_registry_{}.json.gz".format(ts))
    with open(rpath, "rb") as fi, gzip.open(out, "wb") as fo:
        fo.write(fi.read())
    print("✅ 已归档: " + out)
    return 0


def cmd_ganzhi(args, rdir):
    gz = ganzhi_full(args.dt)
    print("📅 " + gz["iso"])
    print("   年柱: {}年 ({}年)".format(gz["year"], gz["shengxiao"]))
    print("   月柱: {}月".format(gz["month"]))
    print("   日柱: {}日".format(gz["day"]))
    print("   时辰: " + gz["hour"])
    return 0


# ============================================================
# CLI
# ============================================================

def _parse_dt(s):
    if "T" in s:
        return datetime.datetime.fromisoformat(s)
    return datetime.datetime.fromisoformat(s + "T12:00:00")


def main():
    ap = argparse.ArgumentParser(
        description="龍魂系统 · DNA追溯码权威生成器（干支四柱+时辰+卦名+唯一双锚）")
    ap.add_argument("--registry", default=_default_registry_dir(), help="注册表目录")
    sub = ap.add_subparsers(dest="cmd", required=True)

    def _common(p):
        p.add_argument("--date", default=None,
                       help="YYYY-MM-DD 或 YYYY-MM-DDTHH:MM，默认=现在")

    p = sub.add_parser("generate", help="生成新DNA并注册")
    p.add_argument("--title", required=True)
    p.add_argument("--action", required=True, help="动作标签，如 AUDIT-REPORT")
    p.add_argument("--version", default="v1.0")
    p.add_argument("--category", default="other", choices=CATEGORIES)
    p.add_argument("--file", default=None)
    _common(p)

    p = sub.add_parser("verify", help="校验DNA是否注册")
    p.add_argument("--dna", required=True)

    p = sub.add_parser("recover", help="凭DNA恢复元数据与全文")
    p.add_argument("--dna", required=True)

    p = sub.add_parser("register", help="登记已有文件/旧DNA（冻结不改写）")
    p.add_argument("--dna", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--category", default="other", choices=CATEGORIES)
    p.add_argument("--file", default=None)

    p = sub.add_parser("list", help="列出注册表")
    p.add_argument("--category", default=None, choices=CATEGORIES)

    sub.add_parser("compress", help="注册表gzip归档")

    p = sub.add_parser("ganzhi", help="仅查询干支四柱")
    _common(p)

    args = ap.parse_args()
    rdir = os.path.abspath(args.registry)
    os.makedirs(rdir, exist_ok=True)
    args.dt = _parse_dt(args.date) if getattr(args, "date", None) else datetime.datetime.now()

    return {
        "generate": cmd_generate,
        "verify": cmd_verify,
        "recover": cmd_recover,
        "register": cmd_register,
        "list": cmd_list,
        "compress": cmd_compress,
        "ganzhi": cmd_ganzhi,
    }[args.cmd](args, rdir)


if __name__ == "__main__":
    sys.exit(main())
