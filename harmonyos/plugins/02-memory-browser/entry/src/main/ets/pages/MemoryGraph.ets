/**
 * 🐉 龍魂·MemoryGraph — 记忆图谱可视化
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-MEMORY-GRAPH-UID9622
 *
 * Canvas 绘制记忆关联图谱 · 节点大小=优先级权重 · 双指缩放+拖拽
 */

import { MemoryViewModel } from '../viewmodel/MemoryViewModel';

interface GraphNode {
  x: number; y: number;
  id: string; label: string;
  priority: number; radius: number;
  color: string;
}

interface GraphEdge {
  from: string; to: string;
}

@Entry
@Component
struct MemoryGraph {
  private viewModel: MemoryViewModel = new MemoryViewModel();
  private canvasSettings: RenderingContextSettings = new RenderingContextSettings(true);
  private context: CanvasRenderingContext2D = new CanvasRenderingContext2D(this.canvasSettings);
  @State scale: number = 1.0;
  @State offsetX: number = 0;
  @State offsetY: number = 0;
  private nodes: GraphNode[] = [];
  private edges: GraphEdge[] = [];

  private readonly colors: Record<number, string> = {
    0: '#E63946',
    1: '#F4A261',
    2: '#457B9D',
    3: '#A8DADC',
  };

  aboutToAppear(): void {
    this.viewModel.loadMemories().then(() => {
      this.buildGraph();
    });
  }

  buildGraph(): void {
    const memories = this.viewModel.memories;
    this.nodes = [];
    this.edges = [];

    // 圆形布局
    const centerX = 180;
    const centerY = 360;
    const radius = 160;
    const count = Math.min(memories.length, 20);

    for (let i = 0; i < count; i++) {
      const angle = (2 * Math.PI * i) / count - Math.PI / 2;
      const r = radius * (memories[i].priority === 0 ? 1.2 : 1.0);
      this.nodes.push({
        x: centerX + r * Math.cos(angle),
        y: centerY + r * Math.sin(angle),
        id: memories[i].id,
        label: memories[i].category || memories[i].content.substring(0, 6),
        priority: memories[i].priority,
        radius: 24 - memories[i].priority * 4, // P0=24 P3=12
        color: this.colors[memories[i].priority] || '#457B9D'
      });
    }

    // 创建边（相邻节点+同级节点连线）
    for (let i = 0; i < this.nodes.length - 1; i++) {
      this.edges.push({ from: this.nodes[i].id, to: this.nodes[i + 1].id });
    }
    // 闭环
    if (this.nodes.length > 2) {
      this.edges.push({ from: this.nodes[this.nodes.length - 1].id, to: this.nodes[0].id });
    }

    this.drawCanvas();
  }

  drawCanvas(): void {
    const ctx = this.context;
    ctx.clearRect(0, 0, 360, 720);

    // 画连线
    for (const edge of this.edges) {
      const fromNode = this.nodes.find(n => n.id === edge.from);
      const toNode = this.nodes.find(n => n.id === edge.to);
      if (fromNode && toNode) {
        ctx.beginPath();
        ctx.moveTo(fromNode.x * this.scale + this.offsetX, fromNode.y * this.scale + this.offsetY);
        ctx.lineTo(toNode.x * this.scale + this.offsetX, toNode.y * this.scale + this.offsetY);
        ctx.strokeStyle = '#334155';
        ctx.lineWidth = 1;
        ctx.stroke();
      }
    }

    // 画节点
    for (const node of this.nodes) {
      const cx = node.x * this.scale + this.offsetX;
      const cy = node.y * this.scale + this.offsetY;

      // 外发光
      ctx.beginPath();
      ctx.arc(cx, cy, node.radius + 4, 0, 2 * Math.PI);
      ctx.fillStyle = node.color + '33';
      ctx.fill();

      // 节点圆
      ctx.beginPath();
      ctx.arc(cx, cy, node.radius, 0, 2 * Math.PI);
      ctx.fillStyle = node.color;
      ctx.fill();

      // 边框
      ctx.beginPath();
      ctx.arc(cx, cy, node.radius, 0, 2 * Math.PI);
      ctx.strokeStyle = '#C9A84C';
      ctx.lineWidth = 1.5;
      ctx.stroke();

      // 标签
      ctx.fillStyle = '#E5E7EB';
      ctx.font = '8px sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(node.label, cx, cy + node.radius + 12);
    }
  }

  build() {
    Column() {
      // 顶栏
      Row() {
        Text('← 返回')
          .fontSize(14)
          .fontColor('#C9A84C')
          .onClick(() => { router.back(); })

        Blank()

        Text('🐉 记忆关联图谱')
          .fontSize(18)
          .fontColor('#C9A84C')
          .fontWeight(FontWeight.Bold)

        Blank()

        Text(`节点:${this.nodes.length}`)
          .fontSize(11)
          .fontColor('#6B7280')
      }
      .width('100%')
      .padding(16)

      // Canvas 图谱
      Canvas(this.context)
        .width('100%')
        .layoutWeight(1)
        .backgroundColor('#0F172A')
        .onReady(() => { this.drawCanvas(); })
        .gesture(
          PinchGesture()
            .onActionUpdate((event: GestureEvent) => {
              this.scale = Math.max(0.5, Math.min(2.0, event.scale));
              this.drawCanvas();
            })
        )
        .gesture(
          PanGesture()
            .onActionUpdate((event: GestureEvent) => {
              this.offsetX += event.offsetX;
              this.offsetY += event.offsetY;
              this.drawCanvas();
            })
        )

      // 图例
      Row({ space: 16 }) {
        ForEach(['P0·永恒', 'P1·重要', 'P2·普通', 'P3·临时'] as string[],
          (label: string, index: number) => {
            Row({ space: 4 }) {
              Circle({ width: 8, height: 8 })
                .fill(this.colors[index])
              Text(label)
                .fontSize(10)
                .fontColor('#6B7280')
            }
          })
      }
      .width('100%')
      .justifyContent(FlexAlign.Center)
      .padding({ bottom: 16 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0F172A')
  }
}
