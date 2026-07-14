// 龍魂 · 外带登记弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Seal, SealStatus, SealOutRecord, sealState } from '../models/SealModel';

@CustomDialog
export struct OutRecordDialog {
  controller: CustomDialogController;
  preselectedSeal?: Seal;

  @State private selectedSealIndex: number = 0;
  @State private borrower: string = '';
  @State private borrowerDept: string = '';
  @State private purpose: string = '';
  @State private destination: string = '';
  @State private escort: string = '';
  @State private borrowDate: string = '';
  @State private expectedReturn: string = '';
  @State private remarks: string = '';

  private sealOptions: string[] = [];

  aboutToAppear() {
    this.sealOptions = sealState.seals
      .filter(s => s.status === SealStatus.IN_VAULT)
      .map(s => `${s.name} (${s.sealNo})`);

    if (this.preselectedSeal) {
      const idx = sealState.seals.findIndex(s => s.id === this.preselectedSeal!.id);
      if (idx >= 0) {
        this.selectedSealIndex = idx;
      }
    }

    this.borrower = sealState.currentUser || '';
    this.borrowerDept = sealState.currentDept || '';

    const now = new Date();
    this.borrowDate = now.toLocaleString();

    const tomorrow = new Date(now.getTime() + 24 * 60 * 60 * 1000);
    this.expectedReturn = tomorrow.toLocaleDateString();
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('印章外带登记')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#ff6600')
        Blank()
        Button() {
          Text('✕')
            .fontSize(20)
            .fontColor('#888')
        }
        .type(ButtonType.Circle)
        .backgroundColor('transparent')
        .onClick(() => this.controller.close())
      }
      .width('100%')
      .padding(16)
      .border({ width: { bottom: 1 }, color: '#333' })

      // 安全提醒横幅
      Row() {
        Text('⚠️')
          .fontSize(20)
          .margin({ right: 8 })
        Column() {
          Text('印章外带安全提醒')
            .fontSize(13)
            .fontWeight(FontWeight.Bold)
            .fontColor('#ffcc00')
          Text('外带期间将启动GPS追踪和定时回传')
            .fontSize(11)
            .fontColor('#ffcc00')
        }
        .alignItems(HorizontalAlign.Start)
        .layoutWeight(1)
      }
      .width('100%')
      .padding(12)
      .backgroundColor('rgba(255,204,0,0.1)')
      .border({ width: { bottom: 1 }, color: 'rgba(255,204,0,0.3)' })

      Scroll() {
        Column() {
          // 选择印章
          this.SectionTitle('选择印章')

          if (this.sealOptions.length > 0) {
            Select(this.sealOptions.map((o, i) => ({ value: o, index: i })))
              .width('100%')
              .height(40)
              .backgroundColor('#2a2a2a')
              .fontColor('#fff')
              .borderRadius(6)
              .selected(this.selectedSealIndex)
              .value(this.sealOptions[this.selectedSealIndex])
              .onSelect((index: number) => { this.selectedSealIndex = index })
              .padding({ top: 4, bottom: 4 })
          } else {
            Text('暂无可外带的在库印章')
              .fontSize(13)
              .fontColor('#ff6600')
              .padding({ top: 8, bottom: 8 })
          }

          // 借出信息
          this.SectionTitle('借出信息')

          this.InputField('借出人', this.borrower, (v: string) => { this.borrower = v })
          this.InputField('借出部门', this.borrowerDept, (v: string) => { this.borrowerDept = v })
          this.InputField('外带目的', this.purpose, (v: string) => { this.purpose = v }, true)
          this.InputField('目的地', this.destination, (v: string) => { this.destination = v })
          this.InputField('陪同人', this.escort, (v: string) => { this.escort = v })

          // 时间信息
          this.SectionTitle('时间信息')

          this.ReadOnlyField('借出时间', this.borrowDate)
          this.InputField('预计归还', this.expectedReturn, (v: string) => { this.expectedReturn = v })

          // 安全设置
          this.SectionTitle('安全设置')

          this.CheckItem('✅ GPS实时追踪已启用')
          this.CheckItem('✅ 定时回传已启用（每小时）')
          this.CheckItem('✅ 电子围栏已启用')
          this.CheckItem('⚠️ 外带期间双人同行')

          this.InputField('备注', this.remarks, (v: string) => { this.remarks = v }, true)
        }
        .width('100%')
        .padding({ left: 16, right: 16, bottom: 80 })
      }
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)

      // 底部按钮
      Row() {
        Button('取消')
          .fontSize(15)
          .fontColor('#888')
          .backgroundColor('#2a2a2a')
          .borderRadius(8)
          .layoutWeight(1)
          .height(44)
          .onClick(() => this.controller.close())

        Button('确认外带')
          .fontSize(15)
          .fontColor('#fff')
          .backgroundColor('#ff6600')
          .borderRadius(8)
          .layoutWeight(2)
          .height(44)
          .margin({ left: 12 })
          .onClick(() => {
            this.submit();
          })
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 12, bottom: 12 })
      .backgroundColor('#1a1a1a')
      .border({ width: { top: 1 }, color: '#333' })
    }
    .width('100%')
    .height('90%')
    .backgroundColor('#0a0a0a')
    .borderRadius({ topLeft: 16, topRight: 16 })
  }

  @Builder
  SectionTitle(title: string) {
    Text(title)
      .fontSize(14)
      .fontWeight(FontWeight.Bold)
      .fontColor('#ff6600')
      .width('100%')
      .padding({ top: 16, bottom: 8 })
  }

  @Builder
  InputField(label: string, value: string, onChange: (v: string) => void, multiline: boolean = false) {
    Column() {
      Text(label)
        .fontSize(12)
        .fontColor('#888')
        .width('100%')
        .padding({ bottom: 4 })
      TextInput({ text: value })
        .width('100%')
        .height(multiline ? 80 : 40)
        .backgroundColor('#2a2a2a')
        .fontColor('#fff')
        .placeholderColor('#555')
        .borderRadius(6)
        .padding({ left: 8, right: 8 })
        .onChange(onChange)
    }
    .width('100%')
    .padding({ top: 4, bottom: 4 })
  }

  @Builder
  ReadOnlyField(label: string, value: string) {
    Row() {
      Text(label)
        .fontSize(12)
        .fontColor('#666')
        .width(80)
      Text(value)
        .fontSize(13)
        .fontColor('#888')
        .layoutWeight(1)
    }
    .width('100%')
    .padding({ top: 4, bottom: 4 })
  }

  @Builder
  CheckItem(text: string) {
    Row() {
      Text(text)
        .fontSize(12)
        .fontColor('#00aa00')
    }
    .width('100%')
    .padding({ top: 4, bottom: 4 })
  }

  private submit() {
    if (!this.borrower.trim() || !this.purpose.trim() || !this.destination.trim()) {
      return;
    }

    const inVaultSeals = sealState.seals.filter(s => s.status === SealStatus.IN_VAULT);
    if (inVaultSeals.length === 0) {
      return;
    }

    const seal = inVaultSeals[this.selectedSealIndex];
    if (!seal) {
      return;
    }

    const expectedDate = new Date(this.expectedReturn);
    if (isNaN(expectedDate.getTime())) {
      return;
    }

    const record = new SealOutRecord({
      sealId: seal.id,
      sealName: seal.name,
      borrower: this.borrower,
      borrowerDept: this.borrowerDept,
      purpose: this.purpose,
      destination: this.destination,
      escort: this.escort,
      expectedReturn: expectedDate,
      status: 'out'
    });

    sealState.registerOut(record);
    this.controller.close();
  }
}
