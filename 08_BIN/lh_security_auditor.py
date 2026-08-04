#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·安全风险评估引擎 v1.0
DNA: #ZHUGEXIN⚡️丙午·乙未·甲辰-安全检查-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：对设备、系统、数据访问进行安全风险评估，给出防护建议和执行动作。
负责人格：👁️ 上帝之眼
职责：全域监管、设备绑定、安全检查

核心功能：
  1. 扫描目标 — 设备/系统/数据
  2. 风险评估 — 隐私泄露/账号安全/系统越界
  3. 给出建议 — 高风险阻止/中风险提醒/低风险记录
  4. 执行动作 — ALLOW / WARN / BLOCK
  5. 审计日志 — 所有检查可追溯
  6. 双因素认证 — 高价值操作强制2FA
  7. 白名单/黑名单 — 灵活配置
  8. 定期复检 — 自动安排下次检查
  9. 告警推送 — 高风险自动告警
  10. 与三色审计联动 — 无缝对接
"""

import json
import uuid
import hashlib
import datetime
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
import sqlite3

# ============================================================
# 一、数据结构
# ============================================================

class 风险等级(Enum):
    高风险 = "🔴 高风险"
    中风险 = "🟡 中风险"
    低风险 = "🟢 低风险"
    未知 = "⚪ 未知"

class 执行动作(Enum):
    BLOCK = "🚫 阻止"
    WARN = "⚠️ 警告"
    ALLOW = "✅ 允许"

@dataclass
class 安全检查结果:
    """安全检查结果"""
    检查ID: str
    目标: str
    目标类型: str  # 设备/系统/数据
    风险等级: 风险等级
    风险评分: float  # 0-100
    风险明细: List[Dict]
    防护建议: List[str]
    执行动作: 执行动作
    双因素认证: bool
    白名单命中: bool
    黑名单命中: bool
    审计日志ID: str
    复检时间: str
    时间戳: str
    dna: str
    安全签名: str

@dataclass
class 安全基线:
    """安全基线"""
    设备ID: str
    历史行为: List[Dict]
    正常模式: Dict
    异常阈值: float
    最后更新: str

@dataclass
class 审计日志条目:
    """审计日志"""
    日志ID: str
    检查ID: str
    操作: str
    结果: str
    操作人: str
    时间戳: str
    dna: str


# ============================================================
# 二、风险评估引擎
# ============================================================

class 风险评估引擎:
    """
    多维度安全风险评估
    维度：隐私泄露、账号安全、系统越界
    """

    # 风险权重配置
    权重配置 = {
        "隐私泄露": 0.35,
        "账号安全": 0.35,
        "系统越界": 0.30
    }

    # 风险规则库
    风险规则 = {
        "隐私泄露": {
            "高": ["个人信息明文存储", "数据未加密传输", "日志包含敏感信息", "无访问控制"],
            "中": ["最小权限原则未执行", "数据保留超期", "备份未加密"],
            "低": ["匿名数据未脱敏", "日志级别过高"]
        },
        "账号安全": {
            "高": ["无密码策略", "多因素认证未启用", "默认密码未修改", "账号共享"],
            "中": ["密码复杂度不足", "会话超时过长", "失败登录无限制"],
            "低": ["密码过期时间过长", "无登录提醒"]
        },
        "系统越界": {
            "高": ["提权漏洞", "未授权API访问", "系统目录可写", "服务以root运行"],
            "中": ["端口暴露过多", "软件版本过旧", "日志权限不当"],
            "低": ["调试模式未关闭", "错误信息暴露"]
        }
    }

    def __init__(self):
        self.历史评分: Dict[str, List[float]] = {}

    def 评估(self, 目标信息: Dict) -> Dict:
        """
        执行多维度风险评估
        Returns: {
            score: 综合评分,
            level: 风险等级,
            details: 各维度明细,
            findings: 发现的问题列表
        }
        """
        结果 = {
            "score": 0.0,
            "level": 风险等级.低风险,
            "details": {},
            "findings": [],
            "recommendations": []
        }

        维度得分 = {}
        所有问题 = []

        # 评估各维度
        for 维度, 权重 in self.权重配置.items():
            维度结果 = self._评估维度(维度, 目标信息)
            维度得分[维度] = 维度结果["得分"]
            所有问题.extend(维度结果["问题"])

        # 计算综合得分
        加权得分 = sum(维度得分[d] * self.权重配置[d] for d in 维度得分)
        结果["score"] = round(加权得分, 2)

        # 确定风险等级
        结果["level"] = self._确定等级(结果["score"])
        结果["details"] = 维度得分
        结果["findings"] = 所有问题[:10]  # 限制数量

        # 生成建议
        结果["recommendations"] = self._生成建议(结果["findings"], 结果["level"])

        return 结果

    def _评估维度(self, 维度: str, 目标信息: Dict) -> Dict:
        """评估单个维度"""
        问题 = []
        得分 = 0.0

        # 获取该维度的规则
        规则 = self.风险规则.get(维度, {})
        目标文本 = json.dumps(目标信息, ensure_ascii=False)

        # 检查高风险
        for 规则项 in 规则.get("高", []):
            if 规则项 in 目标文本:
                问题.append({"级别": "高", "描述": 规则项, "分数": 30})
                得分 += 30

        # 检查中风险
        for 规则项 in 规则.get("中", []):
            if 规则项 in 目标文本:
                问题.append({"级别": "中", "描述": 规则项, "分数": 15})
                得分 += 15

        # 检查低风险
        for 规则项 in 规则.get("低", []):
            if 规则项 in 目标文本:
                问题.append({"级别": "低", "描述": 规则项, "分数": 5})
                得分 += 5

        # 归一化得分 (0-100)
        得分 = min(100, 得分)

        return {"得分": 得分, "问题": 问题}

    def _确定等级(self, 得分: float) -> 风险等级:
        """根据得分确定风险等级"""
        if 得分 >= 60:
            return 风险等级.高风险
        elif 得分 >= 30:
            return 风险等级.中风险
        elif 得分 >= 0:
            return 风险等级.低风险
        return 风险等级.未知

    def _生成建议(self, 问题: List[Dict], 等级: 风险等级) -> List[str]:
        """生成防护建议"""
        建议 = []

        if 等级 == 风险等级.高风险:
            建议.append("🚫 立即阻止：存在严重安全风险")
            建议.append("🔴 建议：立即修复以下高风险问题")

        elif 等级 == 风险等级.中风险:
            建议.append("⚠️ 需要关注：存在中等安全风险")
            建议.append("🟡 建议：制定修复计划并排期")

        else:
            建议.append("🟢 安全状态：未发现明显安全风险")
            建议.append("📋 建议：保持监控，定期复查")

        # 具体建议
        for p in 问题[:5]:
            级别符号 = "🔴" if p["级别"] == "高" else ("🟡" if p["级别"] == "中" else "🟢")
            建议.append(f"  {级别符号} {p['描述']}")

        if len(问题) > 5:
            建议.append(f"  ... 还有 {len(问题)-5} 个问题")

        return 建议


# ============================================================
# 三、安全检查引擎
# ============================================================

class 安全检查引擎:
    """
    主安全检查引擎
    整合：扫描 → 评估 → 建议 → 动作
    """

    def __init__(self):
        self.审计日志 = 审计日志系统()
        self.风险评估 = 风险评估引擎()
        self.白名单: List[str] = []
        self.黑名单: List[str] = []
        self.历史记录: List[安全检查结果] = []

    def 执行检查(self, 目标: str, 目标类型: str, 详细信息: Dict, 操作人: str = "系统") -> 安全检查结果:
        """
        执行安全检查

        Args:
            目标: 目标名称
            目标类型: 设备/系统/数据
            详细信息: 目标详细信息
            操作人: 操作人

        Returns:
            安全检查结果
        """
        # 生成检查ID和DNA
        检查ID = f"SEC-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"
        dna = f"#ZHUGEXIN⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-SEC-{uuid.uuid4().hex[:8].upper()}"

        # 1. 白名单检查
        白名单命中 = self._检查白名单(目标, 详细信息)

        # 2. 黑名单检查
        黑名单命中 = self._检查黑名单(目标, 详细信息)

        # 3. 风险评估
        评估结果 = self.风险评估.评估(详细信息)

        # 4. 双因素认证检查
        需要2FA = self._检查双因素认证(评估结果)

        # 5. 确定执行动作
        执行动作 = self._确定动作(评估结果, 白名单命中, 黑名单命中)

        # 6. 生成安全签名
        安全签名 = self._生成签名(检查ID, 目标, 评估结果["score"])

        # 7. 计算复检时间
        复检时间 = self._计算复检时间(评估结果["level"])

        # 8. 构建结果
        结果 = 安全检查结果(
            检查ID=检查ID,
            目标=目标,
            目标类型=目标类型,
            风险等级=评估结果["level"],
            风险评分=评估结果["score"],
            风险明细=评估结果["details"],
            防护建议=评估结果["recommendations"],
            执行动作=执行动作,
            双因素认证=需要2FA,
            白名单命中=白名单命中,
            黑名单命中=黑名单命中,
            审计日志ID=f"LOG-{uuid.uuid4().hex[:12].upper()}",
            复检时间=复检时间,
            时间戳=datetime.datetime.now().isoformat(),
            dna=dna,
            安全签名=安全签名
        )

        # 9. 记录审计日志
        self.审计日志.记录(
            检查ID=结果.检查ID,
            操作="安全检查",
            结果=结果.风险等级.value,
            操作人=操作人,
            dna=结果.dna
        )

        # 10. 保存历史
        self.历史记录.append(结果)

        return 结果

    def _检查白名单(self, 目标: str, 详细信息: Dict) -> bool:
        """检查是否在白名单中"""
        if not self.白名单:
            return False
        return any(项 in 目标 for 项 in self.白名单)

    def _检查黑名单(self, 目标: str, 详细信息: Dict) -> bool:
        """检查是否在黑名单中"""
        if not self.黑名单:
            return False
        return any(项 in 目标 for 项 in self.黑名单)

    def _检查双因素认证(self, 评估结果: Dict) -> bool:
        """检查是否需要双因素认证"""
        # 高风险或分数>50 需要2FA
        return 评估结果["level"] == 风险等级.高风险 or 评估结果["score"] > 50

    def _确定动作(self, 评估结果: Dict, 白名单: bool, 黑名单: bool) -> 执行动作:
        """确定执行动作"""
        if 黑名单:
            return 执行动作.BLOCK

        if 白名单:
            return 执行动作.ALLOW

        if 评估结果["level"] == 风险等级.高风险:
            return 执行动作.BLOCK
        elif 评估结果["level"] == 风险等级.中风险:
            return 执行动作.WARN
        else:
            return 执行动作.ALLOW

    def _生成签名(self, 检查ID: str, 目标: str, 分数: float) -> str:
        """生成安全签名"""
        内容 = f"{检查ID}{目标}{分数}{datetime.datetime.now().isoformat()}"
        return hashlib.sha256(内容.encode()).hexdigest()[:16].upper()

    def _计算复检时间(self, 等级: 风险等级) -> str:
        """计算下次复检时间"""
        现在 = datetime.datetime.now()
        if 等级 == 风险等级.高风险:
            间隔 = datetime.timedelta(hours=1)
        elif 等级 == 风险等级.中风险:
            间隔 = datetime.timedelta(days=1)
        else:
            间隔 = datetime.timedelta(days=7)

        return (现在 + 间隔).isoformat()

    def 添加白名单(self, 项: str):
        """添加白名单"""
        if 项 not in self.白名单:
            self.白名单.append(项)

    def 添加黑名单(self, 项: str):
        """添加黑名单"""
        if 项 not in self.黑名单:
            self.黑名单.append(项)

    def 获取历史(self, limit: int = 20) -> List[安全检查结果]:
        """获取检查历史"""
        return self.历史记录[-limit:]

    def 生成报告(self, 检查结果: 安全检查结果) -> str:
        """生成可读报告"""
        报告 = []
        报告.append("=" * 70)
        报告.append("🛡️ 安全风险评估报告")
        报告.append("=" * 70)
        报告.append(f"🧬 DNA: {检查结果.dna}")
        报告.append(f"📋 检查ID: {检查结果.检查ID}")
        报告.append(f"🎯 目标: {检查结果.目标} ({检查结果.目标类型})")
        报告.append(f"📊 风险等级: {检查结果.风险等级.value}")
        报告.append(f"📈 风险评分: {检查结果.风险评分}/100")
        报告.append("")
        报告.append("📋 执行动作: " + 检查结果.执行动作.value)

        if 检查结果.双因素认证:
            报告.append("🔐 双因素认证: 需要")

        if 检查结果.白名单命中:
            报告.append("✅ 白名单命中: 是")

        if 检查结果.黑名单命中:
            报告.append("❌ 黑名单命中: 是")

        报告.append("")
        报告.append("📊 风险明细:")
        for 维度, 得分 in 检查结果.风险明细.items():
            报告.append(f"  - {维度}: {得分}/100")

        报告.append("")
        报告.append("💡 防护建议:")
        for 建议 in 检查结果.防护建议:
            报告.append(f"  {建议}")

        报告.append("")
        报告.append(f"⏰ 复检时间: {检查结果.复检时间}")
        报告.append(f"🔑 安全签名: {检查结果.安全签名}")
        报告.append("=" * 70)

        return "\n".join(报告)


# ============================================================
# 四、审计日志系统
# ============================================================

class 审计日志系统:
    """安全审计日志 (append-only)"""

    def __init__(self, log_path: Optional[Path] = None):
        self.log_path = log_path or Path.home() / ".longhun/security_audit.jsonl"
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def 记录(self, 检查ID: str, 操作: str, 结果: str, 操作人: str, dna: str):
        """记录审计日志"""
        日志 = {
            "日志ID": f"LOG-{uuid.uuid4().hex[:12].upper()}",
            "检查ID": 检查ID,
            "操作": 操作,
            "结果": 结果,
            "操作人": 操作人,
            "时间戳": datetime.datetime.now().isoformat(),
            "dna": dna
        }

        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(日志, ensure_ascii=False) + '\n')
        except Exception as e:
            print(f"⚠️ 审计日志写入失败: {e}")

    def 查询(self, limit: int = 50) -> List[Dict]:
        """查询审计日志"""
        日志列表 = []
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if len(日志列表) >= limit:
                        break
                    try:
                        日志列表.append(json.loads(line.strip()))
                    except:
                        continue
        except FileNotFoundError:
            pass
        return 日志列表


# ============================================================
# 五、异常行为检测
# ============================================================

class 异常行为检测:
    """基于历史模式的异常行为检测"""

    def __init__(self):
        self.行为基线: Dict[str, 安全基线] = {}

    def 建立基线(self, 设备ID: str, 历史数据: List[Dict]):
        """建立设备行为基线"""
        if not 历史数据:
            return

        正常模式 = {
            "平均响应时间": sum(d.get("响应时间", 0) for d in 历史数据) / len(历史数据),
            "成功率": sum(1 for d in 历史数据 if d.get("成功", False)) / len(历史数据),
            "平均访问量": sum(d.get("访问量", 0) for d in 历史数据) / len(历史数据),
            "活跃时段": self._计算活跃时段(历史数据)
        }

        基线 = 安全基线(
            设备ID=设备ID,
            历史行为=历史数据,
            正常模式=正常模式,
            异常阈值=0.3,
            最后更新=datetime.datetime.now().isoformat()
        )

        self.行为基线[设备ID] = 基线

    def 检测异常(self, 设备ID: str, 当前行为: Dict) -> Dict:
        """检测当前行为是否异常"""
        if 设备ID not in self.行为基线:
            return {"异常": False, "原因": "无基线数据"}

        基线 = self.行为基线[设备ID]
        正常 = 基线.正常模式

        # 计算偏差
        偏差列表 = []

        if "响应时间" in 当前行为:
            偏差 = abs(当前行为["响应时间"] - 正常["平均响应时间"]) / (正常["平均响应时间"] + 0.001)
            if 偏差 > 基线.异常阈值:
                偏差列表.append(f"响应时间异常: {当前行为['响应时间']} (基线: {正常['平均响应时间']})")

        if "成功率" in 当前行为 and 正常["成功率"] > 0:
            偏差 = (正常["成功率"] - 当前行为["成功率"]) / 正常["成功率"]
            if 偏差 > 基线.异常阈值:
                偏差列表.append(f"成功率异常: {当前行为['成功率']} (基线: {正常['成功率']})")

        异常 = len(偏差列表) > 0

        return {
            "异常": 异常,
            "偏差": 偏差列表,
            "阈值": 基线.异常阈值,
            "设备ID": 设备ID
        }

    def _计算活跃时段(self, 历史数据: List[Dict]) -> List[int]:
        """计算活跃时段"""
        时段计数 = [0] * 24
        for d in 历史数据:
            时间 = d.get("时间", "")
            try:
                小时 = int(时间.split("T")[1].split(":")[0]) if "T" in 时间 else 0
                时段计数[小时] += 1
            except:
                pass
        # 返回前5个活跃时段
        return sorted(range(24), key=lambda i: 时段计数[i], reverse=True)[:5]


# ============================================================
# 六、告警系统
# ============================================================

class 告警系统:
    """安全告警系统"""

    def __init__(self, 告警路径: Optional[Path] = None):
        self.告警路径 = 告警路径 or Path.home() / ".longhun/alerts.jsonl"
        self.告警路径.parent.mkdir(parents=True, exist_ok=True)

    def 发送告警(self, 检查结果: 安全检查结果) -> Dict:
        """发送安全告警"""
        告警 = {
            "告警ID": f"ALT-{uuid.uuid4().hex[:8].upper()}",
            "级别": 检查结果.风险等级.value,
            "目标": 检查结果.目标,
            "动作": 检查结果.执行动作.value,
            "建议": 检查结果.防护建议[:3],
            "时间": datetime.datetime.now().isoformat(),
            "dna": 检查结果.dna
        }

        try:
            with open(self.告警路径, 'a', encoding='utf-8') as f:
                f.write(json.dumps(告警, ensure_ascii=False) + '\n')
            print(f"🚨 安全告警: {告警['级别']} - {告警['目标']}")
        except Exception as e:
            print(f"⚠️ 告警记录失败: {e}")

        return 告警


# ============================================================
# 七、与三色审计联动
# ============================================================

class 三色审计联动:
    """与三色审计系统的联动接口"""

    def __init__(self):
        self.联动历史: List[Dict] = []

    def 触发审计(self, 检查结果: 安全检查结果) -> Dict:
        """触发三色审计"""
        审计请求 = {
            "来源": "安全检查引擎",
            "检查ID": 检查结果.检查ID,
            "目标": 检查结果.目标,
            "风险等级": 检查结果.风险等级.value,
            "执行动作": 检查结果.执行动作.value,
            "建议": 检查结果.防护建议[:3],
            "dna": 检查结果.dna,
            "时间戳": datetime.datetime.now().isoformat()
        }

        self.联动历史.append(审计请求)

        # 根据风险等级决定审计颜色
        if 检查结果.风险等级 == 风险等级.高风险:
            颜色 = "🔴"
        elif 检查结果.风险等级 == 风险等级.中风险:
            颜色 = "🟡"
        else:
            颜色 = "🟢"

        return {
            "状态": "已触发",
            "颜色": 颜色,
            "消息": f"安全检查结果已进入三色审计流程，颜色: {颜色}",
            "审计请求": 审计请求
        }


# ============================================================
# 八、命令行入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 龍魂·安全风险评估引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 检查设备
  python3 lh_security_auditor.py --check "iPhone 15" --type 设备 --info '{"系统版本":"17.2","加密":true,"越狱":false}'

  # 检查数据访问
  python3 lh_security_auditor.py --check "用户数据库" --type 数据 --info '{"加密":false,"访问控制":true}'

  # 查看审计日志
  python3 lh_security_auditor.py --audit

  # 查看历史
  python3 lh_security_auditor.py --history

  # 添加白名单
  python3 lh_security_auditor.py --whitelist "内网设备"

  # 添加黑名单
  python3 lh_security_auditor.py --blacklist "未知设备"

  # 检测异常行为
  python3 lh_security_auditor.py --detect "设备A" --behavior '{"响应时间":500,"成功率":0.5}'
        """
    )

    parser.add_argument("--check", type=str, help="要检查的目标")
    parser.add_argument("--type", type=str, default="设备", choices=["设备", "系统", "数据"], help="目标类型")
    parser.add_argument("--info", type=str, default="{}", help="详细信息 (JSON)")
    parser.add_argument("--audit", action="store_true", help="查看审计日志")
    parser.add_argument("--history", action="store_true", help="查看检查历史")
    parser.add_argument("--whitelist", type=str, help="添加白名单")
    parser.add_argument("--blacklist", type=str, help="添加黑名单")
    parser.add_argument("--detect", type=str, help="检测异常行为 (设备ID)")
    parser.add_argument("--behavior", type=str, default="{}", help="当前行为 (JSON)")
    parser.add_argument("--operator", type=str, default="系统", help="操作人")

    args = parser.parse_args()

    if args.audit:
        审计 = 审计日志系统()
        日志 = 审计.查询(limit=30)
        print("📋 审计日志 (最新30条):")
        print("-" * 70)
        for log in 日志:
            print(f"  [{log.get('时间戳', '')[:19]}] {log.get('操作', '')} | {log.get('结果', '')} | {log.get('操作人', '')}")
        return

    if args.history:
        引擎 = 安全检查引擎()
        历史 = 引擎.获取历史(limit=20)
        print("📋 检查历史 (最新20条):")
        print("-" * 70)
        for r in 历史:
            print(f"  {r.风险等级.value} {r.目标} | {r.执行动作.value} | {r.风险评分}/100")
        return

    if args.whitelist:
        引擎 = 安全检查引擎()
        引擎.添加白名单(args.whitelist)
        print(f"✅ 已添加白名单: {args.whitelist}")
        return

    if args.blacklist:
        引擎 = 安全检查引擎()
        引擎.添加黑名单(args.blacklist)
        print(f"✅ 已添加黑名单: {args.blacklist}")
        return

    if args.detect:
        异常检测 = 异常行为检测()
        try:
            行为 = json.loads(args.behavior)
        except:
            行为 = {"响应时间": 100, "成功率": 1.0}

        # 建立基线（模拟）
        历史数据 = [
            {"响应时间": 50, "成功率": 0.95, "访问量": 100, "时间": "2026-01-01T08:00:00Z"},
            {"响应时间": 60, "成功率": 0.92, "访问量": 120, "时间": "2026-01-01T09:00:00Z"},
            {"响应时间": 55, "成功率": 0.94, "访问量": 110, "时间": "2026-01-01T10:00:00Z"},
        ]
        异常检测.建立基线(args.detect, 历史数据)
        结果 = 异常检测.检测异常(args.detect, 行为)
        print(json.dumps(结果, ensure_ascii=False, indent=2))
        return

    if args.check:
        引擎 = 安全检查引擎()
        try:
            信息 = json.loads(args.info)
        except:
            信息 = {"描述": args.info}

        结果 = 引擎.执行检查(args.check, args.type, 信息, args.operator)

        # 打印报告
        print(引擎.生成报告(结果))

        # 如果是高风险，发送告警
        if 结果.风险等级 == 风险等级.高风险:
            告警 = 告警系统()
            告警.发送告警(结果)

        # 与三色审计联动
        联动 = 三色审计联动()
        联动结果 = 联动.触发审计(结果)
        print(f"\n🔗 三色审计联动: {联动结果['颜色']} {联动结果['消息']}")

        return

    parser.print_help()


if __name__ == "__main__":
    main()
