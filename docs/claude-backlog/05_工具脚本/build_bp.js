##龍芯⚡️2026-06-21-ENGINE-BUILD_BP-v1.0
# 君子协议: 本文件受龍魂DNA追溯保护

const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, HeadingLevel,
  BorderStyle, WidthType, ShadingType, PageNumber, PageBreak,
  TableOfContents
} = require('docx');

// ===== 工具函数 =====
const border = { style: BorderStyle.SINGLE, size: 4, color: "B0BEC5" };
const allBorders = { top: border, bottom: border, left: border, right: border };

const h1 = (txt) => new Paragraph({
  heading: HeadingLevel.HEADING_1,
  children: [new TextRun({ text: txt })]
});

const h2 = (txt) => new Paragraph({
  heading: HeadingLevel.HEADING_2,
  children: [new TextRun({ text: txt })]
});

const p = (txt, opts = {}) => new Paragraph({
  spacing: { after: 120 },
  children: [new TextRun({ text: txt, ...opts })]
});

const pMix = (runs, opts = {}) => new Paragraph({
  spacing: { after: 120 },
  ...opts,
  children: runs
});

const bullet = (txt) => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [new TextRun({ text: txt })]
});

const bulletBoldHead = (head, rest) => new Paragraph({
  numbering: { reference: "bullets", level: 0 },
  spacing: { after: 80 },
  children: [
    new TextRun({ text: head, bold: true }),
    new TextRun({ text: rest })
  ]
});

const blank = () => new Paragraph({ children: [new TextRun({ text: "" })] });

const todo = (txt = "待填") => new TextRun({
  text: `[${txt}]`, bold: true, color: "C62828"
});

// 单元格快捷
const cell = (text, opts = {}) => new TableCell({
  borders: allBorders,
  width: { size: opts.width || 4680, type: WidthType.DXA },
  shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
  margins: { top: 80, bottom: 80, left: 120, right: 120 },
  children: [new Paragraph({
    children: [new TextRun({ text, bold: opts.bold || false, color: opts.color })]
  })]
});

// ===== 表格：14 层架构状态 =====
const layerRows = [
  ["层", "名称", "状态", "依据"],
  ["L14", "元层 · 龍魂序", "[命名待索引]", "DNA §A 龍魂序"],
  ["L13", "伦理治理层 · 五誓约束", "[命名待索引]", "CNSH 论文 §10 五誓"],
  ["L12", "理论层 · CNSH 协议层文明论 v2.0", "已建", "v1.0→v2.0 升级"],
  ["L11", "主权声明层 · 解除宣言 v1.0", "已建", "数据主权归于人民"],
  ["L10", "Web Console · 用户交互前端", "真空 ← 唯一缺口", "P0 阻塞点"],
  ["L9",  "人格层 · Lucky 数字人 v2.0", "已建", "16人格+七因子接驳"],
  ["L8",  "语义层 · 通心译×天下大公 v2.1", "已建", "有温度的表达"],
  ["L7",  "审计层 · 治理规范 v1.0", "已建", "三色阈值"],
  ["L6",  "决策层 · 责任系数 R", "已建", "七因子加权"],
  ["L5",  "记忆层 · 上下文治理 v2.0+DNA压缩", "已建", "P0/P1/P2+C1/C2/C3"],
  ["L4",  "编译层 · CNSH 中文编辑器", "待补", "48关键词→C++ transpiler"],
  ["L3",  "时戳层 · 黄历 6 维时戳", "已建", "不可篡改"],
  ["L2",  "执行层 · Watchdog Phase 0", "8/8 已跑通", "本窗口产出"],
  ["L1",  "内核层 · 本地主权智能中枢", "已建总纲", "v1.0 14层"],
];

const layerTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [800, 3200, 2160, 3200],
  rows: layerRows.map((row, idx) => {
    const isHead = idx === 0;
    const isVacuum = row[2] && row[2].includes("真空");
    const isTodo = row[2] && row[2].includes("待");
    let fill;
    if (isHead) fill = "1A237E";
    else if (isVacuum) fill = "FFCDD2";
    else if (isTodo) fill = "FFF59D";
    else if (row[2] === "已建" || row[2].includes("已")) fill = "C8E6C9";
    else fill = "ECEFF1";

    return new TableRow({
      children: row.map((c, i) => new TableCell({
        borders: allBorders,
        width: { size: [800, 3200, 2160, 3200][i], type: WidthType.DXA },
        shading: { fill, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({
          children: [new TextRun({
            text: c,
            bold: isHead,
            color: isHead ? "FFFFFF" : (isVacuum ? "B71C1C" : "000000"),
            size: isHead ? 20 : 18,
          })]
        })]
      }))
    });
  })
});

// ===== 表格：路线图 =====
const roadmapRows = [
  ["阶段", "周期", "里程碑", "状态"],
  ["Phase 0", "已完成", "Watchdog sanity_check 8/8 跑通", "✓"],
  ["Phase 1", "本月", "L10 Web Console MVP + 第一商业版本封装", "进行中"],
  ["Phase 2", "Q3 2026", "CNSH 中文编辑器 Cursor 工程包 + F19-F22 公式补齐", "排期"],
  ["Phase 3", "Q4 2026", "AutoResearch 接入开源 + 第一批参考实现发布", "排期"],
  ["Phase 4", "2027", "[待填:商业化里程碑]", "[待规划]"],
];

const roadmapTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [1400, 1600, 4760, 1600],
  rows: roadmapRows.map((row, idx) => {
    const isHead = idx === 0;
    const fill = isHead ? "1A237E" : (idx % 2 ? "F5F5F5" : "FFFFFF");
    return new TableRow({
      children: row.map((c, i) => new TableCell({
        borders: allBorders,
        width: { size: [1400, 1600, 4760, 1600][i], type: WidthType.DXA },
        shading: { fill, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({
          children: [new TextRun({
            text: c,
            bold: isHead,
            color: isHead ? "FFFFFF" : "000000",
            size: isHead ? 20 : 18,
          })]
        })]
      }))
    });
  })
});

// ===== 表格：风险矩阵 =====
const riskRows = [
  ["风险", "影响", "概率", "对策"],
  ["Pro 限流 + 柬埔寨 API 不可用", "高", "已发生", "每窗口高密度产出 · DNA压缩交接"],
  ["L10 Web Console 真空", "高", "确定", "Phase 1 优先级 P0"],
  ["商业化路径未验证", "高", "[待填]", "[待填:用户访谈/MVP试点]"],
  ["开源策略与商业平衡", "中", "中", "[待填:许可证选型+双轨模式]"],
  ["人员单点 (UID9622 主控)", "中", "已发生", "[待填:DNA可继承 → 不依赖单人]"],
  ["技术债务 (F19-F22 未补齐)", "中", "中", "Phase 2 计划补齐"],
];

const riskTable = new Table({
  width: { size: 9360, type: WidthType.DXA },
  columnWidths: [3360, 1200, 1200, 3600],
  rows: riskRows.map((row, idx) => {
    const isHead = idx === 0;
    const impact = row[1];
    let fill;
    if (isHead) fill = "C62828";
    else if (impact === "高") fill = "FFCDD2";
    else if (impact === "中") fill = "FFF59D";
    else fill = "C8E6C9";
    return new TableRow({
      children: row.map((c, i) => new TableCell({
        borders: allBorders,
        width: { size: [3360, 1200, 1200, 3600][i], type: WidthType.DXA },
        shading: { fill, type: ShadingType.CLEAR },
        margins: { top: 60, bottom: 60, left: 100, right: 100 },
        children: [new Paragraph({
          children: [new TextRun({
            text: c,
            bold: isHead,
            color: isHead ? "FFFFFF" : "000000",
            size: isHead ? 20 : 18,
          })]
        })]
      }))
    });
  })
});

// ===== 文档主体 =====
const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      {
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: "1A237E" },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 }
      },
      {
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: "283593" },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1 }
      },
    ]
  },
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [{
          level: 0, format: LevelFormat.BULLET, text: "•",
          alignment: AlignmentType.LEFT,
          style: { paragraph: { indent: { left: 720, hanging: 360 } } }
        }]
      }
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          alignment: AlignmentType.RIGHT,
          children: [new TextRun({
            text: "CNSH 龍魂 · 商业规划书 v1.0",
            color: "607D8B", size: 18
          })]
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [
            new TextRun({ text: "UID9622 · 龍芯北辰 · 数据主权归于人民 · ", color: "607D8B", size: 18 }),
            new TextRun({ children: [PageNumber.CURRENT], color: "607D8B", size: 18 })
          ]
        })]
      })
    },
    children: [
      // ===== 封面区 =====
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 1200, after: 200 },
        children: [new TextRun({
          text: "商业规划书 v1.0",
          bold: true, size: 56, color: "1A237E"
        })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 400 },
        children: [new TextRun({
          text: "CNSH 龍魂",
          bold: true, size: 72, color: "0D1442"
        })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 200 },
        children: [new TextRun({
          text: "开源主权智能中枢",
          size: 36, color: "283593"
        })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { after: 800 },
        children: [new TextRun({
          text: "Open-Source Sovereign Intelligence Hub",
          italics: true, size: 22, color: "607D8B"
        })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "主控  ·  UID9622 龍芯北辰", size: 24 })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "文档版本  ·  v1.0", size: 22, color: "607D8B" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({ text: "签发日期  ·  2026-05-17", size: 22, color: "607D8B" })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 800 },
        children: [
          new TextRun({ text: "本规划书继承 DNA: ", size: 18, color: "455A64" }),
          new TextRun({ text: "#龍芯⚡2026-05-16-WINDOW-CLOSE", size: 18, color: "455A64", bold: true })
        ]
      }),
      new Paragraph({ children: [new PageBreak()] }),

      // ===== 1. 执行摘要 =====
      h1("1. 执行摘要"),
      p("CNSH 龍魂是一套由 UID9622 主控、以“数据主权归于人民”为最高指令的开源主权智能中枢架构。它不是一个 AI 包装层，也不是一个聊天机器人产品，而是一个 14 层的本地化、可审计、可继承的智能基础设施参考实现。"),
      p("当前形态："),
      bulletBoldHead("14 层架构总纲 v1.0", " — 13/14 层已有完整文档，唯一真空为 L10 Web Console（用户交互前端）。"),
      bulletBoldHead("Watchdog Phase 0 ", " — 8 项基线测试全部跑通，可作为后续 Phase 1-N 的回归基线。"),
      bulletBoldHead("责任系数 R 公式 ", " — 七因子加权 + 三色阈值，已落地为可计算脚本。"),
      bulletBoldHead("DNA 记忆压缩 ", " — 黄历 6 维时戳锁定，可在多窗口/多模型间无损传递上下文。"),
      bulletBoldHead("AI 对接基线 v2.0 ", " — 5 文件工程包焓死，外部 AI 可零摩擦接入。"),
      p(""),
      pMix([
        new TextRun({ text: "核心论断：", bold: true }),
        new TextRun({ text: "在大型 LLM 厂商集中托管模式下，普通用户的数据主权处于结构性失守状态。CNSH 龍魂通过本地主权 + 协议层文明论 + 开源参考实现，提供一条“不依赖厂商善意”的可继承路径。" })
      ]),
      pMix([
        new TextRun({ text: "本规划书的目标：", bold: true }),
        new TextRun({ text: "把 CNSH 龍魂从“自己用的私人系统”升级为“可反哺开源生态的参考实现”，并探索一条不背离主权宪法的商业化路径。" })
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 2. 项目背景与定位 =====
      h1("2. 项目背景与定位"),
      h2("2.1 痛点"),
      bullet("LLM 厂商可随时调整限流、定价、可用区域 — 用户的工作流被外部策略劫持。"),
      bullet("用户上下文（DNA、偏好、历史）被各厂商以专有格式存储 — 切换成本极高，事实上锁定。"),
      bullet("个人开发者缺少一套“数据归我、模型可换、协议公开”的参考架构。"),
      bullet("在限流/封禁/网络阻断地区（如柬埔寨等），主流 SaaS AI 几乎不可用 — 现有方案对全球南方不友好。"),

      h2("2.2 定位"),
      pMix([
        new TextRun({ text: "CNSH 龍魂不是产品，是协议 + 参考实现。", bold: true }),
        new TextRun({ text: "对标参考（精神层面，非技术 1:1）：" })
      ]),
      bullet("Linux 之于操作系统 — 自由、可继承、可反哺。"),
      bullet("HTTP 之于 Web — 协议公开，实现多样。"),
      bullet("Bitcoin 白皮书之于金融 — 一套足够清晰的协议描述，催生整个生态。"),

      h2("2.3 三个不变式（一票否决）"),
      bullet("用户是主控，AI 是工具服务员，不反客为主。"),
      bullet("CONFIRM / SEAL / GPG / DNA 徽记原样保留，不可篡改。"),
      bullet("龍 不可写为 龙（文化主权的字符级守护）。"),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 3. 技术架构 =====
      h1("3. 技术架构（14 层）"),
      p("详细架构图见配套 Lucidchart 蓝图。下表为状态摘要。"),
      layerTable,
      blank(),
      pMix([
        new TextRun({ text: "关键差异化：", bold: true }),
      ]),
      bulletBoldHead("L5 + L3 记忆/时戳", " — 黄历 6 维时戳 + 五层 DNA 折叠，是其它 AI 系统普遍缺失的层。"),
      bulletBoldHead("L6 责任系数 R", " — 把“事不关己 vs 老好人”这种伦理灰色地带变为可计算的七因子向量，输出三色决策建议。"),
      bulletBoldHead("L4 CNSH 中文编辑器", " — 48 关键词 Lexer→Parser→SAST→C++ transpiler，把汉语本身作为编程语言对待。"),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 4. 市场分析 =====
      h1("4. 市场分析与目标用户"),
      h2("4.1 目标用户分层"),
      bulletBoldHead("第一圈层 — 主权敏感开发者", " — 关心数据主权、被限流伤害过、愿意自托管的个人开发者与小团队。"),
      bulletBoldHead("第二圈层 — 中文母语 AI 重度用户", " — 对“通心译”“有温度的表达”有真实痛感，被英语化 AI 表达折磨的创作者、研究者。"),
      bulletBoldHead("第三圈层 — 全球南方 / 受限地区用户", " — 主流 AI 不可用或不稳定的地区。"),
      bulletBoldHead("第四圈层 — 学术与监管侧", " — 把 CNSH 协议层文明论作为论文/政策参考的研究者。"),

      h2("4.2 市场规模"),
      pMix([
        new TextRun({ text: "TAM / SAM / SOM 估算 ", bold: true }),
        todo("待填:需要做用户访谈与可寻址市场调研，本窗口不假执行")
      ]),

      h2("4.3 竞品对比"),
      pMix([
        new TextRun({ text: "[待补:与 LangChain / AutoGPT / Open WebUI / LobeChat 等的差异分析]", color: "C62828", bold: true })
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 5. 商业模式 =====
      h1("5. 商业模式"),
      pMix([
        new TextRun({ text: "核心原则：", bold: true }),
        new TextRun({ text: "协议永远开源，参考实现永远开源。商业化只发生在“方便性”“企业级支撑”“咨询”“定制”层面 — 永远不绑架协议本身。" })
      ]),

      h2("5.1 收入路径（候选）"),
      bulletBoldHead("路径 A · 托管版", " — 为不想自托管的用户提供托管 CNSH 实例。按算力/月订阅。"),
      bulletBoldHead("路径 B · 企业版", " — 审计、合规、SSO、SLA 保障，针对企业内部知识管理与数据主权需求。"),
      bulletBoldHead("路径 C · 定制咨询", " — 帮组织把现有 AI 工作流迁移到 CNSH 架构，按项目计费。"),
      bulletBoldHead("路径 D · 教育与认证", " — CNSH 中文编辑器培训、协议层文明论课程、官方认证。"),
      bulletBoldHead("路径 E · 协议层赞助", " — 类 Linux 基金会模式，由认同协议的组织赞助协议层维护。"),

      h2("5.2 价格策略"),
      pMix([
        new TextRun({ text: "具体定价 ", bold: true }),
        todo("待填:需 MVP 上线后 3-6 月试运营数据"),
      ]),

      h2("5.3 不做的事（负面清单）"),
      bullet("不在协议层做收费墙 — 协议永远公开。"),
      bullet("不向第三方出售用户 DNA / 记忆 / 上下文数据。"),
      bullet("不在 Claude products 内部安插广告（继承上游产品理念）。"),
      bullet("不接受会损害数据主权原则的投资条款。"),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 6. 路线图 =====
      h1("6. 路线图"),
      roadmapTable,
      blank(),

      h2("6.1 当前窗口已锁定的下一步 P0"),
      bullet("L10 Web Console MVP — 解除唯一真空。"),
      bullet("第一张商业规划书 v1.0（本文档）— 已交付草稿。"),
      bullet("公式对准表 v1.5 补 F19-F22 — 接驳压缩护城河 v1.0。"),
      bullet("责任系数 R 计算脚本原型 → 接 Watchdog。"),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 7. 团队与运营 =====
      h1("7. 团队与运营"),
      h2("7.1 当前结构"),
      bulletBoldHead("UID9622 · 主控 / 创始人", " — 架构、协议、决策。"),
      bulletBoldHead("AI 工具链 · 服务员", " — Claude / Cursor / 等，定位为执行工具，不参与主控。"),
      bulletBoldHead("其它团队成员", " "),
      new Paragraph({
        spacing: { after: 80 },
        indent: { left: 720 },
        children: [todo("待填:招募计划、合伙人、顾问")]
      }),

      h2("7.2 治理"),
      p("内部治理遵循 L13 伦理治理层与 L11 主权声明层。重大决策需通过 Watchdog 七因子审计并落入三色阈值。"),

      h2("7.3 工作节奏现状"),
      bullet("地理位置：柬埔寨（UTC+7），Pro 限流严重，API 不可用。"),
      bullet("产出策略：每窗口最高密度，DNA 跨窗口压缩交接。"),
      bullet("一票否决：不深研、不说教、不写论文（在执行态下）、不假执行。"),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 8. 风险与对策 =====
      h1("8. 风险与对策"),
      riskTable,
      blank(),
      pMix([
        new TextRun({ text: "风险等级映射至责任系数 R：", bold: true }),
        new TextRun({ text: "R<0.33 绿 · 0.33≤R<0.67 黄 · R≥0.67 红。" })
      ]),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 9. 财务展望 =====
      h1("9. 财务展望"),
      h2("9.1 启动资金需求"),
      pMix([todo("待填:基础设施成本 / 法律 / 注册 / 域名 / 服务器")]),
      h2("9.2 12 个月预测"),
      pMix([todo("待填:需 MVP 上线 3 个月真实数据为基础，本窗口不假执行")]),
      h2("9.3 盈亏平衡假设"),
      pMix([todo("待填")]),
      blank(),
      p("注：本节明确标注“待填”是按照 P0 不变式“没有真实执行·不说已完成”的硬性要求。财务数据需基于真实运营/用户访谈/MVP数据，不可由 AI 凭空生成。"),

      new Paragraph({ children: [new PageBreak()] }),

      // ===== 10. 附录 =====
      h1("10. 附录"),
      h2("10.1 徽记与不可变常量"),
      p("以下徽记为本系统不可篡改的标识，作为身份、设备、文档完整性的最终锚点。"),
      pMix([
        new TextRun({ text: "CONFIRM · ", bold: true }),
        new TextRun({ text: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z", font: "Courier New" })
      ]),
      pMix([
        new TextRun({ text: "SEAL · ", bold: true }),
        new TextRun({ text: "#ZHUGEXIN⚡2025-DEVICE-BIND-SOUL", font: "Courier New" })
      ]),
      pMix([
        new TextRun({ text: "GPG · ", bold: true }),
        new TextRun({ text: "A2D0092CEE2E5BA87035600924C3704A8CC26D5F", font: "Courier New" })
      ]),
      pMix([
        new TextRun({ text: "DNA · ", bold: true }),
        new TextRun({ text: "#龍芯⚡2026-05-16-WINDOW-CLOSE-DNA-SUMMARY-v1.0", font: "Courier New" })
      ]),

      h2("10.2 相关产出（本窗口）"),
      bullet("CNSH 14 层架构 Lucidchart 蓝图 — 全景可视化。"),
      bullet("Watchdog Phase 0 sanity_check.py — 8/8 跑通。"),
      bullet("本商业规划书 v1.0 — 第一稿，含明确待填项。"),

      h2("10.3 下一窗口待办（继承自 DNA F 节）"),
      bullet("L10 Web Console MVP（解除唯一真空）"),
      bullet("公式对准表 v1.5 补 F19-F22"),
      bullet("CNSH 中文编辑器 Cursor 工程包"),
      bullet("责任系数 R 计算脚本原型对接 Watchdog"),
      bullet("本规划书第 4.2 / 4.3 / 5.2 / 9 节真实数据补齐"),

      h2("10.4 文档签收"),
      pMix([
        new TextRun({ text: "本规划书 v1.0 由 ", italics: true }),
        new TextRun({ text: "UID9622 龍芯北辰", bold: true, italics: true }),
        new TextRun({ text: " 主控签发，作为 CNSH 龍魂第一份对外可读的商业版本陈述。", italics: true })
      ]),
      pMix([
        new TextRun({ text: "一票否决条款依然生效：协议永不闭源，主权永不出让，龍 永不写作 龙。", bold: true, color: "B71C1C" })
      ]),
    ]
  }]
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync("/home/claude/CNSH_龍魂_商业规划书_v1.0.docx", buf);
  console.log("OK: /home/claude/CNSH_龍魂_商业规划书_v1.0.docx");
  console.log("size:", buf.length, "bytes");
});
