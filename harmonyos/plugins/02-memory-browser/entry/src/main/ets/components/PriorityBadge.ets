/**
 * 🐉 龍魂·PriorityBadge — 优先级徽章组件
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-PRIORITY-BADGE-UID9622
 *
 * 显示 P0-P3 优先级颜色徽章
 */

@Component
export struct PriorityBadge {
  @Prop priority: number = 2;
  @Prop showLabel: boolean = true;

  private readonly colors: Record<number, string> = {
    0: '#E63946', // P0 血红
    1: '#F4A261', // P1 橙金
    2: '#457B9D', // P2 钢蓝
    3: '#A8DADC', // P3 冰灰
  };

  private readonly labels: Record<number, string> = {
    0: 'P0',
    1: 'P1',
    2: 'P2',
    3: 'P3',
  };

  build() {
    Row() {
      Text(this.labels[this.priority] || 'P2')
        .fontSize(10)
        .fontColor(Color.White)
        .fontWeight(FontWeight.Bold)
        .padding({ left: 4, right: 4, top: 1, bottom: 1 })
        .borderRadius(3)
        .backgroundColor(this.colors[this.priority] || '#457B9D')
    }
  }
}
