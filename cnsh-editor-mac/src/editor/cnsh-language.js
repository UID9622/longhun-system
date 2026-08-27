# 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
/**
 * 🐉 CNSH 语言语法定义 for Monaco Editor
 * 100%中文关键字高亮 · DNA: #龍芯⚡️丙午·丙申·辛酉·己丑·䷹兑为泽-CNSH-LANG-UID9622
 * License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
 */

// 全局变量 · Monaco AMD 加载器注册语言
(function () {
  const cnshLanguage = {
    // 中文关键字
    keywords: [
      '函数', '类', '如果', '否则', '否则如果', '循环', '当', '返回',
      '导入', '从', '真', '假', '空', '且', '或', '非', '在', '是',
      '使用', '作为', '尝试', '捕获', '最终', '抛出', '生成',
      '整数', '文本', '列表', '字典', '元组', '集合', '布尔', '浮点',
      '输出', '长度', '类型', '区间', '枚举', '压缩', '映射', '过滤',
      '求和', '最大值', '最小值', '排序', '反转', '打开', '读取', '写入', '关闭'
    ],

    // 操作符
    operators: [
      '＋', '－', '×', '÷', '＝', '≠', '＞', '＜', '≥', '≤',
      '并且', '或者', '取反', '属于', '不属于'
    ],

    // 内置函数
    builtins: [
      '输出', '长度', '类型', '整数', '文本', '列表', '字典',
      '区间', '枚举', '压缩', '映射', '过滤', '求和', '最大值', '最小值',
      '排序', '反转', '打开', '读取', '写入', '关闭'
    ],

    // 注释
    comments: {
      lineComment: '#',
      blockComment: ['/*', '*/']
    },

    // 字符串
    strings: {
      double: ['"', '"']
    },

    // 数字
    numbers: /[0-9]+/
  };

  // 导出供 Monaco register 与模块化使用
  if (typeof window !== 'undefined') {
    window.cnshLanguage = cnshLanguage;
  }
  if (typeof module !== 'undefined' && module.exports) {
    module.exports = cnshLanguage;
  }
})();
