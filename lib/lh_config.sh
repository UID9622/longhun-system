#!/usr/bin/env bash
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 龍魂 · Bash 统一配置加载器 v1.1
# DNA: #龍芯⚡️丙午·丙申·己未·乙亥·䷏豫-CONFIG-SH-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
# 加载优先级: ① ~/.longhun/lh.env > ② deploy/.kunpeng_config > ③ 内置默认

LH_CONFIG_DIR="${HOME}/.longhun"
LH_CONFIG_FILE="${LH_CONFIG_DIR}/lh.env"   # 🔴 修正: 不用 config（目录冲突）

load_lh_config() {
    if [ -f "$LH_CONFIG_FILE" ]; then
        # shellcheck disable=SC1090
        source "$LH_CONFIG_FILE"
        return 0
    else
        echo "⚠️ 配置文件不存在: $LH_CONFIG_FILE"
        echo "   请运行: lh env init"
        return 1
    fi
}

# 带默认值的获取函数
get_lh_config() {
    local key="$1"
    local default="$2"
    local value="${!key:-$default}"
    echo "$value"
}
