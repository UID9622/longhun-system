// entry/src/main/ets/components/OverlayContainer.ets
// 龍魂 · Stack 遮罩层容器

import { overlayState, OverlayState, LayerType, MaskType, AnimationType, DialogConfig, ToastConfig, LoadingConfig } from '../models/StackModel';

@Component
export struct OverlayContainer {
  @StorageLink('overlayState') overlayState: OverlayState = overlayState;
  @BuilderParam contentBuilder: () => void;  // 基础内容Builder

  // 动画效果
  getAnimation(effect: AnimationType): object {
    switch (effect) {
      case AnimationType.FADE: return { opacity: [0, 1], duration: 300 };
      case AnimationType.SLIDE_UP: return { translate: { y: ['100%', '0%'] }, opacity: [0, 1], duration: 300 };
      case AnimationType.SLIDE_DOWN: return { translate: { y: ['-100%', '0%'] }, opacity: [0, 1], duration: 300 };
      case AnimationType.SLIDE_LEFT: return { translate: { x: ['100%', '0%'] }, opacity: [0, 1], duration: 300 };
      case AnimationType.SLIDE_RIGHT: return { translate: { x: ['-100%', '0%'] }, opacity: [0, 1], duration: 300 };
      case AnimationType.SCALE: return { scale: { x: [0.8, 1], y: [0.8, 1] }, opacity: [0, 1], duration: 300 };
      case AnimationType.ROTATE: return { rotate: { z: [-90, 0] }, opacity: [0, 1], duration: 300 };
      case AnimationType.BOUNCE: return { scale: { x: [0.3, 1.1, 1], y: [0.3, 1.1, 1] }, opacity: [0, 1], duration: 500 };
      default: return { opacity: [0, 1], duration: 300 };
    }
  }

  build() {
    Stack({ alignContent: Alignment.Center }) {
      // === 基础层 ===
      this.contentBuilder()

      // === 遮罩层 ===
      if (this.overlayState.isMaskVisible) {
        Column()
          .width('100%')
          .height('100%')
          .backgroundColor(this.overlayState.maskColor)
          .zIndex(this.overlayState.maskZIndex)
          .onClick(() => { this.overlayState.handleMaskTap(); })
          .transition(TransitionType.All)
          .animation({ duration: 300, curve: Curve.EaseInOut })
      }

      // === 弹窗层 ===
      if (this.overlayState.currentDialog) {
        this.DialogBuilder(this.overlayState.currentDialog)
      }

      // === Toast 层 ===
      if (this.overlayState.currentToast) {
        this.ToastBuilder(this.overlayState.currentToast)
      }

      // === Loading 层 ===
      if (this.overlayState.currentLoading) {
        this.LoadingBuilder(this.overlayState.currentLoading)
      }
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // === 弹窗 Builder ===
  @Builder
  DialogBuilder(config: DialogConfig) {
    Column() {
      Column() {
        // 图标
        if (config.icon) {
          Text(config.icon)
            .fontSize(48)
            .margin({ bottom: 16 })
        }

        // 标题
        Text(config.title)
          .fontSize(18)
          .fontWeight(FontWeight.Bold)
          .fontColor('#fff')
          .textAlign(TextAlign.Center)
          .width('100%')

        // 消息
        Text(config.message)
          .fontSize(14)
          .fontColor('#888')
          .textAlign(TextAlign.Center)
          .width('100%')
          .margin({ top: 8, bottom: 16 })

        // 输入框
        if (config.hasInput) {
          TextInput({ placeholder: config.inputPlaceholder || '请输入...' })
            .width('100%')
            .height(44)
            .backgroundColor('#1a1a1a')
            .fontColor('#fff')
            .placeholderColor('#666')
            .borderRadius(8)
            .padding({ left: 12, right: 12 })
            .margin({ bottom: 16 })
        }

        // 按钮组
        Row() {
          if (config.cancelButton) {
            Button(config.cancelButton.label)
              .fontSize(14)
              .fontColor('#888')
              .backgroundColor('#1a1a1a')
              .borderRadius(8)
              .padding({ left: 16, right: 16 })
              .layoutWeight(1)
              .onClick(() => {
                config.cancelButton?.action?.();
                this.overlayState.dismissDialog();
              })
          }

          if (config.secondaryButton) {
            Button(config.secondaryButton.label)
              .fontSize(14)
              .fontColor('#fff')
              .backgroundColor('#333')
              .borderRadius(8)
              .padding({ left: 16, right: 16 })
              .layoutWeight(1)
              .margin({ left: 8 })
              .onClick(() => {
                config.secondaryButton?.action?.();
              })
          }

          if (config.primaryButton) {
            Button(config.primaryButton.label)
              .fontSize(14)
              .fontColor('#fff')
              .backgroundColor('#c41e3a')
              .borderRadius(8)
              .padding({ left: 16, right: 16 })
              .layoutWeight(1)
              .margin({ left: 8 })
              .onClick(() => {
                config.primaryButton?.action?.();
                this.overlayState.dismissDialog();
              })
          }
        }
        .width('100%')
      }
      .width(`${config.width}%`)
      .padding(24)
      .backgroundColor('#262626')
      .borderRadius(config.borderRadius)
      .shadow({ radius: 16, color: 'rgba(0,0,0,0.5)' })
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .zIndex(config.zIndex)
    .transition(this.getAnimation(config.enterAnimation))
    .animation({ duration: config.animationDuration, curve: Curve.EaseInOut })
    .onClick(() => {}) // 阻止事件冒泡
  }

  // === Toast Builder ===
  @Builder
  ToastBuilder(config: ToastConfig) {
    Column() {
      Row() {
        if (config.icon) {
          Text(config.icon)
            .fontSize(20)
            .margin({ right: 8 })
        }

        Text(config.message)
          .fontSize(14)
          .fontColor('#fff')
      }
      .padding({ left: 16, right: 16, top: 12, bottom: 12 })
      .backgroundColor('rgba(0,0,0,0.8)')
      .borderRadius(8)
    }
    .width('100%')
    .height('100%')
    .justifyContent(
      config.position === 'top' ? FlexAlign.Start :
      config.position === 'bottom' ? FlexAlign.End : FlexAlign.Center
    )
    .alignItems(HorizontalAlign.Center)
    .padding({ top: config.position === 'top' ? 80 : 0, bottom: config.position === 'bottom' ? 80 : 0 })
    .zIndex(config.zIndex)
    .transition(TransitionType.All)
    .animation({ duration: 300, curve: Curve.EaseInOut })
    .onClick(() => { this.overlayState.dismissToast(); })
  }

  // === Loading Builder ===
  @Builder
  LoadingBuilder(config: LoadingConfig) {
    Column() {
      Column() {
        // Loading 动画
        LoadingProgress()
          .width(48)
          .height(48)
          .color('#c41e3a')

        // 消息
        Text(config.message)
          .fontSize(14)
          .fontColor('#fff')
          .margin({ top: 16 })

        // 进度条
        if (config.progress !== undefined) {
          Stack() {
            Row()
              .width('100%')
              .height(4)
              .backgroundColor('#333')
              .borderRadius(2)

            Row()
              .width(`${config.progress}%`)
              .height(4)
              .backgroundColor('#c41e3a')
              .borderRadius(2)
          }
          .width(200)
          .height(4)
          .margin({ top: 12 })

          Text(`${config.progress}%`)
            .fontSize(12)
            .fontColor('#888')
            .margin({ top: 4 })
        }

        // 取消按钮
        if (config.cancelable) {
          Button('取消')
            .fontSize(12)
            .fontColor('#888')
            .backgroundColor('transparent')
            .margin({ top: 12 })
            .onClick(() => { this.overlayState.dismissLoading(); })
        }
      }
      .padding(32)
      .backgroundColor('#262626')
      .borderRadius(12)
    }
    .width('100%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
    .zIndex(config.zIndex)
    .transition(TransitionType.All)
    .animation({ duration: 300, curve: Curve.EaseInOut })
    .onClick(() => {}) // 阻止事件冒泡
  }
}
