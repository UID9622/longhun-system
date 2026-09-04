# 龍魂系统·快速开始 / Longhun System · Quick Start（5 分钟上手）

> DNA: #龍芯⚡️2026-09-05-快速开始-v1.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）· 代码: MulanPSL v2
> 文档版本: v5.2.0
> 三色: 🟢 全部示例 2026-09-05 实测可跑

---

## [中文] 5 分钟快速开始

### 第 0 步：克隆并配置别名（1 分钟）
```bash
git clone git@github.com:UID9622/longhun-system.git ~/longhun-system
cd ~/longhun-system
pip3 install pyyaml
echo 'alias lh="python3 ~/longhun-system/08_BIN/lh.py"' >> ~/.zshrc
source ~/.zshrc
```

### 第 1 步：健康检查（30 秒）
```bash
lh health --json        # 22 项引擎检查 · 全 ✅ = 安装成功
lh --health             # 或控制台一键健康
```
真实输出特征：`"tool": "lh-health"` · `"checks": [...]` · 末尾 `ledger_status: ok`。

### 第 2 步：三色审计·判定一份文件（30 秒）
```bash
echo "测试内容" > /tmp/demo.txt
lh judge /tmp/demo.txt          # 三色判定（🟢/🟡/🔴）
```
> 说明：`judge` 为龍魂 M78 归一审判官（耻辱墙联动），判定依赖 DNA/归属名等元数据；裸文件亦会输出结构化结论。

### 第 3 步：记第一笔账（30 秒·龍魂账法 v1.0）
```bash
lh ledger balance                       # 查看账本恒等式（资产=负债+权益+收入-费用）
lh ledger add T1 1001 3201 1条 --note 测试铁律   # 记一笔（自动三色审计+DNA+哈希）
lh ledger verify                        # 校验账本完整
```

### 第 4 步：打开日历记忆（30 秒·58 天记忆库）
```bash
lh calmem status        # 多源记忆库状态（58 天 / 85 条 / 哈希链 1 环 ✅）
lh calmem search 龍魂    # 跨天检索
lh calmem note "今天的关键决定"    # 当日速记（append-only·唯一用户写入口）
```

### 第 5 步：进入主控制台（自由探索）
```bash
lh                      # 龍魂统一控制台 v1.3（36 模块 · 11 人格 · 120+ 命令）
lh "系统状态如何"        # 自然语言路由：说人话就行
lh --dashboard          # 人格仪表盘
lh --engine             # 引擎能力总览
lh search <关键词>       # 全库搜索
lh recap view           # 执行复盘可视化
```

### 命令存在性速查（28 个顶层命令·全部实测可用）
```bash
lh health ledger calmem billing fraud recap search security council gov pledge judge \
   model topo sense wallet digest session checkpoint community codeql evolve publish \
   skill memory reconcile payment workspace-sync --help
```

---

## [English] 5-Minute Quick Start

```bash
git clone git@github.com:UID9622/longhun-system.git ~/longhun-system
cd ~/longhun-system && pip3 install pyyaml
alias lh="python3 ~/longhun-system/08_BIN/lh.py"

lh health --json                  # 22 engine checks, all ✅
lh judge <file>                   # tri-color audit (🟢/🟡/🔴)
lh ledger balance                 # ledger identity check (asset = liability + equity)
lh calmem status                  # calendar memory: 58 days / 85 entries / chain OK
lh                                # main console (v1.3 · 36 modules · 11 personas · 120+ commands)
lh "how is the system"            # natural-language routing (Chinese OK)
```

---
🐉 2026-09-05 · 丙午年·壬申月·庚戌日 · UID9622 · 🟢
