import ProtocolHero from '@/pages/protocol/ProtocolHero'
import NavSpine from '@/pages/protocol/NavSpine'
import P0Section from '@/pages/protocol/P0Section'
import P1Section from '@/pages/protocol/P1Section'
import P2Section from '@/pages/protocol/P2Section'
import P3Section from '@/pages/protocol/P3Section'
import P4Section from '@/pages/protocol/P4Section'
import SignSection from '@/pages/protocol/SignSection'

/**
 * 龍魂协议 `/protocol`（design/protocol.md）
 * PageHero → 层级导航脊（sticky）→ P0 焊死底座 → P1 核心宪法 → P2 系统规则
 * → P3 区域适配 → P4 用户自定义 → 签署区（pin）
 */
export default function Protocol() {
  return (
    <>
      <ProtocolHero />
      <NavSpine />
      <P0Section />
      <P1Section />
      <P2Section />
      <P3Section />
      <P4Section />
      <SignSection />
    </>
  )
}
