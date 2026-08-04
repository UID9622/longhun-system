#!/usr/bin/env python3
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
🐉 龍魂·强化学习反馈循环引擎 v1.0
DNA: #ZHUGEXIN⚡️丙午·乙未·甲辰-强化学习循环-v1.0
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

定位：系统的"大脑"，从经验中学习，奖励好行为，惩罚坏行为。
目标：让系统越用越聪明，但不越界。

核心组件：
  1. 数据收集器 — 采集用户行为、系统响应、结果反馈
  2. 模式识别器 — 识别高效/低效模式
  3. 奖惩判定器 — 计算奖惩积分，决定权重调整
  4. 权重更新器 — 动态调整模板权重
  5. 全局同步器 — 同步学习成果到所有实例
  6. 安全边界检查 — 防止权重越界/过拟合
  7. 时间衰减因子 — 旧数据影响力递减
  8. 学习报告生成器 — 输出学习建议和决策
  9. A/B测试框架 — 对比新旧策略效果
  10. 反馈循环终止条件 — 防止无限循环
"""

import json
import uuid
import math
import copy
import sqlite3
import hashlib
import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict

# ============================================================
# 一、数据结构
# ============================================================

class 学习模式(Enum):
    探索 = "explore"  # 尝试新策略
    利用 = "exploit"   # 利用已知最优
    平衡 = "balance"   # 两者平衡

@dataclass
class 行为记录:
    """单次行为记录"""
    id: str
    模板ID: str
    用户行为: Dict[str, Any]
    系统响应: Dict[str, Any]
    结果反馈: Dict[str, Any]
    时间戳: str
    奖励分数: float = 0.0
    惩罚分数: float = 0.0

@dataclass
class 模板权重:
    """模板权重"""
    模板ID: str
    权重: float
    历史表现: List[float]
    成功次数: int
    失败次数: int
    总使用次数: int
    最后更新: str

@dataclass
class 奖惩决策:
    """奖惩决策结果"""
    模板ID: str
    奖励积分: float
    惩罚积分: float
    旧权重: float
    新权重: float
    原因: str
    是否淘汰: bool = False

@dataclass
class 学习报告:
    """学习报告"""
    报告ID: str
    时间: str
    总行为数: int
    优质模式: List[str]
    低效模式: List[str]
    奖惩决策: List[奖惩决策]
    权重调整: Dict[str, float]
    淘汰清单: List[str]
    学习建议: List[str]
    dna: str


# ============================================================
# 二、数据收集器
# ============================================================

class 数据收集器:
    """收集用户行为、系统响应、结果反馈"""

    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or Path.home() / ".longhun/rl_history.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            CREATE TABLE IF NOT EXISTS behaviors (
                id TEXT PRIMARY KEY,
                template_id TEXT,
                user_behavior TEXT,
                system_response TEXT,
                result_feedback TEXT,
                timestamp TEXT,
                reward REAL DEFAULT 0,
                penalty REAL DEFAULT 0,
                processed INTEGER DEFAULT 0
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS templates (
                template_id TEXT PRIMARY KEY,
                weight REAL DEFAULT 1.0,
                history TEXT,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                total_uses INTEGER DEFAULT 0,
                last_update TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_decisions (
                id TEXT PRIMARY KEY,
                template_id TEXT,
                decision TEXT,
                reason TEXT,
                old_weight REAL,
                new_weight REAL,
                timestamp TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS patterns (
                id TEXT PRIMARY KEY,
                pattern_type TEXT,
                features TEXT,
                weight REAL,
                created_at TEXT,
                last_used TEXT
            )
        """)
        conn.commit()
        conn.close()

    def collect(self, 模板ID: str, 用户行为: Dict, 系统响应: Dict, 结果反馈: Dict) -> 行为记录:
        """收集一次行为数据"""
        记录 = 行为记录(
            id=str(uuid.uuid4()),
            模板ID=模板ID,
            用户行为=用户行为,
            系统响应=系统响应,
            结果反馈=结果反馈,
            时间戳=datetime.datetime.now().isoformat()
        )

        conn = sqlite3.connect(str(self.db_path))
        conn.execute("""
            INSERT INTO behaviors (id, template_id, user_behavior, system_response, result_feedback, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            记录.id,
            记录.模板ID,
            json.dumps(记录.用户行为),
            json.dumps(记录.系统响应),
            json.dumps(记录.结果反馈),
            记录.时间戳
        ))
        conn.commit()
        conn.close()

        return 记录

    def get_unprocessed(self, limit: int = 100) -> List[行为记录]:
        """获取未处理的行为记录"""
        conn = sqlite3.connect(str(self.db_path))
        cur = conn.execute("""
            SELECT id, template_id, user_behavior, system_response, result_feedback, timestamp
            FROM behaviors WHERE processed = 0 LIMIT ?
        """, (limit,))
        rows = cur.fetchall()
        conn.close()

        records = []
        for row in rows:
            records.append(行为记录(
                id=row[0],
                模板ID=row[1],
                用户行为=json.loads(row[2]),
                系统响应=json.loads(row[3]),
                结果反馈=json.loads(row[4]),
                时间戳=row[5]
            ))
        return records

    def mark_processed(self, 记录ID: str):
        """标记为已处理"""
        conn = sqlite3.connect(str(self.db_path))
        conn.execute("UPDATE behaviors SET processed = 1 WHERE id = ?", (记录ID,))
        conn.commit()
        conn.close()


# ============================================================
# 三、模式识别器
# ============================================================

class 模式识别器:
    """识别高效/低效模式"""

    def __init__(self):
        self.高效特征 = ["用户重复使用", "响应速度快", "错误率低", "资源消耗少", "用户满意度高"]
        self.低效特征 = ["用户频繁放弃", "响应速度慢", "错误率高", "资源消耗大", "用户投诉"]
        self.模式库 = {}

    def 识别(self, 行为记录: 行为记录) -> Dict:
        """识别模式类型"""
        结果 = {
            "类型": "未知",
            "特征": [],
            "分数": 0.0,
            "证据": []
        }

        高效得分 = 0
        低效得分 = 0

        # 检查高效特征
        for 特征 in self.高效特征:
            if 特征 in str(行为记录.用户行为) or 特征 in str(行为记录.系统响应) or 特征 in str(行为记录.结果反馈):
                高效得分 += 1
                结果["特征"].append(f"✅ {特征}")
                结果["证据"].append(特征)

        # 检查低效特征
        for 特征 in self.低效特征:
            if 特征 in str(行为记录.用户行为) or 特征 in str(行为记录.系统响应) or 特征 in str(行为记录.结果反馈):
                低效得分 += 1
                结果["特征"].append(f"❌ {特征}")
                结果["证据"].append(特征)

        # 判断类型
        if 高效得分 > 低效得分:
            结果["类型"] = "高效模式"
            结果["分数"] = 高效得分 / (高效得分 + 低效得分 + 1)
        elif 低效得分 > 高效得分:
            结果["类型"] = "低效模式"
            结果["分数"] = 低效得分 / (高效得分 + 低效得分 + 1)
        else:
            结果["类型"] = "混合模式"
            结果["分数"] = 0.5

        return 结果


# ============================================================
# 四、奖惩判定器
# ============================================================

class 奖惩判定器:
    """
    奖惩判定器 — 计算奖惩积分，决定权重调整

    规则：
      奖励：提升用户体验/优化系统效率 → +10分，权重×1.2
      惩罚：降低用户体验/浪费系统资源 → -10分，权重×0.8
      淘汰：惩罚积分 < -50 → 淘汰该模式
    """

    # 奖励规则
    奖励规则 = [
        {"条件": "用户满意度 > 0.8", "积分": 15, "倍率": 1.3},
        {"条件": "响应时间 < 100", "积分": 10, "倍率": 1.2},
        {"条件": "错误率 == 0", "积分": 10, "倍率": 1.2},
        {"条件": "用户重复使用", "积分": 8, "倍率": 1.15},
        {"条件": "任务完成率 > 0.9", "积分": 12, "倍率": 1.25},
    ]

    # 惩罚规则
    惩罚规则 = [
        {"条件": "用户满意度 < 0.3", "积分": -15, "倍率": 0.7},
        {"条件": "响应时间 > 1000", "积分": -10, "倍率": 0.8},
        {"条件": "错误率 > 0.2", "积分": -12, "倍率": 0.75},
        {"条件": "用户频繁放弃", "积分": -10, "倍率": 0.8},
        {"条件": "任务完成率 < 0.3", "积分": -15, "倍率": 0.7},
    ]

    # 淘汰阈值
    淘汰阈值 = -50

    def __init__(self):
        self.历史奖惩: Dict[str, float] = defaultdict(float)

    def 判定(self, 行为记录: 行为记录, 模式结果: Dict) -> 奖惩决策:
        """执行奖惩判定"""
        模板ID = 行为记录.模板ID
        总奖励 = 0.0
        总惩罚 = 0.0
        原因列表 = []

        # 检查奖励规则
        for 规则 in self.奖励规则:
            if self._检查条件(规则["条件"], 行为记录):
                总奖励 += 规则["积分"]
                原因列表.append(f"✅ {规则['条件']} (+{规则['积分']})")

        # 检查惩罚规则
        for 规则 in self.惩罚规则:
            if self._检查条件(规则["条件"], 行为记录):
                总惩罚 += 规则["积分"]
                原因列表.append(f"❌ {规则['条件']} ({规则['积分']})")

        # 模式类型修正
        if 模式结果["类型"] == "高效模式":
            总奖励 += 5
            原因列表.append("📈 高效模式 (+5)")
        elif 模式结果["类型"] == "低效模式":
            总惩罚 -= 5
            原因列表.append("📉 低效模式 (-5)")

        # 计算净积分
        净积分 = 总奖励 + 总惩罚

        # 更新历史
        self.历史奖惩[模板ID] += 净积分

        # 计算权重调整
        if 净积分 > 0:
            权重调整 = 1.0 + (净积分 / 100)
            新权重 = min(2.0, 权重调整)  # 上限2.0
        else:
            权重调整 = 1.0 + (净积分 / 100)
            新权重 = max(0.1, 权重调整)  # 下限0.1

        # 判断是否淘汰
        是否淘汰 = self.历史奖惩[模板ID] < self.淘汰阈值

        return 奖惩决策(
            模板ID=模板ID,
            奖励积分=总奖励,
            惩罚积分=总惩罚,
            旧权重=1.0,  # 实际应从数据库读取
            新权重=新权重,
            原因=", ".join(原因列表) if 原因列表 else "无显著奖惩信号",
            是否淘汰=是否淘汰
        )

    def _检查条件(self, 条件: str, 记录: 行为记录) -> bool:
        """检查条件是否满足"""
        # 简单实现：检查条件和数据是否匹配
        数据文本 = json.dumps({
            "用户行为": 记录.用户行为,
            "系统响应": 记录.系统响应,
            "结果反馈": 记录.结果反馈
        }, ensure_ascii=False)

        if ">" in 条件:
            # 数值比较
            try:
                key, value = 条件.split(">")
                key = key.strip()
                value = float(value.strip())
                # 在数据中查找对应值
                for source in [记录.用户行为, 记录.系统响应, 记录.结果反馈]:
                    if isinstance(source, dict) and key in source:
                        return float(source[key]) > value
            except:
                pass
        elif "<" in 条件:
            try:
                key, value = 条件.split("<")
                key = key.strip()
                value = float(value.strip())
                for source in [记录.用户行为, 记录.系统响应, 记录.结果反馈]:
                    if isinstance(source, dict) and key in source:
                        return float(source[key]) < value
            except:
                pass
        else:
            # 字符串包含
            return 条件 in 数据文本

        return False


# ============================================================
# 五、权重更新器
# ============================================================

class 权重更新器:
    """动态调整模板权重，包含时间衰减和安全边界"""

    # 安全边界
    权重上限 = 2.0
    权重下限 = 0.1
    学习率 = 0.1
    时间衰减系数 = 0.95  # 每天衰减

    def __init__(self):
        self.权重历史: Dict[str, List[float]] = defaultdict(list)

    def 更新(self, 模板ID: str, 决策: 奖惩决策, 当前时间: Optional[str] = None) -> Tuple[float, Dict]:
        """更新权重"""
        当前时间 = 当前时间 or datetime.datetime.now().isoformat()

        # 获取旧权重（从数据库或历史）
        旧权重 = 决策.旧权重

        # 时间衰减
        衰减因子 = self._计算时间衰减(模板ID)

        # 基础更新
        奖惩调整 = 1.0 + (决策.奖励积分 + 决策.惩罚积分) / 100 * self.学习率

        # 综合新权重
        新权重 = 旧权重 * 衰减因子 * 奖惩调整

        # 安全边界限制
        新权重 = max(self.权重下限, min(self.权重上限, 新权重))

        # 记录历史
        self.权重历史[模板ID].append(新权重)

        return 新权重, {
            "旧权重": 旧权重,
            "衰减因子": 衰减因子,
            "奖惩调整": 奖惩调整,
            "学习率": self.学习率
        }

    def _计算时间衰减(self, 模板ID: str) -> float:
        """计算时间衰减因子"""
        # 如果没有历史，返回1.0
        if 模板ID not in self.权重历史:
            return 1.0

        # 历史越长，衰减越小（旧数据影响力递减）
        历史长度 = len(self.权重历史[模板ID])
        if 历史长度 == 0:
            return 1.0

        # 使用时间衰减公式
        衰减因子 = self.时间衰减系数 ** (1 / (历史长度 + 1))
        return 衰减因子

    def 安全边界检查(self, 新权重: float) -> bool:
        """检查权重是否在安全边界内"""
        return self.权重下限 <= 新权重 <= self.权重上限


# ============================================================
# 六、全局同步器
# ============================================================

@dataclass
class 全局同步状态:
    模式特征库: List[Dict]
    权重矩阵: Dict[str, float]
    高效路径: List[str]
    淘汰清单: List[str]
    版本: str
    最后同步: str

class 全局同步器:
    """同步学习成果到所有实例"""

    def __init__(self, sync_path: Optional[Path] = None):
        self.sync_path = sync_path or Path.home() / ".longhun/rl_sync.json"
        self.sync_path.parent.mkdir(parents=True, exist_ok=True)
        self.冲突解决策略 = "时间戳优先"  # 或 "权重优先"

    def 同步(self, 本地状态: Dict) -> Dict:
        """同步到全局"""
        # 读取全局状态
        全局状态 = self._读取全局()

        # 合并（带冲突检测）
        合并状态 = self._合并(全局状态, 本地状态)

        # 写入全局
        self._写入全局(合并状态)

        return 合并状态

    def _读取全局(self) -> Dict:
        if self.sync_path.exists():
            with open(self.sync_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"版本": "1.0", "权重矩阵": {}, "模式特征库": [], "高效路径": [], "淘汰清单": []}

    def _写入全局(self, 状态: Dict):
        状态["最后同步"] = datetime.datetime.now().isoformat()
        with open(self.sync_path, 'w', encoding='utf-8') as f:
            json.dump(状态, f, ensure_ascii=False, indent=2)

    def _合并(self, 全局: Dict, 本地: Dict) -> Dict:
        """合并两个状态，处理冲突"""
        合并后 = copy.deepcopy(全局)

        # 合并权重矩阵（本地优先）
        if "权重矩阵" in 本地:
            for 模板ID, 权重 in 本地["权重矩阵"].items():
                if 模板ID in 合并后.get("权重矩阵", {}):
                    # 冲突解决：取最大权重（鼓励探索）
                    合并后["权重矩阵"][模板ID] = max(权重, 合并后["权重矩阵"][模板ID])
                else:
                    合并后["权重矩阵"][模板ID] = 权重

        # 合并模式特征库（去重）
        if "模式特征库" in 本地:
            现有模式 = {p.get("特征", "") for p in 合并后.get("模式特征库", [])}
            for 模式 in 本地["模式特征库"]:
                特征 = 模式.get("特征", "")
                if 特征 and 特征 not in 现有模式:
                    合并后["模式特征库"].append(模式)

        # 合并高效路径（去重）
        if "高效路径" in 本地:
            合并后["高效路径"] = list(set(合并后.get("高效路径", []) + 本地["高效路径"]))

        # 合并淘汰清单（取并集）
        if "淘汰清单" in 本地:
            合并后["淘汰清单"] = list(set(合并后.get("淘汰清单", []) + 本地["淘汰清单"]))

        合并后["版本"] = f"v{float(合并后.get('版本', '1.0').replace('v', '')) + 0.1:.1f}"

        return 合并后


# ============================================================
# 七、学习报告生成器
# ============================================================

class 学习报告生成器:
    """生成学习报告"""

    def __init__(self):
        self.报告历史: List[学习报告] = []

    def 生成(self, 所有记录: List[行为记录], 所有决策: List[奖惩决策],
             权重调整: Dict, 淘汰清单: List[str]) -> 学习报告:

        报告 = 学习报告(
            报告ID=f"RPT-{datetime.datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}",
            时间=datetime.datetime.now().isoformat(),
            总行为数=len(所有记录),
            优质模式=[],
            低效模式=[],
            奖惩决策=所有决策,
            权重调整=权重调整,
            淘汰清单=淘汰清单,
            学习建议=[],
            dna=f"#ZHUGEXIN⚡️{datetime.datetime.now().strftime('%Y-%m-%d')}-LEARN-{uuid.uuid4().hex[:8].upper()}"
        )

        # 提取优质/低效模式
        for 决策 in 所有决策:
            if 决策.奖励积分 > 0:
                报告.优质模式.append(决策.模板ID)
            if 决策.惩罚积分 < 0:
                报告.低效模式.append(决策.模板ID)

        # 生成学习建议
        报告.学习建议 = self._生成建议(所有决策, 权重调整)

        self.报告历史.append(报告)
        return 报告

    def _生成建议(self, 决策列表: List[奖惩决策], 权重调整: Dict) -> List[str]:
        建议 = []

        # 分析高效模式
        高效模板 = [d.模板ID for d in 决策列表 if d.奖励积分 > 0]
        if 高效模板:
            建议.append(f"📈 发现高效模式：{', '.join(高效模板[:3])}，建议推广使用")
        else:
            建议.append("📊 暂无显著高效模式，建议继续探索")

        # 分析低效模式
        低效模板 = [d.模板ID for d in 决策列表 if d.惩罚积分 < 0]
        if 低效模板:
            建议.append(f"📉 发现低效模式：{', '.join(低效模板[:3])}，建议优化或淘汰")

        # 权重调整建议
        增加模板 = [k for k, v in 权重调整.items() if v > 1.0]
        减少模板 = [k for k, v in 权重调整.items() if v < 1.0]
        if 增加模板:
            建议.append(f"⬆️ 建议提升权重：{', '.join(增加模板[:3])}")
        if 减少模板:
            建议.append(f"⬇️ 建议降低权重：{', '.join(减少模板[:3])}")

        # 学习率建议
        建议.append(f"🎯 当前学习率：{权重更新器.学习率}，建议保持稳定")

        return 建议


# ============================================================
# 八、主引擎：强化学习反馈循环
# ============================================================

class 强化学习反馈循环:
    """龙魂系统学习引擎主控"""

    def __init__(self):
        self.收集器 = 数据收集器()
        self.识别器 = 模式识别器()
        self.判定器 = 奖惩判定器()
        self.更新器 = 权重更新器()
        self.同步器 = 全局同步器()
        self.报告生成器 = 学习报告生成器()

        self.学习历史: List[行为记录] = []
        self.决策历史: List[奖惩决策] = []
        self.运行次数 = 0
        self.最大迭代次数 = 1000  # 反馈循环终止条件

    def 运行一次(self, 模板ID: str, 用户行为: Dict, 系统响应: Dict, 结果反馈: Dict) -> Dict:
        """
        执行一次完整的学习循环

        流程：收集 → 识别 → 判定 → 更新 → 同步
        """
        self.运行次数 += 1

        # 检查终止条件
        if self.运行次数 > self.最大迭代次数:
            return {"状态": "终止", "原因": f"达到最大迭代次数 {self.最大迭代次数}"}

        # 1. 数据收集
        记录 = self.收集器.collect(模板ID, 用户行为, 系统响应, 结果反馈)
        self.学习历史.append(记录)

        # 2. 模式识别
        模式结果 = self.识别器.识别(记录)

        # 3. 奖惩判定
        决策 = self.判定器.判定(记录, 模式结果)
        self.决策历史.append(决策)

        # 4. 权重更新
        新权重, 调整详情 = self.更新器.更新(模板ID, 决策)

        # 5. 安全边界检查
        if not self.更新器.安全边界检查(新权重):
            return {
                "状态": "警告",
                "原因": f"权重 {新权重} 超出安全边界 [{更新器.权重下限}, {更新器.权重上限}]",
                "决策": 决策
            }

        # 6. 标记已处理
        self.收集器.mark_processed(记录.id)

        # 7. 返回结果
        return {
            "状态": "成功",
            "记录": 记录,
            "模式": 模式结果,
            "决策": 决策,
            "新权重": 新权重,
            "调整详情": 调整详情,
            "运行次数": self.运行次数
        }

    def 批量运行(self, 批量数据: List[Dict]) -> Dict:
        """批量处理多条行为记录"""
        结果列表 = []
        总决策 = []

        for 数据 in 批量数据:
            结果 = self.运行一次(
                模板ID=数据.get("模板ID", "unknown"),
                用户行为=数据.get("用户行为", {}),
                系统响应=数据.get("系统响应", {}),
                结果反馈=数据.get("结果反馈", {})
            )
            结果列表.append(结果)
            if "决策" in 结果:
                总决策.append(结果["决策"])

        return {
            "总处理": len(结果列表),
            "成功": sum(1 for r in 结果列表 if r.get("状态") == "成功"),
            "警告": sum(1 for r in 结果列表 if r.get("状态") == "警告"),
            "终止": sum(1 for r in 结果列表 if r.get("状态") == "终止"),
            "结果": 结果列表
        }

    def 生成学习报告(self) -> 学习报告:
        """生成学习报告"""
        return self.报告生成器.生成(
            所有记录=self.学习历史,
            所有决策=self.决策历史,
            权重调整={d.模板ID: d.新权重 for d in self.决策历史},
            淘汰清单=[d.模板ID for d in self.决策历史 if d.是否淘汰]
        )

    def 同步全局(self) -> Dict:
        """同步全局状态"""
        本地状态 = {
            "权重矩阵": {d.模板ID: d.新权重 for d in self.决策历史[-20:]},
            "模式特征库": [],  # 简化
            "高效路径": [d.模板ID for d in self.决策历史 if d.奖励积分 > 0],
            "淘汰清单": [d.模板ID for d in self.决策历史 if d.是否淘汰]
        }
        return self.同步器.同步(本地状态)


# ============================================================
# 九、A/B测试框架
# ============================================================

class AB测试框架:
    """A/B测试框架 — 对比新旧策略效果"""

    def __init__(self):
        self.测试结果: Dict[str, Dict] = {}

    def 创建测试(self, 测试ID: str, A策略: Dict, B策略: Dict) -> Dict:
        """创建A/B测试"""
        self.测试结果[测试ID] = {
            "A策略": A策略,
            "B策略": B策略,
            "A结果": [],
            "B结果": [],
            "开始时间": datetime.datetime.now().isoformat(),
            "状态": "运行中"
        }
        return self.测试结果[测试ID]

    def 记录结果(self, 测试ID: str, 策略: str, 结果: Dict) -> Dict:
        """记录测试结果"""
        if 测试ID not in self.测试结果:
            return {"错误": "测试不存在"}

        if 策略 == "A":
            self.测试结果[测试ID]["A结果"].append(结果)
        elif 策略 == "B":
            self.测试结果[测试ID]["B结果"].append(结果)
        else:
            return {"错误": f"未知策略: {策略}"}

        return {"状态": "记录成功"}

    def 分析(self, 测试ID: str) -> Dict:
        """分析测试结果"""
        if 测试ID not in self.测试结果:
            return {"错误": "测试不存在"}

        测试 = self.测试结果[测试ID]
        A结果 = 测试["A结果"]
        B结果 = 测试["B结果"]

        A_成功率 = sum(1 for r in A结果 if r.get("成功", False)) / max(1, len(A结果))
        B_成功率 = sum(1 for r in B结果 if r.get("成功", False)) / max(1, len(B结果))

        胜出者 = "A" if A_成功率 > B_成功率 else "B" if B_成功率 > A_成功率 else "平局"

        测试["状态"] = "已完成"
        测试["结束时间"] = datetime.datetime.now().isoformat()
        测试["分析"] = {
            "A成功率": A_成功率,
            "B成功率": B_成功率,
            "胜出者": 胜出者,
            "样本数": {"A": len(A结果), "B": len(B结果)},
            "推荐": f"建议采用{胜出者}策略" if 胜出者 != "平局" else "无显著差异，建议继续测试"
        }

        return 测试


# ============================================================
# 十、命令行入口
# ============================================================

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="🐉 强化学习反馈循环引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 单次学习循环
  python3 lh_rl_feedback_loop.py --template T001 --user '{"满意度":0.9}' --response '{"耗时":50}' --result '{"完成":true}'

  # 批量学习
  python3 lh_rl_feedback_loop.py --batch data.json

  # 生成学习报告
  python3 lh_rl_feedback_loop.py --report

  # 同步全局
  python3 lh_rl_feedback_loop.py --sync

  # A/B测试
  python3 lh_rl_feedback_loop.py --ab-test --id TEST001
        """
    )

    parser.add_argument("--template", type=str, help="模板ID")
    parser.add_argument("--user", type=str, help="用户行为 (JSON)")
    parser.add_argument("--response", type=str, help="系统响应 (JSON)")
    parser.add_argument("--result", type=str, help="结果反馈 (JSON)")
    parser.add_argument("--batch", type=str, help="批量数据文件路径")
    parser.add_argument("--report", action="store_true", help="生成学习报告")
    parser.add_argument("--sync", action="store_true", help="同步全局")
    parser.add_argument("--ab-test", action="store_true", help="运行A/B测试")
    parser.add_argument("--id", type=str, help="测试ID")

    args = parser.parse_args()

    # 通用序列化辅助函数（dataclass → dict）
    def _可序列化(obj):
        if hasattr(obj, '__dataclass_fields__'):
            return asdict(obj)
        if isinstance(obj, dict):
            return {k: _可序列化(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_可序列化(i) for i in obj]
        return obj

    引擎 = 强化学习反馈循环()

    if args.batch:
        with open(args.batch, 'r', encoding='utf-8') as f:
            数据 = json.load(f)
        if isinstance(数据, list):
            结果 = 引擎.批量运行(数据)
            print(json.dumps(_可序列化(结果), ensure_ascii=False, indent=2))
        else:
            print("❌ 批量数据格式错误，应为列表")
        return

    if args.report:
        报告 = 引擎.生成学习报告()
        print("\n" + "=" * 70)
        print("📊 学习报告")
        print("=" * 70)
        print(f"🧬 DNA: {报告.dna}")
        print(f"📋 总行为数: {报告.总行为数}")
        print(f"📈 优质模式: {报告.优质模式}")
        print(f"📉 低效模式: {报告.低效模式}")
        print(f"\n💡 学习建议:")
        for 建议 in 报告.学习建议:
            print(f"  - {建议}")
        print("=" * 70)
        return

    if args.sync:
        结果 = 引擎.同步全局()
        print("🔄 全局同步完成")
        print(json.dumps(_可序列化(结果), ensure_ascii=False, indent=2))
        return

    if args.ab_test:
        测试框架 = AB测试框架()
        if args.id:
            测试 = 测试框架.分析(args.id)
            print(json.dumps(测试, ensure_ascii=False, indent=2))
        else:
            测试 = 测试框架.创建测试(
                "TEST001",
                {"策略": "保守型", "学习率": 0.05},
                {"策略": "激进型", "学习率": 0.15}
            )
            print("📊 A/B测试已创建")
            print(json.dumps(测试, ensure_ascii=False, indent=2))
        return

    if args.template and args.user and args.response and args.result:
        用户行为 = json.loads(args.user)
        系统响应 = json.loads(args.response)
        结果反馈 = json.loads(args.result)

        结果 = 引擎.运行一次(args.template, 用户行为, 系统响应, 结果反馈)
        print(json.dumps(_可序列化(结果), ensure_ascii=False, indent=2))
        return

    parser.print_help()


if __name__ == "__main__":
    main()
