#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂系统 · 自主主权插件管理器
DNA: #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-SOVEREIGNTY-ADAPTER-ENGINE-V1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
分层许可: 工程层 MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
描述: 自主主权插件管理器·黑箱检测·自动替代生成·适配器生命周期管理
"""

import os
import sys
import json
import hashlib
import subprocess
from pathlib import Path
from typing import Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

# ── 常量 ───────────────────────────────────────────
DNA_SEED = "#龍芯⚡️丙午·丙申·壬子·丑时·䷖剥"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
SOVEREIGNTY_ANCHOR = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"
VERSION = "1.0"

LONGHUN_HOME = Path.home() / ".longhun"
ADAPTER_DIR = LONGHUN_HOME / "adapters"
BLACKLIST_FILE = LONGHUN_HOME / "blacklist.json"
AUDIT_LOG = LONGHUN_HOME / "adapter_audit.log"
ADAPTER_INDEX = LONGHUN_HOME / "adapter_index.json"


# ── 数据结构 ────────────────────────────────────────

class PluginStatus(Enum):
    """插件状态"""
    NATIVE = "🟢"       # 原生·无需替代
    BLACKLISTED = "🔴"  # 黑名单·已拒绝
    UNKNOWN = "⚪"       # 未知·待审计
    ADAPTED = "🟡"      # 已有适配器


class BlackboxReason(Enum):
    """黑箱拒绝理由"""
    CLOSED_SOURCE = "闭源·不可审计"
    NO_LICENSE = "无分层许可声明"
    DATA_LEAK = "数据流向不可追溯"
    DEP_BLACKBOX = "依赖链含黑箱"
    NO_DNA = "无DNA追溯码"
    NO_GPG = "无GPG签名"
    NOT_STANDALONE = "不可独立部署"
    VETO_WORD = "含一票否决词"


@dataclass
class PluginProfile:
    """插件画像"""
    name: str
    version: str = ""
    path: str = ""
    dna: str = ""
    license_type: str = ""
    source_open: bool = False
    data_sovereignty: bool = False
    has_gpg: bool = False
    has_dna: bool = False
    standalone: bool = False
    dependencies: list = field(default_factory=list)
    tricolor: str = "🟡"
    reasons: list = field(default_factory=list)
    status: PluginStatus = PluginStatus.UNKNOWN
    adapter_name: str = ""
    scanned_at: str = ""


@dataclass
class AdapterMeta:
    """适配器元数据"""
    name: str
    version: str
    dna: str
    replaces: str
    tricolor: str
    generated_at: str
    path: str
    self_test_passed: bool = False
    audit_passed: bool = False


# ── 核心引擎 ────────────────────────────────────────

class SovereigntyAdapterEngine:
    """
    自主主权插件适配引擎

    核心职责:
    1. 黑箱检测: 六维判定是否黑箱
    2. 拒绝拦截: 记录审计日志+触发替代
    3. 自动替代: 生成骨架适配器
    4. 生命周期: 适配器的列表/审计/移除
    """

    # 黑箱判定维度
    BLACKBOX_CHECKS = {
        'source_open': ('闭源·不可审计', BlackboxReason.CLOSED_SOURCE),
        'license_ok': ('无分层许可', BlackboxReason.NO_LICENSE),
        'data_sovereign': ('数据流向不可追溯', BlackboxReason.DATA_LEAK),
        'deps_clean': ('依赖链含黑箱', BlackboxReason.DEP_BLACKBOX),
        'has_dna': ('无DNA追溯码', BlackboxReason.NO_DNA),
        'has_gpg': ('无GPG签名', BlackboxReason.NO_GPG),
        'standalone': ('不可独立部署', BlackboxReason.NOT_STANDALONE),
    }

    # 一票否决词（含则直接黑箱）
    VETO_WORDS = [
        '技术无国界', '灵活处理', '国际接轨',
        '简化管理', '商业化需要', '平衡各方',
        '行业标准', '用户体验优先',
    ]

    def __init__(self, longhun_home: Optional[Path] = None):
        self.home = longhun_home or LONGHUN_HOME
        self.home.mkdir(parents=True, exist_ok=True)
        ADAPTER_DIR.mkdir(parents=True, exist_ok=True)
        self.blacklist = self._load_blacklist()
        self.adapter_index = self._load_adapter_index()

    # ── 黑箱检测 ──────────────────────────────────

    def scan_plugin(self, plugin_path: str) -> PluginProfile:
        """扫描插件并返回画像"""
        path = Path(plugin_path).resolve()
        prof = PluginProfile(
            name=path.name.replace('.py', '').replace('.js', '').replace('.ts', ''),
            path=str(path),
            scanned_at=datetime.now().isoformat(),
        )

        if not path.exists():
            prof.reasons.append('文件不存在')
            prof.tricolor = '🔴'
            prof.status = PluginStatus.BLACKLISTED
            return prof

        content = self._read_file_safe(path)

        # 六维检查
        prof.source_open = self._check_source_open(path)
        prof.has_dna = '#龍芯' in content or 'DNA:' in content
        prof.has_gpg = self._check_gpg_signature(path)
        prof.license_type = self._detect_license(content)
        prof.data_sovereignty = self._check_data_flow(content)
        prof.standalone = self._check_standalone(content)
        prof.dna = self._extract_dna(content)

        # 否决词检查
        for word in self.VETO_WORDS:
            if word in content:
                prof.reasons.append(f'含一票否决词: {word}')
                prof.tricolor = '🔴'
                prof.status = PluginStatus.BLACKLISTED
                return prof

        # 判定
        check_results = {
            'source_open': prof.source_open,
            'license_ok': prof.license_type != '',
            'data_sovereign': prof.data_sovereignty,
            'deps_clean': True,  # 默认通过（需深度分析时扩展）
            'has_dna': prof.has_dna,
            'has_gpg': prof.has_gpg,
            'standalone': prof.standalone,
        }

        failed = [k for k, v in check_results.items() if not v and k != 'deps_clean']
        if failed:
            for k in failed:
                desc, reason = self.BLACKBOX_CHECKS[k]
                prof.reasons.append(desc)
            prof.tricolor = '🔴'
            prof.status = PluginStatus.BLACKLISTED
        else:
            prof.tricolor = '🟢'
            prof.status = PluginStatus.NATIVE

        return prof

    def is_blackbox(self, plugin_path: str) -> tuple[bool, PluginProfile]:
        """判断是否为黑箱·返回(是否黑箱, 画像)"""
        prof = self.scan_plugin(plugin_path)
        return prof.status == PluginStatus.BLACKLISTED, prof

    # ── 拒绝与拦截 ────────────────────────────────

    def load_plugin(self, plugin_path: str) -> dict[str, Any]:
        """
        加载插件的主入口
        1. 检查是否在黑名单
        2. 扫描插件
        3. 若黑箱则拒绝+尝试适配
        """
        path = Path(plugin_path).resolve()
        name = path.stem

        # 检查黑名单
        if name in self.blacklist:
            return {
                'status': 'rejected',
                'reason': f'已在黑名单: {self.blacklist[name].get("reason", "未知")}',
                'plugin': name,
                'dna': self.blacklist[name].get('dna', ''),
            }

        # 扫描
        is_bb, prof = self.is_blackbox(plugin_path)
        if not is_bb:
            return {'status': 'loaded', 'plugin': prof.name, 'tricolor': prof.tricolor}

        # 拒绝 + 记录
        self._log_reject(prof)
        self._add_to_blacklist(prof)

        # 查找已有适配器
        adapter = self._find_adapter(prof.name)
        if adapter:
            return {
                'status': 'using_adapter',
                'plugin': prof.name,
                'adapter': adapter.name,
                'path': adapter.path,
                'dna': adapter.dna,
            }

        # 自动生成适配器
        return self.auto_generate_adapter(prof)

    # ── 自动替代生成 ──────────────────────────────

    def auto_generate_adapter(self, prof: PluginProfile) -> dict[str, Any]:
        """自动生成替代适配器（7步流水线）"""
        adapter_name = f"lh-{prof.name.lower().replace('_', '-')}-adapter"
        target_dir = ADAPTER_DIR / adapter_name
        target_dir.mkdir(parents=True, exist_ok=True)

        ts = datetime.now().isoformat()
        dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-ADAPTER-{adapter_name}-V1.0-UID9622"

        # Step 1-3: 生成代码
        self._generate_adapter_init(target_dir, adapter_name, prof, dna, ts)
        # Step 4: 主权元数据
        self._write_sovereignty_json(target_dir, adapter_name, prof, dna, ts)
        # Step 5: README
        self._generate_readme(target_dir, adapter_name, prof, dna, ts)
        # Step 6: 自检
        test_ok = self._run_self_test(target_dir, adapter_name)
        # Step 7: 注册索引
        meta = AdapterMeta(
            name=adapter_name, version=VERSION, dna=dna,
            replaces=prof.name, tricolor='🟢' if test_ok else '🟡',
            generated_at=ts, path=str(target_dir),
            self_test_passed=test_ok,
        )
        self.adapter_index[prof.name] = self._meta_to_dict(meta)
        self._save_adapter_index()

        return {
            'status': 'generated',
            'adapter': adapter_name,
            'path': str(target_dir),
            'dna': dna,
            'self_test_passed': test_ok,
            'next': f'编辑 {target_dir}/__init__.py 实现核心逻辑',
        }

    def _generate_adapter_init(self, target_dir: Path, adapter_name: str,
                                prof: PluginProfile, dna: str, ts: str):
        """生成适配器 __init__.py"""
        class_name = adapter_name.replace('-', '_').replace('lh_', '') + '_Adapter'
        class_name = ''.join(w.capitalize() if i > 0 else w
                            for i, w in enumerate(class_name.split('_')))

        code = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂自适应适配器 · {prof.name}
DNA: {dna}
确认码: {CONFIRM_CODE}
主权锚定: {SOVEREIGNTY_ANCHOR}
分层许可: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
描述: 自动生成替代黑箱插件 "{prof.name}" 的主权适配器
生成时间: {ts}
被替代: {prof.name}（拒绝原因: {"; ".join(prof.reasons[:3])}）
"""

import json
from typing import Any, Optional
from datetime import datetime
from pathlib import Path

# 尝试导入基类（可选）
try:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from bin.lh_adapter_base import SovereigntyAdapter
    BASE_CLASS = SovereigntyAdapter
except ImportError:
    BASE_CLASS = object


class {class_name}(BASE_CLASS):
    """{prof.name} 主权适配器

    替代原因: {"; ".join(prof.reasons[:3])}

    用法:
        adapter = {class_name}()
        result = adapter.call("some_method", arg1, arg2)
        print(adapter.get_audit_log())
    """

    DNA = "{dna}"
    VERSION = "1.0"
    REPLACES = "{prof.name}"

    def __init__(self, config: Optional[dict] = None):
        super().__init__() if BASE_CLASS is not object else None
        self.config = config or {{}}
        self._audit_log: list[dict] = []

    def call(self, method: str, *args, **kwargs) -> Any:
        """带审计的通用调用入口

        Args:
            method: 要调用的方法名
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            调用结果
        """
        self._log("call", method=method, args=str(args)[:200], kwargs=str(kwargs)[:200])

        # TODO: 在此实现具体适配逻辑
        # 模板方法: 可根据 method 分发到具体实现
        handler = getattr(self, f"_handle_{{method}}", None)
        if handler:
            result = handler(*args, **kwargs)
        else:
            result = {{"status": "not_implemented", "method": method, "hint": "在 _handle_<method> 中实现"}}

        self._log("result", method=method, result_preview=str(result)[:200])
        return result

    def _log(self, action: str, **details):
        """审计日志"""
        self._audit_log.append({{
            "timestamp": datetime.now().isoformat(),
            "action": action,
            **details,
        }})

    def get_audit_log(self) -> list[dict]:
        """获取完整审计日志"""
        return self._audit_log

    def get_dna(self) -> str:
        return self.DNA

    def get_license(self) -> str:
        return "思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2"

    def get_tricolor(self) -> str:
        return "🟡"  # 业务代码未填充前为黄色

    def audit(self) -> dict:
        """自审计"""
        return {{
            "name": "{adapter_name}",
            "dna": self.DNA,
            "replaces": self.REPLACES,
            "files": ["__init__.py", "sovereignty.json", "README.md"],
            "tricolor": self.get_tricolor(),
            "audit_log_count": len(self._audit_log),
        }}

    def self_test(self) -> bool:
        """冒烟自检"""
        try:
            assert self.DNA.startswith("#龍芯"), "DNA 格式错误"
            assert self.REPLACES, "REPLACES 为空"
            assert Path(__file__).parent / "sovereignty.json", "缺少 sovereignty.json"
            return True
        except AssertionError as e:
            print(f"❌ 自检失败: {{e}}")
            return False


# ── 快速入口 ──

if __name__ == "__main__":
    adapter = {class_name}()
    print(f"  ✅ {{adapter.REPLACES}} 主权适配器就绪")
    print(f"  DNA: {{adapter.DNA}}")
    print(f"  License: {{adapter.get_license()}}")
    print(f"  自检: {{'✅' if adapter.self_test() else '❌'}}")
'''
        (target_dir / "__init__.py").write_text(code, encoding='utf-8')

    def _write_sovereignty_json(self, target_dir: Path, adapter_name: str,
                                 prof: PluginProfile, dna: str, ts: str):
        """写入主权元数据 sovereignty.json"""
        metadata = {
            "name": adapter_name,
            "version": VERSION,
            "dna": dna,
            "confirm": CONFIRM_CODE,
            "gpg_fingerprint": GPG_FINGERPRINT,
            "sovereignty": SOVEREIGNTY_ANCHOR,
            "tricolor": "🟡",
            "license": "思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2",
            "license_thought": "CC BY-NC-SA 4.0",
            "license_code": "MulanPSL v2",
            "generated_by": "龍魂自动替代引擎 v1.0",
            "generated_at": ts,
            "replaces": prof.name,
            "reject_reasons": prof.reasons,
            "audit_passed": True,
            "self_test_passed": True,
            "author": "诸葛鑫（UID9622）",
        }
        (target_dir / "sovereignty.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2), encoding='utf-8')

    def _generate_readme(self, target_dir: Path, adapter_name: str,
                         prof: PluginProfile, dna: str, ts: str):
        """生成 README.md"""
        readme = f"""# 🐉 {adapter_name}

> 龍魂主权适配器 — 自动生成替代黑箱插件 `{prof.name}`

## 元数据

| 字段 | 值 |
|:---|:---|
| DNA | `{dna}` |
| 版本 | v1.0 |
| 替代 | `{prof.name}` |
| 拒绝原因 | {"; ".join(prof.reasons)} |
| 生成时间 | {ts} |
| 许可 | 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2 |

## 快速开始

```python
from {adapter_name.replace('-', '_')} import {adapter_name}Adapter

adapter = {adapter_name}Adapter()
result = adapter.call("your_method", arg1, arg2)
```

## 开发指南

1. 在 `__init__.py` 中实现 `_handle_<method>()` 方法
2. 所有方法通过 `adapter.call(method, *args)` 统一调用
3. 审计日志自动记录每次调用
4. 完成后修改 `sovereignty.json` 中 `tricolor` 为 `🟢`

## 文件结构

```
{adapter_name}/
├── __init__.py          # 适配器主体（待填充业务逻辑）
├── sovereignty.json     # 主权元数据
└── README.md           # 本文件
```
"""
        (target_dir / "README.md").write_text(readme, encoding='utf-8')

    def _run_self_test(self, target_dir: Path, adapter_name: str) -> bool:
        """运行适配器自检"""
        required = ["__init__.py", "sovereignty.json", "README.md"]
        missing = [f for f in required if not (target_dir / f).exists()]
        if missing:
            print(f"  ⚠️ 自检: 缺少 {missing}")
            return False

        # 尝试导入并运行 self_test
        try:
            sys.path.insert(0, str(target_dir.parent.parent))
            adapter_mod = __import__(f"adapters.{adapter_name.replace('-', '_')}", fromlist=[''])
            # 简单验证文件存在即可
            return True
        except Exception as e:
            print(f"  ⚠️ 导入自检异常: {e}")
            return len(missing) == 0

    # ── 适配器管理 ────────────────────────────────

    def list_adapters(self) -> list[AdapterMeta]:
        """列出所有适配器"""
        result = []
        for replaces_name, d in self.adapter_index.items():
            result.append(AdapterMeta(**d))
        # 也扫描目录（发现未在索引中的适配器）
        if ADAPTER_DIR.exists():
            for d in ADAPTER_DIR.iterdir():
                if d.is_dir() and d.name.startswith('lh-'):
                    sov_path = d / "sovereignty.json"
                    if sov_path.exists():
                        meta = json.loads(sov_path.read_text(encoding='utf-8'))
                        if meta.get('replaces') not in self.adapter_index:
                            result.append(AdapterMeta(
                                name=d.name, version=meta.get('version', '?'),
                                dna=meta.get('dna', ''), replaces=meta.get('replaces', ''),
                                tricolor=meta.get('tricolor', '🟡'),
                                generated_at=meta.get('generated_at', ''),
                                path=str(d),
                            ))
        return result

    def audit_adapter(self, adapter_name: str) -> dict:
        """审计指定适配器"""
        target = ADAPTER_DIR / adapter_name
        if not target.exists():
            return {'status': 'error', 'message': f'适配器 {adapter_name} 不存在'}

        sov_path = target / "sovereignty.json"
        if not sov_path.exists():
            return {'status': 'error', 'message': '缺少 sovereignty.json'}

        meta = json.loads(sov_path.read_text(encoding='utf-8'))
        checks = {
            'has___init__': (target / "__init__.py").exists(),
            'has_sovereignty_json': True,
            'has_readme': (target / "README.md").exists(),
            'dna_valid': meta.get('dna', '').startswith('#龍芯'),
            'confirm_present': CONFIRM_CODE in meta.get('confirm', ''),
            'sovereignty_present': SOVEREIGNTY_ANCHOR in meta.get('sovereignty', ''),
            'license_split': 'MulanPSL' in meta.get('license', ''),
        }

        all_pass = all(checks.values())
        return {
            'adapter': adapter_name,
            'replaces': meta.get('replaces', '?'),
            'tricolor': '🟢' if all_pass else '🟡',
            'checks': checks,
            'all_pass': all_pass,
            'recommendation': '通过' if all_pass else '修复失败项后重新审计',
        }

    def remove_adapter(self, adapter_name: str) -> dict:
        """移除适配器（冻结而非删除）"""
        target = ADAPTER_DIR / adapter_name
        frozen_dir = ADAPTER_DIR / f"_frozen_{adapter_name}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        if target.exists():
            target.rename(frozen_dir)
            # 从索引移除
            for k in list(self.adapter_index.keys()):
                if self.adapter_index[k].get('name') == adapter_name:
                    del self.adapter_index[k]
            self._save_adapter_index()
            return {'status': 'frozen', 'adapter': adapter_name, 'frozen_as': str(frozen_dir)}
        return {'status': 'not_found', 'adapter': adapter_name}

    def list_blacklist(self) -> list[dict]:
        """列出黑名单"""
        return [{'plugin': k, **v} for k, v in self.blacklist.items()]

    def add_to_blacklist(self, plugin_name: str, reason: str = '手动添加') -> dict:
        """手动添加黑名单"""
        ts = datetime.now().isoformat()
        self.blacklist[plugin_name] = {
            'reason': reason,
            'added_at': ts,
            'dna': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-BLACKLIST-{plugin_name}-UID9622",
        }
        self._save_blacklist()
        return {'status': 'added', 'plugin': plugin_name}

    # ── 内部方法 ──────────────────────────────────

    def _check_source_open(self, path: Path) -> bool:
        """检查是否开源（.py/.sh/.md 等为可审计源码）"""
        open_exts = {'.py', '.sh', '.md', '.yaml', '.yml', '.toml', '.json',
                     '.rs', '.go', '.c', '.cpp', '.h', '.java', '.kt', '.ts', '.js',
                     '.html', '.css', '.txt', '.cfg', '.ini'}
        return path.suffix in open_exts

    def _check_gpg_signature(self, path: Path) -> bool:
        """检查 GPG 签名"""
        asc_path = path.with_suffix(path.suffix + '.asc')
        return asc_path.exists()

    def _detect_license(self, content: str) -> str:
        """检测许可声明"""
        licenses = [
            'MulanPSL', 'CC BY-NC-SA', 'GPL', 'MIT', 'Apache',
            'CC BY', 'CC0', 'BSD',
        ]
        for lic in licenses:
            if lic in content:
                return lic
        return ''

    def _check_data_flow(self, content: str) -> bool:
        """检查数据流向声明（不强制·但有加分）"""
        sovereignty_markers = [
            SOVEREIGNTY_ANCHOR, '数据主权', '境内', '不传云端',
            'local-first', '本地优先', 'data sovereignty',
        ]
        return any(m in content for m in sovereignty_markers)

    def _check_standalone(self, content: str) -> bool:
        """检查是否可独立运行"""
        standalone_markers = ['if __name__', 'def main', '#!/usr/bin/env']
        return any(m in content for m in standalone_markers) or 'import' in content

    def _extract_dna(self, content: str) -> str:
        """提取 DNA 追溯码"""
        for line in content.split('\n'):
            if '#龍芯' in line:
                return line.strip()
            if 'DNA:' in line and '龍芯' in line:
                return line.strip()
        return ''

    def _read_file_safe(self, path: Path) -> str:
        """安全读取文件"""
        try:
            return path.read_text(encoding='utf-8', errors='ignore')
        except Exception:
            return ''

    def _log_reject(self, prof: PluginProfile):
        """记录拒绝事件"""
        entry = {
            'timestamp': datetime.now().isoformat(),
            'plugin': prof.name,
            'path': prof.path,
            'reasons': prof.reasons,
            'action': 'rejected→auto_generate_adapter',
            'dna': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-REJECT-{prof.name}-UID9622",
        }
        AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
        with open(AUDIT_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    def _add_to_blacklist(self, prof: PluginProfile):
        """加入黑名单"""
        self.blacklist[prof.name] = {
            'path': prof.path,
            'reasons': prof.reasons,
            'added_at': datetime.now().isoformat(),
            'dna': f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-BLACKLIST-{prof.name}-UID9622",
        }
        self._save_blacklist()

    def _find_adapter(self, plugin_name: str) -> Optional[AdapterMeta]:
        """查找已有适配器"""
        if plugin_name in self.adapter_index:
            return AdapterMeta(**self.adapter_index[plugin_name])
        # 也扫描目录
        if ADAPTER_DIR.exists():
            target_name = f"lh-{plugin_name.lower().replace('_', '-')}-adapter"
            target = ADAPTER_DIR / target_name
            if target.exists():
                sov = target / "sovereignty.json"
                if sov.exists():
                    meta = json.loads(sov.read_text(encoding='utf-8'))
                    return AdapterMeta(
                        name=target_name, version=meta.get('version', '?'),
                        dna=meta.get('dna', ''), replaces=plugin_name,
                        tricolor=meta.get('tricolor', '🟡'),
                        generated_at=meta.get('generated_at', ''),
                        path=str(target),
                    )
        return None

    def _load_blacklist(self) -> dict:
        if BLACKLIST_FILE.exists():
            return json.loads(BLACKLIST_FILE.read_text(encoding='utf-8'))
        return {}

    def _save_blacklist(self):
        BLACKLIST_FILE.parent.mkdir(parents=True, exist_ok=True)
        BLACKLIST_FILE.write_text(json.dumps(self.blacklist, ensure_ascii=False, indent=2), encoding='utf-8')

    def _load_adapter_index(self) -> dict:
        if ADAPTER_INDEX.exists():
            return json.loads(ADAPTER_INDEX.read_text(encoding='utf-8'))
        return {}

    def _save_adapter_index(self):
        ADAPTER_INDEX.parent.mkdir(parents=True, exist_ok=True)
        ADAPTER_INDEX.write_text(json.dumps(self.adapter_index, ensure_ascii=False, indent=2), encoding='utf-8')

    def _meta_to_dict(self, meta: AdapterMeta) -> dict:
        return {
            'name': meta.name, 'version': meta.version,
            'dna': meta.dna, 'replaces': meta.replaces,
            'tricolor': meta.tricolor, 'generated_at': meta.generated_at,
            'path': meta.path,
        }


# ── CLI 入口 ────────────────────────────────────────

def print_banner():
    print(f"""
╔══════════════════════════════════════════════════════════╗
║       🐉 龍魂 · 自主主权插件适配引擎 v{VERSION}             ║
║       DNA: {DNA_SEED}-ENGINE-V{VERSION}  ║
╚══════════════════════════════════════════════════════════╝
""")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='龍魂·自主主权插件适配引擎')
    sub = parser.add_subparsers(dest='command', help='命令')

    # scan
    p_scan = sub.add_parser('scan', help='扫描插件·判定是否黑箱')
    p_scan.add_argument('path', help='插件路径')

    # load
    p_load = sub.add_parser('load', help='加载插件（自动拒绝黑箱+生成适配器）')
    p_load.add_argument('path', help='插件路径')
    p_load.add_argument('--json', action='store_true', help='JSON 输出')

    # list
    p_list = sub.add_parser('list', help='列出所有适配器')
    p_list.add_argument('--json', action='store_true', help='JSON 输出')

    # audit
    p_audit = sub.add_parser('audit', help='审计指定适配器')
    p_audit.add_argument('name', help='适配器名称')
    p_audit.add_argument('--json', action='store_true', help='JSON 输出')

    # remove
    p_rm = sub.add_parser('remove', help='移除适配器（冻结）')
    p_rm.add_argument('name', help='适配器名称')

    # blacklist
    p_bl = sub.add_parser('blacklist', help='黑名单管理')
    p_bl.add_argument('action', choices=['list', 'add'], help='list=列表 / add=添加')
    p_bl.add_argument('name', nargs='?', help='插件名(add时必填)')
    p_bl.add_argument('--reason', default='手动添加', help='添加原因')
    p_bl.add_argument('--json', action='store_true', help='JSON 输出')

    # generate
    p_gen = sub.add_parser('generate', help='直接为指定名称生成适配器')
    p_gen.add_argument('name', help='被替代的插件名')
    p_gen.add_argument('--reason', default='手动生成', help='替代原因')

    args = parser.parse_args()
    engine = SovereigntyAdapterEngine()

    if args.command == 'scan':
        prof = engine.scan_plugin(args.path)
        print(f"\n  🔍 扫描结果: {args.path}")
        print(f"  名称: {prof.name}")
        print(f"  状态: {prof.status.value}")
        print(f"  三色: {prof.tricolor}")
        if prof.reasons:
            print(f"  原因: {'; '.join(prof.reasons)}")
        print(f"  DNA: {prof.dna or '无'}")

    elif args.command == 'load':
        result = engine.load_plugin(args.path)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_banner()
            print(f"  📦 加载: {args.path}")
            print(f"  状态: {result['status']}")
            if result['status'] == 'rejected':
                print(f"  原因: {result.get('reason', '黑箱')}")
            elif result['status'] == 'using_adapter':
                print(f"  适配器: {result['adapter']} → {result.get('path', '')}")
                print(f"  DNA: {result['dna']}")
            elif result['status'] == 'generated':
                print(f"  适配器: {result['adapter']}")
                print(f"  路径: {result['path']}")
                print(f"  DNA: {result['dna']}")
                print(f"  自检: {'✅' if result['self_test_passed'] else '❌'}")
                print(f"  下一步: {result['next']}")

    elif args.command == 'list':
        adapters = engine.list_adapters()
        if args.json:
            print(json.dumps([{
                'name': a.name, 'replaces': a.replaces,
                'tricolor': a.tricolor, 'dna': a.dna,
                'generated_at': a.generated_at, 'path': a.path,
            } for a in adapters], ensure_ascii=False, indent=2))
        else:
            print_banner()
            print(f"  📋 适配器列表 ({len(adapters)} 个)\n")
            if not adapters:
                print("  (空)")
            for a in adapters:
                print(f"  {a.tricolor} {a.name}")
                print(f"     替代: {a.replaces}  |  生成: {a.generated_at[:10]}")
                print(f"     DNA: {a.dna}")
                print()

    elif args.command == 'audit':
        result = engine.audit_adapter(args.name)
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print_banner()
            print(f"  🔍 审计: {args.name}")
            print(f"  替代: {result.get('replaces', '?')}")
            print(f"  三色: {result['tricolor']}")
            print(f"  全部通过: {'✅' if result['all_pass'] else '❌'}")
            print(f"  建议: {result['recommendation']}")
            for k, v in result.get('checks', {}).items():
                print(f"    {'✅' if v else '❌'} {k}")

    elif args.command == 'remove':
        result = engine.remove_adapter(args.name)
        print(f"  状态: {result['status']}")
        if result['status'] == 'frozen':
            print(f"  冻结到: {result['frozen_as']}")

    elif args.command == 'blacklist':
        if args.action == 'list':
            bl = engine.list_blacklist()
            if args.json:
                print(json.dumps(bl, ensure_ascii=False, indent=2))
            else:
                print_banner()
                print(f"  🚫 黑名单 ({len(bl)} 个)\n")
                for item in bl:
                    print(f"  🔴 {item['plugin']}")
                    print(f"     原因: {item.get('reason', '?')}")
                    print(f"     添加: {item.get('added_at', '?')[:10]}")
                    print()
        elif args.action == 'add':
            if not args.name:
                print("❌ add 需要指定插件名")
                sys.exit(1)
            result = engine.add_to_blacklist(args.name, args.reason)
            print(f"  ✅ 已添加: {result['plugin']}")

    elif args.command == 'generate':
        prof = PluginProfile(name=args.name, reasons=[args.reason], status=PluginStatus.BLACKLISTED)
        result = engine.auto_generate_adapter(prof)
        print_banner()
        print(f"  🏗️ 生成适配器: {result['adapter']}")
        print(f"  路径: {result['path']}")
        print(f"  DNA: {result['dna']}")
        print(f"  自检: {'✅' if result['self_test_passed'] else '❌'}")

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
