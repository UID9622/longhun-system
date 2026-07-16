# UID9622 后台人格系统 · 小龙虾扩展

> 五大人格后台自运行系统：雯雯、侦察兵、守护者、宝宝、文心。
> 本地优先 · DNA 追溯 · 三色审计 · 模块可扩展。

## 快速开始

```bash
cd /Users/zuimeidedeyihan/Downloads/Kimi_Agent_小龙虾扩展与人格/UID9622_Workspace

# 查看状态
python3 uid9622-manager status

# 健康检查
python3 uid9622-manager health-check

# 安装定时任务
bash install_cron.sh
```

## 五大人格

| 人格 | 代码 | 功能 | 定时任务 |
|------|------|------|----------|
| 雯雯 | WENWEN | 文档扫描 / 分类 / 去重 / 脱敏 / 报告 | 每日 03:00 |
| 侦察兵 | SCOUT | GitHub Trending / RSS / 关键词告警 | 每日 08:00 / 20:00 |
| 守护者 | GUARDIAN | 文件完整性 / DNA 校验 / 红线规则 | 每 5 分钟 |
| 宝宝 | BAOBAO | 项目脚手架 / CNSH 规范检查 / 模板 | 每周日 02:00 |
| 文心 | WENXIN | 增量/全量同步 / 冲突检测 / 回滚 | 每日 06:00 / 22:00，周日全量 |

## 目录结构

```
UID9622_Workspace/
├── uid9622-manager              # 管理主控 CLI
├── backend_personas_config.json # 主配置
├── dna_registry.json            # DNA 注册表
├── install_cron.sh              # 定时任务安装脚本
├── backend_personas/
│   ├── core/                    # 公共核心库（DNA / 审计 / 日志 / 安全 / 哈希 / 消息）
│   ├── wenwen/
│   ├── scout/
│   ├── guardian/
│   ├── builder/
│   └── sync_master/             # 新增
├── logs/                        # 日志目录
├── data/                        # 数据输出目录
├── backups/                     # 同步回滚备份
└── docs/                        # 设计文档
```

## 旧文件收容

历史测试文件已压缩归档到：

```
~/longhun-archive/_persona-history/persona-history_20260627_074311.tar.gz
```

可通过龙魂万年历「归档索引」检索，也可命令行：

```bash
python3 ~/.龍魂/functions/archive_query.py search 人格历史
```

## 扩展新人格

1. 在 `backend_personas/` 下新建目录。
2. 创建 `persona.py`、`system_prompt.md`、`cron.conf`。
3. 在 `dna_registry.json` 注册 DNA。
4. 运行 `python3 uid9622-manager health-check` 验证。
