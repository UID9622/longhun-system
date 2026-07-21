// entry/src/main/ets/pages/StackDemoPage.ets
// 龍魂 · Stack 布局演示页面

import { overlayState, OverlayState, DialogConfig, ToastConfig, LoadingConfig, AnimationType, LayerType } from '../models/StackModel';
import { OverlayContainer } from '../components/OverlayContainer';
import { OverlayUtils } from '../utils/OverlayUtils';

const MASTER_DNA = "ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️";
const MASTER_UID = "9622";

@Entry
@Component
struct StackDemoPage {
  @StorageLink('overlayState') overlayState: OverlayState = overlayState;
  @State private demoProgress: number = 0;

  build() {
    OverlayContainer({ contentBuilder: this.MainContentBuilder.bind(this) })
  }

  @Builder
  MainContentBuilder() {
    Column() {
      this.HeaderBuilder()
      this.StatsBuilder()
      this.DemoButtonsBuilder()
      this.LayerInfoBuilder()
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
        Text('龍魂 Stack 布局').fontSize(20).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text(`UID:${MASTER_UID} · API 24`).fontSize(12).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start).layoutWeight(1)
    }
    .width('100%').height(56).padding({ left: 16, right: 16 }).backgroundColor('#1a1a1a').border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatsBuilder() {
    Row() {
      this.StatCard('层级', this.overlayState.statistics.totalLayers.toString(), '#fff')
      this.StatCard('遮罩', this.overlayState.statistics.isMaskActive ? '●' : '○', this.overlayState.statistics.isMaskActive ? '#00ff00' : '#666')
      this.StatCard('Z-Index', this.overlayState.statistics.maxZIndex.toString(), '#ffcc00')
      this.StatCard('弹窗', this.overlayState.statistics.hasDialog ? '●' : '○', this.overlayState.statistics.hasDialog ? '#c41e3a' : '#666')
      this.StatCard('加载', this.overlayState.statistics.hasLoading ? '●' : '○', this.overlayState.statistics.hasLoading ? '#0066cc' : '#666')
    }
    .width('100%').height(80).padding({ left: 12, right: 12, top: 8, bottom: 8 }).backgroundColor('#1a1a1a').border({ width: { bottom: 1 }, color: '#333' })
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() { Text(value).fontSize(24).fontWeight(FontWeight.Bold).fontColor(color); Text(label).fontSize(11).fontColor('#666').margin({ top: 4 }); }
    .width('20%').height('100%').justifyContent(FlexAlign.Center).alignItems(HorizontalAlign.Center)
  }

  @Builder
  DemoButtonsBuilder() {
    Scroll() {
      Column() {
        Text('弹窗演示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('确认弹窗').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            OverlayUtils.confirm('确认操作', '您确定要执行此操作吗？', () => { OverlayUtils.success('操作已确认'); });
          })
          Button('警告弹窗').fontSize(12).fontColor('#fff').backgroundColor('#ff6600').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.alert('系统警告', '检测到异常状态，请检查配置。');
          })
          Button('错误弹窗').fontSize(12).fontColor('#fff').backgroundColor('#c41e3a').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.error('操作失败', '网络连接超时，请重试。');
          })
          Button('输入弹窗').fontSize(12).fontColor('#fff').backgroundColor('#0066cc').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.prompt('请输入', '请输入项目名称', (value) => { OverlayUtils.success(`输入: ${value}`); });
          })
        }
        .width('100%').margin({ bottom: 16 })

        Text('Toast 演示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('成功 Toast').fontSize(12).fontColor('#fff').backgroundColor('#00ff00').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            OverlayUtils.success('操作成功！');
          })
          Button('错误 Toast').fontSize(12).fontColor('#fff').backgroundColor('#ff0000').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.errorToast('操作失败！');
          })
          Button('顶部 Toast').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            overlayState.showToast(new ToastConfig({ message: '顶部提示', position: 'top', duration: 2000 }));
          })
          Button('底部 Toast').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            overlayState.showToast(new ToastConfig({ message: '底部提示', position: 'bottom', duration: 2000 }));
          })
        }
        .width('100%').margin({ bottom: 16 })

        Text('Loading 演示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('显示 Loading').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            OverlayUtils.showLoading('正在加载数据...');
            setTimeout(() => { OverlayUtils.hideLoading(); OverlayUtils.success('加载完成'); }, 3000);
          })
          Button('进度 Loading').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.demoProgress = 0;
            OverlayUtils.showProgressLoading('下载中...', 0);
            const interval = setInterval(() => {
              this.demoProgress += 10;
              OverlayUtils.updateProgress(this.demoProgress);
              if (this.demoProgress >= 100) {
                clearInterval(interval);
                setTimeout(() => { OverlayUtils.hideLoading(); OverlayUtils.success('下载完成'); }, 500);
              }
            }, 300);
          })
          Button('可取消 Loading').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            OverlayUtils.showLoading('处理中...', true);
          })
        }
        .width('100%').margin({ bottom: 16 })

        Text('动画演示').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('淡入').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            this.showAnimatedDialog(AnimationType.FADE);
          })
          Button('滑入').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.showAnimatedDialog(AnimationType.SLIDE_UP);
          })
          Button('缩放').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.showAnimatedDialog(AnimationType.SCALE);
          })
          Button('弹跳').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.showAnimatedDialog(AnimationType.BOUNCE);
          })
        }
        .width('100%').margin({ bottom: 16 })

        Text('层级管理').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ top: 16, bottom: 12 }).width('100%')

        Row() {
          Button('清空所有').fontSize(12).fontColor('#fff').backgroundColor('#c41e3a').borderRadius(8).padding({ left: 12, right: 12 }).onClick(() => {
            OverlayUtils.clearAll();
          })
          Button('多层弹窗').fontSize(12).fontColor('#fff').backgroundColor('#333').borderRadius(8).padding({ left: 12, right: 12 }).margin({ left: 8 }).onClick(() => {
            this.showMultiLayerDemo();
          })
        }
        .width('100%').margin({ bottom: 16 })
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
    .scrollBar(BarState.Auto)
  }

  @Builder
  LayerInfoBuilder() {
    Column() {
      Text('当前层级栈').fontSize(14).fontWeight(FontWeight.Bold).fontColor('#fff').margin({ bottom: 8 })

      if (this.overlayState.layerStack.layers.length === 0) {
        Text('空').fontSize(12).fontColor('#666')
      } else {
        ForEach(this.overlayState.layerStack.layers, (layer) => {
          Row() {
            Text(`${layer.type}`).fontSize(12).fontColor('#fff').layoutWeight(1)
            Text(`zIndex: ${layer.zIndex}`).fontSize(12).fontColor('#888')
            Text(`${layer.maskType}`).fontSize(12).fontColor('#666').margin({ left: 8 })
          }
          .width('100%')
          .padding({ top: 4, bottom: 4 })
        })
      }
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#1a1a1a')
    .border({ width: { top: 1 }, color: '#333' })
  }

  // 显示动画弹窗
  showAnimatedDialog(animation: AnimationType): void {
    overlayState.showDialog(new DialogConfig({
      title: '动画演示',
      message: `这是 ${animation} 动画效果`,
      icon: '🎬',
      primaryButton: { label: '确定', type: 'primary' },
      enterAnimation: animation,
      animationDuration: 500
    }));
  }

  // 多层弹窗演示
  showMultiLayerDemo(): void {
    overlayState.showDialog(new DialogConfig({
      title: '第一层',
      message: '点击确定打开第二层',
      primaryButton: { 
        label: '打开第二层', 
        type: 'primary',
        action: () => {
          overlayState.showDialog(new DialogConfig({
            title: '第二层',
            message: '这是第二层弹窗',
            primaryButton: { label: '确定', type: 'primary' }
          }));
        }
      }
    }));
  }
}
