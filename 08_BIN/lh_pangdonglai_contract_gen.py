# DNA: #龍芯⚡️丙午·丙申·甲子·癸酉·䷪夬-CODE-补DNA-b08d67df
#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
lh_pangdonglai_contract_gen — 龍魂·胖东来分成契约生成器 v1.0

生成 PDF 签约模板和 HTML 网页版契约。
支持企业信息自动填入、DNA编码生成、签章区域。

DNA: #龍芯⚡️丙午·癸未·丁亥·丙午·䷣明-PANGDONGLAI-CONTRACT-GEN-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用法:
  python3 bin/lh_pangdonglai_contract_gen.py generate --name "企业全称" --uscc "信用代码"
  python3 bin/lh_pangdonglai_contract_gen.py generate --name "企业全称" --legal-person "法人名"
  python3 bin/lh_pangdonglai_contract_gen.py generate --name "企业全称" --modules "数据主权,审计链"
  python3 bin/lh_pangdonglai_contract_gen.py generate --all  # 交互式填写
  python3 bin/lh_pangdonglai_contract_gen.py template         # 输出空白模板
  python3 bin/lh_pangdonglai_contract_gen.py batch --csv enterprises.csv  # 批量生成

输出:
  contracts/{企业代码}_胖东来分成契约_{日期}.pdf
  contracts/{企业代码}_胖东来分成契约_{日期}.html
"""

import argparse
import hashlib
import json
import os
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTRACT_DIR = PROJECT_ROOT / "01_protocols" / "contracts"

# ═══════════════════════════════════════════════════════════
# 数据模型
# ═══════════════════════════════════════════════════════════

@dataclass
class ContractData:
    """契约数据"""
    enterprise_name: str = ""
    uscc: str = ""
    legal_person: str = ""
    registered_address: str = ""
    modules: List[str] = field(default_factory=list)
    sign_date: str = ""
    dna: str = ""

    def enterprise_code(self) -> str:
        """企业代码（USCC后6位或名称hash）"""
        if self.uscc and len(self.uscc) >= 6:
            return self.uscc[-6:]
        return hashlib.sha256(self.enterprise_name.encode()).hexdigest()[:6].upper()

    def generate_dna(self) -> str:
        """生成契约DNA"""
        today = datetime.now().strftime("%Y%m%d")
        code = self.enterprise_code()
        hash_input = f"{self.enterprise_name}{self.uscc}{today}"
        h = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
        self.dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-PANGDONGLAI-COVENANT-{code}-{h}"
        return self.dna

    def to_dict(self) -> Dict:
        return {
            "enterprise_name": self.enterprise_name,
            "uscc": self.uscc,
            "legal_person": self.legal_person,
            "registered_address": self.registered_address,
            "modules": self.modules,
            "sign_date": self.sign_date or datetime.now().strftime("%Y-%m-%d"),
            "dna": self.dna,
        }


# ═══════════════════════════════════════════════════════════
# 模板引擎
# ═══════════════════════════════════════════════════════════

MODULE_OPTIONS = {
    "数据主权": "□ 数据主权 (P0-03)",
    "审计链": "□ 审计链 (P0-06)",
    "行为密码学": "□ 行为密码学 (P0-07)",
    "CNSH协议": "□ CNSH协议 (P0-01)",
}

MODULE_LIST = list(MODULE_OPTIONS.keys())


def render_text_template(data: ContractData) -> str:
    """生成ASCII艺术文本版契约"""
    modules_checked = []
    for m in MODULE_LIST:
        checked = "☑" if m in data.modules else "☐"
        desc = MODULE_OPTIONS[m].replace("□", "")
        modules_checked.append(f"  {checked} {desc}")
    modules_text = "\n".join(modules_checked) if modules_checked else "  ☐ 未指定"

    other_checked = "☑" if any(m not in MODULE_LIST for m in data.modules) else "☐"
    other_text = ", ".join(m for m in data.modules if m not in MODULE_LIST) if data.modules else "____"

    today = data.sign_date or datetime.now().strftime("%Y-%m-%d")
    dna = data.dna or data.generate_dna()

    return f"""
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║         龍魂·胖东来分成数学契约                                       ║
║         PANGDONGLAI PROFIT-SPLIT COVENANT                            ║
║                                                                      ║
║         协议层级: P1 核心宪法                                         ║
║         DNA: {dna:<52s}║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  缔约方信息:                                                          ║
║  ─────────────────────────────────────────────────────────────       ║
║  企业全称: {data.enterprise_name or '____________________':<56s}║
║  统一社会信用代码: {data.uscc or '____________________':<50s}║
║  法定代表人: {data.legal_person or '____________________':<54s}║
║  注册地址: {data.registered_address or '____________________':<52s}║
║                                                                      ║
║  接入核心模块:                                                        ║
║  ─────────────────────────────────────────────────────────────       ║
{modules_text}                                                          ║
║  {other_checked} 其他: {other_text:<54s}║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  本人/本企业自愿接受以下数学约束（焊死·不可修改）:                     ║
║                                                                      ║
║  1. 员工分配（含分红/奖金/股权激励）≥ 净利润的 50%                     ║
║  2. 创始人/实控人提取 ≤ 净利润的 10%                                  ║
║  3. 再投资（研发/扩产/技术升级）≥ 净利润的 30%                        ║
║  4. 公益/社会 ≥ 净利润的 5%                                          ║
║  5. 全部分成数据上链审计，数据经端侧加密后仅存哈希指纹                   ║
║  6. 接受每季度自动审计，审计结果可公开查询                              ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  违约后果:                                                            ║
║  ▸ 自动冻结龍魂核心赋能接口（立即生效）                                ║
║  ▸ DNA追溯公开（违约事实写入不可篡改链）                               ║
║  ▸ 创始人/企业进入龍魂体系失信名单                                     ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  签署区:                                                              ║
║                                                                      ║
║  企业公章:  ___________________________    日期: {today:<20s}║
║                                                                      ║
║  法定代表人签字: _______________________    日期: {today:<20s}║
║                                                                      ║
║  龍魂见证人（UID9622）: _______________    日期: {today:<20s}║
║                                                                      ║
║  DNA锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL        ║
║  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z                         ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

═══════════════════════════════════════════════════════════════════════
  龍魂系统 · 主权人格 · 透明审计 · 分布式部署
  UID9622 · 龍芯北辰 · {datetime.now().year}
  协议: CC BY-NC-SA 4.0 · 来源链不可切断 · 数据主权归签署方
═══════════════════════════════════════════════════════════════════════
"""


def render_html_template(data: ContractData) -> str:
    """生成HTML版契约（可用于PDF转换）"""
    today = data.sign_date or datetime.now().strftime("%Y-%m-%d")
    dna = data.dna or data.generate_dna()
    dn = data.enterprise_name or "____________________"
    du = data.uscc or "____________________"
    dl = data.legal_person or "____________________"
    da = data.registered_address or "____________________"

    modules_html = ""
    for m in MODULE_LIST:
        checked = "checked" if m in data.modules else ""
        desc = MODULE_OPTIONS[m].replace("□ ", "")
        modules_html += f"""
        <label class="module-option {'selected' if checked else ''}">
          <input type="checkbox" {checked} disabled> {desc}
        </label>"""

    other_val = ", ".join(m for m in data.modules if m not in MODULE_LIST) if any(m not in MODULE_LIST for m in data.modules) else ""

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>胖东来分成数学契约 - {dn}</title>
<style>
  @page {{ size: A4; margin: 1.5cm; }}
  body {{ font-family: "PingFang SC","Microsoft YaHei","STSong",serif; color:#1a1a1a; max-width:210mm; margin:0 auto; padding:10mm; }}
  .border-box {{ border:3px double #c41e3a; padding:20px; }}
  h1 {{ text-align:center; color:#c41e3a; font-size:24px; margin:0 0 4px 0; }}
  .subtitle {{ text-align:center; color:#888; font-size:12px; margin-bottom:20px; }}
  .dna-bar {{ background:#f5f0eb; border-left:4px solid #c41e3a; padding:8px 12px; font-family:monospace; font-size:10px; margin:16px 0; word-break:break-all; }}
  .section {{ margin:16px 0; }}
  .section h2 {{ color:#c41e3a; font-size:16px; border-bottom:1px solid #d4a574; padding-bottom:4px; }}
  .field {{ display:flex; align-items:center; margin:8px 0; }}
  .field .label {{ width:160px; font-weight:bold; flex-shrink:0; }}
  .field .value {{ border-bottom:1px solid #999; flex:1; padding:4px 8px; min-width:200px; }}
  .field .value.filled {{ color:#1a1a1a; }}
  .field .value.empty {{ color:#ccc; }}
  .module-option {{ display:inline-block; margin:4px 12px 4px 0; padding:6px 12px; border:1px solid #ddd; border-radius:4px; font-size:13px; }}
  .module-option.selected {{ background:#fff3e0; border-color:#d4a574; }}
  .module-option input {{ margin-right:4px; }}
  .rules {{ background:#fafafa; border:1px solid #eee; border-radius:6px; padding:12px 16px; }}
  .rules li {{ margin:6px 0; line-height:1.6; }}
  .violations {{ background:#fff3e0; border:1px solid #ffcc80; border-radius:6px; padding:12px 16px; margin:16px 0; }}
  .violations h3 {{ color:#e65100; margin:0 0 8px 0; }}
  .signatures {{ display:flex; gap:20px; margin:24px 0; }}
  .sig-block {{ flex:1; }}
  .sig-block .sig-line {{ border-bottom:1px solid #333; margin:30px 0 4px 0; }}
  .sig-block .sig-label {{ font-size:12px; color:#666; }}
  .footer {{ margin-top:30px; padding-top:12px; border-top:1px solid #eee; font-size:10px; color:#888; text-align:center; }}
  .seal {{ color:#c41e3a; font-size:14px; font-weight:bold; }}
  @media print {{ body {{ padding:0; }} .border-box {{ border:none; padding:0; }} }}
</style>
</head>
<body>
<div class="border-box">

<h1>龍魂·胖东来分成数学契约</h1>
<div class="subtitle">PANGDONGLAI PROFIT-SPLIT COVENANT · 协议层级 P1 核心宪法</div>
<div class="dna-bar">
  契约DNA: {dna}<br>
  确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z<br>
  GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
</div>

<div class="section">
  <h2>一、缔约方信息</h2>
  <div class="field"><span class="label">企业全称</span><span class="value {'filled' if data.enterprise_name else 'empty'}">{dn}</span></div>
  <div class="field"><span class="label">统一社会信用代码</span><span class="value {'filled' if data.uscc else 'empty'}">{du}</span></div>
  <div class="field"><span class="label">法定代表人</span><span class="value {'filled' if data.legal_person else 'empty'}">{dl}</span></div>
  <div class="field"><span class="label">注册地址</span><span class="value {'filled' if data.registered_address else 'empty'}">{da}</span></div>
</div>

<div class="section">
  <h2>二、接入核心模块</h2>
  <div>{modules_html}</div>
  <div class="field" style="margin-top:8px">
    <span class="label">其他模块</span>
    <span class="value {'filled' if other_val else 'empty'}">{other_val or '____________________'}</span>
  </div>
</div>

<div class="section">
  <h2>三、数学约束（焊死·不可修改）</h2>
  <div class="rules">
    <ol>
      <li><strong>员工分配</strong>（含分红/奖金/股权激励）<strong>≥ 净利润的 50%</strong></li>
      <li><strong>创始人/实控人提取 ≤ 净利润的 10%</strong></li>
      <li><strong>再投资</strong>（研发/扩产/技术升级）<strong>≥ 净利润的 30%</strong></li>
      <li><strong>公益/社会 ≥ 净利润的 5%</strong></li>
      <li>全部分成数据<strong>上链审计</strong>，数据经端侧加密后仅存哈希指纹</li>
      <li>接受<strong>每季度自动审计</strong>，审计结果可公开查询</li>
    </ol>
  </div>
</div>

<div class="section">
  <h2>四、违约后果</h2>
  <div class="violations">
    <h3>⚠️ 违反任一条款将触发：</h3>
    <ul>
      <li><strong>自动冻结</strong>龍魂核心赋能接口（立即生效·不可申诉）</li>
      <li><strong>DNA追溯公开</strong>——违约事实写入不可篡改链</li>
      <li>创始人/企业进入<strong>龍魂体系失信名单</strong></li>
    </ul>
  </div>
</div>

<div class="section">
  <h2>五、签署</h2>
  <div class="signatures">
    <div class="sig-block">
      <div class="sig-line"></div>
      <div class="sig-label">企业公章</div>
      <div style="font-size:11px;color:#888;margin-top:4px">日期: {today}</div>
    </div>
    <div class="sig-block">
      <div class="sig-line"></div>
      <div class="sig-label">法定代表人签字</div>
      <div style="font-size:11px;color:#888;margin-top:4px">日期: {today}</div>
    </div>
    <div class="sig-block">
      <div class="sig-line"></div>
      <div class="sig-label">龍魂见证人（UID9622）</div>
      <div style="font-size:11px;color:#888;margin-top:4px">日期: {today}</div>
    </div>
  </div>
</div>

<div class="seal" style="text-align:center;margin:20px 0">
  DNA锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
</div>

<div class="footer">
  龍魂系统 · 胖东来分成数学协议 v1.0 · 创建者: 诸葛鑫（UID9622·龍芯北辰）<br>
  协议许可: CC BY-NC-SA 4.0 · 来源链不可切断 · 数据主权归签署方<br>
  审计引擎: bin/lh_pangdonglai_audit.py · 契约生成: bin/lh_pangdonglai_contract_gen.py
</div>

</div>
</body>
</html>"""


# ═══════════════════════════════════════════════════════════
# PDF 生成
# ═══════════════════════════════════════════════════════════

def generate_pdf(html_content: str, output_path: str) -> bool:
    """通过 weasyprint 生成 PDF"""
    try:
        from weasyprint import HTML, CSS as WCSS
        import markdown as md

        css = WCSS(string="""
@page { size: A4; margin: 1.5cm; }
body { font-family: "PingFang SC","Microsoft YaHei","STSong",serif; }
""")
        HTML(string=html_content).write_pdf(output_path, stylesheets=[css])
        return True
    except ImportError:
        return False


def save_contract(data: ContractData, output_dir: Optional[str] = None) -> Dict[str, str]:
    """保存契约（HTML + 尝试PDF）"""
    if output_dir:
        out_dir = Path(output_dir)
    else:
        out_dir = CONTRACT_DIR
    out_dir.mkdir(parents=True, exist_ok=True)

    code = data.enterprise_code()
    today = datetime.now().strftime("%Y%m%d")
    base_name = f"{code}_胖东来分成契约_{today}"

    # 生成内容
    data.generate_dna()
    html_content = render_html_template(data)
    text_content = render_text_template(data)

    results = {}

    # 保存HTML
    html_path = out_dir / f"{base_name}.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    results["html"] = str(html_path)

    # 尝试生成PDF
    pdf_path = out_dir / f"{base_name}.pdf"
    if generate_pdf(html_content, str(pdf_path)):
        results["pdf"] = str(pdf_path)
    else:
        results["pdf"] = None
        # 降级：保存Markdown版本（可用 md_to_pdf.py 后续转换）
        md_path = out_dir / f"{base_name}.md"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(text_content)
        results["md"] = str(md_path)

    # 保存JSON元数据
    json_path = out_dir / f"{base_name}.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data.to_dict(), f, ensure_ascii=False, indent=2)
    results["json"] = str(json_path)

    return results


# ═══════════════════════════════════════════════════════════
# 命令行入口
# ═══════════════════════════════════════════════════════════

def interactive_fill() -> ContractData:
    """交互式填写契约信息"""
    print("\n╔══════════════════════════════════════════╗")
    print("║  龍魂·胖东来分成契约 — 交互式填写       ║")
    print("╚══════════════════════════════════════════╝\n")

    name = input("企业全称: ").strip()
    uscc = input("统一社会信用代码 (回车跳过): ").strip()
    legal = input("法定代表人 (回车跳过): ").strip()
    address = input("注册地址 (回车跳过): ").strip()

    print("\n接入核心模块（多选用逗号分隔）:")
    for i, m in enumerate(MODULE_LIST, 1):
        print(f"  {i}. {m}")
    print(f"  {len(MODULE_LIST)+1}. 全部")
    choice = input("选择 (如 1,2,3 或 all): ").strip()

    if choice.lower() == "all" or str(len(MODULE_LIST)+1) in choice:
        modules = MODULE_LIST.copy()
    elif choice:
        try:
            indices = [int(x.strip())-1 for x in choice.split(",")]
            modules = [MODULE_LIST[i] for i in indices if 0 <= i < len(MODULE_LIST)]
        except (ValueError, IndexError):
            modules = [m.strip() for m in choice.split(",")]
    else:
        modules = []

    # 询问是否添加自定义模块
    custom = input("其他自定义模块 (逗号分隔·回车跳过): ").strip()
    if custom:
        modules.extend([m.strip() for m in custom.split(",") if m.strip()])

    data = ContractData(
        enterprise_name=name,
        uscc=uscc,
        legal_person=legal,
        registered_address=address,
        modules=modules,
    )

    print("\n预览:\n")
    print(render_text_template(data))

    confirm = input("确认生成？(Y/n): ").strip().lower()
    if confirm and confirm != "y":
        print("已取消")
        sys.exit(0)

    return data


def main():
    parser = argparse.ArgumentParser(description="龍魂·胖东来分成契约生成器 v1.0")
    sub = parser.add_subparsers(dest="command")

    # generate 子命令
    gen_p = sub.add_parser("generate", help="生成契约")
    gen_p.add_argument("--name", "-n", help="企业全称")
    gen_p.add_argument("--uscc", "-u", help="统一社会信用代码")
    gen_p.add_argument("--legal-person", "-l", help="法定代表人")
    gen_p.add_argument("--address", "-a", help="注册地址")
    gen_p.add_argument("--modules", "-m", help="接入模块·逗号分隔")
    gen_p.add_argument("--all", action="store_true", help="交互式填写全部字段")
    gen_p.add_argument("--output", "-o", help="输出目录")
    gen_p.add_argument("--print", action="store_true", dest="print_only", help="仅打印到终端·不保存文件")

    # template 子命令
    sub.add_parser("template", help="输出空白HTML模板")

    # batch 子命令
    batch_p = sub.add_parser("batch", help="批量生成·从CSV/JSON读取")
    batch_p.add_argument("--csv", help="CSV文件路径（列: name,uscc,legal_person,address,modules）")
    batch_p.add_argument("--json", help="JSON文件路径")
    batch_p.add_argument("--output", "-o", help="输出目录")

    args = parser.parse_args()

    if args.command == "generate":
        if args.all:
            data = interactive_fill()
        elif args.name:
            modules = [m.strip() for m in args.modules.split(",")] if args.modules else []
            data = ContractData(
                enterprise_name=args.name,
                uscc=args.uscc or "",
                legal_person=args.legal_person or "",
                registered_address=args.address or "",
                modules=modules,
                sign_date=datetime.now().strftime("%Y-%m-%d"),
            )
        else:
            print("❌ 请提供 --name 或使用 --all 交互式填写")
            sys.exit(1)

        if getattr(args, 'print_only', False):
            print(render_text_template(data))
        else:
            results = save_contract(data, args.output)
            print(f"\n✅ 契约已生成:")
            for fmt, path in results.items():
                if path:
                    print(f"  {fmt.upper()}: {path}")
                else:
                    print(f"  PDF: ⚠️  weasyprint 未安装·已生成HTML/MD降级版本")
            print(f"\n  DNA: {data.dna}")

    elif args.command == "template":
        data = ContractData()
        print(render_html_template(data))

    elif args.command == "batch":
        enterprises = []
        if args.csv:
            import csv
            with open(args.csv, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    modules = [m.strip() for m in row.get("modules", "").split(",") if m.strip()]
                    enterprises.append(ContractData(
                        enterprise_name=row.get("name", ""),
                        uscc=row.get("uscc", ""),
                        legal_person=row.get("legal_person", ""),
                        registered_address=row.get("address", ""),
                        modules=modules,
                        sign_date=datetime.now().strftime("%Y-%m-%d"),
                    ))
        elif args.json:
            with open(args.json, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                for raw in raw_list:
                    enterprises.append(ContractData(
                        enterprise_name=raw.get("enterprise_name", raw.get("name", "")),
                        uscc=raw.get("uscc", ""),
                        legal_person=raw.get("legal_person", ""),
                        registered_address=raw.get("registered_address", raw.get("address", "")),
                        modules=raw.get("modules", []),
                        sign_date=datetime.now().strftime("%Y-%m-%d"),
                    ))

        if not enterprises:
            print("❌ 未读取到任何企业数据")
            sys.exit(1)

        for ent in enterprises:
            results = save_contract(ent, args.output)
            print(f"✅ {ent.enterprise_name}: {results.get('html','?')}")

        print(f"\n共生成 {len(enterprises)} 份契约")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
