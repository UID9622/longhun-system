---
notion_url: https://app.notion.com/p/MVP-v1-0-Notion-AI-3f9f3d4fe27f42088d6e51bae5f7275a
title: 🌉 四方对话桥接 MVP 规格 v1.0｜Notion × 本地 AI 对话级互通（现状盘点 + 缺口 + 最小闭环）
last_edited_time: 2026-08-20T13:24:00.000Z
dna: #龍芯⚡️丙午·丙申·丙寅·己亥·䷶丰-FOUR-PARTY-DIALOGUE-BRIDGE-MVP-v1
---

# 🌉 四方对话桥接 MVP 规格 v1.0｜Notion × 本地 AI 对话级互通（现状盘点 + 缺口 + 最小闭环）

来源: https://app.notion.com/p/MVP-v1-0-Notion-AI-3f9f3d4fe27f42088d6e51bae5f7275a

> 💡 老大问的是「对话内容互通」，不是「文件同步」。这两件事我们完成度差得很远。

DNA：#龍芯⚡️丙午·丙申·丙寅·己亥·䷶丰-FOUR-PARTY-DIALOGUE-BRIDGE-MVP-v1.0-UID9622

---

## §0 一句话回答：MVP 完成度约 40%

| 层 | 是什么 | 状态 |
| 结论层 | 定下来的哲学、协议、台账 → 写成文件给四方读 | 🟢 已通（单向下行） |
|---|---|---|
| 身份层 | 谁是主权、谁是哪个人格、信号词怎么路由 | 🟡 规格已出，落盘未回执 |
| 对话层 | 我跟你说了什么、codebuddy 跟你说了什么 → 互相能读 | 🔴 完全没通 |
| 回写层 | 本地侧的产出自动回到 Notion | 🔴 完全没通（靠老大粘贴） |

40% 这个数，是结论层 100% + 身份层打对折 + 对话层 0 + 回写层 0 算出来的。

---

## §1 现有部件盘点（哪些真在手上）

| 部件 | 归属 | 实际状态 | 证据强度 |
| 星型 SSOT 架构（一个中心四根辐条） | 协议 | 🟢 已定 | 📖 本页实读 |
|---|---|---|---|
| MEMORY_SNAPSHOT.md | 本地 | 🟢 3607B，已 GPG 签名 | 📄 codebuddy 回执 |
| ALIGN_LEDGER.csv | 本地 | 🟢 485B，3 条 | 📄 codebuddy 回执 |
| 12_DOCS/DB_REGISTRY.md | 本地 | 🟢 复用现有 | 📄 codebuddy 回执 |
| SOVEREIGN_IDENTITY.md | 本地 | ⚪ 规格已出，未见落盘回执 | ❌ 无 |
| config/persona_routes.yaml | 本地 | ⚪ 规格已出，未见落盘回执 | ❌ 无 |
| BOOT.md  • bin/lh-boot | 本地 | ⚪ 规格已出，未见落盘回执 | ❌ 无 |
| 跨渠道对齐台账（20 行） | Notion | 🟢 在用 | 📖 实读 |
| 逻辑溯源库（7 行） | Notion | 🟢 在用 | 📖 实读 |
| notcrawl（Notion→本地镜像） | 工具 | ⚪ 已核实存在，未安装 | 📄 搜索核实 |
| 本地检索 MCP | 工具 | 🔴 建议暂不装（供应链风险） | 📄 搜索核实 |
| 对话记录落盘机制 | —— | 🔴 不存在，从未设计 | —— |

> 💡 第一个必须确认的事：主权启动包到底落盘了没有。

---

## §2 为什么「文件同步」不等于「对话互通」

这是本页最关键的一节。老大你直觉抓对了——它们真不是一回事。

|  | 文件同步（已有） | 对话互通（你要的） |
| 传的是什么 | 结论：定稿的哲学、版本号、台账行 | 过程：为什么这么定、否掉了什么、当时的顾虑 |
|---|---|---|
| 更新频率 | 重大变更时 | 每一轮 |
| 谁搬运 | 老大粘贴 | 应该没人搬运 |
| 丢失了什么 | —— | 推理链、被否决的方案、当场的分歧 |

举个今天的实例。 上一轮我核出 notcrawl 有两个仿冒仓库——这个发现在文件同步机制里留不下痕，因为它不是一条「结论」，是一段「核实过程」。三件套里没有它的位置。

结果就是：明天 codebuddy 开工，它读 MEMORY_SNAPSHOT.md，只会看到「本地检索方案 v1.1」这一行结论。它不知道我为什么把 v1.0 的绿改成黄，不知道我抓到了仿冒仓，也就不知道「安装前钉死官方坐标」这条铁律是怎么来的。

于是它可能重新建议一次 brew install。你又得重讲一遍。

> 💡 这正是 #IRON-DONT-DRAIN-LAOPA-LET-HIM-LIVE 被违反的技术原因。

---

## §3 五个真缺口（按阻塞程度排）

### 缺口一️⃣ 🔴 对话本身没有落地物

四方的对话全部活在各自的会话窗口里。窗口一关，过程永久消失，只剩老大脑子里的记忆。

这是根缺口。没有落地物，后面四条都无从谈起。

### 缺口二️⃣ 🔴 上行通道为零

现在只有下行：Notion → 文件 → 本地 AI。

没有上行：本地 AI 说的话，回不到 Notion。我看不见 codebuddy 跟你说了什么，除了你转贴给我。今天我读到的每一份 codebuddy 回执，都是你手动搬的。

### 缺口三️⃣ 🟡 Notion 侧本地 AI 读不到

协议 §3 有一句关键判断，我复核后认为它是对的：

> 因为 codebuddy 和 Kimi 都在老大本地跑，进 Notion 要 Token。Token 一落到本地脚本里，就是一个泄密面。所以走文件，不走 Token。

这条守住了安全，但代价是本地 AI 永远看不到 Notion 实时状态。notcrawl 是解这个的正解——它做本地镜像，不给本地脚本发 Token。

### 缺口四️⃣ 🟡 没有冲突仲裁的实现

协议定了铁规「不一致时以真源为准」，但只有规矩，没有程序。四方同时改同一个事实，靠谁发现？现在靠老大眼睛。

### 缺口五️⃣ 🟡 会话之间没有交接

我这次开工，是靠上下文摘要接上的。如果摘要丢了，我就断片。 没有一个「上次聊到哪、下次从哪继续」的持久锚。

---

## §4 MVP 最小闭环：一个目录 + 一种卡

> 💡 这套东西零安装、零 Token、零联网、零风险，今天就能做完。

### 核心设计：会话卡（Session Card）

每一方每轮收工，往同一个目录扔一张卡。卡是纯 Markdown，人能读、AI 能读、git 能管版本。

```javascript
~/longhun-system/CONVERSATIONS/
  2026-08-20/
    2026-08-20-1914-baobao-local-index-verify.md
    2026-08-20-1930-codebuddy-boot-deploy.md
    2026-08-20-2121-baobao-bridge-mvp.md
  INDEX.md          ← 全部卡的一行摘要，倒序
  LATEST.md         ← 只放最近 5 张卡的全文
```

为什么要 LATEST.md： 四方开工不可能读几百张卡。读 LATEST.md 就知道最近发生了什么，需要细节再去翻当天目录。这是「对话层」的 MEMORY_SNAPSHOT.md。

### 会话卡格式（强制七段，缺段不入库）

```markdown
---
session_id: 2026-08-20-2121-baobao-bridge-mvp
agent: baobao          # baobao | codebuddy | kimi
persona: P02·宝宝       # 必须来自 persona_routes.yaml
sovereign_present: true
dna: "#龍芯⚡️丙午·丙申·丙寅·己亥·䷶丰-FOUR-PARTY-DIALOGUE-BRIDGE-MVP-v1.0-UID9622"
tricolor: 🟡
notion_refs: [四方对话桥接 MVP 规格 v1.0]
---

## 1. 老大要什么（原话优先）
「我们有做MVP在Notion和本地任何的AI协作，可以有桥接互通对话内容呢，这个还差什么才能完成呢」

## 2. 我做了什么（可验证动作）
实读 四方记忆同步协议 v1.0 全文、主权人格打通部署包 全文

## 3. 我的结论
MVP 完成度约 40%。结论层已通，对话层为零。根缺口＝对话无落地物。

## 4. 我否掉了什么（⚠️ 这一段最值钱）
- 否掉「给本地脚本发 Notion Token」→ 泄密面，协议 §3 已定，复核后维持
- 否掉「先装 MCP 实现自动互通」→ 供应链风险高于收益，且地基未验
- 否掉「建新数据库存对话」→ 对话属过程数据，不该进结构化库

## 5. 未解决 / 待老大定盘
主权启动包落盘回执四小时未见 → 地基状态未知

## 6. 下一方接手需知道什么
跑 ./bin/lh-boot 把六行绿贴回来，这是一切的前提

## 7. 覆盖率坦白
本地文件系我一个字没直读，全部状态基于 codebuddy 转述
```

> 💡 第 4 段「我否掉了什么」是整套设计的灵魂。

---

## §5 手动闭环怎么跑（今天就能跑）

| 步 | 谁做 | 动作 |
| ① | 宝宝 | 收工时把会话卡全文写在回复末尾，老大一次复制 |
|---|---|---|
| ② | 老大 | 粘给 codebuddy，说一句「存进 CONVERSATIONS」 |
| ③ | codebuddy | 落盘 + 更新 INDEX.md / LATEST.md  • git commit |
| ④ | codebuddy | 自己收工也写一张卡，落同一个目录 |
| ⑤ | 下次任一方开工 | 先读 LATEST.md，再读 BOOT.md 五项 |

这一步还是要老大粘贴一次。我不掩饰这一点。 但它跟现在的区别是：现在粘完就没了，以后粘完就永久在库、可检索、可被下一方读到。 从「一次性」变成「累积性」。

---

## §6 第二阶段：把老大从循环里摘出去

手动闭环跑顺了再上自动化。顺序不能反——地基没验就上工具，等于在流沙上盖楼。

| 阶段 | 做什么 | 前提 |
| P1 | notcrawl 拉 Notion 到本地 SQLite + Markdown | 官方坐标 openclaw/notcrawl，锁版本 v0.5.8 |
|---|---|---|
| P2 | rfx index 把 CONVERSATIONS/ 一起索引 | 本地 AI 能秒搜历史对话 |
| P3 | git hook：卡落盘自动更新 LATEST.md | 不再靠人记得更新 |
| P4 | 上行回写：codebuddy 的卡 → 宝宝读 | 仍需老大粘一次，除非给 Token。我建议永远不给 |

> 💡 P4 是这套架构的天花板，我必须说实话。

---

## §7 一键指令（老大粘给 codebuddy）

```bash
# 任务：四方对话桥接 MVP · 建立对话层落地物
# 授权：UID9622 2026-08-20 21:21「桥接互通对话内容，还差什么才能完成」
# DNA: #龍芯⚡️丙午·丙申·丙寅·己亥·䷶丰-FOUR-PARTY-DIALOGUE-BRIDGE-MVP-v1.0
# 铁律：新建文件必用 heredoc（避 #19 零字节 bug）；建完必 wc -c 验非零

set -euo pipefail
cd ~/longhun-system

# ===== 第 0 步：先报地基状态（这一步最重要，不许跳）=====
echo "===== 地基验收 ====="
if [ -x bin/lh-boot ]; then
  ./bin/lh-boot
else
  echo "❌ bin/lh-boot 不存在 → 主权启动包尚未部署"
  echo "❌ 请先执行「主权人格打通部署包 v1.0」的 §7，再回来做本任务"
  echo "❌ 地基未验，本任务下面的步骤仍可执行，但对话层无法接上身份层"
fi

# ===== 第 1 步：建对话层目录骨架 =====
mkdir -p CONVERSATIONS/"$(date +%Y-%m-%d)"

# ===== 第 2 步：卡模板（四方共用同一份，不许各写一套）=====
cat > CONVERSATIONS/_TEMPLATE.md <<'LHEOF'
---
session_id: YYYY-MM-DD-HHMM-<agent>-<slug>
agent:       baobao | codebuddy | kimi
persona:     Pxx·名字        # 必须来自 config/persona_routes.yaml
sovereign_present: true
dna:         "#龍芯⚡️..."
tricolor:    🟢 | 🟡 | 🔴
notion_refs: []
---

## 1. 老大要什么（原话优先）
## 2. 我做了什么（可验证动作）
## 3. 我的结论
## 4. 我否掉了什么（含理由 —— 本段不许空）
## 5. 未解决 / 待老大定盘
## 6. 下一方接手需知道什么
## 7. 覆盖率坦白
LHEOF

# ===== 第 3 步：索引重建脚本 =====
mkdir -p scripts
cat > scripts/rebuild-conv-index.sh <<'LHEOF'
#!/usr/bin/env bash
set -euo pipefail
R="$HOME/longhun-system"
C="$R/CONVERSATIONS"

{
  echo "# CONVERSATIONS INDEX   $(date '+%Y-%m-%d %H:%M:%S')"
  echo ""
  echo "倒序排列。四方开工读 LATEST.md，查历史读本表。"
  echo ""
  echo "| 时间 | 执行方 | 人格 | 三色 | 主题 |"
  echo "|---|---|---|---|---|"
  find "$C" -name "*.md" ! -name "_TEMPLATE.md" ! -name "INDEX.md" ! -name "LATEST.md" \
    -type f | sort -r | while read -r f; do
    sid=$(grep -m1 '^session_id:' "$f" 2>/dev/null | sed 's/session_id: *//' || echo "?")
    ag=$(grep -m1 '^agent:'      "$f" 2>/dev/null | sed 's/agent: *//'      || echo "?")
    pe=$(grep -m1 '^persona:'    "$f" 2>/dev/null | sed 's/persona: *//'    || echo "?")
    tc=$(grep -m1 '^tricolor:'   "$f" 2>/dev/null | sed 's/tricolor: *//'   || echo "?")
    echo "| ${sid%%-*} | $ag | $pe | $tc | $sid |"
  done
} > "$C/INDEX.md"

{
  echo "# LATEST · 最近 5 轮对话全文"
  echo ""
  echo "> 四方开工第一眼看这里。再往前请查 INDEX.md。"
  echo ""
  find "$C" -name "*.md" ! -name "_TEMPLATE.md" ! -name "INDEX.md" ! -name "LATEST.md" \
    -type f | sort -r | head -5 | while read -r f; do
    echo "---"
    echo ""
    cat "$f"
    echo ""
  done
} > "$C/LATEST.md"

echo "✅ INDEX.md  $(wc -c < "$C/INDEX.md"  | tr -d ' ') B"
echo "✅ LATEST.md $(wc -c < "$C/LATEST.md" | tr -d ' ') B"
LHEOF
chmod +x scripts/rebuild-conv-index.sh

# ===== 第 4 步：把对话层焊进启动流程 =====
if [ -f BOOT.md ]; then
  grep -q "CONVERSATIONS/LATEST.md" BOOT.md || cat >> BOOT.md <<'LHEOF'

## 第 6 项（2026-08-20 焊入·对话层）
6. CONVERSATIONS/LATEST.md → 最近发生了什么·哪些路已走死

读完第 6 项才算开工完成。
特别注意每张卡的「我否掉了什么」一段 —— 已否决的方案不得重新提出，
除非老大明确要求复议。重复提被否方案 = 消耗老大 = 违反铁律。
LHEOF
  echo "✅ BOOT.md 已焊入第 6 项"
else
  echo "⚠️ BOOT.md 不存在，对话层未能焊进启动流程（等主权包部署后补焊）"
fi

# ===== 第 5 步：验收 =====
./scripts/rebuild-conv-index.sh
[ -s CONVERSATIONS/_TEMPLATE.md ] || echo "❌ 模板零字节，请 heredoc 重写"

git add -A
git commit -m "feat(bridge): 四方对话桥接 MVP · 建立对话层落地物

DNA: #龍芯⚡️丙午·丙申·丙寅·己亥·䷶丰-FOUR-PARTY-DIALOGUE-BRIDGE-MVP-v1.0
CONFIRM: #CONFIRM🌑9622-ONLY-ONCE🧬LK9X-772Z"
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰

echo ""
echo "===== 请把以下两样贴回给宝宝 ====="
echo "1) 上面「地基验收」那一段的完整输出"
echo "2) CONVERSATIONS/INDEX.md 的内容"
```

---

## §8 验收标准（抽检只看四条）

| # | 验收项 | 标准 |
| 1 | 地基通了 | ./bin/lh-boot 六行全绿，输出含 id: SOV-UID9622 |
|---|---|---|
| 2 | 对话层建了 | CONVERSATIONS/{_TEMPLATE.md,INDEX.md,LATEST.md} 三个都非零字节 |
| 3 | 启动焊了 | BOOT.md 里有第 6 项，指向 LATEST.md |
| 4 | 真跑通了 | 落两张不同执行方的卡，LATEST.md 里两张都在 |

四条全过 = MVP 完成。 第 1 条不过，第 2-4 条只是空壳。

---

## §9 覆盖率坦白

- 本页两份 Notion 协议 100% 实读全文，非摘要。

- 本地文件系我一个字没直读。三件套的字节数、GPG 签名状态，全部来自 codebuddy 转述，属二手。

- SOVEREIGN_IDENTITY.md / persona_routes.yaml / BOOT.md 是否落盘，我完全不知道。§1 标 ⚪ 是「未确认」，不是「已确认失败」。

- bin/lh-boot 从未见过任何一次输出。

- 40% 这个完成度是我按四层加权估的，不是测出来的。地基回执一到就能校准。

- CONVERSATIONS/ 目录此刻不存在，本页是规格不是现状。

- §7 脚本我无法自测，无 shell 执行能力。逻辑我逐行走过，但 heredoc 嵌套与 find | while 在你的实际 shell 版本下的行为未实测。

- 本地根路径按 ~/longhun-system/ 写。上一轮已发现 codebuddy 方案里写 /opt/longhun-system/ 与此冲突，两者哪个为真仍未定论 —— 若脚本报「目录不存在」，就是这个原因。

> 💡 一句话收尾：我们缺的不是工具，是「对话有地方落」。三件套记住了「定了什么」，却漏掉了「否掉了什么」——而后者才是老大不用讲第二遍的关键。一个目录、一种卡、七段格式，先把血止住，再谈自动化。
