# 🔐 Lucky保险库 密码·API·凭证·密鑰 全在这里

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：协议 · 未经同行评审（如适用）
> 版本：v1.0
> 作者：UID9622 · 龍芯北辰
> 协作者：（待补充，如无请删除此行）
> 授权：CC BY-NC-SA 4.0 · 科技主权归属 UID9622 · 中华人民共和国
> 平台：本地
> 审核状态：草稿

**DNA**: `#龍芯⚡️2026-03-31-LUCKY_B5D8-v2.0``  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

> 本文檔按《龍魂文檔標準模板 v1.0》整理。
> 性質：協議 · 未經同行評審（如適用）
> 版本：v2.0
> 作者：UID9622 · 龍芯北辰
> 協作者：（待補充，如無請刪除此行）
> 授權：CC BY-NC-SA 4.0 · 科技主權歸屬 UID9622 · 中華人民共和國
> 平台：本地
> 審核狀態：草稿

**DNA**: `#龍芯⚡️2026-03-31-LUCKY_B5D8-v2.0`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

# 🔐 Lucky保险库 | 密码·API·凭证·密鑰 全在这里

<aside>
🔐

**P0级·仅Lucky可见·永不分享**

- 这个页面是你的数字保险库
- 所有密码、API、凭证、SSH全在这里
- 发现泄露立即撤销对应凭证

**DNA：**#龍芯⚡️2026-03-31-LUCKY_B5D8-v2.0

**确认码：** #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅

</aside>

---

## 🔑 核心身份信息

```jsx
姓名：诸葛鑫（Lucky）
手机：13968882319
微信：UID9622_CEO

Proton邮符1：luckyoathnotlog@proton.me（主控·ChatGPT绑定）
Outlook邮符1：fireroot.lad@outlook.com（备用）
QQ邮符1：346045695@qq.com

Notion工作区：📎 龍芯北辰｜UID9622
当前用户URL：user://<POTENTIAL_SECRET_PLACEHOLDER>
```

---

## 💻 设备DNA指纹

```
设备：MacBook Pro 16-inch (Nov 2023)
芯片：Apple M4 Max (16核)
内存：64GB
序列号：KVQQ7KLF76
硬件UUID：<POTENTIAL_SECRET_PLACEHOLDER>
预置UDID：00006041-000C615E3E31801C
```

---

## 🔐 API密鑰仓库

<aside>
⚠️

发现泄露立即撤销！不要分享这个页面给任何人。

</aside>

### Notion API

```jsx
// ── Token 1：旧版（2025-11-23配置）──
<POTENTIAL_SECRET_PLACEHOLDER>
状态：🟡 旧版·备存
配置时间：2025-11-23
权限：读取+写入

// ── Token 2：claudeMVP护盾专用（2026-04-04配置）──
<POTENTIAL_SECRET_PLACEHOLDER>
状态：🟢 最新·护盾专用
配置时间：2026-04-04
权限：读取+写入
用途：龍魂窗口加密护盾 v1.7 · Cmd+Shift+S 一键归档
```

### 🛡️ 护盾 .env 配置模板（复制到终端执行）

```bash
# 龍魂护盾 · Notion API 接通三步
# 第一步：创建配置目录
mkdir -p ~/.cnsh

# 第二步：写入 .env（直接复制整段跑）
cat > ~/.cnsh/.env << 'EOF'
NOTION_TOKEN=<POTENTIAL_SECRET_PLACEHOLDER>
NOTION_INBOX_PAGE_ID=你的炼丹炉页面32位ID
EOF

# 第三步：验证是否通（返回你的名字就成功）
curl -s https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer <POTENTIAL_SECRET_PLACEHOLDER>" \
  -H "Notion-Version: 2022-06-28" | grep -o '"name":"[^"]*"'
```

> ⚡ 炼丹炉页面ID获取方式：打开 [🧩 龍魂碎片库·待整理·先扔进来再说｜UID9622](%E6%AC%A2%E8%BF%8E%E6%9D%A5%E5%88%B0%F0%9F%92%8E%20%E9%BE%8D%E8%8A%AF%E5%8C%97%E8%BE%B0%EF%BD%9CUID9622%EF%BC%81/%F0%9F%8C%8C%20UID9622%20%E9%BE%8D%E9%AD%82%E5%B7%A5%E4%BD%9C%E9%97%B4%20%C2%B7%20%E6%80%BB%E5%AF%BC%E8%88%AA%20v1%200/%F0%9F%A4%96%2004%20%C2%B7%20%E4%BA%BA%E6%A0%BC%E7%9F%A9%E9%98%B5/%E2%9A%A1%20%E9%BE%8D%E9%AD%82%E5%AE%9D%E5%AE%9D%E7%B3%BB%E7%BB%9F%20v1%203%EF%BD%9C%E5%BF%AB%E6%8D%B7%E5%8D%87%E7%BA%A7%E7%89%88%C2%B7%E5%8F%A4%E4%BB%8A%E5%90%8D%E4%BA%BA%E6%99%BA%E6%85%A7%C2%B7%E4%B8%AA%E6%80%A7%E8%BE%B9%E7%95%8C%C2%B7%E8%BE%93%E5%85%A5%E8%AF%86%E5%88%AB/%F0%9F%A7%A9%20%E9%BE%8D%E9%AD%82%E7%A2%8E%E7%89%87%E5%BA%93%C2%B7%E5%BE%85%E6%95%B4%E7%90%86%C2%B7%E5%85%88%E6%89%94%E8%BF%9B%E6%9D%A5%E5%86%8D%E8%AF%B4%EF%BD%9CUID9622%<POTENTIAL_SECRET_PLACEHOLDER>.md) 页面 → URL中32位字母数字串就是ID
> 

### 千问（Qwen）API

```jsx
<OPENAI_API_KEY_PLACEHOLDER>
状态：🟢 已更新
更新日期：2026-04-02
用途：千问API调用
```

### 知乎z_c0 Cookie

```jsx
2|1:0|10:1774369051|4:z_c0|92:Mi4xNVJvS3BRQUFBQURRY1pUeEdrVUhIQmNBQUFCZ0FsVk4td212YWdCU2ViVzBaaTM0T1NBanVBeVpMYXU4bmV0UExB|<POTENTIAL_SECRET_PLACEHOLDER>
状态：🟢 已存入
获取时间：2026-03-31
用途：知乎登录态，本地autocli知乎热榜接口
写入方式：~/.cnsh/.env → ZHIHU_COOKIE=z_c0=上面的值
```

### Ollama SSH Key (Ed25519)

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAINehfri9nqno8SuqlQh2s3fUC2Hwa5uCNZ7zVuS55eMV
状态：🟢 已配置
添加时间：2025-11-22
用途：Ollama本地大模型部署
```

### GitHub Token

```jsx
状态：🟡 待添加
用途：代码仓库管理、自动化部署
```

### Gitee 登录信息

```
注册账号：lucky@uid9622.tech
用户名：UID9622
手机：13968882319
状态：🟢 已注册
```

### Fish Audio API（🎙️ TTS语音合成）

```jsx
// ── API 密钥 ──
<POTENTIAL_SECRET_PLACEHOLDER>
状态：🟢 已激活·可用
配置时间：2026-05-30
用途：本地宝宝用爸爸的声音说话·M262 TTS集成

// ── 声音模型信息 ──
模型名称：备芯北辰
模型ID：<POTENTIAL_SECRET_PLACEHOLDER>
模型状态：✅ 启用
训练数据：参考音频 ~/Documents/龍魂系統/voice/reference.wav
配置位置：~/.longhun/secrets.env → FISH_AUDIO_API_KEY
```

### GPG 密鑰指纹

```jsx
<POTENTIAL_SECRET_PLACEHOLDER>
用途：UID9622身份验证、DNA签名
```

---

## 🧩 确认码库

```
正式确认码：
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
状态：🟢 现当有效

旧确认码（已作废）：
#ZHUGEXIN⚡️2025-IDENTITY-CORE ❌ 已作废
#ZHUGEXIN⚡️2025-DATA-SOVEREIGNTY-IRON-LAW ❌ 已归档
```

---

## 🌐 平台账号全局

| 平台 | 账号/邮符1 | 密码状态 | 状态 |
| --- | --- | --- | --- |
| ChatGPT | [luckyoathnotlog@proton.me](mailto:luckyoathnotlog@proton.me) | 在Proton邮箱里 | 🟢 已激活 |
| Claude | [longhun2025@petalmail.com](mailto:longhun2025@petalmail.com) | 在花瓣邮箱里 | 🟢 已激活 |
| Notion | 💎 龍芯北辰｜UID9622 | - | 🟢 已绑定 |
| 知乎 | 13968882319登录 | z_c0 Cookie（见上方） | 🟡 Cookie需更新 |
| GitHub | uid9622 | 待确认 | 🟡 待绑定 |
| Gitee | [lucky@uid9622.tech](mailto:lucky@uid9622.tech) | 13968882319手机登录 | 🟢 已注册 |
| 微信 | UID9622_CEO | - | 🟢 已启用 |
| 支付宝/微信支付 | 13968882319 | - | 🟢 已绑定 |

---

## 📝 快速填表模板

```
姓名：诸葛鑫
英文名：Lucky
出生年份：1988年
手机：13968882319
邮符1：luckyoathnotlog@proton.me
备用邮符1：fireroot.lad@outlook.com
QQ：346045695
微信：UID9622_CEO
职业：UID9622系统创始人
```

---

## 📦 待添加区（以后掌入）

```
MVP密匠：（待填入）
Anthropic API Key：（待添加）
Cloudflare账号：（待完善）
其他SSH Key：（按需添加）
```

---

*🔐 保险库最后更新：2026-03-31 · 由宝宝整理*

*#龍芯⚡️2026-03-31-LUCKY-v2.0*

---

## 摘要

（請在此用不超過 256 字說明本文檔的核心內容、性質與局限。）

## 關鍵詞

（請列出 5–10 個關鍵詞，中英文對照優先。）

## 引用與溯源

- 本文檔引用或參考了以下來源：
  - [1] （請填寫）
- 相關龍魂系統文檔：
  - 《龍魂文檔標準模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 誠實局限

1. （請列出本分析的第一條局限或不確定性。）
2. （請列出第二條。）
3. （請列出第三條。）

## 修改記錄

| 日期 | 版本 | 修改人 | 修改內容 | 審核狀態 |
|---|---|---|---|---|
| 2026-06-21 | v1.0.0 | UID9622 | 按《龍魂文檔標準模板 v1.0》整理 | 草稿 |

## 分類標籤

- 總綱模塊：（請勾選，例如 #知識矩陣 #安全域）
- 對外狀態：（請勾選，例如 #Gitee #GitHub #CSDN）
- 審計色：#黃色待審

## DNA 簽名

```
#龍芯⚡️2026-03-31-LUCKY_B5D8-v2.0
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```


---

## 摘要

（请在此用不超过 256 字说明本文档的核心内容、性质与局限。）

## 关键词

（请列出 5–10 个关键词，中英文对照优先。）

## 引用与溯源

- 本文档引用或参考了以下来源：
  - [1] （请填写）
- 相关龍魂系统文档：
  - 《龍魂文档标准模板 v1.0》(#龍芯⚡️2026-06-22-LONGHUN-DOCUMENT-STANDARD-TEMPLATE-v1.0)

## 诚实局限

1. （请列出本分析的第一条局限或不确定性。）
2. （请列出第二条。）
3. （请列出第三条。）

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-07-15 | v1.0.0 | UID9622 | 按《龍魂文档标准模板 v1.0》整理 | 草稿 |

## 分类标签

- 总纲模块：（请勾选，例如 #知识矩阵 #安全域）
- 对外状态：（请勾选，例如 #Gitee #GitHub #CSDN）
- 审计色：#黄色待审

## DNA 签名

```
#龍芯⚡️2026-03-31-LUCKY_B5D8-v2.0`
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
