import WorksHero from '@/pages/works/WorksHero'
import SevenScrolls from '@/pages/works/SevenScrolls'
import GentlemanAccord from '@/pages/works/GentlemanAccord'
import CSDNWall from '@/pages/works/CSDNWall'
import OathSection from '@/pages/works/OathSection'

/**
 * 作品开源 `/works`（works.md）
 * PageHero → 七器长卷 → 君子协议双语对照 → CSDN 数据墙 → 开源誓约
 */
export default function Works() {
  return (
    <>
      <WorksHero />
      <SevenScrolls />
      <GentlemanAccord />
      <CSDNWall />
      <OathSection />
    </>
  )
}
