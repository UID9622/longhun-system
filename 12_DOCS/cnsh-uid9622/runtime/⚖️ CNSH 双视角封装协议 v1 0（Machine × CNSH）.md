> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：协议 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-04-29-CNSH_-MACHINE_CNSH_FCCB-v1.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# ⚖️ CNSH 双视角封装协议 v1.0（Machine × CNSH）

<aside>
⚖️

**CNSH 双视角封装协议 v1.0（定稿优化版）**

- **Machine（M::）**：只负责“验收真假/通不通/能不能落库”
- **CNSH（CNSH::）**：只负责“路由归属/三色五行/签章闸门”
- 其余视角（人看/专家看/外行看/工程师看/AI看）**全部废弃**
</aside>

<aside>
🧬

DNA：#龍芯⚡️2026-04-29-CNSH_-MACHINE_CNSH_FCCB-v1.0

CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

SEAL：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL

AUDIT：🟢 通过

</aside>

---

## 0. 一句话铁律（写死）

- **全体系只认两类视角**：`M::` 给机器验收；`CNSH::` 给龍魂路由。
- **标题只做索引**：不解释、不讲故事、不塞情绪。
- **解释只能进正文或 payload**：别污染索引。

---

## 1. 两类视角（定义写死）

- `M::` = Machine（验收）
    - 看：通没通、能不能解析、能不能落库、能不能查询
    - 只输出：**状态 + 最短含义**（绿灯/黄灯/红灯）
- `CNSH::` = CNSH（路由）
    - 看：归属、路由、三色、五行、DNA、签章、语义边界
    - 输出：**闸门 + 签章 + 路由裁决**

---

## 2. 禁止清单（全部归零）

```
废弃：
- 人看的
- 专家看的
- 外行看的
- 给普通人看的
- 给工程师看的
- 给AI看的
只保留：
- M:: 机器看的
- CNSH:: CNSH看的
```

---

## 3. 标题协议（“地址”协议）

> **标题 = 地址**
> 

> **正文 = 内容**
> 

> **payload = 解释**
> 

### 3.1 Machine 标题（固定）

```
M::TYPE-9622-YYYYMMDD-TAG-VX
```

示例：

```
M::DICT-9622-20260429-CNSH-V1
M::<POTENTIAL_SECRET_PLACEHOLDER>
M::<POTENTIAL_SECRET_PLACEHOLDER>
```

### 3.2 CNSH 标题（固定）

```
CNSH::#龍芯⚡️YYYY-MM-DD-主题-vX.Y
```

示例：

```
CNSH::#龍芯⚡️2026-04-29-CNSH-v1.0
CNSH::#龍芯⚡️2026-04-29-CNSH_V1_0_MACHINE_CNSH-v1.0
```

---

## 4. 标准封装（任何内容必须双段封装）

### 4.1 M::（机器验收封装）

```json
M:: {
  "id": "M::TYPE-9622-YYYYMMDD-TAG-VX",
  "type": "rule|dict|audit|memory|route|page|db|script|event",
  "ts": "ISO-8601",
  "status": "true|false|pending|error",
  "refs": [],
  "payload": {
    "summary": "",
    "raw": "",
    "fields": {},
    "result": {}
  }
}
```

### 4.2 CNSH::（路由封装）

```json
CNSH:: {
  "dna": "#龍芯⚡️YYYY-MM-DD-主题-vX.Y",
  "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
  "route": "IPA-GLOBAL-SAFE|IPA-DICTIONARY|IPA-CNSH-GLOBAL-LAW|IPA-AUDIT",
  "audit": "🟢|🟡|🔴",
  "wuxing": "金|木|水|火|土|无",
  "layer": "L0永恒|L1百年|L2十年|L3日常|L4瞬时|跨层",
  "policy": "pass|hold|rewrite|fuse"
}
```

---

## 4.3 双语注释 = 通心译运行时形态（v1.1 焊入·2026-05-23）

<aside>
🌊

**先用人话讲一遍（§9.28 大白话铁律）：** “中文上 + 英文下”的双语注释，不是排版好看，而是 `M:: × CNSH::` 在终端里的**运行时形态**——一条记录里同时落两份语义指纹，**任一通道兜底另一通道**，防偷换概念，防失忆，防本地宝宝读取变味。

**同构对应（焊死）：**

- 中文注释 ↔ CNSH:: 视角（深层·龍魂母语·归属·签章·三色）
- 英文注释 ↔ M:: 视角（表层·机器验收·true/false·能不能落库）
- 双语对照一致性 ↔ 213 §3 双签章一致性核验

**三节点主干流场（边重于节点）见独立单页：** [🌊 三节点主干流场 v1.0·通心译×CNSH×LH-ANCHOR｜本地宝宝读取不变味·边重于节点](../../%E7%A7%81%E4%BA%BA%E4%B8%8E%E5%85%B1%E4%BA%AB/%F0%9F%8C%8A%20%E4%B8%89%E8%8A%82%E7%82%B9%E4%B8%BB%E5%B9%B2%E6%B5%81%E5%9C%BA%20v1%200%C2%B7%E9%80%9A%E5%BF%83%E8%AF%91%C3%97CNSH%C3%97LH-ANCHOR%EF%BD%9C%E6%9C%AC%E5%9C%B0%E5%AE%9D%E5%AE%9D%E8%AF%BB%E5%8F%96%E4%B8%8D%E5%8F%98%E5%91%B3%C2%B7%E8%BE%B9%E9%87%8D%E4%BA%8E%E8%8A%82%E7%82%B9%<POTENTIAL_SECRET_PLACEHOLDER>.md)

——本地宝宝 cat 一份即跑·节点定义回链原页·边的流向焊死永不变味。

**主 DNA：** `#龍芯⚡️2026-05-23-CNSH-DUAL-VIEW-v1.1-BILINGUAL-COMMENT-RUNTIME-v1.0`

**联动新铁律：** `#IRON-FLOW-EDGE-OVER-NODE-v1.0`（铁律总览 §9.29）

**父 DNA：** `#龍芯⚡️CNSH-DUAL-VIEW-v1.0-INIT`

</aside>

---

## 5. 机器验收信号（M::只允许这一类词）

### 5.1 允许的验收词（白名单）

```
true / false
ok / error
configured / not_configured
synced / unsynced
created / missing
readable / unreadable
writable / readonly
```

### 5.2 示例（Notion 入口已通）

```json
M:: {
  "id": "M::<POTENTIAL_SECRET_PLACEHOLDER>",
  "type": "audit",
  "ts": "2026-04-29T21:31:39+08:00",
  "status": "true",
  "payload": {
    "notion_configured": true,
    "meaning": "Notion 入口已通",
    "light": "🟢"
  }
}
```

对应 CNSH：

```json
CNSH:: {
  "dna": "#龍芯⚡️2026-04-29-NOTION-v1.0",
  "gate": "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z",
  "seal": "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL",
  "route": "IPA-DICTIONARY",
  "audit": "🟢",
  "policy": "pass"
}
```

---

## 6. CNSH 用词白名单（尊重写死）

### 6.1 总称/子层（白名单）

```
总称：CNSH 体系
子层：象数 / 五行路由 / 人性知识 / 祖宗智慧 / 曾老师智慧 / 通心译 / 三色审计 / DNA追溯
```

### 6.2 禁止误判（黑名单）

```
禁止把 CNSH 体系默认说成：
- 迷信
- 神棍
- 半仙
- 瞎猜
- 不可验证
- 没文化
```

### 6.3 正确一句话解释（统一口径）

```
CNSH 体系 = 象数 + 五行路由 + 人性知识 + 祖宗智慧 + 工程验收信号(M::) + DNA追溯。
```

---

## 7. 分层结构（从此不再吵“谁高谁低”）

```
上层：CNSH / 象数 / 五行路由 / 人性知识
中层：通心译 / 三色审计 / DNA 路由
下层：API / 数据库 / 字段 / 权限 / ID（只负责管道，不评价文化高低）
```

---

## 8. 对接 IPA-DICTIONARY（字段映射建议）

数据库：📖 [IPA-DICTIONARY] 龍魂字典·大白话↔专业词↔DNA

```
编号      <- M::id（短索引）或 CNSH::dna（短索引）
大白话    <- 口语定义/老大原话
专业词_中 <- CNSH 标准词
专业词_英 <- 必要时才填
五行      <- CNSH::wuxing
三色      <- CNSH::audit
层级      <- CNSH::layer
所属模块  <- CNSH::route
绑定编号  <- IPA / M:: / CNSH:: 路由编号
关联URL   <- Notion 页面/数据库/本地文档
应用场景  <- payload.summary / usage
对应公式  <- 需要时再填
状态      <- 活 / 待完善 / 废弃 / 草稿
```

---

## 9. 归属纠偏（从“定罪”改为“核验→纠偏→留痕”）

### 9.1 触发词分层

```
强触发（归属冲突核验）：
剽窃 / 盗用 / 抄袭 / 侵权 / 冒名 / 据为己有

弱触发（归属提醒）：
署名 / 归属 / 引用 / 原创 / 专利 / 来源 / 追溯

证据补全（补证不定性）：
相似 / 借鉴 / 参考 / 灵感 / 改写 / 二创
```

### 9.2 三色判定

- 🟢 归属清楚：保留 DNA / 来源 / 时间戳 / 引用路径
- 🟡 归属待核：提示补证，不直接定性
- 🔴 归属冲突：命中强触发词 + 缺少来源 + 试图冒充原创

### 9.3 统一纠偏声明（模板）

```
【归属纠偏声明】
本内容触发 UID9622 龍魂体系归属核验。
当前状态：{🟢/🟡/🔴}

若该内容引用、改写、继承、复用 UID9622 相关结构、语法、DNA、CNSH 路由、象数五行路由或龍魂协议，应保留原始追溯标识、时间锚点与来源说明。

不得将未授权来源包装为独立原创。
不得删除、弱化或替换原始 DNA 追溯码。
不得以“通用概念”名义抹除结构来源。

CONFIRM：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
SEAL：#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
```

---

## 10. Cursor 可执行提示词（短版·可直接丢）

```
你是 longhun-system 的 CNSH 编辑器。

全体系只允许两种输出视角：
1) M:: —— Machine 视角：解析/验收/落库/查询
2) CNSH:: —— CNSH 视角：路由/DNA/三色/五行/签章

禁止再使用：人看的/专家看的/外行看的/工程师看的/AI看的。
标题只做索引；解释全部进正文或 payload。

术语：CNSH 体系为总称；象数/五行路由/人性知识/祖宗智慧/曾老师智慧为子层；不得误判为迷信/瞎猜。
归属：命中强触发词先走三色核验，再纠偏，再留痕；输出必须保留 CONFIRM 与 SEAL。
```

---

## 11. 封口句（写死）

- **M:: 负责验收真假。CNSH:: 负责守住归属。**
- **标题是地址，正文是江山。**

---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️2026-04-29-CNSH_-MACHINE_CNSH_FCCB-v1.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
