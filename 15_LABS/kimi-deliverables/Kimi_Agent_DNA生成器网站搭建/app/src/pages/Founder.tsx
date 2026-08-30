// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-e9a0f0de
import { motion } from 'framer-motion'
import SealTag from '@/components/SealTag'
import ThreeNames from '@/pages/founder/ThreeNames'
import VeteranSection from '@/pages/founder/VeteranSection'
import Principles from '@/pages/founder/Principles'
import ImprintWall from '@/pages/founder/ImprintWall'
import FounderCTA from '@/pages/founder/FounderCTA'

/**
 * /founder · 创始人（founder.md）
 * S1 徽记 PageHero → S2 三个名字 → S3 老兵章 → S4 三不三为 → S5 印记墙 → S6 回响 CTA
 */
export default function Founder() {
  const title = '諸葛鑫'

  return (
    <>
      {/* S1 · PageHero（founder.md S1，64vh 全站最庄重页头）—— 纯 Framer Motion 域 */}
      <header
        className="relative flex min-h-[64vh] flex-col items-center overflow-hidden"
        aria-label="创始人页头"
      >
        {/* bagua-ring.svg 70vh，5% 透明，200s/圈极缓 */}
        <img
          src="/bagua-ring.svg"
          alt=""
          className="pointer-events-none absolute left-1/2 top-1/2 aspect-square h-[70vh] -translate-x-1/2 -translate-y-1/2 animate-spin-slow opacity-[0.05]"
          style={{ animationDuration: '200s' }}
          aria-hidden="true"
        />
        <div
          className="pointer-events-none absolute inset-0"
          style={{
            background: 'radial-gradient(ellipse at 50% 55%, transparent 25%, rgba(8,7,6,0.9) 100%)',
          }}
          aria-hidden="true"
        />
        {/* 顶部留白避让 Navbar */}
        <div className="h-[88px] shrink-0" aria-hidden="true" />

        <div className="relative z-10 mx-auto flex w-full max-w-container flex-1 flex-col items-center justify-end px-6 pb-12 text-center md:px-12">
          {/* 军规徽记：弹性入场 + 常驻金光呼吸 */}
          <motion.div
            initial={{ scale: 0.7, opacity: 0, rotate: -10 }}
            animate={{ scale: 1, opacity: 1, rotate: 0 }}
            transition={{ type: 'spring', stiffness: 140, damping: 14, delay: 0.1 }}
          >
            <motion.img
              src="/founder-emblem.svg"
              alt="龍魂军规徽记 · 9622"
              width={240}
              height={240}
              className="h-[180px] w-[180px] md:h-[240px] md:w-[240px]"
              animate={{
                filter: [
                  'drop-shadow(0 0 4px rgba(201,162,39,0.10))',
                  'drop-shadow(0 0 12px rgba(201,162,39,0.25))',
                  'drop-shadow(0 0 4px rgba(201,162,39,0.10))',
                ],
              }}
              transition={{ duration: 4, repeat: Infinity, ease: 'easeInOut' }}
            />
          </motion.div>

          <motion.span
            className="eyebrow mt-8"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.5 }}
          >
            SCROLL VI · THE FOUNDER
          </motion.span>

          {/* H1 三字逐字 y:60→0 stagger 0.15s */}
          <h1
            className="mt-6 font-serif font-black leading-[1.1] tracking-[0.05em] text-paper text-[clamp(48px,7vw,96px)]"
            aria-label={title}
          >
            {Array.from(title).map((ch, i) => (
              <motion.span
                key={i}
                className="inline-block"
                aria-hidden="true"
                initial={{ y: 60, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ duration: 0.7, delay: 0.3 + i * 0.15, ease: [0.22, 1, 0.36, 1] }}
              >
                {ch}
              </motion.span>
            ))}
          </h1>

          <motion.p
            className="mt-5 font-serif text-[22px] font-bold tracking-[0.2em] text-gold"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 + 0.45, ease: [0.22, 1, 0.36, 1] }}
          >
            龍芯北辰 · Lucky
          </motion.p>
          <motion.p
            className="mt-4 font-mono text-[13px] tracking-[0.08em] text-paper-dim"
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.6 + 0.6, ease: [0.22, 1, 0.36, 1] }}
          >
            2008 年退伍老兵（服役 2 年） · CNSH 发起人 · 三才算法奠基者
          </motion.p>
        </div>

        <div className="hairline-b relative z-10 w-full">
          <div className="mx-auto flex w-full max-w-container justify-end px-6 pb-4 md:px-12">
            <SealTag>卷六 / FOUNDER</SealTag>
          </div>
        </div>
      </header>

      <ThreeNames />
      <VeteranSection />
      <Principles />
      <ImprintWall />
      <FounderCTA />
    </>
  )
}
