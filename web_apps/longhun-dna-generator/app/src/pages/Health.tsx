// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-58bfb878
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import PageHero from '@/components/PageHero'
import SectionHeading from '@/components/SectionHeading'
import SealTag from '@/components/SealTag'
import { Activity, Server, ShieldCheck, Zap, Clock, Gauge, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react'

/**
 * 龍魂·系统健康 `/health` — 部署状态 · 引擎监护 · 自愈可视化
 */
export default function Health() {
  return (
    <>
      <PageHero
        eyebrow="DASHBOARD"
        title="系统健康·部署状态"
        subtitle="Mac 52 launchd + 鲲鹏 12 systemd · 每小时自愈巡检 · 异常自动重启 · Bark 实时推送"
        seal="卷玖 / HEALTH"
      />

      {/* 双节点总览 */}
      <section className="px-6 py-24 md:px-12">
        <div className="mx-auto max-w-container">
          <div className="grid gap-8 md:grid-cols-2">
            {[
              {
                name: 'Mac 本地节点',
                host: 'macOS · Apple Silicon',
                services: '52 launchd',
                uptime: '自愈守护运行中',
                status: '🟢 正常',
                items: [
                  { label: '搜索引擎', port: 9631, status: true },
                  { label: '记忆服务', port: 8771, status: true },
                  { label: '知识中枢', port: 8766, status: true },
                  { label: 'AI Hub v2.0', port: 8772, status: true },
                  { label: '多智能体框架', port: 8770, status: true },
                  { label: '三色审计SDK', port: 8775, status: true },
                ],
              },
              {
                name: '鲲鹏节点',
                host: '119.13.90.27 · openEuler',
                services: '12 systemd + K3s v1.36.3',
                uptime: 'K3s集群正常运行',
                status: '🟢 正常',
                items: [
                  { label: 'API网关', port: 443, status: true },
                  { label: 'K3s控制平面', port: 6443, status: true },
                  { label: 'Nginx反向代理', port: 80, status: true },
                  { label: 'Let\'s Encrypt证书', port: 'TLS', status: true },
                  { label: 'DNS解析', domain: 'uid9622.cn', status: true },
                  { label: 'Bark告警推送', port: 8080, status: true },
                ],
              },
            ].map((node, i) => (
              <div key={i} className="hairline flex flex-col bg-ink-2">
                {/* 节点头 */}
                <div className="flex items-center justify-between border-b border-line p-6">
                  <div>
                    <h3 className="font-serif text-[20px] font-bold text-paper">{node.name}</h3>
                    <p className="mt-1 text-[13px] text-paper-dim">{node.host}</p>
                  </div>
                  <span className="flex items-center gap-2 font-mono text-[13px] text-gold">
                    <Activity className="h-4 w-4" /> {node.status}
                  </span>
                </div>

                {/* 服务列表 */}
                <div className="flex flex-col gap-3 p-6">
                  {node.items.map((svc, j) => (
                    <div key={j} className="flex items-center justify-between border-b border-line/50 pb-3 last:border-0 last:pb-0">
                      <div className="flex items-center gap-3">
                        {svc.status ? (
                          <CheckCircle2 className="h-4 w-4 text-gold" />
                        ) : (
                          <XCircle className="h-4 w-4 text-vermilion" />
                        )}
                        <span className="text-[14px] text-paper">{svc.label}</span>
                      </div>
                      <span className="font-mono text-[12px] text-paper-faint">
                        {svc.port ? `:${svc.port}` : svc.domain}
                      </span>
                    </div>
                  ))}
                </div>

                {/* 底部摘要 */}
                <div className="hairline-t mt-auto flex items-center justify-between p-4 text-[12px]">
                  <span className="text-paper-faint">{node.services}</span>
                  <span className="text-paper-dim">{node.uptime}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 自愈引擎 */}
      <section className="hairline-t px-6 py-24 md:px-12">
        <div className="mx-auto max-w-container">
          <SectionHeading
            eyebrow="AUTO-HEAL"
            title="自愈策略"
            subtitle="异常检测 → 自动重启 → 健康上报 → Bark 推送。你睡觉它也在跑"
          />
          <div className="mt-16 grid gap-6 md:grid-cols-3">
            {[
              {
                icon: <Zap className="h-6 w-6 text-gold" />,
                title: '每小时自动巡检',
                desc: '所有 launchd/systemd 服务状态检查 · 端口可达性探测 · 响应时间监控',
              },
              {
                icon: <ShieldCheck className="h-6 w-6 text-gold" />,
                title: '异常自动重启',
                desc: '连续3次失败 → 自动重启服务 · 重启失败 → 升级告警 · Bark + 飞书双通道',
              },
              {
                icon: <Gauge className="h-6 w-6 text-gold" />,
                title: '四级熔断联动',
                desc: 'L3行为级自动恢复 · L2人格级手动解锁 · L1数据级UID9622签章 · L0不可恢复',
              },
            ].map((h, i) => (
              <div key={i} className="hairline flex flex-col gap-4 bg-ink-2 p-8 transition-colors hover:bg-ink-3">
                <span className="flex h-12 w-12 items-center justify-center rounded-none border border-line bg-ink">
                  {h.icon}
                </span>
                <h3 className="font-serif text-[16px] font-bold text-paper">{h.title}</h3>
                <p className="text-[14px] leading-[1.9] text-paper-dim">{h.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 快速命令 */}
      <section className="hairline-t px-6 py-24 md:px-12">
        <div className="mx-auto max-w-container">
          <SectionHeading
            eyebrow="COMMANDS"
            title="快速诊断"
            subtitle="自然语言即可触发。无需记忆命令"
          />
          <div className="mt-12 grid gap-4 md:grid-cols-3">
            {[
              { cmd: 'lh status', desc: '全系统状态概览' },
              { cmd: 'lh audit', desc: '三色审计扫描' },
              { cmd: 'bash deploy/scripts/health_check.sh', desc: '健康检查+Bark推送' },
              { cmd: 'lh bos status', desc: '云存储空间状态' },
              { cmd: 'python3 bin/lh_align_checker.py', desc: '代码对齐检查' },
              { cmd: 'python3 bin/lh_deben_audit.py scan', desc: '德本审计五问' },
            ].map((c, i) => (
              <div key={i} className="hairline flex flex-col gap-3 bg-ink-2 p-5 transition-colors hover:bg-ink-3">
                <p className="text-[14px] text-paper">{c.desc}</p>
                <code className="font-mono text-[12px] text-gold-dim">{c.cmd}</code>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 监控声明 */}
      <section className="hairline-t px-6 py-20 md:px-12">
        <div className="mx-auto max-w-container">
          <div className="hairline flex items-center justify-center gap-6 bg-ink-2 p-10">
            <AlertTriangle className="h-5 w-5 text-gold-dim" />
            <SealTag>主动观察·不被动等命令</SealTag>
          </div>
        </div>
      </section>
    </>
  )
}
