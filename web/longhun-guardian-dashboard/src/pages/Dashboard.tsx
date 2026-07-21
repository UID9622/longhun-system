/**
 * 龍魂操作台仪表盘
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-DASHBOARD-v1.0
 */
import { trpc } from "@/providers/trpc";
import { useAuth } from "@/hooks/useAuth";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import {
  Users, Smartphone, FileText, ScrollText, BrainCircuit,
  Shield, Activity, Zap, Lock, Unlock, AlertTriangle, CheckCircle
} from "lucide-react";

function StatCard({
  title, value, icon: Icon, color, subtitle
}: {
  title: string;
  value: string | number;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  subtitle?: string;
}) {
  return (
    <Card className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
      <CardContent className="p-4">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-xs text-slate-400">{title}</p>
            <p className="text-2xl font-bold text-white mt-1">{value}</p>
            {subtitle && <p className="text-[10px] text-slate-500 mt-1">{subtitle}</p>}
          </div>
          <div className={`rounded-lg p-2.5 ${color}`}>
            <Icon className="h-5 w-5 text-white" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

export default function Dashboard() {
  const { user } = useAuth();
  const { data: stats } = trpc.admin.dashboardStats.useQuery(undefined, {
    enabled: user?.role === "admin",
  });

  const severityIcon = (s: string) => {
    if (s === "critical") return <AlertTriangle className="h-3.5 w-3.5 text-red-500" />;
    if (s === "warning") return <AlertTriangle className="h-3.5 w-3.5 text-amber-500" />;
    return <CheckCircle className="h-3.5 w-3.5 text-emerald-500" />;
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h2 className="text-2xl font-bold text-white flex items-center gap-2">
              <Shield className="h-6 w-6 text-amber-500" />
              龍魂操作台
            </h2>
            <p className="text-sm text-slate-400 mt-1">
              国密认证 · 设备管理 · 人格助手 · 审计追踪
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="border-emerald-600 text-emerald-400 bg-emerald-900/20">
              <Activity className="mr-1 h-3 w-3" />
              系统正常
            </Badge>
            <Badge variant="outline" className="border-amber-600 text-amber-400 bg-amber-900/20">
              <Lock className="mr-1 h-3 w-3" />
              SM3/SM4 就绪
            </Badge>
          </div>
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-3">
          <StatCard title="用户" value={stats?.stats.users ?? 0} icon={Users} color="bg-blue-600" />
          <StatCard title="设备" value={stats?.stats.devices ?? 0} icon={Smartphone} color="bg-emerald-600" />
          <StatCard title="内容" value={stats?.stats.contents ?? 0} icon={FileText} color="bg-violet-600" />
          <StatCard title="人格" value={stats?.stats.personas ?? 0} icon={BrainCircuit} color="bg-pink-600" />
          <StatCard title="技能" value={stats?.stats.skills ?? 0} icon={Zap} color="bg-amber-600" />
          <StatCard title="审计" value={stats?.stats.audits ?? 0} icon={ScrollText} color="bg-red-600" />
        </div>

        <Separator className="bg-slate-800" />

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Quick Actions */}
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-semibold text-white flex items-center gap-2">
                <Zap className="h-4 w-4 text-amber-500" />
                快捷操作
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              <QuickActionButton label="生成国密密钥" icon={Lock} onClick={() => {}} />
              <QuickActionButton label="注册设备证书" icon={Smartphone} onClick={() => {}} />
              <QuickActionButton label="添加人格助手" icon={BrainCircuit} onClick={() => {}} />
              <QuickActionButton label="查看审计日志" icon={ScrollText} onClick={() => {}} />
            </CardContent>
          </Card>

          {/* Recent Audit */}
          <Card className="bg-slate-900 border-slate-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-semibold text-white flex items-center gap-2">
                <ScrollText className="h-4 w-4 text-amber-500" />
                最近审计
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {stats?.recentAudits?.length ? (
                  stats.recentAudits.map((log) => (
                    <div
                      key={log.id}
                      className="flex items-center gap-2 rounded-md bg-slate-800/50 p-2 text-xs"
                    >
                      {severityIcon(log.severity)}
                      <div className="flex-1 min-w-0">
                        <p className="text-slate-300 truncate">{log.action}</p>
                        <p className="text-slate-500 truncate">{log.resource}</p>
                      </div>
                      <span className="text-slate-600 text-[10px] whitespace-nowrap">
                        {new Date(log.createdAt).toLocaleDateString()}
                      </span>
                    </div>
                  ))
                ) : (
                  <p className="text-xs text-slate-500 text-center py-4">暂无审计记录</p>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* System Info */}
        <Card className="bg-slate-900 border-slate-800">
          <CardContent className="p-4">
            <div className="flex flex-wrap items-center gap-4 text-xs text-slate-500">
              <span className="flex items-center gap-1">
                <Shield className="h-3.5 w-3.5 text-amber-500" />
                龍魂体系 v5.0
              </span>
              <span>|</span>
              <span>国密: SM3/SM4 纯TS实现</span>
              <span>|</span>
              <span>DNA追溯: 已启用</span>
              <span>|</span>
              <span>三色审计: 已启用</span>
              <span className="ml-auto font-mono text-[10px]">
                #龍芯⚡️2026-07-11-LONGHUN-PANEL-v5.0
              </span>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  );
}

function QuickActionButton({
  label, icon: Icon, onClick
}: {
  label: string;
  icon: React.ComponentType<{ className?: string }>;
  onClick: () => void;
}) {
  return (
    <Button
      variant="ghost"
      onClick={onClick}
      className="w-full justify-start text-slate-300 hover:text-white hover:bg-slate-800 text-sm"
    >
      <Icon className="mr-2 h-4 w-4 text-amber-500" />
      {label}
    </Button>
  );
}
