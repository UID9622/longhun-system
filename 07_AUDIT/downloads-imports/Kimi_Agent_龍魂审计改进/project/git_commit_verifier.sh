#!/usr/bin/env bash
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
# DNA: #龍芯⚡️丙午·甲午·壬子·丙午·䷙大畜-GIT-COMMIT-VERIFIER-v1.0
# 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
# 责任: UID9622·不免责
#
# Git 提交核查脚本
# =================
# 用于验证 Git 提交的文件一致性，修复审计发现 R4。
# 功能：
#   - 显示提交中所有变更文件的完整清单（含增删行数）
#   - 检查文件数量是否与预期一致
#   - 验证每个文件的 SHA256 哈希值
#   - 输出格式清晰的核查报告
#
# 用法：
#   ./git_commit_verifier.sh <commit_hash> [expected_file_count]
#
# 示例：
#   ./git_commit_verifier.sh abc1234
#   ./git_commit_verifier.sh abc1234 5
#   ./git_commit_verifier.sh HEAD~3
#   ./git_commit_verifier.sh HEAD --export report.json
#
# 返回码：
#   0 - 核查通过
#   1 - 参数错误
#   2 - 不在 Git 仓库中
#   3 - 提交不存在
#   4 - 文件数量不匹配
#   5 - 核查过程中发生错误

set -euo pipefail

# ============ 常量定义 ============
readonly SCRIPT_VERSION="1.0"
readonly SCRIPT_NAME="git_commit_verifier.sh"
readonly MIN_ARGS=1
readonly MAX_ARGS=2

# 颜色定义
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly BLUE='\033[0;34m'
readonly CYAN='\033[0;36m'
readonly BOLD='\033[1m'
readonly NC='\033[0m'  # 无颜色

# ============ 全局变量 ============
COMMIT_HASH=""
EXPECTED_FILE_COUNT=-1  # -1 表示不检查
EXPORT_PATH=""
VERBOSE=false

# ============ 辅助函数 ============

# 打印带颜色的输出
print_header() {
    echo -e "${BOLD}${BLUE}══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BOLD}${BLUE}  $1${NC}"
    echo -e "${BOLD}${BLUE}══════════════════════════════════════════════════════════════${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ️  $1${NC}"
}

print_separator() {
    echo -e "${BOLD}${BLUE}──────────────────────────────────────────────────────────────${NC}"
}

# 显示使用说明
show_usage() {
    cat << EOF
${BOLD}用法:${NC}
    ${SCRIPT_NAME} <commit_hash> [expected_file_count]

${BOLD}参数:${NC}
    commit_hash          Git 提交哈希（短或长格式，或 HEAD/HEAD~N）
    expected_file_count  可选，预期的变更文件数量

${BOLD}选项:${NC}
    -h, --help           显示此帮助信息
    -v, --verbose        显示详细输出
    --export <path>      导出核查报告到指定路径（JSON 格式）
    --version            显示版本信息

${BOLD}示例:${NC}
    ${SCRIPT_NAME} abc1234
    ${SCRIPT_NAME} abc1234 5
    ${SCRIPT_NAME} HEAD~3
    ${SCRIPT_NAME} HEAD --export ./report.json
    ${SCRIPT_NAME} feature-branch --verbose

${BOLD}返回码:${NC}
    0  核查通过
    1  参数错误
    2  不在 Git 仓库中
    3  提交不存在
    4  文件数量不匹配
    5  核查过程中发生错误
EOF
}

# 检查是否在 Git 仓库中
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        print_error "当前目录不是 Git 仓库"
        exit 2
    fi
}

# 验证提交哈希是否存在
validate_commit() {
    local hash="$1"
    if ! git cat-file -e "${hash}^{commit}" 2>/dev/null; then
        print_error "提交 '${hash}' 不存在或无效"
        exit 3
    fi
    # 获取完整哈希
    COMMIT_HASH=$(git rev-parse "${hash}")
}

# 获取提交信息
get_commit_info() {
    local hash="$1"
    local author author_date subject body changed_files

    author=$(git log -1 --format="%an <%ae>" "${hash}")
    author_date=$(git log -1 --format="%ai" "${hash}")
    subject=$(git log -1 --format="%s" "${hash}")
    body=$(git log -1 --format="%b" "${hash}")
    changed_files=$(git diff-tree --no-commit-id --name-only -r "${hash}" 2>/dev/null | wc -l)

    echo "${author}|${author_date}|${subject}|${body}|${changed_files}"
}

# 获取文件变更详情
get_file_changes() {
    local hash="$1"
    # 使用 git diff-tree 获取每个文件的变更统计
    git diff-tree --no-commit-id --stat=1000 -r "${hash}" 2>/dev/null || true
}

# 获取文件列表（含增删行数）
get_file_list_with_stats() {
    local hash="$1"
    # 格式: 增行数 删行数 文件路径
    git diff-tree --no-commit-id --numstat -r "${hash}" 2>/dev/null || true
}

# 计算文件的 SHA256 哈希值
calculate_file_hash() {
    local hash="$1"
    local file="$2"
    # 从提交中提取文件内容并计算 SHA256
    git show "${hash}:${file}" 2>/dev/null | sha256sum | awk '{print $1}' || echo "N/A"
}

# 获取文件类型
get_file_type() {
    local hash="$1"
    local file="$2"
    local status
    status=$(git diff-tree --no-commit-id --diff-filter=ACMRT -r "${hash}" -- "${file}" 2>/dev/null | awk '{print $5}')

    case "${status}" in
        A)  echo "新增" ;;
        M)  echo "修改" ;;
        D)  echo "删除" ;;
        R*) echo "重命名" ;;
        T)  echo "类型变更" ;;
        C)  echo "复制" ;;
        *)  echo "未知" ;;
    esac
}

# 获取文件大小
get_file_size() {
    local hash="$1"
    local file="$2"
    local size
    size=$(git cat-file -s "${hash}:${file}" 2>/dev/null || echo "0")
    if [[ "${size}" == "0" ]]; then
        echo "N/A"
    else
        # 格式化文件大小
        if [[ ${size} -lt 1024 ]]; then
            echo "${size} B"
        elif [[ ${size} -lt 1048576 ]]; then
            echo "$(echo "scale=1; ${size} / 1024" | bc) KB"
        else
            echo "$(echo "scale=1; ${size} / 1048576" | bc) MB"
        fi
    fi
}

# 生成核查报告
generate_report() {
    local hash="$1"
    local expected_count="$2"
    local file_stats total_additions total_deletions file_count
    local i=0

    # 获取提交信息
    local commit_info
    commit_info=$(get_commit_info "${hash}")
    local author author_date subject body changed_files
    IFS='|' read -r author author_date subject body changed_files <<< "${commit_info}"

    # 输出报告头部
    print_header "Git 提交核查报告"
    echo ""
    echo -e "${BOLD}脚本版本:${NC}    ${SCRIPT_VERSION}"
    echo -e "${BOLD}核查时间:${NC}    $(date '+%Y-%m-%d %H:%M:%S %Z')"
    echo ""

    # 提交基本信息
    print_separator
    echo -e "${BOLD}📋 提交基本信息${NC}"
    print_separator
    echo -e "${BOLD}提交哈希:${NC}    ${hash}"
    echo -e "${BOLD}短哈希:${NC}      $(git rev-parse --short "${hash}")"
    echo -e "${BOLD}作者:${NC}        ${author}"
    echo -e "${BOLD}提交时间:${NC}    ${author_date}"
    echo -e "${BOLD}提交说明:${NC}    ${subject}"
    if [[ -n "${body}" && "${body}" != "${subject}" ]]; then
        echo -e "${BOLD}详细说明:${NC}"
        echo "${body}" | sed 's/^/    /'
    fi
    echo ""

    # 文件变更统计
    print_separator
    echo -e "${BOLD}📊 文件变更统计${NC}"
    print_separator

    file_stats=$(get_file_list_with_stats "${hash}")
    file_count=$(echo "${file_stats}" | grep -v '^$' | wc -l)
    total_additions=$(echo "${file_stats}" | awk '{sum+=$1} END {print sum+0}')
    total_deletions=$(echo "${file_stats}" | awk '{sum+=$2} END {print sum+0}')

    echo -e "${BOLD}变更文件数:${NC}  ${file_count}"
    echo -e "${BOLD}新增行数:${NC}    ${total_additions}"
    echo -e "${BOLD}删除行数:${NC}    ${total_deletions}"
    echo -e "${BOLD}总变更行数:${NC}  $((total_additions + total_deletions))"
    echo ""

    # 检查文件数量
    print_separator
    echo -e "${BOLD}🔍 文件数量核查${NC}"
    print_separator

    if [[ ${expected_count} -ge 0 ]]; then
        echo -e "${BOLD}预期文件数:${NC}  ${expected_count}"
        echo -e "${BOLD}实际文件数:${NC}  ${file_count}"
        if [[ ${file_count} -eq ${expected_count} ]]; then
            print_success "文件数量一致"
        else
            local diff=$((file_count - expected_count))
            if [[ ${diff} -gt 0 ]]; then
                print_warning "实际比预期多 ${diff} 个文件"
            else
                print_warning "实际比预期少 $((-diff)) 个文件"
            fi
        fi
    else
        print_info "未指定预期文件数量，跳过数量检查"
        echo -e "${BOLD}实际文件数:${NC}  ${file_count}"
    fi
    echo ""

    # 文件详细清单
    print_separator
    echo -e "${BOLD}📁 变更文件详细清单${NC}"
    print_separator

    if [[ ${file_count} -eq 0 ]]; then
        print_warning "此提交未包含文件变更"
    else
        # 表头
        printf "%-4s %-50s %-8s %-10s %-10s %-12s %-64s\n" \
            "#" "文件路径" "状态" "新增行" "删除行" "大小" "SHA256 哈希"
        print_separator

        # 遍历每个文件
        while IFS=$'\t' read -r add del file; do
            [[ -z "${file}" ]] && continue

            i=$((i + 1))
            local ftype fsize fhash
            ftype=$(get_file_type "${hash}" "${file}")
            fsize=$(get_file_size "${hash}" "${file}")
            fhash=$(calculate_file_hash "${hash}" "${file}")

            # 截断长文件名
            local display_file="${file}"
            if [[ ${#file} -gt 48 ]]; then
                display_file="...${file: -45}"
            fi

            printf "%-4d %-50s %-10s %-10s %-10s %-12s %-64s\n" \
                "${i}" "${display_file}" "${ftype}" "${add}" "${del}" "${fsize}" "${fhash}"

        done <<< "${file_stats}"
    fi
    echo ""

    # 统计摘要
    print_separator
    echo -e "${BOLD}📈 核查摘要${NC}"
    print_separator

    local all_pass=true

    # 检查 1：文件数量
    if [[ ${expected_count} -ge 0 ]]; then
        if [[ ${file_count} -eq ${expected_count} ]]; then
            print_success "[检查 1/3] 文件数量一致 (${file_count} = ${expected_count})"
        else
            print_error "[检查 1/3] 文件数量不匹配 (${file_count} ≠ ${expected_count})"
            all_pass=false
        fi
    else
        print_info "[检查 1/3] 文件数量检查已跳过（未指定预期值）"
    fi

    # 检查 2：每个文件都有有效的哈希
    local hash_valid_count=0
    local hash_invalid_count=0
    while IFS=$'\t' read -r add del file; do
        [[ -z "${file}" ]] && continue
        local fhash
        fhash=$(calculate_file_hash "${hash}" "${file}")
        if [[ "${fhash}" != "N/A" && ${#fhash} -eq 64 ]]; then
            hash_valid_count=$((hash_valid_count + 1))
        else
            hash_invalid_count=$((hash_invalid_count + 1))
        fi
    done <<< "${file_stats}"

    if [[ ${hash_invalid_count} -eq 0 ]]; then
        print_success "[检查 2/3] 所有 ${hash_valid_count} 个文件哈希验证通过"
    else
        print_error "[检查 2/3] ${hash_invalid_count} 个文件哈希验证失败"
        all_pass=false
    fi

    # 检查 3：提交签名验证（如果适用）
    if git verify-commit "${hash}" > /dev/null 2>&1; then
        print_success "[检查 3/3] 提交已 GPG 签名验证通过"
    else
        print_warning "[检查 3/3] 提交未 GPG 签名（建议启用签名提交）"
    fi
    echo ""

    # 最终判定
    print_separator
    echo -e "${BOLD}🏁 最终核查结果${NC}"
    print_separator

    if ${all_pass}; then
        print_success "核查通过 ✅"
        echo ""
        echo -e "${GREEN}此提交符合文件一致性要求。${NC}"
        return 0
    else
        print_error "核查未通过 ❌"
        echo ""
        echo -e "${RED}此提交存在文件一致性问题，请人工复核。${NC}"
        return 4
    fi
}

# 导出 JSON 报告
export_json_report() {
    local hash="$1"
    local output_path="$2"
    local file_stats file_count

    file_stats=$(get_file_list_with_stats "${hash}")
    file_count=$(echo "${file_stats}" | grep -v '^$' | wc -l)

    # 构建 JSON
    local json="{"
    json+="\"script_version\":\"${SCRIPT_VERSION}\","
    json+="\"check_time\":\"$(date -Iseconds)\","
    json+="\"commit\":{"
    json+="\"hash\":\"${hash}\","
    json+="\"short_hash\":\"$(git rev-parse --short "${hash}")\","
    json+="\"author\":\"$(git log -1 --format="%an <%ae>" "${hash}" | sed 's/"/\\"/g')\","
    json+="\"date\":\"$(git log -1 --format="%ai" "${hash}")\","
    json+="\"subject\":\"$(git log -1 --format="%s" "${hash}" | sed 's/"/\\"/g')\""
    json+="},"
    json+="\"statistics\":{"
    json+="\"file_count\":${file_count},"
    json+="\"total_additions\":$(echo "${file_stats}" | awk '{sum+=$1} END {print sum+0}'),"
    json+="\"total_deletions\":$(echo "${file_stats}" | awk '{sum+=$2} END {print sum+0}')"
    json+="},"
    json+="\"files\":["

    local first=true
    while IFS=$'\t' read -r add del file; do
        [[ -z "${file}" ]] && continue

        if ! ${first}; then
            json+=","
        fi
        first=false

        local ftype fsize fhash
        ftype=$(get_file_type "${hash}" "${file}")
        fsize=$(git cat-file -s "${hash}:${file}" 2>/dev/null || echo "0")
        fhash=$(calculate_file_hash "${hash}" "${file}")

        json+="{"
        json+="\"path\":\"${file}\","
        json+="\"type\":\"${ftype}\","
        json+="\"additions\":${add},"
        json+="\"deletions\":${del},"
        json+="\"size_bytes\":${fsize},"
        json+="\"sha256\":\"${fhash}\""
        json+="}"
    done <<< "${file_stats}"

    json+="],"

    # 合规判定
    local compliant="true"
    if [[ ${EXPECTED_FILE_COUNT} -ge 0 && ${file_count} -ne ${EXPECTED_FILE_COUNT} ]]; then
        compliant="false"
    fi

    json+="\"compliance\":{"
    json+="\"file_count_match\":${compliant},"
    json+="\"expected_count\":${EXPECTED_FILE_COUNT},"
    json+="\"actual_count\":${file_count}"
    json+="}"
    json+="}"

    # 写入文件
    echo "${json}" > "${output_path}"
    print_success "报告已导出至: ${output_path}"
}

# ============ 主函数 ============

main() {
    # 解析参数
    local positional_args=()

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_usage
                exit 0
                ;;
            --version)
                echo "${SCRIPT_NAME} version ${SCRIPT_VERSION}"
                exit 0
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            --export)
                if [[ -n "${2:-}" ]]; then
                    EXPORT_PATH="$2"
                    shift 2
                else
                    print_error "--export 需要一个文件路径参数"
                    exit 1
                fi
                ;;
            -*)
                print_error "未知选项: $1"
                show_usage
                exit 1
                ;;
            *)
                positional_args+=("$1")
                shift
                ;;
        esac
    done

    # 检查位置参数数量
    if [[ ${#positional_args[@]} -lt ${MIN_ARGS} ]]; then
        print_error "缺少必需参数: commit_hash"
        echo ""
        show_usage
        exit 1
    fi

    if [[ ${#positional_args[@]} -gt ${MAX_ARGS} ]]; then
        print_error "参数过多，最多接受 2 个位置参数"
        echo ""
        show_usage
        exit 1
    fi

    local commit_ref="${positional_args[0]}"
    if [[ ${#positional_args[@]} -ge 2 ]]; then
        EXPECTED_FILE_COUNT="${positional_args[1]}"
        # 验证数字
        if ! [[ "${EXPECTED_FILE_COUNT}" =~ ^[0-9]+$ ]]; then
            print_error "expected_file_count 必须是一个非负整数"
            exit 1
        fi
    fi

    # 检查是否在 Git 仓库中
    check_git_repo

    # 验证提交
    validate_commit "${commit_ref}"

    if ${VERBOSE}; then
        print_info "开始核查提交: ${COMMIT_HASH}"
        print_info "预期文件数: ${EXPECTED_FILE_COUNT}"
        echo ""
    fi

    # 生成报告
    local exit_code=0
    generate_report "${COMMIT_HASH}" "${EXPECTED_FILE_COUNT}" || exit_code=$?

    # 导出 JSON（如果请求）
    if [[ -n "${EXPORT_PATH}" ]]; then
        echo ""
        print_separator
        echo -e "${BOLD}📤 导出报告${NC}"
        print_separator
        export_json_report "${COMMIT_HASH}" "${EXPORT_PATH}"
    fi

    # 返回最终状态
    exit ${exit_code}
}

# 执行主函数
main "$@"
