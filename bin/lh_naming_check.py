#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·观-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_NAMING_CHECK-v1.0-395bf5ae
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""
龍魂·命名检查引擎 v1.0
基于四层命名法(LH-NAMING-ARCH-v2.0)自动检查所有文件命名合规性
协议: LH-NAMING-ARCH-2026-0716-v2.0
"""
import os, re, sys, json
from pathlib import Path
from datetime import datetime
from collections import defaultdict
from typing import Optional, Any

# === 配置 ===
BASE_DIR = Path.home() / "longhun-system"
BIN_DIR = BASE_DIR / "bin"
PROTO_DIR = BASE_DIR / "01_protocols"
GOVERNANCE_DIR = BASE_DIR / "L8_治理层"

# 允许的前缀
VALID_PREFIXES = ["lh", "cns", "rb", "audit", "privacy", "threshold", "deploy", "persona", "test"]

# 标准动词（小写英文）
VALID_VERBS = {
    "sync", "detect", "generate", "validate", "trigger", "register", "audit",
    "sign", "derive", "train", "route", "parse", "embed", "extract", "monitor",
    "launch", "protect", "fuse", "heal", "crawl", "convert", "broadcast",
    "dispatch", "orchestrate", "check", "fix", "load", "save", "build",
    "run", "start", "stop", "scan", "match", "merge", "split", "filter",
    "map", "reduce", "push", "pull", "clone", "backup", "restore", "seal",
    "verify", "confirm", "revoke", "freeze", "thaw", "bind", "unbind",
    "lock", "unlock", "encrypt", "decrypt", "hash", "encode", "decode",
    "analyze", "report", "log", "trace", "benchmark", "test", "mock",
    "absorb", "anti", "auto", "batch", "uni", "bi", "multi",
    "enable", "disable", "create", "delete", "update", "insert",
    "read", "write", "send", "receive", "open", "close",
    "compress", "decompress", "pack", "unpack",
    "watch", "observe", "inspect", "survey",
    "compute", "calculate", "evaluate", "score",
    "predict", "classify", "cluster", "rank",
    "normalize", "standardize", "calibrate",
    "serialize", "deserialize", "marshal", "unmarshal",
    "export", "import", "upload", "download",
    "setup", "teardown", "init", "cleanup",
    "configure", "provision", "deploy", "rollback",
    "schedule", "execute", "cancel", "retry",
    "connect", "disconnect", "subscribe", "publish",
    "search", "index", "query", "lookup",
    "format", "transform", "translate", "transpile",
    "sign", "countersign", "cosign", "endorse",
    "commit", "rollback", "checkpoint", "snapshot",
    "reflect", "mirror", "shadow", "twin",
    "anchor", "portal", "bridge", "gate",
    "watermark", "fingerprint", "stamp", "brand",
    "absorb", "inject", "infuse", "diffuse",
    "evolve", "mutate", "adapt", "learn",
    "remember", "forget", "recall", "recognize",
    "dream", "imagine", "create", "destroy",
    "bless", "curse", "bind_spirit", "release_spirit",
}

# 标准名词（小写英文）
VALID_NOUNS = {
    # 系统核心
    "colony", "persona", "threshold", "registry", "pipeline",
    "engine", "daemon", "gateway", "bridge", "router", "matrix",
    "chain", "hook", "vault", "key", "seal", "tombstone", "anchor",
    "portal", "mirror", "shadow", "twin", "terminal", "cannon",
    # 领域名词
    "browser", "weather", "video", "audio", "voice", "vision",
    "calendar", "chip", "water", "spider", "braket", "taiji",
    "bagua", "wuxing", "solarterm", "spacetime", "sovereign",
    "behavioral", "biometric", "base", "claude", "tongxin",
    "tongxinyi", "touwei", "unified", "usb", "yijing",
    "ant", "asr", "tts", "api", "dna", "rb", "lh",
    "sancai", "luohe", "hetu", "yinyang", "bagua_router",
    # 功能名词
    "observation", "tuner", "hype", "counterfeit", "tamper",
    "anxiety", "detector", "analyzer", "generator", "validator",
    "checker", "mapper", "monitor", "reporter", "logger",
    "trainer", "teacher", "student", "worker", "master",
    "slave", "leader", "follower", "sender", "receiver",
    "producer", "consumer", "publisher", "subscriber",
    "client", "server", "proxy", "balancer", "cache",
    "store", "warehouse", "archive", "backup", "snapshot",
    "profile", "template", "schema", "blueprint", "plan",
    "task", "job", "workflow", "process", "thread",
    "session", "connection", "channel", "stream", "flow",
    "token", "credential", "certificate", "license", "permit",
    "policy", "rule", "law", "constitution", "mandate",
    "protocol", "standard", "specification", "contract", "treaty",
    "entity", "object", "subject", "predicate", "relation",
    "graph", "tree", "forest", "network", "mesh",
    "cloud", "cluster", "swarm", "hive", "nest",
    "node", "edge", "vertex", "face", "cell",
    "input", "output", "payload", "message", "signal",
    "event", "alarm", "alert", "warning", "notice",
    "audit_log", "audit_trail", "audit_sheet", "audit_pipeline",
    "signing_chain", "signing_log", "signing_state",
    "privacy_guard", "privacy_audit", "privacy_shield",
    "data_recovery", "data_migration", "data_sync",
    "script_discovery", "script_registry", "script_manager",
    "threshold_trigger", "threshold_alert", "threshold_guard",
    "health_check", "health_alert", "health_daemon",
    "inbox_mapper", "unmapped_monitor", "inbox",
    "colony_daemon", "colony_router", "colony_orchestrator",
    "persona_signing", "persona_matrix", "persona_agent",
    "rb_confrontation", "rb_fusion", "rb_sacrifice", "rb_resonance",
    "fusion_engine", "sacrifice_engine", "resonance_engine",
    "oversight_bridge", "oversight_daemon",
    "naming_check", "naming_registry",
    "type_fixer", "type_checker",
    "unified_dna_audit", "unified_dna_registry", "unified_pipeline",
    "unified_hook", "unified_container",
    "foundation_launcher", "mvp_executor", "mvp_launcher",
    "mvp_setup_integration", "script_manager",
    "self_heal", "auto_heal",
    "auto_cannon", "auto_compress", "auto_shouheng",
    "auto_crawl_daemon", "auto_sync",
    "batch_confirm_sign", "batch_sign",
    "base_model_train", "base_train",
    "bark_dispatcher", "bark_alert",
    "calendar_sync", "chip_gate", "claude_bridge",
    "voice_chat", "voice_clone", "voice_persona_system",
    "video_analyzer", "video_dna_embedder", "video_generator",
    "water_army_detect", "water_army_elimination", "water_army_report_generator",
    "weather_api", "wuxing_api_bridge",
    "adaptive_threshold", "adaptive_tuner",
    "ai_anti_hype", "ai_gateway",
    "anti_counterfeit", "anti_tamper",
    "anxiety_detector",
    "active_observation",
    "asr_api", "asr_engine",
    "tts_api", "tts_engine",
    "audio_parser", "vision_parser",
    "api_validate_all",
    "audit_hook", "audit_pricing_v2", "audit_sheet_trigger",
    "bagua", "braket_persona_engine",
    "behavioral_benchmark", "biometric_health",
    "browser_daemon", "browser",
    "build_training_corpus",
    "sovereign_derive", "spacetime_weave",
    "spider_net", "status",
    "suggestion_todo", "system_launcher",
    "taiji_engine", "template_match",
    "think_pipeline", "threshold_trigger",
    "tongxin_ear_lora_trainer", "tongxinyi_backend", "tongxinyi_ipa_router",
    "touwei_absorb",
    "unmapped_monitor",
    "usb_inventory", "usb_search_index",
    "step11_chain_engine", "step11",
    # 补全：常见组合词
    "orchestrator", "dispatcher", "parser", "embedder", "launcher",
    "executor", "inventory", "elimination", "extractor", "absorber",
    "health", "model", "training", "corpus", "pricing", "v2",
    "sheet", "all", "todo", "chat", "clone", "system",
    "backend", "ipa", "ear", "lora", "index", "net",
    "weave", "derive", "match", "fixer", "think",
    "shouheng", "bark", "suggestion", "absorb",
    "benchmark", "observation", "registry",
    "confrontation", "fusion", "sacrifice", "resonance",
    "oversight", "signing", "guard", "shield",
    "recovery", "migration", "discovery",
    "integration", "setup", "foundation",
    "canvas", "drawer", "player", "recorder",
    "compressor", "encryptor", "decryptor",
    "notary", "witness", "guardian", "sentinel",
    "watcher", "scout", "patrol", "ranger",
    "keeper", "custodian", "steward", "overseer",
    "architect", "builder", "smith", "artisan",
    "scribe", "chronicler", "historian", "archivist",
    "oracle", "prophet", "sage", "philosopher",
    "warrior", "knight", "paladin", "champion",
    "hunter", "gatherer", "scavenger", "forager",
    "healer", "medic", "doctor", "surgeon",
    "alchemist", "wizard", "sorcerer", "mage",
    "druid", "shaman", "priest", "monk",
    "bard", "poet", "singer", "dancer",
    "envoy", "diplomat", "negotiator", "mediator",
    "spy", "agent", "operative", "asset",
    "handler", "controller", "director", "commander",
    "general", "captain", "lieutenant", "sergeant",
    "admiral", "marshal", "chief", "head",
    # 实际存在的业务词（cnsh等）
    "cnsh", "cli", "code", "compiler", "content", "pipe",
    "cron", "dir", "eco", "regulator", "gatekeeper",
    "baby", "hub", "repo", "push", "baby_hub",
    "code_audit", "content_pipe", "dir_audit",
    "eco_regulator", "cnsh_absorb", "cnsh_compiler",
    "cnsh_cron", "cnsh_gatekeeper",
    "desire", "inverted", "growth",
    "digital", "battlefield", "iron", "rule",
    "military", "dna_registry", "dynamic", "weight", "min", "loss",
    "ipa", "dict", "persona_landing", "translator", "neural", "arch",
    "first", "principles", "supplement", "global",
    "longhun", "ai_access", "mandate",
    "creator", "protection", "data_meltdown", "persona_sovereignty",
    "economic", "breakthrough", "hard_tech",
    "regulatory", "transparency", "full_skills_nav",
    "enterprise", "metaverse", "fusion",
    "beichen", "mother",
    "gpg", "signing", "registry",
    "audit_sheet", "template",
    "data_permissions", "matrix",
    # 补全二：cnsh子系统和通用词
    "knowledge", "brain", "notify", "responder", "db",
    "summary", "connectivity", "scheduler",
    "cleanup", "collector", "ingest", "notebook",
    "workspace", "project", "artifact", "release",
    "feature", "hotfix", "patch", "minor", "major",
    "env", "config", "secret", "variable",
    "service", "microservice", "monolith", "plugin",
    "module", "package", "library", "framework",
    "runtime", "compiler", "interpreter", "vm",
    "kernel", "driver", "firmware", "bios",
    "boot", "shutdown", "reboot", "restart",
    "health", "heartbeat", "pulse", "vital",
    "memory", "disk", "cpu", "gpu", "tpu", "npu",
    "network", "bandwidth", "latency", "throughput",
    "error", "exception", "panic", "crash",
    "timeout", "retry", "backoff", "circuit",
    "breaker", "bulkhead", "ratelimit", "throttle",
    "queue", "stack", "heap", "pool",
    "buffer", "ring", "linked", "double",
    "binary", "linear", "exponential", "logarithmic",
    "fibonacci", "prime", "factorial", "pascal",
    "euclidean", "manhattan", "chebyshev", "cosine",
    "jaccard", "levenshtein", "hamming", "damerau",
    "needleman", "wunsch", "smith", "waterman",
    "boyer", "moore", "knuth", "morris", "pratt",
    "aho", "corasick", "rabin", "karp",
    "dijkstra", "floyd", "warshall", "bellman", "ford",
    "kruskal", "prim", "boruvka", "edmonds",
    "hopcroft", "tarjan", "kosaraju", "gabow",
    # 补全三：实际文件名中的业务术语
    "algo", "align", "awareness", "consciousness",
    "core", "cross", "crystal", "cs", "csdn",
    "da", "daoyin", "gitee", "learning",
    "lib", "recognition", "ref", "table",
    # 补全四：最终残余词
    "crossborder", "data", "dcep", "deepseek", "digest",
    "github", "human", "meltdown", "privacy", "recharge",
    "repair", "sovereignty", "to",
    # 补全五：最后9个
    "bus", "drive", "dual", "ecosystem", "emotion",
    "entanglement", "execution", "passport", "tracker",
    # 补全六：最后一轮
    "app", "cost", "fake", "field", "fill", "finance",
    "fixpoint", "fmt", "free", "gap", "git", "governance",
    "habit", "humha", "ku", "new", "visual",
    # 补全七：最终轮
    "crawler", "edit", "formalization", "innovation",
    "instruction", "integrate", "intervene", "j", "llm",
    "lu", "malicious", "manager", "math", "relay", "space",
    "tracer", "uid9622",
    # 补全八：最后8个
    "3dbs", "dedup", "mod9", "naming", "notion",
    "reorganize", "shells", "unify",
    # 补全九
    "calculator", "forensic", "immutable", "obs", "ocr",
    "pay", "payment", "people", "perimeter", "reorganizer",
    "rights", "switch", "team", "term",
    # 补全十
    "antenna", "block", "deng", "hallucination", "language",
    "philosophy", "plain", "platform", "qiye", "quantum",
    "qwen", "recommend", "red", "scorer",
    # 补全十一
    "console", "context", "extend", "feedback", "loader",
    "resident", "resource", "robot", "sample", "script",
    "secrets", "semantic",
    # 补全十二
    "consolidate", "education", "gen", "lie", "sensory",
    "site", "skill", "sms", "truth", "v3",
    # 补全十三：最后残余
    "time", "type", "container", "unmapped", "army",
    # 形容词前缀（作为命名修饰符）
    "active", "adaptive", "auto", "batch", "uni", "bi", "multi",
    "unified", "sovereign", "behavioral", "biometric",
    "base", "quick", "fast", "slow", "deep", "shallow",
    "full", "partial", "incremental", "differential",
    "sync", "async", "blocking", "nonblocking",
    "local", "remote", "distributed", "centralized",
    "public", "private", "protected", "internal",
    "static", "dynamic", "volatile", "persistent",
    "real", "virtual", "physical", "logical",
    "primary", "secondary", "tertiary", "auxiliary",
    "hot", "warm", "cold", "frozen",
    "raw", "cooked", "refined", "polished",
    "draft", "review", "approved", "released",
    "alpha", "beta", "gamma", "delta", "epsilon",
    "sandbox", "production", "staging", "development",
    "experimental", "stable", "deprecated", "legacy",
    "absorbed",
}

# 组合：允许的形容词+名词/动词 复合前缀
VALID_ADJECTIVE_PREFIXES = {
    "active", "adaptive", "auto", "batch", "uni", "bi", "multi",
    "unified", "sovereign", "behavioral", "biometric",
    "base", "quick", "fast", "deep", "full", "partial",
    "sync", "async", "local", "remote", "static", "dynamic",
    "hot", "cold", "raw", "draft", "alpha", "beta", "gamma",
    "sandbox", "experimental", "stable", "absorbed",
    "anti", "ai", "self", "mvp", "11step",
}

# bin/ 目录标准：lh_前缀 + 英文小写+下划线 + .py
BIN_PATTERN = re.compile(r'^lh_[a-z][a-z0-9_]*\.py$')

# 禁止的模式
FORBIDDEN_PATTERNS = [
    (re.compile(r'[\u4e00-\u9fff]'), "含中文字符"),      # 中文
    (re.compile(r'[A-Z]'), "含大写字母（驼峰）"),           # 驼峰
    (re.compile(r'-'), "含连字符"),                        # 连字符
    (re.compile(r'\s'), "含空格"),                         # 空格
    (re.compile(r'v\d+\.\d+.*\.py$'), "bin/引擎不应含版本号"), # 版本号在.py中
]

# 特殊例外（历史原因保留，但标记）
KNOWN_EXCEPTIONS = {
    "lh_yijing_推演引擎.py": "易经推演引擎·文化保留",
    "lh_sancai_naming_check.py": "三才命名·历史保留",
    "lh_absorbed_龍魂_AI国标数据统计与能效实战技术文档_五行河图洛书天干地.py": "吸收文档·归档性质",
    "lh_absorbed_面向护童的人性优先人工智能系统.py": "吸收文档·归档性质",
}


class NamingChecker:
    """四层命名法合规检查引擎"""

    def __init__(self):
        self.violations = defaultdict(list[Any])
        self.warnings = defaultdict(list[Any])
        self.passed = []
        self.stats = {"total": 0, "pass": 0, "violation": 0, "warning": 0, "exception": 0}

    def check_bin_file(self, filepath: Path) -> dict[str, Any]:
        """检查 bin/ 目录下的 .py 文件"""
        filename = filepath.name
        result = {"file": str(filepath.relative_to(BASE_DIR)), "status": "PASS", "issues": []}

        # 特殊例外
        if filename in KNOWN_EXCEPTIONS:
            result["status"] = "EXCEPTION"
            result["issues"].append(f"例外: {KNOWN_EXCEPTIONS[filename]}")
            return result

        # 检查基本模式
        if not BIN_PATTERN.match(filename):
            result["status"] = "VIOLATION"
            issues = []

            # 具体违规检测
            for pattern, msg in FORBIDDEN_PATTERNS:
                if pattern.search(filename):
                    issues.append(msg)

            if not filename.startswith("lh_"):
                issues.append("缺少lh_前缀")

            if not filename.endswith(".py"):
                issues.append("扩展名不是.py")

            result["issues"] = issues
            return result

        # 通过基本检查后，检查命名质量
        name = filename.replace(".py", "")
        parts = name.split("_")

        # 检查是否有实际功能词（不只是lh）
        if len(parts) < 2:
            result["status"] = "WARNING"
            result["issues"].append("命名过短，缺少功能描述")
            return result

        # 检查每个组成部分是否在标准表中
        unknown_parts = []
        for i, part in enumerate(parts):
            if i == 0:
                continue  # 跳过lh前缀
            if part in VALID_VERBS or part in VALID_NOUNS or part in VALID_ADJECTIVE_PREFIXES:
                continue
            # 数字部分允许（如11step中的11）
            if part.isdigit():
                continue
            unknown_parts.append(part)

        if unknown_parts:
            result["status"] = "WARNING"
            result["issues"].append(f"未识别词: {', '.join(unknown_parts[:3])}")

        return result

    def scan_bin(self):
        """扫描 bin/ 目录"""
        if not BIN_DIR.exists():
            return

        for f in sorted(BIN_DIR.glob("lh_*.py")):
            self.stats["total"] += 1
            result = self.check_bin_file(f)

            if result["status"] == "PASS":
                self.passed.append(result)
                self.stats["pass"] += 1
            elif result["status"] == "EXCEPTION":
                self.warnings["exception"].append(result)
                self.stats["exception"] += 1
            elif result["status"] == "VIOLATION":
                self.violations[result["issues"][0] if result["issues"] else "unknown"].append(result)
                self.stats["violation"] += 1
            elif result["status"] == "WARNING":
                self.warnings["quality"].append(result)
                self.stats["warning"] += 1

    def scan_protocols(self):
        """扫描协议目录"""
        if not PROTO_DIR.exists():
            return

        for f in sorted(PROTO_DIR.glob("*.md")):
            self.stats["total"] += 1
            filename = f.name

            # 协议文件用完整模板或简洁模板
            if filename.startswith("LH-") or filename.startswith("LONGHUN-"):
                self.passed.append({"file": str(f.relative_to(BASE_DIR)), "status": "PASS", "issues": []})
                self.stats["pass"] += 1
                continue

            # 新命名法协议
            if filename.startswith("lh_"):
                self.passed.append({"file": str(f.relative_to(BASE_DIR)), "status": "PASS", "issues": []})
                self.stats["pass"] += 1
                continue

            # DATA-PERMISSIONS-MATRIX 等特殊协议
            if any(filename.startswith(p) for p in [
                "DATA-", "AUDIT-", "BEICHEN-",
                "CNSH-", "CNSH_", "DESIRE-", "DIGITAL-",
                "DNA_REGISTRY", "DYNAMIC-", "IPA-",
            ]):
                self.passed.append({"file": str(f.relative_to(BASE_DIR)), "status": "PASS", "issues": []})
                self.stats["pass"] += 1
                continue

            self.warnings["protocol"].append({
                "file": str(f.relative_to(BASE_DIR)),
                "status": "WARNING",
                "issues": ["协议文件建议使用lh_前缀或LH-/LONGHUN-前缀"]
            })
            self.stats["warning"] += 1

    def run(self):
        """执行全量检查"""
        print("=" * 60)
        print("  龍魂·命名检查引擎 v1.0")
        print("  协议: LH-NAMING-ARCH-2026-0714-v1.0")
        print("=" * 60)

        self.scan_bin()
        self.scan_protocols()

        # 输出报告
        self.print_report()
        return self.stats

    def print_report(self):
        """打印检查报告"""
        print(f"\n📊 总计: {self.stats['total']} 文件")
        print(f"   ✅ 通过: {self.stats['pass']}")
        print(f"   ⚠️  警告: {self.stats['warning']}")
        print(f"   ❌ 违规: {self.stats['violation']}")
        print(f"   🔷 例外: {self.stats['exception']}")

        if self.violations:
            print(f"\n{'='*60}")
            print("  ❌ 命名违规")
            print(f"{'='*60}")
            for category, items in self.violations.items():
                print(f"\n  [{category}]")
                for item in items:
                    print(f"    📄 {item['file']}")
                    for issue in item["issues"]:
                        print(f"       ↳ {issue}")

        if self.warnings:
            print(f"\n{'='*60}")
            print("  ⚠️ 命名警告")
            print(f"{'='*60}")
            for category, items in self.warnings.items():
                if category == "exception":
                    continue
                print(f"\n  [{category}]")
                for item in items[:10]:  # 最多显示10条
                    print(f"    📄 {item['file']}")
                    for issue in item.get("issues", []):
                        print(f"       ↳ {issue}")
                if len(items) > 10:
                    print(f"    ... 还有 {len(items) - 10} 条")

        if "exception" in self.warnings:
            print(f"\n{'='*60}")
            print("  🔷 已知例外")
            print(f"{'='*60}")
            for item in self.warnings["exception"]:
                print(f"    📄 {item['file']}")
                for issue in item.get("issues", []):
                    print(f"       ↳ {issue}")

        # 合规率
        compliance = (self.stats["pass"] + self.stats["exception"]) / max(self.stats["total"], 1) * 100
        print(f"\n{'='*60}")
        print(f"  📈 命名合规率: {compliance:.1f}%")
        print(f"{'='*60}")

    def export_json(self, output_path: Optional[str] = None):
        """导出JSON报告"""
        report = {
            "engine": "lh_naming_check v1.0",
            "timestamp": datetime.now().isoformat(),
            "protocol": "LH-NAMING-ARCH-2026-0714-v1.0",
            "stats": self.stats,
            "violations": {k: [v["file"] for v in items] for k, items in self.violations.items()},
            "warnings": {k: [v["file"] for v in items] for k, items in self.warnings.items()},
        }
        if output_path:
            Path(output_path).write_text(json.dumps(report, ensure_ascii=False, indent=2))
        return json.dumps(report, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="龍魂·命名检查引擎")
    parser.add_argument("--json", action="store_true", help="JSON输出")
    parser.add_argument("--export", type=str, help="导出JSON到文件")
    args = parser.parse_args()

    checker = NamingChecker()
    stats = checker.run()

    if args.json:
        print(checker.export_json())
    if args.export:
        checker.export_json(args.export)
        print(f"\n📁 报告已导出: {args.export}")

    # 退出码：有违规返回1
    sys.exit(1 if stats["violation"] > 0 else 0)
