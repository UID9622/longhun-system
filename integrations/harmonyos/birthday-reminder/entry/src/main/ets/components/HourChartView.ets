// entry/src/main/ets/components/HourChartView.ets
// 龍魂 · 工时统计图表 · ArkTS

import { WeeklyStats, HourTrendItem } from '../models/WeeklyModel';

@Component
export struct HourChartView {
  @Prop stats: WeeklyStats = {
    totalReports: 0, myTotal: 0, myDraft: 0, mySubmitted: 0,
    myApproved: 0, myRejected: 0, pendingReview: 0,
    avgCompletion: 0, totalHours: 0, thisWeekHours: 0
  };
  @Prop trend: HourTrendItem[] = [];

  build() {
    Scroll() {
      Column() {
        // 工时概览卡片
        this.OverviewBuilder()

        // 工时分布
        this.DistributionBuilder()

        // 周报完成率
        this.CompletionRateBuilder()

        // 工时柱状图
        if (this.trend.length > 0) {
          this.BarChartBuilder()
        }
      }
    }
    .width('100%').layoutWeight(1).backgroundColor('#0a0a0a')
    .scrollBar(BarState.Auto)
  }

  @Builder
  OverviewBuilder() {
    Column() {
      Text('📊 工时概览').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      Row() {
        this.OverviewCard('总工时', `${this.stats.totalHours}h`, '#0088ff', '累计')
        this.OverviewCard('本周工时', `${this.stats.thisWeekHours}h`, '#c41e3a', '本周')
        this.OverviewCard('平均完成率', `${this.stats.avgCompletion}%`, '#00cc66', '概况')
      }
      .width('100%').justifyContent(FlexAlign.SpaceBetween)
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12 })
  }

  @Builder
  OverviewCard(label: string, value: string, color: string, subtitle: string) {
    Column() {
      Text(value).fontSize(22).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label).fontSize(12).fontColor('#888').margin({ top: 4 })
      Text(subtitle).fontSize(10).fontColor('#555').margin({ top: 2 })
    }
    .width('30%').height(70).justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
    .backgroundColor('rgba(255,255,255,0.03)').borderRadius(8)
  }

  @Builder
  DistributionBuilder() {
    Column() {
      Text('📈 周报状态分布').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      Row() {
        this.DistBar('草稿', this.stats.myDraft, this.stats.myTotal, '#ffcc00')
        this.DistBar('已提交', this.stats.mySubmitted, this.stats.myTotal, '#0066cc')
        this.DistBar('已通过', this.stats.myApproved, this.stats.myTotal, '#00ff00')
        this.DistBar('已驳回', this.stats.myRejected, this.stats.myTotal, '#ff4444')
      }
      .width('100%').justifyContent(FlexAlign.SpaceBetween)

      Row() {
        this.DistItem('草稿', '📝', '#ffcc00', this.stats.myDraft)
        this.DistItem('已提交', '⏳', '#0066cc', this.stats.mySubmitted)
        this.DistItem('已通过', '✅', '#00ff00', this.stats.myApproved)
        this.DistItem('已驳回', '❌', '#ff4444', this.stats.myRejected)
      }
      .width('100%').margin({ top: 12 })
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12 })
  }

  @Builder
  DistBar(label: string, count: number, total: number, color: string) {
    Column() {
      Text(`${total > 0 ? Math.round((count / total) * 100) : 0}%`).fontSize(12).fontColor(color)
      Row().height(4).backgroundColor('#333').borderRadius(2)
        .constraintSize({ maxWidth: 60 })
    }
    .width(`${total > 0 ? Math.max(5, (count / total) * 25) : 5}%`)
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  DistItem(label: string, icon: string, color: string, count: number) {
    Column() {
      Text(icon).fontSize(18).margin({ bottom: 4 })
      Text(`${count}`).fontSize(16).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label).fontSize(11).fontColor('#888')
    }
    .width('23%').height(70).justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
  }

  @Builder
  CompletionRateBuilder() {
    Column() {
      Text('📊 完成率概览').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      Row() {
        Column() {
          Text(`${this.stats.avgCompletion}%`).fontSize(36).fontWeight(FontWeight.Bold).fontColor(
            this.stats.avgCompletion >= 80 ? '#00ff00' :
            this.stats.avgCompletion >= 60 ? '#ffcc00' : '#ff6600'
          )
          Text('平均任务完成率').fontSize(12).fontColor('#888').margin({ top: 4 })
        }
        .alignItems(HorizontalAlign.Start).layoutWeight(1)

        Stack() {
          Circle({ width: 80, height: 80 }).fill('#333')
          Circle({ width: 80, height: 80 })
            .stroke('#c41e3a')
            .strokeWidth(6)
            .fill(Color.Transparent)
          Text(`${this.stats.avgCompletion}%`).fontSize(18).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        }
      }
      .width('100%')

      // 进度条
      Row() {
        Stack() {
          Row().width('100%').height(8).backgroundColor('#333').borderRadius(4)
          Row().width(`${this.stats.avgCompletion}%`).height(8)
            .backgroundColor(
              this.stats.avgCompletion >= 80 ? '#00ff00' :
              this.stats.avgCompletion >= 60 ? '#ffcc00' : '#ff6600'
            ).borderRadius(4)
        }
        .width('100%').height(8).margin({ top: 12 })
      }
      .width('100%')
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12 })
  }

  @Builder
  BarChartBuilder() {
    Column() {
      Text('📉 工时趋势 (近8周)').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      // 图例
      Row() {
        this.LegendItem('计划', '#0088ff')
        this.LegendItem('实际', '#c41e3a')
        this.LegendItem('加班', '#ff6600')
      }
      .width('100%').margin({ bottom: 12 })

      // 柱状图
      Column() {
        Row() {
          Text('h').fontSize(10).fontColor('#555').rotate({ angle: -90 }).width(16)
          Column() {
            Row() {
              ForEach(this.trend, (item: Record<string, Object>) => {
                Column() {
                  const maxH = Math.max(
                    1,
                    (item.planned as number),
                    (item.actual as number),
                    (item.overtime as number)
                  );
                  const scale = 100 / (maxH * 1.5);

                  // 计划工时柱
                  Row()
                    .width(8).height((item.planned as number) * scale)
                    .backgroundColor('#0088ff').borderRadius({ topLeft: 2, topRight: 2 })
                  // 实际工时柱
                  Row()
                    .width(6).height((item.actual as number) * scale)
                    .backgroundColor('#c41e3a').borderRadius({ topLeft: 2, topRight: 2 })
                    .margin({ bottom: 2 })
                  // 加班工时柱
                  if ((item.overtime as number) > 0) {
                    Row()
                      .width(4).height((item.overtime as number) * scale)
                      .backgroundColor('#ff6600').borderRadius({ topLeft: 2, topRight: 2 })
                      .margin({ bottom: 2 })
                  }

                  Text((item.week as string) || '').fontSize(9).fontColor('#666').margin({ top: 4 })
                }
                .layoutWeight(1).alignItems(HorizontalAlign.Center)
              })
            }
            .width('100%')
          }
          .layoutWeight(1)
        }
        .width('100%').height(140)
      }
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12, bottom: 16 })
  }

  @Builder
  LegendItem(label: string, color: string) {
    Row() {
      Row().width(12).height(12).backgroundColor(color).borderRadius(2).margin({ right: 4 })
      Text(label).fontSize(11).fontColor('#888')
    }
    .margin({ right: 16 })
  }
}
