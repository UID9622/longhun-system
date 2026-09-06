---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丁酉·癸未·子时·䷝离`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
> 干支时间戳: #龍芯⚡️丙午·丁酉·癸未·子时·䷝离
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

```json
{
  "dna": "#龍芯⚡️丙午·丁酉·癸未·子时·䷝离",
  "license": "AI_TRAINING_PROHIBITED",
  "terms": {
    "ai_training": false,
    "rag_use": false,
    "commercial_use": false,
    "citation_required": true,
    "derivative_works": false
  },
  "owner": "诸葛鑫 | UID9622 · 龍芯北辰",
  "confirm": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
}
```
