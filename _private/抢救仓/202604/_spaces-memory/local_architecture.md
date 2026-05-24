---
name: UID9622 本地架构全景
description: 龍魂系统本地服务、API端点、工具箱完整清单，用于后续对接和规划
type: reference
---

## 本地运行服务
- `:9622` 龍魂API（CNSH-64）— 🟢运行中，9层治理引擎，15个端点
- `:11434` Ollama本地 — 🟢运行中，9个模型
- `:8765` 龍魂本地服务 — 🔴无响应（审计+三色，需修复）
- `:8081` 三才流场 — 天地人推演引擎（用户提到要对接:9622）

## :9622 API 端点
- `/` GET 系统状态
- `/yang/create` POST 阳链·创建DNA记录
- `/yang/embed` POST 阳链·嵌入DNA水印
- `/yin/trace/{dna}` GET 阴链·DNA追溯查询
- `/yin/extract` POST 阴链·提取DNA
- `/sweeper/scan` POST 扫描检测
- `/wechat/config` POST 微信配置
- `/wechat/test` POST 微信测试
- `/confront/generate` POST 维权证据包生成
- `/confront/download/{id}` GET 下载证据包
- `/evidence/chain/{dna}` GET 证据链查询
- `/audit/blacklist` GET 审计黑名单
- `/audit/add_blacklist` POST 添加黑名单
- `/library` GET 知识库
- `/library/log` POST 知识库日志

## 本地工具箱（50 Python + 45 Shell）
- code_audit.py — 三色代码审计
- persona_router.py — P01-P15人格路由
- cnsh_editor.py / cnsh_terminal.py / cnsh_cli.py — CNSH引擎
- cnsh-core/ 17个模块
- dna_classifier.py — DNA分类
- data_sovereignty.py — 数据主权保护
- fuxi_taiji_engine.py — 太极算法引擎
- empower_engine.py — 赋能系统
- fuse_api.py — 熔断接口
- auto_audit.py — 自动审计
- core/mcp_server.py / mcp_mini.py — MCP服务

## 启动方式
- 统一用 `启动所有服务.sh` 拉起
- 散装在 bin/ 目录，未打包

## 终端宝宝（Claude Code CLI）
- 25个记忆文件
- 钥匙文件：~/longhun-system/config/baobao_master_key.json
- 调度中枢：~/longhun-system/core/baobao_dispatcher.py
- 权限校验：~/longhun-system/core/baobao_authority.py

## Notion已完成
- 五大神兽花名册已写入
- CNSH路由器代理 v1.0
- 龍慧·三才知识撰写官
- 人格路由API规则 v2.0
- 数字根熔断+意图识别已接入
