# 来源标注: #ZHUGEXIN⚡️ | UID9622 龍魂体系
# 模块定位: CNSH 字元渲染引擎 · 笔画纹理与石刻质感执行层

import json
import os
import random

class CNSH字元纹理引擎_UID9622:
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

    def 侵蚀扰动_cnsh9622(self, 数值, 强度):
        偏移 = (random.random() - 0.5) * 强度 * 40
        return 数值 + 偏移

    def 生成纹理滤镜_cnsh9622(self, 纹理类型):
        """生成 SVG 滤镜定义"""
        if 纹理类型 == "粗糙":
            return """<filter id="纹理_粗糙">
  <feTurbulence type="fractalNoise" baseFrequency="0.05" numOctaves="3" seed="1"/>
  <feDisplacementMap in="SourceGraphic" scale="3"/>
</filter>"""
        elif 纹理类型 == "石刻":
            return """<filter id="纹理_石刻">
  <feTurbulence type="fractalNoise" baseFrequency="0.1" numOctaves="4" seed="2"/>
  <feDisplacementMap in="SourceGraphic" scale="5"/>
  <feGaussianBlur stdDeviation="0.5"/>
</filter>"""
        else:  # 光滑
            return """<filter id="纹理_光滑">
  <feGaussianBlur stdDeviation="0.3"/>
</filter>"""

    def 输出SVG_cnsh龍魂_v1(self, 字元, 输出路径_cnsh9622):
        笔画列表 = sorted(
            self.字元集_cnsh9622[字元]["笔画路径_cnsh9622"],
            key=lambda x: x.get("层级", 0)
        )

        # 收集所有纹理类型
        纹理集合 = set()
        for 动作 in 笔画列表:
            if "纹理" in 动作:
                纹理集合.add(动作["纹理"])

        # 生成滤镜定义
        滤镜定义 = "\n".join(self.生成纹理滤镜_cnsh9622(纹理) for 纹理 in 纹理集合)

        路径片段 = []
        当前点 = None

        for 动作 in 笔画列表:
            if 动作["类型"] == "移动到":
                当前点 = 动作["坐标"]

            elif 动作["类型"] == "直线段":
                终点 = 动作["终点"]
                力度 = 动作.get("力度", 12)
                侵蚀 = 动作.get("侵蚀", 0)
                纹理 = 动作.get("纹理", "光滑")
                
                x1 = self.侵蚀扰动_cnsh9622(当前点[0], 侵蚀)
                y1 = self.侵蚀扰动_cnsh9622(当前点[1], 侵蚀)
                x2 = self.侵蚀扰动_cnsh9622(终点[0], 侵蚀)
                y2 = self.侵蚀扰动_cnsh9622(终点[1], 侵蚀)
                
                路径片段.append(
                    f'<path d="M {x1} {y1} L {x2} {y2}" '
                    f'fill="none" stroke="black" stroke-width="{力度}" '
                    f'stroke-linecap="butt" stroke-linejoin="miter" '
                    f'filter="url(#纹理_{纹理})"/>'
                )
                当前点 = 终点

            elif 动作["类型"] == "三次曲线":
                P1, P2, P3 = 动作["控制点"]
                力度 = 动作.get("力度", 12)
                侵蚀 = 动作.get("侵蚀", 0)
                纹理 = 动作.get("纹理", "光滑")
                
                P1x = self.侵蚀扰动_cnsh9622(P1[0], 侵蚀)
                P1y = self.侵蚀扰动_cnsh9622(P1[1], 侵蚀)
                P2x = self.侵蚀扰动_cnsh9622(P2[0], 侵蚀)
                P2y = self.侵蚀扰动_cnsh9622(P2[1], 侵蚀)
                P3x = self.侵蚀扰动_cnsh9622(P3[0], 侵蚀)
                P3y = self.侵蚀扰动_cnsh9622(P3[1], 侵蚀)
                
                路径片段.append(
                    f'<path d="M {当前点[0]} {当前点[1]} '
                    f'C {P1x} {P1y}, {P2x} {P2y}, {P3x} {P3y}" '
                    f'fill="none" stroke="black" stroke-width="{力度}" '
                    f'stroke-linecap="butt" stroke-linejoin="miter" '
                    f'filter="url(#纹理_{纹理})"/>'
                )
                当前点 = P3

        svg内容 = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600">
<defs>
{滤镜定义}
</defs>
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
    引擎 = CNSH字元纹理引擎_UID9622()
    引擎.载入_cnsh数据_cnsh龍魂_v1("CNSH_字元库_v0011.json")
    引擎.执行渲染_cnsh龍魂_v1("CNSH_字元库_输出_v0011")
    print("✓ v0011 三色审计通过")
    print("✓ 5个字的 SVG 文件已生成（带纹理效果）")
