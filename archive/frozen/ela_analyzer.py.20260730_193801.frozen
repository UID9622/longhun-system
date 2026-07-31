# -*- coding: utf-8 -*-
"""
龍魂P0 · ELA错误级别分析(Error Level Analysis)

原理: 对图像以固定质量重新保存(JPEG)，与原图做差；篡改区域(复制/拼接/重采样)
因压缩率不一致而高亮。
能力: 真实(numpy/PIL)。返回异常区域占比与风险评分(0-1)。
返回: {"capability","tier","ela_score","anomaly_ratio","notes"}
DNA #龍魂⚡️丙午·辛未·P0-ELA-v1
"""

import io
import numpy as np
from PIL import Image, ImageChops


def ela(img_bytes: bytes, quality: int = 90) -> dict[str, Any]:
    res = {"capability": "real", "tier": "🟢真实(ELA正常)",
           "ela_score": 0.0, "anomaly_ratio": 0.0, "notes": ""}
    try:
        im = Image.open(io.BytesIO(img_bytes)).convert("RGB")
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=quality)
        recompressed = Image.open(io.BytesIO(buf.getvalue())).convert("RGB")
        diff = ImageChops.difference(im, recompressed)
        diff_arr = np.asarray(diff, dtype=np.float32)
        # 各像素平均误差
        err = diff_arr.mean(axis=2)
        mean_err = float(err.mean())
        std_err = float(err.std())
        # 异常: 误差显著偏离(> mean+2std 视为疑似篡改区)
        thr = mean_err + 2.0 * (std_err + 1e-6)
        anomaly = (err > thr).mean()
        res["ela_score"] = round(min(1.0, mean_err / 30.0), 4)
        res["anomaly_ratio"] = round(float(anomaly), 4)
        if anomaly > 0.05:
            res["tier"] = "🟡推演(ELA异常区偏高)"
            res["notes"] = f"检出异常误差区域占比{anomaly*100:.1f}%，疑似复制/拼接/重采样，建议人工复核"
        else:
            res["notes"] = f"误差分布均匀(异常区{anomaly*100:.2f}%)，未见明显篡改"
    except Exception as e:
        res["capability"] = "degraded"
        res["tier"] = "🟡推演(ELA不可用)"
        res["notes"] = f"ELA分析失败(可能非JPEG/格式不支持): {e}"
    return res
