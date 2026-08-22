import Hero from '@/pages/home/Hero'
import ClockBand from '@/pages/home/ClockBand'
import Manifesto from '@/pages/home/Manifesto'
import ProtocolPyramid from '@/pages/home/ProtocolPyramid'
import MatrixPreview from '@/pages/home/MatrixPreview'
import WorksRail from '@/pages/home/WorksRail'
import TimelinePreview from '@/pages/home/TimelinePreview'
import StatsSection from '@/pages/home/StatsSection'
import FounderCard from '@/pages/home/FounderCard'
import FinalCTA from '@/pages/home/FinalCTA'

/**
 * 首页 `/`（home.md）
 * Hero → 干支时钟带 → 宣言 → 协议五层 → 矩阵预告 → 作品带 → 远征预告 → CSDN 数据 → 创始人卡 → 终章 CTA
 */
export default function Home() {
  return (
    <>
      <Hero />
      <ClockBand />
      <Manifesto />
      <ProtocolPyramid />
      <MatrixPreview />
      <WorksRail />
      <TimelinePreview />
      <StatsSection />
      <FounderCard />
      <FinalCTA />
    </>
  )
}
