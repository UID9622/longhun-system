归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 消息组件 · 带DNA追溯与三色审计
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v1.0

import { useState } from 'react';
import { Shield, Lock, Copy, Check } from 'lucide-react';
import type { Message as MessageType } from '@/types';
import { AUDIT_CONFIG } from '@/types';
import { encryptSimulate } from '@/utils/dna';

interface Props {
  message: MessageType;
  isSelf: boolean;
  showEncrypted?: boolean;
}

export default function Message({ message, isSelf, showEncrypted = false }: Props) {
  const [showDNA, setShowDNA] = useState(false);
  const [copied, setCopied] = useState(false);
  const auditConfig = AUDIT_CONFIG[message.audit];

  const displayContent = message.encrypted && showEncrypted
    ? encryptSimulate(message.content)
    : message.content;

  const copyDNA = () => {
    navigator.clipboard?.writeText(message.dna).catch(() => {});
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className={`flex ${isSelf ? 'justify-end' : 'justify-start'} mb-4 group`}>
      <div className={`max-w-[80%] ${isSelf ? 'order-1' : 'order-1'}`}>
        {/* 发送者信息 */}
        <div className={`flex items-center gap-2 mb-1 ${isSelf ? 'justify-end' : 'justify-start'}`}>
          <span className="text-xs text-amber-500/80 font-mono">{message.sender.name}</span>
          <span className={`text-[10px] px-1.5 py-0.5 rounded border ${auditConfig.className}`}>
            {message.audit}
          </span>
          {message.encrypted && (
            <Lock className="w-3 h-3 text-emerald-500" />
          )}
        </div>

        {/* 消息气泡 */}
        <div
          className={`relative px-4 py-3 rounded-lg border backdrop-blur-sm cursor-pointer transition-all duration-200 ${
            isSelf
              ? 'bg-amber-500/10 border-amber-500/20 text-amber-100 ml-8'
              : 'bg-zinc-800/80 border-zinc-700/50 text-zinc-200 mr-8'
          } hover:border-amber-500/40`}
          onClick={() => setShowDNA(!showDNA)}
        >
          <p className="text-sm whitespace-pre-wrap leading-relaxed">{displayContent}</p>

          {/* DNA追溯条 */}
          {showDNA && (
            <div className="mt-3 pt-2 border-t border-dashed border-zinc-600/50">
              <div className="flex items-center justify-between gap-2">
                <code className="text-[10px] text-amber-500/90 font-mono truncate">
                  {message.dna}
                </code>
                <button
                  onClick={(e) => { e.stopPropagation(); copyDNA(); }}
                  className="p-1 rounded hover:bg-zinc-700/50 transition-colors shrink-0"
                >
                  {copied ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3 text-zinc-500" />}
                </button>
              </div>
              <div className="flex items-center gap-2 mt-1">
                <code className="text-[10px] text-zinc-600 font-mono">HASH: {message.hash}</code>
                <Shield className="w-3 h-3 text-emerald-600" />
              </div>
            </div>
          )}
        </div>

        {/* 时间戳 */}
        <div className={`flex items-center gap-1 mt-1 ${isSelf ? 'justify-end' : 'justify-start'}`}>
          <span className="text-[10px] text-zinc-600 font-mono">{message.timestamp}</span>
          {message.encrypted && !showEncrypted && (
            <span className="text-[10px] text-emerald-600/70 font-mono">已加密</span>
          )}
        </div>
      </div>
    </div>
  );
}
