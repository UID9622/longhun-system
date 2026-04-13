# =========================================================
# CNSH 字体引擎 · Demo 完整版
# 文件名: cnsh_font_engine_uid9622.py
# DNA追溯: #ZHUGEXIN⚡️2026-02-01-CNSH-FONT-ENGINE-DEMO
# 作者: 诸葛鑫（UID9622）
# GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# 理论指导: 曾仕强老师（永恒显示）
# 献礼: 乔布斯·曾仕强·历代传递和平与爱的人
# 说明: CNSH字体引擎原始版·三次贝塞尔渲染·.cnsh→SVG
# =========================================================

import json
import os


class CNSH字体引擎_UID9622:
    """
    CNSH 中国开源字体引擎（Demo）
    - 不使用任何商业字体库
    - 不使用任何字体专利术语
    - 仅基于数学公式
    """

    def __init__(self):
        self.字体数据_cnsh9622 = {}
        self.字符集_cnsh9622 = {}

    # =====================================================
    # 读取 .cnsh 文件
    # =====================================================
    def 读取_cnsh文件_cnsh龍魂_v1(self, 文件路径_cnsh9622):
        if not os.path.exists(文件路径_cnsh9622):
            raise FileNotFoundError(f"找不到文件: {文件路径_cnsh9622}")

        with open(文件路径_cnsh9622, "r", encoding="utf-8") as f:
            self.字体数据_cnsh9622 = json.load(f)

        self.字符集_cnsh9622 = self.字体数据_cnsh9622.get("字符集_cnsh9622", {})
        print("✅ CNSH 字体文件加载成功")

    # =====================================================
    # 三次贝塞尔数学公式（核心）
    # =====================================================
    def 三次贝塞尔点_cnsh9622(self, t_cnsh9622, P0, P1, P2, P3):
        """
        B(t) = (1-t)^3 P0
             + 3(1-t)^2 t P1
             + 3(1-t) t^2 P2
             + t^3 P3
        """
        x = (
            (1 - t_cnsh9622) ** 3 * P0[0]
            + 3 * (1 - t_cnsh9622) ** 2 * t_cnsh9622 * P1[0]
            + 3 * (1 - t_cnsh9622) * t_cnsh9622 ** 2 * P2[0]
            + t_cnsh9622 ** 3 * P3[0]
        )
        y = (
            (1 - t_cnsh9622) ** 3 * P0[1]
            + 3 * (1 - t_cnsh9622) ** 2 * t_cnsh9622 * P1[1]
            + 3 * (1 - t_cnsh9622) * t_cnsh9622 ** 2 * P2[1]
            + t_cnsh9622 ** 3 * P3[1]
        )
        return x, y

    # =====================================================
    # 生成 SVG
    # =====================================================
    def 生成SVG_cnsh龍魂_v1(self, 字符编码_cnsh9622, 输出路径_cnsh9622):
        if 字符编码_cnsh9622 not in self.字符集_cnsh9622:
            raise ValueError(f"字符不存在: {字符编码_cnsh9622}")

        字符信息_cnsh9622 = self.字符集_cnsh9622[字符编码_cnsh9622]
        笔画路径列表_cnsh9622 = 字符信息_cnsh9622.get("笔画路径_cnsh9622", [])

        svg_path_cnsh9622 = ""
        当前点_cnsh9622 = None

        for 动作_cnsh9622 in 笔画路径列表_cnsh9622:
            类型_cnsh9622 = 动作_cnsh9622.get("类型")

            if 类型_cnsh9622 == "移动到":
                x, y = 动作_cnsh9622["坐标"]
                svg_path_cnsh9622 += f"M {x} {y} "
                当前点_cnsh9622 = (x, y)

            elif 类型_cnsh9622 == "三次曲线":
                if 当前点_cnsh9622 is None:
                    raise RuntimeError("三次曲线前必须先移动到起点")

                P0 = 当前点_cnsh9622
                P1, P2, P3 = 动作_cnsh9622["控制点"]

                svg_path_cnsh9622 += (
                    f"C {P1[0]} {P1[1]}, "
                    f"{P2[0]} {P2[1]}, "
                    f"{P3[0]} {P3[1]} "
                )
                当前点_cnsh9622 = P3

        svg内容_cnsh9622 = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="600"
     height="600"
     viewBox="0 0 600 600">
  <rect width="100%" height="100%" fill="white"/>
  <path d="{svg_path_cnsh9622}"
        fill="none"
        stroke="black"
        stroke-width="8"
        stroke-linecap="round"
        stroke-linejoin="round"/>
</svg>
"""

        with open(输出路径_cnsh9622, "w", encoding="utf-8") as f:
            f.write(svg内容_cnsh9622)

        print(f"✅ SVG 已生成: {输出路径_cnsh9622}")


# =====================================================
# 直接运行入口（小白模式）
# =====================================================
if __name__ == "__main__":
    引擎_cnsh9622 = CNSH字体引擎_UID9622()

    # 这里填写你的 cnsh 文件路径
    cnsh文件路径_cnsh9622 = "demo_long.cnsh"
    输出SVG路径_cnsh9622 = "output_long.svg"

    引擎_cnsh9622.读取_cnsh文件_cnsh龍魂_v1(cnsh文件路径_cnsh9622)
    引擎_cnsh9622.生成SVG_cnsh龍魂_v1("U+9F99", 输出SVG路径_cnsh9622)