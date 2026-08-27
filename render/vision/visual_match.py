# DNA: #龍芯⚡️2026-08-25-RENDER-ENV-v1.0-UID9622
# 创建者: 诸葛鑫（UID9622）
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""视觉模板匹配 · cv2（截图内找模板，返回坐标+置信度）。"""


def match_template(screenshot_bytes: bytes, template_path: str,
                   threshold: float = 0.8) -> dict:
    try:
        import cv2
        import numpy as np
    except ImportError:
        return {"found": False, "error": "opencv 未安装"}

    nparr = np.frombuffer(screenshot_bytes, np.uint8)
    screen = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    template = cv2.imread(template_path)
    if screen is None or template is None:
        return {"found": False, "error": "截图或模板读取失败"}
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if float(max_val) >= threshold:
        h, w = template.shape[:2]
        return {"found": True, "x": int(max_loc[0]), "y": int(max_loc[1]),
                "w": int(w), "h": int(h), "score": round(float(max_val), 4),
                "center": [int(max_loc[0] + w // 2), int(max_loc[1] + h // 2)]}
    return {"found": False, "score": round(float(max_val), 4)}
