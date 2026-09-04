> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统 · 命名即架构 · 四层命名法 v2.0

> 协议编号：LH-NAMING-ARCH-2026-0716-v2.0
> 核心哲学：命名就是架构，文件系统就是数据库，文件名就是联动协议
> 主权人格：UID9622 | 龍芯北辰
> DNA追溯码：#龍魂⚡️丙午·辛未·命名即架构-v2
> 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> 生成时间：2026-07-16（v1.0: 2026-07-14）
> 状态：可执行 · 已部署
> v2.0新增：语义对齐三层体系 + 文件命名格式`[摘要]_[类型]_[结构]_[权限]_[DNA].扩展名`

---

## 〇、v2.0 新增：文件命名格式（焊死）

### 0.1 通用文件命名

```
[摘要]_[类型]_[结构]_[权限]_[DNA].扩展名
```

| 段 | 说明 | 示例 |
|:---|:---|:---|
| **摘要** | 4-8字，说清内容 | `合同审计` `押金陷阱` `清朗行动` |
| **类型** | 内容格式 | `txt` `md` `py` `json` `html` |
| **结构** | 模板类型 | `report` `template` `audit` `decision` `log` |
| **权限** | 谁可看/可改 | `P0` `P1` `P2` `P3` `P4` |
| **DNA** | 追溯码 | `丙午·辛未·001` |

> **引擎层仍用四层命名法**（见§二至§四），本格式适用于通用文档/报告/数据文件。

### 0.2 语义对齐三层体系

```
┌─────────────────────────────────────┐
│  L1 文件名对齐（物理层）             │
│  摘要_类型_结构_权限_DNA.扩展名       │
├─────────────────────────────────────┤
│  L2 语义对齐（逻辑层）               │
│  同义词/近义词/大白话 → 标准语义节点   │
├─────────────────────────────────────┤
│  L3 触角传递（关联层）               │
│  文件内容语义提取 → 节点关联 → 交叉激活 │
└─────────────────────────────────────┘
```

**落地引擎**：
- `L3_数据层/semantic_nodes.py` — 语义节点库 + 标准化器
- `L3_数据层/antenna_network.py` — 触角网络 + 交叉激活
- `L5_服务层/naming_engine.py` — 命名即架构引擎

---

## 一、核心宣言

```
大道至简。

不需要神经网络，不需要数据库，不需要知识库，不需要引用系统。
文件名搞清楚了，一切联动都在命名里。

14亿人用中文语法语义做技术，谁敢卡我们脖子！
```

## 二、四层命名法（引擎层标准）

### 2.1 总览

```
┌─────────────────────────────────────────┐
│  第一层 · 物理层（文件命名）              │
│  ├── 文件名 = 内容标识                    │
│  ├── 目录结构 = 分类体系                  │
│  └── 版本号 = 演进轨迹                    │
├─────────────────────────────────────────┤
│  第二层 · 身份层（DNA标记）               │
│  ├── UID9622 = 你是谁                     │
│  ├── #CONFIRM码 = 一次性验证              │
│  └── 时间戳 = 什么时候                    │
├─────────────────────────────────────────┤
│  第三层 · 主权层（归属身份权）             │
│  ├── GPG指纹 = 数字签名                   │
│  ├── 签章链 = 责任追溯                    │
│  └── 授权层级 = 谁能动                    │
├─────────────────────────────────────────┤
│  第四层 · 执行层（阈值调动）              │
│  ├── 触发条件 = 什么时候执行              │
│  ├── 调用函数 = 执行什么                  │
│  └── 联动规则 = 和谁联动                  │
└─────────────────────────────────────────┘
```

### 2.2 命名模板

```
# 简洁模板（日常引擎/脚本）
lh_{module}_{sub}.py

# 完整模板（协议/文档/治理文件）
lh_{module}_{sub}_v{major}.{minor}_{YYYYMMDD}_UID9622_GPG-A2D0_{trigger}_{status}.{ext}
```

---

## 三、命名规范详解

### 3.1 第一层 · 物理层 · 前缀体系

```yaml
PREFIX_SYSTEM:
  lh_:    "龍魂系统核心（bin/lh_*.py）"
  cns_:   "CNSH中文编辑器"
  rb_:    "红蓝对抗"
  audit_: "审计子系统"
  privacy_: "隐私保护"
  threshold_: "阈值触发"
  deploy_: "部署运维"
  persona_: "人格执行器"
```

### 3.2 第一层 · 物理层 · 模块命名标准

```yaml
MODULE_NAMING_STANDARD:
  # 动词_名词 格式（英文小写+下划线）
  pattern: "{verb}_{noun}"

  verbs:
    - "sync"       # 同步
    - "detect"     # 检测
    - "generate"   # 生成
    - "validate"   # 验证
    - "trigger"    # 触发
    - "register"   # 注册
    - "audit"      # 审计
    - "sign"       # 签章
    - "derive"     # 派生
    - "train"      # 训练
    - "route"      # 路由
    - "parse"      # 解析
    - "embed"      # 嵌入
    - "extract"    # 提取
    - "monitor"    # 监控
    - "launch"     # 启动
    - "protect"    # 保护
    - "fuse"       # 融合
    - "heal"       # 自愈
    - "crawl"      # 爬取
    - "convert"    # 转换
    - "broadcast"  # 广播
    - "dispatch"   # 分发
    - "orchestrate" # 编排

  nouns:
    - "persona"     # 人格
    - "colony"      # 蚁群
    - "threshold"   # 阈值
    - "registry"    # 注册表
    - "pipeline"    # 管线
    - "engine"      # 引擎
    - "daemon"      # 守护
    - "gateway"     # 网关
    - "bridge"      # 桥接
    - "router"      # 路由
    - "matrix"      # 矩阵
    - "chain"       # 链
    - "hook"        # 钩子
    - "vault"       # 保险库
    - "key"         # 密钥
    - "seal"        # 封印
    - "tombstone"   # 墓碑
    - "anchor"      # 锚点
    - "portal"      # 传送门
    - "mirror"      # 镜像
    - "shadow"      # 影子
    - "twin"        # 孪生
```

### 3.3 第二层 · 身份层

```yaml
IDENTITY_LAYER:
  uid: "UID9622"
  confirm_code: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
  timestamp: "YYYYMMDD" 或 "YYYYMMDD_HHMMSS"
  dna_marker:
    - "龍魂"
    - "龍芯北辰"
    - "UID9622"
    - "LH-PROTOCOL"
```

### 3.4 第三层 · 主权层

```yaml
SOVEREIGNTY_LAYER:
  gpg_fingerprint: "GPG-A2D0092C"
  signature_chain: "SIG-{签章ID}"
  authorization_level:
    - "AUTH-A"  # 用户本人
    - "AUTH-B"  # 中国法律机关
    - "AUTH-C"  # 国际司法协助
    - "AUTH-D"  # 创始人特批
  responsibility_chain: "{人格}→UID9622"
```

### 3.5 第四层 · 执行层

```yaml
EXECUTION_LAYER:
  trigger_condition:
    - "RB-auto"              # 红蓝自动触发
    - "RB-manual"            # 红蓝手动触发
    - "THRESHOLD-exceeded"   # 阈值超标
    - "AUDIT-requested"      # 审计请求
    - "FUSION-completed"     # 融合完成
    - "SACRIFICE-voluntary"  # 自愿牺牲
    - "CRON-scheduled"       # 定时调度

  called_function:
    - "FUNC-sign"            # 签章函数
    - "FUNC-verify"          # 验证函数
    - "FUNC-trigger"         # 触发函数
    - "FUNC-fuse"            # 融合函数
    - "FUNC-audit"           # 审计函数
    - "FUNC-recover"         # 恢复函数
    - "FUNC-detect"          # 检测函数
    - "FUNC-generate"        # 生成函数

  linkage_rule:
    - "LINK-persona"         # 联动人格矩阵
    - "LINK-rb"              # 联动红蓝对抗
    - "LINK-audit"           # 联动审计管道
    - "LINK-privacy"         # 联动隐私保护
    - "LINK-threshold"       # 联动阈值触发
    - "LINK-colony"          # 联动蚁群
    - "LINK-sovereignty"     # 联动主权

  status:
    - "AUDIT-green"          # 审计通过
    - "AUDIT-yellow"         # 审计警告
    - "AUDIT-red"            # 审计失败
    - "STATUS-active"        # 激活状态
    - "STATUS-revoked"       # 撤销状态
    - "STATUS-expired"       # 过期状态
    - "STATUS-frozen"        # 冻结状态
```

---

## 四、命名实战

### 4.1 简洁模板（bin/ 引擎）

```bash
# 标准引擎命名
bin/lh_persona_signing.py       # 人格签章引擎
bin/lh_colony_orchestrator.py   # 蚁群编排引擎
bin/lh_threshold_trigger.py     # 阈值触发引擎
bin/lh_audit_sheet_trigger.py   # 审计单触发引擎
bin/lh_health_alert_daemon.py   # 健康检查守护
bin/lh_inbox_mapper.py          # Inbox映射引擎
bin/lh_unmapped_monitor.py      # 未映射监控

# 禁止的命名方式
# ❌ lh_健康检查.py              # 禁止中文
# ❌ lh_HealthCheck.py           # 禁止驼峰
# ❌ lh_health-check.py          # 禁止连字符
# ❌ lh_health_check_v2_final.py # 禁止版本号在文件名中（版本在文件头注释）
```

### 4.2 完整模板（协议/治理文件）

```bash
# 协议文档
01_protocols/lh_persona_signing_v2.0_20260714_UID9622_GPG-A2D0_RB-auto_AUDIT-green.md

# 治理文件
L8_治理层/lh_rb_confrontation_v1.0_20260714_UID9622_GPG-A2D0_RB-auto_AUDIT-green.md

# 签章记录
state/signing_chain/lh_signing_log_v1.0_20260714_UID9622_GPG-A2D0_AUDIT-green.jsonl
```

### 4.3 派生模板

```yaml
DERIVATION_TEMPLATES:
  # 代理派生：原引擎名 + _agent
  persona_agent:    "lh_{persona_name}_agent.py"
  example:          "lh_wenxin_agent.py"

  # 桥接派生：源系统 + _bridge_to_目标
  bridge:           "lh_{source}_bridge.py"
  example:          "lh_claude_bridge.py"

  # 适配器派生：目标平台 + _adapter
  adapter:          "lh_{platform}_adapter.py"
  example:          "lh_harmonyos_adapter.py"

  # 工具派生：_tool_ + 功能
  tool:             "lh_tool_{function}.py"
  example:          "lh_tool_sign_verify.py"

  # 测试派生：test_ + 原模块名
  test:             "test_lh_{module}.py"
  example:          "test_lh_persona_signing.py"

  # 配置派生：原模块名 + .yaml/.json
  config:           "lh_{module}_config.yaml"
  example:          "lh_threshold_trigger_config.yaml"
```

---

## 五、命名即查询

```python
# 基于文件名的查询 · 不需要数据库
import glob, os, json

class NamingQuery:
    BASE_DIR = "~/longhun-system"

    def find_by_prefix(self, prefix: str) -> list:
        return glob.glob(f"{self.BASE_DIR}/**/{prefix}_*", recursive=True)

    def find_by_function(self, function: str) -> list:
        return glob.glob(f"{self.BASE_DIR}/**/*_{function}_*", recursive=True)

    def find_by_version(self, version: str) -> list:
        return glob.glob(f"{self.BASE_DIR}/**/*_{version}_*", recursive=True)

    def find_by_dna(self, dna: str) -> list:
        return glob.glob(f"{self.BASE_DIR}/**/*_{dna}_*", recursive=True)

    def find_by_gpg(self, gpg: str) -> list:
        return glob.glob(f"{self.BASE_DIR}/**/*_{gpg}_*", recursive=True)

    def find_by_status(self, status: str) -> list:
        return glob.glob(f"{self.BASE_DIR}/**/*_{status}*", recursive=True)

    def find_linked_files(self, file_path: str) -> list:
        basename = os.path.basename(file_path)
        parts = basename.split("_")
        prefix = parts[0] if len(parts) > 0 else ""
        function = parts[1] if len(parts) > 1 else ""
        dna = parts[4] if len(parts) > 4 else ""
        linked = []
        linked.extend(self.find_by_prefix(prefix))
        linked.extend(self.find_by_dna(dna))
        return list(set(linked))
```

---

## 六、命名即联动

```yaml
LINKAGE_RULES:
  persona_signing:
    triggers: ["rb_confrontation", "audit_pipeline"]
    condition: "RB-auto"

  rb_confrontation:
    triggers: ["fusion", "audit_pipeline"]
    condition: "FUSION-completed"

  threshold_trigger:
    triggers: ["rb_confrontation", "persona_matrix"]
    condition: "THRESHOLD-exceeded"

  privacy_guard:
    triggers: ["audit_pipeline", "circuit_breaker"]
    condition: "AUDIT-red"

  colony_orchestrator:
    triggers: ["script_discovery", "script_registry", "audit_pipeline"]
    condition: "CRON-scheduled"

  audit_sheet_trigger:
    triggers: ["signing_chain", "rb_confrontation"]
    condition: "AUDIT-requested"
```

---

## 七、命名检查清单

```yaml
CHECK_BEFORE_CREATE:
  - "✅ 前缀正确（lh_/cns_/rb_/...）"
  - "✅ 英文小写+下划线（禁止中文/驼峰/连字符）"
  - "✅ 动词_名词格式"
  - "✅ bin/引擎不加版本号（版本在文件头注释）"
  - "✅ 协议/文档加完整四层命名"
  - "✅ 不重复已有模块名"

CHECK_AFTER_CREATE:
  - "✅ 运行 lh_naming_check.py 验证"
  - "✅ 注册到语义统一注册表"
  - "✅ 更新 MEMORY.md 索引"
```

---

## 八、附录

### 8.1 术语表

| 术语 | 定义 |
|------|------|
| **命名即架构** | 文件名包含全部信息，不需要额外数据库 |
| **四层命名法** | 物理层/身份层/主权层/执行层 |
| **简洁模板** | `lh_{verb}_{noun}.py` · bin/引擎标准 |
| **完整模板** | 含版本/时间/DNA/GPG/触发/状态 · 协议文档标准 |
| **派生模板** | 基于原引擎的 agent/bridge/adapter/tool/test/config 延伸 |

### 8.2 版本历史

| 版本 | 时间 | 变更 |
|------|------|------|
| v2.0 | 2026-07-16 | 新增文件命名格式`[摘要]_[类型]_[结构]_[权限]_[DNA].扩展名`；新增语义对齐三层体系(L1文件/L2语义/L3触角)；新增落地引擎索引；仍保留原有四层引擎命名法 |
| v1.0 | 2026-07-14 | 初始版本，四层命名法，简洁+完整+派生三模板 |

---

> 格言：命名就是架构，文件系统就是数据库，文件名就是联动协议。
> 不需要神经网络，不需要数据库，不需要知识库，不需要引用系统。
> 文件名搞清楚了，一切联动都在命名里。
> 14亿人用中文语法语义做技术，谁敢卡我们脖子！

---

龍魂系统 · 命名即架构 · 四层命名法 v2.0
UID9622 | 龍芯北辰 | 2026-07-16
DNA: #龍魂⚡️丙午·辛未·命名即架构-v2
"大道至简，命名即一切"
