归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂守护面板 · 红蓝对抗
 * DNA: #龍芯⚡️2026-07-12-LONGHUN-GUARDIAN-PANEL-v1.0
 * 自动化扫描 → 修复 → 审计 流水线
 */
import { useState } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  Shield, ShieldAlert, ShieldCheck, Sword, Wrench, Play, RefreshCw,
  Clock, AlertTriangle, CheckCircle, XCircle, Info, Zap,
  Activity, BarChart3, FileSearch, List, RotateCcw, Crosshair,
  Bug, Lock, Code, Cog, HeartPulse, ChevronDown, ChevronUp,
  Dna, Flame, Eye, EyeOff
} from "lucide-react";

const scanTypeConfig: Record<string, { label: string; icon: any; color: string }> = {
  dna_compliance: { label: "DNA合规", icon: Dna, color: "text-amber-400" },
  code_quality: { label: "代码质量", icon: Code, color: "text-blue-400" },
  security_vuln: { label: "安全漏洞", icon: Lock, color: "text-red-400" },
  config_audit: { label: "配置审计", icon: Cog, color: "text-purple-400" },
  supervisor_check: { label: "三监督检查", icon: Eye, color: "text-cyan-400" },
  system_health: { label: "系统健康", icon: HeartPulse, color: "text-emerald-400" },
};

function ScoreRing({ score, size = 80 }: { score: number; size?: number }) {
  const radius = (size - 8) / 2;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;
  const color = score >= 80 ? "#10b981" : score >= 50 ? "#f59e0b" : "#ef4444";

  return (
    <div className="relative inline-flex items-center justify-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle cx={size / 2} cy={size / 2} r={radius} fill="none" stroke="#1e293b" strokeWidth="6" />
        <circle
          cx={size / 2} cy={size / 2} r={radius} fill="none" stroke={color} strokeWidth="6"
          strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round"
          className="transition-all duration-1000"
        />
      </svg>
      <span className="absolute text-lg font-bold" style={{ color }}>{score}</span>
    </div>
  );
}

function FindingCard({ finding, index }: { finding: any; index: number }) {
  const [expanded, setExpanded] = useState(false);
  const severityColors: Record<string, string> = {
    critical: "border-red-500/30 bg-red-500/10",
    warning: "border-amber-500/30 bg-amber-500/10",
    info: "border-blue-500/30 bg-blue-500/10",
  };

  return (
    <div className={`rounded-lg border ${severityColors[finding.severity] || severityColors.info} p-3`}>
      <div className="flex items-start gap-2">
        {finding.severity === "critical" ? <XCircle className="h-4 w-4 text-red-400 shrink-0 mt-0.5" /> :
         finding.severity === "warning" ? <AlertTriangle className="h-4 w-4 text-amber-400 shrink-0 mt-0.5" /> :
         <Info className="h-4 w-4 text-blue-400 shrink-0 mt-0.5" />}
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-slate-200">{finding.issue}</p>
          <p className="text-xs text-slate-500 mt-1">{finding.location}</p>
          <Button
            variant="ghost" size="sm"
            onClick={() => setExpanded(!expanded)}
            className="h-5 text-[10px] text-slate-400 hover:text-white mt-1 p-0"
          >
            {expanded ? <ChevronUp className="h-3 w-3 mr-1" /> : <ChevronDown className="h-3 w-3 mr-1" />}
            {expanded ? "收起" : "详情"}
          </Button>
          {expanded && (
            <div className="mt-2 p-2 rounded bg-slate-900/50 space-y-1">
              <p className="text-xs text-slate-400">证据: {finding.evidence}</p>
              <p className="text-xs text-emerald-400">建议: {finding.suggestion}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default function Guardian() {
  const [running, setRunning] = useState(false);
  const [lastResult, setLastResult] = useState<any>(null);

  const utils = trpc.useUtils();
  const { data: dashboard } = trpc.guardian.dashboard.useQuery();
  const { data: scanHistory } = trpc.guardian.scanHistory.useQuery({ limit: 20 });
  const { data: remediationList } = trpc.guardian.remediationList.useQuery({ limit: 20 });
  const { data: pipelineHistory } = trpc.guardian.pipelineHistory.useQuery({ limit: 10 });

  const runPipeline = trpc.guardian.runPipeline.useMutation({
    onMutate: () => setRunning(true),
    onSuccess: (data) => {
      setLastResult(data);
      setRunning(false);
      utils.guardian.dashboard.invalidate();
      utils.guardian.scanHistory.invalidate();
      utils.guardian.remediationList.invalidate();
      utils.guardian.pipelineHistory.invalidate();
    },
    onError: () => setRunning(false),
  });

  const runScan = trpc.guardian.scan.useMutation({
    onSuccess: () => {
      utils.guardian.dashboard.invalidate();
      utils.guardian.scanHistory.invalidate();
    },
  });

  const verifyFix = trpc.guardian.verifyFix.useMutation({
    onSuccess: () => utils.guardian.remediationList.invalidate(),
  });

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <Shield className="h-6 w-6 text-red-500" />
              龍魂守护
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              红蓝对抗 · 自动化扫描修复 · 全链路审计
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="border-red-500/30 text-red-400 text-xs">
              <Sword className="h-3 w-3 mr-1" />
              红队扫描
            </Badge>
            <Badge variant="outline" className="border-blue-500/30 text-blue-400 text-xs">
              <Wrench className="h-3 w-3 mr-1" />
              蓝队修复
            </Badge>
          </div>
        </div>

        {/* Stats Cards */}
        {dashboard && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">总扫描</div>
              <div className="text-2xl font-bold text-white">{dashboard.stats.totalScans}</div>
            </div>
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">流水线</div>
              <div className="text-2xl font-bold text-amber-400">{dashboard.stats.totalPipelines}</div>
            </div>
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">平均得分</div>
              <div className="text-2xl font-bold text-emerald-400">{dashboard.stats.avgScore}</div>
            </div>
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">自动修复</div>
              <div className="text-2xl font-bold text-blue-400">{dashboard.stats.autoFixed}</div>
            </div>
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">需人工</div>
              <div className="text-2xl font-bold text-amber-400">{dashboard.stats.manualRequired}</div>
            </div>
          </div>
        )}

        {/* Control Panel */}
        <div className="rounded-xl border border-slate-700 bg-slate-800/30 p-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-semibold text-white flex items-center gap-2">
              <Crosshair className="h-5 w-5 text-red-500" />
              红队控制台
            </h2>
            <Button
              onClick={() => runPipeline.mutate({ trigger: "manual" })}
              disabled={running}
              className="bg-red-600 hover:bg-red-700 text-white"
            >
              {running ? <RefreshCw className="h-4 w-4 mr-2 animate-spin" /> : <Play className="h-4 w-4 mr-2" />}
              {running ? "流水线执行中..." : "执行完整守护流水线"}
            </Button>
          </div>

          {/* 快速扫描 */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-2">
            {Object.entries(scanTypeConfig).map(([key, config]) => {
              const Icon = config.icon;
              return (
                <Button
                  key={key}
                  variant="outline"
                  onClick={() => runScan.mutate({ scanType: key as any })}
                  disabled={runScan.isPending}
                  className="border-slate-600 text-slate-300 hover:bg-slate-700 hover:text-white text-xs h-auto py-2 flex flex-col items-center gap-1"
                >
                  <Icon className={`h-4 w-4 ${config.color}`} />
                  <span>{config.label}</span>
                </Button>
              );
            })}
          </div>
        </div>

        {/* 流水线执行结果 */}
        {running && (
          <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-6 text-center">
            <RefreshCw className="h-8 w-8 animate-spin text-amber-500 mx-auto" />
            <p className="mt-2 text-sm text-amber-400">红队扫描中 → 蓝队修复 → 审计报告...</p>
            <div className="flex justify-center gap-4 mt-3 text-xs text-slate-500">
              <span className="flex items-center gap-1"><Sword className="h-3 w-3 text-red-400" /> 6项红队扫描</span>
              <span className="flex items-center gap-1"><Wrench className="h-3 w-3 text-blue-400" /> 自动修复</span>
              <span className="flex items-center gap-1"><ShieldCheck className="h-3 w-3 text-emerald-400" /> 审计归档</span>
            </div>
          </div>
        )}

        {lastResult && !running && (
          <div className="rounded-lg border border-emerald-500/30 bg-emerald-500/5 p-4 space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
                <ShieldCheck className="h-4 w-4" />
                流水线执行完成
              </h3>
              <Badge className={`text-xs ${
                lastResult.summary.triColor === "🟢" ? "bg-emerald-500/20 text-emerald-400" :
                lastResult.summary.triColor === "🟡" ? "bg-amber-500/20 text-amber-400" :
                "bg-red-500/20 text-red-400"
              }`}>
                {lastResult.summary.triColor} 综合评分 {lastResult.summary.avgScore}
              </Badge>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-2 text-xs">
              <div className="rounded bg-slate-900/50 p-2">
                <span className="text-slate-400">扫描项</span>
                <div className="text-white font-bold">{lastResult.summary.totalScans}</div>
              </div>
              <div className="rounded bg-slate-900/50 p-2">
                <span className="text-slate-400">发现问题</span>
                <div className="text-red-400 font-bold">{lastResult.summary.issuesFound}</div>
              </div>
              <div className="rounded bg-slate-900/50 p-2">
                <span className="text-slate-400">自动修复</span>
                <div className="text-blue-400 font-bold">{lastResult.summary.autoFixed}</div>
              </div>
              <div className="rounded bg-slate-900/50 p-2">
                <span className="text-slate-400">需人工</span>
                <div className="text-amber-400 font-bold">{lastResult.summary.manualRequired}</div>
              </div>
            </div>
            {lastResult.dna && (
              <code className="text-[10px] text-amber-400/70 font-mono block">{lastResult.dna}</code>
            )}
          </div>
        )}

        <Separator className="bg-slate-700" />

        {/* Tabs */}
        <Tabs defaultValue="scans" className="w-full">
          <TabsList className="bg-slate-800 border border-slate-700">
            <TabsTrigger value="scans" className="data-[state=active]:bg-red-600 data-[state=active]:text-white text-xs">
              <Sword className="h-3 w-3 mr-1" />
              红队扫描
            </TabsTrigger>
            <TabsTrigger value="remediations" className="data-[state=active]:bg-blue-600 data-[state=active]:text-white text-xs">
              <Wrench className="h-3 w-3 mr-1" />
              蓝队修复
            </TabsTrigger>
            <TabsTrigger value="pipelines" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white text-xs">
              <Zap className="h-3 w-3 mr-1" />
              流水线
            </TabsTrigger>
          </TabsList>

          {/* 红队扫描记录 */}
          <TabsContent value="scans" className="mt-4 space-y-3">
            {scanHistory && scanHistory.length > 0 ? scanHistory.map((scan: any) => (
              <div key={scan.id} className="rounded-lg border border-slate-700 bg-slate-800/30 p-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <ScoreRing score={scan.score ?? 100} size={40} />
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-slate-200">{scan.scanName}</span>
                        <Badge className={`text-[10px] ${
                          scan.severity === "critical" ? "bg-red-500/20 text-red-400 border-red-500/30" :
                          scan.severity === "warning" ? "bg-amber-500/20 text-amber-400 border-amber-500/30" :
                          "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
                        }`}>
                          {scan.severity === "critical" ? "🔴 严重" : scan.severity === "warning" ? "🟡 警告" : "🟢 正常"}
                        </Badge>
                      </div>
                      <div className="text-[10px] text-slate-500 flex gap-2">
                        <span>{scan.targetModule}</span>
                        <span>·</span>
                        <span>{scan.executionMs}ms</span>
                        <span>·</span>
                        <span>{new Date(scan.createdAt).toLocaleString("zh-CN")}</span>
                      </div>
                    </div>
                  </div>
                  <Badge variant="outline" className="text-[10px] border-slate-600">
                    {Array.isArray(scan.findings) ? scan.findings.length : 0} 个问题
                  </Badge>
                </div>
                {/* 发现的问题列表 */}
                {Array.isArray(scan.findings) && scan.findings.length > 0 && (
                  <div className="mt-3 space-y-2">
                    {(scan.findings as any[]).slice(0, 3).map((f, i) => (
                      <FindingCard key={i} finding={f} index={i} />
                    ))}
                    {scan.findings.length > 3 && (
                      <p className="text-xs text-slate-500 text-center">+{scan.findings.length - 3} 更多问题</p>
                    )}
                  </div>
                )}
              </div>
            )) : (
              <div className="text-center py-8 text-slate-500 rounded-lg border border-dashed border-slate-700">
                <Sword className="h-8 w-8 mx-auto mb-2 text-slate-600" />
                暂无扫描记录，点击上方扫描按钮开始
              </div>
            )}
          </TabsContent>

          {/* 蓝队修复记录 */}
          <TabsContent value="remediations" className="mt-4 space-y-3">
            {remediationList && remediationList.length > 0 ? remediationList.map((rem: any) => (
              <div key={rem.id} className="rounded-lg border border-slate-700 bg-slate-800/30 p-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    {rem.remediationType === "auto_fixed" ? (
                      <CheckCircle className="h-4 w-4 text-blue-400" />
                    ) : rem.remediationType === "false_positive" ? (
                      <EyeOff className="h-4 w-4 text-slate-400" />
                    ) : (
                      <Wrench className="h-4 w-4 text-amber-400" />
                    )}
                    <div>
                      <p className="text-sm text-slate-200 line-clamp-1">{rem.issue}</p>
                      <div className="flex items-center gap-2 text-[10px] text-slate-500">
                        <Badge variant="outline" className="text-[10px] border-slate-600">
                          {rem.remediationType === "auto_fixed" ? "🤖 自动" :
                           rem.remediationType === "manual_fix" ? "👤 人工" :
                           rem.remediationType === "false_positive" ? "❌ 误报" : "⏭️ 跳过"}
                        </Badge>
                        <span>{new Date(rem.createdAt).toLocaleString("zh-CN")}</span>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {rem.verified ? (
                      <Badge className="bg-emerald-500/20 text-emerald-400 text-[10px]">✓ 已验证</Badge>
                    ) : (
                      <div className="flex gap-1">
                        <Button
                          variant="ghost" size="sm"
                          onClick={() => verifyFix.mutate({ remediationId: rem.id, verified: true })}
                          className="h-6 text-[10px] text-emerald-400 hover:text-emerald-300 hover:bg-emerald-900/20"
                        >
                          <CheckCircle className="h-3 w-3 mr-1" />
                          通过
                        </Button>
                        <Button
                          variant="ghost" size="sm"
                          onClick={() => verifyFix.mutate({ remediationId: rem.id, verified: false })}
                          className="h-6 text-[10px] text-red-400 hover:text-red-300 hover:bg-red-900/20"
                        >
                          <XCircle className="h-3 w-3 mr-1" />
                          失败
                        </Button>
                      </div>
                    )}
                  </div>
                </div>
                <p className="text-xs text-slate-400 mt-2 pl-6">{rem.actionTaken}</p>
              </div>
            )) : (
              <div className="text-center py-8 text-slate-500 rounded-lg border border-dashed border-slate-700">
                <Wrench className="h-8 w-8 mx-auto mb-2 text-slate-600" />
                暂无修复记录
              </div>
            )}
          </TabsContent>

          {/* 流水线历史 */}
          <TabsContent value="pipelines" className="mt-4 space-y-3">
            {pipelineHistory && pipelineHistory.length > 0 ? pipelineHistory.map((pipe: any) => (
              <div key={pipe.id} className="rounded-lg border border-slate-700 bg-slate-800/30 p-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <Zap className={`h-4 w-4 ${
                      pipe.status === "completed" ? "text-emerald-400" :
                      pipe.status === "running" ? "text-amber-400 animate-pulse" :
                      "text-red-400"
                    }`} />
                    <div>
                      <p className="text-sm font-medium text-slate-200">{pipe.runName}</p>
                      <div className="text-[10px] text-slate-500 flex gap-2">
                        <span>触发: {pipe.triggeredBy}</span>
                        <span>·</span>
                        <span>{new Date(pipe.createdAt).toLocaleString("zh-CN")}</span>
                      </div>
                    </div>
                  </div>
                  <Badge className={`text-[10px] ${
                    pipe.status === "completed" ? "bg-emerald-500/20 text-emerald-400" :
                    pipe.status === "running" ? "bg-amber-500/20 text-amber-400" :
                    pipe.status === "partial" ? "bg-amber-500/20 text-amber-400" :
                    "bg-red-500/20 text-red-400"
                  }`}>
                    {pipe.status === "completed" ? "✅ 完成" :
                     pipe.status === "running" ? "⏳ 执行中" :
                     pipe.status === "partial" ? "⚠️ 部分完成" : "❌ 失败"}
                  </Badge>
                </div>
                {pipe.summary && (
                  <div className="grid grid-cols-4 gap-2 mt-2 text-xs">
                    <div className="text-slate-400">扫描 <span className="text-white">{pipe.summary.totalScans ?? 0}</span></div>
                    <div className="text-slate-400">问题 <span className="text-red-400">{pipe.summary.issuesFound ?? 0}</span></div>
                    <div className="text-slate-400">修复 <span className="text-blue-400">{pipe.summary.autoFixed ?? 0}</span></div>
                    <div className="text-slate-400">评分 <span className="text-amber-400">{pipe.summary.avgScore ?? 100}</span></div>
                  </div>
                )}
                {pipe.stages && Array.isArray(pipe.stages) && (
                  <div className="flex gap-1 mt-2">
                    {(pipe.stages as any[]).map((s, i) => (
                      <div
                        key={i}
                        className={`h-1.5 flex-1 rounded-full ${
                          s.status === "completed" ? "bg-emerald-500" :
                          s.status === "running" ? "bg-amber-500 animate-pulse" :
                          s.status === "failed" ? "bg-red-500" : "bg-slate-700"
                        }`}
                        title={s.stage}
                      />
                    ))}
                  </div>
                )}
              </div>
            )) : (
              <div className="text-center py-8 text-slate-500 rounded-lg border border-dashed border-slate-700">
                <Zap className="h-8 w-8 mx-auto mb-2 text-slate-600" />
                暂无流水线记录
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
