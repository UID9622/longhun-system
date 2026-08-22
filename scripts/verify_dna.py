# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
"""龍魂 DNA 链验签 v1.0 — chain_hash 一致性校验
DNA: #龍芯⚡️丙午·丙申·丙寅·甲午·䷕贲-VERIFY-DNA-CHAIN-v1.0
用法: python3 scripts/verify_dna.py [--staged]
规则: 每条 DNA 记录 = {seq, dna, prev_hash, hash}
      hash = sha256(seq | dna | prev_hash)
License: MulanPSL v2
"""
import hashlib, json, re, sys, subprocess, pathlib

# 支持中文干支四柱/64卦格式: #龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-ZENG-ANCHOR-v1.0 —— 2026-08-22 修误报
DNA_RE = re.compile(r"#龍芯⚡️[^\s]+")
CHAIN = pathlib.Path("dna_chain.json")
BACKLINK = "https://uid9622.notion.site"


def h(seq, dna, prev):
    return hashlib.sha256(f"{seq}|{dna}|{prev}".encode()).hexdigest()


def verify_chain() -> bool:
    if not CHAIN.exists():
        print("🟡 dna_chain.json 不存在，跳过链校验")
        return True
    rec = json.loads(CHAIN.read_text())
    prev = "GENESIS-01F32FFD"
    for r in rec:
        want = h(r["seq"], r["dna"], prev)
        if want != r["hash"]:
            print(f"🔴 LH-FAIL-06 链断裂 @seq={r['seq']}")
            return False
        prev = r["hash"]
    print(f"🟢 DNA 链校验通过（{len(rec)} 条）")
    return True


def staged_files():
    # 2026-08-22: --diff-filter=ACM 排除 D(删除) 文件（clipboard-vault 等已 rm --cached
    #   但工作区仍在的文件不应再检查）；-z 防文件名转义
    out = subprocess.run(["git", "diff", "--cached", "--name-only", "-z", "--diff-filter=ACM"],
                         capture_output=True).stdout
    return [f.decode("utf-8", errors="ignore") for f in out.split(b"\x00")
            if f and f.decode("utf-8", errors="ignore").endswith(".md")]


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
        if any(c in t for c in ["\u200b", "\u200c", "\ufeff", "\u2060"]):
            print(f"🔴 {f} 含零宽/隐藏字符（会被判为提示注入）")
            ok = False
    return ok


if __name__ == "__main__":
    files = staged_files() if "--staged" in sys.argv else \
        [str(p) for p in pathlib.Path('.').rglob('*.md')]
    sys.exit(0 if (verify_chain() and verify_md(files)) else 1)
