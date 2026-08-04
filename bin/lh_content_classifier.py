#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
"""
龍魂·内容自动分类吸收引擎 v1.0
DNA: #龍芯⚡️丙午·乙巳·癸酉·亥时·☰乾-CONTENT-CLASSIFIER-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0

用途: 用户贴任何内容 → 自动分类 → 找目标目录 → 查重 → 合并/新建 → 签名落档
原则: 不做加法·优先合并·不新建不必要文件
"""
import os, re, sys, hashlib, json, argparse
from datetime import datetime
from pathlib import Path

# ── 项目根 ──
ROOT = Path(__file__).resolve().parent.parent

# ── 12分类·目录映射·关键词 ──
CATEGORIES = {
    "protocol": {
        "dir": "01_protocols",
        "label": "协议/规范",
        "keywords": ["协议", "规范", "规则", "标准", "protocol", "规约", "宪法", "constitution",
                      "天条", "授权", "审计", "熔断", "隐私", "算法审计", "战后整顿",
                      "CC BY-NC-SA", "license", "条款", "适用范围", "原则",
                      "不可", "必须", "禁止", "数据主权", "知识共享"],
        "headers": ["# 协议", "# 规范", "协议名称", "适用范围", "# 龍魂"],
        "ext": ".md"
    },
    "code_engine": {
        "dir": "engines",
        "label": "引擎代码",
        "keywords": ["引擎", "engine", "引擎层", "推演", "审计引擎", "分类器",
                      "class Engine", "class.*Engine", "推理引擎", "inference"],
        "headers": ["引擎", "Engine"],
        "ext": ".py"
    },
    "code_tool": {
        "dir": "bin",
        "label": "工具脚本",
        "keywords": ["import argparse", "if __name__", "#!/usr/bin", "CLI", "命令行",
                      "工具", "脚本", "script", "lh_", ".py", "def main"],
        "headers": ["#!/usr/bin/env python", "命令行工具"],
        "ext": ".py"
    },
    "paper": {
        "dir": "papers",
        "label": "论文/学术",
        "keywords": ["abstract", "introduction", "methodology", "conclusion", "references",
                      "论文", "学术", "研究", "证明", "定理", "theorem", "doi",
                      "arXiv", "chinaXiv", "期刊", "发表"],
        "headers": ["# Abstract", "# 摘要", "## Introduction", "## 引言"],
        "ext": ".md"
    },
    "training_data": {
        "dir": "data",
        "label": "训练数据",
        "keywords": ["训练数据", "training", "train.jsonl", "valid.jsonl", "QA对",
                      "instruction", "output", "prompt", "completion", "jsonl",
                      "训练集", "验证集", "语料"],
        "headers": [],
        "ext": ".jsonl"
    },
    "config": {
        "dir": "config",
        "label": "配置文件",
        "keywords": ["配置", "config", ".ini", ".yaml", ".toml", ".env",
                      "端口", "port", "host", "database", "nginx"],
        "headers": [],
        "ext": ".yaml"
    },
    "deploy": {
        "dir": "deploy",
        "label": "部署/运维",
        "keywords": ["部署", "deploy", "docker", "systemd", "nginx", "ssh",
                      "鲲鹏", "119.13.90.27", "health_check", "monitor",
                      "#!/bin/bash", "#!/bin/sh"],
        "headers": [],
        "ext": ".sh"
    },
    "documentation": {
        "dir": "docs",
        "label": "文档",
        "keywords": ["文档", "documentation", "使用说明", "教程", "API参考",
                      "README", "入门", "速查"],
        "headers": ["# 文档", "# README"],
        "ext": ".md"
    },
    "portal": {
        "dir": "portal",
        "label": "前端/Web",
        "keywords": ["<!DOCTYPE html>", "<html", "<script", "<style", "CSS",
                      "React", "Vue", "前端", "页面", "面板", "dashboard",
                      "index.html"],
        "headers": ["<!DOCTYPE html>"],
        "ext": ".html"
    },
    "creative": {
        "dir": "articles",
        "label": "文章/创意",
        "keywords": ["文章", "博客", "blog", "CSDN", "创意", "随笔", "思考",
                      "故事", "案例"],
        "headers": ["# ", "## "],
        "ext": ".md"
    },
    "persona_def": {
        "dir": "personas",
        "label": "人格定义",
        "keywords": ["人格", "persona", "Persona", "IPA编号", "P0", "P0[0-9]",
                      "职能", "路由", "触发词", "熔断"],
        "headers": ["# P0", "# 人格定义"],
        "ext": ".md"
    },
    "skill_def": {
        "dir": "01_技能庫",
        "label": "技能定义",
        "keywords": ["技能", "skill", "触发", "能力", "capability",
                      "MCP", "工具定义"],
        "headers": ["# 技能", "# Skill"],
        "ext": ".md"
    },
}


def extract_features(content: str) -> dict:
    """提取内容特征"""
    features = {
        "lines": len(content.splitlines()),
        "size": len(content),
        "has_code": bool(re.search(r'(def |class |import |function |#!/usr/bin|if __name__)', content)),
        "has_python": bool(re.search(r'(def |class |import |\.py)', content)),
        "has_shell": bool(re.search(r'(#!/bin/(ba)?sh|\bchmod\b|\bsystemctl\b|\bdocker\b)', content)),
        "has_html": bool(re.search(r'(<!DOCTYPE|<html|<script|<style)', content)),
        "has_jsonl": bool(re.search(r'^\{"messages":', content, re.MULTILINE)),
        "has_chinese": bool(re.search(r'[\u4e00-\u9fff]', content)),
        "has_english": bool(re.search(r'[a-zA-Z]{20,}', content)),
        "has_math": bool(re.search(r'(\$.*\$|\\begin\{|\\frac|\\sum|\\int)', content)),
        "first_line": content.split('\n')[0].strip() if content.strip() else "",
        "headers": re.findall(r'^(#{1,3}\s+.+)$', content, re.MULTILINE),
    }
    return features


def classify(content: str) -> tuple:
    """分类内容 → (分类ID, 分类信息, 置信度)"""
    features = extract_features(content)
    scores = {}

    for cat_id, cat_info in CATEGORIES.items():
        score = 0.0

        # 关键词匹配 (权重 40%)
        kw_matches = sum(1 for kw in cat_info["keywords"]
                        if re.search(kw, content, re.IGNORECASE))
        if cat_info["keywords"]:
            score += (kw_matches / max(len(cat_info["keywords"]), 1)) * 0.4

        # 头部匹配 (权重 30%)
        if cat_info["headers"]:
            h_matches = sum(1 for h in cat_info["headers"]
                          if any(h.lower() in line.lower() for line in features["headers"]))
            score += (h_matches / max(len(cat_info["headers"]), 1)) * 0.3

        # 结构特征匹配 (权重 30%)
        if cat_id == "code_engine" and features["has_python"] and "引擎" in content:
            score += 0.3
        elif cat_id == "code_tool" and features["has_python"] and features["lines"] < 500:
            score += 0.2
        elif cat_id == "paper" and features["has_english"] and features["has_math"]:
            score += 0.2
        elif cat_id == "paper" and features["lines"] > 300:
            score += 0.15
        elif cat_id == "training_data" and features["has_jsonl"]:
            score += 0.3
        elif cat_id == "portal" and features["has_html"]:
            score += 0.25
        elif cat_id == "deploy" and features["has_shell"]:
            score += 0.25
        elif cat_id == "config" and (".yaml" in content[:200] or ".toml" in content[:200]):
            score += 0.25
        elif cat_id == "protocol" and features["has_chinese"]:
            # 中文+结构化标题 = 大概率协议
            结构化标题 = re.findall(r'^#{1,3}\s+(?:协议|原则|定义|适用|条款|规范|规则|标准)', content, re.MULTILINE)
            if 结构化标题:
                score += 0.3
            # 包含"不可""必须""禁止"等规范用语
            if re.search(r'(不可|必须|禁止|不得|应.*当|有权)', content):
                score += 0.15

        scores[cat_id] = min(score, 1.0)

    # 取最高分
    best_id = max(scores, key=scores.get)
    best_score = scores[best_id]

    # 如果最高分太低，回退到 documentation
    if best_score < 0.15:
        best_id = "documentation"
        best_score = 0.15

    return best_id, CATEGORIES[best_id], best_score


def suggest_filename(content: str, category_id: str, category_info: dict) -> str:
    """根据内容生成建议文件名"""
    # 提取标题
    title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if title_match:
        title = title_match.group(1).strip()
        # 清理文件名：去特殊字符，保留中英文数字连字符
        title = re.sub(r'[^\w\u4e00-\u9fff\-]', '-', title)
        title = re.sub(r'-{2,}', '-', title).strip('-')
        title = title[:80]  # 限制长度
        return f"LH-{title}{category_info['ext']}"

    # 从内容生成摘要
    clean = content.strip()[:100]
    hash8 = hashlib.sha256(clean.encode()).hexdigest()[:8]
    # 用分类ID而非label做文件名（避免label里的特殊字符）
    return f"LH-{category_id}-{hash8}{category_info['ext']}"


def find_similar(target_dir: str, content: str) -> list:
    """在目标目录查找相似文件"""
    similar = []
    target_path = ROOT / target_dir
    if not target_path.exists():
        return similar

    # 简单的内容哈希指纹
    content_fingerprint = hashlib.sha256(content[:500].encode()).hexdigest()[:16]

    for f in target_path.rglob("*"):
        if f.is_file() and f.suffix in ['.md', '.py', '.jsonl', '.html', '.sh', '.yaml', '.toml']:
            try:
                existing = f.read_text(encoding='utf-8')[:500]
                existing_fp = hashlib.sha256(existing.encode()).hexdigest()[:16]
                # 简单去重：标题相似
                title_new = re.findall(r'^#\s+(.+)$', content, re.MULTILINE)
                title_existing = re.findall(r'^#\s+(.+)$', existing, re.MULTILINE)
                if title_new and title_existing:
                    # 用集合相似度
                    words_new = set(title_new[0].lower().split())
                    words_existing = set(title_existing[0].lower().split())
                    if words_new and words_existing:
                        overlap = len(words_new & words_existing) / max(len(words_new | words_existing), 1)
                        if overlap > 0.5:
                            similar.append({
                                "path": str(f.relative_to(ROOT)),
                                "title": title_existing[0],
                                "similarity": round(overlap, 2)
                            })
            except Exception:
                continue

    return sorted(similar, key=lambda x: x["similarity"], reverse=True)


def generate_dna(category_id: str, filename: str) -> str:
    """生成DNA签章"""
    from datetime import datetime
    now = datetime.now()
    hash8 = hashlib.sha256(f"{category_id}{filename}{now.isoformat()}".encode()).hexdigest()[:8]

    # 简化干支
    ganzhi_map = {
        2026: "丙午", 1: "乙丑", 2: "丙寅", 3: "丁卯", 4: "戊辰",
        5: "己巳", 6: "庚午", 7: "乙未", 8: "丙申"
    }
    year_gz = ganzhi_map.get(now.year, "未知")
    month_gz = ganzhi_map.get(now.month, "未知")

    return f"#龍芯⚡️{year_gz}·{month_gz}·{now.day}日·{category_id}-{filename.split('.')[0]}-v1.0-{hash8}"


def run_classify(content: str, json_output: bool = False) -> dict:
    """主分类流程"""
    category_id, category_info, confidence = classify(content)
    target_dir = category_info["dir"]
    suggested_name = suggest_filename(content, category_id, category_info)
    full_path = ROOT / target_dir / suggested_name
    similar = find_similar(target_dir, content)
    dna = generate_dna(category_id, suggested_name)

    result = {
        "category": category_id,
        "label": category_info["label"],
        "confidence": round(confidence, 2),
        "target_dir": target_dir,
        "suggested_filename": suggested_name,
        "full_path": str(full_path),
        "dna": dna,
        "similar_files": similar,
        "action": "merge" if similar else "create",
        "content_size": len(content),
        "content_lines": len(content.splitlines()),
    }

    return result


def main():
    parser = argparse.ArgumentParser(description="龍魂·内容自动分类吸收引擎 v1.0")
    parser.add_argument("--input", "-i", help="输入文件路径")
    parser.add_argument("--content", "-c", help="直接输入内容文本")
    parser.add_argument("--json", "-j", action="store_true", help="JSON格式输出")
    parser.add_argument("--save", "-s", action="store_true", help="分类后自动保存到目标目录")
    parser.add_argument("--dry-run", "-n", action="store_true", help="只分类不写入")

    args = parser.parse_args()

    # 读取内容
    content = None
    if args.content:
        content = args.content
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        # 从stdin读取
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            print("请通过 --input 或 --content 或管道提供内容", file=sys.stderr)
            sys.exit(1)

    if not content or not content.strip():
        print("错误: 内容为空", file=sys.stderr)
        sys.exit(1)

    # 分类
    result = run_classify(content, json_output=args.json)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # 人类可读输出
        print(f"""
╔══════════════════════════════════════════╗
║   🐉 龍魂·内容分类吸收引擎 v1.0       ║
╚══════════════════════════════════════════╝

📋 分类结果: {result['label']} ({result['category']})
🎯 置信度:   {result['confidence']}
📁 目标目录: {result['target_dir']}/
📄 建议文件名: {result['suggested_filename']}
🧬 DNA:      {result['dna']}
📏 大小:     {result['content_size']} 字节 · {result['content_lines']} 行
⚡ 动作:     {'🔗 合并到已有文件' if result['action'] == 'merge' else '✨ 新建文件'}
""")
        if result['similar_files']:
            print("🔍 发现相似文件:")
            for s in result['similar_files'][:5]:
                print(f"   📄 {s['path']} (相似度: {s['similarity']})")
        print(f"📍 完整路径: {result['full_path']}")

    # 保存
    if args.save and args.dry_run:
        print("\n🔍 [干运行] 未实际写入", file=sys.stderr)
    elif args.save:
        target_path = Path(result['full_path'])
        target_path.parent.mkdir(parents=True, exist_ok=True)

        if result['action'] == 'merge' and result['similar_files']:
            # 合并模式：追加到最相似文件
            best = result['similar_files'][0]
            merge_path = ROOT / best['path']
            existing = merge_path.read_text(encoding='utf-8')
            # 简单追加（实际应更智能）
            new_content = f"\n\n---\n## 追加内容 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\nDNA: {result['dna']}\n\n{content}\n"
            merge_path.write_text(existing + new_content, encoding='utf-8')
            print(f"\n✅ 已合并到: {best['path']}")
        else:
            # 新建模式
            header = f"DNA: {result['dna']}\n创建者: 诸葛鑫（UID9622）\n协议: CC BY-NC-SA 4.0\n日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
            target_path.write_text(header + content, encoding='utf-8')
            print(f"\n✅ 已创建: {result['target_dir']}/{result['suggested_filename']}")

    return result


if __name__ == "__main__":
    main()
