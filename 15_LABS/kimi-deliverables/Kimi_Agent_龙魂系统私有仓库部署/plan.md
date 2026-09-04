**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙申·戊辰·丁巳·䷯井-CODE-补DNA-64879f7d
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 龍魂私有仓库（Docker Registry）鲲鹏部署 · 执行蓝图

## 任务
参考 CSDN 文章《Docker 镜像不求人：从 0 到 1 在自己家里搭一个 13GB 的私有仓库》，
为龍魂系统在华为鲲鹏服务器（ARM64 / openEuler 系）上部署私有 Docker 镜像仓库，
输出一键可复制的部署脚本 + 工程文档，对齐龍魂协议（DNA 追溯、四层命名、P0 焊死）。

## 阶段
- Stage 1 — 情报采集（explore subagent）
  - 抓取 CSDN 参考文章核心步骤（Harbor/registry 方案、13GB 仓库做法）
  - 输出：方案要点清单
- Stage 2 — 工程落地（coder subagent，加载 vibecoding-general-swarm）
  - 产出鲲鹏 ARM64 适配的部署包：
    1. `deploy_registry.sh` 一键部署脚本（Docker + registry:2 / Harbor 轻量方案）
    2. 认证 + TLS + 开机自启 + 磁盘监控（对接华为云扣费监控思路）
    3. Mac 终端推送/拉取镜像操作手册（复制粘贴级）
    4. 龍魂四层命名 + DNA 追溯码（新干支格式，标注待本地生成器校正）
  - 输出：/mnt/agents/output/longhun-registry/ 完整包
- Stage 3 — 校验（verifier subagent）
  - 脚本语法检查、ARM64 镜像可用性核对、文档完整性
- Stage 4 — 交付
  - 打包 tar.gz，KIMI_REF 交付

## 约束
- 用户是代码小白：所有指令必须一键复制级，无废话
- 鲲鹏 ARM64 架构，所有镜像必须有 arm64 manifest
- 敏感链接用快速链接形式呈现
