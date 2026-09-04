/**
 * 🐉 龍魂·Dashboard — 监督仪表盘主页面
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-DASHBOARD-PAGE-UID9622
 *
 * 系统状态条·三层视图·14人格矩阵·审计时间线·暗金主题
 */

import { DashboardViewModel } from '../model/DashboardViewModel';
import { StatusRing } from '../components/StatusRing';
import { PersonaCard } from '../components/PersonaCard';
import { router } from '@kit.ArkUI';

@Entry
@Component
struct Dashboard {
  @State viewModel: DashboardViewModel = new DashboardViewModel();
  @State refreshTime: string = '';

  aboutToAppear(): void {
    this.viewModel.refresh();
    this.refreshTime = new Date().toLocaleTimeString();
  }

  build() {
    Scroll() {
      Column({ space: 0 }) {
        // ─── 顶部状态条 ───
        Row() {
          Column({ space: 2 }) {
            Text('🐉 監督儀表盤')
              .fontSize(20)
              .fontColor('#C9A84C')
              .fontWeight(FontWeight.Bold)
            Text(this.viewModel.systemStatus)
              .fontSize(12)
              .fontColor('#9CA3AF')
          }

          Blank()

          Column({ space: 2 }) {
            Text(`週期 #${this.viewModel.supervisionCycle}`)
              .fontSize(11)
              .fontColor('#6B7280')
            Text(this.viewModel.uptime)
              .fontSize(10)
              .fontColor('#4B5563')
          }
        }
        .width('100%')
        .padding(16)

        // ─── 三层环形进度 ───
        Row({ space: 16 }) {
          StatusRing({ value: this.viewModel.L1.value, label: 'L1決策', sublabel: `攔截 ${this.viewModel.L1.interceptRate}%`, size: 90 })
          StatusRing({ value: this.viewModel.L2.value, label: 'L2執行', sublabel: `攔截 ${this.viewModel.L2.interceptRate}%`, size: 90 })
          StatusRing({ value: this.viewModel.L3.value, label: 'L3行爲', sublabel: `攔截 ${this.viewModel.L3.interceptRate}%`, size: 90 })
        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceEvenly)
        .padding({ top: 0, bottom: 16 })

        // ─── 三层详情入口 ───
        Text('三層監督')
          .fontSize(14)
          .fontColor('#C9A84C')
          .fontWeight(FontWeight.Bold)
          .width('100%')
          .padding({ left: 16, bottom: 8 })

        ForEach(['L1 決策層', 'L2 執行層', 'L3 行爲層'] as string[], (layer: string, idx: number) => {
          Row() {
            Text(layer)
              .fontSize(13)
              .fontColor('#E5E7EB')
              .layoutWeight(1)

            Text(idx === 0 ? '🟢' : idx === 1 ? '🟡' : '🟢')
              .fontSize(18)

            Text('→')
              .fontSize(14)
              .fontColor('#6B7280')
              .margin({ left: 8 })
          }
          .width('100%')
          .padding({ left: 16, right: 16, top: 10, bottom: 10 })
          .backgroundColor('#1E293B')
          .border({ width: { bottom: 0.5 }, color: '#334155', style: BorderStyle.Solid })
          .onClick(() => {
            router.pushUrl({ url: 'pages/LayerDetail', params: { layer: idx } });
          })
        })

        // ─── 人格矩阵滚动区 ───
        Row() {
          Text('人格矩陣')
            .fontSize(14)
            .fontColor('#C9A84C')
            .fontWeight(FontWeight.Bold)

          Blank()

          Text(`${this.viewModel.personas.length} / 14`)
            .fontSize(11)
            .fontColor('#6B7280')
        }
        .width('100%')
        .padding({ left: 16, right: 16, top: 16, bottom: 8 })

        Column() {
          ForEach(this.viewModel.personas.slice(0, 7), (p: Record<string, Object>) => {
            PersonaCard({
              id: p.id as string,
              name: p.name as string,
              role: p.role as string,
              weight: p.weight as number,
              active: p.active as boolean,
              health: p.health as number
            })
          })
        }
        .backgroundColor('#162032')
        .borderRadius(10)
        .margin({ left: 16, right: 16, bottom: 8 })
        .onClick(() => { router.pushUrl({ url: 'pages/PersonalityMatrix' }); })

        // ─── 审计时间线 ───
        Text('審計時間線')
          .fontSize(14)
          .fontColor('#C9A84C')
          .fontWeight(FontWeight.Bold)
          .width('100%')
          .padding({ left: 16, top: 8, bottom: 8 })

        Column({ space: 0 }) {
          ForEach(this.viewModel.auditEvents, (evt: Record<string, Object>, idx: number) => {
            Row() {
              Column() {
                Circle({ width: 10, height: 10 })
                  .fill('#C9A84C')
              }
              .width(20)
              .height('100%')
              .justifyContent(FlexAlign.Start)

              Column({ space: 2 }) {
                Text(evt.time as string)
                  .fontSize(9)
                  .fontColor('#6B7280')
                Text(evt.event as string)
                  .fontSize(11)
                  .fontColor('#E5E7EB')
              }
              .layoutWeight(1)

              Text(evt.tricolor as string)
                .fontSize(14)
            }
            .width('100%')
            .padding({ left: 16, right: 16, top: 6, bottom: 6 })
            .border({ width: { left: 1 }, color: '#1E293B', style: BorderStyle.Solid })
          })
        }

        // ─── 刷新按钮 ───
        Button('🔄 刷新儀表盤')
          .fontSize(13)
          .width('90%')
          .height(44)
          .backgroundColor('#1E293B')
          .fontColor('#C9A84C')
          .border({ width: 1, color: '#C9A84C', style: BorderStyle.Solid })
          .borderRadius(22)
          .margin({ top: 16, bottom: 24 })
          .onClick(() => {
            this.viewModel.refresh();
            this.refreshTime = new Date().toLocaleTimeString();
          })

        Text(`最後更新: ${this.refreshTime}`)
          .fontSize(9)
          .fontColor('#4B5563')
          .margin({ bottom: 16 })
      }
      .width('100%')
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0F172A')
    .scrollBar(BarState.Off)
  }
}
