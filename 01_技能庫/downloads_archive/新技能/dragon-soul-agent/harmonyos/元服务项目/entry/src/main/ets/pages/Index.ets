import { router } from '@kit.ArkUI';

// ============================================================
// 龍魂AI元服务首页 - 核心能力总览
// DNA: #龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0
// 创始人: UID9622 · 龍芯北辰 · 诸葛鑫
// ============================================================

// 功能卡片数据模型
interface 功能卡片数据 {
  标题: string;
  描述: string;
  图标: Resource;
  颜色: string;
  页面: string;
}

@Entry
@Component
struct Index {
  // 状态变量
  @State 当前页面: string = '首页';
  @StorageLink('longhun_dna') dna码: string = '#龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0';
  @StorageLink('gentleman_signed') 已签协议: boolean = false;
  @State 设备类型: string = 'phone'; // phone | tablet | car

  // 核心功能卡片列表
  private 功能列表: 功能卡片数据[] = [
    {
      标题: 'CNSH编辑器',
      描述: '用中文写代码',
      图标: $r('app.media.startIcon'),
      颜色: '#FF6B35',
      页面: 'pages/CNSHEditor'
    },
    {
      标题: '通心译',
      描述: '49术语AI翻译',
      图标: $r('app.media.startIcon'),
      颜色: '#4ECDC4',
      页面: 'pages/TongxinTranslate'
    },
    {
      标题: '三色审计',
      描述: '代码质量审计',
      图标: $r('app.media.startIcon'),
      颜色: '#45B7D1',
      页面: 'pages/AuditDashboard'
    },
    {
      标题: '龍魂识别',
      描述: '图/音/文识别',
      图标: $r('app.media.startIcon'),
      颜色: '#96CEB4',
      页面: 'pages/CNSHEditor' // 暂时跳转编辑器
    }
  ];

  // 顶部Logo区域构建
  @Builder
  顶部Logo区() {
    Row() {
      // 龍魂Logo图标
      Image($r('app.media.startIcon'))
        .width(48)
        .height(48)
        .borderRadius(12)
        .shadow({ radius: 8, color: 'rgba(255,107,53,0.3)' })

      Column() {
        // 应用名称
        Text('龍魂AI')
          .fontSize(24)
          .fontWeight(FontWeight.Bold)
          .fontColor('#1A1A2E')
        // 版本号
        Text('v5.0 · HarmonyOS')
          .fontSize(12)
          .fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .margin({ left: 12 })

      Blank()

      // 设置按钮
      Button() {
        Image($r('app.media.startIcon'))
          .width(20)
          .height(20)
          .fillColor('#666')
      }
      .width(40)
      .height(40)
      .backgroundColor('#F0F0F0')
      .borderRadius(20)
      .onClick(() => {
        router.pushUrl({ url: 'pages/Settings' });
      })
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#FFFFFF')
  }

  // 功能卡片构建器
  @Builder
  功能卡片(数据: 功能卡片数据) {
    Column() {
      // 图标区域
      Row() {
        Image(数据.图标)
          .width(36)
          .height(36)
          .fillColor('#FFFFFF')
      }
      .width(60)
      .height(60)
      .backgroundColor(数据.颜色)
      .borderRadius(16)
      .justifyContent(FlexAlign.Center)
      .margin({ bottom: 12 })

      // 标题
      Text(数据.标题)
        .fontSize(16)
        .fontWeight(FontWeight.Medium)
        .fontColor('#1A1A2E')

      // 描述
      Text(数据.描述)
        .fontSize(12)
        .fontColor('#999')
        .margin({ top: 4 })
    }
    .width('100%')
    .height(140)
    .padding(16)
    .backgroundColor('#FFFFFF')
    .borderRadius(16)
    .shadow({ radius: 8, color: 'rgba(0,0,0,0.06)' })
    .justifyContent(FlexAlign.Center)
    .onClick(() => {
      // 页面导航
      router.pushUrl({
        url: 数据.页面,
        params: { from: '首页', title: 数据.标题 }
      }).catch((err: Error) => {
        console.error('导航失败:', err.message);
      });
    })
  }

  // 快捷操作栏构建
  @Builder
  快捷操作栏() {
    Row() {
      // DNA追溯快捷入口
      Column() {
        Image($r('app.media.startIcon'))
          .width(24)
          .height(24)
          .fillColor('#FF6B35')
        Text('DNA追溯')
          .fontSize(11)
          .fontColor('#666')
          .margin({ top: 4 })
      }
      .layoutWeight(1)
      .onClick(() => {
        // 显示DNA追溯弹窗
        this.显示DNA追溯();
      })

      // 分割线
      Divider()
        .vertical(true)
        .height(30)
        .color('#E0E0E0')

      // 君子协议状态
      Column() {
        Image($r('app.media.startIcon'))
          .width(24)
          .height(24)
          .fillColor(this.已签协议 ? '#4CAF50' : '#FF9800')
        Text(this.已签协议 ? '已签约' : '未签约')
          .fontSize(11)
          .fontColor(this.已签协议 ? '#4CAF50' : '#FF9800')
          .margin({ top: 4 })
      }
      .layoutWeight(1)
      .onClick(() => {
        if (!this.已签协议) {
          router.pushUrl({ url: 'pages/Settings' });
        }
      })

      // 分割线
      Divider()
        .vertical(true)
        .height(30)
        .color('#E0E0E0')

      // 治理框架
      Column() {
        Image($r('app.media.startIcon'))
          .width(24)
          .height(24)
          .fillColor('#45B7D1')
        Text('治理框架')
          .fontSize(11)
          .fontColor('#666')
          .margin({ top: 4 })
      }
      .layoutWeight(1)
      .onClick(() => {
        this.显示治理框架();
      })
    }
    .width('100%')
    .height(70)
    .padding(8)
    .backgroundColor('#FFFFFF')
    .borderRadius(16)
    .shadow({ radius: 8, color: 'rgba(0,0,0,0.06)' })
  }

  // 显示DNA追溯弹窗
  private 显示DNA追溯(): void {
    // DNA追溯信息展示
    AlertDialog.show({
      title: 'DNA追溯链',
      message:
        'DNA: #龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0\n' +
        '创始人: UID9622 · 龍芯北辰 · 诸葛鑫\n' +
        'GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F\n' +
        '六层治理: 作者层→团队层→社区层→AI自省→第三方审计→监管合规\n' +
        '君子协议: v5.0',
      confirm: {
        value: '确认',
        action: () => {
          console.log('DNA追溯已确认');
        }
      }
    });
  }

  // 显示治理框架弹窗
  private 显示治理框架(): void {
    AlertDialog.show({
      title: '龍魂六层治理框架',
      message:
        '第一层 · 作者层: 原创声明与签名\n' +
        '第二层 · 团队层: 内部代码审查\n' +
        '第三层 · 社区层: 开源社区监督\n' +
        '第四层 · AI自省层: 模型自审\n' +
        '第五层 · 第三方审计: 独立审计机构\n' +
        '第六层 · 监管合规: 法律法规遵循\n\n' +
        '铁律自审闸: 任何输出须过自检',
      confirm: {
        value: '确认',
        action: () => {}
      }
    });
  }

  build() {
    Column() {
      // 顶部Logo区域
      this.顶部Logo区()

      Scroll() {
        Column({ space: 16 }) {
          // 欢迎语
          Column() {
            Text($r('app.string.welcome'))
              .fontSize(20)
              .fontWeight(FontWeight.Bold)
              .fontColor('#1A1A2E')
              .margin({ top: 8 })

            Text('中文语义智能能力平台')
              .fontSize(14)
              .fontColor('#999')
              .margin({ top: 4, bottom: 8 })
          }
          .width('100%')
          .alignItems(HorizontalAlign.Start)
          .padding({ left: 16, right: 16 })

          // 快捷操作栏
          this.快捷操作栏()
            .padding({ left: 16, right: 16 })

          // 功能卡片网格
          Grid() {
            ForEach(this.功能列表, (item: 功能卡片数据, index: number) => {
              GridItem() {
                this.功能卡片(item)
              }
            }, (item: 功能卡片数据, index: number) => index.toString())
          }
          .columnsTemplate('1fr 1fr')
          .columnsGap(12)
          .rowsGap(12)
          .padding(16)
          .width('100%')

          // 特色能力展示
          Column({ space: 8 }) {
            Text('特色能力')
              .fontSize(18)
              .fontWeight(FontWeight.Bold)
              .fontColor('#1A1A2E')
              .width('100%')
              .textAlign(TextAlign.Start)

            // CNSH特色介绍
            Row() {
              Column() {
                Text('CNSH')
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#FF6B35')
                Text('Chinese Native Script for Harmony\n用中文关键字编写原生代码')
                  .fontSize(12)
                  .fontColor('#666')
                  .margin({ top: 4 })
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)
            }
            .width('100%')
            .padding(16)
            .backgroundColor('#FFF5F0')
            .borderRadius(12)

            // 通心译特色介绍
            Row() {
              Column() {
                Text('通心译 49术语')
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#4ECDC4')
                Text('跨语言精准翻译，保留文化语义\n支持中英日韩法等8种语言')
                  .fontSize(12)
                  .fontColor('#666')
                  .margin({ top: 4 })
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)
            }
            .width('100%')
            .padding(16)
            .backgroundColor('#F0FFFE')
            .borderRadius(12)

            // 三色审计特色介绍
            Row() {
              Column() {
                Text('三色审计')
                  .fontSize(16)
                  .fontWeight(FontWeight.Bold)
                  .fontColor('#45B7D1')
                Text('🟢通过 🟡警告 🔴违规\n六层来源链可追溯审计')
                  .fontSize(12)
                  .fontColor('#666')
                  .margin({ top: 4 })
              }
              .alignItems(HorizontalAlign.Start)
              .layoutWeight(1)
            }
            .width('100%')
            .padding(16)
            .backgroundColor('#F0FAFF')
            .borderRadius(12)
          }
          .padding({ left: 16, right: 16 })
          .width('100%')

          // 底部留白
          Blank()
            .height(20)
        }
        .width('100%')
      }
      .layoutWeight(1)
      .scrollBar(BarState.Off)

      // 底部DNA追溯栏 - 每个页面必须显示
      Column() {
        Text(this.dna码)
          .fontSize(10)
          .fontColor('#BBB')
        Text($r('app.string.founder_info'))
          .fontSize(9)
          .fontColor('#CCC')
          .margin({ top: 2 })
      }
      .width('100%')
      .padding(8)
      .backgroundColor('#FAFAFA')
      .border({ width: { top: 1 }, color: '#EEE' })
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }
}