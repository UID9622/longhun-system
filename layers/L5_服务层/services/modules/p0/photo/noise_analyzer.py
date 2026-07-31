# DNA: #龍芯⚡️丙午·乙未·乙丑·同人-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# -*- coding: utf-8 -*-
"""
龍魂P0 · 噪声一致性分析

原理: 自然图像各区域噪声特征(方差/均值)应一致；合成/替换区域噪声统计偏离。
能力: 真实(numpy/scipy)。将图像分块，统计每块噪声(高频残差)方差，
偏离整体分布即标异常。
返回: {"capability","tier","block_std_mean","block_std_std","outlier_ratio","notes"}
DNA #龍魂⚡️丙午·辛未·P0-NOISE-v1
"""

import io
import numpy as np
from PIL import Image
from scipy import ndimage


def noise_consistency(img_bytes: bytes, grid: int = 8) -> dict[str, Any]:
    res = {"capability": "real", "tier": "🟢真实(噪声一致)",
           "block_std_mean": 0.0, "block_std_std": 0.0, "outlier_ratio": 0.0,
           "notes": ""}
    try:
        im = np.asarray(Image.open(io.BytesIO(img_bytes)).convert("L"), dtype=np.float32)
        # 高频残差 = 原图 - 高斯平滑
        smooth = ndimage.gaussian_filter(im, sigma=2.0)
        residual = np.abs(im - smooth)
        h, w = residual.shape
        gh, gw = h // grid, w // grid
        stds = []
        for i in range(grid):
            for j in range(grid):
                block = residual[i*gh:(i+1)*gh, j*gw:(j+1)*gw]
                stds.append(float(block.std()))
        stds = np.array(stds)
        mean, std = float(stds.mean()), float(stds.std())
        outlier = float(((stds > mean + 2*std) | (stds < mean - 2*std)).mean())
        res["block_std_mean"] = round(mean, 4)
        res["block_std_std"] = round(std, 4)
        res["outlier_ratio"] = round(outlier, 4)
        if outlier > 0.15:
            res["tier"] = "🟡推演(噪声不一致)"
            res["notes"] = f"分块噪声异常占比{outlier*100:.1f}%，疑似区域合成/替换"
        else:
            res["notes"] = f"各区域噪声特征一致(异常{outlier*100:.1f}%)"
    except Exception as e:
        res["capability"] = "degraded"
        res["tier"] = "🟡推演(噪声分析不可用)"
        res["notes"] = f"噪声分析失败: {e}"
    return res
