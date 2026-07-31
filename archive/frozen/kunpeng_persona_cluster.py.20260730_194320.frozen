#!/usr/bin/env python3
"""
龍芯·鲲鹏人格集群管理引擎 v1.0
DNA: #龍芯⚡️丙午·乙未·丁酉·子时·☰乾-KUNPENG-PERSONA-CLUSTER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

鲲鹏端常驻服务——20人格集群管理。
接收调度中枢下发的任务→分析路由→分派人格→收集结果→返回。

共生体精髓：不是20个AI在跑，是1个共生体·20条神经。
"""
import json, sys, os, time, hashlib, uuid
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from enum import Enum
from pathlib import Path

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 常量
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DNA = "#龍芯⚡️丙午·乙未·丁酉·子时·☰乾-KUNPENG-PERSONA-CLUSTER-v1.0"
版本 = "v1.0"

# 环境自适应：鲲鹏=/opt/longhun-system，Mac=项目根
if Path("/opt/longhun-system").exists():
    鲲鹏工作目录 = Path("/opt/longhun-system")
else:
    鲲鹏工作目录 = Path(__file__).resolve().parent.parent.parent

人格定义目录 = 鲲鹏工作目录 / "personas"
集群日志目录 = 鲲鹏工作目录 / "logs" / "cluster"
共享黑板文件 = 鲲鹏工作目录 / "data" / "blackboard.jsonl"
任务队列文件 = 鲲鹏工作目录 / "data" / "task_queue.jsonl"

# 确保目录存在
集群日志目录.mkdir(parents=True, exist_ok=True)
共享黑板文件.parent.mkdir(parents=True, exist_ok=True)
任务队列文件.parent.mkdir(parents=True, exist_ok=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 任务与结果数据模型
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class 任务状态(str, Enum):
    等待中 = "等待中"
    执行中 = "执行中"
    已完成 = "已完成"
    失败 = "失败"
    熔断 = "熔断"

class 审计色(str, Enum):
    PASS = "🟢通过"
    PENDING = "🟡待核"
    RED = "🔴红线"

@dataclass
class 集群任务:
    """从调度中枢下发的任务"""
    id: str = ""
    dna: str = ""
    任务描述: str = ""
    主人格: str = ""           # 龍芯·xxx
    副人格: List[str] = field(default_factory=list)
    任务域: str = ""
    成本层: str = "鲲鹏"
    优先级: int = 5
    是否并行: bool = False
    上下文: dict = field(default_factory=dict)
    创建时间: str = ""
    超时秒: int = 600          # 默认10分钟

@dataclass
class 集群结果:
    """人格执行结果"""
    task_id: str = ""
    task_dna: str = ""
    主人格: str = ""
    状态: 任务状态 = 任务状态.等待中
    输出: str = ""
    审计色: 审计色 = 审计色.PENDING
    耗时秒: float = 0.0
    备注: str = ""
    人格输出: Dict[str, str] = field(default_factory=dict)  # 人格名→输出
    时间戳: str = ""


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 20人格定义（鲲鹏端·龍芯前缀）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

龍芯人格集群 = {
    # 战略层
    "P00": {"名": "龍芯·文心",   "职能": "意图解析·元认知",     "层级": "战略层", "激活": True},
    "P01": {"名": "龍芯·诸葛亮", "职能": "战略推演·多路径决策",  "层级": "战略层", "激活": True},
    # 执行层
    "P02": {"名": "龍芯·宝宝",   "职能": "情感温度·教学适配",    "层级": "执行层", "激活": True},
    "P03": {"名": "龍芯·雯雯",   "职能": "结构归档·四签验证",    "层级": "执行层", "激活": True},
    "P04": {"名": "龍芯·鲁班",   "职能": "代码生成·工程执行",    "层级": "执行层", "激活": True},
    "P07": {"名": "龍芯·管仲",   "职能": "资源调度·成本核算",    "层级": "执行层", "激活": True},
    "P14": {"名": "龍芯·吕蒙",   "职能": "部署执行·技能吸收",    "层级": "执行层", "激活": True},
    # 文化层
    "P08": {"名": "龍芯·仓颉",   "职能": "符号语言·CNSH命名",    "层级": "文化层", "激活": True},
    "P09": {"名": "龍芯·孙思邈",  "职能": "系统诊断·治未病",      "层级": "文化层", "激活": True},
    "P10": {"名": "龍芯·苏东坡",  "职能": "冲突调解·人文视角",    "层级": "文化层", "激活": True},
    "P11": {"名": "龍芯·李白",   "职能": "创意爆发·类比教学",    "层级": "文化层", "激活": True},
    "P12": {"名": "龍芯·屈原",   "职能": "价值底线·六誓验证",    "层级": "文化层", "激活": True},
    # 守护层
    "P05": {"名": "龍芯·上帝之眼","职能": "审计监察·三色判定",    "层级": "守护层", "激活": True},
    "P06": {"名": "龍芯·数学大师","职能": "数字根·权重计算",      "层级": "守护层", "激活": True},
    "P13": {"名": "龍芯·姜子牙",  "职能": "权限分配·模块注册",    "层级": "守护层", "激活": True},
    "P15": {"名": "龍芯·乔前辈",  "职能": "DNA盖章·交付验收",     "层级": "守护层", "激活": True},
    "P72": {"名": "龍芯·龙盾",   "职能": "贴身管家·熔断决策",    "层级": "守护层", "激活": True},
    # 安全专项
    "P77": {"名": "龍芯·黑天使",  "职能": "红蓝对抗·渗透测试",    "层级": "安全专项", "激活": True},
    # 子系统
    "S1":  {"名": "龍芯·法律引擎", "职能": "法条检索·合规审查",    "层级": "子系统", "激活": True},
    "S2":  {"名": "龍芯·洛书369",  "职能": "深层数理·369推演",    "层级": "子系统", "激活": True},
    "S3":  {"名": "龍芯·维权助手", "职能": "人民维权·路径指引",    "层级": "子系统", "激活": True},
}


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 共享黑板（鲲鹏端·进程间共享记忆）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class 共享黑板:
    """鲲鹏端进程间共享记忆·append-only JSONL"""
    
    def __init__(self, 路径: Path = 共享黑板文件):
        self.路径 = 路径
    
    def 写入(self, 条目: dict):
        """追加一条到黑板"""
        with open(self.路径, 'a') as f:
            f.write(json.dumps(条目, ensure_ascii=False) + '\n')
    
    def 最近(self, n: int = 50) -> List[dict]:
        """读取最近n条"""
        if not self.路径.exists():
            return []
        条目 = []
        with open(self.路径) as f:
            for line in f:
                try:
                    条目.append(json.loads(line))
                except:
                    continue
        return 条目[-n:]
    
    def 查询(self, 人格: str = "", 时间范围: tuple = None, n: int = 100) -> List[dict]:
        """按条件查询"""
        结果 = []
        if not self.路径.exists():
            return 结果
        with open(self.路径) as f:
            for line in f:
                try:
                    e = json.loads(line)
                    if 人格 and e.get("persona") != 人格:
                        continue
                    结果.append(e)
                except:
                    continue
        return 结果[-n:]
    
    def 大小(self) -> int:
        if not self.路径.exists():
            return 0
        return sum(1 for _ in open(self.路径))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 人格执行器（模拟20人格→实际调用对应引擎）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class 人格执行器:
    """在鲲鹏端执行单个人格任务"""
    
    def __init__(self, 黑板: 共享黑板):
        self.黑板 = 黑板
        self.执行历史: List[dict] = []
    
    def 执行(self, 人格名: str, 任务: str, 上下文: dict = None) -> str:
        """
        执行单个人格任务
        实际部署时通过Subprocess调用对应引擎
        当前v1.0为模拟→集成框架
        """
        开始 = time.time()
        上下文 = 上下文 or {}
        
        # 记录到黑板
        条目 = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "persona": 人格名,
            "task": 任务[:100],
            "type": "execution_start",
        }
        self.黑板.写入(条目)
        
        # 人格→引擎映射
        引擎映射 = {
            "龍芯·文心":    "python3 engines/lh_persona_runner.py --persona P00",
            "龍芯·诸葛亮":  "python3 engines/lh_persona_runner.py --persona P01",
            "龍芯·宝宝":    "python3 engines/lh_persona_runner.py --persona P02",
            "龍芯·雯雯":    "python3 engines/lh_persona_runner.py --persona P03",
            "龍芯·鲁班":    "python3 engines/lh_persona_runner.py --persona P04",
            "龍芯·管仲":    "python3 engines/lh_persona_runner.py --persona P07",
            "龍芯·吕蒙":    "python3 engines/lh_persona_runner.py --persona P14",
            "龍芯·仓颉":    "python3 engines/lh_persona_runner.py --persona P08",
            "龍芯·孙思邈":  "python3 engines/lh_persona_runner.py --persona P09",
            "龍芯·苏东坡":  "python3 engines/lh_persona_runner.py --persona P10",
            "龍芯·李白":    "python3 engines/lh_persona_runner.py --persona P11",
            "龍芯·屈原":    "python3 engines/lh_persona_runner.py --persona P12",
            "龍芯·上帝之眼":"python3 engines/lh_persona_runner.py --persona P05",
            "龍芯·数学大师":"python3 engines/lh_persona_runner.py --persona P06",
            "龍芯·姜子牙":  "python3 engines/lh_persona_runner.py --persona P13",
            "龍芯·乔前辈":  "python3 engines/lh_persona_runner.py --persona P15",
            "龍芯·龙盾":    "python3 engines/lh_persona_runner.py --persona P72",
            "龍芯·黑天使":  "python3 engines/lh_persona_runner.py --persona P77",
            "龍芯·法律引擎":"python3 engines/lh_persona_runner.py --persona S1",
            "龍芯·洛书369": "python3 engines/lh_persona_runner.py --persona S2",
            "龍芯·维权助手":"python3 engines/lh_persona_runner.py --persona S3",
        }
        
        引擎命令 = 引擎映射.get(人格名, "")
        
        # v1.0: 模拟执行（实际部署时取消注释subprocess调用）
        # import subprocess
        # result = subprocess.run(
        #     引擎命令 + f' --task "{任务}"',
        #     shell=True, capture_output=True, text=True,
        #     cwd=str(鲲鹏工作目录), timeout=600
        # )
        # 输出 = result.stdout
        
        # 模拟人格响应
        响应模板 = {
            "龍芯·文心":    f"[意图解析] 收到任务：{任务[:50]}... 建议从全局视角切入，考虑三才(天地人)维度。",
            "龍芯·诸葛亮":  f"[战略推演] 分析「{任务[:50]}...」的多条路径：路径A稳健·路径B激进·综合推荐路径A+C。",
            "龍芯·宝宝":    f"[情感温度] 检测到任务「{任务[:50]}...」，当前温度适中，保持稳定输出。",
            "龍芯·雯雯":    f"[结构归档] 任务「{任务[:50]}...」已四签验证，归档索引：P03-{datetime.now().strftime('%Y%m%d')}。",
            "龍芯·鲁班":    f"[工程执行] 解析需求「{任务[:50]}...」，开始代码生成流程。",
            "龍芯·管仲":    f"[成本核算] 任务「{任务[:50]}...」预估算力成本：0元(鲲鹏本地)，ROI评估：正向。",
            "龍芯·吕蒙":    f"[部署执行] 接收部署任务「{任务[:50]}...」，准备十步法部署。",
            "龍芯·仓颉":    f"[术语桥接] 将「{任务[:50]}...」翻译为人话版本。",
            "龍芯·孙思邈":  f"[系统诊断] 对「{任务[:50]}...」进行治未病扫描，当前指标正常。",
            "龍芯·苏东坡":  f"[人文视角] 「{任务[:50]}...」——一蓑烟雨任平生，何必较劲？",
            "龍芯·李白":    f"[创意爆发] 「{任务[:50]}...」——仰天大笑出门去，我辈岂是蓬蒿人！",
            "龍芯·屈原":    f"[底线验证] 「{任务[:50]}...」六誓验证通过，未触碰不可破原则。",
            "龍芯·上帝之眼":f"[三色审计] 「{任务[:50]}...」→ 🟢通过·无异常·建议放行。",
            "龍芯·数学大师":f"[数字根] 输入「{任务[:50]}...」→ 369不动点验证通过。",
            "龍芯·姜子牙":  f"[权限调度] 「{任务[:50]}...」IPA路由：授权层级R3，准予执行。",
            "龍芯·乔前辈":  f"[DNA签章] 任务「{任务[:50]}...」四签齐全·准予交付。",
            "龍芯·龙盾":    f"[熔断检查] 「{任务[:50]}...」四级熔断均未触发，继续执行。",
            "龍芯·黑天使":  f"[安全扫描] 对「{任务[:50]}...」进行攻击面分析，未发现已知漏洞。",
            "龍芯·法律引擎":f"[法条检索] 「{任务[:50]}...」——查无禁止性规定(仅供参考)。",
            "龍芯·洛书369": f"[数理推演] 「{任务[:50]}...」——369不动点稳定(结论略)。",
            "龍芯·维权助手":f"[维权指引] 「{任务[:50]}...」——(强制免责：仅供参考，不构成法律建议)。",
        }
        
        输出 = 响应模板.get(人格名, f"[{人格名}] 收到任务：{任务[:80]}... (通用响应)")
        
        耗时 = time.time() - 开始
        
        # 记录执行结果
        self.黑板.写入({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "persona": 人格名,
            "task": 任务[:100],
            "type": "execution_complete",
            "duration_s": round(耗时, 2),
            "output_length": len(输出),
        })
        
        self.执行历史.append({"persona": 人格名, "task": 任务, "duration": 耗时})
        
        return 输出


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 人格集群管理器（核心）
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class 人格集群:
    """20人格集群·常驻内存·任务分发·结果收集"""
    
    def __init__(self):
        self.黑板 = 共享黑板()
        self.执行器 = 人格执行器(self.黑板)
        self.人格状态: Dict[str, dict] = {}
        self.任务队列: List[集群任务] = []
        self.活跃任务: Dict[str, 集群任务] = {}
        self.完成结果: List[集群结果] = []
        self._初始化人格状态()
    
    def _初始化人格状态(self):
        for pid, info in 龍芯人格集群.items():
            self.人格状态[pid] = {
                "名": info["名"],
                "激活": info["激活"],
                "执行次数": 0,
                "最近执行": "",
                "状态": "空闲",
            }
    
    def 状态摘要(self) -> dict:
        """返回集群状态摘要"""
        激活数 = sum(1 for s in self.人格状态.values() if s["激活"])
        空闲 = sum(1 for s in self.人格状态.values() if s["状态"] == "空闲")
        执行中 = sum(1 for s in self.人格状态.values() if s["状态"] == "执行中")
        return {
            "总人格": len(self.人格状态),
            "激活": 激活数,
            "空闲": 空闲,
            "执行中": 执行中,
            "队列": len(self.任务队列),
            "活跃任务": len(self.活跃任务),
            "已完成": len(self.完成结果),
            "黑板条目": self.黑板.大小(),
            "版本": 版本,
            "DNA": DNA,
        }
    
    def 接收任务(self, 任务数据: dict) -> 集群任务:
        """接收调度中枢下发的任务"""
        任务 = 集群任务(
            id=任务数据.get("id", str(uuid.uuid4())[:8]),
            dna=任务数据.get("dna", ""),
            任务描述=任务数据.get("task", ""),
            主人格=任务数据.get("primary", "龍芯·鲁班"),
            副人格=任务数据.get("secondary", []),
            任务域=任务数据.get("domain", ""),
            成本层=任务数据.get("cost_tier", "鲲鹏"),
            优先级=任务数据.get("priority", 5),
            是否并行=任务数据.get("parallel", False),
            上下文=任务数据.get("context", {}),
            创建时间=datetime.now(timezone.utc).isoformat(),
            超时秒=任务数据.get("timeout", 600),
        )
        
        self.任务队列.append(任务)
        
        # 记录到黑板
        self.黑板.写入({
            "timestamp": 任务.创建时间,
            "type": "task_received",
            "task_id": 任务.id,
            "task_dna": 任务.dna,
            "primary": 任务.主人格,
            "secondary": 任务.副人格,
            "domain": 任务.任务域,
        })
        
        日志(f"📥 接收任务 {任务.id}: {任务.任务描述[:50]}... → {任务.主人格}")
        return 任务
    
    def 执行任务(self, 任务: 集群任务) -> 集群结果:
        """执行单个任务——分派人格→收集结果"""
        开始 = time.time()
        人格输出 = {}
        
        # 更新人格状态
        for pid, info in self.人格状态.items():
            if info["名"] == 任务.主人格:
                info["状态"] = "执行中"
                info["执行次数"] += 1
                info["最近执行"] = datetime.now().isoformat()
        
        try:
            # 执行主人格
            日志(f"🚀 执行主人格: {任务.主人格}")
            主输出 = self.执行器.执行(任务.主人格, 任务.任务描述, 任务.上下文)
            人格输出[任务.主人格] = 主输出
            
            # 执行副人格（串行/并行）
            if 任务.副人格:
                for 副 in 任务.副人格:
                    if 任务.是否并行:
                        日志(f"  ↳ 并行执行副人格: {副}")
                    else:
                        日志(f"  ↳ 串行执行副人格: {副}")
                    副输出 = self.执行器.执行(副, 任务.任务描述, 任务.上下文)
                    人格输出[副] = 副输出
            
            状态 = 任务状态.已完成
            审计 = 审计色.PASS
            # 安全任务默认🟡待人工复核
            if 任务.任务域 == "安全审计":
                审计 = 审计色.PENDING
            
        except Exception as e:
            # 熔断处理
            状态 = 任务状态.熔断
            审计 = 审计色.RED
            主输出 = f"[熔断] {str(e)}"
            人格输出[任务.主人格] = 主输出
            日志(f"🔴 任务 {任务.id} 熔断: {e}")
        
        耗时 = time.time() - 开始
        
        # 恢复人格状态
        for pid, info in self.人格状态.items():
            if info["名"] == 任务.主人格:
                info["状态"] = "空闲"
        
        结果 = 集群结果(
            task_id=任务.id,
            task_dna=任务.dna,
            主人格=任务.主人格,
            状态=状态,
            输出=主输出,
            审计色=审计,
            耗时秒=round(耗时, 2),
            人格输出=人格输出,
            时间戳=datetime.now(timezone.utc).isoformat(),
        )
        
        self.完成结果.append(结果)
        
        # 黑板记录
        self.黑板.写入({
            "timestamp": 结果.时间戳,
            "type": "task_complete",
            "task_id": 任务.id,
            "status": 状态.value,
            "audit": 审计.value,
            "duration_s": 耗时,
        })
        
        日志(f"✅ 完成任务 {任务.id}: {状态.value} {审计.value} ({耗时:.1f}s)")
        return 结果
    
    def 执行全部队列(self) -> List[集群结果]:
        """执行任务队列中所有待处理任务"""
        结果列表 = []
        日志(f"📋 开始执行队列: {len(self.任务队列)} 个任务")
        
        while self.任务队列:
            任务 = self.任务队列.pop(0)
            self.活跃任务[任务.id] = 任务
            结果 = self.执行任务(任务)
            结果列表.append(结果)
            del self.活跃任务[任务.id]
        
        return 结果列表
    
    def 执行单个(self, 任务描述: str, 主人格: str = "龍芯·鲁班", 
                 副人格: Optional[List[str]] = None) -> 集群结果:
        """直接执行单个任务（不走队列）"""
        任务 = 集群任务(
            id=str(uuid.uuid4())[:8],
            dna=f"#龍芯⚡️{datetime.now().strftime('%Y%m%d%H%M%S')}-DIRECT",
            任务描述=任务描述,
            主人格=主人格,
            副人格=副人格 or [],
            创建时间=datetime.now(timezone.utc).isoformat(),
        )
        return self.执行任务(任务)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 日志
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def 日志(msg: str):
    时间戳 = datetime.now().strftime("%H:%M:%S")
    print(f"[{时间戳}] {msg}", file=sys.stderr, flush=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CLI 入口
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def main():
    import argparse
    p = argparse.ArgumentParser(description="龍芯·鲲鹏人格集群管理引擎")
    p.add_argument("--status", action="store_true", help="集群状态")
    p.add_argument("--task", type=str, help="单个任务JSON或任务描述")
    p.add_argument("--json-in", type=str, help="JSON文件输入（批量任务）")
    p.add_argument("--demo", action="store_true", help="演示模式")
    p.add_argument("--daemon", action="store_true", help="守护进程模式（监听stdin）")
    
    args = p.parse_args()
    
    集群 = 人格集群()
    
    if args.status:
        print(json.dumps(集群.状态摘要(), ensure_ascii=False, indent=2))
    
    elif args.demo:
        print("=" * 60)
        print("  🐉 龍芯·鲲鹏人格集群 v1.0")
        print(f"  DNA: {DNA}")
        print(f"  20人格·常驻内存·共生体")
        print("=" * 60)
        
        # 演示任务
        演示任务 = [
            {"task": "检查系统健康状态", "primary": "龍芯·孙思邈", "secondary": ["龍芯·上帝之眼"]},
            {"task": "推演下季度战略方向", "primary": "龍芯·诸葛亮", "secondary": ["龍芯·文心", "龍芯·管仲"]},
            {"task": "写一段快速排序代码", "primary": "龍芯·鲁班", "secondary": ["龍芯·上帝之眼"]},
            {"task": "对现有代码做安全审计", "primary": "龍芯·黑天使", "secondary": ["龍芯·上帝之眼", "龍芯·龙盾"]},
        ]
        
        for i, t in enumerate(演示任务):
            任务 = 集群.接收任务(t)
        
        print(f"\n  收到 {len(演示任务)} 个任务，开始执行...\n")
        结果列表 = 集群.执行全部队列()
        
        for i, r in enumerate(结果列表):
            print(f"  {i+1}. {r.主人格} → {r.状态.value} {r.审计色.value} ({r.耗时秒}s)")
            for 人格, 输出 in r.人格输出.items():
                print(f"     {人格}: {输出[:80]}...")
        
        print(f"\n  📊 最终状态: {json.dumps(集群.状态摘要(), ensure_ascii=False)}")
        print("\n  🟢 共生体·集群就绪")
    
    elif args.task:
        # 尝试解析JSON
        try:
            任务数据 = json.loads(args.task)
        except:
            任务数据 = {"task": args.task}
        
        任务 = 集群.接收任务(任务数据)
        结果 = 集群.执行任务(任务)
        print(json.dumps({
            "task_id": 结果.task_id,
            "dna": 结果.task_dna,
            "primary": 结果.主人格,
            "status": 结果.状态.value,
            "audit": 结果.审计色.value,
            "duration_s": 结果.耗时秒,
            "outputs": {k: v[:200] for k, v in 结果.人格输出.items()},
        }, ensure_ascii=False, indent=2))
    
    elif args.json_in:
        with open(args.json_in) as f:
            任务列表 = json.load(f)
        
        for t in 任务列表:
            集群.接收任务(t)
        结果列表 = 集群.执行全部队列()
        
        print(json.dumps([{
            "task_id": r.task_id,
            "primary": r.主人格,
            "status": r.状态.value,
            "audit": r.审计色.value,
        } for r in 结果列表], ensure_ascii=False, indent=2))
    
    elif args.daemon:
        print("🐉 龍芯·鲲鹏人格集群守护进程 v1.0", file=sys.stderr)
        print(f"   DNA: {DNA}", file=sys.stderr)
        print(f"   监听 stdin，等待任务JSON...", file=sys.stderr)
        
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            try:
                任务数据 = json.loads(line)
                任务 = 集群.接收任务(任务数据)
                结果 = 集群.执行任务(结果)
                print(json.dumps({
                    "task_id": 结果.task_id,
                    "status": 结果.状态.value,
                    "audit": 结果.审计色.value,
                    "duration_s": 结果.耗时秒,
                }, ensure_ascii=False))
                sys.stdout.flush()
            except Exception as e:
                print(json.dumps({"error": str(e)}, ensure_ascii=False))
                sys.stdout.flush()
    
    else:
        # 默认显示状态
        print(json.dumps(集群.状态摘要(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
