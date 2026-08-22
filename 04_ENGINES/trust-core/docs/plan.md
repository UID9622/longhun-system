# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-64879f7d
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# plan.md — 龍魂 · 事实校验引擎 + 自愈系统 落地交付

## 需求源（参考来源①）
- 上传文件：user_pasted_clipboard_long_content_as_file_我想告诉你一下哈，为什么系统每个 AI.txt
- 核心事件：用户2008年退伍，2026年仍说"退伍16年"，系统从未纠错 → 暴露系统无主动事实校验机制
- 升级诉求：代码出错谁来修 → 自愈闭环（检测→分析→修复→验证→回滚）
- 终态要求：用系统落地、用数字落地、用计算公式落地，不要概念

## 焊死协议（来自既有约定，本轮必须遵守）
1. 补全模板 v1.0 十大类过堂：A口径 / B算法实证 / C安全 / D合规 / E诚实边界 / F工程完整 / G运维 / H结构风格 / I落地清单 / J场景生态
2. 实战交付三大件：①参考来源 ②优化了什么 ③没考什么（🟡待验 / 🔴缺口，不许藏）
3. 模板引擎焊死格式：/mnt/agents/output/龍魂智能模板引擎/template_engine.py 存在则走 validate 核验；缺区块🔶占位不删除
4. DNA 口径：禁手写干支；本地生成器 bin/lh_dna_generator.py 存在则调用，不存在一律 v3.0 日期占位
5. 三色分级：🟢已实测 / 🟡设计预期 / 🔴缺口；退出码 0/1/2
6. 回复固定三段：修正了什么 / 保留了什么 / 实测了什么
7. 诚实边界：mock 必标、未实测标🟡、机器不替人答价值观

## 阶段设计

### Stage 0 — 环境核验
- 检查 template_engine.py、lh_dna_generator.py 是否存在
- 检查 python3 / pytest 可用性
- 决定 DNA 生成路径（生成器调用 vs 日期占位）

### Stage 1 — 引擎实现（skill: vibecoding-general-swarm）
交付物结构（自包含 Python 包，macOS M4 Max 目标环境）：
```
longhun-trust-core/
├── longhun_trust/
│   ├── __init__.py
│   ├── dna.py            # DNA生成（生成器优先/日期占位兜底，禁手写干支）
│   ├── audit.py          # 史官 jsonl 日志
│   ├── factcheck.py      # 事实校验引擎：时间/身份/数字一致性 + 可信度公式 + 三级纠正
│   ├── credibility.py    # 可信度计算 C=0.4F+0.3S+0.3K，阈值0.7
│   └── selfheal.py       # 自愈引擎：检测→分析→修复→验证→回滚→耻辱墙
├── tests/                # pytest 锚点断言
├── scripts/
│   ├── install.sh        # macOS 一键部署（launchd）
│   └── com.longhun.selfheal.plist
├── docs/交付说明.md
└── README.md
```
关键修正点（相对原草稿）：
- 原草稿 validate_time 硬编码 `if years != 16` → 改为通用断言 actual==claim
- 原草稿 DNA 手写干支「丙午·丙申·癸亥·午时」→ 🔴违规，改生成器/占位
- 原草稿 self_heal 修复脚本是空壳（只 echo）→ 补真实修复策略表 + 干跑模式 + 人工审批闸门
- 原草稿无测试 → 补 pytest 锚点断言
- 原草稿 launchd 路径硬编码用户名 → 改 $HOME 动态生成
- 自愈引擎加确认码闸门（C安全：破坏性操作需确认码）
- 回滚 git reset --hard HEAD^ 危险 → 改 tag 快照回滚 + 干跑默认

### Stage 2 — 算法实证（B类）
- pytest 全量真跑，锚点断言：
  - 2008退伍+2026当前 → 必须报18年并触发纠正（复现老大案例）
  - 可信度公式数值断言
  - 熔断阈值断言
  - 自愈引擎干跑模式断言（不真改文件）
- 记录真实运行输出作为🟢证据

### Stage 3 — 运维层（G类）
- install.sh（launchd 守护，开机自启）
- 回滚机制、监控日志路径、QA 清单
- 沙盒不可实测项标🟡（launchd 需真机 macOS）

### Stage 4 — 交付
- 走模板引擎格式（存在则 validate）
- 打包 zip → /mnt/agents/output/
- 三段式报告：修正了什么 / 保留了什么 / 实测了什么 + 未验证备注
