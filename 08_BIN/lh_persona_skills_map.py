#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 人格技能映射引擎 v1.0
# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
DNA: #龍芯⚡️丙午·丙申·乙巳·庚子·䷋否-PERSONA-SKILLS-MAP-v1.0-UID9622
CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F

功能：
  1. 24人格(P00-P15/P18/P19/P20/P72/P77/S1-S3) → 技能清单显式映射
  2. 同步三处：persona-registry.yaml(权威) + persona_registry.json(运行时) + longhun-skills.json(反向关联)
  3. 全部技能 id 注册表校验，不存在的自动剔除并报告
  4. 映射可复用可重跑（幂等）

用法：
  python3 08_BIN/lh_persona_skills_map.py          # 全量同步三文件
  python3 08_BIN/lh_persona_skills_map.py --verify  # 仅校验映射完整性
  python3 08_BIN/lh_persona_skills_map.py --json    # 输出映射 JSON
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YAML_FILE = ROOT / "20_CONFIG" / "persona-registry.yaml"
RUNTIME_JSON = ROOT / "personas" / "runtime" / "persona_registry.json"
SKILLS_JSON = ROOT / "skills" / "longhun-skills.json"

# ════════════════════════════════════════════════════════════
# 24人格 → 技能 映射表（核心定义 · 按人格职能挂载实际注册技能）
# ════════════════════════════════════════════════════════════
PERSONA_SKILLS = {
    # ── 战略层 ──
    "P00": [  # 文心 · 元认知·意图解析·路由
        "longhun-orchestrator", "longhun-persona-orchestrate", "longhun-persona-router",
        "longhun-creator", "dragon-soul-agent",
    ],
    "P01": [  # 诸葛亮 · 战略推理·多路径推演
        "longhun-innovation", "longhun-riemann", "longhun-math-formula-core",
        "longhun-search", "cnsh-semantic-v2-1",
    ],
    # ── 执行层 ──
    "P02": [  # 宝宝 · 情感温度·修复·教学
        "longhun-empower-engine", "longhun-behavior-engine", "longhun-workflow-transparent",
        "longhun-memory-load",
    ],
    "P03": [  # 雯雯 · 结构归档·四签·德字闸
        "longhun-archive", "longhun-review", "longhun-memory-bootstrap", "longhun-compress",
    ],
    "P04": [  # 鲁班 · 工程实现·架构
        "longhun-cnsh", "longhun-cnsh-translate", "longhun-integration",
        "longhun-formula-opt", "longhun-cross-platform",
    ],
    "P07": [  # 管仲 · 成本核算·资源调度
        "longhun-xpay", "longhun-finance", "longhun-multicurrency", "longhun-trust-protocol",
    ],
    "P14": [  # 吕蒙 · 部署执行
        "longhun-deploy", "longhun-cloud-deploy", "longhun-deployment-ready",
        "longhun-cloud-panel", "longhun-daemon",
    ],
    # ── 文化层 ──
    "P08": [  # 仓颉 · CNSH命名·术语桥接
        "cnsh-protocol-v2-0", "cnsh-semantic-v2-1", "longhun-tongxinyi",
        "longhun-tongxinyi-v2", "longhun-nlp", "longhun-ai-lexicon",
    ],
    "P09": [  # 孙思邈 · 系统诊断·治未病
        "longhun-auto-heal", "longhun-monitoring", "longhun-behavior-engine",
        "longhun-forensic-toolkit",
    ],
    "P10": [  # 苏东坡 · 冲突调解·沟通
        "longhun-orchestrator", "dragon-soul-agent", "longhun-persona-router",
        "longhun-workflow-transparent",
    ],
    "P11": [  # 李白 · 创意爆发·破局
        "longhun-innovation", "longhun-creator", "longhun-zeng-digital-human",
        "longhun-video-diffusion",
    ],
    "P12": [  # 屈原 · 价值底线·六誓
        "longhun-deben-audit", "longhun-iron-laws", "longhun-circuit-breaker",
        "longhun-trust-protocol",
    ],
    # ── 守护层 ──
    "P05": [  # 上帝之眼 · 三色审计·十道闸
        "longhun-three-color-audit", "longhun-dual-audit", "longhun-anti-tamper",
        "longhun-circuit-breaker", "longhun-tricolor-audit", "longhun-audit",
    ],
    "P06": [  # 数学大师 · 数字根·五行·权重
        "longhun-digital-root", "longhun-wuxing", "longhun-math-formula-core",
        "longhun-flow-viz", "longhun-riemann",
    ],
    "P13": [  # 姜子牙 · 权限分配·封神榜
        "longhun-governance", "longhun-persona-orchestrate", "longhun-persona-router",
        "longhun-merit-hall",
    ],
    "P15": [  # 乔前辈 · GPG签章·交付验收
        "longhun-gpg-sign", "longhun-dna-align", "longhun-identity-verify",
        "longhun-forensic-toolkit",
    ],
    "P72": [  # 龍盾 · 四级熔断·紧急响应
        "longhun-circuit-breaker", "longhun-auto-heal", "longhun-shield",
        "longhun-anti-tamper", "longhun-vuln-detect",
    ],
    "P18": [  # 基因登记官 · DNA注册·资产登记
        "longhun-anti-tamper", "longhun-dna-align", "longhun-identity-verify",
        "longhun-forensic-toolkit",
    ],
    "P19": [  # 极简审计官 · UI审计·前端质量
        "longhun-three-color-audit", "longhun-audit", "longhun-dual-audit",
        "longhun-review",
    ],
    "P20": [  # 贡献公证官 · 信任积分·三分桶
        "longhun-trust-score", "longhun-merit-hall", "longhun-trust-protocol",
        "longhun-behavior-engine",
    ],
    # ── 安全专项 ──
    "P77": [  # 黑天使军团 · 红蓝对抗·渗透
        "black-angel-legion", "longhun-vuln-detect", "longhun-anti-tamper",
        "longhun-circuit-breaker", "longhun-forensic-toolkit",
    ],
    # ── 子系统 ──
    "S1": [  # 法律引擎 · 法条检索·合规
        "longhun-governance", "longhun-deben-audit", "longhun-trust-protocol",
        "longhun-review",
    ],
    "S2": [  # 洛书369 · 深层数理
        "longhun-digital-root", "longhun-wuxing", "longhun-math-formula-core",
        "longhun-flow-viz",
    ],
    "S3": [  # 人民维权助手 · 维权路径
        "longhun-behavior-engine", "longhun-empower-engine", "longhun-deben-audit",
        "longhun-trust-protocol",
    ],
}


def load_skills() -> dict:
    """加载技能注册表，返回 {id: skill}"""
    with open(SKILLS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    return {s["id"]: s for s in data.get("skills", [])}


def validate(skills_reg: dict) -> dict:
    """校验映射中所有技能 id 存在性，剔除不存在的"""
    clean = {}
    missing = {}
    for persona, ids in PERSONA_SKILLS.items():
        ok, bad = [], []
        for sid in ids:
            (ok if sid in skills_reg else bad).append(sid)
        clean[persona] = ok
        if bad:
            missing[persona] = bad
    return clean, missing


def update_yaml(clean: dict) -> int:
    """文本级插入 skills 字段到 persona-registry.yaml（保留注释）· 插在 priority 行后"""
    if not YAML_FILE.exists():
        print(f"❌ 缺 {YAML_FILE}"); return 0
    lines = YAML_FILE.read_text(encoding="utf-8").splitlines()
    # 1) 定位每个人格块 priority 行的索引
    insert_at = {}  # line_index -> skills_str
    i = 0
    while i < len(lines):
        m = re.match(r"^(\s{2})(P\d{2}|S[1-3]):\s*$", lines[i])
        if m:
            code = m.group(2)
            if code in clean and clean[code]:
                j = i + 1
                while j < len(lines) and (lines[j].startswith("  ") and not lines[j].startswith("  #") and lines[j].strip()):
                    if re.match(r"^    priority:", lines[j]):
                        insert_at[j] = f"    skills: [{', '.join(clean[code])}]"
                        break
                    if re.match(r"^  [A-Z_]+:", lines[j]):  # 下一个顶层块
                        break
                    j += 1
        i += 1
    # 2) 逆序插入，保持行号稳定
    out = lines[:]
    for idx in sorted(insert_at, reverse=True):
        out.insert(idx + 1, insert_at[idx])
    changed = len(insert_at)
    if changed:
        YAML_FILE.write_text("\n".join(out) + "\n", encoding="utf-8")
        print(f"✅ yaml 已补 skills 字段: {changed} 个人格（priority 行后）")
    else:
        print("ℹ️ yaml 无新增（可能已存在或块结构异常）")
    return changed


def update_skills_json(clean: dict, skills_reg: dict) -> int:
    """反向：132条技能补 persona 关联字段"""
    persona_of = {}  # skill_id -> [persona...]
    for persona, ids in clean.items():
        for sid in ids:
            persona_of.setdefault(sid, []).append(persona)
    changed = 0
    with open(SKILLS_JSON, encoding="utf-8") as f:
        data = json.load(f)
    for s in data.get("skills", []):
        p = persona_of.get(s["id"], [])
        if p and s.get("persona") != p:
            s["persona"] = p
            changed += 1
        elif not p and "persona" in s:
            del s["persona"]
    with open(SKILLS_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"✅ skills.json 已补 persona 反向关联: {changed} 条技能")
    return changed


def update_runtime_json(clean: dict) -> int:
    """运行时注册表核心人格补 skills 字段"""
    if not RUNTIME_JSON.exists():
        print(f"❌ 缺 {RUNTIME_JSON}"); return 0
    with open(RUNTIME_JSON, encoding="utf-8") as f:
        data = json.load(f)
    personas = data.get("personas", {})
    changed = 0
    for code, ids in clean.items():
        if code in personas and ids:
            if personas[code].get("skills") != ids:
                personas[code]["skills"] = ids
                changed += 1
    if changed:
        with open(RUNTIME_JSON, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            f.write("\n")
        print(f"✅ runtime json 已补 skills: {changed} 个人格")
    else:
        print("ℹ️ runtime json 无新增")
    return changed


def update_persona_mds(clean: dict, skills_reg: dict) -> int:
    """人格定义 md 补『技能挂载』段（幂等）"""
    types = {s["id"]: s.get("type", "doc") for s in skills_reg.values()}
    added = 0
    for md in sorted(Path("personas").glob("P*.md")):
        m = re.match(r"P(\d{2})", md.name)
        if not m:
            continue
        ids = clean.get("P" + m.group(1))
        if not ids:
            continue
        text = md.read_text(encoding="utf-8")
        if "## 技能挂载" in text:
            continue
        lines = [f"- `{sid}`（{types.get(sid, 'doc')}）" for sid in ids]
        section = (
            "## 技能挂载\n\n"
            + "\n".join(lines)
            + "\n\n> 权威源: `20_CONFIG/persona-registry.yaml` · 同步器: `08_BIN/lh_persona_skills_map.py`\n\n"
        )
        text = text.replace("## 核心职能", section + "## 核心职能", 1)
        md.write_text(text, encoding="utf-8")
        added += 1
    print(f"✅ 人格md 已挂载技能段: {added} 个")
    return added


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "sync"
    skills_reg = load_skills()
    clean, missing = validate(skills_reg)

    if missing:
        print("⚠️ 以下映射技能不在注册表（已自动剔除）:")
        for p, ids in missing.items():
            print(f"  {p}: {ids}")

    total_mapped = sum(len(v) for v in clean.values())
    print(f"📊 24人格映射: {len(clean)} 人格 · {total_mapped} 条技能关联（去重 {len({s for v in clean.values() for s in v})} 条唯一技能）")

    if mode == "--verify":
        print(f"✅ 校验完成: 全部映射技能存在于注册表, 缺失 {len(missing)} 组")
        return

    if mode == "--json":
        print(json.dumps(clean, ensure_ascii=False, indent=2))
        return

    update_yaml(clean)
    update_skills_json(clean, skills_reg)
    update_runtime_json(clean)
    update_persona_mds(clean, skills_reg)
    print("🎯 四层同步完成: yaml权威源 + skills.json反向 + runtime + 人格md")


if __name__ == "__main__":
    main()
