// entry/src/main/ets/components/InventoryDetailDialog.ets
// 龍魂 · 物资详情弹窗

import { SupplyItem, ItemStatus, SupplyCategory, InventoryRecord, inventoryState } from '../models/InventoryModel';

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";

@CustomDialog
export struct InventoryDetailDialog {
  controller: CustomDialogController;
  item: SupplyItem;
  @State private currentTab: number = 0;

  build() {
    Column() {
      // 标题栏
      Row() {
        Text(this.item.name)
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
          .layoutWeight(1)

        Button() { Text('✕').fontSize(16).fontColor('#888') }
          .type(ButtonType.Circle)
          .backgroundColor('transparent')
          .width(32).height(32)
          .onClick(() => this.controller.close())
      }
      .width('100%')
      .padding(16)

      // 健康度条
      Row() {
        Text(`健康度 ${this.item.getHealthScore()}%`)
          .fontSize(12).fontColor('#888')
        Blank()
        Progress({ value: this.item.getHealthScore(), total: 100, type: ProgressType.Linear })
          .width(100).height(4)
          .color(
            this.item.getHealthScore() > 80 ? '#00ff00' :
            this.item.getHealthScore() > 50 ? '#ffcc00' : '#ff0000'
          )
          .backgroundColor('#333')
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 12 })

      // 标签切换
      Row() {
        ForEach(['基本信息', '库存详情', '流水记录'], (label: string, index: number) => {
          Column() {
            Text(label)
              .fontSize(13)
              .fontColor(this.currentTab === index ? '#c41e3a' : '#888')
              .fontWeight(this.currentTab === index ? FontWeight.Bold : FontWeight.Normal)
            if (this.currentTab === index) {
              Divider().strokeWidth(2).color('#c41e3a').width(20).margin({ top: 4 })
            }
          }
          .padding({ left: 16, right: 16, top: 8, bottom: 8 })
          .onClick(() => { this.currentTab = index; })
        })
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceAround)
      .border({ width: { bottom: 1 }, color: '#333' })

      // 内容区
      if (this.currentTab === 0) {
        this.BasicInfoTab()
      } else if (this.currentTab === 1) {
        this.StockDetailTab()
      } else {
        this.RecordTab()
      }
    }
    .width('90%')
    .backgroundColor('#1a1a1a')
    .borderRadius(16)
    .border({ width: 1, color: '#c41e3a' })
  }

  @Builder
  BasicInfoTab() {
    Scroll() {
      Column() {
        this.InfoRow('物料编码', this.item.sku, true)
        this.InfoRow('分类', this.item.category)
        this.InfoRow('规格型号', this.item.specification)
        this.InfoRow('品牌', this.item.brand)
        this.InfoRow('单位', this.item.unit)
        this.InfoRow('存放位置', this.item.location)
        this.InfoRow('保管员', this.item.custodian)
        this.InfoRow('所属部门', this.item.department)
        this.InfoRow('供应商', this.item.supplier)
        this.InfoRow('批次号', this.item.batchNo)
        this.InfoRow('采购日期', this.item.purchaseDate.toLocaleDateString())
        if (this.item.expiryDate) {
          this.InfoRow('保质期至', this.item.expiryDate.toLocaleDateString(),
            this.item.checkExpiry() ? '#ff0000' : '#888')
        }
        this.InfoRow('条码', this.item.barcode, false, '#666')
        this.InfoRow('DNA签名', this.item.dnaSignature.substring(0, 24) + '...', false, '#444')

        Divider().color('#333').margin({ top: 12, bottom: 12 })

        Text(`🐉 ${MASTER_DNA.substring(0, 30)}...`)
          .fontSize(10).fontColor('#444').width('100%').textAlign(TextAlign.Center)
        Text(`UID: ${MASTER_UID}`)
          .fontSize(10).fontColor('#444').margin({ top: 4 })
      }
      .width('100%')
      .padding(16)
    }
    .layoutWeight(1)
  }

  @Builder
  StockDetailTab() {
    Scroll() {
      Column() {
        // 库存状态指示器
        Row() {
          Text(this.item.status)
            .fontSize(14).fontWeight(FontWeight.Bold)
            .fontColor(
              this.item.status === ItemStatus.OUT_OF_STOCK ? '#ff0000' :
              this.item.status === ItemStatus.LOW_STOCK ? '#ffcc00' : '#00ff00'
            )
            .padding({ left: 12, right: 12, top: 4, bottom: 4 })
            .backgroundColor(
              this.item.status === ItemStatus.OUT_OF_STOCK ? 'rgba(255,0,0,0.15)' :
              this.item.status === ItemStatus.LOW_STOCK ? 'rgba(255,204,0,0.15)' :
              'rgba(0,255,0,0.15)'
            )
            .borderRadius(12)
        }
        .width('100%')
        .justifyContent(FlexAlign.Center)
        .padding({ top: 16, bottom: 8 })

        // 库存数量大数字
        Text(`${this.item.quantity}`)
          .fontSize(48).fontWeight(FontWeight.Bold)
          .fontColor(
            this.item.quantity <= 0 ? '#ff0000' :
            this.item.quantity <= this.item.minQuantity ? '#ffcc00' : '#00ff00'
          )
        Text(this.item.unit)
          .fontSize(16).fontColor('#888').margin({ top: 4 })

        // 库存刻度
        Row() {
          Column() {
            Text('安全线').fontSize(10).fontColor('#666')
            Text(`${this.item.minQuantity}`).fontSize(14).fontColor('#ffcc00')
          }.alignItems(HorizontalAlign.Center)

          Column() {
            Text('订购点').fontSize(10).fontColor('#666')
            Text(`${this.item.reorderPoint}`).fontSize(14).fontColor('#ff9900')
          }.alignItems(HorizontalAlign.Center)

          Column() {
            Text('最大库存').fontSize(10).fontColor('#666')
            Text(`${this.item.maxQuantity}`).fontSize(14).fontColor('#888')
          }.alignItems(HorizontalAlign.Center)
        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceAround)
        .padding({ top: 12, bottom: 12 })
        .backgroundColor('#222')
        .borderRadius(8)
        .margin({ top: 12, left: 16, right: 16 })

        Divider().color('#333').margin({ top: 16, bottom: 16 })

        this.InfoRow('采购单价', `¥${this.item.purchasePrice.toFixed(2)}`)
        this.InfoRow('库存总值', `¥${this.item.totalValue.toFixed(2)}`, false, '#c41e3a')
        if (this.item.lastUsedBy) {
          this.InfoRow('最后领用人', this.item.lastUsedBy)
          this.InfoRow('最后领用日期',
            this.item.lastUsedDate?.toLocaleDateString() || '未知')
        }
      }
      .width('100%')
      .padding({ bottom: 16 })
    }
    .layoutWeight(1)
  }

  @Builder
  RecordTab() {
    Scroll() {
      Column() {
        const records = inventoryState.getRecordsForItem(this.item.id);
        if (records.length === 0) {
          Column() {
            Text('📋').fontSize(40).margin({ bottom: 8 })
            Text('暂无流水记录').fontSize(14).fontColor('#666')
          }
          .width('100%').height(200)
          .justifyContent(FlexAlign.Center)
        } else {
          ForEach(records, (record: InventoryRecord) => {
            Column() {
              Row() {
                Text(record.type === '入库' ? '📥' : '📤')
                  .fontSize(20).margin({ right: 8 })
                Column() {
                  Text(`${record.type} ${record.quantity}${this.item.unit}`)
                    .fontSize(14).fontColor('#fff')
                  Text(`${record.reason} · ${record.operator}`)
                    .fontSize(12).fontColor('#888')
                }
                .alignItems(HorizontalAlign.Start)
                .layoutWeight(1)
                Text(new Date(record.timestamp).toLocaleString())
                  .fontSize(11).fontColor('#666')
              }
              .width('100%').padding(12)

              Divider().color('#2a2a2a')
            }
          })
        }
      }
      .width('100%')
      .padding(16)
    }
    .layoutWeight(1)
  }

  @Builder
  InfoRow(label: string, value: string, mono?: boolean, valueColor?: string) {
    Row() {
      Text(label).fontSize(13).fontColor('#888').width('30%')
      Text(value)
        .fontSize(13)
        .fontColor(valueColor || '#ccc')
        .fontFamily(mono ? 'monospace' : '')
        .layoutWeight(1)
        .textAlign(TextAlign.End)
    }
    .width('100%')
    .padding({ top: 8, bottom: 8 })
    .border({ width: { bottom: 0.5 }, color: '#2a2a2a' })
  }
}
