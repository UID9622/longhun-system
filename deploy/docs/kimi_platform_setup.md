# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🌙 Kimi 开放平台配置 SOP

> **目标**：确认 Kimi API Key 额度、创建应用、了解模型选择。
> **已配置位置**：Mac `~/.bashrc` + launchd / 鲲鹏 `/etc/systemd/system.conf.d/99-longhun-kimi-env.conf`

---

## 第一步：登录 Kimi 开放平台

1. 打开 [Kimi 开放平台](https://platform.moonshot.cn/)。
2. 用购买 699 元包月的账号登录。

---

## 第二步：查看 API 额度

1. 左侧 → **账户管理** / **额度管理**。
2. 确认 **API 调用额度** 有余额。
   - 注意：`699 元包月` 是 Chat 网页/APP 会员，**不一定包含 API 额度**。
   - 如果 API 额度为 0，需要单独充值或购买 API 套餐。
3. 如果显示 `账户已欠费 / suspended`，点击充值。

---

## 第三步：创建 API Key

1. 左侧 → **API Key 管理** → **创建 API Key**。
2. 填写名称，例如：`longhun-kimi-key`。
3. 复制生成的 Key（以 `sk-` 开头）。
4. 把 Key 更新到本地和鲲鹏：
   - **Mac**：`~/.bashrc` 和 `~/Library/LaunchAgents/com.longhun.kg-api.plist` 里的 `KIMI_API_KEY` / `MOONSHOT_API_KEY`。
   - **鲲鹏**：`/etc/systemd/system.conf.d/99-longhun-kimi-env.conf` 里的 `DefaultEnvironment=KIMI_API_KEY=... MOONSHOT_API_KEY=...`。
5. 重启相关服务：
   ```bash
   # Mac
   launchctl unload ~/Library/LaunchAgents/com.longhun.kg-api.plist
   launchctl load ~/Library/LaunchAgents/com.longhun.kg-api.plist
   launchctl unload ~/Library/LaunchAgents/com.longhun.notion-bridge.plist
   launchctl load ~/Library/LaunchAgents/com.longhun.notion-bridge.plist

   # 鲲鹏
   ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27
   systemctl daemon-reload
   for s in $(systemctl list-unit-files "longhun-*.service" --no-legend | awk '{print $1}'); do
     systemctl restart "$s"
     sleep 1
   done
   ```

---

## 第四步：测试 API

```bash
# Mac
source ~/.bashrc
curl https://api.moonshot.cn/v1/chat/completions \
  -H "Authorization: Bearer $MOONSHOT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"moonshot-v1-auto","messages":[{"role":"user","content":"你好"}]}'
```

如果返回 `"choices"`，说明 Key 可用。

---

## 第五步：模型选择建议

| 场景 | 推荐模型 |
|:---|:---|
| 普通对话 / 快速回复 | `moonshot-v1-auto` |
| 长文档分析 | `moonshot-v1-128k` |
| 代码/推理 | `moonshot-v1-32k` |
| 低成本试探 | `moonshot-v1-8k` |

在 Notion 对话桥里指定：
```bash
lh notion-bridge chat "问题" --provider kimi --model moonshot-v1-auto
```

---

## 常见问题

### Q1: 返回 `exceeded_current_quota_error`
API 额度耗尽，需要充值。

### Q2: 返回 `429 Too Many Requests`
触发限流，稍后再试，或检查是否多个服务共用同一个 Key。

### Q3: Notion 对话桥走不到 Kimi
检查 `~/.bashrc` 里的 `MOONSHOT_API_KEY` 是否设置，以及 Notion 对话桥 launchd plist 里是否也写了 Key。
