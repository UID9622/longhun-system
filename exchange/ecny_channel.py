#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龍魂审计链 · 数字人民币结算通道 v1.0
DNA: #龍芯⚡️2026-08-23-ECNY-CHANNEL-v1.0-UID9622
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

两种模式:
  sandbox → 本地模拟，零配置，立即可用
  live    → 对接数币达跨境结算 API（有 API Key 后自动切换）
"""

import json, sqlite3, os, time, yaml, urllib.request
from datetime import datetime
from dna_utils import generate_dna, now_iso

DB_PATH = os.path.join(os.path.dirname(__file__), "db", "ledger.db")
CFG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")

def _load_cfg() -> dict:
    with open(CFG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

class ECNYChannel:
    """
    数字人民币结算通道
    · sandbox 模式：本地记账，立即确认，零外部依赖
    · live 模式：对接数币达API，真实跨境结算
    """

    def __init__(self):
        cfg = _load_cfg()["ecny"]
        # 🔴 P77 加固：API Key 优先从环境变量注入（禁明文入库），有值自动升 live
        self.api_key = (os.environ.get("ECNY_API_KEY") or cfg.get("api_key") or "").strip()
        self.api_base = cfg.get("live_api_base", "")
        self.merchant_id = cfg["merchant_id"]
        self.notify_url = (os.environ.get("ECNY_NOTIFY_URL") or cfg.get("notify_url") or "").strip()
        if self.api_key:
            self.mode = "live"
        else:
            self.mode = "sandbox"
        print(f"  💴 ECNYChannel 模式: {self.mode}")

    def settle(self, ecny_amount: float, recipient: str,
               payment_dna: str = "") -> dict:
        """
        执行 eCNY 结算
        返回: { settle_dna, status, mode, ecny_amount, recipient, confirmed_at }
        """
        settle_dna = generate_dna("SETTLE", {
            "amount": ecny_amount,
            "recipient": recipient,
            "payment_dna": payment_dna,
        })

        if self.mode == "sandbox":
            return self._sandbox_settle(ecny_amount, recipient, settle_dna, payment_dna)
        else:
            return self._live_settle(ecny_amount, recipient, settle_dna)

    def _sandbox_settle(self, amount: float, recipient: str,
                        settle_dna: str, payment_dna: str = "") -> dict:
        """沙盒模式：本地记账，瞬时确认"""
        confirmed_at = now_iso()
        # 写账本（🔴 修复 2026-08-24：原实现用 recipient 匹配 dna 列→永远更新不到账，改按 payment_dna）
        conn = sqlite3.connect(DB_PATH)
        if payment_dna:
            conn.execute(
                "UPDATE payments SET status='settled', settle_dna=? "
                "WHERE dna=?",
                (settle_dna, payment_dna)
            )
        conn.commit()
        conn.close()

        return {
            "settle_dna":   settle_dna,
            "status":       "settled",
            "mode":         "sandbox",
            "ecny_amount":  amount,
            "recipient":    recipient,
            "confirmed_at": confirmed_at,
            "tri_color":    "🟢",
            "note":         "沙盒模式·本地确认·等API Key后自动切换live",
        }

    def _live_settle(self, amount: float, recipient: str,
                     settle_dna: str) -> dict:
        """Live 模式：对接数币达跨境结算API"""
        # 🔴 P77 加固：notify_url 禁止硬编码假域名，未配置则拒绝 live
        if not self.notify_url:
            return {
                "settle_dna":   settle_dna,
                "status":       "failed",
                "mode":         "live",
                "ecny_amount":  amount,
                "recipient":    recipient,
                "confirmed_at": now_iso(),
                "error":        "notify_url 未配置：请设置环境变量 ECNY_NOTIFY_URL（P77 安全门）",
                "tri_color":    "🔴",
            }
        payload = json.dumps({
            "merchant_id": self.merchant_id,
            "amount":      amount,
            "currency":    "eCNY",
            "recipient":   recipient,
            "out_trade_no": settle_dna,
            "notify_url":  self.notify_url,
        }).encode()

        req = urllib.request.Request(
            f"{self.api_base}/transfer",
            data=payload,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
                "X-DNA": settle_dna,
            },
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                result = json.loads(resp.read().decode())
                return {
                    "settle_dna":   settle_dna,
                    "status":       result.get("status", "submitted"),
                    "mode":         "live",
                    "ecny_amount":  amount,
                    "recipient":    recipient,
                    "confirmed_at": now_iso(),
                    "api_response": result,
                    "tri_color":    "🟢",
                }
        except Exception as e:
            # 🔴 P77 加固：live 失败禁止静默降级 sandbox（防虚假结算记录），如实报错终止
            print(f"  🔴 Live API 结算失败（不降级·如实上报）: {e}")
            return {
                "settle_dna":   settle_dna,
                "status":       "failed",
                "mode":         "live",
                "ecny_amount":  amount,
                "recipient":    recipient,
                "confirmed_at": now_iso(),
                "error":        f"live 结算失败（未降级）: {e}",
                "tri_color":    "🔴",
            }
