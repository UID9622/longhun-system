# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂P0 · 克隆/复制粘贴检测

原理: 篡改常复制图像某块粘贴到另一处遮盖物体。检测重复像素块(归一化互相关系数)。
能力: 真实(numpy)。滑窗提取小块，做块间相似度比对，超阈值即标疑似克隆。
返回: {"capability","tier","clone_pairs","max_corr","notes"}
DNA #龍魂⚡️丙午·辛未·P0-CLONE-v1
"""

import io
import numpy as np
from PIL import Image


def clone_detect(img_bytes: bytes, block: int = 32, stride: int = 8,
                 corr_thr: float = 0.92, max_pairs: int = 50) -> dict[str, Any]:
    res = {"capability": "real", "tier": "🟢真实(未检出克隆)",
           "clone_pairs": 0, "max_corr": 0.0, "notes": ""}
    try:
        gray = np.asarray(Image.open(io.BytesIO(img_bytes)).convert("L"), dtype=np.float32)
        h, w = gray.shape
        # 抽取归一化块向量
        blocks = []
        coords = []
        for y in range(0, h - block, stride):
            for x in range(0, w - block, stride):
                patch = gray[y:y+block, x:x+block]
                p = (patch - patch.mean()) / (patch.std() + 1e-6)
                blocks.append(p.ravel())
                coords.append((x, y))
        if len(blocks) < 2:
            res["notes"] = "图像过小，跳过克隆检测"
            return res
        B = np.array(blocks)
        n = len(B)
        # 全量比对(块数受控时)；过大则抽样但保证覆盖
        idx = list(range(n))
        if n > 1200:
            rng = np.random.default_rng(0)
            idx = sorted(rng.choice(n, size=1200, replace=False).tolist())
        pairs = 0
        maxc = 0.0
        for ii in range(len(idx)):
            for jj in range(ii+1, len(idx)):
                a, b = idx[ii], idx[jj]
                if abs(coords[a][0]-coords[b][0]) < block and abs(coords[a][1]-coords[b][1]) < block:
                    continue  # 相邻块跳过
                c = float(np.dot(B[a], B[b]) / (np.linalg.norm(B[a])*np.linalg.norm(B[b]) + 1e-6))
                if c > maxc:
                    maxc = c
                if c > corr_thr:
                    pairs += 1
                    if pairs >= max_pairs:
                        break
            if pairs >= max_pairs:
                break
        res["clone_pairs"] = pairs
        res["max_corr"] = round(maxc, 4)
        if pairs > 0:
            res["tier"] = "🟡推演(检出疑似克隆块)"
            res["notes"] = f"检出{pairs}组高相似复制块(最大相关{maxc:.2f})，疑似复制粘贴遮盖"
        else:
            res["notes"] = f"未检出高相似复制块(最大相关{maxc:.2f})"
    except Exception as e:
        res["capability"] = "degraded"
        res["tier"] = "🟡推演(克隆检测不可用)"
        res["notes"] = f"克隆检测失败: {e}"
    return res
