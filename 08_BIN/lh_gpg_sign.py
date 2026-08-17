#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""
龍魂·GPG自动签名引擎 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·酉时·☰乾-GPG-AUTO-SIGN-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

自动对指定目录/文件进行GPG分离签名。
- 签名模式: --local-user A2D0092CEE2E5BA87035600924C3704A8CC26D5F
- 输出: .asc分离签名文件
- 已签名文件跳过（除非 --force）
"""
import subprocess
import sys
import os
import json
from pathlib import Path
from datetime import datetime
import argparse

GPG_KEY = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
GP = ["gpg", "--local-user", GPG_KEY, "--armor", "--detach-sign", "--batch", "--yes", "--no-tty"]


SIGNING_LOG = Path(__file__).resolve().parent.parent / "state" / "signing_chain" / "signing_log.jsonl"


def _append_signing_log(filepath: str) -> None:
    """签名成功后追加签章链日志（供 lh_threshold_trigger.py signing 守卫审计）"""
    try:
        SIGNING_LOG.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "trigger_time_iso": datetime.now().astimezone().isoformat(),
            "trigger_time": "auto",
            "file": filepath,
            "gpg_verified": True,
            "action_type": "gpg_sign",
            "guard": "signing",
        }
        with open(SIGNING_LOG, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    except Exception:
        pass  # 日志写入失败不阻断签名


def sign_file(filepath: str, force: bool = False) -> dict:
    asc = filepath + ".asc"
    if os.path.exists(asc) and not force:
        return {"file": filepath, "status": "skip", "reason": "already signed"}
    r = subprocess.run(GP + ["-o", asc, filepath], capture_output=True, text=True)
    if r.returncode == 0:
        _append_signing_log(filepath)
        return {"file": filepath, "status": "ok"}
    else:
        return {"file": filepath, "status": "fail", "error": r.stderr.strip()[:200]}


def verify_file(filepath: str) -> dict:
    asc = filepath + ".asc"
    if not os.path.exists(asc):
        return {"file": filepath, "status": "missing_asc"}
    r = subprocess.run(
        ["gpg", "--verify", asc, filepath], capture_output=True, text=True
    )
    ok = ("Good signature" in r.stderr or "Good signature" in r.stdout or
          "完好的签名" in r.stderr or "完好的签名" in r.stdout)
    return {"file": filepath, "status": "verified" if ok else "bad_sig", "output": r.stderr.strip()}


def find_unsigned(directory: str, patterns=None) -> list:
    # 修正 (P77 黑天使审计 2026-08-14): 补部署配置类型 .conf/.service/.html/.txt 及无扩展名 LICENSE-*,
    #   否则 nginx/systemd/LICENSE 等核心配置永远签不上 (GATE-11 签名闸形同虚设)
    if patterns is None:
        patterns = ["*.md", "*.py", "*.sh", "*.json", "*.yaml", "*.toml", "*.dart", "*.ets", "*.ts", "*.yml",
                    "*.conf", "*.service", "*.html", "*.txt", "*.ini", "LICENSE-*", "*.example", "*.env"]
    # 构建产物/依赖目录排除 (防误签)
    EXCLUDE_DIRS = ("__pycache__", "node_modules", "venv", ".venv", "dist", "build",
                    "site-packages", ".git", ".idea", ".DS_Store")
    unsigned = []
    for p in patterns:
        for f in Path(directory).rglob(p):
            fstr = str(f)
            if ".asc" in fstr or "__pycache__" in fstr or "node_modules" in fstr:
                continue
            if any(seg in EXCLUDE_DIRS for seg in Path(fstr).parts):
                continue
            if not os.path.exists(fstr + ".asc"):
                unsigned.append(fstr)
    return sorted(unsigned)


def scan_report(paths: list) -> dict:
    """扫描目录返回签名统计"""
    total, signed, unsigned = 0, 0, 0
    unsigned_list = []
    for p in paths:
        if os.path.isfile(p):
            if p.endswith(".asc"):
                continue
            total += 1
            if os.path.exists(p + ".asc"):
                signed += 1
            else:
                unsigned += 1
                unsigned_list.append(p)
        elif os.path.isdir(p):
            for f in find_unsigned(p):
                total += 1
                unsigned += 1
                unsigned_list.append(f)
    return {"total": total, "signed": signed, "unsigned": unsigned, "unsigned_list": unsigned_list}


def main():
    parser = argparse.ArgumentParser(description="龍魂GPG自动签名引擎")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # sign
    p_sign = sub.add_parser("sign", help="签名文件")
    p_sign.add_argument("paths", nargs="+", help="文件或目录路径")
    p_sign.add_argument("--force", action="store_true", help="强制重签（覆盖已有签名）")
    p_sign.add_argument("--dry-run", action="store_true", help="仅预览不执行")

    # verify
    p_verify = sub.add_parser("verify", help="验证签名")
    p_verify.add_argument("paths", nargs="+", help="文件或目录路径")

    # scan
    p_scan = sub.add_parser("scan", help="扫描未签名文件")
    p_scan.add_argument("paths", nargs="+", help="目录路径")
    p_scan.add_argument("--json", action="store_true", help="JSON输出")

    args = parser.parse_args()

    if args.cmd == "sign":
        from pathlib import Path
        all_files = []
        for p in args.paths:
            pp = Path(p)
            if pp.is_file() and not p.endswith(".asc"):
                all_files.append(p)
            elif pp.is_dir():
                all_files.extend(find_unsigned(p))

        if args.dry_run:
            print(f"[DRY-RUN] 将签名 {len(all_files)} 个文件:")
            for f in all_files:
                print(f"  {f}")
            return

        results = []
        for f in all_files:
            r = sign_file(f, args.force)
            results.append(r)
            status_icon = {"ok": "✅", "skip": "⏭️", "fail": "❌"}.get(r["status"], "?")
            print(f"{status_icon} {r['file']}")

        ok = sum(1 for r in results if r["status"] == "ok")
        skip = sum(1 for r in results if r["status"] == "skip")
        fail = sum(1 for r in results if r["status"] == "fail")
        print(f"\n签名: ✅{ok} ⏭️{skip} ❌{fail}")
        if fail > 0:
            sys.exit(1)

    elif args.cmd == "verify":
        for p in args.paths:
            r = verify_file(p)
            icon = {"verified": "✅", "missing_asc": "🔴", "bad_sig": "🔴"}.get(r["status"], "?")
            print(f"{icon} {r['file']}")

    elif args.cmd == "scan":
        report = scan_report(args.paths)
        if args.json:
            import json
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(f"总计: {report['total']} | 已签: {report['signed']} | 未签: {report['unsigned']}")
            if report['unsigned'] > 0:
                print(f"\n未签名文件 ({report['unsigned']}):")
                for f in report['unsigned_list']:
                    print(f"  🔴 {f}")


if __name__ == "__main__":
    main()
