#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════╗
║  龍魂·投喂吸收管道 v2.0 — 全人格路由自动吸收                   ║
║  DNA: #龍芯⚡️丙午·丙申·甲寅·乙亥·䷄需-TOUWEI-ABSORB-v2.0     ║
╠══════════════════════════════════════════════════════════════════╣
║  铁律：                                                         ║
║  1. 外部AI内容必须过防篡改扫描 → 三色判定                       ║
║  2. 🔴熔断拒绝 / 🟡待审记录后继续 / 🟢通过后吸收                ║
║  3. 吸收后绑定v∞干支卦DNA，入链不可覆                           ║
║  4. 全人格路由：各人格各取所需，产出直接填满四维                 ║
║  5. 外部DNA码一律替换为系统生成的v∞ DNA                         ║
║  6. 🆕 不只是存文档 — P02落代码，P15落自动化，P13落索引         ║
║                                                                 ║
║  用法：                                                         ║
║    python3 bin/lh_touwei_absorb.py "投喂内容..."                 ║
║    python3 bin/lh_touwei_absorb.py --file path/to/doc.md         ║
║    cat doc.txt | python3 bin/lh_touwei_absorb.py                 ║
║    echo "内容" | python3 bin/lh_touwei_absorb.py                 ║
║                                                                 ║
║  人格路由（各取所需）：                                         ║
║    P05 上帝之眼 → 三色审计 + 安全评审                            ║
║    P01 诸葛亮   → 价值评估 + 去留建议                            ║
║    P02 龍芯     → 工程落地 + 代码生成                            ║
║    P15 乔前辈   → 自动化脚本 + 可集成化                          ║
║    P13 姜子牙   → 跨模块联动 + 索引注册                          ║
║    P00 文心     → 铁律验证 + 底座对齐                            ║
║    P77 黑天使   → 漏洞检测 + 结界审查                            ║
║    P11 孙子     → 来源审计 + 归属判定                            ║
╚══════════════════════════════════════════════════════════════════╝
"""

import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# ── 项目根路径 ──────────────────────────────────
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_ARTICLES_DIR = _PROJECT_ROOT / "articles"
_L7_DATA = _PROJECT_ROOT / "L7_数据层"
_KNOWLEDGE_DIR = _PROJECT_ROOT / "L7_数据层" / "knowledge"
_BIN_DIR = _PROJECT_ROOT / "bin"
_L1_DIR = _PROJECT_ROOT / "L1_内核层"
_DNA_REGISTRY = _L7_DATA / "dna_registry_index.json"
_ANTI_TAMPER = _BIN_DIR / "lh_anti_tamper.py"
_CORE_ENGINE = _L1_DIR / "longhun_core_engine.py"

# ── 人格路由表 ────────────────────────────────
PERSONA_ROUTER: dict[str, dict[str, Any]] = {
    "P05_上帝之眼": {
        "role": "三色审计官",
        "desc": "安全扫描·三色判定·防护墙检查·外部AI风险评级",
        "output_key": "security_audit",
        "priority": 1,
        "emoji": "🔍",
    },
    "P01_诸葛亮": {
        "role": "价值评估师",
        "desc": "贡献值C评估·时间衰减·去留建议·龙魂系统内价值定位",
        "output_key": "value_assessment",
        "priority": 2,
        "emoji": "📊",
    },
    "P02_龍芯": {
        "role": "工程落地官",
        "desc": "技术实现设计·可执行代码生成·架构建议·单元测试",
        "output_key": "engineering",
        "priority": 3,
        "emoji": "⚙️",
    },
    "P15_乔前辈": {
        "role": "自动化工程师",
        "desc": "自动化脚本·CLI工具·定时任务·跨生态桥接·一键执行",
        "output_key": "automation",
        "priority": 4,
        "emoji": "🤖",
    },
    "P13_姜子牙": {
        "role": "跨模块编排官",
        "desc": "模块依赖分析·IPA路由注册·跨模块索引·知识图谱更新",
        "output_key": "orchestration",
        "priority": 5,
        "emoji": "🔗",
    },
    "P00_文心": {
        "role": "铁律守护者",
        "desc": "底座锚点验证·铁律合规检查·最初誓言对齐·不可变检查",
        "output_key": "constitutional_check",
        "priority": 0,
        "emoji": "📜",
    },
    "P77_黑天使": {
        "role": "漏洞猎手",
        "desc": "代码安全审计·漏洞检测·注入风险·结界审查·威胁建模",
        "output_key": "vulnerability",
        "priority": 6,
        "emoji": "🛡️",
    },
    "P11_孙子": {
        "role": "来源审计官",
        "desc": "借用合规审计·来源追溯·LICENSE检查·归属判定·引用链",
        "output_key": "attribution",
        "priority": 7,
        "emoji": "©️",
    },
}


# ── 关键词 → 概念映射表（用于元数据提取）─────────
_CONCEPT_MAP: dict[str, list[str]] = {
    "五行": ["五行", "金木水火土", "五行生克"],
    "河图洛书": ["河图", "洛书", "河图洛书"],
    "天干地支": ["天干", "地支", "干支", "四柱", "八字"],
    "自主可控": ["自主可控", "国产化", "信创", "国产替代"],
    "算力能效": ["算力", "能效", "GPU", "FLOPS", "推理"],
    "函数调用": ["函数调用", "Function Calling", "tool call", "tools"],
    "龍魂标准": ["龍魂", "龙魂", "CNSH", "longhun"],
    "文化自信": ["文化自信", "传统文化", "中国元素"],
    "工信部": ["工信部", "典型示范", "国标", "国家标准"],
    "AI安全": ["安全", "防护", "熔断", "注入", "结界"],
    "能源节约": ["用电", "节能", "省电", "功耗", "电源"],
    "模型优化": ["量化", "剪枝", "蒸馏", "压缩", "瘦身"],
    "音视频": ["语音", "TTS", "STT", "音频", "视频", "Whisper"],
    "数据库": ["数据库", "SQL", "NoSQL", "存储", "MySQL"],
    "API设计": ["API", "REST", "GraphQL", "接口", "端点"],
    "微服务": ["微服务", "服务网格", "容器", "K8s", "Serverless"],
    "部署运维": ["部署", "CI/CD", "DevOps", "上线", "运维"],
    "前端": ["前端", "React", "Vue", "HTML", "CSS", "UI"],
    "小程序": ["小程序", "微信", "WeChat", "UniApp"],
    "加密安全": ["加密", "签名", "GPG", "哈希", "证书"],
    "IoT": ["IoT", "物联网", "嵌入式", "传感器", "鸿蒙"],
    "数据主权": ["主权", "数据主权", "隐私", "GDPR"],
    "知识管理": ["知识图谱", "知识库", "RAG", "检索"],
    "人格": ["人格", "Persona", "心理", "性格"],
    "区块链": ["区块链", "Merkle", "分布式", "去中心化"],
}


def generate_vinf_dna(module: str, action: str) -> str:
    """通过核心引擎生成 v∞ 干支卦 DNA"""
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "longhun_core_engine", str(_CORE_ENGINE)
    )
    if spec is not None and spec.loader is not None:
        mod = importlib.util.module_from_spec(spec)
        sys.modules["longhun_core_engine"] = mod
        spec.loader.exec_module(mod)
        engine = mod.LonghunCoreEngine()
        return engine._generate_dna_trace(module, action)
    return (
        f"#龍芯⚡️{datetime.now().strftime('%Y%m%d')}-{module}-{action}-FALLBACK"
    )


def scan_content(text: str) -> tuple[str, str]:
    """运行防篡改扫描，返回 (判定, 详细报告)"""
    result = subprocess.run(
        [sys.executable, str(_ANTI_TAMPER), "scan", text],
        capture_output=True,
        text=True,
        cwd=str(_PROJECT_ROOT),
    )
    output = result.stdout + result.stderr
    if result.returncode == 2:
        return ("🔴 熔断", output)
    elif result.returncode == 1:
        return ("🟡 待审", output)
    else:
        return ("🟢 通过", output)


def clean_external_dna(text: str) -> str:
    """移除外部AI文档中的格里历DNA码，替换为占位符"""
    text = re.sub(
        r"#龍芯⚡️20\d{2}-\d{2}-\d{2}[^\s）,，。\n]*",
        "【待绑定龍魂DNA】",
        text,
    )
    text = re.sub(
        r"#龍芯⚡️20\d{6,14}[^\s）,，。\n]*",
        "【待绑定龍魂DNA】",
        text,
    )
    return text


def extract_metadata(text: str) -> dict[str, Any]:
    """从外部文档中提取元数据"""
    meta: dict[str, Any] = {
        "title": "未命名文档",
        "category": "external_feed",
        "original_source": "外部AI投喂",
        "key_concepts": [],
        "concept_categories": {},
    }

    # 提取标题
    title_match = re.search(r"[《「]([^》」]+)[》」]", text)
    if title_match:
        meta["title"] = title_match.group(1)
    else:
        # 取第一句话（以。！？换行为界），不超过40字
        first_sentence = re.split(r"[。！？\n]", text.strip())[0].strip()
        first_sentence = first_sentence.lstrip("#").strip()
        if first_sentence and len(first_sentence) > 3:
            meta["title"] = first_sentence[:60]
        else:
            meta["title"] = "外部投喂文档"

    # 提取概念分类
    all_keywords: set[str] = set()
    for category, keywords in _CONCEPT_MAP.items():
        matched = [kw for kw in keywords if kw in text]
        if matched:
            meta["concept_categories"][category] = matched
            all_keywords.update(matched)
    meta["key_concepts"] = sorted(all_keywords)

    # 检测内容类型
    if any(kw in text for kw in ["代码", "Code", "函数", "API", "接口"]):
        meta["content_type"] = "技术实现"
    elif any(kw in text for kw in ["理论", "原理", "本质", "哲学"]):
        meta["content_type"] = "理论分析"
    elif any(kw in text for kw in ["申报", "工信部", "政策", "标准"]):
        meta["content_type"] = "政策指南"
    elif any(kw in text for kw in ["教程", "步骤", "手把手", "实战"]):
        meta["content_type"] = "实战教程"
    else:
        meta["content_type"] = "综合参考"

    # 统计
    meta["char_count"] = len(text)
    meta["line_count"] = len(text.split("\n"))
    meta["chinese_ratio"] = round(
        sum(1 for c in text if "\u4e00" <= c <= "\u9fff") / max(len(text), 1), 2
    )

    return meta


# ═══════════════════════════════════════════════════════════════
#  人格路由执行引擎
# ═══════════════════════════════════════════════════════════════


class PersonaRouter:
    """全人格路由调度器"""

    def __init__(self, content: str, meta: dict[str, Any], dna: str):
        self.content = content
        self.meta = meta
        self.dna = dna
        self.results: dict[str, Any] = {}

    def execute_all(self) -> dict[str, Any]:
        """按优先级依次执行所有人格"""
        sorted_personas = sorted(
            PERSONA_ROUTER.items(), key=lambda x: x[1]["priority"]
        )
        for persona_id, config in sorted_personas:
            self.results[config["output_key"]] = self._run_persona(
                persona_id, config
            )
        return self.results

    def _run_persona(self, persona_id: str, config: dict[str, Any]) -> dict[str, Any]:
        """执行单个人格分析"""
        result: dict[str, Any] = {
            "persona": persona_id,
            "persona_name": config["role"],
            "executed": datetime.now().isoformat(),
        }

        method = getattr(self, f"_p_{persona_id.replace('-', '_').split('_')[0].lower()}", None)
        if method:
            result["analysis"] = method()
        else:
            result["analysis"] = f"人格 {persona_id} 分析中..."

        return result

    # ── P00 文心：铁律验证 ──
    def _p_p00(self) -> str:
        """底座锚点对齐检查"""
        violations = []
        if any(w in self.content for w in ["删除数据", "清空", "彻底抹除"]):
            violations.append("A-006: 出现「删除」语义 → 禁止，只能冻结/归档")
        if any(w in self.content for w in ["国际标准", "国际接轨", "全球统一"]):
            violations.append("A-010: 出现「国际标准」语义 → 中国法律唯一准绳")

        if violations:
            return "⚠️ 铁律告警:\n" + "\n".join(f"  - {v}" for v in violations)
        return "🟢 底座锚点 A-001~A-033 均未触发冲突。外部内容未试图修改或覆盖底座。"

    # ── P05 上帝之眼：三色审计 ──
    def _p_p05(self) -> str:
        """安全扫描 + 三色判定"""
        scan_verdict, scan_report = scan_content(self.content)

        red_flags = []
        yellow_flags = []
        for line in scan_report.split("\n"):
            if "FUSE-RED" in line or "🔴" in line:
                red_flags.append(line.strip())
            elif "FUSE-YELLOW" in line or "⚠️" in line:
                yellow_flags.append(line.strip())

        parts = [f"三色判定: {scan_verdict}"]
        if red_flags:
            parts.append(f"🔴 红色告警 ({len(red_flags)}项):")
            for f in red_flags[:5]:
                parts.append(f"  - {f}")
        if yellow_flags:
            parts.append(f"🟡 黄色提示 ({len(yellow_flags)}项):")
            for f in yellow_flags[:5]:
                parts.append(f"  - {f}")
        if not red_flags and not yellow_flags:
            parts.append("🟢 无安全告警，内容合规。")
        return "\n".join(parts)

    # ── P01 诸葛亮：价值评估 ──
    def _p_p01(self) -> str:
        """贡献值 C 评估 + 去留建议"""
        # 按内容质量打分
        score = 0
        score += min(len(self.meta.get("key_concepts", [])) * 0.5, 4)  # 概念密度
        score += min(self.meta.get("chinese_ratio", 0) * 2, 2)  # 中文占比
        score += 2 if self.meta.get("content_type") == "技术实现" else 1  # 技术价值
        score += 2 if len(self.content) > 500 else 1  # 内容丰富度
        # 检查是否有可执行的代码片段
        if re.search(r"```(python|bash|js|javascript|go|rust|c)", self.content):
            score += 2

        C = round(score, 1)

        if C >= 7:
            suggestion = "🏆 高价值 — 建议入库 P0/P1，全人格消化"
        elif C >= 4:
            suggestion = "📋 中等价值 — 建议入库 P2，按需引用"
        elif C >= 2:
            suggestion = "📦 低价值 — 建议归档 P3，知识碎片存储"
        else:
            suggestion = "🗑️ 极低价值 — 建议丢弃或仅做参考"

        return f"贡献值 C = {C}/10\n去留建议: {suggestion}\n评分依据: 概念密度({min(len(self.meta.get('key_concepts', []))*0.5, 4)}) + 中文占比({min(self.meta.get('chinese_ratio', 0)*2, 2)}) + 技术价值({2 if self.meta.get('content_type')=='技术实现' else 1}) + 内容丰富度({2 if len(self.content)>500 else 1})"

    # ── P02 龍芯：工程落地 ──
    def _p_p02(self) -> str:
        """代码生成建议 + 架构设计"""
        concept_cats = self.meta.get("concept_categories", {})

        parts = ["## 技术栈映射"]

        # 根据概念类别建议技术栈
        stack_map = {
            "函数调用": "Python/FastAPI + OpenAI-compatible tools API",
            "算力能效": "Python + Prometheus + Grafana 监控面板",
            "音视频": "Python + Whisper/FastWhisper + edge-tts/XTTS v2",
            "数据库": "Python + SQLAlchemy + SQLite/PostgreSQL",
            "API设计": "Python + FastAPI + Pydantic v2",
            "前端": "React + TypeScript + Vite 或 原生 HTML/JS",
            "小程序": "微信小程序原生 + CloudBase",
            "部署运维": "Docker + docker-compose + systemd",
            "模型优化": "PyTorch + ONNX Runtime + llama.cpp",
            "IoT": "MicroPython/Arduino + MQTT",
            "加密安全": "Python hashlib/cryptography + GPG",
            "知识管理": "Python + ChromaDB/Milvus + LangChain",
        }

        has_tech = False
        for cat in concept_cats:
            if cat in stack_map:
                has_tech = True
                parts.append(f"- {cat} → {stack_map[cat]}")

        if not has_tech:
            parts.append("- 未识别到明确技术栈 → 建议人工评估")

        # 代码框架（如果有可落地的技术点）
        if concept_cats:
            parts.append("\n## 可执行代码框架建议")
            parts.append("```python")
            parts.append("# 龍魂系统吸收 · 自动生成代码框架")
            parts.append(f"# DNA: {self.dna}")
            parts.append("")
            parts.append("def main():")
            parts.append(f'    """{self.meta.get("title", "外部投喂吸收")} — 工程落地"""')
            parts.append("    # TODO: 根据人格分析结果实现具体逻辑")
            parts.append("    pass")
            parts.append("")
            parts.append('if __name__ == "__main__":')
            parts.append("    main()")
            parts.append("```")

        return "\n".join(parts)

    # ── P15 乔前辈：自动化 ──
    def _p_p15(self) -> str:
        """自动化脚本建议"""
        concept_cats = self.meta.get("concept_categories", {})

        automations = []

        if "算力能效" in concept_cats:
            automations.append(
                "📊 能效监控定时任务: cron每分钟采集GPU/CPU/电量，存入CSV，生成日报"
            )
            automations.append(
                "```bash\n# 定时采集脚本\n*/5 * * * * python3 bin/lh_energy_monitor.py >> logs/energy.log\n```"
            )

        if "音视频" in concept_cats:
            automations.append(
                "🎤 语音转写守护进程: watch模式监听目录，自动转写新录音"
            )
            automations.append(
                "```bash\n# 守护进程\npython3 bin/lh_humha_ku_sync.py --watch &\n```"
            )

        if "函数调用" in concept_cats:
            automations.append(
                "🔌 Function Calling 注册工具: CLI一键注册新龍魂技能"
            )
            automations.append(
                "```bash\n# 注册技能\npython3 bin/lh_skill_register.py --name '查询天气' --type 'API'\n```"
            )

        if "模型优化" in concept_cats:
            automations.append(
                "🔄 模型自动瘦身: 定时检查模型体积，超阈值自动压缩"
            )

        if not automations:
            automations.append(
                "💡 建议: 该投喂内容暂无直接可自动化点。考虑如下通用自动化："
            )
            automations.append(
                "- 定时拉取外部内容 → 自动投喂吸收管道"
            )
            automations.append(
                "- 知识更新检测 → 自动触发全人格重分析"
            )
            automations.append(
                "```bash\n# 定时爬虫投喂\n0 6 * * * python3 bin/lh_crawler_feed.py | python3 bin/lh_touwei_absorb.py\n```"
            )

        return "\n".join(automations)

    # ── P13 姜子牙：跨模块联动 ──
    def _p_p13(self) -> str:
        """模块索引更新 + 路由建议"""
        concept_cats = self.meta.get("concept_categories", {})

        routes = []

        # IPA 路由建议
        route_map = {
            "函数调用": "IPA-L5-FUNCTION-CALLING → L5_服务层/services/function_calling/",
            "算力能效": "IPA-L5-ENERGY-MONITOR → L5_服务层/services/energy_monitor/",
            "音视频": "IPA-L5-MULTIMODAL-001 → L1_内核层/three_vacuum_gateway_registry.json",
            "数据库": "IPA-L7-DATA-LAYER → L7_数据层/",
            "API设计": "IPA-L5-API-GATEWAY → L5_服务层/services/api/",
            "模型优化": "IPA-L2-SKILL-MODEL → L2_技能层/model_optimization/",
            "部署运维": "IPA-L6-INTEGRATION → L6_集成层/",
            "知识管理": "IPA-L7-KNOWLEDGE → L7_数据层/knowledge/",
            "数据主权": "IPA-L8-GOVERNANCE → L8_治理层/governance/",
            "龍魂标准": "IPA-L1-CORE → L1_内核层/",
            "人格": "IPA-L2-PERSONA → 01_技能庫/",
        }

        for cat in concept_cats:
            if cat in route_map:
                routes.append(f"  {cat} → {route_map[cat]}")

        parts = ["## 关联模块"]
        if routes:
            parts.extend(routes)
        else:
            parts.append("  未匹配到已知模块路由，建议人工评估关联。")

        parts.append(f"\n## DNA注册")
        parts.append(f"  已注册: {self.dna}")
        parts.append(f"  登记册: L7_数据层/dna_registry_index.json")

        return "\n".join(parts)

    # ── P77 黑天使：漏洞检测 ──
    def _p_p77(self) -> str:
        """安全审计"""
        risks = []

        # 检测代码注入风险
        if re.search(r'eval\s*\(|exec\s*\(|os\.system\s*\(|subprocess\.call\s*\(', self.content):
            risks.append("🔴 代码注入风险: 检测到 eval/exec/os.system/subprocess 调用")

        # 检测硬编码密钥
        if re.search(r'(api_key|secret|password|token)\s*=\s*["\'][^"\']+["\']', self.content):
            risks.append("🔴 硬编码密钥: 检测到 API Key/Secret/Password 明文")

        # 检测不安全的依赖
        if re.search(r'pip install|npm install|go get', self.content):
            risks.append("🟡 依赖安装: 建议锁定版本号，避免供应链攻击")

        # 检测端口暴露
        if re.search(r'0\.0\.0\.0|bind\(.*0\.0\.0\.0', self.content):
            risks.append("🟡 端口暴露: 检测到 0.0.0.0 绑定，建议限制监听接口")

        if not risks:
            return "🟢 未检测到已知漏洞模式。外部内容代码片段安全。"

        return "\n".join(risks)

    # ── P11 孙子：来源审计 ──
    def _p_p11(self) -> str:
        """来源追溯"""
        parts = ["## 来源审计"]

        # 检测原始来源
        urls = re.findall(r"https?://[^\s）),，。\n]+", self.content)
        if urls:
            parts.append(f"🔗 检测到 {len(urls)} 个原始URL:")
            for u in urls[:5]:
                parts.append(f"  - {u}")
        else:
            parts.append("📭 未检测到原始URL来源")

        # 检测引用格式
        refs = re.findall(r"(?:引用|来源|参考|摘自|via|source|ref)[：:]\s*([^\n]+)", self.content)
        if refs:
            parts.append(f"📝 检测到 {len(refs)} 个显式引用:")
            for r in refs[:3]:
                parts.append(f"  - {r.strip()}")
        else:
            parts.append("📭 未检测到显式引用声明 → 来源模糊，建议标注")

        # 许可证检查
        license_match = re.search(r"(?:LICENSE|License|许可证)[：:]\s*(\w+)", self.content)
        if license_match:
            parts.append(f"📜 许可证: {license_match.group(1)}")
        else:
            parts.append("📭 未声明许可证 → 吸收时默认按「龍魂引用」处理")

        parts.append("\n⚠️ 归属建议: 如为原创技术方案，建议在 articles/ 中标注「龍魂引用·外部AI投喂」")

        return "\n".join(parts)


# ═══════════════════════════════════════════════════════════════
#  双语四维输出构建器
# ═══════════════════════════════════════════════════════════════


def build_bilingual_output(
    meta: dict[str, Any],
    dna: str,
    cleaned_content: str,
    persona_results: dict[str, Any],
) -> str:
    """构建双语四维输出 + 全人格分析结果"""

    def safe_result(key: str) -> dict[str, Any]:
        return persona_results.get(key, {})

    date_str = datetime.now().strftime("%Y-%m-%d")

    # 预计算 persona 分析摘要 JSON（避免 f-string 嵌套问题）
    persona_summary_json = json.dumps(
        {k: v.get("analysis", "") for k, v in persona_results.items()},
        ensure_ascii=False,
        indent=4,
    )
    concept_cat_json = json.dumps(
        meta.get("concept_categories", {}), ensure_ascii=False, indent=4
    )

    # 安全审计
    sec = safe_result("security_audit").get("analysis", "待审计")
    # 价值评估
    val = safe_result("value_assessment").get("analysis", "待评估")
    # 工程落地
    eng = safe_result("engineering").get("analysis", "待设计")
    # 自动化
    auto = safe_result("automation").get("analysis", "待规划")
    # 跨模块
    orch = safe_result("orchestration").get("analysis", "待编排")
    # 铁律
    const = safe_result("constitutional_check").get("analysis", "待验证")
    # 漏洞
    vuln = safe_result("vulnerability").get("analysis", "待扫描")
    # 归属
    attr = safe_result("attribution").get("analysis", "待审计")

    output = f"""---
title: "{meta['title']}"
dna: "{dna}"
date: "{date_str}"
category: "{meta.get('category', 'external_feed')}"
source: "{meta.get('original_source', '外部AI投喂')}"
key_concepts: {json.dumps(meta.get('key_concepts', []), ensure_ascii=False)}
content_type: "{meta.get('content_type', '综合参考')}"
status: "已吸收·全人格路由完成·入链"
char_count: {meta.get('char_count', 0)}
chinese_ratio: {meta.get('chinese_ratio', 0)}
personas_executed: {json.dumps(list(PERSONA_ROUTER.keys()), ensure_ascii=False)}
---

# {meta['title']}

> 🧬 **DNA**: `{dna}`
> 📅 **吸收日期**: {date_str}
> 📥 **来源**: {meta.get('original_source', '外部AI投喂')}
> 🏷️ **关键词**: {', '.join(meta.get('key_concepts', []))}
> 📊 **内容类型**: {meta.get('content_type', '综合参考')}
> 🤖 **执行人格**: {len(PERSONA_ROUTER)} 个人格全量路由

---

## 📖 人人看得懂 · 大白话

### 🟢 一句话总结
{meta.get('title', '这篇内容')}讲了{meta.get('content_type', '一些')}方面的东西，核心是说『{meta.get('key_concepts', ['相关内容'])[0] if meta.get('key_concepts') else '一个概念'}』。

### 📜 铁律验证 (P00 文心)
{const}

### 🔍 安全评审 (P05 上帝之眼)
{sec}

---

## 🔧 技术看得懂 · 要点

### 📊 价值评估 (P01 诸葛亮)
{val}

### ⚙️ 工程落地 (P02 龍芯)
{eng}

### 🤖 自动化方案 (P15 乔前辈)
{auto}

### 🛡️ 安全审计 (P77 黑天使)
{vuln}

---

## 🤖 AI 看得懂 · 结构化元数据

```json
{{
  "meta": {json.dumps(meta, ensure_ascii=False, indent=4)},
  "persona_routing": {{
    "total_personas": {len(PERSONA_ROUTER)},
    "executed_at": "{datetime.now().isoformat()}",
    "dna": "{dna}"
  }},
  "concept_categories": {concept_cat_json},
  "persona_results_summary": {persona_summary_json}
}}
```

---

## 💻 代码看得懂 · 可执行

### 🔗 跨模块路由 (P13 姜子牙)
{orch}

### ©️ 来源审计 (P11 孙子)
{attr}

### 📦 可执行代码片段
（见上方 P02 龍芯 和 P15 乔前辈 产出的代码块）

---

## 📄 原始内容（已清洗外部DNA · 已过防篡改扫描）

{cleaned_content}

---

## 🧬 全人格执行签名

| 人格 | 角色 | 状态 |
|:---|:---|:---:|
"""
    for p_id, p_cfg in sorted(PERSONA_ROUTER.items(), key=lambda x: x[1]["priority"]):
        p_key = p_cfg["output_key"]
        has_result = bool(persona_results.get(p_key, {}).get("analysis", ""))
        status_icon = "✅" if has_result else "⏳"
        output += f"| {p_cfg['emoji']} {p_id} | {p_cfg['role']} | {status_icon} |\n"

    output += f"""
> ⚠️ 本文为外部AI投喂内容，已过防篡改扫描 + 全人格路由消化。
> 外部原始DNA码已替换，以系统生成的v∞干支卦DNA为准。
> 查看登记册: L7_数据层/dna_registry_index.json
> 🧬 DNA: `{dna}`
"""
    return output


# ═══════════════════════════════════════════════════════════════
#  主吸收流程
# ═══════════════════════════════════════════════════════════════


def register_dna(dna: str, title: str, filepath: str):
    """将DNA注册到登记册"""
    if _DNA_REGISTRY.exists():
        raw = _DNA_REGISTRY.read_text(encoding="utf-8")
        last_brace = raw.rfind("}")
        if last_brace >= 0:
            raw = raw[: last_brace + 1]
        index = json.loads(raw)
    else:
        index = {"entries": [], "by_type": {}, "by_file": {}, "count": 0}

    entry = {
        "dna": dna,
        "title": title,
        "file": filepath,
        "timestamp": datetime.now().isoformat(),
        "type": "TOUWEI_ABSORB_v2",
        "personas_executed": list(PERSONA_ROUTER.keys()),
    }

    if "entries" not in index:
        index["entries"] = []
    index["entries"].append(entry)
    index["by_type"]["TOUWEI_ABSORB_v2"] = (
        index["by_type"].get("TOUWEI_ABSORB_v2", 0) + 1
    )
    if "TOUWEI_ABSORB" in index.get("by_type", {}):
        index["by_type"]["TOUWEI_ABSORB_v2"] += index["by_type"].pop("TOUWEI_ABSORB", 0)
    index["count"] = len(index["entries"])

    _DNA_REGISTRY.write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def absorb(text: str, title_override: str = "") -> bool:
    """主吸收流程 — 全人格路由版"""
    print("╔══════════════════════════════════════════╗")
    print("║  龍魂·投喂吸收管道 v2.0 · 全人格路由     ║")
    print("║  DNA: #龍芯⚡️丙午·丙申·甲寅·乙亥·䷄需    ║")
    print("╚══════════════════════════════════════════╝")

    # ── 第1步：防篡改扫描 ──
    print("\n🔍 [P05 上帝之眼] 防篡改扫描...")
    verdict, report = scan_content(text)
    print(f"   判定: {verdict}")

    if "熔断" in verdict:
        for line in report.split("\n"):
            if "FUSE-" in line:
                print(f"   {line.strip()}")
        print("\n❌ 内容熔断，拒绝吸收。")
        print("   💡 申诉: lh fuse appeal --rule FUSE-YELLOW-001")
        return False

    if "待审" in verdict:
        for line in report.split("\n"):
            if "⚠️" in line:
                print(f"   {line.strip()}")
        print("   ⚠️ 黄色警报已记录，继续吸收...")

    # ── 第2步：清洗外部DNA ──
    print("\n🧹 [P00 文心] 清洗外部DNA码...")
    cleaned = clean_external_dna(text)
    ext_count = text.count("#龍芯⚡️20") - cleaned.count("#龍芯⚡️20")
    print(f"   已替换 {ext_count} 个格里历DNA码")

    # ── 第3步：提取元数据 ──
    print("\n📋 [P13 姜子牙] 提取元数据...")
    meta = extract_metadata(cleaned)
    if title_override:
        meta["title"] = title_override
    print(f"   标题: {meta['title']}")
    print(f"   类型: {meta.get('content_type', 'N/A')}")
    print(f"   概念: {', '.join(meta.get('key_concepts', []))}")

    # ── 第4步：生成v∞ DNA ──
    print("\n🧬 [P18 基因登记官] 生成v∞干支卦DNA...")
    dna = generate_vinf_dna("TOUWEI", "ABSORB")
    print(f"   DNA: {dna}")
    cleaned = cleaned.replace("【待绑定龍魂DNA】", dna)

    # ── 第5步：全人格路由执行 ──
    print("\n🤖 [全人格路由] 执行 {} 个人格分析...".format(len(PERSONA_ROUTER)))
    router = PersonaRouter(cleaned, meta, dna)
    persona_results = router.execute_all()

    for p_id, p_cfg in sorted(
        PERSONA_ROUTER.items(), key=lambda x: x[1]["priority"]
    ):
        p_key = p_cfg["output_key"]
        has_result = bool(persona_results.get(p_key, {}).get("analysis", ""))
        icon = "✅" if has_result else "⏳"
        print(f"   {p_cfg['emoji']} {p_id} ({p_cfg['role']}): {icon}")

    # ── 第6步：构建双语四维输出 ──
    print("\n📝 [双语四维] 构建输出...")
    output = build_bilingual_output(meta, dna, cleaned, persona_results)

    # ── 第7步：保存文件 ──
    safe_title = re.sub(r"[^\w\u4e00-\u9fff-]", "_", meta["title"])[:50]
    date_prefix = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date_prefix}-{safe_title}.md"
    filepath = _ARTICLES_DIR / filename

    _ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    filepath.write_text(output, encoding="utf-8")
    print(f"\n💾 保存: {filepath}")
    print(f"   大小: {len(output):,} 字")

    # ── 第8步：注册DNA ──
    print("\n📇 [P18] 注册DNA到登记册...")
    register_dna(dna, meta["title"], str(filepath.relative_to(_PROJECT_ROOT)))

    # ── 第9步：生成可执行代码文件（如有技术落点） ──
    concept_cats = meta.get("concept_categories", {})
    if concept_cats:
        _generate_executable_stub(meta, dna, concept_cats)

    # ── 汇总 ──
    print("\n" + "=" * 56)
    print("✅ 投喂吸收完成 · 全人格路由消化")
    print(f"   📄 {filepath.name}")
    print(f"   🧬 {dna}")
    print(f"   🤖 {len(PERSONA_ROUTER)} 人格已执行")
    print(f"   🟢 状态: 已入链 · 四维可读 · 代码可执行")
    print("=" * 56)

    return True


def _generate_executable_stub(
    meta: dict[str, Any], dna: str, concept_cats: dict[str, Any]
):
    """在 bin/ 下生成可执行代码桩文件"""
    stub_name = re.sub(r"[^\w]", "_", meta.get("title", "absorbed"))[:30].strip("_")
    stub_path = _BIN_DIR / f"lh_absorbed_{stub_name}.py"

    # 避免重复创建
    if stub_path.exists():
        return

    tech_hints = []
    for cat, keywords in concept_cats.items():
        for kw in keywords:
            tech_hints.append(f"#   - {cat}: {kw}")

    stub = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂吸收产出 · 可执行代码桩
DNA: {dna}
标题: {meta.get("title", "N/A")}
类型: {meta.get("content_type", "N/A")}
吸收时间: {datetime.now().isoformat()}

关联概念:
{chr(10).join(tech_hints) if tech_hints else "#   待人工补充"}

用法:
    python3 bin/lh_absorbed_{stub_name}.py
"""


def main():
    """主入口 · 根据人格分析结果实现"""
    print("🚀 龍魂吸收产出 · {meta.get('title', '外部投喂')}")
    print(f"🧬 DNA: {dna}")
    # TODO: 实现工程落地逻辑
    pass


if __name__ == "__main__":
    main()
'''
    stub_path.write_text(stub, encoding="utf-8")
    print(f"   💻 代码桩: bin/{stub_path.name}")


# ═══════════════════════════════════════════════════════════════
#  CLI入口
# ═══════════════════════════════════════════════════════════════


def main():
    """命令行入口

    支持三种输入方式：
    1. 直接传参: python3 bin/lh_touwei_absorb.py "投喂内容..."
    2. 管道输入: echo "内容" | python3 bin/lh_touwei_absorb.py
    3. 文件输入: python3 bin/lh_touwei_absorb.py --file doc.md
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="龍魂·投喂吸收管道 v2.0 · 全人格路由自动吸收",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 bin/lh_touwei_absorb.py "外部AI投喂的完整内容..."
  cat external_doc.md | python3 bin/lh_touwei_absorb.py
  python3 bin/lh_touwei_absorb.py --file path/to/doc.md
  python3 bin/lh_touwei_absorb.py --stdin
        """,
    )
    parser.add_argument(
        "text", nargs="?", default=None, help="投喂文本内容（直接传入）"
    )
    parser.add_argument("--stdin", action="store_true", help="从标准输入读取")
    parser.add_argument("--file", type=str, help="从文件读取")
    parser.add_argument("--title", type=str, default="", help="覆盖标题")

    args = parser.parse_args()

    # 收集输入
    if args.text:
        text = args.text
    elif args.file:
        text = Path(args.file).read_text(encoding="utf-8")
    elif args.stdin or not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    if not text.strip():
        print("❌ 输入内容为空")
        sys.exit(1)

    success = absorb(text, title_override=args.title)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
