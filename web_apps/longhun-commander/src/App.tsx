// 龍之心语 v2.0 · 龍魂社交最小可运行版本
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v2.0
// 归属：中华人民共和国 · 龍魂系统 · UID9622

import { useState, useCallback } from 'react';
import {
  Shield, Terminal, Cpu, Home, GitFork, Code, Key, MessageSquare,
  Sparkles, Server, Lock, Zap, Siren, BookOpen, Users
} from 'lucide-react';
import type { Message, Room, AuditEntry, AIModel, PageRoute } from '@/types';
import { CURRENT_USER, INITIAL_ROOMS, INITIAL_AUDITS } from '@/utils/data';
import { generateDNA } from '@/utils/dna';
import Sidebar from '@/sections/Sidebar';
import ChatRoom from '@/sections/ChatRoom';
import RightPanel from '@/sections/RightPanel';
import ModelPlaza from '@/sections/ModelPlaza';
import OpenPlaza from '@/sections/OpenPlaza';
import DeveloperCenter from '@/sections/DeveloperCenter';
import AuthManager from '@/sections/AuthManager';
import CommandCenter from '@/sections/CommandCenter';
import PublicDocuments from '@/sections/PublicDocuments';
import Dashboard from '@/sections/Dashboard';

const NAV_ITEMS: { key: PageRoute; label: string; icon: typeof Home }[] = [
  { key: 'home', label: '模型广场', icon: Sparkles },
  { key: 'commander', label: '指挥调度', icon: Siren },
  { key: 'docs', label: '公开文档', icon: BookOpen },
  { key: 'plaza', label: '开源广场', icon: GitFork },
  { key: 'chat', label: '对话空间', icon: MessageSquare },
  { key: 'developer', label: '开发者', icon: Code },
  { key: 'auth', label: '授权', icon: Key },
];

function App() {
  // ---- 页面路由 ----
  // 如果 SPA 被挂载在 /auth/ 路径下，默认进入授权中心；/auth/dashboard 进仪表盘
  const getInitialPage = (): PageRoute => {
    if (typeof window === 'undefined') return 'home';
    const p = window.location.pathname;
    if (p.startsWith('/auth/dashboard')) return 'dashboard';
    if (p.startsWith('/auth')) return 'auth';
    return 'home';
  };
  const [page, setPage] = useState<PageRoute>(getInitialPage());

  // ---- 模型选择 ----
  const [selectedModel, setSelectedModel] = useState<AIModel | null>(null);

  // ---- 聊天室状态 ----
  const [rooms, setRooms] = useState<Room[]>(INITIAL_ROOMS);
  const [activeRoomId, setActiveRoomId] = useState<string>('room_team');
  const [audits, setAudits] = useState<AuditEntry[]>(INITIAL_AUDITS);

  const activeRoom = rooms.find(r => r.id === activeRoomId) || rooms[0];

  const handleSendMessage = useCallback((message: Message) => {
    setRooms(prev => prev.map(room => {
      if (room.id === message.roomId) {
        return {
          ...room,
          messages: [...room.messages, message],
          lastActive: message.timestamp,
        };
      }
      return room;
    }));

    const newAudit: AuditEntry = {
      id: `audit-${Date.now()}`,
      timestamp: message.timestamp,
      module: '消息发送',
      level: message.audit,
      message: `${message.sender.name} 在 ${activeRoom?.name || '未知房间'} 发送消息 [${message.audit}]`,
      dna: message.dna,
    };
    setAudits(prev => [newAudit, ...prev].slice(0, 100));
  }, [activeRoom?.name]);

  const handleRoomSelect = useCallback((roomId: string) => {
    setActiveRoomId(roomId);
    setRooms(prev => prev.map(r =>
      r.id === roomId ? { ...r, unreadCount: 0 } : r
    ));
  }, []);

  const handleSelectModel = useCallback((model: AIModel) => {
    setSelectedModel(model);
    setPage('chat');
  }, []);

  const handleNavigate = useCallback((target: PageRoute) => {
    setPage(target);
  }, []);

  // ---- 渲染主内容区 ----
  const renderMainContent = () => {
    switch (page) {
      case 'home':
        return (
          <ModelPlaza
            onSelectModel={handleSelectModel}
            onNavigate={handleNavigate}
            selectedModelId={selectedModel?.id || null}
          />
        );
      case 'commander':
        return <CommandCenter />;
      case 'docs':
        return <PublicDocuments />;
      case 'plaza':
        return (
          <OpenPlaza onNavigate={handleNavigate} />
        );
      case 'chat':
        return (
          <>
            <Sidebar
              rooms={rooms}
              activeRoomId={activeRoomId}
              onRoomSelect={handleRoomSelect}
              uid={CURRENT_USER.uid}
              creditScore={CURRENT_USER.creditScore}
              contributionScore={CURRENT_USER.contributionScore}
              gpgFingerprint={CURRENT_USER.gpgFingerprint || ''}
            />
            <ChatRoom
              room={activeRoom}
              currentUser={CURRENT_USER}
              activeModel={selectedModel}
              onSendMessage={handleSendMessage}
              onNavigate={handleNavigate}
              rooms={rooms}
              activeRoomId={activeRoomId}
              onRoomSelect={handleRoomSelect}
            />
            <RightPanel audits={audits} />
          </>
        );
      case 'developer':
        return (
          <DeveloperCenter onNavigate={handleNavigate} />
        );
      case 'auth':
        return (
          <AuthManager onNavigate={handleNavigate} />
        );
      case 'dashboard':
        return <Dashboard />;
      default:
        return null;
    }
  };

  const isChatPage = page === 'chat';

  return (
    <div className="h-screen w-screen flex flex-col bg-zinc-950 text-zinc-100 overflow-hidden">
      {/* ===== 顶部DNA导航栏 ===== */}
      <header className="h-11 flex items-center px-4 border-b border-zinc-800/50 bg-zinc-950/90 backdrop-blur-sm shrink-0 z-50">
        {/* Logo */}
        <div className="flex items-center gap-2 mr-6">
          <div className="w-7 h-7 rounded bg-gradient-to-br from-red-500/20 to-amber-500/20 border border-red-500/30 flex items-center justify-center">
            <span className="text-sm">龍</span>
          </div>
          <div className="flex items-center gap-1.5">
            <h1 className="text-sm font-bold bg-gradient-to-r from-amber-400 to-red-400 bg-clip-text text-transparent">
              龍之心语
            </h1>
            <span className="text-[10px] px-1 py-0.5 rounded bg-zinc-800/50 text-zinc-500 font-mono border border-zinc-700/30">
              v2.0
            </span>
          </div>
        </div>

        {/* 主导航 */}
        <nav className="flex items-center gap-1">
          {NAV_ITEMS.map(item => {
            const Icon = item.icon;
            const isActive = page === item.key;
            return (
              <button
                key={item.key}
                onClick={() => setPage(item.key)}
                className={`
                  flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium transition-all
                  ${isActive
                    ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20'
                    : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50 border border-transparent'
                  }
                `}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
                {item.key === 'chat' && (
                  <span className="ml-0.5 text-[10px] px-1 py-0 rounded-full bg-zinc-800 text-zinc-500">
                    {rooms.reduce((sum, r) => sum + r.unreadCount, 0)}
                  </span>
                )}
              </button>
            );
          })}
        </nav>

        {/* 外部社区入口 */}
        <a
          href="http://localhost:8888"
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/50 border border-transparent transition-all"
        >
          <Users className="w-3.5 h-3.5" />
          <span>开发者社区</span>
        </a>

        {/* DNA 显示 */}
        <div className="flex-1 flex items-center justify-center">
          <code className="text-[10px] text-amber-500/40 font-mono truncate max-w-lg">
            {generateDNA('HEART-TALK', 'SYSTEM-ACTIVE')}
          </code>
        </div>

        {/* 状态指示器 */}
        <div className="flex items-center gap-3">
          {selectedModel && (
            <div className="flex items-center gap-1 text-[10px] px-2 py-1 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Server className="w-3 h-3" />
              <span>{selectedModel.name}</span>
              <span className="text-emerald-500/50">{selectedModel.type === 'local' ? '· 本地' : selectedModel.type === 'cloud' ? '· 云端' : '· 龍魂'}</span>
            </div>
          )}
          <div className="flex items-center gap-1 text-[10px] text-zinc-500">
            <Shield className="w-3 h-3 text-emerald-500" />
            <span>已加密</span>
          </div>
          <div className="flex items-center gap-1 text-[10px] text-zinc-500">
            <Terminal className="w-3 h-3 text-amber-500" />
            <span>终端模式</span>
          </div>
          <div className="flex items-center gap-1 text-[10px] text-zinc-500">
            <Cpu className="w-3 h-3 text-sky-500" />
            <span>本地优先</span>
          </div>
          <div className="w-px h-4 bg-zinc-800" />
          <span className="text-[10px] text-zinc-600 font-mono">UID9622</span>
        </div>
      </header>

      {/* ===== 主内容区 ===== */}
      <main className={`
        flex-1 overflow-hidden
        ${isChatPage ? 'flex' : ''}
      `}>
        {renderMainContent()}
      </main>

      {/* ===== 底部状态栏 ===== */}
      <footer className="h-6 flex items-center px-4 border-t border-zinc-800/50 bg-zinc-950/90 text-[10px] text-zinc-600 shrink-0">
        <div className="flex items-center gap-1">
          <span className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse" />
          <span>龍魂系统运行中</span>
        </div>
        <div className="w-px h-3 bg-zinc-800 mx-3" />
        <span>龍魂万年历已激活</span>
        <div className="w-px h-3 bg-zinc-800 mx-3" />
        <span>三层监督: 在线</span>
        <div className="w-px h-3 bg-zinc-800 mx-3" />
        <span>DNA追溯: 激活</span>
        <div className="w-px h-3 bg-zinc-800 mx-3" />
        <Lock className="w-3 h-3 text-zinc-700 mr-1" />
        <span className="text-zinc-700">端侧加密</span>
        <div className="w-px h-3 bg-zinc-800 mx-3" />
        <Zap className="w-3 h-3 text-zinc-700 mr-1" />
        <span className="text-zinc-700">MCP就绪</span>
        <div className="flex-1" />
        <code className="text-zinc-700 font-mono">#龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v2.0</code>
        <span className="ml-2 text-zinc-700">中华人民共和国 · 龍魂系统 · UID9622</span>
      </footer>
    </div>
  );
}

export default App;
