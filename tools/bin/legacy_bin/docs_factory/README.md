# 龍魂文档工厂 · 能力清单

> 本地可控·DNA嵌入·不依赖平台审核
> 最后验证: 丙午·辛未·乙酉 (2026-07-16)

## 已落地能力（实测可用）

| 能力 | 工具 | 依赖 | 状态 |
|------|------|------|:----:|
| **网页生成** | 暗色龍魂金HTML/CSS/JS | 无(纯前端) | ✅ 实战: docs.longhun888.com |
| **PPT生成** | `make_ppt.py` (python-pptx) | venv | ✅ 实测出.pptx |
| **Word生成** | `md_to_docx.py` (python-docx) | venv | ✅ 实测出.docx |
| **PDF生成** | `md_to_pdf.py` (markdown+weasyprint) | venv | ✅ 实测出.pdf |
| **图片DNA水印** | `dna_watermark.py` (PIL) | 系统PIL | ✅ 实测·保留作者署名 |
| **图片EXIF溯源** | `image_exif.py` (PIL) | 系统PIL | ✅ 实测 |
| **反向搜图/图片搜索** | 待接入图片搜索工具 | — | ⏳ 环境无该工具 |

## 目录
```
bin/docs_factory/
├── factory.sh          # 统一入口: bash factory.sh <ppt|docx|pdf|watermark|exif|install>
├── make_ppt.py         # PPT生成器
├── md_to_docx.py       # Markdown→Word
├── md_to_pdf.py        # Markdown→PDF
├── dna_watermark.py    # 图片DNA水印(PIL)
├── image_exif.py       # 图片EXIF提取(PIL)
└── README.md
output/                 # 产物
├── web/ ppt/ pdf/ docx/ images/
```

## 快速使用
```bash
cd /Users/zuimeidedeyihan/longhun-system
source .venv_docs/bin/activate        # PPT/PDF/Word 必须先激活venv

# PPT
bash bin/docs_factory/factory.sh ppt --title "标题" --subtitle "副标" --out output/ppt/x.pptx

# Word
bash bin/docs_factory/factory.sh docx 输入.md output/docx/x.docx

# PDF
bash bin/docs_factory/factory.sh pdf 输入.md output/pdf/x.pdf

# 图片DNA水印 (无需venv)
bash bin/docs_factory/factory.sh watermark 原图.png 输出.png --author "原作者/来源"

# EXIF
bash bin/docs_factory/factory.sh exif 图片.png --json
```

## 设计系统（龍魂规范）
- 红 `#c41e3a` · 金 `#d4a574` · 黑 `#1a1a1a` · 白 `#f5f5f5`
- 每页/每文嵌入 DNA: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`
- 图片引用必须保留原作者/来源/许可证，龍魂DNA为二次创作追溯

## 注意
- 首次使用若缺依赖: `bash bin/docs_factory/factory.sh install`（建.venv_docs并装pptx/docx/markdown/weasyprint）
- 网页能力不在此目录生成，由 `docs/` 下站点直接维护（如 `docs/监管审计系列17篇/`）
- 反向搜图/图片搜索需接入对应工具，当前环境未提供，标记为待接入
