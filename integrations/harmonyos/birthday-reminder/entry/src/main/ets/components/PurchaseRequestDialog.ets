// entry/src/main/ets/components/PurchaseRequestDialog.ets
// 龍魂 · 采购申请弹窗

import { PurchaseRequest, PurchaseItem, ApprovalStatus, inventoryState } from '../models/InventoryModel';

@CustomDialog
export struct PurchaseRequestDialog {
  controller: CustomDialogController;
  @State private requester: string = '';
  @State private department: string = '';
  @State private requiredDays: string = '7';
  @State private items: PurchaseItemDraft[] = [];
  @State private errorMsg: string = '';
  @State private successMsg: string = '';
  @State private currentStep: number = 0; // 0=添加物项 1=确认提交

  aboutToAppear() {
    // 初始化一个空行
    this.addItem();
  }

  build() {
    Column() {
      // 标题
      Row() {
        Text('📝 采购申请').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').layoutWeight(1)
        Button() { Text('✕').fontSize(16).fontColor('#888') }
          .type(ButtonType.Circle).backgroundColor('transparent')
          .width(32).height(32)
          .onClick(() => this.controller.close())
      }
      .width('100%').padding(16)

      // 步骤指示器
      Row() {
        ForEach(['填写物项', '确认提交'], (label: string, index: number) => {
          Row() {
            Text(`${index + 1}`)
              .fontSize(12).fontColor(this.currentStep >= index ? '#fff' : '#888')
              .backgroundColor(this.currentStep >= index ? '#c41e3a' : '#333')
              .borderRadius(12).width(24).height(24)
              .textAlign(TextAlign.Center)
            Text(label)
              .fontSize(12)
              .fontColor(this.currentStep >= index ? '#fff' : '#666')
              .margin({ left: 8 })
          }
          if (index === 0) {
            Divider().width(24).color('#444').margin({ left: 4, right: 4 })
          }
        })
      }
      .width('100%').padding({ left: 16, right: 16, bottom: 12 })
      .justifyContent(FlexAlign.Center)

      Scroll() {
        Column() {
          if (this.currentStep === 0) {
            // 步骤1：添加采购物项
            Column() {
              Text('采购物项清单')
                .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#ccc')
                .width('100%').margin({ bottom: 12 })

              ForEach(this.items, (draft: PurchaseItemDraft, index: number) => {
                Column() {
                  Row() {
                    Text(`#${index + 1}`).fontSize(12).fontColor('#c41e3a')
                      .margin({ right: 8 })
                    Text(draft.name || '新物项').fontSize(13).fontColor('#ccc')
                      .layoutWeight(1).maxLines(1)
                      .textOverflow({ overflow: TextOverflow.Ellipsis })

                    if (draft.name) {
                      Text(`¥${draft.estimatedPrice * draft.quantity}`)
                        .fontSize(12).fontColor('#00ff00')
                    }

                    Button() { Text('✕').fontSize(10).fontColor('#ff0000') }
                      .type(ButtonType.Circle).backgroundColor('transparent')
                      .width(24).height(24)
                      .onClick(() => {
                        this.items.splice(index, 1);
                      })
                  }
                  .width('100%')

                  // 物项输入
                  Row() {
                    TextInput({ text: $$draft.name, placeholder: '物项名称' })
                      .fontColor('#fff').placeholderColor('#666')
                      .backgroundColor('#2a2a2a').borderRadius(4)
                      .height(36).layoutWeight(2).padding({ left: 8 })
                      .margin({ right: 4 })

                    TextInput({ text: $$draft.specification, placeholder: '规格' })
                      .fontColor('#fff').placeholderColor('#666')
                      .backgroundColor('#2a2a2a').borderRadius(4)
                      .height(36).layoutWeight(1).padding({ left: 8 })
                      .margin({ right: 4 })
                  }
                  .width('100%').margin({ top: 4 })

                  Row() {
                    TextInput({ text: $$draft.quantityStr, placeholder: '数量' })
                      .type(InputType.Number).fontColor('#fff').placeholderColor('#666')
                      .backgroundColor('#2a2a2a').borderRadius(4)
                      .height(36).layoutWeight(1).padding({ left: 8 })
                      .margin({ right: 4 })
                      .onChange(() => {
                        const v = parseInt(draft.quantityStr);
                        if (!isNaN(v)) draft.quantity = v;
                      })

                    TextInput({ text: $$draft.unit, placeholder: '单位' })
                      .fontColor('#fff').placeholderColor('#666')
                      .backgroundColor('#2a2a2a').borderRadius(4)
                      .height(36).layoutWeight(1).padding({ left: 8 })
                      .margin({ right: 4 })

                    TextInput({ text: $$draft.priceStr, placeholder: '预估单价' })
                      .type(InputType.Number).fontColor('#fff').placeholderColor('#666')
                      .backgroundColor('#2a2a2a').borderRadius(4)
                      .height(36).layoutWeight(1).padding({ left: 8 })
                      .onChange(() => {
                        const v = parseFloat(draft.priceStr);
                        if (!isNaN(v)) draft.estimatedPrice = v;
                      })
                  }
                  .width('100%').margin({ top: 4 })

                  TextInput({ text: $$draft.supplier, placeholder: '供应商（选填）' })
                    .fontColor('#fff').placeholderColor('#666')
                    .backgroundColor('#2a2a2a').borderRadius(4)
                    .height(36).width('100%').padding({ left: 8 })
                    .margin({ top: 4 })
                }
                .width('100%')
                .padding(12)
                .backgroundColor('#222')
                .borderRadius(8)
                .margin({ bottom: 8 })
              })

              // 添加物项按钮
              Button() { Text('+ 添加物项').fontSize(13).fontColor('#00aaff') }
                .backgroundColor('rgba(0,170,255,0.1)').borderRadius(8)
                .width('100%').height(36)
                .onClick(() => this.addItem())
            }
            .width('100%')
            .padding({ left: 16, right: 16 })
          } else {
            // 步骤2：确认提交
            Column() {
              Text('申请人信息').fontSize(14).fontWeight(FontWeight.Bold)
                .fontColor('#ccc').width('100%').margin({ bottom: 12 })

              TextInput({ text: $$this.requester, placeholder: '申请人姓名' })
                .fontColor('#fff').placeholderColor('#666')
                .backgroundColor('#2a2a2a').borderRadius(8)
                .width('100%').height(40).padding({ left: 12 })
                .margin({ bottom: 12 })

              TextInput({ text: $$this.department, placeholder: '申请部门' })
                .fontColor('#fff').placeholderColor('#666')
                .backgroundColor('#2a2a2a').borderRadius(8)
                .width('100%').height(40).padding({ left: 12 })
                .margin({ bottom: 12 })

              TextInput({ text: $$this.requiredDays, placeholder: '需求天数' })
                .type(InputType.Number).fontColor('#fff').placeholderColor('#666')
                .backgroundColor('#2a2a2a').borderRadius(8)
                .width('100%').height(40).padding({ left: 12 })
                .margin({ bottom: 16 })

              // 摘要
              Text('采购摘要').fontSize(14).fontWeight(FontWeight.Bold)
                .fontColor('#ccc').width('100%').margin({ bottom: 8 })

              Column() {
                const validItems = this.items.filter(i => i.name && i.quantity > 0);
                const totalAmount = validItems.reduce((sum, i) => sum + i.estimatedPrice * i.quantity, 0);

                ForEach(validItems, (item: PurchaseItemDraft) => {
                  Row() {
                    Text(item.name).fontSize(13).fontColor('#ccc').layoutWeight(1)
                    Text(`${item.quantity}${item.unit}`).fontSize(13).fontColor('#888')
                    Text(`¥${(item.estimatedPrice * item.quantity).toFixed(2)}`)
                      .fontSize(13).fontColor('#00ff00').margin({ left: 8 })
                  }
                  .width('100%').padding({ top: 4, bottom: 4 })
                })

                Divider().color('#333').margin({ top: 8, bottom: 8 })

                Row() {
                  Text('合计').fontSize(14).fontWeight(FontWeight.Bold).fontColor('#fff').layoutWeight(1)
                  Text(`¥${totalAmount.toFixed(2)}`)
                    .fontSize(16).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
                }
                .width('100%')
              }
              .width('100%')
              .padding(12)
              .backgroundColor('#222')
              .borderRadius(8)
            }
            .width('100%')
            .padding({ left: 16, right: 16 })
          }

          // 错误/成功信息
          if (this.errorMsg) {
            Text(this.errorMsg).fontSize(12).fontColor('#ff0000')
              .width('100%').padding({ left: 16, right: 16 }).margin({ top: 12 })
          }
          if (this.successMsg) {
            Text(this.successMsg).fontSize(13).fontColor('#00ff00')
              .width('100%').textAlign(TextAlign.Center)
              .padding(12).margin({ top: 12, left: 16, right: 16 })
              .backgroundColor('rgba(0,255,0,0.1)').borderRadius(8)
          }
        }
        .width('100%').padding({ bottom: 16 })
      }
      .layoutWeight(1)

      // 底部按钮
      Row() {
        if (this.currentStep > 0) {
          Button('上一步').fontSize(14).fontColor('#888')
            .backgroundColor('#2a2a2a').borderRadius(8)
            .padding({ left: 20, right: 20 })
            .onClick(() => { this.currentStep = 0; this.errorMsg = ''; })
        }

        Button('取消').fontSize(14).fontColor('#888')
          .backgroundColor('#2a2a2a').borderRadius(8)
          .padding({ left: 20, right: 20 })
          .onClick(() => this.controller.close())

        Button(this.currentStep === 0 ? '下一步' : '提交申请')
          .fontSize(14).fontColor('#fff')
          .backgroundColor('#0066cc').borderRadius(8)
          .padding({ left: 20, right: 20 })
          .onClick(() => {
            if (this.currentStep === 0) {
              this.goNext();
            } else {
              this.submitRequest();
            }
          })
      }
      .width('100%').padding(16)
      .justifyContent(FlexAlign.SpaceAround)
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('90%')
    .backgroundColor('#1a1a1a')
    .borderRadius(16)
    .border({ width: 1, color: '#0066cc' })
  }

  private addItem() {
    this.items.push({
      name: '',
      specification: '',
      quantity: 1,
      quantityStr: '1',
      unit: '个',
      estimatedPrice: 0,
      priceStr: '',
      supplier: '',
      remark: ''
    });
  }

  private goNext() {
    const validItems = this.items.filter(i => i.name && i.quantity > 0);
    if (validItems.length === 0) {
      this.errorMsg = '请至少填写一个有效物项';
      return;
    }
    this.errorMsg = '';
    this.currentStep = 1;
  }

  private submitRequest() {
    if (!this.requester.trim()) {
      this.errorMsg = '请输入申请人姓名';
      return;
    }
    if (!this.department.trim()) {
      this.errorMsg = '请输入申请部门';
      return;
    }

    const validItems = this.items.filter(i => i.name && i.quantity > 0);
    if (validItems.length === 0) {
      this.errorMsg = '没有有效物项';
      return;
    }

    const purchaseItems = validItems.map(i => new PurchaseItem({
      itemName: i.name,
      specification: i.specification,
      quantity: i.quantity,
      unit: i.unit,
      estimatedPrice: i.estimatedPrice,
      supplier: i.supplier,
      remark: i.remark
    }));

    const days = parseInt(this.requiredDays) || 7;

    const request = new PurchaseRequest({
      items: purchaseItems,
      requester: this.requester.trim(),
      department: this.department.trim(),
      requiredDate: new Date(Date.now() + days * 24 * 60 * 60 * 1000)
    });
    request.submit();

    inventoryState.addPurchaseRequest(request);

    this.successMsg = `采购申请已提交！单号: ${request.requestNo}`;
    this.errorMsg = '';

    setTimeout(() => {
      this.controller.close();
    }, 1500);
  }
}

// 草稿物项
interface PurchaseItemDraft {
  name: string;
  specification: string;
  quantity: number;
  quantityStr: string;
  unit: string;
  estimatedPrice: number;
  priceStr: string;
  supplier: string;
  remark: string;
}
