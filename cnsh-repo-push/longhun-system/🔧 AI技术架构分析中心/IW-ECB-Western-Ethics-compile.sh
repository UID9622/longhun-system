#!/bin/bash
# 🐉 龍魂系统 | IW-ECB 论文编译脚本
# DNA: #龍芯⚡️2026-03-04-PAPER-COMPILE-v1.0
echo "🐉 编译 IW-ECB IEEE 论文..."

# XeLaTeX 编译（支持中文 + Unicode 符号）
xelatex IW-ECB-Western-Ethics.tex
bibtex IW-ECB-Western-Ethics
xelatex IW-ECB-Western-Ethics.tex
xelatex IW-ECB-Western-Ethics.tex

echo "✅ 编译完成！输出：IW-ECB-Western-Ethics.pdf"
echo "🧬 DNA: #龍芯⚡️2026-03-04-PAPER-LATEX-IEEE-v1.0"
