归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 龍魂操作台 - 人格助手配置
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-PERSONA-CONFIG-v1.0
 */
import { useState } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BrainCircuit, Plus, Trash2, MessageSquare, Sparkles, Shield, Zap } from "lucide-react";

const styleLabels: Record<string, string> = {
  formal: "正式", casual: "随意", military: "军事", friendly: "友好",
};

const styleColors: Record<string, string> = {
  formal: "bg-blue-600", casual: "bg-green-600", military: "bg-red-600", friendly: "bg-pink-600",
};

export default function PersonaConfig() {
  const utils = trpc.useUtils();
  const { data: personas, isLoading } = trpc.admin.personaList.useQuery();
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState({
    personaName: "", systemPrompt: "", triggerKeywords: "",
    responseStyle: "formal" as const, priority: 0, enabledSkills: "[]",
  });

  const createMutation = trpc.admin.personaCreate.useMutation({
    onSuccess: () => { utils.admin.personaList.invalidate(); setIsOpen(false); resetForm(); },
  });
  const updateMutation = trpc.admin.personaUpdate.useMutation({
    onSuccess: () => utils.admin.personaList.invalidate(),
  });
  const deleteMutation = trpc.admin.personaDelete.useMutation({
    onSuccess: () => utils.admin.personaList.invalidate(),
  });

  const resetForm = () => setForm({
    personaName: "", systemPrompt: "", triggerKeywords: "",
    responseStyle: "formal", priority: 0, enabledSkills: "[]",
  });

  return (
    <DashboardLayout>
      <div className="space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <BrainCircuit className="h-5 w-5 text-amber-500" />
            人格助手配置
          </h2>
          <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
              <Button className="bg-amber-600 hover:bg-amber-700">
                <Plus className="mr-1 h-4 w-4" /> 添加人格
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-lg max-h-[80vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <Sparkles className="h-4 w-4 text-amber-500" />
                  新建人格助手
                </DialogTitle>
              </DialogHeader>
              <div className="space-y-3">
                <div>
                  <Label className="text-xs text-slate-400">人格名称</Label>
                  <Input value={form.personaName} onChange={(e) => setForm({ ...form, personaName: e.target.value })} className="bg-slate-800 border-slate-700" />
                </div>
                <div>
                  <Label className="text-xs text-slate-400">系统提示词</Label>
                  <Textarea value={form.systemPrompt} onChange={(e) => setForm({ ...form, systemPrompt: e.target.value })} rows={4} className="bg-slate-800 border-slate-700" placeholder="你是龙魂体系的..." />
                </div>
                <div>
                  <Label className="text-xs text-slate-400">触发关键词</Label>
                  <Input value={form.triggerKeywords} onChange={(e) => setForm({ ...form, triggerKeywords: e.target.value })} className="bg-slate-800 border-slate-700" placeholder="逗号分隔的关键词" />
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label className="text-xs text-slate-400">回复风格</Label>
                    <Select value={form.responseStyle} onValueChange={(v) => setForm({ ...form, responseStyle: v as any })}>
                      <SelectTrigger className="bg-slate-800 border-slate-700"><SelectValue /></SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        <SelectItem value="formal">正式</SelectItem>
                        <SelectItem value="casual">随意</SelectItem>
                        <SelectItem value="military">军事</SelectItem>
                        <SelectItem value="friendly">友好</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label className="text-xs text-slate-400">优先级</Label>
                    <Input type="number" value={form.priority} onChange={(e) => setForm({ ...form, priority: parseInt(e.target.value) || 0 })} className="bg-slate-800 border-slate-700" />
                  </div>
                </div>
                <Button
                  className="w-full bg-amber-600 hover:bg-amber-700"
                  onClick={() => createMutation.mutate({ userId: 1, ...form })}
                  disabled={!form.personaName}
                >
                  {createMutation.isPending ? "创建中..." : "创建人格"}
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        <div className="grid gap-3">
          {personas?.map((p) => (
            <Card key={p.id} className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
              <CardContent className="p-4">
                <div className="flex items-start justify-between gap-4">
                  <div className="flex-1 min-w-0 space-y-2">
                    <div className="flex items-center gap-2 flex-wrap">
                      <h3 className="text-white font-semibold">{p.personaName}</h3>
                      <Badge className={`${styleColors[p.responseStyle] ?? "bg-slate-600"} text-white text-[10px]`}>
                        {styleLabels[p.responseStyle] ?? p.responseStyle}
                      </Badge>
                      <Badge className={`${p.isActive ? "bg-emerald-600" : "bg-slate-600"} text-white text-[10px]`}>
                        {p.isActive ? "激活" : "停用"}
                      </Badge>
                      {p.priority > 0 && (
                        <Badge className="bg-amber-600 text-white text-[10px]">
                          <Zap className="mr-1 h-2.5 w-2.5" />
                          P{p.priority}
                        </Badge>
                      )}
                    </div>
                    {p.systemPrompt && (
                      <p className="text-xs text-slate-400 line-clamp-2">{p.systemPrompt}</p>
                    )}
                    {p.triggerKeywords && (
                      <div className="flex items-center gap-1 flex-wrap">
                        <MessageSquare className="h-3 w-3 text-slate-500" />
                        {p.triggerKeywords.split(",").map((k) => (
                          <Badge key={k} variant="outline" className="border-slate-700 text-slate-400 text-[10px]">
                            {k.trim()}
                          </Badge>
                        ))}
                      </div>
                    )}
                  </div>
                  <div className="flex items-center gap-1 flex-shrink-0">
                    <Switch
                      checked={p.isActive}
                      onCheckedChange={(checked) =>
                        updateMutation.mutate({ id: p.id, isActive: checked })
                      }
                    />
                    <Button
                      variant="ghost" size="icon"
                      onClick={() => deleteMutation.mutate({ id: p.id })}
                      className="h-8 w-8 text-slate-400 hover:text-red-400"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
          {!personas?.length && !isLoading && (
            <div className="text-center py-12 text-slate-500">
              <BrainCircuit className="mx-auto h-10 w-10 mb-2 opacity-50" />
              <p>暂未配置人格助手</p>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
