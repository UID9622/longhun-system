/**
 * 🐉 龍魂·PersonalityMatrix + LayerDetail 页面
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-PERSONALITY-MATRIX-UID9622
 */

import { DashboardViewModel } from '../model/DashboardViewModel';
import { PersonaCard } from '../components/PersonaCard';
import { StatusRing } from '../components/StatusRing';
import { router } from '@kit.ArkUI';

// ─── 14人格矩阵全页 ───
@Entry
@Component
struct PersonalityMatrix {
  @State viewModel: DashboardViewModel = new DashboardViewModel();

  build() {
    Column() {
      Row() {
        Text('← 返回')
          .fontSize(14).fontColor('#C9A84C')
          .onClick(() => { router.back(); })
        Blank()
        Text('完整人格矩陣')
          .fontSize(18).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      }
      .width('100%').padding(16)

      // 统计
      Row() {
        Text(`活躍: ${this.viewModel.personas.filter(p => p.active).length}/14`)
          .fontSize(11).fontColor('#4ADE80').margin({ right: 12 })
        Text(`平均健康: ${Math.round(this.viewModel.personas.reduce((s, p) => s + p.health, 0) / this.viewModel.personas.length)}%`)
          .fontSize(11).fontColor('#6B7280')
      }
      .width('100%').padding({ left: 16, bottom: 8 })

      List() {
        ForEach(this.viewModel.personas, (p: Record<string, Object>) => {
          ListItem() {
            PersonaCard({
              id: p.id as string,
              name: p.name as string,
              role: p.role as string,
              weight: p.weight as number,
              active: p.active as boolean,
              health: p.health as number
            })
          }
        })
      }
      .layoutWeight(1)
    }
    .width('100%').height('100%')
    .backgroundColor('#0F172A')
  }
}

// ─── 单层监督详情 ───
@Entry
@Component
struct LayerDetail {
  @State layerIndex: number = 0;
  @State viewModel: DashboardViewModel = new DashboardViewModel();
  private layerNames: string[] = ['L1 決策層監督', 'L2 執行層監督', 'L3 行爲層監督'];
  private layerDescs: string[] = [
    '意圖解析·多路徑推演·貢獻值評估·時間衰減判定',
    '代碼審計·資源優化·部署驗證·自動回滾',
    '交互溫度·情感隔離·道德底線·一票否決詞檢測'
  ];

  aboutToAppear(): void {
    const params = router.getParams() as Record<string, Object>;
    this.layerIndex = (params?.['layer'] as number) ?? 0;
  }

  build() {
    Column() {
      Row() {
        Text('←').fontSize(16).fontColor('#C9A84C')
          .onClick(() => { router.back(); })
        Blank()
        Text(this.layerNames[this.layerIndex])
          .fontSize(18).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      }
      .width('100%').padding(16)

      Scroll() {
        Column({ space: 16 }) {
          // 描述
          Text(this.layerDescs[this.layerIndex])
            .fontSize(13).fontColor('#9CA3AF')
            .width('100%').padding(16)
            .backgroundColor('#1E293B').borderRadius(10)
            .margin({ left: 16, right: 16 })

          // 大号环形图
          Row() { StatusRing({ value: 92, label: '健康度', size: 140 }) }
            .width('100%').justifyContent(FlexAlign.Center)

          // 详情区
          Text('最近攔截')
            .fontSize(14).fontColor('#C9A84C')
            .width('100%').padding({ left: 16, top: 8 })

          ForEach(['P04魯班·技術執行', 'P05上帝之眼·三色審計', 'P12屈原·價值底線'], (item: string) => {
            Row() {
              Text(item).fontSize(13).fontColor('#E5E7EB').layoutWeight(1)
              Text('🟢').fontSize(14)
            }
            .width('100%').padding({ left: 24, right: 16, top: 10, bottom: 10 })
            .backgroundColor('#1E293B')
            .border({ width: { bottom: 0.5 }, color: '#334155', style: BorderStyle.Solid })
          })
        }
        .width('100%')
      }
      .layoutWeight(1)
    }
    .width('100%').height('100%')
    .backgroundColor('#0F172A')
  }
}
