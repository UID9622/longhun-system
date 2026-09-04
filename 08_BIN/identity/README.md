# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·主权人格身份系统

**DNA**: `#龍芯⚡️丙午·乙未·丁酉·亥时·䷀乾-IDENTITY-v1.0`  
**确认码**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

本地身份密钥 + 设备指纹 + 行为密码学 + 鲲鹏服务端验证。

---

## 设计原则

1. **私钥不出本地**：Ed25519 私钥物理隔离存储于 `~/.longhun/identity/`，权限 `0600`，不入 git、不上云。
2. **公钥注册鲲鹏**：公钥 `data/resident_registry/uid9622_identity.pub` 同步到鲲鹏服务端，用于验证签名。
3. **一次性签名**：每次广播带 session nonce 与时间戳，服务端拒绝重放。
4. **设备指纹脱敏**：所有硬件敏感字段均哈希处理，原始数据不落盘。
5. **行为密码学**：采集打字节奏、停顿模式、高频命令，形成 UID9622 专属行为轮廓。

---

## 文件结构

| 文件 | 角色 |
|:---|:---|
| `lh_identity_keygen.py` | 生成 UID9622 身份密钥对 |
| `lh_identity_core.py` | 设备指纹、行为密码学、广播信号、签名验证 |
| `lh_identity_client.py` | 本地生成主权人格广播信号 |
| `lh_identity_server.py` | 鲲鹏端 FastAPI 验证服务 |
| `lh_behavior_trainer.py` | 交互式行为密码学训练 |
| `README.md` | 本文件 |

---

## 依赖

```bash
pip install cryptography fastapi uvicorn pydantic
```

---

## 使用流程

### 第一步：生成身份密钥

```bash
python3 bin/identity/lh_identity_keygen.py --passphrase "你的强口令"
```

产出：
- `~/.longhun/identity/uid9622_private.enc`（私钥，权限 0600）
- `data/resident_registry/uid9622_identity.pub`（公钥）
- `data/resident_registry/uid9622_identity.json`（元数据）

### 第二步：训练行为密码学

```bash
python3 bin/identity/lh_behavior_trainer.py --rounds 5
```

产出：
- `state/identity_behavior.json`（行为轮廓）
- `state/identity_device_fp.hash`（当前设备指纹哈希）

### 第三步：生成并发送广播信号

```bash
# 本地生成
python3 bin/identity/lh_identity_client.py --passphrase "你的强口令"

# 通过 HTTPS 公网验证（推荐）
python3 bin/identity/lh_identity_client.py \
  --passphrase "你的强口令" \
  --send https://uid9622.cn/identity/identify

# 或直连鲲鹏内网端口（需安全组开放 8772）
python3 bin/identity/lh_identity_client.py \
  --passphrase "你的强口令" \
  --send http://119.13.90.27:8772/identify
```

---

## 鲲鹏部署

### 1. 同步公钥到鲲鹏

```bash
scp data/resident_registry/uid9622_identity.pub \
  data/resident_registry/uid9622_identity.json \
  root@119.13.90.27:/opt/longhun-system/data/resident_registry/
```

### 2. 注册设备指纹与行为轮廓

首次在本地训练后，把 `state/identity_device_fp.hash` 和 `state/identity_behavior.json` 同步到鲲鹏：

```bash
scp state/identity_device_fp.hash \
  state/identity_behavior.json \
  root@119.13.90.27:/opt/longhun-system/state/
```

### 3. 启动验证服务

```bash
python3 bin/identity/lh_identity_server.py --host 0.0.0.0 --port 8772
```

> 注意：8771 端口已被审计即服务占用，身份服务使用 8772。公网访问通过 Nginx `https://uid9622.cn/identity/` 反代。

建议用 systemd 守护：

```ini
# /etc/systemd/system/longhun-identity.service
[Unit]
Description=LongHun Sovereign Identity Service
After=network.target

[Service]
Type=simple
User=longhun
WorkingDirectory=/opt/longhun-system
ExecStart=/usr/bin/python3 /opt/longhun-system/bin/identity/lh_identity_server.py --host 0.0.0.0 --port 8772
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

---

## 广播信号格式

人类可读形式：

```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z|<base64_payload>
```

完整 JSON 载荷包含：
- `confirm_code`: 主权确认码
- `uid`: 9622
- `dna`: 系统 DNA 标签
- `timestamp`: ISO UTC 时间戳
- `session_nonce`: 一次性随机 nonce
- `device_fingerprint`: 设备指纹（脱敏）
- `behavior_profile`: 行为轮廓（可选）
- `signature`: Ed25519 签名

---

## 安全注意事项

- 私钥文件 `uid9622_private.enc` 必须保持 `0600` 权限。
- 不要用弱口令加密私钥。
- 服务端不存储任何私钥，只验证公钥签名。
- 行为轮廓样本越多，识别越稳定；建议至少训练 5 轮。
- 临时签名 `LK9X-772Z` 仅本次会话有效，服务端不长期存储。

---

> v1.0 · 2026-07-24 · 龍魂主权人格广播协议
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
