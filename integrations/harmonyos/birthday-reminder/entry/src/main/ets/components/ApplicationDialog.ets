// 龍魂 · 用印申请弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Seal, SealType, SealApplication, UsageType, ApprovalLevel, sealState } from '../models/SealModel';

@CustomDialog
export struct ApplicationDialog {
  controller: CustomDialogController;
  preselectedSeal?: Seal;

  @State private selectedSealIndex: number = 0;
  @State private usageTypeIndex: number = 0;
  @State private urgencyIndex: number = 0;
  @State private approvalLevelIndex: number = 1;
  @State private documentName: string = '';
  @State private usageDesc: string = '';
  @State private documentCount: number = 1;
  @State private documentPages: number = 1;
  @State private remarks: string = '';

  private sealOptions: string[] = [];
  private usageTypeOptions: string[] = Object.values(UsageType);
  private urgencyOptions: string[] = ['普通', '紧急', '特急'];
  private approvalOptions: string[] = Object.values(ApprovalLevel);

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
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('用印申请')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
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
            Text('暂无可用的在库印章')
              .fontSize(13)
              .fontColor('#ff6600')
              .padding({ top: 8, bottom: 8 })
          }

          // 用印信息
          this.SectionTitle('用印信息')

          this.SelectField('用印类型', this.usageTypeOptions, this.usageTypeIndex, (i: number) => { this.usageTypeIndex = i })
          this.InputField('文件名称', this.documentName, (v: string) => { this.documentName = v })
          this.InputField('用印事由', this.usageDesc, (v: string) => { this.usageDesc = v }, true)

          Row() {
            Column() {
              Text('文件份数')
                .fontSize(12)
                .fontColor('#888')
              Counter({ value: this.documentCount })
                .onChange((v: number) => { this.documentCount = v })
            }
            .width('48%')

            Column() {
              Text('每份页数')
                .fontSize(12)
                .fontColor('#888')
              Counter({ value: this.documentPages })
                .onChange((v: number) => { this.documentPages = v })
            }
            .width('48%')
          }
          .width('100%')
          .padding({ top: 8, bottom: 8 })
          .justifyContent(FlexAlign.SpaceBetween)

          // 审批与紧急度
          this.SectionTitle('审批设置')

          this.SelectField('紧急程度', this.urgencyOptions, this.urgencyIndex, (i: number) => { this.urgencyIndex = i })
          this.SelectField('审批级别', this.approvalOptions, this.approvalLevelIndex, (i: number) => { this.approvalLevelIndex = i })

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

        Button('提交申请')
          .fontSize(15)
          .fontColor('#fff')
          .backgroundColor('#0066cc')
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
      .fontColor('#c41e3a')
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
        .type(multiline ? InputType.Normal : InputType.Normal)
        .onChange(onChange)
    }
    .width('100%')
    .padding({ top: 4, bottom: 4 })
  }

  @Builder
  SelectField(label: string, options: string[], selected: number, onSelect: (i: number) => void) {
    Column() {
      Text(label)
        .fontSize(12)
        .fontColor('#888')
        .width('100%')
        .padding({ bottom: 4 })
      Select(options.map((o, i) => ({ value: o, index: i })))
        .width('100%')
        .height(40)
        .backgroundColor('#2a2a2a')
        .fontColor('#fff')
        .borderRadius(6)
        .selected(selected)
        .value(options[selected])
        .onSelect((index: number) => {
          onSelect(index);
        })
    }
    .width('100%')
    .padding({ top: 4, bottom: 4 })
  }

  private submit() {
    if (!this.documentName.trim() || !this.usageDesc.trim()) {
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

    const app = new SealApplication({
      sealId: seal.id,
      sealName: seal.name,
      sealType: seal.type,
      applicant: sealState.currentUser || '当前用户',
      department: sealState.currentDept || seal.department,
      usageType: this.usageTypeOptions[this.usageTypeIndex] as UsageType,
      usageDesc: this.usageDesc,
      documentName: this.documentName,
      documentCount: this.documentCount,
      documentPages: this.documentPages,
      urgency: this.urgencyOptions[this.urgencyIndex] as '普通' | '紧急' | '特急',
      approvalLevel: this.approvalOptions[this.approvalLevelIndex] as ApprovalLevel,
      remarks: this.remarks
    });

    app.submit();
    sealState.submitApplication(app);
    this.controller.close();
  }
}
