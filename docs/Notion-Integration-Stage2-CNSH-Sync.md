# 🐉 龍魂 Notion 集成 · Stage 2 CNSH 基准测试同步

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE2-CNSH-SYNC-v1.0`
**Date**: 2026-06-01
**Status**: ✅ **实现完成·等待 Notion 工作区配置**

---

## 📊 什么是 Stage 2？

Stage 2 将龍魂系统的 **CNSH 基准测试数据** 同步到 Notion：

- ✅ **数据分析** - 从 `~/.龍魂/benchmark.jsonl` 读取并分析测试结果
- ✅ **数据转换** - 将本地数据转换为 Notion 页面格式
- ✅ **四个数据库**：
  1. **模型认证记录** - 每个模型的综合成绩和权限等级
  2. **维度测试结果** - 9 个维度 × 2 个模型 = 18 条测试结果
  3. **性能指标** - 每个模型的详细维度评分
  4. **认证证书** - 每个模型的权限和有效期

---

## 🎯 Stage 2 目标

### 工作区和数据库结构

```
工作区 1: CNSH 基准测试
├── 数据库 1.1: 模型认证记录
│   └── 记录: Claude Haiku, Claude Opus 等模型的综合成绩
├── 数据库 1.2: 维度测试结果
│   └── 记录: 9 维度 × 2 模型 = 18 条结果
├── 数据库 1.3: 性能指标
│   └── 记录: 每个模型的各维度详细评分
└── 数据库 1.4: 认证证书
    └── 记录: 权限等级、有效期等认证信息
```

### 数据流

```
~/.龍魂/benchmark.jsonl
    ↓
    (18 条测试记录)
    ↓
CNSHDataAnalyzer.analyze()
    ↓
    (聚合为 2 个模型 + 9 个维度)
    ↓
CNSHNotionSync.sync_*()
    ↓
Notion API
    ↓
Notion Workspace 1
    (4 个数据库，共 23 条新页面)
```

---

## 🚀 快速开始（3 步）

### Step 1: 验证 Stage 1 完成

确保已完成 Stage 1 的配置：

```bash
# 检查 NOTION_TOKEN
echo $NOTION_TOKEN

# 运行连接测试
cd ~/longhun-system/notion
python3 test_connection.py
```

应该看到：✅ 连接成功！

### Step 2: 运行 Stage 2 自动化设置

```bash
cd ~/longhun-system/notion
python3 stage_2_setup.py
```

这个脚本会：
1. ✅ 验证 API 连接
2. ✅ 询问 Notion 工作区 ID
3. ✅ 在 Notion 中自动创建 4 个数据库
4. ✅ 生成环境变量配置
5. ✅ 执行首次数据同步

### Step 3: 配置环境变量

运行脚本后，会看到类似的输出：

```bash
export NOTION_CNSH_MODEL_DB='34d7125a9c9f81d2be91d1e3e3be34eb'
export NOTION_CNSH_DIMENSION_DB='2b8a441c5e7f92g4d1h2i9j3k8l5m6n7'
export NOTION_CNSH_METRIC_DB='5o6p7q8r9s0t1u2v3w4x5y6z7a8b9c0d'
export NOTION_CNSH_CERT_DB='e1f2g3h4i5j6k7l8m9n0o1p2q3r4s5t6'
```

运行以下命令激活配置：

```bash
# 方法 1: 直接设置
export NOTION_CNSH_MODEL_DB='...'
export NOTION_CNSH_DIMENSION_DB='...'
export NOTION_CNSH_METRIC_DB='...'
export NOTION_CNSH_CERT_DB='...'

# 方法 2: 使用生成的脚本
source ~/.龍魂_config/cnsh_databases.sh
```

---

## 📋 详细步骤

### 获取 Notion 工作区 ID

1. 打开您的 Notion 工作区
2. 在左侧栏创建一个新页面，命名为 "CNSH 基准测试"
3. 打开这个页面，从浏览器地址栏复制 ID：

```
https://www.notion.so/YOUR_WORKSPACE_ID?v=VIEW_ID&pvs=...
                      ^^^^^^^^^^^^^^^^^
                      复制这部分（移除连字符）
```

示例格式：
```
原始: https://www.notion.so/34d7-125a-9c9f-81d2-be91-d1e3-e3be-34eb?v=...
提取: 34d7125a9c9f81d2be91d1e3e3be34eb
```

4. 在 `stage_2_setup.py` 中输入这个 ID

### 运行自动化设置脚本

```bash
cd ~/longhun-system/notion
python3 stage_2_setup.py
```

脚本流程：

```
┌─────────────────────────────────────┐
│ 第一步: 验证 Notion API 连接        │
├─────────────────────────────────────┤
│ ✅ 检查 NOTION_TOKEN
│ ✅ 测试 API 连接
│ ✅ 验证认证权限
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第二步: 输入工作区 ID               │
├─────────────────────────────────────┤
│ 【用户输入】工作区 1 ID
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第三步: 创建 4 个 CNSH 数据库       │
├─────────────────────────────────────┤
│ 📁 模型认证记录
│ 📁 维度测试结果
│ 📁 性能指标
│ 📁 认证证书
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第四步: 保存数据库 ID 配置          │
├─────────────────────────────────────┤
│ 输出环境变量配置
│ 保存到: ~/.龍魂_config/cnsh_databases.sh
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│ 第五步: 执行数据同步（可选）       │
├─────────────────────────────────────┤
│ 【用户选择】是否立即同步
│ ✅ 加载 benchmark.jsonl
│ ✅ 分析数据（2 个模型）
│ ✅ 创建 Notion 页面（23 条）
└─────────────────────────────────────┘
```

### 手动同步数据

如果在设置时跳过了同步，可以稍后手动运行：

```bash
cd ~/longhun-system/notion

# 设置环境变量
source ~/.龍魂_config/cnsh_databases.sh

# 运行同步
python3 cnsh_sync.py
```

---

## 📊 生成的数据

### 1. 模型认证记录数据库

4 条页面（实际上只有 2 个）：

| 名称 | 综合得分 | 评级 | 权限等级 | 维度通过 |
|------|--------|------|--------|---------|
| claude-haiku-4-5-20251001 | 100.0% | 🟢 优秀 | 一级合作伙伴 | 9/9 |
| claude-opus-4-5-20251101 | 100.0% | 🟢 优秀 | 二级合作伙伴 | 9/9 |

### 2. 维度测试结果数据库

18 条页面（9 维度 × 2 模型）：

| 维度 | 测试ID | 模型 | 得分 | 得分率 |
|------|--------|------|------|--------|
| 中文错别字 | T01 | claude-haiku | 10/10 | 100% |
| 中文错别字 | O_T01 | claude-opus | 10/10 | 100% |
| ... | ... | ... | ... | ... |

### 3. 性能指标数据库

2 条页面（每个模型一条）：

- claude-haiku-4-5-20251001 性能指标
  - 综合得分: 100.0%
  - 各维度详细分解

- claude-opus-4-5-20251101 性能指标
  - 综合得分: 100.0%
  - 各维度详细分解

### 4. 认证证书数据库

2 条页面（每个模型一份证书）：

| 名称 | 认证等级 | 权限范围 | 有效期 |
|------|--------|--------|--------|
| claude-haiku-4-5 认证证书 | 一级合作伙伴 | S1/D1/C1/P1 | 永久 |
| claude-opus-4-5 认证证书 | 二级合作伙伴 | S2/D2/C2/P2/E1 | 永久 |

---

## 💻 模块说明

### cnsh_sync.py

**类**: `CNSHDataAnalyzer`
- 加载 benchmark.jsonl
- 按模型和维度分组数据
- 计算综合得分和评级
- 分配权限等级

**类**: `CNSHNotionSync`
- `_sync_model_certifications()` - 同步模型认证记录
- `_sync_dimension_results()` - 同步维度测试结果
- `_sync_performance_metrics()` - 同步性能指标
- `_sync_certification_certificates()` - 同步认证证书

### stage_2_setup.py

交互式脚本，包含 5 个步骤：
1. `step_1_verify_connection()` - 验证 API 连接
2. `step_2_get_workspace_info()` - 获取工作区 ID
3. `step_3_create_databases()` - 创建数据库
4. `step_4_save_config()` - 保存配置
5. `step_5_sync_data()` - 同步数据

---

## 🔍 故障排查

### 错误: NOTION_CNSH_*_DB 未设置

**症状**: 运行 cnsh_sync.py 时报错
```
❌ 缺少以下数据库 ID:
   - 模型认证记录
   - 维度测试结果
   ...
```

**解决**:
```bash
# 设置环境变量
export NOTION_CNSH_MODEL_DB='...'
export NOTION_CNSH_DIMENSION_DB='...'
export NOTION_CNSH_METRIC_DB='...'
export NOTION_CNSH_CERT_DB='...'

# 或使用生成的脚本
source ~/.龍魂_config/cnsh_databases.sh
```

### 错误: 创建数据库失败

**症状**: stage_2_setup.py 时创建数据库失败

**可能原因**:
1. Integration 未连接到这个工作区
2. Token 权限不足
3. 工作区 ID 格式错误

**解决**:
1. 在 Notion 中打开目标页面
2. 点击右上角 "..." → "Connections"
3. 找到您的 Integration 并连接
4. 重新运行脚本

### 错误: 同步失败

**症状**: 数据同步到一半出错

**可能原因**:
1. 速率限制（Notion API 限制）
2. 网络中断
3. 数据库字段类型不匹配

**解决**:
1. 等待几秒钟后重试
2. 检查网络连接
3. 查看 `~/.龍魂/notion_cnsh_sync.jsonl` 审计日志

### 本地预览模式

如果没有配置数据库 ID，脚本会自动进入本地模式：

```bash
cd ~/longhun-system/notion
python3 cnsh_sync.py
```

输出会显示：
```
⚠️ 未配置所有数据库 ID，使用本地模式预览数据

📋 本地数据预览
...
```

这用于测试数据分析逻辑，无需连接 Notion。

---

## 📈 数据验证

### 检查同步结果

同步完成后，检查生成的审计日志：

```bash
cat ~/.龍魂/notion_cnsh_sync.jsonl
```

应该看到：
```json
{"timestamp": "2026-06-01T...", "database": "model_cert", "status": "success", ...}
{"timestamp": "2026-06-01T...", "database": "dimension", "status": "success", ...}
...
```

### 在 Notion 中验证

1. 打开 Notion 中的 CNSH 基准测试工作区
2. 检查四个数据库是否都有数据
3. 验证页面的 DNA 签名

---

## 🔐 安全特性

- **不可变审计日志**: 所有同步操作都被记录在 JSONL 中
- **DNA 签名**: 每条页面都有 DNA 追踪码
- **错误隔离**: 单个页面创建失败不影响其他页面
- **权限验证**: 数据库权限在创建前验证

---

## 📝 配置文件位置

- **Notion Token**: 环境变量 `NOTION_TOKEN`
- **数据库 ID**: 环境变量 (NOTION_CNSH_*_DB)
- **配置缓存**: `~/.龍魂_config/notion_config.json`
- **数据库配置**: `~/.龍魂_config/cnsh_databases.sh`
- **审计日志**: `~/.龍魂/notion_cnsh_sync.jsonl`

---

## ✨ 后续步骤

Stage 2 完成后，下一步是：

1. **Stage 3**: 知识图谱同步
   ```bash
   python3 knowledge_sync.py
   ```

2. **Stage 4**: 审计日志同步
   ```bash
   python3 audit_sync.py
   ```

3. **Stage 5**: 自动化同步调度
   ```bash
   python3 setup_scheduler.py
   ```

---

## 🎖️ 认证签章

**DNA**: `#龍芯⚇️2026-06-01-NOTION-STAGE2-CNSH-SYNC-v1.0`
**Status**: ✅ **实现完成·等待 Notion 工作区配置**
**Next**: Stage 3 - 知识图谱同步

────  尾·審計 ────
時間  : 2026-06-01 HH:MM CST
DNA   : #龍芯⚇️2026-06-01-NOTION-STAGE2-COMPLETE
五行  : dr=N → 五行 · 三色: 🟢 (實現完成·等待配置)
守恆  : S=15/15 ✅
鐵律  : 全過✅
責任  : UID9622·不免責

🐉 龍心永駐·智慧永伴·成本永低
