# UID9622 五大后台人格部署计划

## 目标
将五大后台自运行人格从配置文档转化为实际可运行的自动化系统。

## 五大人格
1. **P-AK-WENWEN** 雯雯·技术整理师 - 文档整理/知识结构化
2. **P-AK-SCOUT** 侦察兵·信息猎手 - 信息收集/数据调研
3. **P-AK-GUARDIAN** 上帝之眼·守护者 - 安全监控/三色审计
4. **P-AK-BUILDER** 宝宝·构建师 - 系统构建/架构设计
5. **P-AK-SYNC-MASTER** 文心·同步专家 - 数据同步/协调管理

## 阶段

### Stage 1: 基础环境搭建
- 创建工作目录结构
- 初始化DNA注册表
- 创建配置文件（backend_personas_config.yaml）
- 创建管理主脚本（uid9622-manager）

### Stage 2: 人格部署（并行）
- 部署雯雯：整理脚本 + cron定时任务
- 部署侦察兵：信息收集框架 + RSS源配置
- 部署上帝之眼：监控脚本 + 审计规则
- 部署宝宝：构建工具链 + 模板库
- 部署文心：同步引擎 + 冲突检测

### Stage 3: 协作链路配置
- MCP协议通信配置
- 人格间消息路由
- 触发链设置

### Stage 4: 系统验证
- 启动所有人格
- 验证cron任务
- 测试协作链路
- 生成分署报告

## 技能加载
- Stage 1: longhun-system（体系框架）+ longhun-daemon（守护进程）
- Stage 2: longhun-governance（治理层/安全）+ longhun-automation（自动化）
- Stage 3: longhun-daemon（服务管理）
- Stage 4: longhun-integration（集成测试）
