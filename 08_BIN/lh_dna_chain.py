#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂·DNA接龍链引擎 v1.0
只追加·不覆盖·不删除·焊死铁律
每个AI/人格的每次修改都接在链尾·行为密码学指纹嵌入每节

DNA: #龍芯⚡️丙午·丙申·癸丑·戌时·䷒临-DNA-CHAIN-ENGINE-v1.0-INIT
创建者: 诸葛鑫（UID9622）
协议: MulanPSL v2（工程实现层）
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
"""
import json, os, re, sys, hashlib, subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
VALID_ACTIONS = ["创建","修改","审计","签章","归档","部署","修复","优化","审查","验证","翻译","重构","回滚"]

# ═══════════════════════════════════════
# 格式映射
# ═══════════════════════════════════════
FORMAT_MAP = {
    ".py": "python", ".pyi": "python", ".pyx": "python",
    ".md": "markdown", ".html": "html", ".htm": "html",
    ".js": "jsdoc", ".ts": "jsdoc", ".jsx": "jsdoc", ".tsx": "jsdoc", ".mjs": "jsdoc",
    ".sh": "shell", ".bash": "shell", ".zsh": "shell",
    ".yaml": "yaml", ".yml": "yaml",
    ".json": "json", ".toml": "toml",
    ".css": "css", ".scss": "css", ".less": "css",
    ".rs": "rust_c", ".go": "rust_c", ".java": "rust_c",
    ".c": "rust_c", ".cpp": "rust_c", ".cc": "rust_c", ".h": "rust_c", ".hpp": "rust_c",
    ".xml": "xml", ".svg": "xml",
}

def get_file_format(filepath: str) -> str:
    fp = filepath.lower()
    base = os.path.basename(fp).upper()
    if base in ("DOCKERFILE", "MAKEFILE", "VAGRANTFILE"):
        return "shell"
    return FORMAT_MAP.get(os.path.splitext(fp)[1], "shell")

# ═══════════════════════════════════════
# 嵌入器：每种格式的注释方式
# ═══════════════════════════════════════
EMBED = {
    # (comment_prefix,  block_start,  block_end,  is_multiline)
    "python":    ("# ",  "\n# ⛓️ 龍魂DNA接龍链 " + "─"*30 + "\n",
                        "\n# ⛓️ 龍魂DNA接龍末端 " + "─"*30 + "\n", True),
    "markdown":  ("",    "\n<!-- ⛓️DNA-CHAIN\n",
                        "\n⛓️END-->\n", True),
    "html":      ("",    "\n<!-- ⛓️DNA-CHAIN\n",
                        "\n⛓️END-->\n", True),
    "jsdoc":     (" * ", "\n/**\n * ⛓️ 龍魂DNA接龍链\n",
                        "\n * ⛓️END\n */\n", True),
    "shell":     ("# ⛓️ ", "", "", False),
    "yaml":      ("#   - ", "\n# ⛓️DNA-CHAIN\n",
                        "\n# ⛓️END\n", True),
    "json":      ("  ",  '\n"_dna_chain": [\n',
                        "\n]\n", True),
    "toml":      ("# ",  "\n# ⛓️DNA-CHAIN\n",
                        "\n# ⛓️END\n", True),
    "css":       ("",    "\n/* ⛓️DNA-CHAIN\n",
                        "\n⛓️END*/\n", True),
    "rust_c":    ("// ⛓️ ", "", "", False),
    "xml":       ("",    "\n<!-- ⛓️DNA-CHAIN\n",
                        "\n⛓️END-->\n", True),
}


def sha8(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:8]


def get_compact_ts() -> str:
    """获取紧凑干支时间戳: 丙午·丙申·癸丑·戌时·䷒临"""
    try:
        r = subprocess.run([sys.executable, str(PROJECT_ROOT/"bin"/"lh_time_engine.py"), "--stamp"],
                          capture_output=True, text=True, timeout=5)
        line = r.stdout.strip()
        # 从完整行提取: [丙午·丙申·癸丑·戌时·䷒临·🟢] 2026-08-07T20:40:02+08:00
        m = re.search(r'\[(.+?·[🟢🟡🔴])\]', line)
        if m:
            # 去掉三色标记: 丙午·丙申·癸丑·戌时·䷒临·🟢 → 丙午·丙申·癸丑·戌时·䷒临
            return m.group(1).rsplit("·", 1)[0]
        # 降级尝试
        m2 = re.match(r'([\u4e00-\u9fff]+·[\u4e00-\u9fff]+·[\u4e00-\u9fff]+·[\u4e00-\u9fff]+·[\u4dc0-\u4dff\u2630-\u2637]+)', line)
        if m2:
            return m2.group(1)
    except:
        pass
    return f"丙午·{datetime.now().month:02d}月{datetime.now().day:02d}日·亥时"


def get_bhash(filepath: str, persona: str, action: str) -> str:
    """行为密码学指纹 bhash"""
    try:
        sys.path.insert(0, str(PROJECT_ROOT/"04_ENGINES"/"behavioral_crypto"))
        from seven_factor_model import SevenFactorModel
        model = SevenFactorModel()
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        factors = model.extract_all(content)
        data = json.dumps({k: round(v,6) for k,v in factors.items()}, sort_keys=True)
        return sha8(data)
    except:
        with open(filepath, "r", encoding="utf-8") as f:
            snippet = f.read(1024)
        return sha8(f"{get_compact_ts()}|{persona}|{action}|{snippet}")


def get_chash(filepath: str) -> str:
    """当前文件内容哈希（移除已有DNA链后）"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        content_clean = _strip_chain(content)
        return sha8(content_clean)
    except:
        return "00000000"


def _strip_chain(text: str) -> str:
    """移除所有DNA链标记"""
    # 移除各种格式的DNA链
    patterns = [
        r'# ⛓️ 龍魂DNA接龍链 .*?# ⛓️ 龍魂DNA接龍末端[^\n]*\n?',
        r'<!-- ⛓️DNA-CHAIN.*?⛓️END-->\n?',
        r'/\*\*\n \* ⛓️ 龍魂DNA接龍链.*?\* ⛓️END\n \*/\n?',
        r'/\* ⛓️DNA-CHAIN.*?⛓️END\*/\n?',
        r'"_dna_chain":\s*\[[^\]]*\],?\n?',
        r'# ⛓️DNA-CHAIN\n.*?# ⛓️END\n?',
        r'^[#\s/]*⛓️\s*DNA:V\d+.*$',
        r'^[#\s/]*_dna_chain.*$',
    ]
    for p in patterns:
        text = re.sub(p, '', text, flags=re.MULTILINE | re.DOTALL)
    return text


def parse_chain(filepath: str) -> list[dict]:
    """解析文件中的已有DNA链条目"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except:
        return []
    
    entries = []
    pattern = r'DNA:V(\d+)\|([^|]+)\|([^|]+)\|([^|]+)\|([^|]*?)\|bhash:([a-f0-9]{8})\|chash:([a-f0-9]{8})\|←([A-Za-z0-9]+)'
    
    for m in re.finditer(pattern, content):
        entries.append(dict(
            V=int(m.group(1)), ts=m.group(2).strip(), persona=m.group(3).strip(),
            action=m.group(4).strip(), note=m.group(5).strip(),
            bhash=m.group(6), chash=m.group(7), prev=m.group(8),
        ))
    return sorted(entries, key=lambda e: e["V"])


def _build_dna_line(version: int, ts: str, persona: str, action: str, note: str,
                    bhash: str, chash: str, prev: str, fmt: str) -> str:
    """根据格式组装一行DNA"""
    prefix, _, _, is_multiline = EMBED.get(fmt, EMBED["shell"])
    dna = f"DNA:V{version}|{ts}|{persona}|{action}|{note}|bhash:{bhash}|chash:{chash}|←{prev}"
    
    if fmt == "json":
        # JSON 数组元素必须是合法 JSON 字符串（带引号），否则整个 JSON 文件会被破坏
        return f'{prefix}"{dna}"'
    if is_multiline:
        return f"{prefix}{dna}"
    else:
        # 单行格式直接用prefix+DNA
        return f"{prefix}{dna}"


def append_chain(filepath: str, persona: str = "P04鲁班", action: str = "修改", note: str = "") -> dict:
    """追加DNA链接到文件（只追加·不覆盖）"""
    if not os.path.exists(filepath):
        return {"success": False, "error": f"文件不存在: {filepath}"}
    if action not in VALID_ACTIONS:
        return {"success": False, "error": f"非法动作: {action}, 合法={VALID_ACTIONS}"}
    
    fmt = get_file_format(filepath)
    if fmt not in EMBED:
        return {"success": False, "error": f"不支持格式: {fmt}"}
    
    existing = parse_chain(filepath)
    version = len(existing) + 1
    prev_chash = existing[-1]["chash"] if existing else "GENESIS"
    
    ts = get_compact_ts()
    bhash_val = get_bhash(filepath, persona, action)
    chash_val = get_chash(filepath)
    
    dna_line = _build_dna_line(version, ts, persona, action, note, bhash_val, chash_val, prev_chash, fmt)

    if fmt == "json":
        # JSON 安全模式：解析→更新 _dna_chain key→写回，保证文件永远是合法 JSON
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return {"success": False, "error": f"JSON 解析失败: {e}"}
        if not isinstance(data, dict):
            return {"success": False, "error": "JSON 根必须是对象"}
        chain = data.get("_dna_chain")
        if not isinstance(chain, list):
            chain = []
        # dna_line 形如 `  "DNA:V1|..."`，转为纯字符串入数组
        entry = dna_line.strip().strip('"')
        chain.append(entry)
        data["_dna_chain"] = chain
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
        except Exception as e:
            return {"success": False, "error": f"写入失败: {e}"}
        return {
            "success": True, "version": version, "filepath": filepath,
            "persona": persona, "action": action, "note": note,
            "bhash": bhash_val, "chash": chash_val, "prev": prev_chash,
        }

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return {"success": False, "error": f"读取失败: {e}"}
    
    _, block_start, block_end, is_multiline = EMBED.get(fmt, EMBED["shell"])
    
    if existing and is_multiline:
        # 已有链（块模式）：在 block_end 前插入新行
        if block_end.strip() in content:
            insert_line = f"{dna_line}\n{block_end.strip()}"
            # 只替换最后的block_end出现
            last_idx = content.rfind(block_end.strip())
            if last_idx >= 0:
                content = content[:last_idx] + insert_line + content[last_idx + len(block_end.strip()):]
            else:
                content += f"\n{dna_line}\n"
        else:
            content += f"\n{dna_line}\n"
    elif existing and not is_multiline:
        # 已有链（单行模式）：直接追加
        content += f"\n{dna_line}\n"
    elif not existing and is_multiline:
        # 首次（块模式）：创建完整块
        content += f"{block_start}{dna_line}{block_end}"
    else:
        # 首次（单行模式）
        content += f"\n{dna_line}\n"
    
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return {"success": False, "error": f"写入失败: {e}"}
    
    return {
        "success": True, "version": version, "filepath": filepath,
        "persona": persona, "action": action, "note": note,
        "bhash": bhash_val, "chash": chash_val, "prev": prev_chash,
    }


def verify_chain(filepath: str) -> dict:
    entries = parse_chain(filepath)
    if not entries:
        return {"has_chain": False, "status": "🟡", "message": "无DNA接龍链"}
    
    issues = []
    current_chash = get_chash(filepath)
    
    for i, e in enumerate(entries):
        if i == 0 and e["prev"] != "GENESIS":
            issues.append(f"V{e['V']}: 首节prev≠GENESIS")
        elif i > 0 and e["prev"] != entries[i-1]["chash"]:
            issues.append(f"V{e['V']}: 🔴断链 prev={e['prev']} 期望={entries[i-1]['chash']}")
    
    if entries[-1]["chash"] != current_chash:
        issues.append(f"V{entries[-1]['V']}: 🟡内容变更 ({entries[-1]['chash']}→{current_chash})")
    
    if issues:
        return {"has_chain": True, "status": "🔴" if any("🔴" in i for i in issues) else "🟡",
                "message": "\n".join(issues), "entries_count": len(entries), "latest_v": len(entries)}
    return {"has_chain": True, "status": "🟢",
            "message": f"DNA链完整·{len(entries)}版本·全通", "entries_count": len(entries), "latest_v": len(entries)}


def show_chain(filepath: str) -> dict:
    entries = parse_chain(filepath)
    if not entries:
        return {"has_chain": False, "message": "无DNA接龍链"}
    return {
        "has_chain": True, "filepath": filepath, "total_versions": len(entries),
        "personas": sorted(set(e["persona"] for e in entries)),
        "actions": sorted(set(e["action"] for e in entries)),
        "entries": entries,
    }


def init_chain(filepath: str, persona: str = "P04鲁班", note: str = "初始创建") -> dict:
    if os.path.exists(filepath) and parse_chain(filepath):
        return {"success": False, "error": "文件已有DNA链，请用 append"}
    return append_chain(filepath, persona, "创建", note)


def scan_directory(directory: str) -> dict:
    results = {"with_chain": [], "without_chain": [], "broken": []}
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in ("__pycache__",".git",".venv","venv","node_modules",".codebuddy","dist","_private")]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            base = os.path.basename(file).upper()
            if ext not in FORMAT_MAP and base not in ("DOCKERFILE","MAKEFILE"):
                continue
            fp = os.path.join(root, file)
            entries = parse_chain(fp)
            if entries:
                vr = verify_chain(fp)
                if vr["status"] == "🔴":
                    results["broken"].append(fp)
                else:
                    results["with_chain"].append(fp)
            else:
                results["without_chain"].append(fp)
    return results


def auto_append(filepath: str, note: str = "自动检测变更") -> Optional[dict]:
    if not os.path.exists(filepath):
        return None
    entries = parse_chain(filepath)
    if not entries:
        return init_chain(filepath, note=note)
    latest = entries[-1]
    current = get_chash(filepath)
    if latest["chash"] == current:
        return None
    return append_chain(filepath, note=note)


# ═══════════════════════════════════════
# CLI
# ═══════════════════════════════════════
def main():
    import argparse
    p = argparse.ArgumentParser(description="龍魂·DNA接龍链引擎 v1.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="只追加·不覆盖·不删除\n例: lh dna-chain init main.py\n    lh dna-chain append main.py -p P05 -a 审计 -n \"五问通过\"\n    lh dna-chain verify main.py\n    lh dna-chain show main.py\n    lh dna-chain scan bin/")
    
    sp = p.add_subparsers(dest="cmd")
    
    pi = sp.add_parser("init"); pi.add_argument("file"); pi.add_argument("--persona","-p",default="P04鲁班"); pi.add_argument("--note","-n",default="初始创建")
    pa = sp.add_parser("append"); pa.add_argument("file"); pa.add_argument("--persona","-p",default="P04鲁班"); pa.add_argument("--action","-a",default="修改"); pa.add_argument("--note","-n",required=True)
    pv = sp.add_parser("verify"); pv.add_argument("file"); pv.add_argument("--json","-j",action="store_true")
    ps = sp.add_parser("show"); ps.add_argument("file"); ps.add_argument("--json","-j",action="store_true")
    psc = sp.add_parser("scan"); psc.add_argument("directory",nargs="?",default=".")
    pau = sp.add_parser("auto"); pau.add_argument("path"); pau.add_argument("--note","-n",default="自动检测变更"); pau.add_argument("--persona","-p",default="P04鲁班")
    
    args = p.parse_args()
    if not args.cmd: p.print_help(); return
    
    if args.cmd == "init":
        r = init_chain(args.file, args.persona, args.note); print(f"⛓️ V1 → {args.file}" if r["success"] else f"❌ {r['error']}")
    elif args.cmd == "append":
        r = append_chain(args.file, args.persona, args.action, args.note)
        if r["success"]:
            print(f"⛓️ V{r['version']} → {args.file}\n   人格:{r['persona']} 动作:{r['action']}\n   说明:{r['note']}\n   bhash:{r['bhash']} chash:{r['chash']}")
        else:
            print(f"❌ {r['error']}")
    elif args.cmd == "verify":
        r = verify_chain(args.file)
        if args.json: print(json.dumps(r,ensure_ascii=False,indent=2))
        else:
            s = r.get("status","🟡"); print(f"{s} {r['message']}")
            if r.get("entries_count"): print(f"   版本:{r['entries_count']}")
    elif args.cmd == "show":
        r = show_chain(args.file)
        if args.json: print(json.dumps(r,ensure_ascii=False,indent=2))
        elif r["has_chain"]:
            print(f"⛓️ {r['filepath']}\n   版本:{r['total_versions']} 人格:{', '.join(r['personas'])}\n   {'─'*60}")
            for e in r["entries"]:
                print(f"   V{e['V']:2d}|{e['ts'][:18]:18s}|{e['persona']:12s}|{e['action']:4s}|{e['note'][:28]:28s}|←{e['prev']}")
        else:
            print(f"🟡 {r['message']}")
    elif args.cmd == "scan":
        r = scan_directory(args.directory)
        t = len(r["with_chain"])+len(r["without_chain"])+len(r["broken"])
        print(f"🔍 {args.directory}\n   有链:{len(r['with_chain'])} 无链:{len(r['without_chain'])} 断链:{len(r['broken'])}🔴 总计:{t}")
        if r["broken"]:
            print("   🔴断链:"); [print(f"      {f}") for f in r["broken"]]
    elif args.cmd == "auto":
        if os.path.isdir(args.path):
            count = 0
            for root,dirs,files in os.walk(args.path):
                dirs[:]=[d for d in dirs if d not in ("__pycache__",".git",".venv","node_modules","_private")]
                for file in files:
                    fp = os.path.join(root,file)
                    if os.path.splitext(file)[1].lower() in FORMAT_MAP:
                        r = auto_append(fp, args.note)
                        if r: print(f"⛓️ V{r['version']} → {fp}"); count += 1
            print(f"\n✅ {count}文件自动接龍")
        else:
            r = auto_append(args.path, args.note)
            print(f"⛓️ V{r['version']} → {args.path}" if r else "🟢 无变更")


if __name__ == "__main__":
    main()

# ⛓️ 龍魂DNA接龍链 ──────────────────────────────
# DNA:V1|丙午·丙申·癸丑·亥时·䷓观|P04鲁班|创建|DNA接龍链引擎v1.0·十种格式·只追加不覆盖|bhash:35d3996b|chash:05f16491|←GENESIS
# ⛓️ 龍魂DNA接龍末端 ──────────────────────────────
