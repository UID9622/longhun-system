// entry/src/main/ets/pages/PerformancePage.ets
// 龍魂 · 性能优化演示页面 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import {
  performanceState,
  PerformanceState,
  MetricType,
  PerformanceThreshold,
  OptimizeStrategy,
  PerformanceReport,
  PerformanceMetric
} from '../models/PerformanceModel';
import { perfMonitor } from '../utils/PerformanceMonitor';
import { LazyList } from '../components/LazyList';
import { AsyncImage } from '../components/AsyncImage';
import { ConditionalRender, DeferredRender, BatchedRender } from '../components/ConditionalRender';
import { PerformanceDatabase } from '../database/PerformanceDatabase';

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";

@Entry
@Component
struct PerformancePage {
  @StorageLink('performanceState') performanceState: PerformanceState = performanceState;
  @State private demoData: string[] = [];
  @State private showHeavyComponent: boolean = false;
  @State private selectedTab: number = 0;
  @State private pageName: string = 'PerformancePage';

  aboutToAppear(): void {
    // 生成1000条测试数据
    this.demoData = Array.from({ length: 1000 }, (_, i) => `列表项 ${i + 1}`);
    PerformanceDatabase.init();

    // 开始首帧监控
    perfMonitor.monitorFirstFrame(this.pageName);
  }

  build() {
    Column() {
      this.HeaderBuilder()
      this.StatsBuilder()
      this.TabBuilder()
      this.ContentBuilder()
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // === 头部 ===
  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉')
        .fontSize(28)
        .margin({ right: 8 })

      Column() {
        Text('龍魂性能优化')
          .fontSize(20)
          .fontWeight(FontWeight.Bold)
          .fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · 首帧优化`)
          .fontSize(12)
          .fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Button('生成报告')
        .fontSize(12)
        .fontColor('#fff')
        .backgroundColor('#c41e3a')
        .borderRadius(8)
        .padding({ left: 12, right: 12 })
        .onClick(() => {
          perfMonitor.generateReport(this.pageName);
          PerformanceDatabase.saveReport(performanceState.reports[performanceState.reports.length - 1]);
        })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // === 统计卡片 ===
  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('首帧', `${this.performanceState.statistics.avgFirstFrameTime}ms`, this.getFirstFrameColor())
      this.StatCard('布局', `${this.performanceState.statistics.avgLayoutTime}ms`, this.getLayoutColor())
      this.StatCard('FPS', `${this.performanceState.statistics.avgFPS}`, this.getFPSColor())
      this.StatCard('优化率', `${this.performanceState.statistics.optimizationRate}%`, '#00ff00')
      this.StatCard('组件', `${this.performanceState.statistics.totalComponents}`, '#fff')
    }
    .width('100%')
    .height(80)
    .padding({ left: 12, right: 12, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  private getFirstFrameColor(): string {
    const time = this.performanceState.statistics.avgFirstFrameTime;
    if (time === 0) return '#666';
    if (time < 100) return '#00ff00';
    if (time < 300) return '#88ff00';
    if (time < 500) return '#ffcc00';
    if (time < 1000) return '#ff6600';
    return '#ff0000';
  }

  private getLayoutColor(): string {
    const time = this.performanceState.statistics.avgLayoutTime;
    if (time === 0) return '#666';
    if (time < 50) return '#00ff00';
    if (time < 100) return '#88ff00';
    if (time < 200) return '#ffcc00';
    if (time < 500) return '#ff6600';
    return '#ff0000';
  }

  private getFPSColor(): string {
    const fps = this.performanceState.statistics.avgFPS;
    if (fps >= 55) return '#00ff00';
    if (fps >= 45) return '#88ff00';
    if (fps >= 30) return '#ffcc00';
    if (fps >= 15) return '#ff6600';
    return '#ff0000';
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value)
        .fontSize(20)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(11)
        .fontColor('#666')
        .margin({ top: 4 })
    }
    .width('20%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }

  // === 标签栏 ===
  @Builder
  TabBuilder() {
    Row() {
      ForEach(
        [
          { label: '懒加载', icon: '📋', desc: 'LazyForEach' },
          { label: '异步', icon: '⏳', desc: 'Async Render' },
          { label: '监控', icon: '📊', desc: 'Monitor' },
          { label: '报告', icon: '📈', desc: 'Report' }
        ],
        (item: { label: string; icon: string; desc: string }, index: number) => {
          Column() {
            Text(`${item.icon} ${item.label}`)
              .fontSize(13)
              .fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal)
              .fontColor(this.selectedTab === index ? '#c41e3a' : '#888')
            Text(item.desc)
              .fontSize(10)
              .fontColor(this.selectedTab === index ? '#c41e3a' : '#555')
              .margin({ top: 2 })

            if (this.selectedTab === index) {
              Divider()
                .strokeWidth(2)
                .color('#c41e3a')
                .width(20)
                .margin({ top: 4 })
            }
          }
          .padding({ top: 12, bottom: 12, left: 16, right: 16 })
          .onClick(() => { this.selectedTab = index })
        }
      )
    }
    .width('100%')
    .justifyContent(FlexAlign.SpaceAround)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  // === 内容区 ===
  @Builder
  ContentBuilder() {
    if (this.selectedTab === 0) {
      this.LazyLoadDemoBuilder()
    } else if (this.selectedTab === 1) {
      this.AsyncDemoBuilder()
    } else if (this.selectedTab === 2) {
      this.MonitorDemoBuilder()
    } else {
      this.ReportDemoBuilder()
    }
  }

  // === 懒加载演示 ===
  @Builder
  LazyLoadDemoBuilder() {
    Column() {
      Text('LazyForEach 懒加载演示')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ bottom: 12 })
        .width('100%')

      Row() {
        Text(`数据量: ${this.demoData.length} 条`)
          .fontSize(12)
          .fontColor('#666')
        Text(' · 仅渲染可见项')
          .fontSize(12)
          .fontColor('#c41e3a')
        Text(' · 缓冲5项')
          .fontSize(12)
          .fontColor('#666')
      }
      .width('100%')
      .margin({ bottom: 12 })

      // 懒加载列表
      LazyList<string>({
        data: this.demoData,
        itemHeight: 56,
        bufferSize: 5,
        pageName: this.pageName,
        itemBuilder: (item: string, index: number) => {
          Row() {
            Text(`${index + 1}`)
              .fontSize(12)
              .fontColor('#666')
              .width(40)
              .textAlign(TextAlign.Center)

            Text(item)
              .fontSize(14)
              .fontColor('#fff')
              .layoutWeight(1)

            Text('›')
              .fontSize(18)
              .fontColor('#666')
          }
          .width('100%')
          .height('100%')
          .padding({ left: 16, right: 16 })
          .backgroundColor('#1a1a1a')
        }
      })
      .layoutWeight(1)
    }
    .width('100%')
    .padding(16)
    .layoutWeight(1)
  }

  // === 异步渲染演示 ===
  @Builder
  AsyncDemoBuilder() {
    Scroll() {
      Column() {
        Text('异步渲染演示')
          .fontSize(16)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
          .margin({ bottom: 12 })
          .width('100%')

        // 异步图片加载
        Text('异步图片加载 (LRU缓存)')
          .fontSize(14)
          .fontColor('#c41e3a')
          .margin({ top: 12, bottom: 8 })
          .width('100%')

        Row() {
          AsyncImage({ src: 'https://example.com/image1.jpg', width: 100, height: 100 })
          AsyncImage({ src: 'https://example.com/image2.jpg', width: 100, height: 100 })
            .margin({ left: 12 })
          AsyncImage({ src: 'https://example.com/image3.jpg', width: 100, height: 100 })
            .margin({ left: 12 })
        }
        .width('100%')
        .margin({ bottom: 8 })

        Text(`缓存命中: ${AsyncImage.getCacheSize()} 张`)
          .fontSize(11)
          .fontColor('#666')
          .margin({ bottom: 16 })
          .width('100%')

        // 延迟渲染
        Text('延迟渲染 (DeferredRender)')
          .fontSize(14)
          .fontColor('#c41e3a')
          .margin({ top: 12, bottom: 8 })
          .width('100%')

        DeferredRender({
          delayMs: 200,
          priority: 'medium',
          contentBuilder: () => {
            Column() {
              ForEach(Array.from({ length: 5 }), (_, i) => {
                Row() {
                  Text(`延迟渲染项 ${i + 1}`)
                    .fontSize(12)
                    .fontColor('#00ff00')
                }
                .width('100%')
                .height(40)
                .padding({ left: 16 })
                .backgroundColor('#1a1a1a')
                .margin({ top: 4 })
                .borderRadius(4)
              })
            }
            .width('100%')
          }
        })
        .width('100%')
        .margin({ bottom: 16 })

        // 条件渲染
        Text('条件渲染 (按需加载)')
          .fontSize(14)
          .fontColor('#c41e3a')
          .margin({ top: 12, bottom: 8 })
          .width('100%')

        Row() {
          Button(this.showHeavyComponent ? '隐藏重组件' : '显示50项重组件')
            .fontSize(12)
            .fontColor('#fff')
            .backgroundColor(this.showHeavyComponent ? '#ff6600' : '#c41e3a')
            .borderRadius(8)
            .padding({ left: 16, right: 16 })
            .onClick(() => {
              const markName = 'heavy_component_toggle';
              perfMonitor.mark(markName);
              this.showHeavyComponent = !this.showHeavyComponent;
              perfMonitor.measure(markName, MetricType.RENDER_TIME, this.pageName, 'HeavyComponent');
            })

          Text(this.showHeavyComponent ? '已渲染50项' : '未渲染')
            .fontSize(12)
            .fontColor('#888')
            .margin({ left: 12 })
        }
        .width('100%')
        .margin({ bottom: 8 })

        ConditionalRender({
          condition: this.showHeavyComponent,
          deferTime: 100,
          pageName: this.pageName,
          componentName: 'HeavyComponent',
          trueBuilder: () => {
            Column() {
              ForEach(Array.from({ length: 50 }), (_, i) => {
                Row() {
                  Text(`重组件项 ${i + 1}`)
                    .fontSize(12)
                    .fontColor('#fff')
                  Text(`${Math.round(Math.random() * 100)}ms`)
                    .fontSize(10)
                    .fontColor('#666')
                    .margin({ left: 8 })
                }
                .width('100%')
                .height(40)
                .padding({ left: 16, right: 16 })
                .backgroundColor('#1a1a1a')
                .margin({ top: 4 })
                .borderRadius(4)
              })
            }
            .width('100%')
          }
        })
        .width('100%')
        .margin({ top: 8 })

        // 分批渲染
        Text('分批渲染 (BatchedRender)')
          .fontSize(14)
          .fontColor('#c41e3a')
          .margin({ top: 16, bottom: 8 })
          .width('100%')

        BatchedRender({
          items: Array.from({ length: 30 }, (_, i) => `批次项 ${i + 1}`),
          batchSize: 10,
          intervalMs: 100,
          itemBuilder: (item: string, index: number) => {
            Row() {
              Text(item)
                .fontSize(12)
                .fontColor('#fff')
            }
            .width('100%')
            .height(36)
            .padding({ left: 16 })
            .backgroundColor('#1a1a1a')
            .margin({ top: 4 })
            .borderRadius(4)
          }
        })
        .width('100%')
        .margin({ bottom: 16 })
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  // === 监控演示 ===
  @Builder
  MonitorDemoBuilder() {
    Column() {
      Text('实时性能监控')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ bottom: 12 })
        .width('100%')

      // 实时指标
      Row() {
        this.MonitorCard('FPS', `${this.performanceState.currentFPS}`, this.getFPSColor())
        this.MonitorCard(
          '内存',
          `${this.performanceState.currentMemory}MB`,
          this.performanceState.currentMemory < 100 ? '#00ff00' : this.performanceState.currentMemory < 200 ? '#ffcc00' : '#ff0000'
        )
        this.MonitorCard(
          'CPU',
          `${this.performanceState.currentCPU}%`,
          this.performanceState.currentCPU < 30 ? '#00ff00' : this.performanceState.currentCPU < 70 ? '#ffcc00' : '#ff0000'
        )
      }
      .width('100%')
      .margin({ bottom: 16 })

      // FPS详情
      if (this.performanceState.isMonitoring) {
        Row() {
          const fpsStats = perfMonitor.getFPSStats();
          Text(`FPS详情: 当前${fpsStats.current} · 平均${fpsStats.avg} · 最低${fpsStats.min} · 最高${fpsStats.max}`)
            .fontSize(11)
            .fontColor('#888')
        }
        .width('100%')
        .margin({ bottom: 12 })
        .padding(8)
        .backgroundColor('#1a1a1a')
        .borderRadius(8)
      }

      // 操作按钮
      Text('监控控制')
        .fontSize(14)
        .fontColor('#fff')
        .margin({ top: 12, bottom: 8 })
        .width('100%')

      Row() {
        Button('开始监控')
          .fontSize(12)
          .fontColor('#000')
          .backgroundColor('#00ff00')
          .borderRadius(8)
          .padding({ left: 12, right: 12 })
          .onClick(() => {
            perfMonitor.startComprehensiveMonitor();
          })

        Button('停止监控')
          .fontSize(12)
          .fontColor('#fff')
          .backgroundColor('#ff0000')
          .borderRadius(8)
          .padding({ left: 12, right: 12 })
          .margin({ left: 8 })
          .onClick(() => {
            perfMonitor.stopComprehensiveMonitor();
          })

        Button('记录首帧')
          .fontSize(12)
          .fontColor('#fff')
          .backgroundColor('#333')
          .borderRadius(8)
          .padding({ left: 12, right: 12 })
          .margin({ left: 8 })
          .onClick(() => {
            perfMonitor.monitorFirstFrame(this.pageName);
          })
      }
      .width('100%')
      .margin({ bottom: 16 })

      // 优化检查
      Row() {
        Button('运行优化检查')
          .fontSize(12)
          .fontColor('#fff')
          .backgroundColor('#c41e3a')
          .borderRadius(8)
          .padding({ left: 12, right: 12 })
          .onClick(() => {
            const result = perfMonitor.runOptimizationCheck(this.pageName);
            console.info(`[龍魂] 优化检查完成: ${result.passedCount}/${result.totalChecks} 通过, 得分: ${result.score}`);
          })
      }
      .width('100%')
      .margin({ bottom: 16 })

      // 最近指标
      Text('最近指标记录')
        .fontSize(14)
        .fontColor('#fff')
        .margin({ top: 12, bottom: 8 })
        .width('100%')

      List() {
        ForEach(this.performanceState.metrics.slice(-20).reverse(), (metric: PerformanceMetric) => {
          ListItem() {
            Row() {
              Column() {
                Text(metric.name)
                  .fontSize(12)
                  .fontColor('#fff')
                Text(metric.pageName)
                  .fontSize(10)
                  .fontColor('#555')
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)

              Text(`${metric.value}${metric.unit}`)
                .fontSize(14)
                .fontWeight(FontWeight.Bold)
                .fontColor(metric.getThresholdColor())

              Text(metric.getThresholdLabel())
                .fontSize(11)
                .fontColor('#666')
                .margin({ left: 8 })
                .backgroundColor('rgba(255,255,255,0.05)')
                .borderRadius(4)
                .padding({ left: 6, right: 6, top: 2, bottom: 2 })
            }
            .width('100%')
            .padding(8)
            .backgroundColor('#1a1a1a')
            .borderRadius(8)
          }
          .margin({ bottom: 4 })
        })
      }
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)
    }
    .width('100%')
    .padding(16)
    .layoutWeight(1)
  }

  @Builder
  MonitorCard(label: string, value: string, color: string) {
    Column() {
      Text(value)
        .fontSize(24)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(11)
        .fontColor('#666')
        .margin({ top: 4 })
    }
    .width('33%')
    .height(80)
    .backgroundColor('#1a1a1a')
    .borderRadius(8)
    .justifyContent(FlexAlign.Center)
  }

  // === 报告演示 ===
  @Builder
  ReportDemoBuilder() {
    Column() {
      Text('性能报告')
        .fontSize(16)
        .fontWeight(FontWeight.Bold)
        .fontColor('#fff')
        .margin({ bottom: 12 })
        .width('100%')

      if (this.performanceState.reports.length === 0) {
        Column() {
          Text('暂无报告')
            .fontSize(14)
            .fontColor('#666')
          Text('点击右上角"生成报告"按钮')
            .fontSize(12)
            .fontColor('#444')
            .margin({ top: 4 })
        }
        .width('100%')
        .height(200)
        .justifyContent(FlexAlign.Center)
        .alignItems(HorizontalAlign.Center)
      }

      ForEach(this.performanceState.reports, (report: PerformanceReport) => {
        Column() {
          // 报告头部
          Row() {
            Text(report.pageName)
              .fontSize(14)
              .fontWeight(FontWeight.Medium)
              .fontColor('#fff')
              .layoutWeight(1)

            Text(`${report.getScore()}分`)
              .fontSize(16)
              .fontWeight(FontWeight.Bold)
              .fontColor(report.getScoreColor())
          }
          .width('100%')
          .margin({ bottom: 8 })

          // 指标汇总
          Row() {
            this.ReportBadge('优秀', report.excellentCount, '#00ff00')
            this.ReportBadge('良好', report.goodCount, '#88ff00')
            this.ReportBadge('一般', report.fairCount, '#ffcc00')
            this.ReportBadge('较差', report.poorCount, '#ff6600')
            this.ReportBadge('严重', report.criticalCount, '#ff0000')
          }
          .width('100%')
          .margin({ bottom: 8 })

          // 关键时间
          Row() {
            Text(`首帧: ${report.firstFrameTime}ms`)
              .fontSize(11)
              .fontColor(report.firstFrameTime < 300 ? '#00ff00' : '#ffcc00')
            Text(`布局: ${report.layoutCalcTime}ms`)
              .fontSize(11)
              .fontColor(report.layoutCalcTime < 100 ? '#00ff00' : '#ffcc00')
              .margin({ left: 12 })
            Text(`总指标: ${report.totalMetrics}`)
              .fontSize(11)
              .fontColor('#666')
              .margin({ left: 12 })
          }
          .width('100%')
          .margin({ bottom: 8 })

          // 优化建议
          if (report.suggestions.length > 0) {
            Text('优化建议:')
              .fontSize(12)
              .fontColor('#ffcc00')
              .margin({ bottom: 4 })

            ForEach(report.suggestions, (suggestion) => {
              Row() {
                Text('•')
                  .fontSize(12)
                  .fontColor('#c41e3a')
                  .margin({ right: 6 })

                Column() {
                  Text(suggestion.title)
                    .fontSize(12)
                    .fontColor('#fff')
                  Text(suggestion.impact)
                    .fontSize(10)
                    .fontColor('#666')
                    .margin({ top: 2 })
                }
                .alignItems(HorizontalAlign.Start)
                .layoutWeight(1)

                Text(suggestion.priority)
                  .fontSize(10)
                  .fontColor(
                    suggestion.priority === 'critical' ? '#ff0000' :
                    suggestion.priority === 'high' ? '#ff6600' :
                    suggestion.priority === 'medium' ? '#ffcc00' : '#888'
                  )
                  .backgroundColor('rgba(255,255,255,0.05)')
                  .borderRadius(4)
                  .padding({ left: 6, right: 6, top: 2, bottom: 2 })
              }
              .width('100%')
              .padding({ top: 4, bottom: 4 })
            })
          }
        }
        .width('100%')
        .padding(12)
        .backgroundColor('#1a1a1a')
        .borderRadius(8)
        .margin({ bottom: 8 })
      })
    }
    .width('100%')
    .padding(16)
    .layoutWeight(1)
  }

  @Builder
  ReportBadge(label: string, count: number, color: string) {
    Column() {
      Text(`${count}`)
        .fontSize(14)
        .fontWeight(FontWeight.Bold)
        .fontColor(color)
      Text(label)
        .fontSize(9)
        .fontColor('#666')
    }
    .width('20%')
    .alignItems(HorizontalAlign.Center)
  }

  // === 底部栏 ===
  @Builder
  FooterBuilder() {
    Row() {
      Column() {
        Text('🐉')
          .fontSize(20)
        Text(`UID:${MASTER_UID}`)
          .fontSize(10)
          .fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Row() {
        Text(`📊 ${this.performanceState.metrics.length} 指标`)
          .fontSize(12)
          .fontColor('#888')
        Text(`📈 ${this.performanceState.reports.length} 报告`)
          .fontSize(12)
          .fontColor('#888')
          .margin({ left: 12 })
      }
    }
    .width('100%')
    .height(40)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }
}
