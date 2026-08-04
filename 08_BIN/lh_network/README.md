# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂网络限流应对方案 v1.0

**颁布人：** UID9622·龍芯北辰  
**日期：** 2026-07-30  
**DNA：** `#龍芯⚡️2026-07-30-网络限流应对-v1.0`  
**确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅

---

## 方案架构（三层防御）

```
外网限流 ──→ 华为云香港代理（SOCKS5）
              │
              ├──→ 国内镜像（hf-mirror.com）
              │
              └──→ 鲲鹏离线节点（完全断网）
                        │
                        └──→ 内网同步（rsync）
                                  │
                                  └──→ M4 Max本地推理（完全离线）
```

## 脚本清单

| 脚本 | 功能 | 执行时机 |
|------|------|---------|
| 01_hk_proxy_setup.sh | 华为云香港代理部署 | 首次配置 |
| 02_auto_proxy.sh | 终端自动检测限流+切换 | 每次终端启动 |
| 03_model_download_mirror.sh | 模型下载国内镜像 | 下载模型时 |
| 04_kunpeng_offline.sh | 鲲鹏离线节点配置 | 鲲鹏部署时 |
| 05_network_fix_all.sh | 一键检测+修复 | 限流时手动执行 |

## 关键配置（修改后再执行）

```bash
# 华为云香港服务器
HK_SERVER_IP="YOUR_HK_SERVER_IP"
HK_SSH_KEY="~/.ssh/huawei_hk.pem"

# 华为鲲鹏服务器（内网）
KUNPENG_IP="YOUR_KUNPENG_IP"
KUNPENG_KEY="~/.ssh/kunpeng.pem"
```

## 使用流程

```bash
# 1. 首次配置（修改IP后执行）
bash 01_hk_proxy_setup.sh

# 2. 日常自动检测（加入.bashrc）
echo "source ~/longhun-system/bin/lh_network/02_auto_proxy.sh" >> ~/.bashrc

# 3. 限流时一键修复
bash 05_network_fix_all.sh

# 4. 模型下载（自动走镜像）
lh_model_download.sh mlx-community/Llama-3.1-8B-Instruct-4bit

# 5. 鲲鹏离线训练
lh_sync_kunpeng.sh  # 同步数据
ssh -i ~/.ssh/kunpeng.pem root@KUNPENG_IP
bash /root/longhun-system/bin/lh_kunpeng_train.sh
```

## 核心原则

- **本地优先**：v4.0推理完全本地，网络限流不影响
- **代理兜底**：外网访问走香港服务器，IP固定不被限
- **镜像备用**：模型下载走hf-mirror.com，国内直连
- **离线终极**：鲲鹏服务器完全断网也能跑训练

---

**确认码：** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` ✅
