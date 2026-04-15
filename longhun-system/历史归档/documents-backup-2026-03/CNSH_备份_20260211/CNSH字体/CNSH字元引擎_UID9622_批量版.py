# 来源标注: #ZHUGEXIN⚡️ | UID9622 龍魂体系
# 模块定位: CNSH 字元批量渲染核心
# DNA追溯码: #ZHUGEXIN⚡️-CNSH-ENGINE-0002
# 约束: 仅直线段 + 三次贝塞尔；SVG 输出；无英文术语

import json
import os

class CNSH字元引擎_UID9622:
    def __init__(self):
        self.字元集_cnsh9622 = {}

    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622):
        with open(路径_cnsh9622, "r", encoding="utf-8") as 文件:
            数据 = json.load(文件)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        print(f"✅ 已加载 {len(self.字元集_cnsh9622)} 个字元")

    def 输出单字SVG_cnsh龍魂_v1(self, 字元, 输出目录_cnsh9622):
        if 字元 not in self.字元集_cnsh9622:
            print(f"❌ 字元不存在: {字元}")
            return

        笔画 = self.字元集_cnsh9622[字元]["笔画路径_cnsh9622"]
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
                P1, P2, P3 = 动作["控制点"]
                路径 += f"C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]} "
                当前点 = P3

        svg内容 = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <rect width="100%" height="100%" fill="white"/>
  <path d="{路径}" fill="none" stroke="black" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="10" y="20" font-size="12" fill="#888">{字元}</text>
</svg>"""

        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        输出文件 = os.path.join(输出目录_cnsh9622, f"CNSH_字元_{字元}_v0002.svg")
        with open(输出文件, "w", encoding="utf-8") as 文件:
            文件.write(svg内容)
        print(f"✅ {字元} → {输出文件}")

    def 批量渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622):
        print(f"\n🎯 开始批量渲染到: {输出目录_cnsh9622}")
        for 字元 in self.字元集_cnsh9622:
            self.输出单字SVG_cnsh龍魂_v1(字元, 输出目录_cnsh9622)
        print(f"\n🎉 批量渲染完成！")

# 执行入口
if __name__ == "__main__":
    引擎 = CNSH字元引擎_UID9622()
    引擎.载入_cnsh数据_cnsh龍魂_v1("CNSH_字元库_v0002.json")
    引擎.批量渲染_cnsh龍魂_v1("CNSH_字元库_输出_v0002")
