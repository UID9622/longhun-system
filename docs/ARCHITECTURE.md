# 龍魂系统 · 多层架构全貌

> DNA: `#龍芯⚡️丙午·乙未·乙卯·巳时·需-L1-ARCH-DOC-v1.0`
> 确认: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
> 生成: 2026-07-10 · AI从系统自吸收·七层架构正本

---

## 层架总览

```
┌─────────────────────────────────────────────────┐
│  L0 神圣层  │ 宪法·永恒锁·AGENTS·33锚点          │  焊死·不可变
├─────────────────────────────────────────────────┤
│  L1 内核层  │ 核心引擎·DNA·注册·联动·三真空      │  引擎底座
├─────────────────────────────────────────────────┤
│  L2 技能层  │ 技能标准·自动补全·计算框架          │  shim入口
├─────────────────────────────────────────────────┤
│  L5 服务层  │ Web操作台·API·门户·桌面·财务        │  面向用户
├─────────────────────────────────────────────────┤
│  L6 集成层  │ 外部桥接·16+集成·Claude·内容主权   │  向外连接
├─────────────────────────────────────────────────┤
│  L7 数据层  │ 语义护盾·人格知识·归档·日志·爬虫   │  数据底座
├─────────────────────────────────────────────────┤
│  辅助层     │ bin工具·models模型·skills·docs     │  工具链
└─────────────────────────────────────────────────┘
```

---

## L0 · 神圣宪法层（焊死·不可变）

| 文件 | 大小 | 职责 |
|:---|:---|:---|
| `AGENTS.md` | 32KB | AI操作手册·33永恒锚点·意图路由·铁律 |
| `CLAUDE.md` | 4KB | Claude Code项目上下文·环境变量·工具链 |
| `CONSTITUTION.md.asc` | 833B | 系统宪法·GPG签名 |
| `P0_ETERNAL_LOCK.md.asc` | 833B | 永恒锁定·369不动点·三才 |
| `STANDARD.md.asc` | 833B | 标准文件 |

**锚点（33个 A-001 ~ A-033）**: 身份/算法/主权/时间/人格/审计/传承/经济/过滤/道引/登记/信任/原声/JSON真理/涉密结界

**意图→人格路由（30+意图域）**: 检查→P05 修复→P02 同步→P15 自动化→P15 部署→P14 算→P06 值不值得→P01 漏洞→P77 铁律→P00

---

## L1 · 内核层（1.2MB / 25文件）

```
L1_内核层/
├── longhun_core_engine.py      15KB  【核心引擎：JSON规则→三色审计→DNA追溯→执行】
├── longhun_voice_persona_router.py 28KB 【IPA人格→TTS音色映射】
├── three_vacuum_gateway_registry.json 7KB 【三真空区：通心听/通心语/嘿咕仓 双向映射】
└── kernel/
    ├── cross_module_registry.json  96KB 【跨模块联动依赖图·最大JSON】
    ├── algorithms/
    │   └── longhun-algorithms-cnsh-v1.0.md 32KB 【CNSH算法全集】
    ├── engines/                              【10个核心引擎】
    │   ├── cnsh_translator_engine.py     88KB 通心译v2.5
    │   ├── governance_engine.py          71KB 分层治理自愈v2.0
    │   ├── cnsh_editor_engine.py         69KB CNSH编辑器v2.5
    │   ├── daodejing_scene_engine_v2.md  28KB 道德经场景引擎
    │   ├── memory_compaction_engine.py   24KB 记忆压缩v1.0
    │   ├── hybrid_search_engine.py       22KB 混合检索v1.0
    │   ├── graceful_degradation_engine.py 21KB 优雅降级v1.0
    │   ├── audit_engine.py               20KB 审计引擎v1.0
    │   ├── memory_flush_engine.py        17KB Memory Flush
    │   ├── rule_engine.py                16KB 规则引擎v1.0
    │   └── yijing_engine.py              10KB 易经推演v0.1
    └── masters/  ⚠️存根（已迁移）
```

---

## L2 · 技能层（shim入口）

```
L2_技能层/skills/standards/skill-standards.integrated/
├── longhun-skill-auto-completion-engine.py  → skills/core/
└── longhun-standard-calculation-framework.py → skills/core/
```

实际技能实现分布在 `skills/` 目录（205文件/9.7MB）。

---

## L5 · 服务层（35MB / 283文件）

```
L5_服务层/services/
├── dashboard/web/           【Web操作台·多版本HTML】
│   ├── CNSH_龍魂操作台v4.0.html
│   ├── longhun_flow_portal_v2.html
│   ├── longhun-flow-field-v9.html
│   ├── longhun-luoshu-vortex-v2.html
│   ├── longhun-master-control.html
│   ├── longhun-unified-v9.html
│   ├── longhun-neural-network-3d-v1.html
│   ├── index.html / current.html
│   └── api/  【声影桥·DNA注册API】
├── desktop/desktop/         【Electron桌面端】
├── portal/                  【门户·流场可视化·身份】
│   ├── flow-viz/
│   ├── identity/
│   └── portal/
├── finance/                 【财务模块】
├── spider_net/              【蜘蛛网监控】
├── extensions/              【Kimi WebBridge扩展】
├── shared/fonts/            【共享字体】
└── api/                     【控制面板·DNA注册表API】
```

---

## L6 · 集成层（对外桥接）

```
L6_集成层/
├── claude_runtime_wrapper.py          9KB  Claude运行时包装
├── content_sovereignty_protocol_v2.1.py 36KB 内容主权协议
├── longhun_braket.py                  26KB 量子/经典混合桥
└── 龙魂系统_API接口完整实现_v1.0.py   29KB API完整实现

integrations/（144MB / 16+集成）
├── clipboard/      剪贴板集成
├── csdn/           CSDN博客同步
├── deepseek/       DeepSeek AI
├── fish_audio/     鱼声音频
├── gitcode/        GitCode代码托管
├── harmonyos/      鸿蒙OS·通心译
├── mcp/            MCP协议服务器
├── notion/         Notion知识库
├── qiaojie/        乔前辈自动化
└── wechat_public_account/ 微信公众号·小程序
```

---

## L7 · 数据层（719MB / 966文件）

```
L7_数据层/
├── semantic_shield/          【语义护盾·防火墙】
│   ├── semantic_firewall_master.json  涉密结界主配置
│   ├── 反语义注入黑名单.json/md
│   ├── 火气通心译对照表.json/md
│   └── 涉密语义库模板.json/md
├── persona_knowledge/        【人格知识库】
│   ├── P01_诸葛亮/  P02_张衡/
│   ├── P04_鲁班/    P06_镜像审计者/
├── desktop_archive/          【桌面归档】
│   ├── articles/ functions/ keys/
│   ├── loose_files/ screenshots/ subdir_snapshots/ videos/
├── desktop_media/            【桌面媒体·截屏+视频】
├── claude_extracted/          【Claude提取·raw/scanned/structured】
├── spider_net/               【蜘蛛网数据】
├── logs/                     【系统日志】
├── data/regulatory/           【法规数据】
├── handoff/                  【接力包】
├── memory_backups/           【记忆备份】
├── memory_packing/           【记忆打包】
├── eval_reports/             【评估报告】
├── daoyin/mirror/            【道引镜像】
├── auto_compressor/          【自动压缩】
├── auto_crawl_daemon/        【自动爬虫守护】
├── crawl_governor/           【爬虫治理】
├── root_fragment_index/      【根碎片索引】
├── strategy_reports/         【策略报告·含执行日志】
└── tombstone_vault/          【墓碑保险库】
```

---

## 辅助层

| 目录 | 文件数 | 大小 | 说明 |
|:---|:---|:---|:---|
| `bin/` | 162 | 3.6MB | 所有CLI工具·训练器·审计·DNA·爬虫·记忆·自动化 |
| `models/` | 18 | ~3GB | longhun-v1.0 LoRA·longhun Ollama |
| `skills/` | 205 | 9.7MB | 技能实现·跨平台·KG·红队·护盾·标签·通心译·审计 |
| `docs/` | 1370 | 200MB | cnsh-uid9622/dragon-soul-open-hub/laozi369/契约矩阵等 |
| `01_技能庫/` | 3 | 50KB | 宝宝人格HTML·曾仕强数字人·语义抽屉JSON |

---

## 外部扩展模块

| 目录 | 大小 | 说明 |
|:---|:---|:---|
| `voice-twin/` | 1.3GB | 真声克隆·TTS服务·语音数据集·声音孪生 |
| `voice-dna/` | — | 声纹锚定·身份印证·加密 |
| `baobao-guardian/` | — | 宝宝守护·前后端 |
| `android-auto/` | — | Android自动化 |
| `backend/` | — | 后端服务 |
| `xpay/` | — | 支付模块 |
| `龍魂洛书369引擎/` | — | 洛书369独立引擎 |
| `龍魂取证内核/` | — | 取证内核 |
| `人民维权助手/` | — | 维权工具 |
| `龙魂日记本-iOS/` | 12KB | iOS日记本 |
| `法律引擎/` | — | 法律引擎 |
| `统一入口/` | — | 统一入口 |
| `.龍魂/` | — | 运行时配置 |
| `03_后土OS/` | — | 后土OS·boot+kernel |
| `03_知識圖譜/` | — | 知识图谱 |
| `03_compiler/` | — | CNSH编译器 |

---

## 旧文件/备份清单（已压缩）

| 路径 | 原始大小 | 操作 |
|:---|:---|:---|
| `.git.bak-pre-clean-20260624104302/` | 2.7GB | → `.archive/git-bak-20260624.tar.gz` |
| `backups/` | 389MB | → `.archive/backups-20260701.tar.gz` |
| `agents/quarantine/` | — | → `.archive/agents-quarantine.tar.gz` |
| `.venv_longhun_math/` | 901MB | → 标记.gitignore（虚拟环境不归档） |
| `voice-twin/.venv-tts/` | ~500MB | → 标记.gitignore |

---

## 系统流场（数据流动方向）

```
外部输入（声音/文字/API）
    │
    ▼
心节点（三真空区：通心听·通心语·嘿咕仓）
    │
    ▼
骨节点（CNSH编译·翻译引擎·编辑器）
    │
    ├──► 眼节点（可视化·操作台·门户·3D）
    │
    ▼
门节点（签名·DNA·GPG·加密·出站）
    │
    ▼
外部输出（Notion/GitHub/Gitee/微信/鸿蒙）
```

---

> 此文档由AI从龍魂系统自吸收生成，每次架构变更后应更新。
> 归档旧文件存放于 `.archive/` 目录。
