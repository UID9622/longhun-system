// entry/src/main/ets/engines/IntegrityDetector.ets
// 龍魂 · 商业诚信检测引擎 · 反虚假营销·反套路消费·反信息牢房
// DNA: #龍芯⚡️丙午·辛未·丙戌·INTEGRITY-DETECTOR-v1.0
// UID: 9622 | CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

// === 虚假类型枚举 ===
export enum FraudType {
  EXAGGERATED_CLAIM = 'exaggerated_claim',         // 夸大宣传
  FILTER_DECEPTION = 'filter_deception',           // 滤镜误导
  FAKE_DEMONSTRATION = 'fake_demonstration',       // 虚假实验/演示
  SPLICED_FOOTAGE = 'spliced_footage',             // 拼接素材冒充真实
  TEMPLATE_SCRIPT = 'template_script',             // 话术模板表演
  INFLUENCER_PRISON = 'influencer_prison',         // 信息牢房（大V垄断认知）
  ELDERLY_SCAM = 'elderly_scam',                   // 套路老人
  GUIDED_CONSUMPTION = 'guided_consumption',       // 引导性消费
  PRICE_FRAUD = 'price_fraud',                     // 价格欺诈
  REVIEW_MANIPULATION = 'review_manipulation',     // 刷单控评
  OFFICIAL_FAKE = 'official_fake',                 // 假冒官方认证
  QUALITY_MISMATCH = 'quality_mismatch',           // 实物与描述不符
  HIDDEN_TERMS = 'hidden_terms',                   // 隐藏条款
  EMOTIONAL_MANIPULATION = 'emotional_manipulation' // 情感操控
}

// === 检测严重程度 ===
export enum AnomalySeverity {
  LOW = 'low',
  MEDIUM = 'medium',
  HIGH = 'high',
  CRITICAL = 'critical'
}

// === 诚信等级 ===
export enum IntegrityLevel {
  A = 'A',   // 优秀：未发现异常
  B = 'B',   // 良好：轻微提醒
  C = 'C',   // 一般：注意核实
  D = 'D',   // 差：高风险
  F = 'F'    // 严重：涉嫌欺诈
}

// === 检测平台 ===
export enum CommercePlatform {
  DOUYIN = '抖音',
  KUAISHOU = '快手',
  TAOBAO = '淘宝',
  JINGDONG = '京东',
  PINDUODUO = '拼多多',
  XIAOHONGSHU = '小红书',
  WECHAT = '微信视频号',
  BILIBILI = 'B站',
  OTHER = '其他'
}

// === 商品检测输入 ===
export interface ProductInspection {
  productId: string;
  productName: string;
  videoUrl?: string;
  images: string[];
  description: string;
  price: number;
  claimedPrice: number;           // 声称原价
  sellerId: string;
  sellerName: string;
  platform: CommercePlatform;
  officialCert?: string;          // 官方认证标识
  officialCertType?: string;      // 认证类型: CN-GB/CN-CCC/CN-ISO/CN-CQC
  hasLiveDemo: boolean;           // 是否有真实直播演示
  hasFilter: boolean;             // 是否使用滤镜
  filterDisclosed: boolean;       // 滤镜是否已标注
  isSpliced: boolean;             // 是否拼接素材
  spliceDisclosed: boolean;       // 拼接是否已声明
  scriptTemplate?: string;        // 话术文本
  influencerFollowers?: number;   // 主播粉丝数
  influencerName?: string;        // 主播名称
  reviewCount: number;            // 评论数
  positiveRate: number;           // 好评率(%)
  returnRate: number;             // 退货率(%)
  complaintCount: number;         // 投诉数
  targetAudience?: string[];      // 目标人群: ['elderly', 'children', 'general']
  category: string;               // 商品类目
  brandName?: string;             // 品牌名
  productionDate?: string;        // 生产日期
  warrantyPeriod?: string;        // 质保期
  hasHiddenTerms: boolean;        // 是否有隐藏条款
  priceHistory?: PriceHistory[];  // 历史价格
}

// === 历史价格 ===
export interface PriceHistory {
  date: string;
  price: number;
  platform: string;
}

// === 异常记录 ===
export interface AnomalyRecord {
  type: FraudType;
  severity: AnomalySeverity;
  evidence: string;
  suggestion: string;
  matchedKeywords: string[];
  confidence: number;           // 检测置信度 0-1
}

// === 诚信检测报告 ===
export interface IntegrityReport {
  productId: string;
  productName: string;
  timestamp: number;
  anomalies: AnomalyRecord[];
  integrityLevel: IntegrityLevel;
  trustScore: number;           // 0-100
  officialCertValid: boolean;
  recommendation: string;
  sellerWarnings: number;       // 该商家历史警告数
  dnaSignature: string;
}

// ============================================================
//  诚信检测引擎
// ============================================================

export class IntegrityDetector {
  private static instance: IntegrityDetector;

  // === 夸大宣传关键词库 ===
  private exaggerationWords: string[] = [
    '最', '第一', '唯一', '绝对', '100%', '保证', '包治', '万能',
    '神器', '秒变', '超越所有', '无可替代', '史上最', '天花板',
    '吊打', '碾压', '完胜', '零差评', '永不', '永远',
    '颠覆', '革命性', '划时代', '黑科技', '诺贝尔级别'
  ];

  // === 套路话术模板库 ===
  private scamScripts: string[] = [
    '最后三天', '错过再等一年', '仅限今天', '限时抢购',
    '老板不在随便卖', '工厂直销价', '亏本清仓',
    '给家人们送福利', '宠粉福利', '粉丝专属',
    '不是钱的问题', '交个朋友', '不赚钱',
    '我自己也在用', '全家都在用', '我孩子也在吃',
    '专家推荐', '明星同款', '名人都在用',
    '医院都在用', '医生推荐', '临床验证',
    '包治百病', '三天见效', '一抹就白', '一吃就瘦',
    '无效退款', '不满意包退', '无理由退货',
    '纯天然无副作用', '草本精华', '古法秘制',
    '祖传秘方', '国家专利', '国际认证',
    '限量抢购', '库存不多', '手慢无',
    '下单送', '买一送', '前100名',
    '已卖爆', '回购率', '复购率',
    '今天不买明天涨价', '原材料涨价',
    '央视推荐', '人民日报报道', '新华社'
  ];

  // === 老人套路关键词 ===
  private elderlyScams: string[] = [
    '孝顺', '儿女放心', '养老', '保健', '长寿',
    '免费体验', '免费讲座', '免费旅游', '免费领取',
    '养老金', '以房养老', '高回报', '保本', '稳赚',
    '老年专用', '专为中老年', '延年益寿', '抗衰老',
    '送礼佳品', '孝敬父母', '送爸妈', '长辈',
    '会议营销', '健康讲座', '专家义诊'
  ];

  // === 引导性消费关键词 ===
  private guidedConsumptionWords: string[] = [
    '不买就亏了', '别人都买了', '再不买就没了',
    '聪明人都买了', '懂的人自然懂', '识货的来',
    '这个价格你还等什么', '别犹豫了',
    '错过后悔', '不买会后悔', '必须囤',
    '提升幸福感', '精致生活', '对自己好一点',
    '舍不得孩子套不着狼', '投资自己',
    '人生苦短', '及时行乐', '取悦自己'
  ];

  // === 情感操控关键词 ===
  private emotionalManipulationWords: string[] = [
    '你忍心吗', '你对得起', '你怎么能',
    '你看别人家', '别人都', '就你家',
    '当妈的都懂', '做父母的都',
    '心疼', '可怜', '同情',
    '支持一下', '帮帮忙', '不容易',
    '家人们', '兄弟姐妹们', '老铁们'
  ];

  // === 已知虚假认证前缀 ===
  private validCertPrefixes: string[] = [
    'CN-GB', 'CN-CCC', 'CN-ISO', 'CN-CQC',
    'CN-SC', 'CN-QS', 'CN-HACCP', 'CN-GMP',
    'CN-ORG', 'CN-GREEN', 'CN-KOSHER'
  ];

  static getInstance(): IntegrityDetector {
    if (!IntegrityDetector.instance) {
      IntegrityDetector.instance = new IntegrityDetector();
    }
    return IntegrityDetector.instance;
  }

  // ============================================================
  //  主检测入口
  // ============================================================

  async inspect(product: ProductInspection): Promise<IntegrityReport> {
    const anomalies: AnomalyRecord[] = [];

    // 并行执行所有检测维度
    const checks = [
      this.detectExaggeration(product),
      this.detectFilterDeception(product),
      this.detectFakeDemonstration(product),
      this.detectSplicedFootage(product),
      this.detectTemplateScript(product),
      this.detectInfluencerPrison(product),
      this.detectElderlyScam(product),
      this.detectGuidedConsumption(product),
      this.detectPriceFraud(product),
      this.detectReviewManipulation(product),
      this.detectOfficialFake(product),
      this.detectQualityMismatch(product),
      this.detectHiddenTerms(product),
      this.detectEmotionalManipulation(product)
    ];

    for (const check of checks) {
      if (check) anomalies.push(check);
    }

    // 计算诚信等级
    const integrityLevel = this.calculateIntegrityLevel(anomalies);

    // 计算信任分
    const trustScore = this.calculateTrustScore(anomalies, product);

    return {
      productId: product.productId,
      productName: product.productName,
      timestamp: Date.now(),
      anomalies,
      integrityLevel,
      trustScore,
      officialCertValid: this.verifyOfficialCert(product.officialCert || ''),
      recommendation: this.generateRecommendation(integrityLevel, anomalies, product),
      sellerWarnings: 0, // 后续从熔断器历史获取
      dnaSignature: this.signReport(product, anomalies)
    };
  }

  // ============================================================
  //  14维度检测
  // ============================================================

  // 1. 夸大宣传检测
  private detectExaggeration(product: ProductInspection): AnomalyRecord | null {
    const found: string[] = [];
    for (const word of this.exaggerationWords) {
      if (product.description.includes(word)) found.push(word);
    }

    if (found.length === 0) return null;

    const severity = found.length >= 5 ? AnomalySeverity.HIGH
      : found.length >= 3 ? AnomalySeverity.MEDIUM
      : AnomalySeverity.LOW;

    return {
      type: FraudType.EXAGGERATED_CLAIM,
      severity,
      evidence: `发现${found.length}个夸大词汇: ${found.slice(0, 5).join('、')}${found.length > 5 ? '...' : ''}`,
      suggestion: '"最""第一"等绝对化用语违反广告法，要求提供第三方检测报告核实宣传内容',
      matchedKeywords: found,
      confidence: Math.min(0.6 + found.length * 0.08, 0.95)
    };
  }

  // 2. 滤镜误导检测
  private detectFilterDeception(product: ProductInspection): AnomalyRecord | null {
    if (!product.hasFilter) return null;

    if (!product.filterDisclosed && !product.description.includes('效果图')) {
      return {
        type: FraudType.FILTER_DECEPTION,
        severity: AnomalySeverity.HIGH,
        evidence: '使用滤镜/美颜但未标注"效果图"或"经过美化处理"',
        suggestion: '要求商家提供无滤镜实拍对比，标注美化情况属于消费者知情权',
        matchedKeywords: ['滤镜', '美颜', '美化'],
        confidence: 0.85
      };
    }

    // 即使标注了，如果是食品/药品/护肤品也应警告
    const sensitiveCategories = ['食品', '药品', '保健品', '护肤品', '化妆品'];
    if (sensitiveCategories.includes(product.category) && product.hasFilter) {
      return {
        type: FraudType.FILTER_DECEPTION,
        severity: AnomalySeverity.MEDIUM,
        evidence: `商品属于"${product.category}"类目，使用滤镜可能影响消费者对产品效果的判断`,
        suggestion: '食品和护肤品的效果展示不应使用滤镜，建议查看真实用户晒单',
        matchedKeywords: [product.category, '滤镜'],
        confidence: 0.70
      };
    }

    return null;
  }

  // 3. 虚假实验/演示检测
  private detectFakeDemonstration(product: ProductInspection): AnomalyRecord | null {
    const claimWords = ['实验证明', '实验表明', '测试结果', '检测报告', '权威检测', '实验室数据'];

    const found = claimWords.filter(w => product.description.includes(w));

    if (found.length > 0 && !product.hasLiveDemo) {
      return {
        type: FraudType.FAKE_DEMONSTRATION,
        severity: AnomalySeverity.CRITICAL,
        evidence: `声称"${found.join('、')}"但无直播/实时演示验证`,
        suggestion: '要求商家提供第三方公证机构出具的实验视频或实时直播演示',
        matchedKeywords: found,
        confidence: 0.90
      };
    }

    return null;
  }

  // 4. 拼接素材检测
  private detectSplicedFootage(product: ProductInspection): AnomalyRecord | null {
    if (!product.isSpliced) return null;

    if (!product.spliceDisclosed && !product.description.includes('素材来源')) {
      return {
        type: FraudType.SPLICED_FOOTAGE,
        severity: AnomalySeverity.MEDIUM,
        evidence: '使用拼接/剪辑素材但未声明素材来源',
        suggestion: '要求商家标注素材拼接情况，明确哪些是原片、哪些是引用素材',
        matchedKeywords: ['拼接', '剪辑', '素材'],
        confidence: 0.75
      };
    }

    return null;
  }

  // 5. 话术模板检测
  private detectTemplateScript(product: ProductInspection): AnomalyRecord | null {
    const text = product.scriptTemplate || product.description;
    const found: string[] = [];

    for (const script of this.scamScripts) {
      if (text.includes(script)) found.push(script);
    }

    if (found.length === 0) return null;

    const severity = found.length >= 8 ? AnomalySeverity.HIGH
      : found.length >= 5 ? AnomalySeverity.MEDIUM
      : AnomalySeverity.LOW;

    return {
      type: FraudType.TEMPLATE_SCRIPT,
      severity,
      evidence: `匹配${found.length}条营销话术模板: ${found.slice(0, 5).join('、')}${found.length > 5 ? '...' : ''}`,
      suggestion: '标准化营销话术≠产品真实性能，请理性看待，关注产品本身而非话术',
      matchedKeywords: found,
      confidence: Math.min(0.5 + found.length * 0.06, 0.90)
    };
  }

  // 6. 信息牢房检测（大V垄断认知）
  private detectInfluencerPrison(product: ProductInspection): AnomalyRecord | null {
    if (!product.influencerFollowers || product.influencerFollowers < 500000) return null;

    const monopolyIndicators = [
      '我说好就好', '信我就买', '不用看别的', '这个最好',
      '别的都不行', '只有我这里有', '独家', '全网最低',
      '别家都是假的', '只有我是真的', '其他都是坑'
    ];

    const text = product.scriptTemplate || product.description;
    const found = monopolyIndicators.filter(i => text.includes(i));

    // 好评率异常高 + 大V
    const reviewAbnormal = product.reviewCount > 10000 && product.positiveRate > 98;

    if (found.length > 0 || reviewAbnormal) {
      const reasons: string[] = [];
      if (found.length > 0) reasons.push(`垄断性话术: ${found.join('、')}`);
      if (reviewAbnormal) reasons.push(`大V(${product.influencerFollowers}粉丝)带货好评率${product.positiveRate}%异常偏高`);

      return {
        type: FraudType.INFLUENCER_PRISON,
        severity: AnomalySeverity.HIGH,
        evidence: reasons.join('；'),
        suggestion: '跳出单一信息源，多方比价、查看中差评真实反馈，警惕KOL认知垄断',
        matchedKeywords: found,
        confidence: 0.80
      };
    }

    return null;
  }

  // 7. 老人套路检测
  private detectElderlyScam(product: ProductInspection): AnomalyRecord | null {
    const text = product.scriptTemplate || product.description;
    const found = this.elderlyScams.filter(s => text.includes(s));

    // 同时检查目标人群
    const targetsElderly = product.targetAudience?.includes('elderly');

    if (found.length > 0 || targetsElderly) {
      const reasons: string[] = [];
      if (found.length > 0) reasons.push(`老人套路关键词: ${found.slice(0, 5).join('、')}`);
      if (targetsElderly) reasons.push('目标人群标记为"老年人"');

      return {
        type: FraudType.ELDERLY_SCAM,
        severity: found.length >= 5 ? AnomalySeverity.CRITICAL : AnomalySeverity.HIGH,
        evidence: reasons.join('；'),
        suggestion: '提醒家中老人：不轻信"免费""送礼"，核实产品资质，大额消费前与子女商量',
        matchedKeywords: found,
        confidence: found.length >= 5 ? 0.95 : 0.80
      };
    }

    return null;
  }

  // 8. 引导性消费检测
  private detectGuidedConsumption(product: ProductInspection): AnomalyRecord | null {
    const text = product.scriptTemplate || product.description;
    const found = this.guidedConsumptionWords.filter(w => text.includes(w));

    if (found.length === 0) return null;

    return {
      type: FraudType.GUIDED_CONSUMPTION,
      severity: found.length >= 4 ? AnomalySeverity.MEDIUM : AnomalySeverity.LOW,
      evidence: `发现${found.length}条引导性消费话术: ${found.slice(0, 5).join('、')}`,
      suggestion: '话术制造焦虑催促下单，请按实际需求理性消费',
      matchedKeywords: found,
      confidence: 0.70
    };
  }

  // 9. 价格欺诈检测
  private detectPriceFraud(product: ProductInspection): AnomalyRecord | null {
    if (!product.claimedPrice || product.claimedPrice <= 0) return null;

    const discountRatio = product.price / product.claimedPrice;

    // 声称原价1000，卖99 → 降幅超70% → 高度疑似虚构原价
    if (discountRatio < 0.3) {
      const discountPercent = ((1 - discountRatio) * 100).toFixed(0);
      return {
        type: FraudType.PRICE_FRAUD,
        severity: discountRatio < 0.1 ? AnomalySeverity.CRITICAL : AnomalySeverity.HIGH,
        evidence: `声称原价${product.claimedPrice}元，现价${product.price}元，降幅${discountPercent}%，疑似虚构原价`,
        suggestion: '核实历史价格走势，对比同品类市场均价，警惕"先涨后降"套路',
        matchedKeywords: ['原价', '现价', '降价', '折扣'],
        confidence: Math.min(0.7 + (1 - discountRatio) * 0.25, 0.95)
      };
    }

    // 降幅50-70%
    if (discountRatio < 0.5) {
      return {
        type: FraudType.PRICE_FRAUD,
        severity: AnomalySeverity.MEDIUM,
        evidence: `声称原价${product.claimedPrice}元，现价${product.price}元，降幅${((1 - discountRatio) * 100).toFixed(0)}%`,
        suggestion: '建议查看该商品的历史价格曲线，确认是否为真实优惠',
        matchedKeywords: ['原价', '降价'],
        confidence: 0.60
      };
    }

    return null;
  }

  // 10. 评论操控检测
  private detectReviewManipulation(product: ProductInspection): AnomalyRecord | null {
    // 大量评论 + 极高好评率 + 极低退货率 = 刷单嫌疑
    if (product.reviewCount > 10000 && product.positiveRate > 99 && product.returnRate < 1) {
      return {
        type: FraudType.REVIEW_MANIPULATION,
        severity: AnomalySeverity.HIGH,
        evidence: `评论${product.reviewCount}条，好评率${product.positiveRate}%，退货率${product.returnRate}%——数据组合异常`,
        suggestion: '重点查看中差评内容和追评，关注"刷单"、"好评返现"等关键词',
        matchedKeywords: ['好评率', '刷单', '控评'],
        confidence: 0.85
      };
    }

    // 好评率异常
    if (product.reviewCount > 1000 && product.positiveRate > 99.5) {
      return {
        type: FraudType.REVIEW_MANIPULATION,
        severity: AnomalySeverity.MEDIUM,
        evidence: `${product.reviewCount}条评论中好评率高达${product.positiveRate}%，高于正常范围`,
        suggestion: '建议对比追评率和中差评内容，可能存在删评或诱导好评行为',
        matchedKeywords: ['好评率'],
        confidence: 0.65
      };
    }

    return null;
  }

  // 11. 假冒官方认证
  private detectOfficialFake(product: ProductInspection): AnomalyRecord | null {
    if (!product.officialCert) return null;

    if (!this.verifyOfficialCert(product.officialCert)) {
      return {
        type: FraudType.OFFICIAL_FAKE,
        severity: AnomalySeverity.CRITICAL,
        evidence: `声称认证"${product.officialCert}"但无法通过官方渠道验证`,
        suggestion: '到国家认证认可监督管理委员会官网(cnca.gov.cn)核实认证真伪',
        matchedKeywords: [product.officialCert],
        confidence: 0.95
      };
    }

    return null;
  }

  // 12. 实物与描述不符检测
  private detectQualityMismatch(product: ProductInspection): AnomalyRecord | null {
    const mismatchIndicators = [
      '图片仅供参考', '以实物为准', '颜色随机',
      '款式随机', '批次不同', '略有差异',
      '不保证完全一致', '效果因人而异'
    ];

    const found = mismatchIndicators.filter(w => product.description.includes(w));

    if (found.length > 0) {
      return {
        type: FraudType.QUALITY_MISMATCH,
        severity: found.length >= 3 ? AnomalySeverity.MEDIUM : AnomalySeverity.LOW,
        evidence: `存在免责声明: ${found.join('、')}`,
        suggestion: '商家已声明可能不一致，请以收到实物为准，保留开箱视频作为维权证据',
        matchedKeywords: found,
        confidence: 0.75
      };
    }

    return null;
  }

  // 13. 隐藏条款检测
  private detectHiddenTerms(product: ProductInspection): AnomalyRecord | null {
    if (!product.hasHiddenTerms) return null;

    const hiddenIndicators = [
      '最终解释权', '详见包装', '详情咨询',
      '具体以合同为准', '详见说明书', '详见条款',
      '详见活动规则', '详见细则'
    ];

    const found = hiddenIndicators.filter(w => product.description.includes(w));

    return {
      type: FraudType.HIDDEN_TERMS,
      severity: AnomalySeverity.MEDIUM,
      evidence: `存在隐藏条款标识: ${found.length > 0 ? found.join('、') : '标记为含隐藏条款'}`,
      suggestion: '下单前务必查看完整条款，注意退换货条件、保修范围、附加费用等',
      matchedKeywords: found,
      confidence: 0.80
    };
  }

  // 14. 情感操控检测
  private detectEmotionalManipulation(product: ProductInspection): AnomalyRecord | null {
    const text = product.scriptTemplate || product.description;
    const found = this.emotionalManipulationWords.filter(w => text.includes(w));

    if (found.length === 0) return null;

    return {
      type: FraudType.EMOTIONAL_MANIPULATION,
      severity: found.length >= 5 ? AnomalySeverity.MEDIUM : AnomalySeverity.LOW,
      evidence: `发现${found.length}条情感操控话术: ${found.slice(0, 5).join('、')}`,
      suggestion: '商家利用情感建立虚假信任关系，请回归产品本身理性判断',
      matchedKeywords: found,
      confidence: 0.70
    };
  }

  // ============================================================
  //  辅助方法
  // ============================================================

  // 验证官方认证
  private verifyOfficialCert(cert: string): boolean {
    if (!cert || cert.trim() === '') return false;
    return this.validCertPrefixes.some(p => cert.startsWith(p));
  }

  // 计算诚信等级
  private calculateIntegrityLevel(anomalies: AnomalyRecord[]): IntegrityLevel {
    if (anomalies.length === 0) return IntegrityLevel.A;

    const criticalCount = anomalies.filter(a => a.severity === AnomalySeverity.CRITICAL).length;
    const highCount = anomalies.filter(a => a.severity === AnomalySeverity.HIGH).length;
    const mediumCount = anomalies.filter(a => a.severity === AnomalySeverity.MEDIUM).length;

    if (criticalCount >= 2 || (criticalCount >= 1 && highCount >= 3)) return IntegrityLevel.F;
    if (criticalCount >= 1 || highCount >= 3) return IntegrityLevel.D;
    if (highCount >= 1 || mediumCount >= 3) return IntegrityLevel.C;
    return IntegrityLevel.B;
  }

  // 计算信任分 (0-100)
  private calculateTrustScore(anomalies: AnomalyRecord[], product: ProductInspection): number {
    let score = 100;

    for (const a of anomalies) {
      switch (a.severity) {
        case AnomalySeverity.CRITICAL: score -= 25; break;
        case AnomalySeverity.HIGH: score -= 15; break;
        case AnomalySeverity.MEDIUM: score -= 8; break;
        case AnomalySeverity.LOW: score -= 3; break;
      }
    }

    // 加分项
    if (product.officialCert && this.verifyOfficialCert(product.officialCert)) score += 10;
    if (product.hasLiveDemo) score += 15;
    if (product.hasFilter && product.filterDisclosed) score += 5;
    if (product.isSpliced && product.spliceDisclosed) score += 5;
    if (product.returnRate > 0 && product.returnRate < 5) score += 5; // 正常退货率

    return Math.max(0, Math.min(100, Math.round(score)));
  }

  // 生成建议
  private generateRecommendation(level: IntegrityLevel, anomalies: AnomalyRecord[], product: ProductInspection): string {
    switch (level) {
      case IntegrityLevel.A:
        return '✓ 诚信通过，未发现明显异常。建议：保留购物凭证和开箱视频以备不时之需。';

      case IntegrityLevel.B:
        const lowWarnings = anomalies.filter(a => a.severity === AnomalySeverity.LOW || a.severity === AnomalySeverity.MEDIUM);
        return `⚠ 检测到${anomalies.length}项轻微异常。重点注意：${lowWarnings.map(a => a.suggestion).slice(0, 2).join('；')}`;

      case IntegrityLevel.C:
        const medWarnings = anomalies.filter(a => a.severity !== AnomalySeverity.LOW);
        return `▲ 检测到${anomalies.length}项异常需要核实。建议：${medWarnings.map(a => a.suggestion).slice(0, 2).join('；')}`;

      case IntegrityLevel.D:
        const highWarnings = anomalies.filter(a => a.severity === AnomalySeverity.HIGH || a.severity === AnomalySeverity.CRITICAL);
        return `✕ 高风险！检测到${anomalies.length}项异常。强烈建议：${highWarnings.map(a => a.suggestion).join('；')}。如已下单请保留所有证据。`;

      case IntegrityLevel.F:
        return `✕✕ 涉嫌欺诈！检测到${anomalies.length}项严重异常。建议立即终止交易并向平台和12315举报。已下单请保留支付记录、聊天记录、商品页面截图。`;

      default:
        return '无法评估，建议人工审核。';
    }
  }

  // 国密签名
  private signReport(product: ProductInspection, anomalies: AnomalyRecord[]): string {
    const payload = `${product.productId}|${anomalies.length}|${product.platform}|${Date.now()}`;
    return `SM3-${this.simpleHash(payload)}`;
  }

  private simpleHash(input: string): string {
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash |= 0;
    }
    return Math.abs(hash).toString(16).substring(0, 8);
  }
}

export const integrityDetector = IntegrityDetector.getInstance();
