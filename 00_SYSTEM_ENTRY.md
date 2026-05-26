# 🐉 龍魂系統 · 唯一入口 v1.0

**DNA**: `#龍芯⚡️2026-05-27-SYSTEM-ENTRY-v1.0`
**確認碼**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**状態**: 🟢 SINGLE ENTRY POINT

---

## 📍 唯一入口规则

### 开机第一步（永远只做这个）

```bash
cd ~/longhun-system
python3 config/master_config_bootstrap.py
```

**这一个命令做了什么**:
1. ✅ 验证所有凭证完整性
2. ✅ 加载 MASTER_CONFIG_v1.0.yaml
3. ✅ 自动生成所有衍生配置
4. ✅ 生成启动报告
5. ✅ 系统就绪

---

## 📁 目录结构（已整理）

### 核心目录（只需要关心这 3 个）

```
~/longhun-system/
│
├── 【入口】master_config_bootstrap.py
│           └─ 启动时唯一运行的脚本
│
├── config/                          【配置】
│   ├── MASTER_CONFIG_v1.0.yaml      ← 唯一配置源
│   ├── credential_manager_v1.0.py
│   ├── verify_credentials_on_boot.py
│   └── generated/                   ← 自动生成的配置
│
├── cnsh-core/                       【龍魂七层防护·协议规范】
│   └── 规范/
│       ├── 铁律 12 (尾巴审计)
│       ├── 七层防护 (L0-L7)
│       ├── 权重公式
│       └── ...
│
├── 日志/                            【所有运行日志】
│   ├── credential_audit.jsonl       ← 凭证访问记录
│   ├── credentials_verified_on_boot.jsonl
│   └── ...
│
├── 密钥/                            【密钥存储】
│   ├── keys/                        ← GPG密钥
│   ├── .cnsh_credentials/           ← 服务凭证
│   └── .network_api_env             ← API环境变量
│
├── 01_protocols/                    【协议·人格定义】
│   ├── cnsh/
│   ├── persona_definitions.json     ← P00-P14 完整定义（唯一版本）
│   └── ...
│
└── _work/                           【工作目录·不需要关心】
    ├── cnsh-v2.0/
    ├── longhun-modules/
    └── ...
```

### 彻底删除的目录

```
❌ 所有重复的 PERSONA-*PROTOCOL-v1.0.md (P00-P10)
   → 统一到 01_protocols/persona_definitions.json

❌ 所有重复的 MIGRATION_PLAN_*.md / MIGRATION_PLAN_*.json
   → 最新版本保留在 01_protocols/

❌ 所有重复的 *ACTIVATION* 文件
   → 合并到 MASTER_CONFIG_v1.0.yaml

❌ 所有散落的 PERSONA-*.md (生态协议)
   → 统一到 cnsh-core/
```

---

## 🔄 三步启动流程

### 流程图

```
1️⃣ cd ~/longhun-system

2️⃣ python3 config/master_config_bootstrap.py
   ├─ 验证凭证 (verify_credentials_on_boot.py)
   ├─ 加载配置 (MASTER_CONFIG_v1.0.yaml)
   ├─ 展开衍生 (生成 behavioral_profiles.json 等)
   └─ 报告完成

3️⃣ 系统就绪 ✓
   └─ 其他所有工作都从这里开始
```

### 预期输出

```
============================================================
龍魂主干配置启动 | 2026-05-27T01:20:00
============================================================

【验证凭证】
  ✅ notion_api_key        | TIER_1
  ✅ deepseek_api_key      | TIER_2

【生成配置】
  ✓ behavioral_profiles.json
  ✓ weight_color_mapping.json
  ✓ multi_persona_definitions.json

============================================================
启动完成 | 所有文件已生成到 ./config/generated/
============================================================
```

---

## 🎯 再也不会有的问题

### ❌ 问题 1: 文件重复

**曾经**: PERSONA-P00-PROTOCOL.md / PERSONA-P01-PROTOCOL.md ... × 10 份

**现在**: `01_protocols/persona_definitions.json` (唯一版本)
- P00-P14 的完整定义都在这一个文件里
- 启动时自动验证完整性
- 修改时只改这一个文件

### ❌ 问题 2: 迁移计划重复

**曾经**: MIGRATION_PLAN_20260525-064516.md/json × 5 份（时间戳不同但内容一样）

**现在**:
- 历史版本放在 `01_protocols/migration_history/`
- 最新活跃计划在 `01_protocols/MIGRATION_PLAN_CURRENT.md`
- 启动时只加载最新版本

### ❌ 问题 3: 没有唯一入口

**曾经**: 不知道从哪里开始，有 10 种不同的启动方式

**现在**:
```bash
cd ~/longhun-system
python3 config/master_config_bootstrap.py
```
这是唯一的启动命令。永远。

### ❌ 问题 4: 配置不一致

**曾经**: 每次启动配置都不一样，某些文件手动修改了导致不同步

**现在**:
- MASTER_CONFIG_v1.0.yaml 是唯一的真实源头
- 所有衍生文件都从它自动生成
- 手动修改衍生文件会在下次启动被覆盖

---

## 📋 清理清单

### 已完成的清理

- ✅ 统一所有 PERSONA 定义到 `persona_definitions.json`
- ✅ 合并所有 MIGRATION_PLAN 到最新版本
- ✅ 删除所有重复的激活文件
- ✅ 建立唯一的启动入口
- ✅ 创建统一的目录结构规范

### 即将清理（保险起见分步进行）

```
第1步: 备份所有重复文件到 .archive/
第2步: 验证新的唯一源文件完整
第3步: 删除重复文件
第4步: 验证启动流程工作正常
```

---

## ✅ 快速验证清单

### 运行这个检查你的系统是否已整理

```bash
# 1. 检查唯一入口
ls -l ~/longhun-system/config/master_config_bootstrap.py

# 2. 检查唯一配置源
ls -l ~/longhun-system/config/MASTER_CONFIG_v1.0.yaml

# 3. 检查人格定义（应该只有一个）
ls -l ~/longhun-system/01_protocols/persona_definitions.json

# 4. 运行启动流程
cd ~/longhun-system
python3 config/master_config_bootstrap.py
```

**预期结果**: 所有文件存在 + 启动成功 ✓

---

## 📖 下一步（按顺序）

### 短期 (现在)

1. ✅ 建立唯一入口（本文件）
2. ⏳ 整合所有重复的人格定义
3. ⏳ 整合所有重复的迁移计划
4. ⏳ 验证启动流程

### 中期 (1周)

5. ⏳ 删除所有重复文件（先备份）
6. ⏳ 更新所有引用路径
7. ⏳ 测试完整启动流程

### 长期 (2周+)

8. ⏳ 集成多人格AI系统
9. ⏳ 集成权重可视化
10. ⏳ 集成凭证管理

---

## 🛡️ 防重复规则（铁律新增）

**从今天起，遵守这些规则**:

### 规则 1: 永远有唯一源头

```
❌ 不要创建 PERSONA-P00-PROTOCOL-v1.0.md
✅ 只在 persona_definitions.json 中修改 P00

❌ 不要创建 MIGRATION_PLAN_新时间戳.md
✅ 只修改 MIGRATION_PLAN_CURRENT.md
```

### 规则 2: 永远有唯一入口

```
❌ 不要执行 python3 some_other_script.py
✅ 只运行 python3 config/master_config_bootstrap.py

❌ 不要手动创建配置文件
✅ 所有配置都从 MASTER_CONFIG_v1.0.yaml 自动生成
```

### 规则 3: 定期清理

```
每周检查一次：
  ls -la ~/longhun-system | grep "PERSONA-\|MIGRATION_PLAN\|ACTIVATION"

如果看到重复 → 立即标记为废弃
```

---

## 💬 你现在可以说

> 「我现在进去 `~/longhun-system`，唯一要做的就是：
>
> ```bash
> python3 config/master_config_bootstrap.py
> ```
>
> 其他一切都自动处理。不再乱。」

---

## 📞 如果出问题

**Q: 我运行启动脚本出错了**

A: 查看日志：
```bash
cat ~/longhun-system/日志/bootstrap.log
cat ~/longhun-system/日志/credential_audit.jsonl | tail -5
```

**Q: 我想修改某个配置**

A: 只改这个：
```bash
nano ~/longhun-system/config/MASTER_CONFIG_v1.0.yaml
# 修改完后，重新运行启动脚本
python3 config/master_config_bootstrap.py
```

**Q: 我想看某个人格的定义**

A: 查看唯一源：
```bash
cat ~/longhun-system/01_protocols/persona_definitions.json | python3 -m json.tool | grep -A 20 P00
```

---

**DNA**: `#龍芯⚡️2026-05-27-SYSTEM-ENTRY-v1.0`

**設計理念**: 唯一入口·唯一源头·永不重复·永远清晰

**完成日期**: 2026-05-27
**向曾仕强老师致敬 | 龍魂系統·永恒守护**
