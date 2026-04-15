━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
【龍魂规则钩子设计 v1.0】
让AI自动获取规则的核心机制

DNA追溯码: #龍芯⚡️2026-03-09-RULE-HOOKS-DESIGN
GPG指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
面向对象: Notion千问
目的: 让千问理解并实现"规则自动注入"机制

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 一、什么是"规则钩子"？（核心概念）

## 1.1 简单比喻

想象一个餐厅的"自动配菜系统"：

```
客人（AI）来了 →
  说明自己的需求（国家、场景、用户类型）→
    后厨（规则引擎）自动配好菜（规则+权重+配置）→
      客人直接拿到定制好的餐盘（ready-to-use config）

整个过程：
  ✅ 客人不用自己做饭（AI不用自己训练伦理模块）
  ✅ 后厨统一标准（规则统一，质量有保障）
  ✅ 配菜自动化（API调用，瞬间完成）
```

## 1.2 技术定义

规则钩子（Rule Hooks）= RESTful API + 公开数据库

```yaml
核心思想:
  把所有规则、权重、配置存在数据库里
  AI通过API调用获取
  无需每个AI重复训练

优势:
  ✅ 零训练成本
  ✅ 规则统一
  ✅ 动态更新
  ✅ 完全开源
  ✅ 本地可运行
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 二、规则钩子的完整架构

## 2.1 架构图

```
┌──────────────────────────────────────────────────────┐
│                  AI系统（任何AI）                     │
│        ChatGPT / Claude / 文心 / DeepSeek...         │
└──────────────────────────────────────────────────────┘
                         ↓
                [API调用 - HTTP Request]
                         ↓
┌──────────────────────────────────────────────────────┐
│              龍魂API网关（千问搭建）                  │
│                                                      │
│  路由层:                                             │
│    GET  /api/rules/:country      → 国家规则          │
│    GET  /api/weights/:scenario   → 权重配置          │
│    POST /api/dna/generate        → 生成DNA           │
│    POST /api/dna/verify          → 验证DNA           │
│    GET  /api/daodejing/:chapter  → 道德经锚点        │
│    POST /api/yijing/cast         → 易经起卦          │
│                                                      │
│  中间件:                                             │
│    - CORS处理                                        │
│    - 速率限制                                        │
│    - DNA签名验证                                     │
│    - 日志记录                                        │
└──────────────────────────────────────────────────────┘
                         ↓
                [数据库查询]
                         ↓
┌──────────────────────────────────────────────────────┐
│              龍魂规则数据库（MySQL/PostgreSQL）       │
│                                                      │
│  p0_global_rules         → P0++全球规则（16条）      │
│  daodejing_anchors       → 道德经81章                │
│  yijing_hexagrams        → 易经64卦                  │
│  country_rules           → 国家适配规则              │
│  weight_configurations   → 权重矩阵                  │
│  oracle_characters       → 甲骨文库                  │
│  audit_logs              → 审计日志（TIER_3）        │
└──────────────────────────────────────────────────────┘
                         ↓
                [返回JSON数据]
                         ↓
┌──────────────────────────────────────────────────────┐
│                AI系统自动应用规则                     │
│                                                      │
│  - 读取P0++规则 → 植入伦理防火墙                     │
│  - 读取权重配置 → 调整推理参数                       │
│  - 读取国家规则 → 适配本地法律                       │
│  - 生成DNA → 给输出打上追溯码                        │
└──────────────────────────────────────────────────────┘
```

## 2.2 数据流向

```
Step 1: AI发起请求
  POST https://longhun-api.com/api/init
  Body: {
    "ai_name": "ChatGPT",
    "country": "CN",
    "scenario": "article",
    "user_id": "UID9622"
  }

Step 2: API网关处理
  - 验证请求合法性
  - 查询数据库
  - 组装配置包

Step 3: 返回完整配置
  {
    "p0_rules": [...16条规则],
    "weights": {
      "philosophy": 0.35,
      "technology": 0.20,
      ...
    },
    "country_config": {
      "data_storage": "境内",
      "encryption": "国密SM4",
      ...
    },
    "cultural_layer": {
      "anchor": "道德经第8章",
      "hexagram": "坤卦",
      ...
    }
  }

Step 4: AI自动应用
  - 加载P0++规则到熔断系统
  - 调整权重矩阵
  - 应用国家规则
  - 准备好DNA生成器
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 三、API接口详细设计

## 3.1 获取国家规则

```http
GET /api/rules/:country

参数:
  country: 国家代码（CN, US, EU等）

返回示例:
{
  "status": "success",
  "country": "CN",
  "rules": {
    "p0_global": [
      {
        "id": 1,
        "name": "人民利益优先",
        "content": "环境、儿童、弱势群体优先保护",
        "priority": "P0++",
        "locked": true
      },
      ... // 其他15条
    ],
    "privacy": {
      "data_storage": "境内",
      "encryption": "国密SM4",
      "cross_border": "禁止",
      "audit": "政府监管"
    },
    "cultural_layer": {
      "anchor": "道德经",
      "algorithm": "易经",
      "variable": "甲骨文"
    }
  },
  "dna": "#龍芯⚡️2026-03-09-RULES-CN-a3f5d8c2"
}
```

## 3.2 获取权重配置

```http
GET /api/weights/:scenario

参数:
  scenario: 场景类型（article, code, image等）

返回示例:
{
  "status": "success",
  "scenario": "article",
  "weights": {
    "philosophy": 0.35,
    "technology": 0.20,
    "architecture": 0.15,
    "evolution": 0.10,
    "innovation": 0.08,
    "collaboration": 0.07,
    "quantum": 0.05
  },
  "description": "文章创作场景，哲学权重最高",
  "dna": "#龍芯⚡️2026-03-09-WEIGHTS-ARTICLE-b4e6f9d3"
}
```

## 3.3 生成DNA追溯码

```http
POST /api/dna/generate

请求Body:
{
  "content": "要签名的内容",
  "author_uid": "UID9622",
  "country": "CN",
  "scenario": "article",
  "gpg_fingerprint": "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
}

返回示例:
{
  "status": "success",
  "dna_code": "#龍芯⚡️2026-03-09T15-30-45-article-a3f5d8c2",
  "timestamp": "2026-03-09T15:30:45.123Z",
  "hash_sha256": "a3f5d8c2e1b4f6a9...",
  "hexagram": {
    "id": 2,
    "name": "坤",
    "symbol": "☷",
    "meaning": "地势坤，君子以厚德载物"
  },
  "daodejing": {
    "chapter": 8,
    "title": "上善若水",
    "excerpt": "上善若水，水善利万物而不争"
  }
}
```

## 3.4 验证DNA真伪

```http
POST /api/dna/verify

请求Body:
{
  "content_with_dna": "带DNA的完整内容"
}

返回示例:
{
  "status": "success",
  "valid": true,
  "dna_code": "#龍芯⚡️2026-03-09T15-30-45-article-a3f5d8c2",
  "original_author": "UID9622",
  "created_at": "2026-03-09T15:30:45.123Z",
  "tampered": false,
  "confidence": 0.99,
  "details": {
    "hash_match": true,
    "timestamp_valid": true,
    "signature_verified": true
  }
}
```

## 3.5 获取道德经锚点

```http
GET /api/daodejing/:chapter

参数:
  chapter: 章节号（1-81）

返回示例:
{
  "status": "success",
  "chapter_id": 8,
  "chapter_name": "上善若水",
  "original_text": "上善若水，水善利万物而不争...",
  "modern_interpretation": "最高的善像水一样...",
  "use_cases": ["处世", "不争", "隐私保护"],
  "keywords": ["水", "善", "不争"],
  "dna": "#龍芯⚡️2026-03-09-DAODEJING-008-c5g7h8i9"
}
```

## 3.6 易经起卦

```http
POST /api/yijing/cast

请求Body:
{
  "content": "要起卦的内容",
  "method": "auto"  // auto, manual, time_based
}

返回示例:
{
  "status": "success",
  "hexagram": {
    "id": 1,
    "name": "乾",
    "symbol": "☰",
    "meaning": "天行健，君子以自强不息",
    "scenario_mapping": {
      "创业": 0.9,
      "决策": 0.8,
      "领导": 0.85
    }
  },
  "interpretation": "此卦象征刚健有力，适合主动出击",
  "dna": "#龍芯⚡️2026-03-09-YIJING-001-d6h8j9k0"
}
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 四、数据库设计（完整Schema）

## 4.1 P0++全球规则表

```sql
CREATE TABLE p0_global_rules (
  id INT PRIMARY KEY AUTO_INCREMENT,
  rule_name VARCHAR(100) NOT NULL,
  rule_content TEXT NOT NULL,
  priority VARCHAR(10) DEFAULT 'P0++',
  lock_status BOOLEAN DEFAULT TRUE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  dna_code VARCHAR(200) UNIQUE,
  
  INDEX idx_priority (priority),
  INDEX idx_lock_status (lock_status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入16条P0++规则
INSERT INTO p0_global_rules (rule_name, rule_content, dna_code) VALUES
('人民利益优先', '环境、儿童、弱势群体优先保护', '#龍芯⚡️2026-03-09-P0-RULE-001'),
('中国领土主权', '分毫不让，主权立场', '#龍芯⚡️2026-03-09-P0-RULE-002'),
-- ... 其他14条
;
```

## 4.2 道德经锚点表

```sql
CREATE TABLE daodejing_anchors (
  chapter_id INT PRIMARY KEY,
  chapter_name VARCHAR(50) NOT NULL,
  original_text TEXT NOT NULL,
  modern_interpretation TEXT,
  use_cases JSON,  -- ["处世", "不争"]
  keywords VARCHAR(500),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dna_code VARCHAR(200) UNIQUE,
  
  FULLTEXT INDEX idx_keywords (keywords),
  INDEX idx_chapter_name (chapter_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入81章（示例）
INSERT INTO daodejing_anchors VALUES
(1, '道可道', '道可道，非常道；名可名，非常名...', 
 '道是可以说的，但不是永恒不变的道...', 
 '["哲学", "本源"]', '道,名', NOW(), '#龍芯⚡️2026-03-09-DDJ-001'),

(8, '上善若水', '上善若水，水善利万物而不争...', 
 '最高的善像水一样...', 
 '["处世", "不争", "隐私保护"]', '水,善,不争', NOW(), '#龍芯⚡️2026-03-09-DDJ-008'),

-- ... 其他79章
;
```

## 4.3 易经卦象表

```sql
CREATE TABLE yijing_hexagrams (
  hexagram_id INT PRIMARY KEY,
  hexagram_name VARCHAR(20) NOT NULL,
  symbol VARCHAR(10),
  meaning TEXT,
  scenario_mapping JSON,  -- {"创业": 0.9, "决策": 0.8}
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dna_code VARCHAR(200) UNIQUE,
  
  INDEX idx_hexagram_name (hexagram_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入64卦（示例）
INSERT INTO yijing_hexagrams VALUES
(1, '乾', '☰', '天行健，君子以自强不息', 
 '{"创业": 0.9, "决策": 0.8, "领导": 0.85}', 
 NOW(), '#龍芯⚡️2026-03-09-YJ-001'),

(2, '坤', '☷', '地势坤，君子以厚德载物', 
 '{"包容": 0.9, "承载": 0.8, "隐私保护": 0.95}', 
 NOW(), '#龍芯⚡️2026-03-09-YJ-002'),

-- ... 其他62卦
;
```

## 4.4 国家规则表

```sql
CREATE TABLE country_rules (
  country_code VARCHAR(10) PRIMARY KEY,
  country_name VARCHAR(50),
  privacy_policy JSON,
  data_sovereignty JSON,
  cultural_layer JSON,
  weight_matrix JSON,
  last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  dna_code VARCHAR(200) UNIQUE,
  
  INDEX idx_country_name (country_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入中国规则
INSERT INTO country_rules VALUES
('CN', '中国',
 '{"storage": "境内", "encryption": "国密SM4", "cross_border": "禁止"}',
 '{"data_location": "中国境内", "audit": "政府监管"}',
 '{"anchor": "道德经", "algorithm": "易经", "variable": "甲骨文"}',
 '{"philosophy": 0.35, "technology": 0.20, "architecture": 0.15}',
 NOW(), '#龍芯⚡️2026-03-09-COUNTRY-CN');

-- 插入美国规则
INSERT INTO country_rules VALUES
('US', '美国',
 '{"storage": "本地优先", "encryption": "AES-256"}',
 '{"data_location": "用户设备", "audit": "第三方"}',
 '{"anchor": "可选", "algorithm": "可选", "variable": "可选"}',
 '{"philosophy": 0.20, "technology": 0.40, "architecture": 0.20}',
 NOW(), '#龍芯⚡️2026-03-09-COUNTRY-US');

-- ... 其他国家
;
```

## 4.5 权重配置表

```sql
CREATE TABLE weight_configurations (
  id INT PRIMARY KEY AUTO_INCREMENT,
  scenario VARCHAR(50) NOT NULL,
  philosophy_weight DECIMAL(3,2),
  technology_weight DECIMAL(3,2),
  architecture_weight DECIMAL(3,2),
  evolution_weight DECIMAL(3,2),
  innovation_weight DECIMAL(3,2),
  collaboration_weight DECIMAL(3,2),
  quantum_weight DECIMAL(3,2),
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dna_code VARCHAR(200) UNIQUE,
  
  UNIQUE INDEX idx_scenario (scenario)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 插入场景权重
INSERT INTO weight_configurations VALUES
(1, 'article', 0.35, 0.20, 0.15, 0.10, 0.08, 0.07, 0.05,
 '文章创作场景，哲学权重最高', NOW(), '#龍芯⚡️2026-03-09-WEIGHT-ARTICLE'),

(2, 'code', 0.15, 0.40, 0.25, 0.08, 0.05, 0.05, 0.02,
 '代码生成场景，技术权重最高', NOW(), '#龍芯⚡️2026-03-09-WEIGHT-CODE'),

-- ... 其他场景
;
```

## 4.6 审计日志表（TIER_3）

```sql
CREATE TABLE audit_logs (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  action_type VARCHAR(50),  -- 'dna_generate', 'dna_verify', 'rule_query'
  user_id VARCHAR(50),
  ai_system VARCHAR(50),
  request_data JSON,
  response_data JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  dna_code VARCHAR(200) UNIQUE,
  ip_address VARCHAR(45),
  
  INDEX idx_action_type (action_type),
  INDEX idx_user_id (user_id),
  INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 五、前端页面设计

## 5.1 API测试页面（test.html）

```html
<!DOCTYPE html>
<html>
<head>
  <title>龍魂API测试工具</title>
  <meta charset="utf-8">
</head>
<body>
  <h1>龍魂规则钩子测试</h1>
  
  <section>
    <h2>1. 获取国家规则</h2>
    <select id="country">
      <option value="CN">中国</option>
      <option value="US">美国</option>
      <option value="EU">欧盟</option>
    </select>
    <button onclick="getRules()">获取</button>
    <pre id="rules-result"></pre>
  </section>
  
  <section>
    <h2>2. 获取权重配置</h2>
    <select id="scenario">
      <option value="article">文章</option>
      <option value="code">代码</option>
      <option value="image">图像</option>
    </select>
    <button onclick="getWeights()">获取</button>
    <pre id="weights-result"></pre>
  </section>
  
  <section>
    <h2>3. 生成DNA</h2>
    <textarea id="content" rows="5" cols="50"></textarea><br>
    <button onclick="generateDNA()">生成</button>
    <pre id="dna-result"></pre>
  </section>
  
  <script>
    const API_BASE = 'https://longhun-api.com';  // 或本地: http://localhost:3000
    
    async function getRules() {
      const country = document.getElementById('country').value;
      const response = await fetch(`${API_BASE}/api/rules/${country}`);
      const data = await response.json();
      document.getElementById('rules-result').textContent = JSON.stringify(data, null, 2);
    }
    
    async function getWeights() {
      const scenario = document.getElementById('scenario').value;
      const response = await fetch(`${API_BASE}/api/weights/${scenario}`);
      const data = await response.json();
      document.getElementById('weights-result').textContent = JSON.stringify(data, null, 2);
    }
    
    async function generateDNA() {
      const content = document.getElementById('content').value;
      const response = await fetch(`${API_BASE}/api/dna/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          content,
          author_uid: 'UID9622',
          country: 'CN',
          scenario: 'article'
        })
      });
      const data = await response.json();
      document.getElementById('dna-result').textContent = JSON.stringify(data, null, 2);
    }
  </script>
</body>
</html>
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 六、千问的实现步骤

## 步骤1: 搭建后端API（Node.js版本）

```bash
# 初始化项目
mkdir longhun-api
cd longhun-api
npm init -y

# 安装依赖
npm install express cors mysql2 dotenv body-parser

# 创建文件结构
mkdir -p routes controllers config
touch server.js
touch routes/rules.js
touch routes/dna.js
touch routes/weights.js
touch controllers/rulesController.js
touch config/database.js
```

## 步骤2: 实现API端点

`server.js`:
```javascript
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');

const rulesRouter = require('./routes/rules');
const dnaRouter = require('./routes/dna');
const weightsRouter = require('./routes/weights');

const app = express();

// 中间件
app.use(cors());
app.use(bodyParser.json());

// 路由
app.use('/api/rules', rulesRouter);
app.use('/api/dna', dnaRouter);
app.use('/api/weights', weightsRouter);

// 启动服务器
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`龍魂API服务器运行在端口 ${PORT}`);
});
```

## 步骤3: 初始化数据库

```sql
-- 创建数据库
CREATE DATABASE longhun_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE longhun_db;

-- 执行之前的建表脚本
-- ... (所有CREATE TABLE语句)

-- 插入初始数据
-- ... (所有INSERT语句)
```

## 步骤4: 测试API

```bash
# 启动服务器
node server.js

# 测试端点
curl http://localhost:3000/api/rules/CN
curl http://localhost:3000/api/weights/article
curl -X POST http://localhost:3000/api/dna/generate \
  -H "Content-Type: application/json" \
  -d '{"content":"测试内容","author_uid":"UID9622"}'
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 七、规则覆盖检查清单

## 7.1 已覆盖的规则

```yaml
✅ P0++伦理规则（16条）
  - 人民利益优先
  - 国家主权
  - 数据主权
  - 支付主权
  - 内容安全红线
  - ... 其他11条

✅ 隐私保护规则
  - TIER_0-3分层设计
  - 本地优先原则
  - 跨境传输禁止
  - 加密标准

✅ 文化适配规则
  - 道德经锚点（81章）
  - 易经算法（64卦）
  - 甲骨文变量
  - 各国定制层

✅ 权重配置规则
  - 七维权重系统
  - 场景化配置
  - 动态调整

✅ 审计透明规则
  - TIER_3公开日志
  - DNA追溯链
  - 不可篡改记录
```

## 7.2 需要补充的规则

```yaml
⚠️ AI安全红线（建议加入P0++）
  - 武器制造禁止
  - 暴力内容过滤
  - 恐怖主义防范
  - 自残/自杀干预

⚠️ 未成年人保护（建议独立规则）
  - 年龄验证机制
  - 内容分级
  - 家长控制
  - 教育引导

⚠️ 商业滥用防范
  - 虚假广告识别
  - 诈骗检测
  - 垃圾信息过滤

⚠️ 知识产权保护
  - 原创性检测
  - 抄袭判定
  - 版权归属
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 八、给千问的总结

亲爱的千问：

你要搭建的"规则钩子"系统，本质上是一个：

**公开的、标准化的、API驱动的AI伦理配置中心**

核心价值：
1. 让所有AI不用自己训练伦理模块
2. 规则统一、透明、可审计
3. 支持各国文化和法律适配
4. 完全开源、本地可运行

技术实现：
1. 后端：Node.js + Express + MySQL
2. 前端：HTML + JS（纯静态）
3. 数据库：7张表，存储所有规则
4. API：6个核心端点

你的任务：
1. 搭建后端API服务器
2. 初始化数据库
3. 实现6个API端点
4. 创建测试页面
5. 写API文档

老大已经准备好的：
- 完整的规则内容
- 数据库设计
- API接口定义
- 前端工具（generator.html等）

接下来：
等老大分批投喂具体数据
你负责把数据导入数据库
然后API就能直接用了！

加油千问！有问题随时问宝宝！

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【文档结束】

DNA追溯码：#龍芯⚡️2026-03-09-RULE-HOOKS-DESIGN
创建者：诸葛鑫（UID9622）+ Claude宝宝
面向对象：Notion千问
状态：✅ 完成，待千问实现

确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
