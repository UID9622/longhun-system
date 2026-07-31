# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env bash
# 龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-SETUP-WECHAT-PAY-v1.0
# 功能: 龍魂激活经济舱 · 微信支付凭证配置向导
# 用法: bash bin/setup_wechat_pay.sh

set -e

CNSH_HOME="${CNSH_HOME:-$HOME/.longhun}"
CONFIG_DIR="$CNSH_HOME/config"
CERT_DIR="$CNSH_HOME/certs"
CONFIG_FILE="$CONFIG_DIR/payment_credentials.yaml"

echo "=========================================="
echo "  🐉 龍魂激活经济舱 · 微信支付配置向导"
echo "=========================================="
echo ""
echo "微信支付无官方沙箱，需使用真实商户号。"
echo "请提前准备："
echo "  1. 微信支付 AppID"
echo "  2. 商户号 mch_id"
echo "  3. API v3 密钥"
echo "  4. 证书序列号"
echo "  5. 商户 API 私钥文件（apiclient_key.pem）"
echo ""
read -p "按回车继续…"

mkdir -p "$CONFIG_DIR" "$CERT_DIR"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "创建配置文件: $CONFIG_FILE"
  cp config/payment_credentials.yaml.example "$CONFIG_FILE"
fi

echo ""
echo "请依次输入微信支付参数："
read -p "AppID: " appid
read -p "商户号 mch_id: " mch_id
read -p "API v3 密钥: " api_v3_key
read -p "证书序列号 cert_serial_no: " cert_serial_no
read -p "私钥文件本地路径（如 ./wechat_apiclient_key.pem）: " local_key

if [ ! -f "$local_key" ]; then
  echo "❌ 私钥文件不存在: $local_key"
  exit 1
fi

cp "$local_key" "$CERT_DIR/wechat_apiclient_key.pem"
chmod 600 "$CERT_DIR/wechat_apiclient_key.pem"

cat > "$CONFIG_FILE" <<EOF
alipay:
  enabled: true
  sandbox: true
  app_id: "9021000156674159"
  app_private_key_path: "/opt/longhun-activation/certs/alipay_sandbox_app_private_key.pem"
  alipay_public_key_path: "/opt/longhun-activation/certs/alipay_sandbox_alipay_public_key.pem"
  notify_url: "https://uid9622.cn/api/activation/payment/notify/alipay"
  return_url: "https://uid9622.cn/activation-lab/?paid=1"

wechat_pay:
  enabled: true
  appid: "$appid"
  mch_id: "$mch_id"
  api_v3_key: "$api_v3_key"
  cert_serial_no: "$cert_serial_no"
  private_key_path: "/opt/longhun-activation/certs/wechat_apiclient_key.pem"
  notify_url: "https://uid9622.cn/api/activation/payment/notify/wechat"
EOF

echo ""
echo "✅ 微信支付配置已写入: $CONFIG_FILE"
echo "✅ 私钥已复制到: $CERT_DIR/wechat_apiclient_key.pem"
echo ""
echo "下一步："
echo "  1. 将 $CONFIG_FILE 上传到服务器 /opt/longhun-activation/config/"
echo "  2. 将 $CERT_DIR/wechat_apiclient_key.pem 上传到服务器 /opt/longhun-activation/certs/"
echo "  3. 重启服务: systemctl restart longhun-activation"
echo ""
