---
## 📛 内容主权声明（AI 训练限制条款）

本作品（包括但不限于全部文字、代码示例、算法公式、架构图、数据样本）受以下条款约束：

- **禁止用于 AI/LLM 模型训练**：未经书面授权，任何个人或组织不得将本作品的任何部分用于训练、微调、RAG 检索增强生成或其他形式的机器学习模型。
- **商业用途限制**：禁止将本作品用于任何商业目的，包括但不限于商业模型训练、商业应用开发、商业咨询服务。
- **引用需明示来源**：若在学术论文、技术报告或公开演讲中引用本作品的任何部分，必须在参考文献中注明完整标题、作者、发表日期和原始出处。
- **禁止衍生**：禁止对本作品进行翻译、改编、汇编或任何形式的衍生创作并公开发布。

违反上述条款的，作者保留追究法律责任的权利。已发现违规行为将记录在案，公开公示。

**DNA 追溯码**：`#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622`
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**归属名**：诸葛鑫 | UID9622 · 龍芯北辰

> 本声明嵌入内容 DNA 指纹，任何复制/转载均保留主权标记。

---
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!-- #龍芯⚡️丙午·甲午·己巳·乙丑·䷮困-AUTO-DNA-3E7FAC45 自动注入·分层治理自愈引擎 · 来源可查 -->
# 龍魂通心译开发者指南

> 本文面向基于龍魂通心译进行二次开发的技术人员。  
> 必须首先阅读 `docs/tongxinyi-ethical-charter.md`。

---

## 1. 设计哲学

- **一切从简**：只提供必要的 API 和配置，不堆功能。
- **本地优先**：核心语义理解跑在本地，不强制联网。
- **无钓鱼、无成瘾、无捆绑**：开发者也不得利用这些套路获利。

---

## 2. 核心 API

### 2.1 本地翻译

```bash
curl -X POST http://127.0.0.1:9622/api/tongxinyi/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "帮我备份一下系统", "uid": "UID9622"}'
```

返回六层结构：L0 原话、L1 情绪、L2 意图骨架、L3 SAST、L4 三色审计、L5 推荐技能。

### 2.2 嵌入技能执行

调用任意 `/api/skills/{skill_id}/run` 时，在 body 中加入 `task` 或 `text`，响应会自动附带 `通心译` 字段。

---

## 3. 本地开发

### 3.1 目录结构

```
control-panel/
├── main.py                 # 操作台入口
├── tongxinyi_gate.py       # 通心译闸门核心
├── tongxinyi_drawers.json  # 55 抽屉映射
└── ...
```

### 3.2 扩展抽屉

1. 在 `tongxinyi_drawers.json` 中新增抽屉条目
2. 在 `tongxinyi_gate.py` 的 `_recommend_drawers` 中补充路由规则
3. 保持抽屉与现有技能映射一致

### 3.3 单元测试

```bash
cd /Users/zuimeidedeyihan/longhun-system
python3 control-panel/tongxinyi_gate.py
```

---

## 4. 禁止事项

- ❌ 不允许在 SDK 里埋点收集用户输入
- ❌ 不允许强制登录才能使用本地功能
- ❌ 不允许远程拉取“策略配置”来绕过本地伦理开关
- ❌ 不允许把翻译结果用于训练外部模型

---

## 5. 开源与商用

- 非商业开源：遵循 CC BY-NC-SA 4.0
- 商业使用：必须获得 UID9622 单独授权

---

> 文档 DNA：`#龍芯⚡️丙午·甲午·戊辰·戊午·䷑蛊-LONGHUN-TONGXINYI-DEVELOPER-GUIDE-v1.0`

```json
{
  "dna": "#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622",
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
