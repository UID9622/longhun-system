/**
 * 🐉 龍魂·MemoryCard — 记忆卡片组件
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-MEMORY-CARD-UID9622
 *
 * P0红/P1橙/P2蓝/P3灰 · 暗金主题 · 长按操作菜单
 */

@Component
export struct MemoryCard {
  @Prop id: string = '';
  @Prop priority: number = 2;
  @Prop category: string = '';
  @Prop content: string = '';
  @Prop timestamp: string = '';
  @Prop tricolor: string = '🟢';
  @Prop dna: string = '';
  @Prop keywords: string[] = [];
  onCardClick?: () => void;
  onCardLongPress?: () => void;

  private readonly colors: Record<number, { bg: string; border: string; indicator: string }> = {
    0: { bg: '#2D1B1B', border: '#E63946', indicator: '#E63946' },
    1: { bg: '#2D2419', border: '#F4A261', indicator: '#F4A261' },
    2: { bg: '#1B2A35', border: '#457B9D', indicator: '#457B9D' },
    3: { bg: '#1E2328', border: '#A8DADC', indicator: '#A8DADC' },
  };

  private readonly labels: Record<number, string> = {
    0: 'P0·永恒', 1: 'P1·重要', 2: 'P2·普通', 3: 'P3·临时',
  };

  build() {
    Column() {
      // 顶部三色指示条
      Row()
        .width('100%')
        .height(3)
        .backgroundColor((this.colors[this.priority] || this.colors[2]).indicator)
        .borderRadius({ topLeft: 8, topRight: 8 })

      Column() {
        // 标题行：分类 + 优先级徽章 + 三色
        Row() {
          Text(this.category)
            .fontSize(11)
            .fontColor('#C9A84C') // 龍魂金
            .fontWeight(FontWeight.Medium)
            .maxLines(1)

          Blank()

          Badge(this.labels[this.priority] || 'P2')
            .fontSize(9)
            .fontColor(Color.White)
            .borderRadius(3)
            .padding({ left: 4, right: 4, top: 1, bottom: 1 })
            .backgroundColor((this.colors[this.priority] || this.colors[2]).indicator)

          Text(this.tricolor)
            .fontSize(14)
            .margin({ left: 6 })
        }
        .width('100%')
        .margin({ bottom: 6 })

        // 内容摘要
        Text(this.content)
          .fontSize(13)
          .fontColor('#E5E7EB')
          .maxLines(3)
          .textOverflow({ overflow: TextOverflow.Ellipsis })
          .lineHeight(18)
          .width('100%')
          .margin({ bottom: 8 })

        // 底部：关键词 + 时间 + DNA
        Row() {
          if (this.keywords && this.keywords.length > 0) {
            Text(this.keywords.slice(0, 3).join(' · '))
              .fontSize(9)
              .fontColor('#6B7280')
              .maxLines(1)
              .textOverflow({ overflow: TextOverflow.Ellipsis })
              .flexShrink(1)
          }

          Blank()

          Column({ space: 2 }) {
            Text(this.formatTime(this.timestamp))
              .fontSize(9)
              .fontColor('#6B7280')
            Text(this.dna.substring(0, 20) + '...')
              .fontSize(8)
              .fontColor('#4B5563')
              .fontFamily('monospace')
          }
          .alignItems(HorizontalAlign.End)
        }
        .width('100%')
      }
      .padding(12)
      .width('100%')
    }
    .backgroundColor((this.colors[this.priority] || this.colors[2]).bg)
    .border({ width: 1, color: (this.colors[this.priority] || this.colors[2]).border, style: BorderStyle.Solid })
    .borderRadius(10)
    .margin({ left: 16, right: 16, top: 4, bottom: 4 })
    .onClick(() => { this.onCardClick?.(); })
    .gesture(
      LongPressGesture()
        .onAction(() => { this.onCardLongPress?.(); })
    )
  }

  private formatTime(iso: string): string {
    if (!iso) return '';
    try {
      const d = new Date(iso);
      return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`;
    } catch (e) {
      return iso.substring(0, 16);
    }
  }
}
