#!/bin/bash
# 🐉 龍魂系统 | V9博弈论论文编译脚本
# DNA: #龍芯⚡️2026-03-04-PAPER-GAMETHEORY-COMPILE-v1.0
echo "🐉 编译 V9博弈论论文..."

# XeLaTeX 编译（支持中文 + Unicode 符号）
xelatex V9-GameTheory-Claude-Collaboration.tex
bibtex V9-GameTheory-Claude-Collaboration
xelatex V9-GameTheory-Claude-Collaboration.tex
xelatex V9-GameTheory-Claude-Collaboration.tex

echo "✅ 编译完成！输出：V9-GameTheory-Claude-Collaboration.pdf"
echo "🧬 DNA: #龍芯⚡️2026-03-04-PAPER-GAMETHEORY-IEEE-v1.0"
echo "🤝 协作: Claude × Anthropic PBC × Lucky UID9622"
