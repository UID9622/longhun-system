// entry/src/main/ets/components/StockOperationDialog.ets
// 龍魂 · 出入库操作弹窗

import { SupplyItem, inventoryState } from '../models/InventoryModel';

@CustomDialog
export struct StockOperationDialog {
  controller: CustomDialogController;
  item?: SupplyItem;
  @State private operationType: '入库' | '出库' = '入库';
  @State private selectedItem: SupplyItem | undefined = undefined;
  @State private quantity: string = '';
  @State private operator: string = '';
  @State private reason: string = '';
  @State private errorMsg: string = '';
  @State private successMsg: string = '';

  aboutToAppear() {
    if (this.item) {
      this.selectedItem = this.item;
    }
  }

  build() {
    Column() {
      // 标题
      Row() {
        Text(this.item ? `${this.operationType}操作` : '出入库登记')
          .fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').layoutWeight(1)
        Button() { Text('✕').fontSize(16).fontColor('#888') }
          .type(ButtonType.Circle).backgroundColor('transparent')
          .width(32).height(32)
          .onClick(() => this.controller.close())
      }
      .width('100%').padding(16)

      // 出入库切换
      if (!this.item) {
        Row() {
          Button('📥 入库')
            .fontSize(14)
            .fontColor(this.operationType === '入库' ? '#fff' : '#888')
            .backgroundColor(this.operationType === '入库' ? '#00aa00' : '#2a2a2a')
            .borderRadius(8)
            .padding({ left: 24, right: 24 })
            .onClick(() => { this.operationType = '入库'; })
          Button('📤 出库')
            .fontSize(14)
            .fontColor(this.operationType === '出库' ? '#fff' : '#888')
            .backgroundColor(this.operationType === '出库' ? '#c41e3a' : '#2a2a2a')
            .borderRadius(8)
            .padding({ left: 24, right: 24 })
            .margin({ left: 12 })
            .onClick(() => { this.operationType = '出库'; })
        }
        .width('100%').padding({ left: 16, right: 16, bottom: 12 })
        .justifyContent(FlexAlign.Center)
      }

      Scroll() {
        Column() {
          // 物资选择（未指定时）
          if (!this.item) {
            Text('选择物资').fontSize(13).fontColor('#888').width('100%').margin({ bottom: 8 })
            Select(inventoryState.items.map(i => ({ value: `${i.name} [${i.sku}]` })))
              .fontColor('#fff')
              .backgroundColor('#2a2a2a')
              .borderRadius(8)
              .width('100%')
              .height(40)
              .padding({ left: 12 })
              .onSelect((index: number) => {
                this.selectedItem = inventoryState.items[index];
                this.errorMsg = '';
              })
          }

          if (this.selectedItem) {
            // 当前库存显示
            Row() {
              Text('当前库存:').fontSize(13).fontColor('#888')
              Text(`${this.selectedItem.quantity} ${this.selectedItem.unit}`)
                .fontSize(16).fontWeight(FontWeight.Bold)
                .fontColor(
                  this.selectedItem.quantity <= 0 ? '#ff0000' :
                  this.selectedItem.quantity <= this.selectedItem.minQuantity ? '#ffcc00' : '#00ff00'
                )
                .margin({ left: 8 })
              Blank()
              Text(this.selectedItem.location).fontSize(12).fontColor('#666')
            }
            .width('100%')
            .padding(12)
            .backgroundColor('#222')
            .borderRadius(8)
            .margin({ bottom: 16 })

            // 数量输入
            Text('数量').fontSize(13).fontColor('#888').width('100%').margin({ bottom: 8 })
            TextInput({ text: $$this.quantity, placeholder: `请输入${this.operationType}数量` })
              .type(InputType.Number)
              .fontColor('#fff')
              .placeholderColor('#666')
              .backgroundColor('#2a2a2a')
              .borderRadius(8)
              .width('100%')
              .height(40)
              .padding({ left: 12 })
              .onChange(() => { this.errorMsg = ''; })

            // 快速数量按钮
            Row() {
              ForEach([1, 5, 10, 20, 50, 100], (num: number) => {
                Button(`${num}`)
                  .fontSize(11).fontColor('#888')
                  .backgroundColor('#2a2a2a')
                  .borderRadius(4)
                  .padding({ left: 8, right: 8 })
                  .onClick(() => {
                    this.quantity = num.toString();
                  })
              })
            }
            .width('100%')
            .justifyContent(FlexAlign.SpaceBetween)
            .margin({ top: 8, bottom: 16 })

            // 操作人
            Text('操作人').fontSize(13).fontColor('#888').width('100%').margin({ bottom: 8 })
            TextInput({ text: $$this.operator, placeholder: '请输入操作人姓名' })
              .fontColor('#fff')
              .placeholderColor('#666')
              .backgroundColor('#2a2a2a')
              .borderRadius(8)
              .width('100%')
              .height(40)
              .padding({ left: 12 })
              .onChange(() => { this.errorMsg = ''; })

            // 原因
            Text('原因').fontSize(13).fontColor('#888').width('100%').margin({ top: 16, bottom: 8 })
            TextInput({ text: $$this.reason, placeholder: '请输入出入库原因' })
              .fontColor('#fff')
              .placeholderColor('#666')
              .backgroundColor('#2a2a2a')
              .borderRadius(8)
              .width('100%')
              .height(40)
              .padding({ left: 12 })
          }

          // 错误信息
          if (this.errorMsg) {
            Text(this.errorMsg)
              .fontSize(12).fontColor('#ff0000')
              .width('100%')
              .margin({ top: 12 })
          }

          // 成功信息
          if (this.successMsg) {
            Text(this.successMsg)
              .fontSize(13).fontColor('#00ff00')
              .width('100%')
              .textAlign(TextAlign.Center)
              .margin({ top: 12 })
              .padding(12)
              .backgroundColor('rgba(0,255,0,0.1)')
              .borderRadius(8)
          }
        }
        .width('100%')
        .padding({ left: 16, right: 16 })
      }
      .layoutWeight(1)

      // 底部按钮
      Row() {
        Button('取消')
          .fontSize(14).fontColor('#888')
          .backgroundColor('#2a2a2a').borderRadius(8)
          .padding({ left: 24, right: 24 })
          .onClick(() => this.controller.close())

        Button('确认提交')
          .fontSize(14).fontColor('#fff')
          .backgroundColor(this.operationType === '入库' ? '#00aa00' : '#c41e3a')
          .borderRadius(8)
          .padding({ left: 24, right: 24 })
          .onClick(() => this.submitOperation())
      }
      .width('100%')
      .padding(16)
      .justifyContent(FlexAlign.SpaceAround)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('90%')
    .backgroundColor('#1a1a1a')
    .borderRadius(16)
    .border({ width: 1, color: '#c41e3a' })
  }

  private submitOperation() {
    // 校验
    if (!this.selectedItem) {
      this.errorMsg = '请选择物资';
      return;
    }

    const qty = parseInt(this.quantity);
    if (isNaN(qty) || qty <= 0) {
      this.errorMsg = '请输入有效数量';
      return;
    }

    if (this.operationType === '出库' && qty > this.selectedItem.quantity) {
      this.errorMsg = `库存不足！当前仅 ${this.selectedItem.quantity}${this.selectedItem.unit}`;
      return;
    }

    if (!this.operator.trim()) {
      this.errorMsg = '请输入操作人';
      return;
    }

    if (!this.reason.trim()) {
      this.errorMsg = '请输入原因';
      return;
    }

    try {
      if (this.operationType === '入库') {
        inventoryState.stockIn(this.selectedItem.id, qty, this.operator.trim(), this.reason.trim());
      } else {
        inventoryState.stockOut(this.selectedItem.id, qty, this.operator.trim(), this.reason.trim());
      }

      this.successMsg = `${this.operationType}成功！${qty}${this.selectedItem.unit}`;
      this.errorMsg = '';

      // 1.5秒后关闭
      setTimeout(() => {
        this.controller.close();
      }, 1500);
    } catch (e) {
      this.errorMsg = `操作失败: ${e}`;
    }
  }
}
