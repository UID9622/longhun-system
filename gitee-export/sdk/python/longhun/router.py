"""人格路由器 · 中文输入 → 人格分发

DNA: #龍芯⚡️丙午·丙申·丙辰·戊子·坎-SDK-ROUTER-v2.1
"""
from dataclasses import dataclass
from typing import Optional
import hashlib


@dataclass
class RouteResult:
    persona: str
    persona_name: str
    action: str
    confidence: float
    dna: str

    def __str__(self) -> str:
        """格式化输出"""
        return (
            f"🟢 {self.persona} {self.persona_name} · {self.action}\n"
            f"   confidence: {self.confidence:.2f}\n"
            f"   DNA: {self.dna}"
        )


@dataclass
class RouteInfo:
    persona: str
    persona_name: str
    action: str
    keywords: list[str]
    confidence: float


# ── 内联路由表（30+ 意图域 · 10 人格）──
# 格式: (关键词列表, 人格, 人格名, 动作)
_ROUTE_TABLE: list[tuple[list[str], str, str, str]] = [
    (["检查", "审计", "安全", "有没有问题", "安全吗", "合规"], "P05", "上帝之眼", "audit"),
    (["修", "修复", "不报错", "改好", "修正", "bug", "报错", "错误"], "P02", "龍芯", "fix"),
    (["同步", "联动", "串起来", "索引", "关联", "归档"], "P15", "乔前辈", "sync"),
    (["自动化", "补代码", "乔接", "Mac自动", "快捷指令", "开机自启"], "P15", "乔前辈", "automate"),
    (["部署", "发布", "上线", "deploy"], "P14", "吕蒙", "deploy"),
    (["算", "数字根", "五行", "八卦", "属性"], "P06", "数学大师", "compute"),
    (["值得", "过期", "还顶用", "还能留吗", "贡献值"], "P01", "诸葛亮", "evaluate"),
    (["漏洞", "渗透", "红客", "黑客", "注入", "XSS", "越权", "攻防"], "P77", "黑天使军团", "pentest"),
    (["代码审计", "静态分析", "依赖审计"], "P77", "黑天使军团", "code_audit"),
    (["CVE", "0day", "APT", "威胁情报", "暗网"], "P77", "黑天使军团", "threat_intel"),
    (["铁律", "规矩", "宪法", "底座", "不骗", "对外", "史记", "最初誓言"], "P00", "文心", "anchor_guard"),
    (["借用", "引用", "来源", "署名", "注明", "归属", "蒸馏", "原创"], "P05", "上帝之眼", "source_audit"),
    (["主权", "国家", "国管国", "红线"], "P00", "文心", "sovereignty"),
    (["接火", "水印", "后果自负", "传播"], "P03", "墨子", "watermark"),
    (["家族", "几代", "亲属", "谁死谁活", "直系", "旁系"], "P00", "文心", "family"),
    (["防卡", "太紧", "卡了", "接力", "SOS", "收口"], "P02", "龍芯", "handoff"),
    (["外部AI", "裸吞", "ChatGPT", "Kimi", "实证复核"], "P05", "上帝之眼", "external_review"),
    (["太笼统", "空话", "装逼", "5字段"], "P05", "上帝之眼", "precision_check"),
    (["历史", "篡改", "颠倒是非", "勿忘国耻"], "P00", "文心", "history_guard"),
    (["熔断申诉", "人工审计", "凭什么拒绝", "我不服"], "P05", "上帝之眼", "fuse_appeal"),
    (["上传", "删除", "密钥", "sudo", "git push", "涉密"], "P77", "黑天使军团", "veto_check"),
    (["情绪", "心情", "我懂你", "共情", "加油"], "P00", "文心", "emotion_absorb"),
    (["决策", "来源", "凭啥", "怎么得出", "推理链", "透明化"], "P05", "上帝之眼", "decision_card"),
    (["许愿池", "一块钱", "人民资源池", "公益"], "P01", "诸葛亮", "wish_pool"),
    (["曾仕强", "捡回德", "师德", "德字闸", "德污"], "P00", "文心", "virtue_guard"),
    (["道引", "开源吸收", "吸收代码", "引入开源"], "P01", "诸葛亮", "daoyin"),
    (["自驱", "事事有回应", "件件有着落", "开干"], "P02", "龍芯", "self_drive"),
    (["大白话", "术语", "行话", "听不懂", "人话"], "P00", "文心", "plain_lang"),
    (["流场", "节点流向", "边", "失败回退"], "P13", "姜子牙", "flow_audit"),
    (["钻石", "都一样吗", "主干合并", "同一概念"], "P13", "姜子牙", "dedup"),
    (["情绪", "依赖", "上瘾", "不重读"], "P00", "文心", "addiction_guard"),
    (["法律", "武器", "天下为公", "外公", "家人"], "P00", "文心", "law_weapon"),
    (["API出口", "密钥隔离", "本地中继", "下水道"], "P15", "乔前辈", "api_relay"),
    (["IP伪装", "VPN", "Tor", "八项一致"], "P15", "乔前辈", "ip_mask"),
    (["军魂", "分别心", "用其器", "五净律"], "P00", "文心", "military_soul"),
    (["代码出口", "git", "主干", "force-with-lease"], "P15", "乔前辈", "code_export"),
    (["数据出口", "大文件", "BFG", "仓库瘦身"], "P15", "乔前辈", "data_export"),
    (["最初誓言", "不变字面", "不扭曲"], "P00", "文心", "oath_verify"),
    (["自逼为王", "三大试炼", "守望孤独", "倾尽所有", "永恒守护"], "P01", "诸葛亮", "trial_check"),
    (["心即神", "思维接口", "相由心生"], "P02", "龍芯", "mind_bridge"),
    (["道阳佛阴", "太极平衡", "太刚太执", "物极必反"], "P00", "文心", "balance_audit"),
    (["二次元之眼", "看全局", "监控态势", "异常预警"], "P77", "黑天使军团", "surveillance"),
    (["一槌定音", "收网", "连根拔起", "时机成熟"], "P05", "上帝之眼", "final_strike"),
    (["传承契约", "接着受着守着", "接着道", "受着佛", "守着太极"], "P00", "文心", "inheritance"),
    (["开源三戒", "star", "完美焦虑", "商业化妥协"], "P01", "诸葛亮", "oss_reminder"),
    (["DNA登记", "注册资产", "登记册", "查归属", "黑户"], "P18", "基因登记官", "dna_register"),
    (["信任积分", "贡献分", "功德分", "公益分", "政审"], "P20", "贡献公证官", "trust_score"),
    (["创新溯源", "谁先", "自研争议", "谁发明的", "谁先提出"], "P05", "上帝之眼", "innovation_trace"),
    # 兜底
    ([], "P02", "龍芯", "assist"),
]


class PersonaRouter:
    """中文语义输入 → 自动匹配人格 → 分发执行

    v2.1: 内联路由表（30+ 意图域 · 10 人格），零外部依赖。
    支持指定人格 + 自动匹配。
    """

    def __init__(self, engine: str = "builtin"):
        """初始化路由器

        Args:
            engine: "builtin"(内联路由表) | "native"(对接 bin/ 语义抽屉引擎)
        """
        self._engine = engine
        self._route_table = _ROUTE_TABLE

    def route(self, text: str, persona: Optional[str] = None) -> RouteResult:
        """路由分发

        Args:
            text: 中文自然语言输入
            persona: 强制指定人格（可选，跳过自动匹配）

        Returns:
            RouteResult with persona, action, dna

        Raises:
            ValueError: text 为空时
        """
        if not text:
            raise ValueError("text 不能为空")

        if persona:
            # 强制指定 → 跳过匹配
            return self._build_result(persona, text)

        # 自动匹配：找第一个命中关键词的规则
        matched = None
        for keywords, p, name, action in self._route_table:
            if not keywords:
                continue  # 跳过兜底
            if any(kw in text for kw in keywords):
                matched = (p, name, action, keywords)
                break

        if matched:
            p, name, action, kws = matched
            confidence = min(0.95, 0.6 + len(kws) * 0.05)
        else:
            # 兜底 → P02 龍芯
            p, name, action = "P02", "龍芯", "assist"
            kws = ["兜底"]
            confidence = 0.45

        return self._build_result(p, name, action, confidence, kws, text)

    def info(self, text: str) -> RouteInfo:
        """获取路由匹配的元信息"""
        if not text:
            raise ValueError("text 不能为空")

        matched = None
        for keywords, p, name, action in self._route_table:
            if not keywords:
                continue
            if any(kw in text for kw in keywords):
                matched = (p, name, action, keywords)
                break

        if matched:
            p, name, action, kws = matched
            confidence = min(0.95, 0.6 + len(kws) * 0.05)
        else:
            p, name, action = "P02", "龍芯", "assist"
            kws = ["兜底"]
            confidence = 0.45

        return RouteInfo(
            persona=p,
            persona_name=name,
            action=action,
            keywords=kws,
            confidence=confidence,
        )

    def _build_result(self, persona_id: str, name: str = "", action: str = "",
                      confidence: float = 0.9, _keywords: Optional[list[str]] = None,
                      text: str = "") -> RouteResult:
        """构建 RouteResult"""
        if not name:
            # 从路由表查找人格名
            for _, p, n, _ in self._route_table:
                if p == persona_id:
                    name = n
                    break
            if not name:
                name = persona_id
        if not action:
            action = "dispatch"

        h = hashlib.sha256(
            f"{persona_id}-{action}-{text}".encode()
        ).hexdigest()[:8].upper()

        return RouteResult(
            persona=persona_id,
            persona_name=name,
            action=action,
            confidence=confidence,
            dna=f"#龍芯⚡️丙午·丙申·丙辰·戊子·坎-ROUTE-{action.upper()}-{h}",
        )
