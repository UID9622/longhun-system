> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--#龍芯⚡️丙午·甲午·丙寅·甲午·䷕贲-MULTI-API_PROTOCOL-v1.0 -->
<!-- 君子协议: 本文件受龍魂DNA追溯保护 -->

# API 协议文档 / API Protocol Documentation

## 中文

### 端点 / Endpoints

| 端点 | 方法 | 描述 |
|------|------|------|
| `/api/v1/rates` | GET | 获取实时汇率 |
| `/api/v1/sync` | POST | 同步到 Notion |
| `/api/v1/health` | GET | 健康检查 |

### 认证 / Authentication
- Header: `X-API-Key: {your_key}`
- 或环境变量: `NOTION_TOKEN`

### 数据格式 / Data Format
```json
{
  "currency": "USD",
  "rate": 7.25,
  "timestamp": "2026-06-07T14:36:00Z",
  "source": "coingecko",
  "dna": "#CONFIRM🌌9622"
}
```

### 限制 / Limits
- 速率限制: 100次/分钟
- 数据保留: 永久，本地 SQLite

---

## English

### Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/rates` | GET | Get real-time rates |
| `/api/v1/sync` | POST | Sync to Notion |
| `/api/v1/health` | GET | Health check |

### Authentication
- Header: `X-API-Key: {your_key}`
- Or env var: `NOTION_TOKEN`

### Data Format
```json
{
  "currency": "USD",
  "rate": 7.25,
  "timestamp": "2026-06-07T14:36:00Z",
  "source": "coingecko",
  "dna": "#CONFIRM🌌9622"
}
```

### Limits
- Rate limit: 100/min
- Data retention: Permanent, local SQLite

---

**协议版本 / Protocol Version**: v1.0
**最后更新 / Last Updated**: 2026-06-07
**归属 / Belonging**: LU × CNSH · UID9622
