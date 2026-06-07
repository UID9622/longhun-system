"""
龍魂三合同步器 v1.0 · 完整測試套件

DNA: #龍芯⚡️2026-06-06-SANCAI-SYNC-TEST-SUITE-v1.0
GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
UID: 9622·諸葛鑫

測試覆蓋：
- 數據結構完整性
- 三個轉換函數
- 驗證函數
- DNA 生成
- 三環無死鎖檢查
"""

import pytest
from datetime import datetime
from ..sancai_sync_hub import (
    SancaiSyncHub,
    IPAReceipt,
    ParticleInstruction,
    NeuralSignal,
    PalaceNode
)


class TestDataStructures:
    """測試數據結構"""

    def test_ipa_receipt_creation(self):
        """測試 IPA 回執創建"""
        ipa = IPAReceipt(
            ipa_node="IPA-FLOW-GATE-PRIVACY",
            ipa_address="/flow/gate/privacy",
            main_persona="P03",
            input_node_id="FLOW-9622-20260606-ABC123",
            output_signal="pass",
            next_ipa="IPA-FLOW-GATE-DR",
            dna="#龍芯⚡️2026-06-06-IPA-GATE-PRIVACY-v1.0",
            timestamp=datetime.now().isoformat()
        )
        assert ipa.ipa_node == "IPA-FLOW-GATE-PRIVACY"
        assert ipa.output_signal == "pass"
        assert ipa.main_persona == "P03"

    def test_particle_instruction_creation(self):
        """測試粒子指令創建"""
        particle = ParticleInstruction(
            id=0,
            x=400.0,
            y=300.0,
            vx=1.0,
            vy=0.5,
            synaptic=0.7,
            plasticity=0.8,
            seed_bias=0.5,
            trail=[(400.0, 300.0)],
            life=600
        )
        assert particle.id == 0
        assert particle.x == 400.0
        assert len(particle.trail) == 1

    def test_neural_signal_creation(self):
        """測試神經信號創建"""
        signal = NeuralSignal(
            neuron_id="NEURON-001",
            activation=0.8,
            firing_rate=0.7,
            synapse_weight=0.5,
            temporal_context="ring_age_150_cycles",
            spatial_location=(400.0, 300.0)
        )
        assert signal.neuron_id == "NEURON-001"
        assert signal.activation == 0.8

    def test_palace_node_creation(self):
        """測試宮位節點創建"""
        palace = PalaceNode(
            palace_name="乾宮",
            element="金",
            persona_assigned="P00",
            contribution=8.5,
            confidence=0.9,
            dna_chain="parent:xyz|self:abc"
        )
        assert palace.palace_name == "乾宮"
        assert palace.element == "金"


class TestSancaiSyncHub:
    """測試 SancaiSyncHub 核心類"""

    @pytest.fixture
    def hub(self):
        """創建 Hub 實例"""
        return SancaiSyncHub(seed=9622)

    @pytest.fixture
    def sample_ipa(self):
        """創建樣本 IPA 回執"""
        return IPAReceipt(
            ipa_node="IPA-FLOW-GATE-PRIVACY",
            ipa_address="/flow/gate/privacy",
            main_persona="P03",
            input_node_id="FLOW-9622-20260606-ABC123",
            output_signal="pass",
            next_ipa="IPA-FLOW-GATE-DR",
            dna="#龍芯⚡️2026-06-06-IPA-GATE-PRIVACY-v1.0",
            timestamp=datetime.now().isoformat()
        )

    @pytest.fixture
    def sample_ring(self):
        """創建樣本年輪數據"""
        return {
            'age': 150,
            'radius': 120.0,
            'strength': 0.85,
            'x': 400.0,
            'y': 300.0
        }

    @pytest.fixture
    def sample_knowledge_graph(self):
        """創建樣本知識圖"""
        return {
            'nodes': [
                {'weight': 0.9, 'edges': [1, 2, 3]},
                {'weight': 0.8, 'edges': [0, 2]},
                {'weight': 0.7, 'edges': [0, 1, 3]},
            ],
            'parent_dna': '#龍芯⚡️2026-06-06-KNOWLEDGE-GRAPH-v1.0'
        }

    def test_hub_initialization(self, hub):
        """測試 Hub 初始化"""
        assert hub.seed == 9622
        assert len(hub.particle_buffer) == 0
        assert len(hub.neural_buffer) == 0
        assert len(hub.palace_buffer) == 0

    def test_ipa_to_particle_conversion(self, hub, sample_ipa):
        """測試 IPA → 粒子轉換"""
        particles = hub.ipa_to_particle(sample_ipa, particle_count=20)

        assert len(particles) == 20
        assert len(hub.particle_buffer) == 20
        assert all(isinstance(p, ParticleInstruction) for p in particles)
        assert all(p.life > 0 for p in particles)  # pass 信號應有正生命值

    def test_ipa_to_particle_fuse_signal(self, hub, sample_ipa):
        """測試 IPA → 粒子轉換（熔斷信號）"""
        sample_ipa.output_signal = "fuse"
        particles = hub.ipa_to_particle(sample_ipa, particle_count=10)

        assert all(p.life == 0 for p in particles)  # fuse 信號應導致零生命值

    def test_ring_to_neural_conversion(self, hub, sample_ring):
        """測試年輪 → 神經信號轉換"""
        signals = hub.ring_to_neural(sample_ring)

        assert len(signals) > 0
        assert len(hub.neural_buffer) == len(signals)
        assert all(isinstance(s, NeuralSignal) for s in signals)
        assert all(0 <= s.activation <= 1.0 for s in signals)

    def test_knowledge_to_palace_conversion(self, hub, sample_knowledge_graph):
        """測試知識圖 → 宮位轉換"""
        palaces = hub.knowledge_to_palace(sample_knowledge_graph)

        assert len(palaces) == 3  # 三個節點→三個宮位
        assert len(hub.palace_buffer) == 3
        assert all(isinstance(p, PalaceNode) for p in palaces)
        assert all(p.element in ["金", "木", "水", "火", "土"] for p in palaces)

    def test_palace_assignment(self, hub, sample_knowledge_graph):
        """測試宮位人格分配"""
        palaces = hub.knowledge_to_palace(sample_knowledge_graph)

        personas = [p.persona_assigned for p in palaces]
        # 驗證人格被正確分配
        assert all(p.startswith('P') for p in personas)

    def test_verify_sync_empty(self, hub):
        """測試驗證函數（空緩衝）"""
        ok, msg = hub.verify_sync()
        assert not ok
        assert "粒子緩衝為空" in msg

    def test_verify_sync_complete(self, hub, sample_ipa, sample_ring, sample_knowledge_graph):
        """測試驗證函數（完整轉換）"""
        hub.ipa_to_particle(sample_ipa, particle_count=30)
        hub.ring_to_neural(sample_ring)
        hub.knowledge_to_palace(sample_knowledge_graph)

        ok, msg = hub.verify_sync()
        assert ok
        assert "三環無死鎖" in msg

    def test_dna_generation(self, hub):
        """測試 DNA 生成"""
        dna = hub.generate_dna(parent_dna="#龍芯⚡️2026-06-06-SANCAI-SYNC-TEST-v1.0")

        assert dna.startswith("#龍芯⚡️")
        assert "THREE-INTEGRATION-SYNC" in dna
        assert hub.dna_chain['current'] == dna
        assert hub.dna_chain['parent'] == "#龍芯⚡️2026-06-06-PARENT-v1.0"

    def test_json_export(self, hub, sample_ipa, sample_ring, sample_knowledge_graph):
        """測試 JSON 導出"""
        hub.ipa_to_particle(sample_ipa, particle_count=20)
        hub.ring_to_neural(sample_ring)
        hub.knowledge_to_palace(sample_knowledge_graph)

        json_str = hub.to_json()
        assert isinstance(json_str, str)
        assert "particles" in json_str
        assert "signals" in json_str
        assert "palaces" in json_str

    def test_integration_normal_flow(self, hub, sample_ipa, sample_ring, sample_knowledge_graph):
        """集成測試：完整流程"""
        # 步驟 1：IPA 轉粒子
        particles = hub.ipa_to_particle(sample_ipa, particle_count=30)
        assert len(particles) == 30

        # 步驟 2：年輪轉神經
        signals = hub.ring_to_neural(sample_ring)
        assert len(signals) > 0

        # 步驟 3：知識圖轉宮位
        palaces = hub.knowledge_to_palace(sample_knowledge_graph)
        assert len(palaces) == 3

        # 步驟 4：驗證無死鎖
        ok, msg = hub.verify_sync()
        assert ok

        # 步驟 5：生成 DNA
        dna = hub.generate_dna(parent_dna="#龍芯⚡️2026-06-06-PARENT-v1.0")
        assert dna.startswith("#龍芯⚡️")

        # 步驟 6：JSON 導出
        json_str = hub.to_json()
        assert "particles" in json_str


class TestEdgeCases:
    """測試邊界情況"""

    def test_empty_knowledge_graph(self):
        """測試空知識圖"""
        hub = SancaiSyncHub()
        graph = {'nodes': [], 'parent_dna': ''}
        palaces = hub.knowledge_to_palace(graph)
        assert len(palaces) == 0

    def test_large_particle_count(self):
        """測試大量粒子生成"""
        hub = SancaiSyncHub()
        ipa = IPAReceipt(
            ipa_node="IPA-TEST",
            ipa_address="/test",
            main_persona="P05",
            input_node_id="TEST-001",
            output_signal="pass",
            next_ipa="IPA-NEXT",
            dna="#龍芯⚡️TEST",
            timestamp=datetime.now().isoformat()
        )
        particles = hub.ipa_to_particle(ipa, particle_count=500)
        assert len(particles) == 500

    def test_extreme_ring_values(self):
        """測試極端年輪值"""
        hub = SancaiSyncHub()
        ring = {
            'age': 10000,  # 超大年齡
            'radius': 1000.0,  # 超大半徑
            'strength': 0.01,  # 非常弱
            'x': 0.0,
            'y': 0.0
        }
        signals = hub.ring_to_neural(ring)
        assert len(signals) > 0
        assert all(s.activation >= 0.1 for s in signals)  # activation 不應低於 0.1


class TestPersonaRouting:
    """測試人格路由"""

    def test_persona_assignment_sequence(self):
        """測試人格分配順序"""
        hub = SancaiSyncHub()
        graph = {
            'nodes': [
                {'weight': 0.9, 'edges': []},
                {'weight': 0.8, 'edges': []},
                {'weight': 0.7, 'edges': []},
                {'weight': 0.6, 'edges': []},
            ],
            'parent_dna': ''
        }
        palaces = hub.knowledge_to_palace(graph)

        personas = [p.persona_assigned for p in palaces]
        expected = ["P00", "P01", "P02", "P03"]
        assert personas == expected


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
