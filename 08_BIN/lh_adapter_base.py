#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 主权适配器基类
DNA: #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-ADAPTER-BASE-V1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
主权锚定: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
分层许可: 工程层 MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
描述: 所有龍魂主权适配器的基类·提供审计/签名/自检/生命周期标准接口

用法:
    from bin.lh_adapter_base import SovereigntyAdapter

    class MyAdapter(SovereigntyAdapter):
        DNA = "#龍芯⚡️2026-08-06-ADAPTER-MY-V1.0-UID9622"
        REPLACES = "target_plugin"
"""

import json
import sys
from abc import ABC, abstractmethod
from pathlib import Path
from datetime import datetime
from typing import Any, Optional


# ── 常量 ───────────────────────────────────────────
SOVEREIGNTY_ANCHOR = "#ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL"
CONFIRM_CODE = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


class SovereigntyAdapter(ABC):
    """
    主权适配器基类

    所有龍魂适配器必须继承此类并实现:

    必须覆盖:
        DNA: str        — 适配器DNA追溯码
        REPLACES: str   — 被替代的原始插件名

    可选覆盖:
        VERSION: str    — 版本号（默认 "1.0"）
        _handle_<method> — 具体业务逻辑方法
    """

    # ── 子类必须定义 ──
    DNA: str = ""
    REPLACES: str = ""

    # ── 子类可选覆盖 ──
    VERSION: str = "1.0"

    def __init__(self, config: Optional[dict] = None):
        self.config = config or {}
        self._audit_log: list[dict] = []
        self._init_at = datetime.now().isoformat()
        self._validate()

    def _validate(self):
        """启动时自验证"""
        if not self.DNA:
            raise ValueError(f"{self.__class__.__name__}: DNA 未定义")
        if not self.DNA.startswith('#龍芯'):
            raise ValueError(f"{self.__class__.__name__}: DNA 格式错误，必须以 #龍芯 开头")
        if not self.REPLACES:
            raise ValueError(f"{self.__class__.__name__}: REPLACES 未定义（被替代的插件名）")

    # ── 审计接口 ──────────────────────────────────

    def _log(self, action: str, **details):
        """内部审计日志"""
        self._audit_log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            **details,
        })

    def get_audit_log(self) -> list[dict]:
        """获取完整审计日志"""
        return list(self._audit_log)

    def export_audit(self, fmt: str = 'json') -> str:
        """导出审计日志"""
        if fmt == 'json':
            return json.dumps(self._audit_log, ensure_ascii=False, indent=2)
        elif fmt == 'jsonl':
            return '\n'.join(json.dumps(e, ensure_ascii=False) for e in self._audit_log)
        return str(self._audit_log)

    # ── 主权接口 ──────────────────────────────────

    def get_dna(self) -> str:
        """获取 DNA 追溯码"""
        return self.DNA

    def get_license(self) -> str:
        """获取许可声明"""
        return "思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2"

    def get_sovereignty(self) -> str:
        """获取主权锚定"""
        return SOVEREIGNTY_ANCHOR

    def get_tricolor(self) -> str:
        """获取当前三色状态

        默认 🟡（业务代码未验证）。实现完整后覆盖返回 🟢。
        """
        return "🟡"

    # ── 通用调用入口 ──────────────────────────────

    def call(self, method: str, *args, **kwargs) -> Any:
        """带审计的通用调用入口

        Args:
            method: 方法名 → 自动分发给 self._handle_<method>()
            *args, **kwargs: 透传参数

        Returns:
            调用结果
        """
        self._log("call_begin", method=method,
                  args_preview=str(args)[:200], kwargs_preview=str(kwargs)[:200])

        handler = getattr(self, f"_handle_{method}", None)
        if handler is None:
            result = {
                "status": "not_implemented",
                "method": method,
                "hint": f"在 {self.__class__.__name__} 中实现 _handle_{method}()",
            }
            self._log("call_missing", method=method)
        else:
            try:
                result = handler(*args, **kwargs)
                self._log("call_success", method=method)
            except Exception as e:
                self._log("call_error", method=method, error=str(e))
                raise

        self._log("call_end", method=method, result_type=type(result).__name__)
        return result

    # ── 审计与自检 ────────────────────────────────

    def audit(self) -> dict[str, Any]:
        """自审计·返回审计报告"""
        checks = {
            'dna_valid': self.DNA.startswith('#龍芯'),
            'replaces_set': bool(self.REPLACES),
            'implements_handle': self._count_handlers() > 0,
            'audit_log_not_empty': len(self._audit_log) > 0,
        }
        return {
            'adapter': self.__class__.__name__,
            'dna': self.DNA,
            'replaces': self.REPLACES,
            'version': self.VERSION,
            'tricolor': self.get_tricolor(),
            'checks': checks,
            'all_pass': all(checks.values()),
            'audit_count': len(self._audit_log),
        }

    def self_test(self) -> bool:
        """冒烟自检·默认检查DNA+REPLACES"""
        try:
            assert self.DNA, "DNA 为空"
            assert self.DNA.startswith('#龍芯'), f"DNA 格式错误: {self.DNA[:20]}"
            assert self.REPLACES, "REPLACES 为空"
            return True
        except AssertionError as e:
            print(f"  ❌ {self.__class__.__name__} 自检失败: {e}", file=sys.stderr)
            return False

    # ── 元信息 ────────────────────────────────────

    def info(self) -> dict[str, str]:
        """返回适配器元信息"""
        return {
            'class': self.__class__.__name__,
            'dna': self.DNA,
            'replaces': self.REPLACES,
            'version': self.VERSION,
            'tricolor': self.get_tricolor(),
            'init_at': self._init_at,
            'license': self.get_license(),
        }

    def _count_handlers(self) -> int:
        """统计已实现的 _handle_* 方法数量"""
        return sum(1 for name in dir(self) if name.startswith('_handle_') and callable(getattr(self, name)))


# ── 模板生成器 ────────────────────────────────────

def generate_adapter_stub(adapter_name: str, replaces: str, target_dir: Path) -> Path:
    """快速生成适配器骨架（供其他工具调用）"""
    target_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().isoformat()
    dna = f"#龍芯⚡️{datetime.now().strftime('%Y-%m-%d')}-ADAPTER-{adapter_name}-V1.0-UID9622"
    class_name = ''.join(w.capitalize() for w in adapter_name.replace('-', '_').split('_')) + 'Adapter'

    stub = f'''#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂主权适配器 · {replaces}
DNA: {dna}
确认码: {CONFIRM_CODE}
主权锚定: {SOVEREIGNTY_ANCHOR}
分层许可: 工程层 MulanPSL v2
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from bin.lh_adapter_base import SovereigntyAdapter


class {class_name}(SovereigntyAdapter):
    """{replaces} 主权适配器"""

    DNA = "{dna}"
    REPLACES = "{replaces}"

    def _handle_hello(self, name: str = "世界") -> dict:
        """示例方法"""
        return {{"greeting": f"🐉 你好 {{name}}，我是 {replaces} 的主权替代"}}

    def get_tricolor(self) -> str:
        return "🟡"


if __name__ == "__main__":
    adapter = {class_name}()
    print(f"✅ {{adapter.REPLACES}} 适配器就绪")
    print(f"   DNA: {{adapter.DNA}}")
    print(f"   自检: {{'✅' if adapter.self_test() else '❌'}}")
    print(f"   测试: {{adapter.call('hello', 'UID9622')}}")
'''

    (target_dir / "__init__.py").write_text(stub, encoding='utf-8')

    # sovereignty.json
    meta = {
        "name": adapter_name, "version": "1.0", "dna": dna,
        "confirm": CONFIRM_CODE, "sovereignty": SOVEREIGNTY_ANCHOR,
        "tricolor": "🟡",
        "license": "思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2",
        "replaces": replaces,
        "generated_at": ts,
    }
    (target_dir / "sovereignty.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding='utf-8')

    return target_dir / "__init__.py"


# ── 验证工具 ──────────────────────────────────────

def validate_adapter(adapter_path: Path) -> dict:
    """验证适配器是否符合主权标准"""
    results = {
        'exists': adapter_path.exists(),
        'has_sovereignty_json': (adapter_path / "sovereignty.json").exists(),
        'has_init': (adapter_path / "__init__.py").exists(),
    }

    if results['has_sovereignty_json']:
        meta = json.loads((adapter_path / "sovereignty.json").read_text(encoding='utf-8'))
        results.update({
            'dna_valid': meta.get('dna', '').startswith('#龍芯'),
            'confirm_present': CONFIRM_CODE in meta.get('confirm', ''),
            'sovereignty_present': SOVEREIGNTY_ANCHOR in meta.get('sovereignty', ''),
            'replaces_set': bool(meta.get('replaces')),
        })

    results['all_pass'] = all(
        v for k, v in results.items()
        if k not in ('all_pass',)
    )
    return results


# ── CLI ────────────────────────────────────────────

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='龍魂·适配器基类工具')
    sub = parser.add_subparsers(dest='cmd')

    p_stub = sub.add_parser('stub', help='快速生成适配器骨架')
    p_stub.add_argument('name', help='适配器名')
    p_stub.add_argument('replaces', help='被替代插件名')
    p_stub.add_argument('-o', '--output', default='.', help='输出目录')

    p_val = sub.add_parser('validate', help='验证适配器')
    p_val.add_argument('path', help='适配器路径')

    p_info = sub.add_parser('info', help='显示基类信息')

    args = parser.parse_args()

    if args.cmd == 'stub':
        out = Path(args.output) / args.name
        path = generate_adapter_stub(args.name, args.replaces, out)
        print(f"✅ 骨架生成: {path}")

    elif args.cmd == 'validate':
        result = validate_adapter(Path(args.path))
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.cmd == 'info':
        print(f"""
🐉 龍魂·主权适配器基类 v1.0
DNA: #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-ADAPTER-BASE-V1.0-UID9622
主权: {SOVEREIGNTY_ANCHOR}
许可: 工程层 MulanPSL v2

基类提供:
  ✅ 审计日志 (get_audit_log / export_audit)
  ✅ 通用调用入口 (call)
  ✅ 自检 (self_test)
  ✅ 自审计 (audit)
  ✅ 元信息 (info)
  ✅ 骨架生成器 (generate_adapter_stub)
  ✅ 验证器 (validate_adapter)

子类必须定义:
  DNA: str     — 以 #龍芯 开头的DNA追溯码
  REPLACES: str — 被替代的原插件名
""")
    else:
        parser.print_help()
