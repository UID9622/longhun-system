#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/bin/bash
# =============================================================================
# DNA 标识: DRAGON-SOUL-SAFE-CLEANUP-v1.2.0
# 作者: 龍魂系统运维团队
# 创建时间: 2024-01-15
# 最后修改: 2024-01-15
# 审计修复: M5 - 文件清理不一致, L2 - 临时目录安全
# =============================================================================
#
# 安全文件清理脚本
#
# 功能:
#   - 接受文件列表作为参数进行安全删除
#   - 每个文件删除前检查是否存在
#   - 删除后使用 ls -la 验证已删除
#   - 返回明确的 SUCCESS/FAIL 状态
#   - 支持 --verify 模式: 仅检查不删除
#   - 支持 --dry-run 模式: 显示将要删除的文件
#
# 用法:
#   ./safe_cleanup.sh /tmp/file1.tmp /tmp/file2.tmp
#   ./safe_cleanup.sh --dry-run /tmp/*.tmp
#   ./safe_cleanup.sh --verify /tmp/file1.tmp
#   ./safe_cleanup.sh --help
#
# =============================================================================

# 严格错误处理
set -euo pipefail

# ---------------------------------------------------------------------------
# 常量定义
# ---------------------------------------------------------------------------
readonly SCRIPT_NAME="$(basename "$0")"
readonly SCRIPT_VERSION="1.2.0"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="${SCRIPT_DIR}/.cleanup.log"

# 返回状态码
readonly STATUS_SUCCESS=0
readonly STATUS_PARTIAL=1
readonly STATUS_FAILURE=2
readonly STATUS_INVALID_ARGS=3
readonly STATUS_NOT_FOUND=4

# ---------------------------------------------------------------------------
# 用户专属临时目录（修复 L2）
# ---------------------------------------------------------------------------
ensure_user_temp_dir() {
    local user_tmp_dir
    user_tmp_dir="${TMPDIR:-/tmp}/dragon_soul_$(id -u -n)_$$"
    if [[ ! -d "$user_tmp_dir" ]]; then
        mkdir -p "$user_tmp_dir"
        chmod 700 "$user_tmp_dir"
    fi
    echo "$user_tmp_dir"
}

readonly USER_TEMP_DIR="$(ensure_user_temp_dir)"

# ---------------------------------------------------------------------------
# 日志函数
# ---------------------------------------------------------------------------
log() {
    local level="$1"
    shift
    local message
    message="$(date '+%Y-%m-%d %H:%M:%S %Z') [${level}] $*"
    echo "$message" | tee -a "$LOG_FILE" 2>/dev/null || echo "$message"
}

log_info()  { log "INFO"  "$@"; }
log_warn()  { log "WARN"  "$@"; }
log_error() { log "ERROR" "$@"; }
log_debug() { log "DEBUG" "$@"; }

# ---------------------------------------------------------------------------
# 用法帮助
# ---------------------------------------------------------------------------
show_usage() {
    cat << EOF
===============================================================================
安全文件清理脚本 v${SCRIPT_VERSION} | DNA: DRAGON-SOUL-SAFE-CLEANUP
===============================================================================

用法:
    ${SCRIPT_NAME} [选项] <文件1> [文件2] ... [文件N]

选项:
    --verify       仅验证文件是否存在，不执行删除
    --dry-run      显示将要删除的文件列表（不实际删除）
    --temp-dir     显示当前用户专属临时目录路径
    --version      显示版本信息
    --help         显示此帮助信息

返回码:
    ${STATUS_SUCCESS}  = 全部成功
    ${STATUS_PARTIAL}  = 部分成功
    ${STATUS_FAILURE}  = 全部失败
    ${STATUS_INVALID_ARGS} = 参数无效
    ${STATUS_NOT_FOUND}= 文件不存在

示例:
    # 删除指定文件
    ${SCRIPT_NAME} /tmp/file1.tmp /tmp/file2.tmp

    # 仅检查文件是否存在
    ${SCRIPT_NAME} --verify /tmp/file1.tmp

    # 预览将要删除的文件
    ${SCRIPT_NAME} --dry-run /tmp/*.tmp

    # 显示临时目录
    ${SCRIPT_NAME} --temp-dir

===============================================================================
EOF
}

# ---------------------------------------------------------------------------
# 版本信息
# ---------------------------------------------------------------------------
show_version() {
    echo "${SCRIPT_NAME} version ${SCRIPT_VERSION}"
    echo "DNA: DRAGON-SOUL-SAFE-CLEANUP-v${SCRIPT_VERSION}"
    echo "User temp directory: ${USER_TEMP_DIR}"
}

# ---------------------------------------------------------------------------
# 检查文件是否存在且可删除
# ---------------------------------------------------------------------------
check_file() {
    local filepath="$1"

    if [[ -z "$filepath" ]]; then
        log_error "文件路径为空"
        return "$STATUS_INVALID_ARGS"
    fi

    if [[ ! -e "$filepath" ]]; then
        log_warn "文件不存在: ${filepath}"
        return "$STATUS_NOT_FOUND"
    fi

    if [[ -d "$filepath" ]]; then
        log_warn "路径为目录，跳过: ${filepath}"
        return "$STATUS_INVALID_ARGS"
    fi

    if [[ ! -w "$filepath" ]]; then
        log_warn "文件无写权限: ${filepath}"
        return "$STATUS_FAILURE"
    fi

    return "$STATUS_SUCCESS"
}

# ---------------------------------------------------------------------------
# 验证文件已删除
# ---------------------------------------------------------------------------
verify_deleted() {
    local filepath="$1"
    local dir
    dir="$(dirname "$filepath")"
    local filename
    filename="$(basename "$filepath")"

    # 使用 ls -la 验证文件已删除
    if ls -la "$dir" 2>/dev/null | grep -q "^.*${filename}$"; then
        return "$STATUS_FAILURE"
    else
        return "$STATUS_SUCCESS"
    fi
}

# ---------------------------------------------------------------------------
# 安全删除单个文件
# ---------------------------------------------------------------------------
safe_remove_file() {
    local filepath="$1"
    local mode="${2:-normal}"  # normal, dry-run, verify

    # 规范化路径
    filepath="$(cd "$(dirname "$filepath")" && pwd)/$(basename "$filepath")" 2>/dev/null || true

    log_info "处理: ${filepath} [模式: ${mode}]"

    # 1. 检查文件
    check_file "$filepath"
    local check_result=$?

    if [[ $check_result -ne 0 ]]; then
        return $check_result
    fi

    case "$mode" in
        verify)
            # --verify 模式: 仅检查，不删除
            log_info "VERIFY PASS: ${filepath} 存在且可删除"
            return "$STATUS_SUCCESS"
            ;;

        dry-run)
            # --dry-run 模式: 显示将要删除的文件
            local filesize
            filesize="$(stat -c%s "$filepath" 2>/dev/null || stat -f%z "$filepath" 2>/dev/null || echo "unknown")"
            log_info "DRY-RUN: 将要删除 ${filepath} (大小: ${filesize} 字节)"
            return "$STATUS_SUCCESS"
            ;;

        normal)
            # 正常删除模式
            log_info "正在删除: ${filepath}"

            if rm -f "$filepath"; then
                # 验证已删除
                if verify_deleted "$filepath"; then
                    log_info "SUCCESS: ${filepath} 已删除并验证"
                    return "$STATUS_SUCCESS"
                else
                    log_error "FAIL: ${filepath} 删除后验证失败"
                    return "$STATUS_FAILURE"
                fi
            else
                log_error "FAIL: ${filepath} 删除操作失败"
                return "$STATUS_FAILURE"
            fi
            ;;

        *)
            log_error "未知模式: ${mode}"
            return "$STATUS_INVALID_ARGS"
            ;;
    esac
}

# ---------------------------------------------------------------------------
# 清理用户临时目录中的过期文件
# ---------------------------------------------------------------------------
cleanup_temp_dir() {
    local max_age_hours="${1:-24}"
    local cleaned=0
    local failed=0

    log_info "清理临时目录: ${USER_TEMP_DIR} (超过 ${max_age_hours} 小时的文件)"

    if [[ ! -d "$USER_TEMP_DIR" ]]; then
        log_info "临时目录不存在，无需清理"
        return "$STATUS_SUCCESS"
    fi

    while IFS= read -r -d '' file; do
        if rm -f "$file" 2>/dev/null; then
            ((cleaned++)) || true
        else
            ((failed++)) || true
        fi
    done < <(find "$USER_TEMP_DIR" -type f -mmin +$((max_age_hours * 60)) -print0 2>/dev/null)

    log_info "临时目录清理完成: ${cleaned} 成功, ${failed} 失败"
    return "$STATUS_SUCCESS"
}

# =============================================================================
# 主函数
# =============================================================================
main() {
    local mode="normal"
    local files=()
    local total=0
    local success=0
    local failed=0
    local notfound=0

    # 解析参数
    if [[ $# -eq 0 ]]; then
        show_usage
        exit "$STATUS_INVALID_ARGS"
    fi

    while [[ $# -gt 0 ]]; do
        case "$1" in
            --help|-h)
                show_usage
                exit "$STATUS_SUCCESS"
                ;;
            --version|-v)
                show_version
                exit "$STATUS_SUCCESS"
                ;;
            --verify)
                mode="verify"
                shift
                ;;
            --dry-run)
                mode="dry-run"
                shift
                ;;
            --temp-dir)
                echo "${USER_TEMP_DIR}"
                exit "$STATUS_SUCCESS"
                ;;
            --cleanup-temp)
                local hours="${2:-24}"
                cleanup_temp_dir "$hours"
                shift 2
                ;;
            --)
                shift
                files+=("$@")
                break
                ;;
            -*)
                log_error "未知选项: $1"
                show_usage
                exit "$STATUS_INVALID_ARGS"
                ;;
            *)
                files+=("$1")
                shift
                ;;
        esac
    done

    # 检查是否有文件参数
    if [[ ${#files[@]} -eq 0 ]]; then
        log_error "未提供文件参数"
        show_usage
        exit "$STATUS_INVALID_ARGS"
    fi

    # 记录开始
    log_info "=========================================="
    log_info "安全清理脚本启动"
    log_info "DNA: DRAGON-SOUL-SAFE-CLEANUP-v${SCRIPT_VERSION}"
    log_info "模式: ${mode}"
    log_info "文件数量: ${#files[@]}"
    log_info "=========================================="

    # 处理每个文件
    for filepath in "${files[@]}"; do
        # 处理通配符展开后的空值
        if [[ -z "$filepath" ]]; then
            continue
        fi

        ((total++)) || true

        safe_remove_file "$filepath" "$mode"
        local rc=$?

        case $rc in
            "$STATUS_SUCCESS")
                ((success++)) || true
                ;;
            "$STATUS_NOT_FOUND")
                ((notfound++)) || true
                ;;
            *)
                ((failed++)) || true
                ;;
        esac
    done

    # 汇总报告
    log_info "=========================================="
    log_info "清理任务完成"
    log_info "总计: ${total}"
    log_info "成功: ${success}"
    log_info "失败: ${failed}"
    log_info "不存在: ${notfound}"
    log_info "=========================================="

    # 返回总体状态
    if [[ $failed -gt 0 && $success -gt 0 ]]; then
        echo "STATUS: PARTIAL"
        exit "$STATUS_PARTIAL"
    elif [[ $failed -gt 0 ]]; then
        echo "STATUS: FAIL"
        exit "$STATUS_FAILURE"
    elif [[ $success -gt 0 ]]; then
        echo "STATUS: SUCCESS"
        exit "$STATUS_SUCCESS"
    else
        echo "STATUS: NOTHING_TO_DO"
        exit "$STATUS_SUCCESS"
    fi
}

# =============================================================================
# 脚本入口
# =============================================================================
main "$@"
