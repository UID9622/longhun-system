// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-aa16911b
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import PageHero from '@/components/PageHero'
import SectionHeading from '@/components/SectionHeading'
import SealTag from '@/components/SealTag'
import { Cloud, HardDrive, Database, Shield, ArrowRight, Server, RefreshCw, CheckCircle2, AlertTriangle } from 'lucide-react'

/**
 * 龍魂·云存储 `/storage` — 数据主权基础设施
 * 自动化备份·多云冗余·本地优先·加密传输
 */
export default function Storage() {
  return (
    <>
      <PageHero
        eyebrow="INFRASTRUCTURE"
        title="云存储·数据主权"
        subtitle="百度云BOS + 鲲鹏双写 · 增量自动备份 · 端到端国密加密 · 环境变量独享 · 六小时自检 · 境内节点闭环"
        seal="卷捌 / STORAGE"
      />

      {/* 存储拓扑概览 */}
      <section className="px-6 py-24 md:px-12">
        <div className="mx-auto max-w-container">
          <SectionHeading
            eyebrow="ARCHITECTURE"
            title="三层存储拓扑"
            subtitle="本地优先·云上加密·鲲鹏镜像——三重保障，数据永不丢失"
          />
          <div className="mt-16 grid gap-8 md:grid-cols-3">
            {[
              {
                icon: <HardDrive className="h-7 w-7 text-gold" />,
                title: 'L1 · 本地存储',
                desc: 'Mac本地 `/longhun-system/` · 实时读写 · 离线可用 · 性能优先',
                items: ['代码/协议/数据全量驻留', '每天自动索引', 'GPG签名覆盖全部文件'],
              },
              {
                icon: <Cloud className="h-7 w-7 text-gold" />,
                title: 'L2 · 百度云BOS',
                desc: '北京节点(bj)· 增量同步 · 端侧国密加密 · 仅存密文',
                items: ['每6小时自动备份', '保留90天历史版本', '过期自动清理'],
              },
              {
                icon: <Server className="h-7 w-7 text-gold" />,
                title: 'L3 · 鲲鹏镜像',
                desc: '华为云 119.13.90.27 · 每日全量同步 · 本地冷备',
                items: ['每日定时同步', '保留7天本地快照', '一键恢复脚本'],
              },
            ].map((c, i) => (
              <div
                key={i}
                className="hairline group flex flex-col gap-5 bg-ink-2 p-8 transition-colors duration-300 hover:bg-ink-3"
              >
                <div className="flex items-center gap-4">
                  <span className="flex h-12 w-12 items-center justify-center rounded-none border border-line bg-ink">
                    {c.icon}
                  </span>
                  <h3 className="font-serif text-[18px] font-bold text-paper">{c.title}</h3>
                </div>
                <p className="text-[14px] leading-[1.8] text-paper-dim">{c.desc}</p>
                <ul className="flex flex-col gap-2 border-t border-line pt-4">
                  {c.items.map((it, j) => (
                    <li key={j} className="flex items-start gap-2 text-[13px] text-paper-faint">
                      <CheckCircle2 className="mt-0.5 h-3.5 w-3.5 shrink-0 text-gold-dim" />
                      {it}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 备份指令 */}
      <section className="hairline-t px-6 py-24 md:px-12">
        <div className="mx-auto max-w-container">
          <SectionHeading
            eyebrow="COMMANDS"
            title="一键备份与恢复"
            subtitle="自然语言即可触发，无需记忆命令。AI 代理自动执行"
          />
          <div className="mt-16 grid gap-6 md:grid-cols-2">
            {[
              {
                cmd: 'lh bos backup --dirs ./data/ ./config/',
                label: '手动备份指定目录',
                icon: <Cloud className="h-5 w-5" />,
              },
              {
                cmd: 'bash deploy/scripts/cloud_backup.sh',
                label: '全量自动备份到百度云+鲲鹏',
                icon: <RefreshCw className="h-5 w-5" />,
              },
              {
                cmd: 'lh bos sync ./web_apps/',
                label: '增量同步单目录（仅传变更）',
                icon: <ArrowRight className="h-5 w-5" />,
              },
              {
                cmd: 'bash deploy/scripts/cloud_pull.sh bos 2026-08-07',
                label: '从百度云恢复指定日期备份',
                icon: <Database className="h-5 w-5" />,
              },
              {
                cmd: 'lh bos status',
                label: '查看云存储空间状态',
                icon: <Shield className="h-5 w-5" />,
              },
              {
                cmd: 'lh bos list --prefix longhun/',
                label: '列出云端全部文件',
                icon: <Server className="h-5 w-5" />,
              },
            ].map((c, i) => (
              <div key={i} className="flex items-start gap-4 bg-ink-2 p-5 transition-colors hover:bg-ink-3">
                <span className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center border border-line text-gold">
                  {c.icon}
                </span>
                <div className="min-w-0 flex-1">
                  <p className="text-[14px] text-paper">{c.label}</p>
                  <code className="mt-2 block truncate font-mono text-[12px] text-gold-dim">{c.cmd}</code>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 安全策略 */}
      <section className="hairline-t px-6 py-24 md:px-12">
        <div className="mx-auto max-w-container">
          <SectionHeading
            eyebrow="SECURITY"
            title="安全传输策略"
            subtitle="数据主权不可让渡——不上传隐私·端侧加密·境内闭环"
          />
          <div className="mt-16 grid gap-4 md:grid-cols-4">
            {[
              { label: '传输加密', value: 'HTTPS + 国密SM4', icon: <Shield className="h-5 w-5" /> },
              { label: '存储加密', value: '端侧加密·云存密文', icon: <Database className="h-5 w-5" /> },
              { label: '备份地域', value: '北京节点（境内）', icon: <Server className="h-5 w-5" /> },
              { label: '密钥管理', value: '环境变量·不入代码', icon: <AlertTriangle className="h-5 w-5" /> },
            ].map((s, i) => (
              <div key={i} className="hairline flex flex-col gap-3 bg-ink-2 p-6 text-center">
                <span className="mx-auto flex h-10 w-10 items-center justify-center border border-line text-gold-dim">
                  {s.icon}
                </span>
                <p className="eyebrow">{s.label}</p>
                <p className="text-[14px] font-semibold text-paper">{s.value}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 告警声明 */}
      <section className="hairline-t px-6 py-20 md:px-12">
        <div className="mx-auto max-w-container">
          <div className="hairline flex flex-col items-center gap-6 bg-ink-2 p-10 text-center">
            <SealTag>D1 绝密数据永不入云</SealTag>
            <p className="max-w-[640px] text-[14px] leading-[2] text-paper-faint">
              GPG 私钥 · DNA 种子 · 用户生物特征 · 家庭/财务/健康数据 —— 物理隔离，本地存储，
              永不触碰任何云端。请求即熔断。
            </p>
          </div>
        </div>
      </section>
    </>
  )
}
