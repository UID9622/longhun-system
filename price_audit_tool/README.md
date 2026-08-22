# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 价格透明度审计工具 v1.0 · Price Audit Tool

> **算法审计平民化 · 人人都是审计员**
>
> DNA: #龍芯⚡️丙午·丙申·癸酉·丁巳·䷒临-PRICE-AUDIT-TOOL-DELIVERY-63A56877
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0

---

## 一、项目背景

这篇文章[《算法裸奔时代：他们明知道会爆雷，为什么还不改？》](https://blog.csdn.net/UID9622/article/details/163260087)揭露了互联网平台利用算法进行"大数据杀熟""信息茧房"等违规行为。平台不改是因为**用户举证困难、作恶成本太低**。

本工具的目标：**让每个普通人都有能力检测大数据杀熟**——不需要懂代码，不需要懂算法，输入价格数据就能得到一份通俗的审计报告。

> 🛡️ **铁律**: 所有数据本地存储，不上传任何云端。你的数据你做主。

---

## 二、功能概览

| 功能 | 说明 |
|:---|:---|
| **Web仪表盘** | 浏览器打开即用，输入数据→一键审计→可视化报告 |
| **CLI命令行** | 终端高手用，支持JSON/CSV/交互式输入 |
| **四层检测引擎** | IQR统计 + 用户分组 + 时间序列 + 综合评分 |
| **历史报告** | 自动保存，随时回溯对比 |
| **示例数据** | 一键加载典型杀熟场景，快速体验 |

### 四层检测策略

| 层 | 方法 | 检测什么 | 权重 |
|:---:|:---|:---|:---:|
| L1 | Tukey's IQR Fences | 价格是否处于统计异常区间 | 25分 |
| L2 | 用户分组均值差异 | 新老用户/VIP等看到的价格差异 | 35分 |
| L3 | 滑动平均 + Z-Score | 短期内价格是否剧烈波动 | 25分 |
| L4 | 加权综合评分 | 汇总以上三维度给出0-100杀熟评分 | 15分 (数据充分度) |

### 评分解读

| 分数 | 判定 | 建议 |
|:---:|:---|:---|
| 0-15 | 🟢 未检出异常 | 当前数据未发现明显异常定价 |
| 15-40 | 🟢 轻微可疑 | 数据量有限，建议多收集数据后重新检测 |
| 40-70 | 🟡 中度可疑 | 建议继续观察，对比其他平台价格 |
| 70-100 | 🔴 严重可疑 | 强烈建议截图留证，向12315或平台投诉 |

---

## 三、安装

### 前置条件

- **Python 3.9+**（macOS 自带，Ubuntu 需安装）
- pip（Python 自带）
- 无需数据库、无需 Docker、无需任何外部服务

### 方式一：一键安装启动（推荐）

```bash
cd price_audit_tool
chmod +x setup.sh
./setup.sh
```

脚本会自动：
1. 创建 Python 虚拟环境
2. 安装依赖（fastapi, uvicorn, pydantic）
3. 运行测试套件验证
4. 启动 Web 服务

### 方式二：手动安装

```bash
cd price_audit_tool

# 1. 创建虚拟环境（可选但推荐）
python3 -m venv .venv
source .venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行测试（验证安装正确）
python3 tests/test_detector.py

# 4. 启动服务
python3 backend/app.py
```

### 依赖清单

| 包 | 版本 | 用途 |
|:---|:---|:---|
| fastapi | ≥0.104 | Web API框架 |
| uvicorn | ≥0.24 | ASGI服务器 |
| pydantic | ≥2.5 | 数据验证 |

> 全为标准Python包，从PyPI安装。无第三方商业依赖。

---

## 四、使用方式

### 4.1 Web仪表盘（推荐）

启动服务后，浏览器打开：

```
http://localhost:8899/dashboard
```

**操作流程**：
1. 在左侧输入框填入价格数据（逗号或换行分隔）
2. （可选）填入不同用户分组的价格对比——这是杀熟检测的关键数据
3. （可选）填入带时间戳的价格序列——检测短期异常波动
4. 点击「开始审计」
5. 右侧展示完整审计报告，含四层分析 + 综合评分

**快速体验**：点击「加载示例数据」按钮，自动填入典型杀熟场景数据并执行审计。

**API文档**（开发者）：`http://localhost:8899/docs`

### 4.2 CLI命令行

```bash
# 快速审计（逗号分隔价格）
cd price_audit_tool
source .venv/bin/activate
python3 cli/audit_cli.py --prices "9.9,10.0,12.0,12.5,9.8"

# 从JSON文件审计（支持分组+时序）
python3 cli/audit_cli.py --json data/sample_input.json

# 从CSV文件审计
python3 cli/audit_cli.py --csv data/sample_input.csv

# 交互模式（逐步输入）
python3 cli/audit_cli.py --interactive

# 查看历史报告
python3 cli/audit_cli.py --list

# 查看全局统计
python3 cli/audit_cli.py --stats

# 查看特定报告
python3 cli/audit_cli.py --report 20260728000001
```

### 4.3 API调用（开发者）

```bash
# 健康检查
curl http://localhost:8899/api/health

# 快速审计
curl -X POST http://localhost:8899/api/quick \
  -H "Content-Type: application/json" \
  -d '{"prices":[9.9,10.0,12.0,12.5]}'

# 完整审计（含分组+时序）
curl -X POST http://localhost:8899/api/audit \
  -H "Content-Type: application/json" \
  -d '{
    "prices":[9.9,10.0,9.8,12.0,12.5,12.3],
    "groups":{"新用户":[9.9,10.0,9.8],"老用户":[12.0,12.5,12.3]},
    "timeseries":[
      {"time":"7-20","price":9.9},
      {"time":"7-24","price":12.5}
    ],
    "product_name":"手机",
    "platform":"某电商"
  }'

# 查看统计
curl http://localhost:8899/api/stats
```

### 4.4 在代码中调用

```python
import sys
sys.path.insert(0, "price_audit_tool/backend")

from detector import detect_price_anomaly, quick_check, check_with_groups

# 方式1: 最简调用
result = quick_check([9.9, 10.0, 12.0, 12.5])

# 方式2: 带分组（推荐用于杀熟检测）
result = check_with_groups(
    [9.9, 10.0, 9.8, 12.0, 12.5, 12.3],
    {"新用户": [9.9, 10.0, 9.8], "老用户": [12.0, 12.5, 12.3]}
)

# 方式3: 完整审计
result = detect_price_anomaly(
    prices=[...],
    groups={...},
    timeseries=[...]
)

print(f"杀熟评分: {result['composite_assessment']['score']}/100")
print(f"判定: {result['composite_assessment']['level']}")
print(f"建议: {result['composite_assessment']['advice']}")
```

---

## 五、数据格式说明

### JSON输入格式

```json
{
  "prices": [9.9, 10.0, 9.8, 12.0, 12.5],
  "groups": {
    "新用户": [9.9, 10.0, 9.8],
    "老用户": [12.0, 12.5]
  },
  "timeseries": [
    {"time": "2026-07-20", "price": 9.9},
    {"time": "2026-07-24", "price": 12.5}
  ]
}
```

### CSV输入格式

| price | group | time |
|:---|:---|:---|
| 9.9 | 新用户 | 2026-07-20 |
| 10.0 | 新用户 | 2026-07-21 |
| 12.0 | 老用户 | 2026-07-20 |
| 12.5 | 老用户 | 2026-07-24 |

---

## 六、实操指南：如何检测大数据杀熟

> 以下步骤摘自文章理念，用本工具落地。

### Step 1: 收集数据

同一件商品，用**不同账号**（新注册 vs. 老用户；会员 vs. 非会员）分别查看价格，记录：

- 商品名称
- 平台名称
- 看到的价格
- 查看时间
- 用的什么账号类型

> 💡 **技巧**：可以用浏览器无痕模式/不同手机号注册来模拟不同用户类型。

### Step 2: 录入数据

打开仪表盘 `http://localhost:8899/dashboard`，填入：

1. **所有价格**文本框：把各账号看到的价格都填进去
2. **分组价格**文本框：按账号类型分组，如：
   ```json
   {"新用户":[9.9,10.0],"老用户":[12.0,12.5]}
   ```
3. 点击「开始审计」

### Step 3: 解读报告

- 看「综合评分」—— 40分以上值得关注，70分以上强烈建议投诉
- 看「[L2] 用户分组差异」—— 这是杀熟的核心证据
- 截屏保存报告页面作为证据
- 如果多次审计都高分，说明该平台可能存在系统性杀熟行为

### Step 4: 维权

- **12315**：通过全国12315平台投诉
- **平台客服**：要求解释价格差异
- **社交曝光**：公开审计报告，推动舆论监督

---

## 七、项目结构

```
price_audit_tool/
├── README.md                   # 本文档
├── requirements.txt            # Python依赖
├── setup.sh                    # 一键安装启动脚本
│
├── backend/
│   ├── __init__.py             # 模块初始化
│   ├── detector.py             # 核心检测引擎（四层算法）
│   ├── models.py               # 数据存储（本地JSONL）
│   └── app.py                  # FastAPI Web服务
│
├── frontend/
│   └── index.html              # Web仪表盘（纯HTML，无框架依赖）
│
├── cli/
│   └── audit_cli.py            # CLI命令行工具
│
├── tests/
│   └── test_detector.py        # 9项测试
│
└── data/
    ├── sample_input.json       # JSON示例
    ├── sample_input.csv        # CSV示例
    └── reports.jsonl           # 审计报告存储（自动生成）
```

---

## 八、算法透明度（A-BOM备案）

| 算法 | 方法 | 参数 | 阈值来源 |
|:---|:---|:---|:---|
| L1 IQR异常值 | Tukey's Fences | Q1-1.5×IQR / Q3+1.5×IQR (温和) ; Q1-3×IQR / Q3+3×IQR (极端) | Tukey, 1977 |
| L2 分组差异 | 均值差异百分比 | 阈值 5%（可疑）/ 15%（严重） | 实证设定，可调整 |
| L3 时序异常 | 滑动平均 + Z-Score | window=5; threshold=2σ | 标准统计方法 |
| L4 综合评分 | 加权求和 | 权重: 25/35/25/15 | 分组差异权重量高（杀熟核心指标） |

---

## 九、隐私 & 安全

- ✅ **本地优先**：所有数据存储在本地 `data/reports.jsonl`
- ✅ **零云端**：不连接任何远程服务器，不上传任何数据
- ✅ **无追踪**：无cookie、无分析、无第三方脚本
- ✅ **开源透明**：CC BY-NC-SA 4.0，算法完全可审计
- ✅ **前端即服务**：仪表盘是纯静态HTML，可直接用浏览器打开

---

## 十、常见问题

**Q: 我只有一个账号的数据，能检测吗？**
A: 可以。工具会用L1 IQR统计方法检测价格是否在异常区间。但最有效的杀熟检测需要对比不同用户看到的价格（L2分组检测）。

**Q: 需要多少数据才准确？**
A: 建议每组至少3-5个价格点。数据越多，检测越准确。

**Q: 这工具能自动抓取电商价格吗？**
A: 当前版本需要手动输入数据。自动采集涉及平台反爬机制，后续版本考虑。手动录入也是保护你的隐私。

**Q: 为什么用 IQR 而不是机器学习？**
A: IQR方法简单、可解释、不需要训练数据。这正是"算法审计透明"的核心——你不需要信任一个黑箱模型。

**Q: 工具在哪运行？需要联网吗？**
A: 完全本地运行。`localhost:8899` 是你自己的电脑。不需要任何网络连接。

---

## 十一、端口配置

默认端口: **8899**

如需修改：
```bash
# 方式1: 通过setup.sh
./setup.sh 8080

# 方式2: 直接改app.py最后一行
uvicorn.run(app, host="0.0.0.0", port=你的端口)
```

---

> v1.0 · 2026-07-28 · 算法审计平民化
> 阅读文章: https://blog.csdn.net/UID9622/article/details/163260087
> #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
