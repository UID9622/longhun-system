// entry/src/main/ets/pages/ClipPage.ets
// 龍魂 · Clip裁剪演示页面

import { clipState, ClipState, ClipType } from '../models/ClipModel';
import { CircleAvatar } from '../components/CircleAvatar';
import { RoundedCard } from '../components/RoundedCard';
import { ImageCropper } from '../components/ImageCropper';
import { SafeAreaClip } from '../components/SafeAreaClip';
import { MaskClip } from '../components/MaskClip';

@Entry
@Component
struct ClipPage {
  @StorageLink('clipState') clipState: ClipState = clipState;
  @State private selectedTab: number = 0;
  @State private demoImage: Resource = $r('app.media.demo_image');

  build() {
    Column() {
      this.HeaderBuilder()
      this.StatsBuilder()
      this.TabBuilder()
      this.ContentBuilder()
      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 8 })
      Column() {
        Text('龍魂 Clip 裁剪').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:9622 · 图形边界控制`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('配置', `${this.clipState.statistics.totalConfigs}`, '#00ff00')
      this.StatCard('效果', `${this.clipState.statistics.totalEffects}`, '#88ff00')
      this.StatCard('活跃', `${this.clipState.statistics.activeEffects}`, '#ffcc00')
      this.StatCard('渲染', `${this.clipState.statistics.avgRenderTime}ms`, '#ff6600')
      this.StatCard('缓存', `${this.clipState.statistics.cacheHitRate}%`, '#fff')
    }
    .width('100%')
    .height(80)
    .padding({ left: 12, right: 12, top: 8, bottom: 8 })
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value).fontSize(20).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label).fontSize(11).fontColor('#666').margin({ top: 4 })
    }
    .width('20%')
    .height('100%')
    .justifyContent(FlexAlign.Center)
    .alignItems(HorizontalAlign.Center)
  }

  @Builder
  TabBuilder() {
    Row() {
      ForEach([
        { label: '圆形', icon: '⭕' },
        { label: '圆角', icon: '▢' },
        { label: '裁剪', icon: '✂️' },
        { label: '安全区', icon: '🛡️' },
        { label: '蒙版', icon: '👻' }
      ], (item: {label: string, icon: string}, index: number) => {
        Column() {
          Text(`${item.icon} ${item.label}`)
            .fontSize(13)
            .fontWeight(this.selectedTab === index ? FontWeight.Bold : FontWeight.Normal)
            .fontColor(this.selectedTab === index ? '#c41e3a' : '#888')
          if (this.selectedTab === index) {
            Divider()
              .strokeWidth(2)
              .color('#c41e3a')
              .width(20)
              .margin({ top: 4 })
          }
        }
        .padding({ top: 12, bottom: 12, left: 16, right: 16 })
        .onClick(() => { this.selectedTab = index; })
      })
    }
    .width('100%')
    .justifyContent(FlexAlign.SpaceAround)
    .backgroundColor('#1a1a1a')
    .border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  ContentBuilder() {
    if (this.selectedTab === 0) { this.CircleDemoBuilder() }
    else if (this.selectedTab === 1) { this.RoundedDemoBuilder() }
    else if (this.selectedTab === 2) { this.CropperDemoBuilder() }
    else if (this.selectedTab === 3) { this.SafeAreaDemoBuilder() }
    else { this.MaskDemoBuilder() }
  }

  // === 圆形裁剪演示 ===
  @Builder
  CircleDemoBuilder() {
    Scroll() {
      Column() {
        Text('圆形头像裁剪').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })

        // 不同尺寸圆形头像
        Row() {
          CircleAvatar({ src: this.demoImage, size: 40, borderWidth: 1 })
          CircleAvatar({ src: this.demoImage, size: 60, borderWidth: 2 })
          CircleAvatar({ src: this.demoImage, size: 80, borderWidth: 2, borderColor: '#c41e3a' })
          CircleAvatar({ src: this.demoImage, size: 100, borderWidth: 3, borderColor: '#00ff00' })
        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceAround)
        .margin({ bottom: 24 })

        // 圆形图片展示
        Text('圆形图片展示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })

        Image(this.demoImage)
          .width(200)
          .height(200)
          .objectFit(ImageFit.Cover)
          .clip(new Circle({ width: 200, height: 200 }))
          .border({ width: 3, color: '#c41e3a', radius: 100 })
          .shadow({ radius: 12, color: 'rgba(196,30,58,0.4)', offsetY: 6 })

        // 圆形徽章
        Text('圆形徽章').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 24, bottom: 16 })

        Stack() {
          CircleAvatar({ src: this.demoImage, size: 120 })
          Row() {
            Text('VIP').fontSize(12).fontWeight(FontWeight.Bold).fontColor('#fff')
          }
          .width(36)
          .height(36)
          .backgroundColor('#c41e3a')
          .clip(new Circle({ width: 36, height: 36 }))
          .border({ width: 2, color: '#fff', radius: 18 })
          .position({ x: 84, y: 84 })
        }
        .width(120)
        .height(120)
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  // === 圆角裁剪演示 ===
  @Builder
  RoundedDemoBuilder() {
    Scroll() {
      Column() {
        Text('圆角卡片裁剪').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })

        // 统一圆角
        RoundedCard({
          radius: 16,
          contentBuilder: () => {
            Column() {
              Text('统一圆角卡片').fontSize(14).fontColor('#fff').fontWeight(FontWeight.Medium)
              Text('radius: 16px').fontSize(12).fontColor('#666').margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.Start)
          }
        })
        .margin({ bottom: 12 })

        // 顶部圆角
        RoundedCard({
          radius: 0,
          topRadius: 16,
          bottomRadius: 0,
          backgroundColor: '#c41e3a',
          contentBuilder: () => {
            Column() {
              Text('顶部圆角').fontSize(14).fontColor('#fff').fontWeight(FontWeight.Medium)
              Text('topRadius: 16px').fontSize(12).fontColor('rgba(255,255,255,0.7)').margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.Start)
          }
        })
        .margin({ bottom: 12 })

        // 底部圆角
        RoundedCard({
          radius: 0,
          topRadius: 0,
          bottomRadius: 16,
          backgroundColor: '#1a3a1a',
          contentBuilder: () => {
            Column() {
              Text('底部圆角').fontSize(14).fontColor('#fff').fontWeight(FontWeight.Medium)
              Text('bottomRadius: 16px').fontSize(12).fontColor('#666').margin({ top: 4 })
            }
            .alignItems(HorizontalAlign.Start)
          }
        })
        .margin({ bottom: 12 })

        // 大圆角图片
        Text('圆角图片').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 12, bottom: 16 })

        Image(this.demoImage)
          .width('100%')
          .height(200)
          .objectFit(ImageFit.Cover)
          .clip(new RoundedRect({
            width: '100%',
            height: 200,
            topLeft: 24,
            topRight: 24,
            bottomLeft: 8,
            bottomRight: 8
          }))
          .shadow({ radius: 8, color: 'rgba(0,0,0,0.3)', offsetY: 4 })
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  // === 裁剪器演示 ===
  @Builder
  CropperDemoBuilder() {
    Column() {
      Text('交互式裁剪').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })

      ImageCropper({
        src: this.demoImage,
        aspectRatio: 1,
        cropShape: 'circle'
      })
      .layoutWeight(1)
    }
    .width('100%')
    .padding(16)
    .layoutWeight(1)
  }

  // === 安全区演示 ===
  @Builder
  SafeAreaDemoBuilder() {
    Column() {
      Text('安全区域裁剪').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })

      SafeAreaClip({
        safeTop: true,
        safeBottom: true,
        extraTop: 10,
        extraBottom: 10,
        contentBuilder: () => {
          Column() {
            Text('内容区域').fontSize(16).fontColor('#fff').fontWeight(FontWeight.Bold)
            Text('自动避开刘海/挖孔/手势条').fontSize(12).fontColor('#666').margin({ top: 8 })
            Text('顶部安全区: 44px').fontSize(12).fontColor('#888').margin({ top: 24 })
            Text('底部安全区: 34px').fontSize(12).fontColor('#888')
            Text('额外间距: 10px').fontSize(12).fontColor('#888')
          }
          .width('100%')
          .height('100%')
          .justifyContent(FlexAlign.Center)
          .backgroundColor('#1a1a1a')
        }
      })
      .width('100%')
      .height(400)
      .backgroundColor('#0a0a0a')
      .border({ width: 1, color: '#333' })
    }
    .width('100%')
    .padding(16)
    .layoutWeight(1)
  }

  // === 蒙版演示 ===
  @Builder
  MaskDemoBuilder() {
    Scroll() {
      Column() {
        Text('渐变蒙版裁剪').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 16 })

        // 底部渐变
        Text('底部渐变消失').fontSize(14).fontColor('#fff').margin({ bottom: 8 })
        Stack() {
          Image(this.demoImage)
            .width('100%')
            .height(200)
            .objectFit(ImageFit.Cover)

          MaskClip({
            direction: 'bottom',
            fadeLength: 80,
            contentBuilder: () => {
              Column().width('100%').height('100%')
            }
          })
        }
        .width('100%')
        .height(200)
        .margin({ bottom: 16 })

        // 顶部渐变
        Text('顶部渐变消失').fontSize(14).fontColor('#fff').margin({ bottom: 8 })
        Stack() {
          Image(this.demoImage)
            .width('100%')
            .height(200)
            .objectFit(ImageFit.Cover)

          MaskClip({
            direction: 'top',
            fadeLength: 60,
            contentBuilder: () => {
              Column().width('100%').height('100%')
            }
          })
        }
        .width('100%')
        .height(200)
        .margin({ bottom: 16 })

        // 左右渐变
        Text('左右渐变消失').fontSize(14).fontColor('#fff').margin({ bottom: 8 })
        Row() {
          Stack() {
            Image(this.demoImage)
              .width('100%')
              .height(150)
              .objectFit(ImageFit.Cover)

            MaskClip({
              direction: 'right',
              fadeLength: 50,
              contentBuilder: () => {
                Column().width('100%').height('100%')
              }
            })
          }
          .width('50%')
          .height(150)

          Stack() {
            Image(this.demoImage)
              .width('100%')
              .height(150)
              .objectFit(ImageFit.Cover)

            MaskClip({
              direction: 'left',
              fadeLength: 50,
              contentBuilder: () => {
                Column().width('100%').height('100%')
              }
            })
          }
          .width('50%')
          .height(150)
        }
        .width('100%')
        .margin({ bottom: 16 })
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  @Builder
  FooterBuilder() {
    Row() {
      Column() {
        Text('🐉').fontSize(20)
        Text('UID:9622').fontSize(10).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Row() {
        Text(`📐 ${this.clipState.statistics.totalConfigs} 配置`).fontSize(12).fontColor('#888')
        Text(`✂️ ${this.clipState.statistics.totalEffects} 效果`).fontSize(12).fontColor('#888').margin({ left: 12 })
      }
    }
    .width('100%')
    .height(40)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }
}
