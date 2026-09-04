归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 聊天室主面板 · 带模型切换
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v2.0

import { useState, useRef, useEffect } from 'react';
import { Send, Lock, Unlock, Shield, Users, FileText, Cpu, ChevronLeft } from 'lucide-react';
import type { Room, Message as MessageType, User, AIModel, PageRoute } from '@/types';
import { ROOM_TYPE_CONFIG, PROVIDER_NAMES } from '@/types';
import Message from '@/components/Message';
import { createMessage } from '@/utils/data';
import { generateDNA } from '@/utils/dna';

interface Props {
  room: Room;
  currentUser: User;
  activeModel: AIModel | null;
  onSendMessage: (message: MessageType) => void;
  onNavigate: (page: PageRoute) => void;
  rooms: Room[];
  activeRoomId: string;
  onRoomSelect: (roomId: string) => void;
}

export default function ChatRoom({
  room, currentUser, activeModel, onSendMessage, onNavigate,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  rooms: _rooms,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  activeRoomId: _activeRoomId,
  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  onRoomSelect: _onRoomSelect,
}: Props) {
  const [input, setInput] = useState('');
  const [showEncrypted, setShowEncrypted] = useState(false);
  const [showSidebar, setShowSidebar] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);
  const config = ROOM_TYPE_CONFIG[room.type];

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [room.messages.length]);

  const handleSend = () => {
    if (!input.trim()) return;
    const modelId = activeModel?.id;
    const prefix = activeModel ? `[${activeModel.name}] ` : '';
    const msg = createMessage(room.id, currentUser, prefix + input.trim(), modelId);
    onSendMessage(msg);
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-zinc-950/40 relative">
      {/* 房间头部 */}
      <div className="h-14 flex items-center px-4 border-b border-zinc-800/50 bg-zinc-950/60 backdrop-blur-sm shrink-0">
        <button
          onClick={() => setShowSidebar(!showSidebar)}
          className="mr-3 p-1.5 rounded border border-zinc-700/50 text-zinc-500 hover:text-zinc-300 lg:hidden"
        >
          <ChevronLeft className="w-4 h-4" />
        </button>

        <div className="flex items-center gap-3 flex-1 min-w-0">
          <span className="text-lg">{config.icon}</span>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-2">
              <h2 className="text-sm font-bold text-zinc-200">{room.name}</h2>
              <span className={`text-[10px] px-1.5 py-0.5 rounded border ${config.color}`}>
                {config.label}
              </span>
            </div>
            <div className="flex items-center gap-2 mt-0.5">
              <code className="text-[9px] text-amber-500/60 font-mono truncate">{room.dna}</code>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 shrink-0 ml-4">
          {/* 当前模型显示 */}
          {activeModel && (
            <div className="flex items-center gap-1.5 px-2.5 py-1.5 rounded text-xs border bg-amber-500/5 border-amber-500/20 text-amber-400">
              <Cpu className="w-3 h-3" />
              <span>{activeModel.name}</span>
              <span className="text-[9px] text-amber-500/50">{PROVIDER_NAMES[activeModel.provider]}</span>
            </div>
          )}

          <button
            onClick={() => onNavigate('home')}
            className="flex items-center gap-1 px-2.5 py-1.5 rounded text-xs border border-zinc-700/50 bg-zinc-800/50 text-zinc-400 hover:text-zinc-300 transition-all"
          >
            <Cpu className="w-3 h-3" />换模型
          </button>

          <button
            onClick={() => setShowEncrypted(!showEncrypted)}
            className={`flex items-center gap-1 px-2.5 py-1.5 rounded text-xs border transition-all ${
              showEncrypted
                ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-400'
                : 'bg-zinc-800/50 border-zinc-700/50 text-zinc-400 hover:text-zinc-300'
            }`}
          >
            {showEncrypted ? <Lock className="w-3 h-3" /> : <Unlock className="w-3 h-3" />}
            {showEncrypted ? '加密视图' : '明文'}
          </button>

          <div className="flex items-center gap-1 px-2.5 py-1.5 rounded bg-zinc-800/50 border border-zinc-700/50 text-xs text-zinc-400">
            <Users className="w-3 h-3" />
            {room.members.length}
          </div>

          <div className={`flex items-center gap-1 px-2.5 py-1.5 rounded border text-xs ${
            room.auditLevel === '🟢' ? 'bg-green-500/10 border-green-500/30 text-green-400' :
            room.auditLevel === '🟡' ? 'bg-amber-500/10 border-amber-500/30 text-amber-400' :
            'bg-red-500/10 border-red-500/30 text-red-400'
          }`}>
            <Shield className="w-3 h-3" />
            {room.auditLevel}
          </div>
        </div>
      </div>

      {/* 移动端侧边栏遮罩 */}
      {showSidebar && (
        <div
          className="absolute inset-0 bg-black/50 z-40 lg:hidden"
          onClick={() => setShowSidebar(false)}
        />
      )}

      {/* 消息区域 */}
      <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-1 scrollbar-thin">
        {/* 模型提示 */}
        {activeModel && (
          <div className="flex justify-center mb-4">
            <div className="flex items-center gap-2 px-3 py-1.5 rounded-full border border-amber-500/15 bg-amber-500/5 text-[10px] text-amber-400">
              <Cpu className="w-3 h-3" />
              <span>当前使用模型: {activeModel.name} ({PROVIDER_NAMES[activeModel.provider]})</span>
            </div>
          </div>
        )}

        {room.messages.length === 0 ? (
          <div className="h-full flex flex-col items-center justify-center text-zinc-700">
            <div className="text-4xl mb-3 opacity-20">龍</div>
            <p className="text-sm">房间已创建，等待第一条消息</p>
            <code className="text-[10px] font-mono mt-1 opacity-40">{room.dna}</code>
          </div>
        ) : (
          room.messages.map(msg => (
            <Message
              key={msg.id}
              message={msg}
              isSelf={msg.sender.uid === currentUser.uid}
              showEncrypted={showEncrypted}
            />
          ))
        )}
      </div>

      {/* 输入区域 */}
      <div className="px-4 pb-4 pt-2 shrink-0">
        <div className="flex items-end gap-2 p-2 rounded-lg border border-zinc-800/50 bg-zinc-900/50 backdrop-blur-sm focus-within:border-amber-500/30 transition-colors">
          <textarea
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={activeModel
              ? `使用「${activeModel.name}」在「${room.name}」发送消息...`
              : `在「${room.name}」发送消息... (每条消息自动带DNA追溯)`
            }
            className="flex-1 bg-transparent text-sm text-zinc-200 placeholder-zinc-600 resize-none outline-none min-h-[40px] max-h-[120px] py-2 px-1 leading-relaxed"
            rows={1}
          />
          <div className="flex items-center gap-1.5 pb-1 shrink-0">
            <div className="flex items-center gap-1 text-[10px] text-zinc-600 px-1.5">
              <FileText className="w-3 h-3" />
              <span className="font-mono">{input.length}</span>
            </div>
            <button
              onClick={handleSend}
              disabled={!input.trim()}
              className={`p-2.5 rounded-md transition-all ${
                input.trim()
                  ? 'bg-amber-500/20 text-amber-400 border border-amber-500/30 hover:bg-amber-500/30 active:scale-95'
                  : 'bg-zinc-800/50 text-zinc-600 border border-zinc-700/30 cursor-not-allowed'
              }`}
            >
              <Send className="w-4 h-4" />
            </button>
          </div>
        </div>
        <div className="flex items-center justify-between mt-1.5 px-1">
          <code className="text-[9px] text-zinc-700 font-mono">
            DNA: {generateDNA('HEART-TALK', 'INPUT-ACTIVE')}
          </code>
          <div className="flex items-center gap-3">
            {activeModel && (
              <span className="text-[9px] text-amber-600/70">
                模型: {activeModel.name}
              </span>
            )}
            <span className="text-[9px] text-zinc-700">Enter发送 · Shift+Enter换行</span>
          </div>
        </div>
      </div>
    </div>
  );
}
