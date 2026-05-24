# -*- coding: utf-8 -*-
"""四路示例：normal / burn / sealed / L0（供验收与快照）"""
from __future__ import annotations

from .cnsh_flow_decision_core import CONFIRM_REQUIRED, GPG_REQUIRED, run_flow_decision


def example_normal() -> dict:
    r = run_flow_decision(
        "函数 主函数() 返回类型 整数 { 打印「你好」 返回 0 }",
        {
            "title": "示例·常态",
            "confirm_code": CONFIRM_REQUIRED,
            "gpg": GPG_REQUIRED,
            "privacy_mode": "normal",
            "dna_current": "#龍芯⚡️2026-05-03-EX-NORMAL-v1.0",
        },
    )
    return {"name": "normal", "fused": r.fused, "status": r.node.result_status, "receipts": len(r.ipa_receipts)}


def example_burn() -> dict:
    r = run_flow_decision(
        "临时草稿·不保留正文",
        {
            "title": "示例·burn",
            "confirm_code": CONFIRM_REQUIRED,
            "gpg": GPG_REQUIRED,
            "privacy_mode": "burn",
        },
    )
    return {
        "name": "burn",
        "fused": r.fused,
        "destroy_proof": bool(r.node.storage_destroy_proof),
        "raw_allowed": r.node.raw_body_allowed,
    }


def example_sealed() -> dict:
    r = run_flow_decision(
        "正文不可持久化",
        {
            "title": "示例·sealed",
            "confirm_code": CONFIRM_REQUIRED,
            "gpg": GPG_REQUIRED,
            "privacy_mode": "sealed",
        },
    )
    return {"name": "sealed", "hold": r.node.result_status == "hold", "seal_proof": bool(r.node.storage_seal_proof)}


def example_l0() -> dict:
    r = run_flow_decision(
        "L0 永恒档",
        {
            "title": "示例·L0",
            "confirm_code": CONFIRM_REQUIRED,
            "gpg": GPG_REQUIRED,
            "level": "L0永恒",
        },
    )
    return {
        "name": "L0",
        "need_uid_confirm": r.node.audit_need_uid_confirm,
        "tricolor": r.node.audit_tricolor,
    }


def all_examples() -> dict:
    return {
        "normal": example_normal(),
        "burn": example_burn(),
        "sealed": example_sealed(),
        "L0": example_l0(),
    }
