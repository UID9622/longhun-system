# 来源标注: #ZHUGEXIN⚡️ | UID9622 龍魂体系
# 模块定位: CNSH 字元渲染引擎 · 笔画层级执行层
# DNA追溯码: #ZHUGEXIN⚡️-CNSH-ENGINE-0008
# 约束: 仅 CNSH 字元；仅直线段 + 三次贝塞尔；SVG 输出

import json
import os

class CNSH字元层级引擎_UID9622:
    def __init__(self):
        self.字元集_cnsh9622 = {}
        self.审计_cnsh9622 = {}
        self.工程信息_cnsh9622 = {}

    def 载入_cnsh数据_cnsh龍魂_v1(self, 路径_cnsh9622):
        with open(路径_cnsh9622, "r", encoding="utf-8") as 文件:
            数据 = json.load(文件)
        self.字元集_cnsh9622 = 数据["字符集_cnsh9622"]
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
            raise RuntimeError("❌ 三色审计未通过，层级渲染被禁止")
        
        print(f"\n🟢 三色审计全部通过，准许笔画层级渲染")

    def 棱角参数_cnsh9622(self, 类型):
        """将棱角类型映射到 SVG 属性"""
        if 类型 == "断锋":
            return "butt", "miter"
        elif 类型 == "锐角":
            return "square", "miter"
        else:  # 平锋
            return "round", "bevel"

    def 输出SVG_cnsh龍魂_v1(self, 字元, 输出路径_cnsh9622):
        if 字元 not in self.字元集_cnsh9622:
            print(f"❌ 字元不存在: {字元}")
            return

        笔画列表 = self.字元集_cnsh9622[字元]["笔画路径_cnsh9622"]
        
        # 按层级排序笔画（低层级先绘制，高层级后绘制，后绘制的在前面）
        笔画列表_排序 = sorted(笔画列表, key=lambda x: x.get("层级", 0))
        
        路径片段 = []
        当前点 = None
        当前层级 = 0

        for 动作 in 笔画列表_排序:
            新层级 = 动作.get("层级", 当前层级)
            
            # 层级变化时，打印信息
            if 新层级 != 当前层级:
                当前层级 = 新层级

            if 动作["类型"] == "移动到":
                当前点 = 动作["坐标"]

            elif 动作["类型"] == "直线段":
                终点 = 动作["终点"]
                力度 = 动作.get("力度", 12)
                棱角 = 动作.get("棱角", "平锋")
                停顿 = 动作.get("停顿", 0)
                
                透明度 = max(0.2, 1 - 停顿)
                端点, 连接 = self.棱角参数_cnsh9622(棱角)
                
                路径片段.append(
                    f'<path d="M {当前点[0]} {当前点[1]} L {终点[0]} {终点[1]}" '
                    f'fill="none" stroke="black" stroke-width="{力度}" '
                    f'stroke-opacity="{透明度:.2f}" '
                    f'stroke-linecap="{端点}" stroke-linejoin="{连接}"/>'
                )
                当前点 = 终点

            elif 动作["类型"] == "三次曲线":
                P1, P2, P3 = 动作["控制点"]
                力度 = 动作.get("力度", 12)
                棱角 = 动作.get("棱角", "平锋")
                停顿 = 动作.get("停顿", 0)
                
                透明度 = max(0.2, 1 - 停顿)
                端点, 连接 = self.棱角参数_cnsh9622(棱角)
                
                路径片段.append(
                    f'<path d="M {当前点[0]} {当前点[1]} '
                    f'C {P1[0]} {P1[1]}, {P2[0]} {P2[1]}, {P3[0]} {P3[1]}" '
                    f'fill="none" stroke="black" stroke-width="{力度}" '
                    f'stroke-opacity="{透明度:.2f}" '
                    f'stroke-linecap="{端点}" stroke-linejoin="{连接}"/>'
                )
                当前点 = P3

        svg内容 = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 600" width="600" height="600">
  <rect width="100%" height="100%" fill="white"/>
  {''.join(路径片段)}
  <text x="10" y="20" font-size="12" fill="#aaa">{字元} - 层级版 v0008</text>
  <text x="10" y="590" font-size="10" fill="#ddd">笔画按层级排序：低层级在后，高层级在前</text>
</svg>"""

        with open(输出路径_cnsh9622, "w", encoding="utf-8") as 文件:
            文件.write(svg内容)
        print(f"✅ {字元} (层级渲染) → {输出路径_cnsh9622}")

    def 执行渲染_cnsh龍魂_v1(self, 输出目录_cnsh9622):
        print(f"\n🎯 开始笔画层级渲染 ({len(self.字元集_cnsh9622)} 个字元)...")
        os.makedirs(输出目录_cnsh9622, exist_ok=True)
        for 字元 in self.字元集_cnsh9622:
            输出路径 = os.path.join(输出目录_cnsh9622, f"CNSH_字元_{字元}_层级_v0008.svg")
            self.输出SVG_cnsh龍魂_v1(字元, 输出路径)
        print(f"\n🎉 笔画层级渲染完成！")

# 执行入口
if __name__ == "__main__":
    引擎 = CNSH字元层级引擎_UID9622()
    引擎.载入_cnsh数据_cnsh龍魂_v1("CNSH_字元库_v0008.json")
    引擎.执行三色审计_cnsh龍魂_v1()
    引擎.执行渲染_cnsh龍魂_v1("CNSH_字元库_输出_v0008")
