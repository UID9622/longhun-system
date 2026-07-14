/**
 * 龍魂操作台 - 设备证书管理
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-DEVICE-MGMT-v1.0
 */
import { useState } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Switch } from "@/components/ui/switch";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Smartphone, Plus, Trash2, Shield, ShieldAlert, Fingerprint, Cpu } from "lucide-react";

const deviceIcons: Record<string, React.ComponentType<{ className?: string }>> = {
  huawei: Cpu, apple: Smartphone, other: Fingerprint,
};

export default function DeviceMgmt() {
  const utils = trpc.useUtils();
  const { data: devices, isLoading } = trpc.admin.deviceList.useQuery();
  const [isOpen, setIsOpen] = useState(false);
  const [form, setForm] = useState({
    deviceType: "huawei" as const, deviceName: "", deviceModel: "",
    certificatePem: "", fingerprint: "", userId: 1,
  });

  const createMutation = trpc.admin.deviceCreate.useMutation({
    onSuccess: () => { utils.admin.deviceList.invalidate(); setIsOpen(false); resetForm(); },
  });
  const updateTrustMutation = trpc.admin.deviceUpdateTrust.useMutation({
    onSuccess: () => utils.admin.deviceList.invalidate(),
  });
  const deleteMutation = trpc.admin.deviceDelete.useMutation({
    onSuccess: () => utils.admin.deviceList.invalidate(),
  });

  const resetForm = () => setForm({
    deviceType: "huawei", deviceName: "", deviceModel: "",
    certificatePem: "", fingerprint: "", userId: 1,
  });

  return (
    <DashboardLayout>
      <div className="space-y-4">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-3">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <Smartphone className="h-5 w-5 text-amber-500" />
            设备证书管理
          </h2>
          <Dialog open={isOpen} onOpenChange={setIsOpen}>
            <DialogTrigger asChild>
              <Button className="bg-amber-600 hover:bg-amber-700">
                <Plus className="mr-1 h-4 w-4" /> 注册设备
              </Button>
            </DialogTrigger>
            <DialogContent className="bg-slate-900 border-slate-700 text-white max-w-lg max-h-[80vh] overflow-y-auto">
              <DialogHeader>
                <DialogTitle className="flex items-center gap-2">
                  <Shield className="h-4 w-4 text-amber-500" />
                  注册新设备
                </DialogTitle>
              </DialogHeader>
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <Label className="text-xs text-slate-400">设备类型</Label>
                    <Select value={form.deviceType} onValueChange={(v) => setForm({ ...form, deviceType: v as any })}>
                      <SelectTrigger className="bg-slate-800 border-slate-700"><SelectValue /></SelectTrigger>
                      <SelectContent className="bg-slate-800 border-slate-700">
                        <SelectItem value="huawei">华为</SelectItem>
                        <SelectItem value="apple">苹果</SelectItem>
                        <SelectItem value="other">其他</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                  <div>
                    <Label className="text-xs text-slate-400">设备名称</Label>
                    <Input value={form.deviceName} onChange={(e) => setForm({ ...form, deviceName: e.target.value })} className="bg-slate-800 border-slate-700" />
                  </div>
                </div>
                <div>
                  <Label className="text-xs text-slate-400">设备型号</Label>
                  <Input value={form.deviceModel} onChange={(e) => setForm({ ...form, deviceModel: e.target.value })} className="bg-slate-800 border-slate-700" />
                </div>
                <div>
                  <Label className="text-xs text-slate-400">证书 PEM</Label>
                  <textarea
                    value={form.certificatePem}
                    onChange={(e) => setForm({ ...form, certificatePem: e.target.value })}
                    rows={4}
                    className="w-full rounded-md bg-slate-800 border border-slate-700 p-2 text-xs text-slate-300 font-mono focus:outline-none focus:ring-1 focus:ring-amber-500"
                    placeholder="-----BEGIN CERTIFICATE-----"
                  />
                </div>
                <div>
                  <Label className="text-xs text-slate-400">指纹</Label>
                  <Input value={form.fingerprint} onChange={(e) => setForm({ ...form, fingerprint: e.target.value })} className="bg-slate-800 border-slate-700 font-mono text-xs" placeholder="SHA256:..." />
                </div>
                <Button
                  className="w-full bg-amber-600 hover:bg-amber-700"
                  onClick={() => createMutation.mutate(form)}
                  disabled={!form.deviceName}
                >
                  {createMutation.isPending ? "注册中..." : "注册设备"}
                </Button>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        <div className="grid gap-3">
          {devices?.map((d) => {
            const Icon = deviceIcons[d.deviceType] ?? Fingerprint;
            return (
              <Card key={d.id} className="bg-slate-900 border-slate-800 hover:border-slate-700 transition-colors">
                <CardContent className="p-4">
                  <div className="flex items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <div className={`rounded-lg p-2.5 ${d.isTrusted ? "bg-emerald-600/20" : "bg-slate-800"}`}>
                        <Icon className={`h-5 w-5 ${d.isTrusted ? "text-emerald-400" : "text-slate-400"}`} />
                      </div>
                      <div>
                        <div className="flex items-center gap-2">
                          <h3 className="text-white font-medium">{d.deviceName || `设备 #${d.id}`}</h3>
                          <Badge className={`${d.isTrusted ? "bg-emerald-600" : "bg-amber-600"} text-white text-[10px]`}>
                            {d.isTrusted ? (
                              <><Shield className="mr-1 h-2.5 w-2.5" />已信任</>
                            ) : (
                              <><ShieldAlert className="mr-1 h-2.5 w-2.5" />待验证</>
                            )}
                          </Badge>
                        </div>
                        <div className="flex items-center gap-3 mt-1 text-xs text-slate-500">
                          <span className="capitalize">{d.deviceType}</span>
                          {d.deviceModel && <span>{d.deviceModel}</span>}
                          {d.fingerprint && (
                            <span className="font-mono text-[10px] truncate max-w-[200px]">
                              {d.fingerprint}
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                    <div className="flex items-center gap-2 flex-shrink-0">
                      <span className="text-[10px] text-slate-500 mr-1">信任</span>
                      <Switch
                        checked={d.isTrusted}
                        onCheckedChange={(checked) =>
                          updateTrustMutation.mutate({ id: d.id, isTrusted: checked })
                        }
                      />
                      <Button
                        variant="ghost" size="icon"
                        onClick={() => deleteMutation.mutate({ id: d.id })}
                        className="h-8 w-8 text-slate-400 hover:text-red-400"
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })}
          {!devices?.length && !isLoading && (
            <div className="text-center py-12 text-slate-500">
              <Smartphone className="mx-auto h-10 w-10 mb-2 opacity-50" />
              <p>暂无注册设备</p>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
}
