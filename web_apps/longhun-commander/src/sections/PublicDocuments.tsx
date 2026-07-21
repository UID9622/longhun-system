// 龍魂公开文档中心 · 宪法 / 协议 / 论文一站式展示
// DNA: #龍芯⚡️2026-06-28-LONGHUN-PUBLIC-DOCS-v1.0

import { useEffect, useState } from 'react';
import { BookOpen, Shield, FileText, Globe, FlaskConical, Scale, ExternalLink } from 'lucide-react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { generateDNA } from '@/utils/dna';

interface PublicDoc {
  id: string;
  title: string;
  version: string;
  url: string;
  category: string;
}

const CATEGORY_CONFIG: Record<string, { label: string; icon: typeof BookOpen; color: string }> = {
  constitution: { label: '最高宪法', icon: Shield, color: 'text-red-400 border-red-400/30 bg-red-400/10' },
  protocol: { label: '协议规范', icon: Scale, color: 'text-amber-400 border-amber-400/30 bg-amber-400/10' },
  overview: { label: '系统概览', icon: Globe, color: 'text-sky-400 border-sky-400/30 bg-sky-400/10' },
  research: { label: '学术论文', icon: FlaskConical, color: 'text-purple-400 border-purple-400/30 bg-purple-400/10' },
  spec: { label: '技术规格', icon: FileText, color: 'text-emerald-400 border-emerald-400/30 bg-emerald-400/10' },
};

export default function PublicDocuments() {
  const [docs, setDocs] = useState<PublicDoc[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('/api/public-docs')
      .then(r => r.json())
      .then(data => {
        if (data.ok) setDocs(data.docs || []);
        else setError('接口返回异常');
      })
      .catch(e => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="h-full flex flex-col bg-zinc-950 text-zinc-100 overflow-hidden">
      {/* 顶部栏 */}
      <div className="h-14 flex items-center justify-between px-6 border-b border-zinc-800/50 bg-zinc-900/30 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-red-500/20 to-amber-500/20 border border-red-500/30 flex items-center justify-center">
            <BookOpen className="w-4 h-4 text-red-400" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-zinc-100">龍魂公开文档中心</h2>
            <p className="text-[10px] text-zinc-500">宪法 · 协议 · 论文 · 全部可溯源</p>
          </div>
        </div>
        <code className="text-[10px] text-amber-500/50 font-mono hidden sm:block">
          {generateDNA('PUBLIC-DOCS', 'UI-ACTIVE')}
        </code>
      </div>

      {/* 内容区 */}
      <div className="flex-1 overflow-auto p-6">
        <div className="max-w-5xl mx-auto space-y-6">
          {/* 宪法置顶区 */}
          <Card className="bg-gradient-to-br from-red-950/20 to-zinc-900/50 border-red-500/20">
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium text-red-300 flex items-center gap-2">
                <Shield className="w-4 h-4" />
                北辰-母协议 · 最高宪法
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <p className="text-xs text-zinc-300 leading-relaxed">
                北辰-母协议是龍魂系统的最高宪法，守护六条永恒原则与三条红线。任何决策、AI 行为、技术路线都必须服从该协议。
                协议永久公开，接受全世界监督，连创造者 UID9622 本人也不可违背。
              </p>
              <div className="flex flex-wrap gap-2">
                <Badge className="text-[10px] border-red-500/30 text-red-400 bg-red-500/10">为人民服务</Badge>
                <Badge className="text-[10px] border-red-500/30 text-red-400 bg-red-500/10">技术主权在中国</Badge>
                <Badge className="text-[10px] border-red-500/30 text-red-400 bg-red-500/10">开源透明</Badge>
                <Badge className="text-[10px] border-red-500/30 text-red-400 bg-red-500/10">DNA 全追溯</Badge>
              </div>
            </CardContent>
          </Card>

          {/* 文档列表 */}
          {loading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[...Array(4)].map((_, i) => (
                <Skeleton key={i} className="h-32 bg-zinc-900/50" />
              ))}
            </div>
          ) : error ? (
            <div className="p-6 rounded border border-red-500/20 bg-red-500/5 text-xs text-red-400">
              加载失败：{error}
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {docs.map(doc => {
                const cfg = CATEGORY_CONFIG[doc.category] || CATEGORY_CONFIG.overview;
                const Icon = cfg.icon;
                return (
                  <Card key={doc.id} className="bg-zinc-900/50 border-zinc-800/50 hover:border-zinc-700/50 transition-colors">
                    <CardHeader className="pb-2">
                      <div className="flex items-start justify-between gap-2">
                        <CardTitle className="text-xs font-medium text-zinc-200 flex items-center gap-2">
                          <Icon className={`w-3.5 h-3.5 ${cfg.color.split(' ')[0]}`} />
                          {doc.title}
                        </CardTitle>
                        <span className={`text-[10px] px-1.5 py-0.5 rounded border ${cfg.color}`}>
                          {cfg.label}
                        </span>
                      </div>
                    </CardHeader>
                    <CardContent className="space-y-3">
                      <div className="flex items-center gap-2 text-[10px] text-zinc-500">
                        <span>版本 {doc.version}</span>
                        <span className="w-px h-3 bg-zinc-700" />
                        <span className="font-mono">{doc.id}</span>
                      </div>
                      <a
                        href={doc.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-1 text-[10px] text-sky-400 hover:text-sky-300 transition-colors"
                      >
                        查看原文 <ExternalLink className="w-3 h-3" />
                      </a>
                    </CardContent>
                  </Card>
                );
              })}
            </div>
          )}

          {/* 主权声明 */}
          <div className="p-4 rounded border border-zinc-800/50 bg-zinc-900/30 text-[10px] text-zinc-500 leading-relaxed">
            <p>
              所有公开内容均归属中华人民共和国 · 龍魂系统 · UID9622。技术主权归中国，使用权归人民，贡献权归全人类。
              本页仅展示主权信封与公开索引，不涉及私钥、明文或未授权隐私内容。
            </p>
            <p className="mt-2 font-mono text-amber-500/50">#龍芯⚡️2026-06-28-LONGHUN-PUBLIC-DOCS-v1.0</p>
          </div>
        </div>
      </div>
    </div>
  );
}
