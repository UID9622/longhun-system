#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲午·庚午·䷳艮为山-SHUIJUN-DISCLOSE-V1.2-PATCH
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂系统 · 水军显化补丁内核 v1.2
作者：诸葛鑫（UID9622）
DNA: #龍芯⚡️丙午·乙未·甲午·庚午·䷳艮为山-SHUIJUN-DISCLOSE-V1.2-PATCH
"""

import hashlib
import math

W7 = {"设备": 0.20, "关联簇": 0.20, "地理IP": 0.10, "时间": 0.15,
      "兴趣": 0.10, "社交图": 0.15, "文本": 0.10}          # 3.2 权重（Σ=1）
阈值 = {"G0": 0.80, "G1": 0.50, "G2": 0.25}                # c≥0.80 G0 … <0.25 G3


class CNSH_水军补丁内核:
    DNA = "#龍芯⚡️丙午·乙未·甲午·庚午·䷳艮为山-SHUIJUN-DISCLOSE-V1.2-PATCH"

    # ===== 3.2/4.1 七因子综合可信度（置信门≥5/7） =====
    def 可信度(self, 因子分: dict) -> dict:
        可算 = {k: v for k, v in 因子分.items() if v is not None}
        if len(可算) < 5:
            return {"标注": False, "原因": "可计算因子<5，疑罪从无不标注"}
        c = sum(W7[k] * 可算[k] for k in 可算) / sum(W7[k] for k in 可算)
        级 = "G0" if c >= 0.80 else "G1" if c >= 0.50 else "G2" if c >= 0.25 else "G3"
        return {"标注": True, "c": round(c, 3), "级别": 级}

    # ===== 3.3/4.6 冷启动热度权重 =====
    @staticmethod
    def 冷启动权重(账号天数: int, 样本数: int) -> float:
        if 账号天数 >= 90 and 样本数 >= 100:
            return 1.0
        return min(1.0, 账号天数 / 90)                # 能说话，但声音不大

    # ===== 3.4/4.7 自然簇豁免 =====
    @staticmethod
    def 自然簇豁免(熵方差: float, 时间互相关: float, 模板J: float,
                   熵方差阈=0.5) -> bool:
        return 熵方差 > 熵方差阈 and 时间互相关 < 0.3 and 模板J < 0.3

    # ===== 3.5/4.3 嫁祸推定 =====
    @staticmethod
    def 水军雇主认定(支付: bool, 指令: bool, 历史: bool, 声明: bool,
                     人工终裁: bool) -> str:
        E = sum([支付, 指令, 历史, 声明])
        if E >= 2 and 人工终裁:
            return "🔴 认定自营水军"
        return "🟡 维持'被异常流量波及'保护性标签（受益≠罪证）"

    # ===== 3.6/4.8 误判补偿 =====
    @staticmethod
    def 误判补偿(基线日曝光: float, 误判期日曝光: float, 天数: int) -> float:
        return max(0.0, 基线日曝光 - 误判期日曝光) * 天数 * 1.2

    # ===== 3.7/4.5 标签衰减 =====
    @staticmethod
    def 标签衰减(W0: float, 天数: int, 级别: str) -> dict:
        t半 = 90 if 级别 == "G1" else 180
        W = W0 * (0.5 ** (天数 / t半))
        return {"W": round(W, 3), "摘标": W < 0.1}

    # ===== 3.8/4.4 批评可见度 + 秩相关 =====
    @staticmethod
    def 批评可见度(批评前50数: int, 批评总数: int, G0总数: int) -> float:
        if 批评总数 == 0 or G0总数 == 0:
            return 1.0
        return (批评前50数 / 50) / (批评总数 / G0总数)

    @staticmethod
    def 肯德尔τ(应然序: list, 实际序: list) -> float:
        n = len(应然序)
        同 = 0
        逆 = 0
        for i in range(n):
            for j in range(i + 1, n):
                a = (应然序[i] - 应然序[j]) * (实际序[i] - 实际序[j])
                if a > 0:
                    同 += 1
                elif a < 0:
                    逆 += 1
        return (同 - 逆) / max(同 + 逆, 1)

    # ===== 3.14 标签三态上链哈希（T24可测单元） =====
    @staticmethod
    def 标签状态哈希(评论ID哈希: str, 标签: str, 置信度: float,
                     时间戳: str, 操作者: str) -> str:
        """标签生成/变更/撤销的链上指纹；任一字段改动则哈希变。"""
        payload = f"{评论ID哈希}|{标签}|{置信度:.4f}|{时间戳}|{操作者}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


if __name__ == "__main__":
    核 = CNSH_水军补丁内核()
    print("七因子可信度:", 核.可信度({
        "设备": 0.9, "关联簇": 0.85, "地理IP": 0.8, "时间": 0.9,
        "兴趣": 0.7, "社交图": 0.8, "文本": 0.85
    }))
    print("新号冷启动权重:", 核.冷启动权重(10, 20))
    print("自然簇豁免:", 核.自然簇豁免(0.8, 0.1, 0.1))
    print("嫁祸认定:", 核.水军雇主认定(True, True, False, False, True))
    print("误判补偿:", 核.误判补偿(10000, 3000, 10))
    print("标签衰减:", 核.标签衰减(1.0, 90, "G1"))
    print("批评可见度:", 核.批评可见度(5, 20, 100))
    print("肯德尔τ:", 核.肯德尔τ([1, 2, 3, 4], [4, 3, 2, 1]))
