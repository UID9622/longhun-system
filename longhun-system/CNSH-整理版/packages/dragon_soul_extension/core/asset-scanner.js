// core/asset-scanner.js - 龍魂数字资产扫描器 v2.0 - 完整关键词版
// DNA: #龍芯⚡️2026-03-03-ASSET-SCANNER-V2-UID9622

class AssetScanner {
  constructor() {
    this.uid = "9622";
    this.dnaPrefix = "#龍芯⚡️";

    // ===== 完整原创关键词库 =====
    this.originalMarkers = [
      // 身份锚（核弹级，有一个就够）
      "UID9622", "宝宝", "诸葛鑫", "Lucky",
      "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
      "LK9X-772Z", "#龍芯", "#ZHUGEXIN", "CONFIRM🌌9622",

      // 体系关键词
      "北辰协议", "P0", "铁律", "红线", "宣言",
      "三才算法", "天爻", "地爻", "人爻", "冲气以为和",
      "太极", "易经", "八卦", "卦象", "道德经",
      "量子纠缠", "Bra-Ket", "叠加态", "观测坍缩",
      "元宇宙", "元知", "数字人", "元世界",

      // 技术关键词
      "LU_", "LU指令", "主控指令", "熔断", "净化器",
      "DNA追溯", "三色审计", "CNSH", "龍魂", "龙魂",
      "星辰记忆", "压缩卡", "语义压缩", "记忆编辑器",
      "人格路由", "ROUTE_", "persona", "fuse_manager",
      "snapshot_core", "dragon_soul",

      // 理念关键词
      "人格", "推演", "开源", "主权", "算法宪法",
      "愿景", "内核", "规则引擎", "权限管理",
      "H武器", "数字资产", "贡献尊严",

      // 代码特征
      "PersonaRoute", "DragonSoul", "ROUTE_GUARDIAN",
      "ROUTE_ARCHITECT", "SemanticCompression",
    ];

    // 外部代码特征
    this.externalMarkers = [
      "MIT License", "Apache License", "Copyright (c)",
      "All rights reserved", "DO NOT EDIT",
      "Auto-generated", "This file is generated"
    ];
  }

  /**
   * 扫描文本内容
   * @param {string} content - 文本内容
   * @returns {object} 扫描结果
   */
  scanContent(content) {
    const originalHits = this.originalMarkers.filter(m => content.includes(m));
    const externalHits = this.externalMarkers.filter(m => content.includes(m));

    // 只要有"宝宝"或"UID9622"直接认定原创
    const isCore = ["UID9622", "宝宝", "#龍芯", "#ZHUGEXIN"].some(k => content.includes(k));

    let category;
    if (isCore) {
      category = "✅ 核心原创";
    } else if (originalHits.length > 0 && externalHits.length === 0) {
      category = "🟢 原创";
    } else if (originalHits.length > 0 && externalHits.length > 0) {
      category = "🟡 混合";
    } else if (externalHits.length > 0) {
      category = "📦 外部";
    } else {
      category = "❓ 未标记";
    }

    return {
      类型: category,
      原创标记: originalHits,
      外部标记: externalHits,
      字符数: content.length,
      标记数量: originalHits.length + externalHits.length
    };
  }

  /**
   * 扫描文件（浏览器环境）
   * @param {File} file - 文件对象
   * @returns {Promise<object>} 扫描结果
   */
  async scanFile(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();

      reader.onload = (e) => {
        try {
          const content = e.target.result;
          const result = this.scanContent(content);

          resolve({
            文件: file.name,
            文件大小: file.size,
            类型: result.类型,
            原创标记: result.原创标记.slice(0, 5),
            字符数: result.字符数,
            修改时间: file.lastModified ? new Date(file.lastModified).toLocaleString('zh-CN') : '未知'
          });
        } catch (error) {
          reject(error);
        }
      };

      reader.onerror = () => reject(reader.error);
      reader.readAsText(file, 'utf-8');
    });
  }

  /**
   * 批量扫描文件
   * @param {Array<File>} files - 文件数组
   * @returns {Promise<Array>} 扫描结果数组
   */
  async batchScanFiles(files) {
    const results = [];

    for (const file of files) {
      try {
        const result = await this.scanFile(file);
        results.push(result);
      } catch (error) {
        console.error(`扫描文件失败: ${file.name}`, error);
      }
    }

    return results;
  }

  /**
   * 生成扫描报告
   * @param {Array} results - 扫描结果数组
   * @returns {object} 扫描报告
   */
  generateReport(results) {
    const categories = {
      "✅ 核心原创": [],
      "🟢 原创": [],
      "🟡 混合": [],
      "📦 外部": [],
      "❓ 未标记": []
    };

    results.forEach(result => {
      categories[result.类型].push(result);
    });

    const core = categories["✅ 核心原创"].length;
    const original = categories["🟢 原创"].length;
    const total = results.length;

    return {
      扫描时间: new Date().toISOString(),
      DNA: `${this.dnaPrefix}${new Date().toISOString().split('T')[0]}-SCAN-UID${this.uid}`,
      统计: {
        "✅ 核心原创": core,
        "🟢 原创": original,
        "🟡 混合": categories["🟡 混合"].length,
        "📦 外部": categories["📦 外部"].length,
        "❓ 未标记": categories["❓ 未标记"].length,
        总计: total,
        合计原创: core + original
      },
      详情: categories
    };
  }

  /**
   * 导出报告为 JSON
   * @param {object} report - 扫描报告
   * @returns {string} JSON 字符串
   */
  exportReportToJSON(report) {
    return JSON.stringify(report, null, 2);
  }

  /**
   * 导出报告为 Markdown
   * @param {object} report - 扫描报告
   * @returns {string} Markdown 字符串
   */
  exportReportToMarkdown(report) {
    let markdown = `# 🐲 龍魂资产扫描报告\n\n`;
    markdown += `**扫描时间**: ${report.扫描时间}\n`;
    markdown += `**DNA**: ${report.DNA}\n\n`;
    markdown += `## 📊 统计摘要\n\n`;
    markdown += `| 类型 | 数量 |\n`;
    markdown += `|------|------|\n`;

    for (const [type, count] of Object.entries(report.统计)) {
      markdown += `| ${type} | ${count} |\n`;
    }

    markdown += `\n## 📁 详细列表\n\n`;

    for (const [category, items] of Object.entries(report.详情)) {
      if (items.length === 0) continue;

      markdown += `### ${category} (${items.length} 个文件)\n\n`;

      items.forEach(item => {
        markdown += `- **${item.文件}**\n`;
        markdown += `  - 字符数: ${item.字符数}\n`;
        markdown += `  - 修改时间: ${item.修改时间}\n`;
        if (item.原创标记 && item.原创标记.length > 0) {
          markdown += `  - 标记: ${item.原创标记.slice(0, 3).join(', ')}\n`;
        }
        markdown += `\n`;
      });
    }

    markdown += `\n---\n\n`;
    markdown += `确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z ✅\n`;

    return markdown;
  }

  /**
   * 搜索关键词
   * @param {string} keyword - 关键词
   * @param {Array} results - 扫描结果数组
   * @returns {Array} 匹配的结果
   */
  searchKeyword(keyword, results) {
    const lowerKeyword = keyword.toLowerCase();
    return results.filter(result =>
      result.文件.toLowerCase().includes(lowerKeyword) ||
      result.原创标记.some(m => m.toLowerCase().includes(lowerKeyword))
    );
  }

  /**
   * 获取统计图表数据
   * @param {object} report - 扫描报告
   * @returns {object} 图表数据
   */
  getChartData(report) {
    return {
      labels: Object.keys(report.统计).filter(k => k !== '总计' && k !== '合计原创'),
      data: Object.values(report.统计).filter((v, i) => {
        const keys = Object.keys(report.统计);
        return keys[i] !== '总计' && keys[i] !== '合计原创';
      })
    };
  }
}

// 全局单例
window.assetScanner = new AssetScanner();
