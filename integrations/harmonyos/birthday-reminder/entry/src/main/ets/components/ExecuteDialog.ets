// 龍魂 · 执行弹窗 · 用印现场记录 · ArkTS
// DNA: ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️

import { SealApplication, sealState } from '../models/SealModel';

@CustomDialog
export struct ExecuteDialog {
  controller: CustomDialogController;
  application?: SealApplication;

  @State private executor: string = '';
  @State private witness: string = '';
  @State private actualCount: number = 1;
  @State private gpsLat: string = '';
  @State private gpsLng: string = '';
  @State private photos: string[] = [];
  @State private fingerprintVerify: boolean = false;
  @State private faceVerify: boolean = false;
  @State private remarks: string = '';
  @State private step: number = 1; // 1=信息填写 2=拍照验证

  aboutToAppear() {
    this.executor = sealState.currentUser || '';
    if (this.application) {
      this.actualCount = this.application.documentCount;
    }
  }

  build() {
    Column() {
      // 标题栏
      Row() {
        Text('执行用印登记')
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
        Blank()
        if (this.step > 1) {
          Button('上一步')
            .fontSize(12)
            .fontColor('#888')
            .backgroundColor('#2a2a2a')
            .borderRadius(4)
            .padding({ left: 8, right: 8 })
            .onClick(() => { this.step-- })
            .margin({ right: 8 })
        }
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

      // 步骤指示器
      Row() {
        ForEach([1, 2], (s: number) => {
          Row() {
            if (s > 1) {
              Divider()
                .strokeWidth(2)
                .color(this.step >= s ? '#c41e3a' : '#333')
                .width(60)
            }
            Column() {
              Text(`${s}`)
                .fontSize(14)
                .fontWeight(FontWeight.Bold)
                .fontColor(this.step >= s ? '#fff' : '#666')
            }
            .width(28)
            .height(28)
            .backgroundColor(this.step >= s ? '#c41e3a' : '#333')
            .borderRadius(14)
            .justifyContent(FlexAlign.Center)
          }
        })

        Text(this.step === 1 ? '信息填写' : '拍照验证')
          .fontSize(12)
          .fontColor('#c41e3a')
          .margin({ left: 8 })
      }
      .width('100%')
      .padding({ top: 12, bottom: 12 })
      .justifyContent(FlexAlign.Center)

      Scroll() {
        Column() {
          if (this.step === 1) {
            this.Step1Content()
          } else {
            this.Step2Content()
          }
        }
        .width('100%')
        .padding({ left: 16, right: 16, bottom: 80 })
      }
      .width('100%')
      .layoutWeight(1)
      .scrollBar(BarState.Auto)

      // 底部按钮
      Row() {
        if (this.step === 1) {
          Button('下一步')
            .fontSize(15)
            .fontColor('#fff')
            .backgroundColor('#0066cc')
            .borderRadius(8)
            .width('100%')
            .height(44)
            .onClick(() => {
              if (this.executor.trim() && this.witness.trim()) {
                this.step = 2;
              }
            })
        } else {
          Button('取消')
            .fontSize(15)
            .fontColor('#888')
            .backgroundColor('#2a2a2a')
            .borderRadius(8)
            .layoutWeight(1)
            .height(44)
            .onClick(() => this.controller.close())

          Button('确认执行')
            .fontSize(15)
            .fontColor('#fff')
            .backgroundColor('#00aa00')
            .borderRadius(8)
            .layoutWeight(2)
            .height(44)
            .margin({ left: 12 })
            .onClick(() => {
              this.execute();
            })
        }
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
  Step1Content() {
    Column() {
      this.SectionTitle('执行人信息')

      this.InputField('执行人（用印人）', this.executor, (v: string) => { this.executor = v })
      this.InputField('监印人', this.witness, (v: string) => { this.witness = v })

      Row() {
        Column() {
          Text('实际用印份数')
            .fontSize(12)
            .fontColor('#888')
          Counter({ value: this.actualCount })
            .onChange((v: number) => { this.actualCount = v })
        }
        .width('48%')

        Column() {
          // 空白占位
        }
        .width('48%')
      }
      .width('100%')
      .padding({ top: 8, bottom: 8 })
      .justifyContent(FlexAlign.SpaceBetween)

      this.SectionTitle('GPS定位')

      this.InputField('纬度', this.gpsLat, (v: string) => { this.gpsLat = v })
      this.InputField('经度', this.gpsLng, (v: string) => { this.gpsLng = v })

      Row() {
        Button('📍 获取当前位置')
          .fontSize(12)
          .fontColor('#fff')
          .backgroundColor('#0066cc')
          .borderRadius(6)
          .padding({ left: 12, right: 12 })
          .onClick(() => {
            this.getCurrentLocation();
          })
      }
      .width('100%')
      .padding({ top: 8 })

      this.InputField('备注', this.remarks, (v: string) => { this.remarks = v }, true)
    }
    .width('100%')
  }

  @Builder
  Step2Content() {
    Column() {
      this.SectionTitle('生物验证')

      Row() {
        Column() {
          Text('指纹验证')
            .fontSize(13)
            .fontColor('#888')
          Toggle({ type: ToggleType.Switch, isOn: this.fingerprintVerify })
            .onChange((v: boolean) => { this.fingerprintVerify = v })
        }
        .width('48%')
        .padding(12)
        .backgroundColor(this.fingerprintVerify ? 'rgba(0,255,0,0.05)' : '#1a1a1a')
        .borderRadius(8)
        .border({ width: 1, color: this.fingerprintVerify ? '#00ff00' : '#333' })

        Column() {
          Text('人脸验证')
            .fontSize(13)
            .fontColor('#888')
          Toggle({ type: ToggleType.Switch, isOn: this.faceVerify })
            .onChange((v: boolean) => { this.faceVerify = v })
        }
        .width('48%')
        .padding(12)
        .backgroundColor(this.faceVerify ? 'rgba(0,255,0,0.05)' : '#1a1a1a')
        .borderRadius(8)
        .border({ width: 1, color: this.faceVerify ? '#00ff00' : '#333' })
      }
      .width('100%')
      .justifyContent(FlexAlign.SpaceBetween)
      .padding({ top: 8, bottom: 8 })

      this.SectionTitle('现场拍照')

      Row() {
        Button('📷 拍照')
          .fontSize(14)
          .fontColor('#fff')
          .backgroundColor('#0066cc')
          .borderRadius(8)
          .padding({ left: 16, right: 16, top: 8, bottom: 8 })
          .onClick(() => {
            this.takePhoto();
          })
      }
      .width('100%')
      .padding({ top: 8, bottom: 8 })

      // 已拍照片缩略图
      if (this.photos.length > 0) {
        Row() {
          ForEach(this.photos, (photo: string) => {
            Stack() {
              Image(photo)
                .width(80)
                .height(80)
                .borderRadius(6)
                .objectFit(ImageFit.Cover)

              Button() {
                Text('✕')
                  .fontSize(10)
                  .fontColor('#fff')
              }
              .type(ButtonType.Circle)
              .backgroundColor('rgba(255,0,0,0.8)')
              .width(20)
              .height(20)
              .position({ x: 60, y: -6 })
              .onClick(() => {
                const idx = this.photos.indexOf(photo);
                if (idx >= 0) {
                  this.photos.splice(idx, 1);
                }
              })
            }
            .margin({ right: 8 })
          })
        }
        .width('100%')
        .padding({ top: 8, bottom: 8 })
        .flexWrap(FlexWrap.Wrap)
      }

      // 执行概要确认
      this.SectionTitle('执行确认')

      this.ReadOnlyField('执行人', this.executor)
      this.ReadOnlyField('监印人', this.witness)
      this.ReadOnlyField('用印份数', `${this.actualCount}份`)
      this.ReadOnlyField('GPS', `${this.gpsLat}, ${this.gpsLng}`)
      this.ReadOnlyField('指纹验证', this.fingerprintVerify ? '✅ 已验证' : '❌ 未验证')
      this.ReadOnlyField('人脸验证', this.faceVerify ? '✅ 已验证' : '❌ 未验证')
      this.ReadOnlyField('现场照片', `${this.photos.length}张`)
    }
    .width('100%')
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
        .fontColor('#fff')
        .layoutWeight(1)
    }
    .width('100%')
    .padding({ top: 4, bottom: 4 })
  }

  private getCurrentLocation() {
    // 模拟GPS坐标
    this.gpsLat = '39.9042';
    this.gpsLng = '116.4074';
  }

  private takePhoto() {
    // 模拟拍照
    this.photos.push(`photo_${Date.now()}.jpg`);
  }

  private execute() {
    if (!this.executor.trim() || !this.witness.trim()) {
      return;
    }

    const lat = parseFloat(this.gpsLat) || 0;
    const lng = parseFloat(this.gpsLng) || 0;

    if (this.application) {
      sealState.executeApplication(
        this.application.id,
        this.executor,
        this.witness,
        this.photos,
        { lat, lng }
      );
    }

    this.controller.close();
  }
}
