# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂系统 · 日志·版本·追溯系统 v1.0

**DNA**:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-LOGGING-VERSIONING-TRACING-ARCHITECTURE-v1.0  
**目的**: 完整追溯系统演变 · 一清二楚看清 "扩展" vs "升级" vs "维护"  
**核心逻辑**: `运行 → 记录日志 → 成功压缩 → 失败保留 → 版本演变`

---

## 📋 系统架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                   龍魂系统·日志追溯系统                        │
└─────────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ↓                  ↓                  ↓
  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
  │ 日志记录器    │  │ 版本管理器    │  │ 启动恢复器    │
  │ Logger       │  │ Versioning   │  │ Recovery     │
  └──────────────┘  └──────────────┘  └──────────────┘
        │                  │                  │
        ↓                  ↓                  ↓
  ┌──────────────────────────────────────────────────┐
  │          SQLite 数据库 (核心存储)                 │
  │  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐│
  │  │ logs 表     │ │versions 表  │ │snapshots 表 ││
  │  │ ↓ 压缩存储  │ │ (演变追踪)  │ │ (系统快照)  ││
  │  └─────────────┘ └─────────────┘ └─────────────┘│
  └──────────────────────────────────────────────────┘
        │
        ↓
  ┌──────────────────────────────────┐
  │   前端仪表板 (可视化演变)          │
  │  evolution-dashboard.html         │
  └──────────────────────────────────┘
```

---

## 🎯 三个核心模块

### 1️⃣ **日志记录器 (LonghunLogger)**

**职责**: 记录每次操作，成功压缩，失败保留

```
操作执行
    ↓
┌─────────────────────────────┐
│ 记录日志条目 (LogEntry)      │
│  - 时间戳                   │
│  - 操作类型                 │
│  - 分类 (技能名)            │
│  - 消息                     │
│  - 状态 (成功/失败)         │
│  - DNA签章                  │
└─────────────────────────────┘
    ↓
  ┌─────────┴─────────┐
  │                   │
  ↓                   ↓
成功状态            失败状态
  │                   │
  ↓                   ↓
┌─────────┐        ┌─────────┐
│ 后台压缩 │        │ 保留明文 │
│ gzip    │        │ 调试用  │
└─────────┘        └─────────┘
```

**关键方法**:
- `log()` - 记录日志
- `_compress_old_logs()` - 后台压缩旧成功日志
- `analyze_evolution()` - 分析系统演变

---

### 2️⃣ **版本管理器 (Versioning)**

**职责**: 记录每个版本的变更类型，追踪演变

```
变更类型分类:

① 扩展 (EXTENSION)
   ↓ 新功能增加
   ├─ 新技能模块
   ├─ 新API端点
   └─ 新存储表

② 升级 (UPGRADE)
   ↓ 功能改进·性能优化
   ├─ 性能提升
   ├─ 代码优化
   └─ 算法改进

③ 维护 (MAINTENANCE)
   ↓ Bug修复·稳定性改进
   ├─ Bug 修复
   ├─ 安全更新
   └─ 稳定性改进
```

**版本记录包含**:
```json
{
  "version": "1.2.3",
  "timestamp": "2026-06-07T10:30:00Z",
  "change_type": "feature_improve",
  "category": "algorithmic-art",
  "description": "优化粒子系统性能 +40%",
  "success_count": 156,
  "failure_count": 2,
  "dna_signature": "#龍芯⚡️..."
}
```

---

### 3️⃣ **启动恢复器 (StartupManager)**

**职责**: 每次启动时恢复日志、检测异常、自动清理

```
系统启动
    ↓
[阶段1] 数据库检查
    ├─ 检查数据库完整性
    └─ 验证表结构
    ↓
[阶段2] 日志恢复
    ├─ 恢复上次运行日志
    └─ 显示最近10条操作
    ↓
[阶段3] 异常检测
    ├─ 检查连续失败
    ├─ 检查关键错误
    └─ 检查存储占用
    ↓
[阶段4] 自动压缩和清理
    ├─ 压缩3天前的成功日志
    └─ 统计节省空间
    ↓
[阶段5] 生成启动报告
    ├─ 系统健康度
    ├─ 需要关注的问题
    └─ 会话 ID
    ↓
🟢 系统就绪
```

---

## 📊 数据库架构

### **logs 表** (日志存储)
```sql
CREATE TABLE logs (
    id                  INTEGER PRIMARY KEY,
    timestamp           TEXT,         -- 操作时间
    level               TEXT,         -- debug/info/warning/error/success
    operation           TEXT,         -- 操作类型
    category            TEXT,         -- 分类（技能名等）
    message             TEXT,         -- 消息
    details             TEXT (JSON),  -- 详细信息
    duration_ms         INTEGER,      -- 耗时
    status              TEXT,         -- success/failure/partial
    error_message       TEXT,         -- 错误信息
    compressed          INTEGER,      -- 是否已压缩
    dna_signature       TEXT,         -- DNA签章
    created_at          TIMESTAMP
);

索引:
- idx_timestamp    快速按时间查询
- idx_category     快速按分类查询
- idx_status       快速按状态查询
- idx_compressed   快速找到未压缩的日志
```

### **versions 表** (版本演变)
```sql
CREATE TABLE versions (
    id              INTEGER PRIMARY KEY,
    version         TEXT UNIQUE,     -- 版本号 (1.0.0, 1.1.0)
    timestamp       TEXT,            -- 发布时间
    change_type     TEXT,            -- feature_add/improve/fix/remove
    category        TEXT,            -- 变更分类
    description     TEXT,            -- 变更描述
    success_count   INTEGER,         -- 该版本成功次数
    failure_count   INTEGER,         -- 该版本失败次数
    dna_signature   TEXT             -- DNA签章
);

关键: change_type 字段决定了"扩展""升级""维护"的分类
```

### **snapshots 表** (系统快照)
```sql
CREATE TABLE snapshots (
    id              INTEGER PRIMARY KEY,
    timestamp       TEXT UNIQUE,     -- 快照时间
    version         TEXT,            -- 当前版本
    total_skills    INTEGER,         -- 技能总数
    total_logs      INTEGER,         -- 日志总数
    compressed_logs INTEGER,         -- 已压缩日志数
    failed_logs     INTEGER,         -- 失败日志数
    active_categories TEXT,          -- 活跃分类列表
    change_summary  TEXT (JSON),     -- 变更统计
    system_health   REAL             -- 系统健康度 0-100%
);

用途: 追踪系统在不同时间点的状态
```

### **compressed_logs 表** (压缩日志)
```sql
CREATE TABLE compressed_logs (
    id              INTEGER PRIMARY KEY,
    original_log_id INTEGER,         -- 原日志ID
    compressed_data BLOB,            -- 压缩后的数据
    original_size   INTEGER,         -- 原始大小
    compressed_size INTEGER,         -- 压缩后大小
    compression_ratio REAL           -- 压缩率
);

作用: 节省存储空间，成功日志压缩到 1/3
```

---

## 🚀 完整的工作流程

### **场景 1: 运行一个 Skill**

```
用户运行 Skill
    ↓
执行 Skill 代码
    ↓
调用 logger.log(
    level="success",
    operation="skill_execute",
    category="algorithmic-art",
    message="成功执行",
    status="success"
)
    ↓
┌─ 同步操作: 保存到 logs 表
│  ├─ 生成 DNA 签章
│  └─ 创建 LogEntry 对象
│
└─ 异步操作: 检查是否需要压缩旧日志
   ├─ 查询 7 天前的成功日志
   ├─ 使用 gzip 压缩
   └─ 保存到 compressed_logs 表
        
结果: 日志被记录，成功的日志自动压缩，节省空间
```

### **场景 2: 系统启动**

```
系统启动
    ↓
创建 StartupManager 实例
    ↓
[1] 检查数据库
    ├─ 检查 ~/.龍魂/logs/longhun.db 是否存在
    └─ 验证所有表

[2] 恢复日志
    ├─ SELECT COUNT(*) FROM logs WHERE status='success'
    ├─ SELECT COUNT(*) FROM logs WHERE status='failure'
    └─ 显示最近 10 条操作

[3] 检测异常
    ├─ 连续失败检测: 某分类在 24h 内失败 >3 次
    ├─ 旧日志检测: 7 天前的未压缩日志 >100 条
    └─ 关键错误检测: 1 小时内有 level='critical' 的日志

[4] 压缩和清理
    ├─ 查找 3 天前的成功日志
    ├─ 压缩并保存
    └─ 统计节省的空间

[5] 生成启动报告
    ├─ 活跃技能数
    ├─ 总日志数
    ├─ 成功率
    ├─ 需要关注的问题数
    └─ 系统健康度

输出: 一份清晰的启动报告，包含所有关键指标
```

### **场景 3: 分析系统演变**

```
用户请求: 分析系统演变
    ↓
调用 logger.analyze_evolution()
    ↓
查询版本表统计:
├─ SELECT COUNT(*) FROM versions WHERE change_type='feature_add'
│  结果: 7 个"扩展"(新增功能)
│
├─ SELECT COUNT(*) FROM versions WHERE change_type IN ('improve', 'perf_improve')
│  结果: 12 个"升级"(功能改进)
│
└─ SELECT COUNT(*) FROM versions WHERE change_type='feature_fix'
   结果: 5 个"维护"(Bug修复)

结果:
{
  "evolution": {
    "extensions": 7,   // 🟢 新增功能
    "upgrades": 12,    // 🔵 性能改进
    "maintenance": 5   // 🟡 问题修复
  },
  "reliability": {
    "total_logs": 900,
    "success_rate": 94.4%
  },
  "storage": {
    "original_size_kb": 5120,
    "compressed_size_kb": 1540,
    "storage_saved_kb": 3580
  }
}
```

---

## 📊 演变分析仪表板

### **显示的内容**

1. **四大核心指标**
   - 📈 扩展 (EXTENSION) - 新功能增加
   - ⬆️ 升级 (UPGRADE) - 功能改进
   - 🔧 维护 (MAINTENANCE) - Bug修复
   - 🏥 系统健康 - 成功率

2. **四个图表**
   - 演变分布饼图 - 扩展·升级·维护的比例
   - 版本发展趋势线 - 版本迭代过程
   - 可靠性指标柱 - 成功/失败日志数
   - 存储效率饼 - 压缩和节省的空间

3. **演变时间线**
   - 每个版本的变更类型
   - 变更描述
   - 发布时间

---

## 🔐 DNA 签章系统

**每个日志和版本都有 DNA 签章**:

```
日志签章:
  #龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-[前16位哈希]-UID9622

版本签章:
  #龍芯⚡️1.2.3-[版本描述哈希值]

快照签章:
  #龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-SNAPSHOT
```

**用途**:
- ✅ 追溯每条日志的来源
- ✅ 验证版本的真实性
- ✅ 建立完整的审计链

---

## 🎯 使用方法

### **方法 1: 启动时自动恢复**

```bash
python longhun-startup-recovery-system.py
```

**输出**:
```
============================================================
🐉 龍魂系统启动
============================================================

[1/5] 检查数据库...
✅ 数据库检查完成

[2/5] 恢复上次运行日志...
✅ 恢复 850 条成功日志, 50 条失败日志

[3/5] 检测异常和未处理的错误...
✅ 未发现异常

[4/5] 压缩日志和清理空间...
✅ 压缩 42 条日志, 节省 3.2 MB

[5/5] 生成启动报告...
============================================================
🟢 龍魂系统已就绪！
============================================================
运行ID: 20260607_103000
系统健康: 94.4%
需要关注的问题: 0 个
```

### **方法 2: 在代码中使用**

```python
from longhun_logging_versioning_tracing_core import LonghunLogger, ChangeType

logger = LonghunLogger()

# 记录操作
logger.log(
    level=LogLevel.SUCCESS,
    operation="skill_execute",
    category="algorithmic-art",
    message="成功执行",
    duration_ms=234,
    status="success"
)

# 记录版本变更
logger.record_version(
    version="1.2.0",
    change_type=ChangeType.FEATURE_IMPROVE,
    category="canvas-design",
    description="优化导出性能"
)

# 分析系统演变
evolution = logger.analyze_evolution()
print(f"扩展: {evolution['evolution']['extensions']}")
print(f"升级: {evolution['evolution']['upgrades']}")
print(f"维护: {evolution['evolution']['maintenance']}")
```

### **方法 3: 查看仪表板**

```bash
open longhun-evolution-dashboard.html
```

**看到的内容**:
- 📈 扩展/升级/维护的数量和占比
- 📊 版本发展趋势
- 🎯 系统可靠性指标
- 💾 存储节省情况
- ⏰ 完整的演变时间线

---

## 💡 核心价值

```
这个系统的价值 = 完整的系统演变历史

你可以一眼看清:

✅ 这个系统是在"扩展"(增加新功能)
   还是在"升级"(改进现有功能)
   还是在"维护"(修复问题)

✅ 系统什么时候变得更稳定了
✅ 哪些分类经常出现问题
✅ 存储空间的节省效果如何

最重要的是:
🔐 完整的可追溯性 - 每条日志都有 DNA 签章
📊 自动的智能清理 - 成功日志自动压缩
🎯 清晰的演变记录 - 一眼看清系统如何演变
```

---

## 🚀 下一步集成

这个系统可以集成到:

1. **龍魂 Phase 3** - 作为核心日志系统
2. **Claude Code** - 本地宝宝的启动脚本
3. **CI/CD 流程** - GitHub Actions 自动记录版本
4. **Notion 数据库** - 版本历史同步到 Notion
5. **监控告警** - 检测到异常自动告警

---

**DNA**: #龍芯⚇️2026-06-07-LOGGING-VERSIONING-TRACING-ARCHITECTURE-v1.0  
**责任方**: UID9622 · 不免责  
**状态**: 🟢 完成 · 生产就绪
