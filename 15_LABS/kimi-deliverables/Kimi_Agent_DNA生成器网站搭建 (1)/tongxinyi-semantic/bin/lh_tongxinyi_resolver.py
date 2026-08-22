# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-a2b40a75
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂 · 通心译引用解析器 v0.1
输入中文意图 → 抽屉路由 → 词元匹配 → 输出 en/CNSH 映射 + DNA
引用语法: @D03.铸码  或  自然语言 "帮我铸造DNA"
归属: 龍魂系统 UID9622 · 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
import os, sys, glob, difflib

try:
    import yaml
except ImportError:
    yaml = None

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DRAWERS_DIR = os.path.join(BASE, "drawers")


def load_library():
    """加载全部抽屉 → 扁平词元表"""
    lib = []
    for fp in sorted(glob.glob(os.path.join(DRAWERS_DIR, "D*.yaml"))):
        if yaml:
            with open(fp, encoding="utf-8") as f:
                doc = yaml.safe_load(f)
            for e in doc.get("entries", []):
                e["drawer"] = doc["drawer"]
                e["drawer_name"] = doc["name"]
                lib.append(e)
    return lib


def resolve(query, lib, top_k=3):
    """四级匹配: 显式引用 → 精确词元 → 别名 → 模糊 → 抽屉路由"""
    q = query.strip().lstrip("@")
    hits = []
    # 0) 显式引用 @D03.铸码
    if "." in q and q.split(".")[0].startswith("D"):
        did, term = q.split(".", 1)
        for e in lib:
            if e["drawer"] == did and e["term"] == term:
                return [dict(e, score=1.0, via="显式引用")]
    # 1) 精确词元
    for e in lib:
        if e["term"] in q or q in e["term"]:
            hits.append(dict(e, score=0.95, via="精确词元"))
    # 2) 别名
    if not hits:
        for e in lib:
            for a in e.get("alias", []):
                if a and (a in q or q in a):
                    hits.append(dict(e, score=0.85, via="别名:" + a))
                    break
    # 3) 模糊（编辑距离）
    if not hits:
        terms = {e["term"]: e for e in lib}
        close = difflib.get_close_matches(q, list(terms), n=top_k, cutoff=0.5)
        for t in close:
            hits.append(dict(terms[t], score=0.6, via="模糊匹配"))
    # 4) 抽屉路由（按抽屉名/领域字命中）
    if not hits:
        for e in lib:
            if e["drawer_name"] in q:
                hits.append(dict(e, score=0.4, via="抽屉路由"))
    # 去重排序
    seen, out = set(), []
    for h in sorted(hits, key=lambda x: -x["score"]):
        key = (h["drawer"], h["term"])
        if key not in seen:
            seen.add(key)
            out.append(h)
    return out[:top_k]


def main():
    lib = load_library()
    print("语义库已加载: {} 词元 / {} 抽屉".format(len(lib), len(set(e["drawer"] for e in lib))))
    if len(sys.argv) > 1:
        queries = [" ".join(sys.argv[1:])]
    else:
        queries = ["@D03.铸码", "帮我铸造DNA", "我要维权", "备份到华为云", "红蓝对抗", "看看日志文件"]
    for q in queries:
        print("\n[问] " + q)
        hits = resolve(q, lib)
        if not hits:
            print("   [未命中] 建议: 增补词元进对应抽屉")
            continue
        for h in hits:
            print("   [命中] @{drawer}.{term}  score={score}  via={via}".format(**h))
            print("      en: {en}  |  CNSH: {cnsh}  |  {gua}  |  {note}".format(
                en=h["en"], cnsh=h["cnsh"], gua=h["gua"], note=h.get("note", "")))


if __name__ == "__main__":
    main()
