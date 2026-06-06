/**
 * 龍魂五行計算器 · 視覺化系統
 *
 * 🐉 DNA: #龍芯⚡️2026-06-07-WUXING-VISUAL-v3.5
 * 責任: UID9622 · 不免責
 */

import React, { useState, useMemo, useCallback } from 'react';
import { Canvas } from '@react-three/fiber';
import * as THREE from 'three';

// ============================================================================
// [接口定義]
// ============================================================================

interface River {
  id: string;
  name: string;
  wuxing: 'metal' | 'wood' | 'water' | 'fire' | 'earth';
  color: string;
  description: string;
}

interface Node {
  id: string;
  label: string;
  riverId: string;
  layer: number;
  children: Node[];
  dnaStatus: 'verified' | 'pending' | 'rejected';
}

interface WuxingData {
  center: {
    id: string;
    label: string;
  };
  rivers: River[];
  nodes: Node[];
  archiveNodes: Node[];
}

// ============================================================================
// [Layer 0: 北辰不動點 · 中心節點]
// ============================================================================

const Layer0: React.FC<{ center: WuxingData['center'] }> = ({ center }) => {
  return (
    <div className="layer-0 absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
      <div className="center-node relative w-24 h-24 rounded-full bg-gradient-to-br from-cyan-500 to-blue-600 flex items-center justify-center shadow-2xl">
        <div className="absolute inset-1 rounded-full border-2 border-cyan-300 opacity-50"></div>
        <span className="text-white font-bold text-center text-sm">{center.label}</span>
        <div className="absolute inset-0 rounded-full animate-pulse" style={{ boxShadow: '0 0 30px rgba(0, 188, 255, 0.5)' }}></div>
      </div>
    </div>
  );
};

// ============================================================================
// [Layer 1: 五行河道 · 主流向]
// ============================================================================

const Layer1: React.FC<{
  rivers: River[];
  activeRiver: string | null;
  onSelect: (riverId: string) => void;
}> = ({ rivers, activeRiver, onSelect }) => {
  const riverPositions = [
    { angle: 0, name: '東方' },
    { angle: 72, name: '東南' },
    { angle: 144, name: '西南' },
    { angle: 216, name: '西北' },
    { angle: 288, name: '東北' },
  ];

  return (
    <div className="layer-1 absolute inset-0">
      {rivers.map((river, idx) => {
        const pos = riverPositions[idx];
        const rad = (pos.angle * Math.PI) / 180;
        const x = 200 * Math.cos(rad);
        const y = 200 * Math.sin(rad);

        return (
          <button
            key={river.id}
            onClick={() => onSelect(river.id)}
            className={`absolute w-20 h-20 rounded-full transition-all duration-300 transform ${
              activeRiver === river.id ? 'scale-125 shadow-2xl' : 'hover:scale-110'
            }`}
            style={{
              background: `linear-gradient(135deg, ${river.color}, ${river.color}dd)`,
              left: `calc(50% + ${x}px)`,
              top: `calc(50% + ${y}px)`,
              transform: `translate(-50%, -50%) ${activeRiver === river.id ? 'scale(1.25)' : ''}`,
            }}
            title={river.name}
          >
            <span className="text-white font-bold text-xs text-center block">{river.name}</span>
          </button>
        );
      })}
    </div>
  );
};

// ============================================================================
// [Layer 2-4: 支流展開 + 水流流向 + DNA 門]
// ============================================================================

const Layer234: React.FC<{
  activeRiver: string | null;
  nodes: Node[];
  expandedNodes: Set<string>;
  onToggle: (nodeId: string) => void;
}> = ({ activeRiver, nodes, expandedNodes, onToggle }) => {
  const filteredNodes = nodes.filter((n) => n.riverId === activeRiver);

  return (
    <div className="layer-234 relative w-full h-full">
      {filteredNodes.map((node) => (
        <div key={node.id} className="node-group">
          {/* 節點圓圈 */}
          <div
            className="absolute w-16 h-16 rounded-full cursor-pointer transition-all duration-200 flex items-center justify-center"
            onClick={() => onToggle(node.id)}
            style={{
              background:
                node.dnaStatus === 'verified'
                  ? 'linear-gradient(135deg, #4ade80, #22c55e)'
                  : node.dnaStatus === 'pending'
                    ? 'linear-gradient(135deg, #f59e0b, #fbbf24)'
                    : 'linear-gradient(135deg, #ef4444, #dc2626)',
              left: `${50 + node.layer * 40}%`,
              top: `${Math.random() * 60 + 20}%`,
              boxShadow:
                node.dnaStatus === 'verified'
                  ? '0 0 20px rgba(74, 222, 128, 0.5)'
                  : '0 0 15px rgba(0, 0, 0, 0.3)',
            }}
          >
            <span className="text-white font-semibold text-center text-xs">{node.label}</span>
          </div>

          {/* 展開指示器 */}
          {node.children.length > 0 && expandedNodes.has(node.id) && (
            <div className="text-xs text-gray-400 absolute ml-20">
              ↳ {node.children.length} children
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

// ============================================================================
// [Layer 5-6: 外圈歸檔 + DNA 審計門]
// ============================================================================

const Layer56: React.FC<{ archiveNodes: Node[] }> = ({ archiveNodes }) => {
  return (
    <div className="layer-56 absolute bottom-10 left-10 right-10">
      <div className="flex gap-4">
        {/* DNA 審計門 */}
        <div className="audit-gate flex-1 p-4 rounded-lg border-2 border-cyan-400 bg-gradient-to-br from-cyan-500/10 to-blue-500/10">
          <h4 className="text-cyan-300 font-semibold text-sm mb-2">🔐 DNA 審計門</h4>
          <p className="text-gray-300 text-xs">
            已驗證: <span className="text-green-400">{archiveNodes.length}</span>
          </p>
        </div>

        {/* 待審外圈 */}
        <div className="archive-ring flex-1 p-4 rounded-lg border-2 border-yellow-400 bg-gradient-to-br from-yellow-500/10 to-orange-500/10">
          <h4 className="text-yellow-300 font-semibold text-sm mb-2">📦 待審外圈</h4>
          <p className="text-gray-300 text-xs">等待復核中...</p>
        </div>

        {/* 熔斷隔離 */}
        <div className="fusion-break flex-1 p-4 rounded-lg border-2 border-red-400 bg-gradient-to-br from-red-500/10 to-pink-500/10">
          <h4 className="text-red-300 font-semibold text-sm mb-2">🔴 熔斷隔離</h4>
          <p className="text-gray-300 text-xs">安全風險隔離</p>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// [三色審計面板]
// ============================================================================

const AuditPanel: React.FC<{ activeRiver: string | null }> = ({ activeRiver }) => {
  const auditStatus = activeRiver ? 'verified' : 'pending';

  return (
    <div className="audit-panel absolute top-10 right-10 w-80 p-4 rounded-lg border border-gray-600 bg-gradient-to-br from-gray-900 to-gray-800">
      <h3 className="text-lg font-bold text-white mb-4">🎯 三色審計</h3>

      <div className="space-y-2">
        <div
          className={`p-3 rounded-lg transition-all ${
            auditStatus === 'verified' ? 'bg-green-500/20 border border-green-400' : 'bg-gray-700/50'
          }`}
        >
          <span className="text-green-300 font-semibold">✅ 綠色 · 通行</span>
          <p className="text-gray-300 text-xs mt-1">系統狀態良好，可繼續執行</p>
        </div>

        <div className="p-3 rounded-lg bg-gray-700/50 border border-gray-600">
          <span className="text-yellow-300 font-semibold">🟡 黃色 · 待審</span>
          <p className="text-gray-300 text-xs mt-1">需要進一步確認</p>
        </div>

        <div className="p-3 rounded-lg bg-gray-700/50 border border-gray-600">
          <span className="text-red-300 font-semibold">🔴 紅色 · 熔斷</span>
          <p className="text-gray-300 text-xs mt-1">安全隔離，禁止通行</p>
        </div>
      </div>
    </div>
  );
};

// ============================================================================
// [主組件]
// ============================================================================

export const WuxingVisualSystem: React.FC<{ data: WuxingData }> = ({ data }) => {
  const [activeRiver, setActiveRiver] = useState<string | null>(null);
  const [expandedNodes, setExpandedNodes] = useState<Set<string>>(new Set());

  const handleRiverSelect = useCallback((riverId: string) => {
    setActiveRiver((prev) => (prev === riverId ? null : riverId));
  }, []);

  const handleNodeToggle = useCallback((nodeId: string) => {
    setExpandedNodes((prev) => {
      const next = new Set(prev);
      next.has(nodeId) ? next.delete(nodeId) : next.add(nodeId);
      return next;
    });
  }, []);

  return (
    <div className="wuxing-visual-container relative w-full h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 overflow-hidden">
      {/* 背景網格 */}
      <div
        className="absolute inset-0 opacity-10"
        style={{
          backgroundImage: 'linear-gradient(0deg, transparent 24%, rgba(0, 188, 255, .05) 25%, rgba(0, 188, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 188, 255, .05) 75%, rgba(0, 188, 255, .05) 76%, transparent 77%, transparent), linear-gradient(90deg, transparent 24%, rgba(0, 188, 255, .05) 25%, rgba(0, 188, 255, .05) 26%, transparent 27%, transparent 74%, rgba(0, 188, 255, .05) 75%, rgba(0, 188, 255, .05) 76%, transparent 77%, transparent)',
          backgroundSize: '50px 50px',
        }}
      ></div>

      {/* 層級容器 */}
      <div className="absolute inset-0">
        <Layer0 center={data.center} />
        <Layer1 rivers={data.rivers} activeRiver={activeRiver} onSelect={handleRiverSelect} />
        <Layer234
          activeRiver={activeRiver}
          nodes={data.nodes}
          expandedNodes={expandedNodes}
          onToggle={handleNodeToggle}
        />
        <Layer56 archiveNodes={data.archiveNodes} />
      </div>

      {/* 審計面板 */}
      <AuditPanel activeRiver={activeRiver} />

      {/* 頂部信息欄 */}
      <div className="absolute top-4 left-4 text-white font-mono text-sm">
        <p>🐉 龍魂五行計算器 v3.5</p>
        <p className="text-cyan-400 text-xs mt-1">
          {activeRiver ? `當前河道: ${data.rivers.find((r) => r.id === activeRiver)?.name}` : '選擇河道開始'}
        </p>
      </div>
    </div>
  );
};

export default WuxingVisualSystem;
