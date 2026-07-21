/*
 * ==========================================================================
 * 通心译 — 学习引擎 (铁律5: 永远在线·永远迭代)
 * DNA:#龍芯⚡️丙午·丙申·癸丑·午时·需-TONGXINYI-LEARN-v1.0
 * ==========================================================================
 * 功能: 记录用户反馈 / 学习用户偏好 / 动态优化翻译 / 术语库自我扩展
 * 反馈类型: 👍好评 / 👎差评 / 💡建议 / 🌟新术语
 * 鸿蒙底座: 学习数据存储在设备沙箱·永不出境
 * ==========================================================================
 */

import { preferences } from '@kit.ArkData';
import { LearningFeedback, UserPreferences, TranslationMode } from '../common/types';

const PREF_NAME: string = 'tongxin_learning';
const MAX_FEEDBACK_HISTORY: number = 100;

export class LearningEngine {
  private feedbackHistory: LearningFeedback[] = [];
  private userPreferences: UserPreferences = {
    preferredMode: TranslationMode.BILINGUAL,
    culturalStrictness: 'normal',
    sovereignCharPreference: 'auto',
    favoriteTerms: {},
    avoidedTerms: {}
  };
  private termFrequency: Record<string, number> = {};
  private context: Context | null = null;

  /**
   * 初始化学习引擎
   * @param context 应用上下文 (用于preferences存储)
   */
  async initialize(context: Context): Promise<void> {
    this.context = context;
    await this.loadMemory();
  }

  /** 加载学习记忆 */
  private async loadMemory(): Promise<void> {
    if (!this.context) return;

    try {
      const prefs = await preferences.getPreferences(this.context, PREF_NAME);
      const dataStr: string = prefs.getSync('learning_data', '') as string;
      if (dataStr) {
        const data = JSON.parse(dataStr);
        this.feedbackHistory = data.feedback || [];
        if (data.preferences) {
          this.userPreferences = { ...this.userPreferences, ...data.preferences };
        }
        this.termFrequency = data.termFrequency || {};
      }
    } catch {
      // 首次加载，使用默认设置
    }
  }

  /** 保存学习记忆 */
  private async saveMemory(): Promise<void> {
    if (!this.context) return;

    try {
      const prefs = await preferences.getPreferences(this.context, PREF_NAME);
      const data = JSON.stringify({
        feedback: this.feedbackHistory.slice(-MAX_FEEDBACK_HISTORY),
        preferences: this.userPreferences,
        termFrequency: this.termFrequency,
        lastUpdated: new Date().toISOString()
      });
      prefs.putSync('learning_data', data);
      await prefs.flush();
    } catch {
      // 静默失败
    }
  }

  /** 记录用户反馈 */
  async recordFeedback(
    original: string,
    translated: string,
    feedbackType: '👍' | '👎' | '💡' | '🌟',
    comment: string = ''
  ): Promise<void> {
    const record: LearningFeedback = {
      timestamp: Date.now(),
      original,
      translated,
      feedbackType,
      comment
    };
    this.feedbackHistory.push(record);

    if (feedbackType === '👍') {
      this.processPositiveFeedback(translated);
    } else if (feedbackType === '👎') {
      this.processNegativeFeedback(original, translated, comment);
    }

    await this.saveMemory();
  }

  /** 处理正面反馈 */
  private processPositiveFeedback(translated: string): void {
    const terms: string[] = this.extractTerms(translated);
    for (const term of terms) {
      this.termFrequency[term] = (this.termFrequency[term] || 0) + 1;
    }
  }

  /** 处理负面反馈 */
  private processNegativeFeedback(original: string, translated: string, comment: string): void {
    this.userPreferences.avoidedTerms[original] = {
      badTranslation: translated,
      reason: comment
    };
  }

  /** 从文本中提取术语 */
  private extractTerms(text: string): string[] {
    const matches = text.match(/[\u4e00-\u9fff]{2,}/g);
    return matches || [];
  }

  /** 获取用户偏好 */
  getPreference<K extends keyof UserPreferences>(key: K): UserPreferences[K] {
    return this.userPreferences[key];
  }

  /** 设置用户偏好 */
  async setPreference<K extends keyof UserPreferences>(key: K, value: UserPreferences[K]): Promise<void> {
    this.userPreferences[key] = value;
    await this.saveMemory();
  }

  /** 生成学习报告 */
  generateLearningReport(): string {
    const total: number = this.feedbackHistory.length;
    const positive: number = this.feedbackHistory.filter(f => f.feedbackType === '👍').length;
    const negative: number = this.feedbackHistory.filter(f => f.feedbackType === '👎').length;
    const suggestions: number = this.feedbackHistory.filter(f => f.feedbackType === '💡').length;

    const topTerms = Object.entries(this.termFrequency)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);

    let report = `╔══════════════════════════════════════════╗\n`;
    report += `║   通心译 · 学习报告 (Learning Report)   ║\n`;
    report += `╚══════════════════════════════════════════╝\n\n`;
    report += `📊 反馈统计:\n`;
    report += `  总反馈数: ${total}\n`;
    report += `  👍 好评: ${positive}\n`;
    report += `  👎 差评: ${negative}\n`;
    report += `  💡 建议: ${suggestions}\n`;
    report += `  满意度: ${total > 0 ? (positive/total*100).toFixed(1) : '0.0'}%\n\n`;

    report += `📚 高频术语 (Top ${topTerms.length}):\n`;
    if (topTerms.length === 0) {
      report += `  (暂无数据)\n`;
    } else {
      topTerms.forEach(([term, freq], i) => {
        report += `  ${i + 1}. ${term} — 使用 ${freq} 次\n`;
      });
    }

    report += `\n⚙️ 当前偏好:\n`;
    report += `  翻译模式: ${this.userPreferences.preferredMode}\n`;
    report += `  文化严格度: ${this.userPreferences.culturalStrictness}\n`;
    report += `  主权字偏好: ${this.userPreferences.sovereignCharPreference}\n`;

    return report;
  }
}
