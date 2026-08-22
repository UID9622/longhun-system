#!/bin/bash
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂文档工厂 · 统一入口
# 功能: 网页/PPT/PDF/Word/图片水印/EXIF 一键调度
# 用法: bash bin/docs_factory/factory.sh <子命令> [参数]
set -e
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENV="$ROOT/.venv_docs"
FAC="$ROOT/bin/docs_factory"

_activate() {
  if [ -f "$VENV/bin/activate" ]; then source "$VENV/bin/activate"
  else echo "⚠️ venv未就绪，正在后台安装..."; fi
}

case "$1" in
  ppt)
    _activate
    python3 "$FAC/make_ppt.py" "${@:2}"
    ;;
  docx)
    _activate
    python3 "$FAC/md_to_docx.py" "${@:2}"
    ;;
  pdf)
    _activate
    python3 "$FAC/md_to_pdf.py" "${@:2}"
    ;;
  watermark)
    python3 "$FAC/dna_watermark.py" "${@:2}"   # 仅依赖PIL，无需venv
    ;;
  exif)
    python3 "$FAC/image_exif.py" "${@:2}"      # 仅依赖PIL
    ;;
  install)
    python3 -m venv "$VENV"
    source "$VENV/bin/activate"
    pip install --quiet --upgrade pip
    pip install python-pptx python-docx markdown weasyprint
    echo "✅ 依赖安装完成"
    ;;
  *)
    echo "🐉 龍魂文档工厂"
    echo "用法: bash factory.sh <子命令> [参数]"
    echo "  ppt  --title 标题 --subtitle 副标 --out 输出.pptx"
    echo "  docx <输入.md> <输出.docx>"
    echo "  pdf  <输入.md> <输出.pdf>"
    echo "  watermark <输入图> <输出图> [--dna 码] [--author 作者]"
    echo "  exif <图片> [--json]"
    echo "  install   (安装pptx/docx/markdown/weasyprint到venv)"
    ;;
esac
