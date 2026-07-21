/**
 * 龍魂操作台 - 内容管理
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-CONTENT-MGMT-v1.0
 */
import { useState } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { FileText, Plus, Search, Trash2, Pencil, Dna } from "lucide-react";

const typeColors: Record<string, string> = {
  skill: "bg-blue-600",
  persona: "bg-pink-600",
  document: "bg-violet-600",
  config: "bg-amber-600",
  audit: "bg-red-600",
};

const statusColors: Record<string, string> = {
  draft: "bg-slate-600",
  published: "bg-emerald-600",
  archived: "bg-slate-500",
};

export default function ContentMgmt() {
  const utils = trpc.useUtils();
  const { data: items, isLoading } = trpc.admin.contentList.useQuery({});
  const [search, setSearch] = useState("");
  const [typeFilter, setTypeFilter] = useState<string>("");
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState({
    title: "", slug: "", type: "skill" as const, content: "", tags: "", status: "draft" as const,
  });

  const createMutation = trpc.admin.contentCreate.useMutation({
    onSuccess: () => { utils.admin.contentList.invalidate(); setIsOpen(false); resetForm(); },
  });
  const deleteMutation = trpc.admin.contentDelete.useMutation({
    onSuccess: () => utils.admin.contentList.invalidate(),
  });

  const resetForm = () => setForm({ title: "", slug: "", type: "skill", content: "", tags: "", status: "draft" });

  const filtered = items?.filter((item) => {
    if (search && !item.title.includes(search)) return false;
    if (typeFilter && item.type !== typeFilter) return false;
    return true;
  });

  return (
    <DashboardLayout>
      <div className="space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <FileText className="h-5 w-5 text-amber-500" />
            内容管理
          </h2>
          <div className="flex gap-2">
            <Input
              placeholder="搜索标题..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-48 bg-slate-900 border-slate-700 text-white"
            />
            <Select value={typeFilter} onValueChange={setTypeFilter}>
              <SelectTrigger className="w-32 bg-slate-900 border-slate-700 text-white">
                <SelectValue placeholder="类型" />
              </SelectTrigger>
              <SelectContent className="bg-slate-800 border-slate-700">
                <SelectItem value="">全部</SelectItem>
                <SelectItem value="skill">技能</SelectItem>
                <SelectItem value="persona">人格</SelectItem>
                <SelectItem value="document">文档</SelectItem>
                <SelectItem value="config">配置</SelectItem>
              </SelectContent>
            </Select>
            <Dialog open={isOpen} onOpenChange={setIsOpen}>
              <DialogTrigger asChild>
                <Button className="bg-amber-600 hover:bg-amber-700">
                  <Plus className="mr-1 h-4 w-4" /> 新增
                </Button>
              </DialogTrigger>
              <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-lg max-h-[80vh] overflow-y-auto">
                <DialogHeader>
                  <DialogTitle className="flex items-center gap-2">
                    <Plus className="h-4 w-4 text-amber-500" />
                    新建内容
                  </DialogTitle>
                </DialogHeader>
                <div className="space-y-3">
                  <div>
                    <Label className="text-xs text-slate-400">标题</Label>
                    <Input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} className="bg-slate-800 border-slate-700" />
                  </div>
                  <div>
                    <Label className="text-xs text-slate-400">Slug</Label>
                    <Input value={form.slug} onChange={(e) => setForm({ ...form, slug: e.target.value })} className="bg-slate-800 border-slate-700" />
                  </div>
                  <div className="grid grid-cols-2 gap-2">
                    <div>
                      <Label className="text-xs text-slate-400">类型</Label>
                      <Select value={form.type} onValueChange={(v) => setForm({ ...form, type: v as any })}>
                        <SelectTrigger className="bg-slate-800 border-slate-700"><SelectValue /></SelectTrigger>
                        <SelectContent className="bg-slate-800 border-slate-700">
                          <SelectItem value="skill">技能</SelectItem>
                          <SelectItem value="persona">人格</SelectItem>
                          <SelectItem value="document">文档</SelectItem>
                          <SelectItem value="config">配置</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                    <div>
                      <Label className="text-xs text-slate-400">状态</Label>
                      <Select value={form.status} onValueChange={(v) => setForm({ ...form, status: v as any })}>
                        <SelectTrigger className="bg-slate-800 border-slate-700"><SelectValue /></SelectTrigger>
                        <SelectContent className="bg-slate-800 border-slate-700">
                          <SelectItem value="draft">草稿</SelectItem>
                          <SelectItem value="published">已发布</SelectItem>
                          <SelectItem value="archived">已归档</SelectItem>
                        </SelectContent>
                      </Select>
                    </div>
                  </div>
                  <div>
                    <Label className="text-xs text-slate-400">内容</Label>
                    <Textarea value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} rows={4} className="bg-slate-800 border-slate-700" />
                  </div>
                  <div>
                    <Label className="text-xs text-slate-400">标签</Label>
                    <Input value={form.tags} onChange={(e) => setForm({ ...form, tags: e.target.value })} placeholder="逗号分隔" className="bg-slate-800 border-slate-700" />
                  </div>
                  <Button
                    className="w-full bg-amber-600 hover:bg-amber-700"
                    onClick={() => createMutation.mutate({ userId: 1, ...form })}
                    disabled={!form.title || !form.slug}
                  >
                    {createMutation.isPending ? "创建中..." : "创建内容"}
                  </Button>
                </div>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        <div className="rounded-lg border border-slate-800 overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-slate-800/50 text-slate-400 text-xs">
              <tr>
                <th className="px-3 py-2 text-left">ID</th>
                <th className="px-3 py-2 text-left">标题</th>
                <th className="px-3 py-2 text-left">类型</th>
                <th className="px-3 py-2 text-left">状态</th>
                <th className="px-3 py-2 text-left">DNA</th>
                <th className="px-3 py-2 text-left">创建时间</th>
                <th className="px-3 py-2 text-right">操作</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filtered?.map((item) => (
                <tr key={item.id} className="hover:bg-slate-800/30 transition-colors">
                  <td className="px-3 py-2 text-slate-500">{item.id}</td>
                  <td className="px-3 py-2 text-white font-medium">{item.title}</td>
                  <td className="px-3 py-2">
                    <Badge className={`${typeColors[item.type] ?? "bg-slate-600"} text-white text-[10px]`}>
                      {item.type}
                    </Badge>
                  </td>
                  <td className="px-3 py-2">
                    <Badge className={`${statusColors[item.status] ?? "bg-slate-600"} text-white text-[10px]`}>
                      {item.status}
                    </Badge>
                  </td>
                  <td className="px-3 py-2">
                    {item.dnaMarker ? (
                      <span className="flex items-center gap-1 text-[10px] text-amber-400 font-mono">
                        <Dna className="h-3 w-3" />
                        {item.dnaMarker.slice(0, 24)}...
                      </span>
                    ) : (
                      <span className="text-slate-600 text-xs">-</span>
                    )}
                  </td>
                  <td className="px-3 py-2 text-slate-500 text-xs">
                    {new Date(item.createdAt).toLocaleDateString()}
                  </td>
                  <td className="px-3 py-2 text-right">
                    <Button
                      variant="ghost" size="icon"
                      onClick={() => deleteMutation.mutate({ id: item.id })}
                      className="h-7 w-7 text-slate-400 hover:text-red-400"
                    >
                      <Trash2 className="h-3.5 w-3.5" />
                    </Button>
                  </td>
                </tr>
              ))}
              {!filtered?.length && (
                <tr>
                  <td colSpan={7} className="px-3 py-8 text-center text-slate-500">
                    {isLoading ? "加载中..." : "暂无内容"}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </DashboardLayout>
  );
}
