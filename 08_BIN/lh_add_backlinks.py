#!/usr/bin/env python3
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
# DNA: #龍芯⚡️丙午·丙酉·壬戌·戌时·䷬萃-ADD_BACKLINKS-UID9622-9E993EC1
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""给12份面试题库添加Notion反向链接"""
import os

BANKS_DIR = "/Users/zuimeidedeyihan/_work/interview-question-banks"

notion_urls = {
    "csharp": "https://www.notion.so/uid9622/3b57125a9c9f81069b25d55f78ce3e17",
    "go": "https://www.notion.so/uid9622/3b57125a9c9f81b28da0fbd18f576a96",
    "java": "https://www.notion.so/uid9622/3b57125a9c9f81719ea4f7b7bd00bde9",
    "js": "https://www.notion.so/uid9622/3b57125a9c9f817fb989c8df180d087d",
    "kotlin": "https://www.notion.so/uid9622/3b57125a9c9f81868217cbfbaabb9bc1",
    "php": "https://www.notion.so/uid9622/3b57125a9c9f81829ea1e681f3412b1d",
    "ruby": "https://www.notion.so/uid9622/3b57125a9c9f81c58a7afcfb673862d1",
    "rust": "https://www.notion.so/uid9622/3b57125a9c9f81cab250ece5c09b8b22",
    "shell": "https://www.notion.so/uid9622/3b57125a9c9f81ffb6bae984d71ed562",
    "sql": "https://www.notion.so/uid9622/3b57125a9c9f814694bde7b5315a9fd8",
    "swift": "https://www.notion.so/uid9622/3b57125a9c9f81678d73ee3d809d4923",
    "ts": "https://www.notion.so/uid9622/3b57125a9c9f81ec8e9ae0cdc3ef2a61",
}

for fname in sorted(os.listdir(BANKS_DIR)):
    if not fname.endswith(".md"):
        continue
    code = fname.split("-")[0]
    url = notion_urls.get(code)
    if not url:
        print(f"  ⚠️  {fname}: no URL found")
        continue
    
    fpath = os.path.join(BANKS_DIR, fname)
    with open(fpath, encoding="utf-8") as f:
        content = f.read()
    
    backlink = f"> 📓 **Notion 镜像**: [{url}]({url})\n> 📺 **CSDN 博客**: [uid9622-01.blog.csdn.net](https://uid9622-01.blog.csdn.net)\n> 📦 **GitHub 仓库**: [UID9622/longhun-system](https://github.com/UID9622/longhun-system)\n"
    
    # Insert after the "> 分层许可" line (which is the last metadata line before content)
    if "> 分层许可" in content:
        lines = content.split("\n")
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if "> 分层许可" in line and i < len(lines) - 1:
                # Add backlink after this line if next line is blank or "---"
                new_lines.append("")
                new_lines.append(backlink.rstrip())
        content = "\n".join(new_lines)
    elif "📓 **Notion 镜像**" not in content:
        # Fallback: add after the GPG line
        lines = content.split("\n")
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.startswith("> GPG:") and "📓" not in content:
                new_lines.append("")
                new_lines.append(backlink.rstrip())
                break
        content = "\n".join(new_lines)
    
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"  ✅ {fname}")

print("\n🎉 反向链接已添加到12份题库文件")
