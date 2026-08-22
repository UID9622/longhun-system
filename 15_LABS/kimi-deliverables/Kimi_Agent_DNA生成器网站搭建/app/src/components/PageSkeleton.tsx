import { type FC } from 'react'

/** 路由切换时的骨架屏，与全站黑金基调一致 */
const PageSkeleton: FC<{ height?: string }> = ({ height = '80vh' }) => (
  <div
    className="flex items-center justify-center bg-ink"
    style={{ minHeight: height }}
    aria-label="加载中"
    role="status"
  >
    <div className="flex flex-col items-center gap-6">
      {/* 简笔卦符呼吸 */}
      <span
        className="select-none animate-pulse font-serif text-[64px] leading-none text-gold/15"
        aria-hidden="true"
      >
        ䷀
      </span>
      {/* 细线加载条 */}
      <div className="h-[2px] w-[120px] overflow-hidden rounded-full bg-gold/10">
        <div
          className="h-full animate-[shimmer_1.8s_ease-in-out_infinite] rounded-full bg-gold/40"
          style={{ width: '40%' }}
        />
      </div>
      <span className="text-[13px] tracking-[0.15em] text-paper-dim">加载中</span>
    </div>
  </div>
)

export default PageSkeleton
