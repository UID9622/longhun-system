#!/bin/bash
# 二进制文件转换为文本脚本
# DNA: #ZHUGEXIN⚡️2026-01-27-BINARY-CONVERT-v1.0
# 用途：将 .docx、.pdf 等二进制文件转换为文本格式，便于AI读取

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BUNDLE_ROOT="$(dirname "$SCRIPT_DIR")"
TEXT_OUTPUT_DIR="$BUNDLE_ROOT/text_content"

# 创建输出目录
mkdir -p "$TEXT_OUTPUT_DIR"

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${RESET} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${RESET} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${RESET} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${RESET} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖工具..."

    local missing_deps=()

    # 检查 unzip (用于 .docx)
    if ! command -v unzip &> /dev/null; then
        missing_deps+=("unzip")
    fi

    # 检查 python3 (用于 .pdf)
    if ! command -v python3 &> /dev/null; then
        missing_deps+=("python3")
    fi

    # 检查 pandoc (可选，更强大的转换)
    if ! command -v pandoc &> /dev/null; then
        log_warning "pandoc 未安装，功能受限"
    fi

    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "缺少依赖: ${missing_deps[*]}"
        log_info "请安装缺少的工具:"
        log_info "  brew install ${missing_deps[*]}"
        return 1
    fi

    log_success "所有依赖检查通过"
    return 0
}

# 转换 .docx 文件
convert_docx() {
    local docx_file="$1"
    local base_name=$(basename "$docx_file" .docx)
    local output_file="$TEXT_OUTPUT_DIR/${base_name}.txt"

    log_info "转换 .docx 文件: $docx_file"

    # 使用 unzip 提取文本
    local temp_dir=$(mktemp -d)
    unzip -q "$docx_file" -d "$temp_dir" 2>/dev/null || {
        log_error "解压 .docx 失败: $docx_file"
        rm -rf "$temp_dir"
        return 1
    }

    # 提取文本内容（word/document.xml）
    if [ -f "$temp_dir/word/document.xml" ]; then
        # 提取文本并清理XML标签
        sed 's/<[^>]*>//g' "$temp_dir/word/document.xml" | \
        sed 's/&lt;/</g; s/&gt;/>/g; s/&amp;/\&/g' | \
        tr -s '[:space:]' '\n' | \
        grep -v '^$' > "$output_file"

        log_success "已生成: $output_file"
    else
        log_warning "未找到文档内容: $docx_file"
    fi

    # 清理临时目录
    rm -rf "$temp_dir"

    return 0
}

# 转换 .pdf 文件
convert_pdf() {
    local pdf_file="$1"
    local base_name=$(basename "$pdf_file" .pdf)
    local output_file="$TEXT_OUTPUT_DIR/${base_name}.txt"

    log_info "转换 .pdf 文件: $pdf_file"

    # 检查 Python PDF 解析库
    if python3 -c "import PyPDF2" 2>/dev/null; then
        # 使用 PyPDF2
        python3 - <<PYTHON_SCRIPT
import sys
import PyPDF2

try:
    with open('$pdf_file', 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'

    with open('$output_file', 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"成功提取 {len(reader.pages)} 页")
except Exception as e:
    print(f"错误: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT
        log_success "已生成: $output_file"
    elif python3 -c "import pdfplumber" 2>/dev/null; then
        # 使用 pdfplumber（更好的文本提取）
        python3 - <<PYTHON_SCRIPT
import sys
import pdfplumber

try:
    text = ''
    with pdfplumber.open('$pdf_file') as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text += f'--- Page {i+1} ---\n{page_text}\n'

    with open('$output_file', 'w', encoding='utf-8') as f:
        f.write(text)

    print(f"成功提取 {len(pdf.pages)} 页")
except Exception as e:
    print(f"错误: {e}", file=sys.stderr)
    sys.exit(1)
PYTHON_SCRIPT
        log_success "已生成: $output_file"
    else
        # 尝试使用 pdftotext (如果安装了)
        if command -v pdftotext &> /dev/null; then
            pdftotext "$pdf_file" "$output_file"
            log_success "已生成: $output_file (使用 pdftotext)"
        else
            log_error "无法转换 .pdf 文件: 缺少 PDF 解析库"
            log_info "请安装: pip install PyPDF2 或 pdfplumber"
            return 1
        fi
    fi

    return 0
}

# 转换 .doc 文件（旧版Word）
convert_doc() {
    local doc_file="$1"
    local base_name=$(basename "$doc_file" .doc)
    local output_file="$TEXT_OUTPUT_DIR/${base_name}.txt"

    log_info "转换 .doc 文件: $doc_file"

    if command -v pandoc &> /dev/null; then
        pandoc "$doc_file" -t plain -o "$output_file"
        log_success "已生成: $output_file (使用 pandoc)"
    else
        log_error "无法转换 .doc 文件: 需要 pandoc"
        log_info "请安装: brew install pandoc"
        return 1
    fi

    return 0
}

# 转换 .rtf 文件
convert_rtf() {
    local rtf_file="$1"
    local base_name=$(basename "$rtf_file" .rtf)
    local output_file="$TEXT_OUTPUT_DIR/${base_name}.txt"

    log_info "转换 .rtf 文件: $rtf_file"

    if command -v pandoc &> /dev/null; then
        pandoc "$rtf_file" -t plain -o "$output_file"
        log_success "已生成: $output_file (使用 pandoc)"
    else
        log_error "无法转换 .rtf 文件: 需要 pandoc"
        log_info "请安装: brew install pandoc"
        return 1
    fi

    return 0
}

# 处理单个文件
process_file() {
    local file="$1"

    if [ ! -f "$file" ]; then
        log_error "文件不存在: $file"
        return 1
    fi

    local ext="${file##*.}"

    case "$ext" in
        docx)
            convert_docx "$file"
            ;;
        pdf)
            convert_pdf "$file"
            ;;
        doc)
            convert_doc "$file"
            ;;
        rtf)
            convert_rtf "$file"
            ;;
        *)
            log_warning "不支持的文件类型: $ext"
            return 1
            ;;
    esac
}

# 批量转换
batch_convert() {
    local target_dir="$1"

    log_info "批量转换目录: $target_dir"

    # 查找所有二进制文档文件
    find "$target_dir" -type f \( -name "*.docx" -o -name "*.pdf" -o -name "*.doc" -o -name "*.rtf" \) -print0 | \
    while IFS= read -r -d '' file; do
        echo ""
        process_file "$file"
    done
}

# 显示使用帮助
show_help() {
    cat << EOF
二进制文件转换为文本脚本 v1.0

用法:
  $0 [选项] [文件/目录]

选项:
  -h, --help          显示此帮助信息
  -c, --check         检查依赖
  -f, --file FILE     转换单个文件
  -d, --dir DIR       批量转换目录
  -o, --output DIR    指定输出目录 (默认: text_content/)

支持格式:
  .docx  - Word 文档
  .pdf   - PDF 文档
  .doc   - 旧版 Word 文档 (需要 pandoc)
  .rtf   - 富文本格式 (需要 pandoc)

示例:
  # 转换单个文件
  $0 -f document.docx

  # 批量转换目录
  $0 -d /path/to/documents

  # 检查依赖
  $0 -c

EOF
}

# 主函数
main() {
    local target_files=()
    local target_dir=""
    local output_dir=""

    # 解析命令行参数
    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -c|--check)
                check_dependencies
                exit $?
                ;;
            -f|--file)
                target_files+=("$2")
                shift 2
                ;;
            -d|--dir)
                target_dir="$2"
                shift 2
                ;;
            -o|--output)
                output_dir="$2"
                TEXT_OUTPUT_DIR="$output_dir"
                mkdir -p "$TEXT_OUTPUT_DIR"
                shift 2
                ;;
            *)
                # 默认作为文件处理
                if [ -f "$1" ]; then
                    target_files+=("$1")
                elif [ -d "$1" ]; then
                    target_dir="$1"
                else
                    log_error "未知的参数或文件不存在: $1"
                    show_help
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # 如果没有指定目标，显示帮助
    if [ ${#target_files[@]} -eq 0 ] && [ -z "$target_dir" ]; then
        show_help
        exit 1
    fi

    # 检查依赖
    check_dependencies || exit 1

    echo "=========================================="
    echo "二进制文件转换工具"
    echo "输出目录: $TEXT_OUTPUT_DIR"
    echo "=========================================="
    echo ""

    # 转换文件
    if [ ${#target_files[@]} -gt 0 ]; then
        for file in "${target_files[@]}"; do
            process_file "$file"
        done
    fi

    # 批量转换目录
    if [ -n "$target_dir" ]; then
        batch_convert "$target_dir"
    fi

    echo ""
    echo "=========================================="
    log_success "转换完成！"
    log_info "输出目录: $TEXT_OUTPUT_DIR"
    echo "=========================================="
}

# 执行主函数
main "$@"
