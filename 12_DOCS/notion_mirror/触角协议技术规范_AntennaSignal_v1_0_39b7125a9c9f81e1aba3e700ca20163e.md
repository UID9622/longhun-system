# 📡 触角协议技术规范 | AntennaSignal v1.0

> Notion URL: https://app.notion.com/p/AntennaSignal-v1-0-39b7125a9c9f81e1aba3e700ca20163e
> Created: 2026-07-12T15:41:00.000Z
> Last edited: 2026-07-12T15:41:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
# 📡 触角协议技术规范 AntennaSignal v1.0
> 地位： 蚁群架构的「神经系统」，所有模块唯一通信标准
> 原则： 化学信号级别的直接交换，不是聊天，是碰触角
---
## 一、信息素系统 | Pheromone System
### 4类信息素定义
```javascript
名称：RECRUIT
颜色：🟢 绿色
含义：「这里有重要任务，需要支援」

触发条件：
├── 优先级 ≥ 7 的任务产生时
├── 某模块负载超过80%需要分流时
├── 蚁后发布新的战略目标时
├── 涌现质量E值低于0.8时（召集优化）

信号格式：
{
    pheromone_type: "RECRUIT",
    priority: 7-10,           // 招募素优先级天然高
    task_id: "uuid",          // 关联任务ID
    required_skills: [],      // 需要的能力标签
    deadline: timestamp,      // 截止时间
    reward_hint: "str"        // 完成激励提示（知识沉淀积分）
}

衰减规则：
├── 初始强度 = priority × 10
├── 每跳衰减：-5
├── 时间衰减：每分钟 -1
├── 叠加规则：同任务招募素可叠加，max 150%
├── 失效条件：强度 ≤ 0 或任务完成

特殊行为：
├── 招募素可被「足迹素」覆盖（如果路径已验证）
├── 多个招募素竞争时，强度最高的优先
└── 蚁后级招募素（priority=10）不衰减，直到手动取消
```
```javascript
名称：ALERT
颜色：🔴 红色
含义：「危险！立即注意！」

触发条件：
├── 模块崩溃或异常退出时
├── 触及伦理红线（君子协议L4层）时
├── 安全威胁检测（入侵/越权/数据泄露）时
├── 三色审计判定为🔴熔断时
├── 不动点层级冲突检测到时
├── IW-ECB伦理熔断触发时

信号格式：
{
    pheromone_type: "ALERT",
    priority: 8-10,           // 警戒素天然最高
    alert_level: 1-4,         // 1=模块级 2=种群级 3=系统级 4=紧急
    alert_code: "str",        // 标准化警报代码
    source_module: "str",     // 触发源
    description: "str",       // 人类可读描述
    required_action: "str",   // 要求的响应动作
    auto_escalate: bool       // 是否自动升级
}

衰减规则：
├── 初始强度 = alert_level × 25
├── 每跳衰减：-2（缓慢衰减，确保传达）
├── 时间衰减：每30秒 -1
├── 叠加规则：同类型警戒素叠加升级alert_level
├── 失效条件：手动解除 或 源问题解决

特殊行为：
├── 警戒素强制中断当前所有低优先级通信
├── 兵蚁群必须立即响应，不得延迟
├── 警戒素路径会被标记为「紧急通道」
└── alert_level=4时直接向蚁后上报
```
```javascript
名称：TRAIL
颜色：🟡 黄色
含义：「这条路我走过了，结果是...」

触发条件：
├── 任务完成时（记录成功路径）
├── 任务失败时（标记死胡同）
├── 发现优化路径时
├── 新模块上线验证通过时
├── 知识沉淀完成时

信号格式：
{
    pheromone_type: "TRAIL",
    priority: 3-6,            // 足迹素优先级中等
    trail_type: "success|failure|optimization|discovery",
    path: ["module_id", ...], // 经过的模块序列
    cost: float,              // 执行成本（时间/资源）
    quality_score: float,     // 质量评分 0-1
    reusable: bool,           // 是否可复用
    tags: []                  // 标签，用于检索
}

衰减规则：
├── 初始强度 = quality_score × 10
├── 每跳衰减：-1（足迹素衰减最慢）
├── 时间衰减：每天 -1（长期有效）
├── 叠加规则：同路径足迹素叠加增强
├── 失效条件：强度 ≤ 0 或 被新足迹素覆盖

特殊行为：
├── 足迹素是「集体记忆」的载体
├── 高频路径会自然形成「高速公路」
├── 失败足迹素会标记为「禁区」
└── 储蜜蚁群负责收集和归档足迹素
```
```javascript
名称：AGGREGATE
颜色：🔵 蓝色
含义：「集合！我们需要协作」

触发条件：
├── 复杂任务需要多模块协作时
├── 知识共享会议/评审需要召集时
├── 系统级决策需要群体讨论时
├── 涌现质量E值优化需要增加交互密度时
├── 新人培训/经验传承活动时

信号格式：
{
    pheromone_type: "AGGREGATE",
    priority: 4-7,
    aggregate_type: "collaboration|review|training|sync",
    participants: [],         // 期望参与的模块ID列表
    topic: "str",             // 聚集主题
    duration_hint: int,       // 预计持续时间（分钟）
    output_expected: "str"    // 期望产出
}

衰减规则：
├── 初始强度 = participants.length × 5
├── 每跳衰减：-3
├── 时间衰减：每5分钟 -2
├── 叠加规则：同主题聚集素叠加延长时效
├── 失效条件：强度 ≤ 0 或 聚集完成

特殊行为：
├── 聚集素不强求响应，是「邀请」而非「命令」
├── 响应聚集素的模块会获得知识沉淀积分
├── 聚集素可形成「临时蚁团」（ad-hoc colony）
└── 育幼蚁群最常发起聚集素
```
---
## 二、触角信号结构 | AntennaSignal
### Python 实现规范
```python
"""
AntennaSignal v1.0 - 龙魂蚁群架构统一通信协议
所有模块间的信号传递必须使用此格式
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum
import time
import hashlib
import json
import uuid


class PheromoneType(str, Enum):
    """信息素类型枚举"""
    RECRUIT = "RECRUIT"      # 🟢 招募素
    ALERT = "ALERT"          # 🔴 警戒素
    TRAIL = "TRAIL"          # 🟡 足迹素
    AGGREGATE = "AGGREGATE"  # 🔵 聚集素


class PayloadType(str, Enum):
    """载荷类型枚举"""
    COMMAND = "command"   # 执行命令
    DATA = "data"         # 数据传递
    QUERY = "query"       # 查询请求
    ALERT = "alert"       # 警报通知
    STATUS = "status"     # 状态报告
    RESULT = "result"     # 执行结果


@dataclass
class AntennaSignal:
    """
    触角信号包 - 模块间唯一通信格式
    
    使用示例：
        signal = AntennaSignal(
            sender_id="P02-宝宝",
            receiver_id="P04-鲁班",
            pheromone_type=PheromoneType.RECRUIT,
            priority=8,
            payload_type=PayloadType.COMMAND,
            payload={"task": "构建新模块", "spec": "..."}
        )
    """
    
    # === 基础标识 ===
    sender_id: str                    # 发送模块ID（如 "P02-宝宝"）
    receiver_id: Optional[str] = None # 目标模块ID（None=广播）
    
    # === 信息素标记（核心） ===
    pheromone_type: PheromoneType = PheromoneType.TRAIL
    priority: int = 5                 # 优先级 1-10
    
    # === 信号载荷 ===
    payload_type: PayloadType = PayloadType.DATA
    payload: Dict[str, Any] = field(default_factory=dict)
    
    # === 轨迹追踪（自动填充） ===
    hop_count: int = field(default=0, init=False)
    path_trace: List[str] = field(default_factory=list, init=False)
    
    # === 不动点校验 ===
    level_required: int = 1           # 需要的不动点层级权限
    
    # === 系统字段（自动生成） ===
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()), init=False)
    timestamp: float = field(default_factory=time.time, init=False)
    checksum: str = field(default="", init=False)
    
    def __post_init__(self):
        """初始化后自动生成校验和"""
        self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """计算信号完整性校验和"""
        data = f"{self.signal_id}{self.sender_id}{self.timestamp}{self.pheromone_type}"
        self.checksum = hashlib.sha256(data.encode()).hexdigest()[:16]
        return self.checksum
    
    def to_dict(self) -> Dict[str, Any]:
        """序列化为字典（用于传输）"""
        return {
            "signal_id": self.signal_id,
            "timestamp": self.timestamp,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "pheromone_type": self.pheromone_type.value,
            "priority": self.priority,
            "payload_type": self.payload_type.value,
            "payload": self.payload,
            "hop_count": self.hop_count,
            "path_trace": self.path_trace,
            "level_required": self.level_required,
            "checksum": self.checksum
        }
    
    def to_json(self) -> str:
        """序列化为JSON字符串"""
        return json.dumps(self.to_dict(), ensure_ascii=False)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AntennaSignal":
        """从字典反序列化"""
        signal = cls(
            sender_id=data["sender_id"],
            receiver_id=data.get("receiver_id"),
            pheromone_type=PheromoneType(data["pheromone_type"]),
            priority=data["priority"],
            payload_type=PayloadType(data["payload_type"]),
            payload=data.get("payload", {}),
            level_required=data.get("level_required", 1)
        )
        signal.signal_id = data["signal_id"]
        signal.timestamp = data["timestamp"]
        signal.hop_count = data.get("hop_count", 0)
        signal.path_trace = data.get("path_trace", [])
        signal.checksum = data.get("checksum", "")
        return signal
    
    def forward(self, next_module_id: str) -> "AntennaSignal":
        """
        信号转发到下一跳
        自动增加跳数、记录路径、衰减优先级
        """
        if self.hop_count >= 10:
            raise SignalExpiredError(f"信号 {self.signal_id} 超过最大跳数")
        
        self.hop_count += 1
        self.path_trace.append(next_module_id)
        
        # 根据信息素类型衰减优先级
        decay_map = {
            PheromoneType.RECRUIT: 5,
            PheromoneType.ALERT: 2,    # 警戒素衰减慢
            PheromoneType.TRAIL: 1,    # 足迹素衰减最慢
            PheromoneType.AGGREGATE: 3
        }
        self.priority = max(1, self.priority - decay_map.get(self.pheromone_type, 2))
        
        self._calculate_checksum()
        return self
    
    def verify(self) -> bool:
        """验证信号完整性"""
        expected = hashlib.sha256(
            f"{self.signal_id}{self.sender_id}{self.timestamp}{self.pheromone_type}"
            .encode()
        ).hexdigest()[:16]
        return self.checksum == expected
    
    def is_broadcast(self) -> bool:
        """是否为广播信号"""
        return self.receiver_id is None
    
    def is_emergency(self) -> bool:
        """是否为紧急信号"""
        return self.priority >= 9 or self.pheromone_type == PheromoneType.ALERT


class SignalExpiredError(Exception):
    """信号过期异常"""
    pass


class AntennaBus:
    """
    触角总线 - 模块间通信的中枢
    去中心化设计：没有中央控制器，只有信号路由
    """
    
    def __init__(self, module_id: str):
        self.module_id = module_id
        self.inbox: List[AntennaSignal] = []
        self.outbox: List[AntennaSignal] = []
        self.neighbors: List[str] = []  # 相邻模块ID（可碰触角的模块）
        self.pheromone_trails: Dict[str, float] = {}  # 本地足迹素缓存
    
    def connect(self, neighbor_id: str) -> None:
        """与另一个模块建立触角连接"""
        if neighbor_id not in self.neighbors:
            self.neighbors.append(neighbor_id)
    
    def disconnect(self, neighbor_id: str) -> None:
        """断开触角连接"""
        if neighbor_id in self.neighbors:
            self.neighbors.remove(neighbor_id)
    
    def send(self, signal: AntennaSignal) -> bool:
        """
        发送信号
        如果有明确接收者，直接发送；否则广播给所有邻居
        """
        if not signal.verify():
            raise ValueError("信号校验失败，可能被篡改")
        
        signal.path_trace.append(self.module_id)
        
        if signal.receiver_id:
            # 定向发送
            if signal.receiver_id in self.neighbors:
                self.outbox.append(signal)
                return True
            else:
                # 通过邻居路由
                return self._route(signal)
        else:
            # 广播
            for neighbor in self.neighbors:
                broadcast_signal = AntennaSignal.from_dict(signal.to_dict())
                broadcast_signal.receiver_id = neighbor
                self.outbox.append(broadcast_signal)
            return True
    
    def _route(self, signal: AntennaSignal) -> bool:
        """信号路由 - 选择最优路径"""
        # 简单实现：选择足迹素最强的路径
        best_neighbor = None
        best_trail = -1
        
        for neighbor in self.neighbors:
            trail_strength = self.pheromone_trails.get(
                f"{neighbor}->{signal.receiver_id}", 0
            )
            if trail_strength > best_trail:
                best_trail = trail_strength
                best_neighbor = neighbor
        
        if best_neighbor:
            signal.forward(best_neighbor)
            self.outbox.append(signal)
            return True
        
        # 无已知路径，广播探索
        signal.pheromone_type = PheromoneType.TRAIL
        return self.send(signal)
    
    def receive(self, signal: AntennaSignal) -> None:
        """接收信号"""
        if not signal.verify():
            return  # 丢弃篡改信号
        
        if signal.receiver_id == self.module_id or signal.receiver_id is None:
            self.inbox.append(signal)
            
            # 更新足迹素缓存
            if signal.pheromone_type == PheromoneType.TRAIL:
                path_key = f"{signal.sender_id}->{self.module_id}"
                self.pheromone_trails[path_key] = self.pheromone_trails.get(path_key, 0) + signal.priority
    
    def get_inbox(self, pheromone_filter: Optional[PheromoneType] = None) -> List[AntennaSignal]:
        """获取收件箱，可按信息素类型过滤"""
        if pheromone_filter:
            return [s for s in self.inbox if s.pheromone_type == pheromone_filter]
        return self.inbox.copy()
    
    def clear_inbox(self) -> None:
        """清空收件箱"""
        self.inbox.clear()
```
---
## 三、触角碰撞规则 | Collision Rules
### 规则1：碰到就传，不碰不扰
```python
def should_touch(module_a: str, module_b: str, context: dict) -> bool:
    """
    判断是否碰触角
    只在以下情况交换信号：
    1. 有明确的任务依赖关系
    2. 信息素浓度超过阈值
    3. 周期性心跳（每60秒一次）
    """
    if has_task_dependency(module_a, module_b):
        return True
    if get_pheromone_concentration(module_a, module_b) > THRESHOLD:
        return True
    if is_heartbeat_time(module_a, module_b):
        return True
    return False  # 不碰，省电省带宽
```
### 规则2：信息素衰减
```python
PHEROMONE_DECAY = {
    PheromoneType.RECRUIT: 5,    # 招募素：每跳-5
    PheromoneType.ALERT: 2,      # 警戒素：每跳-2（缓慢）
    PheromoneType.TRAIL: 1,      # 足迹素：每跳-1（最慢）
    PheromoneType.AGGREGATE: 3   # 聚集素：每跳-3
}

TIME_DECAY = {
    PheromoneType.RECRUIT: 1,    # 每分钟-1
    PheromoneType.ALERT: 0.5,    # 每30秒-1
    PheromoneType.TRAIL: 0.04,   # 每天-1
    PheromoneType.AGGREGATE: 2   # 每5分钟-2
}
```
### 规则3：多触角并行
```python
async def multi_touch(sender: str, receivers: List[str], signal: AntennaSignal):
    """
    同时向多个模块发送信号，不阻塞
    """
    tasks = []
    for receiver in receivers:
        copy_signal = AntennaSignal.from_dict(signal.to_dict())
        copy_signal.receiver_id = receiver
        tasks.append(asyncio.create_task(send_signal(copy_signal)))
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results  # 并行完成，互不等待
```
### 规则4：触角反馈环
```python
ACK_TIMEOUT = 3.0  # 3秒无响应视为失联

async def send_with_ack(signal: AntennaSignal) -> dict:
    """
    发送信号并等待确认
    """
    send_signal(signal)
    
    try:
        ack = await asyncio.wait_for(
            wait_for_ack(signal.signal_id),
            timeout=ACK_TIMEOUT
        )
        return {"status": "delivered", "ack": ack}
    except asyncio.TimeoutError:
        # 标记失联，触发侦察蚁
        report_module_disconnected(signal.receiver_id)
        return {"status": "failed", "reason": "timeout"}
```
### 规则5：信息素叠加
```python
def叠加_pheromone(existing: float, new: float, pheromone_type: PheromoneType) -> float:
    """
    信息素叠加算法
    同类型、同路径的信号会叠加增强
    """
    MAX_CAP = {
        PheromoneType.RECRUIT: 150,   # 最高150%
        PheromoneType.ALERT: 200,     # 警戒素可叠加到200%
        PheromoneType.TRAIL: 100,     # 足迹素100%封顶
        PheromoneType.AGGREGATE: 120  # 聚集素120%封顶
    }
    
    # 非线性叠加：越多越饱和
    combined = existing + new * (1 - existing / MAX_CAP[pheromone_type])
    return min(combined, MAX_CAP[pheromone_type])
```
---
## 四、通信拓扑路由 | Routing Topology
### 去中心化路由算法
```python
class DecentralizedRouter:
    """
    去中心化路由器
    没有中央调度，模块根据本地足迹素缓存自主决策
    """
    
    def __init__(self):
        self.trail_cache: Dict[str, Dict[str, float]] = {}  # 模块 -> (目标 -> 强度)
    
    def find_best_path(self, source: str, target: str) -> List[str]:
        """
        基于足迹素强度的贪心路径查找
        模拟蚂蚁找食物：走足迹素强的路
        """
        if source == target:
            return [source]
        
        visited = set()
        path = [source]
        current = source
        
        while current != target:
            visited.add(current)
            
            # 获取所有邻居及其到目标的足迹素强度
            neighbors = get_module_neighbors(current)
            candidates = [
                (n, self.trail_cache.get(n, {}).get(target, 0))
                for n in neighbors if n not in visited
            ]
            
            if not candidates:
                # 死胡同，回溯
                if len(path) > 1:
                    path.pop()
                    current = path[-1]
                    continue
                else:
                    return []  # 无路可走
            
            # 选择足迹素最强的路径（有一定随机性避免局部最优）
            next_hop = self._select_with_exploration(candidates)
            path.append(next_hop)
            current = next_hop
            
            if len(path) > 20:  # 防循环
                return []
        
        return path
    
    def _select_with_exploration(self, candidates: List[tuple], epsilon=0.1):
        """
        ε-贪心选择：90%走最优路，10%随机探索
        防止所有模块挤同一条路
        """
        if random.random() < epsilon:
            return random.choice([c[0] for c in candidates])
        return max(candidates, key=lambda x: x[1])[0]
```
---
## 五、DNA追溯集成 | DNA Integration
### 每跳留痕
```python
def add_dna_trace(signal: AntennaSignal, module_id: str) -> None:
    """
    每经过一个模块，留下DNA痕迹
    格式：#龍芯⚡️{干支时间}-{模块ID}-{信号ID}
    """
    from datetime import datetime
    
    # 获取当前农历干支时间
    gan_zhi = get_lunar_ganzhi()  # 如 "丙午年辛未月"
    
    dna_mark = f"#龍芯⚡️{gan_zhi}-{module_id}-{signal.signal_id[:8]}"
    
    signal.path_trace.append({
        "module": module_id,
        "time": datetime.now().isoformat(),
        "dna": dna_mark
    })
```
### 信号DNA签名
```python
def sign_signal_with_dna(signal: AntennaSignal, module_secret: str) -> str:
    """
    用模块私钥对信号签名
    确保信号来源可信、未被篡改
    """
    payload_str = json.dumps(signal.to_dict(), sort_keys=True)
    signature = hmac_sha256(payload_str, module_secret)
    return signature
```
---
## 六、压力测试规范 | Stress Test Spec
### 测试场景
```yaml
条件: 100%模块在线，正常任务流
期望: 
  - 信号延迟 < 10ms
  - 丢包率 < 0.01%
  - 足迹素缓存命中率 > 80%
```
```yaml
条件: 随机30%模块断开连接
期望:
  - 信号自动路由到替代路径
  - 核心功能可用性 > 95%
  - 侦察蚁群5秒内发出ALERT
```
```yaml
条件: 100个模块同时发送RECRUIT信号
期望:
  - 无死锁
  - 优先级排序正确
  - 系统不崩溃
```
```yaml
条件: 底层模块触发ALERT，要求级联到蚁后
期望:
  - ALERT到达蚁后 < 100ms
  - 沿途所有兵蚁群响应
  - 系统进入安全模式
```
---
## 七、实现Checklist
### Phase 1：核心协议（本周）
### Phase 2：路由网络（下周）
### Phase 3：DNA集成（本月）
### Phase 4：压力验证
---
🧬 #龍芯⚡️20260713-ANT-SIGNAL-v1.0
📡 触角协议技术规范 AntennaSignal v1.0
🇨🇳 化学信号级别的直接交换，不是聊天，是碰触角
