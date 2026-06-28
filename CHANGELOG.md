# 龍魂系统变更日志

DNA: #龍芯⚡️2026-06-28-LONGHUN-CHANGELOG-v1.1

## 2026-06-28

- 主干自我迭代系统 v1.0 部署签章。
- 集成 `lh-self-update`：检测 `formula_alignment_v1_6_raw.md` SHA256 变化，自动重建 512 维 TF-IDF 向量、刷新 KG 索引、保留 5 份滚动备份、支持 `--rollback`。
- `lh` 命令注册表新增：全局索引、公式对准表、notion 同步、主干自我迭代。
- 体检脚本纳入主干自我迭代检查项。
- 通心译门 v1.1 升级：引入五行向量与人性偏移评分，新增 `tongxinyi_wuxing_dict.json`。
- 本次部署 DNA：#龍芯⚡️2026-06-28-SELF-UPDATE-INTEGRATION-DEPLOY-v1.0

## 2026-06-22

- 修复每日复盘六项黄灯项：文件完整性、系统心跳、测试、操作日志、API服务、备份状态。
- 修复 longhun-daemon 健康检查 daemon_state.json PID 记录。
- 修复 macOS 日历写入 AppleScript 语法错误。
- 新增基础回归测试 `tests/test_longhun_basic.py`。
- 优化自动化评估脚本，改用项目真实路径与 CNSH 终端 CLI。

## 2026-06-21

- 完成 longhun-daemon 真实服务挂载与四阶段启动。
- DNA 对齐率达 99.6%，重复 DNA 清零。

---

君子协议：本文件受龍魂 DNA 追溯保护。
