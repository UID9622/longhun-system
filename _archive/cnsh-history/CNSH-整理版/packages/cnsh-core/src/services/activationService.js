/**
 * 激活码服务
 * Creator: Lucky (诸葛鑫) | UID9622
 * License: Mulan PSL v2
 */

const crypto = require('crypto');
const fs = require('fs').promises;
const path = require('path');
const DigitalIdentity = require('../config/digital-identity');

class ActivationService {
    constructor() {
        this.activationsPath = path.join(__dirname, '../../.cache/activations');
        this.dnaSignature = "UID9622⚡️ZHUGEXIN🇨🇳2025";
        this.init();
    }

    async init() {
        try {
            await fs.mkdir(this.activationsPath, { recursive: true });
            console.log('🔑 激活服务初始化完成');
        } catch (error) {
            console.error('❌ 激活服务初始化失败:', error);
        }
    }

    /**
     * 生成激活码
     * @param {string} feature - 功能模块
     * @param {string} userId - 用户ID
     * @param {number} duration - 有效期（天）
     * @returns {string} 激活码
     */
    generateActivationCode(feature, userId, duration = 365) {
        const timestamp = Date.now();
        const expiry = timestamp + (duration * 24 * 60 * 60 * 1000);
        const data = `${feature}:${userId}:${expiry}:${this.dnaSignature}`;
        
        // 创建数字签名
        const signature = crypto.createHmac('sha256', this.dnaSignature)
            .update(data)
            .digest('hex');
        
        // 生成激活码
        const activationCode = Buffer.from(`${data}:${signature}`).toString('base64');
        
        console.log(`🔑 生成激活码: ${feature} for ${user} (${duration}天)`);
        return activationCode;
    }

    /**
     * 验证激活码
     * @param {string} activationCode - 激活码
     * @returns {Object} 验证结果
     */
    verifyActivationCode(activationCode) {
        try {
            // 解码激活码
            const decoded = Buffer.from(activationCode, 'base64').toString();
            const [feature, userId, expiry, dnaSig, signature] = decoded.split(':');
            
            // 验证DNA签名
            if (dnaSig !== this.dnaSignature) {
                return {
                    valid: false,
                    error: '无效的DNA签名',
                    code: 'INVALID_DNA_SIGNATURE'
                };
            }
            
            // 验证数字签名
            const data = `${feature}:${userId}:${expiry}:${this.dnaSignature}`;
            const expectedSignature = crypto.createHmac('sha256', this.dnaSignature)
                .update(data)
                .digest('hex');
            
            if (signature !== expectedSignature) {
                return {
                    valid: false,
                    error: '激活码签名验证失败',
                    code: 'INVALID_SIGNATURE'
                };
            }
            
            // 验证有效期
            const now = Date.now();
            if (now > parseInt(expiry)) {
                return {
                    valid: false,
                    error: '激活码已过期',
                    code: 'EXPIRED'
                };
            }
            
            // 验证功能模块
            if (!this.isValidFeature(feature)) {
                return {
                    valid: false,
                    error: '无效的功能模块',
                    code: 'INVALID_FEATURE'
                };
            }
            
            // 返回验证成功信息
            return {
                valid: true,
                data: {
                    feature,
                    userId,
                    expiry: new Date(parseInt(expiry)),
                    daysRemaining: Math.ceil((parseInt(expiry) - now) / (24 * 60 * 60 * 1000))
                }
            };
            
        } catch (error) {
            return {
                valid: false,
                error: '激活码格式错误',
                code: 'INVALID_FORMAT'
            };
        }
    }

    /**
     * 验证功能模块
     * @param {string} feature - 功能模块名称
     * @returns {boolean} 是否有效
     */
    isValidFeature(feature) {
        const validFeatures = [
            'advanced_personas',
            'custom_ai_training',
            'enterprise_deployment',
            'multi_device_sync',
            'professional_api',
            'metaverse_identity',
            'virtual_asset_creation',
            'metaverse_collaboration'
        ];
        
        return validFeatures.includes(feature);
    }

    /**
     * 激活用户功能
     * @param {string} activationCode - 激活码
     * @param {string} userId - 用户ID
     * @returns {Object} 激活结果
     */
    async activateFeature(activationCode, userId) {
        try {
            // 验证激活码
            const verification = this.verifyActivationCode(activationCode);
            
            if (!verification.valid) {
                return {
                    success: false,
                    error: verification.error,
                    code: verification.code
                };
            }
            
            // 检查用户ID匹配
            if (verification.data.userId !== userId) {
                return {
                    success: false,
                    error: '用户ID不匹配',
                    code: 'USER_ID_MISMATCH'
                };
            }
            
            // 记录激活信息
            const activationInfo = {
                userId,
                feature: verification.data.feature,
                activationCode,
                activatedAt: new Date().toISOString(),
                expiresAt: verification.data.expiry,
                daysRemaining: verification.data.daysRemaining
            };
            
            await this.saveActivation(activationInfo);
            
            console.log(`✅ 功能激活成功: ${verification.data.feature} for ${userId}`);
            
            return {
                success: true,
                data: {
                    feature: verification.data.feature,
                    expiresAt: verification.data.expiry,
                    daysRemaining: verification.data.daysRemaining
                }
            };
            
        } catch (error) {
            console.error('❌ 激活过程中出错:', error);
            return {
                success: false,
                error: '激活过程出错',
                code: 'ACTIVATION_ERROR'
            };
        }
    }

    /**
     * 保存激活信息
     * @param {Object} activationInfo - 激活信息
     */
    async saveActivation(activationInfo) {
        try {
            const userActivationPath = path.join(this.activationsPath, `${activationInfo.userId}.json`);
            
            // 读取现有激活信息
            let existingActivations = [];
            try {
                const data = await fs.readFile(userActivationPath, 'utf8');
                existingActivations = JSON.parse(data);
            } catch (error) {
                // 文件不存在，使用空数组
            }
            
            // 添加新激活信息
            existingActivations.push(activationInfo);
            
            // 保存激活信息
            await fs.writeFile(userActivationPath, JSON.stringify(existingActivations, null, 2));
            
        } catch (error) {
            console.error('❌ 保存激活信息失败:', error);
            throw error;
        }
    }

    /**
     * 获取用户激活信息
     * @param {string} userId - 用户ID
     * @returns {Array} 激活信息列表
     */
    async getUserActivations(userId) {
        try {
            const userActivationPath = path.join(this.activationsPath, `${userId}.json`);
            const data = await fs.readFile(userActivationPath, 'utf8');
            return JSON.parse(data);
        } catch (error) {
            return [];
        }
    }

    /**
     * 检查用户功能是否激活
     * @param {string} userId - 用户ID
     * @param {string} feature - 功能名称
     * @returns {boolean} 是否已激活
     */
    async isFeatureActivated(userId, feature) {
        try {
            const activations = await this.getUserActivations(userId);
            
            // 查找匹配的激活信息
            const activation = activations.find(act => 
                act.feature === feature && new Date(act.expiresAt) > new Date()
            );
            
            return !!activation;
        } catch (error) {
            console.error('❌ 检查激活状态失败:', error);
            return false;
        }
    }

    /**
     * 获取功能描述
     * @param {string} feature - 功能名称
     * @returns {Object} 功能描述
     */
    getFeatureDescription(feature) {
        const features = {
            advanced_personas: {
                name: "高级人格模块",
                description: "解锁全部124个高级人格，包括专业领域人格",
                benefits: [
                    "专业领域深度对话",
                    "场景化人格调用",
                    "个性化人格定制"
                ]
            },
            custom_ai_training: {
                name: "自定义AI训练",
                description: "基于您的数据训练专属AI模型",
                benefits: [
                    "个人数据主权",
                    "个性化响应风格",
                    "私有AI部署"
                ]
            },
            enterprise_deployment: {
                name: "企业级部署",
                description: "支持企业级大规模部署和管理",
                benefits: [
                    "多用户管理",
                    "企业级安全",
                    "定制化开发"
                ]
            },
            multi_device_sync: {
                name: "多设备同步",
                description: "跨设备无缝同步数据和对话",
                benefits: [
                    "云端数据同步",
                    "跨平台支持",
                    "实时数据备份"
                ]
            },
            professional_api: {
                name: "专业API访问",
                description: "获取高级API功能和更高配额",
                benefits: [
                    "高级API接口",
                    "更高访问配额",
                    "优先技术支持"
                ]
            },
            metaverse_identity: {
                name: "元宇宙身份验证",
                description: "跨平台统一数字身份",
                benefits: [
                    "统一数字身份",
                    "跨平台互认",
                    "身份自主权"
                ]
            },
            virtual_asset_creation: {
                name: "虚拟资产创建",
                description: "AI辅助的虚拟内容创作工具",
                benefits: [
                    "AI辅助创作",
                    "虚拟资产确权",
                    "跨平台发布"
                ]
            },
            metaverse_collaboration: {
                name: "元宇宙协作空间",
                description: "多用户协作的虚拟空间",
                benefits: [
                    "多用户实时协作",
                    "虚拟空间管理",
                    "协作历史记录"
                ]
            }
        };
        
        return features[feature] || null;
    }

    /**
     * 生成白名单激活码（给官方合作伙伴）
     * @param {Object} partnerInfo - 合作伙伴信息
     * @param {Array} features - 功能列表
     * @param {number} count - 激活码数量
     * @returns {Array} 激活码列表
     */
    generateWhitelistActivationCodes(partnerInfo, features, count = 1) {
        // 验证合作伙伴
        if (!this.isValidPartner(partnerInfo)) {
            throw new Error('无效的合作伙伴');
        }
        
        const activationCodes = [];
        
        for (let i = 0; i < count; i++) {
            features.forEach(feature => {
                const userId = `${partnerInfo.id}_user_${Date.now()}_${i}`;
                const code = this.generateActivationCode(feature, userId);
                
                activationCodes.push({
                    code,
                    feature,
                    partner: partnerInfo.name,
                    generatedAt: new Date().toISOString(),
                    status: 'available'
                });
            });
        }
        
        console.log(`🔑 为合作伙伴 ${partnerInfo.name} 生成 ${activationCodes.length} 个激活码`);
        return activationCodes;
    }

    /**
     * 验证合作伙伴
     * @param {Object} partnerInfo - 合作伙伴信息
     * @returns {boolean} 是否有效
     */
    isValidPartner(partnerInfo) {
        const validPartners = [
            {
                id: 'huawei',
                name: '华为应用市场',
                type: 'official_channel'
            },
            {
                id: 'deepseek',
                name: 'DeepSeek',
                type: 'technical_partner'
            }
        ];
        
        return validPartners.some(partner => 
            partner.id === partnerInfo.id && partner.name === partnerInfo.name
        );
    }
}

module.exports = ActivationService;