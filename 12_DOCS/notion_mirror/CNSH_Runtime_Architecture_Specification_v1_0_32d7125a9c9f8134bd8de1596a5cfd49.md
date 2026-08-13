# ⚙️ CNSH Runtime Architecture Specification v1.0

> Notion URL: https://app.notion.com/p/CNSH-Runtime-Architecture-Specification-v1-0-32d7125a9c9f8134bd8de1596a5cfd49
> Created: 2026-03-24T16:16:00.000Z
> Last edited: 2026-07-01T13:43:00.000Z
> Archived at: 2026-08-12T01:40:45.558086
---
## § 0｜系统识别卡
---
## § 1｜总体系统架构
### 完整执行链
```javascript
输入指令
  ↓
CNSH 语法层（命令解析）
  ↓
命令解析器（结构化 ExecutionContext）
  ↓
扩展接口层（发现 · 验证 · 注册 · 分发）
  ↓
策略引擎（allow / require_confirmation / block）
  ↓
Local Shield Core（5层防御 · 主权保障）
  ↓
算法建模引擎 / AI模型运行时 / 执行沙箱
  ↓
节点网络接口（分布式 · ECDH加密）
  ↓
数据接口层（本地 / 云 / 区块链）
  ↓
审计系统（DNA Trace · SHA-256链式哈希）
  ↓
输出结果
```
### 层级职责矩阵
---
## § 2｜CNSH 语法层
### 命令结构规范
```javascript
@MODULE:ACTION / PARAMS{} / EXT[] / SECURITY[] / TRACE[]
```
### 命令示例
```bash
# 算法执行
@ALGORITHM:EXECUTE / PARAMS{id:"mesh_v2", input:{}} / EXT[geometry] / SECURITY[shield:ENCRYPTED] / TRACE[dna:on]

# AI推理
@AI:INFER / PARAMS{model:"local_llm", prompt:"...", max_tokens:512} / SECURITY[shield:TOP_SECRET] / TRACE[dna:on]

# 节点任务
@NODE:DISPATCH / PARAMS{task_id:"t001", payload:{}} / EXT[compute_node] / SECURITY[shield:ENCRYPTED]
```
### Command 数据类
```python
@dataclass
class Command:
    module: str          # 目标模块
    action: str          # 执行动作
    params: dict         # 参数块
    extensions: list     # 扩展列表
    security: dict       # 安全约束
    trace: dict          # 审计配置
    raw: str             # 原始命令字符串
    timestamp: float     # 解析时间戳
```
---
## § 3｜命令解析器
### 解析流程
```javascript
原始字符串
  → 词法分析（tokenize）
  → 语法校验（validate_syntax）
  → 语义提取（extract_semantics）
  → 构造 Command 对象
  → 构造 ExecutionContext
```
### ExecutionContext 定义
```python
@dataclass
class ExecutionContext:
    command: Command
    session_id: str
    user_id: str
    shield_level: ShieldLevel
    permissions: list[str]
    dna_chain: str       # 当前 DNA 链哈希
    created_at: float
    metadata: dict
```
### ShieldLevel 枚举
```python
class ShieldLevel(Enum):
    PUBLIC     = 1   # 公开，无加密
    ENCRYPTED  = 2   # 标准加密传输
    TOP_SECRET = 3   # 高级别保护
    SOVEREIGN  = 4   # 主权级，∞权重拦截
```
---
## § 4｜扩展接口层
### 目录结构
```javascript
extensions/
├── registry.json          # 扩展注册表
├── {ext_id}/
│   ├── manifest.json      # 扩展清单
│   ├── main.py            # 入口文件
│   ├── signature.gpg      # GPG签名（必须存在）
│   └── assets/
```
### manifest.json 标准
```json
{
  "ext_id": "mesh_sculpt_v2",
  "name": "Mesh Sculpt Engine v2",
  "version": "2.0.0",
  "type": "algorithm",
  "permissions": ["mesh_read", "mesh_write", "compute"],
  "shield_level": "ENCRYPTED",
  "entry": "main.py",
  "dna_enabled": true,
  "author": "UID9622",
  "gpg_fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
}
```
### 扩展加载流程
```javascript
1. 扩展发现（扫描 extensions/ 目录）
2. GPG签名验证（signature.gpg）
3. 权限校验（manifest.permissions vs 用户权限集）
4. 注册到 ExtensionRegistry
5. 实例化扩展对象
6. 分发执行请求
```
### 扩展类型表
### 最小权限模型
---
## § 5｜策略引擎
### 核心原则
策略引擎是纯规则评估器，不执行任何操作，只返回决策结果。
### 决策结果枚举
```python
class PolicyDecision(Enum):
    ALLOW                = "allow"
    REQUIRE_CONFIRMATION = "require_confirmation"
    BLOCK                = "block"
```
### 规则评估逻辑
```python
class PolicyEngine:
    def evaluate(self, ctx: ExecutionContext) -> PolicyDecision:
        # 主权级：∞权重，无条件拦截
        if ctx.shield_level == ShieldLevel.SOVEREIGN:
            return PolicyDecision.BLOCK

        # 权限检查
        required = ctx.command.extensions_permissions()
        if not self._has_permissions(ctx.user_id, required):
            return PolicyDecision.BLOCK

        # 敏感操作需确认
        if self._is_sensitive_action(ctx.command):
            return PolicyDecision.REQUIRE_CONFIRMATION

        # 通过所有检查
        return PolicyDecision.ALLOW

    def _has_permissions(self, user_id, required_perms) -> bool:
        user_perms = self.permission_store.get(user_id, set())
        return required_perms.issubset(user_perms)

    def _is_sensitive_action(self, cmd: Command) -> bool:
        sensitive = {"DELETE", "EXPORT", "BROADCAST", "OVERRIDE"}
        return cmd.action in sensitive
```
---
## § 6｜Local Shield Core
### 5层防御模型
### 5层处理流程
```javascript
输入请求
  → Shield-4 感知层（意图分析 · 风险评估）
  → Shield-3 伦理层（内容安全 · 价值观对齐）
  → Shield-2 策略层（权限规则 · 动作白名单）
  → Shield-1 主权层（数据边界 · 主权验证）
  → 放行执行
  → Shield-5 执行层（沙箱隔离 · 配额限制）
  → DNA Trace（全链记录）
```
### Python 实现骨架
```python
class LocalShieldCore:
    def __init__(self):
        self.sovereignty = SovereigntyLayer()
        self.policy = PolicyLayer()
        self.ethics = EthicsLayer()
        self.perception = PerceptionLayer()
        self.execution = ExecutionLayer()

    def process(self, ctx: ExecutionContext) -> ShieldResult:
        # 感知层：意图识别
        risk = self.perception.analyze(ctx)
        if risk.level == RiskLevel.HIGH:
            return ShieldResult.block("high_risk_intent")

        # 伦理层：内容安全
        ethics_result = self.ethics.check(ctx)
        if not ethics_result.safe:
            return ShieldResult.block(ethics_result.reason)

        # 策略层：权限评估
        policy_result = self.policy.evaluate(ctx)
        if policy_result == PolicyDecision.BLOCK:
            return ShieldResult.block("policy_violation")

        # 主权层：数据边界（∞权重）
        sovereignty_result = self.sovereignty.check(ctx)
        if not sovereignty_result.within_boundary:
            return ShieldResult.block("sovereignty_violation")

        # 全部通过
        return ShieldResult.allow()
```
### DNA 熔断机制
```python
class DNACircuitBreaker:
    """连续失败超过阈值时触发熔断"""
    def __init__(self, threshold=3, cooldown=300):
        self.failure_count = 0
        self.threshold = threshold
        self.cooldown = cooldown  # 秒
        self.tripped_at = None

    def record_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.threshold:
            self.tripped_at = time.time()

    def is_open(self) -> bool:
        if self.tripped_at is None:
            return False
        return (time.time() - self.tripped_at) < self.cooldown

---

## § 7｜算法建模引擎（AME）

### 算法注册表

```
ALGORITHM_REGISTRY = {
}
```javascript

### AME 标准接口

```
class AlgorithmInterface(ABC):
@dataclass
class AlgorithmResult:
```javascript

### Algorithm Sculpt Engine（几何操作子系统）

| 操作 | 方法 | 说明 |
|---|---|---|
| inflate | inflate(mesh, factor) | 膨胀操作 |
| smooth | smooth(mesh, iterations) | 平滑迭代 |
| deform | deform(mesh, field) | 变形场应用 |
| remesh | remesh(mesh, target_faces) | 重拓扑 |
| boolean | boolean(mesh_a, mesh_b, op) | 布尔运算 |

```
class MeshSculptEngine(AlgorithmInterface):
```javascript

---

## § 8｜AI 模型运行时接口

### AIModelInterface 标准

```
class AIModelInterface(ABC):
@dataclass
class AIInferenceResult:
```javascript

### 支持的模型类型

| 模型类型 | 说明 | 运行位置 |
|---|---|---|
| local_llm | 本地大语言模型 | 设备本地（默认）|
| local_vision | 本地视觉模型 | 设备本地 |
| remote_llm | 远程LLM（需授权）| 云端（TOP_SECRET拦截）|
| embedding | 向量嵌入模型 | 设备本地 |

### AIOutputFilter（输出过滤器）

```
class AIOutputFilter:
```javascript

---

## § 9｜执行沙箱

### 沙箱架构

```
执行沙箱
├── 进程隔离（独立进程 / 容器）
├── 文件系统隔离（只读挂载 + 临时写区）
├── 网络隔离（默认断网，按需开放）
├── CPU配额（最大使用率限制）
├── 内存配额（硬限制，超出强制终止）
└── 时间配额（最大执行时长）
```javascript

### 配额配置表

| 资源 | 默认限制 | 最大限制 | 超出处理 |
|---|---|---|---|
| CPU | 80% | 95% | 降速 |
| 内存 | 2GB | 8GB | 强制终止 |
| 执行时长 | 30s | 300s | 超时终止 |
| 文件写入 | 100MB | 1GB | 拒绝写入 |
| 网络带宽 | 0（断网）| 10Mbps | 策略控制 |

### 资源强制执行

```
class ExecutionSandbox:
```javascript

---

## § 10｜节点网络接口

### 节点清单格式

```
{
}
```javascript

### 通信协议（ECDH加密）

```
1. 节点发现（Node Discovery）
1. 密钥交换（ECDH Key Exchange）
1. 任务分发（Task Dispatch）
1. 结果回传（Result Return）
1. DNA验证（Trace Verify）
```javascript

---

## § 11｜数据接口层

### DataInterface 标准

```
class DataInterface(ABC):
```javascript

### 支持的后端

| 后端类型 | 实现类 | 适用场景 |
|---|---|---|
| 本地SQLite | SQLiteBackend | 审计日志、配置存储 |
| 本地文件系统 | FileSystemBackend | 大型媒体、模型文件 |
| 加密本地存储 | EncryptedLocalBackend | 敏感数据（TOP_SECRET）|
| 云存储（可选）| CloudBackend | 非敏感协作数据 |
| IPFS（可选）| IPFSBackend | 去中心化不可篡改存储 |

---

## § 12｜审计系统 — DNA Trace

### dna_trace.db 表结构

```
CREATE TABLE dna_trace (
);
```javascript

### DNA链式哈希特性

| 特性 | 说明 |
|---|---|
| 不可篡改 | 修改任一条记录会破坏后续所有哈希 |
| 链式验证 | chain_hash = SHA256(prev_hash + content_hash) |
| DNA标签格式 | #龍芯⚡️{YYYY-MM-DD}-{action}-{hash8} |
| 存储位置 | 本地 dna_trace.db（不上云）|
| 完整性验证 | verify_chain() 遍历验证全链 |

---

## § 13｜扩展生命周期管理

### 生命周期状态机

```
INSTALLED → INITIALIZED → ACTIVE → UPDATING → ACTIVE
```javascript

### 状态说明

| 状态 | 说明 |
|---|---|
| INSTALLED | 扩展文件已安装，尚未初始化 |
| INITIALIZED | 初始化完毕，可接受请求 |
| ACTIVE | 运行中 |
| UPDATING | 版本升级中，暂时不可用 |
| PAUSED | 暂停服务，保留状态 |
| REMOVED | 已卸载，资源已释放 |

### 生命周期 API

```
class ExtensionLifecycleManager:
```javascript

### 版本兼容性

| 类型 | 说明 | 处理 |
|---|---|---|
| MAJOR 升级 | 破坏性变更 | 需手动迁移 |
| MINOR 升级 | 向后兼容 | 自动热更新 |
| PATCH 升级 | Bug修复 | 自动应用 |

---

## § 14｜CNSH Developer SDK

### SDK 目录结构

```
cnsh_sdk/
├── core/
│   ├── base.py           # AlgorithmInterface, AIModelInterface
│   ├── context.py        # ExecutionContext, Command, ShieldLevel
│   ├── result.py         # AlgorithmResult, AIInferenceResult
│   └── exceptions.py     # CNSH自定义异常
├── security/
│   ├── shield.py         # LocalShieldCore
│   ├── policy.py         # PolicyEngine
│   └── dna.py            # DNA Trace 工具
├── extensions/
│   ├── registry.py       # ExtensionRegistry
│   ├── lifecycle.py      # ExtensionLifecycleManager
│   └── validator.py      # GPG验证工具
├── utils/
│   ├── crypto.py         # ECDH、SHA-256工具
│   ├── sandbox.py        # ExecutionSandbox
│   └── logging.py        # 结构化日志
├── templates/
│   ├── algorithm_ext/    # 算法扩展模板
│   └── ai_ext/           # AI扩展模板
└── examples/
```javascript

### 核心导入

```
from cnsh_sdk.core import (
)
from cnsh_sdk.security import LocalShieldCore, DNATrace
from cnsh_sdk.utils import ExecutionSandbox
```javascript

### 示例扩展：最小可行算法

```
# my_algorithm/main.py
from cnsh_sdk.core import AlgorithmInterface, AlgorithmResult
class MyAlgorithm(AlgorithmInterface):
```javascript

### 开发工作流

```
cnsh_sdk init my_extension   # 初始化扩展模板
# 编写算法逻辑（继承 AlgorithmInterface）
cnsh_sdk validate             # 本地验证 manifest + GPG
cnsh_sdk test                 # 单元测试
gpg --sign signature.gpg      # GPG签名
cnsh_sdk install ./           # 安装到本地运行时
```javascript

---

## § 15｜生态拓扑

### 连接点表

| 连接点 | 内部模块 | 外部接口 | 协议 |
|---|---|---|---|
| 算法入口 | AME | 算法扩展开发者 | AlgorithmInterface |
| AI入口 | AI Runtime | AI模型扩展开发者 | AIModelInterface |
| 节点入口 | Node Network | 分布式计算节点 | REST + ECDH |
| 数据入口 | Data Interface | 外部数据系统 | DataInterface |
| 审计出口 | DNA Trace | 外部审计工具 | SQLite API |

### 未来扩展点

| 扩展方向 | 说明 | 优先级 |
|---|---|---|
| 跨设备同步 | ECDH加密的设备间数据同步 | 高 |
| 沙箱容器化 | Docker/Podman隔离 | 高 |
| 多模型AI内核 | 同时运行多个AI模型 | 中 |
| 第三方审计认证 | SOC2/ISO27001互联 | 中 |

---

## § 16｜完整执行链 — Zero-Break 保证

### 全注释执行链

```
用户输入
```javascript

### 三重保证

<callout icon="✅" color="green_bg">
**保证一：主权保障**
Shield-1主权层权重无穷大，任何试图输出敏感数据的请求将被无条件拦截。本地数据永远不出设备。
</callout>

<callout icon="🔗" color="blue_bg">
**保证二：审计完整**
DNA Trace 链式哈希保证每一条执行记录不可篡改。任何篡改将使后续哈希验证全部失败。
</callout>

<callout icon="🛡️" color="purple_bg">
**保证三：扩展可信**
所有扩展必须通过 GPG 签名验证，未签名或签名失效的扩展不得安装。
</callout>

### 系统身份

```
CNSH Runtime = 单一语法标准 + 层级安全防御 + 不可篡改审计
DNA标签：  #龍芯⚡️2026-03-CNSH-RUNTIME-v1.0
核心等式：  CNSH = 主权保障 × 全链审计 × 沙箱隔离
```javascript

---

<callout icon="🐉" color="blue_bg">
**DNA追溯：** #龍芯⚡️2026-03-CNSH-RUNTIME-v1.0
**GPG指纹：** A2D0092CEE2E5BA87035600924C3704A8CC26D5F
**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**三色审计：** 🟢
**版本：** v1.0 · 16章节全覆盖 · Zero-Break保证
</callout>

### 示例 DNA 条目

```
trace_id:    trace_20260325_abc123
timestamp:   1742825600.123
module:      @ALGORITHM
action:      EXECUTE
shield:      ENCRYPTED
prev_hash:   a3f9e2...（前一条）
content:     SHA256({module+action+params+result})
chain_hash:  SHA256(prev_hash + content_hash)
dna_tag:     #龍芯⚡️2026-03-25-ALGO-EXECUTE-a3f9e2
```javascript

### DNA 验证函数

```
def verify_chain(db_path: str) -> VerifyResult:
```python

```
