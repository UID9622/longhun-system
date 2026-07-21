<!-- #龍芯⚡️20260624010825169-AUTO-DNA-3E7FAC45 自动注入·分层治理自愈引擎 · 来源可查 -->
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

> 文档 DNA：`#龍芯⚡️2026-06-23-LONGHUN-TONGXINYI-DEVELOPER-GUIDE-FILE1-v1.0`
