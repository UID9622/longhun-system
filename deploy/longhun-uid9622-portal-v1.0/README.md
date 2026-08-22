# 龍魂·uid9622.cn 三入口门户部署包 v2.0

## 参考来源
- 龍魂系统 GitHub 主仓库: https://github.com/UID9622/longhun-system
- 龍魂 10_PORTAL 目录结构 (静态站点入口)
- 龍魂 CNSH 编辑器 / 七因子行为密码学 / DNA 追溯系统
- 龍魂官网: longhun888.com
- 本地开发环境: localhost:8899/apps/knowledge.html

## 修正了什么
- 新建本部署包，无上一版
- 基于仓库现有 10_PORTAL 结构，补充缺失的三入口体系
- 新增无障碍入口 (WCAG 2.1 AA 标准)
- 新增开发者入口 (API 文档 / SDK / 技术接入)
- 新增普通者入口 (简洁易用，面向大众)
- 全量 Nginx 配置 + SSL + 本地 Kimi 可执行脚本

## 保留了什么
- 龍魂 P0 安全基线 (确认码闸门 / 密钥环境变量 / GPG 签名)
- 现有 DNA 服务器 7000 端口不动
- longhun888.com 现有部署不动
- 仓库原有 10_PORTAL 内容不动 (本包为增量补充)

## 实测了什么（2026-08-16 公网实机验证）
- 🟢 所有 HTML/CSS/JS 语法通过浏览器标准校验
- 🟢 Nginx 配置语法逻辑校验通过
- 🟢 **已在真实鲲鹏服务器(119.13.90.27)增量部署上线**（不动现有官网 30 个 nginx 配置）
- 🟢 **公网实测全绿**: `/accessible.html` `/developer.html` `/common/*` `/index.html` 全部 HTTP 200
- 🟢 **部署脚本 v2.0 实机走通**: 幂等检查 → 同步 → nginx校验 → reload → 公网验证 → 日志落盘 → Bark回调
- 🟢 部署日志: `logs/portal-deploy-*.log`（时间戳/每步结果/HTTP状态码）
- 🟡 无障碍入口按 WCAG 2.1 AA 设计规范编写，未经过真实屏幕阅读器测试
- 🟡 Bark 回调通道 key 为占位符，配置真实 `BARK_KEY` 后自动生效

---

## 三入口体系

| 入口 | 文件 | 路径 | 受众 | 核心功能 |
|------|------|------|------|----------|
| **普通者** | `portal/index.html` | `/` | 普通用户 | 系统介绍、快速了解、下载入口 |
| **无障碍** | `portal/accessible.html` | `/accessible.html` | 视障/听障/老年 | 大字体、高对比、语音朗读、键盘全导航 |
| **开发者** | `portal/developer.html` | `/developer.html` | 开发者/技术人 | API 文档、SDK、CNSH 规范、接入指南 |

---

## 快速开始

### 方式一: 本地 Kimi 一键部署 (推荐)
```bash
# 1. 下载部署包并解压
# 2. 进入目录
chmod +x scripts/*.sh
./scripts/deploy-local.sh

# 3. 浏览器访问
open http://localhost:8899
```

### 方式二: 鲲鹏服务器公网部署（v2.0 正规增量·推荐）
```bash
chmod +x scripts/*.sh

# 常规部署（默认鲲鹏 119.13.90.27，密钥 ~/.ssh/longhun_kunpeng_ed25519）
./scripts/deploy-server.sh

# 带 Bark 部署完成回调（配置真实 BARK_KEY 后生效）
BARK_KEY=你的key ./scripts/deploy-server.sh

# 指定服务器
SERVER_IP=1.2.3.4 ./scripts/deploy-server.sh
```
安全特性: 幂等检查（已存在跳过追加）· 远端 nginx 配置备份 · `nginx -t` 校验 · reload ·
公网 5 URL 验证 · 部署日志 `logs/portal-deploy-*.log` · Bark 回调通知。

访问: https://uid9622.cn/accessible.html

### 方式三: 手动复制到现有 10_PORTAL
```bash
# 直接复制 portal/ 目录到本地 longhun-system/10_PORTAL/
cp -r portal/* ~/longhun-system/10_PORTAL/
# 然后按仓库原有流程部署
```

---

## 文件清单

```
longhun-uid9622-portal-v1.0/
├── README.md                          # 本文件
├── portal/
│   ├── index.html                     # 🏠 普通者入口 (主站)
│   ├── accessible.html                # ♿ 无障碍入口
│   ├── developer.html                 # 🛠 开发者入口
│   ├── common/
│   │   ├── style.css                  # 共享样式
│   │   ├── accessible.css             # 无障碍专用样式
│   │   ├── developer.css            # 开发者专用样式
│   │   ├── main.js                    # 共享脚本
│   │   └── accessible.js              # 无障碍辅助脚本
│   └── assets/
│       └── (图标/图片占位)
├── nginx/
│   ├── uid9622-portal.conf            # Nginx 三入口站点配置
│   └── security-headers.conf          # 安全响应头
├── scripts/
│   ├── deploy-local.sh                # 🖥 本地 Kimi 一键部署
│   ├── deploy-server.sh               # 🌐 鲲鹏服务器部署
│   ├── sync-to-server.sh              # 本地→服务器同步
│   └── lh-portal.sh                   # lh 命令扩展 (portal 子命令)
└── configs/
    └── robots.txt                     # 搜索引擎爬虫规则
```

---

## Makefile 与 lh 命令

### Makefile 统一入口
```bash
make local      # 本地启动 (localhost:8899)
make start      # 同 local
make stop       # 停止本地服务
make status     # 查看状态
make sync       # 同步到服务器 (SERVER_IP 可覆盖)
make deploy     # 服务器一键部署 (Nginx + SSL)
```

### lh portal 扩展
```bash
# 安装
cp scripts/lh-portal.sh ~/.longhun/bin/lh-portal && chmod +x ~/.longhun/bin/lh-portal

# 使用
lh portal start     # 本地启动
lh portal stop      # 停止本地
lh portal sync      # 同步到服务器
lh portal deploy    # 服务器部署
lh portal status    # 查看状态
```

---

## 本地 Kimi 执行说明

本部署包专为"本地 Kimi 执行"设计:

1. **deploy-local.sh** 可在任何 Mac/Linux 终端直接运行，无需 root (使用 1024+ 端口)
2. 自动检测 Python3 或 Node.js 作为本地服务器
3. 启动后输出访问地址，自动打开浏览器
4. 支持热重载 (文件修改后刷新即生效)

---

## 安全基线 (P0)

- 所有脚本含确认码闸门
- 密钥通过环境变量注入，禁止硬编码
- Nginx 仅开放 80/443，管理端口不暴露
- SSL 强制 HSTS
- 安全响应头 (CSP/X-Frame-Options/XSS-Protection)
- 日志全量审计

---

DNA: #龍芯⚡️丙午·甲申·丁未·丙午·䷝离为火-三入口门户-v1.0
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
