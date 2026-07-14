/**
 * 龍魂操作台 - 审计日志
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-AUDIT-LOG-v1.0
 */
import { useState } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { ScrollText, AlertTriangle, CheckCircle, InfoIcon, Filter } from "lucide-react";

const severityConfig = {
  critical: { color: "text-red-400", bg: "bg-red-600/10 border-red-800", icon: AlertTriangle },
  warning: { color: "text-amber-400", bg: "bg-amber-600/10 border-amber-800", icon: AlertTriangle },
  info: { color: "text-emerald-400", bg: "bg-emerald-600/10 border-emerald-800", icon: CheckCircle },
};

export default function AuditLog() {
  const [severity, setSeverity] = useState<string>("");
  const [limit, setLimit] = useState<string>("100");

  const { data: logs, isLoading } = trpc.admin.auditList.useQuery(
    { severity: severity || undefined, limit: parseInt(limit) },
  );

  const stats = {
    critical: logs?.filter((l) => l.severity === "critical").length ?? 0,
    warning: logs?.filter((l) => l.severity === "warning").length ?? 0,
    info: logs?.filter((l) => l.severity === "info").length ?? 0,
  };

  return (
    <DashboardLayout>
      <div className="space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <ScrollText className="h-5 w-5 text-amber-500" />
            审计日志
          </h2>
          <div className="flex gap-2">
            <Select value={severity} onValueChange={setSeverity}>
              <SelectTrigger className="w-36 bg-slate-900 border-slate-700 text-white">
                <Filter className="mr-1 h-3.5 w-3.5" />
                <SelectValue placeholder="严重级别" />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="">全部</SelectItem>
                <SelectItem value="critical">
                  <span className="flex items-center gap-2"><AlertTriangle className="h-3 w-3 text-red-400" />严重</span>
                </SelectItem>
                <SelectItem value="warning">
                  <span className="flex items-center gap-2"><AlertTriangle className="h-3 w-3 text-amber-400" />警告</span>
                </SelectItem>
                <SelectItem value="info">
                  <span className="flex items-center gap-2"><CheckCircle className="h-3 w-3 text-emerald-400" />信息</span>
                </SelectItem>
              </SelectContent>
            </Select>
            <Select value={limit} onValueChange={setLimit}>
              <SelectTrigger className="w-28 bg-slate-900 border-slate-700 text-white">
                <SelectValue />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="50">50条</SelectItem>
                <SelectItem value="100">100条</SelectItem>
                <SelectItem value="200">200条</SelectItem>
                <SelectItem value="500">500条</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-3">
          <Card className="bg-red-950/30 border-red-900">
            <CardContent className="p-3 flex items-center justify-between">
              <div>
                <p className="text-[10px] text-red-400">严重</p>
                <p className="text-xl font-bold text-red-300">{stats.critical}</p>
              </div>
              <AlertTriangle className="h-5 w-5 text-red-500" />
            </CardContent>
          </Card>
          <Card className="bg-amber-950/30 border-amber-900">
            <CardContent className="p-3 flex items-center justify-between">
              <div>
                <p className="text-[10px] text-amber-400">警告</p>
                <p className="text-xl font-bold text-amber-300">{stats.warning}</p>
              </div>
              <AlertTriangle className="h-5 w-5 text-amber-500" />
            </CardContent>
          </Card>
          <Card className="bg-emerald-950/30 border-emerald-900">
            <CardContent className="p-3 flex items-center justify-between">
              <div>
                <p className="text-[10px] text-emerald-400">信息</p>
                <p className="text-xl font-bold text-emerald-300">{stats.info}</p>
              </div>
              <CheckCircle className="h-5 w-5 text-emerald-500" />
            </CardContent>
          </Card>
        </div>

        {/* Log List */}
        <div className="space-y-2 max-h-[60vh] overflow-y-auto pr-1">
          {logs?.map((log) => {
            const cfg = severityConfig[log.severity as keyof typeof severityConfig] ?? severityConfig.info;
            const Icon = cfg.icon;
            return (
              <Card key={log.id} className={`${cfg.bg} border`}>
                <CardContent className="p-3">
                  <div className="flex items-start gap-3">
                    <Icon className={`h-4 w-4 mt-0.5 ${cfg.color}`} />
                    <div className="flex-1 min-w-0 space-y-1">
                      <div className="flex items-center gap-2 flex-wrap">
                        <span className="text-sm font-medium text-white">{log.action}</span>
                        <Badge className={`${log.severity === "critical" ? "bg-red-600" : log.severity === "warning" ? "bg-amber-600" : "bg-emerald-600"} text-white text-[10px]`}>
                          {log.severity}
                        </Badge>
                        {log.method && (
                          <Badge variant="outline" className="border-slate-600 text-slate-400 text-[10px]">
                            {log.method}
                          </Badge>
                        )}
                      </div>
                      {log.resource && (
                        <p className="text-xs text-slate-400">资源: {log.resource}</p>
                      )}
                      {log.ipAddress && (
                        <p className="text-xs text-slate-500 font-mono">IP: {log.ipAddress}</p>
                      )}
                      {log.dnaMarker && (
                        <p className="text-[10px] text-amber-400 font-mono truncate">{log.dnaMarker}</p>
                      )}
                    </div>
                    <span className="text-[10px] text-slate-500 whitespace-nowrap">
                      {new Date(log.createdAt).toLocaleString()}
                    </span>
                  </div>
                </CardContent>
              </Card>
            );
          })}
          {!logs?.length && !isLoading && (
            <div className="text-center py-12 text-slate-500">
              <ScrollText className="mx-auto h-10 w-10 mb-2 opacity-50" />
              <p>暂无审计日志</p>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
