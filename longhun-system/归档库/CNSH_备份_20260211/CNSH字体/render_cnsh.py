# CNSH 字元渲染器 · UID9622
# DNA: #ZHUGEXIN⚡️-CNSH-RENDERER-0001

import json
import os

class CNSH字元渲染器_UID9622:
    def __init__(self):
        self.字元集_cnsh9622 = {}

    def 载入_cnsh定义_cnsh龍魂_v1(self, 文件路径_cnsh9622):
        with open(文件路径_cnsh9622, "r", encoding="utf-8") as f:
            数据 = json.load(f)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        print(f"✅ 加载字元集: {list(self.字元集_cnsh9622.keys())}")

    def 三次贝塞尔点_cnsh9622(self, t, P0, P1, P2, P3):
        x = (1-t)**3*P0[0] + 3*(1-t)**2*t*P1[0] + 3*(1-t)*t**2*P2[0] + t**3*P3[0]
        y = (1-t)**3*P0[1] + 3*(1-t)**2*t*P1[1] + 3*(1-t)*t**2*P2[1] + t**3*P3[1]
        return x, y

    def 输出SVG_cnsh龍魂_v1(self, 字符, 输出路径_cnsh9622):
        if 字符 not in self.字元集_cnsh9622:
            print(f"❌ 字符不存在: {字符}")
            return

        笔画 = self.字元集_cnsh9622[字符]["笔画路径_cnsh9622"]
        路径 = ""
        当前点 = None

        for 动作 in 笔画:
            if 动作["类型"] == "移动到":
                x, y = 动作["坐标"]
                路径 += f"M {x} {y} "
                当前点 = (x, y)
            elif 动作["类型"] == "直线段":
                x, y = 动作["终点"]
                路径 += f"L {x} {y} "
                当前点 = (x, y)
            elif 动作["类型"] == "三次曲线":
                P0 = 当前点
                P1, P2, P3 = 动作["控制点"]
                路径 += f"C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]} "
                当前点 = P3

        svg = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <rect width="100%" height="100%" fill="white"/>
  <path d="{路径}" fill="none" stroke="black" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>"""

        with open(输出路径_cnsh9622, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"✅ {字符} → {输出路径_cnsh9622}")

# 执行
if __name__ == "__main__":
    渲染器 = CNSH字元渲染器_UID9622()
    渲染器.载入_cnsh定义_cnsh龍魂_v1("demo_long.cnsh")
    
    for 字符 in ["龍", "中", "华", "民", "魂"]:
        输出文件 = f"CNSH_字元_{字符}_output.svg"
        渲染器.输出SVG_cnsh龍魂_v1(字符, 输出文件)
