#!/usr/bin/env python3
#龍芯⚡️2026-06-19-CNSH-CHINA-COMPLIANCE-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║  DNA: #龍芯⚡️2026-06-19-CNSH-CHINA-COMPLIANCE-v1.0              ║
║  中国合规矩阵 — 主检查器 · 龍魂体系                               ║
║  China Compliance Matrix — Master Checker · Dragon Soul Arch       ║
╚══════════════════════════════════════════════════════════════════════╝

【君子协议】本系统仅用于中国法律合规自检，不构成法律意见。
【Gentleman's Agreement】For self-checking PRC laws only; not legal advice.

覆盖法律 / Covered Laws:
  1. 《个人信息保护法》(PIPL) — 个保法检查器
  2. 《数据安全法》(DSL) — 数安法检查器
  3. 《电子商务法》— 电商法检查器
  4. 《网络安全法》(CSL) — 网安法检查器
  5. e-CNY相关规定 — eCNY合规检查器

三色审计 / Three-Color Audit:
  🟢 合规 Compliant (≥80分) | 🟡 警示 Warning (60-79分) | 🔴 违规 Violation (<60分)

评分权重 / Scoring Weights:
  - 个保法: 30% (涉及个人隐私，权重最高)
  - 数安法: 25% (数据安全基础)
  - 电商法: 15% (电商场景适用)
  - 网安法: 20% (网络安全基础)
  - e-CNY: 10% (数字人民币场景适用)
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional

from .个保法检查器 import 个保法检查器, 个保法检查结果
from .数安法检查器 import 数安法检查器, 数安法检查结果
from .电商法检查器 import 电商法检查器, 电商法检查结果
from .网安法检查器 import 网安法检查器, 网安法检查结果
from .eCNY合规检查器 import eCNY合规检查器, eCNY检查结果


# ═══════════════════════════════════════════════════════════════
# 合规报告类
# ═══════════════════════════════════════════════════════════════

class 合规报告:
    """
    合规报告 — 汇总各法律维度检查结果
    Compliance Report — Aggregated results from all law dimensions
    """

    def __init__(self):
        self.DNA = "#龍芯⚡️2026-06-19-CNSH-CHINA-COMPLIANCE-v1.0"
        self.报告生成时间 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.平台名称 = ""
        self.综合得分 = 100
        self.总体风险等级 = "🟢低"
        self.检查通过 = True
        # 各法律维度结果
        self.个保法结果: Optional[个保法检查结果] = None
        self.数安法结果: Optional[数安法检查结果] = None
        self.电商法结果: Optional[电商法检查结果] = None
        self.网安法结果: Optional[网安法检查结果] = None
        self.eCNY结果: Optional[eCNY检查结果] = None
        # 汇总
        self.全部不合规项: List[str] = []
        self.全部改进建议: List[str] = []
        self.覆盖法律数 = 5
        self.检查维度数 = 40  # 8维度 × 5法律

    def to_dict(self) -> Dict[str, Any]:
        """导出字典 / Export to dict"""
        return {
            "DNA": self.DNA,
            "报告生成时间": self.报告生成时间,
            "平台名称": self.平台名称,
            "综合得分": self.综合得分,
            "总体风险等级": self.总体风险等级,
            "检查通过": self.检查通过,
            "覆盖法律数": self.覆盖法律数,
            "检查维度数": self.检查维度数,
            "个保法": self.个保法结果.to_dict() if self.个保法结果 else None,
            "数安法": self.数安法结果.to_dict() if self.数安法结果 else None,
            "电商法": self.电商法结果.to_dict() if self.电商法结果 else None,
            "网安法": self.网安法结果.to_dict() if self.网安法结果 else None,
            "eCNY": self.eCNY结果.to_dict() if self.eCNY结果 else None,
            "全部不合规项": self.全部不合规项,
            "全部改进建议": self.全部改进建议,
        }

    def to_markdown(self) -> str:
        """导出完整Markdown报告 / Export full Markdown report"""
        md = f"""# 🇨🇳 中国法律合规检查报告

> **DNA**: `{self.DNA}`  
> **报告生成时间**: {self.报告生成时间}  
> **被检平台**: {self.平台名称 if self.平台名称 else "未指定"}  
> **【君子协议】本报告仅用于合规自检，不构成法律意见。**

---

## 📊 综合评估

| 指标 | 值 |
|------|-----|
| 综合得分 | **{self.综合得分}**/100 |
| 总体风险等级 | **{self.总体风险等级}** |
| 检查通过 | {'✅ 是' if self.检查通过 else '❌ 否'} |
| 覆盖法律 | {self.覆盖法律数}部 |
| 检查维度 | {self.检查维度数}项 |

---

## 📈 各法律维度得分

| 法律 | 得分 | 风险等级 | 状态 |
|------|------|----------|------|
"""
        # 个保法
        if self.个保法结果:
            图标 = self._风险等级图标(self.个保法结果.风险等级)
            md += f"| 《个人信息保护法》 | {self.个保法结果.综合得分} | {self.个保法结果.风险等级} | {图标} |\n"
        # 数安法
        if self.数安法结果:
            图标 = self._风险等级图标(self.数安法结果.风险等级)
            md += f"| 《数据安全法》 | {self.数安法结果.综合得分} | {self.数安法结果.风险等级} | {图标} |\n"
        # 电商法
        if self.电商法结果:
            图标 = self._风险等级图标(self.电商法结果.风险等级)
            md += f"| 《电子商务法》 | {self.电商法结果.综合得分} | {self.电商法结果.风险等级} | {图标} |\n"
        # 网安法
        if self.网安法结果:
            图标 = self._风险等级图标(self.网安法结果.风险等级)
            md += f"| 《网络安全法》 | {self.网安法结果.综合得分} | {self.网安法结果.风险等级} | {图标} |\n"
        # e-CNY
        if self.eCNY结果:
            图标 = self._风险等级图标(self.eCNY结果.风险等级)
            md += f"| e-CNY相关规定 | {self.eCNY结果.综合得分} | {self.eCNY结果.风险等级} | {图标} |\n"

        # 总体风险等级解读
        md += f"\n### 🎯 风险等级说明\n\n"
        md += "- 🟢 **低**: 合规状况良好，继续维护\n"
        md += "- 🟡 **中**: 存在风险点，建议改进\n"
        md += "- 🔴 **高**: 严重不合规，需立即整改\n"

        # 各法律详细报告
        if self.个保法结果:
            md += f"\n---\n\n{self.个保法结果.to_markdown()}\n"
        if self.数安法结果:
            md += f"\n---\n\n{self.数安法结果.to_markdown()}\n"
        if self.电商法结果:
            md += f"\n---\n\n{self.电商法结果.to_markdown()}\n"
        if self.网安法结果:
            md += f"\n---\n\n{self.网安法结果.to_markdown()}\n"
        if self.eCNY结果:
            md += f"\n---\n\n{self.eCNY结果.to_markdown()}\n"

        # 不合规项汇总
        if self.全部不合规项:
            md += "\n---\n\n## 🔴 全部不合规项汇总\n\n"
            for i, item in enumerate(self.全部不合规项, 1):
                md += f"{i}. {item}\n"

        # 改进建议汇总
        if self.全部改进建议:
            md += "\n---\n\n## 💡 全部改进建议汇总\n\n"
            for i, sug in enumerate(self.全部改进建议, 1):
                md += f"{i}. {sug}\n"

        md += "\n---\n\n*报告生成: 龍魂体系 · CNSH中国合规检查系统 v1.0*\n"
        return md

    def to_json(self) -> str:
        """导出JSON格式 / Export JSON format"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)

    @staticmethod
    def _风险等级图标(等级: str) -> str:
        if "🟢" in 等级:
            return "✅"
        elif "🟡" in 等级:
            return "⚠️"
        elif "🔴" in 等级:
            return "❌"
        return "❓"


# ═══════════════════════════════════════════════════════════════
# 中国合规矩阵 — 主检查器
# ═══════════════════════════════════════════════════════════════

class 中国合规矩阵:
    """
    中国合规矩阵 — 统一合规检查入口
    China Compliance Matrix — Unified compliance checking gateway

    【君子协议】本系统仅用于中国法律合规自检，不构成法律意见。
    【Gentleman's Agreement】For self-checking PRC laws only; not legal advice.
    """

    # 评分权重 / Scoring weights
    权重 = {
        "个保法": 0.30,
        "数安法": 0.25,
        "电商法": 0.15,
        "网安法": 0.20,
        "eCNY": 0.10,
    }

    def __init__(self):
        self.DNA = "#龍芯⚡️2026-06-19-CNSH-CHINA-COMPLIANCE-v1.0"
        self.创建时间 = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # 初始化各检查器
        self.个保法检查器 = 个保法检查器()
        self.数安法检查器 = 数安法检查器()
        self.电商法检查器 = 电商法检查器()
        self.网安法检查器 = 网安法检查器()
        self.eCNY检查器 = eCNY合规检查器()

    def 全面合规检查(self, 操作数据: Dict[str, Any], 平台名: str = "未指定") -> 合规报告:
        """
        执行全面合规检查 — 所有法律维度
        Perform comprehensive compliance check across all laws

        参数 / Parameters:
            操作数据: 包含所有法律维度的检查数据
                - 个保法数据: dict 个保法检查数据
                - 数安法数据: dict 数安法检查数据
                - 电商法数据: dict 电商法检查数据
                - 网安法数据: dict 网安法检查数据
                - eCNY数据: dict eCNY检查数据
            平台名: 被检平台名称

        返回 / Returns:
            合规报告对象
        """
        报告 = 合规报告()
        报告.平台名称 = 平台名

        print(f"\n{'='*60}")
        print(f"🇨🇳 中国合规矩阵 — 全面合规检查启动")
        print(f"   平台: {平台名}")
        print(f"   DNA: {self.DNA}")
        print(f"{'='*60}")

        # ═══════════════════════════════════════════════
        # 1. 个保法检查
        # ═══════════════════════════════════════════════
        print("\n[1/5] 正在检查《个人信息保护法》...")
        个保法数据 = 操作数据.get("个保法数据", {})
        报告.个保法结果 = self.个保法检查(个保法数据)
        print(f"      得分: {报告.个保法结果.综合得分}  风险: {报告.个保法结果.风险等级}")

        # ═══════════════════════════════════════════════
        # 2. 数安法检查
        # ═══════════════════════════════════════════════
        print("\n[2/5] 正在检查《数据安全法》...")
        数安法数据 = 操作数据.get("数安法数据", {})
        报告.数安法结果 = self.数安法检查(数安法数据)
        print(f"      得分: {报告.数安法结果.综合得分}  风险: {报告.数安法结果.风险等级}")

        # ═══════════════════════════════════════════════
        # 3. 电商法检查
        # ═══════════════════════════════════════════════
        print("\n[3/5] 正在检查《电子商务法》...")
        电商法数据 = 操作数据.get("电商法数据", {})
        报告.电商法结果 = self.电商法检查(电商法数据, 平台名)
        print(f"      得分: {报告.电商法结果.综合得分}  风险: {报告.电商法结果.风险等级}")

        # ═══════════════════════════════════════════════
        # 4. 网安法检查
        # ═══════════════════════════════════════════════
        print("\n[4/5] 正在检查《网络安全法》...")
        网安法数据 = 操作数据.get("网安法数据", {})
        报告.网安法结果 = self.网安法检查(网安法数据)
        print(f"      得分: {报告.网安法结果.综合得分}  风险: {报告.网安法结果.风险等级}")

        # ═══════════════════════════════════════════════
        # 5. e-CNY检查
        # ═══════════════════════════════════════════════
        print("\n[5/5] 正在检查e-CNY合规...")
        eCNY数据 = 操作数据.get("eCNY数据", {})
        报告.eCNY结果 = self.eCNY合规检查(eCNY数据)
        print(f"      得分: {报告.eCNY结果.综合得分}  风险: {报告.eCNY结果.风险等级}")

        # ═══════════════════════════════════════════════
        # 汇总计算
        # ═══════════════════════════════════════════════
        self._汇总报告(报告)

        print(f"\n{'='*60}")
        print(f"🇨🇳 全面合规检查完成")
        print(f"   综合得分: {报告.综合得分}/100")
        print(f"   总体风险: {报告.总体风险等级}")
        print(f"   检查通过: {'✅' if 报告.检查通过 else '❌'}")
        print(f"{'='*60}")

        return 报告

    def 个保法检查(self, 操作数据: Dict[str, Any]) -> 个保法检查结果:
        """个保法检查 / PIPL Check"""
        return self.个保法检查器.检查(操作数据)

    def 数安法检查(self, 操作数据: Dict[str, Any]) -> 数安法检查结果:
        """数安法检查 / DSL Check"""
        return self.数安法检查器.检查(操作数据)

    def 电商法检查(self, 操作数据: Dict[str, Any], 平台名: str = "") -> 电商法检查结果:
        """电商法检查 / E-Commerce Law Check"""
        return self.电商法检查器.检查(操作数据, 平台名)

    def 网安法检查(self, 操作数据: Dict[str, Any]) -> 网安法检查结果:
        """网安法检查 / CSL Check"""
        return self.网安法检查器.检查(操作数据)

    def eCNY合规检查(self, 交易数据: Dict[str, Any]) -> eCNY检查结果:
        """e-CNY合规检查 / e-CNY Compliance Check"""
        return self.eCNY检查器.检查(交易数据)

    def 生成合规报告(self, 报告: 合规报告) -> str:
        """生成合规报告文本 / Generate compliance report text"""
        return 报告.to_markdown()

    def 风险等级评估(self, 得分: int) -> str:
        """
        风险等级评估
        Risk level assessment

        参数 / Parameters:
            得分: 0-100的综合得分

        返回 / Returns:
            🟢低 / 🟡中 / 🔴高
        """
        if 得分 >= 80:
            return "🟢低"
        elif 得分 >= 60:
            return "🟡中"
        else:
            return "🔴高"

    def _汇总报告(self, 报告: 合规报告):
        """内部方法：汇总各维度结果 / Internal: aggregate results"""
        scores = []
        weights = []

        if 报告.个保法结果:
            scores.append(报告.个保法结果.综合得分)
            weights.append(self.权重["个保法"])
            报告.全部不合规项.extend(报告.个保法结果.不合规项)
            报告.全部改进建议.extend(报告.个保法结果.改进建议)

        if 报告.数安法结果:
            scores.append(报告.数安法结果.综合得分)
            weights.append(self.权重["数安法"])
            报告.全部不合规项.extend(报告.数安法结果.不合规项)
            报告.全部改进建议.extend(报告.数安法结果.改进建议)

        if 报告.电商法结果:
            scores.append(报告.电商法结果.综合得分)
            weights.append(self.权重["电商法"])
            报告.全部不合规项.extend(报告.电商法结果.不合规项)
            报告.全部改进建议.extend(报告.电商法结果.改进建议)

        if 报告.网安法结果:
            scores.append(报告.网安法结果.综合得分)
            weights.append(self.权重["网安法"])
            报告.全部不合规项.extend(报告.网安法结果.不合规项)
            报告.全部改进建议.extend(报告.网安法结果.改进建议)

        if 报告.eCNY结果:
            scores.append(报告.eCNY结果.综合得分)
            weights.append(self.权重["eCNY"])
            报告.全部不合规项.extend(报告.eCNY结果.不合规项)
            报告.全部改进建议.extend(报告.eCNY结果.改进建议)

        # 加权平均
        if scores and weights:
            total_weight = sum(weights)
            报告.综合得分 = round(sum(s * w for s, w in zip(scores, weights)) / total_weight)

        报告.总体风险等级 = self.风险等级评估(报告.综合得分)
        报告.检查通过 = 报告.综合得分 >= 60


# ═══════════════════════════════════════════════════════════════
# 演示代码 / Demo
# ═══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 70)
    print("🇨🇳 中国合规矩阵 — 全面演示 / China Compliance Matrix Demo")
    print("=" * 70)

    # 创建合规矩阵
    合规矩阵 = 中国合规矩阵()

    # 场景1: 全合规平台
    print("\n" + "🟢" * 30)
    print("【场景1: 全合规平台演示】")
    print("🟢" * 30)

    全合规数据 = {
        "个保法数据": {
            "数据类型": ["手机号", "邮箱", "昵称"],
            "用户同意": True,
            "同意方式": "明确点击",
            "单独同意": False,
            "告知规则": True,
            "目的限定": "用户注册与服务提供",
            "实际用途": "用户注册与服务提供",
            "加密传输": True,
            "加密存储": True,
            "访问控制": True,
            "留存期限": 90,
            "自动删除": True,
            "第三方共享": False,
            "隐私政策": True,
            "政策链接": "https://example.com/privacy",
            "数据最小化": True,
        },
        "数安法数据": {
            "数据分类": "重要数据",
            "分级保护": True,
            "全流程管理": True,
            "管理制度文件": True,
            "责任人": "张三（数据安全官）",
            "安全审计": True,
            "审计周期": "每季度",
            "应急预案": True,
            "演练记录": True,
            "数据备份": True,
            "异地备份": True,
            "恢复测试": True,
            "访问权限": True,
            "最小权限": True,
            "权限审计": True,
            "交易中介": False,
            "员工培训": True,
            "日志留存": True,
        },
        "电商法数据": {
            "经营者信息": {"营业执照": True, "联系方式": True, "经营地址": True},
            "商品信息": True,
            "价格透明": True,
            "虚假宣传": False,
            "搜索结果": True,
            "竞价排名标识": True,
            "提供非个性化选项": True,
            "用户评价": True,
            "删除差评": False,
            "刷好评": False,
            "用户信息查询": True,
            "用户信息更正": True,
            "用户信息删除": True,
            "注销账户": True,
            "注销便捷": True,
            "注销条件合理": True,
            "默认搭售": False,
            "押金退还": True,
            "大数据杀熟": False,
            "发票开具": True,
            "争议处理": True,
            "七天无理由": True,
        },
        "网安法数据": {
            "安全认证": True,
            "安全漏洞报告": True,
            "恶意程序防范": True,
            "日志留存": True,
            "日志留存月数": 6,
            "数据加密": True,
            "用户信息保护制度": True,
            "保密协议": True,
            "信息泄露事件": False,
            "用户身份核验": True,
            "实名制": True,
            "违法信息处置": True,
            "处置时限": "24小时内",
            "协助执法": True,
            "等级保护": True,
            "等保级别": "三级",
            "应急预案": True,
            "演练记录": True,
            "报告时限": "1小时内",
        },
        "eCNY数据": {
            "钱包类型": "二类钱包",
            "实名认证": True,
            "认证等级": "实名",
            "交易金额": 5000.0,
            "日累计金额": 8000.0,
            "年累计金额": 20000.0,
            "跨境交易": False,
            "可疑交易": False,
            "KYC完成": True,
            "身份核验": True,
            "职业信息": True,
            "交易目的": "日常消费",
            "反洗钱筛查": True,
            "资金来源": "工资收入",
            "大额报告": False,
            "匿名交易": False,
            "可追溯": True,
        },
    }

    报告1 = 合规矩阵.全面合规检查(全合规数据, "合规商城")
    print(f"\n📊 综合得分: {报告1.综合得分}/100")
    print(f"🎯 总体风险: {报告1.总体风险等级}")
    print(f"✅ 检查通过: {报告1.检查通过}")

    # 场景2: 问题平台
    print("\n" + "🔴" * 30)
    print("【场景2: 问题平台演示】")
    print("🔴" * 30)

    问题数据 = {
        "个保法数据": {
            "数据类型": ["手机号", "人脸特征", "精确地理位置", "银行卡号"],
            "用户同意": False,
            "单独同意": False,
            "告知规则": False,
            "目的限定": "",
            "实际用途": "用户画像与精准营销",
            "加密传输": False,
            "加密存储": False,
            "访问控制": False,
            "留存期限": 1825,
            "自动删除": False,
            "第三方共享": True,
            "第三方同意": False,
            "第三方列表": ["广告公司A", "数据平台B"],
            "隐私政策": False,
            "数据最小化": False,
            "影响评估": False,
        },
        "数安法数据": {
            "数据分类": "",
            "分级保护": False,
            "全流程管理": False,
            "管理制度文件": False,
            "责任人": "",
            "安全审计": False,
            "应急预案": False,
            "数据备份": False,
            "访问权限": False,
            "交易中介": True,
            "审核义务": False,
            "数据来源": False,
            "员工培训": False,
            "日志留存": False,
        },
        "电商法数据": {
            "经营者信息": {},
            "商品信息": False,
            "价格透明": False,
            "虚假宣传": True,
            "搜索结果": True,
            "竞价排名标识": False,
            "提供非个性化选项": False,
            "用户评价": True,
            "删除差评": True,
            "刷好评": True,
            "用户信息查询": False,
            "用户信息更正": False,
            "用户信息删除": False,
            "注销账户": False,
            "默认搭售": True,
            "押金退还": False,
            "大数据杀熟": True,
            "发票开具": False,
            "争议处理": False,
            "七天无理由": False,
        },
        "网安法数据": {
            "安全认证": False,
            "安全漏洞报告": False,
            "恶意程序防范": False,
            "日志留存": False,
            "日志留存月数": 0,
            "数据加密": False,
            "用户信息保护制度": False,
            "保密协议": False,
            "信息泄露事件": True,
            "事件报告": False,
            "补救措施": False,
            "用户身份核验": False,
            "实名制": False,
            "违法信息处置": False,
            "协助执法": False,
            "等级保护": False,
            "等保级别": "",
            "应急预案": False,
            "演练记录": False,
        },
        "eCNY数据": {
            "钱包类型": "四类钱包",
            "实名认证": False,
            "交易金额": 80000.0,
            "日累计金额": 100000.0,
            "年累计金额": 200000.0,
            "跨境交易": True,
            "央行审批": False,
            "可疑交易": True,
            "可疑报告": False,
            "KYC完成": False,
            "身份核验": False,
            "反洗钱筛查": False,
            "大额报告": False,
            "匿名交易": True,
            "可追溯": False,
        },
    }

    报告2 = 合规矩阵.全面合规检查(问题数据, "问题平台")
    print(f"\n📊 综合得分: {报告2.综合得分}/100")
    print(f"🎯 总体风险: {报告2.总体风险等级}")
    print(f"✅ 检查通过: {报告2.检查通过}")

    if 报告2.全部不合规项:
        print(f"\n🔴 不合规项共 {len(报告2.全部不合规项)} 项")

    # 导出报告示例
    print("\n" + "=" * 70)
    print("📄 Markdown报告预览（前500字符）:")
    print("=" * 70)
    md_preview = 报告2.to_markdown()[:500]
    print(md_preview + "...")

    # JSON导出示例
    print("\n📄 JSON报告预览（前300字符）:")
    json_preview = 报告2.to_json()[:300]
    print(json_preview + "...")

    print("\n" + "=" * 70)
    print("演示完成 / Demo completed")
    print("=" * 70)
