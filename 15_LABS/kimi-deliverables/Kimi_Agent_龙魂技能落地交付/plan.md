# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-64879f7d
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 🐉 龍魂 · nginx 流量拓扑工程落地交付 · plan.md

## 任务判定
- 类型：落地交付（实战工程类）→ 触发记忆34「补全模板v1.0十大类过堂」+ 记忆35「实战交付模板三大件」+ 记忆37「模板引擎焊死格式」+ 记忆32「DNA生成器干支算法禁手写」
- 输入：3份稿件（nginx反向代理焊死配置v1.0 / 流量拓扑完整设计v1.0 / 全节点部署手册）
- 交付物：可直接上华为云鲲鹏服务器执行的一键部署工程包（配置+脚本+服务代码+systemd+监控+验证）+ 落地交付报告

## 阶段分解

### Stage 0 · 口径基座（主agent亲自执行，P0不外包）
- 0.1 重建 DNA 干支生成器 `bin/lh_dna_generator.py`（真实算法：四柱干支以节气/历法锚点计算，卦名按日序取六十四卦；禁手写）
- 0.2 重建模板引擎 `/mnt/agents/output/龍魂智能模板引擎/template_engine.py`（头部元数据→固定模块顺序→字符级签名块→validate核验，三色退出码0/1/2）
- 0.3 用生成器算出 2026-08-13 真实干支，替换稿件中全部手写干支

### Stage 1 · 十大类过堂审查（reviewer subagent）
- 按补全模板A~J十大类审查3份稿件，输出缺陷清单（已知疑点对）：
  - A口径：手写干支🔴 ×3处、DNA未对齐注册表
  - B算法实证：稿件代码均未真跑、无锚点断言
  - C安全：autoindex on 对外暴露目录列表🔴、`if` 嵌套在 location 内的 nginx 经典坑、SSL会话票据/证书路径
  - F工程完整：deploy脚本中配置是占位符「(完整配置见上方)」🔴、缺requirements.txt、缺systemd单元、/var/log/longhun目录未建、nohup裸奔无守护
  - G运维：无回滚实测、Prometheus告警规则引用不存在的metric名
  - E诚实边界：监控指标全是纸面目标值，需标🟡
- 输出：修正清单 → 喂给 Stage 2

### Stage 2 · 工程实现（coder subagent，加载 vibecoding-general-swarm）
- 产出 `/mnt/agents/output/longhun-flow-deploy/` 工程包：
  - conf/nginx/nginx.conf + sites-available/longhun（完整版，非占位符）
  - 08_BIN/ 三个 FastAPI 服务（api_gateway:8970 / collab_hub:19622 / chat_bridge:18799）+ historian/shame_wall 审计模块
  - systemd 单元 ×3（替代nohup裸奔）
  - requirements.txt、deploy.sh（幂等、可回滚、含前置检查）、rollback.sh
  - health_check.sh + crontab 片段
  - README_DEPLOY.md（部署流程图/验证清单/故障排查）
- 全部 DNA 头由 Stage 0 生成器输出注入

### Stage 3 · 真机实测（verifier subagent 沙箱实测）
- Python服务：pip安装依赖→逐个启动→curl健康检查→DNA头校验→审计落盘断言（锚点断言）
- nginx配置：沙箱安装nginx→`nginx -t`语法核验→（443/域名不可达的项标🟡待验，不许谎报）
- 输出：实测报告（跑过什么/没跑过什么）

### Stage 4 · 交付封装（主agent）
- 落地交付报告走模板引擎焊死格式 → validate 核验 🟢 方可交付
- 打包 tar.gz → /mnt/agents/output/
- 回复固定三段：修正了什么 / 保留了什么 / 实测了什么

## 技能加载表
| 阶段 | 技能/工具 |
|:---|:---|
| Stage 0 | 无（主agent手写基座） |
| Stage 1 | reviewer preset（补全模板十大类内联进prompt） |
| Stage 2 | vibecoding-general-swarm（阶段开始时读SKILL.md） |
| Stage 3 | verifier preset |
| Stage 4 | 模板引擎 validate |
