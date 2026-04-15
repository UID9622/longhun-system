<?php
/**
 * CNSH-64 社区系统插件配置
 * Discuz! X3.5
 */

if(!defined('IN_DISCUZ')) {
    exit('Access Denied');
}

// 插件标识
$_config['cnsh']['version'] = '1.0.0';
$_config['cnsh']['name'] = 'CNSH-64社区系统';

// CNSH护盾API地址
$_config['cnsh']['shield_api'] = 'http://localhost:16384';

// 数字人民币模块地址
$_config['cnsh']['ecny_api'] = 'http://localhost:16385';

// API密钥（用于CNSH护盾回调验证）
$_config['cnsh']['api_key'] = '';

// 70%治理阈值
$_config['cnsh']['governance_threshold'] = 0.7;

// DNA绑定上限（一个DNA最多绑定N个社区身份）
$_config['cnsh']['max_bindings_per_dna'] = 5;

// 信誉分同步间隔（秒）
$_config['cnsh']['reputation_sync_interval'] = 300;

// 投票频率限制
$_config['cnsh']['vote_limit_per_day'] = 10;

// 打赏限制
$_config['cnsh']['tip_max_per_tip'] = 1000;
$_config['cnsh']['tip_max_per_day'] = 5000;
$_config['cnsh']['tip_cooldown'] = 60;

// 最低投票信誉分
$_config['cnsh']['min_reputation_to_vote'] = 30;

// 最低提案信誉分
$_config['cnsh']['min_reputation_to_propose'] = 50;

// 调试模式
$_config['cnsh']['debug'] = false;

// 日志级别: 0=关闭, 1=错误, 2=警告, 3=信息, 4=调试
$_config['cnsh']['log_level'] = 2;
?>
