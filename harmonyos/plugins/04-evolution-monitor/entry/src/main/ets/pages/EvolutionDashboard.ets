/**
 * 🐉 龍魂·EvolutionDashboard — 进化仪表盘 + 版本历史 + 规则编辑器
 * DNA:   #龍芯⚡️丙午·癸未·乙酉·坤卦-EVOLUTION-PAGES-UID9622
 */

import { router } from '@kit.ArkUI';

// ─── 进化状态类型 ───
interface VersionInfo {
  version: string; dna: string; timestamp: string; tricolor: string;
  changes: string[]; metrics: Record<string, number>;
}
interface RuleInfo {
  name: string; layer: string; threshold: number; confidence: number; tricolor: string; dna: string;
}

// ─── 进化仪表盘主页 ───
@Entry
@Component
struct EvolutionDashboard {
  @State version: string = 'v1.0.3-harmonyos';
  @State health: number = 92;
  @State cycles: number = 7;
  @State versions: VersionInfo[] = [
    { version: 'v1.0.3', dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-EVO-v1.0.3', timestamp: '2026-08-06 01:00', tricolor: '🟢', changes: ['安全熵阈值优化', 'IPC超时增加重试'], metrics: { intercept: 96, health: 92, entropy: 0.12 } },
    { version: 'v1.0.2', dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-EVO-v1.0.2', timestamp: '2026-08-05 20:00', tricolor: '🟢', changes: ['新增一票否决词检测'], metrics: { intercept: 94, health: 90, entropy: 0.15 } },
    { version: 'v1.0.1', dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-EVO-v1.0.1', timestamp: '2026-08-05 12:00', tricolor: '🟡', changes: ['人格矩阵权重校准'], metrics: { intercept: 91, health: 86, entropy: 0.22 } },
    { version: 'v1.0.0', dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-EVO-v1.0.0', timestamp: '2026-08-05 00:00', tricolor: '🟢', changes: ['鸿蒙生态初始版本'], metrics: { intercept: 88, health: 85, entropy: 0.25 } },
  ];

  build() {
    Scroll() {
      Column({ space: 12 }) {
        Row() {
          Text('🐉 進化監控').fontSize(20).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
          Blank()
          Text(`週期#${this.cycles}`).fontSize(11).fontColor('#6B7280')
        }.width('100%').padding(16)

        // 健康度仪表
        Card('系統健康度') {
          Row({ space: 20 }) {
            this.buildGauge('攔截率', this.versions[0].metrics.intercept, '#4ADE80')
            this.buildGauge('健康度', this.health, '#C9A84C')
            this.buildGauge('熵值', Math.round(this.versions[0].metrics.entropy * 100), '#F4A261')
          }.justifyContent(FlexAlign.SpaceEvenly).width('100%')
        }

        // 版本演进时间线
        Row() {
          Text('版本演進').fontSize(14).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
          Blank()
          Text(`全部 ${this.versions.length} 版`).fontSize(11).fontColor('#6B7280')
        }.width('100%').padding({ left: 16, right: 16, top: 8 })

        ForEach(this.versions, (v: VersionInfo, idx: number) => {
          Row() {
            Column() {
              Circle({ width: 12, height: 12 }).fill(v.tricolor === '🟢' ? '#4ADE80' : '#F4A261')
              if (idx < this.versions.length - 1) {
                Divider().vertical(true).height(24).width(1).color('#1E293B')
              }
            }.alignItems(HorizontalAlign.Center)

            Column({ space: 2 }) {
              Row({ space: 6 }) {
                Text(v.version).fontSize(13).fontColor('#E5E7EB').fontWeight(FontWeight.Medium)
                Text(v.tricolor).fontSize(14)
              }
              Text(v.timestamp).fontSize(9).fontColor('#6B7280')
              Text(v.changes.join(' · ')).fontSize(10).fontColor('#9CA3AF').maxLines(1)
            }.alignItems(HorizontalAlign.Start).margin({ left: 10 }).layoutWeight(1)

            Text('→').fontSize(14).fontColor('#6B7280')
          }
          .width('100%').padding({ left: 16, right: 16, top: 6, bottom: 6 })
          .onClick(() => { router.pushUrl({ url: 'pages/VersionHistory', params: { version: idx } }); })
        })

        // 规则入口
        Row() {
          Text('監督規則').fontSize(14).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
          Blank()
          Text('查看 →').fontSize(12).fontColor('#C9A84C')
        }.width('100%').padding({ left: 16, right: 16, top: 12 })
        .onClick(() => { router.pushUrl({ url: 'pages/RuleEditor' }); })

        Button('🔄 手動進化檢查').fontSize(13).width('90%').height(44)
          .backgroundColor('#1E293B').fontColor('#C9A84C')
          .border({ width: 1, color: '#C9A84C', style: BorderStyle.Solid }).borderRadius(22)
          .margin({ top: 8, bottom: 24 })
      }.width('100%')
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }

  @Builder buildGauge(label: string, value: number, color: string) {
    Column({ space: 4 }) {
      Text(`${value}%`).fontSize(22).fontColor(color).fontWeight(FontWeight.Bold)
      Text(label).fontSize(10).fontColor('#6B7280')
    }.alignItems(HorizontalAlign.Center)
  }
}

// ─── 版本历史 ───
@Entry
@Component
struct VersionHistory {
  @State versionIdx: number = 0;

  aboutToAppear(): void {
    const p = router.getParams() as Record<string, Object>;
    this.versionIdx = (p?.['version'] as number) ?? 0;
  }

  build() {
    Column() {
      Row() {
        Text('←').fontSize(16).fontColor('#C9A84C').onClick(() => { router.back(); })
        Blank()
        Text('版本詳情').fontSize(18).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      }.width('100%').padding(16)

      Column() {
        Text('v1.0.3').fontSize(24).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
        Text('#龍芯⚡️丙午·癸未·乙酉·坤卦-EVO-v1.0.3').fontSize(9).fontColor('#6B7280').fontFamily('monospace')
      }.width('100%').padding(16).backgroundColor('#1E293B')

      // 变更项
      ForEach(['安全熵阈值从0.3→0.25', 'IPC通信超时从5s→10s+重试3次', '新增P77黑天使联动检测'], (c: string) => {
        Row() {
          Text('•').fontSize(14).fontColor('#4ADE80').margin({ right: 8 })
          Text(c).fontSize(13).fontColor('#E5E7EB').layoutWeight(1)
        }.width('100%').padding({ left: 16, right: 16, top: 8, bottom: 8 })
      })
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }
}

// ─── 规则编辑器 ───
@Entry
@Component
struct RuleEditor {
  @State rules: RuleInfo[] = [
    { name: '拦截率阈值', layer: 'L2执行层', threshold: 95, confidence: 0.92, tricolor: '🟢', dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-RULE-INTERCEPT' },
    { name: '红队成功率', layer: 'L3行为层', threshold: 85, confidence: 0.88, tricolor: '🟢', dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-RULE-REDTEAM' },
    { name: '系统熵值', layer: 'L1决策层', threshold: 25, confidence: 0.90, tricolor: '🟡', dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-RULE-ENTROPY' },
    { name: '情感隔离率', layer: 'L3行为层', threshold: 30, confidence: 0.85, tricolor: '🟢', dna: '#龍芯⚡️丙午·癸未·乙酉·坤卦-RULE-ISOLATION' },
  ];

  build() {
    Column() {
      Row() {
        Text('←').fontSize(16).fontColor('#C9A84C').onClick(() => { router.back(); })
        Blank()
        Text('規則檢視').fontSize(18).fontColor('#C9A84C').fontWeight(FontWeight.Bold)
      }.width('100%').padding(16)

      List() {
        ForEach(this.rules, (r: RuleInfo) => {
          ListItem() {
            Column() {
              Row() {
                Text(r.name).fontSize(14).fontColor('#E5E7EB').fontWeight(FontWeight.Medium).layoutWeight(1)
                Text(r.tricolor).fontSize(16)
              }
              Row() {
                Text(`層: ${r.layer} | 閾值: ${r.threshold}% | 置信度: ${r.confidence}`).fontSize(10).fontColor('#6B7280')
                Blank()
                Text(r.dna.substring(0, 18) + '...').fontSize(8).fontColor('#4B5563').fontFamily('monospace')
              }.margin({ top: 4 })
            }
            .width('100%').padding(12)
            .backgroundColor('#1E293B').borderRadius(8).margin({ left: 16, right: 16, top: 4, bottom: 4 })
          }
        })
      }.layoutWeight(1)
    }
    .width('100%').height('100%').backgroundColor('#0F172A')
  }
}
