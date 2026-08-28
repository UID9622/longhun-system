归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂 e-CNY 一元充值页面
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-RECHARGE-v1.0
 */
import { useState } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import {
  Wallet, RefreshCw, Zap, CheckCircle, Clock, AlertCircle,
  History, QrCode, CircleDollarSign
} from "lucide-react";

const statusConfig: Record<string, { color: string; icon: React.ComponentType<{ className?: string }>; label: string }> = {
  initiated: { color: "text-amber-400", icon: Clock, label: "待支付" },
  paid: { color: "text-emerald-400", icon: CheckCircle, label: "已支付" },
  confirmed: { color: "text-blue-400", icon: CheckCircle, label: "已确认" },
  failed: { color: "text-red-400", icon: AlertCircle, label: "失败" },
  refunded: { color: "text-slate-400", icon: RefreshCw, label: "已退款" },
};

export default function Recharge() {
  const utils = trpc.useUtils();
  const [amount, setAmount] = useState("1.00");
  const [billNo, setBillNo] = useState("");

  const { data: records, isLoading } = trpc.payment.rechargeList.useQuery({ limit: 20 });
  const { data: queueStatus } = trpc.payment.queueStatus.useQuery(undefined, {
    refetchInterval: 5000,
  });

  const initiateMutation = trpc.payment.initiateRecharge.useMutation({
    onSuccess: (data) => {
      setBillNo(data.billNo);
      utils.payment.rechargeList.invalidate();
    },
  });

  const simulateMutation = trpc.payment.simulatePay.useMutation({
    onSuccess: () => {
      utils.payment.rechargeList.invalidate();
      setTimeout(() => utils.payment.callbackList.invalidate(), 1000);
    },
  });

  const quickAmounts = ["1.00", "10.00", "50.00", "100.00", "500.00", "1000.00"];

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <CircleDollarSign className="h-5 w-5 text-amber-500" />
            e-CNY 一元充值
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            数字人民币支付 · 无上限充值 · 回调自动激活
          </p>
        </div>

        {/* 充值卡片 */}
        <Card className="bg-slate-900 border-slate-800">
          <CardHeader>
            <CardTitle className="text-sm text-white flex items-center gap-2">
              <Wallet className="h-4 w-4 text-amber-500" />
              发起充值
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* 快捷金额 */}
            <div className="grid grid-cols-3 lg:grid-cols-6 gap-2">
              {quickAmounts.map((a) => (
                <Button
                  key={a}
                  variant={amount === a ? "default" : "outline"}
                  onClick={() => setAmount(a)}
                  className={amount === a
                    ? "bg-amber-600 hover:bg-amber-700 text-white"
                    : "border-slate-700 text-slate-300 hover:bg-slate-800"
                  }
                >
                  ¥{a}
                </Button>
              ))}
            </div>

            {/* 自定义金额 */}
            <div className="flex gap-2">
              <Input
                type="number"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
                placeholder="输入金额"
                className="bg-slate-800 border-slate-700 text-white text-lg"
                min="0.01"
                step="0.01"
              />
              <span className="flex items-center text-slate-400 text-lg">CNY</span>
            </div>

            {/* 操作按钮 */}
            <div className="flex gap-2">
              <Button
                onClick={() => initiateMutation.mutate({ amount, currency: "CNY", paymentMethod: "ecny" })}
                disabled={initiateMutation.isPending}
                className="flex-1 bg-emerald-600 hover:bg-emerald-700"
              >
                <QrCode className="mr-2 h-4 w-4" />
                {initiateMutation.isPending ? "生成中..." : "生成支付码"}
              </Button>
              {billNo && (
                <Button
                  onClick={() => simulateMutation.mutate({ billNo, amount })}
                  disabled={simulateMutation.isPending}
                  variant="outline"
                  className="border-amber-600 text-amber-400 hover:bg-amber-900/20"
                >
                  <Zap className="mr-2 h-4 w-4" />
                  模拟支付
                </Button>
              )}
            </div>

            {/* 生成的账单信息 */}
            {initiateMutation.data && (
              <div className="rounded-lg bg-emerald-950/30 border border-emerald-800 p-3 space-y-2">
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4 text-emerald-400" />
                  <span className="text-sm text-emerald-300">支付码已生成</span>
                </div>
                <div className="space-y-1 text-xs font-mono">
                  <div className="flex justify-between">
                    <span className="text-slate-500">账单号</span>
                    <span className="text-emerald-400">{initiateMutation.data.billNo}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">金额</span>
                    <span className="text-emerald-400">{initiateMutation.data.amount} {initiateMutation.data.currency}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500">DNA</span>
                    <span className="text-amber-400 text-[10px]">{initiateMutation.data.dna}</span>
                  </div>
                </div>
                <p className="text-[10px] text-slate-500">
                  回调地址: <code className="text-emerald-500">POST /api/trpc/payment.webhook</code>
                </p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* 队列状态 */}
        {queueStatus && (
          <Card className="bg-slate-900 border-slate-800">
            <CardContent className="p-3">
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-4">
                  <span className="text-slate-400">
                    队列: <span className="text-amber-400">{queueStatus.pending}</span> 待处理
                  </span>
                  <span className="text-slate-400">
                    并发: <span className="text-blue-400">{queueStatus.activeConsumers}</span>/{queueStatus.processing ? "运行中" : "空闲"}
                  </span>
                  <span className="text-slate-400">
                    已处理: <span className="text-emerald-400">{queueStatus.processedCount}</span>
                  </span>
                </div>
                <RefreshCw className="h-3 w-3 text-slate-600 animate-spin" />
              </div>
            </CardContent>
          </Card>
        )}

        <Separator className="bg-slate-800" />

        {/* 充值记录 */}
        <div>
          <h3 className="text-sm font-semibold text-white flex items-center gap-2 mb-3">
            <History className="h-4 w-4 text-amber-500" />
            充值记录
          </h3>
          <div className="space-y-2">
            {records?.map((r) => {
              const cfg = statusConfig[r.status] ?? statusConfig.initiated;
              const Icon = cfg.icon;
              return (
                <Card key={r.id} className="bg-slate-900 border-slate-800">
                  <CardContent className="p-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <Icon className={`h-4 w-4 ${cfg.color}`} />
                        <div>
                          <div className="flex items-center gap-2">
                            <span className="text-white font-medium">{r.amount} {r.currency}</span>
                            <Badge className="text-[10px] bg-slate-700 text-slate-300">{r.paymentMethod}</Badge>
                          </div>
                          <p className="text-[10px] text-slate-500 font-mono mt-0.5">{r.billNo}</p>
                        </div>
                      </div>
                      <div className="text-right">
                        <span className={`text-xs ${cfg.color}`}>{cfg.label}</span>
                        <p className="text-[10px] text-slate-600">
                          {new Date(r.createdAt).toLocaleDateString()}
                        </p>
                      </div>
                    </div>
                    {r.dnaMarker && (
                      <p className="text-[9px] text-amber-500/50 font-mono mt-1 truncate">{r.dnaMarker}</p>
                    )}
                  </CardContent>
                </Card>
              );
            })}
            {!records?.length && !isLoading && (
              <div className="text-center py-8 text-slate-500">
                <History className="mx-auto h-8 w-8 mb-2 opacity-50" />
                <p className="text-sm">暂无充值记录</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
