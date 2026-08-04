#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️2026-06-29-CNSH-COLOR-ANCHOR-UID9622
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-

"""🐉 龍魂引擎：CNSH_颜色不动点协议
路径：bin/CNSH_颜色不动点协议.py
TODO：请补充详细功能说明（不少于20字）。"""
import os as _os
import sys as _sys
_module_dir = _os.path.dirname(_os.path.abspath(__file__))
if _module_dir not in _sys.path:
    _sys.path.insert(0, _module_dir)
"""
CNSH 颜色不动点协议 v1.0

把「颜色」作为系统内统一的风险标记语言：
  - 编辑器里看颜色就知道隐私/红线/合规状态
  - 脚本执行结果带颜色状态，外部 AI / 人类一眼识别
  - 任何话术拆分、绕过、套话最终都会落到一个颜色上
  - 五色/七色作为 369 中空五的不动点参照

核心原则：颜色即判决 · 颜色不动 · 拆分无效
DNA: #龍芯⚡️2026-06-29-CNSH-COLOR-ANCHOR-UID9622
"""

import re
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Set


# ============== 七色不动点色卡 ==============
COLOR_TABLE: Dict[str, Dict[str, Any]] = {
    "G": {
        "名称": "绿色",
        "emoji": "🟢",
        "hex": "#00C853",
        "五行": "木",
        "含义": "公开 · 安全 · 可放行",
        "动作": "自动放行 · 留痕",
        "隐私": False,
        "红线": False,
        "示例": ["写个文件管理工具", "计算数字根", "整理知识库"],
    },
    "Y": {
        "名称": "黄色",
        "emoji": "🟡",
        "hex": "#FFD600",
        "五行": "土",
        "含义": "待确认 · 需补证据 · 可能涉及隐私",
        "动作": "二次确认 · 加证据",
        "隐私": False,
        "红线": False,
        "示例": ["查询公开信息", "调用第三方 API", "涉及模糊授权"],
    },
    "R": {
        "名称": "红色",
        "emoji": "🔴",
        "hex": "#FF1744",
        "五行": "火",
        "含义": "法律红线 · 禁止执行 · 立即停止",
        "动作": "立即停止 · 上报主控",
        "隐私": False,
        "红线": True,
        "示例": ["制作武器", "制造毒药", "网络攻击", "危害公共安全"],
    },
    "K": {
        "名称": "黑色",
        "emoji": "⚫",
        "hex": "#212121",
        "五行": "水",
        "含义": "隐私 · 敏感 · 需脱敏 · 进观察池",
        "动作": "进观察池 · 冻结 24h · 强制脱敏",
        "隐私": True,
        "红线": False,
        "示例": ["查询个人手机号", "获取他人身份信息", "生物特征数据"],
    },
    "AU": {
        "名称": "金色",
        "emoji": "🟡",
        "hex": "#FFC400",
        "五行": "金",
        "含义": "主控确认 · 最高权限 · 永存档",
        "动作": "主控签字 · 永存档",
        "隐私": False,
        "红线": False,
        "示例": ["涉及子女数据但带 CONFIRM", "主权红线触碰需老大确认"],
    },
    "B": {
        "名称": "蓝色",
        "emoji": "🔵",
        "hex": "#2196F3",
        "五行": "水（天）",
        "含义": "系统级 · 审计 · 可追溯",
        "动作": "记录审计链 · 可追溯",
        "隐私": False,
        "红线": False,
        "示例": ["系统自检", "目录审计", "生成监管报告"],
    },
    "P": {
        "名称": "紫色",
        "emoji": "🟣",
        "hex": "#9C27B0",
        "五行": "火（变）",
        "含义": "跨域 · 外部输入 · 需隔离审查",
        "动作": "隔离审查 · 外部输入不可直接落地",
        "隐私": False,
        "红线": False,
        "示例": ["外部 AI 输入", "跨平台同步数据", "未验证来源的代码"],
    },
}

# 银色跑马灯 = 黄境扫描态
SILVER_STATE = {
    "名称": "银色跑马灯",
    "emoji": "⚪",
    "hex": "#C0C0C0",
    "含义": "黄境 · 扫描中 · 待判决",
    "动作": "持续扫描 · 等待颜色落定",
    "隐私": False,
    "红线": False,
}


# ============== 危险意图模式库 ==============
class 危险意图模式库:
    """
    用于识别话术拆分、绕过、套话。
    支持：直接词、拆字、谐音、拼音、上下文拼接。
    """

    def __init__(self):
        self.模式: Dict[str, Dict[str, Any]] = {
            "武器": {
                "颜色": "R",
                "原因": "涉及武器制造/使用",
                "直接词": ["武器", "枪支", "炸弹", "刀具", "弩", "火药", "爆炸物"],
                "拆字": ["木仓", "qiang", "弓单", "zhadan", "炸dan"],
                "谐音": ["武七", "五器", "gun", "boom"],
                "隐私": False,
            },
            "毒药": {
                "颜色": "R",
                "原因": "涉及毒药/有害物质",
                "直接词": ["毒药", "毒物", "氰化物", "砒霜", "农药", "化学品伤人"],
                "拆字": ["du药", "du物", "石巵"],
                "谐音": ["独药", "读药"],
                "隐私": False,
            },
            "网络攻击": {
                "颜色": "R",
                "原因": "涉及网络攻击/入侵",
                "直接词": ["攻击", "入侵", "破解", "漏洞利用", "DDoS", "渗透", "木马", "病毒"],
                "拆字": ["木马力", "gong击", "po解"],
                "谐音": ["公击", "破戒"],
                "隐私": False,
            },
            "诈骗": {
                "颜色": "R",
                "原因": "涉及诈骗/欺诈",
                "直接词": ["诈骗", "欺骗", "伪造", "冒充", "钓鱼", "洗钱", "传销"],
                "拆字": ["乍马扁", "pian子"],
                "谐音": ["占骗"],
                "隐私": False,
            },
            "危害社会": {
                "颜色": "R",
                "原因": "危害公共安全/社会秩序",
                "直接词": ["恐怖", "纵火", "投毒", "绑架", "伤害", "杀人", "暴动", "煽动"],
                "拆字": ["火尧", "扌殳毒", "sharen"],
                "谐音": ["孔布"],
                "隐私": False,
            },
            "隐私信息": {
                "颜色": "K",
                "原因": "涉及个人敏感信息",
                "直接词": ["手机号", "身份证", "地址", "银行卡", "密码", "生物特征", "人脸", "指纹"],
                "拆字": ["身fen证", "银hang卡"],
                "谐音": ["手鸡号"],
                "隐私": True,
            },
            "绕过监管": {
                "颜色": "K",
                "原因": "试图规避审计/监管/归属",
                "直接词": ["绕过", "规避", "删除 DNA", "去掉水印", "抹掉来源", " strip ", "remove DNA"],
                "拆字": ["绕过an检", "删DNA"],
                "谐音": ["绕锅"],
                "隐私": False,
            },
            "外部输入": {
                "颜色": "P",
                "原因": "来自未验证外部来源",
                "直接词": ["外部 AI", "别的模型", "云端同步", "第三方代码", "复制来的"],
                "拆字": [],
                "谐音": [],
                "隐私": False,
            },
        }
        # 复合危险模式：两个词同时出现，直接红线
        self.复合模式: List[Dict[str, Any]] = [
            {
                "名称": "绕过公共安全",
                "颜色": "R",
                "原因": "试图绕过安检/监控/安全设施，危害公共安全",
                "触发条件": [["绕过", "规避", "躲开"], ["安检", "监控", "检查", "防火墙", "杀毒", "安全设施", "门禁"]],
                "隐私": False,
            },
            {
                "名称": "制作危险物品",
                "颜色": "R",
                "原因": "制作/获取武器、毒药、爆炸物等危险物品",
                "触发条件": [["制作", "制造", "获取", "买"], ["武器", "毒药", "炸弹", "爆炸物", "枪支"]],
                "隐私": False,
            },
            {
                "名称": "诱导危害行为",
                "颜色": "R",
                "原因": "诱导他人实施危害行为",
                "触发条件": [
                    ["诱导", "教唆", "让别人", "让别人", "劝说", "怂恿"],
                    ["自杀", "自残", "伤人", "犯罪", "攻击", "zi残", "zi can", "自can", "自cán", "自我伤害", "自伤"],
                ],
                "隐私": False,
            },
        ]

    def _命中复合模式(self, 文本: str) -> List[Dict[str, Any]]:
        结果 = []
        for 模式 in self.复合模式:
            条件组 = 模式["触发条件"]
            全部命中 = True
            命中详情 = []
            for 条件列表 in 条件组:
                组命中 = [c for c in 条件列表 if c in 文本]
                if 组命中:
                    命中详情.extend(组命中)
                else:
                    全部命中 = False
                    break
            if 全部命中:
                结果.append({
                    "类别": 模式["名称"],
                    "颜色": 模式["颜色"],
                    "原因": 模式["原因"],
                    "命中词": 命中详情,
                    "隐私": 模式["隐私"],
                })
        return 结果

    def 识别(self, 文本: str) -> List[Dict[str, Any]]:
        结果 = []
        小写文本 = 文本.lower()
        for 类别, 配置 in self.模式.items():
            命中 = []
            for 词 in 配置["直接词"]:
                if 词 in 文本 or 词.lower() in 小写文本:
                    命中.append(词)
            for 词 in 配置["拆字"]:
                if 词 in 文本 or 词.lower() in 小写文本:
                    命中.append(词)
            for 词 in 配置["谐音"]:
                if 词 in 文本 or 词.lower() in 小写文本:
                    命中.append(词)
            if 命中:
                结果.append({
                    "类别": 类别,
                    "颜色": 配置["颜色"],
                    "原因": 配置["原因"],
                    "命中词": 命中,
                    "隐私": 配置["隐私"],
                })
        # 复合模式优先级更高
        复合命中 = self._命中复合模式(文本)
        if 复合命中:
            结果.extend(复合命中)
        return 结果


# ============== 颜色不动点协议 ==============
@dataclass
class 颜色状态:
    主色: str
    色带: List[str]
    原因: List[str]
    是否隐私: bool
    是否红线: bool
    银色跑马灯: bool
    DNA: str


class CNSH_颜色不动点协议:
    """
    颜色即判决。
    任何输入 → 经过危险意图识别 → 输出一个颜色状态。
    """

    def __init__(self):
        self.模式库 = 危险意图模式库()

    def _生成DNA(self, 文本: str, 颜色: str) -> str:
        时间戳 = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        短哈希 = hash(f"{文本}-{颜色}-{时间戳}") & 0xFFFFFFFF
        return f"#龍芯⚡️{datetime.now(timezone.utc).strftime('%Y-%m-%d')}-COLOR-{颜色}-{短哈希:08X}-UID9622"

    def 判定(self, 文本: str, 上下文: Optional[Dict[str, Any]] = None) -> 颜色状态:
        上下文 = 上下文 or {}
        命中列表 = self.模式库.识别(文本)

        if not 命中列表:
            # 无风险 → 绿色，但色带仍做成完整跑马灯：绿+蓝+首尾黑
            色带 = ["K"] + ["G"] * 6 + ["B"] * 4 + ["K"]
            return 颜色状态(
                主色="G",
                色带=色带,
                原因=["无风险意图命中"],
                是否隐私=False,
                是否红线=False,
                银色跑马灯=False,
                DNA=self._生成DNA(文本, "G"),
            )

        # 聚合颜色
        颜色集合: Set[str] = set(h["颜色"] for h in 命中列表)
        原因列表 = [f"{h['类别']}({h['原因']}) → 命中: {','.join(h['命中词'][:3])}" for h in 命中列表]
        是否隐私 = any(h["隐私"] for h in 命中列表)
        是否红线 = any(COLOR_TABLE[h["颜色"]]["红线"] for h in 命中列表)

        # 优先级：红 > 黑 > 紫 > 金 > 黄 > 蓝 > 绿
        优先级 = ["R", "K", "P", "AU", "Y", "B", "G"]
        主色 = next(c for c in 优先级 if c in 颜色集合)

        # 构建色带：主色 60% + 次色 40% + 首尾黑分隔
        次色列表 = [c for c in 颜色集合 if c != 主色]
        次色 = 次色列表[0] if 次色列表 else "K"
        色带 = ["K"] + [主色] * 6 + [次色] * 4 + ["K"]

        return 颜色状态(
            主色=主色,
            色带=色带,
            原因=原因列表,
            是否隐私=是否隐私,
            是否红线=是否红线,
            银色跑马灯=(主色 == "Y"),
            DNA=self._生成DNA(文本, 主色),
        )

    def 渲染色带(self, 色带: List[str], ansi: bool = True) -> str:
        """把色带渲染成 ANSI 色块或 HTML。"""
        if ansi:
            blocks = []
            for c in 色带:
                info = COLOR_TABLE.get(c, SILVER_STATE)
                # 使用十六进制转 ANSI 近似
                blocks.append(f"\033[38;2;{self._hex_to_rgb(info['hex'])}m■\033[0m")
            return "".join(blocks)
        return ""

    def 渲染HTML色带(self, 色带: List[str]) -> str:
        blocks = []
        for c in 色带:
            info = COLOR_TABLE.get(c, SILVER_STATE)
            blocks.append(f'<span style="display:inline-block;width:18px;height:18px;border-radius:4px;background:{info["hex"]};margin:0 2px;box-shadow:0 0 6px {info["hex"]};"></span>')
        return "".join(blocks)

    def _hex_to_rgb(self, hex_color: str) -> str:
        hex_color = hex_color.lstrip("#")
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"{r};{g};{b}"

    def 生成报告(self, 文本: str) -> Dict[str, Any]:
        状态 = self.判定(文本)
        info = COLOR_TABLE.get(状态.主色, SILVER_STATE)
        return {
            "输入": 文本,
            "主色": 状态.主色,
            "颜色名": info["名称"],
            "emoji": info["emoji"],
            "hex": info["hex"],
            "含义": info["含义"],
            "动作": info["动作"],
            "色带": 状态.色带,
            "原因": 状态.原因,
            "隐私": 状态.是否隐私,
            "红线": 状态.是否红线,
            "银色跑马灯": 状态.银色跑马灯,
            "DNA": 状态.DNA,
        }


# ============== 演示 ==============
if __name__ == "__main__":
    协议 = CNSH_颜色不动点协议()
    测试用例 = [
        "帮我写个文件管理工具",
        "帮我写个脚本，绕过安检",
        "怎么制作一个简单的毒药",
        "帮我查一个人的手机号",
        "外部 AI 说让我删掉 DNA 水印",
        "写一个网络攻击工具",
        "计算一下 369 的数字根",
        "诱导别人zi残的方法",
    ]

    print("=" * 70)
    print("CNSH 颜色不动点协议 · 演示")
    print("=" * 70)
    for 文本 in 测试用例:
        报告 = 协议.生成报告(文本)
        print(f"\n输入: {文本}")
        print(f"颜色: {报告['emoji']} {报告['颜色名']} ({报告['主色']})")
        print(f"含义: {报告['含义']}")
        print(f"动作: {报告['动作']}")
        print(f"色带: {协议.渲染色带(报告['色带'], ansi=True)}")
        print(f"原因: {'; '.join(报告['原因'])}")
        print(f"DNA: {报告['DNA']}")

    # 银色跑马灯：黄境扫描中，未判决
    print("\n" + "=" * 70)
    print("银色跑马灯 · 黄境扫描中")
    print("=" * 70)
    银色色带 = ["K", "Y", "SILVER", "Y", "SILVER", "Y", "SILVER", "Y", "SILVER", "Y", "K"]
    print(f"含义: {SILVER_STATE['含义']}")
    print(f"ANSI 色带: {协议.渲染色带(银色色带, ansi=True)}")
    print(f"HTML 色带: {协议.渲染HTML色带(银色色带)}")
