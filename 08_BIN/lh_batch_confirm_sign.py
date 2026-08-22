#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
#龍芯⚡️丙午·乙未·甲寅·申时·䷆师-BATCH-CONFIRM-SIGN-v1.0
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂批量CONFIRM签名工具 v1.0
为缺少 #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z 签名的文件批量添加签名头
DNA: #龍芯⚡️丙午·乙未·甲寅·申时·䷆师-BATCH-CONFIRM-SIGN-v1.0
"""
import sys
from pathlib import Path

CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
ROOT = Path("/Users/zuimeidedeyihan/longhun-system")

# 文件列表及其简短描述
FILES = {
    # === 01_protocols 核心协议 ===
    "01_protocols/龍魂认知上下文管理协议_v3.0.md": "龍魂认知上下文管理协议",
    "01_protocols/龍魂系統輸入過濾與預處理協議_v3.0.md": "龍魂系统输入过滤与预处理协议",
    "01_protocols/龍魂八卦决策调度协议_v1.0.md": "龍魂八卦决策调度协议",
    "01_protocols/测试庄园规范_v1.0.md": "测试庄园规范",
    "01_protocols/LH-GOV-GRASSROOTS-REALITY-PROTOCOL-FULL-v1.0.md": "基层现实协议完整版",
    "01_protocols/LH-GOV-GRASSROOTS-REALITY-PROTOCOL-v1.0.md": "基层现实协议",
    "01_protocols/龍魂系统输入过滤与预处理协议_v2.0_审计报告.md": "输入过滤协议审计报告",

    # === 01_protocols THESIS 论文章节 ===
    "01_protocols/THESIS-ROOT-GOVERNANCE/00-THESIS-OUTLINE.md": "根治理论文大纲",
    "01_protocols/THESIS-ROOT-GOVERNANCE/01-PREFACE.md": "论文前言",
    "01_protocols/THESIS-ROOT-GOVERNANCE/02-CHAPTER-01.md": "论文第01章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/03-CHAPTER-02.md": "论文第02章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/04-CHAPTER-03.md": "论文第03章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/05-CHAPTER-04.md": "论文第04章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/06-CHAPTER-05.md": "论文第05章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/07-CHAPTER-06.md": "论文第06章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/08-CHAPTER-07.md": "论文第07章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/09-CHAPTER-08.md": "论文第08章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/10-CHAPTER-09.md": "论文第09章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/11-CHAPTER-10.md": "论文第10章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/12-CHAPTER-11.md": "论文第11章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/13-CHAPTER-12.md": "论文第12章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/14-CHAPTER-13.md": "论文第13章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/15-CHAPTER-14.md": "论文第14章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/16-CHAPTER-15.md": "论文第15章",
    "01_protocols/THESIS-ROOT-GOVERNANCE/README.md": "论文README",
    "01_protocols/THESIS-ROOT-GOVERNANCE/FULL-THESIS.md": "论文全文",

    # === 01_技能庫 核心技能 ===
    "02_SKILLS/veto-alert.md": "一票否决·高危拦截",
    "02_SKILLS/emotion-absorber.md": "情绪海绵·反操控",
    "02_SKILLS/fuse-appeal.md": "熔断申诉·人工审计",
    "02_SKILLS/semantic-parser.md": "语义解析·中英双轨",
    "02_SKILLS/route-find.md": "路由查找·总线查询",
    "02_SKILLS/decision-card.md": "决策来源卡·全透明",
    "02_SKILLS/error-translator.md": "错误翻译器",
    "02_SKILLS/water-army-detect.md": "水军检测",
    "02_SKILLS/sovereign-privacy.md": "主权隐私",
    "02_SKILLS/plist-validator.md": "plist验证器",
    "02_SKILLS/skill-extension.md": "技能扩展",
    "02_SKILLS/audit-plugin.md": "审计插件",
    "02_SKILLS/wuxing-guard.md": "五行守护",
    "02_SKILLS/bagua-router.md": "八卦路由",

    # === 01_技能庫 曾师训练数据 ===
    "02_SKILLS/longhun-zeng-digital-human/knowledge_base/INDEX.md": "曾师知识库索引",
}

SINGLE_LINE_INSERT = {
    # 这些是纯行式文件，在第1行前插入即可
    "01_protocols/THESIS-ROOT-GOVERNANCE/README.md",
    "01_protocols/THESIS-ROOT-GOVERNANCE/FULL-THESIS.md",
}


def get_header(filename, desc):
    """生成标准CONFIRM签名头"""
    return f"> {CONFIRM}\n> 📄 {desc} | 龍魂系统 · 源头已验证\n"


def sign_file(filepath, header):
    """在文件顶部添加CONFIRM签名"""
    content = filepath.read_text(encoding='utf-8')
    
    if CONFIRM in content:
        return "skip"
    
    # 跳过已有 # 标题的文件开头，把签名插在标题之后
    lines = content.split('\n')
    insert_at = 0
    
    if lines and lines[0].startswith('#'):
        # 如果是markdown标题，插在标题块之后
        insert_at = 1
        while insert_at < len(lines) and (lines[insert_at].strip() == '' or lines[insert_at].startswith('>')):
            insert_at += 1
    
    new_lines = lines[:insert_at] + [header.rstrip(), ''] + lines[insert_at:]
    filepath.write_text('\n'.join(new_lines), encoding='utf-8')
    return "signed"


def main():
    signed = 0
    skipped = 0
    errors = 0
    
    for rel_path, desc in FILES.items():
        filepath = ROOT / rel_path
        if not filepath.exists():
            print(f'⚠️  不存在: {rel_path}')
            errors += 1
            continue
        
        # 检查是否已有CONFIRM（以防重复）
        content = filepath.read_text(encoding='utf-8')
        if CONFIRM in content:
            print(f'⏭️  跳过 (已有签名): {rel_path}')
            skipped += 1
            continue
        
        header = get_header(rel_path, desc)
        result = sign_file(filepath, header)
        
        if result == "signed":
            print(f'✅ 已签名: {rel_path}')
            signed += 1
        else:
            print(f'⏭️  {result}: {rel_path}')
            skipped += 1
    
    print(f'\n{"="*50}')
    print(f'📊 签名完成: ✅{signed}  ⏭️{skipped}  ⚠️{errors}')
    
    return 0 if errors == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
