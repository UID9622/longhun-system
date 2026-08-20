#!/usr/bin/env python3
"""龍魂 DNA 链验签 v1.0 — chain_hash 一致性校验
DNA: #龍芯⚡️VERIFY-DNA-CHAIN-v1.0
用法: python3 scripts/verify_dna.py [--staged]
规则: 每条 DNA 记录 = {seq, dna, prev_hash, hash}
      hash = sha256(seq | dna | prev_hash)
"""
import hashlib, json, re, sys, subprocess, pathlib

DNA_RE = re.compile(r"#龍芯⚡️[0-9A-Za-z:\-]+")
CHAIN = pathlib.Path("dna_chain.json")
BACKLINK = "uid9622.notion.site-22"


def h(seq, dna, prev):
    return hashlib.sha256(f"{seq}|{dna}|{prev}".encode()).hexdigest()


def verify_chain() -> bool:
    if not CHAIN.exists():
        print("🟡 dna_chain.json 不存在，跳过链校验"); return True
    rec = json.loads(CHAIN.read_text())
    prev = "GENESIS-01F32FFD"
    for r in rec:
        want = h(r["seq"], r["dna"], prev)
        if want != r["hash"]:
            print(f"🔴 LH-FAIL-06 链断裂 @seq={r['seq']}"); return False
        prev = r["hash"]
    print(f"🟢 DNA 链校验通过（{len(rec)} 条）"); return True


def staged_files():
    out = subprocess.run(["git", "diff", "--cached", "--name-only"],
                         capture_output=True, text=True).stdout
    return [f for f in out.split() if f.endswith(".md")]


def verify_md(files) -> bool:
    ok = True
    for f in files:
        p = pathlib.Path(f)
        if not p.exists():
            continue
        t = p.read_text(errors="ignore")
        if not DNA_RE.search(t):
            print(f"🟡 {f} 缺 DNA 追溯码")
        if BACKLINK not in t:
            print(f"🟡 {f} 缺反向链接回公开首页（反向链接铁律）")
        if any(c in t for c in ["\u200b", "\u200c", "\u200d", "\ufeff"]):
            print(f"🔴 {f} 含零宽/隐藏字符（会被判为提示注入）"); ok = False
    return ok


if __name__ == "__main__":
    files = staged_files() if "--staged" in sys.argv else \
        [str(p) for p in pathlib.Path('.').rglob('*.md')]
    sys.exit(0 if (verify_chain() and verify_md(files)) else 1)
