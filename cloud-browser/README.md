# 龍魂·云浏览器服务 v2.0（全平台生态版）

> DNA: #龍芯⚡️丙午·乙巳·癸酉·癸亥·䷵归妹-☰乾-CLOUD-BROWSER-v2.0-FULL-PLATFORM
> 创建者: 诸葛鑫（UID9622） · License: MulanPSL v2
> 核心价值: **登录一次·AI 永久替你干活**——浏览器登录态持久化缓存在鲲鹏，AI 通过 API 带登录态操作，老大不用每次自己登录。
> v2.0 新增: **39 平台全接入**（CSDN/知乎/公众号/GitHub/阿里云/华为云/Notion/飞书…）· 一句话自然语言调度

## 一句话架构

```
鲲鹏(119.13.90.27)
└─ Docker: longhun-cloud-browser (:8899·仅回环)
   ├─ Chromium 持久化档案  /data/browser/profiles/<站点>/   ← 登录态自动落盘
   ├─ 加密保险柜备份        /data/browser/vault/*.gpg        ← AES256 对称加密
   ├─ 全平台调度            platforms.yaml(39平台) + platform_dispatcher.py
   └─ FastAPI 控制接口      execute/platforms/open/action/screenshot/snapshot
```

## 🔥 v2.0 新能力

### 一句话执行（全平台调度）
说一句话，自动打开对应平台（每个平台独立档案=独立登录态）：
```
POST /api/execute {"command": "打开阿里云开通短信服务"}
POST /api/execute {"command": "在CSDN发布文章，同步到知乎"}
POST /api/execute {"command": "同步代码到GitHub和Gitee"}
POST /api/execute {"command": "搜索龍魂系统"}
```
调度器按「平台名+别名+描述」关键词匹配（长关键词优先消歧：微信公众号≠微信），
返回每个平台打开后的页面快照，AI 可接着用 `/api/browser/action` 精细化操作。

### 39 平台一览
| 类目 | 平台 |
|:---|:---|
| 内容创作(10) | CSDN 知乎 公众号 微博 抖音 B站 头条号 小红书 掘金 博客园 |
| 代码开源(6) | GitHub Gitee GitLab 开源中国 Coding GitCode |
| 云平台AI(6) | 华为云 阿里云 腾讯云 DeepSeek Kimi OpenAI |
| 知识协作(6) | Notion 飞书 钉钉 企业微信 Slack Discord |
| 社区社交(4) | 微信 QQ 即刻 豆瓣 |
| 工具服务(7) | 百度 邮箱 短信服务 日历 腾讯会议 网盘 支付 |

### 🔐 强 Token（v2.0 焊死）
- Token 由 `.env` 的 `BROWSER_API_TOKEN` 注入（64 位随机 hex，`secrets.token_hex(32)` 生成）
- **无默认值**——未配置直接拒绝启动（防默认口令裸奔）
- 校验用 `secrets.compare_digest` 恒时比较（防时序攻击）
- 保险柜密钥 `BROWSER_VAULT_KEY` 同样强随机

## 核心原理

`launch_persistent_context(user_data_dir=...)` 是 Playwright 的持久化模式——
浏览器把 **cookies / localStorage / session** 全部写入档案目录。只要档案在，登录态就在。
Docker 卷 `browser-data` 保证容器重启不丢。

### ⚠️ 登录态持久化行为（实测结论 2026-08-15）
| 数据类型 | 重启后是否保留 | 说明 |
|:---|:---:|:---|
| localStorage | ✅ | 已验证保留 |
| 持久 cookie（带 expires） | ✅ | 已验证保留（阿里云等主流平台登录 cookie 属此类） |
| session cookie（expires=-1） | ❌ | **浏览器原生理行为**（真实 Chrome 也一样）：无过期时间的 cookie 关闭即失效 |

> 结论：主流平台（阿里云/腾讯云/各种 SaaS）登录态**重启后保持**。
> 纯 session-cookie 站点的登录态在容器重启后会掉，属网站设计（非缺陷）。
> 浏览器进程常驻期间（容器运行中）session cookie 一直在，AI 随时可用。

## 优雅关闭（登录态刷盘）
服务收到 SIGTERM（`docker restart`/`docker stop`）时会先正常关闭所有浏览器
（`ctx.close()` 触发 Chromium 把 cookie/localStorage 刷盘），再退出进程。
日志可见：`>>> shutdown 信号收到` → `全部浏览器已优雅关闭（登录态已刷盘）`。

## API 手册（AI 调用用）

所有接口需带 `Authorization: Bearer <BROWSER_API_TOKEN>`。

| 接口 | 方法 | 说明 |
|:---|:---|:---|
| `/health` | GET | 服务状态 + 平台数 + 档案列表 |
| `/api/execute` | POST | `{command}` 一句话执行：解析→打开平台→返回快照 |
| `/api/platforms` | GET | 39 平台列表（按类目分组） |
| `/api/browser/open` | POST | `{profile, url}` 打开站点（自动启动持久化浏览器） |
| `/api/browser/action` | POST | `{profile, action, args}` 执行动作（见下） |
| `/api/browser/screenshot?profile=` | GET | 返回 PNG 截图 |
| `/api/profiles` | GET | 已保存的登录档案列表 |
| `/api/vault/backup` | POST | `{profile}` 加密备份档案到保险柜 |
| `/api/vault/list` | GET | 保险柜备份列表 |

### action 支持的动作
- `goto`   `{url}` 跳转
- `click`  `{selector}` 点击（CSS 选择器）
- `type`   `{selector, text}` 输入
- `press`  `{key}` 按键（如 `Enter`）
- `wait`   `{ms}` 等待
- `screenshot` 截图（返回 base64）
- `snapshot` 页面可读快照（title/url/输入框/按钮/链接/文本——AI 理解页面用）
- `cookies` 返回域名与数量（**绝不返回 cookie 值**·数据主权）
- `login-check` 登录态判断（URL/标题/cookie 域名/文本片段）
- `close` 关闭当前档案浏览器

### 典型流程（AI 替老大办事）
```bash
# 1. 打开站点（首次会自动创建档案）
curl -s -X POST http://127.0.0.1:8899/api/browser/open \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"profile":"aliyun","url":"https://account.aliyun.com"}'

# 2. 看页面（snapshot 给 AI 理解，screenshot 给老大确认）
curl -s -X POST http://127.0.0.1:8899/api/browser/action \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"profile":"aliyun","action":"snapshot"}'

# 3. 需要验证码/扫码 → 截图给老大，老大人工配合一次 → 登录态落盘
# 4. 之后 AI 直接操作，无需再登录
curl -s -X POST http://127.0.0.1:8899/api/browser/action \
  -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
  -d '{"profile":"aliyun","action":"click","args":{"selector":"#search"}}'
```

## 部署（鲲鹏·已上线）

```bash
# 服务位置
cd /opt/cloud-browser
docker compose up -d            # 容器: longhun-cloud-browser :8899(仅回环)
docker compose down && up -d    # 重建（镜像已固化 chromium-1179，无需重新下载）

# 环境变量（v2.0 用 .env 文件·docker compose 自动读取·权限 600）
# cloud-browser/.env 内容:
#   BROWSER_API_TOKEN=<64位随机hex>   ← secrets.token_hex(32) 生成·无默认值
#   BROWSER_VAULT_KEY=<64位随机hex>   ← 保险柜加密密钥
chmod 600 .env
# 换 token: 改 .env → docker compose down && docker compose up -d
```

> ⚠️ 镜像已用 `docker commit` 固化（含 chromium-1179 + headless_shell-1179）。
> 若日后 `docker compose build` 重建，Dockerfile 内已含 `python3 -m playwright install chromium` 自动补齐，不会缺浏览器。

## 公网访问（可选·nginx 反代）

鲲鹏 nginx 加一条（`conf.d/` 下），控制台页面走公网，API 仅本机：
```nginx
location /browser/ {
    proxy_pass http://127.0.0.1:8899/;
    proxy_set_header Authorization $http_authorization;
}
location = /browser/console { alias /opt/cloud-browser/console.html; }
```
> 建议 API 不对外暴露，AI 在鲲鹏本机调用即可；老大看截图走控制台（只读）。

## 安全基线（P0 数据主权）
- 登录凭据只存自己服务器（鲲鹏卷）· 不传任何第三方
- cookie 值接口永不返回（`cookies` 只给域名+数量）
- 档案加密备份（AES256·密钥环境变量注入·不落代码）
- 服务只监听 127.0.0.1 · Bearer Token 鉴权
- 操作日志脱敏：不打印 cookie / 密码原文
- 验证码/扫码/人脸等环节 AI 无法代替，需老大人工配合一次（这是登录安全设计，不是缺陷）

## 文件清单
```
cloud-browser/
├─ backend/browser_service.py        # 核心服务（单 worker 串行·持久化·优雅关闭·v2.0 全平台 API）
├─ backend/platform_dispatcher.py    # 平台调度器（自然语言→平台×动作×目标）
├─ backend/platforms.yaml            # 39 平台配置（名称/URL/别名/类目/动作）
├─ backend/requirements.txt          # fastapi/uvicorn/playwright==1.53.0/pydantic/pyyaml
├─ .env                              # 🔐 强 Token + 保险柜密钥（chmod 600·不入 git）
├─ Dockerfile                        # 官方 Playwright 镜像 + apt pip + 浏览器固化
├─ docker-compose.yml                # 卷持久化·内存限制·回环监听·代码挂载
├─ console.html                      # 控制台 v2.0（一句话执行/平台列表/截图/快照）
└─ README.md                         # 本文档
```
