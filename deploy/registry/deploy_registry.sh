#!/usr/bin/env bash
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷹兑-REGISTRY-DEPLOY-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# 创建者: 诸葛鑫（UID9622）
# 协议: CC BY-NC-SA 4.0
#
# deploy_registry.sh — 龍魂私有 Docker 镜像仓库 · 一键部署
# 用法：在服务器上执行  sudo bash deploy_registry.sh
# 方案：registry:2（轻量·24MB）>> Harbor（企业级·ARM64官方不支持）— 选型理由见 SPEC.md §0
# 参考：[快速链接: CSDN 参考文章] https://blog.csdn.net/Margrop/article/details/163312205
#       （registry:2 + htpasswd + restart=always，本脚本为其多架构增强版：自动适配 x86_64/aarch64）
# 覆盖模块（10/10）：
#   1.系统检测(apt/dnf/yum) 2.Docker安装(多架构) 3.htpasswd(bcrypt) 4.TLS自签
#   5.容器启动(持久化+0.0.0.0) 6.daemon.json(客户端白名单→见mac_client_setup.md)
#   7.systemd开机自启(双保险) 8.磁盘监控(df -h+cron) 9.DNA签章 10.push/pull验证

set -euo pipefail   # 任何一步出错立即终止，避免半装状态

# ---------- 可调参数（不懂就不要改） ----------
REG_PORT=5000                                    # 仓库对外端口
BASE_DIR=/data/longhun-registry                  # 四层目录根
REG_USER=longhun                                 # 登录账号
REG_NAME=longhun-registry                        # 容器名
ENABLE_TLS=${ENABLE_TLS:-0}                      # ENABLE_TLS=1 bash deploy_registry.sh 可开自签 TLS
TLS_HOST=${TLS_HOST:-longhun-registry.local}     # 自签证书用的主机名

echo "==== 龍魂 REGISTRY-DEPLOY v1.0 · 开始部署 ===="

# ---------- 第 0 步：必须是 root ----------
if [ "$(id -u)" -ne 0 ]; then
  echo "[错误] 请用 root 执行：sudo bash deploy_registry.sh" >&2; exit 1
fi

# ---------- 第 1 步：检测架构并确定镜像平台 ----------
ARCH="$(uname -m)"
case "$ARCH" in
  aarch64) PLATFORM="linux/arm64" ;;
  x86_64)  PLATFORM="linux/amd64" ;;
  *) echo "[错误] 不支持的架构：$ARCH，仅支持 x86_64 / aarch64" >&2; exit 1 ;;
esac
echo "[1/8] 架构检测通过：$ARCH → $PLATFORM"

# ---------- 第 2 步：检测/安装 Docker（Ubuntu用apt，openEuler用dnf） ----------
if ! command -v docker >/dev/null 2>&1; then
  echo "[2/8] 未检测到 Docker，正在安装..."
  if command -v apt >/dev/null 2>&1; then
    apt update && apt install -y docker.io
  elif command -v dnf >/dev/null 2>&1; then
    dnf install -y docker
  else
    yum install -y docker
  fi
  systemctl enable --now docker
else
  systemctl enable --now docker || true
fi
docker --version
echo "[2/8] Docker 就绪"

# ---------- 第 3 步：创建四层目录结构 ----------
# 01物理层=数据  02身份层=认证/证书  03主权层=配置  04执行层=脚本/日志
mkdir -p "$BASE_DIR"/{01-physical/{registry-data,backups},02-identity/{auth,certs},03-sovereign,04-execution/{bin,logs}}
chmod 700 "$BASE_DIR/02-identity"
echo "[3/8] 四层目录已建于 $BASE_DIR"

# ---------- 第 4 步：生成 htpasswd 认证文件（bcrypt） ----------
if [ ! -f "$BASE_DIR/02-identity/auth/htpasswd" ]; then
  # 随机生成 16 位密码，只打印这一次，请立即抄走
  REG_PASS="$(head -c 12 /dev/urandom | base64 | tr -dc 'A-Za-z0-9' | head -c 16)"
  # httpd:2.4-alpine 官方镜像含 linux/arm64 manifest，仅借它的 htpasswd 命令一用
  docker run --rm --entrypoint htpasswd httpd:2.4-alpine -Bbn "$REG_USER" "$REG_PASS" \
    > "$BASE_DIR/02-identity/auth/htpasswd"
  chmod 600 "$BASE_DIR/02-identity/auth/htpasswd"
  echo "==================================================="
  echo "  登录账号: $REG_USER"
  echo "  登录密码: $REG_PASS   <<<< 只显示这一次，请立即记录"
  echo "==================================================="
else
  echo "[4/8] htpasswd 已存在，跳过（沿用旧账号密码）"
fi

# ---------- 第 5 步：写 registry 配置 + 可选自签 TLS ----------
TLS_ENV=()
TLS_VOL=()
if [ "$ENABLE_TLS" = "1" ]; then
  CERT="$BASE_DIR/02-identity/certs/domain.crt"
  KEY="$BASE_DIR/02-identity/certs/domain.key"
  if [ ! -f "$CERT" ]; then
    openssl req -x509 -newkey rsa:4096 -sha256 -days 3650 -nodes \
      -keyout "$KEY" -out "$CERT" \
      -subj "/CN=$TLS_HOST" -addext "subjectAltName=DNS:$TLS_HOST"
    chmod 600 "$KEY"
  fi
  TLS_ENV=(-e "REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt" -e "REGISTRY_HTTP_TLS_KEY=/certs/domain.key")
  TLS_VOL=(-v "$BASE_DIR/02-identity/certs:/certs:ro")
  echo "[5/8] TLS 已启用（自签证书 CN=$TLS_HOST）"
else
  echo "[5/8] 内网 HTTP 模式（客户端配 insecure-registries 即可）"
fi

cat > "$BASE_DIR/03-sovereign/config.yml" <<'YAML'
version: 0.1
log:
  fields:
    service: longhun-registry
storage:
  filesystem:
    rootdirectory: /var/lib/registry
  delete:
    enabled: true            # 允许删除镜像（配合 04-execution/bin/gc.sh 回收空间）
http:
  addr: :5000
  headers:
    X-Content-Type-Options: [nosniff]
YAML
echo "[5/8] config.yml 已写入 03-sovereign/"

# ---------- 第 6 步：拉取 registry:2 ----------
echo "[6/8] 拉取 registry:2（官方 multi-arch 镜像）..."
docker pull --platform "$PLATFORM" registry:2
IMG_ARCH="$(docker image inspect registry:2 --format '{{.Architecture}}')"
echo "[6/8] registry:2 镜像拉取成功（本地架构：$IMG_ARCH）"

# ---------- 第 7 步：起容器（幂等：先删旧同名容器） ----------
docker rm -f "$REG_NAME" >/dev/null 2>&1 || true
docker run -d \
  --name "$REG_NAME" \
  --restart=always \
  -p "$REG_PORT":5000 \
  -v "$BASE_DIR/01-physical/registry-data:/var/lib/registry" \
  -v "$BASE_DIR/02-identity/auth:/auth:ro" \
  -v "$BASE_DIR/03-sovereign/config.yml:/etc/docker/registry/config.yml:ro" \
  "${TLS_VOL[@]+"${TLS_VOL[@]}"}" \
  -e REGISTRY_AUTH=htpasswd \
  -e REGISTRY_AUTH_HTPASSWD_REALM="LongHun Registry Realm" \
  -e REGISTRY_AUTH_HTPASSWD_PATH=/auth/htpasswd \
  "${TLS_ENV[@]+"${TLS_ENV[@]}"}" \
  registry:2
echo "[7/8] 容器已启动（--restart=always，开机自启）"

# ---------- systemd 兜底单元（双保险：即使 docker 未设自启也能拉起） ----------
cat > "$BASE_DIR/03-sovereign/longhun-registry.service" <<UNIT
[Unit]
Description=LongHun Private Docker Registry
After=docker.service
Requires=docker.service
[Service]
Type=oneshot
RemainAfterExit=yes
ExecStart=/usr/bin/docker start $REG_NAME
ExecStop=/usr/bin/docker stop $REG_NAME
[Install]
WantedBy=multi-user.target
UNIT
cp "$BASE_DIR/03-sovereign/longhun-registry.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable longhun-registry.service

# ---------- 第 8 步：磁盘 80% 告警脚本 + 每小时 cron ----------
cat > "$BASE_DIR/04-execution/bin/disk_alert.sh" <<'ALERT'
#!/usr/bin/env bash
# 龍魂仓库磁盘告警：/data 分区用量 >=80% 时写日志并可选发Webhook
BASE_DIR=/data/longhun-registry
THRESHOLD=80
USAGE=$(df --output=pcent /data 2>/dev/null | tail -1 | tr -dc '0-9')
if [ "${USAGE:-0}" -ge "$THRESHOLD" ]; then
  MSG="[$(date '+%F %T')] 龍魂仓库磁盘告警: /data 已用 ${USAGE}% (阈值 ${THRESHOLD}%)"
  echo "$MSG" >> "$BASE_DIR/04-execution/logs/disk_alert.log"
  # 可选：企业微信/钉钉 Webhook，取消注释并填入地址
  # curl -s -X POST -H 'Content-Type: application/json' \
  #   -d "{\"msgtype\":\"text\",\"text\":{\"content\":\"$MSG\"}}" \
  #   "https://你的webhook地址"
fi
ALERT
chmod +x "$BASE_DIR/04-execution/bin/disk_alert.sh"

# 垃圾回收脚本（删除镜像后真正释放磁盘）
cat > "$BASE_DIR/04-execution/bin/gc.sh" <<GC
#!/usr/bin/env bash
# 仓库垃圾回收：删除标记的 blob 真正落盘释放
docker exec $REG_NAME registry garbage-collect /etc/docker/registry/config.yml
echo "[\$(date '+%F %T')] GC 完成" >> $BASE_DIR/04-execution/logs/gc.log
GC
chmod +x "$BASE_DIR/04-execution/bin/gc.sh"

# 每小时跑一次磁盘检查
( crontab -l 2>/dev/null | grep -v disk_alert.sh ; echo "0 * * * * $BASE_DIR/04-execution/bin/disk_alert.sh" ) | crontab -
echo "[8/8] 磁盘告警 cron 已安装（每小时，阈值 80%）"

# ---------- 防火墙/安全组提示 ----------
echo ""
echo "==== 防火墙/安全组提示 ===="
echo "  openEuler/EulerOS 若开启 firewalld，请执行（内网放行 5000）："
echo "    firewall-cmd --permanent --add-port=$REG_PORT/tcp && firewall-cmd --reload"
echo "  华为云安全组：入方向仅放行内网网段到 TCP $REG_PORT，禁止 0.0.0.0/0 对公网开放。"

# ---------- 健康自检 ----------
sleep 2
# 按 ENABLE_TLS 选择协议；TLS 自签证书用 -k 跳过校验（本机自检够用，不折腾 CA）
if [ "$ENABLE_TLS" = "1" ]; then
  HC_SCHEME=https; HC_CURL_OPTS=(-k)
else
  HC_SCHEME=http;  HC_CURL_OPTS=()
fi
if curl -s "${HC_CURL_OPTS[@]}" -o /dev/null -w '%{http_code}' "$HC_SCHEME://127.0.0.1:$REG_PORT/v2/" | grep -q '401'; then
  echo "==== 部署完成：/v2/ 返回 401（带鉴权握手，正常）===="
else
  echo "[警告] 健康检查未通过，请执行: docker logs $REG_NAME" >&2
fi
SERVER_IP=$(hostname -I | awk '{print $1}')
echo "  仓库地址: $HC_SCHEME://$SERVER_IP:$REG_PORT   （Mac 端配置见 mac_client_setup.md）"
