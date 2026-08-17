#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·历史DNA全量扫描器 v1.0 —— CB-002 篡改检测 + 四柱重算差异报告
DNA: #龍芯⚡️丙午·丙申·戊午·未时·䷐随-DNA-SCAN-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)  ← 工程实现层
"""

"""
功能：
  scan <目录>   — 全量扫描：提取 DNA 头四柱 vs 文件 mtime 重算四柱（差异报告）
                   + GPG 分离签名校验（.asc 失效 = 真·篡改信号）
  watch <目录>  — cron 模式：对比上次 state，只输出"新出现异常"（避免每小时重复刷屏）

判据分级：
  🔴 GPG 签名失效（有 .asc 但 gpg --verify 失败）         → 硬篡改信号
  🟡 DNA 四柱与 mtime 重算不符                            → 旧算法生成 or 正常修改未更新DNA（推演性）
  🟢 全部通过

返回码：0=全绿 / 1=有新增异常 / 2=有异常但均为旧（无新增）
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# ── 天干地支基表 ──
TIAN_GAN = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
DI_ZHI = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
GAN_RE = "[" + "".join(TIAN_GAN) + "]"
ZHI_RE = "[" + "".join(DI_ZHI) + "]"
# DNA 行里的四柱：丙午·丙申·戊午·戊午（3~4 组干支对）
PILLAR_RE = re.compile(
    GAN_RE + ZHI_RE + r"(?:[·\-]" + GAN_RE + ZHI_RE + r"){2,3}"
)
# 卦象符号（64卦 Unicode U+4DC0~U+4DFF）
GUA_RE = re.compile(r"[\u4dc0-\u4dff]")

# 扫描排除目录（保持低算力）
SKIP_DIRS = {
    ".git", ".codebuddy", "node_modules", "__pycache__", "dist", "build",
    "models", "archive", "_archive", "backups", "_work", "backup",
    "venv", ".venv", "target", "CNSH_加工输出", "CNSH_修复输出", "CNSH_护盾数据",
}
# 扫描文件类型
SCAN_EXTS = {".md", ".py", ".sh", ".json", ".txt", ".conf", ".plist", ".yml", ".yaml", ".service"}

# 密钥指纹（UID9622）
GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def _dna_lines(text: str):
    """提取文件里所有含 DNA 的行"""
    for line in text.splitlines():
        if "龍芯" in line or "龍芯" in line:
            yield line


def extract_pillars(line: str):
    """从 DNA 行提取四柱干支对（年·月·日·[时]），返回列表"""
    m = PILLAR_RE.search(line)
    if not m:
        return []
    raw = m.group(0).replace("-", "·")
    parts = [p for p in raw.split("·") if len(p) == 2 and p[0] in TIAN_GAN and p[1] in DI_ZHI]
    return parts[:4]


def extract_gua(line: str):
    """提取 DNA 行里的卦符"""
    m = GUA_RE.search(line)
    return m.group(0) if m else ""


_GANZHI_FN = None


def _locate_generator():
    """定位 lh_dna_generator.py：本目录 / ../bin ../08_BIN / 鲲鹏 /opt/longhun-system"""
    here = Path(__file__).resolve().parent
    candidates = [
        here,
        here.parent / "bin",
        here.parent / "08_BIN",
        Path("/opt/longhun-system/bin"),
        Path("/opt/longhun-system/08_BIN"),
    ]
    for d in candidates:
        if (d / "lh_dna_generator.py").exists():
            return d
    return None


def recompute_ganzhi(mtime: float):
    """按文件 mtime 用修正后算法重算四柱（import lh_dna_generator，单一真相源）"""
    global _GANZHI_FN
    if _GANZHI_FN is None:
        d = _locate_generator()
        if d is None:
            raise ImportError("lh_dna_generator.py 未找到（bin/ 或 /opt/longhun-system/bin/）")
        sys.path.insert(0, str(d))
        from lh_dna_generator import get_ganzhi
        _GANZHI_FN = get_ganzhi
    return _GANZHI_FN(datetime.fromtimestamp(mtime))


def verify_signature(filepath: str):
    """GPG 分离签名校验：返回 ok / missing / fail"""
    asc = filepath + ".asc"
    if not os.path.exists(asc):
        return "missing"
    r = subprocess.run(
        ["gpg", "--verify", asc, filepath],
        capture_output=True, text=True,
    )
    return "ok" if r.returncode == 0 else "fail"


def file_digest(filepath: str):
    """文件 SHA256 前 12 位（供事件指纹去重用）"""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


def scan_dir(root: str, limit: int = 0):
    """全量扫描"""
    root = Path(root)
    if not root.is_dir():
        raise SystemExit(f"目录不存在: {root}")

    results = {
        "scan_time": datetime.now(timezone.utc).astimezone().isoformat(),
        "root": str(root),
        "total_files": 0,
        "with_dna": 0,
        "stats": {"sig_ok": 0, "sig_missing": 0, "sig_fail": 0, "ganzhi_diff": 0, "gua_diff": 0},
        "signature_failures": [],   # 🔴
        "ganzhi_diffs": [],         # 🟡
        "unsigned_core": [],        # 🟡 含DNA但无签名
        "verdict": "🟢",
    }

    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in SCAN_EXTS:
                continue
            fp = os.path.join(dirpath, fn)
            results["total_files"] += 1
            try:
                with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                    # DNA 头集中在文件前部，.md 多看后 30 行签名区
                    head = f.read(20000)
                    tail = ""
                    if ext == ".md":
                        f.seek(max(0, os.path.getsize(fp) - 8000))
                        tail = f.read(8000)
            except (OSError, UnicodeDecodeError):
                continue
            text = head + "\n" + tail
            if "龍芯" not in text and "龍芯" not in text:
                continue
            results["with_dna"] += 1
            count += 1
            if limit and count > limit:
                break

            # ── DNA 四柱提取 ──
            dna_pillars = []
            dna_gua = ""
            for line in _dna_lines(text):
                ps = extract_pillars(line)
                if ps:
                    dna_pillars = ps  # 取第一个含四柱的
                g = extract_gua(line)
                if g and not dna_gua:
                    dna_gua = g
            if not dna_pillars:
                continue

            # ── mtime 重算四柱 ──
            try:
                mtime = os.path.getmtime(fp)
                gz = recompute_ganzhi(mtime)
                exp = [gz["year"], gz["month"], gz["day"]]
                if len(dna_pillars) >= 4 and gz["hour"]:
                    exp.append(gz["hour"])
            except ImportError:
                raise SystemExit("❌ 找不到 lh_dna_generator.py，请放在 bin/ 或 08_BIN/")

            # ── 四柱差异（年柱算法未变过，主查月柱/日柱）──
            diffs = []
            for i, (dna, e) in enumerate(zip(dna_pillars, exp)):
                if dna != e:
                    diffs.append(f"{['年','月','日','时'][i]}柱{dna}≠{e}")
            if diffs:
                results["ganzhi_diffs"].append({
                    "file": fp,
                    "dna": "·".join(dna_pillars),
                    "expected": "·".join(exp),
                    "diff": " ".join(diffs),
                })
                results["stats"]["ganzhi_diff"] += 1

            # ── GPG 签名 ──
            sig = verify_signature(fp)
            if sig == "fail":
                results["signature_failures"].append({"file": fp, "reason": "gpg verify fail"})
                results["stats"]["sig_fail"] += 1
            elif sig == "missing":
                results["stats"]["sig_missing"] += 1
                results["unsigned_core"].append(fp)
            else:
                results["stats"]["sig_ok"] += 1

        if limit and count > limit:
            break

    # ── 三色判定 ──
    if results["signature_failures"]:
        results["verdict"] = "🔴"
    elif results["ganzhi_diffs"] or results["unsigned_core"]:
        results["verdict"] = "🟡"
    return results


def _fingerprint(rep):
    """异常指纹（用于 watch 去重）"""
    fails = sorted(f["file"] for f in rep["signature_failures"])
    diffs = sorted(d["file"] for d in rep["ganzhi_diffs"])
    return {"sig_fail": fails, "ganzhi_diff": diffs}


def watch(root: str, state_file: str, new_out: str):
    """cron 模式：对比上次 state，输出新增异常"""
    rep = scan_dir(root)
    fp_new = _fingerprint(rep)
    prev = {"sig_fail": [], "ganzhi_diff": []}
    if os.path.exists(state_file):
        try:
            prev = json.loads(open(state_file).read())
        except Exception:
            pass

    new_fail = sorted(set(fp_new["sig_fail"]) - set(prev.get("sig_fail", [])))
    new_diff = sorted(set(fp_new["ganzhi_diff"]) - set(prev.get("ganzhi_diff", [])))

    os.makedirs(os.path.dirname(state_file) or ".", exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(fp_new, f, ensure_ascii=False, indent=2)
    if new_out:
        with open(new_out, "w") as f:
            json.dump({"new_sig_fail": new_fail, "new_ganzhi_diff": new_diff}, f, ensure_ascii=False, indent=2)

    # 控制台
    print(f"🔴 新签名失效: {len(new_fail)}  🟡 新四柱差异: {len(new_diff)}")
    for p in new_fail:
        print(f"   🔴 {p}")
    for p in new_diff:
        print(f"   🟡 {p}")
    if new_fail:
        return 1
    if new_diff:
        return 1
    return 0


def main():
    ap = argparse.ArgumentParser(description="🐉 龍魂·历史DNA全量扫描器 v1.0")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_scan = sub.add_parser("scan", help="全量扫描")
    p_scan.add_argument("root", help="扫描目录")
    p_scan.add_argument("--json", action="store_true", help="JSON输出")
    p_scan.add_argument("--out", help="报告写入路径")
    p_scan.add_argument("--limit", type=int, default=0, help="仅扫描前N个含DNA文件(调试)")
    p_watch = sub.add_parser("watch", help="cron对比模式")
    p_watch.add_argument("root", help="扫描目录")
    p_watch.add_argument("--state", default="state/dna_scan_state.json", help="state文件")
    p_watch.add_argument("--new-out", default="state/dna_new_fail.json", help="新增异常输出")
    args = ap.parse_args()

    if args.cmd == "watch":
        sys.exit(watch(args.root, args.state, args.new_out))

    rep = scan_dir(args.root, args.limit)
    if args.out:
        os.makedirs(os.path.dirname(args.out) or ".", exist_ok=True)
        with open(args.out, "w") as f:
            json.dump(rep, f, ensure_ascii=False, indent=2)
        print(f"📄 报告已写入: {args.out}")
    if args.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return

    # 人类可读报告
    s = rep["stats"]
    print("=" * 62)
    print(f"龍魂·历史DNA扫描报告  时间: {rep['scan_time']}")
    print(f"目录: {rep['root']}")
    print("=" * 62)
    print(f"总扫描文件: {rep['total_files']}  含DNA: {rep['with_dna']}")
    print(f"GPG签名: 有效 {s['sig_ok']} / 缺失 {s['sig_missing']} / 失效 {s['sig_fail']}")
    print(f"四柱差异: {s['ganzhi_diff']}  卦象差异: {s['gua_diff']}")
    print(f"判定: {rep['verdict']}")
    if rep["signature_failures"]:
        print("\n🔴 签名失效（疑似篡改）:")
        for x in rep["signature_failures"][:20]:
            print(f"   {x['file']}  ({x['reason']})")
    if rep["ganzhi_diffs"]:
        print(f"\n🟡 四柱差异（旧算法 or 修改未更新DNA）: 共{len(rep['ganzhi_diffs'])}")
        for x in rep["ganzhi_diffs"][:20]:
            print(f"   {x['file']}\n      DNA={x['dna']}  期望={x['expected']}  [{x['diff']}]")
    if len(rep["ganzhi_diffs"]) > 20:
        print(f"   ... 其余 {len(rep['ganzhi_diffs'])-20} 条见完整报告")
    print("=" * 62)


if __name__ == "__main__":
    main()
