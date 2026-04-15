<?php
/**
 * CNSH-64 API接口
 * 供CNSH护盾调用的回调接口
 */

if(!defined('IN_DISCUZ')) {
    exit('Access Denied');
}

class cnsh_api {
    
    /**
     * 验证API密钥
     */
    function verify_api_key() {
        global $_G;
        $api_key = $_GET['api_key'] ?: $_POST['api_key'];
        $config_key = $_G['cache']['plugin']['cnsh']['api_key'];
        
        if (empty($config_key) || $api_key !== $config_key) {
            echo json_encode(array('error' => '无效的API密钥'));
            exit;
        }
    }
    
    /**
     * DNA查询接口
     * 供CNSH护盾查询DNA绑定的社区身份
     */
    function dna_query() {
        $this->verify_api_key();
        
        $dna = trim($_GET['dna']);
        if (empty($dna)) {
            echo json_encode(array('error' => 'DNA地址不能为空'));
            exit;
        }
        
        $bindings = C::t('#cnsh#cnsh_dna_binding')->fetch_all_by_dna($dna);
        
        $result = array();
        foreach ($bindings as $binding) {
            $user = C::t('common_member')->fetch($binding['uid']);
            $result[] = array(
                'uid' => $binding['uid'],
                'username' => $user['username'],
                'reputation' => floatval($binding['reputation']),
                'bound_at' => $binding['bound_at'],
                'status' => $binding['status']
            );
        }
        
        echo json_encode(array(
            'success' => true,
            'dna' => $dna,
            'bindings' => $result,
            'count' => count($result)
        ));
        exit;
    }
    
    /**
     * 信誉同步接口
     * CNSH护盾主动推送信誉变动
     */
    function reputation_sync() {
        $this->verify_api_key();
        
        $dna = trim($_POST['dna']);
        $new_reputation = floatval($_POST['reputation']);
        $reason = trim($_POST['reason']);
        $tx_hash = trim($_POST['tx_hash']);
        
        if (empty($dna)) {
            echo json_encode(array('error' => 'DNA地址不能为空'));
            exit;
        }
        
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_dna($dna);
        if (!$binding) {
            echo json_encode(array('error' => 'DNA未绑定'));
            exit;
        }
        
        $old_score = floatval($binding['reputation']);
        
        // 更新信誉
        C::t('#cnsh#cnsh_dna_binding')->update($binding['id'], array(
            'reputation' => $new_reputation,
            'last_sync' => TIMESTAMP
        ));
        
        // 记录日志
        C::t('#cnsh#cnsh_reputation_log')->insert(array(
            'dna' => $dna,
            'old_score' => $old_score,
            'new_score' => $new_reputation,
            'change' => $new_reputation - $old_score,
            'reason' => $reason ?: '链上同步',
            'related_tx' => $tx_hash,
            'created_at' => TIMESTAMP
        ));
        
        // 更新用户组
        $this->update_user_group($binding['uid'], $new_reputation);
        
        echo json_encode(array(
            'success' => true,
            'dna' => $dna,
            'old_score' => $old_score,
            'new_score' => $new_reputation
        ));
        exit;
    }
    
    /**
     * 批量信誉同步
     */
    function batch_reputation_sync() {
        $this->verify_api_key();
        
        $updates = json_decode($_POST['updates'], true);
        if (!is_array($updates)) {
            echo json_encode(array('error' => '无效的更新数据'));
            exit;
        }
        
        $success_count = 0;
        $failed = array();
        
        foreach ($updates as $update) {
            $dna = $update['dna'];
            $reputation = $update['reputation'];
            
            $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_dna($dna);
            if (!$binding) {
                $failed[] = array('dna' => $dna, 'error' => '未绑定');
                continue;
            }
            
            C::t('#cnsh#cnsh_dna_binding')->update($binding['id'], array(
                'reputation' => $reputation,
                'last_sync' => TIMESTAMP
            ));
            
            $this->update_user_group($binding['uid'], $reputation);
            $success_count++;
        }
        
        echo json_encode(array(
            'success' => true,
            'updated' => $success_count,
            'failed' => $failed
        ));
        exit;
    }
    
    /**
     * DNA封禁接口
     */
    function ban_dna() {
        $this->verify_api_key();
        
        $dna = trim($_POST['dna']);
        $reason = trim($_POST['reason']);
        $tx_hash = trim($_POST['tx_hash']);
        
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_dna($dna);
        if (!$binding) {
            echo json_encode(array('error' => 'DNA未绑定'));
            exit;
        }
        
        // 封禁所有绑定
        C::t('#cnsh#cnsh_dna_binding')->update_by_dna($dna, array(
            'status' => 2,
            'reputation' => 0
        ));
        
        // 封禁用户
        $bindings = C::t('#cnsh#cnsh_dna_binding')->fetch_all_by_dna($dna);
        foreach ($bindings as $b) {
            C::t('common_member')->update($b['uid'], array('groupid' => 4)); // 禁止访问组
        }
        
        // 记录日志
        C::t('#cnsh#cnsh_ban_log')->insert(array(
            'dna' => $dna,
            'reason' => $reason,
            'tx_hash' => $tx_hash,
            'banned_at' => TIMESTAMP
        ));
        
        echo json_encode(array(
            'success' => true,
            'dna' => $dna,
            'affected_users' => count($bindings)
        ));
        exit;
    }
    
    /**
     * 获取治理统计
     */
    function governance_stats() {
        $this->verify_api_key();
        
        $stats = array(
            'total_proposals' => C::t('#cnsh#cnsh_proposals')->count(),
            'active_proposals' => C::t('#cnsh#cnsh_proposals')->count_by_status(0),
            'passed_proposals' => C::t('#cnsh#cnsh_proposals')->count_by_status(1),
            'total_votes' => C::t('#cnsh#cnsh_votes')->count(),
            'total_vote_weight' => C::t('#cnsh#cnsh_votes')->sum_weight()
        );
        
        echo json_encode(array(
            'success' => true,
            'stats' => $stats
        ));
        exit;
    }
    
    /**
     * 获取经济统计
     */
    function ecny_stats() {
        $this->verify_api_key();
        
        $stats = array(
            'total_tips' => C::t('#cnsh#cnsh_tips')->count(),
            'total_tip_amount' => C::t('#cnsh#cnsh_tips')->sum_amount(),
            'active_wallets' => C::t('#cnsh#cnsh_dna_binding')->count_by_status(1),
            'today_tips' => C::t('#cnsh#cnsh_tips')->count_today(),
            'today_amount' => C::t('#cnsh#cnsh_tips')->sum_today()
        );
        
        echo json_encode(array(
            'success' => true,
            'stats' => $stats
        ));
        exit;
    }
    
    /**
     * 心跳检测
     */
    function ping() {
        echo json_encode(array(
            'success' => true,
            'service' => 'CNSH-Community-API',
            'version' => '1.0.0',
            'timestamp' => TIMESTAMP,
            'discuz_version' => DISCUZ_VERSION
        ));
        exit;
    }
    
    /**
     * 更新用户组
     */
    function update_user_group($uid, $reputation) {
        $groupid = 10;
        if ($reputation >= 90) $groupid = 1;
        elseif ($reputation >= 70) $groupid = 2;
        elseif ($reputation >= 50) $groupid = 3;
        elseif ($reputation >= 30) $groupid = 11;
        
        C::t('common_member')->update($uid, array('groupid' => $groupid));
    }
}
?>
