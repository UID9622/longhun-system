// 侧边栏 · 身份面板 + 房间列表 + GitHub仓库
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v1.0

import { Shield, CreditCard, Award, Github, ExternalLink, UserCheck, Zap, Key } from 'lucide-react';
import type { Room } from '@/types';
import RoomCard from '@/components/RoomCard';
import { GITHUB_REPOS } from '@/utils/data';

interface Props {
  rooms: Room[];
  activeRoomId: string;
  onRoomSelect: (roomId: string) => void;
  uid: string;
  creditScore: number;
  contributionScore: number;
  gpgFingerprint: string;
}

export default function Sidebar({
  rooms, activeRoomId, onRoomSelect,
  uid, creditScore, contributionScore, gpgFingerprint,
}: Props) {
  return (
    <div className="w-80 h-full flex flex-col border-r border-zinc-800/50 bg-zinc-950/80 backdrop-blur-xl">
      {/* 身份面板 */}
      <div className="p-4 border-b border-zinc-800/50">
        <div className="flex items-center gap-3">
          <div className="relative">
            <div className="w-12 h-12 rounded-lg bg-gradient-to-br from-amber-500/20 to-red-500/20 border border-amber-500/30 flex items-center justify-center">
              <span className="text-xl">龍</span>
            </div>
            <div className="absolute -bottom-0.5 -right-0.5 w-3.5 h-3.5 rounded-full bg-green-500 border-2 border-zinc-950" />
          </div>
          <div className="flex-1 min-w-0">
            <div className="flex items-center gap-1.5">
              <h2 className="text-sm font-bold text-amber-400">龍芯北辰</h2>
              <UserCheck className="w-3 h-3 text-emerald-500" />
            </div>
            <p className="text-[10px] text-zinc-500 font-mono truncate">{uid}</p>
            <div className="flex items-center gap-2 mt-1">
              <span className="flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                <Shield className="w-2.5 h-2.5" />已认证
              </span>
              <span className="flex items-center gap-1 text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 border border-zinc-700/50">
                <Key className="w-2.5 h-2.5" />GPG
              </span>
            </div>
          </div>
        </div>

        {/* 积分面板 */}
        <div className="grid grid-cols-2 gap-2 mt-3">
          <div className="p-2 rounded border border-zinc-800/50 bg-zinc-900/30">
            <div className="flex items-center gap-1 text-[10px] text-zinc-500">
              <CreditCard className="w-3 h-3" />信用积分
            </div>
            <p className="text-lg font-bold text-amber-400 font-mono mt-0.5">{creditScore.toLocaleString()}</p>
          </div>
          <div className="p-2 rounded border border-zinc-800/50 bg-zinc-900/30">
            <div className="flex items-center gap-1 text-[10px] text-zinc-500">
              <Award className="w-3 h-3" />贡献分
            </div>
            <p className="text-lg font-bold text-emerald-400 font-mono mt-0.5">{contributionScore.toLocaleString()}</p>
          </div>
        </div>

        {/* GPG指纹 */}
        <div className="mt-2 p-1.5 rounded bg-zinc-900/50 border border-zinc-800/30">
          <p className="text-[9px] text-zinc-600 font-mono truncate" title={gpgFingerprint}>
            {gpgFingerprint}
          </p>
        </div>
      </div>

      {/* 房间列表 */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2 scrollbar-thin">
        <div className="flex items-center justify-between mb-1">
          <h3 className="text-xs text-zinc-500 font-medium uppercase tracking-wider">房间列表</h3>
          <span className="text-[10px] text-zinc-700 font-mono">{rooms.length}个房间</span>
        </div>
        {rooms.map(room => (
          <RoomCard
            key={room.id}
            room={room}
            isActive={room.id === activeRoomId}
            onClick={() => onRoomSelect(room.id)}
          />
        ))}
      </div>

      {/* GitHub仓库 */}
      <div className="p-3 border-t border-zinc-800/50 max-h-[220px] overflow-y-auto">
        <div className="flex items-center gap-1.5 mb-2">
          <Github className="w-3.5 h-3.5 text-zinc-500" />
          <h3 className="text-xs text-zinc-500 font-medium">公开仓库</h3>
          <span className="text-[10px] text-zinc-700 font-mono ml-auto">{GITHUB_REPOS.length}</span>
        </div>
        <div className="space-y-1.5">
          {GITHUB_REPOS.map(repo => (
            <a
              key={repo.name}
              href={repo.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 p-2 rounded border border-zinc-800/30 bg-zinc-900/20 hover:border-zinc-700/50 hover:bg-zinc-800/30 transition-all group"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-1">
                  <span className="text-[11px] text-amber-400/80 font-mono truncate">{repo.name}</span>
                  <ExternalLink className="w-2.5 h-2.5 text-zinc-700 opacity-0 group-hover:opacity-100 transition-opacity shrink-0" />
                </div>
                <p className="text-[9px] text-zinc-600 truncate">{repo.language}</p>
              </div>
              <div className="flex items-center gap-0.5 text-[10px] text-zinc-600 shrink-0">
                <Zap className="w-3 h-3" />
                {repo.stars}
              </div>
            </a>
          ))}
        </div>
      </div>
    </div>
  );
}
