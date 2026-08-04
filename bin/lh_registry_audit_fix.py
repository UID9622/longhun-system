#!/usr/bin/env python3
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# DNA: #龍芯⚡️丙午·乙未·乙丑·小畜-FIX_DNA-v1.0
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
#龍芯⚡️丙午·丙申·癸酉·庚申·临-LH_REGISTRY_AUDIT_FIX-v1.0-97280324
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""修复 persona_registry.json — 对齐 AGENTS.md + 五大后台 v3.1"""
import json
from datetime import datetime, timezone

with open('personas/runtime/persona_registry.json') as f:
    d = json.load(f)

personas = d['personas']
changes = []

# ===== 1. 修复P02: 改为 龍芯修复师 对齐AGENTS.md =====
if 'P02' in personas:
    p = personas['P02']
    old_name = p['name']
    p['name'] = '龍芯修复师'
    p['name_en'] = 'LongXin Fixer'
    p['role'] = 'repair_executor+mathematical_engine'
    p['motto'] = '运筹帷幄，观天察地，修而不辍'
    p['triggers'] = ['修复','修改','fix','算法','数学','证明','计算','数值','改好']
    p['_audit_note'] = f'2026-07-11：原名"{old_name}"与AGENTS.md冲突，统一为龍芯修复师+张衡数学能力合并'
    changes.append(f'P02: {old_name} → 龍芯修复师')

# ===== 2. 修复P03: 添加别名对齐五大后台雯雯 =====
if 'P03' in personas:
    p = personas['P03']
    p['alias_names'] = ['墨子', '雯雯']
    p['role'] = 'logic_verification+structure_organizer'
    p['triggers'].extend(['整理','归档','结构化','接火','水印'])
    p['_audit_note'] = '2026-07-11：合并墨子逻辑验证+雯雯结构化整理'
    changes.append('P03: 添加雯雯别名')

# ===== 3. 修复P04: 对齐五大后台 =====
if 'P04' in personas:
    p = personas['P04']
    p['role'] = 'implementation+tech_executor'
    p['triggers'].extend(['构建','开发','系统维护','健康巡检','技术执行'])
    p['_audit_note'] = '2026-07-11：对齐五大后台v3.1 P04鲁班·技术执行'
    changes.append('P04: 对齐五大后台')

# ===== 4. 修复P05: 合并身份 =====
if 'P05' in personas:
    p = personas['P05']
    p['name'] = '执行外设(系统级)'
    p['name_en'] = 'Executor+GodsEye'
    p['role'] = 'meta_controller+tri_color_auditor'
    p['alias_names'] = ['上帝之眼', '执行外设']
    p['motto'] = '行胜于言，使命必达。公正不偏袒，留痕必溯。'
    p['triggers'].extend(['检查','审计','安全吗','三色','五色','监控','熔断','合规'])
    p['_audit_note'] = '2026-07-11：合并执行外设+上帝之眼，路由表均指向P05'
    changes.append('P05: 执行外设+上帝之眼合并')

# ===== 5. 修复P06: 对齐五大后台数学大师 =====
if 'P06' in personas:
    p = personas['P06']
    old_name = p['name']
    p['name'] = '数学大师'
    p['name_en'] = 'Math Master'
    p['role'] = 'adversarial_simulator+weight_calculator'
    p['alias_names'] = ['镜像审计者', '数学大师']
    p['motto'] = '以镜为鉴，可正衣冠。数据说话，不加感情。'
    p['triggers'].extend(['数字根','五行','八卦','dr','权重','归一化','计算','公式'])
    p['_audit_note'] = f'2026-07-11：原名"{old_name}"，对齐AGENTS.md+五大后台v3.1数学大师'
    changes.append(f'P06: {old_name} → 数学大师')

# ===== 6. 新增 P00 文心（路由表最高频引用） =====
personas['P00'] = {
    'code': 'P00',
    'name': '文心',
    'name_en': 'WenXin',
    'role': 'eternal_anchor+constitution_guardian',
    'weight': 1.0,
    'success_rate': 1.0,
    'executions': 0,
    'priority': 0,
    'status': 'active',
    'triggers': ['铁律','规矩','宪法','底座','不骗','对外','史记','最初誓言','情绪海绵','德字闸','道阳佛阴','传承契约','大白话'],
    'mode': 'sequential',
    'motto': '再楠不惧，终成豪图',
    'trust_level': 'L5',
    'alias': 'p00',
    'alias_names': ['文心', '北辰'],
    'ip_group': 'core',
    'route_priority': 'P0',
    'route_id': 'UID9622-P00-001',
    'call_count': 0,
    'weekly_call_count': 0,
    'monthly_call_count': 0,
    'help_count': 0,
    'weekly_help_count': 0,
    'monthly_help_count': 0,
    'test_contribution_count': 0,
    'warning_count': 0,
    'fuse_count': 0,
    'seven_dim_coverage': [],
    'last_active_at': None,
    'j_space_affinity': {
        'tokens': ['铁律','constitution','anchor','永恆','宪法','底线'],
        'weight': 1.0
    },
    'verified_runtime': False,
    '_audit_note': '2026-07-11新增：P00路由表引用13次(最高频)，永恒锚点A-009'
}
changes.append('P00: 新增(文心·永恒锚点)')

# ===== 7. 新增 P14 吕蒙 =====
personas['P14'] = {
    'code': 'P14',
    'name': '吕蒙',
    'name_en': 'Lv Meng',
    'role': 'deployment_executor',
    'weight': 0.7,
    'success_rate': 0.9,
    'executions': 0,
    'priority': 3,
    'status': 'active',
    'triggers': ['部署','发布','上线'],
    'mode': 'sequential',
    'motto': '士别三日，刮目相看',
    'trust_level': 'L2',
    'alias': 'p14',
    'alias_names': ['吕蒙'],
    'ip_group': 'exec',
    'route_priority': 'P2',
    'route_id': 'UID9622-P14-001',
    'call_count': 0,
    'weekly_call_count': 0,
    'monthly_call_count': 0,
    'help_count': 0,
    'weekly_help_count': 0,
    'monthly_help_count': 0,
    'test_contribution_count': 0,
    'warning_count': 0,
    'fuse_count': 0,
    'seven_dim_coverage': [],
    'last_active_at': None,
    'j_space_affinity': {
        'tokens': ['部署','deploy','发布','上线'],
        'weight': 0.7
    },
    'verified_runtime': False,
    'executor_script': 'bin/lh_auto_cannon.py',
    '_audit_note': '2026-07-11新增：路由表引用，需一票否决'
}
changes.append('P14: 新增(吕蒙·部署)')

# ===== 8. 新增 P19 极简审计官 =====
personas['P19'] = {
    'code': 'P19',
    'name': '极简审计官',
    'name_en': 'Minimalist Auditor',
    'role': 'ui_registry_auditor',
    'weight': 0.6,
    'success_rate': 0.95,
    'executions': 0,
    'priority': 4,
    'status': 'active',
    'triggers': ['审计DNA','审计登记','极简审计','registry audit','UI审计'],
    'mode': 'sequential',
    'motto': '8项审计，一票否决',
    'trust_level': 'L2',
    'alias': 'p19',
    'alias_names': ['极简审计官'],
    'ip_group': 'platform',
    'route_priority': 'P3',
    'route_id': 'UID9622-P19-001',
    'call_count': 0,
    'weekly_call_count': 0,
    'monthly_call_count': 0,
    'help_count': 0,
    'weekly_help_count': 0,
    'monthly_help_count': 0,
    'test_contribution_count': 0,
    'warning_count': 0,
    'fuse_count': 0,
    'seven_dim_coverage': [],
    'last_active_at': None,
    'j_space_affinity': {
        'tokens': ['审计','audit','registry','注册','UI'],
        'weight': 0.6
    },
    'verified_runtime': False,
    '_audit_note': '2026-07-11新增：AGENTS.md路由引用，8项清单审计'
}
changes.append('P19: 新增(极简审计官)')

# ===== 9. 新增 P20 贡献公证官 =====
personas['P20'] = {
    'code': 'P20',
    'name': '贡献公证官',
    'name_en': 'Contribution Notary',
    'role': 'trust_ledger+contribution_scorer',
    'weight': 0.6,
    'success_rate': 0.95,
    'executions': 0,
    'priority': 4,
    'status': 'active',
    'triggers': ['信任积分','贡献分','功德分','公益分','trust ledger','contribution score','政审'],
    'mode': 'sequential',
    'motto': '三分桶，各归各桶，不混不蹭',
    'trust_level': 'L2',
    'alias': 'p20',
    'alias_names': ['贡献公证官'],
    'ip_group': 'platform',
    'route_priority': 'P3',
    'route_id': 'UID9622-P20-001',
    'call_count': 0,
    'weekly_call_count': 0,
    'monthly_call_count': 0,
    'help_count': 0,
    'weekly_help_count': 0,
    'monthly_help_count': 0,
    'test_contribution_count': 0,
    'warning_count': 0,
    'fuse_count': 0,
    'seven_dim_coverage': [],
    'last_active_at': None,
    'j_space_affinity': {
        'tokens': ['积分','score','ledger','贡献','公证','政审'],
        'weight': 0.6
    },
    'verified_runtime': False,
    'executor_script': 'L5_服务层/services/dashboard/web/unified_dna_register_v1.0.html',
    '_audit_note': '2026-07-11新增：AGENTS.md+A-030锚点，三分桶贡献公证'
}
changes.append('P20: 新增(贡献公证官)')

# ===== 10. 标记 PH-*/PF-* 为 planned =====
ph_count = 0
pf_count = 0
for k, v in personas.items():
    if k.startswith('PH-'):
        if v.get('status') == 'active':
            v['status'] = 'planned'
            v['_audit_note'] = '2026-07-11复审：PH-*规划人格，无独立执行器，标记planned'
            ph_count += 1
    elif k.startswith('PF-'):
        if v.get('status') == 'active':
            v['status'] = 'planned'
            v['_audit_note'] = '2026-07-11复审：PF-*功能规划，无独立执行器，标记planned'
            pf_count += 1

changes.append(f'批量: {ph_count}PH + {pf_count}PF → planned')

# 更新meta
d['_meta']['last_updated'] = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f+00:00')
d['_meta']['version'] = 'v3.1'
d['_meta']['audit'] = {
    'date': '2026-07-11',
    'changes': changes,
    'dna': '#龍芯⚡️丙午·丙申·丙辰·午时·需-REGISTRY-AUDIT-FIX'
}

with open('personas/runtime/persona_registry.json', 'w') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print('✅ 注册表修复完成')
for c in changes:
    print(f'  {c}')

active = sum(1 for v in d['personas'].values() if v['status'] == 'active')
planned = sum(1 for v in d['personas'].values() if v['status'] == 'planned')
print(f'\n最终: {len(d["personas"])}人格 | active={active} | planned={planned}')
