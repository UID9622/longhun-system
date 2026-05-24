/**
 * 市场路由处理 - 元宇宙生态市场
 * Creator: Lucky (诸葛鑫) | UID9622
 * License: Mulan PSL v2
 */

const express = require('express');
const router = express.Router();
const ActivationService = require('../services/activationService');
const DigitalIdentity = require('../config/digital-identity');

const activationService = new ActivationService();

/**
 * 市场首页 - 展示所有可用的功能模块
 */
router.get('/', (req, res) => {
    try {
        const marketplaceData = {
            categories: [
                {
                    id: 'ai_features',
                    name: 'AI功能',
                    description: '增强AI能力的高级功能',
                    icon: '🤖',
                    features: [
                        'advanced_personas',
                        'custom_ai_training',
                        'professional_api'
                    ]
                },
                {
                    id: 'deployment',
                    name: '部署方案',
                    description: '不同规模的部署方案',
                    icon: '🚀',
                    features: [
                        'enterprise_deployment',
                        'multi_device_sync'
                    ]
                },
                {
                    id: 'metaverse',
                    name: '元宇宙',
                    description: '元宇宙相关功能',
                    icon: '🌐',
                    features: [
                        'metaverse_identity',
                        'virtual_asset_creation',
                        'metaverse_collaboration'
                    ]
                }
            ],
            features: getMarketplaceFeatures(),
            creator: DigitalIdentity.creator,
            collaboration: DigitalIdentity.collaboration
        };
        
        res.json({
            success: true,
            data: marketplaceData,
            message: '市场数据获取成功'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '市场数据获取失败'
        });
    }
});

/**
 * 功能详情 - 获取特定功能的详细信息
 */
router.get('/feature/:featureId', (req, res) => {
    try {
        const { featureId } = req.params;
        
        // 验证功能是否存在
        if (!activationService.isValidFeature(featureId)) {
            return res.status(404).json({
                success: false,
                error: '功能不存在',
                message: '请选择有效的功能模块'
            });
        }
        
        // 获取功能详细信息
        const featureInfo = getFeatureDetails(featureId);
        
        res.json({
            success: true,
            data: featureInfo,
            message: '功能详情获取成功'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '功能详情获取失败'
        });
    }
});

/**
 * 获取激活价格
 */
router.get('/pricing/:featureId', (req, res) => {
    try {
        const { featureId } = req.params;
        const { duration = 365 } = req.query;
        
        // 验证功能是否存在
        if (!activationService.isValidFeature(featureId)) {
            return res.status(404).json({
                success: false,
                error: '功能不存在',
                message: '请选择有效的功能模块'
            });
        }
        
        // 获取价格信息
        const pricingInfo = getPricingInfo(featureId, parseInt(duration));
        
        res.json({
            success: true,
            data: pricingInfo,
            message: '价格信息获取成功'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '价格信息获取失败'
        });
    }
});

/**
 * 合作伙伴申请 - 提交合作伙伴申请
 */
router.post('/partner/apply', (req, res) => {
    try {
        const {
            companyName,
            contactPerson,
            email,
            phone,
            description,
            collaborationType,
            expectedBenefits
        } = req.body;
        
        // 验证必填字段
        if (!companyName || !contactPerson || !email) {
            return res.status(400).json({
                success: false,
                error: '缺少必要信息',
                message: '请填写完整的申请信息'
            });
        }
        
        // 生成申请记录
        const application = {
            id: generateApplicationId(),
            companyName,
            contactPerson,
            email,
            phone: phone || '',
            description: description || '',
            collaborationType: collaborationType || 'general',
            expectedBenefits: expectedBenefits || '',
            status: 'pending',
            createdAt: new Date().toISOString(),
            reviewProcess: [
                { step: '提交申请', status: 'completed', time: new Date().toISOString() },
                { step: '初步审核', status: 'pending', time: null },
                { step: '技术评估', status: 'pending', time: null },
                { step: '商务洽谈', status: 'pending', time: null },
                { step: '协议签订', status: 'pending', time: null }
            ]
        };
        
        // 保存申请记录
        savePartnerApplication(application);
        
        res.json({
            success: true,
            data: application,
            message: '合作伙伴申请提交成功，我们会尽快联系您'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '合作伙伴申请提交失败'
        });
    }
});

/**
 * 获取元宇宙生态状态
 */
router.get('/metaverse/status', (req, res) => {
    try {
        const metaverseStatus = {
            vision: DigitalIdentity.metaverse.vision,
            principles: DigitalIdentity.metaverse.principles,
            activations: getMetaverseActivations(),
            statistics: getMetaverseStatistics(),
            roadmap: getMetaverseRoadmap()
        };
        
        res.json({
            success: true,
            data: metaverseStatus,
            message: '元宇宙状态获取成功'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '元宇宙状态获取失败'
        });
    }
});

/**
 * 获取市场功能列表
 * @returns {Array} 功能列表
 */
function getMarketplaceFeatures() {
    const allFeatures = [];
    
    // AI功能
    const aiFeatures = [
        'advanced_personas',
        'custom_ai_training',
        'professional_api'
    ];
    
    // 部署方案
    const deploymentFeatures = [
        'enterprise_deployment',
        'multi_device_sync'
    ];
    
    // 元宇宙功能
    const metaverseFeatures = [
        'metaverse_identity',
        'virtual_asset_creation',
        'metaverse_collaboration'
    ];
    
    // 为所有功能添加详细信息
    [...aiFeatures, ...deploymentFeatures, ...metaverseFeatures].forEach(feature => {
        allFeatures.push({
            id: feature,
            ...activationService.getFeatureDescription(feature),
            category: aiFeatures.includes(feature) ? 'ai_features' :
                     deploymentFeatures.includes(feature) ? 'deployment' : 'metaverse'
        });
    });
    
    return allFeatures;
}

/**
 * 获取功能详细信息
 * @param {string} featureId - 功能ID
 * @returns {Object} 功能详细信息
 */
function getFeatureDetails(featureId) {
    const baseInfo = activationService.getFeatureDescription(featureId);
    const pricing = getPricingInfo(featureId, 365);
    
    return {
        ...baseInfo,
        pricing,
        requirements: getFeatureRequirements(featureId),
        testimonials: getFeatureTestimonials(featureId),
        relatedFeatures: getRelatedFeatures(featureId)
    };
}

/**
 * 获取价格信息
 * @param {string} featureId - 功能ID
 * @param {number} duration - 有效期（天）
 * @returns {Object} 价格信息
 */
function getPricingInfo(featureId, duration) {
    const basePrices = {
        advanced_personas: 299,
        custom_ai_training: 599,
        enterprise_deployment: 999,
        multi_device_sync: 199,
        professional_api: 399,
        metaverse_identity: 149,
        virtual_asset_creation: 349,
        metaverse_collaboration: 499
    };
    
    const basePrice = basePrices[featureId] || 0;
    const dailyPrice = basePrice / 365;
    const totalPrice = Math.round(dailyPrice * duration);
    
    // 长期折扣
    let discount = 0;
    if (duration >= 365) discount = 0; // 1年无折扣
    else if (duration >= 180) discount = 0.1; // 半年9折
    else if (duration >= 90) discount = 0.2; // 季度8折
    
    const discountedPrice = Math.round(totalPrice * (1 - discount));
    
    return {
        basePrice,
        dailyPrice: Math.round(dailyPrice * 100) / 100,
        duration,
        discount,
        discountedPrice,
        currency: 'CNY',
        paymentMethods: ['digitalCNY', 'wechat', 'usdt']
    };
}

/**
 * 获取功能需求
 * @param {string} featureId - 功能ID
 * @returns {Array} 需求列表
 */
function getFeatureRequirements(featureId) {
    const requirements = {
        advanced_personas: [
            '基础BaoBao AI Assistant',
            'Python 3.8+',
            '至少4GB内存',
            '网络连接'
        ],
        custom_ai_training: [
            'BaoBao AI Assistant专业版',
            'Python 3.8+',
            '至少8GB内存',
            'GPU支持（推荐）',
            '至少10GB训练数据'
        ],
        enterprise_deployment: [
            'BaoBao AI Assistant企业版',
            '服务器环境',
            '至少16GB内存',
            '专用数据库',
            '技术管理员'
        ]
    };
    
    return requirements[featureId] || [
        'BaoBao AI Assistant基础版',
        'Python 3.8+',
        '网络连接'
    ];
}

/**
 * 获取功能评价
 * @param {string} featureId - 功能ID
 * @returns {Array} 评价列表
 */
function getFeatureTestimonials(featureId) {
    const testimonials = {
        advanced_personas: [
            {
                user: '张先生',
                role: '产品经理',
                content: '高级人格模块让我们的AI助手更专业，大大提升了工作效率。',
                rating: 5
            },
            {
                user: '李女士',
                role: '教育工作者',
                content: '场景化人格功能非常实用，能够根据不同场景调用合适的人格。',
                rating: 5
            }
        ],
        custom_ai_training: [
            {
                user: '王总',
                role: '企业创始人',
                content: '自定义AI训练功能让我们能够训练专属的AI模型，数据主权得到了保障。',
                rating: 5
            }
        ]
    };
    
    return testimonials[featureId] || [];
}

/**
 * 获取相关功能
 * @param {string} featureId - 功能ID
 * @returns {Array} 相关功能列表
 */
function getRelatedFeatures(featureId) {
    const relatedMap = {
        advanced_personas: ['custom_ai_training', 'professional_api'],
        custom_ai_training: ['advanced_personas', 'enterprise_deployment'],
        enterprise_deployment: ['multi_device_sync', 'professional_api'],
        metaverse_identity: ['virtual_asset_creation', 'metaverse_collaboration'],
        virtual_asset_creation: ['metaverse_identity', 'metaverse_collaboration'],
        metaverse_collaboration: ['metaverse_identity', 'virtual_asset_creation']
    };
    
    return relatedMap[featureId] || [];
}

/**
 * 生成申请ID
 * @returns {string} 申请ID
 */
function generateApplicationId() {
    return `partner_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * 保存合作伙伴申请
 * @param {Object} application - 申请信息
 */
function savePartnerApplication(application) {
    // 这里应该保存到数据库
    // 现在暂时保存到文件
    const fs = require('fs').promises;
    const path = require('path');
    
    const applicationsPath = path.join(__dirname, '../../.cache/partner-applications.json');
    
    fs.readFile(applicationsPath, 'utf8')
        .then(data => {
            const applications = JSON.parse(data || '[]');
            applications.push(application);
            return fs.writeFile(applicationsPath, JSON.stringify(applications, null, 2));
        })
        .catch(() => {
            // 文件不存在，创建新文件
            return fs.writeFile(applicationsPath, JSON.stringify([application], null, 2));
        })
        .catch(error => {
            console.error('❌ 保存合作伙伴申请失败:', error);
        });
}

/**
 * 获取元宇宙激活状态
 * @returns {Object} 激活状态
 */
function getMetaverseActivations() {
    // 这里应该从数据库获取实际数据
    return {
        totalActivations: 1250,
        activeUsers: 890,
        todayActivations: 45,
        popularFeatures: [
            { feature: 'metaverse_identity', count: 450 },
            { feature: 'virtual_asset_creation', count: 380 },
            { feature: 'metaverse_collaboration', count: 420 }
        ]
    };
}

/**
 * 获取元宇宙统计数据
 * @returns {Object} 统计数据
 */
function getMetaverseStatistics() {
    // 这里应该从数据库获取实际数据
    return {
        totalUsers: 5890,
        activeUsers: 3200,
        totalVirtualAssets: 12500,
        totalCollaborationSpaces: 890,
        averageSessionTime: '45分钟',
        userSatisfaction: 4.8
    };
}

/**
 * 获取元宇宙路线图
 * @returns {Array} 路线图
 */
function getMetaverseRoadmap() {
    return [
        {
            phase: 'Q1 2026',
            features: [
                '跨平台身份验证',
                '虚拟资产NFT化',
                'AI驱动的内容生成'
            ],
            status: 'planned'
        },
        {
            phase: 'Q2 2026',
            features: [
                '多人实时协作',
                '虚拟经济系统',
                '开发者API开放'
            ],
            status: 'planned'
        },
        {
            phase: 'Q3 2026',
            features: [
                '去中心化存储',
                '跨链互操作性',
                '元宇宙搜索引擎'
            ],
            status: 'planned'
        }
    ];
}

module.exports = router;