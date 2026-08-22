<!--
#龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-REGISTRY-DEPLOY-v1.0
# 注：干支以本地生成器 bin/lh_dna_generator.py 输出为准，禁止手写
# 署名：龍芯北辰 UID9622
-->
# README — 龍魂私有 Docker 镜像仓库（鲲鹏版）

**这是什么**：在华为鲲鹏服务器（ARM64）上跑一个属于龍魂自己的 Docker 镜像仓库（`registry:2` + htpasswd 认证 + 可选 TLS），Mac M4 Max 推拉镜像全走内网，不再受 Docker Hub 限流和断网影响。方案参考 CSDN 文章的 registry:2 私有化路线并做鲲鹏适配：[快速链接: 参考文章] https://blog.csdn.net/Margrop/article/details/163312205。

**怎么装**：把 `deploy_registry.sh` 拷到鲲鹏服务器，以 root 执行 `bash deploy_registry.sh` 一条命令完成（自动检测 aarch64、装 Docker、生成随机密码、起容器、开机自启、磁盘 80% 告警），结尾打印的账号密码立即抄走。细节见 `SPEC.md`。

**怎么用**：在 Mac 上按 `mac_client_setup.md` 配一次白名单 → `docker login` → `docker tag/push/pull` 三步走；日常删除镜像、备份恢复、磁盘告警、华为云扣费监控见 `ops_handbook.md`。

## 文件清单

| 文件 | 用途 |
|---|---|
| SPEC.md | 架构、端口、数据卷、安全边界 |
| deploy_registry.sh | 鲲鹏端一键部署脚本（bash -n 自检通过） |
| mac_client_setup.md | Mac 终端复制粘贴手册 |
| ops_handbook.md | 运维手册（查/删/备份/告警/扣费监控） |
| README.md | 本文件 |

## 关于文件头的干支占位符（bin/lh_dna_generator.py）

本包各文件头部注释中的 `{年干支}·{月干支}·{日干支}·{卦名}` 为占位符，由龍魂本地系统的干支生成器 `bin/lh_dna_generator.py` 生成回填。该生成器属于龍魂本地系统，**不在本部署包内**，请勿在本包目录中查找或手写干支。

部署前若手头没有生成器：可暂时保留占位符原样部署，不影响任何功能；待本地生成器产出干支后再回填各文件头注释即可。按"旧DNA不追溯改写"原则，回填只改本包文件头，已生成的旧DNA不做追溯改写。
