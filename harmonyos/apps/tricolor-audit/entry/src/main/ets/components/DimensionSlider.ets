/**
 * 维度滑块组件
 * License: MulanPSL v2
 */
import { DARK_GOLD } from '../models/Constants';

interface DimensionItem {
  name: string;
  score: number;
  weight: number;
  weightedScore: number;
}

@Component
export struct DimensionSlider {
  @Prop dimension: DimensionItem;
  @Prop index: number;

  build() {
    Row() {
      // 维度名 + 权重
      Column() {
        Text(this.dimension.name)
          .fontSize(14)
          .fontColor(DARK_GOLD.TEXT_PRIMARY)
        Text(`权重 ${this.dimension.weight}%`)
          .fontSize(10)
          .fontColor(DARK_GOLD.TEXT_SECONDARY)
      }
      .width(100)
      .alignItems(HorizontalAlign.Start)

      // 进度条
      Column() {
        // 分数
        Row() {
          Progress({
            value: this.dimension.score * 100,
            total: 100,
            type: ProgressType.Linear
          })
            .width('100%')
            .height(6)
            .color(this.getColor())
            .style({ strokeWidth: 6, strokeRadius: 3 })
        }
        .width('100%')

        Text(`${(this.dimension.score * 100).toFixed(0)} 分  → 加权 ${(this.dimension.weightedScore * 100).toFixed(1)}`)
          .fontSize(10)
          .fontColor(DARK_GOLD.TEXT_SECONDARY)
          .margin({ top: 2 })
      }
      .layoutWeight(1)
      .margin({ left: 8 })
    }
    .width('100%')
    .padding({ top: 6, bottom: 6 })
  }

  getColor(): string {
    const v = this.dimension.score;
    if (v >= 0.70) return DARK_GOLD.SUCCESS;
    if (v >= 0.40) return DARK_GOLD.WARNING;
    return DARK_GOLD.ERROR;
  }
}
