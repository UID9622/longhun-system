/**
 * 🐉 CNSH 编辑器主逻辑 · Monaco 初始化 + 中文语法注册 + 菜单桥接
 * DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-EDITOR-JS-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

// 本地加载 Monaco（不绑境外CDN·主权铁律）
require.config({
  paths: { vs: '../../node_modules/monaco-editor/min/vs' }
});

require(['vs/editor/editor.main'], function () {
  const { cnshLanguage } = require('./cnsh-language.js');
  const DNAGenerator = require('./dna.js');
  const AuditEngine = require('./audit.js');

  // ===== 注册 CNSH 中文语言 =====
  monaco.languages.register({ id: 'cnsh' });

  monaco.languages.setMonarchTokensProvider('cnsh', {
    keywords: cnshLanguage.keywords,
    builtins: cnshLanguage.builtins,
    tokenizer: {
      root: [
        [/[a-zA-Z_]\w*/, 'identifier'],
        [/[0-9]+/, 'number'],
        [/"([^"\\]|\\.)*"/, 'string'],
        [/#.*$/, 'comment'],
        [
          /[函数类如果否则循环当返回导入从真假空且或非在使用作为尝试捕获最终抛出生成整数文本列表字典元组集合布尔浮点输出长度类型区间枚举压缩映射过滤求和最大值最小值排序反转打开读取写入关闭]/,
          { cases: { '@keywords': 'keyword', '@builtins': 'predefined' } }
        ],
        [/[＋－×÷＝≠＞＜≥≤并且或者取反属于不属于]/, 'operator'],
        [/\s+/, 'white']
      ]
    }
  });

  monaco.editor.defineTheme('longhun-dark', {
    base: 'vs-dark',
    inherit: true,
    rules: [
      { token: 'keyword', foreground: 'd4af37', fontStyle: 'bold' },
      { token: 'predefined', foreground: '7c9fff' },
      { token: 'string', foreground: '7ec699' },
      { token: 'comment', foreground: '5a5a6e', fontStyle: 'italic' },
      { token: 'number', foreground: 'e5c07b' },
      { token: 'operator', foreground: 'd4af37' }
    ],
    colors: { 'editor.background': '#0a0a14' }
  });

  // ===== 状态 =====
  let editor = null;
  let currentFilePath = null;
  let currentDna = '';

  // ===== 初始化编辑器 =====
  const container = document.getElementById('editor-container');
  editor = monaco.editor.create(container, {
    value: sampleCode(),
    language: 'cnsh',
    theme: 'longhun-dark',
    automaticLayout: true,
    fontSize: 15,
    fontFamily: "'PingFang SC', 'Microsoft YaHei', monospace",
    minimap: { enabled: true },
    scrollBeyondLastLine: false,
    tabSize: 4
  });

  // ===== 状态栏更新 =====
  function updateStatus() {
    const model = editor.getModel();
    document.getElementById('lineCount').textContent = model.getLineCount();
    document.getElementById('fileName').textContent = currentFilePath ? currentFilePath.split('/').pop() : '未命名.cnsh';
    // 实时审计
    const audit = AuditEngine.audit(model.getValue());
    const dot = document.getElementById('statusDot');
    dot.className = 'dot' + (audit.color === '🟢' ? '' : audit.color === '🟡' ? ' warning' : ' error');
    document.getElementById('statusText').textContent = audit.status;
    document.getElementById('auditDisplay').textContent = `${audit.color} 审计 ${audit.score}分`;
  }

  editor.onDidChangeModelContent(() => updateStatus());
  updateStatus();

  // ===== 菜单桥接 =====
  window.cnshAPI.onMenu(async (action) => {
    const model = editor.getModel();
    switch (action) {
      case 'new': {
        currentFilePath = null;
        currentDna = '';
        editor.setValue(sampleCode());
        updateStatus();
        break;
      }
      case 'open': {
        const result = await window.cnshAPI.openFile();
        if (result) {
          currentFilePath = result.path;
          editor.setValue(result.content);
        }
        break;
      }
      case 'save':
      case 'save-as': {
        const result = await window.cnshAPI.saveFile({ content: model.getValue(), path: currentFilePath });
        if (result.success) {
          currentFilePath = result.path;
          currentDna = await window.cnshAPI.generateDna({ content: model.getValue(), module: 'SAVE' });
          document.getElementById('statusDna').textContent = `🧬 DNA: ${currentDna}`;
        } else if (result.error) {
          alert(`保存失败: ${result.error}`);
        }
        break;
      }
      case 'export-c': {
        const cCode = await window.cnshAPI.compileToC({ content: model.getValue() });
        const result = await window.cnshAPI.saveFile({ content: cCode, path: currentFilePath ? currentFilePath.replace(/\.cnsh$/, '.c') : null });
        if (result.success) alert(`✅ 已导出C代码: ${result.path}`);
        break;
      }
      case 'generate-dna': {
        currentDna = await window.cnshAPI.generateDna({ content: model.getValue(), module: 'EDITOR' });
        document.getElementById('statusDna').textContent = `🧬 DNA: ${currentDna}`;
        document.getElementById('titleDna').textContent = currentDna;
        break;
      }
      case 'audit': {
        const audit = await window.cnshAPI.auditContent({ content: model.getValue() });
        alert(`${audit.color} 三色审计: ${audit.status} (${audit.score}分)\n\n${audit.issues.length ? '⚠️ ' + audit.issues.join('\n⚠️ ') : '✅ 全部通过'}`);
        break;
      }
      case 'sync-kunpeng': {
        const name = currentFilePath ? currentFilePath.split('/').pop() : 'untitled.cnsh';
        const result = await window.cnshAPI.syncKunpeng({ content: model.getValue(), filename: name });
        alert(result.success ? `✅ 已同步鲲鹏: ${result.message}` : `❌ 同步失败: ${result.error}`);
        break;
      }
      case 'sync-notion': {
        alert('🔄 Notion 同步需在龍魂环境中配置 token 后使用（API 入口: uid9622.cn/api/onboarding/bootstrap）');
        break;
      }
    }
  });

  // ===== 示例代码 =====
  function sampleCode() {
    return `# 🐉 龍魂 · CNSH 中文原生脚本示例
# DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-DEMO-UID9622

函数 问候(文本 姓名):
    输出("你好，" + 姓名 + "！欢迎使用龍魂CNSH编辑器")
    返回 真

类 计算器:
    整数 总数 = 0

    函数 加法(整数 甲, 整数 乙):
        整数 结果 = 甲 + 乙
        输出("相加结果: ", 结果)
        返回 结果

# 主流程
如果 真:
    问候("诸葛鑫")
    计算器 计算 = 新建 计算器()
    循环 整数 次数 从 1 到 3:
        计算.加法(次数, 次数 × 10)

当 假:
    输出("不会执行")
`;
  }
});
