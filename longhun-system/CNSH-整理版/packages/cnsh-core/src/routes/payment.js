/**
 * 支付路由处理
 * Creator: Lucky (诸葛鑫) | UID9622
 * License: Mulan PSL v2
 */

const express = require('express');
const router = express.Router();
const ActivationService = require('../services/activationService');
const DigitalIdentity = require('../config/digital-identity');

const activationService = new ActivationService();

/**
 * 支付状态查询
 */
router.get('/status', (req, res) => {
    try {
        const paymentStatus = {
            supported: {
                domestic: {
                    digitalCNY: DigitalIdentity.payment.domestic.digitalCNY,
                    wechat: DigitalIdentity.payment.domestic.wechat
                },
                international: {
                    usdt: DigitalIdentity.payment.international.usdt
                }
            },
            businessModel: DigitalIdentity.businessModel,
            collaboration: DigitalIdentity.collaboration
        };
        
        res.json({
            success: true,
            data: paymentStatus,
            message: '支付状态查询成功'
        });
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '支付状态查询失败'
        });
    }
});

/**
 * 支付方式选择
 */
router.post('/method', (req, res) => {
    try {
        const { paymentMethod, amount, feature } = req.body;
        
        // 验证支付方式
        if (!isValidPaymentMethod(paymentMethod)) {
            return res.status(400).json({
                success: false,
                error: '不支持的支付方式',
                message: '请选择数字人民币或微信支付宝'
            });
        }
        
        // 验证功能
        if (!activationService.isValidFeature(feature)) {
            return res.status(400).json({
                success: false,
                error: '无效的功能模块',
                message: '请选择有效的功能模块'
            });
        }
        
        // 根据支付方式返回相应的支付信息
        let paymentInfo;
        
        switch (paymentMethod) {
            case 'digitalCNY':
                paymentInfo = {
                    type: '数字人民币支付',
                    network: '数字人民币运营网络',
                    instructions: '请使用数字人民币APP扫描二维码或输入支付地址',
                    qrCode: generateDigitalCNYQR(amount, feature),
                    address: generateDigitalCNYAddress(feature)
                };
                break;
                
            case 'wechat':
                paymentInfo = {
                    type: '微信支付宝',
                    account: DigitalIdentity.payment.domestic.wechat.account,
                    instructions: '请使用微信或支付宝扫描二维码或转账到指定账户',
                    qrCode: generateWechatQR(amount, feature),
                    account: DigitalIdentity.payment.domestic.wechat.account
                };
                break;
                
            case 'usdt':
                paymentInfo = {
                    type: 'USDT登记',
                    mode: '登记模式',
                    instructions: '我们不直接接收USDT，仅进行登记处理',
                    process: '登记→审核→转换为合规支付方式',
                    form: generateUSDTRegistrationForm(amount, feature)
                };
                break;
                
            default:
                return res.status(400).json({
                    success: false,
                    error: '无效的支付方式',
                    message: '请选择支持的支付方式'
                });
        }
        
        res.json({
            success: true,
            data: {
                paymentMethod,
                amount,
                feature,
                featureInfo: activationService.getFeatureDescription(feature),
                paymentInfo
            },
            message: '支付方式选择成功'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '支付方式选择失败'
        });
    }
});

/**
 * 激活码申请
 */
router.post('/activate', async (req, res) => {
    try {
        const { userId, activationCode, feature } = req.body;
        
        // 验证必填字段
        if (!userId || !activationCode) {
            return res.status(400).json({
                success: false,
                error: '缺少必要参数',
                message: '请提供用户ID和激活码'
            });
        }
        
        // 激活功能
        const activationResult = await activationService.activateFeature(activationCode, userId);
        
        if (activationResult.success) {
            res.json({
                success: true,
                data: {
                    userId,
                    feature: activationResult.data.feature,
                    expiresAt: activationResult.data.expiresAt,
                    daysRemaining: activationResult.data.daysRemaining,
                    featureInfo: activationService.getFeatureDescription(activationResult.data.feature)
                },
                message: '功能激活成功'
            });
        } else {
            res.status(400).json({
                success: false,
                error: activationResult.error,
                code: activationResult.code,
                message: '功能激活失败'
            });
        }
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '激活码验证失败'
        });
    }
});

/**
 * 用户激活状态查询
 */
router.get('/activations/:userId', async (req, res) => {
    try {
        const { userId } = req.params;
        
        if (!userId) {
            return res.status(400).json({
                success: false,
                error: '缺少用户ID',
                message: '请提供用户ID'
            });
        }
        
        // 获取用户激活信息
        const activations = await activationService.getUserActivations(userId);
        
        // 过滤有效激活
        const validActivations = activations.filter(activation => 
            new Date(activation.expiresAt) > new Date()
        );
        
        // 添加功能描述
        const enrichedActivations = validActivations.map(activation => ({
            ...activation,
            featureInfo: activationService.getFeatureDescription(activation.feature)
        }));
        
        res.json({
            success: true,
            data: {
                userId,
                totalActivations: validActivations.length,
                activations: enrichedActivations
            },
            message: '激活状态查询成功'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '激活状态查询失败'
        });
    }
});

/**
 * 合作伙伴激活码生成
 */
router.post('/partner/activate', (req, res) => {
    try {
        const { partnerInfo, features, count } = req.body;
        
        // 验证合作伙伴
        if (!activationService.isValidPartner(partnerInfo)) {
            return res.status(400).json({
                success: false,
                error: '无效的合作伙伴',
                message: '只有官方合作伙伴才能生成激活码'
            });
        }
        
        // 生成激活码
        const activationCodes = activationService.generateWhitelistActivationCodes(
            partnerInfo, 
            features, 
            count || 1
        );
        
        res.json({
            success: true,
            data: {
                partner: partnerInfo,
                activationCodes,
                generatedAt: new Date().toISOString()
            },
            message: '合作伙伴激活码生成成功'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: '激活码生成失败'
        });
    }
});

/**
 * USDT登记表单处理
 */
router.post('/usdt/register', (req, res) => {
    try {
        const { 
            userId, 
            amount, 
            feature, 
            usdtAddress, 
            transactionHash,
            contactInfo 
        } = req.body;
        
        // 验证必填字段
        if (!userId || !amount || !feature || !usdtAddress) {
            return res.status(400).json({
                success: false,
                error: '缺少必要信息',
                message: '请填写完整的登记信息'
            });
        }
        
        // 生成登记记录
        const registration = {
            id: generateId(),
            userId,
            amount,
            feature,
            usdtAddress,
            transactionHash,
            contactInfo,
            status: 'pending',
            createdAt: new Date().toISOString(),
            processSteps: [
                { step: '登记', status: 'completed', time: new Date().toISOString() },
                { step: '审核', status: 'pending', time: null },
                { step: '转换', status: 'pending', time: null },
                { step: '激活', status: 'pending', time: null }
            ]
        };
        
        // 保存登记记录（这里应该保存到数据库）
        saveUSDTRegistration(registration);
        
        res.json({
            success: true,
            data: registration,
            message: 'USDT登记成功，请等待审核和转换处理'
        });
        
    } catch (error) {
        res.status(500).json({
            success: false,
            error: error.message,
            message: 'USDT登记失败'
        });
    }
});

/**
 * 验证支付方式
 * @param {string} paymentMethod - 支付方式
 * @returns {boolean} 是否有效
 */
function isValidPaymentMethod(paymentMethod) {
    const validMethods = ['digitalCNY', 'wechat', 'usdt'];
    return validMethods.includes(paymentMethod);
}

/**
 * 生成数字人民币二维码
 * @param {number} amount - 金额
 * @param {string} feature - 功能模块
 * @returns {string} 二维码数据
 */
function generateDigitalCNYQR(amount, feature) {
    // 这里应该集成实际的数字人民币API
    return `dcny://payment?amount=${amount}&feature=${feature}&uid=UID9622`;
}

/**
 * 生成数字人民币支付地址
 * @param {string} feature - 功能模块
 * @returns {string} 支付地址
 */
function generateDigitalCNYAddress(feature) {
    return `dcny:uid9622@digitalcny.cn?feature=${feature}`;
}

/**
 * 生成微信/支付宝二维码
 * @param {number} amount - 金额
 * @param {string} feature - 功能模块
 * @returns {string} 二维码数据
 */
function generateWechatQR(amount, feature) {
    // 这里应该集成实际的微信/支付宝API
    return `wxalipay://payment?amount=${amount}&feature=${feature}&uid=UID9622`;
}

/**
 * 生成USDT登记表单
 * @param {number} amount - 金额
 * @param {string} feature - 功能模块
 * @returns {Object} 登记表单
 */
function generateUSDTRegistrationForm(amount, feature) {
    return {
        fields: [
            {
                name: 'userId',
                label: '用户ID',
                type: 'text',
                required: true
            },
            {
                name: 'amount',
                label: 'USDT金额',
                type: 'number',
                required: true,
                value: amount
            },
            {
                name: 'feature',
                label: '功能模块',
                type: 'select',
                required: true,
                options: [
                    { value: 'advanced_personas', label: '高级人格模块' },
                    { value: 'custom_ai_training', label: '自定义AI训练' },
                    { value: 'enterprise_deployment', label: '企业级部署' },
                    { value: 'multi_device_sync', label: '多设备同步' },
                    { value: 'professional_api', label: '专业API访问' },
                    { value: 'metaverse_identity', label: '元宇宙身份验证' },
                    { value: 'virtual_asset_creation', label: '虚拟资产创建' },
                    { value: 'metaverse_collaboration', label: '元宇宙协作空间' }
                ],
                value: feature
            },
            {
                name: 'usdtAddress',
                label: 'USDT钱包地址',
                type: 'text',
                required: true
            },
            {
                name: 'transactionHash',
                label: '交易哈希',
                type: 'text',
                required: true
            },
            {
                name: 'contactInfo',
                label: '联系方式',
                type: 'text',
                required: true
            }
        ],
        instructions: [
            '1. 请将USDT发送到指定地址（联系我们获取）',
            '2. 填写完整的交易信息',
            '3. 我们会在24-48小时内审核',
            '4. 审核通过后会转换为相应的激活码'
        ]
    };
}

/**
 * 生成唯一ID
 * @returns {string} 唯一ID
 */
function generateId() {
    return `usdt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * 保存USDT登记记录
 * @param {Object} registration - 登记记录
 */
function saveUSDTRegistration(registration) {
    // 这里应该保存到数据库
    // 现在暂时保存到文件
    const fs = require('fs').promises;
    const path = require('path');
    
    const registrationsPath = path.join(__dirname, '../../.cache/usdt-registrations.json');
    
    fs.readFile(registrationsPath, 'utf8')
        .then(data => {
            const registrations = JSON.parse(data || '[]');
            registrations.push(registration);
            return fs.writeFile(registrationsPath, JSON.stringify(registrations, null, 2));
        })
        .catch(() => {
            // 文件不存在，创建新文件
            return fs.writeFile(registrationsPath, JSON.stringify([registration], null, 2));
        })
        .catch(error => {
            console.error('❌ 保存USDT登记记录失败:', error);
        });
}

module.exports = router;