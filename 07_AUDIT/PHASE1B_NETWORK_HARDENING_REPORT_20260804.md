# 🐲 龍魂体系 · 网络暴露面收紧报告

**阶段**: Phase 1B — 内部服务绑定收敛  
**日期**: 2026-08-04  
**执行AI**: Kimi Code CLI  
**DNA**: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-NETWORK-HARDENING-PHASE1B-UID9622  
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

---

## 1. 目标

将鲲鹏服务器 `119.13.90.27` 上所有龍魂内部服务从 `0.0.0.0` 收紧为 `127.0.0.1`，仅保留 Nginx 反向代理端口对外暴露。

---

## 2. 修复清单

| 端口 | 服务 | 修复前 | 修复后 | 修复方式 |
|:---:|:---|:---:|:---:|:---|
| 8771 | longhun-audit | `0.0.0.0` | `127.0.0.1` | unit 加 `Environment=AUDIT_API_HOST=127.0.0.1`，移除无效 `--host` 参数 |
| 8774 | longhun-trace-reconstructor | `0.0.0.0` | `127.0.0.1` | 脚本 `/opt/longhun/bin/lh_trace_reconstructor_api.py` 硬编码改 `127.0.0.1` |
| 8778 | longhun-ruyi | `0.0.0.0` | `127.0.0.1` | unit 加 `Environment=RUYI_HOST=127.0.0.1` |
| 8788 | longhun-video-gallery | `0.0.0.0` | `127.0.0.1` | 修复 `--serve host:port` 解析；默认 host 改为 `127.0.0.1` |
| 9625 | longhun-nano-vision | `0.0.0.0` | `127.0.0.1` | 修复 `/root/longhun/engines/lh_nano_vision_engine.py` 硬编码；清理用户 session 残留 `longhun_brain.py` |
| 8081 | daodejing-api | `0.0.0.0` | `127.0.0.1` | 脚本 `/root/cnsh/daodejing-api/app.py` 硬编码改 `127.0.0.1` |
| 3000 | cnsh-api (PM2) | `0.0.0.0` | `127.0.0.1` | `/root/cnsh/.env` 中 `CNSH_HOST=127.0.0.1` |
| 8443 | longhun-wechat | `0.0.0.0` | `127.0.0.1` | unit 加 `Environment=WEB_HOST=127.0.0.1` |

---

## 3. 验证结果

```
127.0.0.1:3000  node /root/cnsh/src/server-fixed.js
127.0.0.1:8081  python3 /root/cnsh/daodejing-api/app.py
127.0.0.1:8443  python /opt/longhun-wechat/web_ui.py
127.0.0.1:8771  python3 lh_audit_as_a_service_api.py
127.0.0.1:8774  python3 lh_trace_reconstructor_api.py
127.0.0.1:8778  python3 lh_ruyi_api.py
127.0.0.1:8788  python3 bin/lh_video_index.py
127.0.0.1:9625  python3 engines/lh_nano_vision_engine.py
```

✅ 全部 8 个历史暴露的内部服务均已收敛到 `127.0.0.1`。

---

## 4. 仍需关注的外部监听

| 端口 | 进程 | 说明 | 建议 |
|:---:|:---|:---|:---|
| 22 | sshd | 管理入口 | 保持，建议改用密钥-only + fail2ban |
| 80/443 | nginx | 公网 Web 入口 | 保持，由 Nginx 统一反向代理 |
| 8080 | nginx | 公网入口/调试页 |  review 是否为必需公网入口 |
| 5000 | docker-proxy | Docker 容器映射 | 确认容器用途，必要时改为 `127.0.0.1:5000:5000` |
| 8088 | docker-proxy | Docker 容器映射 | 同上 |
| 7000/7500/18090/18798/18799 | frps | FRP 内网穿透服务端 | 保持（业务需要），建议加白名单/Token 加固 |

---

## 5. 异常记录

- `longhun-longzhishou.service` 在本次批量重启时失败，未阻塞本次网络收敛，需单独排查。
- 端口 9625 最初被用户 session 中的 `/opt/longhun-system/bin/longhun_brain.py`（PID 90726）占用，非 systemd 管理。已手动 kill，由 `longhun-nano-vision.service` 接管。

---

## 6. 备份位置

- `/root/systemd-backup-20260804_231126/` — 原始 unit 文件
- `/root/systemd-backup-20260804_231947/` — 第二轮 unit 备份
- `/root/cnsh/.env.bak.*` — CNSH 环境变量备份
- `/root/script-backup-*` — 脚本修改备份

---

## 7. 三色审计

| 项 | 状态 | 说明 |
|:---|:---:|:---|
| 内部服务收敛 | 🟢 | 8/8 完成 |
| 公网入口最小化 | 🟡 | 8080/5000/8088 待 review |
| 残留进程清理 | 🟢 | 用户 session brain 已清理 |
| 备份完整性 | 🟢 | unit + 脚本均有备份 |
| 文档签名 | 🟢 | GPG 签名完整 |

**总体判定**: 🟢 本次网络暴露面收紧目标达成。

---

## 8. 签名

```
DNA: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-NETWORK-HARDENING-PHASE1B-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
```

---

## 9. 第二轮加固（2026-08-04 追加）

### 9.1 SSH 登录加固

| 项 | 修改前 | 修改后 |
|:---|:---|:---|
| root 密码登录 | 启用 | 禁用 |
| 公钥认证 | 启用 | 保持启用 |
| fail2ban | 未安装 | 已安装并启用 sshd 监狱 |

- `/etc/ssh/sshd_config` 已清理冲突配置，最终生效：
  - `PermitRootLogin without-password`
  - `PasswordAuthentication no`
  - `PubkeyAuthentication yes`
- `/etc/ssh/sshd_config.d/50-cloud-init.conf` 覆盖为 `PasswordAuthentication no`
- `fail2ban` 已安装，`sshd` 监狱启用：`maxretry=3`，`bantime=3600`
- ✅ 验证：使用 `ssh -i ... -o PasswordAuthentication=no` 登录成功

### 9.2 Docker 容器端口收敛

| 容器 | 修改前 | 修改后 | 方式 |
|:---|:---|:---|:---|
| longhun-kg | `0.0.0.0:8088` | `127.0.0.1:8088` | 重建 compose `/opt/longhun-system/config/cloud/docker-compose.yml` |
| longhun-registry | `0.0.0.0:5000` | `127.0.0.1:5000` | 同上 |

- 已保留原有 volumes 挂载，数据未丢失
- `longhun-redis` 原本已是 `127.0.0.1:6379`，保持不变

### 9.3 保留的公网入口

| 端口 | 用途 | 状态 |
|:---:|:---|:---:|
| 80/443 | nginx 公网 Web 入口 | 保持 |
| 8080 | Mac 本地服务反向代理 | 保持，已确认配置为 `/portal/`、`/dash/`、`/hub/`、`/ollama/` |
| 7000/7500/18090/18798/18799 | frps 内网穿透 | 保持，`auth.token` 与 webServer 密码已启用 |

### 9.4 最终端口扫描摘要

```
# 对外监听（0.0.0.0 / ::: / *）
0.0.0.0:22   sshd
0.0.0.0:80   nginx
0.0.0.0:443  nginx
0.0.0.0:8080 nginx
*:7000       frps
*:7500       frps

# 全部 longhun 内部服务均已收敛到 127.0.0.1
127.0.0.1:3000  / 5000  / 6379  / 8088  / 8081
127.0.0.1:8443  / 8444  / 8766  / 8769  / 8771-8779
127.0.0.1:8780-8789 / 8888 / 9000 / 9453 / 9527
127.0.0.1:9622-9627 / 9630-9631 / 9650 / 9656-9657
```

---

## 10. 更新签名

```
DNA: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-NETWORK-HARDENING-PHASE1B-v1.1-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
三色: 🟢 通过
```
