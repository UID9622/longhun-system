// 龍魂 · 印章详情弹窗 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { Seal, SealType, SealMaterial, SealStatus, sealState } from '../models/SealModel';

@CustomDialog
export struct SealDetailDialog {
  controller: CustomDialogController;
  seal?: Seal;

  @State private name: string = '';
  @State private sealNo: string = '';
  @State private selectedType: number = 0;
  @State private selectedMaterial: number = 0;
  @State private selectedStatus: number = 0;
  @State private diameter: number = 40;
  @State private shape: string = '圆形';
  @State private pattern: string = '';
  @State private font: string = '宋体';
  @State private custodian: string = '';
  @State private deputyCustodian: string = '';
  @State private department: string = '';
  @State private vaultLocation: string = '';
  @State private safeNo: string = '';
  @State private rfidTag: string = '';
  @State private fingerprintLock: boolean = false;
  @State private faceLock: boolean = false;
  @State private gpsTracker: boolean = false;

  private typeOptions: string[] = Object.values(SealType);
  private materialOptions: string[] = Object.values(SealMaterial);
  private statusOptions: string[] = Object.values(SealStatus);

  aboutToAppear() {
    if (this.seal) {
      this.name = this.seal.name;
      this.sealNo = this.seal.sealNo;
      this.selectedType = this.typeOptions.indexOf(this.seal.type);
      this.selectedMaterial = this.materialOptions.indexOf(this.seal.material);
      this.selectedStatus = this.statusOptions.indexOf(this.seal.status);
      this.diameter = this.seal.diameter;
      this.shape = this.seal.shape;
      this.pattern = this.seal.pattern;
      this.font = this.seal.font;
      this.custodian = this.seal.custodian;
      this.deputyCustodian = this.seal.deputyCustodian;
      this.department = this.seal.department;
      this.vaultLocation = this.seal.vaultLocation;
      this.safeNo = this.seal.safeNo;
      this.rfidTag = this.seal.rfidTag;
      this.fingerprintLock = this.seal.fingerprintLock;
      this.faceLock = this.seal.faceLock;
      this.gpsTracker = this.seal.gpsTracker;
    }
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text(this.seal ? '编辑印章' : '新增印章')
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

      // 内容滚动区
      Scroll() {
        Column() {
          // 基本信息
          this.SectionTitle('基本信息')

          this.InputField('印章名称', this.name, (v: string) => { this.name = v })
          this.InputField('印章编号', this.sealNo, (v: string) => { this.sealNo = v })

          this.SelectField('印章类型', this.typeOptions, this.selectedType, (i: number) => { this.selectedType = i })
          this.SelectField('印章材质', this.materialOptions, this.selectedMaterial, (i: number) => { this.selectedMaterial = i })
          this.SelectField('印章状态', this.statusOptions, this.selectedStatus, (i: number) => { this.selectedStatus = i })

          // 物理特征
          this.SectionTitle('物理特征')

          Row() {
            Text('直径(mm)')
              .fontSize(13)
              .fontColor('#888')
              .layoutWeight(1)
            Slider({
              value: this.diameter,
              min: 20,
              max: 80,
              step: 1,
              style: SliderStyle.InSet
            })
              .width('60%')
              .onChange((v: number) => { this.diameter = v })
            Text(`${this.diameter}mm`)
              .fontSize(12)
              .fontColor('#fff')
              .width(50)
              .textAlign(TextAlign.End)
          }
          .width('100%')
          .padding({ top: 8, bottom: 8 })

          this.InputField('形状', this.shape, (v: string) => { this.shape = v })
          this.InputField('图案描述', this.pattern, (v: string) => { this.pattern = v })
          this.InputField('字体', this.font, (v: string) => { this.font = v })

          // 管理信息
          this.SectionTitle('管理信息')

          this.InputField('保管人', this.custodian, (v: string) => { this.custodian = v })
          this.InputField('副保管人', this.deputyCustodian, (v: string) => { this.deputyCustodian = v })
          this.InputField('所属部门', this.department, (v: string) => { this.department = v })
          this.InputField('保险柜位置', this.vaultLocation, (v: string) => { this.vaultLocation = v })
          this.InputField('保险柜编号', this.safeNo, (v: string) => { this.safeNo = v })

          // 安全特征
          this.SectionTitle('安全特征')

          this.InputField('RFID标签', this.rfidTag, (v: string) => { this.rfidTag = v })

          this.ToggleField('指纹锁', this.fingerprintLock, (v: boolean) => { this.fingerprintLock = v })
          this.ToggleField('人脸锁', this.faceLock, (v: boolean) => { this.faceLock = v })
          this.ToggleField('GPS追踪器', this.gpsTracker, (v: boolean) => { this.gpsTracker = v })

          // 审计信息（只读）
          if (this.seal) {
            this.SectionTitle('审计信息')

            this.ReadOnlyField('DNA签名', this.seal.dnaSignature)
            this.ReadOnlyField('创建时间', this.seal.createdAt.toLocaleString())
            this.ReadOnlyField('最后更新', this.seal.updatedAt.toLocaleString())
            this.ReadOnlyField('累计使用', `${this.seal.useCount}次`)
          }
        }
        .width('100%')
        .padding({ left: 16, right: 16, bottom: 80 })
      }
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)

      // 底部保存按钮
      Row() {
        Button('保存')
          .fontSize(15)
          .fontColor('#fff')
          .backgroundColor('#c41e3a')
          .borderRadius(8)
          .width('100%')
          .height(44)
          .onClick(() => {
            this.save();
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
  InputField(label: string, value: string, onChange: (v: string) => void) {
    Row() {
      Text(label)
        .fontSize(13)
        .fontColor('#888')
        .width(100)
      TextInput({ text: value })
        .layoutWeight(1)
        .height(36)
        .backgroundColor('#2a2a2a')
        .fontColor('#fff')
        .placeholderColor('#555')
        .borderRadius(6)
        .padding({ left: 8, right: 8 })
        .onChange(onChange)
    }
    .width('100%')
    .padding({ top: 6, bottom: 6 })
  }

  @Builder
  SelectField(label: string, options: string[], selected: number, onSelect: (i: number) => void) {
    Row() {
      Text(label)
        .fontSize(13)
        .fontColor('#888')
        .width(100)
      Select(options.map((o, i) => ({ value: o, index: i })))
        .layoutWeight(1)
        .height(36)
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
    .padding({ top: 6, bottom: 6 })
  }

  @Builder
  ToggleField(label: string, value: boolean, onChange: (v: boolean) => void) {
    Row() {
      Text(label)
        .fontSize(13)
        .fontColor('#888')
        .layoutWeight(1)
      Toggle({ type: ToggleType.Switch, isOn: value })
        .onChange(onChange)
    }
    .width('100%')
    .padding({ top: 8, bottom: 8 })
  }

  @Builder
  ReadOnlyField(label: string, value: string) {
    Row() {
      Text(label)
        .fontSize(12)
        .fontColor('#666')
        .width(80)
      Text(value)
        .fontSize(12)
        .fontColor('#888')
        .fontFamily('monospace')
        .layoutWeight(1)
        .maxLines(1)
        .textOverflow({ overflow: TextOverflow.Ellipsis })
    }
    .width('100%')
    .padding({ top: 4, bottom: 4 })
  }

  private save() {
    if (!this.name.trim()) {
      return;
    }

    if (this.seal) {
      sealState.updateSeal(this.seal.id, {
        name: this.name,
        sealNo: this.sealNo,
        type: this.typeOptions[this.selectedType] as SealType,
        material: this.materialOptions[this.selectedMaterial] as SealMaterial,
        status: this.statusOptions[this.selectedStatus] as SealStatus,
        diameter: this.diameter,
        shape: this.shape as '圆形' | '方形' | '椭圆形' | '其他',
        pattern: this.pattern,
        font: this.font,
        custodian: this.custodian,
        deputyCustodian: this.deputyCustodian,
        department: this.department,
        vaultLocation: this.vaultLocation,
        safeNo: this.safeNo,
        rfidTag: this.rfidTag,
        fingerprintLock: this.fingerprintLock,
        faceLock: this.faceLock,
        gpsTracker: this.gpsTracker
      });
    } else {
      const newSeal = new Seal({
        name: this.name,
        type: this.typeOptions[this.selectedType] as SealType,
        material: this.materialOptions[this.selectedMaterial] as SealMaterial,
        status: this.statusOptions[this.selectedStatus] as SealStatus,
        diameter: this.diameter,
        shape: this.shape as '圆形' | '方形' | '椭圆形' | '其他',
        pattern: this.pattern,
        font: this.font,
        custodian: this.custodian,
        deputyCustodian: this.deputyCustodian,
        department: this.department,
        vaultLocation: this.vaultLocation,
        safeNo: this.safeNo,
        rfidTag: this.rfidTag,
        fingerprintLock: this.fingerprintLock,
        faceLock: this.faceLock,
        gpsTracker: this.gpsTracker
      });
      sealState.addSeal(newSeal);
    }

    this.controller.close();
  }
}
