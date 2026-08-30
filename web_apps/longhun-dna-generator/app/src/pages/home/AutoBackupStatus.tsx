// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-203c0fd0
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import { Cloud, Server, RefreshCw, ShieldCheck, ArrowRight } from 'lucide-react'
import { Link } from 'react-router'
import SectionHeading from '@/components/SectionHeading'
import OutlineButton from '@/components/OutlineButton'

/**
 * 首页·自动化备份状态指示器
 * 三层备份拓扑 + 自愈守护状态 → 强调自动化、零人工介入
 */
export default function AutoBackupStatus() {
  return (
    <section className="px-6 py-24 md:px-12">
      <div className="mx-auto max-w-container">
        <SectionHeading
          eyebrow="AUTOMATION"
          title="自动化守护·永不掉线"
          subtitle="三层备份 · 六小时同步 · 每小时自愈 · 异常自动重启 · Bark 实时推送"
        />

        {/* 拓扑指示器 */}
        <div className="mt-14 grid gap-6 md:grid-cols-3">
          {[
            {
              icon: <RefreshCw className="h-5 w-5 text-gold" />,
              label: '百度云BOS',
              status: '每 6h 增量同步',
              detail: '北京节点 · 增量仅传变更 · 保留90天',
              color: 'border-gold',
            },
            {
              icon: <Server className="h-5 w-5 text-gold" />,
              label: '鲲鹏镜像',
              status: '每日全量同步',
              detail: '119.13.90.27 · 保留7天本地快照',
              color: 'border-gold-dim',
            },
            {
              icon: <ShieldCheck className="h-5 w-5 text-gold" />,
              label: '自愈守护',
              status: '每小时自动巡检',
              detail: '异常自动重启 · Bark + 飞书推送',
              color: 'border-gold-dim',
            },
          ].map((item, i) => (
            <div
              key={i}
              className={`hairline group flex flex-col items-center gap-4 bg-ink-2 p-8 text-center transition-colors duration-300 hover:bg-ink-3`}
            >
              <span className={`flex h-14 w-14 items-center justify-center rounded-none border ${item.color} bg-ink`}>
                {item.icon}
              </span>
              <div>
                <h3 className="font-serif text-[16px] font-bold text-paper">{item.label}</h3>
                <p className="mt-1 font-mono text-[13px] text-gold">{item.status}</p>
              </div>
              <p className="text-[13px] leading-[1.8] text-paper-dim">{item.detail}</p>
            </div>
          ))}
        </div>

        {/* CTA */}
        <div className="mt-12 flex flex-wrap items-center justify-center gap-6">
          <OutlineButton to="/storage">
            <Cloud className="mr-2 h-4 w-4" />
            查看云端备份
          </OutlineButton>
          <OutlineButton to="/health">
            <ShieldCheck className="mr-2 h-4 w-4" />
            系统健康状态
          </OutlineButton>
          <Link
            to="/api"
            className="group inline-flex items-center gap-2 text-[14px] text-paper-dim transition-colors hover:text-gold"
          >
            <ArrowRight className="h-4 w-4 transition-transform group-hover:translate-x-1" />
            API 接入
          </Link>
        </div>
      </div>
    </section>
  )
}
