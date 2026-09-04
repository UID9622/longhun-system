/**
 * 🐉 龍魂·StatusRing — 环形进度组件
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-STATUS-RING-UID9622
 *
 * Canvas 绘制环形进度 · 绿(>80%)/黄(60-80%)/红(<60%)
 */

@Component
export struct StatusRing {
  @Prop value: number = 85;
  @Prop label: string = '健康度';
  @Prop sublabel: string = '';
  @Prop size: number = 100;
  private canvasSettings: RenderingContextSettings = new RenderingContextSettings(true);
  private context: CanvasRenderingContext2D = new CanvasRenderingContext2D(this.canvasSettings);

  private getColor(): string {
    if (this.value > 80) return '#4ADE80';  // 🟢
    if (this.value > 60) return '#F4A261';  // 🟡
    return '#E63946';                       // 🔴
  }

  drawRing(): void {
    const ctx = this.context;
    const center = this.size / 2;
    const radius = (this.size / 2) - 8;
    const lineWidth = 8;
    const color = this.getColor();

    ctx.clearRect(0, 0, this.size, this.size);

    // 背景环
    ctx.beginPath();
    ctx.arc(center, center, radius, -Math.PI / 2, 1.5 * Math.PI);
    ctx.strokeStyle = '#1E293B';
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';
    ctx.stroke();

    // 进度环
    ctx.beginPath();
    ctx.arc(center, center, radius, -Math.PI / 2, -Math.PI / 2 + (this.value / 100) * 2 * Math.PI);
    ctx.strokeStyle = color;
    ctx.lineWidth = lineWidth;
    ctx.lineCap = 'round';
    ctx.stroke();

    // 中心文字
    ctx.fillStyle = '#E5E7EB';
    ctx.font = `bold ${this.size * 0.22}px sans-serif`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`${Math.round(this.value)}%`, center, center);
  }

  build() {
    Column({ space: 4 }) {
      Canvas(this.context)
        .width(this.size)
        .height(this.size)
        .onReady(() => { this.drawRing(); })

      Text(this.label)
        .fontSize(11)
        .fontColor('#C9A84C')
        .fontWeight(FontWeight.Medium)

      if (this.sublabel) {
        Text(this.sublabel)
          .fontSize(9)
          .fontColor('#6B7280')
      }
    }
    .alignItems(HorizontalAlign.Center)
  }
}
