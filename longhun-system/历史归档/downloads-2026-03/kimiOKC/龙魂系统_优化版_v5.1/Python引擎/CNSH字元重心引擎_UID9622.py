import json, os

class CNSH字元重心引擎_UID9622:
    def __init__(self):
        self.字元集 = {}
        self.审计 = {}

    def 载入(self, 路径):
        with open(路径,"r",encoding="utf-8") as f:
            数据=json.load(f)
        self.字元集=数据["字符集_cnsh9622"]
        self.审计=数据["三色审计_cnsh9622"]

    def 审计检查(self):
        for k in self.审计:
            if self.审计[k]["结果"]!="通过":
                raise RuntimeError("三色审计未通过")

    def 输出SVG(self, 字元, 输出):
        笔画=sorted(self.字元集[字元]["笔画路径_cnsh9622"],key=lambda x:x.get("层级",0))
        当前=None
        片段=[]
        for 动作 in 笔画:
            偏移=动作.get("偏移",[0,0])
            if 动作["类型"]=="移动到":
                当前=[动作["坐标"][0]+偏移[0],动作["坐标"][1]+偏移[1]]
            elif 动作["类型"]=="直线段":
                终点=[动作["终点"][0]+偏移[0],动作["终点"][1]+偏移[1]]
                片段.append(
                    f'<path d="M {当前[0]} {当前[1]} L {终点[0]} {终点[1]}" stroke="black" stroke-width="{动作.get("力度",12)}" fill="none"/>'
                )
                当前=终点
        with open(输出,"w",encoding="utf-8") as f:
            f.write(f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 600 600'>{''.join(片段)}</svg>")

    def 执行(self, 输出目录):
        self.审计检查()
        os.makedirs(输出目录,exist_ok=True)
        for 字元 in self.字元集:
            self.输出SVG(字元,os.path.join(输出目录,f"{字元}.svg"))

if __name__=="__main__":
    引擎=CNSH字元重心引擎_UID9622()
    引擎.载入("/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/CNSH_字元库_v0011.json")
    引擎.执行("/Users/zuimeidedeyihan/Desktop/CNSH 军人的编辑器/CNSH_字元库_输出_v0011/")
    print("✓ v0011 三色审计通过")
    print("✓ 字元重心偏移 SVG 已生成")
