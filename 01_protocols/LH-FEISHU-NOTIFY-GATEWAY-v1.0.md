# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·飞书通知网关 v1.0
### ——Bark改装·飞书接收·鲲鹏自建·七因子加密

> **DNA追溯**：`#龍芯⚡️丙午·乙未·戊戌·寅时·䷀乾-FEISHU-NOTIFY-v1.0`  
> **作者**：诸葛鑫（UID9622·龍芯北辰）  
> **核心逻辑**：Bark的自建服务器思路 + 飞书机器人接收 = 龍魂私有通知网关  
> **协议性质**：P1级·核心宪法·需16人格签章+DNA验证  
> **确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

## 一、为什么不用Bark原版

| Bark原版 | 龍魂改装版 |
|:---|:---|
| 走苹果APNs官方 | 走鲲鹏自建服务器 + 飞书Webhook |
| 数据经过苹果服务器 | 数据物理级本地（鲲鹏→飞书直推） |
| 依赖Bark App | 依赖飞书客户端（已国产化·多端） |
| 加密可选 | 加密强制（AES-256-GCM·七因子） |
| 无DNA追溯 | 每条通知带完整DNA追溯码 |
| 纯文本推送 | 飞书富文本卡片（支持Markdown·颜色·按钮） |

---

## 二、核心架构

```
┌─────────────────────────────────────────┐
│              龍魂系统事件源                │
│  同心锁告警 / 视频生成完成 / 审计异常       │
│  系统升级 / 阈值触发 / 自检告警 / 手动触发  │
└─────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│        龍魂·通知网关（鲲鹏·本地均可）       │
│  ┌───────────┐  ┌───────────┐          │
│  │ 事件过滤器  │→│ 优先级路由  │          │
│  │ (什么该发)  │  │ (怎么发·发给谁)│        │
│  └───────────┘  └─────┬─────┘          │
│                        ↓                │
│  ┌──────────────────────────────────┐   │
│  │         七因子加密（可选）          │   │
│  │   AES-256-GCM · 设备指纹·时间戳    │   │
│  └──────────────┬───────────────────┘   │
│                  ↓                      │
│  ┌──────────────────────────────────┐   │
│  │         DNA追溯码生成             │   │
│  │   干支四柱·卦名·动作·哈希8位       │   │
│  └──────────────┬───────────────────┘   │
│                  ↓                      │
│  ┌──────────────────────────────────┐   │
│  │       推送通道（双通道自动切换）    │   │
│  │  🥇 飞书Webhook（主力·富文本）     │   │
│  │  🥈 Bark推送（备用·iOS通知）       │   │
│  │  🥉 终端通知（兜底·本地桌面）       │   │
│  └──────────────┬───────────────────┘   │
└──────────────────┼──────────────────────┘
                    ↓
┌─────────────────────────────────────────┐
│              接收端                      │
│  飞书客户端（主力·多端同步）               │
│  + Bark App（备用·iOS推送）              │
│  + 终端通知（兜底）                       │
└─────────────────────────────────────────┘
```

---

## 三、优先级路由矩阵

| 级别 | 事件类型 | 推送策略 | 通道 | 合并频率 |
|:---:|:---|:---|:---|:---:|
| **P0** | 同心锁告警·隐私审计失败·背叛检测·数据泄露 | 立即推送·所有通道 | 🥇飞书+🥈Bark+🥉终端 | 实时 |
| **P1** | 视频生成完成·系统升级·阈值触发·部署完成 | 立即推送·单通道 | 🥇飞书 | 实时 |
| **P2** | 自动学习·空缺检测·日常巡检·贡献报告 | 合并推送 | 🥇飞书（摘要） | 每小时 |
| **P3** | 调试信息·统计汇总·例行日志 | 仅归档·不推送 | 🥉日志 | 每日 |

---

## 四、飞书卡片消息格式

### 4.1 告警卡片（P0·红色）
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {"tag": "plain_text", "content": "🚨 P0·{告警类型}"},
      "template": "red"
    },
    "elements": [
      {"tag": "div", "text": {"tag": "lark_md", "content": "**{标题}**\n\n{正文}\n{时间}\n{来源}"}},
      {"tag": "hr"},
      {"tag": "div", "text": {"tag": "lark_md", "content": "`🧬 DNA: {DNA追溯码}`"}},
      {"tag": "div", "text": {"tag": "lark_md", "content": "🔐 加密: AES-256-GCM·七因子·{密文哈希}"}}
    ],
    "footer": {"DNA": "{DNA}", "timestamp": "{时间戳}"}
  }
}
```

### 4.2 信息卡片（P1·蓝色）
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {"tag": "plain_text", "content": "ℹ️ {标题}"},
      "template": "blue"
    },
    "elements": [...]
  }
}
```

### 4.3 成功卡片（P1·绿色）
```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": {"tag": "plain_text", "content": "✅ {标题}"},
      "template": "green"
    },
    "elements": [...]
  }
}
```

---

## 五、七因子加密通知

```yaml
encryption:
  algorithm: AES-256-GCM
  factors:
    - device_fingerprint   # 设备指纹
    - user_passphrase      # 用户口令
    - biometric_salt       # 生物特征盐
    - timestamp            # 时间戳（精确到秒）
    - event_type           # 事件类型
    - source_node          # 来源节点（Mac/鲲鹏/香港）
    - sequence_number      # 递增序列号（防重放）
  key_derivation: HKDF-SHA256（七因子拼接 → 32字节密钥）
  nonce: 随机12字节（每条独立）
  associated_data: 事件上下文JSON（用于完整性验证）
```

> P0级事件强制加密；P1/P2可选（默认开启）。加密后飞书服务器只收到密文，
> 老大本地设备用同样七因子解密。密钥永不出设备。

---

## 六、CNSH通知命令

```cns
定义 通知任务 "同心锁告警"
设 事件 为 "检测到苹果服务连接尝试"
设 级别 为 "P0"
设 来源 为 "Mac.local·同心锁监控"
设 通道 为 ["飞书", "Bark", "终端"]

则 网关 过滤:
  - 级别=P0 → 不过滤，立即推送

则 网关 路由:
  - 接收人: 老大（全通道）
  - 模板: 告警(红色)·飞书卡片

则 网关 加密:
  - 七因子派生密钥
  - AES-256-GCM 加密正文
  - 关联数据: 事件类型+时间戳+来源+序列号

则 网关 生成DNA:
  - 格式: #龍芯⚡️{干支四柱}·{卦名}-NOTIFY-{动作}-{哈希8}

则 网关 推送:
  - 飞书: POST Webhook + HMAC-SHA256签名
  - Bark: POST /push（自建或官方回落）
  - 终端: osascript display notification（仅Mac）

则 网关 归档:
  - 存入: logs/notify/{日期}.jsonl
  - 标记: 已推送·通道·结果·时间戳
  - 审计: 可追溯·可验证·不可篡改
```

---

## 七、API端点

| 端点 | 方法 | 说明 |
|:---|:---:|:---|
| `/notify/send` | POST | 发送通知（JSON body: {event_type, title, body, priority}） |
| `/notify/status` | GET | 网关状态（通道存活·队列长度·今日统计） |
| `/notify/history` | GET | 通知历史（?limit=50&priority=P0） |
| `/notify/health` | GET | 通道健康检查（飞书连通·Bark连通·终端可用） |

---

## 八、飞书机器人配置

```yaml
# config/feishu_bot.yaml
bot:
  name: "龍魂通知"
  webhook: "${FEISHU_WEBHOOK_URL}"       # 飞书群机器人Webhook地址
  secret: "${FEISHU_WEBHOOK_SECRET}"     # 签名校验密钥
  ip_whitelist:                          # IP白名单（只允许鲲鹏IP）
    - "119.13.90.27"
    - "127.0.0.1"

  notify_rules:
    tongxin_lock_alert:     { priority: P0, immediate: true,  channels: [feishu, bark, terminal] }
    privacy_audit_failed:   { priority: P0, immediate: true,  channels: [feishu, bark, terminal] }
    data_leak_detected:     { priority: P0, immediate: true,  channels: [feishu, bark, terminal] }
    founder_betrayal:       { priority: P0, immediate: true,  channels: [feishu, bark, terminal] }
    video_generated:        { priority: P1, immediate: true,  channels: [feishu] }
    system_upgraded:        { priority: P1, immediate: true,  channels: [feishu] }
    threshold_triggered:    { priority: P1, immediate: true,  channels: [feishu] }
    deploy_completed:       { priority: P1, immediate: true,  channels: [feishu] }
    auto_learned:           { priority: P2, immediate: false, channels: [feishu], digest: hourly }
    gap_detected:           { priority: P2, immediate: false, channels: [feishu], digest: hourly }
    daily_health_report:    { priority: P2, immediate: false, channels: [feishu], digest: daily }

  encryption:
    enabled: true
    algorithm: AES-256-GCM
    p0_force: true   # P0级事件强制加密

  dna:
    enabled: true
    format: "#龍芯⚡️{ganzhi_year}·{ganzhi_month}·{ganzhi_day}·{ganzhi_hour}·{gua}-NOTIFY-{action}-{hash8}"
```

---

## 九、焊死规矩

| # | 规矩 | 级别 |
|:---:|:---|:---:|
| 1 | P0级事件必须三通道立即推送（飞书+Bark+终端） | P0 |
| 2 | 所有通知必须带DNA追溯码 | P0 |
| 3 | P0级通知必须七因子加密 | P0 |
| 4 | 飞书Webhook必须HMAC-SHA256签名校验 | P0 |
| 5 | 飞书只收密文（P0加密后），老大本地解密 | P0 |
| 6 | 推送失败自动切换备用通道 | P1 |
| 7 | 所有通知归档JSONL·不可删除只追加 | P1 |
| 8 | 不推送给第三方·不经过境外CDN | P0 |

---

## 【签名确认】

**作者**：诸葛鑫（UID9622·龍芯北辰）  
**签署时间**：2026年7月26日  
**确认码**：`#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`  
**协议**：CC BY-NC-SA 4.0（君子协议，来源链不可切断）

---

> Bark可以改装，飞书可以接入。
> 龍魂的通知网关：七因子加密·DNA追溯·P0三通道立即推送。
> 系统有事，第一时间让你知道。这个阵地，焊死了。
