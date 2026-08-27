> DNA: #龍芯⚡️丙午·壬辰·乙亥·壬午·䷚颐-SYNC-COMPLIANCE-20260827-7A2C9F3D
# 文件归集 · 批次5：browser_profile 排除 + lh_gpg_sign 单一真相源焊死（2026-08-27）

> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 类型: 治理报告 · 文件归集批次5
> 触发: `lh_gpg_sign.py scan 08_BIN --orphans` 报 79 未签名 → 排查发现两类问题

## 问题根因

| # | 现象 | 根因 |
|:---:|:---|:---|
| 1 | 79 个未签名中 60 个是 `08_BIN/browser_profile/user_data/` 浏览器运行时数据（Chrome 缓存/扩展/证书吊销/CRL） | `lh_gpg_sign.py` 的 `EXCLUDE_DIRS` 为硬编码元组，未加载共享排除配置；`scan-exclusions.json` 也无 browser_profile 条目 |
| 2 | 19 个真核心脚本（claude_*/lh_browser_*/lh_dna_*/longhun_* 等）确实未签名 | 文件归集批次1-4 未覆盖到，本次补签 |

## 修复（三步）

### ① 代码级：lh_gpg_sign.py 走单一真相源（repair-pipeline v1.1 铁律1）
- 新增 `_load_shared_exclusions()`：从 `.codebuddy/rules/scan-exclusions.json` 的 `excluded_dirs` 全分类拉平加载 → `EXCLUDE_PREFIXES`（66 个前缀）
- 新增 `_is_excluded(fstr)`：硬编码段名匹配 或 共享配置前缀匹配，统一判定
- `find_all_signable` / `find_orphan_asc` 全部改用 `_is_excluded`
- 效果：改一次配置所有扫描脚本同时生效，不再各自硬编码

### ② 配置级：scan-exclusions.json 加浏览器运行时排除
- 新增分类 `v2_7_runtime_generated`: `["08_BIN/browser_profile"]`
- `_meta` 版本 v1.0→v1.1 · updated 2026-08-27 · `loaded_by` 增加 `lh_gpg_sign.py`
- 注意：分类必须为数组（加载逻辑按 list 拉平），不可用 dict 结构

### ③ 执行级：补签 19 个核心脚本
claude_bone_retriever / claude_gua_classifier / claude_shield_engine / lh_browser_audit_middleware / lh_browser_inject / lh_browser_package / lh_dna_gua_verifier_v1.0 / lh_dna_verify / lh_export_engine / lh_fix_protocol_headers / lh_google_audit / lh_model_bench_ollama / lh_notion_pull_all / lh_responsibility_collapse_v2 / list_skill_commands / longhun_evolution_plus / longhun_fengshui_game_engine_v1 / longhun_multiagent_arch_engine_v1 (1) / longhun_multiagent_arch_engine_v1

## 验证

- 共享排除加载：66 前缀 · browser_profile ✅ · archive ✅
- 重扫 08_BIN：79 → 19 → **0** 未签名
- gpg 直验 3 个抽查：**完好的签名 · 诸葛鑫 · [绝对]** ✅
- py_compile 通过 · lint 0 错误
- GPG 重签：bin/lh_gpg_sign.py + scan-exclusions.json（--force）

## 铁律遵守

- ✅ 单一真相源：lh_gpg_sign 不再硬编码排除目录，全部走 scan-exclusions.json
- ✅ browser_profile 运行时数据不进签章范围（第三方/运行时生成物原则）
- ✅ 核心脚本全部补签（mandatory_sign_dirs 08_BIN/ 覆盖）
- ✅ GPG 签名变更文件 · 台账留档

---
【签名】
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
三色: 🟢 79→0 · 单一真相源焊死 · browser_profile 排除 · 19 核心脚本补签
