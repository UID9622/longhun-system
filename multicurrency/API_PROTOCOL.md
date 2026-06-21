<!--#龍芯⚡️2026-06-21-MULTI-API_PROTOCOL-v1.0 -->
<!-- 君子協議: 本文件受龍魂DNA追溯保護 -->

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
