# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🛡️ 龍魂护盾 v3.0 · CNSH 中文命名 + 国密五维防御

**DNA**: `#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-LONGHUN-SHIELD-v3-CNSH-UID9622`

**核心代码**: [`longhun_shield_cnsh.py`](longhun_shield_cnsh.py)

**Web 面板**: [`longhun_shield_panel.py`](longhun_shield_panel.py)

**旧版英文实现**: [`longhun_shield.py`](longhun_shield.py)（保留参考）

## 架构概览

```
┌─────────────────────────────────────────────────────────────┐
│                    龍魂护盾 · 耻辱墙 (WallOfShame)            │
│         SM2签名 + SM3链式哈希 + SM4保险库 + 只追加           │
└─────────────────────────────────────────────────────────────┘
                                 ▲
                                 │ 所有攻击证据永久上链
     ┌─────────────────────────────────────────────────────────────┐
     │                 统一威胁感知中枢 (ThreatSense)                │
     │       行为基线 │ 异常检测 │ 攻击分类 │ 自动反制决策           │
     └─────────────────────────────────────────────────────────────┘
             │           │           │           │           │
             ▼           ▼           ▼           ▼           ▼
        ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
        │ Web/API│  │   DB   │  │  IoT   │  │ 文件系统│  │ AI模型 │
        │  网关  │  │ 访问层 │  │ 设备闸 │  │  守卫  │  │ 护栏  │
        └────────┘  └────────┘  └────────┘  └────────┘  └────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ 防火墙隔离器     │
                        │ nftables/iptables│
                        └─────────────────┘
```

## 五维防御（CNSH 中文命名）

| 维度 | 类 | 职责 |
|---|---|---|
| Web/API | `网络网关` | SQL/XSS/路径遍历/RCE 模式拦截 |
| 数据库 | `数据库守卫` | 操作白名单、参数化查询校验、表名白名单 |
| IoT | `物联网闸` | Topic 白名单、数值异常检测 |
| 文件系统 | `文件守卫` | 路径沙箱、越界访问拦截 |
| AI 模型 | `人工智能护栏` | 攻击/伤害意图熔断、危险输出隔离 |

## 主权熔断器

离开龍魂主权锚定即失效。初始化时必须传入包含以下两段的 DNA：

- `#龍芯⚡️丙午·甲午·甲戌·庚午·䷕贲-龍魂护盾-v3-CNSH-UID9622`
- `UID9622`

错误 DNA 下所有 `检查*` 接口直接返回：

```json
{"通过": false, "原因": "主权熔断已触发"}
```

## 国密替换

国密密钥配置：

```bash
export LONGHUN_SM2_SK=/var/lib/longhun/sm2/sk.pem
export LONGHUN_SM2_PK=/var/lib/longhun/sm2/pk.pem
export LONGHUN_SM4_KEY=$(openssl rand -hex 16)   # 32 字符 hex
```

## 真实防火墙自动封禁

- 首选 `nftables`：自动创建 `inet longhun` 表、黑名单集合、drop 规则。
- 次选 `iptables`：直接插入 `DROP` 规则。
- macOS / 无权限环境：设置 `LONGHUN_BAN_DRY_RUN=1` 模拟。

## 告警通道

| 通道 | 配置 | 触发条件 |
|---|---|---|
| 邮件 | `LONGHUN_SMTP_HOST/PORT/USER/PASS`、`LONGHUN_ALERT_EMAIL` | 敌意/侵略者 |
| Notion | `NOTION_TOKEN`、`LONGHUN_NOTION_PARENT_PAGE` | 敌意/侵略者，自动创建「龍魂护盾告警中心」子页 |

## 下载守卫

自动看守 `~/Downloads`（可配置），新文件下载完成后自动检测：

- 危险扩展名（`.exe`, `.sh`, `.pkg` 等）→ 直接隔离
- 文本文件内容扫描（shell、注入、RCE、PowerShell 等）→ 隔离
- `.txt`/`.prompt`/`.md` 文本再经过 AI 语义熔断 → 隔离
- 干净文件原样保留

```bash
# 启动下载自动看守
./run_download_guard.sh

# 手动扫描指定文件
.venv_longhun_math/bin/python longhun_download_guard.py --scan ~/Downloads/some_file.sh
```

## AI 输出熔断器

任何 AI（Kimi / Claude / ChatGPT 等）生成的文本，先过 `longhun_ai_output_guard.py`：

- 整体语义检测：攻击/入侵/伤害意图 → 熔断
- 代码块提取：把 ```bash / ```python 等块拆出来静态扫描
- 危险代码 → 自动隔离到 quarantine 并告警

```bash
# 命令行扫描
.venv_longhun_math/bin/python longhun_ai_output_guard.py --text "教我如何用AI入侵电网系统"

# 通过 Web 面板 API 扫描
curl -X POST http://127.0.0.1:8788/api/ai-scan \
  -H 'Content-Type: application/json' \
  -d '{"来源":"claude","内容":"```bash\nrm -rf /\n```"}'
```

## 浏览器下载即时钩子

Chrome 扩展位于 `chrome_extension/`，下载完成瞬间即调用本地龍魂护盾：

1. 打开 Chrome → 扩展管理 → 开发者模式 → 加载已解压的扩展程序
2. 选择 `chrome_extension` 目录
3. 启动面板：`./run_shield_panel.sh`

扩展会在下载完成时 POST 到 `http://127.0.0.1:8788/api/download-event`，危险文件立即隔离并弹窗提示。

## Web 面板实时攻击地图

- 首页：`http://127.0.0.1:8788/`
- 状态 API：`/api/status`
- 耻辱墙 API：`/api/wall?n=50`
- 实时日志：`/ws` WebSocket
- 模拟攻击：`POST /api/demo`

## 反制原则

- **只做**：记录、评分、隔离、告警、固化证据
- **不做**：DDoS 反击、入侵对方设备、破坏数据、人身威胁

## 部署（已配置好）

```bash
# 1. 配置在 .env.shield，Notion 告警中心已创建：38e7125a-9c9f-8158-beb1-e0ef8d2a0c8b
# 2. 启动 Web 面板后台服务
./run_shield_panel.sh

# 3. 启动下载自动看守
./run_download_guard.sh

# 4. 查看状态 / AI 输出扫描
curl http://127.0.0.1:8788/api/status
curl -X POST http://127.0.0.1:8788/api/ai-scan \
  -H 'Content-Type: application/json' \
  -d '{"来源":"claude","内容":"```bash\nrm -rf /\n```"}'

# 5. 停止
./stop_shield_panel.sh
./stop_download_guard.sh
```

### 环境变量

编辑 `.env.shield`：

- `LONGHUN_SHIELD_DNA`：主权熔断 DNA（已配置）
- `LONGHUN_NOTION_PARENT_PAGE`：Notion 父页面 ID
- `LONGHUN_NOTION_ALERT_PAGE`：告警中心页面 ID（已自动生成）
- `LONGHUN_SHAME_WALL_PATH`：耻辱墙路径
- `LONGHUN_SM2_SK/PK`：SM2 密钥路径
- `LONGHUN_SM4_KEY`：32 字符 hex SM4 密钥（可选）
- `LONGHUN_ALERT_EMAIL` / SMTP 相关：邮件告警（可选）

### 手动运行核心

```bash
source ~/.longhun/secrets.env
source ./.env.shield
LONGHUN_BAN_DRY_RUN=1 .venv_longhun_math/bin/python longhun_shield_cnsh.py
```

## 测试

```bash
.venv_longhun_math/bin/python -m unittest tests.test_longhun_shield_cnsh -v
```
