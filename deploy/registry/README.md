# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--
DNA: #龍芯⚡️丙午·乙未·乙丑·兑-REGISTRY-DEPLOY-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
-->
# README — 龍魂私有 Docker 镜像仓库

**这是什么**：在龍魂服务器上跑一个属于自己的 Docker 镜像仓库（`registry:2` + htpasswd 认证 + 可选 TLS），Mac 推拉镜像全走内网，不再受 Docker Hub 限流和断网影响。

**为什么选 registry:2 而不是 Harbor**：registry:2 镜像仅 24MB，官方 multi-arch 直接支持 x86_64/aarch64，一条命令跑起来。Harbor 官方不支持 ARM64，社区方案需要额外编译。选型对比详见 `SPEC.md §0`。

方案参考：[快速链接: CSDN 参考文章] https://blog.csdn.net/Margrop/article/details/163312205（registry:2 私有化路线 + 4大坑，本部署包为其多架构增强版）。

**怎么装**：把 `deploy_registry.sh` 拷到服务器，以 root 执行 `sudo bash deploy_registry.sh` 一条命令完成（自动检测架构、装 Docker、生成随机密码、起容器、systemd 开机自启、磁盘 80% 告警），结尾打印的账号密码立即抄走。细节见 `SPEC.md`。

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
