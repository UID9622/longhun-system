归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂模型指挥调度系统 · 官网控制台
// DNA: #龍芯⚡️2026-06-28-LONGHUN-COMMANDER-UI-v1.0

import { useState } from 'react';
import { Terminal, Play, Activity, GitBranch, BarChart3, Search, Shield, Cpu, Zap, ClipboardCheck } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { generateDNA } from '@/utils/dna';

export default function CommandCenter() {
  const [task, setTask] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const [lastDNA, setLastDNA] = useState('');

  const getIdentity = () => {
    if (typeof window === 'undefined') return null;
    const raw = localStorage.getItem('longhun_identity');
    return raw ? JSON.parse(raw) : null;
  };

  const callApi = async (endpoint: string, options?: RequestInit) => {
    const res = await fetch(endpoint, options);
    const data = await res.json();
    if (data.ok) return data.stdout || JSON.stringify(data, null, 2);
    if (data.audit === '🟡') return `🟡 授权不足\n${data.message || ''}\n${data.suggestion || ''}`;
    return `❌ 错误: ${data.stderr || data.error || data.message || '未知错误'}`;
  };

  const handleDispatch = async () => {
    if (!task.trim()) return;
    setLoading(true);
    setOutput('');
    try {
      const identity = getIdentity();
      const text = await callApi('/api/dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          task,
          soul_id: identity?.soul_id || '',
          uid: identity?.uid || '',
        }),
      });
      setOutput(text);
      const match = text.match(/#龍芯⚡️[\S]+/);
      if (match) setLastDNA(match[0]);
    } finally {
      setLoading(false);
    }
  };

  const quickAction = async (endpoint: string) => {
    setLoading(true);
    setOutput('');
    try {
      const text = await callApi(endpoint);
      setOutput(text);
    } finally {
      setLoading(false);
    }
  };

  const handleTrace = async () => {
    if (!lastDNA) {
      setOutput('❌ 先执行一次调度，获取 DNA 后再追踪');
      return;
    }
    setLoading(true);
    try {
      const text = await callApi(`/api/trace?dna=${encodeURIComponent(lastDNA)}`);
      setOutput(text);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="h-full flex flex-col bg-zinc-950 text-zinc-100 overflow-hidden">
      {/* 顶部栏 */}
      <div className="h-14 flex items-center justify-between px-6 border-b border-zinc-800/50 bg-zinc-900/30 shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-gradient-to-br from-amber-500/20 to-red-500/20 border border-amber-500/30 flex items-center justify-center">
            <Terminal className="w-4 h-4 text-amber-400" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-zinc-100">龍魂指挥调度</h2>
            <p className="text-[10px] text-zinc-500">本地底座 · 云端补充 · 人格联动 · DNA追溯</p>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <Badge variant="outline" className="text-[10px] border-emerald-500/30 text-emerald-400 bg-emerald-500/10">
            <Shield className="w-3 h-3 mr-1" /> 宪法闸口在线
          </Badge>
          <Badge variant="outline" className="text-[10px] border-sky-500/30 text-sky-400 bg-sky-500/10">
            <Cpu className="w-3 h-3 mr-1" /> 本地优先
          </Badge>
          <code className="text-[10px] text-amber-500/50 font-mono hidden sm:block">
            {generateDNA('COMMANDER', 'UI-ACTIVE')}
          </code>
        </div>
      </div>

      {/* 主内容 */}
      <div className="flex-1 flex overflow-hidden">
        {/* 左侧控制面板 */}
        <div className="w-96 flex flex-col border-r border-zinc-800/50 bg-zinc-900/20 p-4 gap-4 shrink-0">
          <Card className="bg-zinc-900/50 border-zinc-800/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs font-medium text-zinc-300 flex items-center gap-2">
                <Zap className="w-3.5 h-3.5 text-amber-400" />
                任务下发
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Textarea
                placeholder="输入任务描述，例如：用Python写一个快速排序..."
                value={task}
                onChange={(e) => setTask(e.target.value)}
                className="min-h-[120px] bg-zinc-950 border-zinc-800 text-xs text-zinc-100 placeholder:text-zinc-600 resize-none"
              />
              <Button
                onClick={handleDispatch}
                disabled={loading || !task.trim()}
                className="w-full bg-amber-500/10 hover:bg-amber-500/20 text-amber-400 border border-amber-500/30"
              >
                <Play className="w-3.5 h-3.5 mr-1.5" />
                {loading ? '调度中...' : '执行调度'}
              </Button>
            </CardContent>
          </Card>

          <Card className="bg-zinc-900/50 border-zinc-800/50">
            <CardHeader className="pb-2">
              <CardTitle className="text-xs font-medium text-zinc-300 flex items-center gap-2">
                <Activity className="w-3.5 h-3.5 text-emerald-400" />
                监控与追踪
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <Button variant="outline" size="sm" onClick={() => quickAction('/api/status')} className="w-full justify-start text-xs border-zinc-700 text-zinc-300 hover:bg-zinc-800">
                <Activity className="w-3.5 h-3.5 mr-2" /> 系统状态
              </Button>
              <Button variant="outline" size="sm" onClick={() => quickAction('/api/health')} className="w-full justify-start text-xs border-zinc-700 text-zinc-300 hover:bg-zinc-800">
                <Cpu className="w-3.5 h-3.5 mr-2" /> 全链路健康
              </Button>
              <Button variant="outline" size="sm" onClick={() => quickAction('/api/topology')} className="w-full justify-start text-xs border-zinc-700 text-zinc-300 hover:bg-zinc-800">
                <GitBranch className="w-3.5 h-3.5 mr-2" /> 能力拓扑
              </Button>
              <Button variant="outline" size="sm" onClick={() => quickAction('/api/stats')} className="w-full justify-start text-xs border-zinc-700 text-zinc-300 hover:bg-zinc-800">
                <BarChart3 className="w-3.5 h-3.5 mr-2" /> 调用统计
              </Button>
              <Button variant="outline" size="sm" onClick={handleTrace} className="w-full justify-start text-xs border-zinc-700 text-zinc-300 hover:bg-zinc-800">
                <Search className="w-3.5 h-3.5 mr-2" /> 追踪最新DNA
              </Button>
              <Button variant="outline" size="sm" onClick={() => quickAction('/api/audit')} className="w-full justify-start text-xs border-zinc-700 text-zinc-300 hover:bg-zinc-800">
                <ClipboardCheck className="w-3.5 h-3.5 mr-2" /> 自审闭环
              </Button>
            </CardContent>
          </Card>

          {lastDNA && (
            <div className="p-3 rounded border border-amber-500/20 bg-amber-500/5">
              <p className="text-[9px] text-zinc-500 mb-1">最新调度 DNA</p>
              <code className="text-[10px] text-amber-400 font-mono break-all">{lastDNA}</code>
            </div>
          )}
        </div>

        {/* 右侧输出区 */}
        <div className="flex-1 flex flex-col bg-zinc-950">
          <div className="flex items-center justify-between px-4 py-2 border-b border-zinc-800/50 bg-zinc-900/30">
            <span className="text-xs text-zinc-400 flex items-center gap-2">
              <Terminal className="w-3.5 h-3.5" /> 调度输出
            </span>
            {loading && (
              <span className="flex items-center gap-1.5 text-[10px] text-amber-400">
                <span className="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse" />
                执行中...
              </span>
            )}
          </div>
          <div className="flex-1 overflow-auto p-4">
            {output ? (
              <pre className="text-xs text-zinc-300 font-mono whitespace-pre-wrap leading-relaxed">
                {output}
              </pre>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-zinc-600">
                <Terminal className="w-10 h-10 mb-3 opacity-20" />
                <p className="text-xs">等待任务下发...</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
