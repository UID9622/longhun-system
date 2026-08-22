# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂 · 鲲鹏 openEuler 部署指南

> DNA: `#龍芯⚡️丙午·甲午·辛巳·甲午·䷃蒙-KUNPENG-DEPLOY-GUIDE-v2.0`

---

## 你只需要做 2 件事

**① 把鲲鹏服务器插上 mgmt 网口（和你 Mac 同一个网络）**

**② 打开终端，输入这 3 行命令：**

```bash
cd ~/longhun-system
bash deploy/connect-kunpeng.sh config   # 输入 IP + 用户名（30 秒）
bash deploy/connect-kunpeng.sh deploy   # 输入密码 → 后面全自动
```

就这。配置时问 3 个问题：
| 问题 | 示例 | 说明 |
|------|------|------|
| mgmt IP 地址 | `192.168.1.100` | 服务器管理口 IP |
| SSH 用户名 | `root` | 直接回车默认 root |
| SSH 端口 | `22` | 直接回车默认 22 |

`deploy` 时问一次密码，之后系统自动生成密钥替换密码，以后永远不用再输。

---

## 一键部署做了什么

```
deploy 命令 = 5 步全自动
  ├ ① 密码连接 → 生成 ED25519 密钥 → 装到服务器（以后免密）
  ├ ② 检测服务器 CPU/内存/磁盘/系统版本/Python
  ├ ③ 安装 openEuler 环境（Python3/nginx/gcc/firewall/SELinux）
  ├ ④ rsync 同步整个龍魂系统文件
  └ ⑤ 创建 systemd 守护服务 + 启动 + 防火墙放行
```

完成后你就可以在浏览器打开 `http://<IP>:9627/` 看到龍魂操作台。

---

## 日常命令

```bash
bash deploy/connect-kunpeng.sh sync     # 代码改了，增量同步过去
bash deploy/connect-kunpeng.sh check    # 看看服务器状态
bash deploy/connect-kunpeng.sh ssh      # SSH 连上去自己玩
```

---

## 服务端口

| 端口 | 服务 |
|------|------|
| 22 | SSH 管理 |
| 80 | Nginx 反代 |
| 9627 | 龍魂 Dashboard 直连 |
| 8777 | 龍魂核心 API |

---

## 故障排查

```bash
# 连不上？测试一下
ping <鲲鹏 IP>

# 服务挂了？
ssh 上去 → systemctl status longhun-core longhun-dashboard

# 重新部署
bash deploy/connect-kunpeng.sh deploy
```

---

## 脚本清单

| 文件 | 用途 |
|------|------|
| `connect-kunpeng.sh` | **总控** — 配置/连接/部署/同步 |
| `prepare-openEuler.sh` | openEuler 环境安装（dnf 装全家桶） |
| `sync-to-kunpeng.sh` | rsync 搬迁（dry/full 双模式） |
| `setup-systemd.sh` | systemd + Nginx 配置（已集成到 deploy） |
| `.env.kunpeng.example` | 环境变量参考 |
