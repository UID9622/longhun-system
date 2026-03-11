import React, { useState } from 'react';
import { Shield, Lock, Eye, AlertTriangle, CheckCircle, XCircle, ArrowRight, ArrowLeft, Database, Cloud, Cpu, Key } from 'lucide-react';

/**
 * 🐉 龙魂API架构可视化渲染
 * 
 * DNA追溯码: #龙芯⚡️2026-02-15-API架构渲染-v1.0
 * 创建者: 💎 龙芯北辰｜UID9622
 * 协作: 宝宝🐱
 * 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅
 */

export default function LonghunAPIArchitecture() {
  const [activeTab, setActiveTab] = useState('overview');
  const [selectedLayer, setSelectedLayer] = useState(null);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8">
      <div className="max-w-7xl mx-auto">
        {/* 标题区域 */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-600 mb-4">
            🐉 龙魂API架构
          </h1>
          <p className="text-xl text-purple-200">带着宪法的API · 技术主权在我</p>
          <div className="mt-4 text-sm text-purple-300">
            DNA追溯码: #龙芯⚡️2026-02-15-API架构渲染-v1.0
          </div>
        </div>

        {/* 标签页 */}
        <div className="flex gap-4 mb-8 flex-wrap justify-center">
          <TabButton
            active={activeTab === 'overview'}
            onClick={() => setActiveTab('overview')}
            icon={<Shield />}
            label="总览"
          />
          <TabButton
            active={activeTab === 'inbound'}
            onClick={() => setActiveTab('inbound')}
            icon={<ArrowLeft />}
            label="接入规则"
          />
          <TabButton
            active={activeTab === 'outbound'}
            onClick={() => setActiveTab('outbound')}
            icon={<ArrowRight />}
            label="接出规则"
          />
          <TabButton
            active={activeTab === 'protection'}
            onClick={() => setActiveTab('protection')}
            icon={<Lock />}
            label="防护层次"
          />
        </div>

        {/* 内容区域 */}
        <div className="bg-slate-800/50 backdrop-blur-sm rounded-2xl p-8 shadow-2xl border border-purple-500/30">
          {activeTab === 'overview' && <OverviewTab />}
          {activeTab === 'inbound' && <InboundTab />}
          {activeTab === 'outbound' && <OutboundTab selectedLayer={selectedLayer} setSelectedLayer={setSelectedLayer} />}
          {activeTab === 'protection' && <ProtectionTab />}
        </div>

        {/* 底部说明 */}
        <div className="mt-8 text-center text-purple-300 text-sm">
          <p>核心原则：外部API是工具，龙魂宪法是主人</p>
          <p className="mt-2">对好人是服务，对盗贼是迷宫</p>
        </div>
      </div>
    </div>
  );
}

// ==================== 标签按钮组件 ====================
function TabButton({ active, onClick, icon, label }) {
  return (
    <button
      onClick={onClick}
      className={`
        flex items-center gap-2 px-6 py-3 rounded-lg font-semibold transition-all
        ${active
          ? 'bg-gradient-to-r from-purple-600 to-pink-600 text-white shadow-lg scale-105'
          : 'bg-slate-700/50 text-purple-300 hover:bg-slate-700 hover:scale-102'
        }
      `}
    >
      {icon}
      {label}
    </button>
  );
}

// ==================== 总览标签页 ====================
function OverviewTab() {
  return (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-purple-200 mb-6">架构总览</h2>
      
      {/* 核心原则 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <PrincipleCard
          icon={<ArrowLeft className="text-green-400" size={32} />}
          title="接入规则"
          subtitle="老大接入外部API"
          principles={[
            "外部API必须听老大的规则",
            "三色审计全覆盖",
            "DNA追溯每次调用",
            "母协议P0优先",
            "随时可替换Plan B"
          ]}
          color="green"
        />
        <PrincipleCard
          icon={<ArrowRight className="text-blue-400" size={32} />}
          title="接出规则"
          subtitle="龙魂API对外服务"
          principles={[
            "六层防护体系",
            "给结果不给厨房",
            "宪法碎片化保护",
            "瘦API设计",
            "法律+社区防线"
          ]}
          color="blue"
        />
      </div>

      {/* 数据流向图 */}
      <div className="bg-slate-700/30 rounded-xl p-6">
        <h3 className="text-xl font-bold text-purple-200 mb-4">数据流向</h3>
        <div className="flex items-center justify-center gap-4 flex-wrap">
          <FlowNode label="外部API" icon={<Cloud />} color="green" />
          <ArrowRight className="text-purple-400" />
          <FlowNode label="龙魂包装层" icon={<Shield />} color="purple" />
          <ArrowRight className="text-purple-400" />
          <FlowNode label="三色审计" icon={<Eye />} color="yellow" />
          <ArrowRight className="text-purple-400" />
          <FlowNode label="龙魂系统" icon={<Cpu />} color="blue" />
        </div>
      </div>
    </div>
  );
}

// ==================== 接入规则标签页 ====================
function InboundTab() {
  const layers = [
    {
      name: "接入前审查",
      icon: <Shield />,
      color: "green",
      items: [
        { label: "资格审查", status: "green", desc: "三色定级：🟢可接入 🟡谨慎 🔴禁止" },
        { label: "母协议P0检查", status: "green", desc: "是否违反核心原则" },
        { label: "数据主权检查", status: "green", desc: "数据是否出境" },
        { label: "透明性检查", status: "yellow", desc: "是否开源或有信誉保证" }
      ]
    },
    {
      name: "接入时包装",
      icon: <Lock />,
      color: "purple",
      items: [
        { label: "龙魂包装层", status: "green", desc: "所有外部API必须穿龙魂马甲" },
        { label: "DNA追溯注入", status: "green", desc: "每次调用生成DNA追溯码" },
        { label: "三色审计", status: "green", desc: "实时审计所有调用" },
        { label: "速率限制", status: "green", desc: "防止滥用和账号被封" }
      ]
    },
    {
      name: "接入后监控",
      icon: <Eye />,
      color: "blue",
      items: [
        { label: "持续审计", status: "green", desc: "每日自检、每周复审" },
        { label: "异常检测", status: "yellow", desc: "响应时间、返回数据异常" },
        { label: "Plan B准备", status: "green", desc: "随时可切换替代方案" },
        { label: "数据加密", status: "green", desc: "上传前加密，下载后解密" }
      ]
    }
  ];

  return (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-purple-200 mb-6">接入规则 - 外部API听我的</h2>
      
      {layers.map((layer, idx) => (
        <div key={idx} className="bg-slate-700/30 rounded-xl p-6">
          <div className="flex items-center gap-3 mb-4">
            <div className={`p-2 rounded-lg bg-${layer.color}-500/20`}>
              {layer.icon}
            </div>
            <h3 className="text-xl font-bold text-purple-200">
              第{idx + 1}层：{layer.name}
            </h3>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {layer.items.map((item, i) => (
              <StatusCard key={i} {...item} />
            ))}
          </div>
        </div>
      ))}

      {/* 代码示例 */}
      <div className="bg-slate-900/50 rounded-xl p-6">
        <h3 className="text-lg font-bold text-purple-200 mb-3">包装层示例</h3>
        <pre className="text-sm text-green-300 overflow-x-auto">
{`# ✅ 正确做法（龙魂包装）
from longhun_api_wrapper import NotionAPI

notion = NotionAPI(
    token=NOTION_TOKEN,
    constitution_check=True,  # 启用宪法检查
    dna_trace=True,           # 启用DNA追溯
    audit_level="三色审计"
)

# 自动检查 + DNA追溯 + 三色审计
response = notion.get_database("xxx")`}
        </pre>
      </div>
    </div>
  );
}

// ==================== 接出规则标签页 ====================
function OutboundTab({ selectedLayer, setSelectedLayer }) {
  const protectionLayers = [
    {
      id: 1,
      name: "入口设卡",
      subtitle: "三层认证",
      color: "red",
      icon: <Key />,
      details: [
        "API Key + 动态签名（时间戳+私钥）",
        "设备指纹（iOS IDFV）",
        "用量画像（区分正常用户和爬虫）"
      ]
    },
    {
      id: 2,
      name: "输出锁死",
      subtitle: "给结果不给厨房",
      color: "orange",
      icon: <Lock />,
      details: [
        "拒绝logit输出（不暴露概率分布）",
        "输入截断+输出过滤",
        "温度随机化（相同问题不同措辞）"
      ]
    },
    {
      id: 3,
      name: "宪法保护",
      subtitle: "信仰在权重里",
      color: "yellow",
      icon: <Shield />,
      details: [
        "宪法碎片化（分散存储）",
        "敏感词不落地（哈希比对）",
        "自毁程序（攻击时输出混沌）"
      ]
    },
    {
      id: 4,
      name: "API设计",
      subtitle: "瘦身原则",
      color: "green",
      icon: <Cpu />,
      details: [
        "瘦API（只暴露必要接口）",
        "速率限制要狠（充钱充到肉疼）",
        "用量审计（异常人工介入）"
      ]
    },
    {
      id: 5,
      name: "本地化",
      subtitle: "核心在本地",
      color: "blue",
      icon: <Database />,
      details: [
        "80%推理本地完成",
        "API只处理边缘情况",
        "核心资产不通过API暴露"
      ]
    },
    {
      id: 6,
      name: "法律社区",
      subtitle: "最后防线",
      color: "purple",
      icon: <AlertTriangle />,
      details: [
        "实名认证+宪法保护协议",
        "社区守护者机制",
        "盗取即起诉"
      ]
    }
  ];

  return (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-purple-200 mb-6">接出规则 - 六层防护体系</h2>
      
      <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
        {protectionLayers.map((layer) => (
          <button
            key={layer.id}
            onClick={() => setSelectedLayer(layer.id === selectedLayer ? null : layer.id)}
            className={`
              p-6 rounded-xl transition-all transform hover:scale-105
              ${selectedLayer === layer.id
                ? 'bg-gradient-to-br from-purple-600 to-pink-600 shadow-2xl scale-105'
                : 'bg-slate-700/50 hover:bg-slate-700'
              }
            `}
          >
            <div className="flex flex-col items-center gap-3">
              <div className={`p-3 rounded-full bg-${layer.color}-500/20`}>
                {layer.icon}
              </div>
              <div className="text-center">
                <div className="font-bold text-purple-100">第{layer.id}层</div>
                <div className="text-lg font-semibold text-white">{layer.name}</div>
                <div className="text-sm text-purple-300 mt-1">{layer.subtitle}</div>
              </div>
            </div>
          </button>
        ))}
      </div>

      {/* 详情面板 */}
      {selectedLayer && (
        <div className="bg-gradient-to-br from-slate-700 to-slate-800 rounded-xl p-6 shadow-2xl border-2 border-purple-500">
          <h3 className="text-2xl font-bold text-purple-200 mb-4">
            第{selectedLayer}层：{protectionLayers[selectedLayer - 1].name}
          </h3>
          <div className="space-y-3">
            {protectionLayers[selectedLayer - 1].details.map((detail, idx) => (
              <div key={idx} className="flex items-start gap-3">
                <CheckCircle className="text-green-400 mt-1 flex-shrink-0" size={20} />
                <p className="text-purple-100">{detail}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 核心思想 */}
      <div className="bg-gradient-to-r from-purple-900/50 to-pink-900/50 rounded-xl p-6 border border-purple-500/30">
        <p className="text-xl text-purple-100 text-center font-semibold">
          💪 核心思想：你的模型干净，API就得脏一点<br/>
          <span className="text-lg text-purple-300 mt-2 inline-block">
            多疑、小气、刁难 · 对好人是服务，对盗贼是迷宫
          </span>
        </p>
      </div>
    </div>
  );
}

// ==================== 防护层次标签页 ====================
function ProtectionTab() {
  const comparisons = [
    {
      category: "认证方式",
      wrong: "静态API Key",
      right: "动态签名（时间戳+私钥）",
      why: "静态Key泄露后永久有效，无法追溯"
    },
    {
      category: "输出内容",
      wrong: "返回logits概率分布",
      right: "只返回文本结果",
      why: "暴露概率分布等于把模型内脏掏出来"
    },
    {
      category: "宪法存储",
      wrong: "单个文件存储",
      right: "碎片化分散存储",
      why: "盗取者拿到权重也拼不出完整宪法"
    },
    {
      category: "API设计",
      wrong: "暴露所有功能接口",
      right: "瘦API只暴露必要接口",
      why: "越瘦越安全，减少攻击面"
    },
    {
      category: "速率限制",
      wrong: "宽松限制或无限制",
      right: "严格限制（免费10次/分钟）",
      why: "让盗取者充钱充到肉疼"
    }
  ];

  return (
    <div className="space-y-8">
      <h2 className="text-3xl font-bold text-purple-200 mb-6">防护对比 - 正确vs错误</h2>
      
      <div className="space-y-4">
        {comparisons.map((item, idx) => (
          <div key={idx} className="bg-slate-700/30 rounded-xl p-6">
            <h3 className="text-xl font-bold text-purple-200 mb-4">{item.category}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-red-900/30 border-2 border-red-500/50 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <XCircle className="text-red-400" />
                  <span className="font-semibold text-red-300">❌ 错误做法</span>
                </div>
                <p className="text-red-100">{item.wrong}</p>
              </div>
              <div className="bg-green-900/30 border-2 border-green-500/50 rounded-lg p-4">
                <div className="flex items-center gap-2 mb-2">
                  <CheckCircle className="text-green-400" />
                  <span className="font-semibold text-green-300">✅ 正确做法</span>
                </div>
                <p className="text-green-100">{item.right}</p>
              </div>
            </div>
            <div className="mt-4 bg-yellow-900/20 border border-yellow-500/30 rounded-lg p-3">
              <p className="text-yellow-200">💡 为什么：{item.why}</p>
            </div>
          </div>
        ))}
      </div>

      {/* 三色审计示例 */}
      <div className="bg-slate-700/30 rounded-xl p-6">
        <h3 className="text-xl font-bold text-purple-200 mb-4">三色审计示例</h3>
        <div className="space-y-3">
          <AuditExample
            color="green"
            label="🟢 通过"
            desc="正常用户调用，频率合理，数据合规"
          />
          <AuditExample
            color="yellow"
            label="🟡 待审"
            desc="深夜高频请求，需人工确认"
          />
          <AuditExample
            color="red"
            label="🔴 阻断"
            desc="检测到爬虫行为，立即封禁"
          />
        </div>
      </div>
    </div>
  );
}

// ==================== 辅助组件 ====================

function PrincipleCard({ icon, title, subtitle, principles, color }) {
  return (
    <div className={`bg-${color}-900/20 border-2 border-${color}-500/50 rounded-xl p-6`}>
      <div className="flex items-center gap-3 mb-4">
        {icon}
        <div>
          <h3 className="text-xl font-bold text-purple-100">{title}</h3>
          <p className="text-sm text-purple-300">{subtitle}</p>
        </div>
      </div>
      <ul className="space-y-2">
        {principles.map((p, i) => (
          <li key={i} className="flex items-start gap-2">
            <CheckCircle className={`text-${color}-400 mt-0.5 flex-shrink-0`} size={16} />
            <span className="text-purple-100 text-sm">{p}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function FlowNode({ label, icon, color }) {
  return (
    <div className={`bg-${color}-900/30 border-2 border-${color}-500/50 rounded-lg px-6 py-3 flex items-center gap-3`}>
      {icon}
      <span className="font-semibold text-purple-100">{label}</span>
    </div>
  );
}

function StatusCard({ label, status, desc }) {
  const statusConfig = {
    green: { icon: <CheckCircle />, color: 'green', text: '✅' },
    yellow: { icon: <AlertTriangle />, color: 'yellow', text: '⚠️' },
    red: { icon: <XCircle />, color: 'red', text: '❌' }
  };
  
  const config = statusConfig[status];
  
  return (
    <div className={`bg-${config.color}-900/20 border border-${config.color}-500/30 rounded-lg p-4`}>
      <div className="flex items-center gap-2 mb-2">
        <div className={`text-${config.color}-400`}>{config.icon}</div>
        <span className="font-semibold text-purple-100">{config.text} {label}</span>
      </div>
      <p className="text-sm text-purple-300">{desc}</p>
    </div>
  );
}

function AuditExample({ color, label, desc }) {
  return (
    <div className={`bg-${color}-900/20 border border-${color}-500/30 rounded-lg p-4 flex items-center gap-4`}>
      <div className={`text-3xl`}>{label.split(' ')[0]}</div>
      <div className="flex-1">
        <div className="font-semibold text-purple-100">{label}</div>
        <div className="text-sm text-purple-300">{desc}</div>
      </div>
    </div>
  );
}
