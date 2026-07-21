/*
 * ==========================================================================
 * 通心译 — 设置页面 ✅ 检查项#2 (可修改服务器地址)
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-SETTINGS-v1.0
 * ==========================================================================
 */

import { ServerConfig } from '../utils/ServerConfig';
import { DeviceCapability } from '../utils/DeviceCapability';
import { ScreenAdapter } from '../utils/ScreenAdapter';
import { DRAGON_SOUL_MARKS } from '../common/types';

@Entry
@Component
struct Settings {
  @State serverUrl: string = '加载中...';
  @State newServerUrl: string = '';
  @State deviceInfo: string = '';
  @State saveStatus: string = '';

  aboutToAppear(): void {
    this.loadSettings();
    this.deviceInfo = `设备: ${DeviceCapability.getDeviceType()} | SDK: ${DeviceCapability.getSDKVersion()} | 密度: ${DeviceCapability.getScreenDensity()}`;
  }

  async loadSettings(): Promise<void> {
    try {
      const context = getContext(this);
      const url = await ServerConfig.getBaseUrl(context);
      this.serverUrl = url;
      this.newServerUrl = url;
    } catch {
      this.serverUrl = 'http://localhost:8777';
    }
  }

  build() {
    Column() {
      // 标题
      Row() {
        Button('← 返回')
          .fontSize(ScreenAdapter.fp2px(14))
          .backgroundColor(Color.Transparent)
          .fontColor('#4a6cf7')
          .onClick(() => {
            // 返回主页
          })

        Blank()

        Text('通心译 · 设置')
          .fontSize(ScreenAdapter.fp2px(18))
          .fontWeight(FontWeight.Bold)
      }
      .width('100%')
      .padding(16)

      Divider().color('#e0e0e8')

      // 服务器配置
      Column() {
        Text('API 服务器地址')
          .fontSize(ScreenAdapter.fp2px(14))
          .fontColor('#666')
          .margin({ bottom: 8 })
          .alignSelf(ItemAlign.Start)

        TextInput({ text: this.newServerUrl, placeholder: 'http://localhost:8777' })
          .fontSize(ScreenAdapter.fp2px(15))
          .backgroundColor('#ffffff')
          .borderRadius(8)
          .border({ width: 1, color: '#d0d0d8' })
          .padding(12)
          .width('100%')
          .onChange((value: string) => {
            this.newServerUrl = value;
          })

        Row() {
          Button('保存')
            .fontSize(ScreenAdapter.fp2px(14))
            .backgroundColor('#4a6cf7')
            .fontColor('#ffffff')
            .borderRadius(8)
            .padding({ left: 20, right: 20, top: 8, bottom: 8 })
            .onClick(async () => {
              try {
                const context = getContext(this);
                await ServerConfig.setBaseUrl(context, this.newServerUrl);
                this.serverUrl = this.newServerUrl;
                this.saveStatus = '✅ 已保存';
                setTimeout(() => { this.saveStatus = ''; }, 2000);
              } catch {
                this.saveStatus = '❌ 保存失败';
              }
            })

          if (this.saveStatus.length > 0) {
            Text(this.saveStatus)
              .fontSize(ScreenAdapter.fp2px(13))
              .fontColor('#27ae60')
              .margin({ left: 12 })
          }

          Blank()

          Button('重置')
            .fontSize(ScreenAdapter.fp2px(14))
            .backgroundColor('#f0f0f4')
            .fontColor('#666')
            .borderRadius(8)
            .padding({ left: 20, right: 20, top: 8, bottom: 8 })
            .onClick(() => {
              this.newServerUrl = 'http://localhost:8777';
            })
        }
        .width('100%')
        .margin({ top: 12 })
      }
      .width('92%')
      .padding(16)
      .backgroundColor('#ffffff')
      .borderRadius(12)
      .margin({ top: 16, left: 16, right: 16 })

      // 当前状态
      Column() {
        Text('当前服务器: ' + this.serverUrl)
          .fontSize(ScreenAdapter.fp2px(12))
          .fontColor('#999')
      }
      .width('92%')
      .padding(12)
      .margin({ top: 8, left: 16, right: 16 })

      // 设备信息
      Column() {
        Text('设备信息')
          .fontSize(ScreenAdapter.fp2px(14))
          .fontColor('#666')
          .margin({ bottom: 4 })
          .alignSelf(ItemAlign.Start)

        Text(this.deviceInfo)
          .fontSize(ScreenAdapter.fp2px(12))
          .fontColor('#999')

        Text(DRAGON_SOUL_MARKS.DNA)
          .fontSize(ScreenAdapter.fp2px(10))
          .fontColor('#ccc')
          .margin({ top: 8 })
      }
      .width('92%')
      .padding(16)
      .margin({ top: 8, left: 16, right: 16 })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#f5f6fa')
  }
}
