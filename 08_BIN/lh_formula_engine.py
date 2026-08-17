#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·丙申·壬戌·巳时-FORMULA-ENGINE-v1.0-LANDED
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0（核心思想层）
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)（工程实现层）
"""
🐉 龍魂 · 计算公式引擎 v1.0（落地版）

完整实现: 25条核心公式 · 64卦推演 · 三色审计 · 五行平衡 · 中庸决策
§A 三才核心 (A1-A8): 冲气以为和 / 数字根 / 三色熔断 / 五行映射 / 六维路径
                    / 三才卦象 / 五行生克 / 易经决策树
§B 决策审计 (B1-B8): 龍魂仲裁 / 三色审计 / 语义入口 / 时间衰减 / 贡献值
                    / 人格叠加 / 权重效用 / 守恒分数
§C 统一代数 (C1-C9): 统一场 / 五行循环 / 双随机矩阵 / 洛书数字 / 八卦序列
                    / 64卦_id / 干支计算 / 节气权重 / 时间预测

用法:
  python3 bin/lh_formula_engine.py -l                    # 列出全部公式
  python3 bin/lh_formula_engine.py -s                    # 状态
  python3 bin/lh_formula_engine.py -e "A8_易经决策树,question=今年是否适合创业"
  python3 bin/lh_formula_engine.py -e "B2_三色审计,score=75"
  python3 bin/lh_formula_engine.py -e "C8_节气权重,month=6,day=21"

DNA: #龍芯⚡️丙午·丙申·壬戌·巳时-FORMULA-ENGINE-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
"""

import hashlib
import json
import math
import time
import random
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# ============================================================
# 主权锚定
# ============================================================

UID = "9622"
CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
GPG = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"


def generate_dna(suffix: str = "ENGINE") -> str:
    now = datetime.now()
    h = hashlib.sha256(f"{suffix}{time.time()}".encode()).hexdigest()[:8].upper()
    return f"#龍芯⚡️{now.strftime('%Y-%m-%d')}-{suffix}-{h}-{UID}"


# 64卦序列（文王卦序）
GUA_64 = ["乾", "坤", "屯", "蒙", "需", "讼", "师", "比",
          "小畜", "履", "泰", "否", "同人", "大有", "谦", "豫",
          "随", "蛊", "临", "观", "噬嗑", "贲", "剥", "复",
          "无妄", "大畜", "颐", "大过", "坎", "离", "咸", "恒",
          "遁", "大壮", "晋", "明夷", "家人", "睽", "蹇", "解",
          "损", "益", "夬", "姤", "萃", "升", "困", "井",
          "革", "鼎", "震", "艮", "渐", "归妹", "丰", "旅",
          "巽", "兑", "涣", "节", "中孚", "小过", "既济", "未济"]

# ============================================================
# §A: 三才核心公式 (A1-A8)
# ============================================================


class FormulaA:
    """三才核心公式"""

    @staticmethod
    def A1_冲气以为和(tian: int, di: int, ren: int) -> Dict:
        """
        A1: 冲气以为和
        天爻(⚊) + 地爻(⚋) + 人爻(⨯) → 卦象(当前状态)
        """
        if tian == 1 and di == 0 and ren == 2:
            return {"gua": "乾", "state": "刚健", "color": "🟢"}
        elif tian == 0 and di == 1 and ren == 2:
            return {"gua": "坤", "state": "柔顺", "color": "🟢"}
        elif tian == 1 and di == 1 and ren == 0:
            return {"gua": "泰", "state": "通达", "color": "🟢"}
        else:
            gua_map = {
                (0, 0, 0): ("坤", "厚德载物", "🟢"),
                (1, 1, 1): ("乾", "自强不息", "🟢"),
                (0, 1, 0): ("坎", "水深多险", "🔴"),
                (1, 0, 1): ("离", "光明照耀", "🟢"),
            }
            gua, meaning, color = gua_map.get((tian, di, ren), ("未济", "事未成", "🟡"))
            return {"gua": gua, "state": meaning, "color": color}

    @staticmethod
    def A2_数字根(n: int) -> int:
        """
        A2: DR(n) = 1 + ((n - 1) % 9)
        数字根，1-9循环
        """
        if n <= 0:
            return 0
        return 1 + ((n - 1) % 9)

    @staticmethod
    def A3_三色熔断(n: int) -> Dict:
        """
        A3: DR(n) ∈ {3,6,9} → 🔴熔断
        """
        dr = FormulaA.A2_数字根(n)
        if dr in [3, 6, 9]:
            return {"status": "🔴 熔断", "dr": dr, "action": "FUSE"}
        elif dr in [1, 2, 4, 5, 7, 8]:
            return {"status": "🟢 通过", "dr": dr, "action": "PASS"}
        return {"status": "🟡 待定", "dr": dr, "action": "REVIEW"}

    @staticmethod
    def A4_五行映射(element: str) -> Dict:
        """
        A4: 木火土金水 ↔ 生克链循环群 Z₅
        """
        mapping = {
            "木": {"color": "青", "direction": "东", "id": 0, "生": "火", "克": "土"},
            "火": {"color": "红", "direction": "南", "id": 1, "生": "土", "克": "金"},
            "土": {"color": "黄", "direction": "中", "id": 2, "生": "金", "克": "水"},
            "金": {"color": "白", "direction": "西", "id": 3, "生": "水", "克": "木"},
            "水": {"color": "黑", "direction": "北", "id": 4, "生": "木", "克": "火"},
        }
        return mapping.get(element, {"error": f"未知五行: {element}"})

    @staticmethod
    def A5_六维路径(data: str) -> Dict:
        """
        A5: D1-D6: 数字根→洛书→八卦→64卦→五行→天干地支
        """
        hash_val = hashlib.sha256(data.encode()).hexdigest()
        steps = []

        n = int(hash_val[:8], 16)
        dr = FormulaA.A2_数字根(n)
        steps.append({"D1": "数字根", "value": dr})

        luoshu = (dr * 7) % 9 + 1
        steps.append({"D2": "洛书", "value": luoshu})

        bagua = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"][dr % 8]
        steps.append({"D3": "八卦", "value": bagua})

        gua_name = GUA_64[dr % 64]
        steps.append({"D4": "64卦", "value": gua_name})

        wuxing = ["木", "火", "土", "金", "水"][dr % 5]
        steps.append({"D5": "五行", "value": wuxing})

        tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        gan = tian_gan[dr % 10]
        zhi = di_zhi[dr % 12]
        steps.append({"D6": "天干地支", "value": f"{gan}{zhi}"})

        return {"steps": steps, "hash": hash_val[:16]}

    @staticmethod
    def A6_三才卦象(tian: int, di: int, ren: int) -> Dict:
        """
        A6: 三才合一生成卦象
        """
        steps = []
        yao_tian = "⚊" if tian % 2 == 1 else "⚋"
        yao_di = "⚊" if di % 2 == 1 else "⚋"
        yao_ren = "⨯" if ren % 3 == 2 else ("⚊" if ren % 2 == 1 else "⚋")
        steps.append({"三才": f"{yao_tian}{yao_di}{yao_ren}"})

        he = (tian + di + ren) % 3
        if he == 0:
            result = {"卦": "泰", "意": "天地交泰", "色": "🟢"}
        elif he == 1:
            result = {"卦": "否", "意": "天地不交", "色": "🔴"}
        else:
            result = {"卦": "既济", "意": "事已大成", "色": "🟢"}

        return {"steps": steps, "result": result}

    @staticmethod
    def A7_五行生克(from_elem: str, to_elem: str) -> Dict:
        """
        A7: 五行相生相克判断
        """
        sheng_map = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
        ke_map = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}

        if sheng_map.get(from_elem) == to_elem:
            return {"relation": "相生", "type": "sheng", "score": 0.8, "advice": "顺势而行"}
        elif ke_map.get(from_elem) == to_elem:
            return {"relation": "相克", "type": "ke", "score": 0.3, "advice": "需化解阻碍"}
        else:
            return {"relation": "平和", "type": "ping", "score": 0.5, "advice": "稳步推进"}

    @staticmethod
    def A8_易经决策树(question: str) -> Dict:
        """
        A8: 问题 → 卦象匹配 → 时空修正 → 裁决
        """
        hash_val = hashlib.sha256(question.encode()).hexdigest()
        n = int(hash_val[:8], 16)
        dr = FormulaA.A2_数字根(n)

        gua = GUA_64[dr % 64]

        # 时空修正 (节气)
        now = datetime.now()
        month = now.month
        season_weight = 1.0
        if month in [3, 4, 5]:
            season_weight = 1.1
        elif month in [6, 7, 8]:
            season_weight = 0.9
        elif month in [9, 10, 11]:
            season_weight = 1.0
        else:
            season_weight = 0.8

        # 裁决
        score = (dr / 9) * season_weight
        if score >= 0.7:
            judgment = "大吉"
            color = "🟢"
        elif score >= 0.4:
            judgment = "中平"
            color = "🟡"
        else:
            judgment = "需谨慎"
            color = "🔴"

        return {
            "gua": gua,
            "dr": dr,
            "season_weight": round(season_weight, 2),
            "score": round(score, 3),
            "judgment": judgment,
            "color": color,
            "advice": f"当前{judgment}，建议{'积极推进' if score >= 0.7 else '稳健行事' if score >= 0.4 else '暂缓行动'}"
        }


# ============================================================
# §B: 决策与审计公式 (B1-B8)
# ============================================================


class FormulaB:
    """决策与审计公式"""

    @staticmethod
    def B1_龍魂仲裁(values: Dict, history: Dict, yijing: Dict) -> Dict:
        """
        B1: 最终 = 价值观40% + 历史30% + 易经30%
        """
        v_score = values.get("score", 0.5)
        h_score = history.get("score", 0.5)
        y_score = yijing.get("score", 0.5)

        final = v_score * 0.4 + h_score * 0.3 + y_score * 0.3
        return {
            "final_score": round(final, 3),
            "values_weight": round(v_score * 0.4, 3),
            "history_weight": round(h_score * 0.3, 3),
            "yijing_weight": round(y_score * 0.3, 3),
            "status": "🟢" if final >= 0.7 else ("🟡" if final >= 0.4 else "🔴")
        }

    @staticmethod
    def B2_三色审计(score: float) -> Dict:
        """
        B2: 🟢 ≥85分 / 🟡 60-85分 / 🔴 <60分
        注: 使用百分制 (0-100)；与系统三色审计(0-1)口径不同，用前需换算
        """
        if score >= 85:
            return {"color": "🟢", "status": "通过", "advice": "可执行"}
        elif score >= 60:
            return {"color": "🟡", "status": "警告", "advice": "需复核"}
        else:
            return {"color": "🔴", "status": "拒绝", "advice": "熔断"}

    @staticmethod
    def B3_语义入口(text: str) -> Dict:
        """
        B3: α三义 - 语义入口计算
        """
        words = len(text.split())
        chars = len(text)
        hash_val = hashlib.sha256(text.encode()).hexdigest()
        dr = FormulaA.A2_数字根(int(hash_val[:8], 16))

        return {
            "words": words,
            "chars": chars,
            "dr": dr,
            "complexity": round(words / max(chars, 1), 3),
            "entry_score": round(dr / 9, 3)
        }

    @staticmethod
    def B4_时间衰减(timestamp: float, half_life: float = 30) -> float:
        """
        B4: 历史权重衰减 (半衰期半衰期天数)
        """
        age = time.time() - timestamp
        if age <= 0:
            return 1.0
        return round(math.exp(-age / (half_life * 86400)), 3)

    @staticmethod
    def B5_贡献值(persona: Dict, content: str) -> float:
        """
        B5: 人格与内容贡献值
        """
        weight = persona.get("weight", 0.5)
        length_score = min(len(content) / 1000, 1.0)
        return round(weight * (0.3 + 0.7 * length_score), 3)

    @staticmethod
    def B6_人格叠加(personas: List[Dict]) -> Dict:
        """
        B6: 多人格权重聚合
        """
        if not personas:
            return {"total": 0, "weights": [], "dominant": None}

        weights = [p.get("weight", 1 / len(personas)) for p in personas]
        total = sum(weights)
        normalized = [w / total for w in weights]

        return {
            "total": round(total, 3),
            "weights": [round(w, 3) for w in normalized],
            "dominant": personas[weights.index(max(weights))].get("name", "未知")
        }

    @staticmethod
    def B7_权重效用(weights: List[float], scores: List[float]) -> float:
        """
        B7: 综合效用计算
        """
        if not weights or not scores or len(weights) != len(scores):
            return 0.0
        total_w = sum(weights)
        if total_w == 0:
            return 0.0
        return round(sum(w * s for w, s in zip(weights, scores)) / total_w, 3)

    @staticmethod
    def B8_守恒分数(data: Dict) -> float:
        """
        B8: 能量守恒审计
        """
        values = list(data.values())
        if not values:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return round(max(0.0, min(1.0, 1 - variance / 0.3)), 3)


# ============================================================
# §C: 统一代数结构 (C1-C9)
# ============================================================


class FormulaC:
    """统一代数结构公式"""

    @staticmethod
    def C1_统一场(z9: int, z10: int, bits: Tuple[int, int, int, int, int, int], z5: int) -> Dict:
        """
        C1: U = Z₉ × Z₁₀ × {0,1}⁶ × Z₅
        """
        return {
            "Z9": z9 % 9,
            "Z10": z10 % 10,
            "bits": tuple(b % 2 for b in bits[:6]),
            "Z5": z5 % 5,
            "state": f"{z9 % 9}-{z10 % 10}-{''.join(str(b % 2) for b in bits[:6])}-{z5 % 5}"
        }

    @staticmethod
    def C2_五行循环(element: str, steps: int) -> List[str]:
        """
        C2: 生克 = Z₅ 两个生成元
        """
        cycle = ["木", "火", "土", "金", "水"]
        if element not in cycle:
            return []
        idx = cycle.index(element)
        return [cycle[(idx + i) % 5] for i in range(steps)]

    @staticmethod
    def C3_双随机矩阵(state: List[float]) -> List[List[float]]:
        """
        C3: 双随机矩阵收敛到均匀分布
        """
        random.seed(42)
        n = len(state)
        matrix = []
        for _ in range(n):
            row = [random.random() for _ in range(n)]
            row_sum = sum(row)
            row = [x / row_sum for x in row]
            matrix.append(row)
        return [[round(x, 3) for x in row] for row in matrix]

    @staticmethod
    def C4_洛书数字(dr: int) -> int:
        """
        C4: 洛书映射
        """
        luoshu_map = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9}
        return luoshu_map.get(dr, 1)

    @staticmethod
    def C5_八卦序列(start: str) -> List[str]:
        """
        C5: 八卦序列
        """
        all_gua = ["乾", "兑", "离", "震", "巽", "坎", "艮", "坤"]
        if start not in all_gua:
            return all_gua
        idx = all_gua.index(start)
        return all_gua[idx:] + all_gua[:idx]

    @staticmethod
    def C6_64卦_id(gua_name: str) -> int:
        """
        C6: 64卦编号
        """
        try:
            return GUA_64.index(gua_name) + 1
        except ValueError:
            return 0

    @staticmethod
    def C7_干支计算(year: int) -> Dict:
        """
        C7: 天干地支计算
        """
        tian_gan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        di_zhi = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]
        gan = tian_gan[(year - 4) % 10]
        zhi = di_zhi[(year - 4) % 12]
        return {"gan": gan, "zhi": zhi, "ganzhi": f"{gan}{zhi}"}

    @staticmethod
    def C8_节气权重(month: int, day: int) -> float:
        """
        C8: 节气权重计算
        """
        solar_terms = {
            (2, 3): 1.1, (2, 18): 1.05, (3, 5): 1.15, (3, 20): 1.0,
            (4, 4): 0.95, (4, 19): 1.05, (5, 5): 1.2, (5, 21): 1.1,
            (6, 5): 1.15, (6, 21): 1.25, (7, 7): 1.1, (7, 22): 1.2,
            (8, 7): 0.9, (8, 23): 0.85, (9, 7): 0.8, (9, 23): 1.0,
            (10, 8): 0.75, (10, 23): 0.7, (11, 7): 0.6, (11, 22): 0.65,
            (12, 7): 0.55, (12, 22): 0.5, (1, 5): 0.55, (1, 20): 0.6
        }
        key = (month, day)
        if key in solar_terms:
            return solar_terms[key]

        closest = min(solar_terms.keys(), key=lambda k: abs(k[0] * 30 + k[1] - (month * 30 + day)))
        return solar_terms.get(closest, 1.0)

    @staticmethod
    def C9_时间预测(question: str, months: int = 12) -> List[Dict]:
        """
        C9: 时间预测
        """
        results = []
        base = datetime.now()
        hash_val = hashlib.sha256(question.encode()).hexdigest()
        seed = int(hash_val[:8], 16)

        for i in range(months):
            idx = (seed + i * 7) % 64
            gua = GUA_64[idx]
            dr = FormulaA.A2_数字根(seed + i * 13)
            results.append({
                "month": (base.month - 1 + i) % 12 + 1,
                "year": base.year + (base.month - 1 + i) // 12,
                "gua": gua,
                "dr": dr,
                "fortune": round(dr / 9 * (0.8 + 0.2 * (1 - i / months)), 3)
            })

        return results


# ============================================================
# 主引擎
# ============================================================


class FormulaEngine:
    """计算公式引擎 - 25条公式完整实现"""

    def __init__(self):
        self.dna = generate_dna("FORMULA-ENGINE")
        self.A = FormulaA()
        self.B = FormulaB()
        self.C = FormulaC()
        self.history = []

    def evaluate(self, formula_id: str, **kwargs) -> Dict:
        """执行指定公式"""
        method = getattr(self.A, formula_id, None)
        if method is None:
            method = getattr(self.B, formula_id, None)
        if method is None:
            method = getattr(self.C, formula_id, None)

        if method is None:
            return {"error": f"未知公式: {formula_id}"}

        result = method(**kwargs)
        # 修复(2026-08-16): 纯数值返回(如C8节气权重/B4时间衰减)无法挂DNA → 自动包装
        if not isinstance(result, dict):
            result = {"value": result}
        result["formula"] = formula_id
        result["dna"] = generate_dna(formula_id)
        self.history.append(result)
        return result

    def get_status(self) -> Dict:
        return {
            "dna": self.dna,
            "formulas": {
                "A": [m for m in dir(self.A) if m.startswith("A")],
                "B": [m for m in dir(self.B) if m.startswith("B")],
                "C": [m for m in dir(self.C) if m.startswith("C")],
            },
            "history_count": len(self.history),
            "status": "🟢 运行中"
        }


# ============================================================
# 命令行接口
# ============================================================


def main():
    import argparse
    parser = argparse.ArgumentParser(description="🐉 龍魂 · 计算公式引擎")
    parser.add_argument("--list", "-l", action="store_true", help="列出所有公式")
    parser.add_argument("--status", "-s", action="store_true", help="查看状态")
    parser.add_argument("--eval", "-e", type=str, help="执行公式 (格式: 公式名,参数名1=值1,参数名2=值2)")

    args = parser.parse_args()
    engine = FormulaEngine()

    if args.status:
        status = engine.get_status()
        print("\n🐉 计算公式引擎状态")
        print("=" * 50)
        print(f"  DNA: {status['dna']}")
        print(f"  A类公式: {len(status['formulas']['A'])} 条")
        print(f"  B类公式: {len(status['formulas']['B'])} 条")
        print(f"  C类公式: {len(status['formulas']['C'])} 条")
        print(f"  执行历史: {status['history_count']} 次")
        return

    if args.list:
        status = engine.get_status()
        print("\n📋 公式列表 (25条)")
        print("=" * 50)
        print("\n§A 三才核心:")
        for f in status['formulas']['A']:
            print(f"  {f}")
        print("\n§B 决策审计:")
        for f in status['formulas']['B']:
            print(f"  {f}")
        print("\n§C 统一代数:")
        for f in status['formulas']['C']:
            print(f"  {f}")
        return

    if args.eval:
        parts = args.eval.split(",")
        formula_name = parts[0]
        kwargs = {}
        for p in parts[1:]:
            if "=" in p:
                k, v = p.split("=", 1)
                try:
                    kwargs[k] = int(v) if v.isdigit() else float(v) if v.replace('.', '', 1).isdigit() else v
                except ValueError:
                    kwargs[k] = v
        result = engine.evaluate(formula_name, **kwargs)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
