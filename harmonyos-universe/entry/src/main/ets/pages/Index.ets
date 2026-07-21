// 龍魂路径宇宙 · 主页面
// UID9622 | 龍芯北辰 | 2026-07-18

import { LongHunUniverse } from '../components/LongHunUniverse'
import { PathTracer } from '../components/PathTracer'
import { HeaderBar } from '../components/HeaderBar'
import { SearchBar } from '../components/SearchBar'
import { AuditFilter } from '../components/AuditFilter'
import { StatsBar } from '../components/StatsBar'
import { NodeDetail, TraceResultPanel } from '../components/NodeDetail'
import { DNAWatermark } from '../components/DNAWatermark'
import { LoadingView } from '../components/LoadingView'
import { PathNode } from '../models/PathNode'
import { TraceResult } from '../models/TraceResult'
import { P0_ANCHOR, SAMPLE_COUNT } from '../utils/Constants'

@Entry
@Component
struct LongHunApp {
  @State currentPage: string = 'universe'
  @State selectedNode: PathNode | null = null
  @State traceResult: TraceResult | null = null
  @State auditFilter: string = 'all'
  @State isLoading: boolean = true

  aboutToAppear() {
    this.verifyDNA()
    // 模拟加载，让Loading动画展示
    setTimeout(() => {
      this.isLoading = false
    }, 2000)
  }

  verifyDNA() {
    console.info(`🐉 龍魂宇宙启动 | DNA验证: ${P0_ANCHOR.confirm}`)
  }

  build() {
    Stack() {
      if (this.isLoading) {
        // 加载动画
        LoadingView()
      } else {
        // 主界面
        Column() {
          HeaderBar({ title: '龍魂翻译引擎', subtitle: '1650万路径宇宙' })

          SearchBar({
            onTrace: (text: string) => {
              this.handleTrace(text)
            }
          })

          AuditFilter({
            currentFilter: this.auditFilter,
            onFilterChange: (filter: string) => {
              this.auditFilter = filter
            }
          })

          // 3D宇宙视图（占据剩余空间）
          LongHunUniverse({
            auditFilter: this.auditFilter,
            onNodeSelect: (node: PathNode) => {
              this.selectedNode = node
            }
          })
          .layoutWeight(1)

          StatsBar({ sampleCount: SAMPLE_COUNT })
        }
        .width('100%')
        .height('100%')
        .backgroundColor('#0a0a0a')
      }

      // 节点详情弹层
      if (this.selectedNode) {
        NodeDetail({
          node: this.selectedNode,
          onClose: () => {
            this.selectedNode = null
          }
        })
      }

      // 路径追踪结果弹层
      if (this.traceResult) {
        TraceResultPanel({
          result: this.traceResult,
          onClose: () => {
            this.traceResult = null
          }
        })
      }

      // DNA水印（覆盖在最上层）
      DNAWatermark()
    }
    .width('100%')
    .height('100%')
  }

  handleTrace(text: string) {
    const tracer = new PathTracer()
    this.traceResult = tracer.trace(text)
    console.info(`🐉 路径追踪: "${text}" → PathID: ${this.traceResult.pathId}`)
  }
}
