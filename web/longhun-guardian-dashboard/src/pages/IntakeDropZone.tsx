/**
 * 龍魂容器收入口 · Drop Zone
 * DNA: #龍芯⚡️2026-07-12-LONGHUN-INTAKE-DROPZONE-v1.0
 * 统一数据入口 → 粘贴 → 六维评估 → DNA盖章 → 五桶分拣
 */
import { useState, useRef } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  ClipboardPaste, Sparkles, Database, Trash2, Archive,
  Flame, AlertTriangle, CheckCircle, XCircle, Clock,
  ScrollText, BarChart3, Dna, Beaker, Box, Zap, RefreshCw,
  ChevronDown, ChevronUp, Filter, Search
} from "lucide-react";

interface DropResult {
  id: number;
  dna: string;
  stamp: string;
  ganzhi: string;
  eval6: {
    权重层级: string;
    五行归属: string;
    三色审计: string;
    贡献值: number;
    热度状态: string;
    去向判定: string;
  };
  bucket: string;
  status: string;
}

function Eval6Card({ eval6, dna, ganzhi }: { eval6: DropResult["eval6"]; dna: string; ganzhi: string }) {
  const [expanded, setExpanded] = useState(false);
  const colorMap: Record<string, string> = {
    "🟢": "bg-emerald-500/20 text-emerald-400 border-emerald-500/30",
    "🟡": "bg-amber-500/20 text-amber-400 border-amber-500/30",
    "🔴": "bg-red-500/20 text-red-400 border-red-500/30",
  };
  const auditColor = colorMap[eval6.三色审计] ?? colorMap["🟢"];

  return (
    <div className="rounded-lg border border-slate-700 bg-slate-800/50 overflow-hidden">
      <div className="p-3 space-y-2">
        {/* DNA Stamp */}
        <div className="flex items-center gap-2">
          <Dna className="h-4 w-4 text-amber-500 shrink-0" />
          <code className="text-xs text-amber-400 font-mono break-all">{dna}</code>
        </div>
        {/* 四柱 */}
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <ScrollText className="h-3.5 w-3.5 text-slate-500" />
          <span>{ganzhi}</span>
        </div>
        {/* 三色审计 badge */}
        <div className="flex flex-wrap gap-2">
          <Badge className={`${auditColor} text-xs`}>
            {eval6.三色审计} 审计
          </Badge>
          <Badge variant="outline" className="text-xs border-slate-600 text-slate-300">
            {eval6.权重层级}
          </Badge>
          <Badge variant="outline" className="text-xs border-slate-600 text-slate-300">
            五行·{eval6.五行归属}
          </Badge>
          <Badge variant="outline" className="text-xs border-slate-600 text-slate-300">
            贡献值 {eval6.贡献值}/10
          </Badge>
        </div>
        {/* 展开详情 */}
        <Button
          variant="ghost"
          size="sm"
          onClick={() => setExpanded(!expanded)}
          className="h-6 text-[10px] text-slate-400 hover:text-white"
        >
          {expanded ? <ChevronUp className="h-3 w-3 mr-1" /> : <ChevronDown className="h-3 w-3 mr-1" />}
          {expanded ? "收起" : "展开六维详情"}
        </Button>
        {expanded && (
          <div className="grid grid-cols-2 gap-2 text-xs mt-2 p-2 rounded bg-slate-900/50">
            <div className="text-slate-400">权重层级</div>
            <div className="text-slate-200">{eval6.权重层级}</div>
            <div className="text-slate-400">五行归属</div>
            <div className="text-slate-200">{eval6.五行归属}</div>
            <div className="text-slate-400">三色审计</div>
            <div className="text-slate-200">{eval6.三色审计}</div>
            <div className="text-slate-400">贡献值</div>
            <div className="text-slate-200">{eval6.贡献值}/10</div>
            <div className="text-slate-400">热度状态</div>
            <div className="text-slate-200">{eval6.热度状态}</div>
            <div className="text-slate-400">去向判定</div>
            <div className="text-slate-200 font-medium">{eval6.去向判定}</div>
          </div>
        )}
      </div>
    </div>
  );
}

export default function IntakeDropZone() {
  const [content, setContent] = useState("");
  const [dropResult, setDropResult] = useState<DropResult | null>(null);
  const [batchMode, setBatchMode] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const utils = trpc.useUtils();

  const { data: stats } = trpc.intake.stats.useQuery();
  const { data: entries, isLoading: entriesLoading } = trpc.intake.list.useQuery({ limit: 50 });
  const { data: dnaList } = trpc.intake.dnaList.useQuery({ limit: 20 });

  const dropMutation = trpc.intake.drop.useMutation({
    onSuccess: (data) => {
      setDropResult(data as DropResult);
      setContent("");
      utils.intake.list.invalidate();
      utils.intake.stats.invalidate();
      utils.intake.dnaList.invalidate();
    },
  });

  const freezeMutation = trpc.intake.freeze.useMutation({
    onSuccess: () => {
      utils.intake.list.invalidate();
      utils.intake.stats.invalidate();
    },
  });

  const handleDrop = () => {
    if (!content.trim()) return;
    if (batchMode) {
      // 批量模式：每行一条
      const lines = content.split("\n").filter((l) => l.trim());
      dropMutation.mutate({
        content: lines.join("\n---BATCH---\n"),
        contentType: "mixed",
        source: "batch",
      });
    } else {
      dropMutation.mutate({
        content: content.trim(),
        contentType: detectContentType(content),
        source: "manual",
      });
    }
  };

  const handlePaste = async () => {
    try {
      const text = await navigator.clipboard.readText();
      setContent((prev) => prev + text);
    } catch {
      // 降级：让用户手动粘贴
      textareaRef.current?.focus();
    }
  };

  function detectContentType(text: string): "text" | "code" | "link" | "mixed" {
    const hasCode = text.includes("```") || text.includes("function ") || text.includes("class ");
    const hasLink = /^https?:\/\//.test(text.trim());
    const hasCodeBlock = text.includes("{") && text.includes("}");
    if (hasLink && !hasCode) return "link";
    if (hasCode || hasCodeBlock) return "code";
    if (hasCode && hasLink) return "mixed";
    return "text";
  }

  const bucketIcon = (bucket: string) => {
    switch (bucket) {
      case "log": return <CheckCircle className="h-3.5 w-3.5 text-emerald-400" />;
      case "storage": return <Box className="h-3.5 w-3.5 text-blue-400" />;
      case "internal": return <Zap className="h-3.5 w-3.5 text-amber-400" />;
      case "iter_pool": return <RefreshCw className="h-3.5 w-3.5 text-cyan-400" />;
      case "archive": return <Archive className="h-3.5 w-3.5 text-slate-400" />;
      case "fused": return <XCircle className="h-3.5 w-3.5 text-red-400" />;
      default: return <Box className="h-3.5 w-3.5 text-slate-400" />;
    }
  };

  const bucketLabel = (bucket: string) => {
    switch (bucket) {
      case "log": return "🟢 推草日志";
      case "storage": return "📦 入库";
      case "internal": return "⚡ 内部消化";
      case "iter_pool": return "🔁 待迭代池";
      case "archive": return "💤 归档";
      case "fused": return "🔴 熔断";
      default: return bucket;
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white flex items-center gap-2">
              <Beaker className="h-6 w-6 text-amber-500" />
              容器收入口
            </h1>
            <p className="text-sm text-slate-400 mt-1">
              统一数据入口 · 六维评估 · DNA盖章(v∞) · 五桶分拣
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className="border-amber-500/30 text-amber-400 text-xs">
              <Dna className="h-3 w-3 mr-1" />
              DNA v∞ 干支卦
            </Badge>
            {stats && (
              <Badge variant="outline" className="border-slate-600 text-slate-300 text-xs">
                共 {stats.total} 条
              </Badge>
            )}
          </div>
        </div>

        {/* 今日DNA回单 */}
        {stats?.todayDNA && (
          <div className="rounded-lg border border-amber-500/20 bg-amber-500/5 p-3">
            <div className="flex items-center gap-2 text-xs text-amber-400">
              <Sparkles className="h-3.5 w-3.5" />
              <span className="font-mono">{stats.todayDNA}</span>
            </div>
          </div>
        )}

        {/* Stats Cards */}
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">总收录</div>
              <div className="text-2xl font-bold text-white">{stats.total}</div>
            </div>
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">DNA盖章</div>
              <div className="text-2xl font-bold text-amber-400">{stats.dnaTotal}</div>
            </div>
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">桶分布</div>
              <div className="flex flex-wrap gap-1 mt-1">
                {stats.buckets?.map((b: any) => (
                  <Badge key={b.bucket} variant="outline" className="text-[10px] border-slate-600">
                    {bucketLabel(b.bucket)} {b.count}
                  </Badge>
                ))}
              </div>
            </div>
            <div className="rounded-lg border border-slate-700 bg-slate-800/50 p-3">
              <div className="text-xs text-slate-400">三色分布</div>
              <div className="flex gap-2 mt-1">
                {stats.colors?.map((c: any) => (
                  <span key={c.color} className="text-xs">
                    {c.color} <span className="text-white font-bold">{c.count}</span>
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}

        <Separator className="bg-slate-700" />

        {/* Drop Zone */}
        <div className="rounded-xl border-2 border-dashed border-slate-600 bg-slate-800/30 p-4 space-y-4 hover:border-amber-500/40 transition-colors">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <ClipboardPaste className="h-5 w-5 text-amber-500" />
              <h2 className="text-lg font-semibold text-white">Drop Zone</h2>
            </div>
            <div className="flex items-center gap-2">
              <Button
                variant={batchMode ? "default" : "outline"}
                size="sm"
                onClick={() => setBatchMode(!batchMode)}
                className={`text-xs ${batchMode ? "bg-amber-600 hover:bg-amber-700" : "border-slate-600 text-slate-300"}`}
              >
                <Database className="h-3.5 w-3.5 mr-1" />
                {batchMode ? "批量模式开" : "批量模式"}
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={handlePaste}
                className="text-xs border-slate-600 text-slate-300"
              >
                <ClipboardPaste className="h-3.5 w-3.5 mr-1" />
                粘贴
              </Button>
            </div>
          </div>

          {batchMode && (
            <p className="text-xs text-amber-400">
              批量模式：每行一条内容，系统将逐条处理
            </p>
          )}

          <Textarea
            ref={textareaRef}
            value={content}
            onChange={(e) => setContent(e.target.value)}
            placeholder={batchMode
              ? "每行一条，粘贴多条内容..."
              : "粘贴任何内容：对话碎片 / 代码 / 链接 / 想法 / 旧页面 ... 系统将自动清洗、评估、盖DNA"
            }
            className="min-h-[160px] bg-slate-900/50 border-slate-600 text-slate-200 placeholder:text-slate-500 resize-none"
          />

          <div className="flex items-center justify-between">
            <div className="text-xs text-slate-500">
              {content.length > 0 && `共 ${content.length} 字符 · 预估 ${detectContentType(content)}`}
            </div>
            <Button
              onClick={handleDrop}
              disabled={!content.trim() || dropMutation.isPending}
              className="bg-amber-600 hover:bg-amber-700 text-white"
            >
              <Sparkles className="h-4 w-4 mr-2" />
              {dropMutation.isPending ? "处理中..." : batchMode ? "批量投喂" : "投喂 + DNA盖章"}
            </Button>
          </div>
        </div>

        {/* 处理结果 */}
        {dropMutation.isPending && (
          <div className="rounded-lg border border-amber-500/30 bg-amber-500/5 p-6 text-center">
            <RefreshCw className="h-8 w-8 animate-spin text-amber-500 mx-auto" />
            <p className="mt-2 text-sm text-amber-400">六维评估中 · 四柱计算 · DNA盖章...</p>
          </div>
        )}

        {dropResult && !dropMutation.isPending && (
          <div className="space-y-2">
            <h3 className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              处理完成 — DNA已盖
            </h3>
            <Eval6Card
              eval6={dropResult.eval6}
              dna={dropResult.dna}
              ganzhi={dropResult.ganzhi}
            />
          </div>
        )}

        <Separator className="bg-slate-700" />

        {/* Tabs: 记录 / DNA注册表 */}
        <Tabs defaultValue="entries" className="w-full">
          <TabsList className="bg-slate-800 border border-slate-700">
            <TabsTrigger value="entries" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
              <Database className="h-3.5 w-3.5 mr-1" />
              收录记录
            </TabsTrigger>
            <TabsTrigger value="dna" className="data-[state=active]:bg-amber-600 data-[state=active]:text-white">
              <Dna className="h-3.5 w-3.5 mr-1" />
              DNA注册表v2
            </TabsTrigger>
          </TabsList>

          <TabsContent value="entries" className="mt-4">
            {entriesLoading ? (
              <div className="text-center py-8 text-slate-500">加载中...</div>
            ) : entries && entries.length > 0 ? (
              <div className="space-y-2">
                {entries.map((entry: any) => (
                  <div
                    key={entry.id}
                    className="rounded-lg border border-slate-700 bg-slate-800/30 p-3 hover:bg-slate-800/50 transition-colors"
                  >
                    <div className="flex items-start justify-between gap-2">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 flex-wrap">
                          <Badge variant="outline" className="text-[10px] border-slate-600">
                            #{entry.id}
                          </Badge>
                          <Badge className={`text-[10px] ${
                            entry.三色审计 === "🟢"
                              ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
                              : entry.三色审计 === "🟡"
                              ? "bg-amber-500/20 text-amber-400 border-amber-500/30"
                              : "bg-red-500/20 text-red-400 border-red-500/30"
                          }`}>
                            {entry.三色审计}
                          </Badge>
                          <span className="text-[10px] text-slate-500">
                            {bucketLabel(entry.bucket)}
                          </span>
                          <span className="text-[10px] text-slate-500">
                            {entry.权重层级}
                          </span>
                        </div>
                        <p className="text-xs text-slate-300 mt-1 line-clamp-2">
                          {entry.rawContent?.substring(0, 200)}
                          {entry.rawContent?.length > 200 ? "..." : ""}
                        </p>
                        <div className="flex items-center gap-2 mt-1">
                          <code className="text-[10px] text-amber-400/70 font-mono truncate max-w-[300px]">
                            {entry.dnaV2}
                          </code>
                        </div>
                      </div>
                      <div className="flex flex-col gap-1 shrink-0">
                        {bucketIcon(entry.bucket)}
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-6 w-6 text-slate-500 hover:text-red-400"
                          onClick={() => freezeMutation.mutate({ id: entry.id })}
                        >
                          <Trash2 className="h-3 w-3" />
                        </Button>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-slate-500 rounded-lg border border-dashed border-slate-700">
                <Database className="h-8 w-8 mx-auto mb-2 text-slate-600" />
                暂无收录记录，开始投喂吧
              </div>
            )}
          </TabsContent>

          <TabsContent value="dna" className="mt-4">
            {dnaList && dnaList.length > 0 ? (
              <div className="space-y-2">
                {dnaList.map((d: any) => (
                  <div
                    key={d.id}
                    className="rounded-lg border border-slate-700 bg-slate-800/30 p-3"
                  >
                    <div className="flex items-center gap-2">
                      <Dna className="h-4 w-4 text-amber-500 shrink-0" />
                      <code className="text-xs text-amber-400 font-mono break-all">{d.dnaV2}</code>
                    </div>
                    <div className="flex items-center gap-3 mt-1 text-[10px] text-slate-400">
                      <span>{d.stamp}</span>
                      <span>·</span>
                      <span>{d.module}-{d.action}</span>
                      <span>·</span>
                      <span>哈希 {d.hash8}</span>
                    </div>
                    <div className="text-[10px] text-slate-500 mt-1">
                      {d.年干支}年·{d.月干支}月·{d.日干支}日·{d.时辰名}·{d.卦名}卦·五行{d.五行}
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center py-8 text-slate-500 rounded-lg border border-dashed border-slate-700">
                <Dna className="h-8 w-8 mx-auto mb-2 text-slate-600" />
                暂无DNA记录
              </div>
            )}
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
