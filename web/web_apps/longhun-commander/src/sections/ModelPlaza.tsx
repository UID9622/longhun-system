// 模型选择广场 · 首页
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v2.0

import { useState } from 'react';
import { Cpu, Download, Star, Plug, Zap, ChevronRight, Terminal, Hash } from 'lucide-react';
import type { AIModel, PageRoute } from '@/types';
import { MODEL_TYPE_CONFIG, PROVIDER_NAMES } from '@/types';
import { AI_MODELS } from '@/utils/data';

interface Props {
  onSelectModel: (model: AIModel) => void;
  onNavigate: (page: PageRoute) => void;
  selectedModelId: string | null;
}

export default function ModelPlaza({ onSelectModel, onNavigate, selectedModelId }: Props) {
  const [filter, setFilter] = useState<'all' | 'local' | 'cloud' | 'longhun'>('all');
  const [expandedModel, setExpandedModel] = useState<string | null>(null);

  const filtered = filter === 'all' ? AI_MODELS : AI_MODELS.filter(m => m.type === filter);

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* 头部横幅 */}
      <div className="p-6 border-b border-zinc-800/50 bg-gradient-to-r from-zinc-900/50 via-amber-500/5 to-zinc-900/50">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-amber-400 to-red-400 bg-clip-text text-transparent">
              模型选择广场
            </h1>
            <p className="text-sm text-zinc-500 mt-1">
              选择您的AI对话模型 · 本地优先 · 主权可控 · 开放接入
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate('plaza')}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-zinc-700/50 bg-zinc-800/50 text-xs text-zinc-300 hover:border-amber-500/30 hover:bg-amber-500/5 transition-all"
            >
              <Hash className="w-3.5 h-3.5" />开源广场
            </button>
            <button
              onClick={() => onNavigate('developer')}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-zinc-700/50 bg-zinc-800/50 text-xs text-zinc-300 hover:border-amber-500/30 hover:bg-amber-500/5 transition-all"
            >
              <Plug className="w-3.5 h-3.5" />开发者接入
            </button>
            <button
              onClick={() => onNavigate('chat')}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-amber-500/30 bg-amber-500/10 text-xs text-amber-400 hover:bg-amber-500/20 transition-all"
            >
              <Terminal className="w-3.5 h-3.5" />进入对话
              <ChevronRight className="w-3 h-3" />
            </button>
          </div>
        </div>

        {/* 统计条 */}
        <div className="flex items-center gap-6 mt-4">
          {(['all', 'local', 'cloud', 'longhun'] as const).map(type => {
            const allConfig = { label: '全部', icon: '🔥', color: 'text-amber-400 border-amber-400/30 bg-amber-400/5' };
            const config = type === 'all' ? allConfig : MODEL_TYPE_CONFIG[type];
            const count = type === 'all' ? AI_MODELS.length : AI_MODELS.filter(m => m.type === type).length;
            return (
              <button
                key={type}
                onClick={() => setFilter(type)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-md border text-xs transition-all ${
                  filter === type
                    ? `${config.color} border-current`
                    : 'border-zinc-800 text-zinc-500 hover:border-zinc-700 hover:text-zinc-400'
                }`}
              >
                <span>{config.icon}</span>
                <span>{config.label}</span>
                <span className="font-mono text-[10px] opacity-60">({count})</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* 模型卡片网格 */}
      <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
          {filtered.map(model => {
            const config = MODEL_TYPE_CONFIG[model.type];
            const isSelected = model.id === selectedModelId;
            const isExpanded = expandedModel === model.id;
            return (
              <div
                key={model.id}
                className={`rounded-lg border transition-all ${
                  isSelected
                    ? 'border-amber-500/50 bg-amber-500/5 shadow-lg shadow-amber-500/5'
                    : 'border-zinc-800/50 bg-zinc-900/30 hover:border-zinc-700/50 hover:bg-zinc-800/20'
                }`}
              >
                <div className="p-4">
                  {/* 头部 */}
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      <span className="text-lg">{config.icon}</span>
                      <div>
                        <h3 className="text-sm font-bold text-zinc-200">{model.name}</h3>
                        <p className="text-[10px] text-zinc-600">{PROVIDER_NAMES[model.provider]}</p>
                      </div>
                    </div>
                    <div className="flex items-center gap-1">
                      {model.status === 'online' && <span className="w-2 h-2 rounded-full bg-green-500" />}
                      {model.status === 'beta' && <span className="w-2 h-2 rounded-full bg-amber-500" />}
                      {model.status === 'offline' && <span className="w-2 h-2 rounded-full bg-red-500" />}
                      <span className={`text-[10px] ${model.status === 'online' ? 'text-green-400' : model.status === 'beta' ? 'text-amber-400' : 'text-red-400'}`}>
                        {model.status === 'online' ? '在线' : model.status === 'beta' ? '测试' : '离线'}
                      </span>
                    </div>
                  </div>

                  {/* 描述 */}
                  <p className="text-xs text-zinc-400 mt-2 leading-relaxed line-clamp-2">{model.description}</p>

                  {/* 标签 */}
                  <div className="flex flex-wrap gap-1 mt-2">
                    {model.tags.map(tag => (
                      <span key={tag} className="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-500 border border-zinc-700/30">
                        {tag}
                      </span>
                    ))}
                  </div>

                  {/* 参数行 */}
                  <div className="flex items-center gap-3 mt-3 text-[10px] text-zinc-600">
                    <span className="flex items-center gap-1"><Cpu className="w-3 h-3" />{model.parameters}</span>
                    <span className="flex items-center gap-1"><Download className="w-3 h-3" />{model.downloads.toLocaleString()}</span>
                    <span className="flex items-center gap-1"><Star className="w-3 h-3 text-amber-500/50" />{model.rating}</span>
                    {model.mcpSupport && <span className="flex items-center gap-1 text-emerald-500"><Plug className="w-3 h-3" />MCP</span>}
                  </div>

                  {/* DNA */}
                  <code className="text-[9px] text-amber-500/40 font-mono block mt-2 truncate">{model.dna}</code>
                </div>

                {/* 操作区 */}
                <div className="px-4 pb-3 flex items-center gap-2">
                  <button
                    onClick={() => onSelectModel(model)}
                    className={`flex-1 py-1.5 rounded text-xs font-medium transition-all ${
                      isSelected
                        ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                        : 'bg-zinc-800/50 text-zinc-300 border border-zinc-700/30 hover:bg-zinc-700/50'
                    }`}
                  >
                    {isSelected ? '✓ 已选择' : '选择模型'}
                  </button>
                  <button
                    onClick={() => setExpandedModel(isExpanded ? null : model.id)}
                    className="px-3 py-1.5 rounded text-xs text-zinc-500 border border-zinc-700/30 hover:text-zinc-300 transition-all"
                  >
                    {isExpanded ? '收起' : '详情'}
                  </button>
                </div>

                {/* 展开详情 */}
                {isExpanded && (
                  <div className="px-4 pb-3 border-t border-zinc-800/30 pt-2 space-y-2">
                    {model.localInstall && (
                      <div className="flex items-center gap-2">
                        <Terminal className="w-3 h-3 text-emerald-500 shrink-0" />
                        <code className="text-[10px] text-emerald-400/80 font-mono bg-zinc-900/50 px-1.5 py-0.5 rounded">{model.localInstall}</code>
                      </div>
                    )}
                    {model.apiEndpoint && (
                      <div className="flex items-center gap-2">
                        <Zap className="w-3 h-3 text-sky-500 shrink-0" />
                        <code className="text-[10px] text-sky-400/80 font-mono bg-zinc-900/50 px-1.5 py-0.5 rounded">{model.apiEndpoint}</code>
                      </div>
                    )}
                    {model.requirements && (
                      <p className="text-[10px] text-zinc-600">要求: {model.requirements}</p>
                    )}
                    <p className="text-[10px] text-zinc-600">协议: {model.license}</p>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
