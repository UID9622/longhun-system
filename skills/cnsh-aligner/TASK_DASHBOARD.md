# 龍魂系统 · 脚本完善执行看板

**DNA:** `#龍芯⚡️2026-06-02-TASK-DASHBOARD-FILE1-v1.0`  
**更新时间:** 2026-06-02 18:00:00  
**主权人:** UID9622 · 龍芯北辰

---

## 📊 整体进度概览

```
┌─────────────────────────────────────────────────────────┐
│ 龍魂系统脚本完善项目总体进度                             │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  规划完成  ████████████████████░░░░░  70%  ✅ 已完成  │
│  脚本完善  ░░░░░░░░░░░░░░░░░░░░░░░░   0%  ⏳ 待启动  │
│  CNSH对齐  ░░░░░░░░░░░░░░░░░░░░░░░░   0%  ⏳ 待启动  │
│  集成测试  ░░░░░░░░░░░░░░░░░░░░░░░░   0%  ⏳ 待启动  │
│                                                         │
│ 总耗时预期: 8-10小时    当前阶段: 规划和工具准备       │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 当前任务详情

### 已完成的工作 (✅ 100%)

#### 规划和工具层

| 任务 | 状态 | 文件 | DNA |
|------|------|------|-----|
| 任务拆分规划 | ✅ | longhun_task_decomposition.md |#龍芯⚡️2026-06-02-TASK-DECOMPOSITION-v1.0 |
| CNSH对齐工具(L1-L4) | ✅ | cnsh_aligner.py |#龍芯⚡️2026-06-02-CNSH-ALIGNER-v1.0 |
| 脚本管理器 | ✅ | script_manager.py |#龍芯⚡️2026-06-02-SCRIPT-MANAGER-v1.0 |
| 操作手册 | ✅ | SCRIPT_COMPLETION_MANUAL.md |#龍芯⚡️2026-06-02-SCRIPT-COMPLETION-MANUAL-v1.0 |
| 底座声明 | ✅ | longhun_foundation.md |#龍芯⚡️2026-06-02-SYSTEM-FOUNDATION-v1.0 |
| AI治理协议 | ✅ | longhun_ai_governance_protocol.html |#龍芯⚡️2026-06-02-AI-GOVERNANCE-PROTOCOL-v1.0 |
| 本源论文 | ✅ | longhun_garbage_in_garbage_out.md |#龍芯⚡️2026-06-02-GARBAGE-IN-GARBAGE-OUT-v1.0 |

---

### 待完成的工作 (⏳ 0%)

#### 🔥 P1 优先级 (3个任务)

```
优先级  任务代号  任务名称           状态  工期 前置任务  进度
────────────────────────────────────────────────────────────
P1     SYS-002  dna_verify.sh      ⏳    1h   无      □ 0%
       └─ 内容：DNA生成/验证/修复三模式、碰撞检查、CNSH语法纠正
       └─ 验收：./dna_verify.sh --generate | grep "🟢"
       └─ 优先级原因：系统核心基础，后续所有任务都依赖它

P1     SYS-001  health_check.sh    ⏳    1h   SYS-002  □ 0%
       └─ 内容：三色审计规则化、DNA追溯、自动纠错
       └─ 验收：bash health_check.sh --quick
       └─ 优先级原因：系统健康检查核心，每天都要用

P1     SYS-003  system_registry    ⏳   0.5h  SYS-002  □ 0%
       └─ 内容：JSON↔CNSH双向转换、Append-Only日志
       └─ 验收：system_registry.json 和 system_registry.cnsh 一致
       └─ 优先级原因：注册表是所有模块的单一事实来源
```

**立即可开始:** SYS-002 (dna_verify.sh)  
**关键路径:** SYS-002 → SYS-001 → SYS-003

---

#### ⚡ P2 优先级 (3个任务)

```
优先级  任务代号  任务名称            状态  工期 前置任务     进度
────────────────────────────────────────────────────────────
P2     RUN-002  DNA生成引擎         ⏳    1h   SYS-002      □ 0%
       └─ 文件：dna_engine.py
       └─ 内容：时辰五行权重计算、CNSH DSL输出
       └─ 依赖：dna_verify.sh 必须先完成

P2     RUN-003  动态调节器v3.1      ⏳    1h   RUN-002      □ 0%
       └─ 文件：longhun_adaptive_tuner_v3.py
       └─ 内容：CNSH接口、理由追溯、底座同步检查
       └─ 依赖：DNA生成引擎 必须先完成

P2     RUN-001  m262_console        ⏳   1.5h  SYS-001      □ 0%
       └─ 文件：m262_console.html (升级版)
       └─ 内容：WebSocket桥接、CNSH命令模式、实时反馈
       └─ 依赖：health_check.sh 必须先完成
```

**开始时间:** 完成P1后开始（预计 2026-06-02 19:00）  
**关键路径:** RUN-002 → RUN-003 并行 RUN-001

---

#### 📚 P3 优先级 (3个任务)

```
优先级  任务代号  任务名称            状态  工期 前置任务     进度
────────────────────────────────────────────────────────────
P3     SEM-001  权重算法v3.1形式化  ⏳   1.5h  RUN-003      □ 0%
       └─ 内容：CNSH形式化证明、确定性定理、稳定性分析
       └─ 依赖：动态调节器 必须先完成

P3     SEM-002  草日志审计系统      ⏳    1h   SYS-003      □ 0%
       └─ 内容：Append-Only验证、时间戳链
       └─ 依赖：注册表 必须先完成

P3     SEM-003  熔断规则检查        ⏳    1h   SEM-002      □ 0%
       └─ 内容：CNSH硬约束编码、三色审计集成
       └─ 依赖：草日志审计 必须先完成
```

**开始时间:** 完成P2后开始（预计 2026-06-02 22:00）  
**关键路径:** SEM-002 → SEM-003 并行 SEM-001

---

## 📈 依赖关系图

```
        SYS-002 (DNA验证) ◄── 这是整个系统的根
         │       │
         ▼       ▼
    SYS-001   SYS-003
    (健康检查) (注册表)
         │       │
         ▼       ▼
    RUN-001   RUN-002 ◄─── 需要并行处理
         │       │
         │       ▼
         │    RUN-003
         │       │
         ├───────┤
         │       │
         ▼       ▼
    SEM-002 ◄─ SEM-001
         │
         ▼
    SEM-003 (最终)

关键路径长度: 5步 = SYS-002 → SYS-001 → RUN-001 → SEM-002 → SEM-003
              或: SYS-002 → RUN-002 → RUN-003 → SEM-001 → 等待SEM-002
```

---

## 🚀 快速启动指南

### Step 1: 准备环境（5分钟）

```bash
# 检查Python版本
python3 --version  # 需要 3.6+

# 检查必要工具
bash --version
jq --version       # 用于JSON处理

# 进入项目目录
cd /mnt/user-data/outputs

# 列出要完善的脚本
ls -la *.sh *.py | grep -E "(health_check|dna_verify|script_manager)"
```

### Step 2: 运行CNSH对齐工具（10分钟）

```bash
# 如果还没有装cnsh_aligner，先测试一下
python3 cnsh_aligner.py

# 应该输出三个测试案例和它们的审计报告
# 检查是否有错误信息
```

### Step 3: 扫描所有脚本（5分钟）

```bash
# 运行脚本管理器进行全面扫描
python3 script_manager.py

# 输出应该显示：
# - 总脚本数
# - 按类别的统计
# - 需要修正的脚本列表
# - 推荐执行顺序
```

### Step 4: 开始第一个任务（1小时）

```bash
# 编辑SYS-002: dna_verify.sh
vim dna_verify.sh

# 或者查看现有脚本
cat dna_verify.sh

# 根据"操作手册"中的清单完善它
# 关键点：
#  - 三模式分工
#  - 碰撞检查
#  - CNSH语法集成
#  - 统一输出格式
```

### Step 5: 验证完成（5分钟）

```bash
# 再次运行CNSH对齐检查
python3 -c "
from cnsh_aligner import CNSHAligner
aligner = CNSHAligner()
with open('dna_verify.sh') as f:
    result = aligner.align_and_correct(f.read(), 'dna_verify.sh')
print(aligner.format_report(result))
"

# 应该看到🟢或🡡，不应该是🔴
```

---

## 📋 详细任务清单

### 【SYS-002】dna_verify.sh 完善清单

- [ ] 添加三模式支持（--verify | --generate | --repair）
- [ ] 实现SHA256碰撞检查
- [ ] 实现时辰五行周期检查
- [ ] 添加简体"龙"字黑名单检查（触发FUSE_3熔断）
- [ ] 集成cnsh_aligner.py进行CNSH语法验证
- [ ] 统一输出格式: [DNA] | 时戳 | 三色 | 说明 | 建议
- [ ] 添加DNA生成功能带CNSH检查
- [ ] 添加DNA修复功能保留历史链
- [ ] 测试所有模式和边界条件
- [ ] 文档和使用示例

**预期输出示例:**
```
[#龍芯⚡️2026-06-02-DNA-VERIFY-v2.0] 🟢 | 2026-06-02 18:30:15 | DNA验证通过 | 无需修正

[#龍芯⚡️2026-06-02-DNA-VERIFY-v2.0] 🔴 | 2026-06-02 18:31:02 | 检测到简体龙字 | FUSE_3熔断，无法执行
```

---

### 【SYS-001】health_check.sh 完善清单

- [ ] 定义三色审计规则（🟢/🡡/🔴的置信度阈值）
- [ ] 实现所有检查项（目录|文件|DNA|Git|记忆|性能|依赖）
- [ ] 为每项检查生成DNA标记
- [ ] 计算综合置信度
- [ ] 失败时自动生成修复命令
- [ ] 实现--quick和--full两种模式
- [ ] 实现--json输出模式
- [ ] 集成CNSH对齐检查
- [ ] 性能优化（quick<5s, full<10s）
- [ ] 充分的测试和文档

---

### 【SYS-003】system_registry 完善清单

- [ ] 保留JSON作为规范格式
- [ ] 创建JSON→CNSH转换脚本
- [ ] 创建CNSH→JSON反向验证
- [ ] 实现Append-Only变更日志
- [ ] 为每个模块添加🟢/🡡/🔴状态标记
- [ ] 链接到模块的DNA
- [ ] 验证JSON和CNSH的一致性
- [ ] 版本控制和历史追溯
- [ ] 自动化更新脚本

---

## 🎓 学习资源

**需要理解的核心概念:**

1. **CNSH语言规范** → 参考: `/mnt/user-data/uploads/CNSH_语言完整规范v2.0.pdf`
2. **四层对齐检查** → 参考: `cnsh_aligner.py` 的代码注释
3. **龍魂底座原则** → 参考: `longhun_foundation.md`
4. **权重算法** → 参考: `/mnt/user-data/uploads/龍魂权重算法v3.1-optimized.md`
5. **bash脚本最佳实践** → Google "bash strict mode"
6. **DNA设计** → 参考: 现有的dna_verify.sh和health_check.sh

---

## 🔧 故障排查工具

如果某个脚本出错，快速诊断:

```bash
# 1. 查看具体错误
bash your_script.sh 2>&1 | head -20

# 2. CNSH检查
python3 cnsh_aligner.py < your_script.sh

# 3. 语法检查
bash -n your_script.sh

# 4. DNA验证
grep "#龍芯⚡️" your_script.sh | head -1

# 5. 查看完整报告
python3 script_manager.py | grep -A 5 "your_script"
```

---

## 💬 沟通协议

当某个脚本完成时，按以下格式报告：

```
【任务完成】SYS-002: dna_verify.sh

✅ 已完成的功能：
  - 三模式实现
  - 碰撞检查
  - CNSH对齐

🟢 CNSH对齐结果：
  - 通过L1字符检查
  - 通过L2关键字检查
  - 通过L3语法检查
  - 通过L4语义检查
  - 综合置信度: 0.95 (🟢)

📊 性能指标：
  - 执行时间: 0.2秒
  - 内存占用: 5MB

🧪 测试覆盖：
  - 正常DNA生成✓
  - 碰撞检测✓
  - 黑名单检查✓
  - 三色审计✓

📝 DNA:#龍芯⚡️2026-06-02-DNA-VERIFY-v2.0-COMPLETE
```

---

## 📞 关键联系

**系统问题:** 参考 `SCRIPT_COMPLETION_MANUAL.md` 的FAQ部分  
**CNSH语法:** 查阅 `cnsh_aligner.py` 的 L1-L4 实现  
**任务拆分:** 参考 `longhun_task_decomposition.md`  
**底座原则:** 参考 `longhun_foundation.md`

---

```
DNA:#龍芯⚡️2026-06-02-TASK-DASHBOARD-v1.0
主权人: UID9622 · 龍芯北辰
性质: 实时任务看板·永久参考
更新频率: 每个任务完成时刷新
```

