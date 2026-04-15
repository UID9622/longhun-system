# 来源标注: #ZHUGEXIN⚡️ | UID9622 龍魂体系
import json
import os

class CNSH字元排版引擎_UID9622:
    def __init__(self):
        self.字元集_cnsh9622 = {}
        self.审计_cnsh9622 = {}
        self.排版规则_cnsh9622 = {}

    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622):
        with open(路径_cnsh9622, "r", encoding="utf-8") as 文件:
            数据 = json.load(文件)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        self.审计_cnsh9622 = 数据["三色审计_cnsh9622"]
        self.排版规则_cnsh9622 = 数据.get("排版规则_cnsh9622", {})

    def 执行三色审计_cnsh龍魂_v1(self):
        for 颜色 in self.审计_cnsh9622:
            if self.审计_cnsh9622[颜色]["结果"] != "通过":
                raise RuntimeError(f"三色审计未通过: {颜色}")

    def 输出SVG_cnsh龍魂_v1(self, 输出路径_cnsh9622):
        所有路径 = []
        for 字元名 in self.字元集_cnsh9622:
            字元数据 = self.字元集_cnsh9622[字元名]
            笔画列表 = sorted(字元数据["笔画路径_cnsh9622"], key=lambda x: x.get("层级", 0))
            当前点 = None
            for 动作 in 笔画列表:
                if 动作["类型"] == "移动到":
                    当前点 = 动作["坐标"]
                elif 动作["类型"] == "直线段":
                    终点 = 动作["终点"]
                    力度 = 动作.get("力度", 12)
                    所有路径.append(
                        f'<path d="M {当前点[0]} {当前点[1]} L {终点[0]} {终点[1]}" '
                        f'fill="none" stroke="black" stroke-width="{力度}" stroke-linecap="square"/>'
                    )
                    当前点 = 终点
                elif 动作["类型"] == "三次曲线":
                    P1, P2, P3 = 动作["控制点"]
                    力度 = 动作.get("力度", 12)
                    所有路径.append(
                        f'<path d="M {当前点[0]} {当前点[1]} C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]}" '
                        f'fill="none" stroke="black" stroke-width="{力度}" stroke-linecap="square"/>'
                    )
                    当前点 = P3

        svg内容 = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600">
{''.join(所有路径)}
</svg>'''
        with open(输出路径_cnsh9622, "w", encoding="utf-8") as 文件:
            文件.write(svg内容)

    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622):
        self.执行三色审计_cnsh龍魂_v1()
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        self.输出SVG_cnsh龍魂_v1(os.path.join(输出目录_cnsh9622, "碑文_龍中华民魂.svg"))

if __name__ == "__main__":
    引擎 = CNSH字元排版引擎_UID9622()
    引擎.载入_cnsh数据_cnsh龍魂_v1("/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/CNSH_字元库_v0013.json")
    引擎.执行渲染_cnsh龍魂_v1("/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/CNSH_字元库_输出_v0013")
    print("✓ v0013 多字排版层完成")
