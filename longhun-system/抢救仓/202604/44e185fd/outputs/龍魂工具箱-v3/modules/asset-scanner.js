// ===== 龍魂数字资产扫描器模块 =====

window.assetScanner = (function() {

  // 核心原创关键词
  const CORE_KEYWORDS = [
    'UID9622', '龍魂', '龍芯', '诸葛芯', 'ZHUGEXIN', '宝宝', '华仔',
    '太极算法', 'DNA追溯', '记忆压缩', '数据主权', '技术主权',
    '龍魂系统', '龍魂引擎', '龍魂协议', 'DragonSoul',
    '#龍芯⚡️', '#CONFIRM🌌9622'
  ];

  // 原创标记关键词
  const ORIGINAL_KEYWORDS = [
    '原创', 'Original', 'Copyright', '版权',
    'Author:', '作者:', 'Created by', '创建者',
    'DNA:', '#龍芯', 'UID9622'
  ];

  // 外部库/框架标记
  const EXTERNAL_MARKERS = [
    'node_modules', 'vendor', 'lib/', 'dist/',
    'jquery', 'react', 'vue', 'angular', 'bootstrap',
    'lodash', 'moment', 'axios', 'webpack'
  ];

  // 扫描单个文件
  async function scanFile(file) {
    return new Promise((resolve) => {
      const reader = new FileReader();
      reader.onload = (e) => {
        const content = e.target.result;
        const result = analyzeContent(content, file.name, file.size, file.lastModified);
        resolve(result);
      };
      reader.onerror = () => {
        resolve({
          文件: file.name,
          类型: '❓ 未标记',
          字符数: 0,
          文件大小: file.size,
          修改时间: new Date(file.lastModified).toLocaleString('zh-CN'),
          错误: '读取失败'
        });
      };
      reader.readAsText(file);
    });
  }

  // 分析内容
  function analyzeContent(content, filename, fileSize, lastModified) {
    const coreMatches = [];
    const originalMatches = [];
    const externalMatches = [];

    // 检测核心原创标记
    CORE_KEYWORDS.forEach(kw => {
      if (content.includes(kw)) {
        coreMatches.push(kw);
      }
    });

    // 检测原创标记
    ORIGINAL_KEYWORDS.forEach(kw => {
      if (content.includes(kw)) {
        originalMatches.push(kw);
      }
    });

    // 检测外部标记
    EXTERNAL_MARKERS.forEach(kw => {
      if (content.toLowerCase().includes(kw.toLowerCase())) {
        externalMatches.push(kw);
      }
    });

    // 判定类型
    let type;
    if (coreMatches.length >= 2) {
      type = '✅ 核心原创';
    } else if (coreMatches.length >= 1 || originalMatches.length >= 2) {
      type = '🟢 原创';
    } else if (originalMatches.length >= 1 && externalMatches.length >= 1) {
      type = '🟡 混合';
    } else if (externalMatches.length >= 1) {
      type = '📦 外部';
    } else {
      type = '❓ 未标记';
    }

    return {
      文件: filename,
      类型: type,
      字符数: content.length,
      文件大小: fileSize,
      修改时间: new Date(lastModified).toLocaleString('zh-CN'),
      核心标记: coreMatches,
      原创标记: [...coreMatches, ...originalMatches],
      外部标记: externalMatches,
      内容预览: content.substring(0, 200)
    };
  }

  // 批量扫描文件
  async function batchScanFiles(files) {
    const results = [];
    for (let i = 0; i < files.length; i++) {
      const result = await scanFile(files[i]);
      results.push(result);
    }
    return results;
  }

  // 生成报告
  function generateReport(results) {
    const stats = {
      '✅ 核心原创': 0,
      '🟢 原创': 0,
      '🟡 混合': 0,
      '📦 外部': 0,
      '❓ 未标记': 0,
      '总计': results.length,
      '合计原创': 0
    };

    results.forEach(r => {
      if (stats[r.类型] !== undefined) stats[r.类型]++;
    });
    stats['合计原创'] = stats['✅ 核心原创'] + stats['🟢 原创'];

    return {
      统计: stats,
      详情: results,
      生成时间: new Date().toISOString(),
      DNA: `#龍芯⚡️${new Date().toISOString().split('T')[0]}-SCAN-REPORT`
    };
  }

  // 搜索关键词
  function searchKeyword(keyword, results) {
    return results.filter(r =>
      r.文件.includes(keyword) ||
      (r.核心标记 && r.核心标记.some(m => m.includes(keyword))) ||
      (r.原创标记 && r.原创标记.some(m => m.includes(keyword))) ||
      (r.内容预览 && r.内容预览.includes(keyword))
    );
  }

  // 导出为 JSON
  function exportReportToJSON(report) {
    return JSON.stringify(report, null, 2);
  }

  // 导出为 Markdown
  function exportReportToMarkdown(report) {
    let md = `# 🐲 龍魂数字资产扫描报告\n\n`;
    md += `**生成时间:** ${report.生成时间}\n`;
    md += `**DNA:** ${report.DNA}\n\n`;
    md += `## 统计概览\n\n`;
    md += `| 类型 | 数量 |\n|------|------|\n`;
    Object.entries(report.统计).forEach(([key, val]) => {
      md += `| ${key} | ${val} |\n`;
    });
    md += `\n## 详细结果\n\n`;
    report.详情.forEach(item => {
      md += `### ${item.文件}\n`;
      md += `- 类型: ${item.类型}\n`;
      md += `- 字符数: ${item.字符数}\n`;
      md += `- 标记: ${item.原创标记.join(', ') || '无'}\n\n`;
    });
    return md;
  }

  return {
    scanFile, batchScanFiles, analyzeContent, generateReport,
    searchKeyword, exportReportToJSON, exportReportToMarkdown
  };
})();
