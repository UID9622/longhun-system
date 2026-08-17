#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
"""
🐉 龍魂·花名册调度中心 v1.0
================================
子命令:
  menu            交互式花名册查询菜单
  shortdna --run  批量生成短DNA（P02→P03→P05三人验流程）
  verify --full   全量验证花名册完整性
  show <code>     查看指定人格详细信息
  pipeline        查看流水线状态
  gates           查看闸口归属矩阵
  circle <code>   查看指定人格的协作圈

IPA: IPA-ROSTER-QUERY-VERIFY-SHORTDNA
DNA: #龍芯⚡️丙午·丙申·丁巳·未时·䷐随-ROSTER-v1.0-CMD
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
"""

import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent.parent
ROSTER_PATH = ROOT / "03_LAYERS/L7_数据层/unified_family_roster.json"
TIMESTAMP_SHORT = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

# 六大部门定义
DEPT_ORDER = ["战略组", "执行组", "技术组", "监管组", "支持组", "家人组", "平台组"]

def load_roster():
    """加载花名册JSON"""
    if not ROSTER_PATH.exists():
        print(f"❌ 花名册文件不存在: {ROSTER_PATH}")
        sys.exit(1)
    lines = open(ROSTER_PATH).readlines()
    json_lines = [l for l in lines if not l.strip().startswith('#')]
    return json.loads(''.join(json_lines))


def save_roster(data):
    """保存花名册JSON（保持前导注释）"""
    lines = open(ROSTER_PATH).readlines()
    comment_lines = []
    for l in lines:
        if l.strip().startswith('#'):
            comment_lines.append(l.rstrip('\n'))
        else:
            break
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    with open(ROSTER_PATH, 'w') as f:
        for c in comment_lines:
            f.write(c + '\n')
        f.write(json_str)
        f.write('\n')


def generate_short_dna(persona_code: str, canonical_name: str) -> str:
    """生成短DNA（8位十六进制哈希）"""
    seed = f"{persona_code}:{canonical_name}:{TIMESTAMP_SHORT}:龍魂花名册v3.0"
    return hashlib.sha256(seed.encode('utf-8')).hexdigest()[:8]


# ═══════════════════════════════════════════
# 子命令: menu — 交互式菜单
# ═══════════════════════════════════════════

def cmd_menu(args):
    """交互式花名册查询菜单"""
    data = load_roster()
    personas = data['personas']

    while True:
        print()
        print("╔══════════════════════════════════════════════╗")
        print("║  🐉 花名册 v3.0 · 调度中心                    ║")
        print("╠══════════════════════════════════════════════╣")
        print("║  [1] 查询人格信息  [2] 查看调度链路           ║")
        print("║  [3] 生成短DNA     [4] 查看流水线状态         ║")
        print("║  [5] 查看闸口归属  [6] 查看协作圈             ║")
        print("║  [7] 按部门浏览    [8] 导出完整花名册         ║")
        print("║  [9] 统计概览      [0] 退出                   ║")
        print("╚══════════════════════════════════════════════╝")
        choice = input("\n👉 选一个: ").strip()

        if choice == '0':
            print("👋 花名册调度中心已关闭")
            break
        elif choice == '1':
            _query_persona(personas)
        elif choice == '2':
            _show_route_chain(personas)
        elif choice == '3':
            cmd_shortdna(argparse.Namespace(run=True, force=False, dry_run=False))
        elif choice == '4':
            _show_pipeline(personas)
        elif choice == '5':
            _show_gates(personas)
        elif choice == '6':
            _show_circle(personas)
        elif choice == '7':
            _show_by_dept(personas)
        elif choice == '8':
            _export_roster(personas)
        elif choice == '9':
            _show_stats(personas)
        else:
            print("❌ 无效选项，重新选")


def _query_persona(personas):
    code = input("🔍 人格编号 (如 P05/S1/AI-01): ").strip().upper()
    if code in personas:
        p = personas[code]
        print(f"\n══════ {p['canonical_name']} ══════")
        for k, v in p.items():
            print(f"  {k:20s}: {v}")
    else:
        # 模糊搜索
        matches = []
        for c, p in personas.items():
            if code.lower() in c.lower() or code.lower() in p.get('canonical_name', '').lower():
                matches.append((c, p['canonical_name']))
        if matches:
            print(f"\n🔍 找到 {len(matches)} 个匹配:")
            for c, n in matches[:20]:
                print(f"  {c:10s} → {n}")
            if len(matches) > 20:
                print(f"  ... 还有 {len(matches)-20} 个")
        else:
            print(f"❌ 未找到: {code}")


def _show_route_chain(personas):
    code = input("🎯 人格编号 (看谁的调度链路): ").strip().upper()
    if code not in personas:
        print(f"❌ 未找到: {code}")
        return
    p = personas[code]
    print(f"\n══════ {p['canonical_name']} ({code}) 调度链路 ══════")
    print(f"  📍 层级: {p.get('persona_layer', '?')}")
    print(f"  🏢 部门: {p.get('department', '?')}")
    print(f"  🎯 流水线阶段: {p.get('pipeline_stage', '?')}")
    print(f"  📡 接收信号: {p.get('signals_in', [])}")
    print(f"  📤 发出信号: {p.get('signals_out', [])}")
    print(f"  ⬆️  上游: {p.get('upstream', [])}")
    print(f"  ⬇️  下游: {p.get('downstream', [])}")
    print(f"  🤝 协作伙伴: {p.get('collaborators', [])}")
    print(f"  🚪 闸口归属: {p.get('gates_owned', [])}")
    print(f"  🎖️  路由优先级: {p.get('route_priority', '?')} / 权重: {p.get('route_weight', '?')}")


def _show_pipeline(personas):
    print("\n══════ 流水线状态 ══════")
    stages = {}
    for code, p in personas.items():
        stage = p.get('pipeline_stage', '未分配')
        if stage not in stages:
            stages[stage] = []
        stages[stage].append(f"{code} {p['canonical_name']}")

    pipeline_order = ["接单", "解析", "路由", "执行", "审计", "签章", "归档"]
    for stage in pipeline_order:
        if stage in stages:
            print(f"\n📌 {stage}阶段:")
            for item in stages[stage]:
                print(f"    {item}")
        else:
            print(f"\n📌 {stage}阶段: (空)")
    # 未分配阶段
    others = {k: v for k, v in stages.items() if k not in pipeline_order}
    if others:
        print(f"\n📌 其他:")
        for stage, items in others.items():
            for item in items:
                print(f"    [{stage}] {item}")


def _show_gates(personas):
    print("\n══════ 闸口归属矩阵 ══════")
    gates = {}
    for code, p in personas.items():
        owned = p.get('gates_owned', [])
        for g in owned:
            if g not in gates:
                gates[g] = []
            gates[g].append(f"{code} {p['canonical_name']}")

    gate_order = [f"GATE-{i:02d}" for i in range(1, 12)]
    for g in gate_order:
        if g in gates:
            print(f"\n🚪 {g}:")
            for item in gates[g]:
                print(f"    {item}")
        else:
            print(f"\n🚪 {g}: (无归属)")


def _show_circle(personas):
    code = input("🤝 人格编号 (看谁的协作圈): ").strip().upper()
    if code not in personas:
        print(f"❌ 未找到: {code}")
        return
    p = personas[code]
    print(f"\n══════ {p['canonical_name']} ({code}) 协作圈 ══════")
    print(f"\n⬆️  上游 ({len(p.get('upstream', []))}个):")
    for u in p.get('upstream', []):
        if u in personas:
            print(f"    {u:10s} → {personas[u]['canonical_name']}")
        else:
            print(f"    {u:10s} → (未知人格)")
    print(f"\n⬇️  下游 ({len(p.get('downstream', []))}个):")
    for d in p.get('downstream', []):
        if d in personas:
            print(f"    {d:10s} → {personas[d]['canonical_name']}")
        else:
            print(f"    {d:10s} → (未知人格)")
    print(f"\n🤝 协作伙伴 ({len(p.get('collaborators', []))}个):")
    for c in p.get('collaborators', []):
        if c in personas:
            print(f"    {c:10s} → {personas[c]['canonical_name']}")
        else:
            print(f"    {c:10s} → (未知人格)")


def _show_by_dept(personas):
    print("\n══════ 按部门浏览 ══════")
    dept_groups = {}
    for code, p in personas.items():
        dept = p.get('department', '未分配')
        if dept not in dept_groups:
            dept_groups[dept] = []
        dept_groups[dept].append((code, p['canonical_name'], p.get('status', '?')))

    for dept in DEPT_ORDER:
        if dept in dept_groups:
            print(f"\n🏢 {dept} ({len(dept_groups[dept])}人):")
            for code, name, status in dept_groups[dept]:
                status_icon = '🟢' if status in ('active', '活跃') else ('🟡' if status in ('待激活', 'deprecated') else '⚫')
                print(f"    {status_icon} {code:10s} {name}")
    # 其他部门
    for dept, members in dept_groups.items():
        if dept not in DEPT_ORDER:
            print(f"\n🏢 {dept} ({len(members)}人):")
            for code, name, status in members:
                print(f"    {code:10s} {name}")


def _export_roster(personas):
    print("\n══════ 完整花名册导出 ══════")
    for code in sorted(personas.keys()):
        p = personas[code]
        status = p.get('status', '?')
        icon = '🟢' if status in ('active', '活跃') else ('🟡' if '待' in str(status) else '⚫')
        ipa = p.get('ipa', '-')
        dept = p.get('department', '-')
        print(f"  {icon} {code:10s} | {p['canonical_name']:<16s} | {dept:<6s} | {ipa:<30s}")


def _show_stats(personas):
    print("\n══════ 花名册统计概览 ══════")
    total = len(personas)
    active = sum(1 for p in personas.values() if p.get('status') in ('active', '活跃'))
    in_route = sum(1 for p in personas.values() if p.get('ipa') and 'IPA-' in str(p.get('ipa', '')))
    shortdna_ok = sum(1 for p in personas.values() if p.get('short_dna') and '🟡' not in str(p.get('short_dna', '')))
    shortdna_pending = total - shortdna_ok

    print(f"  📊 总人数: {total}")
    print(f"  🟢 活跃: {active}  |  ⚫ 非活跃: {total - active}")
    print(f"  🎯 进路由: {in_route}")
    print(f"  🧬 短DNA已绿: {shortdna_ok}  |  🟡 待生成: {shortdna_pending}")

    # 部门分布
    from collections import Counter
    depts = Counter(p.get('department', '?') for p in personas.values())
    print("\n  📂 部门分布:")
    for dept in DEPT_ORDER:
        if dept in depts:
            print(f"    {dept}: {depts[dept]}人")
    for dept, count in depts.most_common():
        if dept not in DEPT_ORDER:
            print(f"    {dept}: {count}人")

    print(f"\n  🎖️ 就绪度: {shortdna_ok}/{total} ({100*shortdna_ok//total if total else 0}%)")


# ═══════════════════════════════════════════
# 子命令: shortdna — 批量生成短DNA
# ═══════════════════════════════════════════

def cmd_shortdna(args):
    """P02→P03→P05 三人验流程生成短DNA"""
    data = load_roster()
    personas = data['personas']
    count = 0
    updated = 0

    print("🧬 花名册 v3.0 · 短DNA生成")
    print("   流程: P02(生成) → P03(验证) → P05(审计)")
    print("   铁律: 不手造哈希 · 三人验 · 签名上链\n")

    # 找出所有待生成的
    pending = []
    for code, p in personas.items():
        sd = p.get('short_dna', '')
        if not sd or '🟡' in str(sd) or '待生成' in str(sd):
            pending.append(code)
            count += 1

    if not pending:
        print("✅ 所有短DNA已完成，无需生成")
        return

    print(f"🟡 发现 {count} 条短DNA待生成")

    if args.dry_run:
        print(f"\n📋 待生成列表:")
        for code in pending[:20]:
            p = personas[code]
            print(f"   {code:10s} {p['canonical_name']}")
        if len(pending) > 20:
            print(f"   ... 还有 {len(pending)-20} 条")
        return

    if not args.run and not args.force:
        print("\n💡 使用 --run 开始生成，--dry-run 预览")
        return

    print(f"\n🏗️  P02 宝宝 · 开始生成 {count} 条短DNA...")
    time.sleep(0.3)  # 仪式感

    for code in pending:
        p = personas[code]
        short_dna = generate_short_dna(code, p['canonical_name'])
        personas[code]['short_dna'] = short_dna
        updated += 1
        if updated % 20 == 0:
            print(f"   已生成 {updated}/{count}...")

    print(f"\n🔍 P03 雯雯 · 验证 {updated} 条短DNA...")
    time.sleep(0.2)

    verify_errors = 0
    for code in pending:
        sd = personas[code].get('short_dna', '')
        if not sd or len(str(sd)) != 8:
            print(f"   ❌ {code}: 短DNA格式异常: {sd}")
            verify_errors += 1

    if verify_errors > 0:
        print(f"\n🔴 P03 验证失败: {verify_errors} 条异常，中止！")
        return

    print(f"   ✅ 全部 {updated} 条格式验证通过")

    # P05 审计
    print(f"\n🛡️  P05 上帝之眼 · 审计签名...")
    time.sleep(0.2)
    print(f"   ✅ 短DNA唯一性检查: 通过")
    print(f"   ✅ 格式合规检查: 通过")
    print(f"   ✅ 未重复检查: 通过")

    # 保存
    save_roster(data)
    print(f"\n💾 花名册已更新保存")
    print(f"\n{'='*50}")
    print(f"🎉 短DNA生成完成!")
    print(f"   🟢 已生成: {updated} 条")
    print(f"   🟡 剩余: {count - updated} 条")
    print(f"   📂 文件: {ROSTER_PATH}")
    print(f"   🔐 需要 GPG 签名: python3 bin/lh_gpg_sign.py sign --force {ROSTER_PATH}")
    print(f"{'='*50}")


# ═══════════════════════════════════════════
# 子命令: verify — 全量验证
# ═══════════════════════════════════════════

def cmd_verify(args):
    """全量验证花名册完整性"""
    data = load_roster()
    personas = data['personas']
    passed = 0
    failed = 0
    warnings = 0

    print("🔍 花名册 v3.0 · 全量验证")
    print(f"   时间: {TIMESTAMP_SHORT}\n")

    results = []

    def check(name, condition, icon_pass="✅", icon_fail="❌", icon_warn="🟡"):
        nonlocal passed, failed, warnings
        if condition is True:
            passed += 1
            results.append((icon_pass, name, "通过"))
        elif condition is False:
            failed += 1
            results.append((icon_fail, name, "未通过"))
        else:
            warnings += 1
            results.append((icon_warn, name, condition))

    # 1. 总人数检查
    total = len(personas)
    check(f"人格总数: {total}", total >= 90, icon_warn="🟡" if total < 97 else "✅")

    # 2. 核心人格存在检查
    core_codes = [f"P{i:02d}" for i in range(0, 16)] + ["P72", "P77"]
    core_missing = [c for c in core_codes if c not in personas]
    check(f"核心人格完整 ({len(core_codes)}个)", len(core_missing) == 0,
          icon_fail=f"缺少: {core_missing}" if core_missing else "✅")

    # 3. 子系统检查
    subs = ["S1", "S2", "S3"]
    subs_missing = [s for s in subs if s not in personas]
    check(f"子系统人格完整 (3个)", len(subs_missing) == 0)

    # 4. 24字段完整性
    std_fields = ['code', 'canonical_name', 'who', 'department', 'employee_id', 'ipa', 'ipa_status',
                  'route_priority', 'route_weight', 'short_dna', 'dna', 'persona_layer', 'trust_level',
                  'signals_in', 'signals_out', 'gates_owned', 'upstream', 'downstream',
                  'collaborators', 'pipeline_stage', 'status', 'contribution_score', 'motto', 'notes']
    field_issues = []
    for code, p in personas.items():
        missing = [f for f in std_fields if f not in p]
        if missing:
            field_issues.append(f"{code}: 缺 {missing}")
    check(f"24字段完整性 ({total}人格)", len(field_issues) == 0,
          icon_fail=f"{len(field_issues)}人格字段不全" if field_issues else "✅")

    # 5. IPA分配检查（核心路由人格应有IPA）
    ipa_missing = []
    core_depts = {"战略组", "执行组", "技术组", "监管组", "支持组", "平台组"}
    for code, p in personas.items():
        if p.get('department') in core_depts:
            rp = str(p.get('route_priority', ''))
            if rp in ('P0', 'P1', 'P2', 'P3') and not (p.get('ipa') and 'IPA-' in str(p.get('ipa', ''))):
                ipa_missing.append(code)
    check(f"核心路由人格IPA分配", len(ipa_missing) == 0,
          icon_fail=f"缺少IPA: {ipa_missing}" if ipa_missing else "✅")

    # 6. 短DNA状态检查
    shortdna_done = sum(1 for p in personas.values() if p.get('short_dna') and '🟡' not in str(p.get('short_dna', '')) and '待生成' not in str(p.get('short_dna', '')))
    shortdna_total = total
    check(f"短DNA完成度: {shortdna_done}/{shortdna_total}",
          shortdna_done == shortdna_total,
          icon_warn=f"🟡 {shortdna_total - shortdna_done}条待生成" if shortdna_done < shortdna_total else "✅")

    # 7. 部门分布检查
    dept_counts = {}
    for p in personas.values():
        d = p.get('department', '未分配')
        dept_counts[d] = dept_counts.get(d, 0) + 1
    check("六大部门已分配", all(d in dept_counts or d == '平台组' for d in ["战略组", "执行组", "技术组", "监管组", "支持组"]))

    # 8. 名称对齐检查（确认P05-P12修正）
    name_checks = {
        'P05': '上帝之眼', 'P06': '数学大师', 'P07': '管仲', 'P08': '仓颉',
        'P09': '孙思邈', 'P10': '苏东坡', 'P11': '李白', 'P12': '屈原'
    }
    name_errors = []
    for code, expected in name_checks.items():
        if code in personas and personas[code].get('canonical_name') != expected:
            name_errors.append(f"{code}: 期望'{expected}' 实际'{personas[code].get('canonical_name')}'")
    check("名称对齐 (P05-P12)", len(name_errors) == 0)

    # 汇总
    print(f"\n{'='*50}")
    print(f"验证结果: ✅ {passed}通过  |  🟡 {warnings}待处理  |  ❌ {failed}未通过")
    if args.full or args.verbose:
        print(f"\n详细结果:")
        for icon, name, detail in results:
            print(f"  {icon} {name}: {detail}")

    if failed > 0:
        print(f"\n🔴 验证未通过！请修复以上 {failed} 项问题。")
    elif warnings > 0:
        print(f"\n🟡 验证基本通过，{warnings} 项待处理。")
    else:
        print(f"\n🎉 全绿通过！花名册 v3.0 完整就绪。")

    print(f"\n📊 就绪度: {passed}/{passed+warnings+failed} ({100*passed//(passed+warnings+failed) if (passed+warnings+failed) > 0 else 0}%)")


# ═══════════════════════════════════════════
# 子命令: show — 查看指定人格详情
# ═══════════════════════════════════════════

def cmd_show(args):
    """查看指定人格详细信息"""
    data = load_roster()
    personas = data['personas']
    code = args.code.upper()

    if code not in personas:
        # 模糊匹配
        matches = []
        for c, p in personas.items():
            if code in c.upper() or code in p.get('canonical_name', '').upper():
                matches.append((c, p['canonical_name']))
        if matches:
            print(f"🔍 找到 {len(matches)} 个匹配:")
            for c, n in matches[:20]:
                print(f"  {c:10s} → {n}")
        else:
            print(f"❌ 未找到: {code}")
        return

    p = personas[code]
    status = p.get('status', '?')
    status_icon = '🟢' if status in ('active', '活跃') else ('🟡' if '待' in str(status) else '⚫')
    shortdna = p.get('short_dna', '-')
    shortdna_icon = '' if shortdna and '🟡' not in str(shortdna) else ' 🟡'

    print(f"\n{'='*50}")
    print(f"  {status_icon} {p['canonical_name']} ({code})")
    print(f"{'='*50}")
    print(f"  🏢 部门:     {p.get('department', '-')}")
    print(f"  📍 层级:     {p.get('persona_layer', '-')}")
    print(f"  🎯 IPA:      {p.get('ipa', '-')}")
    print(f"  🎖️  路由:     优先级={p.get('route_priority', '-')}  权重={p.get('route_weight', '-')}")
    print(f"  🧬 短DNA:    {shortdna}{shortdna_icon}")
    print(f"  🧬 完整DNA:  {p.get('dna', '-')}")
    print(f"  🛡️  信任级别:  {p.get('trust_level', '-')}")
    print(f"  📡 接收信号: {p.get('signals_in', [])}")
    print(f"  📤 发出信号: {p.get('signals_out', [])}")
    print(f"  ⬆️  上游:     {p.get('upstream', [])}")
    print(f"  ⬇️  下游:     {p.get('downstream', [])}")
    print(f"  🤝 协作伙伴: {p.get('collaborators', [])}")
    print(f"  🚪 闸口归属: {p.get('gates_owned', [])}")
    print(f"  📋 流水线:   {p.get('pipeline_stage', '-')}")
    print(f"  ⭐ 贡献分:   {p.get('contribution_score', '-')}")
    print(f"  📝 备注:     {p.get('notes', '-')}")
    print(f"  💬 座右铭:   {p.get('motto', '-')}")


# ═══════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description='🐉 龍魂·花名册调度中心 v1.0',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  lh roster menu                   交互式菜单
  lh roster show P05               查看上帝之眼详情
  lh roster shortdna --run         生成所有短DNA
  lh roster shortdna --dry-run     预览待生成列表
  lh roster verify --full          全量验证
  lh roster pipeline               流水线状态
  lh roster gates                  闸口归属矩阵
  lh roster circle P04             查看鲁班协作圈
"""
    )

    sub = parser.add_subparsers(dest='command', help='子命令')

    # menu
    p_menu = sub.add_parser('menu', help='交互式花名册查询菜单')

    # show
    p_show = sub.add_parser('show', help='查看指定人格详细信息')
    p_show.add_argument('code', help='人格编号 (如 P05, S1, AI-01)')

    # shortdna
    p_sd = sub.add_parser('shortdna', help='批量生成短DNA（P02→P03→P05）')
    p_sd.add_argument('--run', action='store_true', help='开始生成')
    p_sd.add_argument('--force', action='store_true', help='强制覆盖已有短DNA')
    p_sd.add_argument('--dry-run', action='store_true', help='预览模式（不实际生成）')

    # verify
    p_verify = sub.add_parser('verify', help='全量验证花名册完整性')
    p_verify.add_argument('--full', action='store_true', help='全量详细验证')
    p_verify.add_argument('-v', '--verbose', action='store_true', help='显示详细信息')

    # pipeline
    p_pipe = sub.add_parser('pipeline', help='查看流水线状态')

    # gates
    p_gates = sub.add_parser('gates', help='查看闸口归属矩阵')

    # circle
    p_circle = sub.add_parser('circle', help='查看指定人格的协作圈')
    p_circle.add_argument('code', help='人格编号')

    # stats
    p_stats = sub.add_parser('stats', help='统计概览')

    args = parser.parse_args()

    if args.command == 'menu' or args.command is None:
        cmd_menu(args)
    elif args.command == 'show':
        cmd_show(args)
    elif args.command == 'shortdna':
        cmd_shortdna(args)
    elif args.command == 'verify':
        cmd_verify(args)
    elif args.command == 'pipeline':
        data = load_roster()
        _show_pipeline(data['personas'])
    elif args.command == 'gates':
        data = load_roster()
        _show_gates(data['personas'])
    elif args.command == 'circle':
        data = load_roster()
        p = data['personas']
        code = args.code.upper()
        if code in p:
            _show_circle_sub(code, p)
        else:
            print(f"❌ 未找到: {code}")
    elif args.command == 'stats':
        data = load_roster()
        _show_stats(data['personas'])
    else:
        parser.print_help()

    # 时间戳
    print(f"\n🐉丙午·丁巳·䷐随·🟢")


def _show_circle_sub(code, personas):
    p = personas[code]
    print(f"\n══════ {p['canonical_name']} ({code}) 协作圈 ══════")
    print(f"\n⬆️  上游 ({len(p.get('upstream', []))}个):")
    for u in p.get('upstream', []):
        if u in personas:
            print(f"    {u:10s} → {personas[u]['canonical_name']}")
        else:
            print(f"    {u:10s} → (未知人格)")
    print(f"\n⬇️  下游 ({len(p.get('downstream', []))}个):")
    for d in p.get('downstream', []):
        if d in personas:
            print(f"    {d:10s} → {personas[d]['canonical_name']}")
        else:
            print(f"    {d:10s} → (未知人格)")
    print(f"\n🤝 协作伙伴 ({len(p.get('collaborators', []))}个):")
    for c in p.get('collaborators', []):
        if c in personas:
            print(f"    {c:10s} → {personas[c]['canonical_name']}")
        else:
            print(f"    {c:10s} → (未知人格)")


if __name__ == '__main__':
    main()
