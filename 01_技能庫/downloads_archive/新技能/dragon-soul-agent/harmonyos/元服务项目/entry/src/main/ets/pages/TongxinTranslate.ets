import { router } from '@kit.ArkUI';

// ============================================================
// 通心译翻译页面 - 49术语AI翻译系统
// DNA: #龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0
// 支持: 49核心术语翻译、语音输入/朗读、历史记录
// ============================================================

// 翻译结果数据模型
interface 翻译结果 {
  原文: string;
  译文: string;
  源语言: string;
  目标语言: string;
  术语解析: 术语条目[];
  时间戳: number;
}

// 术语条目
interface 术语条目 {
  术语: string;
  释义: string;
  类别: string;
  文化注释: string;
}

// 语言选项
interface 语言选项 {
  代码: string;
  名称: string;
  本地名称: string;
  图标: string;
}

@Entry
@Component
struct TongxinTranslate {
  // 状态变量
  @StorageLink('longhun_dna') dna码: string = '#龍芯⚡️2026-06-18-LONGHUN-HARMONYOS-v1.0';
  @State 输入文本: string = '';
  @State 翻译结果文本: string = '';
  @State 源语言: string = 'zh';
  @State 目标语言: string = 'en';
  @State 显示术语解析: boolean = true;
  @State 术语列表: 术语条目[] = [];
  @State 历史记录: 翻译结果[] = [];
  @State 正在翻译: boolean = false;
  @State 显示历史: boolean = false;

  // 支持的语言列表
  private 语言列表: 语言选项[] = [
    { 代码: 'zh', 名称: '中文', 本地名称: '中文', 图标: '🇨🇳' },
    { 代码: 'en', 名称: '英语', 本地名称: 'English', 图标: '🇬🇧' },
    { 代码: 'ja', 名称: '日语', 本地名称: '日本語', 图标: '🇯🇵' },
    { 代码: 'ko', 名称: '韩语', 本地名称: '한국어', 图标: '🇰🇷' },
    { 代码: 'fr', 名称: '法语', 本地名称: 'Français', 图标: '🇫🇷' },
    { 代码: 'es', 名称: '西班牙语', 本地名称: 'Español', 图标: '🇪🇸' },
    { 代码: 'de', 名称: '德语', 本地名称: 'Deutsch', 图标: '🇩🇪' },
    { 代码: 'ru', 名称: '俄语', 本地名称: 'Русский', 图标: '🇷🇺' }
  ];

  // 49核心术语知识库（简化版）
  private 核心术语库: Record<string, Record<string, string>> = {
    'zh-en': {
      '龍魂': 'Dragon Soul (Longhun)',
      '君子协议': 'Gentleman Agreement',
      '六层治理': 'Six-Layer Governance',
      '三色审计': 'Three-Color Audit',
      'DNA追溯': 'DNA Traceability',
      '通心译': 'Tongxin Translation',
      '铁律自审闸': 'Iron Gate Self-Audit',
      '来源链': 'Source Chain',
      'CNSH': 'CNSH (Chinese Native Script)',
      '母语编程': 'Native Language Programming',
      '中文语义': 'Chinese Semantic Intelligence',
      '语义能力': 'Semantic Capability',
      '审计': 'Audit',
      '追溯': 'Trace',
      '治理': 'Governance',
      '合规': 'Compliance',
      '变量': 'Variable',
      '函数': 'Function',
      '类': 'Class',
      '循环': 'Loop',
      '条件': 'Condition',
      '返回': 'Return',
      '打印': 'Print',
      '常量': 'Constant',
      '字典': 'Dictionary',
      '列表': 'List',
      '异步': 'Async',
      '等待': 'Await',
      ' HarmonyOS': 'HarmonyOS',
      '元服务': 'Meta Service',
      'Ability': 'Ability',
      'ArkTS': 'ArkTS'
    },
    'en-zh': {
      'HarmonyOS': '鸿蒙操作系统',
      'Meta Service': '元服务',
      'Ability': '能力组件',
      'ArkTS': '方舟TypeScript',
      'Stage Model': 'Stage模型',
      'Atomic Service': '原子化服务',
      'Super Device': '超级终端',
      'Distributed': '分布式',
      'Bundle': '应用包',
      'HAP': '鸿蒙 Ability 包',
      'HSP': '鸿蒙共享包',
      'Declarative UI': '声明式UI',
      'State Management': '状态管理',
      'LazyForEach': '懒加载遍历',
      'AppStorage': '应用存储',
      'LocalStorage': '本地存储',
      'PixelMap': '像素图',
      'Resource': '资源',
      'Component': '组件',
      'Custom Dialog': '自定义弹窗',
      'Navigation': '导航',
      'Stack': '栈',
      'Column': '纵向排列',
      'Row': '横向排列',
      'Flex': '弹性布局',
      'Grid': '网格',
      'List': '列表',
      'Swiper': '滑动视图'
    }
  };

  // 顶部导航栏
  @Builder
  导航栏() {
    Row() {
      Button() {
        Image($r('app.media.startIcon'))
          .width(20)
          .height(20)
          .fillColor('#666')
      }
      .width(36)
      .height(36)
      .backgroundColor('transparent')
      .onClick(() => {
        router.back();
      })

      Text('通心译 49术语')
        .fontSize(18)
        .fontWeight(FontWeight.Bold)
        .fontColor('#1A1A2E')
        .layoutWeight(1)
        .textAlign(TextAlign.Center)

      Button() {
        Image($r('app.media.startIcon'))
          .width(20)
          .height(20)
          .fillColor('#666')
      }
      .width(36)
      .height(36)
      .backgroundColor('transparent')
      .onClick(() => {
        router.pushUrl({ url: 'pages/Settings' });
      })
    }
    .width('100%')
    .height(56)
    .padding({ left: 8, right: 8 })
    .backgroundColor('#FFFFFF')
  }

  // 语言选择栏
  @Builder
  语言选择栏() {
    Row() {
      // 源语言选择
      Button(this.获取语言名称(this.源语言))
        .fontSize(14)
        .fontColor('#333')
        .backgroundColor('#F0F0F0')
        .height(36)
        .onClick(() => {
          this.显示语言选择器(true);
        })

      // 交换按钮
      Button('⇄') {
        Image($r('app.media.startIcon'))
          .width(20)
          .height(20)
          .fillColor('#666')
      }
      .width(36)
      .height(36)
      .backgroundColor('transparent')
      .onClick(() => {
        // 交换源语言和目标语言
        const 临时 = this.源语言;
        this.源语言 = this.目标语言;
        this.目标语言 = 临时;
      })

      // 目标语言选择
      Button(this.获取语言名称(this.目标语言))
        .fontSize(14)
        .fontColor('#333')
        .backgroundColor('#F0F0F0')
        .height(36)
        .onClick(() => {
          this.显示语言选择器(false);
        })
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#FFFFFF')
    .border({ width: { bottom: 1 }, color: '#EEE' })
    .justifyContent(FlexAlign.SpaceEvenly)
  }

  // 输入区域
  @Builder
  输入区域() {
    Column() {
      Stack({ alignContent: Alignment.BottomEnd }) {
        TextArea({
          placeholder: $r('app.string.input_placeholder_translate'),
          text: $$this.输入文本
        })
          .width('100%')
          .height(120)
          .backgroundColor('#F8F8F8')
          .fontColor('#333')
          .fontSize(15)
          .padding(12)
          .placeholderColor('#999')

        // 语音输入按钮
        Button() {
          Image($r('app.media.startIcon'))
            .width(22)
            .height(22)
            .fillColor('#4ECDC4')
        }
        .width(40)
        .height(40)
        .backgroundColor('#FFFFFF')
        .borderRadius(20)
        .shadow({ radius: 4, color: 'rgba(0,0,0,0.1)' })
        .margin({ right: 8, bottom: 8 })
        .onClick(() => {
          this.启动语音输入();
        })
      }
      .width('100%')

      // 操作按钮行
      Row({ space: 8 }) {
        Button('翻译')
          .fontSize(14)
          .fontColor('#FFFFFF')
          .backgroundColor('#4ECDC4')
          .height(38)
          .layoutWeight(1)
          .onClick(() => {
            this.执行翻译();
          })

        Button('清空')
          .fontSize(14)
          .fontColor('#666')
          .backgroundColor('#F0F0F0')
          .height(38)
          .onClick(() => {
            this.输入文本 = '';
            this.翻译结果文本 = '';
            this.术语列表 = [];
          })

        Button('历史')
          .fontSize(14)
          .fontColor('#666')
          .backgroundColor('#F0F0F0')
          .height(38)
          .onClick(() => {
            this.显示历史 = !this.显示历史;
          })
      }
      .width('100%')
      .padding(12)
    }
    .width('100%')
    .backgroundColor('#FFFFFF')
    .borderRadius(12)
    .margin({ top: 12, left: 12, right: 12 })
  }

  // 翻译结果区域
  @Builder
  翻译结果区() {
    if (this.翻译结果文本.length > 0) {
      Column({ space: 8 }) {
        // 翻译文本
        Column() {
          Row() {
            Text('翻译结果')
              .fontSize(14)
              .fontWeight(FontWeight.Medium)
              .fontColor('#666')

            Blank()

            // 语音朗读按钮
            Button() {
              Image($r('app.media.startIcon'))
                .width(18)
                .height(18)
                .fillColor('#4ECDC4')
            }
            .width(32)
            .height(32)
            .backgroundColor('transparent')
            .onClick(() => {
              this.语音朗读(this.翻译结果文本);
            })

            // 复制按钮
            Button() {
              Image($r('app.media.startIcon'))
                .width(18)
                .height(18)
                .fillColor('#666')
            }
            .width(32)
            .height(32)
            .backgroundColor('transparent')
            .onClick(() => {
              // 复制到剪贴板
              this.复制文本(this.翻译结果文本);
            })
          }
          .width('100%')

          Text(this.翻译结果文本)
            .fontSize(16)
            .fontColor('#1A1A2E')
            .width('100%')
            .margin({ top: 8 })
            .textAlign(TextAlign.Start)
        }
        .width('100%')
        .padding(16)
        .backgroundColor('#F0FFFE')
        .borderRadius(12)

        // 术语解析卡片
        if (this.显示术语解析 && this.术语列表.length > 0) {
          Column() {
            Text('术语解析')
              .fontSize(14)
              .fontWeight(FontWeight.Medium)
              .fontColor('#666')
              .width('100%')
              .margin({ bottom: 8 })

            ForEach(this.术语列表, (术语: 术语条目, 索引: number) => {
              this.术语卡片(术语)
            }, (术语: 术语条目, 索引: number) => 索引.toString())
          }
          .width('100%')
          .padding(16)
          .backgroundColor('#FFFFFF')
          .borderRadius(12)
          .shadow({ radius: 4, color: 'rgba(0,0,0,0.05)' })
        }
      }
      .width('100%')
      .padding({ left: 12, right: 12 })
      .margin({ top: 12 })
    }
  }

  // 术语解析卡片
  @Builder
  术语卡片(术语: 术语条目) {
    Column() {
      Row() {
        // 术语标签
        Text(术语.术语)
          .fontSize(13)
          .fontWeight(FontWeight.Bold)
          .fontColor('#4ECDC4')
          .padding({ left: 8, right: 8, top: 2, bottom: 2 })
          .backgroundColor('#E8F8F6')
          .borderRadius(4)

        Blank()

        // 类别标签
        Text(术语.类别)
          .fontSize(11)
          .fontColor('#999')
      }
      .width('100%')

      Text(术语.释义)
        .fontSize(13)
        .fontColor('#333')
        .width('100%')
        .margin({ top: 4 })

      if (术语.文化注释.length > 0) {
        Text('📝 ' + 术语.文化注释)
          .fontSize(11)
          .fontColor('#FF9800')
          .width('100%')
          .margin({ top: 4 })
      }
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#FAFAFA')
    .borderRadius(8)
    .margin({ top: 8 })
  }

  // 历史记录区域
  @Builder
  历史记录区() {
    if (this.显示历史 && this.历史记录.length > 0) {
      Column() {
        Row() {
          Text('翻译历史')
            .fontSize(14)
            .fontWeight(FontWeight.Medium)
            .fontColor('#666')
          Blank()
          Button('清空历史')
            .fontSize(12)
            .height(28)
            .backgroundColor('#F5F5F5')
            .fontColor('#999')
            .onClick(() => {
              this.历史记录 = [];
            })
        }
        .width('100%')
        .margin({ bottom: 8 })

        List({ space: 8 }) {
          ForEach(this.历史记录, (记录: 翻译结果, 索引: number) => {
            ListItem() {
              Column() {
                Text(记录.原文)
                  .fontSize(13)
                  .fontColor('#666')
                  .width('100%')
                  .maxLines(1)
                  .textOverflow({ overflow: TextOverflow.Ellipsis })

                Text(记录.译文)
                  .fontSize(14)
                  .fontColor('#1A1A2E')
                  .width('100%')
                  .margin({ top: 4 })
                  .maxLines(2)
                  .textOverflow({ overflow: TextOverflow.Ellipsis })

                Text(this.格式化时间(记录.时间戳))
                  .fontSize(10)
                  .fontColor('#CCC')
                  .width('100%')
                  .textAlign(TextAlign.End)
              }
              .width('100%')
              .padding(12)
              .backgroundColor('#F8F8F8')
              .borderRadius(8)
            }
            .onClick(() => {
              this.输入文本 = 记录.原文;
              this.翻译结果文本 = 记录.译文;
              this.显示历史 = false;
            })
          }, (记录: 翻译结果, 索引: number) => 索引.toString())
        }
        .width('100%')
        .height(200)
      }
      .width('100%')
      .padding({ left: 12, right: 12 })
      .margin({ top: 12 })
    }
  }

  // 底部DNA栏
  @Builder
  底部DNA栏() {
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

  // 获取语言名称
  private 获取语言名称(代码: string): string {
    const 语言 = this.语言列表.find(l => l.代码 === 代码);
    return 语言 ? 语言.名称 : 代码;
  }

  // 显示语言选择器
  private 显示语言选择器(是源语言: boolean): void {
    // 简化版: 直接切换几个主要语言
    AlertDialog.show({
      title: 是源语言 ? '选择源语言' : '选择目标语言',
      message: '🇨🇳 中文\n🇬🇧 English\n🇯🇵 日本語\n🇰🇷 한국어\n🇫🇷 Français',
      confirm: {
        value: '确认',
        action: () => {}
      }
    });
  }

  // 执行翻译
  private 执行翻译(): void {
    if (!this.输入文本 || this.输入文本.trim().length === 0) {
      return;
    }

    this.正在翻译 = true;

    // 模拟翻译过程
    const 方向 = `${this.源语言}-${this.目标语言}`;
    let 结果 = '';
    const 解析术语: 术语条目[] = [];

    // 检查核心术语库
    const 术语库 = this.核心术语库[方向] || this.核心术语库['zh-en'];

    if (术语库) {
      // 查找匹配的术语
      for (const [中文, 外文] of Object.entries(术语库)) {
        if (this.输入文本.includes(中文)) {
          解析术语.push({
            术语: 中文,
            释义: 外文,
            类别: this.获取术语类别(中文),
            文化注释: this.获取文化注释(中文)
          });
        }
      }

      // 构建翻译结果
      if (解析术语.length > 0) {
        结果 = this.构建翻译结果(this.输入文本, 解析术语, 方向);
      } else {
        // 使用简单翻译模拟
        结果 = this.模拟通用翻译(this.输入文本, 方向);
      }
    } else {
      结果 = `[通心译] ${this.获取语言名称(this.源语言)} → ${this.获取语言名称(this.目标语言)}\n\n${this.输入文本}\n\n[通用翻译结果]\n${this.输入文本}`;
    }

    this.翻译结果文本 = 结果;
    this.术语列表 = 解析术语;
    this.正在翻译 = false;

    // 添加到历史记录
    this.历史记录.unshift({
      原文: this.输入文本,
      译文: 结果,
      源语言: this.源语言,
      目标语言: this.目标语言,
      术语解析: 解析术语,
      时间戳: Date.now()
    });

    // 限制历史记录数量
    if (this.历史记录.length > 20) {
      this.历史记录 = this.历史记录.slice(0, 20);
    }
  }

  // 获取术语类别
  private 获取术语类别(术语: string): string {
    const 技术术语 = ['CNSH', 'HarmonyOS', '元服务', 'Ability', 'ArkTS', '变量', '函数', '类', '循环'];
    const 治理术语 = ['君子协议', '六层治理', '三色审计', 'DNA追溯', '铁律自审闸', '来源链'];
    const 产品术语 = ['龍魂', '通心译', '中文语义', '母语编程', '语义能力'];

    if (技术术语.includes(术语)) return '技术术语';
    if (治理术语.includes(术语)) return '治理术语';
    if (产品术语.includes(术语)) return '产品术语';
    return '通用术语';
  }

  // 获取文化注释
  private 获取文化注释(术语: string): string {
    const 注释: Record<string, string> = {
      '龍魂': '龍在中国文化中代表尊贵与力量，魂代表精神内核',
      '君子协议': '源自中国传统文化中"君子"的诚信精神',
      '通心译': '"通心"意为心意相通，追求跨语言的心领神会',
      '六层治理': '借鉴中国传统建筑的六层结构理念',
      '铁律自审闸': '借鉴中国古代关隘闸门的审查机制'
    };
    return 注释[术语] || '';
  }

  // 构建翻译结果
  private 构建翻译结果(原文: string, 术语: 术语条目[], 方向: string): string {
    let 结果 = `[通心译 49术语] ${this.获取语言名称(this.源语言)} → ${this.获取语言名称(this.目标语言)}\n`;
    结果 += '━━━━━━━━━━━━━━━━━━━━\n';
    结果 += '【原文】\n' + 原文 + '\n\n';
    结果 += '【译文】\n';

    // 替换术语
    let 译文 = 原文;
    for (const 条目 of 术语) {
      译文 = 译文.replace(
        new RegExp(条目.术语, 'g'),
        `${条目.释义}`
      );
    }
    结果 += 译文 + '\n\n';
    结果 += `【识别术语 ${术语.length} 个】\n`;
    术语.forEach((条目, 索引) => {
      结果 += `${索引 + 1}. ${条目.术语} → ${条目.释义}\n`;
    });

    return 结果;
  }

  // 模拟通用翻译
  private 模拟通用翻译(文本: string, 方向: string): string {
    const 目标 = this.获取语言名称(this.目标语言);
    return `[通心译] 翻译至${目标}\n\n${文本}\n\n[通用翻译模式 - 术语库匹配中...]`;
  }

  // 启动语音输入
  private 启动语音输入(): void {
    AlertDialog.show({
      title: '语音输入',
      message: '请说出您要翻译的内容...\n\n支持: 中文、英语、日语、韩语',
      confirm: {
        value: '结束录音',
        action: () => {
          this.输入文本 = '你好，龍魂AI';
        }
      }
    });
  }

  // 语音朗读
  private 语音朗读(文本: string): void {
    // 模拟TTS
    console.log(`[TTS] 朗读: ${文本.substring(0, 50)}...`);
  }

  // 复制文本
  private 复制文本(文本: string): void {
    console.log(`[剪贴板] 已复制: ${文本.substring(0, 30)}...`);
  }

  // 格式化时间
  private 格式化时间(时间戳: number): string {
    const 日期 = new Date(时间戳);
    return `${日期.getHours().toString().padStart(2, '0')}:${日期.getMinutes().toString().padStart(2, '0')}`;
  }

  build() {
    Column() {
      // 顶部导航栏
      this.导航栏()

      // 语言选择栏
      this.语言选择栏()

      Scroll() {
        Column() {
          // 输入区域
          this.输入区域()

          // 翻译结果
          this.翻译结果区()

          // 历史记录
          this.历史记录区()

          // 底部留白
          Blank()
            .height(20)
        }
        .width('100%')
      }
      .layoutWeight(1)
      .scrollBar(BarState.Off)

      // 底部DNA栏
      this.底部DNA栏()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#F5F5F5')
  }
}