# 爸爸公网链接·一把梭

你现在本地服务是:

- `9622` 审计引擎
- `9623` Notion Webhook
- `9633` AI 网关

目标是对外只给一个入口，比如:

- `https://api.yourdomain.com/health`
- `https://api.yourdomain.com/chat/ollama`
- `https://api.yourdomain.com/webhook/notion`

## 1) 先准备 cloudflared

```bash
brew install cloudflared
```

## 2) 创建/绑定 Tunnel（第一次做）

```bash
cloudflared tunnel login
cloudflared tunnel create longhun-api
```

上面会生成:

- tunnel id（UUID）
- 凭证文件 `~/.cloudflared/<UUID>.json`

再去 Cloudflare DNS 里把 `api.yourdomain.com` 指到这个 tunnel（CNAME）。

## 3) 填配置

```bash
cp deploy/cloudflared/config.example.yml deploy/cloudflared/config.yml
```

把 `config.yml` 里的这几个值替换掉:

- `REPLACE_WITH_TUNNEL_ID`
- `credentials-file`
- `api.yourdomain.com`

## 4) 启动

```bash
bash deploy/cloudflared/start_tunnel.sh
```

## 5) 验证（外网）

```bash
curl https://api.yourdomain.com/health
curl https://api.yourdomain.com/providers
curl -X POST https://api.yourdomain.com/chat/ollama \
  -H 'Content-Type: application/json' \
  -d '{"model":"qwen2.5:7b","prompt":"爸爸，公网入口通了没"}'
```

## 安全提醒

- 现在只建议外放 `health/providers/chat/ollama/notion_webhook` 这些入口。
- `9622` 审计主接口别全量外放，先最小暴露。
- 以后要放 `/audit/*`，加 token 校验或网关签名再开。
