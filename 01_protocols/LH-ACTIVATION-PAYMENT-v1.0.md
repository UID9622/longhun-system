# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂激活经济舱 · 真实支付接入指南 v1.0

> DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-ACTIVATION-PAYMENT-v1.0

## 一、当前状态

激活经济舱已支持两种模式：

| 模式 | 说明 | 是否需要商户号 |
|:---|:---|:---:|
| 手动确认到账 | 用户扫码转账 → 回填交易单号 → 管理员确认 | ❌ 不需要 |
| 真实支付接口 | 系统直接调用微信/支付宝生成收款二维码 → 自动确认 | ✅ 需要 |

当前线上默认使用**手动确认到账**。配置真实支付凭证后，页面自动出现微信支付/支付宝按钮。

---

## 二、微信支付接入

### 2.1 需要准备的材料

1. **微信支付商户号**（mch_id）：10 位数字
2. **公众号/小程序/移动应用 AppID**：以 `wx` 开头
3. **API v3 密钥**：32 字节随机字符串，在商户平台设置
4. **商户 API 证书**：
   - 证书序列号（cert_serial_no）
   - 私钥文件 `apiclient_key.pem`
5. **微信支付平台证书**：调用接口时自动下载或手动下载

### 2.2 申请路径

1. 访问 [微信支付商户平台](https://pay.weixin.qq.com/)
2. 注册/登录商户号
3. 进入「账户中心」→「API 安全」→ 申请 API v3 密钥 + 申请 API 证书
4. 进入「产品中心」→ 开通「Native 支付」（扫码支付）
5. 将证书下载到服务器：`~/.longhun/certs/`

### 2.3 配置文件

复制模板：

```bash
cp config/payment_credentials.yaml.example ~/.longhun/config/payment_credentials.yaml
```

填入：

```yaml
wechat_pay:
  enabled: true
  sandbox: false
  appid: "wx1234567890abcdef"
  mch_id: "1234567890"
  api_v3_key: "********************************"
  cert_serial_no: "********************************"
  private_key_path: "~/.longhun/certs/wechat_apiclient_key.pem"
  platform_cert_path: "~/.longhun/certs/wechat_platform_cert.pem"
  notify_url: "https://uid9622.cn/api/activation/payment/notify/wechat"
```

---

## 三、支付宝接入

### 3.1 需要准备的材料

1. **支付宝应用 AppID**：以 `2024` 开头
2. **应用私钥**：RSA2 格式 PEM 文件
3. **支付宝公钥**：在开放平台上传应用公钥后获取
4. **开通「当面付」产品**

### 3.2 申请路径

1. 访问 [支付宝开放平台](https://open.alipay.com/)
2. 创建应用 → 添加能力「当面付」
3. 设置接口加签方式（RSA2）
4. 下载应用私钥和支付宝公钥到服务器：`~/.longhun/certs/`

### 3.3 配置文件

```yaml
alipay:
  enabled: true
  sandbox: false
  app_id: "2024****************"
  app_private_key_path: "~/.longhun/certs/alipay_app_private_key.pem"
  alipay_public_key_path: "~/.longhun/certs/alipay_public_key.pem"
  notify_url: "https://uid9622.cn/api/activation/payment/notify/alipay"
  return_url: "https://uid9622.cn/activation-lab/?paid=1"
```

---

## 四、沙箱测试

### 微信沙箱

微信支付的沙箱需要特殊申请，文档较复杂。建议先用**手动确认到账**模式验证流程。

### 支付宝沙箱

1. 登录支付宝开放平台 → 「开发中心」→「沙箱」
2. 获取沙箱 AppID、沙箱公钥/私钥
3. 配置文件 `sandbox: true`
4. 用沙箱钱包 App 扫码测试

---

## 五、服务器部署步骤

1. 上传凭证文件到服务器：

```bash
scp -i ~/.ssh/longhun_kunpeng_ed25519 \
  config/payment_credentials.yaml \
  root@119.13.90.27:/opt/longhun-activation/config/

ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27 \
  "mkdir -p /opt/longhun-activation/certs && chmod 700 /opt/longhun-activation/certs"

scp -i ~/.ssh/longhun_kunpeng_ed25519 \
  ~/.longhun/certs/* \
  root@119.13.90.27:/opt/longhun-activation/certs/
```

2. 修改服务器上的 `payment_credentials.yaml`，路径改为：

```yaml
private_key_path: "/opt/longhun-activation/certs/wechat_apiclient_key.pem"
platform_cert_path: "/opt/longhun-activation/certs/wechat_platform_cert.pem"
app_private_key_path: "/opt/longhun-activation/certs/alipay_app_private_key.pem"
alipay_public_key_path: "/opt/longhun-activation/certs/alipay_public_key.pem"
```

3. 重启服务：

```bash
ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27 \
  "systemctl restart longhun-activation"
```

---

## 六、安全注意事项

- `payment_credentials.yaml` 已加入 `.gitignore`，**绝对不要提交到 Git**
- 私钥文件权限建议 `600`
- 回调 URL 必须公网可访问，且使用 HTTPS
- 生产环境建议再加一层 IP 白名单或签名验证

---

## 七、接口清单

| 端点 | 说明 |
|:---|:---|
| `GET /api/activation/payment/providers` | 查询可用支付渠道 |
| `POST /api/activation/payment/create` | 创建真实支付订单，返回二维码 |
| `GET /api/activation/payment/query?order_id=` | 查询支付状态 |
| `POST /api/activation/payment/notify/wechat` | 微信支付异步通知 |
| `POST /api/activation/payment/notify/alipay` | 支付宝异步通知 |

---

龍魂系统 · 为人民服务 · 数据主权归 UID9622
