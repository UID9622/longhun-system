/**
 * 龍魂操作台 - 支付管理后台
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-PAYMENT-MGMT-v1.0
 */
import { useState } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import {
  CreditCard, RefreshCw, AlertTriangle, CheckCircle, Clock,
  RotateCcw, Activity, BarChart3, Filter, Zap
} from "lucide-react";

const cbStatusConfig: Record<string, { color: string; bg: string; label: string }> = {
  pending: { color: "text-amber-400", bg: "bg-amber-600/10", label: "待处理" },
  processing: { color: "text-blue-400", bg: "bg-blue-600/10", label: "处理中" },
  success: { color: "text-emerald-400", bg: "bg-emerald-600/10", label: "成功" },
  failed: { color: "text-red-400", bg: "bg-red-600/10", label: "失败" },
  duplicate: { color: "text-slate-400", bg: "bg-slate-600/10", label: "重复" },
};

export default function PaymentMgmt() {
  const utils = trpc.useUtils();
  const [cbFilter, setCbFilter] = useState("");
  const [searchBillNo, setSearchBillNo] = useState("");

  const { data: callbacks, isLoading: cbLoading } = trpc.payment.callbackList.useQuery(
    { status: cbFilter || undefined, limit: 50 }
  );
  const { data: queueStatus } = trpc.payment.queueStatus.useQuery(undefined, {
    refetchInterval: 3000,
  });
  const { data: queryResult } = trpc.payment.queryStatus.useQuery(
    { billNo: searchBillNo },
    { enabled: searchBillNo.length > 0 }
  );

  const stats = {
    total: callbacks?.length ?? 0,
    success: callbacks?.filter((c) => c.status === "success").length ?? 0,
    failed: callbacks?.filter((c) => c.status === "failed").length ?? 0,
    pending: callbacks?.filter((c) => c.status === "pending" || c.status === "processing").length ?? 0,
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <CreditCard className="h-5 w-5 text-amber-500" />
            支付管理后台
          </h2>
          <Button
            variant="outline"
            size="sm"
            onClick={() => { utils.payment.callbackList.invalidate(); utils.payment.queueStatus.invalidate(); }}
            className="border-slate-700 text-slate-300"
          >
            <RefreshCw className="mr-1 h-3.5 w-3.5" /> 刷新
          </Button>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
          <StatCard title="总回调" value={stats.total} color="bg-blue-600" icon={BarChart3} />
          <StatCard title="成功" value={stats.success} color="bg-emerald-600" icon={CheckCircle} />
          <StatCard title="失败" value={stats.failed} color="bg-red-600" icon={AlertTriangle} />
          <StatCard title="待处理" value={stats.pending} color="bg-amber-600" icon={Clock} />
        </div>

        {/* 队列状态监控 */}
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-white flex items-center gap-2">
              <Activity className="h-4 w-4 text-amber-500" />
              消息队列实时监控
            </CardTitle>
          </CardHeader>
          <CardContent>
            {queueStatus ? (
              <div className="grid grid-cols-4 gap-4 text-center">
                <div>
                  <p className="text-2xl font-bold text-amber-400">{queueStatus.pending}</p>
                  <p className="text-[10px] text-slate-400">队列积压</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-blue-400">{queueStatus.activeConsumers}</p>
                  <p className="text-[10px] text-slate-400">活跃消费者</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-emerald-400">{queueStatus.processedCount}</p>
                  <p className="text-[10px] text-slate-400">已处理总数</p>
                </div>
                <div>
                  <p className="text-2xl font-bold text-purple-400">{queueStatus.processing ? "ON" : "IDLE"}</p>
                  <p className="text-[10px] text-slate-400">处理状态</p>
                </div>
              </div>
            ) : (
              <p className="text-sm text-slate-500 text-center py-4">加载中...</p>
            )}
          </CardContent>
        </Card>

        <Separator className="bg-slate-800" />

        {/* 账单查询 */}
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-white flex items-center gap-2">
              <Zap className="h-4 w-4 text-amber-500" />
              账单状态查询
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            <div className="flex gap-2">
              <Input
                placeholder="输入账单号查询..."
                value={searchBillNo}
                onChange={(e) => setSearchBillNo(e.target.value)}
                className="bg-slate-800 border-slate-700 text-white font-mono text-sm"
              />
            </div>
            {queryResult && (
              <div className="rounded-lg bg-slate-800/50 p-3 space-y-2 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400">账单号</span>
                  <span className="text-white font-mono">{queryResult.billNo}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">回调状态</span>
                  {queryResult.callback ? (
                    <Badge className={`${cbStatusConfig[queryResult.callback.status]?.bg} ${cbStatusConfig[queryResult.callback.status]?.color} text-[10px]`}>
                      {queryResult.callback.status}
                    </Badge>
                  ) : (
                    <span className="text-slate-500">无回调记录</span>
                  )}
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">充值状态</span>
                  {queryResult.recharge ? (
                    <Badge className="bg-emerald-600/10 text-emerald-400 text-[10px]">{queryResult.recharge.status}</Badge>
                  ) : (
                    <span className="text-slate-500">无充值记录</span>
                  )}
                </div>
              </div>
            )}
          </CardContent>
        </Card>

        {/* 回调记录 */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-sm font-semibold text-white flex items-center gap-2">
              <RotateCcw className="h-4 w-4 text-amber-500" />
              回调记录
            </h3>
            <div className="flex gap-2">
              <Filter className="h-4 w-4 text-slate-500" />
              <Select value={cbFilter} onValueChange={setCbFilter}>
                <SelectTrigger className="w-28 h-7 bg-slate-800 border-slate-700 text-xs text-white">
                  <SelectValue placeholder="筛选" />
                </SelectTrigger>
                <SelectContent className="bg-slate-800 border-slate-700">
                  <SelectItem value="">全部</SelectItem>
                  <SelectItem value="success">成功</SelectItem>
                  <SelectItem value="failed">失败</SelectItem>
                  <SelectItem value="pending">待处理</SelectItem>
                  <SelectItem value="duplicate">重复</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          <div className="rounded-lg border border-slate-800 overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-slate-800/50 text-slate-400 text-xs">
                <tr>
                  <th className="px-3 py-2 text-left">ID</th>
                  <th className="px-3 py-2 text-left">账单号</th>
                  <th className="px-3 py-2 text-left">金额</th>
                  <th className="px-3 py-2 text-left">状态</th>
                  <th className="px-3 py-2 text-left">重试</th>
                  <th className="px-3 py-2 text-left">DNA</th>
                  <th className="px-3 py-2 text-left">时间</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800">
                {callbacks?.map((cb) => {
                  const cfg = cbStatusConfig[cb.status] ?? cbStatusConfig.pending;
                  return (
                    <tr key={cb.id} className="hover:bg-slate-800/30">
                      <td className="px-3 py-2 text-slate-500 text-xs">{cb.id}</td>
                      <td className="px-3 py-2 text-white font-mono text-xs">{cb.billNo}</td>
                      <td className="px-3 py-2 text-white text-xs">{cb.amount} {cb.currency}</td>
                      <td className="px-3 py-2">
                        <Badge className={`${cfg.bg} ${cfg.color} text-[10px]`}>
                          {cfg.label}
                        </Badge>
                      </td>
                      <td className="px-3 py-2 text-slate-400 text-xs">{cb.retryCount}</td>
                      <td className="px-3 py-2">
                        {cb.dnaMarker ? (
                          <span className="text-[9px] text-amber-400 font-mono truncate">{cb.dnaMarker.slice(0, 16)}...</span>
                        ) : (
                          <span className="text-slate-600">-</span>
                        )}
                      </td>
                      <td className="px-3 py-2 text-slate-500 text-[10px]">
                        {new Date(cb.createdAt).toLocaleString()}
                      </td>
                    </tr>
                  );
                })}
                {!callbacks?.length && !cbLoading && (
                  <tr>
                    <td colSpan={7} className="px-3 py-8 text-center text-slate-500">
                      暂无回调记录
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

function StatCard({ title, value, icon: Icon, color }: {
  title: string; value: number; icon: React.ComponentType<{ className?: string }>; color: string;
}) {
  return (
    <Card className="bg-slate-900 border-slate-800">
      <CardContent className="p-3">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-[10px] text-slate-400">{title}</p>
            <p className="text-xl font-bold text-white mt-0.5">{value}</p>
          </div>
          <div className={`rounded-lg p-2 ${color}`}>
            <Icon className="h-4 w-4 text-white" />
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
