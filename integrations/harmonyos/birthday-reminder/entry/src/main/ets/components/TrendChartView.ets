// entry/src/main/ets/components/TrendChartView.ets
// 龍魂 · 多周趋势对比视图 · ArkTS

import { HourTrendItem } from '../models/WeeklyModel';

@Component
export struct TrendChartView {
  @Prop trend: HourTrendItem[] = [];

  build() {
    Scroll() {
      Column() {
        // 趋势总览
        this.TrendOverviewBuilder()

        // 折线图（计划 vs 实际）
        this.LineChartBuilder()

        // 偏差分析
        if (this.trend.length > 0) {
          this.VarianceAnalysisBuilder()
        }

        // 加班趋势
        this.OvertimeTrendBuilder()

        // 数据表
        this.DataTableBuilder()
      }
    }
    .width('100%').layoutWeight(1).backgroundColor('#0a0a0a')
    .scrollBar(BarState.Auto)
  }

  @Builder
  TrendOverviewBuilder() {
    Column() {
      Text('📈 工时趋势分析').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      Row() {
        this.TrendCard(
          '平均计划工时',
          this.getAvgPlannedHours(),
          '/周',
          '#0088ff'
        )
        this.TrendCard(
          '平均实际工时',
          this.getAvgActualHours(),
          '/周',
          '#c41e3a'
        )
        this.TrendCard(
          '平均加班',
          this.getAvgOvertimeHours(),
          '/周',
          '#ff6600'
        )
      }
      .width('100%').justifyContent(FlexAlign.SpaceBetween)

      // 趋势方向
      if (this.trend.length >= 2) {
        Row() {
          Text(this.isTrendUp() ? '📈 工时呈上升趋势' : '📉 工时呈下降趋势')
            .fontSize(13).fontColor(this.isTrendUp() ? '#ff6600' : '#00cc66')
        }
        .width('100%').margin({ top: 12 }).padding(8)
        .backgroundColor('rgba(255,255,255,0.03)').borderRadius(6)
      }
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12 })
  }

  @Builder
  TrendCard(label: string, value: string, unit: string, color: string) {
    Column() {
      Text(value).fontSize(24).fontWeight(FontWeight.Bold).fontColor(color)
      Row() {
        Text(label).fontSize(10).fontColor('#888')
        Text(unit).fontSize(9).fontColor('#555').margin({ left: 2 })
      }
      .margin({ top: 4 })
    }
    .width('30%').height(68).justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
    .backgroundColor('rgba(255,255,255,0.03)').borderRadius(8)
  }

  @Builder
  LineChartBuilder() {
    Column() {
      Text('📊 计划 vs 实际工时').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      // 图例
      Row() {
        this.LegendItem('计划工时', '#0088ff', '━')
        this.LegendItem('实际工时', '#c41e3a', '━')
        this.LegendItem('加班工时', '#ff6600', '┅')
      }
      .width('100%').margin({ bottom: 12 })

      // 简易折线图
      Column() {
        Row() {
          Text('h').fontSize(10).fontColor('#555').rotate({ angle: -90 }).width(16)

          Column() {
            Row() {
              ForEach(this.trend, (item: Record<string, Object>, index: number) => {
                Column() {
                  const maxH = Math.max(
                    1,
                    (item.planned as number),
                    (item.actual as number),
                    (item.overtime as number)
                  );
                  const scale = 120 / (maxH * 1.3);

                  // 连接线区域
                  Stack() {
                    // 计划工时点
                    Row()
                      .width(6).height(6)
                      .backgroundColor('#0088ff')
                      .borderRadius(3)
                      .offset({ x: -4, y: 120 - (item.planned as number) * scale - 3 })

                    // 实际工时点
                    Row()
                      .width(8).height(8)
                      .backgroundColor('#c41e3a')
                      .borderRadius(4)
                      .offset({ x: 4, y: 120 - (item.actual as number) * scale - 4 })
                  }
                  .width('100%').height(120)

                  Text((item.week as string) || '').fontSize(9).fontColor('#666').margin({ top: 4 })
                }
                .layoutWeight(1).alignItems(HorizontalAlign.Center)
              })
            }
            .width('100%').height(140)
          }
          .layoutWeight(1)
        }
        .width('100%')
      }
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12 })
  }

  @Builder
  VarianceAnalysisBuilder() {
    Column() {
      Text('📐 计划偏差分析').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      ForEach(this.trend, (item: Record<string, Object>) => {
        const variance = (item.actual as number) - (item.planned as number);
        const absVar = Math.abs(variance);
        const isOver = variance > 0;

        Row() {
          Text((item.week as string) || '').fontSize(12).fontColor('#888').width(40)
          Row() {
            Text(isOver ? '+' : '' + variance.toFixed(1) + 'h').fontSize(12).fontColor(isOver ? '#ff6600' : '#00cc66').width(50)
          }

          Stack() {
            Row().width('100%').height(6).backgroundColor('#333').borderRadius(3)
            Row().width(`${Math.min(100, absVar * 10)}%`).height(6)
              .backgroundColor(isOver ? '#ff6600' : '#00cc66').borderRadius(3)
          }
          .layoutWeight(1).height(6)

          Text(`${isOver ? '超计划' : '节余'} ${absVar.toFixed(1)}h`).fontSize(10).fontColor('#555').margin({ left: 8 })
        }
        .width('100%').height(36)
        .padding({ left: 4, right: 4 })
      })
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12 })
  }

  @Builder
  OvertimeTrendBuilder() {
    Column() {
      Text('🔥 加班趋势').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      const hasOvertime = this.trend.some(item => (item.overtime as number) > 0);

      if (!hasOvertime) {
        Row() {
          Text('✅ 近8周无加班记录').fontSize(14).fontColor('#00cc66')
        }
        .width('100%').padding(16)
        .backgroundColor('rgba(0,204,102,0.05)').borderRadius(8)
      } else {
        ForEach(this.trend, (item: Record<string, Object>) => {
          if ((item.overtime as number) > 0) {
            Row() {
              Text((item.week as string) || '').fontSize(12).fontColor('#888').width(44)
              Row() {
                Stack() {
                  Row().width('100%').height(8).backgroundColor('#333').borderRadius(4)
                  Row().width(`${Math.min(100, (item.overtime as number) * 5)}%`).height(8)
                    .backgroundColor('#ff6600').borderRadius(4)
                }
                .layoutWeight(1).height(8)
              }
              Text(`${item.overtime}h`).fontSize(12).fontWeight(FontWeight.Bold).fontColor('#ff6600').margin({ left: 8 }).width(36)
            }
            .width('100%').height(32)
          }
        })

        const totalOvertime = this.trend.reduce((sum, item) => sum + ((item.overtime as number) || 0), 0);
        Text(`近8周累计加班: ${totalOvertime.toFixed(1)}h`).fontSize(12).fontColor('#ff6600').margin({ top: 8 }).width('100%')
      }
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12 })
  }

  @Builder
  DataTableBuilder() {
    Column() {
      Text('📋 数据明细').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 12 }).alignSelf(ItemAlign.Start)

      // 表头
      Row() {
        Text('周').fontSize(11).fontColor('#888').width(36)
        Text('计划(h)').fontSize(11).fontColor('#0088ff').layoutWeight(1).textAlign(TextAlign.Center)
        Text('实际(h)').fontSize(11).fontColor('#c41e3a').layoutWeight(1).textAlign(TextAlign.Center)
        Text('加班(h)').fontSize(11).fontColor('#ff6600').layoutWeight(1).textAlign(TextAlign.Center)
        Text('偏差').fontSize(11).fontColor('#888').layoutWeight(1).textAlign(TextAlign.Center)
      }
      .width('100%').height(28).padding({ left: 4, right: 4 })
      .backgroundColor('rgba(255,255,255,0.05)').borderRadius(4).margin({ bottom: 4 })

      // 数据行
      ForEach(this.trend, (item: Record<string, Object>) => {
        const variance = (item.actual as number) - (item.planned as number);
        Row() {
          Text((item.week as string) || '').fontSize(12).fontColor('#aaa').width(36)
          Text(`${item.planned}`).fontSize(12).fontColor('#0088ff').layoutWeight(1).textAlign(TextAlign.Center)
          Text(`${item.actual}`).fontSize(12).fontColor('#c41e3a').layoutWeight(1).textAlign(TextAlign.Center)
          Text(`${item.overtime}`).fontSize(12).fontColor('#ff6600').layoutWeight(1).textAlign(TextAlign.Center)
          Text(`${variance >= 0 ? '+' : ''}${variance.toFixed(1)}`)
            .fontSize(11).fontColor(variance >= 0 ? '#ff6600' : '#00cc66')
            .layoutWeight(1).textAlign(TextAlign.Center)
        }
        .width('100%').height(30).padding({ left: 4, right: 4 })
        .border({ width: { bottom: 0.5 }, color: '#222' })
      })
    }
    .width('100%').padding(16)
    .backgroundColor('#1a1a1a').borderRadius(8)
    .margin({ left: 12, right: 12, top: 12, bottom: 16 })
  }

  @Builder
  LegendItem(label: string, color: string, line: string) {
    Row() {
      Text(line).fontSize(14).fontColor(color).margin({ right: 4 })
      Text(label).fontSize(11).fontColor('#888')
    }
    .margin({ right: 16 })
  }

  getAvgPlannedHours(): string {
    if (this.trend.length === 0) return '0';
    return (this.trend.reduce((s, i) => s + (i.planned as number), 0) / this.trend.length).toFixed(1);
  }

  getAvgActualHours(): string {
    if (this.trend.length === 0) return '0';
    return (this.trend.reduce((s, i) => s + (i.actual as number), 0) / this.trend.length).toFixed(1);
  }

  getAvgOvertimeHours(): string {
    if (this.trend.length === 0) return '0';
    return (this.trend.reduce((s, i) => s + ((i.overtime as number) || 0), 0) / this.trend.length).toFixed(1);
  }

  isTrendUp(): boolean {
    if (this.trend.length < 2) return false;
    const last = this.trend[this.trend.length - 1];
    const first = this.trend[0];
    return (last.actual as number) > (first.actual as number);
  }
}
