归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 右侧面板 · 万年历 + 审计日志 + 系统状态
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v1.0

import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { CalendarDays, Activity, Server, BookOpen } from 'lucide-react';
import type { AuditEntry } from '@/types';
import LonghunCalendar from '@/components/LonghunCalendar';
import AuditLog from '@/components/AuditLog';

interface Props {
  audits: AuditEntry[];
}

export default function RightPanel({ audits }: Props) {
  return (
    <div className="w-80 h-full flex flex-col border-l border-zinc-800/50 bg-zinc-950/80 backdrop-blur-xl">
      <Tabs defaultValue="calendar" className="flex-1 flex flex-col">
        <TabsList className="w-full rounded-none border-b border-zinc-800/50 bg-zinc-950/50 p-0 h-10">
          <TabsTrigger value="calendar" className="flex-1 rounded-none text-xs data-[state=active]:bg-amber-500/10 data-[state=active]:text-amber-400 data-[state=active]:border-b-2 data-[state=active]:border-amber-500">
            <CalendarDays className="w-3.5 h-3.5 mr-1.5" />万年历
          </TabsTrigger>
          <TabsTrigger value="audit" className="flex-1 rounded-none text-xs data-[state=active]:bg-green-500/10 data-[state=active]:text-green-400 data-[state=active]:border-b-2 data-[state=active]:border-green-500">
            <Activity className="w-3.5 h-3.5 mr-1.5" />审计
          </TabsTrigger>
          <TabsTrigger value="system" className="flex-1 rounded-none text-xs data-[state=active]:bg-sky-500/10 data-[state=active]:text-sky-400 data-[state=active]:border-b-2 data-[state=active]:border-sky-500">
            <Server className="w-3.5 h-3.5 mr-1.5" />系统
          </TabsTrigger>
        </TabsList>

        <TabsContent value="calendar" className="flex-1 overflow-y-auto p-3 mt-0 scrollbar-thin">
          <LonghunCalendar />
        </TabsContent>

        <TabsContent value="audit" className="flex-1 overflow-y-auto p-3 mt-0 scrollbar-thin">
          <AuditLog entries={audits} />
        </TabsContent>

        <TabsContent value="system" className="flex-1 overflow-y-auto p-3 mt-0 scrollbar-thin">
          <SystemStatus />
        </TabsContent>
      </Tabs>
    </div>
  );
}

function SystemStatus() {
  const modules = [
    { name: '三层监督器', status: '🟢', desc: '感知/认知/决策三级治理就绪' },
    { name: '三色审计器', status: '🟢', desc: '实时审计追踪，10,000条环形缓冲' },
    { name: 'DNA追溯器', status: '🟢', desc: 'SHA256哈希链，消息级追溯' },
    { name: '端侧加密', status: '🟢', desc: '密钥本地生成，不上传服务器' },
    { name: '君子协议', status: '🟢', desc: 'CC BY-NC-SA 4.0 开源宪章' },
    { name: 'AI真相协议', status: '🟢', desc: '输出真实性验证已激活' },
    { name: '五行决策引擎', status: '🟢', desc: '金木水火土相生相克算法' },
    { name: '通心译协议', status: '🟢', desc: '中英双语注释规范' },
    { name: 'CNSH运行时', status: '🟡', desc: '中文原生脚本 v3.0 调试中' },
    { name: '取证矩阵', status: '🟢', desc: '证据链完整性校验' },
  ];

  return (
    <div className="space-y-3">
      {/* 协议版本 */}
      <div className="p-3 rounded-lg border border-amber-500/15 bg-amber-500/5">
        <div className="flex items-center gap-2 mb-2">
          <BookOpen className="w-4 h-4 text-amber-500" />
          <span className="text-sm font-bold text-amber-400">龍之心语协议</span>
        </div>
        <code className="text-[10px] text-amber-500/70 font-mono block">
          #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v1.0
        </code>
        <p className="text-[10px] text-zinc-500 mt-1">
          加密房间 + 积分驱动 + 可复原审计 + 不监控的社交协议
        </p>
      </div>

      {/* 模块状态 */}
      <div className="space-y-1.5">
        <h4 className="text-xs text-zinc-500 font-medium mb-2">龍魂技能模块</h4>
        {modules.map(mod => (
          <div
            key={mod.name}
            className="flex items-center gap-2 p-2 rounded border border-zinc-800/30 bg-zinc-900/20"
          >
            <span className="text-xs">{mod.status}</span>
            <div className="flex-1 min-w-0">
              <p className="text-[11px] text-zinc-300 truncate">{mod.name}</p>
              <p className="text-[9px] text-zinc-600 truncate">{mod.desc}</p>
            </div>
          </div>
        ))}
      </div>

      {/* 主权声明 */}
      <div className="p-3 rounded-lg border border-red-500/15 bg-red-500/5">
        <p className="text-[10px] text-red-400/80 leading-relaxed">
          数据主权归用户个人所有，龍魂系统仅作为基础设施提供方，不参与内容运营。
          社交平台数据主权归人民。
        </p>
        <code className="text-[9px] text-red-500/50 font-mono block mt-1.5">
          中华人民共和国 · 龍魂系统 · UID9622
        </code>
      </div>
    </div>
  );
}
