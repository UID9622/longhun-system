#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂·作假行为检测引擎 v1.0
DNA: #龍芯⚡️2026-09-04-作假检测引擎-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
协议: CC BY-NC-SA 4.0（核心思想层）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色审计: 🟢 通过
文化主权: 不制造作假，仅用于审计识别
"""

import os, re, sys, json, hashlib, subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

FRAUD_TYPES = {
    "DNA_篡改":      {"权重": 0.95, "描述": "DNA追溯码被删除或修改", "颜色": "🔴"},
    "签名伪造":      {"权重": 0.90, "描述": "GPG签名无效或伪造",   "颜色": "🔴"},
    "时间戳篡改":   {"权重": 0.75, "描述": "文件时间戳被篡改",    "颜色": "🟡"},
    "水印抹除":     {"权重": 0.85, "描述": "龙魂水印被裁剪覆盖",  "颜色": "🔴"},
    "代码克隆_无DNA":{"权重": 0.80, "描述": "克隆龙魂代码无DNA",   "颜色": "🟡"},
    "虚假贡献":     {"权重": 0.90, "描述": "伪造提交记录冒充身份","颜色": "🔴"},
    "AI_内容伪造":  {"权重": 0.70, "描述": "AI生成虚假龙魂内容",  "颜色": "🟡"},
}

DNA_PATTERN       = r'#龍芯⚡️[0-9]{4}-[0-9]{2}-[0-9]{2}-[^\s]+'
GPG_PATTERN       = r'A2D0092CEE2E5BA87035600924C3704A8CC26D5F'
WATERMARK_PATTERN = r'🐉|龍魂|UID9622|长恨歌|曾仕强'

def ts(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def sha256(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def extract_dna(s): return re.findall(DNA_PATTERN, s)

def verify_gpg(p):
    asc = p.with_suffix(p.suffix + '.asc')
    if not asc.exists(): return False, "缺少.asc签名文件"
    r = subprocess.run(['gpg','--verify',str(asc),str(p)],
                       capture_output=True, text=True, timeout=10)
    return r.returncode == 0, r.stderr.strip() if r.returncode else "签名有效"

def check_dna(path, content):
    dna = extract_dna(content)
    if not dna: return {"类型":"DNA_篡改","可疑":True,"证据":["无DNA追溯码"],"置信度":0.95}
    ev = []
    if GPG_PATTERN not in content: ev.append("无GPG指纹")
    return {"类型":"DNA_篡改","可疑":bool(ev),"证据":ev,"置信度":0.70 if ev else 0.0}

def check_gpg(path, _):
    ok, msg = verify_gpg(path)
    return {"类型":"签名伪造","可疑":not ok,"证据":[msg] if not ok else [],"置信度":0.90 if not ok else 0.0}

def check_ts(path, _):
    s = path.stat(); now = datetime.now()
    ev = []
    if datetime.fromtimestamp(s.st_mtime) > now: ev.append("修改时间在未来")
    return {"类型":"时间戳篡改","可疑":bool(ev),"证据":ev,"置信度":0.75 if ev else 0.0}

def check_watermark(_, content):
    wm = re.findall(WATERMARK_PATTERN, content)
    if not wm: return {"类型":"水印抹除","可疑":True,"证据":["无水印"],"置信度":0.85}
    return {"类型":"水印抹除","可疑":False,"证据":[],"置信度":0.0}

def check_clone(path, content):
    hits = sum(1 for p in [r'三色审计',r'耻辱墙',r'五行',r'函数\s+'] if re.search(p,content))
    sus = hits >= 2 and not extract_dna(content)
    return {"类型":"代码克隆_无DNA","可疑":sus,"证据":[f"{hits}处龙魂特征无DNA"] if sus else [],"置信度":min(0.80,hits*0.25) if sus else 0.0}

def check_contrib(path, content):
    authors = re.findall(r'作者[:：]\s*[^\s]+', content)
    sus = len(authors) > 2
    return {"类型":"虚假贡献","可疑":sus,"证据":[f"多提交者:{authors[:3]}"] if sus else [],"置信度":0.70 if sus else 0.0}

def check_ai(_, content):
    hits = sum(1 for p in [r'作为一个AI',r'作为人工智能',r'据我所知'] if re.search(p,content,re.I))
    sus = hits >= 2
    return {"类型":"AI_内容伪造","可疑":sus,"证据":[f"{hits}处AI生成特征"] if sus else [],"置信度":min(0.70,hits*0.25) if sus else 0.0}

CHECKS = [check_dna, check_gpg, check_ts, check_watermark, check_clone, check_contrib, check_ai]

def scan_file(path):
    path = Path(path)
    try: content = path.read_text(encoding='utf-8', errors='ignore')
    except: content = ""
    results, top_conf, top_color = [], 0.0, "🟢"
    for fn in CHECKS:
        try:
            r = fn(path, content)
            if r["可疑"]:
                results.append(r)
                if r["置信度"] > top_conf:
                    top_conf = r["置信度"]
                    top_color = FRAUD_TYPES.get(r["类型"],{}).get("颜色","🟡")
        except: pass
    return {"文件":str(path),"状态":top_color,"置信度":top_conf,"问题":results}

def main():
    import argparse
    p = argparse.ArgumentParser(description="🐉 龍魂·作假行为检测")
    sub = p.add_subparsers(dest="cmd")
    s = sub.add_parser("scan"); s.add_argument("路径",nargs="?",default="."); s.add_argument("--报告")
    sub.add_parser("status")
    args = p.parse_args()
    if args.cmd == "scan":
        tp = Path(args.路径)
        files = list(tp.rglob("*")) if tp.is_dir() else [tp]
        results = [scan_file(f) for f in files if f.is_file() and f.suffix not in ('.asc','.pyc','.json')]
        sus = [r for r in results if r["问题"]]
        print(f"🐉 扫描完成: {len(results)}文件 | 🔴可疑:{len(sus)} 🟢正常:{len(results)-len(sus)}")
        for r in sus: print(f"  {r['状态']} {r['文件']} ({r['置信度']:.0%})")
        if args.报告:
            Path(args.报告).write_text(json.dumps({"时间":ts(),"总数":len(results),"可疑":sus},ensure_ascii=False,indent=2))
    elif args.cmd == "status":
        print("🐉 作假检测引擎 v1.0 | DNA: #龍芯⚡️2026-09-04-作假检测引擎-v1.0-UID9622")
        print(f"检测类型: {len(FRAUD_TYPES)}类 | 状态: 🟢 就绪")
    else: p.print_help()

if __name__ == "__main__": main()
