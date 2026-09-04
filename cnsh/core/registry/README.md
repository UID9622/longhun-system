# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂路由注册表 (IPA Route Registry)

**DNA**:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-ROUTE-REGISTRY-README-FILE1-v1.0
**状态**: 🟢 MAIN·可公开
**责任**: UID9622·不免责

---

## 概述

龍魂路由注册表是一个中央服务发现和节点管理系统，提供：
- **O(1) 快速查找** - 基于内存字典，毫秒级响应
- **三色状态管理** - 🟢活跃 / 🟡待归档 / 🔴废弃
- **DNA追溯** - 每个节点绑定不可伪造的追溯码
- **Append-Only持久化** - JSONL格式，仅追加不覆盖
- **自动P0预注册** - 系统启动时自动注册7个核心模块

---

## 快速开始

### 安装和导入

```python
from cnsh_core.registry import (
    get_route_registry,
    find_route,
    register_route,
    list_routes,
    RouteNode,
    NodeStatus,
    NodeType
)
```

### 查找节点

```python
# 快速O(1)查找
node = find_route("IPA-L0-001")
if node:
    print(f"找到: {node.name} - {node.status}")
```

### 注册新节点

```python
from cnsh_core.registry import RouteNode, NodeStatus, NodeType

# 创建节点
node = RouteNode(
    node_id="IPA-L2-001",
    name="my_service",
    node_type=NodeType.LOCAL,
    status=NodeStatus.ACTIVE,
    local_path="my_module.service",
    entry_point="get_service",
    dna="#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-MY-SERVICE-v1.0",
    layer="L2_DECENNIAL",
    description="我的服务描述",
    tags=["service", "custom"],
    dependencies=["IPA-L0-001"],  # 依赖系统配置
)

# 注册
success, msg = register_route(node)
if success:
    print(f"✅ {msg}")
else:
    print(f"❌ {msg}")
```

### 列出和过滤节点

```python
# 列出所有活跃节点
active_nodes = list_routes(status=NodeStatus.ACTIVE)

# 列出 L0_ETERNAL 层的节点
l0_nodes = list_routes(layer="L0_ETERNAL")

# 列出某种类型的节点
local_nodes = list_routes(node_type=NodeType.LOCAL)
```

### 更新节点状态

```python
registry = get_route_registry()

# 将节点标记为待归档
success, msg = registry.update_status("IPA-L2-001", NodeStatus.ARCHIVED)
print(msg)  # "状态更新成功: 🟢 → 🟡"
```

---

## 架构设计

### 节点ID命名规范

```
[PREFIX]-[LAYER]-[NUMBER]
  ↓         ↓        ↓
类型     层级      编号

例: IPA-L0-001
    ↑   ↑  ↑
    │   │  └─ 001-999: 节点编号
    │   └─── L0,L1,L2,L3,L4: 时间层级
    └─────── IPA,CENTER,PERSONA,DB,GATE,LOCAL,TOOL,WIDGET: 节点类型
```

### 节点类型 (NodeType)

| 前缀 | 说明 | 例子 |
|------|------|------|
| IPA | 宣言锚点 (Notion) | IPA-L0-001 |
| CENTER | 五大中心 | CENTER-L1-001 |
| PERSONA | 人格路由 (P00-P72) | PERSONA-L2-001 |
| DB | Notion数据库 | DB-L1-001 |
| GATE | 规则守门人 | GATE-L1-001 |
| LOCAL | 本地模块/引擎 | LOCAL-L0-001 |
| TOOL | Chrome工具箱 | TOOL-L2-001 |
| WIDGET | 前端组件 | WIDGET-L3-001 |

### 时间层级 (Layers)

| 层级 | 周期 | 同步频率 | 用途 |
|------|------|---------|------|
| L0_ETERNAL | 永恒 | 无需 | 系统宪法、核心规则 |
| L1_SEASONAL | 季度 | 每月 | 常规服务、策略 |
| L2_DECENNIAL | 十年 | 每年 | 长期规划、架构 |
| L3_GENERATIONAL | 代际 | 每3-5年 | 文化传承、远景 |
| L4_INSTANT | 即时 | 持续 | 快速响应、应急 |

### 三色状态系统

```
🟢 ACTIVE (活跃)
  ├─ 正常使用
  ├─ 完全可信
  └─ 置信度 >= 85%

🟡 ARCHIVED (待归档)
  ├─ 可用但计划废弃
  ├─ 部分可信
  └─ 置信度 60-85%

🔴 DEPRECATED (已废弃)
  ├─ 不可使用
  ├─ 禁止调用
  └─ 置信度 < 60%
```

---

## API 参考

### 全局函数

```python
def find_route(node_id: str) -> Optional[RouteNode]
    """快速查找路由（O(1)）"""

def register_route(node: RouteNode) -> Tuple[bool, str]
    """注册新路由"""

def list_routes(node_type=None, status=None, layer=None) -> List[RouteNode]
    """列出路由（支持过滤）"""

def check_route_health(node_id: str) -> dict
    """检查路由健康度"""

def get_route_statistics() -> dict
    """获取路由统计信息"""

def selftest_registry() -> Tuple[bool, List[str]]
    """自检路由注册表"""
```

### RouteRegistry 类

```python
class RouteRegistry:
    def register(self, node: RouteNode) -> Tuple[bool, str]
    def find(self, node_id: str) -> Optional[RouteNode]
    def update_status(self, node_id: str, new_status: NodeStatus) -> Tuple[bool, str]
    def list_nodes(self, node_type=None, status=None, layer=None) -> List[RouteNode]
    def check_health(self, node_id: str) -> dict
    def get_statistics(self) -> dict
    def selftest(self) -> Tuple[bool, List[str]]
```

### RouteNode 数据类

```python
@dataclass
class RouteNode:
    # 基础信息
    node_id: str                    # 节点ID
    name: str                       # 节点名称
    node_type: NodeType             # 节点类型
    status: NodeStatus              # 节点状态

    # 位置信息
    local_path: Optional[str]       # Python模块路径
    notion_url: Optional[str]       # Notion链接
    entry_point: Optional[str]      # 入口函数名

    # 追溯信息
    dna: str                        # DNA追溯码
    layer: str                      # L0-L4层级

    # 描述和标签
    description: str                # 节点描述
    tags: List[str]                 # 标签
    dependencies: List[str]         # 依赖节点

    # 时间戳
    created_at: str                 # 创建时间
    updated_at: str                 # 更新时间

    # 扩展
    metadata: Dict[str, Any]        # 其他元数据
```

---

## 数据持久化

### 文件位置

```
~/longhun-system/01_protocols/IPA-ROUTE-REGISTRY.local.md
```

### 格式说明

```
# JSONL 格式 (JSON Lines)
# 每行一个完整的 RouteNode JSON 对象
# 仅追加，不覆盖
# 支持快速恢复和数据审计
```

### 单行示例

```json
{
  "node_id": "IPA-L0-001",
  "name": "constitution",
  "node_type": "LOCAL",
  "status": "🟢",
  "local_path": "cnsh_core.constitution",
  "notion_url": null,
  "entry_point": "get_system_config",
  "dna": "#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-CONSTITUTION-v1.0",
  "layer": "L0_ETERNAL",
  "description": "系统宪法和基础配置",
  "tags": ["L0", "config"],
  "dependencies": [],
  "created_at": "2026-06-03T15:00:00.000000",
  "updated_at": "2026-06-03T15:00:00.000000",
  "metadata": {}
}
```

---

## 与启动器的集成

系统启动时，自动执行以下步骤：

```
[1/7] 加载配置
[2/7] 验证身份
[3/7] 初始化权限
[4/7] 初始化DNA
[5/7] 初始化日志
[6/7] 初始化调度器
[7/7] 初始化路由注册表
      └─ 自动预注册7个P0模块
```

### 预注册的P0模块

| ID | 名称 | 描述 | 层级 |
|----|------|------|------|
| IPA-L0-001 | constitution | 系统宪法配置 | L0 |
| IPA-L0-002 | identity | 三重身份验证 | L0 |
| IPA-L0-003 | permissions | RBAC权限控制 | L0 |
| IPA-L0-004 | dna | DNA追溯码系统 | L0 |
| IPA-L0-005 | logging | Append-Only日志 | L0 |
| IPA-L0-006 | mathematics | 数学公式算法 | L0 |
| IPA-L1-001 | scheduler | 执行调度器 | L1 |

---

## 日志集成

所有路由操作都被记录到系统日志：

```python
# 事件类型
LogEventType.CONFIG_CHANGED    # 节点注册/更新
LogEventType.SYSTEM_ERROR      # 文件操作失败

# 日志位置
~/longhun-system/logs/system_log.jsonl
```

### 日志示例

```json
{
  "timestamp": "2026-06-03T15:00:01.000000",
  "event_type": "CONFIG_CHANGED",
  "message": "注册新节点: IPA-L1-001",
  "context": {
    "node_id": "IPA-L1-001",
    "node_type": "LOCAL",
    "status": "🟢",
    "layer": "L1_SEASONAL"
  }
}
```

---

## 健康检查

```python
health = check_route_health("IPA-L0-001")

print(health)
# {
#     "node_id": "IPA-L0-001",
#     "status": "NodeStatus.ACTIVE",
#     "color": "🟢",
#     "reachable": True,          # 模块可导入
#     "last_checked": "2026-06-03T15:00:00.000000",
#     "issues": []                # 无问题
# }
```

### 检查项目

1. **模块可达性** - local_path 模块是否可导入
2. **DNA格式** - DNA码是否符合 #龍芯⚡️ 格式
3. **节点存在** - 所有依赖节点是否存在
4. **状态有效** - 节点状态是否在允许的三色之内

---

## 自检

```python
from cnsh_core.registry import selftest_registry

all_pass, errors = selftest_registry()

if all_pass:
    print("✅ 自检通过")
else:
    print("❌ 自检失败:")
    for error in errors:
        print(f"  - {error}")
```

### 检查项目

1. 注册表文件可读写
2. 所有节点的local_path可达
3. DNA格式正确
4. 节点ID规范

---

## 使用案例

### 案例1: 服务发现

```python
# P1-2 规则引擎需要调用某个模块
node = find_route("IPA-L0-001")
if node and node.is_active():
    # 动态加载模块
    module = importlib.import_module(node.local_path)
    func = getattr(module, node.entry_point)
    result = func()
```

### 案例2: 依赖验证

```python
# 注册新服务前，验证所有依赖都存在
dependencies = ["IPA-L0-001", "IPA-L0-004"]
for dep_id in dependencies:
    if not find_route(dep_id):
        raise RuntimeError(f"缺少依赖: {dep_id}")
```

### 案例3: 状态变迁

```python
# L2十年周期，进行平台升级
registry = get_route_registry()

# 标记旧节点为待归档
registry.update_status("IPA-L2-001", NodeStatus.ARCHIVED)

# 注册新版本
new_node = RouteNode(...)
register_route(new_node)
```

---

## 未来扩展

### P2 阶段: Notion 同步
- 双向同步：本地注册表 ↔ Notion数据库
- 定时同步任务（利用scheduler）
- 冲突解决策略

### P3 阶段: 可视化
- 关系图展示（节点 + 依赖关系）
- 健康度仪表板
- 层级树视图

### P4 阶段: 高级功能
- 服务网格集成
- 自动发现和注册
- 灰度发布支持
- 版本管理

---

## 故障排查

### 问题: 节点找不到

```python
node = find_route("IPA-UNKNOWN-001")
# None

# 解决: 列出所有节点
all_nodes = list_routes()
for node in all_nodes:
    print(node.node_id)
```

### 问题: 注册失败 - 依赖不存在

```python
# 错误: "依赖节点不存在: IPA-L0-001"

# 解决: 确保先注册依赖
register_route(dependency_node)
register_route(your_node)  # 现在可以成功
```

### 问题: 健康检查失败

```python
health = check_route_health("IPA-L1-001")
# {"issues": ["本地路径不可达: cnsh_core.scheduler"]}

# 解决: 检查 local_path 是否正确
# 或确保对应的Python包已安装
```

---

## 性能特性

| 操作 | 时间复杂度 | 实际性能 |
|------|-----------|---------|
| find | O(1) | < 1ms |
| register | O(1)* | ~10ms |
| list (无过滤) | O(n) | ~50ms (1000节点) |
| list (有过滤) | O(n) | ~50ms |
| update_status | O(n)* | ~100ms |
| selftest | O(n) | ~200ms |

*: 包含文件I/O

---

## 开发者指南

### 添加新功能

1. 在 `RouteNode` 中添加字段（如需要）
2. 在 `RouteRegistry` 中实现操作方法
3. 在 `__init__.py` 中导出便捷函数
4. 添加单元测试
5. 更新本README

### 测试

```bash
cd /Users/zuimeidedeyihan/longhun-system/cnsh-core

# 运行自检
python3 -c "from registry import selftest_registry; print(selftest_registry())"

# 运行启动器（包含注册表测试）
python3 core_system_launcher.py
```

---

## 许可和责任

**DNA**:#龍芯⚡️丙午·癸巳·戊申·戊午·䷙大畜-ROUTE-REGISTRY-README-v1.0
**作者**: UID9622 · 诸葛鑫 · 龍芯北辰
**状态**: 🟢 MAIN·可公开
**责任**: UID9622·不免责
