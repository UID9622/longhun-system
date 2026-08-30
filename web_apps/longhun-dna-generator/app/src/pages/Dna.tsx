// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-4a05d632
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
import LiveDashboard from '@/pages/dna/LiveDashboard'
import FormatAnatomy from '@/pages/dna/FormatAnatomy'
import Generator from '@/pages/dna/Generator'
import Verifier from '@/pages/dna/Verifier'
import AlgorithmSection from '@/pages/dna/AlgorithmSection'
import UniquenessMath from '@/pages/dna/UniquenessMath'
import '@/pages/dna/dna.css'

/**
 * DNA 追溯码 `/dna`（design/dna.md）
 * S1 活 DNA 仪表台 → S2 格式 v2.0 解剖 → S3 在线铸造器 →
 * S4 验证器 → S5 干支算法白皮书 + 64 卦全表 → S6 唯一性数学
 */
export default function Dna() {
  return (
    <>
      <LiveDashboard />
      <FormatAnatomy />
      <Generator />
      <Verifier />
      <AlgorithmSection />
      <UniquenessMath />
    </>
  )
}
