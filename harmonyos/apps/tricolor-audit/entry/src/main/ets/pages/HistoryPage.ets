/**
 * 龙魂·历史页 — 审计记录列表
 * License: MulanPSL v2
 */
import { AuditRecord } from '../models/AuditModels';
import { DARK_GOLD, COLOR_MAP } from '../models/Constants';
import { StorageHelper } from '../utils/StorageHelper';
import { AuditResultCard } from '../components/AuditResultCard';
import router from '@ohos.router';

@Entry
@Component
struct HistoryPage {
  @State records: AuditRecord[] = [];
  @State isLoading: boolean = true;
  private storage: StorageHelper = new StorageHelper();

  async aboutToAppear() {
    await this.loadRecords();
  }

  async loadRecords() {
    this.isLoading = true;
    try {
      await this.storage.init();
      this.records = await this.storage.getAuditRecords();
    } catch (e) {
      console.error(`[龙魂审计] 加载历史失败: ${e}`);
    }
    this.isLoading = false;
  }

  build() {
    Column() {
      // 标题
      Row() {
        Text('←')
          .fontSize(24)
          .fontColor(DARK_GOLD.PRIMARY)
          .onClick(() => router.back())
        Text('审计历史')
          .fontSize(20)
          .fontColor(DARK_GOLD.TEXT_PRIMARY)
          .margin({ left: 12 })
        Text(`共 ${this.records.length} 条`)
          .fontSize(12)
          .fontColor(DARK_GOLD.TEXT_SECONDARY)
          .layoutWeight(1)
          .textAlign(TextAlign.End)
      }
      .width('100%')
      .padding(16)

      if (this.isLoading) {
        LoadingProgress()
          .color(DARK_GOLD.PRIMARY)
          .width(40)
          .height(40)
          .margin({ top: 100 })
        Text('加载审计记录...')
          .fontSize(14)
          .fontColor(DARK_GOLD.TEXT_SECONDARY)
          .margin({ top: 12 })
      } else if (this.records.length === 0) {
        Column() {
          Text('📭')
            .fontSize(48)
            .margin({ top: 80, bottom: 12 })
          Text('暂无审计记录')
            .fontSize(16)
            .fontColor(DARK_GOLD.TEXT_SECONDARY)
          Text('执行一次审计后在此处查看')
            .fontSize(12)
            .fontColor(DARK_GOLD.TEXT_SECONDARY)
            .margin({ top: 4 })
        }
        .width('100%')
        .alignItems(HorizontalAlign.Center)
      } else {
        List() {
          ForEach(this.records, (record: AuditRecord) => {
            ListItem() {
              Row() {
                Text(record.color)
                  .fontSize(28)
                Column() {
                  Text(record.target)
                    .fontSize(14)
                    .fontColor(DARK_GOLD.TEXT_PRIMARY)
                    .maxLines(1)
                  Text(`R=${record.rValue.toFixed(3)} · ${record.timestamp}`)
                    .fontSize(10)
                    .fontColor(DARK_GOLD.TEXT_SECONDARY)
                }
                .layoutWeight(1)
                .margin({ left: 8 })
                .alignItems(HorizontalAlign.Start)
              }
              .width('100%')
              .padding(12)
              .backgroundColor(DARK_GOLD.BG_CARD)
              .borderRadius(8)
              .margin({ bottom: 6, left: 16, right: 16 })
            }
          })
        }
        .layoutWeight(1)
      }

      // 刷新按钮
      Button('🔄 刷新')
        .fontSize(14)
        .backgroundColor(DARK_GOLD.BG_CARD)
        .fontColor(DARK_GOLD.PRIMARY)
        .border({ width: 1, color: DARK_GOLD.BORDER })
        .borderRadius(8)
        .margin({ bottom: 16 })
        .onClick(() => { this.loadRecords(); })
    }
    .width('100%')
    .height('100%')
    .backgroundColor(DARK_GOLD.BG_DARK)
  }
}
