/*
╔═══════════════════════════════════════════════════════════════╗
║  🐉 龙魂系统 | UID9622                                        ║
╠═══════════════════════════════════════════════════════════════╣
║  📦 模块：生成器模块索引                                       ║
║  🧬 DNA：#UID9622⚡️2026-01-26-GENERATORS-INDEX-v1.0          ║
║  🔐 GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F            ║
╚═══════════════════════════════════════════════════════════════╝
*/

// DNA头部生成器
export { DNAHeaderGenerator } from './dnaHeader';

// AI注解生成器
export { AIAnnotationGenerator } from './aiAnnotation';

// Notion水印块生成器
export {
    NotionWatermarkBlockGenerator,
    WatermarkValidator,
    WatermarkChecklist,
    WatermarkType,
    generateWatermark,
    validateWatermark,
    DEFAULT_CONFIG
} from './notionWatermarkBlocks';

export type {
    WatermarkConfig,
    WatermarkIntegrityResult,
    Collaborator
} from './notionWatermarkBlocks';
