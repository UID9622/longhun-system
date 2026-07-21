// entry/src/main/ets/components/ImageCropper.ets
// 龍魂 · 图片裁剪预览组件 · 交互式裁剪

import { clipState, ClipConfig, ClipType } from '../models/ClipModel';

@Component
export struct ImageCropper {
  @Prop src: Resource | string;
  @Prop aspectRatio: number = 1;      // 宽高比 1=正方形, 16/9=宽屏
  @Prop cropShape: 'rect' | 'circle' | 'ellipse' = 'rect';

  @State private imageWidth: number = 300;
  @State private imageHeight: number = 300;
  @State private offsetX: number = 0;
  @State private offsetY: number = 0;
  @State private scale: number = 1;
  @State private isDragging: boolean = false;
  @State private startX: number = 0;
  @State private startY: number = 0;

  // 裁剪区域尺寸
  private getCropWidth(): number {
    return Math.min(this.imageWidth, 300);
  }

  private getCropHeight(): number {
    return this.getCropWidth() / this.aspectRatio;
  }

  // 获取裁剪参数
  getCropData(): { x: number, y: number, width: number, height: number, scale: number } {
    return {
      x: this.offsetX,
      y: this.offsetY,
      width: this.getCropWidth(),
      height: this.getCropHeight(),
      scale: this.scale
    };
  }

  aboutToAppear() {
    const config = new ClipConfig({
      type: this.cropShape === 'circle' ? ClipType.CIRCLE :
            this.cropShape === 'ellipse' ? ClipType.ELLIPSE : ClipType.RECT,
      params: { width: this.getCropWidth(), height: this.getCropHeight() },
      name: 'ImageCropper'
    });
    clipState.addConfig(config);
  }

  build() {
    Column() {
      // 标题
      Text('🐉 图片裁剪').fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })

      // 裁剪容器
      Stack() {
        // 背景遮罩（暗化区域）
        Column()
          .width('100%')
          .height('100%')
          .backgroundColor('rgba(0,0,0,0.7)')

        // 图片层（可拖拽缩放）
        Image(this.src)
          .width(this.imageWidth * this.scale)
          .height(this.imageHeight * this.scale)
          .objectFit(ImageFit.Cover)
          .position({
            x: this.offsetX + (300 - this.getCropWidth()) / 2,
            y: this.offsetY + (300 - this.getCropHeight()) / 2
          })
          .clip(this.getClipShape())
          .gesture(
            PanGesture()
              .onActionStart((event) => {
                this.isDragging = true;
                this.startX = this.offsetX;
                this.startY = this.offsetY;
              })
              .onActionUpdate((event) => {
                this.offsetX = this.startX + event.offsetX;
                this.offsetY = this.startY + event.offsetY;
              })
              .onActionEnd(() => {
                this.isDragging = false;
              })
          )

        // 裁剪框边框
        this.CropFrameBuilder()

        // 角标
        this.CornerMarkersBuilder()
      }
      .width(300)
      .height(300)
      .backgroundColor('#0a0a0a')
      .border({ width: 1, color: '#333' })

      // 控制栏
      this.ControlBarBuilder()
    }
    .width('100%')
    .padding(16)
  }

  @Builder
  private getClipShape() {
    if (this.cropShape === 'circle') {
      return new Circle({ width: this.getCropWidth(), height: this.getCropHeight() });
    } else if (this.cropShape === 'ellipse') {
      return new Ellipse({ width: this.getCropWidth(), height: this.getCropHeight() });
    } else {
      return new Rect({ width: this.getCropWidth(), height: this.getCropHeight() });
    }
  }

  @Builder
  CropFrameBuilder() {
    Column()
      .width(this.getCropWidth())
      .height(this.getCropHeight())
      .border({ width: 2, color: '#c41e3a' })
      .position({
        x: (300 - this.getCropWidth()) / 2,
        y: (300 - this.getCropHeight()) / 2
      })
  }

  @Builder
  CornerMarkersBuilder() {
    const corners = [
      { x: (300 - this.getCropWidth()) / 2, y: (300 - this.getCropHeight()) / 2 },
      { x: (300 + this.getCropWidth()) / 2 - 8, y: (300 - this.getCropHeight()) / 2 },
      { x: (300 - this.getCropWidth()) / 2, y: (300 + this.getCropHeight()) / 2 - 8 },
      { x: (300 + this.getCropWidth()) / 2 - 8, y: (300 + this.getCropHeight()) / 2 - 8 }
    ];

    ForEach(corners, (corner, index) => {
      Row()
        .width(16)
        .height(16)
        .backgroundColor('#c41e3a')
        .border({ width: 2, color: '#fff' })
        .position({ x: corner.x - 4, y: corner.y - 4 })
    })
  }

  @Builder
  ControlBarBuilder() {
    Row() {
      // 缩放控制
      Button('➖').fontSize(14).fontColor('#fff').backgroundColor('#333').borderRadius(8).onClick(() => {
        this.scale = Math.max(0.5, this.scale - 0.1);
      })
      Slider({ value: this.scale * 100, min: 50, max: 200, step: 10 })
        .width(150)
        .onChange((value) => { this.scale = value / 100; })
      Button('➕').fontSize(14).fontColor('#fff').backgroundColor('#333').borderRadius(8).onClick(() => {
        this.scale = Math.min(2.0, this.scale + 0.1);
      })

      // 重置
      Button('重置').fontSize(12).fontColor('#fff').backgroundColor('#c41e3a').borderRadius(8).margin({ left: 12 }).onClick(() => {
        this.offsetX = 0;
        this.offsetY = 0;
        this.scale = 1;
      })
    }
    .width('100%')
    .justifyContent(FlexAlign.Center)
    .margin({ top: 16 })
  }
}
