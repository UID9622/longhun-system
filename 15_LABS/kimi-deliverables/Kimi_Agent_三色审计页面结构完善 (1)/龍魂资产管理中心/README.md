# 🐉 龍魂资产管理中心 v1.0 + 流控模块 v1.2 — 从概念到代码

> DNA: `#龍芯⚡️丙午·丙申·己未·庚午·䷡大壮-ASSET-CENTER-v1.0-UID9622`
> （干支由 `dna_trace.生成DNA()` 算法生成，2026-08-13 实测值，非手写）

本次复盘补齐的两块"只有设计、没有代码"的模块，现在全部可运行、有实测。

---

## 一、资产管理中心 `asset_center.py` + `lh_asset.py`

设计文档里的 `lh asset` 全部子命令已实现：

| 命令 | 功能 | 实测 |
|---|---|---|
| `init --scan <目录>` | 递归扫描入库，自动注册 | ✅ 22 个文件一次入库 |
| `list / show / search` | 查询（支持 --type --tag 过滤 + FTS5 全文） | ✅ |
| `graph <资产ID>` | 关联图遍历（去重） | ✅ |
| `history <资产ID>` | 变更历史 | ✅ |
| `retire --reason / revive` | 注销（⚪标记，永不删除）/ 复活 | ✅ 注销后搜索不可见，复活恢复 |
| `link <源> <目标> <关系>` | 建立关联 | ✅ |
| `export --format json` | 全量导出 | ✅ |
| `verify` | 哈希链完整性校验 | ✅ 见下 |

**核心机制**
- **幂等扫描**：按 `location + SHA-256` 判重 —— 第1次 `{'注册': 22}`，第2/3次 `{'跳过·幂等': 22}`，重复扫描不产生重复资产。
- **哈希链**：每条资产 `chain_hash = SHA256(prev_chain_hash + 文件hash)`，篡改任一文件 → 验链报 `{'完整': False, '断点': 'AST-20260813-001', '三色': '🔴'}`，断点精确定位。
- **不删除只冻结**：`retire` 只把状态改为 ⚪ 并写历史，数据永久保留，符合 P0 铁律。
- **DNA 自动签名**：注册时调 `生成DNA(f"AST{序号:03d}")`，干支全部算法生成。
- **CLI 端到端**：`python3 lh_asset.py init --scan ...` → `verify` 返回 `{'完整': True, '长度': 22, '三色': '🟢'}`，退出码 0。

数据库默认 `~/.longhun/asset_center.db`（assets / edges / history / assets_fts 四表）。

## 二、流控模块 v1.2 `flow_control_v1.2.py`

v1.1 设计文档里列的 4 项修复，全部落地：

1. **租户模式解析** `_解析租户配置`：fnmatch 通配（如 `vip-*`）——实测 vip-001 享受 burst=100 全放行，路人甲 `[True, False]` 被限。
2. **降级自动恢复**：降级 60 秒后自动回检 —— 实测速率 0.5 受限，过期后恢复 1。
3. **update_config 余量迁移**：改配置不再清空令牌桶，余量按比例迁入新桶 —— 实测 90% 余量保留（90.0 → 新 burst 100）。
4. **审计采样**：`audit_sample=0` 时放行长流不记日志，blocked/timeout 永远记录 —— 实测日志仅 `[('check', 'blocked')]`。

## 三、未验证备注 🟡

- 🟡 资产中心 REST API（五头签名网关）仍是设计，未实现 —— 下一轮。
- 🟡 FTS5 在极简 SQLite 编译环境下可能不可用，代码已做降级（退化为 LIKE 查询），本机实测 FTS5 可用。
- 🟡 流控 v1.2 与 v1.1 的 `wait_and_check_v11` 补丁尚未合并成单一文件，目前 v1.2 自含完整实现，可直接替换。

## 用法

```bash
cd 龍魂资产管理中心
python3 lh_asset.py init --scan /path/to/龍魂目录
python3 lh_asset.py list
python3 lh_asset.py verify
```
