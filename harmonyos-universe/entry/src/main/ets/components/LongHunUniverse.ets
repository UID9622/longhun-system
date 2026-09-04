// DNA: #龍芯⚡️丙午·甲申·丁未·亥时·䷎谦-DNA-COMPLETION-33bd3015
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
// 龍魂路径宇宙 · 3D宇宙核心组件
// UID9622 | 龍芯北辰 | 2026-07-18
// 使用 Canvas 2D + 透视投影模拟3D（鸿蒙兼容性最佳）

import { PathNode } from '../models/PathNode'
import { PathTracer } from './PathTracer'
import { SEED, SAMPLE_COUNT, AUDIT_ALPHA } from '../utils/Constants'

@Component
export struct LongHunUniverse {
  @Prop auditFilter: string = 'all'
  @State nodes: PathNode[] = []
  @State rotationX: number = 0
  @State rotationY: number = 0
  @State scale: number = 1
  @State lastTouchX: number = 0
  @State lastTouchY: number = 0
  @State isDragging: boolean = false
  @State canvasWidth: number = 375
  @State canvasHeight: number = 667
  @State selectedNode: PathNode | null = null

  onNodeSelect?: (node: PathNode) => void

  private settings: RenderingContextSettings = new RenderingContextSettings(true)
  private canvasContext: CanvasRenderingContext2D = new CanvasRenderingContext2D(this.settings)
  private isAutoRotating: boolean = true

  aboutToAppear() {
    this.generateNodes(SAMPLE_COUNT)
  }

  generateNodes(count: number) {
    const rng = PathTracer.mulberry32(SEED)
    const newNodes: PathNode[] = []

    for (let i = 0; i < count; i++) {
      const d = Math.floor(rng() * 6)
      const l = Math.floor(rng() * 9)
      const b = Math.floor(rng() * 8)
      const g = Math.floor(rng() * 64)
      const w = Math.floor(rng() * 5)
      const tg = Math.floor(rng() * 120)
      newNodes.push(new PathNode(d, l, b, g, w, tg))
    }

    this.nodes = newNodes
  }

  build() {
    Column() {
      Canvas(this.canvasContext)
        .width('100%')
        .height('100%')
        .backgroundColor('#0a0a0a')
        .onReady(() => {
          this.startRenderLoop()
        })
        .onAreaChange((oldValue: Area, newValue: Area) => {
          this.canvasWidth = newValue.width as number
          this.canvasHeight = newValue.height as number
        })
        .onTouch((event: TouchEvent) => {
          this.handleTouch(event)
        })
        .onClick((event: ClickEvent) => {
          this.handleClick(event)
        })
    }
    .width('100%')
    .height('100%')
  }

  startRenderLoop() {
    const render = () => {
      this.renderFrame()
      // 自动旋转
      if (this.isAutoRotating) {
        this.rotationY += 0.3
      }
      requestAnimationFrame(render)
    }
    requestAnimationFrame(render)
  }

  renderFrame() {
    const ctx = this.canvasContext
    const width = this.canvasWidth
    const height = this.canvasHeight

    // 清空画布
    ctx.fillStyle = '#0a0a0a'
    ctx.fillRect(0, 0, width, height)

    // 投影参数
    const centerX = width / 2
    const centerY = height / 2
    const fov = 500

    // 渲染节点
    this.nodes.forEach(node => {
      // 审计过滤
      if (this.auditFilter !== 'all') {
        const auditKey = node.audit === '🟢' ? 'green' :
                        node.audit === '🟡' ? 'yellow' : 'red'
        if (auditKey !== this.auditFilter) return
      }

      // 3D旋转
      const rx = this.rotationX * Math.PI / 180
      const ry = this.rotationY * Math.PI / 180

      // 绕Y轴旋转
      let x1 = node.x * Math.cos(ry) - node.z * Math.sin(ry)
      let z1 = node.x * Math.sin(ry) + node.z * Math.cos(ry)
      let y1 = node.y

      // 绕X轴旋转
      let y2 = y1 * Math.cos(rx) - z1 * Math.sin(rx)
      let z2 = y1 * Math.sin(rx) + z1 * Math.cos(rx)
      let x2 = x1

      // 缩放
      x2 *= this.scale
      y2 *= this.scale
      z2 *= this.scale

      // 透视投影
      const zOffset = z2 + fov
      if (zOffset <= 0) return

      const projScale = fov / zOffset
      const screenX = centerX + x2 * projScale
      const screenY = centerY - y2 * projScale

      // 视口裁剪
      if (screenX < -20 || screenX > width + 20 ||
          screenY < -20 || screenY > height + 20) return

      // 绘制节点
      const size = Math.max(node.size * projScale, 1)

      // 发光效果
      ctx.globalAlpha = node.alpha * 0.3
      ctx.fillStyle = node.color
      ctx.beginPath()
      ctx.arc(screenX, screenY, size * 2, 0, Math.PI * 2)
      ctx.fill()

      // 节点本体
      ctx.globalAlpha = node.alpha
      ctx.fillStyle = node.color
      ctx.beginPath()
      ctx.arc(screenX, screenY, size, 0, Math.PI * 2)
      ctx.fill()
    })

    ctx.globalAlpha = 1.0

    // 绘制坐标轴
    this.drawAxes(ctx, width, height)
  }

  drawAxes(ctx: CanvasRenderingContext2D, width: number, height: number) {
    ctx.strokeStyle = 'rgba(255, 215, 0, 0.3)'
    ctx.lineWidth = 1
    ctx.font = '10px monospace'

    const cx = 40
    const cy = height - 60

    // X轴
    ctx.beginPath()
    ctx.moveTo(cx, cy)
    ctx.lineTo(cx + 60, cy)
    ctx.stroke()
    ctx.fillStyle = '#FFD700'
    ctx.fillText('X', cx + 65, cy + 4)

    // Y轴
    ctx.beginPath()
    ctx.moveTo(cx, cy)
    ctx.lineTo(cx, cy - 60)
    ctx.stroke()
    ctx.fillText('Y', cx, cy - 65)
  }

  handleTouch(event: TouchEvent) {
    const touch = event.touches[0]
    if (!touch) return

    switch (event.type) {
      case TouchType.Down:
        this.isDragging = true
        this.isAutoRotating = false
        this.lastTouchX = touch.x
        this.lastTouchY = touch.y
        break
      case TouchType.Move:
        if (this.isDragging) {
          const dx = touch.x - this.lastTouchX
          const dy = touch.y - this.lastTouchY
          this.rotationY += dx * 0.5
          this.rotationX += dy * 0.5
          this.lastTouchX = touch.x
          this.lastTouchY = touch.y
        }
        break
      case TouchType.Up:
      case TouchType.Cancel:
        this.isDragging = false
        // 松手后恢复自动旋转
        setTimeout(() => {
          if (!this.isDragging) {
            this.isAutoRotating = true
          }
        }, 2000)
        break
    }
  }

  handleClick(event: ClickEvent) {
    const clickX = event.x ?? 0
    const clickY = event.y ?? 0

    if (this.isDragging) return  // 拖拽中不触发点击

    let nearestNode: PathNode | null = null
    let minDist = Infinity

    const centerX = this.canvasWidth / 2
    const centerY = this.canvasHeight / 2
    const fov = 500

    this.nodes.forEach(node => {
      const rx = this.rotationX * Math.PI / 180
      const ry = this.rotationY * Math.PI / 180

      let x1 = node.x * Math.cos(ry) - node.z * Math.sin(ry)
      let z1 = node.x * Math.sin(ry) + node.z * Math.cos(ry)
      let y1 = node.y

      let y2 = y1 * Math.cos(rx) - z1 * Math.sin(rx)
      let z2 = y1 * Math.sin(rx) + z1 * Math.cos(rx)
      let x2 = x1

      x2 *= this.scale
      y2 *= this.scale
      z2 *= this.scale

      const zOffset = z2 + fov
      if (zOffset <= 0) return

      const projScale = fov / zOffset
      const screenX = centerX + x2 * projScale
      const screenY = centerY - y2 * projScale

      const dist = Math.sqrt((clickX - screenX) ** 2 + (clickY - screenY) ** 2)
      if (dist < minDist && dist < 30) {
        minDist = dist
        nearestNode = node
      }
    })

    if (nearestNode && this.onNodeSelect) {
      this.onNodeSelect(nearestNode)
    }
  }
}
