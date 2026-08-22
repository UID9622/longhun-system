# 🐉 龍魂生态 · 月度主权开发者系统 v2.0

> **月度主权确认金**：**每月 1 元起步 · 上不封顶 · 杜绝一毛不拔**
> 不是一次性买断，是每个月支付确认开发者身份。连续 3 个月未缴 → DNA 冻结（代码只读），补缴欠费月数+当月后恢复。

**DNA:** `#龍芯⚡️丙午·丙申·庚申·丁亥·䷡大壮-DEV-ECOSYSTEM-UID9622`
**确认码:** `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
**GPG:** `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**三色:** 🟢 通过
**分层许可:** 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2（代码可商用·思想名号需授权）

---

## 📜 月度主权确认金公约（核心条款）

| 条款 | 内容 |
|:---|:---|
| 缴纳周期 | **每自然月 1 元起步，上不封顶** |
| 缴纳方式 | 微信 / 支付宝 / 数字人民币（正规网关链路） |
| 逾期宽限 | 连续 3 个月未缴 → 宽限 → 冻结 |
| 冻结后果 | 开发者 DNA 冻结 · 代码可读 · **不可新注入 DNA** · 不参与收益分配 |
| 恢复方式 | 补缴欠费月数×1元 + 当月 1 元 |
| 企业上浮 | 企业/机构自愿多缴，上不封顶，多出部分入生态公共贡献池（公开透明） |

> 完整协议：`01_protocols/LH-DEVELOPER-FEE-CONVENTION-v1.0.md`

## 🎯 功能清单

| # | 功能 | 状态 |
|:---|:---|:---:|
| 1 | 开发者注册（姓名/邮箱/昵称/GPG公钥/身份类型） | ✅ |
| 2 | **月度账单**（每月1日生成·1元起步·自愿上浮） | ✅ |
| 3 | **正规支付网关层**（sandbox 验签闭环 + 微信/支付宝/数币注册位） | ✅ |
| 4 | **月费状态机**（active/grace/frozen·首月免缴·欠费计算） | ✅ |
| 5 | **定时冻结任务**（crontab 每月1日·连续3月未缴冻结） | ✅ |
| 6 | **历史账单查询 + 4类数据导出**（缴费/贡献/代码DNA/名册·CSV/JSON） | ✅ |
| 7 | 开发者DNA生成（唯一·不可篡改·双哈希） | ✅ |
| 8 | 代码DNA注入API（登记+哈希+贡献分·月费状态闸） | ✅ |
| 9 | CLI批量注入工具（13种语言注释模板） | ✅ |
| 10 | Git pre-commit 钩子（缺DNA阻止提交） | ✅ |
| 11 | 贡献记录 + 贡献榜 Top50 | ✅ |
| 12 | 开发者面板（月费状态卡/历史账单/导出/查询/代码/贡献/榜单） | ✅ |

## 📁 项目结构

```
longhun-dev-ecosystem/
├── backend/                 # FastAPI 后端
│   ├── app.py               # 主应用（API + 页面路由）
│   ├── models.py            # SQLAlchemy 模型（Developer月费字段/订单/月费账本）
│   ├── schemas.py           # Pydantic 模型
│   ├── dna_generator.py     # DNA生成引擎（干支+哈希）
│   ├── gateway.py           # 正规支付网关层（4通道·验签·回调·幂等）
│   ├── monthly_fee.py       # 月度确认金模块（账单/状态/冻结/历史/统计/导出）
│   ├── payment.py           # 支付接口（接入网关）
│   └── config.py            # 配置（PAYMENT_GATEWAY 切换真实通道）
├── frontend/
│   ├── register.html        # 注册页（公约+企业上浮选项）
│   ├── dashboard.html       # 开发者面板（月费卡片+历史+导出）
│   └── assets/style.css     # 暗金主题
├── cli/lh_dna_inject.py     # DNA注入CLI
├── hooks/pre-commit         # Git 钩子
├── scripts/migrate_db.py    # 数据库迁移（兼容已有库）
├── scripts/fee_cron.py      # 定时冻结 + CLI 导出
├── requirements.txt
└── README.md
```

## 🚀 快速启动（本地）

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化/迁移数据库（幂等）
python3 scripts/migrate_db.py

# 3. 启动服务
python3 -m uvicorn backend.app:app --host 0.0.0.0 --port 8000

# 4. 访问
#    注册页:    http://localhost:8000/register
#    开发者面板: http://localhost:8000/dashboard
```

## 🔑 开发者流程

1. **注册**：填姓名/邮箱/昵称/GPG公钥 → 生成唯一 DNA（`#龍芯⚡️丙午-DEV-XXXXXXXX-9622`）
2. **首月费支付**：沙箱模拟扫码支付（默认 1 元，企业可自愿上浮）→ 激活（+10 贡献分）
3. **每月确认**：次月起每月 1 元起步，上不封顶；连续 3 个月未缴 → DNA 冻结
4. **注入**：CLI 批量注入代码 DNA（每文件 +1 分，宽限/冻结状态禁止注入）
5. **累积**：贡献榜 Top50 · 面板可查月费状态/历史账单/代码/贡献记录/导出

## ⚙️ CLI 用法

```bash
# 单文件
python3 cli/lh_dna_inject.py --file ./main.py --developer-dna "#龍芯⚡️..."

# 批量递归
python3 cli/lh_dna_inject.py --path ./my-project/ --developer-dna "#龍芯⚡️..." --recursive

# 指定线上服务（生产）
LONGHUN_API_URL="https://uid9622.cn/developer" python3 cli/lh_dna_inject.py --file ./a.py --developer-dna "..."

# 月费冻结任务 / 导出
python3 scripts/fee_cron.py --cron-freeze
python3 scripts/fee_cron.py --export fee-records --format csv
```

## 🌐 生产部署（鲲鹏 uid9622.cn）

- 服务端口：**8800**
- 公网路由：
  - 页面：`https://uid9622.cn/developer/register` / `/developer/dashboard`
  - API：`https://uid9622.cn/developer/api/...`（nginx `location /developer/` 剥离前缀 → 8800）
  - 健康检查：`https://uid9622.cn/developer/health`
- systemd：`longhun-dev-ecosystem.service`
- 定时冻结：crontab 每月 1 日 0 点 `scripts/fee_cron.py --cron-freeze`

```bash
# 一键部署（在 longhun-system 根目录）
rsync -avz -e "ssh -i ~/.ssh/longhun_kunpeng_ed25519" longhun-dev-ecosystem/ \
    root@119.13.90.27:/opt/longhun-dev-ecosystem/
```

## 🛠 换真实支付

支付网关抽象在 `backend/gateway.py`（`PaymentGateway` 基类 + 4 通道）：

| 通道 | 状态 | 说明 |
|:---|:---|:---|
| `sandbox` | ✅ 默认 | HMAC-SHA256 验签闭环 · 内联 SVG 二维码 · 本地/公网测试 |
| `wechat` | 注册位 | 填商户号/APIv3密钥即切换 |
| `alipay` | 注册位 | 填应用ID/私钥即切换 |
| `cbpay` 数币 | 注册位 | 填商户参数即切换 |

**只需改 `backend/config.py` 的 `PAYMENT_GATEWAY`**，接口签名、验签、幂等、回调全不变。
回调入口：`POST /api/pay/notify`（验签 → 金额核对 → 幂等入账 → 联动开发者状态+贡献分）。

## 📤 数据导出 API（管理员）

```bash
# 需要 LONGHUN_DEV_ADMIN_TOKEN（管理员Token·不硬编码在代码库）
GET /api/export/fee-records?token=xxx&format=csv|json     # 历史缴费账单
GET /api/export/contributions?token=xxx&format=csv|json   # 贡献记录
GET /api/export/code-dna?token=xxx&format=csv|json        # 代码DNA
GET /api/export/developers?token=xxx&format=csv|json      # 开发者名册
```

CSV 带 BOM（Excel 直接打开不乱码）。

## 🔐 数据主权

- 数据库 SQLite 本地存储，无云端同步，不上传任何外部服务
- 敏感信息（邮箱/GPG）仅用于身份凭证，默认不公开
- 删除遵循"不删除只冻结"原则，记录永久留档
