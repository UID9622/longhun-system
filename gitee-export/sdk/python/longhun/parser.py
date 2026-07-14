"""CNSH 语义解析器

DNA: #龍芯⚡️丙午·丙申·丙辰·戊子·坎-SDK-PARSER-v2.1
"""
from dataclasses import dataclass


@dataclass
class Intent:
    domain: str
    action: str
    keywords: list[str]
    confidence: float


# ── 内联语义域映射（40+ 意图域）──
# 格式: (关键词列表, 域, 动作)
_DOMAIN_MAP: list[tuple[list[str], str, str]] = [
    (["检查", "审计", "安全", "有没有问题", "安全吗", "合规"], "security", "audit"),
    (["修", "修复", "不报错", "改好", "修正", "bug"], "engineering", "fix"),
    (["同步", "联动", "串起来", "索引", "关联", "归档"], "integration", "sync"),
    (["自动化", "补代码", "乔接", "快捷指令"], "automation", "automate"),
    (["部署", "发布", "上线"], "deployment", "deploy"),
    (["算", "数字根", "五行", "八卦", "属性", "计算"], "math", "compute"),
    (["值得", "过期", "还顶用", "贡献值", "还能留吗"], "governance", "evaluate"),
    (["漏洞", "渗透", "注入", "XSS", "越权", "攻防"], "security", "pentest"),
    (["CVE", "0day", "APT", "威胁情报"], "security", "threat_intel"),
    (["铁律", "规矩", "宪法", "底座", "不骗", "最初誓言"], "constitution", "anchor_guard"),
    (["借用", "引用", "来源", "署名", "归属", "蒸馏"], "sovereignty", "source_audit"),
    (["主权", "国管国", "红线"], "sovereignty", "sovereignty_check"),
    (["接火", "水印", "后果自负", "传播"], "sovereignty", "watermark"),
    (["家族", "几代", "亲属", "直系", "旁系"], "identity", "family_query"),
    (["防卡", "太紧", "接力", "SOS", "收口", "上下文"], "system", "handoff"),
    (["外部AI", "裸吞", "ChatGPT", "Kimi", "实证复核"], "audit", "external_review"),
    (["太笼统", "空话", "装逼", "5字段"], "quality", "precision_check"),
    (["历史", "篡改", "颠倒是非", "勿忘国耻"], "history", "history_guard"),
    (["熔断申诉", "人工审计", "凭什么拒绝", "我不服"], "governance", "fuse_appeal"),
    (["上传", "删除", "密钥", "sudo", "涉密"], "security", "veto_check"),
    (["情绪", "心情", "我懂你", "共情", "加油", "累", "难过"], "emotion", "absorb"),
    (["决策", "来源", "凭啥", "怎么得出", "推理链", "透明化"], "governance", "decision_trace"),
    (["许愿池", "一块钱", "人民资源池", "公益"], "economy", "wish_pool"),
    (["曾仕强", "捡回德", "师德", "德字闸"], "ethics", "virtue_guard"),
    (["道引", "开源吸收", "引入开源"], "integration", "daoyin"),
    (["自驱", "事事有回应", "件件有着落", "开干"], "system", "self_drive"),
    (["大白话", "术语", "行话", "听不懂", "人话"], "language", "plain_lang"),
    (["流场", "节点流向", "边", "失败回退"], "system", "flow_audit"),
    (["钻石", "都一样吗", "主干合并", "同一概念"], "knowledge", "dedup"),
    (["法律", "武器", "天下为公", "家人"], "law", "law_weapon"),
    (["API出口", "密钥隔离", "本地中继", "下水道"], "infrastructure", "api_relay"),
    (["IP伪装", "VPN", "Tor", "八项一致"], "infrastructure", "ip_mask"),
    (["军魂", "分别心", "用其器", "五净律"], "identity", "military_soul"),
    (["代码出口", "git", "主干", "force-with-lease"], "engineering", "code_export"),
    (["数据出口", "大文件", "BFG", "仓库瘦身"], "engineering", "data_export"),
    (["心即神", "思维接口", "相由心生"], "philosophy", "mind_bridge"),
    (["道阳佛阴", "太极平衡", "太刚太执"], "philosophy", "balance_audit"),
    (["二次元之眼", "看全局", "监控态势", "异常预警"], "surveillance", "monitor"),
    (["一槌定音", "收网", "连根拔起"], "governance", "final_strike"),
    (["传承契约", "接着受着守着", "接着道", "受着佛"], "heritage", "inheritance"),
    (["开源三戒", "star", "完美焦虑"], "engineering", "oss_reminder"),
    (["DNA登记", "注册资产", "登记册", "黑户"], "registry", "dna_register"),
    (["信任积分", "贡献分", "功德分", "政审"], "governance", "trust_score"),
    (["创新溯源", "谁先", "自研争议", "谁发明的"], "research", "innovation_trace"),
    (["token", "Token", "续期", "到期", "过期"], "system", "token_check"),
    (["状态", "运行", "在线", "跑着没", "启动"], "system", "status_check"),
    (["语音", "说话", "朗读", "TTS", "合成", "声音"], "voice", "synthesize"),
    (["视觉", "看图", "识别", "图片", "照片"], "vision", "analyze"),
    (["声纹", "DNA", "注册声纹", "验证声纹"], "voice", "voice_dna"),
    ([], "general", "assist"),
]


class CNSHParser:
    """中文语义 → 意图域匹配

    v2.1: 内联语义域映射（40+ 意图域），零外部依赖。
    支持中文大白话输入，自动匹配意图域和动作。
    """

    def __init__(self):
        pass

    def parse(self, text: str) -> Intent:
        """解析中文输入，返回意图域

        Args:
            text: 中文自然语言输入

        Returns:
            Intent with domain, action, keywords, confidence

        Raises:
            ValueError: text 为空时
        """
        if not text:
            raise ValueError("text 不能为空")

        # 关键词匹配
        best_match = None
        best_count = 0

        for keywords, domain, action in _DOMAIN_MAP:
            if not keywords:
                continue
            hits = [kw for kw in keywords if kw in text]
            if len(hits) > best_count:
                best_count = len(hits)
                best_match = (domain, action, hits)

        if best_match and best_count > 0:
            domain, action, hits = best_match
            confidence = min(0.95, 0.5 + best_count * 0.1)
        else:
            # 兜底
            domain, action = "general", "assist"
            hits = ["兜底"]
            confidence = 0.35

        return Intent(
            domain=domain,
            action=action,
            keywords=hits,
            confidence=confidence,
        )
