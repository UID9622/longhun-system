归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 开源社区广场 · 分类/仓库/贡献者
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v2.0

import { useState } from 'react';
import { Search, GitFork, Star, Users, ExternalLink, Award, Shield, FileCode, BookOpen } from 'lucide-react';
import type { PlazaCategory, PageRoute } from '@/types';
import { PLAZA_CATEGORY_CONFIG } from '@/types';
import { PLAZA_REPOS, CONTRIBUTORS } from '@/utils/data';

interface Props {
  onNavigate: (page: PageRoute) => void;
}

export default function OpenPlaza({ onNavigate }: Props) {
  const [category, setCategory] = useState<PlazaCategory>('all');
  const [search, setSearch] = useState('');

  const filteredRepos = PLAZA_REPOS.filter(repo => {
    const matchCat = category === 'all' || repo.category === category;
    const matchSearch = !search || repo.name.toLowerCase().includes(search.toLowerCase()) || repo.description.includes(search);
    return matchCat && matchSearch;
  });

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* 头部 */}
      <div className="p-6 border-b border-zinc-800/50">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-emerald-400 to-sky-400 bg-clip-text text-transparent">
              开源社区广场
            </h1>
            <p className="text-sm text-zinc-500 mt-1">
              龍魂生态仓库 · 分类浏览 · 贡献者排行 · 开放授权
            </p>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={() => onNavigate('auth')}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-zinc-700/50 bg-zinc-800/50 text-xs text-zinc-300 hover:border-emerald-500/30 hover:bg-emerald-500/5 transition-all"
            >
              <Shield className="w-3.5 h-3.5" />授权管理
            </button>
            <button
              onClick={() => onNavigate('developer')}
              className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-zinc-700/50 bg-zinc-800/50 text-xs text-zinc-300 hover:border-emerald-500/30 hover:bg-emerald-500/5 transition-all"
            >
              <FileCode className="w-3.5 h-3.5" />开发者接入
            </button>
          </div>
        </div>

        {/* 搜索 + 分类 */}
        <div className="flex items-center gap-3 mt-4">
          <div className="relative flex-1 max-w-xs">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 w-3.5 h-3.5 text-zinc-600" />
            <input
              value={search}
              onChange={e => setSearch(e.target.value)}
              placeholder="搜索仓库..."
              className="w-full pl-8 pr-3 py-1.5 rounded-lg border border-zinc-800 bg-zinc-900/50 text-xs text-zinc-300 placeholder-zinc-600 outline-none focus:border-emerald-500/30 transition-colors"
            />
          </div>
          <div className="flex flex-wrap gap-1.5">
            {(Object.entries(PLAZA_CATEGORY_CONFIG) as [PlazaCategory, typeof PLAZA_CATEGORY_CONFIG.all][]).map(([key, config]) => (
              <button
                key={key}
                onClick={() => setCategory(key)}
                className={`px-2.5 py-1 rounded text-[11px] border transition-all ${
                  category === key
                    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                    : 'bg-zinc-800/30 text-zinc-500 border-zinc-800/50 hover:border-zinc-700/50'
                }`}
              >
                {config.icon} {config.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 内容区 */}
      <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
          {/* 仓库列表（占2列） */}
          <div className="xl:col-span-2 space-y-3">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xs text-zinc-500 font-medium">仓库列表</h3>
              <span className="text-[10px] text-zinc-700 font-mono">{filteredRepos.length} 个</span>
            </div>
            {filteredRepos.map(repo => (
              <div
                key={repo.id}
                className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20 hover:border-zinc-700/50 hover:bg-zinc-800/20 transition-all group"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <BookOpen className="w-4 h-4 text-amber-500/70" />
                      <h4 className="text-sm font-bold text-amber-400/90">{repo.name}</h4>
                      {repo.authRequired && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded bg-red-500/10 text-red-400 border border-red-500/20">需授权</span>
                      )}
                    </div>
                    <p className="text-xs text-zinc-400 mt-1 leading-relaxed">{repo.description}</p>
                    <div className="flex flex-wrap gap-1 mt-2">
                      {repo.tags.map(tag => (
                        <span key={tag} className="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-500">{tag}</span>
                      ))}
                    </div>
                  </div>
                  <a
                    href={repo.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="shrink-0 ml-3 p-2 rounded border border-zinc-800/50 text-zinc-600 hover:text-emerald-400 hover:border-emerald-500/30 transition-all opacity-0 group-hover:opacity-100"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
                <div className="flex items-center gap-4 mt-3 text-[10px] text-zinc-600">
                  <span className="flex items-center gap-1"><Star className="w-3 h-3" />{repo.stars}</span>
                  <span className="flex items-center gap-1"><GitFork className="w-3 h-3" />{repo.forks}</span>
                  <span className="flex items-center gap-1"><Users className="w-3 h-3" />{repo.contributors}贡献者</span>
                  <span>{repo.language}</span>
                  <span className="ml-auto font-mono text-zinc-700">{repo.license}</span>
                </div>
                <code className="text-[9px] text-amber-500/30 font-mono block mt-1 truncate">{repo.dna}</code>
              </div>
            ))}
          </div>

          {/* 贡献者排行（占1列） */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-xs text-zinc-500 font-medium">贡献者排行</h3>
              <Award className="w-3.5 h-3.5 text-amber-500/50" />
            </div>
            <div className="space-y-2">
              {CONTRIBUTORS.sort((a, b) => b.contributionScore - a.contributionScore).map((c, i) => (
                <div
                  key={c.uid}
                  className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20"
                >
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-full bg-gradient-to-br from-amber-500/20 to-red-500/20 border border-amber-500/20 flex items-center justify-center text-xs font-bold text-amber-400">
                      {i + 1}
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-1.5">
                        <span className="text-sm font-medium text-zinc-300">{c.name}</span>
                        <span className={`text-[10px] ${c.level === 'founder' ? 'text-red-400' : c.level === 'maintainer' ? 'text-amber-400' : c.level === 'developer' ? 'text-emerald-400' : 'text-sky-400'}`}>
                          {c.level}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-[10px] text-zinc-600">
                        <span>积分: {c.contributionScore.toLocaleString()}</span>
                        <span>仓库: {c.repos}</span>
                      </div>
                    </div>
                  </div>
                  <code className="text-[8px] text-amber-500/30 font-mono block mt-1 truncate">{c.dna}</code>
                </div>
              ))}
            </div>

            {/* 快速统计 */}
            <div className="mt-4 p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
              <h4 className="text-xs text-zinc-500 mb-2">广场统计</h4>
              <div className="grid grid-cols-2 gap-2">
                <div className="text-center p-2 rounded bg-zinc-800/30">
                  <p className="text-lg font-bold text-emerald-400">{PLAZA_REPOS.length}</p>
                  <p className="text-[10px] text-zinc-600">仓库</p>
                </div>
                <div className="text-center p-2 rounded bg-zinc-800/30">
                  <p className="text-lg font-bold text-sky-400">{CONTRIBUTORS.length}</p>
                  <p className="text-[10px] text-zinc-600">贡献者</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
