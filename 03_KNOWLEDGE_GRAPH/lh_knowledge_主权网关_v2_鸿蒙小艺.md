# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂系统·主权代理网关 v2.0（鸿蒙 + 小艺完整接入）

> 作者：龍芯北辰·UID9622
> 发布时间：2026-08-15
> 来源：longhun-system/08_BIN/lh_sovereign_gateway.py
> 入库DNA：#龍芯⚡️丙午·丁酉·辛卯·丙申-SOVEREIGN-GATEWAY-v2.0-UID9622

---

> 你是唯一主权人。
> 所有外部工具只能通过主权代理接口访问，不能直连鲲鹏。
> 鸿蒙生态作为最广泛的端侧入口，将龍魂能力带给每一台华为设备。

---

## P0 核心原则

1. 只有 UID9622 可直连鲲鹏服务器
2. 所有代理（Kimi / CodeBuddy / Notion / Mac / 鸿蒙 / 小艺）必须经网关
3. 认证三重：DNA 追溯码 + GPG/HMAC 签名 + 设备证书/会话绑定
4. 数据主存储不出境
5. 全链路入史官审计

---

## P1 系统架构

```
外部工具层
    │
    ▼
主权代理网关 (Sovereign Gateway) v2.0
    • DNA + GPG 验证
    • 鸿蒙设备指纹绑定
    • 小艺会话ID绑定
    • 三色审计 + 史官记录
    │
    ▼
鲲鹏服务器 ( sovereignty core )
    • UID9622 身份锚定
    • 数据主存储
    • 鸿蒙设备统一认证中心
```

---

## P2 关键端点

| 端点 | 用途 |
|---|---|
| `GET /` | 网关状态 |
| `GET /api/sovereign/status` | 主权状态、设备列表、会话列表 |
| `POST /api/proxy/{target}` | 认证转发到下游服务 |
| `POST /api/harmony/register` | 鸿蒙设备注册 |
| `POST /api/harmony/revoke` | 撤销鸿蒙设备 |
| `POST /api/xiaoyi/session/start` | 启动小艺会话 |
| `POST /api/xiaoyi/session/end` | 结束小艺会话 |
| `GET /api/audit` | 审计日志 |
| `GET /api/shame` | 耻辱墙 |

---

## P3 文件位置

- 网关核心：`08_BIN/lh_sovereign_gateway.py`
- 鸿蒙 SDK：`integrations/harmonyos/longhun_sdk/entry/src/main/ets/longhun/LonghunClient.ets`
- 小艺配置：`integrations/xiaoyi/skill.xml`
- 部署脚本：`deploy_sovereign_gateway.sh`

---

## P4 验证命令

```bash
# 状态
curl http://127.0.0.1:8766/

# 注册鸿蒙设备
curl -X POST http://127.0.0.1:8766/api/harmony/register \
  -H "Content-Type: application/json" \
  -d '{"device_id":"HM-001","device_name":"Mate60 Pro"}'

# 启动小艺会话
curl -X POST http://127.0.0.1:8766/api/xiaoyi/session/start \
  -H "Content-Type: application/json" \
  -d '{"user_id":"UID9622"}'
```

---

## 签章

```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#龍芯⚡️丙午·丁酉·辛卯·丙申-SOVEREIGN-GATEWAY-v2.0-UID9622
```

---

> 不是直连，是代理。
> 不是信任，是验证。
> 不是开放，是主权。
