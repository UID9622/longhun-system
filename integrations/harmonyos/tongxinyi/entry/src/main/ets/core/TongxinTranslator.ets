/*
 * ==========================================================================
 * 通心译 — 主翻译器 (TongxinTranslator)
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-TRANSLATOR-v1.0
 * ==========================================================================
 * 核心翻译引擎，实现中文 ⟷ 英文双向翻译。
 * 遵循五大铁律，不是镜像翻译，而是追求"共鸣"。
 * 华为芯片+鸿蒙底座:
 *   - 数据存储于设备沙箱 (S4安全级别)
 *   - SM4国产加密·敏感数据永不出境
 *   - 端侧推理·离线可用
 * ==========================================================================
 */

import {
  TranslationMode, TranslationResult,
  AuditLevel, DRAGON_SOUL_MARKS
} from '../common/types';
import { TerminologyDatabase } from './TerminologyDatabase';
import { DNACodeGenerator } from './DNACodeGenerator';
import { CulturalAdapter } from './CulturalAdapter';
import { QualityAuditor } from './QualityAuditor';

export class TongxinTranslator {
  public db: TerminologyDatabase;
  public dna: DNACodeGenerator;
  public cultural: CulturalAdapter;
  public auditor: QualityAuditor;

  // 代码保留模式 (不翻译)
  private readonly codePatterns: RegExp[] = [
    /\b(def|class|import|from|return|if|else|elif|for|while|try|except|finally|with|as|lambda|yield|async|await|print|len|range|open|True|False|None)\b/,
    /[#"'\\]/,
    /\b\d+\b/,
    /[=+\-*/<>!&|{}[\]().,;:]/
  ];

  // 龍魂标记 (不翻译)
  private readonly sacredMarks: string[] = [
    DRAGON_SOUL_MARKS.DNA,
    DRAGON_SOUL_MARKS.CONFIRM,
    DRAGON_SOUL_MARKS.SEAL
  ];

  constructor() {
    this.db = new TerminologyDatabase();
    this.dna = new DNACodeGenerator();
    this.cultural = new CulturalAdapter();
    this.auditor = new QualityAuditor();
  }

  /**
   * 核心翻译函数
   * @param text 要翻译的文本
   * @param mode 翻译模式
   * @param applyCultural 是否应用文化适配
   * @param applyAudit 是否进行质量审计
   */
  translate(
    text: string,
    mode: TranslationMode = TranslationMode.EN_TO_ZH,
    applyCultural: boolean = true,
    applyAudit: boolean = true
  ): TranslationResult {
    if (!text || text.trim().length === 0) {
      return this.createEmptyResult(text, mode);
    }

    let translated: string = '';

    if (mode === TranslationMode.EN_TO_ZH) {
      translated = this.translateENtoZH(text);
      if (applyCultural) translated = this.cultural.adaptToChinese(translated);
    } else if (mode === TranslationMode.ZH_TO_EN) {
      translated = this.translateZHtoEN(text);
      if (applyCultural) translated = this.cultural.adaptToEnglish(translated);
    } else if (mode === TranslationMode.BILINGUAL) {
      const zhPart = this.translateENtoZH(text);
      translated = this.formatBilingual(
        applyCultural ? this.cultural.adaptToChinese(zhPart) : zhPart,
        text
      );
    }

    // 审计
    let auditLevel: AuditLevel = AuditLevel.GREEN;
    let auditScore: number = 100;
    if (applyAudit) {
      const auditReport = this.auditor.auditTranslation(text, translated, mode);
      const lastRecord = this.auditor.getAuditHistory().slice(-1)[0];
      if (lastRecord) {
        auditLevel = lastRecord.level;
        auditScore = lastRecord.score;
      }
    }

    // 生成DNA
    const dnaCode = this.dna.generateDNACode(text, mode);

    return {
      original: text,
      translated,
      mode,
      dnaCode,
      auditLevel,
      auditScore,
      timestamp: Date.now()
    };
  }

  /** 英文 → 中文翻译 */
  private translateENtoZH(text: string): string {
    const fragments = this.tokenizeMixed(text);
    const parts: string[] = [];

    for (const [fragment, translatable] of fragments) {
      if (!translatable || !this.shouldTranslate(fragment)) {
        parts.push(fragment);
        continue;
      }

      const lookup = this.db.lookupEN(fragment);
      if (lookup) {
        parts.push(lookup);
        continue;
      }

      // 尝试小写
      const lookupLower = this.db.lookupEN(fragment.toLowerCase());
      if (lookupLower) {
        parts.push(lookupLower);
        continue;
      }

      // 复合词分解
      parts.push(this.decomposeAndTranslate(fragment, 'en2zh'));
    }

    return parts.join('');
  }

  /** 中文 → 英文翻译 */
  private translateZHtoEN(text: string): string {
    const result: string[] = [];
    let i: number = 0;

    while (i < text.length) {
      let matched: boolean = false;

      // 最长匹配 (最多8个字符)
      for (let length = Math.min(8, text.length - i); length > 0; length--) {
        const substr = text.substring(i, i + length);
        const lookup = this.db.lookupZH(substr);
        if (lookup) {
          result.push(lookup);
          i += length;
          matched = true;
          break;
        }
      }

      if (!matched) {
        const char = text.charAt(i);
        // 主权字映射
        if (char === '龍') result.push('Dragon');
        else if (char === '芯') result.push('Core');
        else if (char === '魂') result.push('Soul');
        else result.push(char);
        i++;
      }
    }

    return result.join('');
  }

  /** 快速翻译 (无需DNA签证，内部调用) */
  quickTranslate(text: string): string {
    if (!text || text.trim().length === 0) return '';

    // 自动检测语言
    const cnMatches = text.match(/[\u4e00-\u9fff]/g);
    const cnRatio: number = cnMatches ? cnMatches.length / text.length : 0;

    if (cnRatio > 0.3) {
      return this.translateZHtoEN(text);
    } else {
      return this.translateENtoZH(text);
    }
  }

  /** 解释术语 (铁律3: 比喻优先于公式) */
  explainTerm(term: string): string {
    const enLookup = this.db.lookupEN(term);
    const zhLookup = this.db.lookupZH(term);

    let output = `【通心译 · 术语释义】\n\n📖 术语: ${term}\n`;

    if (zhLookup) {
      output += `🈯 中文: ${zhLookup}\n`;
      const zhExpl = this.db.getZHExplanation(zhLookup);
      if (zhExpl) output += `🐉 中文解读:\n  ${zhExpl}\n`;
    }

    if (enLookup) {
      output += `🔤 英文: ${enLookup}\n`;
      const enExpl = this.db.getENExplanation(enLookup);
      if (enExpl) output += `🌍 英文解读:\n  ${enExpl}\n`;
    }

    if (!zhLookup && !enLookup) {
      output += `\n术语 "${term}" 暂无解释。\n铁律5: 永远在线，永远迭代 — 您可以为此术语贡献解释！`;
    }

    return output;
  }

  /** 搜索术语 */
  searchTerms(keyword: string): Array<{ en: string; zh: string }> {
    return this.db.searchTerm(keyword);
  }

  /** 获取术语全文映射 */
  getFullTermMapping(): string {
    let output = `📚 通心译术语映射表 (${this.db.getTermCount()}对术语)\n\n`;
    const categories = this.db.getCategories();

    for (const cat of categories) {
      const terms = this.db.getCategoryTerms(cat);
      output += `【${cat}】(${terms.size}个)\n`;
      let i = 1;
      for (const [en, zh] of terms.entries()) {
        output += `  ${String(i).padStart(2, ' ')}. ${en.padEnd(25)} ↔ ${zh}\n`;
        i++;
      }
      output += '\n';
    }

    return output;
  }

  /** 切分混合文本 */
  private tokenizeMixed(text: string): Array<[string, boolean]> {
    const fragments: Array<[string, boolean]> = [];
    const pattern = /([\u4e00-\u9fff]+)|([a-zA-Z_][a-zA-Z0-9_]*)|([^\w\u4e00-\u9fff]+)/g;
    let match;

    while ((match = pattern.exec(text)) !== null) {
      if (match[1]) fragments.push([match[1], true]);
      else if (match[2]) fragments.push([match[2], true]);
      else if (match[3]) fragments.push([match[3], false]);
    }

    return fragments.length > 0 ? fragments : [[text, true]];
  }

  /** 判断是否应翻译 */
  private shouldTranslate(word: string): boolean {
    for (const mark of this.sacredMarks) {
      if (word.includes(mark)) return false;
    }
    for (const pattern of this.codePatterns) {
      if (pattern.test(word)) return false;
    }
    return true;
  }

  /** 分解复合词并翻译 */
  private decomposeAndTranslate(text: string, direction: string): string {
    if (direction === 'en2zh') {
      // camelCase / snake_case 分解
      const words = text.match(/[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)/g);
      if (!words) return text;

      const translated: string[] = [];
      for (const w of words) {
        const lookup = this.db.lookupEN(w.toLowerCase());
        translated.push(lookup || w);
      }
      return translated.join('');
    }
    return text;
  }

  /** 格式化双语输出 */
  private formatBilingual(zhText: string, enText: string): string {
    return `### 中文\n**${zhText}**\n\n> *✦ Tongxin Translation — 通心译 ✦*\n> *不是镜像，是共鸣 | Not mirror, but resonance*\n\n### English\n**${enText}**`;
  }

  /** 生成完整页眉 */
  getHeader(): string {
    return this.dna.generateFullHeader();
  }

  /** 创建空结果 */
  private createEmptyResult(text: string, mode: TranslationMode): TranslationResult {
    return {
      original: text,
      translated: '',
      mode,
      dnaCode: DRAGON_SOUL_MARKS.DNA,
      auditLevel: AuditLevel.YELLOW,
      auditScore: 0,
      timestamp: Date.now()
    };
  }
}
