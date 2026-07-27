// 三色审计日志组件
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v1.0

import { Activity, AlertTriangle, XCircle } from 'lucide-react';
import type { AuditEntry } from '@/types';
import { AUDIT_CONFIG } from '@/types';

interface Props {
  entries: AuditEntry[];
}

const ICONS = {
  '🟢': Activity,
  '🟡': AlertTriangle,
  '🔴': XCircle,
};

export default function AuditLog({ entries }: Props) {
  const green = entries.filter(e => e.level === '🟢').length;
  const yellow = entries.filter(e => e.level === '🟡').length;
  const red = entries.filter(e => e.level === '🔴').length;
  const health = entries.length > 0 ? Math.round((green / entries.length) * 100) : 100;

  return (
    <div className="space-y-3">
      {/* 健康度仪表盘 */}
      <div className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/50">
        <div className="flex items-center justify-between mb-2">
          <span className="text-xs text-zinc-400">系统健康度</span>
          <span className={`text-sm font-bold font-mono ${health >= 80 ? 'text-green-400' : health >= 50 ? 'text-amber-400' : 'text-red-400'}`}>
            {health}%
          </span>
        </div>
        <div className="flex gap-1">
          <div className="h-1.5 flex-1 rounded-full bg-green-500/30 overflow-hidden">
            <div className="h-full bg-green-500 rounded-full transition-all" style={{ width: `${(green / entries.length) * 100}%` }} />
          </div>
          <div className="h-1.5 flex-1 rounded-full bg-amber-500/30 overflow-hidden">
            <div className="h-full bg-amber-500 rounded-full transition-all" style={{ width: `${(yellow / entries.length) * 100}%` }} />
          </div>
          <div className="h-1.5 flex-1 rounded-full bg-red-500/30 overflow-hidden">
            <div className="h-full bg-red-500 rounded-full transition-all" style={{ width: `${(red / entries.length) * 100}%` }} />
          </div>
        </div>
        <div className="flex justify-between mt-1.5 text-[10px] text-zinc-600">
          <span className="text-green-500/70">🟢 {green}</span>
          <span className="text-amber-500/70">🟡 {yellow}</span>
          <span className="text-red-500/70">🔴 {red}</span>
        </div>
      </div>

      {/* 审计条目列表 */}
      <div className="space-y-1.5 max-h-[280px] overflow-y-auto pr-1 scrollbar-thin">
        {entries.map(entry => {
          const config = AUDIT_CONFIG[entry.level];
          const Icon = ICONS[entry.level];
          return (
            <div
              key={entry.id}
              className={`p-2 rounded border text-xs transition-all ${config.className}`}
            >
              <div className="flex items-center gap-1.5">
                <Icon className="w-3 h-3 shrink-0" />
                <span className="font-medium truncate">{entry.module}</span>
                <span className="text-[10px] opacity-60 ml-auto font-mono shrink-0">{entry.timestamp.slice(11)}</span>
              </div>
              <p className="mt-1 text-[11px] opacity-80 truncate">{entry.message}</p>
              <code className="text-[9px] opacity-50 font-mono truncate block">{entry.dna}</code>
            </div>
          );
        })}
      </div>
    </div>
  );
}
