#!/usr/bin/env python3
#龍芯⚡️丙午·乙未·甲寅·申时·师-REGISTRY-EXTEND-v1.3
# CREATOR: 诸葛鑫 (UID9622)
# PROTOCOL: CC BY-NC-SA 4.0
"""龍魂注册表扩展 v1.3 — 将 L6/L8/L9 层纳入依赖图
DNA: #龍芯⚡️丙午·乙未·甲寅·申时·师-REGISTRY-EXTEND-v1.3
"""
import json
from pathlib import Path

ROOT = Path("/Users/zuimeidedeyihan/longhun-system")
reg_path = ROOT / "L7_数据层/persona_knowledge/registry.json"
reg = json.loads(reg_path.read_text(encoding='utf-8'))
dep = reg['dependency_graph']
routes = reg['ipa_routes']
existing_ipa = {r['node_id'] for r in routes}

NEW_ENTRIES = {
    # L6 集成层
    "L6_集成层/龙魂系统_API接口完整实现_v1.0.py": {"ipa_route":"IPA-L6-001","module_class":"L6::Integration","status":"active","layer":"L6","consumed_by":[{"file":"L5_服务层/services/dashboard/web/","rel":"api_backend"}]},
    "L6_集成层/content_sovereignty_protocol_v2.1.py": {"ipa_route":"IPA-L6-002","module_class":"L6::Sovereignty","status":"active","layer":"L6","consumed_by":[{"file":"01_protocols/LH-GOV-DATA-SOVEREIGNTY-v1.0.md","rel":"protocol_anchor"}]},
    "L6_集成层/claude_runtime_wrapper.py": {"ipa_route":"IPA-L6-003","module_class":"L6::RuntimeBridge","status":"active","layer":"L6","consumed_by":[{"file":"AGENTS.md","rel":"runtime_anchor"}]},
    "L6_集成层/longhun_braket.py": {"ipa_route":"IPA-L6-004","module_class":"L6::QuantumBridge","status":"active","layer":"L6","consumed_by":[{"file":"L1_内核层/","rel":"quantum_core"}]},

    # L8 治理层 - 核心治理文件
    "L8_治理层/记错本.md": {"ipa_route":"IPA-L8-001","module_class":"L8::ErrorLog","status":"active","layer":"L8","consumed_by":[{"file":"AGENTS.md","rel":"error_audit"}]},
    "L8_治理层/governance/FUSE_TRANSPARENCY/FUSE_PROTOCOL.md": {"ipa_route":"IPA-L8-002","module_class":"L8::FuseProtocol","status":"active","layer":"L8","consumed_by":[{"file":"01_技能庫/fuse-appeal.md","rel":"appeal_rules"}]},
    "L8_治理层/governance/曾仕强老师·捡回德_v1.0.md": {"ipa_route":"IPA-L8-003","module_class":"L8::ZengLegacy","status":"active","layer":"L8","consumed_by":[{"file":"AGENTS.md","rel":"A-026_anchor"}]},
    "L8_治理层/governance/ANTI_TAMPER/LONGHUN_ANTI_TAMPER.md": {"ipa_route":"IPA-L8-004","module_class":"L8::AntiTamper","status":"active","layer":"L8","consumed_by":[{"file":"bin/lh_anti_tamper.py","rel":"tamper_engine"}]},
    "L8_治理层/governance/IRON-LAWS/P0_ETERNAL_IRON_LAW_DIRECTORY.md": {"ipa_route":"IPA-L8-005","module_class":"L8::IronLaws","status":"active","layer":"L8","consumed_by":[{"file":"P0_ETERNAL_LOCK.md","rel":"lock_anchor"}]},
    "L8_治理层/governance/TOTAL_GOAL_LEGACY_RELAY.md": {"ipa_route":"IPA-L8-006","module_class":"L8::LegacyRelay","status":"active","layer":"L8","consumed_by":[{"file":"AGENTS.md","rel":"legacy_chain"}]},
    "L8_治理层/governance/CAPITAL_LOVE_AUDIT_PROTOCOL.md": {"ipa_route":"IPA-L8-007","module_class":"L8::CapitalAudit","status":"active","layer":"L8","consumed_by":[]},
    "L8_治理层/governance/INFINITE_GROWTH_ENGINE_v∞.md": {"ipa_route":"IPA-L8-008","module_class":"L8::GrowthEngine","status":"active","layer":"L8","consumed_by":[]},
    "L8_治理层/governance/PUBLIC_TOOLBOX_README.md": {"ipa_route":"IPA-L8-009","module_class":"L8::PublicToolbox","status":"active","layer":"L8","consumed_by":[]},

    # L9 子系统 - 核心子系统
    "L9_子系统/subsystems/lh_shield_v3.0_cnsh.py": {"ipa_route":"IPA-L9-001","module_class":"L9::Shield","status":"active","layer":"L9","consumed_by":[{"file":"L9_子系统/subsystems/longhun_shield.py","rel":"shield_base"}]},
    "L9_子系统/subsystems/zero_trust_guard.py": {"ipa_route":"IPA-L9-002","module_class":"L9::ZeroTrust","status":"active","layer":"L9","consumed_by":[{"file":"AGENTS.md","rel":"security_anchor"}]},
    "L9_子系统/subsystems/second_dimension_eye.py": {"ipa_route":"IPA-L9-003","module_class":"L9::SecondEye","status":"active","layer":"L9","consumed_by":[{"file":"AGENTS.md","rel":"A-020_anchor"}]},
    "L9_子系统/subsystems/trials_engine.py": {"ipa_route":"IPA-L9-004","module_class":"L9::Trials","status":"active","layer":"L9","consumed_by":[{"file":"AGENTS.md","rel":"A-017_anchor"}]},
    "L9_子系统/subsystems/final_strike.py": {"ipa_route":"IPA-L9-005","module_class":"L9::FinalStrike","status":"active","layer":"L9","consumed_by":[{"file":"AGENTS.md","rel":"A-021_anchor"}]},
    "L9_子系统/subsystems/longhun_ai_output_guard.py": {"ipa_route":"IPA-L9-006","module_class":"L9::OutputGuard","status":"active","layer":"L9","consumed_by":[]},
    "L9_子系统/subsystems/longhun_download_guard.py": {"ipa_route":"IPA-L9-007","module_class":"L9::DownloadGuard","status":"active","layer":"L9","consumed_by":[]},
    "L9_子系统/subsystems/longhun_audit_pricing_engine_v2.0.py": {"ipa_route":"IPA-L9-008","module_class":"L9::AuditPricing","status":"active","layer":"L9","consumed_by":[]},
    "L9_子系统/subsystems/longhun_shield_panel.py": {"ipa_route":"IPA-L9-009","module_class":"L9::ShieldPanel","status":"active","layer":"L9","consumed_by":[{"file":"L9_子系统/subsystems/lh_shield_v3.0_cnsh.py","rel":"panel_ui"}]},
    "L9_子系统/subsystems/longhun_notion_dashboard.py": {"ipa_route":"IPA-L9-010","module_class":"L9::NotionDash","status":"active","layer":"L9","consumed_by":[]},
}


def main():
    added = 0
    for path, entry in NEW_ENTRIES.items():
        if path not in dep:
            dep[path] = {
                "ipa_route": entry["ipa_route"],
                "module_class": entry["module_class"],
                "produced_by": [path],
                "consumed_by": entry["consumed_by"],
                "status": entry["status"],
                "layer": entry["layer"]
            }
            added += 1

        if entry["ipa_route"] not in existing_ipa:
            routes.append({
                "node_id": entry["ipa_route"],
                "local_path": path,
                "layer": entry["layer"],
                "status": entry["status"],
                "module_class": entry["module_class"]
            })
            existing_ipa.add(entry["ipa_route"])

    reg['_meta']['version'] = 'v1.3'
    reg['_meta']['last_updated'] = '丙午·乙未·甲寅·申时'
    reg['_meta']['dna'] = '#龍芯⚡️丙午·乙未·甲寅·申时·师-PERSONA-KNOWLEDGE-REGISTRY-v1.3'
    reg['_meta']['covered_layers'] = ['L1','L2','L5','L6','L7','L8','L9']

    reg_path.write_text(json.dumps(reg, ensure_ascii=False, indent=2), encoding='utf-8')

    print(f'✅ 注册表 v1.3: +{added} 模块')
    print(f'   dependency_graph: {len(dep)} 条目')
    print(f'   ipa_routes: {len(routes)} 路由')
    print(f'   covered_layers: {reg["_meta"]["covered_layers"]}')
    return 0

if __name__ == '__main__':
    exit(main())

# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# DNA: #龍芯⚡️丙午·丙申·甲寅·申时·观-CONFIRM-SEAL-lh_registry_extend-8D83BF2C
