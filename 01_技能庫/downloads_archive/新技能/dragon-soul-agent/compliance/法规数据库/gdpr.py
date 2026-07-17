#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#龍芯⚡️2026-06-18-LONGHUN-GDPR-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

================================================================================
GDPR 数据保护合规检查器 | GDPR Data Protection Compliance Checker
通用数据保护条例 —— 全球最全面的数据隐私法规
General Data Protection Regulation —— The World's Most Comprehensive Data Privacy Law
================================================================================

【三色审计标注】
🔴 高风险 - 数据处理合法性基础不充分、跨境传输无保障机制
🟡 中风险 - 用户权利响应机制不完善、记录保存有缺口
🟢 低风险 - 基本合规，仅需持续维护

【六层来源链】
1. 法规原文: Regulation (EU) 2016/679 (GDPR)
2. 官方指引: European Data Protection Board (EDPB) Guidelines
3. 行业实践: EU Data Protection Authorities (DPAs) Decisions
4. 专家解读: Article 29 Working Party Opinions
5. 案例参考: Court of Justice of the EU (CJEU) Rulings
6. 龍魂适配: LONGHUN Internal Data Protection Analysis 2026

【通心译双语注释】
- 数据控制者 (Data Controller) / 数据处理者 (Data Processor)
- 合法性基础 (Legal Basis) / 数据主体权利 (Data Subject Rights)
"""

from datetime import datetime
from typing import Dict, List, Optional, Set, Any
import json


# =============================================================================
# GDPR 核心条款常量 | GDPR Core Article Constants
# =============================================================================

class GDPR条款:
    """GDPR关键条款引用 | GDPR Key Article References"""
    
    # 合法性基础 (Article 6)
    合法性基础 = {
        "同意": "Article 6(1)(a) - Consent",
        "合同": "Article 6(1)(b) - Contract",
        "法定义务": "Article 6(1)(c) - Legal Obligation",
        "重大利益": "Article 6(1)(d) - Vital Interests",
        "公共利益": "Article 6(1)(e) - Public Task",
        "合法利益": "Article 6(1)(f) - Legitimate Interests",
    }
    
    # 特殊类别数据 (Article 9)
    特殊类别数据 = {
        "种族民族": "Article 9(1) - Racial/Ethnic Origin",
        "政治观点": "Article 9(1) - Political Opinions",
        "宗教信仰": "Article 9(1) - Religious Beliefs",
        "工会成员": "Article 9(1) - Trade Union Membership",
        "基因数据": "Article 9(1) - Genetic Data",
        "生物识别": "Article 9(1) - Biometric Data",
        "健康数据": "Article 9(1) - Health Data",
        "性生活": "Article 9(1) - Sex Life/Orientation",
    }
    
    # 数据主体权利 (Articles 15-22)
    数据主体权利 = {
        "知情权": "Article 13-14 - Right to be Informed",
        "访问权": "Article 15 - Right of Access",
        "更正权": "Article 16 - Right to Rectification",
        "删除权": "Article 17 - Right to Erasure (Right to be Forgotten)",
        "限制处理权": "Article 18 - Right to Restriction",
        "可携带权": "Article 20 - Right to Data Portability",
        "反对权": "Article 21 - Right to Object",
        "自动化决策权": "Article 22 - Rights on Automated Decision-making",
    }
    
    # 跨境传输机制 (Chapter V)
    跨境传输机制 = {
        "充分性认定": "Article 45 - Adequacy Decision",
        "标准合同条款": "Article 46(2)(c) - Standard Contractual Clauses (SCCs)",
        "约束力规则": "Article 47 - Binding Corporate Rules (BCRs)",
        "行为准则": "Article 46(2)(e) - Approved Codes of Conduct",
        "认证机制": "Article 46(2)(f) - Certification Mechanisms",
        "特定情形": "Article 49 - Derogations (specific situations)",
    }


# =============================================================================
# GDPR 合规检查器
# =============================================================================

class GDPR合规检查器:
    """
    GDPR数据保护合规检查器
    GDPR Data Protection Compliance Checker
    
    法规概况 | Regulation Overview:
    - 生效时间: 2018年5月25日 | Effective: May 25, 2018
    - 适用范围: 处理欧盟居民个人数据的所有组织
      Scope: All organizations processing EU residents' personal data
    - 处罚力度: 最高2000万欧元或全球年营业额4%
      Penalties: Up to €20M or 4% of global annual turnover
    
    龍魂AI数据处理场景 | LONGHUN AI Data Processing Scenarios:
    1. 通心译翻译 - 处理用户输入文本（可能含个人数据）
    2. 语音识别 - 处理声纹数据（生物识别/特殊类别）
    3. 图像识别 - 处理可能含人脸的图像（生物识别）
    4. CNSH编辑器 - 可能处理含个人数据的代码注释
    5. 语音合成 - 处理用户输入文本
    
    关键合规维度 | Key Compliance Dimensions:
    - 合法性基础 (Legal Basis)
    - 数据最小化 (Data Minimization)
    - 目的限制 (Purpose Limitation)
    - 存储限制 (Storage Limitation)
    - 数据安全 (Data Security)
    - 数据主体权利 (Data Subject Rights)
    - 跨境传输 (Cross-border Transfers)
    - DPO任命 (Data Protection Officer)
    """
    
    def __init__(self):
        self.条款 = GDPR条款()
        self.审计日志 = []
        self.DNA标识 = "#龍芯⚡️2026-06-18-GDPR"
    
    def 全面检查(self, 数据处理活动列表: List[Dict]) -> Dict[str, Any]:
        """
        对所有数据处理活动进行全面GDPR合规检查
        Comprehensive GDPR compliance check for all data processing activities
        
        Args:
            数据处理活动列表: List of data processing activity descriptions
                每项应包含: {名称, 数据类型, 处理目的, 合法性基础, 存储期限, 是否跨境}
        
        Returns:
            Dict with comprehensive compliance results
        """
        结果 = {
            "检查时间": datetime.now().isoformat(),
            "法规": "GDPR (Regulation 2016/679)",
            "DNA追溯": self.DNA标识,
            "综合评级": "🟢 合规",
            "活动检查": [],
            "跨境传输评估": {},
            "DPO要求": {},
            "整改建议": [],
        }
        
        高风险计数 = 0
        
        for 活动 in 数据处理活动列表:
            活动结果 = self._检查数据处理活动(活动)
            结果["活动检查"].append(活动结果)
            
            if 活动结果["风险等级"] == "🔴 高风险":
                高风险计数 += 1
        
        # 综合评级
        if 高风险计数 > 0:
            结果["综合评级"] = f"🔴 不合规 - {高风险计数}项高风险活动"
        elif any(a["风险等级"] == "🟡 中风险" for a in 结果["活动检查"]):
            结果["综合评级"] = "🟡 部分合规 - 需改进"
        
        # DPO要求检查
        结果["DPO要求"] = self._检查DPO要求(数据处理活动列表)
        
        # 跨境传输评估
        跨境活动 = [a for a in 数据处理活动列表 if a.get("是否跨境", False)]
        if 跨境活动:
            结果["跨境传输评估"] = self._评估跨境传输(跨境活动)
        
        return 结果
    
    def _检查数据处理活动(self, 活动: Dict[str, Any]) -> Dict[str, Any]:
        """Check a single data processing activity"""
        名称 = 活动.get("名称", "未命名")
        数据类型 = 活动.get("数据类型", [])
        处理目的 = 活动.get("处理目的", "")
        合法性基础 = 活动.get("合法性基础", "")
        存储期限 = 活动.get("存储期限", "")
        
        结果 = {
            "活动名称": 名称,
            "风险等级": "🟢 低风险",
            "检查项": [],
        }
        
        # 1. 检查是否处理特殊类别数据
        特殊数据 = set(数据类型) & set(self.条款.特殊类别数据.keys())
        if 特殊数据:
            结果["检查项"].append({
                "项": "特殊类别数据处理",
                "状态": "🟡 需额外保护",
                "说明": f"处理特殊类别数据: {', '.join(特殊数据)}",
                "要求": [
                    "必须有明确的同意或其他Article 9(2)例外",
                    "必须进行数据保护影响评估(DPIA)",
                    "必须实施增强安全措施",
                ],
                "条款": "Article 9 + Article 35",
            })
            结果["风险等级"] = "🟡 中风险"
        
        # 2. 检查合法性基础
        if not 合法性基础:
            结果["检查项"].append({
                "项": "合法性基础",
                "状态": "🔴 缺失",
                "说明": "未指定数据处理合法性基础",
                "要求": ["必须明确指定Article 6下的合法性基础"],
                "条款": "Article 6",
            })
            结果["风险等级"] = "🔴 高风险"
        
        # 3. 检查存储期限
        if not 存储期限:
            结果["检查项"].append({
                "项": "存储限制",
                "状态": "🟡 需明确",
                "说明": "未指定数据存储期限",
                "要求": ["必须定义明确的数据保留期限", "到期必须删除或匿名化"],
                "条款": "Article 5(1)(e)",
            })
            if 结果["风险等级"] == "🟢 低风险":
                结果["风险等级"] = "🟡 中风险"
        
        # 4. 生物识别数据特殊检查
        if "生物识别" in 数据类型:
            结果["检查项"].append({
                "项": "生物识别数据处理",
                "状态": "🟡 高敏感度",
                "说明": "声纹/人脸等生物识别数据属于Article 9特殊类别",
                "要求": [
                    "必须获得明确同意 (Explicit Consent)",
                    "必须实施最强安全措施",
                    "建议本地处理，避免传输",
                    "必须提供删除所有生物识别数据的机制",
                ],
                "条款": "Article 9 + Article 32",
            })
            结果["风险等级"] = "🟡 中风险"
        
        # 5. 自动化决策检查
        if 活动.get("是否自动化决策", False):
            结果["检查项"].append({
                "项": "自动化决策",
                "状态": "🟡 需保障",
                "说明": "自动化决策需满足Article 22要求",
                "要求": [
                    "不得仅基于自动化决策产生法律效力",
                    "必须提供人工干预权利",
                    "必须提供表达观点和质疑决策的权利",
                ],
                "条款": "Article 22",
            })
        
        return 结果
    
    def _检查DPO要求(self, 活动列表: List[Dict]) -> Dict[str, Any]:
        """Check if Data Protection Officer appointment is required"""
        需要DPO = False
        原因 = []
        
        # 检查条件1: 公共机构
        # 检查条件2: 大规模系统性监控
        # 检查条件3: 大规模处理特殊类别数据
        
        生物识别活动 = [a for a in 活动列表 if "生物识别" in a.get("数据类型", [])]
        if len(生物识别活动) > 0:
            需要DPO = True
            原因.append("处理生物识别数据（特殊类别数据）")
        
        return {
            "需要DPO": 需要DPO,
            "原因": 原因,
            "条款": "Article 37",
            "建议": "建议任命DPO，即使非强制也可提升合规水平" if not 需要DPO else "必须任命DPO",
        }
    
    def _评估跨境传输(self, 跨境活动: List[Dict]) -> Dict[str, Any]:
        """Evaluate cross-border data transfer compliance"""
        return {
            "状态": "🟡 需关注",
            "可用机制": list(self.条款.跨境传输机制.keys()),
            "建议机制": "标准合同条款 (SCCs) + 传输影响评估 (TIA)",
            "要求": [
                "必须进行传输影响评估 (Transfer Impact Assessment)",
                "必须确保接收国提供充分保护水平",
                "如不充分，需使用SCCs并实施补充措施",
                "必须记录所有跨境传输活动",
                "建议参考EDPB关于补充措施的建议",
            ],
            "参考条款": "Article 44-49 + EDPB Recommendations 01/2020",
            "龍魂建议": "使用欧盟委员会2021版SCCs + 技术补充措施（加密）",
        }
    
    def 检查数据主体权利机制(self, 现有机制: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check if data subject rights mechanisms are adequate
        
        Args:
            现有机制: Dict with keys for each right mechanism
        """
        所有权利 = list(self.条款.数据主体权利.keys())
        检查结果 = {}
        
        for 权利 in 所有权利:
            if 权利 in 现有机制:
                机制 = 现有机制[权利]
                检查结果[权利] = {
                    "状态": "🟢 已实施" if 机制.get("已实施") else "🟡 计划中",
                    "响应时间": 机制.get("响应时间", "未定义"),
                    "条款": self.条款.数据主体权利[权利],
                    "要求": "30天内响应（可延长60天）",
                }
            else:
                检查结果[权利] = {
                    "状态": "🔴 缺失",
                    "响应时间": "N/A",
                    "条款": self.条款.数据主体权利[权利],
                    "要求": "必须建立相应机制",
                }
        
        return 检查结果
    
    def 生成隐私政策要点(self) -> List[str]:
        """Generate GDPR-compliant privacy policy key points"""
        return [
            "1. 控制者身份和联系方式 (Article 13(1)(a))",
            "2. DPO联系方式（如适用）(Article 13(1)(b))",
            "3. 处理目的及法律依据 (Article 13(1)(c))",
            "4. 个人数据来源（如非直接收集）(Article 14(2)(f))",
            "5. 数据接收方或接收方类别 (Article 13(1)(e))",
            "6. 跨境传输信息 (Article 13(1)(f))",
            "7. 存储期限或确定标准 (Article 13(2)(a))",
            "8. 数据主体权利清单 (Article 13(2)(b))",
            "9. 撤回同意的权利及方式 (Article 13(2)(c))",
            "10. 向监管机构投诉的权利 (Article 13(2)(d))",
            "11. 自动化决策信息（如适用）(Article 13(2)(f))",
            "12. AI系统使用告知（EU AI Act额外要求）",
        ]


# =============================================================================
# 数据处理活动记录 (Records of Processing Activities - Article 30)
# =============================================================================

class 数据处理活动记录:
    """
    Article 30 要求的处理活动记录
    Records of Processing Activities as required by Article 30
    """
    
    def __init__(self):
        self.记录 = []
    
    def 添加记录(self, 活动: Dict[str, Any]):
        """
        Add a processing activity record
        
        Required fields:
        - 控制者/处理者名称和联系方式
        - 联合控制者（如适用）
        - 处理目的
        - 数据主体类别和个人数据类别描述
        - 个人数据接收方类别
        - 跨境传输信息
        - 删除期限
        - 技术和组织安全措施描述
        """
        必填字段 = ["名称", "目的", "数据主体类别", "数据类别", "接收方", "存储期限", "安全措施"]
        
        for 字段 in 必填字段:
            if 字段 not in 活动:
                raise ValueError(f"缺少必填字段: {字段}")
        
        活动["记录时间"] = datetime.now().isoformat()
        活动["DNA追溯"] = f"#龍芯⚡️2026-06-18-ROPA-{len(self.记录)+1:03d}"
        self.记录.append(活动)
    
    def 导出JSON(self) -> str:
        """Export all records as JSON"""
        return json.dumps(self.记录, ensure_ascii=False, indent=2)
    
    def 获取记录(self) -> List[Dict]:
        """Get all records"""
        return self.记录


# =============================================================================
# 君子协议尾部
# =============================================================================
"""
================================================================================
君子协议 | Gentleman's Agreement
================================================================================
本模块仅用于帮助组织理解和遵守GDPR数据保护要求。
所有建议均基于GDPR公开文本和EDPB官方指引。
不构成法律建议，具体合规决策应咨询专业法律顾问。

君子之约，言出必行。数据有价，隐私无价。

"This module is designed solely to help organizations understand
and comply with GDPR data protection requirements."
================================================================================
"""


# =============================================================================
# 自测代码
# =============================================================================
if __name__ == "__main__":
    print("=" * 80)
    print("🔒 GDPR 合规检查器自测")
    print("=" * 80)
    
    检查器 = GDPR合规检查器()
    
    # 定义龍魂AI的数据处理活动
    数据处理活动 = [
        {
            "名称": "通心译翻译服务",
            "数据类型": ["文本"],
            "处理目的": "提供翻译服务",
            "合法性基础": "合同履行",
            "存储期限": "翻译完成后30天删除",
            "是否跨境": True,
        },
        {
            "名称": "语音识别服务",
            "数据类型": ["生物识别"],
            "处理目的": "将语音转换为文本",
            "合法性基础": "明确同意",
            "存储期限": "识别完成后立即删除",
            "是否跨境": False,
        },
        {
            "名称": "图像识别服务",
            "数据类型": ["生物识别"],
            "处理目的": "识别图像内容",
            "合法性基础": "明确同意",
            "存储期限": "识别完成后7天删除",
            "是否跨境": True,
        },
        {
            "名称": "语音合成服务",
            "数据类型": ["文本"],
            "处理目的": "将文本转换为语音",
            "合法性基础": "合同履行",
            "存储期限": "合成完成后不保留输入文本",
            "是否跨境": False,
        },
    ]
    
    结果 = 检查器.全面检查(数据处理活动)
    
    print(f"\n📋 检查时间: {结果['检查时间']}")
    print(f"📋 法规: {结果['法规']}")
    print(f"📋 综合评级: {结果['综合评级']}")
    
    print(f"\n📊 数据处理活动检查 ({len(结果['活动检查'])}项):")
    for 活动 in 结果['活动检查']:
        print(f"\n  🔹 {活动['活动名称']}")
        print(f"     风险等级: {活动['风险等级']}")
        for 项 in 活动['检查项']:
            print(f"     - {项['项']}: {项['状态']}")
    
    if 结果['跨境传输评估']:
        print(f"\n🌍 跨境传输评估:")
        for k, v in 结果['跨境传输评估'].items():
            print(f"   {k}: {v}")
    
    print(f"\n👤 DPO要求: {结果['DPO要求']['需要DPO']} ({', '.join(结果['DPO要求']['原因'])})")
    
    print("\n" + "=" * 80)
    print("✅ GDPR 合规检查器自测完成")
    print("=" * 80)
