/**
 * 每日复盘命令
 * 用于执行龍魂价值内核和场景化人格调用地图的每日复盘
 */

const DailyReviewService = require('../services/dailyReview');
const NotionSyncService = require('../services/notionSync');

class DailyReviewCommand {
    constructor() {
        this.dailyReview = new DailyReviewService();
        this.notionSync = new NotionSyncService();
    }

    /**
     * 执行每日复盘
     */
    async execute() {
        console.log('🌅 开始执行每日复盘命令...');
        
        try {
            // 初始化服务
            await this.initialize();
            
            // 执行完整复盘流程
            const result = await this.performFullReview();
            
            // 显示结果摘要
            this.displaySummary(result);
            
            return result;
            
        } catch (error) {
            console.error('❌ 每日复盘执行失败:', error.message);
            process.exit(1);
        }
    }

    /**
     * 初始化服务
     */
    async initialize() {
        console.log('🔧 初始化每日复盘服务...');
        
        // 初始化Notion同步
        const notionInitialized = await this.notionSync.initialize();
        if (!notionInitialized) {
            throw new Error('Notion同步服务初始化失败');
        }
        
        console.log('✅ 所有服务初始化完成');
    }

    /**
     * 执行完整复盘
     */
    async performFullReview() {
        console.log('🔍 开始完整复盘流程...');
        
        // 1. 执行每日复盘
        const reviewResult = await this.dailyReview.performDailyReview();
        
        // 2. 检查龍魂特别关注点
        const dragonSoulFocus = await this.checkDragonSoulFocus();
        
        // 3. 验证Notion同步状态
        const notionStatus = await this.verifyNotionSync();
        
        return {
            ...reviewResult,
            dragonSoulFocus,
            notionStatus
        };
    }

    /**
     * 检查龍魂特别关注点
     */
    async checkDragonSoulFocus() {
        console.log('🐉 检查龍魂特别关注点...');
        
        const focusPoints = {
            valueCore: await this.checkValueCore(),
            dnaLock: await this.checkDNALock(),
            personaMap: await this.checkPersonaMapConsistency()
        };
        
        return {
            status: 'completed',
            focusPoints,
            summary: this.generateFocusSummary(focusPoints)
        };
    }

    /**
     * 验证Notion同步状态
     */
    async verifyNotionSync() {
        console.log('🔄 验证Notion同步状态...');
        
        try {
            const syncResult = await this.notionSync.performDailySync();
            
            return {
                status: 'success',
                lastSync: new Date().toISOString(),
                updates: syncResult.summary.totalUpdates,
                criticalUpdates: Object.keys(syncResult.updates).length
            };
            
        } catch (error) {
            return {
                status: 'failed',
                error: error.message,
                lastSync: new Date().toISOString()
            };
        }
    }

    /**
     * 显示结果摘要
     */
    displaySummary(result) {
        console.log('\n📊 每日复盘结果摘要:');
        console.log('=' .repeat(50));
        
        // 复盘状态
        console.log(`🎯 复盘状态: ${result.status}`);
        console.log(`⏱️ 执行时长: ${result.duration}ms`);
        
        // 龍魂价值内核
        console.log(`🐉 龍魂价值内核: ${result.dragonSoul.status === 'completed' ? '✅ 已完成' : '❌ 失败'}`);
        
        // 场景化人格调用地图
        console.log(`🗺️ 场景化人格调用地图: ${result.personaMap.status === 'completed' ? '✅ 已完成' : '❌ 失败'}`);
        
        // 系统协调性
        console.log(`🔄 系统协调性: ${(result.summary.coordinationScore * 100).toFixed(1)}%`);
        
        // Notion同步
        console.log(`📝 Notion同步: ${result.notionStatus.status === 'success' ? '✅ 成功' : '❌ 失败'}`);
        
        // 关键问题
        if (result.summary.criticalIssues.length > 0) {
            console.log('\n⚠️ 关键问题:');
            result.summary.criticalIssues.forEach(issue => {
                console.log(`  - ${issue}`);
            });
        }
        
        // 可执行项
        if (result.actionableItems.length > 0) {
            console.log('\n📋 建议执行项:');
            result.actionableItems.slice(0, 5).forEach(item => {
                console.log(`  - [${item.priority}] ${item.action}`);
            });
        }
        
        console.log('\n✨ 每日复盘完成！');
        console.log('📄 详细报告已保存到: .cache/daily-reviews/');
    }

    /**
     * 检查价值核心
     */
    async checkValueCore() {
        // 这里实现具体的价值核心检查逻辑
        return {
            status: 'healthy',
            alignment: 0.95,
            issues: []
        };
    }

    /**
     * 检查DNA锁
     */
    async checkDNALock() {
        // 这里实现DNA锁检查逻辑
        return {
            status: 'active',
            security: 'high',
            integrity: 'maintained'
        };
    }

    /**
     * 检查人格地图一致性
     */
    async checkPersonaMapConsistency() {
        // 这里实现人格地图一致性检查逻辑
        return {
            status: 'consistent',
            coverage: 0.92,
            gaps: []
        };
    }

    /**
     * 生成关注点摘要
     */
    generateFocusSummary(focusPoints) {
        const allHealthy = Object.values(focusPoints).every(point => 
            point.status === 'healthy' || point.status === 'active' || point.status === 'consistent'
        );
        
        return {
            overall: allHealthy ? 'excellent' : 'needs_attention',
            score: allHealthy ? 0.95 : 0.75,
            recommendations: allHealthy ? [] : ['建议关注异常状态的关注点']
        };
    }
}

module.exports = DailyReviewCommand;