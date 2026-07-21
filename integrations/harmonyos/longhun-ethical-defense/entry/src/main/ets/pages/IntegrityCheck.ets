// entry/src/main/ets/pages/IntegrityCheck.ets
// 龍魂 · 商业诚信检测控制台 · 反虚假营销·反套路消费·反信息牢房
// DNA: #龍芯⚡️丙午·辛未·丙戌·INTEGRITY-PAGE-v1.0
// UID: 9622 | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

import {
  integrityDetector, IntegrityReport, AnomalyRecord,
  FraudType, AnomalySeverity, IntegrityLevel, ProductInspection,
  CommercePlatform
} from '../engines/IntegrityDetector';
import {
  integrityCircuitBreaker, BreakerDisplay, BreakerLabelLevel,
  BreakerHistoryRecord, SellerIntegrityProfile
} from '../services/IntegrityCircuitBreaker';

// ============================================================
//  诚信检测主页面
// ============================================================

@Entry
@Component
struct IntegrityCheckPage {
  // 输入状态
  @State private inputText: string = '';
  @State private inputUrl: string = '';
  @State private selectedPlatform: string = '抖音';

  // 检测状态
  @State private checking: boolean = false;
  @State private currentResult: BreakerDisplay | null = null;

  // 历史
  @State private history: BreakerHistoryRecord[] = [];
  @State private showHistory: boolean = false;

  // 统计
  @State private todayStats = { inspections: 0, blackFlags: 0, elderlyAlerts: 0 };
  @State private overallStats = { totalInspections: 0, totalBlackFlags: 0, elderlyScamsDetected: 0 };

  // 标签页
  @State private activeTab: number = 0; // 0:检测 1:历史 2:商家 3:统计

  private readonly tabTitles: string[] = ['检测', '历史', '商家', '统计'];
  private readonly platforms: string[] = ['抖音', '快手', '淘宝', '京东', '拼多多', '小红书', '微信视频号', 'B站', '其他'];

  private readonly MASTER_UID: string = '9622';

  aboutToAppear(): void {
    this.refreshData();
  }

  refreshData(): void {
    this.history = integrityCircuitBreaker.getHistory(20);
    this.todayStats = integrityCircuitBreaker.getTodayStats();
    this.overallStats = integrityCircuitBreaker.getStats();
  }

  build() {
    Column() {
      this.HeaderBuilder()
      this.TabBarBuilder()

      if (this.activeTab === 0) {
        this.DetectTab()
      } else if (this.activeTab === 1) {
        this.HistoryTab()
      } else if (this.activeTab === 2) {
        this.SellerTab()
      } else {
        this.StatsTab()
      }

      this.FooterBuilder()
    }
    .width('100%')
    .height('100%')
    .backgroundColor('#0a0a0a')
  }

  // ============================================================
  //  顶部标题栏
  // ============================================================

  @Builder
  HeaderBuilder() {
    Row() {
      Text('🐉').fontSize(28).margin({ right: 10 })

      Column() {
        Text('龍魂诚信检测').fontSize(22).fontWeight(FontWeight.Bold).fontColor('#c41e3a')
        Text('反虚假营销 · 反套路消费 · 反信息牢房').fontSize(11).fontColor('#666')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      // 今日统计摘要
      Row() {
        Column() {
          Text(`${this.todayStats.inspections}`).fontSize(18).fontWeight(FontWeight.Bold).fontColor('#fff')
          Text('今日检测').fontSize(10).fontColor('#666')
        }
        .margin({ right: 12 })

        Column() {
          Text(`${this.todayStats.blackFlags}`).fontSize(18).fontWeight(FontWeight.Bold)
            .fontColor(this.todayStats.blackFlags > 0 ? '#ff2244' : '#00cc66')
          Text('欺诈标记').fontSize(10).fontColor('#666')
        }
        .margin({ right: 12 })

        Column() {
          Text(`${this.todayStats.elderlyAlerts}`).fontSize(18).fontWeight(FontWeight.Bold)
            .fontColor(this.todayStats.elderlyAlerts > 0 ? '#ff8800' : '#00cc66')
          Text('老人预警').fontSize(10).fontColor('#666')
        }
      }
    }
    .width('100%')
    .height(56)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#111111')
    .border({ width: { bottom: 1 }, color: '#222' })
  }

  // ============================================================
  //  标签栏
  // ============================================================

  @Builder
  TabBarBuilder() {
    Row() {
      ForEach(this.tabTitles, (title: string, index: number) => {
        Text(title)
          .fontSize(14)
          .fontColor(this.activeTab === index ? '#c41e3a' : '#888')
          .fontWeight(this.activeTab === index ? FontWeight.Bold : FontWeight.Normal)
          .padding({ left: 16, right: 16, top: 10, bottom: 8 })
          .border({ width: { bottom: 2 }, color: this.activeTab === index ? '#c41e3a' : 'transparent' })
          .onClick(() => { this.activeTab = index; this.refreshData(); })
      })
    }
    .width('100%')
    .backgroundColor('#111111')
    .border({ width: { bottom: 1 }, color: '#222' })
  }

  // ============================================================
  //  检测标签页
  // ============================================================

  @Builder
  DetectTab() {
    Scroll() {
      Column() {
        this.InputSection()

        if (this.checking) {
          this.LoadingSection()
        }

        if (this.currentResult) {
          this.ResultSection()
        }
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
  }

  // 输入区
  @Builder
  InputSection() {
    Column() {
      // 平台选择
      Row() {
        Text('平台').fontSize(13).fontColor('#888').width(40)
        Scroll() {
          Row() {
            ForEach(this.platforms, (p: string) => {
              Text(p)
                .fontSize(12)
                .fontColor(this.selectedPlatform === p ? '#fff' : '#888')
                .backgroundColor(this.selectedPlatform === p ? '#c41e3a' : '#1a1a1a')
                .borderRadius(14)
                .padding({ left: 12, right: 12, top: 4, bottom: 4 })
                .margin({ right: 6 })
                .onClick(() => { this.selectedPlatform = p; })
            })
          }
          .padding({ top: 4, bottom: 4 })
        }
        .layoutWeight(1)
      }
      .width('100%')
      .margin({ bottom: 10 })

      // 文案输入
      Text('粘贴商品文案或主播话术')
        .fontSize(13).fontColor('#fff').width('100%').margin({ bottom: 8 })

      TextArea({ text: $$this.inputText, placeholder: '粘贴商品描述、直播话术、营销文案...' })
        .width('100%').height(100)
        .fontSize(13).fontColor('#fff').placeholderColor('#555')
        .backgroundColor('#1a1a1a').borderRadius(8).padding(12)

      // URL输入
      Text('或粘贴商品链接').fontSize(13).fontColor('#aaa').width('100%')
        .margin({ top: 12, bottom: 8 })

      TextInput({ text: $$this.inputUrl, placeholder: '粘贴商品链接(抖音/淘宝/京东/拼多多...)' })
        .width('100%').height(40)
        .fontSize(13).fontColor('#fff').placeholderColor('#555')
        .backgroundColor('#1a1a1a').borderRadius(8).padding({ left: 12, right: 12 })

      // 检测按钮
      Button(this.checking ? '⚡ 检测中...' : '🔍 开始诚信检测')
        .width('100%').height(46)
        .fontSize(15).fontWeight(FontWeight.Bold).fontColor('#fff')
        .backgroundColor(this.checking ? '#333' : '#c41e3a')
        .borderRadius(10).margin({ top: 14 })
        .enabled(!this.checking)
        .onClick(() => { this.runDetection(); })

      // 红线提示
      Text('⚖️ 只检测 · 只标注 · 只提醒 · 用户自判断 · 不封号不删帖')
        .fontSize(11).fontColor('#555')
        .width('100%').textAlign(TextAlign.Center).margin({ top: 8 })
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#111111')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }

  // 加载中
  @Builder
  LoadingSection() {
    Column() {
      LoadingProgress().width(40).height(40).color('#c41e3a')
      Text('正在检测...').fontSize(13).fontColor('#888').margin({ top: 8 })
    }
    .width('100%')
    .padding(24)
    .backgroundColor('#111111')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }

  // 检测结果
  @Builder
  ResultSection() {
    if (!this.currentResult) return;

    Column() {
      // 等级卡片
      Row() {
        Text(this.currentResult.labelIcon).fontSize(36).margin({ right: 12 })
        Column() {
          Text(this.currentResult.label)
            .fontSize(22).fontWeight(FontWeight.Bold)
            .fontColor(this.currentResult.color)
          Text(`诚信分: ${this.currentResult.trustScore}/100`)
            .fontSize(14).fontColor(this.currentResult.color).margin({ top: 4 })
        }
        .alignItems(HorizontalAlign.Start)
        .layoutWeight(1)

        Column() {
          Text(`等级 ${this.currentResult.integrityLevel}`)
            .fontSize(28).fontWeight(FontWeight.Bold)
            .fontColor(this.currentResult.color)
        }
        .alignItems(HorizontalAlign.End)
      }
      .width('100%')
      .padding(16)
      .backgroundColor(this.currentResult.bgColor)
      .border({ width: 1, color: this.currentResult.color, style: BorderStyle.Dashed })
      .borderRadius(12)

      // 官方认证
      Row() {
        if (this.currentResult.officialCert) {
          Text('✓ 官方认证标识有效')
            .fontSize(12).fontColor('#00cc66')
        } else {
          Text('✗ 未检测到有效的官方认证')
            .fontSize(12).fontColor('#ffcc00')
        }
      }
      .width('100%')
      .padding({ left: 12, right: 12, top: 8, bottom: 8 })
      .backgroundColor(this.currentResult.officialCert ? 'rgba(0,204,102,0.06)' : 'rgba(255,204,0,0.06)')
      .borderRadius(6)
      .margin({ top: 12 })

      // 异常列表
      if (this.currentResult.anomalies.length > 0) {
        Column() {
          Text(`检测到 ${this.currentResult.anomalies.length} 项异常`)
            .fontSize(15).fontWeight(FontWeight.Bold).fontColor('#fff')
            .width('100%').margin({ bottom: 10 })

          ForEach(this.currentResult.anomalies, (anomaly: AnomalyRecord) => {
            this.AnomalyCard(anomaly)
          })
        }
        .width('100%')
        .margin({ top: 12 })
      } else {
        Row() {
          Text('✓').fontSize(16).fontColor('#00cc66').margin({ right: 8 })
          Text('未发现诚信异常，该商品通过14维度检测').fontSize(13).fontColor('#00cc66')
        }
        .width('100%')
        .padding(12)
        .backgroundColor('rgba(0,204,102,0.06)')
        .borderRadius(8)
        .margin({ top: 12 })
      }

      // 建议
      Text('💡 消费建议')
        .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#fff')
        .width('100%').margin({ top: 16, bottom: 8 })

      Text(this.currentResult.recommendation)
        .fontSize(13).fontColor('#ccc')
        .width('100%')
        .padding(14)
        .backgroundColor('#111111')
        .borderRadius(8)
    }
    .width('100%')
    .padding(16)
    .backgroundColor('#111111')
    .borderRadius(12)
    .margin({ bottom: 12 })
  }

  // 单条异常卡片
  @Builder
  AnomalyCard(anomaly: AnomalyRecord) {
    Column() {
      Row() {
        Text(this.getAnomalyIcon(anomaly.severity)).fontSize(16).margin({ right: 8 })
        Text(this.getFraudTypeName(anomaly.type))
          .fontSize(14).fontWeight(FontWeight.Medium).fontColor('#fff')
          .layoutWeight(1)

        Text(this.getSeverityLabel(anomaly.severity))
          .fontSize(10).fontColor(this.getSeverityColor(anomaly.severity))
          .backgroundColor('rgba(255,255,255,0.05)')
          .borderRadius(4)
          .padding({ left: 6, right: 6, top: 2, bottom: 2 })
      }
      .width('100%')

      Text(anomaly.evidence)
        .fontSize(12).fontColor('#999')
        .width('100%').margin({ top: 6 })

      Row() {
        Text('💡').fontSize(12).margin({ right: 4 })
        Text(anomaly.suggestion)
          .fontSize(11).fontColor('#c41e3a')
          .layoutWeight(1)
      }
      .width('100%').margin({ top: 4 })
    }
    .width('100%')
    .padding(12)
    .backgroundColor('#1a1a1a')
    .border({ width: { left: 3 }, color: this.getSeverityColor(anomaly.severity) })
    .borderRadius(6)
    .margin({ bottom: 8 })
  }

  // ============================================================
  //  历史标签页
  // ============================================================

  @Builder
  HistoryTab() {
    Column() {
      // 筛选
      Row() {
        Text('检测历史').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff')
          .layoutWeight(1)

        Text(`共 ${this.overallStats.totalInspections} 条`)
          .fontSize(12).fontColor('#666')
      }
      .width('100%')
      .padding({ left: 16, right: 16, top: 12, bottom: 8 })

      // 高风险筛选按钮
      Row() {
        FilterChip('全部', '')
        FilterChip('🚫 高风险', 'red')
        FilterChip('⛔ 欺诈', 'black')
      }
      .width('100%')
      .padding({ left: 16, right: 16, bottom: 8 })

      // 列表
      if (this.history.length === 0) {
        Column() {
          Text('📭').fontSize(40).margin({ bottom: 8 })
          Text('暂无检测记录').fontSize(14).fontColor('#666')
          Text('输入商品链接或文案开始检测').fontSize(12).fontColor('#444')
        }
        .width('100%').height(200)
        .justifyContent(FlexAlign.Center)
      } else {
        List() {
          ForEach(this.history, (record: BreakerHistoryRecord) => {
            ListItem() {
              this.HistoryCard(record)
            }
          })
        }
        .width('100%')
        .layoutWeight(1)
      }
    }
    .width('100%')
    .layoutWeight(1)
  }

  @Builder
  HistoryCard(record: BreakerHistoryRecord) {
    Row() {
      // 等级色条
      Column()
        .width(4).height('100%')
        .backgroundColor(record.color)
        .borderRadius(2)

      Column() {
        Row() {
          Text(record.labelIcon).fontSize(14).margin({ right: 6 })
          Text(record.label)
            .fontSize(13).fontWeight(FontWeight.Bold).fontColor(record.color)
            .layoutWeight(1)
          Text(`${record.trustScore}分`)
            .fontSize(14).fontWeight(FontWeight.Bold).fontColor(record.color)
        }
        .width('100%')

        Row() {
          Text(record.productName || record.productId)
            .fontSize(12).fontColor('#888')
            .layoutWeight(1).maxLines(1).textOverflow({ overflow: TextOverflow.Ellipsis })
          Text(record.platform)
            .fontSize(10).fontColor('#555')
            .backgroundColor('rgba(255,255,255,0.03)')
            .borderRadius(4)
            .padding({ left: 6, right: 6, top: 2, bottom: 2 })
        }
        .width('100%').margin({ top: 4 })

        if (record.sellerName !== '未知') {
          Text(`商家: ${record.sellerName}`)
            .fontSize(10).fontColor('#555')
            .margin({ top: 2 })
        }

        Text(new Date(record.timestamp).toLocaleString())
          .fontSize(9).fontColor('#444')
          .margin({ top: 2 })
      }
      .layoutWeight(1)
      .padding(12)
    }
    .width('100%')
    .backgroundColor('#111111')
    .borderRadius(8)
    .margin({ left: 12, right: 12, bottom: 6 })
  }

  // ============================================================
  //  商家标签页
  // ============================================================

  @Builder
  SellerTab() {
    Column() {
      Text('商家诚信档案').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff')
        .width('100%').padding({ left: 16, right: 16, top: 12, bottom: 8 })

      List() {
        ForEach(integrityCircuitBreaker.getAllSellerProfiles().slice(0, 20), (profile: SellerIntegrityProfile) => {
          ListItem() {
            this.SellerCard(profile)
          }
        })
      }
      .width('100%')
      .layoutWeight(1)
    }
    .width('100%')
    .layoutWeight(1)
  }

  @Builder
  SellerCard(profile: SellerIntegrityProfile) {
    Row() {
      Column()
        .width(4).height('100%')
        .backgroundColor(this.getSellerWorstColor(profile.worstLevel))
        .borderRadius(2)

      Column() {
        Row() {
          Text(profile.sellerName || profile.sellerId)
            .fontSize(14).fontWeight(FontWeight.Bold).fontColor('#fff')
            .layoutWeight(1)

          if (profile.blacklistFlag) {
            Text('⛔ 黑名单').fontSize(10).fontColor('#ff0000')
              .backgroundColor('rgba(255,0,0,0.1)')
              .borderRadius(4)
              .padding({ left: 6, right: 6, top: 2, bottom: 2 })
          } else if (profile.warningFlag) {
            Text('⚠️ 预警').fontSize(10).fontColor('#ff8800')
              .backgroundColor('rgba(255,136,0,0.1)')
              .borderRadius(4)
              .padding({ left: 6, right: 6, top: 2, bottom: 2 })
          }
        }
        .width('100%')

        Row() {
          Text(`检测${profile.totalInspections}次`)
            .fontSize(11).fontColor('#888').margin({ right: 10 })
          Text(`均分${profile.averageTrustScore}`)
            .fontSize(11).fontColor('#888').margin({ right: 10 })
          Text(`最差${profile.worstLevel}`)
            .fontSize(11).fontColor(this.getSellerWorstColor(profile.worstLevel))
        }
        .width('100%').margin({ top: 4 })

        // 等级分布条
        Row() {
          Bar('绿', profile.greenCount, profile.totalInspections, '#00cc66')
          Bar('黄', profile.yellowCount, profile.totalInspections, '#ffcc00')
          Bar('橙', profile.orangeCount, profile.totalInspections, '#ff8800')
          Bar('红', profile.redCount, profile.totalInspections, '#ff2244')
          Bar('黑', profile.blackCount, profile.totalInspections, '#000')
        }
        .width('100%').height(6).margin({ top: 6 })
        .borderRadius(3)
      }
      .layoutWeight(1)
      .padding(12)
    }
    .width('100%')
    .backgroundColor('#111111')
    .borderRadius(8)
    .margin({ left: 12, right: 12, bottom: 6 })
  }

  // ============================================================
  //  统计标签页
  // ============================================================

  @Builder
  StatsTab() {
    Scroll() {
      Column() {
        // 总体统计
        Text('检测概览').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#fff')
          .width('100%').margin({ bottom: 10 })

        Row() {
          StatCard('总检测数', `${this.overallStats.totalInspections}`, '#00cc66')
          StatCard('欺诈标记', `${this.overallStats.totalBlackFlags}`, '#ff2244')
          StatCard('老人预警', `${this.overallStats.elderlyScamsDetected}`, '#ff8800')
          StatCard('异常总数', `${this.overallStats.totalAnomaliesDetected}`, '#ffcc00')
        }
        .width('100%')
        .justifyContent(FlexAlign.SpaceBetween)
        .margin({ bottom: 16 })

        // 高风险商家
        Text('高风险商家').fontSize(16).fontWeight(FontWeight.Bold).fontColor('#ff2244')
          .width('100%').margin({ top: 8, bottom: 10 })

        ForEach(integrityCircuitBreaker.getHighRiskSellers().slice(0, 5), (profile: SellerIntegrityProfile) => {
          this.SellerCard(profile)
        })
      }
      .width('100%')
      .padding(16)
    }
    .width('100%')
    .layoutWeight(1)
  }

  @Builder
  StatCard(label: string, value: string, color: string) {
    Column() {
      Text(value).fontSize(24).fontWeight(FontWeight.Bold).fontColor(color)
      Text(label).fontSize(11).fontColor('#888')
    }
    .width('23%')
    .padding(10)
    .backgroundColor('rgba(255,255,255,0.03)')
    .borderRadius(8)
  }

  @Builder
  StatBar(label: string, value: number, total: number, color: string) {
    Row() {
      Text(label).fontSize(10).fontColor('#888').width(20)
      Column()
        .width(`${(value / Math.max(total, 1)) * 100}%`)
        .height('100%')
        .backgroundColor(color)
    }
    .width('100%').height(6)
    .backgroundColor('#333')
    .borderRadius(3)
  }

  // ============================================================
  //  底部
  // ============================================================

  @Builder
  FooterBuilder() {
    Row() {
      Column() {
        Text('🐉').fontSize(16)
        Text(`UID:${this.MASTER_UID}`).fontSize(9).fontColor('#555')
      }
      .alignItems(HorizontalAlign.Start)
      .layoutWeight(1)

      Column() {
        Text('只检测 · 只标注 · 用户自判断').fontSize(10).fontColor('#555')
        Text('不封号 · 不删帖 · 不替平台决策').fontSize(10).fontColor('#444')
      }
      .alignItems(HorizontalAlign.End)
    }
    .width('100%')
    .height(42)
    .padding({ left: 16, right: 16 })
    .backgroundColor('#111111')
    .border({ width: { top: 1 }, color: '#222' })
  }

  // ============================================================
  //  检测执行
  // ============================================================

  async runDetection(): Promise<void> {
    const text = this.inputText.trim();
    const url = this.inputUrl.trim();
    if (!text && !url) return;

    this.checking = true;
    this.currentResult = null;

    try {
      // 构造检测输入
      const product: ProductInspection = this.buildProductInspection(text, url);

      // 执行检测
      const report: IntegrityReport = await integrityDetector.inspect(product);

      // 熔断标注
      const display: BreakerDisplay = await integrityCircuitBreaker.break(report, product);

      this.currentResult = display;
      this.refreshData();

    } catch (e) {
      console.error('[龍魂·诚信检测] 检测失败:', e);
    } finally {
      this.checking = false;
    }
  }

  private buildProductInspection(text: string, url: string): ProductInspection {
    // 解析URL获取平台和商品ID（实际应联网解析）
    let platform: CommercePlatform = CommercePlatform.OTHER;
    let productId = `PROD-${Date.now()}`;
    let productName = '待检测商品';

    if (url) {
      if (url.includes('douyin.com')) platform = CommercePlatform.DOUYIN;
      else if (url.includes('kuaishou.com')) platform = CommercePlatform.KUAISHOU;
      else if (url.includes('taobao.com')) platform = CommercePlatform.TAOBAO;
      else if (url.includes('jd.com')) platform = CommercePlatform.JINGDONG;
      else if (url.includes('pinduoduo.com')) platform = CommercePlatform.PINDUODUO;
      else if (url.includes('xiaohongshu.com')) platform = CommercePlatform.XIAOHONGSHU;
      else if (url.includes('bilibili.com')) platform = CommercePlatform.BILIBILI;
    } else {
      // 从文本推断平台
      const pf = this.selectedPlatform;
      if (pf === '抖音') platform = CommercePlatform.DOUYIN;
      else if (pf === '快手') platform = CommercePlatform.KUAISHOU;
      else if (pf === '淘宝') platform = CommercePlatform.TAOBAO;
      else if (pf === '京东') platform = CommercePlatform.JINGDONG;
      else if (pf === '拼多多') platform = CommercePlatform.PINDUODUO;
      else if (pf === '小红书') platform = CommercePlatform.XIAOHONGSHU;
      else if (pf === 'B站') platform = CommercePlatform.BILIBILI;
    }

    return {
      productId,
      productName,
      images: [],
      description: text || url,
      price: 0,
      claimedPrice: 0,
      sellerId: `SELLER-${Date.now() % 10000}`,
      sellerName: '待解析',
      platform,
      hasLiveDemo: false,
      hasFilter: true,
      filterDisclosed: false,
      isSpliced: false,
      spliceDisclosed: false,
      scriptTemplate: text,
      reviewCount: 0,
      positiveRate: 0,
      returnRate: 0,
      complaintCount: 0,
      category: '通用',
      hasHiddenTerms: false
    };
  }

  // ============================================================
  //  显示辅助
  // ============================================================

  private getAnomalyIcon(severity: AnomalySeverity): string {
    const icons: Record<string, string> = {
      low: '•',
      medium: '▲',
      high: '✕',
      critical: '⛔'
    };
    return icons[severity] || '?';
  }

  private getSeverityColor(severity: AnomalySeverity): string {
    const colors: Record<string, string> = {
      low: '#88ff00',
      medium: '#ffcc00',
      high: '#ff6600',
      critical: '#ff0000'
    };
    return colors[severity] || '#666';
  }

  private getSeverityLabel(severity: AnomalySeverity): string {
    const labels: Record<string, string> = {
      low: '轻微',
      medium: '注意',
      high: '严重',
      critical: '危险'
    };
    return labels[severity] || '';
  }

  private getFraudTypeName(type: FraudType): string {
    const names: Record<string, string> = {
      exaggerated_claim: '夸大宣传',
      filter_deception: '滤镜误导',
      fake_demonstration: '虚假演示',
      spliced_footage: '拼接素材',
      template_script: '话术模板',
      influencer_prison: '信息牢房',
      elderly_scam: '老人套路',
      guided_consumption: '引导消费',
      price_fraud: '价格欺诈',
      review_manipulation: '评论操控',
      official_fake: '假冒认证',
      quality_mismatch: '实物不符',
      hidden_terms: '隐藏条款',
      emotional_manipulation: '情感操控'
    };
    return names[type] || type;
  }

  private getSellerWorstColor(level: BreakerLabelLevel): string {
    const colors: Record<string, string> = {
      green: '#00cc66',
      yellow: '#ffcc00',
      orange: '#ff8800',
      red: '#ff2244',
      black: '#ff0000'
    };
    return colors[level] || '#666';
  }
}

// ============================================================
//  子组件
// ============================================================

@Component
struct FilterChip {
  @Prop label: string;
  @Prop filterValue: string;
  @Link @Watch('onFilterChange') activeTab: number;

  onFilterChange(): void { /* handled by parent */ }

  build() {
    Text(this.label)
      .fontSize(12).fontColor('#aaa')
      .backgroundColor('rgba(255,255,255,0.05)')
      .borderRadius(14)
      .padding({ left: 12, right: 12, top: 4, bottom: 4 })
      .margin({ right: 8 })
  }
}

@Component
struct Bar {
  @Prop label: string;
  @Prop count: number;
  @Prop total: number;
  @Prop color: string;

  build() {
    Column()
      .width(`${Math.max((this.count / Math.max(this.total, 1)) * 100, 0)}%`)
      .height('100%')
      .backgroundColor(this.color)
  }
}
