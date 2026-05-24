# UID9622 字段级 AutoFill 指南

**DNA追溯码：** #ZHUGEXIN⚡️2025-WORLD-SYSTEM-V1.0

---

## ⚙️ Field-Level AutoFill Rules（AI Only）

**格式：** DB · Field → AutoFill Source / Default / Condition / Side Effect

---

## Scene DB

```yaml
BBox:
  AutoFill: Default [50,50,20]
  Condition: 缺失

Lighting:
  AutoFill: Default 0.8
  Condition: 缺失

Gravity:
  AutoFill: Inherit Parent Scene
  Condition: 有 Parent

DNA:
  AutoFill: Inherit Parent Scene
  Condition: 新增子场景

Tags:
  AutoFill: From DNA.Tags
  Condition: 自动

Side Effect:
  - 生成 Scene Snapshot（Audit）
```

---

## Object DB

```yaml
Transform:
  AutoFill: Default [0,0,0]
  Condition: 缺失

Scene:
  AutoFill: Context Scene
  Condition: 创建时

DNA:
  AutoFill: Scene.DNA
  Condition: 缺失

Interactions:
  AutoFill: AutoCreate Template
  Condition: Type=Item/Prop

Side Effect:
  - 注册 LogicLink → EnginePayload.Transform
```

---

## Actor DB

```yaml
Level:
  AutoFill: Default 1
  Condition: 缺失

HP:
  AutoFill: From Level Preset
  Condition: 缺失

Behavior:
  AutoFill: From DNA.Type
  Condition: 缺失

Personality:
  AutoFill: AutoCreate Core
  Condition: NPC

Memory:
  AutoFill: AutoCreate Long
  Condition: NPC/Player

Side Effect:
  - 写入 AI Memory DB
```

---

## Rules DB

```yaml
Trigger:
  AutoFill: From Name Pattern
  Condition: 缺失

Action:
  AutoFill: From Object/Event Ref
  Condition: 缺失

Scope:
  AutoFill: Infer（Object/Scene/World）
  Condition: 自动

Side Effect:
  - 生成 Rule Stub → Events
```

---

## Events DB

```yaml
Trigger Type:
  AutoFill: From Linked Rule
  Condition: 缺失

Next Event:
  AutoFill: AutoChain
  Condition: 未终止

Scene:
  AutoFill: Context Scene
  Condition: 缺失

Side Effect:
  - 更新 Event Graph
```

---

## Interaction DB

```yaml
Type:
  AutoFill: From UI Type
  Condition: 缺失

Event:
  AutoFill: AutoBind Closest
  Condition: 缺失

Side Effect:
  - 生成 UI Hook
```

---

## Quest & Story DB

```yaml
Stages:
  AutoFill: AutoCount
  Condition: 缺失

Current Stage:
  AutoFill: 1
  Condition: 新建

Related Events:
  AutoFill: AutoGenerate
  Condition: 缺失

Rewards:
  AutoFill: Economy Preset
  Condition: 缺失

Side Effect:
  - 生成下一阶段 Event
```

---

## DNA DB

```yaml
Inherit Policy:
  AutoFill: Full
  Condition: 缺失

Impact Scope:
  AutoFill: Infer From Type
  Condition: 缺失

Side Effect:
  - 批量更新关联实体
```

---

## LogicLink DB

```yaml
Transform Rule:
  AutoFill: Template Match
  Condition: 缺失

Side Effect:
  - 注册 Translator Snippet
```

---

## WorldBridge DB

```yaml
Condition:
  AutoFill: Scene Entry Rule
  Condition: 缺失

Auto Rule:
  AutoFill: True
  Condition: 默认

Side Effect:
  - 生成跨 Scene Rule
```

---

## MultiShard DB

```yaml
Sync Policy:
  AutoFill: Auto
  Condition: 缺失

Side Effect:
  - Shard Index 更新
```

---

## AuditLog DB

```yaml
Rollback Token:
  AutoFill: AutoGenerate
  Condition: 每次写入

Side Effect:
  - Snapshot Check
```

---

## AI Memory DB

```yaml
Memory Type:
  AutoFill: Long
  Condition: Actor=NCP/Player

Weight:
  AutoFill: From Event Impact
  Condition: 缺失

Side Effect:
  - 影响 Behavior Tree
```

---

## Global State DB

```yaml
Time:
  AutoFill: System Clock
  Condition: 缺失

Weather:
  AutoFill: Cycle Rule
  Condition: 缺失

Side Effect:
  - 触发环境 Events
```

---

## 🔒 执行锁（必须存在）

- **AutoFill 不得修改：** ID / Schema / Field Meaning
- **手动 Override 需写入：** AuditLog.Diff
- **Evolution 仅能：** 创建实例，不可改字段定义

---

## 📋 SideEffects Chain

```
AutoFill → Translator → EnginePayload → AuditLog
```

---

## ✅ Lock Summary

- **NoSchemaChange**：禁止修改 Schema
- **Override→Audit**：手动修改必须记录
- **Evolution=InstanceOnly**：演化只能创建实例

---

**系统版本：** v1.0.0
**最后更新：** 2025-12-27
**状态：** Active
