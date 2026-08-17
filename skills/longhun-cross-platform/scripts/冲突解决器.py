#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂冲突解决器 — 双设备并发修改冲突处理
================================================
DNA: #龍芯⚡️2026-06-19-SYNC-MSG-v1.0
致敬: #致敬⚡️SteveJobs+Concept·跨平台互通

冲突场景:
- 鸿蒙和iOS同时修改了同一条笔记
- 鸿蒙删除了一条笔记，iOS同时修改了它
- 两个设备分别添加了不同的标签

解决策略:
1. DNA时间戳优先 — 以时间戳较新的为准（默认）
2. 字段级合并 — 不同字段分别保留
3. 人工确认 — 标记冲突等待用户决定
4. 双方保留 — 创建冲突副本，保留两个版本

三色审计:
🟢 自动解决 — 无冲突或策略自动处理
🟡 策略解决 — 按预设策略自动合并
🔴 人工确认 — 需要用户介入决策
"""

import json
import time
import copy
import logging
from typing import Dict, Any, Optional, Callable, Tuple
from enum import Enum
from dataclasses import dataclass, field

logger = logging.getLogger("冲突解决器")


# ============================================================
# 君子协议
# ============================================================
君子协议 = """
================================================================================
龍魂冲突解决器 · 君子协议
================================================================================
1. 数据冲突不可静默丢弃任一方的修改
2. 默认策略为DNA时间戳优先，但需记录审计日志
3. 删除操作与其他修改冲突时，优先保留数据
4. 需要人工确认时，双方数据都要完整展示
5. 冲突解决结果必须可追溯
================================================================================
"""


class 冲突策略(Enum):
    """冲突解决策略"""
    DNA时间戳优先 = "timestamp_priority"    # 时间戳较新的为准
    字段级合并 = "field_merge"              # 字段级智能合并
    人工确认 = "manual_confirm"             # 标记等待人工确认
    双方保留 = "both_keep"                  # 保留两个版本


class 解决类型(Enum):
    """解决结果类型"""
    无冲突 = "no_conflict"
    自动解决 = "auto_resolved"
    策略合并 = "merged"
    人工确认 = "needs_manual"
    双方保留 = "kept_both"


@dataclass
class 解决结果:
    """冲突解决结果"""
    成功: bool
    策略: 冲突策略
    类型: 解决类型
    结果数据: Dict[str, Any]
    冲突详情: Optional[Dict] = None
    审计日志: list = field(default_factory=list)
    时间戳: int = 0
    dna: str = ""


class 冲突解决器:
    """
    龍魂冲突解决器
    
    处理iOS与鸿蒙设备间的数据冲突
    提供多种策略，确保数据不丢失
    """
    
    DNA = "#龍芯⚡️2026-06-19-SYNC-MSG-v1.0"
    
    def __init__(self, 默认策略: 冲突策略 = 冲突策略.DNA时间戳优先):
        print(君子协议)
        self.默认策略 = 默认策略
        self._冲突历史: list = []
        self._人工确认回调: Optional[Callable] = None
        
        logger.info("🟢 [初始化] 冲突解决器 — 策略: %s", 默认策略.value)
    
    # ============================================================
    # 核心API
    # ============================================================
    
    def 解决(
        self,
        本地数据: Dict[str, Any],
        远程数据: Dict[str, Any],
        本地向量: Optional[Dict[str, int]] = None,
        远程向量: Optional[Dict[str, int]] = None,
        策略: Optional[冲突策略] = None
    ) -> 解决结果:
        """
        解决数据冲突
        
        流程:
        1. 检测是否真的存在冲突（内容比较）
        2. 根据策略选择解决方式
        3. 执行解决
        4. 记录审计日志
        
        Args:
            本地数据: 本机数据
            远程数据: 对端数据
            本地向量: 本地版本向量（可选）
            远程向量: 远程版本向量（可选）
            策略: 解决策略（默认使用初始化时的策略）
        
        Returns:
            解决结果对象
        """
        使用策略 = 策略 or self.默认策略
        审计日志 = []
        开始时间 = int(time.time() * 1000)
        
        # 步骤1: 检查是否真的不同
        if 本地数据 == 远程数据:
            logger.info("🟢 [冲突] 数据完全相同，无冲突")
            return 解决结果(
                成功=True,
                策略=使用策略,
                类型=解决类型.无冲突,
                结果数据=本地数据,
                审计日志=["🟢 数据完全相同，无需解决"]
            )
        
        # 步骤2: 分析冲突细节
        冲突详情 = self._分析冲突(本地数据, 远程数据)
        审计日志.append(f"🟡 检测到冲突: {冲突详情['冲突摘要']}")
        
        logger.info("🟡 [冲突] %s", 冲突详情['冲突摘要'])
        
        # 步骤3: 根据策略解决
        if 使用策略 == 冲突策略.DNA时间戳优先:
            结果 = self._时间戳优先解决(本地数据, 远程数据, 冲突详情)
        elif 使用策略 == 冲突策略.字段级合并:
            结果 = self._字段级合并解决(本地数据, 远程数据, 冲突详情)
        elif 使用策略 == 冲突策略.人工确认:
            结果 = self._人工确认解决(本地数据, 远程数据, 冲突详情)
        elif 使用策略 == 冲突策略.双方保留:
            结果 = self._双方保留解决(本地数据, 远程数据, 冲突详情)
        else:
            结果 = self._时间戳优先解决(本地数据, 远程数据, 冲突详情)
        
        # 补充元数据
        结果.策略 = 使用策略
        结果.时间戳 = 开始时间
        结果.dna = self.DNA
        结果.审计日志 = 审计日志 + 结果.审计日志
        结果.冲突详情 = 冲突详情
        
        # 记录历史
        self._冲突历史.append({
            "时间": 开始时间,
            "策略": 使用策略.value,
            "结果类型": 结果.类型.value,
            "冲突摘要": 冲突详情['冲突摘要'],
            "成功": 结果.成功
        })
        
        return 结果
    
    # ============================================================
    # 策略实现
    # ============================================================
    
    def _时间戳优先解决(
        self,
        本地数据: Dict,
        远程数据: Dict,
        冲突详情: Dict
    ) -> 解决结果:
        """
        策略: 以时间戳较新的数据为准
        
        比较 sync_time / updated_at / timestamp 字段
        """
        本地时间 = self._提取时间戳(本地数据)
        远程时间 = self._提取时间戳(远程数据)
        
        if 本地时间 > 远程时间:
            结果数据 = copy.deepcopy(本地数据)
            结果数据["_conflict_resolved"] = {
                "strategy": "timestamp_priority",
                "winner": "local",
                "local_time": 本地时间,
                "remote_time": 远程时间,
                "resolution_time": int(time.time() * 1000)
            }
            logger.info("🟢 [解决] 时间戳优先: 本地较新 (%d > %d)", 本地时间, 远程时间)
            return 解决结果(
                成功=True,
                策略=冲突策略.DNA时间戳优先,
                类型=解决类型.自动解决,
                结果数据=结果数据,
                审计日志=[f"🟢 本地时间戳较新 ({本地时间} > {远程_time})，采用本地数据"]
            )
        elif 远程时间 > 本地时间:
            结果数据 = copy.deepcopy(远程数据)
            结果数据["_conflict_resolved"] = {
                "strategy": "timestamp_priority",
                "winner": "remote",
                "local_time": 本地时间,
                "remote_time": 远程时间,
                "resolution_time": int(time.time() * 1000)
            }
            logger.info("🟢 [解决] 时间戳优先: 远程较新 (%d > %d)", 远程时间, 本地时间)
            return 解决结果(
                成功=True,
                策略=冲突策略.DNA时间戳优先,
                类型=解决类型.自动解决,
                结果数据=结果数据,
                审计日志=[f"🟢 远程时间戳较新 ({远程_time} > {本地时间})，采用远程数据"]
            )
        else:
            # 时间戳相同，回退到字段级合并
            logger.warning("🟡 [解决] 时间戳相同，回退到字段级合并")
            return self._字段级合并解决(本地数据, 远程数据, 冲突详情)
    
    def _字段级合并解决(
        self,
        本地数据: Dict,
        远程数据: Dict,
        冲突详情: Dict
    ) -> 解决结果:
        """
        策略: 字段级智能合并
        
        - 仅一方有的字段: 保留
        - 双方都有且相同: 保留
        - 双方都有且不同: 优先较新的（有时间戳）或都保留为数组
        """
        合并结果 = {}
        合并日志 = []
        
        所有键 = set(本地数据.keys()) | set(远程数据.keys())
        
        for 键 in 所有键:
            本地有 = 键 in 本地数据
            远程有 = 键 in 远程数据
            
            if 本地有 and not 远程有:
                合并结果[键] = 本地数据[键]
            elif 远程有 and not 本地有:
                合并结果[键] = 远程数据[键]
            else:
                # 双方都有
                if 本地数据[键] == 远程数据[键]:
                    合并结果[键] = 本地数据[键]
                else:
                    # 冲突字段 — 尝试智能合并
                    合并值 = self._智能合并字段(键, 本地数据[键], 远程数据[键])
                    合并结果[键] = 合并值
                    if isinstance(合并值, list) and len(合并值) == 2:
                        合并日志.append(f"🟡 字段'{键}'保留双版本")
                    else:
                        合并日志.append(f"🟢 字段'{键}'已智能合并")
        
        # 添加解决标记
        合并结果["_conflict_resolved"] = {
            "strategy": "field_merge",
            "merged_fields": len(冲突详情.get("冲突字段", [])),
            "resolution_time": int(time.time() * 1000)
        }
        
        logger.info("🟢 [解决] 字段级合并完成，合并了 %d 个冲突字段",
                     len(冲突详情.get("冲突字段", [])))
        
        return 解决结果(
            成功=True,
            策略=冲突策略.字段级合并,
            类型=解决类型.策略合并,
            结果数据=合并结果,
            审计日志=合并日志 or ["🟢 所有字段已合并"]
        )
    
    def _人工确认解决(
        self,
        本地数据: Dict,
        远程数据: Dict,
        冲突详情: Dict
    ) -> 解决结果:
        """
        策略: 标记为需要人工确认
        
        保留双方数据，添加冲突标记，等待用户决策
        """
        结果数据 = {
            "_conflict_flag": True,
            "_conflict_info": {
                "strategy": "manual_confirm",
                "conflict_time": int(time.time() * 1000),
                "summary": 冲突详情.get("冲突摘要", ""),
                "conflicting_fields": [f["字段"] for f in 冲突详情.get("冲突字段", [])]
            },
            "_local_version": copy.deepcopy(本地数据),
            "_remote_version": copy.deepcopy(远程数据),
            # 默认以较新的作为预览
        }
        
        # 如果设置了回调，触发通知
        if self._人工确认回调:
            try:
                self._人工确认回调(结果数据)
            except Exception as e:
                logger.error("🔴 [回调] 人工确认回调失败: %s", str(e))
        
        logger.warning("🔴 [冲突] 需要人工确认: %s", 冲突详情.get("冲突摘要", ""))
        
        return 解决结果(
            成功=True,  # 技术层面"成功"标记为待确认
            策略=冲突策略.人工确认,
            类型=解决类型.人工确认,
            结果数据=结果数据,
            审计日志=[
                f"🔴 冲突需要人工确认: {冲突详情.get('冲突摘要', '')}",
                f"🔴 冲突字段: {[f['字段'] for f in 冲突详情.get('冲突字段', [])]}"
            ]
        )
    
    def _双方保留解决(
        self,
        本地数据: Dict,
        远程数据: Dict,
        冲突详情: Dict
    ) -> 解决结果:
        """
        策略: 保留两个版本
        
        创建包含两个版本的包装数据
        """
        结果数据 = {
            "_conflict_flag": True,
            "_conflict_info": {
                "strategy": "both_keep",
                "resolution_time": int(time.time() * 1000),
                "summary": 冲突详情.get("冲突摘要", "")
            },
            "_versions": [
                {
                    "source": "local",
                    "data": copy.deepcopy(本地数据),
                    "timestamp": self._提取时间戳(本地数据)
                },
                {
                    "source": "remote",
                    "data": copy.deepcopy(远程数据),
                    "timestamp": self._提取时间戳(远程数据)
                }
            ]
        }
        
        logger.info("🟡 [解决] 双方保留，创建 %d 个版本", 2)
        
        return 解决结果(
            成功=True,
            策略=冲突策略.双方保留,
            类型=解决类型.双方保留,
            结果数据=结果数据,
            审计日志=["🟡 双方数据均已保留，共2个版本"]
        )
    
    # ============================================================
    # 辅助方法
    # ============================================================
    
    def _分析冲突(self, 本地: Dict, 远程: Dict) -> Dict:
        """分析冲突的具体差异"""
        本地键 = set(本地.keys())
        远程键 = set(远程.keys())
        
        仅本地 = list(本地键 - 远程键)
        仅远程 = list(远程键 - 本地键)
        共同键 = 本地键 & 远程键
        
        冲突字段 = []
        for 键 in 共同键:
            if 本地[键] != 远程[键]:
                本地值 = str(本地[键])[:50]
                远程值 = str(远程[键])[:50]
                冲突字段.append({
                    "字段": 键,
                    "本地值": 本地值,
                    "远程值": 远程值
                })
        
        return {
            "冲突字段数": len(冲突字段),
            "冲突字段": 冲突字段,
            "仅本地有": 仅本地,
            "仅远程有": 仅远程,
            "冲突摘要": f"{len(冲突字段)}字段冲突, {len(仅本地)}仅本地, {len(仅远程)}仅远程"
        }
    
    def _提取时间戳(self, 数据: Dict) -> int:
        """从数据中提取时间戳"""
        时间戳字段 = ["sync_time", "updated_at", "timestamp", "modified_at", "time", "created_at"]
        for 字段 in 时间戳字段:
            if 字段 in 数据 and isinstance(数据[字段], (int, float)):
                return int(数据[字段])
        return 0  # 默认返回0（最早）
    
    def _智能合并字段(self, 字段名: str, 本地值: Any, 远程值: Any) -> Any:
        """智能合并单个字段"""
        # 列表类型: 取并集
        if isinstance(本地值, list) and isinstance(远程值, list):
            合并列表 = list(本地值)  # 复制
            for 项 in 远程值:
                if 项 not in 合并列表:
                    合并列表.append(项)
            return 合并列表
        
        # 字符串类型: 取较长的（通常包含更多信息）
        if isinstance(本地值, str) and isinstance(远程值, str):
            if len(远程值) > len(本地值):
                return 远程值
            return 本地值
        
        # 数字类型: 取较大值（适用于计数、版本等）
        if isinstance(本地值, (int, float)) and isinstance(远程值, (int, float)):
            return max(本地值, 远程值)
        
        # 默认: 包装为双版本列表
        return [本地值, 远程值]
    
    # ============================================================
    # 人工确认接口
    # ============================================================
    
    def 设置人工确认回调(self, 回调: Callable):
        """设置人工确认通知回调"""
        self._人工确认回调 = 回调
    
    def 人工确认解决(self, 冲突ID: str, 选择: str, 本地数据: Dict, 远程数据: Dict) -> 解决结果:
        """
        用户人工选择解决冲突
        
        Args:
            冲突ID: 冲突标识
            选择: "local" | "remote" | "merge"
            本地数据: 本地版本
            远程数据: 远程版本
        
        Returns:
            解决结果
        """
        if 选择 == "local":
            结果数据 = copy.deepcopy(本地数据)
            日志 = ["🟢 人工选择: 保留本地版本"]
        elif 选择 == "remote":
            结果数据 = copy.deepcopy(远程数据)
            日志 = ["🟢 人工选择: 保留远程版本"]
        elif 选择 == "merge":
            冲突详情 = self._分析冲突(本地数据, 远程数据)
            return self._字段级合并解决(本地数据, 远程数据, 冲突详情)
        else:
            return 解决结果(
                成功=False,
                策略=冲突策略.人工确认,
                类型=解决类型.人工确认,
                结果数据={},
                审计日志=[f"🔴 无效选择: {选择}"]
            )
        
        结果数据["_conflict_resolved"] = {
            "strategy": "manual_confirm",
            "choice": 选择,
            "resolution_time": int(time.time() * 1000)
        }
        
        logger.info("🟢 [人工] 冲突已解决: 选择 %s", 选择)
        
        return 解决结果(
            成功=True,
            策略=冲突策略.人工确认,
            类型=解决类型.自动解决,
            结果数据=结果数据,
            审计日志=日志
        )
    
    # ============================================================
    # 统计与诊断
    # ============================================================
    
    def 获取历史(self) -> list:
        """获取冲突解决历史"""
        return copy.deepcopy(self._冲突历史)
    
    def 获取统计(self) -> Dict[str, Any]:
        """获取冲突解决统计"""
        if not self._冲突历史:
            return {"总冲突数": 0}
        
        自动解决 = sum(1 for h in self._冲突历史 if h["结果类型"] == "auto_resolved")
        人工确认 = sum(1 for h in self._冲突历史 if h["结果类型"] == "needs_manual")
        双方保留 = sum(1 for h in self._冲突历史 if h["结果类型"] == "kept_both")
        
        return {
            "总冲突数": len(self._冲突历史),
            "自动解决": 自动解决,
            "人工确认": 人工确认,
            "双方保留": 双方保留,
            "默认策略": self.默认策略.value,
            "dna": self.DNA
        }
    
    def 打印统计(self):
        """打印冲突解决统计"""
        print(f"\n{'='*50}")
        print("  冲突解决统计")
        print(f"{'='*50}")
        统计 = self.获取统计()
        for k, v in 统计.items():
            print(f"  {k}: {v}")
        print(f"{'='*50}\n")


# ============================================================
# 测试入口
# ============================================================

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print("  龍魂冲突解决器 — 测试")
    print(f"{'='*60}\n")
    
    解决器 = 冲突解决器(冲突策略.DNA时间戳优先)
    
    # 测试数据
    本地数据 = {
        "id": "note-001",
        "title": "购物清单（鸿蒙修改）",
        "items": ["牛奶", "面包"],
        "sync_time": 1718800000000,
        "harmony_only": "鸿蒙标签"
    }
    
    远程数据 = {
        "id": "note-001",
        "title": "购物清单（iOS修改）",
        "items": ["牛奶", "鸡蛋"],
        "sync_time": 1718800001000,  # iOS更新
        "ios_only": "iOS标签"
    }
    
    print("本地数据:", json.dumps(本地数据, indent=2, ensure_ascii=False))
    print("\n远程数据:", json.dumps(远程数据, indent=2, ensure_ascii=False))
    print()
    
    # 测试策略1: 时间戳优先
    print("[测试] 策略: DNA时间戳优先...")
    结果 = 解决器.解决(本地数据, 远程数据, 策略=冲突策略.DNA时间戳优先)
    print(f"  结果类型: {结果.类型.value}")
    print(f"  审计: {结果.审计日志}")
    
    # 测试策略2: 字段级合并
    print("\n[测试] 策略: 字段级合并...")
    结果 = 解决器.解决(本地数据, 远程数据, 策略=冲突策略.字段级合并)
    print(f"  结果类型: {结果.类型.value}")
    print(f"  合并结果:")
    for k, v in 结果.结果数据.items():
        if not k.startswith("_"):
            print(f"    {k}: {v}")
    
    # 测试策略3: 人工确认
    print("\n[测试] 策略: 人工确认...")
    结果 = 解决器.解决(本地数据, 远程数据, 策略=冲突策略.人工确认)
    print(f"  结果类型: {结果.类型.value}")
    print(f"  冲突标记: {结果.结果数据.get('_conflict_flag', False)}")
    
    # 打印统计
    解决器.打印统计()
