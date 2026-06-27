# 龍魂令系统 · LongHun Orders

**DNA:** `#龍芯⚡️2026-06-28-LONGHUN-ORDERS-v1.0`

龙魂令是龍魂生态的公开裁决平台，部署在 `https://longhun888.com/orders/`。

## 页面

- `/orders/` — 首页，四大令级、执行方式、证据链要求
- `/orders/status/<anchor_id>` — 查询令的状态、级别、进度
- `/orders/initiate` — 发起入口（需 `LONGHUN_ORDERS_INITIATE_KEY`）
- `/orders/bulletin` — 已公示令公告栏

## API

- `/orders-api/health`
- `/orders-api/list`

## 部署

```bash
rsync -avz --delete -e 'ssh -i ~/.ssh/id_ed25519_uid9622' ./ root@119.13.90.27:/var/www/longhun/orders/
ssh -i ~/.ssh/id_ed25519_uid9622 root@119.13.90.27 'systemctl restart longhun-orders'
```

## 令级

| 级别 | 名称 | 卦象 | 证据链要求 |
|------|------|------|------------|
| 1 | 问询令 | ☵ 水洄 | 1 层来源 + 时间戳 |
| 2 | 警示令 | ☶ 山止 | 2 层独立来源 + 摘要 |
| 3 | 封禁令 | ☲ 火明 | 3 层来源链 + 哈希固化 |
| 4 | 追缉令 | ☰ 天行 | 六层来源链 + GPG 签名 + 链式哈希 |

---

*令出即锚 · 锚定即追溯 · 追溯即公示*
