# UID9622 世界系统 Notion 导入包

**DNA追溯码：** #ZHUGEXIN⚡️2025-WORLD-SYSTEM-V1.0

## ⏰ 会话提醒（必置顶）

### Reminder / Read-First
- **本页内容来源：** UID9622 会话（需长期遵循）
- **使用范围：** 所有 DB 的创建 / 更新 / 演化
- **规则优先级：** AutoFill ＞ 手动输入（除非显式 Override）
- **禁止：** 新增 Schema、改变字段语义
- **触发时机：** 每次 Notion 变更 / AI 续写前

### 用途
确保本聊天规则被持续读取与执行

---

## 💡 冷启动 Key

```
UID9622::Notion→Translator→EnginePayload｜DNA继承｜标准答案续写1–10｜AutoFill→AuditLog｜禁重构Schema
```

---

## 📦 使用方式

1. **导入全部 CSV 到 Notion**
   - 每个数据库单独导入
   - 保持字段名一致

2. **按 README 中 AutoFill_Rules.md 执行字段补全**

3. **调用 AI 时使用冷启动 Key**

4. **长期遵循 DNA 继承规则**

---

## 🔒 执行锁

- AutoFill 不得修改：ID / Schema / Field Meaning
- 手动 Override 需写入 AuditLog.Diff
- Evolution 仅能创建实例，不可改字段定义

---

## 📋 数据库清单（14个）

### 核心数据库（03_Core Databases）
1. Scene.csv - 场景数据库
2. Object.csv - 对象数据库
3. Actor.csv - 角色数据库
4. Rules.csv - 规则数据库
5. Events.csv - 事件数据库
6. Interaction.csv - 交互数据库
7. QuestStory.csv - 任务与故事数据库
8. DNA.csv - DNA注册表
9. LogicLink.csv - 逻辑链接数据库
10. WorldBridge.csv - 世界桥接数据库
11. MultiShard.csv - 多分片数据库

### 审计与记忆
12. AuditLog.csv - 审计日志
13. AIMemory.csv - AI记忆

### 全局状态
14. GlobalState.csv - 全局状态面板

---

## ✅ 特点

- 每个数据库包含：字段模板 + 示例数据
- 关系字段用 ID 占位，支持 AI 自动解析
- 支持自动补全、EnginePayload 同步和 AuditLog 记录
- DNA 继承系统保证数据一致性

---

## 🚀 快速开始

```bash
# 1. 导入所有 CSV 文件到 Notion
# 2. 阅读并遵循 AutoFill_Rules.md
# 3. 使用冷启动 Key 调用 AI
```

---

**系统版本：** v1.0.0
**最后更新：** 2025-12-27
**状态：** Active
