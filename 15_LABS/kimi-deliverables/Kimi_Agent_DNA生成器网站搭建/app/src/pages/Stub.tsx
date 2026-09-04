import PageHero from '@/components/PageHero'

interface Props {
  eyebrow: string
  title: string
  subtitle: string
  seal: string
}

/** 子页面占位桩 —— 路由可达，正式页面由后续页面代理实现 */
export default function Stub({ eyebrow, title, subtitle, seal }: Props) {
  return (
    <>
      <PageHero eyebrow={eyebrow} title={title} subtitle={subtitle} seal={seal} />
      <section className="mx-auto flex w-full max-w-container flex-col items-center gap-6 px-6 py-32 text-center md:px-12">
        <p className="font-mono text-[13px] tracking-[0.3em] text-gold-dim">建设中 · UNDER SEAL</p>
        <p className="max-w-[560px] text-[15px] leading-[1.9] text-paper-dim">
          此卷正在篆刻。干支不息，工匠未歇。
        </p>
      </section>
    </>
  )
}
