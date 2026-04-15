#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星辰记忆 · DNA认证版 v1.1-FIXED
DNA: #龍芯⚡️2026-03-24-STAR-DNA-AUTH-v1.1-FIXED
Bug修复记录:
  ①  activate_star_memory → DNAIdentity新增star_activated字段，真正持久化
  ②  示例签名 → 自动生成匹配签名，不再写死"0x1234abcd"
  ③  asyncio.create_task → 改为非阻塞线程，兼容同步调用环境
  ④  UserStatus全部纳入流程 → register/verify/activate/get_status都返回正确状态
"""
import hashlib
import json
import time
import secrets
import threading
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class UserStatus(Enum):
    STRANGER       = "stranger"        # 路人甲 - 无DNA
    DNA_UNVERIFIED = "dna_unverified"  # 有DNA但未认证
    DNA_VERIFIED   = "dna_verified"    # DNA已认证（绑数字人民币）
    STAR_ACTIVATED = "star_activated"  # 星辰记忆已激活 ← Bug①修复：真正用起来


@dataclass
class DNAIdentity:
    dna_hash:      str
    parent_dna:    Optional[str]
    generation:    int
    heart_seed:    str
    fire_seed:     str
    created_at:    float
    e_cny_bound:   bool = False
    e_cny_address: Optional[str] = None
    verified_at:   Optional[float] = None
    star_activated: bool = False      # ← Bug①修复：新增激活状态字段

    def is_verified(self) -> bool:
        return self.e_cny_bound and self.verified_at is not None

    def is_activated(self) -> bool:
        return self.is_verified() and self.star_activated

    def get_status(self) -> UserStatus:  # ← Bug④修复：统一状态查询
        if self.is_activated():
            return UserStatus.STAR_ACTIVATED
        if self.is_verified():
            return UserStatus.DNA_VERIFIED
        if self.dna_hash:
            return UserStatus.DNA_UNVERIFIED
        return UserStatus.STRANGER


@dataclass
class StarSignal:
    signal_id:       str
    timestamp:       float
    user_dna:        str
    scene_type:      str
    score:           int
    emotion_label:   List[str]
    match_degree:    float
    inclusion_delta: float
    auth_level:      str
    e_cny_signature: Optional[str]


class StarMemoryDNAAuth:
    VERSION = "1.1.0-FIXED"
    MOTTO   = "路人甲不配被记住"

    def __init__(self):
        self.dna_registry: Dict[str, DNAIdentity] = {}
        self.star_pool: List[StarSignal] = []
        self.stranger_count = 0
        self.require_e_cny  = True
        self.min_generation = 1

    def register_dna(self, heart_seed: str, fire_seed: str,
                     parent_dna: Optional[str] = None) -> Tuple[str, UserStatus]:
        dna_data = f"{heart_seed}{fire_seed}{time.time()}{secrets.token_hex(8)}"
        dna_hash = hashlib.sha256(dna_data.encode()).hexdigest()[:32]
        generation = 1
        if parent_dna and parent_dna in self.dna_registry:
            generation = self.dna_registry[parent_dna].generation + 1

        identity = DNAIdentity(
            dna_hash=dna_hash, parent_dna=parent_dna, generation=generation,
            heart_seed=hashlib.sha256(heart_seed.encode()).hexdigest()[:16],
            fire_seed=hashlib.sha256(fire_seed.encode()).hexdigest()[:16],
            created_at=time.time()
        )
        self.dna_registry[dna_hash] = identity
        print(f"🧬 DNA已注册: {dna_hash[:16]}... | 世代:{generation} | 状态:未认证")
        return dna_hash, UserStatus.DNA_UNVERIFIED

    def verify_dna(self, dna_hash: str, e_cny_address: str,
                   signature: str) -> Tuple[bool, UserStatus]:  # ← Bug④修复：返回状态
        if dna_hash not in self.dna_registry:
            print(f"❌ DNA不存在")
            return False, UserStatus.STRANGER
        identity = self.dna_registry[dna_hash]
        if not self._verify_e_cny_signature(dna_hash, e_cny_address, signature):
            print(f"❌ 数字人民币签名验证失败")
            return False, UserStatus.DNA_UNVERIFIED
        identity.e_cny_bound   = True
        identity.e_cny_address = e_cny_address
        identity.verified_at   = time.time()
        print(f"✅ DNA已认证: {dna_hash[:16]}... | 绑定地址:{e_cny_address[:20]}...")
        return True, UserStatus.DNA_VERIFIED  # ← Bug④修复

    def activate_star_memory(self, dna_hash: str) -> Tuple[bool, UserStatus]:  # ← Bug①④修复
        if dna_hash not in self.dna_registry:
            print(f"❌ DNA不存在")
            return False, UserStatus.STRANGER
        identity = self.dna_registry[dna_hash]
        if not identity.is_verified():
            print(f"❌ DNA未认证，请先绑定数字人民币")
            return False, UserStatus.DNA_UNVERIFIED
        identity.star_activated = True  # ← Bug①修复：真正写入激活状态
        print(f"🌟 星辰记忆已激活: {dna_hash[:16]}... | 信号将被永久记录")
        return True, UserStatus.STAR_ACTIVATED  # ← Bug④修复

    def get_status(self, dna_hash: str) -> UserStatus:  # ← Bug④辅助方法
        if dna_hash not in self.dna_registry:
            return UserStatus.STRANGER
        return self.dna_registry[dna_hash].get_status()

    def collect_signal(self, dna_hash: str, scene_type: str,
                       score: int, emotions: List[str],
                       input_hint: str, output_hint: str) -> Optional[str]:
        if dna_hash not in self.dna_registry:
            self.stranger_count += 1
            print(f"🚫 路人甲信号 #{self.stranger_count} - 丢弃（DNA未注册）")
            return None
        identity = self.dna_registry[dna_hash]
        # Bug①修复：检查star_activated，而非仅is_verified
        if not identity.is_activated():
            self.stranger_count += 1
            status = identity.get_status()
            print(f"🚫 信号丢弃 | 状态:{status.value} | 需先激活星辰记忆")
            return None
        match_degree = self._calculate_match(input_hint, output_hint)
        signal = StarSignal(
            signal_id=f"STAR-{int(time.time())}-{secrets.token_hex(4)}",
            timestamp=time.time(), user_dna=dna_hash, scene_type=scene_type,
            score=max(1, min(5, score)), emotion_label=emotions[:3],
            match_degree=round(match_degree, 2), inclusion_delta=0.0,
            auth_level="DNA+ECNY",
            e_cny_signature=identity.e_cny_address[:20] if identity.e_cny_address else None
        )
        self.star_pool.append(signal)
        # Bug③修复：包容度更新用线程，不用asyncio.create_task
        threading.Thread(target=self._update_inclusion_params,
                         args=(signal,), daemon=True).start()
        print(f"✅ 信号已记录: {signal.signal_id} | 场景:{scene_type} | 评分:{signal.score}")
        return signal.signal_id

    def get_stats(self) -> Dict:
        activated = sum(1 for d in self.dna_registry.values() if d.is_activated())
        return {
            "total_dna":       len(self.dna_registry),
            "verified_dna":    sum(1 for d in self.dna_registry.values() if d.is_verified()),
            "activated_star":  activated,
            "total_signals":   len(self.star_pool),
            "stranger_dropped": self.stranger_count,
            "motto":           self.MOTTO
        }

    def _verify_e_cny_signature(self, dna_hash: str, e_cny_address: str,
                                  signature: str) -> bool:
        expected = hashlib.sha256(
            f"{dna_hash}{e_cny_address}".encode()
        ).hexdigest()[:32]
        return signature == expected[:16]  # 取前16位做示例验证

    def _calculate_match(self, input_hint: str, output_hint: str) -> float:
        iw = set(input_hint.lower().split())
        ow = set(output_hint.lower().split())
        if not iw: return 0.5
        return min(1.0, len(iw & ow) / len(iw) * 2)

    def _update_inclusion_params(self, signal: StarSignal):
        """包容度异步更新（线程内执行）- Bug③修复点"""
        time.sleep(0.01)  # 模拟IO
        # 实际逻辑：读取pool统计 → 更新包容度参数 → 写回配置


# ═══════════════════════════════════════════════════
# 使用示例（Bug②修复：签名自动生成，不写死）
# ═══════════════════════════════════════════════════
if __name__ == "__main__":
    star = StarMemoryDNAAuth()
    print("=" * 60)
    print("🌟 星辰记忆 · DNA认证版 v1.1-FIXED")
    print("=" * 60)

    # 场景1: 路人甲
    print("\n📌 场景1: 路人甲")
    r = star.collect_signal("unknown", "情绪聊天", 5, ["开心"],
                             "今天很开心", "我也为你开心")
    print(f"   结果: {'记录' if r else '丢弃'}")

    # 场景2: 注册未认证
    print("\n📌 场景2: 注册但未认证")
    dna1, s = star.register_dna("我的心种子", "我的火种子")
    r = star.collect_signal(dna1, "情绪聊天", 5, ["开心"],
                             "今天很开心", "我也为你开心")
    print(f"   结果: {'记录' if r else '丢弃'} | 状态:{star.get_status(dna1).value}")

    # 场景3: 认证并激活 ← Bug②修复：签名自动生成
    print("\n📌 场景3: 认证+激活")
    e_cny_addr = "0x1234567890abcdef"
    # 正确签名 = sha256(dna+address)[:16]
    correct_sig = hashlib.sha256(
        f"{dna1}{e_cny_addr}".encode()
    ).hexdigest()[:16]  # ← Bug②修复：不写死"0x1234abcd"
    ok, s = star.verify_dna(dna1, e_cny_addr, correct_sig)
    print(f"   认证: {'✅' if ok else '❌'} | 状态:{star.get_status(dna1).value}")

    ok, s = star.activate_star_memory(dna1)
    print(f"   激活: {'✅' if ok else '❌'} | 状态:{star.get_status(dna1).value}")

    r = star.collect_signal(dna1, "情绪聊天", 5, ["开心", "被理解"],
                             "今天很开心", "我也为你开心")
    print(f"   结果: {'记录' if r else '丢弃'}")

    print("\n📊 统计")
    print(json.dumps(star.get_stats(), indent=2, ensure_ascii=False))
