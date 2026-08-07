#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 自主主权插件适配引擎 · 全量测试
DNA: #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-ADAPTER-TEST-V1.0-UID9622
确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
分层许可: 工程层 MulanPSL v2
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'engines'))

from lh_sovereignty_adapter_engine import (
    SovereigntyAdapterEngine, PluginProfile, PluginStatus, BlackboxReason, AdapterMeta
)


def test_scan_native_file():
    """扫描原生开源文件 → 应🟢通过"""
    engine = SovereigntyAdapterEngine()
    prof = engine.scan_plugin(str(Path(__file__).parent.parent / 'bin' / 'lh_adapter_base.py'))
    assert prof.status == PluginStatus.NATIVE, f'期望 NATIVE，实际 {prof.status}'
    assert prof.tricolor == '🟢', f'期望 🟢，实际 {prof.tricolor}'
    print(f'  ✅ scan_native: {prof.tricolor} DNA={prof.dna[:30]}...')


def test_scan_nonexistent():
    """扫描不存在的文件 → 🔴"""
    engine = SovereigntyAdapterEngine()
    prof = engine.scan_plugin('/tmp/nonexistent_abc123.py')
    assert prof.status == PluginStatus.BLACKLISTED
    assert '不存在' in prof.reasons[0]
    print(f'  ✅ scan_nonexistent: {prof.tricolor}')


def test_blackbox_detection_veto_word():
    """检测一票否决词"""
    import tempfile
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8')
    tmp.write('# 这段代码应该技术无国界')
    tmp.close()

    engine = SovereigntyAdapterEngine()
    prof = engine.scan_plugin(tmp.name)
    Path(tmp.name).unlink()

    assert prof.status == PluginStatus.BLACKLISTED
    assert any('一票否决词' in r for r in prof.reasons)
    print(f'  ✅ blackbox_veto: {prof.tricolor} → {" | ".join(prof.reasons)}')


def test_auto_generate_adapter():
    """自动生成适配器"""
    engine = SovereigntyAdapterEngine()
    prof = PluginProfile(name='blackbox-lib', reasons=['闭源'], status=PluginStatus.BLACKLISTED)
    result = engine.auto_generate_adapter(prof)

    assert result['status'] == 'generated'
    assert 'lh-blackbox-lib-adapter' in result['adapter']
    assert result['self_test_passed']

    # 验证文件存在
    adapter_dir = Path(result['path'])
    assert (adapter_dir / '__init__.py').exists()
    assert (adapter_dir / 'sovereignty.json').exists()
    assert (adapter_dir / 'README.md').exists()

    # 清理
    engine.remove_adapter(result['adapter'])
    print(f'  ✅ auto_generate: {result["adapter"]} → 3 files → cleaned')


def test_adapter_list_and_audit():
    """适配器列表&amp;审计"""
    engine = SovereigntyAdapterEngine()
    prof = PluginProfile(name='audit-test', reasons=['测试'], status=PluginStatus.BLACKLISTED)
    result = engine.auto_generate_adapter(prof)
    name = result['adapter']

    adapters = engine.list_adapters()
    assert any(a.name == name for a in adapters), f'列表中找不到 {name}'

    audit = engine.audit_adapter(name)
    assert audit['all_pass'], f'审计失败: {audit["checks"]}'
    assert audit['tricolor'] == '🟢'

    engine.remove_adapter(name)
    print(f'  ✅ list+audit: {name} → audit 🟢')


def test_blacklist_management():
    """黑名单管理"""
    engine = SovereigntyAdapterEngine()

    # 添加
    engine.add_to_blacklist('evil-plugin', '恶意插件')
    bl = engine.list_blacklist()
    assert len(bl) == 1
    assert bl[0]['plugin'] == 'evil-plugin'

    # 清理
    engine.blacklist.pop('evil-plugin', None)
    engine._save_blacklist()
    assert len(engine.list_blacklist()) == 0
    print(f'  ✅ blacklist: add → list → cleanup')


def test_load_plugin_flow():
    """加载流程：黑箱→拒绝→适配器"""
    import tempfile
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8')
    tmp.write('# no dna no license no gpg - pure blackbox')
    tmp.close()

    engine = SovereigntyAdapterEngine()
    result = engine.load_plugin(tmp.name)
    Path(tmp.name).unlink()

    assert result['status'] in ('rejected', 'generated', 'using_adapter')
    print(f'  ✅ load_flow: status={result["status"]}')

    # 清理生成的适配器
    if result['status'] == 'generated':
        engine.remove_adapter(result['adapter'])
        # 也清理黑名单
        name = Path(tmp.name).stem
        engine.blacklist.pop(name, None)
        engine._save_blacklist()


def test_adapter_base_stub():
    """适配器基类骨架生成"""
    from bin.lh_adapter_base import generate_adapter_stub, validate_adapter
    import tempfile
    tmp_dir = Path(tempfile.mkdtemp())
    out = tmp_dir / 'test-stub'

    path = generate_adapter_stub('test-stub', 'target-lib', out)
    assert path.exists()

    result = validate_adapter(out)
    assert result['all_pass'], f'验证失败: {result}'

    import shutil
    shutil.rmtree(tmp_dir)
    print(f'  ✅ adapter_base: stub → validate → all_pass')


def test_adapter_base_sovereignty():
    """适配器基类自检"""
    from bin.lh_adapter_base import SovereigntyAdapter

    class TestAdapter(SovereigntyAdapter):
        DNA = '#龍芯⚡️2026-08-06-ADAPTER-TEST-V1.0-UID9622'
        REPLACES = 'test-target'

        def _handle_hello(self, name='World'):
            return {'greeting': f'Hello {name}'}

    adapter = TestAdapter()
    assert adapter.self_test()
    assert adapter.DNA.startswith('#龍芯')
    assert adapter.REPLACES == 'test-target'

    # 测试 call + 审计
    result = adapter.call('hello', 'UID9622')
    assert result['greeting'] == 'Hello UID9622'
    log = adapter.get_audit_log()
    assert len(log) >= 2  # call_begin + call_success
    print(f'  ✅ adapter_base: self_test → call → audit({len(log)} entries)')


# ── 主入口 ────────────────────────────────────────

def main():
    print('🐉 龍魂·自主主权插件适配引擎 · 全量测试')
    print('='*60)

    tests = [
        ('扫描原生文件', test_scan_native_file),
        ('扫描不存在', test_scan_nonexistent),
        ('黑箱检测(否决词)', test_blackbox_detection_veto_word),
        ('自动生成适配器', test_auto_generate_adapter),
        ('适配器列表+审计', test_adapter_list_and_audit),
        ('黑名单管理', test_blacklist_management),
        ('加载流(拒绝→适配)', test_load_plugin_flow),
        ('适配器基类骨架', test_adapter_base_stub),
        ('适配器基类自检', test_adapter_base_sovereignty),
    ]

    passed = 0
    failed = 0

    for name, test_fn in tests:
        try:
            test_fn()
            passed += 1
        except Exception as e:
            print(f'  ❌ {name}: {e}')
            failed += 1

    print('='*60)
    print(f'  结果: {passed}/{len(tests)} ✅  {failed} ❌')
    print(f'  DNA: #龍芯⚡️丙午·丙申·壬子·丑时·䷖剥-ADAPTER-TEST-V1.0-UID9622')

    if failed:
        sys.exit(1)


if __name__ == '__main__':
    main()
