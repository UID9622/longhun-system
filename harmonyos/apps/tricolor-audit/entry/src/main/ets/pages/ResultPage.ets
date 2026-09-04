/**
 * 龙魂·结果页 — 三色标记 + 六维详情 + 主权印章
 * License: MulanPSL v2
 */
import { AuditResult, DimensionScore } from '../models/AuditModels';
import { DARK_GOLD } from '../models/Constants';
import { TricolorBadge } from '../components/TricolorBadge';
import { DimensionSlider } from '../components/DimensionSlider';
import { SovereigntySeal } from '../components/SovereigntySeal';
import { DNAGenerator } from '../engine/DNAGenerator';
import { StorageHelper } from '../utils/StorageHelper';
import promptAction from '@ohos.promptAction';
import router from '@ohos.router';

@Entry
@Component
struct ResultPage {
  @State result: AuditResult | null = null;
  @State saved: boolean = false;
  private storage: StorageHelper = new StorageHelper();

  aboutToAppear() {
    const raw = AppStorage.get<string>('lastAuditResult');
    if (raw) {
      this.result = JSON.parse(raw);
    }
  }

  build() {
    if (!this.result) {
      Column() {
        Text('无审计结果')
          .fontSize(18)
          .fontColor(DARK_GOLD.TEXT_PRIMARY)
      }
      .width('100%')
      .height('100%')
      .backgroundColor(DARK_GOLD.BG_DARK)
      return;
    }

    Scroll() {
      Column() {
        // 头部：三色标记 + R值
        Row() {
          TricolorBadge({ color: this.result!.color, size: 56 })
          Column() {
            Text(`R = ${this.result!.rValue.toFixed(3)}`)
              .fontSize(28)
              .fontColor(DARK_GOLD.PRIMARY)
            Text(this.result!.summary)
              .fontSize(12)
              .fontColor(DARK_GOLD.TEXT_PRIMARY)
              .maxLines(2)
          }
          .layoutWeight(1)
          .margin({ left: 12 })
          .alignItems(HorizontalAlign.Start)
        }
        .width('90%')
        .padding(16)
        .backgroundColor(DARK_GOLD.BG_CARD)
        .borderRadius(12)
        .border({ width: 1, color: DARK_GOLD.BORDER })
        .margin({ bottom: 16 })

        // 六维详情
        Text('六维评分')
          .fontSize(16)
          .fontColor(DARK_GOLD.TEXT_PRIMARY)
          .width('90%')
          .margin({ bottom: 8 })

        Column() {
          ForEach(this.result!.scores, (item: DimensionScore, idx: number) => {
            DimensionSlider({ dimension: item, index: idx })
          })
        }
        .width('90%')
        .padding(12)
        .backgroundColor(DARK_GOLD.BG_CARD)
        .borderRadius(8)
        .margin({ bottom: 16 })

        // 主权印章
        Text('主权印章')
          .fontSize(16)
          .fontColor(DARK_GOLD.TEXT_PRIMARY)
          .width('90%')
          .margin({ bottom: 8 })

        SovereigntySeal({
          dna: this.result!.dna,
          creator: this.result!.sovereignSeal.sovereign,
          timestamp: this.result!.timestamp
        })

        // 操作按钮
        Row() {
          Button(this.saved ? '✅ 已保存' : '💾 保存记录')
            .fontSize(14)
            .backgroundColor(DARK_GOLD.BG_CARD)
            .fontColor(DARK_GOLD.PRIMARY)
            .border({ width: 1, color: DARK_GOLD.BORDER })
            .borderRadius(8)
            .enabled(!this.saved)
            .onClick(() => { this.saveRecord(); })

          Button('返回首页')
            .fontSize(14)
            .backgroundColor(DARK_GOLD.PRIMARY)
            .fontColor(DARK_GOLD.BG_DARK)
            .borderRadius(8)
            .margin({ left: 12 })
            .onClick(() => {
              router.pushUrl({ url: 'pages/Index' });
            })
        }
        .width('90%')
        .margin({ top: 16, bottom: 30 })
        .justifyContent(FlexAlign.SpaceEvenly)
      }
      .width('100%')
      .padding({ top: 16 })
      .alignItems(HorizontalAlign.Center)
    }
    .width('100%')
    .height('100%')
    .backgroundColor(DARK_GOLD.BG_DARK)
  }

  async saveRecord() {
    if (!this.result || this.saved) return;
    try {
      await this.storage.init();
      await this.storage.saveAuditRecord(this.result);
      this.saved = true;
      promptAction.showToast({ message: '审计记录已保存', duration: 2000 });
    } catch (e) {
      promptAction.showToast({ message: `保存失败: ${e}`, duration: 3000 });
    }
  }
}
