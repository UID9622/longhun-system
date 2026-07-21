// 开发者接入中心 · API/MCP/SDK/文档
// DNA: #龍芯⚡️2026-06-28-LONGHUN-HEART-TALK-v2.0

import { useState } from 'react';
import { Code, Terminal, BookOpen, Copy, Check, Plug, Lock, Globe } from 'lucide-react';
import type { PageRoute } from '@/types';
import { API_ENDPOINTS } from '@/utils/data';

interface Props {
  onNavigate: (page: PageRoute) => void;
}

export default function DeveloperCenter({ onNavigate }: Props) {
  const [activeTab, setActiveTab] = useState<'api' | 'mcp' | 'sdk' | 'protocol'>('api');
  const [copied, setCopied] = useState<string | null>(null);

  const copy = (text: string, id: string) => {
    navigator.clipboard?.writeText(text).catch(() => {});
    setCopied(id);
    setTimeout(() => setCopied(null), 2000);
  };

  const tabs = [
    { key: 'api' as const, label: 'API接口', icon: Globe },
    { key: 'mcp' as const, label: 'MCP协议', icon: Plug },
    { key: 'sdk' as const, label: 'SDK下载', icon: Code },
    { key: 'protocol' as const, label: '接入协议', icon: BookOpen },
  ];

  return (
    <div className="h-full flex flex-col overflow-hidden">
      {/* 头部 */}
      <div className="p-6 border-b border-zinc-800/50">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-sky-400 to-emerald-400 bg-clip-text text-transparent">
              开发者接入中心
            </h1>
            <p className="text-sm text-zinc-500 mt-1">
              API文档 · MCP协议 · SDK工具包 · 接入授权
            </p>
          </div>
          <button
            onClick={() => onNavigate('auth')}
            className="flex items-center gap-1.5 px-3 py-2 rounded-lg border border-zinc-700/50 bg-zinc-800/50 text-xs text-zinc-300 hover:border-sky-500/30 hover:bg-sky-500/5 transition-all"
          >
            <Lock className="w-3.5 h-3.5" />申请授权
          </button>
        </div>

        {/* Tab切换 */}
        <div className="flex items-center gap-2 mt-4">
          {tabs.map(tab => (
            <button
              key={tab.key}
              onClick={() => setActiveTab(tab.key)}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded text-xs border transition-all ${
                activeTab === tab.key
                  ? 'bg-sky-500/10 text-sky-400 border-sky-500/30'
                  : 'border-zinc-800 text-zinc-500 hover:border-zinc-700 hover:text-zinc-400'
              }`}
            >
              <tab.icon className="w-3.5 h-3.5" />{tab.label}
            </button>
          ))}
        </div>
      </div>

      {/* 内容区 */}
      <div className="flex-1 overflow-y-auto p-6 scrollbar-thin">
        {activeTab === 'api' && (
          <div className="space-y-4">
            <div className="p-4 rounded-lg border border-sky-500/15 bg-sky-500/5">
              <div className="flex items-center gap-2 mb-2">
                <Globe className="w-4 h-4 text-sky-500" />
                <h3 className="text-sm font-bold text-sky-400">龍魂API网关</h3>
              </div>
              <p className="text-xs text-zinc-500">
                基础地址: <code className="text-sky-400/80 font-mono">http://api.longhun.local/v1</code>
              </p>
              <p className="text-xs text-zinc-600 mt-1">所有请求需携带 X-LongHun-Auth 头部</p>
            </div>

            <div className="space-y-2">
              {API_ENDPOINTS.map(api => (
                <div key={api.id} className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
                  <div className="flex items-center gap-2">
                    <span className={`text-[10px] px-1.5 py-0.5 rounded font-bold ${
                      api.method === 'GET' ? 'bg-emerald-500/10 text-emerald-400' :
                      api.method === 'POST' ? 'bg-sky-500/10 text-sky-400' :
                      api.method === 'PUT' ? 'bg-amber-500/10 text-amber-400' :
                      'bg-red-500/10 text-red-400'
                    }`}>
                      {api.method}
                    </span>
                    <code className="text-xs text-amber-400/80 font-mono">{api.path}</code>
                    {api.auth && <Lock className="w-3 h-3 text-red-400/60" />}
                  </div>
                  <p className="text-xs text-zinc-400 mt-1">{api.description}</p>
                  {api.example && (
                    <div className="mt-2 flex items-center gap-2">
                      <code className="flex-1 text-[10px] text-emerald-400/70 font-mono bg-zinc-900/50 p-1.5 rounded truncate">{api.example}</code>
                      <button
                        onClick={() => copy(api.example!, api.id)}
                        className="p-1 rounded hover:bg-zinc-800 transition-colors shrink-0"
                      >
                        {copied === api.id ? <Check className="w-3 h-3 text-green-400" /> : <Copy className="w-3 h-3 text-zinc-600" />}
                      </button>
                    </div>
                  )}
                  <code className="text-[8px] text-amber-500/30 font-mono block mt-1">{api.dna}</code>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'mcp' && (
          <div className="space-y-4">
            <div className="p-4 rounded-lg border border-emerald-500/15 bg-emerald-500/5">
              <div className="flex items-center gap-2 mb-2">
                <Plug className="w-4 h-4 text-emerald-500" />
                <h3 className="text-sm font-bold text-emerald-400">MCP协议接入</h3>
              </div>
              <p className="text-xs text-zinc-500">龍魂系统支持 Model Context Protocol，任何兼容MCP的客户端均可接入</p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
              {[
                { name: 'longhun-mcp-server', desc: '龍魂MCP主服务器，暴露全部工具', install: 'npx @longhun/mcp-server', status: '已发布' },
                { name: 'longhun-chat-mcp', desc: '对话专用MCP适配器', install: 'pip install longhun-mcp', status: '已发布' },
                { name: 'longhun-code-mcp', desc: '代码辅助MCP工具集', install: 'npm i @longhun/code-mcp', status: 'Beta' },
                { name: 'longhun-audit-mcp', desc: '审计日志MCP查询器', install: 'pip install longhun-audit-mcp', status: '已发布' },
              ].map(tool => (
                <div key={tool.name} className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
                  <div className="flex items-center justify-between">
                    <h4 className="text-sm font-medium text-emerald-400">{tool.name}</h4>
                    <span className={`text-[10px] px-1.5 py-0.5 rounded ${tool.status === '已发布' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-amber-500/10 text-amber-400'}`}>
                      {tool.status}
                    </span>
                  </div>
                  <p className="text-xs text-zinc-400 mt-1">{tool.desc}</p>
                  <div className="mt-2 flex items-center gap-2">
                    <Terminal className="w-3 h-3 text-zinc-600" />
                    <code className="text-[10px] text-emerald-400/70 font-mono">{tool.install}</code>
                  </div>
                </div>
              ))}
            </div>

            <div className="p-3 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
              <h4 className="text-xs font-medium text-zinc-400 mb-2">MCP配置示例</h4>
              <pre className="text-[10px] text-zinc-500 font-mono bg-zinc-950/50 p-3 rounded overflow-x-auto">
{`{
  "mcpServers": {
    "longhun": {
      "command": "npx",
      "args": ["@longhun/mcp-server"],
      "env": {
        "LONGHUN_API_KEY": "your-api-key",
        "LONGHUN_BASE_URL": "http://api.longhun.local/v1"
      }
    }
  }
}`}
              </pre>
            </div>
          </div>
        )}

        {activeTab === 'sdk' && (
          <div className="space-y-4">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-3">
              {[
                { lang: 'Python', pkg: 'pip install longhun-sdk', ver: 'v2.1.0', icon: '🐍', color: 'text-yellow-400' },
                { lang: 'JavaScript', pkg: 'npm install @longhun/sdk', ver: 'v2.1.0', icon: 'JS', color: 'text-amber-400' },
                { lang: 'Rust', pkg: 'cargo add longhun-sdk', ver: 'v1.5.0', icon: '🦀', color: 'text-orange-400' },
              ].map(sdk => (
                <div key={sdk.lang} className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
                  <div className="flex items-center gap-2">
                    <span className={`text-lg font-bold ${sdk.color}`}>{sdk.icon}</span>
                    <h4 className="text-sm font-bold text-zinc-200">{sdk.lang} SDK</h4>
                  </div>
                  <p className="text-xs text-zinc-500 mt-1">{sdk.ver}</p>
                  <code className="text-[10px] text-emerald-400/70 font-mono bg-zinc-900/50 p-1.5 rounded block mt-2">{sdk.pkg}</code>
                  <button className="mt-2 text-[10px] text-sky-400 hover:text-sky-300 transition-colors">查看文档 →</button>
                </div>
              ))}
            </div>

            <div className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
              <h4 className="text-xs font-medium text-zinc-400 mb-2">Python 快速开始</h4>
              <pre className="text-[10px] text-zinc-500 font-mono bg-zinc-950/50 p-3 rounded overflow-x-auto leading-relaxed">
{`from longhun import Client, AIModel

# 初始化客户端
client = Client(api_key="your-key", base_url="http://api.longhun.local/v1")

# 选择模型
model = client.models.select("longhun-core-v5")

# 启动对话（自动带DNA追溯）
response = model.chat("你好，龍魂", enable_dna_trace=True, audit_level="strict")

print(response.content)   # 回复内容
print(response.dna)       # DNA追溯码
print(response.audit)     # 🟢🟡🔴 三色审计`}
              </pre>
            </div>
          </div>
        )}

        {activeTab === 'protocol' && (
          <div className="space-y-4 max-w-2xl">
            {[
              { title: '龍魂君子协议', desc: '所有接入龍魂系统的开发者必须遵守君子协议。核心原则：不抢首创、不做翻译不做创新、完全自主、明确标签、永远在线。', license: 'CC BY-NC-SA 4.0' },
              { title: 'AI Truth Protocol', desc: '所有AI输出必须附带真相标记。标记级别：已验证🟢、高置信🟢、中置信🟡、低置信🟡、未验证🔴、存疑🔴。', license: '内置协议' },
              { title: 'DNA追溯规范', desc: '每个模块、每次提交、每个动作都携带唯一DNA签名。格式：#龍芯⚡️{YYYY-MM-DD}-{项目}-{模块}-{版本}', license: '强制规范' },
              { title: '通心译双语规范', desc: '中文内容优先，英文并行输出。五大铁律：中文活着英文也活着、不是镜像是共鸣、比喻优先于公式、古今打通、永远在线永远迭代。', license: '内置协议' },
              { title: '数据主权声明', desc: '用户数据主权归用户个人所有。龍魂系统仅作为基础设施提供方，不参与内容运营，不做数据贩子，不做监控。', license: '宪法层' },
              { title: '接入审核流程', desc: '1.提交申请 → 2.GPG身份验证 → 3.三层监督审查 → 4.DNA授权码生成 → 5.API密钥发放 → 6.接入完成', license: '操作流程' },
            ].map(item => (
              <div key={item.title} className="p-4 rounded-lg border border-zinc-800/50 bg-zinc-900/20">
                <div className="flex items-center justify-between">
                  <h4 className="text-sm font-bold text-zinc-200">{item.title}</h4>
                  <span className="text-[10px] px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-500">{item.license}</span>
                </div>
                <p className="text-xs text-zinc-400 mt-2 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
