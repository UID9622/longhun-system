# 来源标注: #ZHUGEXIN⚡️ | UID9622 龍魂体系
# 模块定位: CNSH 字元渲染引擎 · 基础三次贝塞尔层

import json
import os

class CNSH字元基础引擎_UID9622:
    def __init__(self):
        self.字元集_cnsh9622 = {}
        self.审计_cnsh9622 = {}

    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622):
        with open(路径_cnsh9622, "r", encoding="utf-8") as 文件:
            数据 = json.load(文件)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        self.审计_cnsh9622 = 数据["三色审计_cnsh9622"]

    def 执行三色审计_cnsh龍魂_v1(self):
        for 颜色 in self.审计_cnsh9622:
            if self.审计_cnsh9622[颜色]["结果"] != "通过":
                raise RuntimeError("三色审计未通过")

    def 输出SVG_cnsh龍魂_v1(self, 字元, 输出路径_cnsh9622):
        笔画列表 = self.字元集_cnsh9622[字元]["笔画路径_cnsh9622"]
        路径片段 = []
        当前点 = None

        for 动作 in 笔画列表:
            if 动作["类型"] == "移动到":
                当前点 = 动作["坐标"]
            elif 动作["类型"] == "直线段":
                终点 = 动作["终点"]
                路径片段.append(
                    f'<path d="M {当前点[0]} {当前点[1]} L {终点[0]} {终点[1]}" '
                    f'fill="none" stroke="black" stroke-width="12" '
                    f'stroke-linecap="butt" stroke-linejoin="miter"/>'
                )
                当前点 = 终点
            elif 动作["类型"] == "三次曲线":
                P1, P2, P3 = 动作["控制点"]
                路径片段.append(
                    f'<path d="M {当前点[0]} {当前点[1]} '
                    f'C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]}" '
                    f'fill="none" stroke="black" stroke-width="12" '
                    f'stroke-linecap="butt" stroke-linejoin="miter"/>'
                )
                当前点 = P3

        svg内容 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600">
{''.join(路径片段)}
</svg>"""

        with open(输出路径_cnsh9622, "w", encoding="utf-8") as 文件:
            文件.write(svg内容)

    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622):
        self.执行三色审计_cnsh龍魂_v1()
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        for 字元 in self.字元集_cnsh9622:
            self.输出SVG_cnsh龍魂_v1(
                字元,
                os.path.join(输出目录_cnsh9622, f"{字元}.svg")
            )

if __name__ == "__main__":
    引擎 = CNSH字元基础引擎_UID9622()
    引擎.载入_cnsh数据_cnsh龍魂_v1("CNSH_字元库_v0002.json")
    引擎.执行渲染_cnsh龍魂_v1("CNSH_字元库_输出_v0002")
    print("✓ v0002 三色审计通过")
    print("✓ 5个字的 SVG 文件已生成")
