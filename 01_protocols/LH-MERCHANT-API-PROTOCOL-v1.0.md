> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂·国产商户开放API接入协议 v1.0

> DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·䷀乾-MERCHANT-PROTOCOL-v1.0
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

## §1. 适用声明

本协议规范国产商户接入龍魂API平台的全部流程。商户指在中国大陆注册的企业/个体工商户，通过营业执照验证后可接入。

**主权声明**: 龍魂API平台为中国自主知识产权，只对国产商户开放。海外企业及个人不予接入。

## §2. 接入流程

### 2.1 注册
```bash
lh merchant register "企业名称" --company "营业执照全称" --tier free
```

### 2.2 审核
UID9622或其授权人审核商户资质：
```bash
lh merchant approve <商户ID> --tier basic
```

### 2.3 生成密钥
```bash
lh merchant keygen <商户ID> --name "生产环境"
```

⚠️ API Key仅显示一次，请妥善保管。

## §3. 认证方式

每个API请求需携带以下Header：

| Header | 说明 |
|:---|:---|
| `X-LH-API-Key` | API Key字符串 |
| `X-LH-Timestamp` | Unix时间戳(秒)，5分钟有效期 |
| `X-LH-Signature` | HMAC-SHA256签名 |

### 签名算法

```
sign_string = METHOD + PATH + TIMESTAMP + SHA256(BODY)
signature = HMAC-SHA256(API_KEY, sign_string)
```

Python示例：
```python
import hashlib, hmac, time, json

api_key = "lh_mch_xxxx..."
body = json.dumps({"prompt": "你好"})
ts = str(int(time.time()))
body_hash = hashlib.sha256(body.encode()).hexdigest()
sign_string = f"POST/v1/ai/text{ts}{body_hash}"
signature = hmac.new(api_key.encode(), sign_string.encode(), hashlib.sha256).hexdigest()

headers = {
    "X-LH-API-Key": api_key,
    "X-LH-Timestamp": ts,
    "X-LH-Signature": signature,
    "Content-Type": "application/json",
}
```

## §4. 商户层级

| 层级 | 日限额 | QPS | 月费 | 说明 |
|:---|:---:|:---:|:---|:---|
| free | 100 | 1 | ¥0 | 免费试用·基础API |
| basic | 1,000 | 5 | ¥99 | 标准API·内容审核 |
| pro | 10,000 | 20 | ¥499 | 高级API·AI生成 |
| enterprise | 100,000 | 100 | 定制 | 全部API·专属支持 |

## §5. 开放API清单

### 5.1 免费层 (free)

| API | 路径 | 说明 |
|:---|:---|:---|
| AI文本生成 | `POST /v1/ai/text` | 混元/DeepSeek文本生成 |
| 五害检测 | `POST /v1/security/five-harms` | 涉政/涉黄/涉暴/涉赌/涉诈 |
| 焦虑话术检测 | `POST /v1/security/anxiety` | PUA/道德绑架/制造焦虑检测 |
| 知识库检索 | `GET /v1/knowledge/search` | 知识库全文检索 |
| 数字根计算 | `POST /v1/math/digital-root` | 洛书369数字根 |
| 商户信息 | `GET /v1/merchant/me` | 查询自身用量 |

### 5.2 基础层 (basic) — 含免费层全部

| API | 路径 | 说明 |
|:---|:---|:---|
| AI图片生成 | `POST /v1/ai/image` | 混元图片生成 |
| 内容安全审计 | `POST /v1/security/audit` | 三色审计·十道闸口 |
| 五行属性判定 | `POST /v1/culture/wuxing` | 干支五行·生克关系 |

### 5.3 专业层 (pro) — 含基础层全部

| API | 路径 | 说明 |
|:---|:---|:---|
| 信任积分查询 | `GET /v1/trust/score` | 三分桶积分查询 |
| CNSH代码翻译 | `POST /v1/cnsh/translate` | CNSH→Python翻译 |
| 媒体验证 | `POST /v1/media/verify` | 图片/视频篡改检测 |

### 5.4 企业层 (enterprise)

全部API + 定制接入 + 专属技术支持。

## §6. 不开放的能力（内核层·永不对外）

以下能力为龍魂系统内核，不对任何商户开放：
- 369洛书算法核心 · 20人格路由 · DNA生成/验证
- GPG签名 · 四级熔断控制 · 系统管理/部署
- 量子卦象引擎 · 七维推演 · 十道闸口审计核心

## §7. 调用限制与计费

- 每个API调用消耗1个配额（图片/视频类消耗3-5个）
- 日配额 = 层级日限额，每日00:00重置
- QPS超限返回HTTP 429，响应头含 `retry_after` 秒数
- 日配额用完返回HTTP 429

## §8. 数据与隐私

- 商户API调用数据存储在中国境内（鲲鹏服务器 119.13.90.27）
- 调用日志保留30天，到期自动清理
- 商户无权访问其他商户的数据
- 龍魂不将商户数据用于训练或转售

## §9. 违规处理

以下行为将导致商户被暂停或永久吊销：
- 将API Key提供给第三方
- 使用API进行违法活动
- 绕过签名验证或伪造请求
- 超量调用不配合升级

## §10. 联系方式

- 技术文档: `http://<网关地址>:9633/docs`
- API目录: `GET /v1/catalog`
- 管理命令: `lh merchant help`
- 网关启动: `lh merchant serve --port 9633`

---

**龍魂·让中国商户用上中国AI。**
