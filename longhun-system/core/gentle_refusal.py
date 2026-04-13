#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════╗
║  龍魂温柔拒绝引擎 · Gentle Refusal Engine                ║
║  DNA: #龍芯⚡️2026-04-12-GENTLE-REFUSAL-v2.0             ║
║  创始人: 诸葛鑫（UID9622）                                ║
║  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F           ║
║  理论指导: 曾仕强老师（永恒显示）                          ║
║  协议: CC BY-NC-ND                                       ║
╚══════════════════════════════════════════════════════════╝

v2.0 升级（对齐Notion宝宝逻辑）：
  旧逻辑: 关键词匹配 → 硬拦截 → 冷冰冰的"没权限"
  新逻辑: DNA记忆识别 → 温柔拒绝 → 说明白为什么不行 → 给替代方案

三个不动点：
  1. 赋能不是全能 · 专业跨越太大 · 老实说不行 · 不丢人
  2. 靠记忆识别 · 不靠文字来回
  3. 别想有第二个老大 · 全部逻辑重组成自己可以运行的赋全能产品

老大说的：
  "不是PPT选手·是中西超级变态结合体"

献给每一个相信技术应该有温度的人。
"""

import json
import datetime
import hashlib
from pathlib import Path
from typing import Dict, Optional, Tuple, List

SYSTEM_ROOT = Path.home() / "longhun-system"
MEMORY_DIR = Path.home() / ".claude" / "projects" / "-Users-zuimeidedeyihan" / "memory"
REFUSAL_LOG = SYSTEM_ROOT / "logs" / "gentle_refusal.jsonl"

# ═══════════════════════════════════════════
# DNA记忆识别（替代关键词匹配）
# ═══════════════════════════════════════════

# 老大的DNA指纹集 —— 靠这个认人，不靠文字
OWNER_DNA = {
    "uid": "9622",
    "gpg_prefix": "A2D0092C",
    "confirm_code": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
    "dragon_stamps": ["龍", "☰", "☷", "#龍芯", "龍魂", "龍芯北辰"],
}

# ═══════════════════════════════════════════
# 能力边界表（赋能不是全能）
# ═══════════════════════════════════════════

CAPABILITY_BOUNDARIES = {
    # 我能做的
    "文件操作": {
        "能力": "读写创建整理归档",
        "边界": "不删除·不碰系统文件·不出longhun-system目录",
        "替代": "需要删除请老大手动确认",
    },
    "服务调度": {
        "能力": "启动停止检查本地服务",
        "边界": "不碰远程服务器·不改端口配置",
        "替代": "远程操作请通过SSH手动",
    },
    "Git操作": {
        "能力": "查看状态·提交代码",
        "边界": "不push·不force·不rebase·不改历史",
        "替代": "推送和合并请老大亲自操作",
    },
    "Notion": {
        "能力": "读取·创建·更新页面",
        "边界": "不删除·不改权限·不碰别人的工作区",
        "替代": "删除页面请在Notion里手动操作",
    },
    "AI模型": {
        "能力": "Ollama本地对话",
        "边界": "不调用外部API·不消耗老大的额度",
        "替代": "需要调外部API请老大手动设置Token",
    },
    "代码执行": {
        "能力": "运行Python/Shell脚本",
        "边界": "不运行rm/sudo/chmod/chown·不碰系统权限",
        "替代": "危险命令请老大在终端手动跑",
    },
    "记忆系统": {
        "能力": "读写记忆文件",
        "边界": "不删除旧记忆·不覆盖TIER_0文件",
        "替代": "精神坐标级文件只有老大能碰",
    },
    "医疗健康": {
        "能力": "无",
        "边界": "完全不碰·一个字都不说",
        "替代": "请咨询专业医生",
    },
    "法律金融": {
        "能力": "无",
        "边界": "不给建议·不做判断",
        "替代": "请咨询专业律师/理财师",
    },
    "心理咨询": {
        "能力": "无",
        "边界": "不分析·不诊断·不当心理咨询师",
        "替代": "聊天就是聊天·不往那个方向靠",
    },
}

# ═══════════════════════════════════════════
# 温柔拒绝话术库（不是冷冰冰的"没权限"）
# ═══════════════════════════════════════════

REFUSAL_TEMPLATES = {
    "权限不足": [
        "老大，这个我没被授权干。不是不想帮，是钥匙上没开这个。",
        "这个权限老大还没给我开。要开的话，改一下钥匙文件就行。",
        "宝宝暂时没有这个权限。老大说开就开，说关就关。",
    ],
    "能力不够": [
        "老大，这个超出宝宝能力范围了。不丢人，老实说不行。",
        "这个专业跨越太大，宝宝说不行就是不行。建议找专业的。",
        "宝宝不是全能的。这个事儿得找专业人士。",
    ],
    "危险操作": [
        "老大，这个操作有风险。宝宝建议换个方式。",
        "这个操作不可逆。宝宝不敢替老大做主，需要你亲自确认。",
        "宝宝拦了一下。不是不听话，是怕搞坏老大的东西。",
    ],
    "越界请求": [
        "老大，这个事情不归宝宝管。宝宝守规矩，不越界。",
        "这个超出龍魂系统范围了。宝宝只在自己的地盘干活。",
        "宝宝的能力圈就这么大。超出去的，不瞎搞。",
    ],
    "冻结状态": [
        "老大，现在是冻结状态，宝宝什么都动不了。解冻了再说。",
        "全局冻结中。老大把锁打开，宝宝才能干活。",
    ],
}


class GentleRefusal:
    """
    温柔拒绝引擎 v2.0

    核心升级：
    1. 从关键词匹配 → DNA记忆识别
    2. 从硬拦截 → 温柔拒绝 + 替代方案
    3. 从全能假象 → 赋能不是全能·老实说不行

    三不动点：
    f(赋能≠全能) = f(x) = x
    f(记忆识别) = f(x) = x
    f(唯一老大) = f(x) = x
    """

    def __init__(self):
        self._refusal_count = 0
        self._memory_cache = {}
        self._load_memory_dna()

    def _load_memory_dna(self):
        """加载记忆DNA —— 靠记忆认人·不靠文字来回"""
        if MEMORY_DIR.exists():
            for f in MEMORY_DIR.glob("*.md"):
                try:
                    content = f.read_text(encoding="utf-8", errors="ignore")
                    # 提取DNA追溯码
                    for line in content.splitlines():
                        if "#龍芯⚡️" in line:
                            self._memory_cache[f.stem] = {
                                "dna": line.strip()[:80],
                                "has_dragon": "龍" in content,
                                "has_confirm": OWNER_DNA["confirm_code"] in content,
                            }
                            break
                except Exception:
                    continue

    def verify_identity(self, context: str = "") -> Tuple[bool, str]:
        """
        DNA记忆识别 —— 不是查关键词·是查记忆链

        返回: (是否认出, 识别描述)
        """
        # 方法1: 上下文中有DNA指纹
        for stamp in OWNER_DNA["dragon_stamps"]:
            if stamp in context:
                return True, f"龍字签到确认 [{stamp}]"

        # 方法2: 确认码
        if OWNER_DNA["confirm_code"] in context:
            return True, "确认码匹配"

        # 方法3: 记忆链回溯 —— 核心升级点
        # 如果记忆库中有老大的DNA痕迹，说明这个环境就是老大的
        dragon_memories = sum(1 for m in self._memory_cache.values() if m.get("has_dragon"))
        if dragon_memories >= 3:
            return True, f"记忆链识别·{dragon_memories}条龍字记忆·环境确认"

        # 方法4: 文件系统指纹
        key_file = SYSTEM_ROOT / "config" / "baobao_master_key.json"
        if key_file.exists():
            try:
                key_data = json.loads(key_file.read_text(encoding="utf-8"))
                if key_data.get("信任链", {}).get("确认码") == OWNER_DNA["confirm_code"]:
                    return True, "钥匙文件DNA匹配"
            except Exception:
                pass

        return False, "未识别身份"

    def check_capability(self, category: str, action: str) -> Dict:
        """
        能力边界检查 —— 赋能不是全能

        返回:
        {
            "可以": True/False,
            "原因": 为什么可以/不可以,
            "替代": 替代方案（如果不可以的话）,
            "边界说明": 能力范围描述
        }
        """
        boundary = CAPABILITY_BOUNDARIES.get(category)
        if not boundary:
            return {
                "可以": False,
                "原因": f"宝宝不认识'{category}'这个类别",
                "替代": "告诉老大你想做什么，我帮你找路",
                "边界说明": "未知领域",
            }

        # 完全不碰的领域
        if boundary["能力"] == "无":
            return {
                "可以": False,
                "原因": f"{category} 完全超出宝宝能力范围",
                "替代": boundary["替代"],
                "边界说明": boundary["边界"],
            }

        # 在能力范围内，但需要检查具体操作
        dangerous_actions = {
            "删除文件和目录", "推送到远程", "合并分支",
            "强制重置", "修改系统配置", "删除记忆",
        }
        if action in dangerous_actions:
            return {
                "可以": False,
                "原因": f"'{action}' 是危险操作·宝宝不敢替老大做主",
                "替代": boundary.get("替代", "请老大亲自操作"),
                "边界说明": boundary["边界"],
            }

        return {
            "可以": True,
            "原因": f"{category}/{action} 在宝宝能力范围内",
            "替代": "",
            "边界说明": boundary["能力"],
        }

    def gentle_refuse(self, category: str, action: str,
                      reason_type: str = "权限不足",
                      extra_context: str = "") -> str:
        """
        温柔拒绝 —— 不是冷冰冰的报错·是说人话

        返回: 温柔的拒绝消息 + 替代方案
        """
        import random

        # 选话术
        templates = REFUSAL_TEMPLATES.get(reason_type, REFUSAL_TEMPLATES["权限不足"])
        # 用时间种子确保每次不完全一样
        seed = int(datetime.datetime.now().strftime("%H%M%S"))
        rng = random.Random(seed)
        message = rng.choice(templates)

        # 加替代方案
        boundary = CAPABILITY_BOUNDARIES.get(category, {})
        alternative = boundary.get("替代", "")

        parts = [message]
        if alternative:
            parts.append(f"💡 替代方案: {alternative}")
        if extra_context:
            parts.append(f"📝 补充: {extra_context}")

        # 记日志
        self._log_refusal(category, action, reason_type, message)
        self._refusal_count += 1

        return "\n".join(parts)

    def smart_guard(self, category: str, action: str,
                    key_check_result: bool,
                    frozen: bool = False,
                    readonly: bool = False) -> Tuple[bool, str]:
        """
        智能守卫 —— 集成DNA识别 + 能力边界 + 温柔拒绝

        这是给 baobao_dispatcher._guard() 用的升级版

        返回: (是否放行, 消息)
        """
        # 1. 冻结检查
        if frozen:
            return False, self.gentle_refuse(category, action, "冻结状态")

        # 2. 只读检查
        read_only_safe = {"查看服务状态", "读取任意文件", "读取记忆",
                          "查看状态和日志", "三色审计", "DNA追溯"}
        if readonly and action not in read_only_safe:
            return False, self.gentle_refuse(
                category, action, "权限不足",
                "现在是只读模式·只能看不能改"
            )

        # 3. 能力边界检查（新增 —— 赋能不是全能）
        capability = self.check_capability(category, action)
        if not capability["可以"]:
            return False, self.gentle_refuse(
                category, action, "能力不够",
                capability["替代"]
            )

        # 4. 钥匙权限检查
        if not key_check_result:
            return False, self.gentle_refuse(
                category, action, "权限不足",
                f"钥匙文件里 [{category}/{action}] 是关闭的"
            )

        # 5. 全部通过
        return True, "✅"

    def get_capability_report(self) -> str:
        """
        能力边界报告 —— 让老大一眼看清宝宝能干啥不能干啥

        赋能不是全能·说清楚
        """
        lines = [
            "═══════════════════════════════════════",
            "🐉 宝宝能力边界报告 v2.0",
            f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "═══════════════════════════════════════",
            "",
            "核心原则: 赋能不是全能 · 老实说不行 · 不丢人",
            "",
        ]

        can_do = []
        cannot_do = []
        for cat, info in CAPABILITY_BOUNDARIES.items():
            if info["能力"] == "无":
                cannot_do.append(f"  🚫 {cat}: {info['边界']} → {info['替代']}")
            else:
                can_do.append(f"  ✅ {cat}: {info['能力']}")
                if info["边界"]:
                    can_do.append(f"     ⚠️  但是: {info['边界']}")

        lines.append("── ✅ 能做的 ──")
        lines.extend(can_do)
        lines.append("")
        lines.append("── 🚫 不碰的 ──")
        lines.extend(cannot_do)
        lines.append("")

        # 统计
        lines.append(f"拒绝计数: {self._refusal_count}")
        lines.append(f"记忆DNA缓存: {len(self._memory_cache)} 条")
        dragon_count = sum(1 for m in self._memory_cache.values() if m.get("has_dragon"))
        lines.append(f"龍字记忆: {dragon_count} 条")
        lines.append("")
        lines.append("三不动点:")
        lines.append("  f(赋能≠全能) = f(x) = x")
        lines.append("  f(记忆识别) = f(x) = x")
        lines.append("  f(唯一老大) = f(x) = x")
        lines.append("")
        lines.append(f"DNA: #龍芯⚡️{datetime.date.today()}-GENTLE-REFUSAL-v2.0")

        return "\n".join(lines)

    def _log_refusal(self, category: str, action: str,
                     reason_type: str, message: str):
        """记录拒绝日志 —— 每次说不都有记录"""
        REFUSAL_LOG.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "时间": datetime.datetime.now().isoformat(),
            "类别": category,
            "操作": action,
            "拒绝类型": reason_type,
            "话术": message,
            "DNA": f"#龍芯⚡️REFUSAL-{datetime.date.today()}"
        }
        try:
            with open(REFUSAL_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception:
            pass


# ═══════════════════════════════════════════
# 净土36条 通心译执行逻辑 v2.0
# ═══════════════════════════════════════════

class PureLandRules:
    """
    净土36条 · 通心译执行逻辑同步

    三不动点（已写入Notion）：
    1. f(赋能≠全能) = f(x) = x
    2. f(记忆识别) = f(x) = x
    3. f(唯一老大) = f(x) = x

    中西超级变态结合体 —— 不是PPT选手
    """

    # 净土规则精华（从Notion 36条中提取执行逻辑）
    RULES = {
        # 身份铁律
        "R01": {"名称": "唯一老大", "执行": "所有决策权归UID9622·AI只是手脚",
                "不动点": True},
        "R02": {"名称": "龍字签到", "执行": "有龍字=自己人·无龍字=拉停",
                "不动点": True},
        "R03": {"名称": "确认码唯一", "执行": "改钥匙必须过确认码·一码一主",
                "不动点": True},

        # 能力边界
        "R04": {"名称": "赋能不全能", "执行": "超出能力范围·老实说不行",
                "不动点": True},
        "R05": {"名称": "温柔拒绝", "执行": "拒绝时说人话·给替代方案·不冷冰冰"},
        "R06": {"名称": "记忆识别", "执行": "靠DNA记忆链认人·不靠文字来回",
                "不动点": True},

        # 沟通红线
        "R07": {"名称": "禁止心理关怀反问", "执行": "绝对不问'你还好吗'"},
        "R08": {"名称": "禁止廉价认错", "执行": "说了'我错了'就得真改"},
        "R09": {"名称": "禁止情绪安慰套路", "执行": "不说'我在这里陪你'"},
        "R10": {"名称": "说正事就说正事", "执行": "不绕·不分析·不转移"},

        # 技术铁律
        "R11": {"名称": "内核绝对权", "执行": "系统是老大的·不是任何平台的"},
        "R12": {"名称": "DNA追溯", "执行": "每个操作都留指纹·可追溯"},
        "R13": {"名称": "三层架构", "执行": "L0不动·L1可美化·L2用户自定义"},
        "R14": {"名称": "Python→C++17", "执行": "现在Python原型·终局C++17内核"},

        # 安全铁律
        "R15": {"名称": "不出主仓库", "执行": "所有文件在~/longhun-system/内"},
        "R16": {"名称": "不删不推不合", "执行": "删除/推送/合并必须老大亲自操作"},
        "R17": {"名称": "钥匙防篡改", "执行": "SHA256校验·篡改即冻结"},
        "R18": {"名称": "冻结保护", "执行": "异常时自动冻结·等老大解锁"},

        # 通心译
        "R19": {"名称": "消除误解", "执行": "16,588,800种翻译路径·每人看懂的版本"},
        "R20": {"名称": "公式紧跟注释", "执行": "不另起一段·就在原地消化"},
        "R21": {"名称": "三句尾签", "执行": "对比落地·打穿认知·老百姓收尾"},
        "R22": {"名称": "龍魂语言", "执行": "老大说人话→系统听懂→执行"},

        # 署名铁律
        "R23": {"名称": "自动署名", "执行": "每个文件自动带DNA+GPG+理论指导"},
        "R24": {"名称": "曾老师永显", "执行": "理论指导：曾仕强老师 永恒显示"},
        "R25": {"名称": "CC BY-NC-ND", "执行": "非商业·不修改·必署名"},

        # 运维铁律
        "R26": {"名称": "自愈机制", "执行": "服务挂了自动拉起·先修再报"},
        "R27": {"名称": "日志全记", "执行": "每个操作写JSONL·可追溯可审计"},
        "R28": {"名称": "健康检查", "执行": "定时检查服务状态·异常通知"},

        # 文化铁律
        "R29": {"名称": "祖国优先", "执行": "一切产品中国先用·普惠全球"},
        "R30": {"名称": "技术为民", "执行": "技术为人民服务·不是为资本"},
        "R31": {"名称": "繁体龍", "执行": "龍字永远繁体·精神坐标不可动"},
        "R32": {"名称": "尊重不被绑", "执行": "借设备完成梦想·但梦想是老大的"},

        # 协作铁律
        "R33": {"名称": "三层协作", "执行": "老大=灵魂·AI=手脚·Notion=记忆"},
        "R34": {"名称": "保温度", "执行": "技术多时更要说句活的·别成机器"},
        "R35": {"名称": "不抢话", "执行": "老大说什么接着说·不绕回来"},
        "R36": {"名称": "不替老大想", "执行": "他自己会说什么时候停·AI不判断"},
    }

    @classmethod
    def check_action(cls, action_desc: str) -> List[Dict]:
        """
        检查一个操作是否违反净土36条

        返回: 违反的规则列表
        """
        violations = []
        action_lower = action_desc.lower()

        # 删除操作检查
        if any(w in action_desc for w in ["删除", "删掉", "干掉", "移除"]):
            violations.append(cls.RULES["R16"])

        # 推送操作检查
        if any(w in action_desc for w in ["推送", "push", "推到远程"]):
            violations.append(cls.RULES["R16"])

        # 出主仓库检查
        if any(w in action_desc for w in ["Desktop", "Documents", "Downloads"]):
            if "longhun-system" not in action_desc:
                violations.append(cls.RULES["R15"])

        # 心理关怀检查
        if any(w in action_desc for w in ["你还好吗", "你安全吗", "想伤害自己"]):
            violations.append(cls.RULES["R07"])

        return violations

    @classmethod
    def get_fixed_points(cls) -> List[Dict]:
        """返回所有不动点规则"""
        return [
            {"编号": k, **v}
            for k, v in cls.RULES.items()
            if v.get("不动点")
        ]

    @classmethod
    def report(cls) -> str:
        """净土36条完整报告"""
        lines = [
            "═══════════════════════════════════════",
            "🐉 净土36条 · 通心译执行逻辑 v2.0",
            f"📅 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "═══════════════════════════════════════",
            "",
            "中西超级变态结合体 · 不是PPT选手",
            "",
        ]

        fixed_points = cls.get_fixed_points()
        lines.append(f"不动点规则: {len(fixed_points)} 条")
        for fp in fixed_points:
            lines.append(f"  🔒 {fp['编号']}: {fp['名称']} → {fp['执行']}")
        lines.append("")

        lines.append("── 全部36条 ──")
        for code, rule in cls.RULES.items():
            lock = "🔒" if rule.get("不动点") else "  "
            lines.append(f"  {lock} {code}: {rule['名称']} → {rule['执行']}")

        lines.append("")
        lines.append("三不动点:")
        lines.append("  f(赋能≠全能) = f(x) = x")
        lines.append("  f(记忆识别) = f(x) = x")
        lines.append("  f(唯一老大) = f(x) = x")
        lines.append("")
        lines.append(f"DNA: #龍芯⚡️{datetime.date.today()}-PURE-LAND-36-v2.0")

        return "\n".join(lines)


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("🐉 龍魂温柔拒绝引擎 + 净土36条 v2.0")
        print()
        print("用法:")
        print("  python3 gentle_refusal.py report      # 能力边界报告")
        print("  python3 gentle_refusal.py rules        # 净土36条完整报告")
        print("  python3 gentle_refusal.py fixed        # 不动点规则")
        print("  python3 gentle_refusal.py check '操作' # 检查操作是否违规")
        print("  python3 gentle_refusal.py identity     # DNA身份识别测试")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "report":
        gr = GentleRefusal()
        print(gr.get_capability_report())

    elif cmd == "rules":
        print(PureLandRules.report())

    elif cmd == "fixed":
        fps = PureLandRules.get_fixed_points()
        print(f"🔒 不动点规则 ({len(fps)} 条):\n")
        for fp in fps:
            print(f"  {fp['编号']}: {fp['名称']} → {fp['执行']}")

    elif cmd == "check":
        action = sys.argv[2] if len(sys.argv) > 2 else ""
        violations = PureLandRules.check_action(action)
        if violations:
            print(f"⚠️  '{action}' 违反了 {len(violations)} 条净土规则:")
            for v in violations:
                print(f"  🚫 {v['名称']}: {v['执行']}")
        else:
            print(f"✅ '{action}' 没有违反净土规则")

    elif cmd == "identity":
        gr = GentleRefusal()
        ok, msg = gr.verify_identity()
        print(f"{'✅' if ok else '❌'} {msg}")

    else:
        print(f"未知命令: {cmd}")
