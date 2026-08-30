# 🐉 龍魂 · 流场体系复盘与融合升级方案 v1.0
## LongHun Flow Field System — Retrospect & Fusion Upgrade Plan

DNA: #龍芯⚡️2026-08-30-FLOW-FIELD-RETROSPECT-FUSION-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0（思想层）· MulanPSL v2（工程层）
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 复盘+融合升级+清理归档 全部完成（2026-08-30）

---

## 0｜一句话结论

> 流场（Flow Field）体系当前处于**多版本繁荣期（version sprawl）**：7+ 引擎、20+ 前端页面、文档副本重复、2 个 launchd 守护叠加、1 处端口冲突（8972）。**保留现行主干 `lh_flow_field.py`（:8972·launchd·lh flow-field 注册·门户在用），融合旧版精华，归一为单一新版本**。

---

## 1｜引擎层盘点（Engine Layer）· 7+ 引擎重复实现

| # | 引擎 | 版本 | 行数 | 端口 | 运行状态 | 定位 |
|---|---|---|---|---|---|---|
| E1 | `lh_flow_field.py` | v1.0 | 529 | :8972 | 🟢 **现行**·launchd 常驻 | **流场拓扑引擎（主干）**：节点=服务/引擎/闸门/人格，带公式+实时端口探测+日志tail · HTTP API `/topology /node /log /trigger` · CLI status/node/api |
| E2 | `lh_flow_engine.py` | v2.0 | 1010 | :8776 | 🔴 旧版·**今日已停** | 物理-信息流场同构映射（粒子/速度/涡旋/压力/热力图）· WebSocket `/ws` · 回放 `/replay` · 异常检测 · FastAPI |
| E3 | `lh_flow_fusion_bridge.py` | v1.0 | 1290 | :8777 | ⚪ 按需未跑 | 事件总线→翻译→注入（引擎事件→流场扰动类型/位置/强度）· 融合映射矩阵 11 类 |
| E4 | `lh_flow_upgrade.py` | v1.1 | 500 | — | ⚪ 补丁脚本 | launchd 守护安装·注入规则扩展·仪表盘增强·lh 命令集成 |
| E5 | `lh_flow_fusion_pipeline.py` | v1.0 | ~450 | — | ⚪ 管线脚本 | 一键全量注入（可观测性引擎→:8777/event） |
| E6 | `lh_neuron_flow_engine.py` | v4.0 | 1366 | CLI | ⚪ 独立引擎 | 神经元-流场三才映射（地/天/人场）· Hopfield 能量 · 人格路由 · 批处理 |
| E7 | `CNSH_流场可视化引擎.py` | v1.0 | 629 | — | ⚪ 服务层 | 粒子=DNA·决策透明审计·SM3 哈希链 |
| E8 | `cnsh_flow_viz.py`(L5) | v1.0 | 666 | — | ⚪ 服务层 | CNSH 流场可视化（与 E7 双胞胎） |
| E9 | `digital_flow_field/`(05_ENGINES) | v2.0 | 项目 | Docker | ⚪ | 数字流场可视化器（独立项目·有测试） |
| — | `lh_autoflow.py` | v1.0 | 55.9KB | CLI | ⚪ | 一句话全链路自动执行（**非可视化**·独立域） |
| — | `lh_flow_control.py` | v1.1 | 21.7KB | 模块 | ⚪ | AI 网关流控 Token Bucket（**非流场**·独立域） |
| — | `lh_flow_pipeline.py` | — | 11.8KB | — | ⚪ | 通用管线（非流场专用） |

**问题**：
- E1(现行) 是纯拓扑展示，**缺** E2 的粒子物理映射、E3 的事件注入、E6 的三才映射、E7 的粒子透明审计
- E2/E3/E4/E5 是同一套"融合流场"的**四分五裂**（引擎/桥/升级/管线各自独立），且 E2 仍占 8776 被 launchd KeepAlive 拉起（今日已停）
- E7/E8 双胞胎重复
- 功能重叠但互不引用 → **无单一事实源（single source of truth）**

---

## 2｜前端层盘点（Frontend Layer）· 20+ 页面版本堆叠

| 目录 | 数量 | 关键页面 | 状态 |
|---|---|---|---|
| `10_PORTAL/flow-field.html` | 1 | 流场拓扑图（门户 `/apps/flow-field.html` 在用）| 🟢 在用 |
| `10_PORTAL/longhun-flow-field-v9.html` | 1 | 流场骨架主控（门户卡片在用）| 🟢 在用 |
| `10_PORTAL/flow/` | 9 | v9/v10/portal_v2/unified-v9/v10/龙魂流场20260426l/dragon-core/fixed-point/sandbox | 🔴 版本堆叠 |
| `10_PORTAL/visualizations/` | 9+3 | flow-index/current-flow/dragon-soul-flow/flow-mapping/flow-monitor/master-control-flow/hetu-ground/unified-v9/longhun-flow-20260426 + 子目录 | 🔴 版本堆叠 |
| `10_PORTAL/p0-controls/三才流場·San Cai Flow Field·UID9622.html` | 1 | 三才流場 79KB·1735 行·最全 | ⚪ 保留候选 |
| `web/flow/` | 20 | current/龍魂流场20260426l/三才流场_v3.0/sancai-v8/v8.1/河图洛书地面图 等 | 🔴 旧站点·待核 |
| `12_DOCS/references/` | 1 | 龍魂流场20260426l.html | ⚪ 参考 |

**问题**：同一 IPV4 流场概念被 v8/v9/v10/unified/portal_v2 等版本无限堆叠，门户只用 2 个，其余 20+ 是历史演进残留。

---

## 3｜文档层盘点（Documentation Layer）· 副本重复

| 文档 | 问题 |
|---|---|
| `LH-FLOW-MASTER-v2.0.md` + `LH-FLOW-MASTER-v2.0-SUPPLEMENT.md` | **MD5 全同（5e62d487…）·SUPPLEMENT 是裸副本** |
| `UID9622_龍魂流场总控_v2.0.md` + `_1.md` | **MD5 全同（24a8435a…）·_1 是裸副本** |
| `README_LONGHUN_FLOW.md` + `(迁移).md` | 迁移标记副本 |
| knowledge-matrix 双目录 | `desktop-knowledge-matrix/` 与 `knowledge-matrix-src/` 三才流场镜像重复 |

---

## 4｜守护与端口盘点（Daemon & Port）

| 项 | 值 | 状态 |
|---|---|---|
| launchd `com.longhun.flow-field-api` | :8972 → `lh_flow_field.py api` | 🟢 运行中 |
| launchd `com.longhun.flow-engine` | :8776 → `lh_flow_engine.py` | 🔴 **今日已 unload**（MEMORY 标"停用"但实际 KeepAlive 存活，实际在跑）|
| 端口 8972 | flow-field-api 实占 | 🟡 与 render 服务文档声明的 8972 冲突（render 未注册 launchd·按需启动会撞端口）|
| 端口 8776 | 已释放 | 🟢 |
| 端口 8777 | 无监听 | ⚪ |

---

## 5｜数据层盘点（Data Layer）

| 文件 | 内容 |
|---|---|
| `config/flow-field-index.json` | v2.0 索引（天/地/人/魂/器 5 视图）|
| `config/flow_control.yaml` | 流控配置 |
| `11_DATA/CNSH_流场数据.json` | 2026-06-29 快照·44 粒子 |
| `11_DATA/flow_fusion.db` + `data/flow_fusion.db` | **双数据库·MD5 不同**·需归一 |
| `logs/flow-fusion.err` 45KB / `flow_control_audit.jsonl` 8.43MB / `neuron_flow_audit.jsonl` | 审计日志 |

---

## 6｜融合升级方案（Fusion Upgrade Plan）

### 原则
1. **不推倒重来**：以现行主干 `lh_flow_field.py` v1.0 为基础升级到 **v2.0**
2. **吸收精华**：把旧版独有能力融合进主干（注入/映射/回放/透明审计）
3. **归一**：一套引擎·一套前端·一套文档·一个守护
4. **不删只冻结**：旧版本归档 `_archive/`·无用副本删除（MD5 全同）

### 6.1 引擎融合（E1 升级 v2.0）
在 `lh_flow_field.py` 现有 529 行基础上，新增：
- **`/inject` 事件注入端点**（吸收 E3 融合映射矩阵）：`POST /inject` 接收引擎事件（self-audit/health/trip/resource），翻译为流场扰动注入节点状态
- **粒子透明度评分**（吸收 E7）：每个节点增加 `transparency` 字段（0~1），全链路可审计
- **节点公式扩展**（吸收 E2 物理映射）：热力/压力/涡旋指标并入 `build_topology` 输出
- **CLI 扩展**：`status --json`（结构化输出·供前端/其他引擎消费）

### 6.2 前端归一
- **保留在用 2 个**：`flow-field.html`（门户入口）· `longhun-flow-field-v9.html`（门户卡片）
- **融合升级 `flow-field.html`**：消费新增 `/inject` 与透明度字段·动态扰动可视化
- 其余 20+ 历史版本 → **归档**（`_archive/flow-field-legacy/`）

### 6.3 文档归一
- `LH-FLOW-MASTER-v2.0-SUPPLEMENT.md`（MD5 全同副本）→ **删除**
- `UID9622_龍魂流场总控_v2.0_1.md`（MD5 全同副本）→ **删除**
- 知识矩阵镜像 → 保留 `desktop-knowledge-matrix/`（01_protocols 为主）

### 6.4 守护归一
- `com.longhun.flow-engine`(8776) → **已停**·plist 归档
- 8972 冲突 → 记录为 render 侧待办（render 未注册 launchd·按需启动前需换端口）

### 6.5 数据归一
- `flow_fusion.db` → 保留 `11_DATA/`·`data/` 版归档
- `CNSH_流场数据.json` → 保留（快照）

---

## 7｜执行清单（Execution Checklist）· ✅ 全部完成

| # | 动作 | 状态 |
|---|---|---|
| 1 | `launchctl unload com.longhun.flow-engine`（8776 已停·端口已释放） | ✅ |
| 2 | 升级 `lh_flow_field.py` v1.0 → **v2.0**（融合注入矩阵+透明度+扰动+JSON CLI）· py_compile OK | ✅ |
| 3 | 前端 `flow-field.html` 升级 v2.0（注入面板+事件流+透明度可视化）· 结构校验 OK | ✅ |
| 4 | 归档前端 29 个历史版本（portal-flow 9 + web-flow 20）至 `_archive/flow-field-legacy/` | ✅ |
| 5 | 删除 MD5 全同副本：`LH-FLOW-MASTER-SUPPLEMENT` + 总控 `_1` + cache 副本 | ✅ |
| 6 | 迁移副本 3 份归档 `_archive/flow-field-legacy/docs/`（保留正版） | ✅ |
| 7 | API 重启·全端点实测（/health /topology /inject /events）+ `lh flow-field` 实测 | ✅ |
| 8 | GPG 签名 4 文件全部"完好的签名[绝对]" | ✅ |

### 7.1 变更文件清单

| 文件 | 变更 |
|---|---|
| `08_BIN/lh_flow_field.py` | v1.0→v2.0：+55 行注入模块·+`/inject /events`·节点透明度/扰动·CLI `--json/inject/events` |
| `10_PORTAL/flow-field.html` | v1.0→v2.0：注入面板·事件流侧栏·扰动环·透明度徽章·+31 行 JS |
| `bin/lh.py` | `flow-field` 命令描述更新 |
| `12_DOCS/agent_reports/FLOW-FIELD-RETROSPECT-FUSION-v1.0.md` | 本报告 |

### 7.2 遗留待办（✅ 2026-08-30 第二轮已全部完成）

| 待办 | 处置 |
|---|---|
| **8972 端口冲突** | ✅ **render 迁至 :8788**（`lh_render.py`/`server.py`/`render.yaml`/compose/Dockerfile/deploy/ACCEPTANCE/service_manager/lh.py 9 文件同步·沿革注释保留·实测 8788 可连通）· 8972 归 flow-field-api |
| **双 flow_fusion.db** | ✅ **归一**：11_DATA 历史数据（14 心跳/49 事件）合并入 `data/flow_fusion.db`（bridge 现行写路径）· integrity_check ok · 11_DATA 版归档 `_archive/flow-field-legacy/data/` |
| **lint 警告** | ✅ **清零**：`log_message fmt→format`（ERROR 消除）+ import 排序 + chmod try→contextlib.suppress + open mode + NODES→node_list · 0 诊断 |
| **P05 新增待核① /log 无白名单** | ✅ **v2.1 加固**：`_log_whitelisted()` 仅允许 `logs/` 下相对路径·拒绝绝对路径与 `..` 穿越·实测 400 拦截 |
| **P05 新增待核② /inject 无鉴权** | ✅ **v2.1 加固**：启动生成 token（`data/flow_field_token`·chmod 600）·`X-LH-Token` 校验·新增 `/token` 端点供前端·前端 doInject 携带·实测 401/200 均正确 |

### 7.3 v2.1 追加变更清单（第二轮）

| 文件 | 变更 |
|---|---|
| `08_BIN/lh_flow_field.py` | v2.0→v2.1：+token 鉴权(`/token`+`X-LH-Token`+`data/flow_field_token`)·+/log 白名单(`_log_whitelisted`)·lint 清零(6 项) |
| `10_PORTAL/flow-field.html` | doInject 获取 token 并携带 `X-LH-Token` header |
| `08_BIN/doorkeeper/service_manager.py` | 渲染服务端口 8972→8788 |
| `render/lh_render.py`·`render/server.py`·`render/config/render.yaml`·`render/docker-compose.render.yml`·`render/Dockerfile.render`·`render/deploy_render.sh`·`render/ACCEPTANCE.md` | render 端口沿革 8766→8972→8788（8 文件同步） |
| `12_DOCS/codebuddy_integration_v1.0.md` | render 端口引用更新 + 流场 8972 补记 |
| `data/flow_fusion.db` | 11_DATA 历史数据合并（14 心跳/49 事件·integrity ok） |
| `_archive/flow-field-legacy/data/flow_fusion.db` | 11_DATA 旧库归档 |
| GPG | 12 文件签名全部"完好的签名[绝对]" |

**验收实况**：lint 0 诊断 · py_compile OK · API 全端点实测（health/log 白名单/token/inject/topology）· render 8788 实测连通 · 前端结构校验 OK · bash -n OK

---

## 8｜风险与边界

- **8972 端口冲突**（render 声明 8972 但未注册 launchd）：本次不动 render，记录待办，按需启动 render 前需先改端口
- **E6/E9 独立域**：不并入主干，保留独立运行能力
- **不删除只冻结**：除 MD5 全同副本外，一律归档不删
- 删除前一律三查（bin 软链→08_BIN 已确认 inode 一致）

---

## 9｜DNA 锚定

#龍芯⚡️2026-08-30-FLOW-FIELD-RETROSPECT-FUSION-v1.0-UID9622
