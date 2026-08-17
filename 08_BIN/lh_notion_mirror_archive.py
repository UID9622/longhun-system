#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
龍魂·Notion镜像归档工具 v1.0
从 12_DOCS/notion_mirror/pages/ 提取结构化内容，按11大类归入项目目录。
DNA: #龍芯⚡️2026-08-07-NOTION-MIRROR-ARCHIVE-v1.0-a7f3b2c1
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
"""

import os
import re
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MIRROR_PAGES = PROJECT_ROOT / "12_DOCS" / "notion_mirror" / "pages"
OUTPUT_REPORT = PROJECT_ROOT / "12_DOCS" / "notion_mirror" / "archive_report.json"
ARCHIVE_DIR = PROJECT_ROOT / "12_DOCS" / "notion_archive_2026-08-07"

# 11大类 → 目标目录映射
CATEGORY_MAP = {
    "宪法与治理层": "01_protocols",
    "大脑与智能路由": "04_ENGINES",
    "DNA与身份架构": "01_protocols",
    "安全与认证": "01_protocols",
    "CNSH与工程实现": "03_compiler",
    "审计与质量保障": "07_AUDIT",
    "知识与学习体系": "03_KNOWLEDGE_GRAPH",
    "通心译与人机交互": "engines",
    "治理与组织": "governance",
    "哲学与数学基础": "03_KNOWLEDGE_GRAPH",
    "协作与未来": "02_執行記錄",
}

# 页面映射（从INDEX.md手工提取）
PAGES = [
    # 1.1 宪法与治理层
    ("宪法与治理层", "8ad36909a4504f0aae24cbaea3c4ea9f.md", "龍魂系统宪法 v1.0", "P0"),
    ("宪法与治理层", "3337125a9c9f8187875eda5b6aa1d7f0.md", "一票否决权×阴阳调和 v1.0", "P0"),
    ("宪法与治理层", "dd9eabae98ec48a7ba583b79aa14f8dc.md", "老大初心宣言·灵魂档案归集 v1.0", "P0"),
    ("宪法与治理层", "2743f5deed0a48b4980b1154a766ba3a.md", "德者永生殿·路由回流协议 v2.0", "P0"),
    ("宪法与治理层", "19a8289545b74cae8b3b873c0e4bce68.md", "动态AI协议入口", "P0"),
    ("宪法与治理层", "a267c3af2ba74da2a379a18572656cf1.md", "全球文化主权与维权宪法 v2.0", "P0"),
    ("宪法与治理层", "c60d629444c94656b2b2ea968a6c72af.md", "北辰协议·原文存档（L0-012）", "P0"),

    # 1.2 大脑与智能路由
    ("大脑与智能路由", "072c483a21b6437f9326b722636af935.md", "智能体大脑集成手册 v1.0", "P0"),
    ("大脑与智能路由", "0d0af05b0b95484182a344f25eaeedc2.md", "沉浸式复交启动页 v1.0", "P0"),
    ("大脑与智能路由", "4566044476014326803e907f7a926ab2.md", "AI自动路由系统", "L3"),
    ("大脑与智能路由", "bec1e986ff4c427999dcc9943b2b0d87.md", "龍魂自动路由系统·宝宝智能管家", "L3"),
    ("大脑与智能路由", "b53160a0479947a98c002179fc1dc298.md", "龍魂记忆中枢·DNA永生记忆", "L2"),

    # 1.3 DNA与身份架构
    ("DNA与身份架构", "1dd88844789e4185a0efbb43017f3e74.md", "DNA時間軸L5分層架構 v1.4", "P0"),
    ("DNA与身份架构", "a07533b376b94bdabab391541216f2bb.md", "統一DNA變量對照表 v1.0（已封存）", "P0"),
    ("DNA与身份架构", "77106ff9282f4db6b3ffb65f83f97c21.md", "DNA時間軸L5分層架構白皮書 v2.1", "P0"),
    ("DNA与身份架构", "c10baabe55694bbcb0f4e5d5377c634e.md", "DNA分层安全设计 v4.0", "L1"),
    ("DNA与身份架构", "c167bf3709414ddfb50df5af4687e0e0.md", "【P0永恒级】数据来源追溯规范", "P0"),

    # 1.4 安全与认证
    ("安全与认证", "2b525f18ec4f4e78a68edb3cac47b899.md", "龍魂数据安全架构", "L1"),
    ("安全与认证", "6c1025697a9e40bc92e52d414500108c.md", "智能身份认证系统 v1.0", "L1"),
    ("安全与认证", "f894aca6671348ad8ca5c0c9a186f495.md", "CNSH代码变量隔离系统", "L2"),
    ("安全与认证", "141f146e598a4bdcb3cb7dcb8e673560.md", "Service DNA 接入规范 v0.2", "L2"),

    # 1.5 CNSH与工程实现
    ("CNSH与工程实现", "1543ceabbcb747d09bcaddd7fcb9d845.md", "CNSH × 龍魂系统·MVP v2.0", "P0"),
    ("CNSH与工程实现", "142168c7f03942e696e8c499d2914e47.md", "龍芯家族花名册·设备主人主权铁律 v1.0", "P0"),
    ("CNSH与工程实现", "16399c8440fa4d1aad5cad3aa8cb5ffe.md", "CNSH工具集本地网页模板", "L3"),
    ("CNSH与工程实现", "ca83c2fd3cd94adabe10159417f2ec67.md", "数字甲骨文字元立碑工程·总系统 v1.0", "P0"),
    ("CNSH与工程实现", "3187125a9c9f80a68158d9064f591f26.md", "CNSH × 北辰协议 IEEE白皮书 v1.1", "P0"),
    ("CNSH与工程实现", "e3d22f7e5d854dbf8c138e72274afd23.md", "开源文件模板系统·CNSH-Editor v1.0", "L3"),

    # 1.6 审计与质量保障
    ("审计与质量保障", "2fef05eeb41a4e0e9beff239289678b8.md", "三色审计·AI回复真实性验证协议 v1.0", "L1"),
    ("审计与质量保障", "de14987164d7414d95d6add1138f8492.md", "三色审计前置评估机制", "L1"),
    ("审计与质量保障", "e0d66f81b4de49698497e349c328d883.md", "宪法合规审计报告", "L1"),
    ("审计与质量保障", "3297125a9c9f81329819fb69b3dc907e.md", "审计日报 2026-03-20", "L3"),
    ("审计与质量保障", "e6e50ba19da645ac9f95d83c39e8bc34.md", "龍魂系统发布验收完整方案", "L2"),

    # 1.7 知识与学习体系
    ("知识与学习体系", "c2df953f773545308593bc65aa3c14ed.md", "龍魂知识库·论文&白皮书总部 v1.0", "L1"),
    ("知识与学习体系", "4419a93e11174045a9fc0ac0b3f7e4a5.md", "AI算法史·NodeCard时间轴 1943-2025 v1.0", "L2"),
    ("知识与学习体系", "fdb1b46b581a4c159d6842bd03e909a8.md", "CSDN占稿·双账号单向架构", "L3"),
    ("知识与学习体系", "837a3b763b7541ab8f681defe3ac7362.md", "北辰协议｜原文存档（L2-021+L1-031）", "P0"),
    ("知识与学习体系", "c4a8ebb5e4db4773a38cee76f04185d5.md", "龍魂系统执行日志 2026-03-13", "L3"),

    # 1.8 通心译与人机交互
    ("通心译与人机交互", "f0f1844b8ae548e485ebdbd4ac4051a1.md", "通心译执行手册 v1.0", "L1"),
    ("通心译与人机交互", "346e0c1babd6475baabb09654fb1efe0.md", "Notion AI龍魂代理宝宝系统 v1.2", "L2"),
    ("通心译与人机交互", "3c8bf63e3d3b49dc84d01407ceeaa3d2.md", "龍魂·Notion API 全景文档", "L3"),

    # 1.9 治理与组织
    ("治理与组织", "84daa1d2030447318ade20e12b1fdb36.md", "龍魂七維AI治理×數字主權執行表 v1.0", "P0"),
    ("治理与组织", "1f9a58996f82415ca02e567c7cd16363.md", "龍魂·世界入口论文", "P0"),
    ("治理与组织", "2e67125a9c9f80eb8b9ff857bea1846a.md", "主控仪表盘（L0）", "L0"),
    ("治理与组织", "a3ca7dc0068c42b2ba23cdbb7dd45361.md", "关键词归集索引", "L3"),

    # 1.10 哲学与数学基础
    ("哲学与数学基础", "数字根_洛书369.md", "数字根·洛书369", "L0"),
    ("哲学与数学基础", "CNSH三才校验公式.md", "CNSH三才校验公式", "L0"),
    ("哲学与数学基础", "CNSH原点能量场公式.md", "CNSH原点能量场公式", "L0"),
    ("哲学与数学基础", "CNSH路由公式.md", "CNSH路由公式", "L1"),
    ("哲学与数学基础", "五行生克算法_WuXing.md", "五行生克算法", "L1"),
    ("哲学与数学基础", "三才向量合成_Sancai_Vector.md", "三才向量合成", "L1"),
    ("哲学与数学基础", "64卦维度_64Gua.md", "64卦维度", "L1"),
    ("哲学与数学基础", "八卦维度_Bagua.md", "八卦维度", "L1"),
    ("哲学与数学基础", "天干地支维度_StemsBranches.md", "天干地支维度", "L1"),
    ("哲学与数学基础", "河洛图维度_Hetu_Luoshu.md", "河洛图维度", "L1"),
    ("哲学与数学基础", "信息论_Information_Theory.md", "信息论", "L2"),
    ("哲学与数学基础", "傅里叶变换_Fourier.md", "傅里叶变换", "L2"),
    ("哲学与数学基础", "采样定理_Nyquist.md", "采样定理", "L2"),
    ("哲学与数学基础", "自动微分_Automatic_Differentiation.md", "自动微分", "L2"),
    ("哲学与数学基础", "数值方法_Numerical_Methods.md", "数值方法", "L2"),
    ("哲学与数学基础", "渲染几何_Geometry_Rendering.md", "渲染几何", "L2"),
    ("哲学与数学基础", "量子计算抽象层_Quantum_Abstract.md", "量子计算抽象层", "L2"),
    ("哲学与数学基础", "通心译翻译引擎_总纲.md", "通心译翻译引擎·总纲", "L1"),

    # 1.11 协作与未来
    ("协作与未来", "dabb25dd74594ecb8de94457be6e1b68.md", "自动化对话档案系统", "L3"),
    ("协作与未来", "3664bb869a0841478008c6c111b9289d.md", "曾老师智慧算法·量子力学重构", "L2"),
    ("协作与未来", "34f7125a9c9f80b9951cee661375dd09.md", "待办", "L3"),
]


def safe_filename(title: str) -> str:
    """生成合法文件名"""
    # 取中文/英文/数字，去掉特殊符号
    safe = re.sub(r'[^\w\u4e00-\u9fff·×\-\|]', '_', title)
    safe = re.sub(r'_+', '_', safe)
    return safe[:80] + ".md"


def check_dna_header(content: str) -> bool:
    """检查是否有DNA头"""
    return bool(re.search(r'DNA:\s*#龍芯', content)) or bool(re.search(r'DNA:\s*#龍芯', content))


def add_dna_header(content: str, title: str, level: str) -> str:
    """为内容添加DNA头"""
    now = datetime.now().strftime("%Y-%m-%d")
    short_hash = hashlib.sha256(content.encode()).hexdigest()[:8]
    header = f"""DNA: #龍芯⚡️{now}-NOTION-ARCHIVE-{level}-{short_hash}
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
来源: Notion镜像归档
标题: {title}

---
"""
    if check_dna_header(content):
        return content
    # 移除原有title（如果第一行是#标题），插入DNA头
    lines = content.strip().split("\n")
    # 跳过已有的空白和标题行
    start = 0
    while start < len(lines) and (
        not lines[start].strip()
        or lines[start].strip().startswith("# ")
        or lines[start].strip().startswith("DNA:")
        or lines[start].strip().startswith("创建者:")
        or lines[start].strip().startswith("协议:")
        or lines[start].strip().startswith("#CONFIRM")
    ):
        start += 1
    body = "\n".join(lines[start:]) if start < len(lines) else ""
    return header + body


def main():
    report = {
        "timestamp": datetime.now().isoformat(),
        "total_pages": len(PAGES),
        "archived": 0,
        "skipped_missing": 0,
        "skipped_exists": 0,
        "details": [],
        "by_category": {},
    }

    # 创建归档目录
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    for category, src_file, title, level in PAGES:
        src_path = MIRROR_PAGES / src_file
        target_dir = PROJECT_ROOT / CATEGORY_MAP.get(category, "12_DOCS")
        target_file = safe_filename(title)
        target_path = target_dir / target_file

        entry = {
            "category": category,
            "src": str(src_path.relative_to(PROJECT_ROOT)),
            "title": title,
            "level": level,
            "status": "",
            "target": str(target_path.relative_to(PROJECT_ROOT)),
            "size_bytes": 0,
        }

        if category not in report["by_category"]:
            report["by_category"][category] = {"total": 0, "archived": 0, "skipped": 0}

        report["by_category"][category]["total"] += 1

        # 1. 检查源文件是否存在
        if not src_path.exists():
            entry["status"] = "MISSING_SOURCE"
            report["skipped_missing"] += 1
            report["by_category"][category]["skipped"] += 1
            report["details"].append(entry)
            print(f"  ❌ 缺失: {src_file} ({title})")
            continue

        entry["size_bytes"] = src_path.stat().st_size
        content = src_path.read_text(encoding="utf-8", errors="replace")

        # 2. 检查是否已有DNA头
        has_dna = check_dna_header(content)

        # 3. 写入目标（命名唯一化）
        # 若目标已有同名文件，追加层级标识
        if target_path.exists():
            base = safe_filename(title).replace(".md", "")
            target_file = f"{base}_{level}.md"
            target_path = target_dir / target_file
            entry["target"] = str(target_path.relative_to(PROJECT_ROOT))

        target_dir.mkdir(parents=True, exist_ok=True)

        # 补DNA头
        if not has_dna:
            content = add_dna_header(content, title, level)

        target_path.write_text(content, encoding="utf-8")
        entry["status"] = "ARCHIVED"
        entry["had_dna"] = has_dna
        report["archived"] += 1
        report["by_category"][category]["archived"] += 1

        # 同时复制到归档目录（按分类存放）
        archive_cat_dir = ARCHIVE_DIR / category
        archive_cat_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(str(target_path), str(archive_cat_dir / target_file))

        report["details"].append(entry)
        dna_tag = "🟢" if has_dna else "🟡+DNA"
        print(f"  {dna_tag} [{level}] {category} → {title}")

    # 输出报告
    OUTPUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_REPORT, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print("\n" + "=" * 60)
    print(f"📊 归档完成")
    print(f"   总计: {report['total_pages']} 页")
    print(f"   ✅ 已归档: {report['archived']}")
    print(f"   ❌ 源缺失: {report['skipped_missing']}")
    print(f"   ⏭️ 已存在跳过: {report['skipped_exists']}")
    print(f"\n📂 按分类:")
    for cat, stats in sorted(report["by_category"].items()):
        bar = "▓" * stats["archived"] + "░" * (stats["total"] - stats["archived"])
        print(f"   {bar} {cat}: {stats['archived']}/{stats['total']}")
    print(f"\n📄 报告: {OUTPUT_REPORT}")
    print(f"📁 归档目录: {ARCHIVE_DIR}")


if __name__ == "__main__":
    main()
