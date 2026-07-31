# DNA: #龍芯⚡️丙午·乙未·乙丑·未济-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-MD_TO_PDF-v1.0-7892795e
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
# -*- coding: utf-8 -*-
"""
龍魂·Markdown转PDF (markdown + weasyprint)
依赖: venv 内 markdown + weasyprint
功能: 将Markdown转HTML后用龍魂CSS生成A4 PDF。

用法:
    source .venv_docs/bin/activate
    python3 bin/docs_factory/md_to_pdf.py input.md output.pdf
"""
import argparse
import markdown as md

CSS = """
@page { size: A4; margin: 2cm; }
body { font-family: "PingFang SC","Microsoft YaHei",sans-serif; color:#1a1a1a; }
h1 { color:#c41e3a; border-bottom:2px solid #c41e3a; padding-bottom:6px; }
h2 { color:#c41e3a; }
.dna { background:#f5f5f5; border-left:3px solid #c41e3a; padding:10px;
       font-family:monospace; font-size:10px; }
table { border-collapse:collapse; width:100%; }
th,td { border:1px solid #ddd; padding:8px; }
th { background:#c41e3a; color:#fff; }
code { background:#f0f0f0; padding:2px 4px; border-radius:3px; }
blockquote { border-left:3px solid #d4a574; margin:0; padding-left:12px; color:#555; }
"""

def build(md_file, out):
    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()
    html = md.markdown(content, extensions=["tables", "fenced_code"])
    full = f"<!DOCTYPE html><html><head><meta charset='utf-8'></head><body>{html}</body></html>"
    try:
        from weasyprint import HTML, CSS as WCSS
        HTML(string=full).write_pdf(out, stylesheets=[WCSS(string=CSS)])
    except Exception as e:
        # 无weasyprint则退化为HTML落盘，保证不丢内容
        with open(out.replace(".pdf", ".html"), "w", encoding="utf-8") as f:
            f.write(full)
        return f"weasyprint不可用，已输出HTML: {out.replace('.pdf','.html')} ({e})"
    return f"PDF已生成: {out}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("md"); ap.add_argument("out")
    a = ap.parse_args()
    print(build(a.md, a.out))

if __name__ == "__main__":
    main()
