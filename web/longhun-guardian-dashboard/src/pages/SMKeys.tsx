/**
 * 龍魂操作台 - 国密密钥管理
 * DNA: #龍芯⚡️2026-07-11-LONGHUN-SMKEYS-v1.0
 */
import { useState } from "react";
import { trpc } from "@/providers/trpc";
import DashboardLayout from "@/components/DashboardLayout";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Fingerprint, Key, Lock, Unlock, Copy, Check, Hash, FileKey } from "lucide-react";

export default function SMKeys() {
  const utils = trpc.useUtils();
  const { data: keys } = trpc.admin.smKeyList.useQuery();
  const [hashInput, setHashInput] = useState("");
  const [hashResult, setHashResult] = useState("");
  const [encInput, setEncInput] = useState("");
  const [encKey, setEncKey] = useState("");
  const [encResult, setEncResult] = useState("");
  const [decInput, setDecInput] = useState("");
  const [decKey, setDecKey] = useState("");
  const [decResult, setDecResult] = useState("");
  const [copied, setCopied] = useState(false);

  const hashMutation = trpc.admin.sm3Hash.useMutation({ onSuccess: (d) => setHashResult(d.hash) });
  const encMutation = trpc.admin.sm4Encrypt.useMutation({ onSuccess: (d) => setEncResult(d.ciphertext) });
  const decMutation = trpc.admin.sm4Decrypt.useMutation({ onSuccess: (d) => setDecResult(d.plaintext) });
  const genMutation = trpc.admin.generateSMKey.useMutation();
  const revokeMutation = trpc.admin.smKeyRevoke.useMutation({
    onSuccess: () => utils.admin.smKeyList.invalidate(),
  });
  const createKeyMutation = trpc.admin.smKeyCreate.useMutation({
    onSuccess: () => utils.admin.smKeyList.invalidate(),
  });

  const copy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <DashboardLayout>
      <div className="space-y-6">
        <h2 className="text-xl font-bold text-white flex items-center gap-2">
          <Fingerprint className="h-5 w-5 text-amber-500" />
          国密算法工具箱
        </h2>

        <Tabs defaultValue="hash" className="w-full">
          <TabsList className="bg-slate-900 border border-slate-800">
            <TabsTrigger value="hash" className="data-[state=active]:bg-amber-600">
              <Hash className="mr-1 h-3.5 w-3.5" /> SM3 哈希
            </TabsTrigger>
            <TabsTrigger value="encrypt" className="data-[state=active]:bg-amber-600">
              <Lock className="mr-1 h-3.5 w-3.5" /> SM4 加密
            </TabsTrigger>
            <TabsTrigger value="decrypt" className="data-[state=active]:bg-amber-600">
              <Unlock className="mr-1 h-3.5 w-3.5" /> SM4 解密
            </TabsTrigger>
            <TabsTrigger value="keys" className="data-[state=active]:bg-amber-600">
              <Key className="mr-1 h-3.5 w-3.5" /> 密钥管理
            </TabsTrigger>
          </TabsList>

          <TabsContent value="hash" className="mt-4">
            <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-4 space-y-3">
                <label className="text-xs text-slate-400">输入数据</label>
                <Textarea value={hashInput} onChange={(e) => setHashInput(e.target.value)} rows={3} className="bg-slate-800 border-slate-700 text-white" placeholder="输入要哈希的数据..." />
                <Button onClick={() => hashMutation.mutate({ data: hashInput })} disabled={!hashInput} className="bg-amber-600 hover:bg-amber-700">
                  <Hash className="mr-1 h-4 w-4" /> 计算 SM3 哈希
                </Button>
                {hashResult && (
                  <div className="rounded-lg bg-slate-800 p-3 space-y-2">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-slate-400">哈希结果 (Hex)</span>
                      <Button variant="ghost" size="sm" onClick={() => copy(hashResult)} className="h-6 text-xs">
                        {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />} 复制
                      </Button>
                    </div>
                    <p className="text-xs text-emerald-400 font-mono break-all">{hashResult}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="encrypt" className="mt-4">
            <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-4 space-y-3">
                <div>
                  <label className="text-xs text-slate-400">明文</label>
                  <Textarea value={encInput} onChange={(e) => setEncInput(e.target.value)} rows={2} className="bg-slate-800 border-slate-700 text-white" placeholder="输入明文..." />
                </div>
                <div>
                  <label className="text-xs text-slate-400">密钥 (Hex, 32字符)</label>
                  <Input value={encKey} onChange={(e) => setEncKey(e.target.value)} className="bg-slate-800 border-slate-700 text-white font-mono text-xs" placeholder="0123456789abcdeffedcba9876543210" />
                </div>
                <Button onClick={() => encMutation.mutate({ plaintext: encInput, key: encKey })} disabled={!encInput || !encKey} className="bg-amber-600 hover:bg-amber-700">
                  <Lock className="mr-1 h-4 w-4" /> SM4 加密
                </Button>
                {encResult && (
                  <div className="rounded-lg bg-slate-800 p-3">
                    <span className="text-xs text-slate-400">密文 (Hex)</span>
                    <p className="text-xs text-emerald-400 font-mono break-all mt-1">{encResult}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="decrypt" className="mt-4">
            <Card className="bg-slate-900 border-slate-800">
              <CardContent className="p-4 space-y-3">
                <div>
                  <label className="text-xs text-slate-400">密文 (Hex)</label>
                  <Textarea value={decInput} onChange={(e) => setDecInput(e.target.value)} rows={2} className="bg-slate-800 border-slate-700 text-white font-mono text-xs" placeholder="输入密文..." />
                </div>
                <div>
                  <label className="text-xs text-slate-400">密钥 (Hex, 32字符)</label>
                  <Input value={decKey} onChange={(e) => setDecKey(e.target.value)} className="bg-slate-800 border-slate-700 text-white font-mono text-xs" placeholder="0123456789abcdeffedcba9876543210" />
                </div>
                <Button onClick={() => decMutation.mutate({ ciphertext: decInput, key: decKey })} disabled={!decInput || !decKey} className="bg-amber-600 hover:bg-amber-700">
                  <Unlock className="mr-1 h-4 w-4" /> SM4 解密
                </Button>
                {decResult && (
                  <div className="rounded-lg bg-slate-800 p-3">
                    <span className="text-xs text-slate-400">明文</span>
                    <p className="text-xs text-emerald-400 font-mono break-all mt-1">{decResult}</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="keys" className="mt-4 space-y-4">
            <div className="flex gap-2">
              <Button onClick={() => genMutation.mutate({ name: "SM4-" + Date.now(), type: "sm4" })} className="bg-emerald-600 hover:bg-emerald-700">
                <FileKey className="mr-1 h-4 w-4" /> 生成 SM4 密钥
              </Button>
              <Button onClick={() => genMutation.mutate({ name: "SECRET-" + Date.now(), type: "secret" })} className="bg-violet-600 hover:bg-violet-700">
                <Key className="mr-1 h-4 w-4" /> 生成 Secret 密钥
              </Button>
            </div>
            {genMutation.data && (
              <Card className="bg-slate-900 border-emerald-800">
                <CardContent className="p-3">
                  <p className="text-xs text-emerald-400 font-mono break-all">{genMutation.data.key}</p>
                </CardContent>
              </Card>
            )}
            <div className="rounded-lg border border-slate-800 overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-slate-800/50 text-slate-400 text-xs">
                  <tr>
                    <th className="px-3 py-2 text-left">ID</th>
                    <th className="px-3 py-2 text-left">名称</th>
                    <th className="px-3 py-2 text-left">状态</th>
                    <th className="px-3 py-2 text-left">DNA</th>
                    <th className="px-3 py-2 text-right">操作</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800">
                  {keys?.map((k) => (
                    <tr key={k.id} className="hover:bg-slate-800/30">
                      <td className="px-3 py-2 text-slate-500">{k.id}</td>
                      <td className="px-3 py-2 text-white">{k.keyName}</td>
                      <td className="px-3 py-2">
                        <Badge className={`${k.status === "active" ? "bg-emerald-600" : k.status === "revoked" ? "bg-red-600" : "bg-slate-600"} text-white text-[10px]`}>
                          {k.status}
                        </Badge>
                      </td>
                      <td className="px-3 py-2 text-[10px] text-amber-400 font-mono">{k.dnaSignature?.slice(0, 20)}...</td>
                      <td className="px-3 py-2 text-right">
                        <Button variant="ghost" size="sm" onClick={() => revokeMutation.mutate({ id: k.id })} className="h-6 text-xs text-red-400 hover:text-red-300">
                          吊销
                        </Button>
                      </td>
                    </tr>
                  ))}
                  {!keys?.length && (
                    <tr><td colSpan={5} className="px-3 py-6 text-center text-slate-500">暂无存储的密钥</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}

function Textarea({ className, ...props }: React.TextareaHTMLAttributes<HTMLTextAreaElement>) {
  return <textarea className={`w-full rounded-md border p-2 text-sm focus:outline-none focus:ring-1 focus:ring-amber-500 ${className}`} {...props} />;
}
