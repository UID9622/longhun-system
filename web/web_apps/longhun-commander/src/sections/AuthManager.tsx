归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 授权管理中心 · 七因子信任等级 · 与 longhun888 官网身份打通
// DNA: #龍芯⚡️2026-06-28-LONGHUN-7FACTOR-AUTH-OFFICIAL-v1.0

import { useEffect, useState } from 'react';
import {
  Shield, Key, UserCheck, FileSignature, Lock, Clock, CheckCircle, XCircle, Plus,
  Mail, Smartphone, KeyRound, Fingerprint, Users, Sparkles, ChevronRight, LogIn, LayoutDashboard
} from 'lucide-react';
import { Switch } from '@/components/ui/switch';
import { Progress } from '@/components/ui/progress';
import type { AuthFactor, AuthLevel, PageRoute } from '@/types';
import { AUTH_LEVEL_CONFIG, AUTH_FACTOR_CONFIG, AUTH_FEATURE_MAP } from '@/types';
import { AUTH_GRANTS } from '@/utils/data';

interface Props {
  onNavigate: (page: PageRoute) => void;
}

interface CommunityIdentity {
  soul_id: string;
  uid: string;
  name: string;
  registered_at: string;
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

function levelColorDot(level: AuthLevel) {
  const map: Record<AuthLevel, string> = {
    visitor: 'bg-zinc-600',
    citizen: 'bg-sky-500',
    developer: 'bg-emerald-500',
    maintainer: 'bg-amber-500',
    guardian: 'bg-purple-500',
    founder: 'bg-red-500',
  };
  return map[level];
}

export default function AuthManager({ onNavigate }: Props) {
  const [showApply, setShowApply] = useState(false);
  const [applyRepo, setApplyRepo] = useState('');
  const [applyLevel, setApplyLevel] = useState<AuthLevel>('developer');
  const [identity, setIdentity] = useState<CommunityIdentity | null>(null);
  const [enabledFactors, setEnabledFactors] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [lastDna, setLastDna] = useState('');

  const isFounder = identity?.uid === 'UID9622';
  const score = isFounder ? 7 : enabledFactors.size;
  const effectiveLevel: AuthLevel = isFounder ? 'founder' : scoreToLevel(score);
  const levelCfg = AUTH_LEVEL_CONFIG[effectiveLevel];
  const unlockedFeatures = AUTH_FEATURE_MAP[effectiveLevel];

  // 加载官网身份 + 七因子状态
  useEffect(() => {
    let mounted = true;
    const raw = typeof window !== 'undefined' ? localStorage.getItem('longhun_identity') : null;
    const parsed: CommunityIdentity | null = raw ? JSON.parse(raw) : null;
    if (!mounted) return;
    setIdentity(parsed);

    if (parsed) {
      fetch(`/api/auth/factors?soul_id=${encodeURIComponent(parsed.soul_id)}`)
        .then(r => r.json())
        .then(data => {
          if (data.ok && Array.isArray(data.factors)) {
            setEnabledFactors(new Set(data.factors));
            setLastDna(data.dna);
          }
        })
        .finally(() => setLoading(false));
    } else {
      setLoading(false);
    }
    return () => { mounted = false; };
  }, []);

  const persistFactors = async (next: Set<string>) => {
    setEnabledFactors(next);
    if (!identity) return;
    try {
      const res = await fetch('/api/auth/factors', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          soul_id: identity.soul_id,
          factors: Array.from(next),
        }),
      });
      const data = await res.json();
      if (data.ok) setLastDna(data.dna);
    } catch (e) {
      console.warn('factor persist failed', e);
    }
  };

  const toggleFactor = (id: string) => {
    if (isFounder) return;
    const next = new Set(enabledFactors);
    if (next.has(id)) next.delete(id);
    else next.add(id);
    persistFactors(next);
  };

  const statusConfig = {
    active: { icon: CheckCircle, color: 'text-green-400', bg: 'bg-green-500/10', label: '有效' },
    expired: { icon: Clock, color: 'text-amber-400', bg: 'bg-amber-500/10', label: '已过期' },
    revoked: { icon: XCircle, color: 'text-red-400', bg: 'bg-red-500/10', label: '已撤销' },
  };

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* 头部 */}
      <div className="p-6 border-b border-zinc-800/50">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-red-400 to-amber-400 bg-clip-text text-transparent">
              授权管理中心
            </h1>
            <p className="text-sm text-zinc-500 mt-1">
              七因子信任等级 · 与 longhun888 官网身份打通 · DNA 追溯
            </p>
          </div>
          <div className="flex items-center gap-2">
            <a
              href="/auth/dashboard"
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-emerald-500/30 bg-emerald-500/10 text-xs text-emerald-400 hover:bg-emerald-500/20 transition-all"
            >
              <LayoutDashboard className="w-3.5 h-3.5" />权限仪表盘
            </a>
            <button
              onClick={() => onNavigate('developer')}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-zinc-700/50 bg-zinc-800/50 text-xs text-zinc-300 hover:border-red-500/30 hover:bg-red-500/5 transition-all"
            >
              <Key className="w-3.5 h-3.5" />开发者接入
            </button>
            <button
              onClick={() => setShowApply(!showApply)}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-red-500/30 bg-red-500/10 text-xs text-red-400 hover:bg-red-500/20 transition-all"
            >
              <Plus className="w-3.5 h-3.5" />申请授权
            </button>
            <a
              href="http://localhost:8888"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-zinc-700/50 bg-zinc-800/50 text-xs text-zinc-300 hover:border-amber-500/30 hover:bg-amber-500/5 transition-all"
            >
              <Users className="w-3.5 h-3.5" />返回社区
            </a>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
        {/* 申请表单 */}
        {showApply && (
          <div className="mb-6 p-4 rounded-lg border border-red-500/20 bg-red-500/5">
            <h3 className="text-sm font-bold text-red-400 mb-3">新授权申请</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <div>
                <label className="text-[10px] text-zinc-500 block mb-1">目标仓库</label>
                <input
                  value={applyRepo}
                  onChange={e => setApplyRepo(e.target.value)}
                  placeholder="如: longhun-system"
                  className="w-full px-3 py-2 rounded border border-zinc-700 bg-zinc-900/50 text-xs text-zinc-300 placeholder-zinc-600 outline-none focus:border-red-500/30"
                />
              </div>
              <div>
                <label className="text-[10px] text-zinc-500 block mb-1">申请级别</label>
                <select
                  value={applyLevel}
                  onChange={e => setApplyLevel(e.target.value as AuthLevel)}
                  className="w-full px-3 py-2 rounded border border-zinc-700 bg-zinc-900/50 text-xs text-zinc-300 outline-none focus:border-red-500/30"
                >
                  {(Object.entries(AUTH_LEVEL_CONFIG) as [AuthLevel, typeof AUTH_LEVEL_CONFIG.visitor][]).map(([key, cfg]) => (
                    <option key={key} value={key}>{cfg.label} — {cfg.desc}</option>
                  ))}
                </select>
              </div>
              <div className="flex items-end">
                <button
                  onClick={() => { setShowApply(false); }}
                  className="w-full py-2 rounded bg-red-500/20 text-red-400 border border-red-500/30 text-xs font-medium hover:bg-red-500/30 transition-all"
                >
                  提交申请（需GPG签名）
                </button>
              </div>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* 七因子面板 */}
          <div className="xl:col-span-2 space-y-6">
            <div className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xs font-medium text-zinc-300 flex items-center gap-1.5">
                  <Shield className="w-3.5 h-3.5 text-amber-400" />
                  七因子防御
                </h3>
                {isFounder && (
                  <span className="text-[10px] text-red-400 border border-red-500/30 bg-red-500/10 px-2 py-0.5 rounded">
                    UID9622 · 创始人权限
                  </span>
                )}
              </div>

              {!identity && !loading && (
                <div className="mb-4 p-3 rounded border border-amber-500/20 bg-amber-500/5 text-xs text-amber-300 flex items-center justify-between">
                  <span className="flex items-center gap-2">
                    <LogIn className="w-3.5 h-3.5" />
                    尚未注册官网主权身份，当前为空壳账号（visitor）
                  </span>
                  <a
                    href="/register.html"
                    className="px-2 py-1 rounded bg-amber-500/20 border border-amber-500/30 hover:bg-amber-500/30 transition-all"
                  >
                    去注册
                  </a>
                </div>
              )}

              {loading ? (
                <p className="text-xs text-zinc-500">加载身份与因子状态...</p>
              ) : (
                <div className="space-y-3">
                  {AUTH_FACTOR_CONFIG.map((factor: AuthFactor) => {
                    const Icon = ICON_MAP[factor.icon] || Lock;
                    const enabled = enabledFactors.has(factor.id);
                    return (
                      <div
                        key={factor.id}
                        className={`flex items-center justify-between p-3 rounded border transition-all ${
                          enabled ? 'border-amber-500/20 bg-amber-500/5' : 'border-zinc-800/50 bg-zinc-900/20'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-8 h-8 rounded flex items-center justify-center border ${
                            enabled ? 'border-amber-500/30 text-amber-400 bg-amber-500/10' : 'border-zinc-700 text-zinc-500 bg-zinc-800/30'
                          }`}>
                            <Icon className="w-4 h-4" />
                          </div>
                          <div>
                            <p className={`text-xs font-medium ${enabled ? 'text-zinc-200' : 'text-zinc-400'}`}>{factor.label}</p>
                            <p className="text-[10px] text-zinc-600">{factor.desc}</p>
                          </div>
                        </div>
                        <Switch
                          checked={enabled}
                          onCheckedChange={() => toggleFactor(factor.id)}
                          disabled={isFounder}
                        />
                      </div>
                    );
                  })}
                </div>
              )}

              <div className="mt-4 space-y-2">
                <div className="flex items-center justify-between text-[10px] text-zinc-500">
                  <span>信任因子 {score} / 7</span>
                  <span>{Math.round((score / 7) * 100)}%</span>
                </div>
                <Progress value={(score / 7) * 100} className="h-1.5 bg-zinc-800" />
              </div>

              {lastDna && (
                <code className="block mt-3 text-[9px] text-amber-500/40 font-mono truncate">
                  {lastDna}
                </code>
              )}
            </div>

            {/* 授权记录 */}
            <div>
              <h3 className="text-xs text-zinc-500 font-medium mb-3 flex items-center gap-1.5">
                <FileSignature className="w-3.5 h-3.5" />授权记录
              </h3>
              <div className="space-y-2">
                {AUTH_GRANTS.map(grant => {
                  const st = statusConfig[grant.status];
                  const grantLevelCfg = AUTH_LEVEL_CONFIG[grant.level];
                  const StatusIcon = st.icon;
                  return (
                    <div key={grant.id} className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center gap-2">
                          <StatusIcon className={`w-4 h-4 ${st.color}`} />
                          <span className="text-sm font-medium text-zinc-300">{grant.grantee}</span>
                          <span className={`text-[10px] px-1.5 py-0.5 rounded ${grantLevelCfg.color} bg-zinc-800/50`}>
                            {grantLevelCfg.label}
                          </span>
                        </div>
                        {grant.gpgSigned && (
                          <span className="flex items-center gap-1 text-[10px] text-emerald-500">
                            <Lock className="w-3 h-3" />GPG已签
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-zinc-500 mt-1">仓库: {grant.repo}</p>
                      <div className="flex items-center gap-3 mt-1 text-[10px] text-zinc-600">
                        <span>授权: {grant.grantedAt}</span>
                        {grant.expiresAt && <span>到期: {grant.expiresAt}</span>}
                        <span className={`px-1 py-0.5 rounded ${st.bg} ${st.color}`}>{st.label}</span>
                      </div>
                      <code className="text-[8px] text-amber-500/30 font-mono block mt-1 truncate">{grant.dna}</code>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* 当前身份 + 已解锁功能 */}
          <div className="space-y-4">
            {/* 当前身份 */}
            <div className={`p-4 rounded-lg border ${effectiveLevel === 'founder' ? 'border-red-500/20 bg-red-500/5' : 'border-amber-500/20 bg-amber-500/5'}`}>
              <h3 className="text-xs font-medium text-amber-400 mb-2 flex items-center gap-1.5">
                <UserCheck className="w-3.5 h-3.5" />当前身份
              </h3>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-red-500/20 to-amber-500/20 border border-red-500/30 flex items-center justify-center text-lg">
                  龍
                </div>
                <div>
                  <p className="text-sm font-bold text-zinc-200">
                    {identity?.name || '未注册访客'}
                  </p>
                  <p className="text-[10px] text-zinc-500">
                    {identity ? identity.uid : '无 UID'}
                  </p>
                </div>
                <span className={`ml-auto text-sm font-bold ${levelCfg.color}`}>{levelCfg.label}</span>
              </div>
              {identity && (
                <>
                  <p className="text-[10px] text-zinc-600 mt-2 font-mono truncate">魂灵ID: {identity.soul_id}</p>
                  <p className="text-[10px] text-zinc-600 mt-1 font-mono truncate">注册时间: {identity.registered_at}</p>
                </>
              )}
            </div>

            {/* 等级说明 */}
            <div className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
              <h3 className="text-xs text-zinc-500 font-medium mb-2 flex items-center gap-1.5">
                <Shield className="w-3.5 h-3.5" />权限等级
              </h3>
              <div className="space-y-2">
                {(Object.entries(AUTH_LEVEL_CONFIG) as [AuthLevel, typeof AUTH_LEVEL_CONFIG.visitor][]).map(([key, cfg]) => {
                  const active = key === effectiveLevel;
                  return (
                    <div key={key} className={`flex items-center gap-3 p-2 rounded border transition-all ${
                      active ? 'border-amber-500/30 bg-amber-500/5' : 'border-zinc-800/30 bg-zinc-900/20'
                    }`}>
                      <div className={`w-3 h-3 rounded-full ${levelColorDot(key)} ${active ? 'ring-2 ring-amber-500/30' : ''}`} />
                      <div className="flex-1">
                        <span className={`text-xs font-medium ${cfg.color}`}>{cfg.label}</span>
                        <p className="text-[10px] text-zinc-600">{cfg.desc}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>

            {/* 已解锁功能 */}
            <div className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
              <h3 className="text-xs text-zinc-400 mb-2 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-emerald-400" />
                已解锁功能（{levelCfg.label}）
              </h3>
              <ul className="space-y-1.5">
                {unlockedFeatures.map((feat, idx) => (
                  <li key={idx} className="flex items-center gap-2 text-[10px] text-zinc-300">
                    <ChevronRight className="w-3 h-3 text-emerald-500" />
                    {feat}
                  </li>
                ))}
              </ul>
            </div>

            {/* 授权流程 */}
            <div className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
              <h4 className="text-xs text-zinc-400 mb-2">授权流程</h4>
              <div className="flex flex-wrap items-center gap-1 text-[10px] text-zinc-600">
                <span className="px-1.5 py-0.5 rounded bg-zinc-800">注册空壳</span>
                <span>→</span>
                <span className="px-1.5 py-0.5 rounded bg-zinc-800">自选因子</span>
                <span>→</span>
                <span className="px-1.5 py-0.5 rounded bg-zinc-800">GPG/硬件验证</span>
                <span>→</span>
                <span className="px-1.5 py-0.5 rounded bg-zinc-800">DNA授权</span>
                <span>→</span>
                <span className="px-1.5 py-0.5 rounded bg-emerald-500/10 text-emerald-400">功能解锁</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
