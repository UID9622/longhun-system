# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍智守飞书机器人配置 SOP

> **目标**：把鲲鹏上的 `longhun-longzhishou` 服务接入飞书自建应用，实现群里 @机器人自动反诈/国学/审计。
> **预计时间**：5–10 分钟
> **无需写代码**，只需在飞书开放平台点鼠标。

---

## 前置检查

1. 服务已运行：
   ```bash
   ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27
   systemctl status longhun-longzhishou.service --no-pager
   curl http://127.0.0.1:8783/health
   ```
2. 安全组/防火墙已放行 TCP `8783`（华为云安全组 + 服务器防火墙）。
3. Webhook 公网地址（走 Nginx 80 端口，无需开放 8783）：
   ```
   http://119.13.90.27/longzhishou/webhook
   ```

---

## 第一步：创建飞书自建应用

1. 打开 [飞书开放平台](https://open.feishu.cn/)。
2. 用企业/个人账号登录（建议用你要部署机器人的企业）。
3. 右上角 → **开发者后台** → **创建企业自建应用**。
4. 填写：
   - 应用名称：`龍智守`
   - 应用描述：`龍魂生活/办公智能守护入口 — 反诈、国学推演、DNA 审计`
   - 应用头像：可上传 `portal/` 下的龍魂 logo
5. 点击 **创建应用**。

---

## 第二步：获取 App ID / App Secret

1. 进入刚创建的应用 → 左侧 **凭证与基础信息**。
2. 复制：
   - `App ID`（形如 `cli_xxxxxxxx`）
   - `App Secret`（点击显示并复制）
3. 把这两个值填入鲲鹏 `.env`：
   ```bash
   ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27
   nano /opt/longhun-system/.env
   ```
   确保有以下三行（`FEISHU_CHAT_ID` 下一步再填）：
   ```bash
   FEISHU_APP_ID=cli_xxxxxxxx
   FEISHU_APP_SECRET=xxxxxxxx
   FEISHU_CHAT_ID=
   ```
4. 重启服务：
   ```bash
   systemctl restart longhun-longzhishou.service
   ```

---

## 第三步：开启机器人能力

1. 左侧菜单 → **添加应用能力** → 添加 **机器人**。
2. 进入 **机器人** 配置页：
   - 机器人名称：`龍智守`
   - 可见范围：选择要让机器人出现的群组/成员。
3. 保存。

---

## 第四步：配置事件订阅（Webhook）

1. 左侧菜单 → **事件订阅**。
2. 打开 **启用事件订阅**。
3. **请求地址** 填：
   ```
   http://119.13.90.27/longzhishou/webhook
   ```
4. 点击 **验证**。如果显示 **验证通过**，说明鲲鹏服务已连上。
   - 如果失败：检查 Nginx 是否运行、`curl http://119.13.90.27/longzhishou/webhook` 是否通。
5. 在 **订阅事件** 中点击 **添加事件**，搜索并勾选：
   - `im.message.receive_v1`（接收消息事件）
6. 保存。

---

## 第五步：把机器人拉进群并获取 chat_id

1. 在飞书里打开目标群聊 → 点击右上角 **设置** → **群机器人** → **添加机器人**。
2. 选择 **龍智守** 并添加。
3. 此时群里 @机器人 发一条消息，例如：
   ```
   @龍智守 测试
   ```
4. 机器人会回复一张交互式卡片。
5. 如果需要固定默认群（守护进程启动时自动发通知），查看鲲鹏日志里的 `chat_id`：
   ```bash
   ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27
   tail -20 /var/log/longhun/longzhishou.log
   ```
   看到形如 `oc_62fdd6dc95007419bf17d5a70b922d96` 的字符串就是 `chat_id`。
6. 填入 `.env`：
   ```bash
   FEISHU_CHAT_ID=oc_xxxxxxxx
   ```
7. 重启服务：
   ```bash
   systemctl restart longhun-longzhishou.service
   ```

---

## 第六步：可选 — 加密验证

如果飞书后台要求 **Encrypt Key**：
1. 在事件订阅页生成一个 **Encrypt Key**。
2. 复制到 `.env`：
   ```bash
   FEISHU_ENCRYPT_KEY=xxxxxxxx
   ```
3. 重启服务。

> 不配置 Encrypt Key 也能用，但建议生产环境开启。

---

## 第七步：可选 — 发布应用

1. 飞书后台 → **版本管理与发布** → **创建版本**。
2. 填写版本号、更新说明。
3. 点击 **申请发布**。
4. 管理员审批后，机器人对所有可见成员可用。

---

## 常见问题

### Q1: 验证 Webhook 时提示 "请求失败"
- Nginx 是否运行：`systemctl status nginx`。
- 公网是否通：`curl http://119.13.90.27/longzhishou/webhook`。
- 服务是否运行：`systemctl status longhun-longzhishou.service`。

### Q2: 机器人不回复
- 查看日志：`tail -50 /var/log/longhun/longzhishou-error.log`
- 确认 `FEISHU_APP_ID` / `FEISHU_APP_SECRET` 已正确写入 `/opt/longhun-system/.env`。
- 确认事件订阅里勾选了 `im.message.receive_v1`。

### Q3: 群里 @机器人没反应
- 确认机器人已添加到该群。
- 确认应用已发布或群在可见范围内。

---

## 相关文件

- 守护进程：`/opt/longhun-system/bin/lh_longzhishou_daemon.py`
- 服务文件：`/etc/systemd/system/longhun-longzhishou.service`
- 环境变量：`/opt/longhun-system/.env`
- 日志：`/var/log/longhun/longzhishou.log` / `longzhishou-error.log`
