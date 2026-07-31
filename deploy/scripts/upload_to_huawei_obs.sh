# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env bash
# ╔══════════════════════════════════════════════════════════════╗
# ║  龍魂·华为云 OBS 上传脚本 v1.0                                ║
# ║  DNA: #龍芯⚡️丙午·乙未·丁酉·亥时·☰乾-HUAWEI-OBS-UPLOAD-v1.0 ║
# ╚══════════════════════════════════════════════════════════════╝
set -e

RELEASE_DIR="/opt/longhun-system/releases"
DATE_TAG="$(date +%Y-%m-%d)"

# ═══ 用户需填写 ═══
# 方式一：环境变量传入
#   export HUAWEI_AK=你的AccessKey
#   export HUAWEI_SK=你的SecretKey
#   export OBS_BUCKET=你的Bucket名
#   export OBS_ENDPOINT=obs.cn-southwest-2.myhuaweicloud.com  # 按实际区域修改
#   bash upload_to_huawei_obs.sh
#
# 方式二：直接修改下面变量（不推荐，会留在磁盘）
HUAWEI_AK="${HUAWEI_AK:-}"
HUAWEI_SK="${HUAWEI_SK:-}"
OBS_BUCKET="${OBS_BUCKET:-}"
OBS_ENDPOINT="${OBS_ENDPOINT:-obs.cn-southwest-2.myhuaweicloud.com}"
OBS_PREFIX="${OBS_PREFIX:-longhun-system/releases}"

# ═══ 校验 ═══
if [[ -z "$HUAWEI_AK" || -z "$HUAWEI_SK" || -z "$OBS_BUCKET" ]]; then
    echo "[ERROR] 请先设置 HUAWEI_AK / HUAWEI_SK / OBS_BUCKET 环境变量"
    echo "示例:"
    echo "  export HUAWEI_AK=AKxxxxxxxxxxxx"
    echo "  export HUAWEI_SK=SKxxxxxxxxxxxx"
    echo "  export OBS_BUCKET=longhun-bucket"
    echo "  export OBS_ENDPOINT=obs.cn-southwest-2.myhuaweicloud.com"
    exit 1
fi

# ═══ 依赖检查 ═══
if ! command -v obsutil >/dev/null 2>&1; then
    echo "[INFO] obsutil 未安装，尝试下载..."
    OBSUTIL_URL="https://obs-community.obs.cn-north-1.myhuaweicloud.com/obsutil/current/obsutil_linux_amd64.tar.gz"
    TMP_DIR="/tmp/obsutil_install_$$"
    mkdir -p "$TMP_DIR"
    cd "$TMP_DIR"
    wget -q "$OBSUTIL_URL" -O obsutil.tar.gz
    tar -xzf obsutil.tar.gz
    OBSUTIL_BIN=$(find . -name 'obsutil' -type f | head -1)
    chmod +x "$OBSUTIL_BIN"
    mv "$OBSUTIL_BIN" /usr/local/bin/obsutil
    cd -
    rm -rf "$TMP_DIR"
    echo "[INFO] obsutil 已安装到 /usr/local/bin/obsutil"
fi

# ═══ 配置 obsutil ═══
obsutil config -i "$HUAWEI_AK" -k "$HUAWEI_SK" -e "$OBS_ENDPOINT" >/dev/null 2>&1

# ═══ 上传 ═══
echo "[INFO] 开始上传 release 包到 OBS..."
echo "[INFO] 源目录: $RELEASE_DIR"
echo "[INFO] 目标: s3://$OBS_BUCKET/$OBS_PREFIX/"

for file in "$RELEASE_DIR"/*.tar.gz; do
    if [[ -f "$file" ]]; then
        filename=$(basename "$file")
        echo "[UPLOAD] $filename -> obs://$OBS_BUCKET/$OBS_PREFIX/$filename"
        obsutil cp "$file" "obs://$OBS_BUCKET/$OBS_PREFIX/$filename" -f -acl=public-read

        # 同时上传 sha256 校验文件
        shafile="$file.sha256"
        if [[ -f "$shafile" ]]; then
            obsutil cp "$shafile" "obs://$OBS_BUCKET/$OBS_PREFIX/$filename.sha256" -f -acl=public-read
        fi
    fi
done

echo ""
echo "[INFO] 上传完成。公开下载链接格式:"
echo "  https://$OBS_BUCKET.$OBS_ENDPOINT/$OBS_PREFIX/longhun-system-code-$DATE_TAG.tar.gz"
echo ""
echo "[INFO] 你也可以在华为云 OBS 控制台查看: https://console.huaweicloud.com/obs/"
