# 🐲 龍魂系统 · 阶段 1 基础设施收口报告 v1.0

> DNA: #龍芯⚡️丙午·癸未·甲申·PHASE1-INFRA-FIX-v1.0-UID9622
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
> 执行时间: 2026-08-04
> 范围: 入口修复、健康检查、服务识别、资产统计、暴露面评估
> 三色: 🟢 4 项修复完成 · 🟡 3 项待决策 · 🔴 1 项安全建议

---

## 1. 本次修复内容

### 1.1 修复 `lh status` 入口崩溃

**问题**: `08_BIN/lh_ctl.py` 读取 `system_registry.json` 时未处理文件头的 DNA/CONFIRM/SEAL 注释，导致 `json.load()` 解析失败，`lh status` 直接崩溃。

**修复**: 在 `check_system_registry()` 中过滤 `#` 开头的注释行后再解析 JSON。

**文件变更**:
- `08_BIN/lh_ctl.py`（已重新 GPG 签名）

**验证**:
```bash
./bin/lh status
# 已正常输出 STATE.md 状态卡
```

---

### 1.2 统一 `/health` 健康检查入口

**问题**: 核心服务健康检查路径不统一，有的用 `/health`，有的用 `/v1/xxx/health`，统一监控困难。

**修复**: 在以下两个服务中新增根路径 `/health` 别名，与原路径等价：
- `08_BIN/lh_knowledge_hub_api.py`（端口 8766）
- `08_BIN/lh_memory_api.py`（端口 8771）

**文件变更**:
- `08_BIN/lh_knowledge_hub_api.py`（待签名，需重启服务加载）
- `08_BIN/lh_memory_api.py`（待签名，已重启加载）

**验证**:
```bash
curl -s http://127.0.0.1:8766/health   # {"status":"ok",...}
curl -s http://127.0.0.1:8771/health   # {"status":"🟢 记忆API在线",...}
```

**当前服务健康检查状态**:

| 端口 | 服务 | /health 状态 |
|---:|:---|:---:|
| 8766 | knowledge-hub-api | ✅ 200（已加 /health） |
| 8779 | notion-chat-bridge | ✅ 200 |
| 8776 | flow-engine | ✅ 200 |
| 8777 | flow-fusion-bridge | ✅ 200 |
| 8778 | portal-api | ✅ 200 |
| 9631 | search-engine | ✅ 200 |
| 9622 | api-gateway | ✅ 200 |
| 9630 | think-pipeline | ✅ 200 |
| 8769 | antenna-8gate-api | ✅ 200 |
| 8770 | guanlan-api | ✅ 200 |
| 8771 | memory-api | ✅ 200（已加 /health） |

---

### 1.3 识别神秘服务

之前端口活跃但身份不明的服务已全部识别：

| PID | 端口 | 服务脚本 | 说明 |
|---:|---:|:---|:---|
| 1534 | 9623 | `deploy/longhun-registry/registry_server.py` | 龍魂注册表服务 |
| 1553 | 8444 | `~/.龍魂/web/main.py` | 龍魂 Web 面板（Python 3.14） |
| 1562 | 8770 | `bin/lh_guanlan_api.py` | 观澜浏览器 AI 联动 API |
| 17389 | 8771 | `bin/lh_memory_api.py` | 统一记忆 API |
| 2098 | 9624 | `~/.龍魂/heart-talk/heart_talk_api.py` | 心谈 API |
| 25957 | 9625 | `bin/longhun_brain.py` | 龍魂大脑中枢 |
| 66714 | 19622 | `bin/lh_api_server.py` | API 服务器实例 1 |
| 67037 | 19624 | `bin/lh_api_server.py` | API 服务器实例 2 |

---

### 1.4 清理测试文件统计

**问题**: 直接用 `find` 搜索 `test_*.py` 得到 10,445 个结果，其中绝大部分来自虚拟环境 `.venv*`、历史归档 `archive`、缓存等噪音。

**修复**: 增强 `08_BIN/lh_inventory.py`：
- 新增 `scan_tests()` 函数
- 排除 `.git`, `__pycache__`, `.venv*`, `_work`, `archive`, `dist`, `_archive`, `_private`, `.pytest_cache`
- 在 `.inventory.json` 的 `summary.tests` 中输出：
  - `total_raw`: 原始匹配数
  - `excluded`: 排除的噪音数
  - `project_tests`: 项目内真实测试文件数

**实测结果**:
- 原始匹配: 10,524
- 排除噪音: 3,405（主要来自 `.venv*` 虚拟环境和 `archive` 历史归档）
- 项目内真实测试文件: **7,119**

**文件变更**:
- `08_BIN/lh_inventory.py`（已重新 GPG 签名）

---

## 2. 待决策事项

### 2.1 公网暴露面（🟡 中等风险）

以下服务当前监听 `0.0.0.0`（`*:端口`），意味着同一局域网内可直接访问。如果路由器/防火墙放行，也可能暴露到公网：

| 端口 | 服务 | 建议 |
|---:|:---|:---|
| 80/8080 | nginx | ✅ 预期对外 |
| 8501 | streamlit (app.py) | 🟡 评估是否应改为 127.0.0.1 + nginx 反代 |
| 8776 | flow-engine | 🟡 评估是否应改为 127.0.0.1 |
| 8777 | flow-fusion-bridge | 🟡 评估是否应改为 127.0.0.1 |
| 8778 | portal-api | 🟡 评估是否应改为 127.0.0.1 |
| 9000 | ASI 增强服务 | 🔴 强烈建议改为 127.0.0.1 |
| 9622 | api-gateway | 🟡 视对外 API 需求决定 |
| 9623 | registry-server | 🔴 强烈建议改为 127.0.0.1 |
| 9625 | longhun-brain | 🟡 视联动需求决定 |
| 9630 | think-pipeline | 🟡 视联动需求决定 |
| 9876/9877 | python http.server | 🔴 强烈建议改为 127.0.0.1 或停止 |

**建议操作**: 对不需要对外的服务，将启动参数 `--host 0.0.0.0` 改为 `--host 127.0.0.1`，或修改对应 launchd/systemd 服务文件。

---

### 2.2 Python 版本碎片化（🟡 中等风险）

当前同时运行 3 个 Python 版本：
- Python 3.9（Xcode）: 心谈 API
- Python 3.12（homebrew）: 绝大多数龍魂服务
- Python 3.14（homebrew python3 默认）: 注册表、龙魂 Web 面板

**建议**:
- 统一使用 `/Users/zuimeidedeyihan/.longhun/bin/python3`，它指向 Python 3.12 且已安装所有依赖。
- 逐步将 Python 3.14 和 3.9 上跑的服务迁移到 3.12。
- 避免依赖 `/opt/homebrew/bin/python3`（目前是 3.14，依赖不全）。

---

### 2.3 knowledge-hub 服务未通过 launchd 重启加载（🟡 低）

`lh_knowledge_hub_api.py` 已修改并编译通过，但当前运行的进程是 launchd 管理的。已使用 `launchctl unload/load` 重启并验证 `/health` 生效。

---

## 3. 安全建议（🔴）

**最小暴露原则**: 数据主权系统应默认所有服务只监听 `127.0.0.1`，只有 nginx 和明确需要对外提供 API 的服务才允许 `0.0.0.0`。

**建议下一阶段立即执行**:
1. 审查所有 launchd plist 和 systemd service 文件中的监听地址。
2. 将 ASI、registry、http.server 等内部服务改为 `127.0.0.1`。
3. 对必须对外的服务加认证/鉴权。

---

## 4. 签名

```
DNA: #龍芯⚡️丙午·癸未·甲申·PHASE1-INFRA-FIX-v1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

> 🐉 基础设施稳，老百姓入口才有根。
