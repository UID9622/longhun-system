import TimelineHero from '@/pages/timeline/TimelineHero'
import ExpeditionTrack from '@/pages/timeline/ExpeditionTrack'
import FutureChapter from '@/pages/timeline/FutureChapter'

/**
 * 远征日志 `/timeline`（timeline.md）
 * PageHero（垂落金线 + 干支字符雨）→ 滚动时间线主轴（五座里程碑章）→ 未来空白章
 */
export default function Timeline() {
  return (
    <>
      <TimelineHero />
      <ExpeditionTrack />
      <FutureChapter />
    </>
  )
}
