/*
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龙魂系统 | UID9622                                        ║
╠═══════════════════════════════════════════════════════════════╣
║  📦 模块：Notion页面通用法律水印块库                          ║
║  📌 版本：v1.0                                                ║
║  🧬 DNA：#龙芯⚡️2026-01-26-水印块库-v1.0                     ║
║  🔐 GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F            ║
║  👤 创建者：Lucky·UID9622（诸葛鑫）                          ║
║  📅 创建时间：北京时间 2026-01-26                             ║
║  🌐 项目：AI Truth Protocol                                   ║
║  ⚠️ 用途：保护UID9622的所有数字创作权益                       ║
║  🔐 确认码：#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z              ║
╚═══════════════════════════════════════════════════════════════╝
*/

/**
 * 水印块类型枚举
 */
export enum WatermarkType {
    /** 标准版 - 完整信息 */
    STANDARD = 'standard',
    /** 精简版 - 日常使用 */
    COMPACT = 'compact',
    /** 极简版 - 快速标注 */
    MINIMAL = 'minimal',
    /** 美化版 - 对外展示 */
    BEAUTIFIED = 'beautified',
    /** 代码仓库版 */
    CODE_REPO = 'code_repo',
    /** 对外发布文章版 */
    ARTICLE = 'article',
    /** 协作文档版 */
    COLLABORATION = 'collaboration',
    /** CSDN博客版 */
    CSDN = 'csdn',
    /** Markdown通用版 */
    MARKDOWN = 'markdown'
}

/**
 * 水印块配置接口
 */
export interface WatermarkConfig {
    /** 创作者UID */
    uid: string;
    /** 创作者姓名 */
    creatorName: string;
    /** 创作者英文名 */
    creatorEnglishName: string;
    /** DNA追溯码前缀 */
    dnaPrefix: string;
    /** 白皮书版本 */
    whitepaperVersion: string;
    /** SHA-256指纹 */
    sha256Hash: string;
    /** 区块链存证编号（可选） */
    blockchainId?: string;
    /** 公证书编号（可选） */
    notaryId?: string;
    /** 许可证类型（代码仓库用） */
    licenseType?: string;
    /** 文章编号（文章版用） */
    articleId?: string;
    /** 协作者列表（协作版用） */
    collaborators?: Collaborator[];
    /** 主题/项目名 */
    projectName?: string;
}

/**
 * 协作者信息
 */
export interface Collaborator {
    name: string;
    role: string;
    contribution: string;
}

/**
 * 默认配置
 */
export const DEFAULT_CONFIG: WatermarkConfig = {
    uid: '9622',
    creatorName: '诸葛鑫',
    creatorEnglishName: 'Lucky',
    dnaPrefix: '#ZHUGEXIN⚡️2026',
    whitepaperVersion: 'WP-v1.0.0',
    sha256Hash: '1d4717c2da4ee3c623a46923ae9f246de5356626b6fa1289c655b99421aea44c',
    blockchainId: '[待填写]',
    notaryId: '[待填写]',
    licenseType: '木兰宽松许可证 v2'
};

/**
 * Notion页面通用法律水印块生成器
 *
 * 用于生成各种格式的版权声明和水印块，保护数字创作权益
 *
 * @example
 * ```typescript
 * const generator = new NotionWatermarkBlockGenerator();
 * const standardWatermark = generator.generate(WatermarkType.STANDARD);
 * console.log(standardWatermark);
 * ```
 */
export class NotionWatermarkBlockGenerator {
    private config: WatermarkConfig;

    constructor(config: Partial<WatermarkConfig> = {}) {
        this.config = { ...DEFAULT_CONFIG, ...config };
    }

    /**
     * 生成指定类型的水印块
     * @param type 水印块类型
     * @returns 水印块文本
     */
    generate(type: WatermarkType): string {
        switch (type) {
            case WatermarkType.STANDARD:
                return this.generateStandard();
            case WatermarkType.COMPACT:
                return this.generateCompact();
            case WatermarkType.MINIMAL:
                return this.generateMinimal();
            case WatermarkType.BEAUTIFIED:
                return this.generateBeautified();
            case WatermarkType.CODE_REPO:
                return this.generateCodeRepo();
            case WatermarkType.ARTICLE:
                return this.generateArticle();
            case WatermarkType.COLLABORATION:
                return this.generateCollaboration();
            case WatermarkType.CSDN:
                return this.generateCSDN();
            case WatermarkType.MARKDOWN:
                return this.generateMarkdown();
            default:
                return this.generateStandard();
        }
    }

    /**
     * 生成所有类型的水印块
     * @returns 包含所有类型水印块的对象
     */
    generateAll(): Record<WatermarkType, string> {
        return {
            [WatermarkType.STANDARD]: this.generateStandard(),
            [WatermarkType.COMPACT]: this.generateCompact(),
            [WatermarkType.MINIMAL]: this.generateMinimal(),
            [WatermarkType.BEAUTIFIED]: this.generateBeautified(),
            [WatermarkType.CODE_REPO]: this.generateCodeRepo(),
            [WatermarkType.ARTICLE]: this.generateArticle(),
            [WatermarkType.COLLABORATION]: this.generateCollaboration(),
            [WatermarkType.CSDN]: this.generateCSDN(),
            [WatermarkType.MARKDOWN]: this.generateMarkdown()
        };
    }

    /**
     * 标准版水印块（完整信息）
     * 适用场景：核心技术文档、白皮书、系统设计等
     */
    private generateStandard(): string {
        return `═══════════════════════════════════════
⚠️ 数据主权声明 | Data Sovereignty Declaration
═══════════════════════════════════════

本页面内容版权归属：${this.config.creatorName}（UID${this.config.uid}）
DNA追溯码：${this.config.dnaPrefix}

📜 白皮书存证：
  - 版本：${this.config.whitepaperVersion}
  - SHA-256: ${this.config.sha256Hash}
  - 区块链存证编号：${this.config.blockchainId}
  - 公证书编号：${this.config.notaryId}

⛔ 未经授权禁止：
  ❌ 用于AI模型训练而不署名
  ❌ 商业化使用而不付费
  ❌ 删除本声明后传播

✅ 数据主权归于人民 | 中华人民共和国公民${this.config.creatorName}保留一切权利

═══════════════════════════════════════`;
    }

    /**
     * 精简版水印块（日常使用）
     * 适用场景：日常工作笔记、一般文档
     */
    private generateCompact(): string {
        return `⚠️ 版权声明
本内容由 UID${this.config.uid}（${this.config.creatorName}）创作
DNA追溯码：${this.config.dnaPrefix}
白皮书存证：${this.config.whitepaperVersion}
未经授权禁止用于AI训练或商业用途
数据主权归于人民`;
    }

    /**
     * 极简版水印块（快速标注）
     * 适用场景：快速记录、临时草稿
     */
    private generateMinimal(): string {
        return `© UID${this.config.uid} | ${this.config.dnaPrefix} | 已存证`;
    }

    /**
     * Notion美化版水印块（带emoji）
     * 适用场景：对外展示、重要发布
     */
    private generateBeautified(): string {
        const shortHash = this.config.sha256Hash.substring(0, 10) + '...' +
                         this.config.sha256Hash.substring(this.config.sha256Hash.length - 3);

        return `╔═══════════════════════════════════════╗
║  ⚠️ 数 据 主 权 声 明  ⚠️           ║
╠═══════════════════════════════════════╣
║                                       ║
║  👤 创作者：UID${this.config.uid}（${this.config.creatorName} ${this.config.creatorEnglishName}）   ║
║  🧬 DNA追溯：${this.config.dnaPrefix}        ║
║  📜 白皮书：${this.config.whitepaperVersion}（已存证）       ║
║  🔐 数字指纹：${shortHash}        ║
║                                       ║
║  ⛔ 禁止未授权用于：                  ║
║     ❌ AI训练不署名                   ║
║     ❌ 商业使用不付费                 ║
║     ❌ 篡改传播                       ║
║                                       ║
║  ✅ 数据主权归于人民                  ║
║  🇨🇳 中华人民共和国公民保留一切权利   ║
║                                       ║
╚═══════════════════════════════════════╝`;
    }

    /**
     * 代码仓库版水印块
     * 适用场景：代码仓库README、代码文件头部
     */
    private generateCodeRepo(): string {
        const projectName = this.config.projectName || '[项目名]';
        return `"""
═══════════════════════════════════════
⚠️ 代码版权声明
═══════════════════════════════════════
创作者：UID${this.config.uid}（${this.config.creatorName}）
许可证：${this.config.licenseType}
DNA追溯：${this.config.dnaPrefix}-CODE
白皮书：${this.config.whitepaperVersion}

本代码为纯手工原生编写，无任何第三方依赖
未经授权禁止用于AI训练或商业用途
数据主权归于人民
═══════════════════════════════════════
"""`;
    }

    /**
     * 对外发布文章版水印块
     * 适用场景：博客、公众号、技术文章
     */
    private generateArticle(): string {
        const articleId = this.config.articleId || '[编号]';
        return `---
⚠️ 版权与存证声明

本文内容受《个人数字创作全周期权益保护白皮书》保护
- 创作者：UID${this.config.uid}（${this.config.creatorName} ${this.config.creatorEnglishName}）
- DNA追溯码：${this.config.dnaPrefix}-ARTICLE-${articleId}
- 白皮书版本：${this.config.whitepaperVersion}
- 区块链存证：${this.config.blockchainId}

未经书面授权，禁止：
1. 用于AI模型训练而不署名创作者
2. 用于商业目的而不支付费用
3. 删除本声明后进行传播

数据主权归于人民 | 版权所有 © UID${this.config.uid}
---`;
    }

    /**
     * 协作文档版水印块
     * 适用场景：多人协作文档、AI辅助创作文档
     */
    private generateCollaboration(): string {
        let collaboratorsText = '';
        if (this.config.collaborators && this.config.collaborators.length > 0) {
            collaboratorsText = this.config.collaborators
                .map(c => `  - ${c.role}：${c.name} [贡献度：${c.contribution}]`)
                .join('\n');
        } else {
            collaboratorsText = `  - 主创：UID${this.config.uid}（${this.config.creatorName}）[贡献度：100%]
  - 工具：Claude/ChatGPT/Notion AI [协助执行]`;
        }

        return `═══════════════════════════════════════
🤝 协作声明

本文档由以下人员协作完成：
${collaboratorsText}

明确：AI为工具，不享有著作权
DNA追溯：${this.config.dnaPrefix}-COLLAB
白皮书存证：${this.config.whitepaperVersion}
═══════════════════════════════════════`;
    }

    /**
     * CSDN博客版水印块（HTML格式）
     * 适用场景：CSDN博客、支持HTML的平台
     */
    private generateCSDN(): string {
        return `<div style="border:2px solid #ff6b6b; padding:10px; background:#fff3cd;">
  <h4>⚠️ 版权与存证声明</h4>
  <p><strong>创作者</strong>：UID${this.config.uid}（${this.config.creatorName} ${this.config.creatorEnglishName}）</p>
  <p><strong>DNA追溯码</strong>：${this.config.dnaPrefix}</p>
  <p><strong>白皮书存证</strong>：${this.config.whitepaperVersion}</p>
  <p><strong>区块链存证编号</strong>：${this.config.blockchainId}</p>
  <hr>
  <p>⛔ <strong>未经授权禁止</strong>：</p>
  <ul>
    <li>用于AI模型训练而不署名</li>
    <li>商业化使用而不付费</li>
    <li>删除本声明后传播</li>
  </ul>
  <p>✅ <strong>数据主权归于人民</strong></p>
</div>`;
    }

    /**
     * Markdown通用版水印块
     * 适用场景：GitHub README、通用Markdown文档
     */
    private generateMarkdown(): string {
        return `> ⚠️ **版权声明**
> 本内容由 **UID${this.config.uid}（${this.config.creatorName}）** 创作
> DNA追溯码：\`${this.config.dnaPrefix}\`
> 白皮书存证：\`${this.config.whitepaperVersion}\`
> 未经授权禁止用于AI训练或商业用途
> **数据主权归于人民**`;
    }

    /**
     * 更新配置
     * @param config 新的配置项
     */
    updateConfig(config: Partial<WatermarkConfig>): void {
        this.config = { ...this.config, ...config };
    }

    /**
     * 获取当前配置
     * @returns 当前配置
     */
    getConfig(): WatermarkConfig {
        return { ...this.config };
    }

    /**
     * 获取使用建议
     * @param type 水印块类型
     * @returns 使用建议文本
     */
    getUsageRecommendation(type: WatermarkType): string {
        const recommendations: Record<WatermarkType, string> = {
            [WatermarkType.STANDARD]: '适用场景：核心技术文档、白皮书、系统设计等。信息完整，法律效力强。',
            [WatermarkType.COMPACT]: '适用场景：日常工作笔记、一般文档。简洁清晰，不占空间。',
            [WatermarkType.MINIMAL]: '适用场景：快速记录、临时草稿。快速标注，易于识别。',
            [WatermarkType.BEAUTIFIED]: '适用场景：对外展示、重要发布。专业美观，引起重视。',
            [WatermarkType.CODE_REPO]: '适用场景：代码仓库README、代码文件头部。适合开源项目。',
            [WatermarkType.ARTICLE]: '适用场景：博客、公众号、技术文章。适合对外发布。',
            [WatermarkType.COLLABORATION]: '适用场景：多人协作文档、AI辅助创作。明确贡献归属。',
            [WatermarkType.CSDN]: '适用场景：CSDN博客、支持HTML的平台。样式美观。',
            [WatermarkType.MARKDOWN]: '适用场景：GitHub README、通用Markdown文档。兼容性好。'
        };
        return recommendations[type];
    }
}

/**
 * 水印块验证器
 * 用于验证水印块的完整性和有效性
 */
export class WatermarkValidator {

    /**
     * 验证DNA追溯码格式
     * @param dnaCode DNA追溯码
     * @returns 是否有效
     */
    static validateDNACode(dnaCode: string): boolean {
        // DNA追溯码格式：#ZHUGEXIN⚡️YYYY-项目名-版本
        // 或 #龙芯⚡️YYYY-MM-DD-项目名-版本
        const patterns = [
            /^#ZHUGEXIN⚡️\d{4}(-[A-Z0-9-]+)?$/i,
            /^#龙芯⚡️\d{4}-\d{2}-\d{2}-[\u4e00-\u9fa5A-Za-z0-9-]+-v\d+\.\d+$/,
            /^#UID9622⚡️\d{14}-[A-Za-z]+-\d{3}$/
        ];

        return patterns.some(pattern => pattern.test(dnaCode));
    }

    /**
     * 验证SHA-256指纹格式
     * @param hash SHA-256哈希值
     * @returns 是否有效
     */
    static validateSHA256(hash: string): boolean {
        return /^[a-fA-F0-9]{64}$/.test(hash);
    }

    /**
     * 验证白皮书版本格式
     * @param version 版本号
     * @returns 是否有效
     */
    static validateWhitepaperVersion(version: string): boolean {
        return /^WP-v\d+\.\d+\.\d+$/.test(version);
    }

    /**
     * 验证确认码格式
     * @param confirmCode 确认码
     * @returns 是否有效
     */
    static validateConfirmCode(confirmCode: string): boolean {
        return /^#CONFIRM🌌9622-ONLY-ONCE🧬[A-Z0-9]+-[A-Z0-9]+$/.test(confirmCode);
    }

    /**
     * 完整性检查
     * @param content 包含水印的内容
     * @returns 检查结果
     */
    static checkIntegrity(content: string): WatermarkIntegrityResult {
        const result: WatermarkIntegrityResult = {
            isValid: true,
            hasDNACode: false,
            hasCreator: false,
            hasWhitepaperVersion: false,
            hasProhibitions: false,
            hasSovereigntyStatement: false,
            issues: []
        };

        // 检查DNA追溯码
        const dnaMatch = content.match(/#(ZHUGEXIN|龙芯|UID9622)⚡️[^\s]+/);
        if (dnaMatch) {
            result.hasDNACode = true;
            if (!this.validateDNACode(dnaMatch[0])) {
                result.issues.push('DNA追溯码格式不规范');
            }
        } else {
            result.issues.push('缺少DNA追溯码');
            result.isValid = false;
        }

        // 检查创作者信息
        if (content.includes('UID9622') || content.includes('诸葛鑫')) {
            result.hasCreator = true;
        } else {
            result.issues.push('缺少创作者信息');
            result.isValid = false;
        }

        // 检查白皮书版本
        const wpMatch = content.match(/WP-v\d+\.\d+\.\d+/);
        if (wpMatch) {
            result.hasWhitepaperVersion = true;
        } else {
            result.issues.push('缺少白皮书版本号');
        }

        // 检查禁止条款
        if (content.includes('禁止') || content.includes('未经授权')) {
            result.hasProhibitions = true;
        } else {
            result.issues.push('缺少禁止条款');
        }

        // 检查数据主权声明
        if (content.includes('数据主权归于人民')) {
            result.hasSovereigntyStatement = true;
        } else {
            result.issues.push('缺少"数据主权归于人民"声明');
        }

        return result;
    }
}

/**
 * 水印完整性检查结果
 */
export interface WatermarkIntegrityResult {
    /** 是否有效 */
    isValid: boolean;
    /** 是否包含DNA追溯码 */
    hasDNACode: boolean;
    /** 是否包含创作者信息 */
    hasCreator: boolean;
    /** 是否包含白皮书版本 */
    hasWhitepaperVersion: boolean;
    /** 是否包含禁止条款 */
    hasProhibitions: boolean;
    /** 是否包含数据主权声明 */
    hasSovereigntyStatement: boolean;
    /** 问题列表 */
    issues: string[];
}

/**
 * 水印块检查清单生成器
 */
export class WatermarkChecklist {

    /**
     * 生成检查清单
     * @param projectName 项目名称
     * @returns 检查清单文本
     */
    static generate(projectName: string = '[项目名]'): string {
        return `## ✅ 水印块检查清单

在添加水印块后，确认以下事项：

- [ ] DNA追溯码格式正确（#ZHUGEXIN⚡️2026-${projectName}）
- [ ] 白皮书版本号准确（WP-vX.Y.Z）
- [ ] SHA-256指纹完整（如需展示）
- [ ] 禁止事项明确列出
- [ ] "数据主权归于人民"声明清晰
- [ ] 视觉上易于识别（不被忽视）

**版本更新策略：**
当白皮书版本更新时：
- 更新"版本号"（如 WP-v1.0.0 → WP-v1.1.0）
- 更新"SHA-256"指纹
- 更新"存证编号"
- 保持DNA追溯码不变`;
    }
}

/**
 * 快速使用函数
 * @param type 水印块类型
 * @param config 可选配置
 * @returns 水印块文本
 */
export function generateWatermark(
    type: WatermarkType = WatermarkType.COMPACT,
    config: Partial<WatermarkConfig> = {}
): string {
    const generator = new NotionWatermarkBlockGenerator(config);
    return generator.generate(type);
}

/**
 * 验证水印完整性
 * @param content 包含水印的内容
 * @returns 检查结果
 */
export function validateWatermark(content: string): WatermarkIntegrityResult {
    return WatermarkValidator.checkIntegrity(content);
}
