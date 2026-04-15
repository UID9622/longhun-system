<?php
/**
 * CNSH-64 社区系统安装脚本
 */

if(!defined('IN_DISCUZ')) {
    exit('Access Denied');
}

// 安装时执行
function install_cnsh() {
    global $_G;
    
    $sql = file_get_contents(__DIR__ . '/install.sql');
    
    // 替换表前缀
    $sql = str_replace('pre_', DB::table(''), $sql);
    
    // 执行SQL
    runquery($sql);
    
    // 生成API密钥
    $api_key = md5(uniqid() . TIMESTAMP . random(16));
    
    // 更新配置
    C::t('common_pluginvar')->insert(array(
        'pluginid' => $pluginid,
        'displayorder' => 0,
        'title' => 'API密钥',
        'variable' => 'api_key',
        'type' => 'text',
        'value' => $api_key
    ));
    
    // 创建缓存
    updatecache('plugin');
    
    // 记录安装日志
    $log = "CNSH-64社区系统安装完成\n";
    $log .= "时间: " . date('Y-m-d H:i:s') . "\n";
    $log .= "API密钥: " . $api_key . "\n";
    $log .= "版本: 1.0.0\n";
    
    file_put_contents(__DIR__ . '/install.log', $log);
    
    return true;
}

// 卸载时执行
function uninstall_cnsh() {
    // 删除数据表
    $tables = array(
        'cnsh_dna_binding',
        'cnsh_proposals',
        'cnsh_votes',
        'cnsh_tips',
        'cnsh_reputation_log',
        'cnsh_binding_log',
        'cnsh_execution_log',
        'cnsh_ban_log'
    );
    
    foreach ($tables as $table) {
        DB::query("DROP TABLE IF EXISTS " . DB::table($table));
    }
    
    // 清理缓存
    updatecache('plugin');
    
    return true;
}

// 升级时执行
function upgrade_cnsh($from_version) {
    // 版本升级逻辑
    switch ($from_version) {
        case '0.9.0':
            // 从0.9升级到1.0
            break;
    }
    
    return true;
}
?>
