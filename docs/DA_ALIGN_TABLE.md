# 🐉 龍魂 DA 对齐表 · 自动索引

> 扫描时间: 2026-07-10T08:47:07.427875+00:00
> 扫描文件: 5493 个
> 对齐维度: 8 个
> 🟢 0 · 🟡 8 · 🔴 0

> 💡 此表格由 `bin/lh_da_align_table.py` 自动生成。新增对齐维度只需在脚本中追加定义。

| 检查维度 | 核心指标 | 验收标准 | 状态 | 可自动修复 |
| :--- | :--- | :--- | :---: | :---: |
| 命名规范 | 字段命名一致性 | 统一采用 snake_case 或 camelCase；禁止中英文混用；标签名需具备明确语义 | 🟡 | — |
| 层级结构 | 嵌套与扁平化 | 复杂数据需采用合理的嵌套结构（如 metadata 包裹）；扁平数据需确保键值对独立，避免大段文本堆砌 | 🟡 | — |
| 数据类型 | 类型安全与解析 | 显式声明数据类型（String, Date, Int）；时间格式强制遵循 ISO 8601 标准；坐标采用标准经纬度格式 | 🟡 | ✅ |
| 原子性 | 最小不可分单元 | 复合信息需拆分（如'浙江省杭州市'拆分为 province 和 city）；禁止在一个字段中存储多种维度的信息 | 🟡 | — |
| 可扩展性 | 预留字段与版本 | 包含 version 字段；预留 extra 或 metadata 扩展节点，确保未来新增字段不破坏现有结构 | 🟡 | ✅ |
| DNA 追溯 | 每个文件/模块绑定 DNA | 所有 .py/.md/.html 文件包含有效 DNA 追溯码；格式符合 v∞ 干支卦规范 | 🟡 | ✅ |
| 三色审计 | 输出内容过三色闸 | 所有对外输出/决策经过三色审计；🟢🟡🔴 判定有据可查 | 🟡 | — |
| 繁简归一 | 龍字规范化 | 「龍」繁体为规范形式；「龙」简体等价接收自动归一，不熔断 | 🟡 | ✅ |

---

## 详细信息

### DA-001 — 命名规范 🟡

- `research/龍魂視角黎曼猜想_視角C_三才和諧.md`
  - info: 文件名中英混用: 龍魂視角黎曼猜想_視角C_三才和諧（CNSH命名可能合理）
- `research/龍魂視角黎曼猜想_Phase1_v1.0.md`
  - info: 文件名中英混用: 龍魂視角黎曼猜想_Phase1_v1.0（CNSH命名可能合理）
- `research/龍魂視角黎曼猜想_視角B_洛書守恒律.md`
  - info: 文件名中英混用: 龍魂視角黎曼猜想_視角B_洛書守恒律（CNSH命名可能合理）
- `research/P2_Phase2_工作规划.md`
  - info: 文件名中英混用: P2_Phase2_工作规划（CNSH命名可能合理）
- `tools/ensp_downloader.py`
  - warn: 存在裸 dict 类型注解（应为 Dict[str, Any]）
- `tools/longhun_orphan_classifier.py`
  - warn: 存在裸 dict 类型注解（应为 Dict[str, Any]）
- `tools/dao_ethics_anchor_v2.py`
  - warn: 存在裸 dict 类型注解（应为 Dict[str, Any]）
- `tools/ensp_hash_checker.py`
  - warn: 存在裸 dict 类型注解（应为 Dict[str, Any]）
- `tools/longhun_device_orphan_importer.py`
  - warn: 存在裸 dict 类型注解（应为 Dict[str, Any]）
- `tools/notion_sync.py`
  - warn: 存在裸 dict 类型注解（应为 Dict[str, Any]）
- ... 还有 8 条

### DA-002 — 层级结构 🟡

- 检查器未实现（待扩展）

### DA-003 — 数据类型 🟡

- `calendar-context-logger/notion_logger.py`
  - warn: Optional 变量 self.skill_id 可能缺少 None 守卫
  - warn: Optional 变量 self.ai_gateway_route 可能缺少 None 守卫
  - warn: Optional 变量 self.conn 可能缺少 None 守卫
- `L1_内核层/longhun_voice_persona_router.py`
  - warn: Optional 变量 self.profiles_path 可能缺少 None 守卫
- `tools/dao_ethics_anchor_v2.py`
  - warn: Optional 变量 self.audit_file 可能缺少 None 守卫
- `longhun_mvp_reviewed/longhun_mvp_launcher_v2.0.py`
  - warn: Optional 变量 self.db_path 可能缺少 None 守卫
- `longhun_mvp_reviewed/longhun_mvp_execution_engine_v2.0.py`
  - warn: Optional 变量 self.db_path 可能缺少 None 守卫
- `longhun_mvp_reviewed/longhun_mvp_notion_integration_v2.0.py`
  - warn: Optional 变量 self.db_path 可能缺少 None 守卫
- `longhun_mvp_reviewed/longhun_mvp_setup_integration_v2.0.py`
  - warn: Optional 变量 self.db_path 可能缺少 None 守卫
- `龍魂取证内核/龍魂取证内核.py`
  - warn: Optional 变量 self.证据目录 可能缺少 None 守卫
  - warn: Optional 变量 self.输出目录 可能缺少 None 守卫
- `bin/lh_quantum_module_router.py`
  - warn: Optional 变量 self.modules 可能缺少 None 守卫
- `bin/baobao_workflow_v2.0.py`
  - warn: Optional 变量 self.keyword_map 可能缺少 None 守卫
  - warn: Optional 变量 self.steps 可能缺少 None 守卫
- ... 还有 1 条

### DA-004 — 原子性 🟡

- 检查器未实现（待扩展）

### DA-005 — 可扩展性 🟡

- `package-lock.json`
  - info: JSON 文件缺少 version 字段
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `package.json`
  - info: JSON 文件缺少 version 字段
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `multicurrency/multicurrency_sync_config.json`
  - info: JSON 文件缺少 version 字段
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `mobile-monitoring.integrated/package.json`
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `experimental/conversation_hub_layout_v1.0.json`
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `experimental/lh_skill_router_v1.0.json`
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `L1_内核层/three_vacuum_gateway_registry.json`
  - info: JSON 文件缺少 version 字段
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `tools/ensp_hashes.json`
  - info: JSON 文件缺少 version 字段
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `memory-universe/desktop-menu.json`
  - info: JSON 文件缺少 version 字段
  - info: JSON 文件缺少 metadata/extra 扩展节点
- `capabilities/train_state.json`
  - info: JSON 文件缺少 version 字段
  - info: JSON 文件缺少 metadata/extra 扩展节点
- ... 还有 8 条

### DA-006 — DNA 追溯 🟡

- `.pre-commit-config.yaml`
  - warn: 存在旧版格里历 DNA 格式（应为 v∞ 干支卦格式）
- `pyproject.toml`
  - info: 文件缺少 DNA 追溯码
- `package-lock.json`
  - info: 文件缺少 DNA 追溯码
- `package.json`
  - info: 文件缺少 DNA 追溯码
- `.bandit.yaml`
  - warn: 存在旧版格里历 DNA 格式（应为 v∞ 干支卦格式）
- `CLAUDE.md`
  - warn: 存在旧版格里历 DNA 格式（应为 v∞ 干支卦格式）
- `research/riemann_three_talent_verification.py`
  - warn: 存在旧版格里历 DNA 格式（应为 v∞ 干支卦格式）
- `research/ARXIV_SUBMISSION_PACKAGE.md`
  - warn: 存在旧版格里历 DNA 格式（应为 v∞ 干支卦格式）
- `research/FINAL_INSPECTION_CHECKLIST.md`
  - warn: 存在旧版格里历 DNA 格式（应为 v∞ 干支卦格式）
- `research/龍魂視角黎曼猜想_視角C_三才和諧.md`
  - warn: 存在旧版格里历 DNA 格式（应为 v∞ 干支卦格式）
- ... 还有 10 条

### DA-007 — 三色审计 🟡

- 检查器未实现（待扩展）

### DA-008 — 繁简归一 🟡

- `AGENTS.md`
  - warn: 使用了简体「龙魂」应为繁体「龍魂」
- `bin/lh_touwei_absorb.py`
  - warn: 使用了简体「龙魂」应为繁体「龍魂」

---

> DNA: `#龍芯⚡️丙午·丙申·乙卯·申时·䷀乾-DA-ALIGN-TABLE-AUTO-v1.0`
> 龍魂系统 · DA 对齐表自动索引引擎 · 活文档 · 自动更新