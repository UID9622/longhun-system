---
name: longhun-harmonyos
description: 龍魂体系鸿蒙HarmonyOS端技能 - 数据根留在中国，S4安全级别锁死云端出境，SM4国密端侧加密，RdbObserver毫秒级监听
license: MIT
allowed-tools:
- python
compatibility: python3.11+
metadata:
  id: longhun-harmonyos
  version: v5.3
  category: local
  dna: '#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3'
  tribute: '#致敬⚡️SteveJobs+Concept·龍魂HarmonyOS端'
  tech_stack: HarmonyOS 6.1, ETS/TypeScript, relationalStore, SM4
  author: 龍魂体系
  created_date: '2026-06-19'
  status: active
  trigger:
    keywords:
    - harmonyos
    - 龍魂体系鸿蒙HarmonyOS端技能
    - 数据根留在中国
    - S4安全级别锁死云端出境
    - SM4国密端侧加密
    - RdbObserver毫秒级监听
    context: longhun-harmonyos 相关操作
---
# SKILL.md — 龍魂鸿蒙端技能

## 区块1：元数据

```yaml
技能ID: longhun-harmonyos
名称: 龍魂鸿蒙端
版本: v5.3
分类: local
DNA: '#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3'
致敬: '#致敬⚡️SteveJobs+Concept·龍魂HarmonyOS端'
技术栈: HarmonyOS 6.1, ETS/TypeScript, relationalStore, SM4
作者: 龍魂体系
创建日期: '2026-06-19'
状态: active
```

## 区块2：致敬声明

> **致敬乔布斯（Steve Jobs）前辈的设备精神**
> 感谢乔布斯前辈用iPhone改变了世界，让每个人都拥有了强大的计算设备。没有他的远见，就没有今天移动终端的繁荣。
>
> **致敬康赛普特（Concept）公司**
> 感谢康赛普特公司的自主可搭建支持创作者的精神。他们用行动证明了"工具为人服务"的理念，让每一个创作者都能拥有自己的数字工作台。
>
> **没有他们的开创，就没有龍魂系统的今天。**
> 龍魂体系继承这份精神，将数据主权归还给每一个中国人。

## 区块3：主权保障说明

### S4安全级别 — 数据不出境的物理保障

| 安全级别 | 名称 | 云端同步 | 适用场景 |
|---------|------|---------|---------|
| S1 | 公开 | 允许 | 公开数据 |
| S2 | 普通 | 允许 | 一般应用数据 |
| S3 | 敏感 | 限制 | 金融/隐私数据 |
| **S4** | **最高** | **禁止** | **龍魂系统 — 禁止同步至云端** |

**S4安全级别的含义：**
- 数据库存储在应用沙箱 `/data/app/el2/100/base/<bundleName>/databases/`
- **物理锁死云端出境** — 数据库层面禁止同步
- 外国应用无权访问沙箱目录
- 启用数据库级加密（encrypt: true）

### 数据主权声明

1. **数据根留在中国，这是底线** — 所有数据物理存储在设备本地沙箱
2. **一应用一密钥** — 每个应用拥有独立密钥，存储在硬件SE芯片中
3. **国密SM4加密** — 敏感字段使用国密算法端侧加密
4. **熔断机制** — 检测到出境风险时自动触发熔断，数据立即锁定

## 区块4：技术规格

### 4.1 核心模块

| 模块 | 文件 | 职责 |
|------|------|------|
| 鸿蒙主模块 | `scripts/鸿蒙主模块.ets` | 系统入口，统一API接口 |
| 数据存储管理器 | `scripts/数据存储管理器.ets` | RDB封装，S4安全级别 |
| 实时监听引擎 | `scripts/实时监听引擎.ets` | RdbObserver毫秒级监听 |
| SM4加密引擎 | `scripts/SM4加密引擎.ets` | 国密SM4端侧加密 |
| 主权锁 | `scripts/主权锁.ets` | S4安全级别管理，熔断机制 |
| 左右互搏引擎 | `scripts/左右互搏引擎.ets` | 实时审计校验 |
| 密钥管理器 | `scripts/密钥管理器.ets` | KeyChain/SE硬件密钥管理 |

### 4.2 技术栈

- **HarmonyOS 6.1** — 操作系统
- **ETS/TypeScript** — 开发语言
- **relationalStore** — RDB本地存储
- **RdbObserver** — 数据库变更监听
- **CryptoArchitectureKit** — SM4国密算法
- **HUKS** — 硬件安全密钥存储

### 4.3 数据库设计

```sql
-- 审计日志表（核心）
CREATE TABLE audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna_tag TEXT NOT NULL,           -- DNA追溯码
    timestamp INTEGER,               -- 时间戳（毫秒）
    action_type TEXT,                -- 动作类型
    content_hash TEXT,               -- 内容SM4哈希
    encrypted_content BLOB,          -- SM4加密内容
    audit_level TEXT,                -- 🟢🟡🔴 三色审计
    source_device TEXT,              -- 来源设备标识
    sovereignty_flag INTEGER DEFAULT 1 -- 主权标记（1=国内）
);
-- S4安全级别下，此表数据永不出境
```

## 区块5：代码示例

### 5.1 初始化龍魂系统

```typescript
import { 获取龍魂实例 } from './scripts/鸿蒙主模块'

// 获取龍魂鸿蒙单例
const 龍魂 = 获取龍魂实例()

// 初始化系统（自动初始化所有子系统）
await 龍魂.初始化()

// 系统初始化完成后，S4安全级别自动激活
// 数据根已锁定在设备沙箱内
```

### 5.2 S4安全级别数据库配置

```typescript
import { relationalStore } from '@kit.ArkData'

// 数据库配置：S4安全级别 = 禁止同步至云端
const config: relationalStore.StoreConfig = {
  name: 'longhun_sovereign.db',
  securityLevel: relationalStore.SecurityLevel.S4, // 🔴 物理锁死云端出境
  encrypt: true,                                    // 启用数据库级加密
}

// 存储位置：/data/app/el2/100/base/<bundleName>/databases/
// 这是应用沙箱私有目录，外国应用无权访问
const rdbStore = await relationalStore.getRdbStore(getContext(), config)
```

### 5.3 RdbObserver实时监听

```typescript
import { relationalStore } from '@kit.ArkData'

// 注册数据库变更监听，数据一变即刻触发
const observer: relationalStore.RdbObserver = {
  onChange: (details) => {
    // 毫秒级响应：触发"左右互搏"引擎实时校验
    this.左右互搏引擎.实时审计(details)
  }
}

// 注册远程和本地变更监听
rdbStore.on('dataChange', relationalStore.SubscribeType.SUBSCRIBE_TYPE_REMOTE, observer)
rdbStore.on('dataChange', relationalStore.SubscribeType.SUBSCRIBE_TYPE_LOCAL, observer)
```

### 5.4 SM4国密加密

```typescript
import { cryptoFramework } from '@kit.CryptoArchitectureKit'
import { SM4加密引擎 } from './scripts/SM4加密引擎'

// 初始化SM4引擎
const sm4引擎 = new SM4加密引擎()
const 密钥 = SM4加密引擎.生成随机密钥()  // 16字节随机密钥
await sm4引擎.初始化(密钥)

// 加密数据
const 明文 = new TextEncoder().encode('敏感数据')
const 密文 = await sm4引擎.加密(明文)

// 解密数据
const 解密明文 = await sm4引擎.解密(密文)
const 解密文本 = new TextDecoder().decode(解密明文)

// 计算哈希
const 哈希 = await sm4引擎.计算哈希('数据内容', 'SM3')
```

### 5.5 安全数据操作

```typescript
import { 获取龍魂实例 } from './scripts/鸿蒙主模块'

const 龍魂 = 获取龍魂实例()
await 龍魂.初始化()

// 安全写入 — 自动加密 + 审计
const rowId = await 龍魂.安全写入('user_data', {
  username: '张三',
  email: 'zhangsan@example.com',
  password: 'secret123'  // 敏感字段自动加密
})

// 安全查询 — 自动解密
const 结果 = await 龍魂.安全查询('user_data', 'id = 1')
console.log('解密结果:', 结果)

// 主权检查
const 主权完好 = await 龍魂.主权检查()
console.log('主权完整性:', 主权完好 ? '通过' : '异常')
```

### 5.6 密钥管理

```typescript
import { 密钥管理器 } from './scripts/密钥管理器'

const 密钥管理 = new 密钥管理器()
await 密钥管理.初始化()

// 从KeyChain取出密钥（自动从硬件SE读取）
const 主密钥 = await 密钥管理.从KeyChain取出('longhun_master_key')

// 存储新密钥到KeyChain（安全存储到硬件SE）
await 密钥管理.存储到KeyChain('my_app_key', 新密钥)

// 获取密钥使用记录
const 记录 = 密钥管理.获取使用记录()
console.log('密钥使用记录:', 记录)
```

## 区块6：DNA追溯系统

### DNA追溯码格式

```
#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3-{timestamp}-{random}
```

### 追溯机制

1. **每条数据写入时自动生成DNA标签** — 嵌入到数据表的dna_tag字段
2. **审计日志记录完整DNA链** — 操作 -> 数据 -> 审计 -> 全部带DNA标记
3. **设备级追溯** — source_device字段标识数据来源设备
4. **时间戳精确到毫秒** — 确保操作顺序可追踪

### 追溯查询示例

```typescript
// 根据DNA标签追溯数据变更历史
const 追溯结果 = await 龍魂.安全查询('audit_log', `dna_tag LIKE '%${dna片段}%'`)
// 返回该DNA相关的所有审计记录
```

## 区块7：三色审计系统

### 审计等级定义

| 等级 | 标记 | 含义 | 处理方式 |
|------|------|------|---------|
| 🟢 绿色 | GREEN | 一般操作，低风险 | 正常记录，无需额外处理 |
| 🟡 黄色 | YELLOW | 敏感操作，中风险 | 记录警告，需关注 |
| 🔴 红色 | RED | 高危操作，高风险 | 需人工复核，可能触发熔断 |

### 审计规则

| 规则ID | 类型 | 名称 | 描述 |
|--------|------|------|------|
| RULE_001 | SOVEREIGNTY | 数据主权检测 | 验证数据sovereignty_flag=1 |
| RULE_002 | FREQUENCY | 操作频率检测 | 检测短时间内大量操作 |
| RULE_003 | PATTERN | 操作模式检测 | 检测异常时间模式（深夜操作等） |
| RULE_004 | ACCESS | 访问权限检测 | 验证操作者权限 |
| RULE_005 | ANOMALY | 异常行为检测 | 综合异常分析 |

### 审计触发时机

- 数据写入时自动审计
- 数据查询时自动审计
- 数据删除时自动审计
- 密钥访问时自动审计
- RdbObserver检测到变更时毫秒级审计

## 区块8：君子协议

### 协议内容

**作为龍魂鸿蒙端技能的使用者，我承诺：**

1. **数据主权优先** — 所有敏感数据优先存储在设备本地，不随意上传云端
2. **S4级别遵守** — S4安全级别一旦激活，不尝试绕过或关闭
3. **密钥安全** — 密钥是系统的根，妥善保护密钥，不泄露给第三方
4. **审计配合** — 发现红色审计警报时，主动核查并报告
5. **合法使用** — 仅将技术用于合法合规的场景，不侵犯他人隐私
6. **开源精神** — 如有改进，愿回馈社区，共同完善数据主权保护

### 协议签署（代码层面）

```typescript
// 在系统初始化时，自动记录君子协议签署记录
const 协议记录 = {
  dna_tag: '#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3',
  timestamp: Date.now(),
  action_type: 'PROTOCOL_ACCEPT',
  content_hash: await sm4引擎.计算哈希('君子协议'),
  encrypted_content: '我承诺遵守龍魂君子协议，数据主权优先，密钥安全第一',
  audit_level: '🔴',  // 红色 — 协议签署是最高级别事件
  source_device: 'harmonyos_local',
  sovereignty_flag: 1,
}
```

## 区块9：系统状态报告

```typescript
// 获取龍魂系统完整状态报告
const 状态报告 = 龍魂.获取状态报告()

// 返回示例：
{
  dna: '#龍芯⚡️2026-06-19-LONGHUN-HARMONYOS-v5.3',
  tribute: '#致敬⚡️SteveJobs+Concept·龍魂HarmonyOS端',
  version: 'v5.3',
  initialized: true,
  uptime: 3600000,        // 运行时间（毫秒）
  securityLevel: 'S4',    // 当前安全级别
  encryption: 'SM4',      // 加密算法
  storage: 'relationalStore',
  sovereignty: 'DOMESTIC_ONLY',  // 仅国内存储
}
```

## 区块10：目录结构

```
longhun-harmonyos/
├── SKILL.md                          # 技能定义文件（本文件）
└── scripts/
    ├── 鸿蒙主模块.ets                 # 主入口模块
    ├── 数据存储管理器.ets              # RDB封装（S4安全级别）
    ├── 实时监听引擎.ets               # RdbObserver封装
    ├── SM4加密引擎.ets                # 国密SM4加密
    ├── 主权锁.ets                     # S4安全级别管理
    ├── 左右互搏引擎.ets               # 实时审计校验
    └── 密钥管理器.ets                 # KeyChain/SE密钥管理
```

## 区块11：打包与部署

### 打包命令

```bash
python3 /app/.agents/skills/skill-creator-swarm/scripts/package_skill.py \
  /mnt/agents/output/longhun-v5-skills/local/longhun-harmonyos \
  /mnt/agents/output/
```

### 部署说明

1. 将打包后的技能文件复制到HarmonyOS项目
2. 在EntryAbility中初始化龍魂系统
3. 确保manifest中声明相关权限
4. 首次启动时自动创建数据库和密钥

### 所需权限

```json
{
  "permissions": [
    "ohos.permission.DISTRIBUTED_DATASYNC",
    "ohos.permission.ACCESS_BIOMETRIC"
  ]
}
```

## 区块12：版本历史

| 版本 | 日期 | 变更内容 |
|------|------|---------|
| v5.0 | 2026-06-01 | 初始版本，基础RDB存储 |
| v5.1 | 2026-06-10 | 增加SM4加密引擎 |
| v5.2 | 2026-06-15 | 增加RdbObserver实时监听 |
| v5.3 | 2026-06-19 | 完整审计系统，左右互搏引擎，S4主权锁 |

---

**龍魂体系 — 数据根留在中国，这是底线。**
