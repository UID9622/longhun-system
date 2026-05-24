/**
 * Notion同步服务 - 49f7125a-9c9f-81ec-9db8-00035916bff5
 * 用于每日自动提取和同步Notion数据库更新
 */

const fs = require('fs').promises;
const path = require('path');

class NotionSyncService {
    constructor() {
        this.notionId = '49f7125a-9c9f-81ec-9db8-00035916bff5';
        this.cacheDir = path.join(__dirname, '../../.cache/notion');
        this.lastSyncFile = path.join(this.cacheDir, 'last_sync.json');
        this.pagesDir = path.join(this.cacheDir, 'pages');
        this.corePages = [
            '场景化人格调用地图',
            '快速协作指南',
            'UID9622龍魂价值内核',
            '全局监控中枢',
            '龍魂系统执行机制'
        ];
    }

    /**
     * 初始化Notion同步服务
     */
    async initialize() {
        try {
            await fs.mkdir(this.cacheDir, { recursive: true });
            await fs.mkdir(this.pagesDir, { recursive: true });
            console.log(`✅ Notion同步服务已初始化 - ID: ${this.notionId}`);
            return true;
        } catch (error) {
            console.error('❌ Notion同步服务初始化失败:', error);
            return false;
        }
    }

    /**
     * 执行每日同步
     */
    async performDailySync() {
        console.log('\n📅 开始每日Notion同步...');
        const startTime = Date.now();
        
        try {
            // 1. 获取最后同步时间
            const lastSync = await this.getLastSyncTime();
            const currentTime = new Date().toISOString();
            
            // 2. 提取核心页面更新
            const updates = await this.extractCorePagesUpdates(lastSync);
            
            // 3. 分析龍魂价值内核变化
            const dragonSoulAnalysis = await this.analyzeDragonSoulChanges();
            
            // 4. 检查场景化人格调用地图更新
            const personaMapUpdate = await this.checkPersonaMapUpdates();
            
            // 5. 生成每日报告
            const dailyReport = await this.generateDailyReport({
                syncTime: currentTime,
                updates,
                dragonSoulAnalysis,
                personaMapUpdate,
                duration: Date.now() - startTime
            });
            
            // 6. 保存同步状态
            await this.updateLastSyncTime(currentTime);
            
            // 7. 存储每日报告
            await this.saveDailyReport(dailyReport);
            
            console.log('✅ 每日Notion同步完成');
            return dailyReport;
            
        } catch (error) {
            console.error('❌ 每日同步失败:', error);
            throw error;
        }
    }

    /**
     * 提取核心页面更新
     */
    async extractCorePagesUpdates(lastSyncTime) {
        console.log('🔍 提取核心页面更新...');
        
        const updates = {};
        
        for (const pageName of this.corePages) {
            try {
                const update = await this.extractPageUpdates(pageName, lastSyncTime);
                if (update.hasChanges) {
                    updates[pageName] = update;
                    console.log(`📝 ${pageName}: 发现更新`);
                }
            } catch (error) {
                console.error(`❌ 提取${pageName}更新失败:`, error);
                updates[pageName] = { hasChanges: false, error: error.message };
            }
        }
        
        return updates;
    }

    /**
     * 提取单个页面更新
     */
    async extractPageUpdates(pageName, lastSyncTime) {
        // 这里应该实现实际的Notion API调用
        // 目前使用模拟数据
        const pageFilePath = path.join(this.pagesDir, `${pageName.replace(/[^a-zA-Z0-9]/g, '_')}.json`);
        
        try {
            const existingData = await fs.readFile(pageFilePath, 'utf8');
            const pageData = JSON.parse(existingData);
            
            const lastModified = new Date(pageData.lastModified);
            const lastSync = new Date(lastSyncTime);
            
            if (lastModified > lastSync) {
                return {
                    hasChanges: true,
                    lastModified: pageData.lastModified,
                    changes: pageData.changes || [],
                    summary: pageData.summary
                };
            }
            
            return { hasChanges: false };
            
        } catch (error) {
            // 文件不存在，可能是第一次同步
            return { hasChanges: true, lastModified: new Date().toISOString(), changes: ['首次同步'] };
        }
    }

    /**
     * 分析龍魂价值内核变化
     */
    async analyzeDragonSoulChanges() {
        console.log('🐉 分析龍魂价值内核变化...');
        
        try {
            const dragonSoulPath = '/Users/zuimeidedeyihan/LuckyCommandCenter/CodeBuddy/20251207144453/UID9622_龍魂系统_执行机制与核心价值观.md';
            const content = await fs.readFile(dragonSoulPath, 'utf8');
            
            // 分析核心价值观变化
            const coreValues = this.extractCoreValues(content);
            const principles = this.extractPrinciples(content);
            const dnaStrategy = this.extractDNAStrategy(content);
            
            return {
                coreValues,
                principles,
                dnaStrategy,
                lastAnalyzed: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('❌ 龍魂价值内核分析失败:', error);
            return { error: error.message };
        }
    }

    /**
     * 检查场景化人格调用地图更新
     */
    async checkPersonaMapUpdates() {
        console.log('🗺️ 检查场景化人格调用地图更新...');
        
        try {
            const personaMapPath = '/Users/zuimeidedeyihan/LuckyCommandCenter/CodeBuddy/20251207144453/CNSH_DNA_MEMORY/tasks/TASK-004-Agent_Structure_Optimization.json';
            const content = await fs.readFile(personaMapPath, 'utf8');
            const personaData = JSON.parse(content);
            
            // 提取场景化人格信息
            const personaScenarios = this.extractPersonaScenarios(personaData);
            const collaborationRules = this.extractCollaborationRules(personaData);
            const switchingRules = this.extractSwitchingRules(personaData);
            
            return {
                personaScenarios,
                collaborationRules,
                switchingRules,
                lastUpdated: new Date().toISOString()
            };
            
        } catch (error) {
            console.error('❌ 场景化人格调用地图检查失败:', error);
            return { error: error.message };
        }
    }

    /**
     * 生成每日报告
     */
    async generateDailyReport(data) {
        console.log('📊 生成每日报告...');
        
        const report = {
            date: new Date().toLocaleDateString('zh-CN'),
            notionId: this.notionId,
            syncTime: data.syncTime,
            duration: data.duration,
            summary: {
                totalUpdates: Object.keys(data.updates).length,
                hasDragonSoulChanges: !!data.dragonSoulAnalysis.coreValues,
                hasPersonaMapChanges: !!data.personaMapUpdate.personaScenarios
            },
            updates: data.updates,
            dragonSoulAnalysis: data.dragonSoulAnalysis,
            personaMapUpdate: data.personaMapUpdate,
            recommendations: this.generateRecommendations(data)
        };
        
        return report;
    }

    /**
     * 获取最后同步时间
     */
    async getLastSyncTime() {
        try {
            const data = await fs.readFile(this.lastSyncFile, 'utf8');
            return JSON.parse(data).lastSync;
        } catch (error) {
            return new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString(); // 默认24小时前
        }
    }

    /**
     * 更新最后同步时间
     */
    async updateLastSyncTime(syncTime) {
        const data = { lastSync: syncTime };
        await fs.writeFile(this.lastSyncFile, JSON.stringify(data, null, 2));
    }

    /**
     * 保存每日报告
     */
    async saveDailyReport(report) {
        const reportDir = path.join(this.cacheDir, 'daily-reports');
        await fs.mkdir(reportDir, { recursive: true });
        
        const reportFile = path.join(reportDir, `report_${report.date.replace(/\//g, '-')}.json`);
        await fs.writeFile(reportFile, JSON.stringify(report, null, 2));
        
        console.log(`📄 每日报告已保存: ${reportFile}`);
    }

    /**
     * 提取核心价值观
     */
    extractCoreValues(content) {
        const values = [];
        const lines = content.split('\n');
        
        for (const line of lines) {
            if (line.includes('人民为本') || line.includes('透明公正') || 
                line.includes('自省进化') || line.includes('传承创新') || 
                line.includes('协同责任')) {
                values.push(line.trim());
            }
        }
        
        return values;
    }

    /**
     * 提取原则
     */
    extractPrinciples(content) {
        const principles = [];
        const lines = content.split('\n');
        
        for (const line of lines) {
            if (line.includes('法则') || line.includes('原则') || line.includes('戒律')) {
                principles.push(line.trim());
            }
        }
        
        return principles;
    }

    /**
     * 提取DNA战略
     */
    extractDNAStrategy(content) {
        const strategy = {};
        const lines = content.split('\n');
        
        for (const line of lines) {
            if (line.includes('DNA本地化')) {
                strategy.localization = line.trim();
            } else if (line.includes('中文系统')) {
                strategy.languageSystem = line.trim();
            } else if (line.includes('自产自销')) {
                strategy.selfProduction = line.trim();
            }
        }
        
        return strategy;
    }

    /**
     * 提取场景化人格
     */
    extractPersonaScenarios(personaData) {
        // 从JSON数据中提取场景化人格信息
        return personaData.personaScenarios || [];
    }

    /**
     * 提取协作规则
     */
    extractCollaborationRules(personaData) {
        return personaData.collaborationRules || [];
    }

    /**
     * 提取切换规则
     */
    extractSwitchingRules(personaData) {
        return personaData.switchingRules || [];
    }

    /**
     * 生成建议
     */
    generateRecommendations(data) {
        const recommendations = [];
        
        if (Object.keys(data.updates).length > 0) {
            recommendations.push('检测到核心页面更新，建议审查内容变化');
        }
        
        if (data.dragonSoulAnalysis.coreValues) {
            recommendations.push('龍魂价值内核已更新，建议同步到系统配置');
        }
        
        if (data.personaMapUpdate.personaScenarios) {
            recommendations.push('场景化人格调用地图已更新，建议测试新场景');
        }
        
        return recommendations;
    }
}

module.exports = NotionSyncService;