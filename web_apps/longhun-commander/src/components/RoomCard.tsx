// 房间卡片组件
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v1.0

import { Lock, Users, MessageSquare, Shield } from 'lucide-react';
import type { Room } from '@/types';
import { ROOM_TYPE_CONFIG } from '@/types';

interface Props {
  room: Room;
  isActive: boolean;
  onClick: () => void;
}

export default function RoomCard({ room, isActive, onClick }: Props) {
  const config = ROOM_TYPE_CONFIG[room.type];

  return (
    <button
      onClick={onClick}
      className={`w-full text-left p-3 rounded-lg border transition-all duration-200 group ${
        isActive
          ? 'bg-amber-500/10 border-amber-500/40 shadow-lg shadow-amber-500/5'
          : 'bg-zinc-900/50 border-zinc-800/50 hover:bg-zinc-800/50 hover:border-zinc-700/50'
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2 flex-1 min-w-0">
          <span className="text-lg">{config.icon}</span>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-1.5">
              <h3 className={`text-sm font-medium truncate ${isActive ? 'text-amber-400' : 'text-zinc-300'}`}>
                {room.name}
              </h3>
              {room.encrypted && <Lock className="w-3 h-3 text-emerald-500 shrink-0" />}
            </div>
            <p className="text-[10px] text-zinc-600 font-mono truncate mt-0.5">{room.dna}</p>
          </div>
        </div>
        {room.unreadCount > 0 && (
          <span className="shrink-0 ml-2 w-5 h-5 flex items-center justify-center rounded-full bg-red-500/20 text-red-400 text-[10px] font-bold border border-red-500/30">
            {room.unreadCount}
          </span>
        )}
      </div>

      <div className="flex items-center gap-3 mt-2 text-[10px] text-zinc-600">
        <span className={`px-1.5 py-0.5 rounded border ${config.color}`}>
          {config.label}
        </span>
        <span className="flex items-center gap-1">
          <Users className="w-3 h-3" />
          {room.members.length}
        </span>
        <span className="flex items-center gap-1">
          <MessageSquare className="w-3 h-3" />
          {room.messages.length}
        </span>
        <span className="flex items-center gap-1 ml-auto">
          <Shield className={`w-3 h-3 ${room.auditLevel === '🟢' ? 'text-green-500' : room.auditLevel === '🟡' ? 'text-amber-500' : 'text-red-500'}`} />
        </span>
      </div>
    </button>
  );
}
