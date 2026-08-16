# 🐉 龍魂 · 透明看板 v1.0

**DNA:** `#龍芯⚡️丙午·丙申·丁酉·辰时-TRANSPARENT-DASHBOARD-UID9622`  
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`  
**三色:** 🟢 通过  
**状态:** 🟢 生效

---

## 核心判断

> **永远没有黑箱操作** 不是功能描述，是道德承诺。透明看板把君子协议从口号变成可视化的契约：所有关键决策、状态、行为，直接暴露给用户验证。

---

## 文件位置

| 组件 | 路径 | 说明 |
|:---|:---|:---|
| 看板服务 | `08_BIN/lh_transparent_dashboard.py` | FastAPI 服务，Web + REST API |
| 启动脚本 | `scripts/start_transparent_dashboard.sh` | 一键启动 |
| 别名注册 | `config/naming_alias_registry.json` | `transparent-dashboard` |
| 测试 | `13_TESTS/test_transparent_dashboard.py` | 3 项测试 |

---

## 展示数据

| 模块 | 来源 | 说明 |
|:---|:---|:---|
| 📜 治理事件 | `.state/industry_governance/governance.sqlite` | 八大痛点评估/执行记录 |
| 🚫 耻辱墙 | SQLite `shame_wall` | 违规记录永久公开 |
| 🏆 荣誉墙 | SQLite `honor_wall` | 贡献者公开表彰 |
| 👤 影子AI检测 | SQLite `unauthorized_ai` | 未授权工具检测记录 |
| 🔗 Agent 绑定 | SQLite `agent_identities` | 法定身份绑定统计 |
| 📜 史官记录 | `~/.longhun/04_AUDIT/*.jsonl` | 系统操作日志 |
| 📚 知识图谱 | `knowledge/graph/graph.json` | 节点/关系统计 |

---

## API 端点

| 方法 | 路径 | 用途 |
|:---|:---|:---|
| GET | `/` | Web 看板页面 |
| GET | `/api/health` | 健康检查 |
| GET | `/api/data` | 完整透明数据 JSON |

---

## 启动方式

```bash
# 本地安全访问（默认）
./scripts/start_transparent_dashboard.sh

# 网络内公开（谨慎使用）
./scripts/start_transparent_dashboard.sh 0.0.0.0 8080
```

---

## 君子协议

- 所有数据公开可查
- 实时更新，每次操作即时同步
- 史官记录不可删除，耻辱墙永久保留
- 这是承诺，不是功能，不容任何变动

<!-- ⛓️DNA-CHAIN
DNA:V1|丙午·丙申·癸亥·辰时·䷗复|P04鲁班|创建|透明看板+双语路由封装|bhash:1a61f31b|chash:69748d01|←GENESIS
⛓️END-->
