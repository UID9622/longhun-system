/**
 * 🐉 龍魂·PersonaCard — 人格卡片组件
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-PERSONA-CARD-UID9622
 *
 * 显示单个人格的ID/名称/角色/权重/健康度
 */

@Component
export struct PersonaCard {
  @Prop id: string = '';
  @Prop name: string = '';
  @Prop role: string = '';
  @Prop weight: number = 5;
  @Prop active: boolean = true;
  @Prop health: number = 90;

  private getHealthColor(): string {
    if (this.health > 90) return '#4ADE80';
    if (this.health > 70) return '#F4A261';
    return '#E63946';
  }

  build() {
    Row() {
      // 头像区
      Column() {
        Text(this.name[0] || '?')
          .fontSize(16)
          .fontColor('#C9A84C')
          .fontWeight(FontWeight.Bold)
      }
      .width(40)
      .height(40)
      .borderRadius(20)
      .backgroundColor('#1E293B')
      .border({ width: 1, color: '#C9A84C', style: BorderStyle.Solid })
      .justifyContent(FlexAlign.Center)

      // 信息区
      Column({ space: 2 }) {
        Row({ space: 6 }) {
          Text(this.name)
            .fontSize(14)
            .fontColor('#E5E7EB')
            .fontWeight(FontWeight.Medium)
          Text(this.id)
            .fontSize(9)
            .fontColor('#6B7280')
        }

        Text(this.role)
          .fontSize(10)
          .fontColor('#9CA3AF')

        // 健康度条
        Row({ space: 6 }) {
          Progress({ value: this.health, total: 100, type: ProgressType.Linear })
            .width(60)
            .height(4)
            .color(this.getHealthColor())
            .backgroundColor('#1E293B')

          Text(`${this.health}%`)
            .fontSize(9)
            .fontColor(this.getHealthColor())
        }
      }
      .alignItems(HorizontalAlign.Start)
      .margin({ left: 10 })
      .layoutWeight(1)

      // 活跃状态
      Circle({ width: 8, height: 8 })
        .fill(this.active ? '#4ADE80' : '#EF4444')
    }
    .width('100%')
    .padding({ top: 8, bottom: 8, left: 4, right: 4 })
    .border({ width: { bottom: 0.5 }, color: '#1E293B', style: BorderStyle.Solid })
  }
}
