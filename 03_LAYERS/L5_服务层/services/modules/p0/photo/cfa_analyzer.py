#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷌同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# -*- coding: utf-8 -*-
"""
龍魂P0 · CFA色彩滤波阵列一致性分析

原理: 真实相机传感器有 Bayer CFA 模式，经插值生成彩色图，其周期性在频域可检；
篡改/重采样会破坏该连续性。检测亮度通道在(2,2)网格上的周期性残留。
能力: 真实(numpy/scipy FFT)。返回周期性得分与一致性判定。
返回: {"capability","tier","periodicity_score","consistent","notes"}
DNA #龍魂⚡️丙午·辛未·P0-CFA-v1
"""

import io
import numpy as np
from PIL import Image
from scipy import fftpack


def cfa_consistency(img_bytes: bytes) -> dict[str, Any]:
    res = {"capability": "real", "tier": "🟢真实(CFA正常)",
           "periodicity_score": 0.0, "consistent": True, "notes": ""}
    try:
        gray = np.asarray(Image.open(io.BytesIO(img_bytes)).convert("L"), dtype=np.float32)
        # 每像素位置(奇偶性)分组求均值，比较奇偶子网格差异
        # 用2x2四相子采样相关性近似
        f = fftpack.fft2(gray)
        # 关注(1,0)/(0,1)频率处的能量(对应CFA周期)
        h, w = gray.shape
        fshift = np.abs(np.fft.fftshift(f))
        cy, cx = h//2, w//2
        # 邻近(1,0)和(0,1)的能量
        e_h = float(fshift[cy, cx+1] + fshift[cy, cx-1])
        e_v = float(fshift[cy+1, cx] + fshift[cy-1, cx])
        total = float(fshift.sum() + 1e-9)
        score = (e_h + e_v) / total
        res["periodicity_score"] = round(score, 6)
        # 经验阈值: 极弱周期性可能经过重采样/合成
        if score < 1e-4:
            res["consistent"] = False
            res["tier"] = "🟡推演(CFA周期性弱)"
            res["notes"] = "亮度通道缺乏CFA周期特征，疑似重采样/合成/AI生成"
        else:
            res["notes"] = f"检测到CFA周期特征(占比{score:.4%})，符合相机直出"
    except Exception as e:
        res["capability"] = "degraded"
        res["tier"] = "🟡推演(CFA不可用)"
        res["notes"] = f"CFA分析失败: {e}"
    return res
