#!/usr/bin/env python3
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# -*- coding: utf-8 -*-
"""
龍魂道引器 · Gitee v2.0 批量吸收（元数据卡模式）

作用：将17个Gitee鸿蒙生态仓库的元数据参数卡写入道引链。
哲学：道引吸收分两步 — ①元数据入链（本脚本）②代码镜像异步补充。
    来源可查、许可证可溯、德字闸可过、DNA可追、IPA可配。

DNA: #龍芯⚡️丙午·丙申·丙辰·戊子·坎-DAOYIN-GITEE-V2-ABSORB-v1.0
"""

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

# ── 路径 ──
LONGHUN_ROOT = Path(__file__).resolve().parent.parent
DAOYIN_DIR = LONGHUN_ROOT / "L7_数据层" / "daoyin"
CHAIN_FILE = DAOYIN_DIR / "daoyin_chain.jsonl"
REGISTRY_FILE = DAOYIN_DIR / "daoyin_registry.jsonl"
ANTI_TAMPER = LONGHUN_ROOT / "bin" / "lh_anti_tamper.py"

SYSTEM_CONFIRM = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def short_hash(text: str, length: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def generate_dna(action: str, source_hash: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
    return f"#龍芯⚡️{ts}-DAOYIN-{action.upper()}-{source_hash[:8].upper()}"


def append_jsonl(path: Path, records: List[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load_registry_sources() -> set[str]:
    """加载已注册的来源URL集合（用于去重）"""
    if not REGISTRY_FILE.exists():
        return set()
    sources = set()
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                sources.add(rec.get("source", ""))
            except json.JSONDecodeError:
                continue
    return sources


# ═══════════════════════════════════════════════════════════
# 17 仓库名单 · 5 梯队 · 元数据
# ═══════════════════════════════════════════════════════════

REPOS: List[Dict] = [
    # ── 第一梯队：鸿蒙底层与内核（权重:10）──
    {
        "source": "https://gitee.com/openharmony/kernel_linux_5.10",
        "tier": 1, "weight": 10,
        "name": "OpenHarmony Linux 5.10 内核",
        "desc": "OpenHarmony 操作系统 Linux 5.10 内核，支持 ARM64/RISC-V 多架构",
        "license_guess": "GPL-2.0",
        "ipa_targets": ["IPA-01-北辰", "IPA-11-程序师", "IPA-02-龍芯"],
        "keywords": ["kernel", "linux", "arm64", "aarch64", "device-tree", "driver", "mmu", "gic"],
        "harmony_dimensions": ["kernel_driver", "security_hardening"],
        "status": "verified",  # 已验证 Gitee 页面存在
    },
    {
        "source": "https://gitee.com/openharmony/drivers_peripheral",
        "tier": 1, "weight": 10,
        "name": "OpenHarmony 外设驱动框架",
        "desc": "HDI接口+HAL实现+驱动模型+测试用例，覆盖音频/编解码/显示/USB等",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-11-程序师", "IPA-01-北辰"],
        "keywords": ["driver", "hdi", "hal", "audio", "codec", "display", "usb", "sensor"],
        "harmony_dimensions": ["kernel_driver", "ui_framework"],
        "status": "verified",
    },
    {
        "source": "https://gitee.com/openharmony/distributed_hardware",
        "tier": 1, "weight": 10,
        "name": "OpenHarmony 分布式硬件",
        "desc": "分布式软总线、设备发现、设备管理、分布式调度等核心能力",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-01-北辰", "IPA-11-程序师", "IPA-15-乔前辈"],
        "keywords": ["distributed", "softbus", "device-discovery", "scheduler", "harmonyos"],
        "harmony_dimensions": ["kernel_driver", "network_protocol"],
        "status": "pending_verify",  # 需验证 Gitee URL
    },
    {
        "source": "https://gitee.com/openharmony/ability_base",
        "tier": 1, "weight": 10,
        "name": "OpenHarmony Ability 基础框架",
        "desc": "Ability 生命周期管理、进程模型、跨设备迁移等应用框架基础",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-01-北辰", "IPA-11-程序师"],
        "keywords": ["ability", "lifecycle", "process-model", "cross-device", "migration"],
        "harmony_dimensions": ["ui_framework"],
        "status": "pending_verify",
    },

    # ── 第二梯队：鲲鹏/昇腾底层算力适配（权重:10）──
    {
        "source": "https://gitee.com/kunpengcompute/KunpengBoostKit",
        "tier": 2, "weight": 10,
        "name": "鲲鹏 BoostKit 应用使能套件",
        "desc": "鲲鹏计算平台加速库：KAE加密加速、KML数学库、大数据/HPC加速等",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-01-北辰", "IPA-30-守护者"],
        "keywords": ["kunpeng", "arm64", "acceleration", "kae", "crypto", "bigdata", "hpc"],
        "harmony_dimensions": ["guomi_crypto", "ai_ml", "security_hardening"],
        "status": "verified_org_exists",
        "note": "kunpengcompute 组织存在，具体仓库路径可能为 boostkit-* 子仓",
    },
    {
        "source": "https://gitee.com/ascend/ascend-cann-toolkit",
        "tier": 2, "weight": 10,
        "name": "昇腾 CANN Toolkit",
        "desc": "昇腾 AI 处理器异构计算架构，含算子库/图引擎/运行时/驱动",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-01-北辰", "IPA-11-程序师", "IPA-02-龍芯"],
        "keywords": ["ascend", "npu", "cann", "operator", "graph-engine", "runtime", "ai"],
        "harmony_dimensions": ["ai_ml", "compiler_toolchain"],
        "status": "pending_verify",
        "note": "昇腾 CANN 以软件包发布，Gitee 仓库地址需确认",
    },
    {
        "source": "https://gitee.com/openeuler/kernel",
        "tier": 2, "weight": 10,
        "name": "openEuler 内核",
        "desc": "openEuler 操作系统内核，适配鲲鹏/飞腾/海光等国产CPU",
        "license_guess": "GPL-2.0",
        "ipa_targets": ["IPA-01-北辰", "IPA-11-程序师", "IPA-02-龍芯"],
        "keywords": ["kernel", "openeuler", "kunpeng", "phytium", "hygon", "arm64", "x86"],
        "harmony_dimensions": ["kernel_driver", "security_hardening"],
        "status": "pending_verify",
    },
    {
        "source": "https://gitee.com/mindspore/mindspore",
        "tier": 2, "weight": 10,
        "name": "MindSpore 全场景 AI 框架",
        "desc": "华为昇思 MindSpore，支持端边云全场景的深度学习框架",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-01-北辰", "IPA-11-程序师", "IPA-02-龍芯"],
        "keywords": ["mindspore", "deep-learning", "neural-network", "ascend", "npu", "training"],
        "harmony_dimensions": ["ai_ml", "compiler_toolchain"],
        "status": "verified",
    },

    # ── 第三梯队：国产安全与国密算法（权重:10）──
    {
        "source": "https://gitee.com/gmssl/GmSSL",
        "tier": 3, "weight": 10,
        "name": "GmSSL 国密算法库（Gitee镜像）",
        "desc": "北京大学开源国密SM2/SM3/SM4/SM9/SSL密码工具箱",
        "license_guess": "BSD-3-Clause",
        "ipa_targets": ["IPA-30-守护者", "IPA-09-法官"],
        "keywords": ["sm2", "sm3", "sm4", "sm9", "guomi", "国密", "tls", "ssl", "certificate"],
        "harmony_dimensions": ["guomi_crypto"],
        "status": "gitee_404",
        "note": "⚠️ gitee.com/gmssl/GmSSL 返回404，官方仓库在 github.com/guanzhi/GmSSL（已道引吸收）",
        "alternative": "github.com/guanzhi/GmSSL (已吸收: F542263F)",
        "skip_absorb": True,  # 已吸收，跳过
    },
    {
        "source": "https://gitee.com/openeuler/openssl",
        "tier": 3, "weight": 10,
        "name": "openEuler OpenSSL（国密增强版）",
        "desc": "openEuler 定制的 OpenSSL，含国密 SM2/SM3/SM4 算法支持",
        "license_guess": "Apache-2.0 (OpenSSL License)",
        "ipa_targets": ["IPA-30-守护者", "IPA-09-法官"],
        "keywords": ["openssl", "sm2", "sm3", "sm4", "tls", "ssl", "certificate", "crypto"],
        "harmony_dimensions": ["guomi_crypto", "security_hardening"],
        "status": "pending_verify",
    },
    {
        "source": "https://gitee.com/openharmony/security_huks",
        "tier": 3, "weight": 10,
        "name": "OpenHarmony 通用密钥库系统 (HUKS)",
        "desc": "鸿蒙通用密钥库，提供密钥生成/存储/使用/销毁全生命周期管理",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-30-守护者", "IPA-09-法官"],
        "keywords": ["huks", "keystore", "keymaster", "key-generation", "secure-boot", "tee"],
        "harmony_dimensions": ["guomi_crypto", "security_hardening"],
        "status": "verified",
    },

    # ── 第四梯队：方舟编译器与工具链（权重:9）──
    {
        "source": "https://gitee.com/openarkcompiler/OpenArkCompiler",
        "tier": 4, "weight": 9,
        "name": "方舟编译器 OpenArkCompiler",
        "desc": "华为方舟编译器开源项目，支持多语言多芯片联合编译运行",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-11-程序师", "IPA-01-北辰", "IPA-02-龍芯"],
        "keywords": ["compiler", "llvm", "jit", "aot", "bytecode", "cross-compile", "toolchain"],
        "harmony_dimensions": ["compiler_toolchain"],
        "status": "verified",
    },
    {
        "source": "https://gitee.com/openharmony-tpc/ohos_build",
        "tier": 4, "weight": 9,
        "name": "OpenHarmony 三方库构建系统",
        "desc": "鸿蒙第三方组件构建与集成工具链",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-11-程序师", "IPA-15-乔前辈"],
        "keywords": ["build", "cmake", "gn", "ninja", "third-party", "package", "dependency"],
        "harmony_dimensions": ["compiler_toolchain"],
        "status": "pending_verify",
    },

    # ── 第五梯队：鸿蒙 UI 框架与图形渲染（权重:8）──
    {
        "source": "https://gitee.com/openharmony/ui",
        "tier": 5, "weight": 8,
        "name": "OpenHarmony UI 框架",
        "desc": "鸿蒙 ArkUI 声明式 UI 框架，组件/布局/动画/事件系统",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-11-程序师", "IPA-01-北辰"],
        "keywords": ["arkui", "declarative", "component", "layout", "animation", "event"],
        "harmony_dimensions": ["ui_framework"],
        "status": "pending_verify",
    },
    {
        "source": "https://gitee.com/openharmony/graphic_2d",
        "tier": 5, "weight": 8,
        "name": "OpenHarmony 2D 图形渲染",
        "desc": "2D 渲染引擎、动画引擎、显示与内存管理",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-11-程序师", "IPA-01-北辰"],
        "keywords": ["graphic", "2d", "render", "canvas", "skia", "opengl", "gpu", "display"],
        "harmony_dimensions": ["ui_framework"],
        "status": "pending_verify",
        "note": "Gitee 上可能为 graphic_graphic_2d 路径",
    },
    {
        "source": "https://gitee.com/openharmony/graphic_3d",
        "tier": 5, "weight": 8,
        "name": "OpenHarmony 3D 图形渲染",
        "desc": "3D 渲染引擎、OpenGL ES/Vulkan 适配",
        "license_guess": "Apache-2.0",
        "ipa_targets": ["IPA-11-程序师", "IPA-01-北辰"],
        "keywords": ["graphic", "3d", "opengl", "vulkan", "gpu", "shader", "render"],
        "harmony_dimensions": ["ui_framework"],
        "status": "pending_verify",
    },
]


def main():
    print(f"\n🔰 龍魂道引器 · Gitee v2.0 批量元数据卡吸收")
    print(f"   链文件: {CHAIN_FILE}")
    print(f"   注册表: {REGISTRY_FILE}")
    print(f"   {'='*60}")

    # 加载已注册来源
    existing_sources = load_registry_sources()
    print(f"\n   已注册来源: {len(existing_sources)} 个")

    new_count = 0
    skip_count = 0
    param_cards = []
    registry_entries = []

    for repo in REPOS:
        source = repo["source"]
        tier = repo["tier"]
        tier_label = ["", "一", "二", "三", "四", "五"][tier]

        # 去重检查
        if source in existing_sources:
            print(f"   ⏭️ 跳过(已注册): 第{tier_label}梯队 {repo['name']}")
            skip_count += 1
            continue

        if repo.get("skip_absorb"):
            print(f"   ⏭️ 跳过(Gitee不可用): [T{tier}] {repo['name']} — {repo.get('note', '')}")
            skip_count += 1
            continue

        # 生成元数据文本用于评分
        meta_text = f"{repo['name']} {repo['desc']} {' '.join(repo['keywords'])}"
        source_hash = short_hash(source + meta_text)

        # 生成参数卡
        param_card = {
            "type": "daoyin_param_card_v2",
            "version": "2.0",
            "absorb_mode": "metadata_card",
            "absorbed_at": now_iso(),
            "source": source,
            "source_type": "gitee",
            "source_hash": source_hash,
            "tier": tier,
            "weight": repo["weight"],
            "name": repo["name"],
            "description": repo["desc"],
            "license": {"spdx": repo["license_guess"], "mode": "metadata_guess"},
            "ipa_targets": repo["ipa_targets"],
            "harmony_dimensions": repo["harmony_dimensions"],
            "verify_status": repo["status"],
            "dna": generate_dna("GITEE_META", source_hash),
            "confirm": SYSTEM_CONFIRM,
            "note": repo.get("note", ""),
        }
        param_cards.append(param_card)

        registry_entry = {
            "source": source,
            "source_hash": source_hash,
            "license": repo["license_guess"],
            "ipa_targets": repo["ipa_targets"],
            "harmony_score": repo["weight"] * 10,
            "absorbed_at": now_iso(),
            "dna": param_card["dna"],
            "mirror_id": "metadata_only",
            "confirm": SYSTEM_CONFIRM,
            "tier": tier,
            "name": repo["name"],
        }
        registry_entries.append(registry_entry)

        status_icon = {"verified": "✅", "pending_verify": "🟡", "verified_org_exists": "🟡", "gitee_404": "🔴"}.get(repo["status"], "❓")
        print(f"   {status_icon} 第{tier_label}梯队 [{repo['weight']}] {repo['name']}")
        print(f"      许可证: {repo['license_guess']} | IPA: {', '.join(repo['ipa_targets'])}")
        print(f"      DNA: {param_card['dna']}")
        new_count += 1

    print(f"\n   {'='*60}")
    print(f"   📊 汇总: 新增 {new_count} · 跳过 {skip_count} · 总计 {len(REPOS)}")

    if not param_cards:
        print(f"\n   ⚠️ 无新增记录，全部已注册或已跳过。")
        return

    # 写入 JSONL
    print(f"\n   📝 写入道引链...")
    append_jsonl(CHAIN_FILE, param_cards)
    print(f"   ✅ 入链: {CHAIN_FILE} (+{len(param_cards)} 条)")

    append_jsonl(REGISTRY_FILE, registry_entries)
    print(f"   ✅ 注册表: {REGISTRY_FILE} (+{len(registry_entries)} 条)")

    # 生成批次报表
    report_path = DAOYIN_DIR / f"gitee_v2_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.md"
    report_lines = [
        f"# 龍魂道引 · Gitee v2.0 批量吸收报表",
        f"",
        f"> 吸收时间: {now_iso()}",
        f"> 模式: 元数据卡（代码镜像异步补充）",
        f"> 确认码: {SYSTEM_CONFIRM}",
        f"",
        f"## 汇总",
        f"",
        f"| 指标 | 数值 |",
        f"|------|------|",
        f"| 目标仓库 | {len(REPOS)} |",
        f"| ✅ 新增入链 | {new_count} |",
        f"| ⏭️ 跳过 | {skip_count} |",
        f"| 🔗 DNA 生成 | {new_count} |",
        f"",
        f"## 按梯队分组",
        f"",
    ]

    for tier_num in range(1, 6):
        tier_label = ["", "一", "二", "三", "四", "五"][tier_num]
        tier_repos = [r for r in REPOS if r["tier"] == tier_num]
        report_lines.append(f"### 第{tier_label}梯队（权重: {tier_repos[0]['weight'] if tier_repos else 'N/A'}）")
        report_lines.append(f"")
        for r in tier_repos:
            status = r["status"]
            icon = {"verified": "✅", "pending_verify": "🟡", "verified_org_exists": "🟡", "gitee_404": "🔴"}.get(status, "❓")
            skip = " ⏭️已跳过" if r.get("skip_absorb") else ""
            report_lines.append(f"- {icon} **{r['name']}**{skip}")
            report_lines.append(f"  - 来源: `{r['source']}`")
            report_lines.append(f"  - 许可证(推测): {r['license_guess']}")
            report_lines.append(f"  - IPA: {', '.join(r['ipa_targets'])}")
            report_lines.append(f"  - 适配维度: {', '.join(r['harmony_dimensions'])}")
            if r.get("note"):
                report_lines.append(f"  - 备注: {r['note']}")
            if r.get("alternative"):
                report_lines.append(f"  - 替代来源: {r['alternative']}")
            report_lines.append(f"")
        report_lines.append(f"")

    report_lines.extend([
        f"---",
        f"",
        f"## 下一步",
        f"",
        f"1. 验证 🟡 状态仓库的 Gitee URL 正确性",
        f"2. 对 🔴 状态仓库查找替代来源",
        f"3. 代码镜像异步补充（git clone → 参数压缩 → 存入 mirror/）",
        f"4. 完成后将 `absorb_mode: metadata_card` 升级为 `absorb_mode: full`",
        f"",
        f"---",
        f"*道引：以道为引，纳开源智慧于龍魂体系。来源可查、去向可追、责任可究。*",
    ])

    report_path.write_text("\n".join(report_lines), encoding="utf-8")
    print(f"   ✅ 报表: {report_path}")

    # 同时保存 JSON 报表
    json_report_path = DAOYIN_DIR / f"gitee_v2_report_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.json"
    json_report = {
        "batch": "gitee_v2_metadata_cards",
        "absorbed_at": now_iso(),
        "total": len(REPOS),
        "new": new_count,
        "skipped": skip_count,
        "repos": [
            {
                "source": r["source"],
                "name": r["name"],
                "tier": r["tier"],
                "weight": r["weight"],
                "dna": next((c["dna"] for c in param_cards if c["source"] == r["source"]), ""),
                "status": r["status"],
                "skip": r.get("skip_absorb", False),
                "ipa": r["ipa_targets"],
            }
            for r in REPOS
        ],
    }
    json_report_path.write_text(json.dumps(json_report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"   ✅ JSON报表: {json_report_path}")


if __name__ == "__main__":
    main()
