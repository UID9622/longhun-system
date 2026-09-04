# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂 UID9622 主权身份注册系统

**DNA**: `#龍芯⚡️丙午·甲午·癸酉·戊午·䷨损-SOVEREIGN-REGISTRY-v1.0`

## 目标

在龍魂官网部署 UID9622 主权身份注册接口，对接现有 DNA 追溯体系。一旦注册，永久锚定，不可修改、不可转让、不可删除。

## 文件结构

| 文件 | 职责 |
|---|---|
| `registry.py` | 生成 UID、DNA、sovereign_hash、confirm_code，写入 manifest |
| `audit.py` | 三色审计：§9.49/§9.50/§9.51/§9.52 铁律守护 |
| `card.py` | 生成 PNG/HTML 主权身份卡（含 QR 码） |
| `api_routes.py` | FastAPI 路由：`/api/sovereign/*` |
| `cli.py` | `lh sovereign` 命令行入口 |

## 官网接口

```bash
POST /api/sovereign/register
POST /api/sovereign/verify
GET  /api/sovereign/identity/{uid}
GET  /api/sovereign/identities
GET  /api/sovereign/card/{uid}.png
GET  /api/sovereign/card/{uid}.html
POST /api/sovereign/modify-fuse
```

## 数据存储

- 主权记录：`~/.龍魂/sovereign_registry/manifest.json`
- 身份卡：`~/.龍魂/sovereign_registry/cards/`
- 耻辱墙：`~/.龍魂/shame_wall/sovereign.jsonl`

## 注册命令

```bash
lh sovereign register "姓名" "身份证" "证件号" [--device ...] [--gpg ...]
lh sovereign verify UID9622-XXXXXX "签名"
lh sovereign identity UID9622-XXXXXX
lh sovereign list
lh sovereign card UID9622-XXXXXX
```

## 前端入口

- 官网首页导航栏：`🏛️ 主权身份注册`
- 注册页：`/sovereign-register.html`
- 注册完成后展示主权身份卡，可下载 PNG / 打印 HTML 为 PDF

## 不可更改机制

- `manifest.json` 为 append-only
- 任何修改/删除请求调用 `/api/sovereign/modify-fuse` 触发 🔴 熔断
- 熔断行为记录到耻辱墙

## 依赖

已安装到 `~/.龍魂/web/.venv/`：

```bash
fastapi uvicorn pydantic pillow qrcode
```

## 启动官网

```bash
cd ~/.龍魂/web
./start_portal.sh
```

访问：http://127.0.0.1:8445/sovereign-register.html
