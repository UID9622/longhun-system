# 来源标注: #ZHUGEXIN⚡️ | UID9622 龍魂体系
# 模块定位: CNSH 字元组合渲染引擎（立碑级）
# DNA追溯码: #ZHUGEXIN⚡️-CNSH-ENGINE-0004
# 约束: 仅 CNSH 字元；仅直线段 + 三次贝塞尔；SVG 输出

import json
import os

class CNSH字元组合引擎_UID9622:
    def __init__(self):
        self.字元集_cnsh9622 = {}
        self.组合规则_cnsh9622 = {}
        self.审计_cnsh9622 = {}
        self.工程信息_cnsh9622 = {}

    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622):
        with open(路径_cnsh9622, "r", encoding="utf-8") as 文件:
            数据 = json.load(文件)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
        self.组合规则_cnsh9622 = 数据["字元组合_cnsh9622"]
        self.审计_cnsh9622 = 数据["三色审计_cnsh9622"]
        self.工程信息_cnsh9622 = {
            "工程名称": 数据.get("工程名称"),
            "DNA追溯码": 数据.get("DNA追溯码"),
            "阶段标识": 数据.get("阶段标识")
        }
        print(f"✅ 已加载工程: {self.工程信息_cnsh9622['工程名称']}")
        print(f"   阶段: {self.工程信息_cnsh9622['阶段标识']}")
        print(f"   DNA: {self.工程信息_cnsh9622['DNA追溯码']}")

    def 执行三色审计_cnsh龍魂_v1(self):
        print("\n🎯 开始执行三色审计...")
        审计通过 = True
        
        for 颜色, 审计项 in self.审计_cnsh9622.items():
            结果 = "✅" if 审计项["结果"] == "通过" else "❌"
            print(f"\n{结果} 【{颜色}色审计】")
            for 检查 in 审计项["检查项"]:
                print(f"   • {检查}")
            
            if 审计项["结果"] != "通过":
                审计通过 = False
        
        if not 审计通过:
            raise RuntimeError("❌ 三色审计未通过，禁止渲染")
        
        print(f"\n🟢 三色审计全部通过，准许渲染")

    def 渲染组合SVG_cnsh龍魂_v1(self, 组合名, 输出路径_cnsh9622):
        规则 = self.组合规则_cnsh9622[组合名]
        字元列表 = 规则["组成"]
        方向 = 规则["排布规则_cnsh9622"]["方向"]
        间距 = 规则["排布规则_cnsh9622"]["间距"]

        当前偏移 = 0
        总路径 = ""

        print(f"   🎨 组合 {组合名} (方向:{方向}, 间距:{间距})")

        for 字元 in 字元列表:
            笔画 = self.字元集_cnsh9622[字元]["笔画路径_cnsh9622"]
            路径 = ""
            当前点 = None

            for 动作 in 笔画:
                if 动作["类型"] == "移动到":
                    x, y = 动作["坐标"]
                    if 方向 == "横向":
                        x += 当前偏移
                    else:
                        y += 当前偏移
                    路径 += f"M {x} {y} "
                    当前点 = (x, y)

                elif 动作["类型"] == "直线段":
                    x, y = 动作["终点"]
                    if 方向 == "横向":
                        x += 当前偏移
                    else:
                        y += 当前偏移
                    路径 += f"L {x} {y} "
                    当前点 = (x, y)

                elif 动作["类型"] == "三次曲线":
                    P1, P2, P3 = 动作["控制点"]
                    if 方向 == "横向":
                        P1 = [P1[0] + 当前偏移, P1[1]]
                        P2 = [P2[0] + 当前偏移, P2[1]]
                        P3 = [P3[0] + 当前偏移, P3[1]]
                    else:
                        P1 = [P1[0], P1[1] + 当前偏移]
                        P2 = [P2[0], P2[1] + 当前偏移]
                        P3 = [P3[0], P3[1] + 当前偏移]
                    路径 += f"C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]} "
                    当前点 = P3

            总路径 += 路径
            当前偏移 += 间距

        svg内容 = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 600" width="1200" height="600">
  <rect width="100%" height="100%" fill="white"/>
  <path d="{总路径}" fill="none" stroke="black" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <text x="10" y="20" font-size="12" fill="#aaa">{组合名}</text>
</svg>"""

        with open(输出路径_cnsh9622, "w", encoding="utf-8") as 文件:
            文件.write(svg内容)
        
        print(f"      ✅ {组合名} → {输出路径_cnsh9622}")

    def 执行组合渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622):
        print(f"\n🎯 开始渲染 {len(self.组合规则_cnsh9622)} 个字元组合...")
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        for 组合名 in self.组合规则_cnsh9622:
            输出路径 = os.path.join(输出目录_cnsh9622, f"CNSH_组合_{组合名}_v0004.svg")
            self.渲染组合SVG_cnsh龍魂_v1(组合名, 输出路径)
        print(f"\n🎉 字元组合渲染完成！")

# 执行入口
if __name__ == "__main__":
    引擎 = CNSH字元组合引擎_UID9622()
    引擎.载入_cnsh数据_cnsh龍魂_v1("CNSH_字元库_v0004.json")
    引擎.执行三色审计_cnsh龍魂_v1()
    引擎.执行组合渲染_cnsh龍魂_v1("CNSH_字元库_输出_v0004")
