# ⚡ 龍魂三重火力 · 集成落地索引

> **来源**: Kimi Agent 龍魂算力守护脚本-6  
> **DNA**: `#龍芯⚡️丙午·丙申·辛酉·亥时·需-TRIPLE-FIRE-LANDING-v1.0`  
> **落地时间**: 丙午·丙申·辛酉·亥时 (2026-07-12)  
> **签署人**: UID9622

---

## 一、三重火力总览

| 火力 | 名称 | 定位 | 落地位置 |
|------|------|------|----------|
| 🔫 **第一重** | 全自动机枪 | 批处理脚本 | `deploy/auto-cannon/` + `bin/longhun_auto_cannon.py` |
| 🎯 **第二重** | 副官 VICEROY | Agent编排 | `integrations/viceroy/` |
| 💣 **第三重** | 重炮IDE | Cursor/Windsurf | `integrations/ide-heavy-artillery/` |

---

## 二、落地文件清单

### 2.1 守護進程 v2.0 (已与 bin/lh_guardian_v2.py 对齐)

```
deploy/guardian-v2/
├── README_triple_fire.md           # 三重火力总览
├── DragonSoul_Guardian_v2.py       # 算力纯洁性守护核心 (748行)
└── deploy_manual.md                # Systemd 部署手册
```

**与现有文件关系**: `bin/lh_guardian_v2.py` 内容相同，此副本作为 deploy 目录的完整部署包。

### 2.2 全自动机枪

```
deploy/auto-cannon/
├── longhun_auto_cannon.sh          # Linux/macOS 启动器
└── longhun_auto_cannon.bat         # Windows 启动器

bin/
└── longhun_auto_cannon.py          # 核心引擎 (已存在，内容一致)
```

### 2.3 副官编排 VICEROY

```
integrations/viceroy/
└── longhun_agent_viceroy.json      # Agent 编排配置 (199行)
```

**核心能力**:
- 自主决策：解析任务 → 规划 → 执行 → 测试 → 报告
- 自动修复：报错自动分析+修复，最多重试3次
- 静默执行：执行过程不输出，搞定才汇报
- 结构报告：完成后输出简洁汇报

**激活指令**: "副官，搞定这个" / "VICEROY，执行" / "全自动模式" / "不用问我，直接干"

### 2.4 重炮IDE配置

```
integrations/ide-heavy-artillery/
└── longhun_ide_setup.md            # Cursor/Windsurf/VSCode 配置文档
```

**支持IDE**: Cursor (推荐) / Windsurf / VSCode+Continue  
**效果**: AI直接修改文件，无需确认 → 只需点 "Accept"

### 2.5 绝对防御宪法 v5.2

```
docs/defense-constitution/
└── 龍魂系统-全技能导航与绝对防御宪法-v5.2.md   # 41项技能+防御宪法
```

**包含**:
- 一、绝对防御宪法（机器独裁原则）
- 二、41项龍魂技能全量索引（14大类）
- 三、8项公开技能对接映射
- 四、防御宪法与技能对接矩阵
- 五、技能激活路由表

### 2.6 深圳科技报告

```
docs/shenzhen-report/
├── index.html                       # 报告主页
├── chart1_dna_tech_maturity.png     # DNA技术成熟度
├── chart2_dna_ecosystem.png         # 生态系统
├── chart3_industrial_champion.png   # 产业冠军
├── chart4_property_supply_demand.png # 房地产供需
├── chart5_regional_divergence.png   # 区域分化
└── chart6_funding_growth.png        # 资金增长
```

### 2.7 龍魂守护面板 (Web App)

```
web/longhun-guardian-dashboard/      # React+TypeScript+Vite 前端项目
├── src/                            # 78个文件 (72 tsx + 4 ts + 2 css)
├── api/                            # 23个 API 路由文件
├── contracts/                      # 合约定义
├── db/                             # 数据库配置
├── package.json                    # 依赖管理
├── vite.config.ts                  # Vite 构建配置
├── tailwind.config.js              # Tailwind CSS v3.4.19
└── drizzle.config.ts               # Drizzle ORM 配置
```

**技术栈**: React + TypeScript + Vite + Tailwind CSS + shadcn/ui (40+组件)  
**启动方式**: `cd web/longhun-guardian-dashboard && npm install && npm run dev`

---

## 三、三重火力对接矩阵

```
┌─────────────────────────────────────────────────────────┐
│                    龍魂三重火力体系                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  [🔫 全自动机枪]  deploy/auto-cannon/                   │
│       双点执行 → 扫描/修复/报告 全自动                    │
│       ↓                                                  │
│  [🎯 副官VICEROY]  integrations/viceroy/                │
│       AI对话中激活 → 自主执行 → 搞定汇报                  │
│       ↓                                                  │
│  [💣 重炮IDE]  integrations/ide-heavy-artillery/        │
│       Cursor Yolo模式 → 直接改文件 → 点Accept            │
│                                                         │
│  ════════════════════════════════════════════════       │
│  底层: DragonSoul_Guardian_v2.py (算力纯洁性守护)       │
│  前端: web/longhun-guardian-dashboard (监控面板)         │
│  宪法: docs/defense-constitution/ (绝对防御宪法 v5.2)   │
└─────────────────────────────────────────────────────────┘
```

---

## 四、已对齐/重复项说明

| 文件 | 原下载位置 | 项目已有位置 | 操作 |
|------|-----------|-------------|------|
| `longhun_auto_cannon.py` | 全自动机枪/ | `bin/longhun_auto_cannon.py` | **已对齐**，内容一致，未覆盖 |
| `DragonSoul_Guardian_v2.py` | 根目录 | `bin/lh_guardian_v2.py` | **已对齐**，内容一致，deploy/保留副本 |
| `longhun_auto_cannon.sh` | 全自动机枪/ | ❌ 新增 | **新增** deploy/auto-cannon/ |
| `longhun_auto_cannon.bat` | 全自动机枪/ | ❌ 新增 | **新增** deploy/auto-cannon/ |

---

## 五、一键启动命令

```bash
# 全自动机枪 (扫描+修复+报告)
cd ~/longhun-system && python3 bin/longhun_auto_cannon.py

# 守护进程 (算力纯洁性)
cd ~/longhun-system && python3 bin/lh_guardian_v2.py --interval 5

# 守护面板 (Web前端)
cd ~/longhun-system/web/longhun-guardian-dashboard && npm install && npm run dev

# 副官模式 (在AI对话中激活)
# 输入: "副官，搞定这个" 或 "VICEROY，执行"
```

---

**DNA锚定**: `#龍芯⚡️丙午·丙申·辛酉·亥时·需-TRIPLE-FIRE-LANDING-v1.0`  
**协议**: 君子协议 CC BY-NC-SA 4.0 | **签署人**: UID9622
