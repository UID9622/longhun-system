#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂文章微信公众号发布版生成器 v1.3
DNA: #龍芯⚡️2026-07-04-LONGHUN-WECHAT-ARTICLE-PROCESSOR-v1.3
"""
import re
from pathlib import Path

SRC_DIR = Path.home() / "Desktop" / "文章" / "原文"
OUT_DIR = Path.home() / "Desktop" / "文章" / "微信公众号发布版"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# 脱敏替换规则：先处理 URL/邮箱等含 uid 的，再处理裸 uid
REPLACEMENTS = [
    # 邮箱（优先处理，避免 uid 被先剥离）
    (r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[联系邮箱]"),
    # 平台个人主页 ID（优先处理含 uid 的 URL）
    (r"blog\.csdn\.net/[\d_]+", "blog.csdn.net/[CSDN用户ID]"),
    (r"juejin\.cn/user/[\d_]+", "juejin.cn/user/[掘金用户ID]"),
    (r"cnblogs\.com/[a-zA-Z0-9_-]+", "cnblogs.com/[博客园用户ID]"),
    (r"[a-zA-Z0-9_-]+\.notion\.site", "[Notion工作区].notion.site"),
    (r"https?://www\.notion\.so/uid9622/[a-zA-Z0-9_-]+", "https://www.notion.so/[Notion工作区]/[页面ID]"),
    (r"gitee\.com/uid9622", "gitee.com/[代码仓库用户]"),
    (r"github\.com/uid9622", "github.com/[代码仓库用户]"),
    (r"github\.com/longhun-system", "github.com/[龍魂系统仓库]"),
    (r"github\.com/CNSH-Editor", "github.com/[CNSH编辑器仓库]"),
    # 个人标识
    (r"UID9622\s*[·/]\s*", ""),
    (r"\s*[·/]\s*UID9622", ""),
    (r"UID9622", ""),
    (r"uid9622", ""),
    (r"-UID9622-", "-"),
    (r"_UID9622_", "_"),
    (r"Lucky·诸葛鑫", "龍魂系统主理人"),
    (r"诸葛鑫", ""),
    (r"ZHUGEXIN", ""),
    (r"老大", "主理人"),
    # 确认码（正文中的文字形态）
    (r"CONFIRM🌌9622-ONLY-ONCE", ""),
    (r"CONFIRM9622-ONLY-ONCE-[A-Z0-9-]+", ""),
    (r"LK9X-772Z", ""),
    # 密钥与敏感字符串
    (r"#CONFIRM🌌[^\s]*", ""),
    (r"SEAL:\s*`?#ZHUGEXIN[^\n]*", ""),
    (r"GPG:\s*`?A2D0092CEE2E5BA87035600924C3704A8CC26D5F`?", ""),
    (r"A2D0092CEE2E5BA87035600924C3704A8CC26D5F", ""),
    (r"35c248aefe474b0d9b16344fc1d50b49", "[API密钥]"),
    (r"HPUASJ5GTYGL3ZYCWZMJ", "[华为云AK]"),
    (r"hTZMSC2lUBiML4TeGQwCj9oQpKsVAySE4sCq8NnP", "[华为云SK]"),
    # 网络地址
    (r"119\.13\.90\.27", "[服务器地址]"),
    # 手机号/身份证号
    (r"(?<!\d)1[3-9]\d{9}(?!\d)", "[手机号]"),
    (r"(?<!\d)\d{17}[\dXx](?!\d)", "[身份证号]"),
    # 本地路径
    (r"`?~/\.longhun[^`]*`?", "`[本地配置路径]`"),
    (r"`?~/longhun-system[^`]*`?", "`[项目路径]`"),
    (r"`?~/.kimi-code[^`]*`?", "`[AI配置路径]`"),
    (r"`?~/.cnsh[^`]*`?", "`[审计路径]`"),
    (r"`?/opt/longhun-system[^`]*`?", "`[云端部署路径]`"),
    (r"`?/root/[^`]*`?", "`[服务器路径]`"),
    (r"`?~/Desktop/[^`]*`?", "`[桌面路径]`"),
    (r"`?~/_work/[^`]*`?", "`[工作脚本路径]`"),
    (r"`?/Users/[^/]+/[^`]*`?", "`[本地路径]`"),
    (r"/var/folders/[^\s)\"'`]+", "[系统临时路径]"),
    # 个人背景信息
    (r"2008年济南二团退伍军人 · 初中文化", "[个人背景]"),
    (r"退伍军人、初中学历", "[个人背景]"),
    (r"退伍军人", "[退伍军人]"),
    (r"初中学历", "[学历背景]"),
    # 修复 gitee 双斜杠
    (r"gitee\.com//", "gitee.com/[代码仓库用户]/"),
    (r"gitee\.com/\[代码仓库用户\]//", "gitee.com/[代码仓库用户]/"),
]

# 需要整行移除的模式
LINE_REMOVALS = [
    r"^\s*GPG:\s*``?\s*$",
    r"^\s*CONFIRM:\s*``?\s*$",
    r"^\s*SEAL:\s*``?\s*$",
    r"^\s*GPG:\s*`?[^`]*`?\s*$",
    r"^\s*CONFIRM:\s*`?[^`]*`?\s*$",
    r"^\s*SEAL:\s*`?#ZHUGEXIN[^\n]*$",
    r">\s*\*\*GPG 指纹：\*\*\s*`?`?\s*",
    r">\s*\*\*GPG:\*\*\s*`?`?\s*",
    r">\s*\*\*CONFIRM:\*\*\s*`?`?\s*",
    r">\s*\*\*SEAL:\*\*\s*`?`?\s*",
]

def clean_text(text: str) -> str:
    """对任意文本应用脱敏规则"""
    for pattern, repl in REPLACEMENTS:
        text = re.sub(pattern, repl, text, flags=re.M)
    return text

def remove_empty_sensitive_lines(text: str) -> str:
    """移除空值的敏感字段行"""
    lines = text.split("\n")
    cleaned = []
    for line in lines:
        keep = True
        for pattern in LINE_REMOVALS:
            if re.match(pattern, line):
                keep = False
                break
        if keep:
            cleaned.append(line)
    return "\n".join(cleaned)

def extract_title(content: str) -> str:
    """从 Markdown 提取标题并脱敏"""
    m = re.search(r"^title:\s*(.+)$", content, re.M)
    if m:
        title = m.group(1).strip().strip('"').strip("'")
    else:
        m = re.search(r"^#\s+(.+)$", content, re.M)
        title = m.group(1).strip() if m else "龍魂系统文章"
    title = clean_text(title)
    title = re.sub(r"\s*[·/]\s*$", "", title)
    title = re.sub(r"^\s*[·/]\s*", "", title)
    return title.strip()

def extract_date(content: str) -> str:
    m = re.search(r"date:\s*(\d{4}-\d{2}-\d{2})", content)
    if m:
        return m.group(1)
    return "2026-07-04"

def extract_dna(content: str) -> str:
    m = re.search(r"#龍芯⚡️[^\s`]+-v[\d.]+", content)
    if m:
        dna = m.group(0)
        dna = re.sub(r"[-_]UID9622", "", dna, flags=re.I)
        dna = re.sub(r"UID9622[-_]", "", dna, flags=re.I)
        dna = re.sub(r"ZHUGEXIN", "", dna)
        return dna
    return ""

def clean_body(content: str) -> str:
    """清洗正文"""
    # 移除 YAML front matter
    content = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.S)
    # 移除第一个 # 标题
    content = re.sub(r"^#\s+.+\n", "", content, flags=re.M)
    # 移除 sovereignty 大声明块
    content = re.sub(r">\s*⛔\s*\*\*主权声明.*?\n(?=\n#|\n##|\Z)", "", content, flags=re.S)
    # 移除 ROOT_CARD（多种形态）
    content = re.sub(r"#?\s*ROOT_CARD\n```yaml\n.*?```", "", content, flags=re.S)
    content = re.sub(r"#?\s*ROOT_CARD\n[\s\S]*?(?=\n#|\n##|\Z)", "", content)
    # 移除版本日志
    content = re.sub(r"##\s*[八九十]+、版本日志.*?(?=\n##|\Z)", "", content, flags=re.S)
    # 移除标签与引用
    content = re.sub(r"##\s*[八九十]+、标签与引用.*?(?=\n##|\Z)", "", content, flags=re.S)
    # 移除文件路径行
    content = re.sub(r"\*\*文件路径:\*\*\s*`?[^`\n]+`?\n", "", content)
    # 移除作者中的 UID
    content = re.sub(r"\*\*作者:\*\*\s*UID9622\s*[·/]\s*", "**作者：**", content)
    # 移除原文顶部的 DNA/确认码/归属元信息块
    content = re.sub(r">\s*\*\*DNA 锚定[：:]\*\*\s*.*?\n", "", content, flags=re.S)
    content = re.sub(r">\s*\*\*源 DNA[：:]\*\*\s*.*?\n", "", content, flags=re.S)
    content = re.sub(r">\s*\*\*确认码[：:]\*\*\s*.*?\n", "", content, flags=re.S)
    content = re.sub(r">\s*\*\*归属[：:]\*\*\s*龍魂系统\s*[·/]\s*\n", "", content)
    content = re.sub(r">\s*\*\*归属[：:]\*\*\s*龍魂系统\s*[·/]\s*UID9622.*?\n", "", content, flags=re.I)
    content = re.sub(r">\s*\*\*性质[：:]\*\*\s*.*?\n", "", content)
    content = re.sub(r">\s*\*\*根基算法[：:]\*\*\s*.*?\n", "", content)
    # 清理被压缩到一行的顶部元信息块
    content = re.sub(r">\s*\*\*归档归属：\*\*.*?\n---\n", "", content, flags=re.S)
    # 清理空引用块
    content = re.sub(r">\s*\n", "", content)
    # 应用替换
    content = clean_text(content)
    # 清理表格中 "实名" 一行空值
    content = re.sub(r"\|\s*\*\*实名\*\*\s*\|\s*\|\n", "", content)
    content = re.sub(r"\|\s*实名\s*\|\s*\|\n", "", content)
    # 清理身份背景行（如果值被替换为占位符）
    content = re.sub(r"\|\s*\*\*身份背景\*\*\s*\|\s*\[个人背景\]\s*\|\n", "", content)
    # 清理 DNA 中的残留连字符
    content = re.sub(r"#龍芯⚡️([^\n`]+)--v", r"#龍芯⚡️\1-v", content)
    content = re.sub(r"#龍芯⚡️([^\n`]+)-`", r"#龍芯⚡️\1`", content)
    # 移除空敏感字段行
    content = remove_empty_sensitive_lines(content)
    # 清理连续分隔符
    content = re.sub(r"---\n---\n", "", content)
    content = re.sub(r"---\n\n---\n", "", content)
    # 清理开头和结尾的分隔符
    content = re.sub(r"^---\n", "", content)
    content = re.sub(r"\n---\s*$", "", content)
    # 清理 "龍芯北辰 ·  / Lucky" 这类残留
    content = re.sub(r"龍芯北辰\s*[·/]\s*\s*[·/]\s*Lucky", "龍芯北辰", content)
    content = re.sub(r"龍芯北辰\s*[·/]\s*Lucky", "龍芯北辰", content)
    # 清理 "让  的创作" 这类双空格（仅空格，不动换行）
    content = re.sub(r"让[ ]{2,}的", "让主理人的", content)
    content = re.sub(r"看清[ ]{2,}的", "看清主理人的", content)
    content = re.sub(r"对[ ]+船长", "对船长", content)
    content = re.sub(r"\|[ ]{2,}统一自启", "| 统一自启", content)
    content = re.sub(r"[ ]{3,}", "  ", content)
    # 清理多余空行
    content = re.sub(r"\n{3,}", "\n\n", content)
    return content.strip()

def first_sentence(text: str, max_len: int = 80) -> str:
    """取第一段第一句的前 max_len 字，不跨行合并"""
    # 去掉 Markdown 标记
    text = re.sub(r"[#*>`|\[\]\(\)\-]", "", text)
    # 按行拆分，取第一行有意义的文本（跳过表格、纯占位符、链接、HTML注释）
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines:
        if line.startswith("|"):
            continue
        if line.startswith("<!--"):
            continue
        if re.match(r"^\[.*\]\(.*\)$", line):
            continue
        if re.match(r"^(https?|ftp)://", line):
            continue
        if len(re.sub(r"\s", "", line)) < 5:
            continue
        text = line
        break
    else:
        return ""
    text = re.sub(r"\s+", "", text)
    if not text:
        return ""
    # 取第一句（到第一个句号/问号/感叹号/分号）
    puncts = [text.find(p) for p in ["。", "？", "！", "；"]]
    first_punct = min([p for p in puncts if p >= 0], default=len(text))
    if first_punct <= max_len and first_punct > 5:
        return text[:first_punct + 1]
    # 否则按长度截断
    if len(text) <= max_len:
        return text
    cut = text[:max_len]
    last_punct = max(cut.rfind("。"), cut.rfind("，"), cut.rfind("；"))
    if last_punct > max_len * 0.6:
        return cut[:last_punct + 1]
    return cut

def generate_wechat_version(src_path: Path) -> str:
    content = src_path.read_text(encoding="utf-8")
    title = extract_title(content)
    date = extract_date(content)
    dna = extract_dna(content)
    body = clean_body(content)

    # 生成导语
    abstract_match = re.search(r"(##?\s*摘要|导读|写在最前面|一句话定盘|一句话定义)\n(.*?)(?=\n---|\n##|\Z)", body, re.S)
    abstract = ""
    if abstract_match and abstract_match.group(2):
        section_text = abstract_match.group(2)
        # 如果是一句话定义/定盘，跳过公式本身，取后面的解释句
        if re.search(r"一句话定义|一句话定盘", abstract_match.group(1)):
            # 去掉公式本身，取后面的解释句
            section_lines = section_text.strip().split("\n")
            # 跳过第一行（公式），取剩余
            if len(section_lines) > 1:
                section_text = "\n".join(section_lines[1:])
        abstract = first_sentence(section_text)
    if not abstract:
        lines = [l for l in body.split("\n") if l.strip() and not l.startswith("#") and not l.startswith(">") and not l.startswith("<!--")]
        if lines:
            abstract = first_sentence("\n".join(lines))

    if abstract.startswith(title):
        abstract = abstract[len(title):].strip("，。、 ")

    output = f"""<!-- 龍魂系统 · 微信公众号发布版 -->
<!-- 来源：{src_path.name} -->
<!-- DNA: {dna or "#龍芯⚡️"} -->

# {title}

> **导语：** {abstract}...
>
> **作者：** 龍魂系统主理人
> **日期：** {date}
> **来源：** 龍魂系统

---

{body}

---

## 🛡️ 版权声眀

> **(C) 2026 龍魂系统 · 版权所有**
>
> 1. 本文全部知识产权归属于创作者，任何机构与个人未经授权不得用于商业 AI 训练、数据蒸馏或模型微调。
> 2. 允许在保留原文 DNA、作者署名、本声明完整的前提下进行非商业转载与引用。
> 3. 禁止删除 DNA 追溯码、篡改主权声明、用于境外平台模型训练、用于水军/煽动/造谣。
> 4. 本文技术内容遵循中国法律法规，服务于人民利益与国家数字主权。
>
> **违反上述条款即视为侵犯数字主权，龍魂审计系统保留追溯权利。**

---

**{dna or "#龍芯⚡️"}**

**龍魂系统 —— 中国人的数字主权，代码里的精神根脉。**
*数据主权归于人民 · 技术为人民服务 · 祖国优先*
"""

    # 最终后处理
    output = clean_text(output)
    output = remove_empty_sensitive_lines(output)
    output = re.sub(r"\n---\n---\n", "\n---\n", output)
    output = re.sub(r"\n---\n\n---\n", "\n---\n", output)
    output = re.sub(r"龍芯北辰\s*[·/]\s*\s*[·/]\s*Lucky", "龍芯北辰", output)
    output = re.sub(r"龍芯北辰\s*[·/]\s*Lucky", "龍芯北辰", output)
    output = re.sub(r"让[ ]{2,}的", "让主理人的", output)
    output = re.sub(r"看清[ ]{2,}的", "看清主理人的", output)
    output = re.sub(r"对[ ]+船长", "对船长", output)
    output = re.sub(r"\|[ ]{2,}统一自启", "| 统一自启", output)
    output = re.sub(r"[ ]{3,}", "  ", output)
    output = re.sub(r"\n{3,}", "\n\n", output)
    return output.strip()

def main():
    count = 0
    for src in sorted(SRC_DIR.glob("*.md")):
        if "template" in src.name.lower():
            continue
        out_name = src.stem + "-微信公众号版.md"
        out_path = OUT_DIR / out_name
        try:
            wechat_content = generate_wechat_version(src)
            out_path.write_text(wechat_content, encoding="utf-8")
            print(f"✅ {out_name}")
            count += 1
        except Exception as e:
            print(f"❌ {src.name}: {e}")
    print(f"\n共生成 {count} 篇微信公众号发布版，输出目录：{OUT_DIR}")

if __name__ == "__main__":
    main()
