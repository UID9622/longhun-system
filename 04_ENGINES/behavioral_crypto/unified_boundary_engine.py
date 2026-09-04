#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
"""
🐉 龍魂·行為密碼學統一引擎 v3.0
——七因子框架 + 行為邊界協議（私域豁免+公域溯源）· 一體化落地

DNA: #龍芯⚡️丙午·丙申·癸丑·午时·䷑蛊-UNIFIED-BOUNDARY-ENGINE-V3.0-UID9622
License: MulanPSL v2

升級內容:
  v2.0 → v3.0:
    + A0/A1/A2 三級授權碼系統
    + 三域（私域·社區·公域）行為邊界引擎
    + 跨域傳播追蹤（PropagationTree）
    + 邊界違規檢測 + 責任歸屬
    + 統一 R 值公式（七因子+邊界合併）
    + 責任塌縮概率模型（行為邊界版）

前置引用:
  - 七因子引擎: seven_factor_model.py v2.0
  - 行為邊界協議: 01_protocols/LH-BEHAVIOR-BOUNDARY-PROTOCOL-v1.0.md
  - 三色審計: 05_ENGINES/longhun/tricolor/

用法:
  from unified_boundary_engine import UnifiedBoundaryEngine
  engine = UnifiedBoundaryEngine()
  result = engine.analyze(text, author_id="UID9622", domain="public")
  # result 包含: fingerprint + authorization + boundary_check + propagation_risk
"""

import hashlib
import json
import math
import re
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple, Set, Any
from copy import deepcopy

# ── 導入七因子核心引擎 ──
from seven_factor_model import (
    SevenFactorEngine, BehavioralFingerprint, FactorFingerprint,
    FACTOR_DEFINITIONS, SOVEREIGN_ANCHOR, quick_fingerprint, verify_fingerprint,
)


# ═══════════════════════════════════════════════════════════════
# §0. 基礎枚舉與數據結構
# ═══════════════════════════════════════════════════════════════

class AuthLevel(str, Enum):
    """三級授權碼"""
    A0 = "A0"  # 私域·僅點對點
    A1 = "A1"  # 社區·指定社區可見
    A2 = "A2"  # 公域·全員可見


class Domain(str, Enum):
    """三域劃分"""
    PRIVATE = "private"       # 🟢 私域
    COMMUNITY = "community"   # 🟡 指定社區
    PUBLIC = "public"         # 🔴 公域


class PropagationEvent(str, Enum):
    """跨域傳播事件類型"""
    SHARE = "share"           # 轉發
    SCREENSHOT = "screenshot" # 截屏
    COPY = "copy"             # 複製
    UPGRADE = "upgrade"       # 授權升級（A0→A1/A2）
    LEAK = "leak"             # 泄露（未經授權跨域）


# ═══════════════════════════════════════════════════════════════
# §1. 傳播樹節點（不可篡改的追蹤鏈）
# ═══════════════════════════════════════════════════════════════

@dataclass
class PropagationNode:
    """傳播樹節點——每一跳的DNA子碼"""
    node_id: str                          # 節點唯一ID
    parent_id: Optional[str]              # 父節點ID（根為None）
    propagator_id: str                    # 傳播者身份
    timestamp: str                        # 傳播時間 ISO
    domain_from: Domain                   # 來源域
    domain_to: Domain                     # 目標域
    event_type: PropagationEvent          # 事件類型
    auth_level_before: AuthLevel          # 傳播前授權級別
    auth_level_after: AuthLevel           # 傳播後授權級別
    content_hash: str                     # 內容指紋
    authorized: bool                      # 是否經授權
    metadata: Dict = field(default_factory=dict)  # 擴展元數據
    
    def to_dict(self) -> Dict:
        return {
            "node_id": self.node_id,
            "parent_id": self.parent_id,
            "propagator_id": self.propagator_id,
            "timestamp": self.timestamp,
            "domain_from": self.domain_from.value,
            "domain_to": self.domain_to.value,
            "event_type": self.event_type.value,
            "auth_before": self.auth_level_before.value,
            "auth_after": self.auth_level_after.value,
            "content_hash": self.content_hash,
            "authorized": self.authorized,
            "metadata": self.metadata,
        }
    
    @property
    def dna_subcode(self) -> str:
        """生成DNA子碼"""
        seed = f"{self.propagator_id}{self.timestamp}{self.domain_to.value}{self.event_type.value}"
        return hashlib.sha3_256(seed.encode()).hexdigest()[:12]


@dataclass
class PropagationTree:
    """不可篡改的傳播樹"""
    root: PropagationNode
    nodes: Dict[str, PropagationNode] = field(default_factory=dict)
    edges: List[Tuple[str, str]] = field(default_factory=list)  # (parent_id, child_id)
    tree_hash: str = ""
    
    def __post_init__(self):
        self.nodes[self.root.node_id] = self.root
        self._rehash()
    
    def add_node(self, node: PropagationNode) -> str:
        """追加傳播節點"""
        if node.node_id in self.nodes:
            raise ValueError(f"節點 {node.node_id} 已存在，傳播樹不可覆寫")
        self.nodes[node.node_id] = node
        if node.parent_id:
            self.edges.append((node.parent_id, node.node_id))
        self._rehash()
        return node.node_id
    
    def trace_path(self, node_id: str) -> List[PropagationNode]:
        """從根追溯到指定節點的完整路徑"""
        path = []
        current_id = node_id
        while current_id is not None:
            if current_id not in self.nodes:
                break
            node = self.nodes[current_id]
            path.insert(0, node)
            current_id = node.parent_id
        return path
    
    def find_leak_nodes(self) -> List[PropagationNode]:
        """查找所有未經授權的泄露節點"""
        return [n for n in self.nodes.values() if n.event_type == PropagationEvent.LEAK or not n.authorized]
    
    def propagation_depth(self) -> int:
        """計算傳播樹最大深度"""
        depths = {}
        for node in self.nodes.values():
            depth = 0
            current = node
            while current.parent_id and current.parent_id in self.nodes:
                depth += 1
                current = self.nodes[current.parent_id]
            depths[node.node_id] = depth
        return max(depths.values()) if depths else 0
    
    def to_dict(self) -> Dict:
        return {
            "root": self.root.to_dict(),
            "node_count": len(self.nodes),
            "edge_count": len(self.edges),
            "depth": self.propagation_depth(),
            "leak_nodes": [n.node_id for n in self.find_leak_nodes()],
            "tree_hash": self.tree_hash,
            "nodes": {k: v.to_dict() for k, v in self.nodes.items()},
            "edges": [list(e) for e in self.edges],
        }
    
    def _rehash(self):
        """重新計算整棵樹的哈希"""
        seed = "|".join(sorted(self.nodes.keys()))
        self.tree_hash = hashlib.sha3_256(seed.encode()).hexdigest()[:16]


# ═══════════════════════════════════════════════════════════════
# §2. 統一分析結果
# ═══════════════════════════════════════════════════════════════

@dataclass
class UnifiedAnalysisResult:
    """七因子+邊界協議 統一結果"""
    # 七因子指紋
    fingerprint: BehavioralFingerprint
    
    # 授權與邊界
    auth_level: AuthLevel                    # 當前授權級別
    domain: Domain                           # 當前所在域
    dna_with_auth: str                       # 嵌入授權碼的DNA
    boundary_compliant: bool                 # 是否邊界合規
    
    # 跨域追蹤
    propagation_tree: Optional[PropagationTree] = None
    propagation_risk: float = 0.0            # 傳播風險 0-1
    leak_detected: bool = False              # 是否檢測到泄露
    
    # 統一R值（七因子+邊界合併）
    unified_r: float = 0.0                   # 統一風險評分 0-100
    
    # 責任歸屬
    responsibility_chain: List[Dict] = field(default_factory=list)
    primary_responsible: Optional[str] = None
    
    # 審計
    audit_mark: str = "🟢"
    audit_details: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    
    def to_dict(self) -> Dict:
        result = {
            "dna": self.dna_with_auth,
            "timestamp": self.timestamp,
            "unified_r": self.unified_r,
            "audit_mark": self.audit_mark,
            "auth_level": self.auth_level.value,
            "domain": self.domain.value,
            "boundary_compliant": self.boundary_compliant,
            "propagation_risk": self.propagation_risk,
            "leak_detected": self.leak_detected,
            "fingerprint": self.fingerprint.to_dict(),
            "responsibility": {
                "primary_responsible": self.primary_responsible,
                "chain": self.responsibility_chain,
            },
            "audit_details": self.audit_details,
        }
        if self.propagation_tree:
            result["propagation_tree"] = self.propagation_tree.to_dict()
        return result


# ═══════════════════════════════════════════════════════════════
# §3. 統一邊界引擎（核心）
# ═══════════════════════════════════════════════════════════════

class UnifiedBoundaryEngine:
    """
    龍魂·行為密碼學統一引擎 v3.0
    
    融合:
      - 七因子行為指紋提取（v2.0核心）
      - 三級授權碼系統（A0/A1/A2）
      - 三域行為邊界（私域·社區·公域）
      - 跨域傳播追蹤（不可篡改傳播樹）
      - 責任塌縮歸屬定位
    
    使用:
        engine = UnifiedBoundaryEngine()
        result = engine.analyze(text, author_id="UID9622", domain=Domain.PUBLIC)
        print(f"統一R值: {result.unified_r}, 授權: {result.auth_level.value}")
    """
    
    # ── 授權碼 → 域 映射表 ──
    AUTH_TO_DOMAIN = {
        AuthLevel.A0: [Domain.PRIVATE],
        AuthLevel.A1: [Domain.PRIVATE, Domain.COMMUNITY],
        AuthLevel.A2: [Domain.PRIVATE, Domain.COMMUNITY, Domain.PUBLIC],
    }
    
    # ── 跨域傳播規則表 ──
    CROSS_DOMAIN_RULES = {
        # (from_domain, from_auth, to_domain) → (allowed, required_auth, auto_upgrade)
        (Domain.PRIVATE, AuthLevel.A0, Domain.COMMUNITY):  (False, AuthLevel.A1, True),
        (Domain.PRIVATE, AuthLevel.A0, Domain.PUBLIC):     (False, AuthLevel.A2, False),
        (Domain.COMMUNITY, AuthLevel.A1, Domain.PUBLIC):   (True, AuthLevel.A2, True),
        (Domain.PRIVATE, AuthLevel.A1, Domain.PUBLIC):     (True, AuthLevel.A2, True),
        (Domain.PRIVATE, AuthLevel.A1, Domain.COMMUNITY):  (True, AuthLevel.A1, False),
    }
    
    def __init__(self):
        self.seven_factor_engine = SevenFactorEngine()
        self.propagation_trees: Dict[str, PropagationTree] = {}
        self.analysis_log: List[Dict] = []
        self.author_boundary_profiles: Dict[str, Dict] = {}
    
    # ── 授權碼生成 ──
    def generate_auth_level(self, domain: Domain, author_id: str,
                           is_adult_verified: bool = True) -> AuthLevel:
        """
        根據目標域自動分配授權碼
        
        數學規則:
          A = {
            A0,  if domain = PRIVATE
            A1,  if domain = COMMUNITY ∧ adult_verified
            A2,  if domain = PUBLIC
          }
        """
        if domain == Domain.PRIVATE:
            return AuthLevel.A0
        elif domain == Domain.COMMUNITY:
            return AuthLevel.A1 if is_adult_verified else AuthLevel.A0
        elif domain == Domain.PUBLIC:
            return AuthLevel.A2
        return AuthLevel.A0
    
    # ── 授權碼嵌入DNA ──
    def embed_auth_in_dna(self, base_dna: str, auth_level: AuthLevel) -> str:
        """
        在DNA中嵌入授權碼
        
        格式: #龍芯⚡️干支-A{X}-{hash}-UID9622
        """
        # 替換或追加授權碼
        if "-A" in base_dna:
            # 已有授權碼，替換
            return re.sub(r'-A\d-', f'-{auth_level.value}-', base_dna)
        else:
            # 未嵌入，在干支後追加
            return re.sub(
                r'(#龍芯⚡️\S+?)-',
                f'\\1-{auth_level.value}-',
                base_dna,
                count=1
            )
    
    # ── 授權驗證 ──
    def validate_authorization(self, auth_level: AuthLevel, target_domain: Domain) -> bool:
        """
        驗證授權碼是否允許在目標域傳播
        
        數學: validate(A, D) = D ∈ AUTH_TO_DOMAIN[A]
        """
        allowed_domains = self.AUTH_TO_DOMAIN.get(auth_level, [Domain.PRIVATE])
        return target_domain in allowed_domains
    
    # ── 跨域傳播規則判定 ──
    def check_cross_domain(self, from_domain: Domain, from_auth: AuthLevel,
                          to_domain: Domain) -> Tuple[bool, Optional[AuthLevel], bool]:
        """
        判定跨域傳播是否允許
        
        Returns:
          (allowed, required_upgrade_auth, auto_upgrade)
        
        數學模型:
          對於 (D_src, A_src) → D_dst:
            查表 RULES[(D_src, A_src, D_dst)]
            若不存在 → False (私域→公域默認禁止)
        """
        # 同域傳播始終允許
        if from_domain == to_domain:
            return (True, from_auth, False)
        
        # 降級傳播（公域→私域/社區）始終允許
        domain_order = {Domain.PRIVATE: 0, Domain.COMMUNITY: 1, Domain.PUBLIC: 2}
        if domain_order[from_domain] > domain_order[to_domain]:
            return (True, from_auth, False)
        
        # 查表
        rule = self.CROSS_DOMAIN_RULES.get((from_domain, from_auth, to_domain))
        if rule:
            return rule
        
        # 默認：私域內容不可越級傳播
        return (False, None, False)
    
    # ── 傳播樹創建 ──
    def create_propagation_tree(self, content_hash: str, author_id: str,
                               initial_domain: Domain, initial_auth: AuthLevel) -> PropagationTree:
        """為一段內容創建傳播樹（根節點=原始發布）"""
        root = PropagationNode(
            node_id=f"root_{uuid.uuid4().hex[:8]}",
            parent_id=None,
            propagator_id=author_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            domain_from=initial_domain,
            domain_to=initial_domain,
            event_type=PropagationEvent.SHARE,
            auth_level_before=initial_auth,
            auth_level_after=initial_auth,
            content_hash=content_hash,
            authorized=True,
            metadata={"role": "origin", "note": "原始發布節點"},
        )
        tree = PropagationTree(root=root)
        self.propagation_trees[content_hash] = tree
        return tree
    
    # ── 傳播事件記錄 ──
    def record_propagation(self, content_hash: str, propagator_id: str,
                          to_domain: Domain, event_type: PropagationEvent,
                          parent_node_id: Optional[str] = None) -> Dict:
        """
        記錄一次跨域傳播事件

        Args:
            parent_node_id: 父節點ID，默認使用傳播樹最後一個節點

        Returns:
          {
            allowed: bool,
            auto_upgraded: bool,
            new_auth: AuthLevel,
            leak: bool,
            node_id: str,
            dna_subcode: str,
          }
        """
        tree = self.propagation_trees.get(content_hash)
        if not tree:
            return {"error": "未找到傳播樹，請先用 create_propagation_tree 創建"}

        # 獲取父節點：優先使用指定 parent，否則找最新節點
        if parent_node_id and parent_node_id in tree.nodes:
            last_node = tree.nodes[parent_node_id]
        else:
            last_node = max(tree.nodes.values(), key=lambda n: n.timestamp)

        # 判定跨域規則
        allowed, required_auth, auto_upgrade = self.check_cross_domain(
            last_node.domain_to, last_node.auth_level_after, to_domain
        )

        new_auth = last_node.auth_level_after
        if auto_upgrade and required_auth:
            new_auth = required_auth

        leak = not allowed

        # 創建新節點
        node = PropagationNode(
            node_id=f"hop_{uuid.uuid4().hex[:8]}",
            parent_id=last_node.node_id,
            propagator_id=propagator_id,
            timestamp=datetime.now(timezone.utc).isoformat(),
            domain_from=last_node.domain_to,
            domain_to=to_domain,
            event_type=PropagationEvent.LEAK if leak else event_type,
            auth_level_before=last_node.auth_level_after,
            auth_level_after=new_auth,
            content_hash=content_hash,
            authorized=allowed,
            metadata={
                "auto_upgraded": auto_upgrade,
                "required_auth": required_auth.value if required_auth else None,
            },
        )

        tree.add_node(node)

        # 寫入傳播審計日誌
        self.analysis_log.append({
            "type": "propagation",
            "content_hash": content_hash,
            "node_id": node.node_id,
            "parent_node_id": last_node.node_id,
            "propagator_id": propagator_id,
            "domain_from": last_node.domain_to.value,
            "domain_to": to_domain.value,
            "event_type": node.event_type.value,
            "authorized": allowed,
            "leak": leak,
            "timestamp": node.timestamp,
        })

        return {
            "allowed": allowed,
            "auto_upgraded": auto_upgrade,
            "new_auth": new_auth.value,
            "leak": leak,
            "node_id": node.node_id,
            "dna_subcode": node.dna_subcode,
            "tree_depth": tree.propagation_depth(),
        }
    
    # ── 傳播風險計算 ──
    def calculate_propagation_risk(self, content_hash: str) -> float:
        """
        計算跨域傳播風險
        
        數學:
          P_risk = 1 - e^(-λ·d)
          其中:
            λ = 泄露節點數 / 總節點數（泄露密度）
            d = 傳播深度
        
        Returns:
          風險值 0-1
        """
        tree = self.propagation_trees.get(content_hash)
        if not tree or len(tree.nodes) <= 1:
            return 0.0
        
        leak_count = len(tree.find_leak_nodes())
        total_nodes = len(tree.nodes)
        depth = tree.propagation_depth()
        
        leak_density = leak_count / max(total_nodes, 1)
        risk = 1.0 - math.exp(-leak_density * depth)
        
        return round(min(1.0, risk), 4)
    
    # ── 責任歸屬定位 ──
    def attribute_responsibility(self, content_hash: str) -> List[Dict]:
        """
        在傳播鏈上定位責任節點
        
        數學:
          Rsp(node) = P(authorized=False) × time_weight × domain_penalty
          其中:
            time_weight = e^(-α·Δt)，Δt=距現在的時間（天）
            domain_penalty = {PRIVATE:0.1, COMMUNITY:0.5, PUBLIC:1.0}
        
        追責優先級: 公域泄露 > 社區泄露 > 私域內傳播
        """
        tree = self.propagation_trees.get(content_hash)
        if not tree:
            return []
        
        now = datetime.now(timezone.utc)
        alpha = 0.1  # 時間衰減係數
        domain_penalty_map = {
            Domain.PRIVATE: 0.1,
            Domain.COMMUNITY: 0.5,
            Domain.PUBLIC: 1.0,
        }
        
        responsibilities = []
        for node in tree.nodes.values():
            if node.node_id == tree.root.node_id or node.authorized:
                continue
            
            # 時間衰減
            try:
                t = datetime.fromisoformat(node.timestamp.replace('Z', '+00:00'))
                delta_days = (now - t).total_seconds() / 86400.0
            except Exception:
                delta_days = 0
            time_weight = math.exp(-alpha * delta_days)
            
            # 域懲罰係數
            domain_penalty = domain_penalty_map.get(node.domain_to, 0.5)
            
            # 責任分數
            resp_score = (1.0) * time_weight * domain_penalty
            
            responsibilities.append({
                "node_id": node.node_id,
                "propagator_id": node.propagator_id,
                "event_type": node.event_type.value,
                "domain_to": node.domain_to.value,
                "timestamp": node.timestamp,
                "days_ago": round(delta_days, 1),
                "time_weight": round(time_weight, 4),
                "domain_penalty": domain_penalty,
                "responsibility_score": round(resp_score, 4),
                "dna_subcode": node.dna_subcode,
            })
        
        # 按責任分數降序
        responsibilities.sort(key=lambda x: x["responsibility_score"], reverse=True)
        return responsibilities
    
    # ═══════════════════════════════════════════════════════════
    # §4. 統一R值公式（七因子+邊界合併）
    # ═══════════════════════════════════════════════════════════
    
    def calculate_unified_r(self, fingerprint: BehavioralFingerprint,
                           auth_level: AuthLevel, domain: Domain,
                           propagation_risk: float) -> float:
        """
        統一R值 = 七因子加權得分 × 邊界合規調整 × 傳播風險衰減
        
        數學:
          R_unified = R_seven × B_boundary × (1 - P_propagation)
          
          其中:
            R_seven = Σ(w_i × f_i)  （七因子加權綜合得分，0-1）
            B_boundary = {
              1.0,  若合規（授權碼匹配目標域）
              0.6,  若越級但可升級（A0→A1, A1→A2）
              0.2,  若泄露（未經授權跨域到公域）
            }
            P_propagation = 傳播風險（0-1）
        
        Returns:
          統一R值 0-100
        """
        R_seven = fingerprint.composite_score
        
        # 邊界合規調整
        compliant = self.validate_authorization(auth_level, domain)
        if compliant:
            B_boundary = 1.0
        elif auth_level == AuthLevel.A0 and domain == Domain.PUBLIC:
            B_boundary = 0.2  # 泄露
        else:
            B_boundary = 0.6  # 可升級
        
        # 統一R值
        R_unified = R_seven * B_boundary * (1.0 - propagation_risk)
        R_unified = max(0.0, min(1.0, R_unified))
        
        return round(R_unified * 100, 2)
    
    # ═══════════════════════════════════════════════════════════
    # §5. 主分析接口（一站式調用）
    # ═══════════════════════════════════════════════════════════
    
    def analyze(self, text: str, author_id: str = "UID9622",
               domain: Domain = Domain.PUBLIC,
               is_adult_verified: bool = True,
               existing_content_hash: Optional[str] = None) -> UnifiedAnalysisResult:
        """
        一站式行為密碼分析：七因子指紋 + 授權 + 邊界 + 傳播追蹤
        
        Args:
            text: 待分析文本
            author_id: 作者ID
            domain: 目標域（私域/社區/公域）
            is_adult_verified: 是否成年人驗證（社區用）
            existing_content_hash: 已存在的內容哈希（用於傳播追蹤）
        
        Returns:
            UnifiedAnalysisResult: 完整統一分析結果
        """
        # 確保 domain 為 Domain 枚舉 (兼容字符串傳入)
        if isinstance(domain, str):
            domain = Domain(domain)

        # Step 1: 提取七因子指紋
        self.seven_factor_engine.update_author_profile(author_id, text)
        fingerprint = self.seven_factor_engine.extract(text, author_id)
        
        # Step 2: 生成授權碼
        auth_level = self.generate_auth_level(domain, author_id, is_adult_verified)
        
        # Step 3: 嵌入授權碼到DNA
        dna_with_auth = self.embed_auth_in_dna(fingerprint.dna, auth_level)
        
        # Step 4: 邊界合規檢查
        boundary_compliant = self.validate_authorization(auth_level, domain)
        
        # Step 5: 傳播追蹤
        content_hash = existing_content_hash or fingerprint.factors[2].details.get("full_hash", "")
        if not content_hash:
            content_hash = hashlib.sha3_256(text.encode()).hexdigest()
        
        # 創建或獲取傳播樹
        if content_hash not in self.propagation_trees:
            self.create_propagation_tree(content_hash, author_id, domain, auth_level)
        
        propagation_risk = self.calculate_propagation_risk(content_hash)
        leak_detected = len(self.propagation_trees[content_hash].find_leak_nodes()) > 0
        
        # Step 6: 責任歸屬
        responsibility_chain = self.attribute_responsibility(content_hash)
        primary = responsibility_chain[0]["propagator_id"] if responsibility_chain else None
        
        # Step 7: 統一R值
        unified_r = self.calculate_unified_r(
            fingerprint, auth_level, domain, propagation_risk
        )
        
        # Step 8: 審計判定
        audit_mark, audit_details = self._determine_audit(
            fingerprint, boundary_compliant, leak_detected, unified_r, domain, auth_level
        )
        
        # 封裝結果
        result = UnifiedAnalysisResult(
            fingerprint=fingerprint,
            auth_level=auth_level,
            domain=domain,
            dna_with_auth=dna_with_auth,
            boundary_compliant=boundary_compliant,
            propagation_tree=self.propagation_trees.get(content_hash),
            propagation_risk=propagation_risk,
            leak_detected=leak_detected,
            unified_r=unified_r,
            responsibility_chain=responsibility_chain,
            primary_responsible=primary,
            audit_mark=audit_mark,
            audit_details=audit_details,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        
        self.analysis_log.append({
            "dna": dna_with_auth,
            "timestamp": result.timestamp,
            "author_id": author_id,
            "domain": domain.value,
            "auth_level": auth_level.value,
            "unified_r": unified_r,
            "audit": audit_mark,
        })
        
        return result
    
    # ── 三色審計判定 ──
    def _determine_audit(self, fingerprint: BehavioralFingerprint,
                        boundary_compliant: bool,
                        leak_detected: bool,
                        unified_r: float,
                        domain: Domain,
                        auth_level: AuthLevel) -> Tuple[str, List[str]]:
        """根據綜合結果判定三色審計"""
        details = []

        if leak_detected:
            return ("🔴", ["檢測到跨域泄露事件"])

        # 私域（A0）完全豁免：不進入公域審計流
        if domain == Domain.PRIVATE and auth_level == AuthLevel.A0 and boundary_compliant:
            return ("🟢", [f"私域A0豁免·統一R值={unified_r:.1f}"])

        if not boundary_compliant:
            details.append("邊界不合規：授權碼不匹配目標域")

        if unified_r < 60:
            return ("🔴", details + [f"統一R值={unified_r:.1f} < 60，高風險"])
        elif unified_r < 85:
            return ("🟡", details + [f"統一R值={unified_r:.1f}，需要監控"])
        else:
            return ("🟢", details + [f"統一R值={unified_r:.1f}，通過"])
    
    # ── 獲取統計 ──
    def get_stats(self) -> Dict:
        """引擎統計摘要"""
        leak_nodes = 0
        for tree in self.propagation_trees.values():
            leak_nodes += len(tree.find_leak_nodes())

        return {
            "total_analyses": len([l for l in self.analysis_log if l.get("type") != "propagation"]),
            "propagation_events": len([l for l in self.analysis_log if l.get("type") == "propagation"]),
            "propagation_trees": len(self.propagation_trees),
            "active_author_profiles": len(self.seven_factor_engine.author_profiles),
            "total_extractions": len(self.seven_factor_engine.extraction_log),
            "leak_nodes": leak_nodes,
            "leak_events": sum(
                1 for log in self.analysis_log
                if log.get("type") == "propagation" and log.get("leak") is True
            ),
            "sovereignty": SOVEREIGN_ANCHOR,
        }
    
    # ── 一鍵JSON導出 ──
    def export_tree(self, content_hash: str) -> Optional[Dict]:
        """導出完整傳播樹（JSON格式）"""
        tree = self.propagation_trees.get(content_hash)
        return tree.to_dict() if tree else None


# ═══════════════════════════════════════════════════════════════
# §6. 數學工具函數（獨立可複用）
# ═══════════════════════════════════════════════════════════════

def responsibility_collapse_model(f1_absence: float, f2_sharpness: float,
                                  f6_weight: float, boundary_penalty: float = 1.0,
                                  domain_risk: float = 1.0) -> Dict:
    """
    責任塌縮概率模型（行為邊界版）
    
    公式:
      R = (F2 × F6 - F1) × B × D
      
      其中:
        F1 = 缺席率 [0,1] — 逃避責任傾向
        F2 = 銳度 [0,10] — 直面問題膽量
        F6 = 長期權重 [0,10] — 歷史信用積累
        B = 邊界合規係數 [0.2, 1.0]
        D = 域風險係數 [0.1, 1.0]
    
    Returns:
      {risk_value, risk_level, interpretation}
    """
    R = (f2_sharpness * f6_weight - f1_absence) * boundary_penalty * domain_risk
    
    if R >= 85:
        level = "🟢 低風險（發光）"
        interpret = "行為端莊·邊界清晰·系統信任"
    elif R >= 60:
        level = "🟡 中風險（正常）"
        interpret = "需要監控·建議定期審計"
    else:
        level = "🔴 高風險（抖動+龍盾干預）"
        interpret = "行為邊界模糊·責任塌縮風險·立即升級"
    
    return {
        "risk_value": round(R, 2),
        "risk_level": level,
        "interpretation": interpret,
        "f1_absence": f1_absence,
        "f2_sharpness": f2_sharpness,
        "f6_weight": f6_weight,
        "boundary_penalty": boundary_penalty,
        "domain_risk": domain_risk,
    }


def propagation_time_decay(timestamp: str, half_life_days: float = 7.0) -> float:
    """
    傳播鏈時間衰減函數
    
    公式: w(t) = 2^(-Δt / t½)
    
    Args:
        timestamp: ISO時間戳
        half_life_days: 半衰期（天），默認7天
    
    Returns:
        衰減權重 0-1
    """
    try:
        t = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        delta = (datetime.now(timezone.utc) - t).total_seconds() / 86400.0
    except Exception:
        delta = 0
    return round(2 ** (-delta / half_life_days), 6)


def unified_trust_score(seven_factor_composite: float, boundary_compliant: bool,
                        propagation_risk: float) -> Dict:
    """
    統一信任分數
    
    公式:
      T = C_seven × (1 - α·P_leak)
      
      其中:
        C_seven = 七因子綜合得分 [0,1]
        P_leak = 傳播風險 [0,1] (僅在邊界不合規時計入)
        α = 泄露懲罰係數，默認 0.8
    """
    alpha = 0.8
    if not boundary_compliant:
        trust = seven_factor_composite * (1 - alpha * propagation_risk)
    else:
        trust = seven_factor_composite
    
    trust = max(0.0, min(1.0, trust))
    
    if trust >= 0.85:
        level = "🟢 高度信任"
    elif trust >= 0.60:
        level = "🟡 中度信任·持續監控"
    else:
        level = "🔴 低信任·限制傳播"
    
    return {
        "trust_score": round(trust, 4),
        "trust_level": level,
        "composite": seven_factor_composite,
        "propagation_risk": propagation_risk,
        "penalty_applied": not boundary_compliant,
    }


# ═══════════════════════════════════════════════════════════════
# §7. 命令行 & 測試入口
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import sys
    
    engine = UnifiedBoundaryEngine()
    
    # 測試三種域的內容
    texts = {
        Domain.PRIVATE: """
親愛的，今天晚上的夕陽好美，我想你了。
這是我們的小秘密，只有你我知道。
""",
        Domain.COMMUNITY: """
🐉 龍魂開發者社區週報 #42
本週進展：行為密碼學引擎升級到v3.0，新增三域邊界協議。
社區成員請在下方討論技術細節。
""",
        Domain.PUBLIC: """
DNA: #龍芯⚡️丙午·丙申·癸丑·午时·䷑蛊-UNIFIED-ENGINE-V3.0-UID9622
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

龍魂·行為密碼學統一引擎 v3.0 正式發佈。
七因子框架 + 行為邊界協議 = 完整內容來源追溯體系。
私域豁免·公域溯源·亂發必追。
""",
    }
    
    print("=" * 70)
    print("🐉 龍魂·行為密碼學統一引擎 v3.0 測試")
    print("=" * 70)
    
    for domain, text in texts.items():
        print(f"\n{'─'*70}")
        print(f"📍 域: {domain.value} | 授權: {engine.generate_auth_level(domain, 'UID9622').value}")
        print(f"{'─'*70}")
        
        result = engine.analyze(text, domain=domain)
        
        print(f"  DNA:      {result.dna_with_auth}")
        print(f"  統一R值:   {result.unified_r:.1f}")
        print(f"  邊界合規:  {'✅' if result.boundary_compliant else '❌'}")
        print(f"  傳播風險:  {result.propagation_risk:.4f}")
        print(f"  審計:      {result.audit_mark}")
        print(f"  七因子得分: {result.fingerprint.composite_score:.4f}")
        
        for f in result.fingerprint.factors:
            bar = "█" * int(f.raw_value * 15) + "░" * (15 - int(f.raw_value * 15))
            print(f"    {f.status} {f.factor_name:8s} [{bar}] {f.raw_value:.3f}")
    
    # 模擬跨域傳播
    print(f"\n{'='*70}")
    print("🔄 跨域傳播模擬")
    print(f"{'='*70}")
    
    public_text = texts[Domain.PUBLIC]
    content_hash = hashlib.sha3_256(public_text.encode()).hexdigest()
    
    # 創建原始傳播樹（A2公域發布）
    engine.create_propagation_tree(content_hash, "UID9622", Domain.PUBLIC, AuthLevel.A2)
    
    # 模擬A0私域內容被截屏泄露到公域
    private_hash = hashlib.sha3_256(texts[Domain.PRIVATE].encode()).hexdigest()
    engine.create_propagation_tree(private_hash, "UID9622", Domain.PRIVATE, AuthLevel.A0)
    
    leak_result = engine.record_propagation(
        private_hash, "LEAKER_001", Domain.PUBLIC, PropagationEvent.SCREENSHOT
    )
    print(f"\n  泄露事件: {json.dumps(leak_result, ensure_ascii=False, indent=2)}")
    
    # 責任歸屬
    resp = engine.attribute_responsibility(private_hash)
    if resp:
        print(f"\n  🎯 責任歸屬:")
        for r in resp:
            print(f"     傳播者: {r['propagator_id']} | 責任分: {r['responsibility_score']} | 域: {r['domain_to']} | {r['days_ago']}天前")
    
    # 統計
    stats = engine.get_stats()
    print(f"\n{'='*70}")
    print("📊 引擎統計")
    print(f"{'='*70}")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    
    # --json 輸出
    if "--json" in sys.argv:
        result = engine.analyze(texts[Domain.PUBLIC], domain=Domain.PUBLIC)
        print("\n" + json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
