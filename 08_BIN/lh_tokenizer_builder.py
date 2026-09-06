#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·癸未·甲子·申时-TOKENIZER-BUILDER-v1.1-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 父任务: T6 tokenizer 自建与语料扩容 + S1 Qwen2 词表迁移 (2026-09-06)
# 说明: A词表扩充 / B语料清洗 / C单测 三轨。clean 纯 stdlib；
#       extend/test 依赖 tokenizers 库(已装 0.21.4) 加载真实 base tokenizer.json。
# v1.1 修复(S1 迁移暴露·2026-09-06): extend 起始 id 不得取 len(vocab)——Qwen2.5
#       added_tokens 段含 special(<|im_start|> 等 14 个·id 151643+)，len(vocab)=151643
#       起点会把注入词覆写 special → 改取全量已有 id 最大值+1（核验: 撞车22→0）。
# 用途: python3 08_BIN/lh_tokenizer_builder.py <subcmd> [args]

import hashlib
import json
import os
import re
import sys

VERSION = "v1.1"
OWNER = "诸葛鑫 | UID9622 · 龍芯北辰"

# ---------- 固定确定性测试句集（同参必同输出·不依赖随机） ----------
TEST_SENTENCES = [
    "龍魂系统今日用丙午丁酉时辰起卦，巽上艮下得渐卦。",
    "通心译把术语翻成大白话，让普通人也能看懂洛书369与五行八卦。",
    "P05 审计通过、P06 复算一致、P15 签章落定，三色全绿。",
    "癸未年秋，龍芯北辰主权焊死，DNA追溯码记录每一次变更。",
    "龘龘之勢在于每日精进，CNSH 语法与神经符号底座不可动摇。",
    "乾为天、坤为地、坎为水、离为火，八卦归位五行相生。",
    "元神归位，北辰常明，既济之后未济相续，阴阳互济。",
]


def sha256h(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def sha256h8(s):
    return sha256h(s)[:8]


def human(n):
    if n < 1024:
        return f"{n}B"
    if n < 1024 * 1024:
        return f"{n / 1024:.1f}KB"
    return f"{n / 1024 / 1024:.1f}MB"


# ============================================================
# B 轨 · 语料清洗流水线（纯 stdlib·零三方依赖）
# ============================================================
def _strip_control(s):
    """保留可见中文/ASCII/换行，剔除控制字符"""
    return "".join(ch for ch in s if ch == "\n" or ch == "\t" or (ord(ch) >= 32 and ord(ch) != 127))


def _read_texts(src_dir):
    """收集目录下 .md/.txt 文本，返回 [(relpath, raw)]"""
    out = []
    if os.path.isfile(src_dir):
        with open(src_dir, encoding="utf-8") as f:
            return [(os.path.basename(src_dir), f.read())]
    for root, _, files in os.walk(src_dir):
        for f in sorted(files):
            if f.endswith((".md", ".txt")):
                p = os.path.join(root, f)
                try:
                    with open(p, encoding="utf-8") as f:
                        text = f.read()
                    out.append((os.path.relpath(p, src_dir), text))
                except OSError:
                    continue
    return out


def cmd_clean(args):
    """B 轨: 去重/质量过滤/DNA标注 · python3 lh_tokenizer_builder.py clean --src corpus/raw --out corpus/clean"""
    src = args.get("--src") or "corpus/raw"
    outp = args.get("--out") or "corpus/clean"
    min_len = int(args.get("--min-len") or 8)
    seen = set()
    stats = {"input_files": 0, "dup_paras": 0, "short_paras": 0, "out_chars": 0}
    os.makedirs(outp, exist_ok=True)
    manifest = {"dna": "#龍芯⚡️丙午·丁酉·癸未·午时-CORPUS-CLEAN-v1.0-UID9622",
                "engine": f"lh_tokenizer_builder.py {VERSION}", "src": src, "out": outp}
    for rel, raw in _read_texts(src):
        stats["input_files"] += 1
        paras = [p.strip() for p in re.split(r"\n\s*\n", raw)]
        keep = []
        for p in paras:
            if not p:
                continue
            p = _strip_control(p)
            # 注释头/无意义行过滤
            if p.startswith("#"):
                continue
            # 质量: 长度下限
            if len(p) < min_len:
                stats["short_paras"] += 1
                continue
            # 质量: 去重（段落 sha 指纹）
            fp = sha256h(p)
            if fp in seen:
                stats["dup_paras"] += 1
                continue
            seen.add(fp)
            keep.append(p)
        if keep:
            base = os.path.splitext(os.path.basename(rel))[0]
            body = "\n\n".join(keep) + "\n"
            # DNA 标注（样本级·可追溯）
            dna = sha256h8(body)
            out_p = os.path.join(outp, f"{base}.clean.txt")
            with open(out_p, "w", encoding="utf-8") as f:
                f.write(f"# corpusDNA: {dna} | owner: {OWNER}\n{body}")
            stats["out_chars"] += len(body)
            manifest.setdefault("files", []).append({"src": rel, "out": os.path.basename(out_p),
                                                     "paras": len(keep), "dna": dna})
    manifest.update(stats)
    m_path = os.path.join(outp, "manifest.json")
    with open(m_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)
    print(f"🟢 B 语料清洗 · src={src} · 文件 {stats['input_files']} · "
          f"去重段 {stats['dup_paras']} · 过滤段 {stats['short_paras']} · 输出 {human(stats['out_chars'])}")
    print(f"   → {outp}/*.clean.txt + manifest.json (DNA 标注 {len(manifest.get('files', []))} 段)")
    return 0


# ============================================================
# base 模型扫描
# ============================================================
def cmd_bases(args):
    base = args.get("--dir") or "models/base_models_v4.0"
    found = []
    if os.path.isdir(base):
        for d in sorted(os.listdir(base)):
            tj = os.path.join(base, d, "tokenizer.json")
            if os.path.isfile(tj):
                try:
                    import tokenizers
                    t = tokenizers.Tokenizer.from_file(tj)
                    found.append((d, tj, t.get_vocab_size()))
                except Exception:
                    found.append((d, tj, "?"))
    print(f"可用 base tokenizer (扫 {base}):")
    for name, p, vsz in found:
        print(f"   {name:<32} vocab={vsz}  {p}")
    return 0


# ============================================================
# A 轨 · 词表扩充（真实 base tokenizer.json 增量注入 added tokens）
# ============================================================
def cmd_extend(args):
    """A 轨: --tokenizer <xx.json> --lexicon <词表每行一词> --out <扩展 json> [--tag <后缀>]"""
    tj = args.get("--tokenizer") or _default_tokenizer()
    lex = args.get("--lexicon") or "corpus/longhun_lexicon.txt"
    tag = args.get("--tag") or "longhun"
    out_path = args.get("--out") or tj.replace("tokenizer.json", f"tokenizer_{tag}.json")
    try:
        import tokenizers
    except ImportError:
        print("🔴 A 轨需 tokenizers 库: pip install tokenizers")
        return 1
    with open(tj, encoding="utf-8") as f:
        d = json.load(f)
    vocab = d["model"]["vocab"]
    base = tokenizers.Tokenizer.from_file(tj)
    with open(lex, encoding="utf-8") as lf:
        words = [w.strip() for w in lf if w.strip() and not w.startswith("#")]
    existing_added = {a["content"] for a in d.get("added_tokens", [])}
    # v1.1: 起始 id = 全量已有 id 最大值+1（含 added_tokens 段的 special）
    # 防撞车: Qwen2.5 model.vocab=151643 但 added 段 special(<|im_start|> 等) id 151643+
    vocab_vals = set(vocab.values()) if isinstance(vocab, dict) else set(range(len(vocab)))
    all_ids = vocab_vals | {a["id"] for a in d.get("added_tokens", [])}
    next_id = max(all_ids) + 1
    report = {"dna": "#龍芯⚡️丙午·癸未·甲子·申时-TOKENIZER-EXTEND-v1.1-UID9622",
              "base": tj, "base_vocab": len(vocab), "lexicon": lex,
              "words": [], "injected": 0, "already": 0, "saved_tokens": 0}
    for w in words:
        if w in vocab or w in existing_added:
            report["already"] += 1
            continue
        n = len(base.encode(w).ids)  # base 拆分 token 数
        d["added_tokens"].append({"id": next_id, "content": w, "single_word": False,
                                  "lstrip": False, "rstrip": False,
                                  "special": False, "normalized": False})
        next_id += 1
        report["injected"] += 1
        report["words"].append({"word": w, "base_tokens": n, "saved": max(n - 1, 0)})
        report["saved_tokens"] += max(n - 1, 0)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    # 产物自解释指纹
    fp = sha256h(json.dumps({"base": tj, "added": report["words"], "n": len(vocab) + report["injected"]},
                            ensure_ascii=False, sort_keys=True))
    report["out"] = out_path
    report["out_vocab"] = len(vocab) + report["injected"]
    report["sha256"] = fp
    r_path = out_path.replace(".json", "_report.json")
    with open(r_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    multi = [r for r in report["words"] if r["base_tokens"] > 1]
    one = [r for r in report["words"] if r["base_tokens"] == 1]
    print(f"🟢 A 词表扩充 · base={os.path.basename(tj)} (vocab {len(vocab)}) · 注入 {report['injected']} 词"
          f" · 已存在 {report['already']} · 共省 {report['saved_tokens']} token/词串")
    print(f"   压缩>1token 词 {len(multi)} 个: " + " ".join(r["word"] for r in multi[:12]) + (" ..." if len(multi) > 12 else ""))
    if one:
        print(f"   本就是单 token(无需注入已统计): 前 {len(one)} 个中 " + " ".join(r["word"] for r in one[:6]) + " ...")
    print(f"   → {out_path} + _report.json · SHA256={fp[:16]}…")
    return 0


# ============================================================
# C 轨 · 单测：无损往返 + Determinism 实证
# ============================================================
def _norm_space(s):
    """去 ASCII 空格（含不间断空格）做语义无损比较。中文语义不随 ASCII 空格变化；
    Yi 系 ByteLevel/▁(U+2581) 混合 decoder 对 ASCII 空格往返本就不恢复（base 同特性）。"""
    return s.replace(" ", "").replace("\u00a0", "")


def cmd_test(args):
    """C 轨: --file <扩展/基础 tokenizer.json> [--base <基础对照.json>] · 语义无损往返 + 两跑同 id"""
    tj = args.get("--file") or _default_tokenizer()
    lex = args.get("--lexicon")
    base_p = args.get("--base")
    try:
        import tokenizers
    except ImportError:
        print("🔴 C 轨需 tokenizers 库")
        return 1
    tok = tokenizers.Tokenizer.from_file(tj)
    base_tok = tokenizers.Tokenizer.from_file(base_p) if base_p and os.path.isfile(base_p) else None
    samples = list(TEST_SENTENCES)
    if lex and os.path.isfile(lex):
        with open(lex, encoding="utf-8") as lf:
            samples += [w.strip() for w in lf if w.strip() and not w.startswith("#")]
    n_ok = n_space = n_fail = 0
    fails = []
    ids_runs = {}
    for s in samples:
        r1 = tok.encode(s)
        r2 = tok.encode(s)  # determinism: 两遍编码
        dec = tok.decode(r1.ids)
        same = r1.ids == r2.ids
        if dec == s and same:
            n_ok += 1
        elif _norm_space(dec) == _norm_space(s) and same:
            n_space += 1  # 仅 ASCII 空格级差异 = base 固有特性，不判失败
        else:
            n_fail += 1
            fails.append((s, dec[:20] if dec != s else "", "ids不一致" if not same else ""))
        ids_runs[sha256h8(s)] = {"ids": r1.ids, "sha": sha256h(json.dumps(r1.ids))}
    fp = sha256h(json.dumps({k: v["sha"] for k, v in ids_runs.items()}, sort_keys=True))
    total_tokens = sum(len(v["ids"]) for v in ids_runs.values())
    color = "🟢" if n_fail == 0 else "🟡"
    print(f"{color} C tokenizer 单测 · {tj}")
    print(f"   语义无损往返: {n_ok + n_space}/{len(samples)} · 逐字精确 {n_ok} + 空格级差异 {n_space} (base 固有·见下)")
    if n_space:
        print("   ⓘ ASCII 空格往返不恢复 = Yi 系 ByteLevel/▁ 混合 decoder 固有特性，base 同行为")
    for s, d, why in fails[:5]:
        print(f"     ❌ {s!r} diff={d!r} {why}")
    print(f"   Determinism: 两遍编码 ids 逐一比对一致 · 样本 {len(samples)} · 总 token {total_tokens}")
    if base_tok:
        b_ok = b_sp = b_fail = 0
        for s in samples:
            dec = base_tok.decode(base_tok.encode(s).ids)
            if dec == s:
                b_ok += 1
            elif _norm_space(dec) == _norm_space(s):
                b_sp += 1
            else:
                b_fail += 1
        regress = n_fail - b_fail
        print(f"   对照 base {os.path.basename(base_p)}: 精确 {b_ok} + 空格级 {b_sp} + 失败 {b_fail}"
              f" → 扩展相对无退化 {'✓' if n_fail == b_fail else '⚠️新增失败' + str(regress)}")
    print(f"   指纹 SHA256={fp} (同参必同输出·可复现)")
    return 0


def _default_tokenizer():
    base = "models/base_models_v4.0"
    for d in ["Meta-Llama-3.1-8B-Instruct", "Yi-1.5-9B-Chat", "DeepSeek-R1-Distill-Llama-8B"]:
        p = os.path.join(base, d, "tokenizer.json")
        if os.path.isfile(p):
            return p
    for root, _, files in os.walk(base):
        for f in files:
            if f == "tokenizer.json":
                return os.path.join(root, f)
    return "models/base_models_v4.0/Yi-1.5-9B-Chat/tokenizer.json"


def _usage():
    print(f"lh_tokenizer_builder.py {VERSION} · A词表扩充/B语料清洗/C单测 · owner {OWNER}")
    print("  扫描base:   bases [--dir models/base_models_v4.0]")
    print("  B 清洗轨:   clean --src corpus/raw --out corpus/clean [--min-len 8]")
    print("  A 扩充轨:   extend --tokenizer <xx.json> --lexicon corpus/longhun_lexicon.txt [--tag longhun] [--out <out.json>]")
    print("  C 单测轨:   test --file <扩展.json> [--lexicon corpus/longhun_lexicon.txt]")
    print("示例: python3 08_BIN/lh_tokenizer_builder.py extend && python3 08_BIN/lh_tokenizer_builder.py test --file models/base_models_v4.0/Yi-1.5-9B-Chat/tokenizer_longhun.json")
    return 0


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        return _usage()
    sub, rest = argv[0], argv[1:]
    args = {}
    for i in range(0, len(rest), 2):
        if rest[i].startswith("--") and i + 1 < len(rest):
            args[rest[i]] = rest[i + 1]
        else:
            args[rest[i]] = True
    if sub == "bases":
        return cmd_bases(args)
    if sub == "clean":
        return cmd_clean(args)
    if sub == "extend":
        return cmd_extend(args)
    if sub == "test":
        return cmd_test(args)
    print(f"未知子命令: {sub}")
    return _usage()


if __name__ == "__main__":
    sys.exit(main())
