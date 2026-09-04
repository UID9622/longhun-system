// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-0ff5bc5d
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂路径宇宙 · 节点详情弹层
// UID9622 | 龍芯北辰 | 2026-07-18

import { PathNode } from '../models/PathNode'

@Component
export struct NodeDetail {
  @Prop node: PathNode
  onClose?: () => void

  build() {
    Column() {
      // 标题行
      Row() {
        Text('🐉 节点详情')
          .fontSize(16)
          .fontColor('#FFD700')
          .fontWeight(FontWeight.Bold)
        Blank()
        Text('×')
          .fontSize(24)
          .fontColor('#888')
          .onClick(() => {
            if (this.onClose) this.onClose()
          })
      }
      .width('100%')
      .padding(15)
      .border({ width: { bottom: 1 }, color: '#333' })

      // 详情行
      this.DetailRow({ label: 'PathID', value: this.node.pathId.toString() })
      this.DetailRow({ label: '3D坐标', value: `(${this.node.x}, ${this.node.y}, ${this.node.z})` })
      this.DetailRow({ label: '数字根', value: this.node.dr.toString() })
      this.DetailRow({ label: '五行', value: this.node.wuxing, color: this.node.color })
      this.DetailRow({ label: '审计状态', value: this.node.audit })
      this.DetailRow({
        label: '六维坐标',
        value: `D${this.node.d}·L${this.node.l}·B${this.node.b}·G${this.node.g}·W${this.node.w}·TG${this.node.tg}`
      })
    }
    .width('80%')
    .backgroundColor('rgba(0,0,0,0.95)')
    .border({ width: 2, color: '#FFD700', radius: 10 })
    .position({ x: '10%', y: '30%' })
  }

  @Builder
  DetailRow(config: { label: string, value: string, color?: string }) {
    Row() {
      Text(config.label)
        .fontSize(12)
        .fontColor('#888')
      Blank()
      Text(config.value)
        .fontSize(12)
        .fontColor(config.color ?? '#fff')
        .fontWeight(FontWeight.Bold)
        .fontFamily('monospace')
    }
    .width('100%')
    .padding(10)
    .border({ width: { bottom: 1 }, color: '#1a1a1a' })
  }
}

// 追踪结果面板
@Component
export struct TraceResultPanel {
  @Prop result: import('../models/TraceResult').TraceResult
  onClose?: () => void

  build() {
    Column() {
      Row() {
        Text('🔥 路径追踪结果')
          .fontSize(16)
          .fontColor('#FFD700')
          .fontWeight(FontWeight.Bold)
        Blank()
        Text('×')
          .fontSize(24)
          .fontColor('#888')
          .onClick(() => {
            if (this.onClose) this.onClose()
          })
      }
      .width('100%')
      .padding(15)
      .border({ width: { bottom: 1 }, color: '#333' })

      Text(`输入: "${this.result.text}"`)
        .fontSize(12)
        .fontColor('#fff')
        .padding(10)

      this.DetailRow({ label: 'PathID', value: this.result.pathId.toString() })
      this.DetailRow({ label: '3D坐标', value: `(${this.result.x}, ${this.result.y}, ${this.result.z})` })
      this.DetailRow({ label: '数字根', value: this.result.dr.toString() })
      this.DetailRow({ label: '五行', value: this.result.wuxing, color: '#FFD700' })
      this.DetailRow({ label: '审计', value: this.result.audit })
    }
    .width('80%')
    .backgroundColor('rgba(0,0,0,0.95)')
    .border({ width: 2, color: '#FFD700', radius: 10 })
    .position({ x: '10%', y: '25%' })
  }

  @Builder
  DetailRow(config: { label: string, value: string, color?: string }) {
    Row() {
      Text(config.label)
        .fontSize(12)
        .fontColor('#888')
      Blank()
      Text(config.value)
        .fontSize(12)
        .fontColor(config.color ?? '#fff')
        .fontWeight(FontWeight.Bold)
        .fontFamily('monospace')
    }
    .width('100%')
    .padding(10)
    .border({ width: { bottom: 1 }, color: '#1a1a1a' })
  }
}
