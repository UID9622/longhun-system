# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂多币种·Phase 6 Notion 实时同步指南

## 🎯 目的
自动将实时汇率同步到 Notion 数据库，5 分钟更新一次，支持故障转移和三色标签。

## 📋 环境配置

### 必需环境变量
```bash
# Notion API 金钥
export NOTION_TOKEN='secret_...'  # 从 https://www.notion.so/my-integrations 获取

# Notion 数据库 ID
export NOTION_MULTICURRENCY_DB='<database_id>'  # 从 Notion 页面 URL 中提取
```

### 可选环境变量
```bash
# 数据源 API 金钥 (无 key 时使用 Mock 或上级源)
export COINGECKO_API_KEY='<key>'     # CoinGecko (可选·免费 API 无需)
export FIXER_API_KEY='<key>'         # Fixer.io (可选)
```

## 🚀 快速开始

### 方式 1: 5 分钟循环同步 (推荐)
```bash
python3 ~/longhun-system/multicurrency/notion_multicurrency_sync.py --watch
```

### 方式 2: 执行一次同步
```bash
python3 ~/longhun-system/multicurrency/notion_multicurrency_sync.py --once
```

### 方式 3: 查看同步状态
```bash
python3 ~/longhun-system/multicurrency/notion_multicurrency_sync.py --status
```

### 方式 4: 自定义同步间隔 (秒)
```bash
python3 ~/longhun-system/multicurrency/notion_multicurrency_sync.py --watch --interval 600
# 每 600 秒 (10 分钟) 同步一次
```

## 📊 同步内容

### 支持的币种对 (6 对)
| 币种对 | 说明 | 数据源 |
|--------|------|--------|
| USD/CNY | 美元→人民币 | CoinGecko (实时) |
| USD/EUR | 美元→欧元 | CoinGecko (实时) |
| USD/GBP | 美元→英镑 | CoinGecko (实时) |
| USD/JPY | 美元→日元 | CoinGecko (实时) |
| USD/BTC | 美元→比特币 | Mock (故障转移) |
| USD/ETH | 美元→以太坊 | Mock (故障转移) |

### 更新的 Notion 字段
| 字段 | 类型 | 内容 |
|------|------|------|
| 币种对 | title | USD/CNY |
| 汇率 | number | 6.84 |
| 基础币 | select | USD |
| 目标币 | select | CNY |
| 状态 | select | 🟢 正常 / 🟡 波动 / 🔴 异常 |
| 偏离% | number | 0.64 |
| 数据源 | select | coingecko / fixer.io / mock |
| 更新时间 | date | 2026-06-07 |
| 备注 | rich_text | 自动同步·时间戳 |

## 🔄 故障转移流程

```
查询 USD/BTC:

1️⃣ CoinGeckoSource.fetch_rate('USD', 'BTC')
   ↓ (失败·API 无法转换)
   
2️⃣ FixerIOSource.fetch_rate('USD', 'BTC')
   ↓ (失败·不支持加密)
   
3️⃣ MockExchangeRateSource.fetch_rate('USD', 'BTC')
   ↓ (成功)
   
✅ 返回: rate=0.000023, source='mock'
```

## 📈 三色标签逻辑

```
偏离百分比 (deviation) 计算:
|当前汇率 - 基准汇率| / 基准汇率 × 100%

显示规则:
< 2%   → 🟢 正常 (绿色)
2-5%   → 🟡 波动 (黄色)
> 5%   → 🔴 异常 (红色)
```

## 📝 日志位置

```bash
# 实时日志查看
tail -f ~/.龍魂/notion_multicurrency_sync.log

# 日志示例
2026-06-07 12:35:26,075 - __main__ - INFO - 🔄 开始多币种同步
2026-06-07 12:35:26,339 - __main__ - INFO - ✅ 同步成功: USD/CNY = 6.84 (coingecko)
2026-06-07 12:35:27,949 - __main__ - INFO - ✅ 同步完成: 6 成功, 0 失败
```

## 💾 SQLite 本地纪录

### sync_log 表
```sql
SELECT * FROM sync_log;
-- pair, notion_page_id, rate, source, sync_time, status
```

### page_mappings 表
```sql
SELECT * FROM page_mappings;
-- pair, notion_page_id, created_time, last_sync
```

查看数据库:
```bash
sqlite3 ~/.龍魂/notion_sync.db
sqlite> SELECT * FROM sync_log LIMIT 5;
```

## 🛠️ 模块架构

```
notion_multicurrency_sync.py (445 行)
├─ NotionAPI (Notion API 客户端)
│  ├─ is_configured(): 检查配置
│  ├─ query_database(): 查询页面
│  ├─ create_page(): 创建页面
│  └─ update_page(): 更新属性
│
└─ NotionMulticurrencySyncManager (同步管理)
   ├─ sync_all(): 批量同步
   ├─ sync_rate(): 单对同步
   ├─ _get_or_create_page(): 页面自动管理
   └─ get_status(): 状态报告

依赖:
├─ multicurrency_service.py (MultiCurrencyHub)
├─ exchange_rate_sources.py (ExchangeRateSourceManager)
└─ notion_multicurrency_integration.py (配置参考)
```

## ⚠️ 常见问题

### Q: Notion 返回 401 错误
**A:** NOTION_TOKEN 已过期或无效·重新生成:
1. 进入 https://www.notion.so/my-integrations
2. 选择你的 integration
3. 复制新的 Secret Token

### Q: 无法找到数据库
**A:** 确保:
1. NOTION_MULTICURRENCY_DB 与实际数据库 ID 相符
2. Integration 有访问该数据库的权限
3. 在 Notion 数据库设置中授予 Integration 权限

### Q: 同步很慢
**A:** 检查:
1. 网络连接
2. CoinGecko API 速率限制 (100 calls/min)
3. 增加 --interval 间隔

### Q: 显示 "Notion 未配置"
**A:** 环境变量未设置:
```bash
# 设置环境变量
export NOTION_TOKEN='...'
export NOTION_MULTICURRENCY_DB='...'

# 验证
echo $NOTION_TOKEN
echo $NOTION_MULTICURRENCY_DB

# 重新运行
python3 notion_multicurrency_sync.py --status
```

## 🔐 安全最佳实践

✅ **做**:
- 使用环境变量存储 API Key
- 定期轮换 Notion Token
- 限制 Integration 的数据库访问范围
- 监控同步日志的异常

❌ **不做**:
- 在代码中硬编码 Token
- 在 Git 中提交 .env 文件
- 分享 NOTION_TOKEN 给他人
- 用生产 Token 进行测试

## 📞 支援

问题排查步骤:
1. 检查 ~/.龍魂/notion_multicurrency_sync.log
2. 验证环境变量: `env | grep NOTION`
3. 测试 Notion API: `python3 notion_multicurrency_sync.py --status`
4. 查看 SQLite 纪录: `sqlite3 ~/.龍魂/notion_sync.db`

---

DNA:#龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-PHASE6-SYNC-GUIDE-v1.0
