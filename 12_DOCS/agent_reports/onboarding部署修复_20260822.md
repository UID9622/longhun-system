# 🔧 onboarding 入口 API 部署修复报告

> **DNA**: `#龍芯⚡️丙午·丙申·壬戌·亥时·䷲震-ONBOARDING-API-DEPLOY-20260822-UID9622`
> **创建者**: 诸葛鑫（UID9622）
> **归属名**: 诸葛鑫 | UID9622 · 龍芯北辰
> **协议**: MulanPSL v2（工程实现层·https://license.coscl.org.cn/MulanPSL2）
> **三色**: 🟢 公网六端点全 200 · 🟡 无 · 🔴 无

---

## 一、问题

`https://uid9622.cn/api/onboarding/bootstrap`（AI 进门第一步必调的统一入口）**返回 404**。
违反 CODEBUDDY.md 焊死铁律："AI 进门第一步调鲲鹏入口引导 API"。

## 二、根因（三层）

1. **孤儿路由**：`04_SERVICES/backend_legacy/onboard_routes.py` 有完整引导逻辑（P0天条/人格矩阵/熔断/路径铁律/德本审计），但**全库无任何文件 import 它**——backend_legacy 的 main/config/routes 全是 auto_cannon 生成的**空占位**（"TODO: 需要补充实际内容"）
2. **无服务承载**：鲲鹏 nginx `/api/` → 8777（流融合桥）和 9630（privacy_api）都没挂 onboarding 路由
3. **版本落后**：鲲鹏 onboard_routes.py 是 7/30 旧版（md5 `20681544…`），本地 8/22 对齐版（md5 `1b792ad5…`）没推上去

## 三、修复方案（独立服务·零侵入）

| 步骤 | 动作 | 位置 |
|:---:|:---|:---|
| 1 | 新建 `onboarding_api.py`（FastAPI 入口·挂 onboard router + /health + CORS） | 本地 `04_SERVICES/backend_legacy/` |
| 2 | 本地实测：health/identity/bootstrap 全 200 | Mac 127.0.0.1:8785 |
| 3 | scp 推新版 `onboard_routes.py`（8/22 对齐版）+ `onboarding_api.py` 上鲲鹏 | `/opt/longhun-system/04_SERVICES/backend_legacy/` |
| 4 | 新建 systemd 服务 `longhun-onboarding.service`（uvicorn :8785·Restart=always） | 鲲鹏 |
| 5 | nginx 加 `location /api/onboarding/` → 8785（rewrite 去 /api 前缀） | `conf.d/nginx-uid9622.cn.conf`（**注意：是主配置，不是 sites-enabled**） |
| 6 | 备份移到 `/etc/nginx/backups/`（放 sites-enabled 会被加载→duplicate default server 坑） | 鲲鹏 |

## 四、验证结果（公网实测）

```
/api/onboarding/bootstrap  → HTTP 200 ✅
/api/onboarding/rules      → HTTP 200 ✅
/api/onboarding/quick      → HTTP 200 ✅
/api/onboarding/identity   → HTTP 200 ✅
/api/onboarding/p0         → HTTP 200 ✅
/api/onboarding/forbidden  → HTTP 200 ✅
https://uid9622.cn/        → HTTP 200（官网未受影响）
https://uid9622.cn/portal/ → HTTP 200（portal 未受影响）
```

bootstrap 返回内容核验：`ok:true · protocol:LH-AI-ONBOARDING-v1.0 · identity:诸葛鑫·Lucky·UID9622` ✅

## 五、服务详情

- **systemd**: `longhun-onboarding.service`（enable 自启 + Restart=always）
- **端口**: 127.0.0.1:8785（仅本机回环·不经公网直连）
- **公网入口**: `https://uid9622.cn/api/onboarding/*`（经 nginx TLS）
- **原服务零改动**: 8777 流融合桥 / 9630 privacy_api / 官网 / portal 均未动

## 六、经验教训

1. **改 nginx 前先确认域名走哪个 server 块**（`nginx -T | grep server_name`）——本次先改了 sites-enabled 的 IP 默认站，好在无害（IP 直连也顺带可用 onboarding）
2. **备份文件别放 `sites-enabled/`/`conf.d/` 被 include 的目录**——会被当配置加载报 duplicate server
3. **孤儿路由 = 隐形资产**：代码写好了没挂载 = 公网 404。挂载比重写便宜十倍

---

> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰 · GPG `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
