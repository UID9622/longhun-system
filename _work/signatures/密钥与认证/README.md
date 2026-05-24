# 龍魂密钥与认证中心
# DNA: #龍芯⚡️2026-05-21-KEY-AUTH-CENTER-v1.0

## 目录结构

```
密钥与认证/
├── API密钥/
│   └── 密钥位置索引.md     # 所有API密钥的位置（不存实际密钥）
├── GPG签名/
│   ├── GPG签名指南.md
│   ├── 快速签名指南-已有密钥.md
│   ├── 授权声明签名.asc
│   ├── 数字身份签名区块-标准版.md
│   ├── 签名工具使用说明.md
│   └── 🔐 UID9622密钥管理中心-统一身份激活码确认码总库.md
├── MCP配置/
│   └── longhun888_MCP_v0.2.md    # MCP接入完整指南
└── 文档/
```

---

## 快速操作

### 填写 Notion Token（让MCP能用）
```bash
nano ~/.longhun/secrets.env
# 填 NOTION_TOKEN=ntn_你的token
```

### 检查 GPG 密钥
```bash
gpg --list-keys
# 你的指纹: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
```

### GPG 签名文件
```bash
gpg --armor --detach-sign 文件名
```

### 启动 MCP 服务
```bash
双击桌面「龍魂MCP启动.command」
# 或: bash ~/longhun-system/命令/开NotionMCP9623.sh
```

---

## 安全铁律

1. **密钥永不上传** - .env / secrets 永远在 .gitignore
2. **最小权限** - API token 只给必要权限
3. **定期轮换** - Token 90天换一次
4. **审计留痕** - 每次使用都有 DNA 签名

---

UID9622 · 龍魂系统 · 2026-05-21
