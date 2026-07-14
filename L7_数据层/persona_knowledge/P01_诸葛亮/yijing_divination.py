#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""🐉 易经起卦引擎 · P01 诸葛亮
DNA: #龍芯⚡️丙午·乙未·甲寅·申时·中孚-P01-YIJING"""
from __future__ import annotations
import hashlib, json, math, time, random
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[4]
HEXAGRAMS_FILE = Path(__file__).resolve().parent / "hexagrams.json"
KG_FILE = Path(__file__).resolve().parent / "knowledge_graph.json"

# — 八卦·五行定义（焊死） —
八卦先天 = {"乾": ("☰","天","金",1,"南"),"兑": ("☱","泽","金",2,"东南"),
             "离": ("☲","火","火",3,"东"),"震": ("☳","雷","木",4,"东北"),
             "巽": ("☴","风","木",5,"西南"),"坎": ("☵","水","水",6,"西"),
             "艮": ("☶","山","土",7,"西北"),"坤": ("☷","地","土",8,"北")}
河图五行 = {1:"水",2:"火",3:"木",4:"金",5:"土",6:"水",7:"火",8:"木",9:"金",0:"土"}
五行相生 = {"木":"火","火":"土","土":"金","金":"水","水":"木"}
五行相克 = {"木":"土","土":"水","水":"火","火":"金","金":"木"}

def _数字根(n: int) -> int:
    if n == 0: return 0
    r = n % 9; return 9 if r == 0 else r

def _sha8(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:8]

@dataclass
class 卦象:
    卦名: str; 卦符: str; 上卦: str; 下卦: str
    卦序: int = 0; 五行: str = ""; 大象: str = ""

@dataclass
class 起卦结果:
    主卦: 卦象; 变卦: 卦象; 互卦: Optional[卦象] = None
    综卦: Optional[卦象] = None; 错卦: Optional[卦象] = None
    动爻: int = 0; 天时: str = ""
    五行诊断: Dict[str, Any] = field(default_factory=dict)
    dna: str = ""

class YijingDivination:
    """易经起卦引擎 · 64卦运算 · 五行诊断"""

    def __init__(self):
        self.八卦 = 八卦先天
        self._加载六十四卦()
        self.案例库: List[Dict] = []

    def _加载六十四卦(self):
        if HEXAGRAMS_FILE.exists():
            self.六十四卦 = json.loads(HEXAGRAMS_FILE.read_text("utf-8"))
        else:
            self.六十四卦 = self._内置64卦()

    def _内置64卦(self) -> List[Dict[str, Any]]:
        """精简64卦定义（完整在 hexagrams.json）"""
        base = [
            (1,"乾","䷀","乾","乾","金","天行健，君子以自强不息"),
            (2,"坤","䷁","坤","坤","土","地势坤，君子以厚德载物"),
            (3,"屯","䷂","坎","震","水","云雷屯，君子以经纶"),
            (7,"师","䷆","坤","坎","土","地中有水，师。君子以容民畜众"),
            (11,"泰","䷊","坤","乾","土","天地交，泰。后以财成天地之道"),
            (12,"否","䷋","乾","坤","金","天地不交，否。君子以俭德辟难"),
            (14,"大有","䷍","离","乾","火","火在天上，大有。君子以遏恶扬善"),
            (30,"离","䷝","离","离","火","明两作，离。大人以继明照于四方"),
            (50,"鼎","䷱","离","巽","火","木上有火，鼎。君子以正位凝命"),
            (63,"既济","䷾","坎","离","水","水在火上，既济。君子以思患而预防之"),
            (64,"未济","䷿","离","坎","火","火在水上，未济。君子以慎辨物居方"),
        ]
        return [{"卦序":n,"卦名":m,"卦符":f,"上卦":s,"下卦":x,"五行":w,"大象":e}
                for n,m,f,s,x,w,e in base]

    def 时间起卦(self, 时间戳: Optional[str] = None) -> 起卦结果:
        """按时辰起卦：年+月+日 之和→上卦，年+月+日+时 之和→下卦"""
        from datetime import datetime
        dt = datetime.fromisoformat(时间戳) if 时间戳 else datetime.now()
        Y, M, D, h = dt.year, dt.month, dt.day, dt.hour
        s1 = sum(int(c) for c in str(Y)+str(M)+str(D))
        s2 = s1 + sum(int(c) for c in str(h))
        上卦数 = _数字根(s1)
        下卦数 = _数字根(s2)
        上卦名 = [k for k,v in self.八卦.items() if v[3]==上卦数][0] if 上卦数 in [v[3] for v in self.八卦.values()] else "乾"
        下卦名 = [k for k,v in self.八卦.items() if v[3]==下卦数][0] if 下卦数 in [v[3] for v in self.八卦.values()] else "坤"
        动爻 = (_数字根(s1+s2) % 6) + 1
        return self._组装卦象(上卦名, 下卦名, 动爻, f"{Y}年{M}月{D}日{h}时")

    def 随机起卦(self, 种子: Optional[str] = None) -> 起卦结果:
        """三枚铜钱法起卦"""
        if 种子:
            random.seed(int(hashlib.sha256(种子.encode()).hexdigest()[:8], 16))
        def 掷爻(): return (random.randint(0,1) + random.randint(0,1) + random.randint(0,1))
        lines = [掷爻() for _ in range(6)]
        change_pos = [i for i, v in enumerate(lines) if v % 2 != 1]
        动爻 = change_pos[0] + 1 if change_pos else 0
        上卦名, 下卦名 = self._爻线转卦(lines)
        return self._组装卦象(上卦名, 下卦名, 动爻)

    def _爻线转卦(self, lines: List[int]) -> Tuple[str, str]:
        lines = [l % 2 for l in lines]
        def 三爻转卦(tri): 
            code = f"{tri[0]}{tri[1]}{tri[2]}"
            for k, v in self.八卦.items():
                if v[3] == int(code, 2) + 1: return k
            return "坤"
        return 三爻转卦(lines[3:]), 三爻转卦(lines[:3])

    def _组装卦象(self, 上: str, 下: str, 动爻: int, 天时: str = "") -> 起卦结果:
        main = self._找卦(上, 下)
        changed = self._应用动爻(main, 动爻) if 动爻 > 0 else main
        wuxing = self._五行诊断(main)
        dna_raw = f"卦:{main.卦名}{main.卦符} 动爻:{动爻} ts:{time.time()}"
        return 起卦结果(
            主卦=main, 变卦=changed, 动爻=动爻, 天时=天时,
            五行诊断=wuxing, dna=f"#龍芯⚡️丙午·乙未·甲寅·申时·中孚-DIV-{_sha8(dna_raw)}"
        )

    def _找卦(self, 上: str, 下: str) -> 卦象:
        for g in self.六十四卦:
            if g["上卦"] == 上 and g["下卦"] == 下:
                return 卦象(卦名=g["卦名"], 卦符=g["卦符"], 上卦=上, 下卦=下,
                           卦序=g["卦序"], 五行=g["五行"], 大象=g.get("大象",""))
        return 卦象(卦名="未知", 卦符="??", 上卦=上, 下卦=下)

    def _应用动爻(self, 原卦: 卦象, 动爻: int) -> 卦象:
        """爻变：动爻处阴阳互换 → 变卦"""
        lines = [0]*6
        for k, v in self.八卦.items():
            if k == 原卦.上卦: offset = v[3]-1
            if k == 原卦.下卦: offset2 = v[3]-1
        changed_上 = chr(ord(原卦.上卦) + (1 if 动爻 > 3 else 0))
        changed_下 = chr(ord(原卦.下卦) + (1 if 动爻 <= 3 else 0))
        return self._找卦(changed_上, changed_下)

    def _五行诊断(self, 卦: 卦象) -> Dict[str, Any]:
        上五行 = self.八卦.get(卦.上卦, ("", "", "土", 0, ""))[2]
        下五行 = self.八卦.get(卦.下卦, ("", "", "土", 0, ""))[2]
        scores = {}
        for w in ["金","木","水","火","土"]:
            scores[w] = (7.0 if w==上五行 else 5.0) + (3.0 if w==下五行 else 0.0)
        avg = sum(scores.values()) / 5
        std = math.sqrt(sum((v-avg)**2 for v in scores.values()) / 5)
        wbi = max(0, min(100, 100 - (std/avg*100) if avg > 0 else 0))
        相生分 = 1.0 if 下五行 in 五行相生 and 五行相生[下五行]==上五行 else 0.5
        相克分 = 0.5 if 下五行 in 五行相克 and 五行相克[下五行]==上五行 else 0.0
        return {"五行分数": scores, "WBI": round(wbi, 1), "生克": {"相生": 相生分, "相克": 相克分},
                "总评": "🟢 平衡" if wbi > 70 else "🟡 微偏" if wbi > 40 else "🔴 失衡"}

    def 解读(self, 卦: 卦象) -> str:
        g = next((x for x in self.六十四卦 if x["卦名"]==卦.卦名), None)
        if not g: return f"{卦.卦名}卦，待补。"
        return f"[{卦.卦符} {卦.卦名}] {g['大象']} · 五行:{g['五行']} · 卦序:{g['卦序']}"

    def 保存案例(self, result: 起卦结果, question: str = ""):
        self.案例库.append({"question": question, "卦名": result.主卦.卦名,
                           "五行诊断": result.五行诊断, "dna": result.dna,
                           "timestamp": time.time()})

# CLI
if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="🐉 易经起卦引擎")
    p.add_argument("mode", choices=["time","random","解读"], help="起卦模式")
    p.add_argument("--question", "-q", help="问题")
    p.add_argument("--seed", "-s", help="随机种子")
    args = p.parse_args()
    yj = YijingDivination()
    if args.mode == "time":
        r = yj.时间起卦()
    else:
        r = yj.随机起卦(args.seed)
    print(f"主卦: {r.主卦.卦符} {r.主卦.卦名}  变卦: {r.变卦.卦符} {r.变卦.卦名}  动爻: {r.动爻}")
    print(f"解读: {yj.解读(r.主卦)}")
    print(f"五行诊断: WBI={r.五行诊断['WBI']} {r.五行诊断['总评']}")
    print(f"DNA: {r.dna}")

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·恒-CONFIRM-SEAL-yijing_divination-371449CA
