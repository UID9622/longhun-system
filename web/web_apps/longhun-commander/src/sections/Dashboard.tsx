归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 用户权限仪表盘 · 个人中心
// DNA: #龍芯⚡️2026-06-28-LONGHUN-AUTH-DASHBOARD-v1.0

import { useEffect, useState } from 'react';
import {
  Shield, Lock, Mail, Smartphone, FileSignature, KeyRound, Fingerprint, Users,
  Activity, History, ChevronRight, LogIn, ArrowRight
} from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import type { AuthFactor, AuthLevel } from '@/types';
import { AUTH_LEVEL_CONFIG, AUTH_FACTOR_CONFIG, AUTH_FEATURE_MAP } from '@/types';

interface CommunityIdentity {
  soul_id: string;
  uid: string;
  name: string;
  registered_at: string;
  dna: string;
}

interface HistoryEntry {
  timestamp: string;
  action: 'enable' | 'disable' | 'level_change' | string;
  factor?: string;
  old_level?: string;
  new_level?: string;
  dna: string;
}

const ICON_MAP: Record<string, typeof Lock> = {
  Lock, Mail, Smartphone, FileSignature, KeyRound, Fingerprint, Users,
};

function scoreToLevel(score: number): AuthLevel {
  if (score === 0) return 'visitor';
  if (score <= 2) return 'citizen';
  if (score <= 4) return 'developer';
  if (score <= 6) return 'maintainer';
  return 'guardian';
}

export default function Dashboard() {
  const [identity, setIdentity] = useState<CommunityIdentity | null>(null);
  const [factors, setFactors] = useState<string[]>([]);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [lastDna, setLastDna] = useState('');

  const level = identity
    ? (identity.uid === 'UID9622' ? 'founder' : scoreToLevel(factors.length))
    : 'visitor';
  const levelCfg = AUTH_LEVEL_CONFIG[level];
  const unlockedFeatures = AUTH_FEATURE_MAP[level];

  useEffect(() => {
    const raw = typeof window !== 'undefined' ? localStorage.getItem('longhun_identity') : null;
    const parsed: CommunityIdentity | null = raw ? JSON.parse(raw) : null;
    setIdentity(parsed);

    if (parsed) {
      fetch(`/api/auth/factors?soul_id=${encodeURIComponent(parsed.soul_id)}`)
        .then(r => r.json())
        .then(data => {
          if (data.ok) {
            setFactors(data.factors || []);
            setHistory(data.history || []);
            setLastDna(data.dna);
          }
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
  }, []);

  if (!identity && !loading) {
    return (
      <div className="h-full flex flex-col items-center justify-center bg-zinc-950 text-zinc-100 p-6">
        <div className="max-w-md w-full p-6 rounded-xl border border-amber-500/20 bg-amber-500/5 text-center">
          <LogIn className="w-10 h-10 text-amber-400 mx-auto mb-4" />
          <h2 className="text-lg font-bold text-zinc-200 mb-2">尚未登录</h2>
          <p className="text-xs text-zinc-400 mb-4">
            请先在官网注册主权身份，个人中心才能显示你的七因子状态与授权等级。
          </p>
          <div className="flex items-center justify-center gap-3">
            <a href="/register.html" className="px-4 py-2 rounded bg-amber-500/20 border border-amber-500/30 text-amber-400 text-xs hover:bg-amber-500/30 transition-all">
              去注册
            </a>
            <a href="/auth/" className="px-4 py-2 rounded border border-zinc-700 text-zinc-300 text-xs hover:bg-zinc-800/50 transition-all">
              授权中心
            </a>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="h-full flex flex-col bg-zinc-950 text-zinc-100 overflow-hidden">
      {/* 顶部 */}
      <div className="h-14 flex items-center justify-between px-6 border-b border-zinc-800/50 bg-zinc-900/30 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-emerald-500/20 to-sky-500/20 border border-emerald-500/30 flex items-center justify-center">
            <Activity className="w-4 h-4 text-emerald-400" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-zinc-100">用户权限仪表盘</h2>
            <p className="text-[10px] text-zinc-500">个人中心 · 七因子 · 授权历史</p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <a
            href="http://localhost:8888"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 text-[10px] text-zinc-400 hover:text-zinc-300 transition-colors"
          >
            返回社区
          </a>
          <a
            href="/auth/"
            className="flex items-center gap-1 text-[10px] text-amber-400 hover:text-amber-300 transition-colors"
          >
            前往授权中心 <ArrowRight className="w-3 h-3" />
          </a>
        </div>
      </div>

      {/* 内容 */}
      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-5xl mx-auto space-y-6">
          {/* 身份与等级 */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className={`p-4 rounded-lg border ${level === 'founder' ? 'border-red-500/20 bg-red-500/5' : 'border-emerald-500/20 bg-emerald-500/5'}`}>
              <h3 className="text-xs font-medium text-emerald-400 mb-2 flex items-center gap-1.5">
                <Shield className="w-3.5 h-3.5" />当前身份
              </h3>
              <p className="text-sm font-bold text-zinc-200">{identity?.name || '未注册访客'}</p>
              <p className="text-[10px] text-zinc-500 font-mono truncate">UID: {identity?.uid || '-'}</p>
              <p className="text-[10px] text-zinc-600 font-mono truncate mt-1">魂灵ID: {identity?.soul_id || '-'}</p>
            </div>

            <div className="p-4 rounded-lg border border-amber-500/20 bg-amber-500/5">
              <h3 className="text-xs font-medium text-amber-400 mb-2 flex items-center gap-1.5">
                <Activity className="w-3.5 h-3.5" />授权等级
              </h3>
              <p className={`text-2xl font-bold ${levelCfg.color}`}>{levelCfg.label}</p>
              <p className="text-[10px] text-zinc-500 mt-1">{levelCfg.desc}</p>
            </div>

            <div className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
              <h3 className="text-xs font-medium text-zinc-400 mb-2">信任因子</h3>
              <div className="flex items-center justify-between text-[10px] text-zinc-500 mb-1">
                <span>{factors.length} / 7</span>
                <span>{Math.round((factors.length / 7) * 100)}%</span>
              </div>
              <Progress value={(factors.length / 7) * 100} className="h-1.5 bg-zinc-800" />
              {lastDna && (
                <code className="block mt-3 text-[9px] text-amber-500/40 font-mono truncate">{lastDna}</code>
              )}
            </div>
          </div>

          {/* 七因子状态 */}
          <div className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
            <h3 className="text-xs font-medium text-zinc-300 mb-4 flex items-center gap-1.5">
              <Shield className="w-3.5 h-3.5 text-amber-400" />七因子开启状态
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
              {AUTH_FACTOR_CONFIG.map((factor: AuthFactor) => {
                const Icon = ICON_MAP[factor.icon] || Lock;
                const enabled = factors.includes(factor.id);
                return (
                  <div
                    key={factor.id}
                    className={`flex items-center gap-3 p-3 rounded border transition-all ${
                      enabled ? 'border-amber-500/20 bg-amber-500/5' : 'border-zinc-800/50 bg-zinc-900/30'
                    }`}
                  >
                    <div className={`w-8 h-8 rounded flex items-center justify-center border ${
                      enabled ? 'border-amber-500/30 text-amber-400 bg-amber-500/10' : 'border-zinc-700 text-zinc-600 bg-zinc-800/30'
                    }`}>
                      <Icon className="w-4 h-4" />
                    </div>
                    <div>
                      <p className={`text-xs font-medium ${enabled ? 'text-zinc-200' : 'text-zinc-500'}`}>{factor.label}</p>
                      <p className="text-[10px] text-zinc-600">{enabled ? '已启用' : '未启用'}</p>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* 已解锁功能 */}
          <div className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
            <h3 className="text-xs font-medium text-zinc-400 mb-3 flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-emerald-400" />
              已解锁功能（{levelCfg.label}）
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {unlockedFeatures.map((feat, idx) => (
                <div key={idx} className="flex items-center gap-2 text-[11px] text-zinc-300">
                  <ChevronRight className="w-3 h-3 text-emerald-500" />
                  {feat}
                </div>
              ))}
            </div>
          </div>

          {/* 授权历史 */}
          <div className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
            <h3 className="text-xs font-medium text-zinc-400 mb-3 flex items-center gap-1.5">
              <History className="w-3.5 h-3.5 text-sky-400" />
              授权变更历史（仅本人可见）
            </h3>
            {history.length === 0 ? (
              <p className="text-[11px] text-zinc-600">暂无授权变更记录。</p>
            ) : (
              <div className="space-y-2 max-h-64 overflow-auto pr-2">
                {history.slice().reverse().map((h, idx) => (
                  <div key={idx} className="p-2 rounded border border-zinc-800/30 bg-zinc-900/30 text-[11px]">
                    <div className="flex items-center justify-between mb-1">
                      <span className="text-zinc-300">
                        {h.action === 'enable' && `开启 ${h.factor}`}
                        {h.action === 'disable' && `关闭 ${h.factor}`}
                        {h.action === 'level_change' && `等级变更 ${h.old_level} → ${h.new_level}`}
                      </span>
                      <span className="text-[10px] text-zinc-500">{h.timestamp}</span>
                    </div>
                    <code className="block text-[9px] text-amber-500/40 font-mono truncate">{h.dna}</code>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
