<?php
/**
 * CNSH-64 70%治理投票系统
 * 社区自治的核心机制
 */

if(!defined('IN_DISCUZ')) {
    exit('Access Denied');
}

class plugin_cnsh_governance {
    
    var $config = array();
    
    function __construct() {
        global $_G;
        $this->config = $_G['cache']['plugin']['cnsh'];
    }
    
    /**
     * 在导航栏添加治理入口
     */
    function global_nav_extra() {
        return '<a href="plugin.php?id=cnsh:governance">社区治理</a>';
    }
    
    /**
     * 计算投票权重
     */
    function calculate_vote_weight($uid) {
        // 1. 获取用户DNA绑定
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($uid);
        if (!$binding || $binding['status'] != 1) {
            return 0; // 未绑定DNA无法投票
        }
        
        // 2. 基础权重 = 信誉分
        $base_weight = floatval($binding['reputation']);
        
        // 3. 活跃度加成
        $activity = $this->get_user_activity($uid);
        $activity_bonus = min($activity * 0.1, 20); // 最多+20
        
        // 4. 心种子加成
        $seed_bonus = $this->get_heart_seed_bonus($binding['heart_seed_hash']);
        
        // 5. 70%治理规则：高信誉用户权重更大
        $total_weight = $base_weight + $activity_bonus + $seed_bonus;
        
        return min($total_weight, 100); // 上限100
    }
    
    /**
     * 获取用户活跃度
     */
    function get_user_activity($uid) {
        // 最近30天发帖数
        $posts = C::t('forum_post')->count_by_authorid($uid, 30);
        // 最近30天登录天数
        $logins = C::t('common_member_status')->fetch($uid);
        $login_days = $logins ? intval((TIMESTAMP - $logins['lastip']) / 86400) : 0;
        
        return min($posts + $login_days, 200);
    }
    
    /**
     * 获取心种子加成
     */
    function get_heart_seed_bonus($hash) {
        if (empty($hash)) return 0;
        // 根据心种子哈希计算加成
        $bonus = 0;
        for ($i = 0; $i < min(4, strlen($hash)); $i++) {
            $char = $hash[$i];
            if (ctype_digit($char)) {
                $bonus += intval($char);
            } else {
                $bonus += (ord(strtolower($char)) - ord('a') + 1) % 10;
            }
        }
        return min($bonus, 15);
    }
    
    /**
     * 检查用户是否可以投票
     */
    function can_vote($uid, $proposal_id) {
        // 检查是否已投票
        $voted = C::t('#cnsh#cnsh_votes')->fetch_by_proposal_uid($proposal_id, $uid);
        if ($voted) {
            return array('can' => false, 'reason' => '您已投过票');
        }
        
        // 检查权重
        $weight = $this->calculate_vote_weight($uid);
        if ($weight <= 0) {
            return array('can' => false, 'reason' => '未绑定DNA或信誉不足，无法投票');
        }
        
        // 检查提案状态
        $proposal = C::t('#cnsh#cnsh_proposals')->fetch($proposal_id);
        if (!$proposal || $proposal['status'] != 0) {
            return array('can' => false, 'reason' => '提案不在投票期');
        }
        
        if (TIMESTAMP > $proposal['end_time']) {
            return array('can' => false, 'reason' => '投票已结束');
        }
        
        return array('can' => true, 'weight' => $weight);
    }
}

/**
 * 治理页面控制器
 */
class cnsh_governance {
    
    function __construct() {
        global $_G;
        if (!$_G['uid']) {
            showmessage('请先登录', 'member.php?mod=logging&action=login');
        }
    }
    
    /**
     * 治理首页 - 提案列表
     */
    function index() {
        global $_G;
        
        $page = max(1, intval($_GET['page']));
        $perpage = 20;
        
        // 获取提案列表
        $proposals = C::t('#cnsh#cnsh_proposals')->fetch_all_by_page($page, $perpage);
        $total = C::t('#cnsh#cnsh_proposals')->count();
        
        // 获取用户投票权重
        $plugin = new plugin_cnsh_governance();
        $my_weight = $plugin->calculate_vote_weight($_G['uid']);
        
        // 分页
        $multipage = multi($total, $perpage, $page, 'plugin.php?id=cnsh:governance');
        
        include template('cnsh:governance');
    }
    
    /**
     * 提案详情
     */
    function view() {
        global $_G;
        
        $proposal_id = intval($_GET['pid']);
        $proposal = C::t('#cnsh#cnsh_proposals')->fetch($proposal_id);
        
        if (!$proposal) {
            showmessage('提案不存在');
        }
        
        // 获取投票统计
        $stats = $this->tally_votes($proposal_id);
        
        // 检查用户投票状态
        $plugin = new plugin_cnsh_governance();
        $vote_status = $plugin->can_vote($_G['uid'], $proposal_id);
        $my_vote = C::t('#cnsh#cnsh_votes')->fetch_by_proposal_uid($proposal_id, $_G['uid']);
        
        include template('cnsh:proposal_view');
    }
    
    /**
     * 创建提案页面
     */
    function create() {
        global $_G;
        
        // 检查创建权限（需要50+信誉）
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($_G['uid']);
        if (!$binding || $binding['reputation'] < 50) {
            showmessage('需要50+信誉分才能创建提案');
        }
        
        include template('cnsh:proposal_create');
    }
    
    /**
     * 提交提案
     */
    function submit_proposal() {
        global $_G;
        
        if (!submitcheck('submit')) {
            showmessage('非法提交');
        }
        
        $title = trim($_POST['title']);
        $content = trim($_POST['content']);
        $type = intval($_POST['type']);
        $duration = intval($_POST['duration']);
        
        if (empty($title) || empty($content)) {
            showmessage('标题和内容不能为空');
        }
        
        // 检查权限
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($_G['uid']);
        if (!$binding || $binding['reputation'] < 50) {
            showmessage('权限不足');
        }
        
        // 创建提案
        $data = array(
            'title' => $title,
            'content' => $content,
            'proposer_uid' => $_G['uid'],
            'proposer_dna' => $binding['dna'],
            'type' => $type,
            'status' => 0,
            'start_time' => TIMESTAMP,
            'end_time' => TIMESTAMP + ($duration * 86400),
            'created_at' => TIMESTAMP
        );
        
        $proposal_id = C::t('#cnsh#cnsh_proposals')->insert($data, true);
        
        // 同步到CNSH链
        $this->sync_proposal_to_cnsh($proposal_id, $data);
        
        showmessage('提案创建成功', 'plugin.php?id=cnsh:governance&action=view&pid=' . $proposal_id);
    }
    
    /**
     * 处理投票
     */
    function vote() {
        global $_G;
        
        $proposal_id = intval($_POST['proposal_id']);
        $choice = intval($_POST['choice']); // 1=支持, 0=反对
        $signature = trim($_POST['signature']);
        
        // 验证投票权限
        $plugin = new plugin_cnsh_governance();
        $vote_status = $plugin->can_vote($_G['uid'], $proposal_id);
        
        if (!$vote_status['can']) {
            showmessage($vote_status['reason']);
        }
        
        $weight = $vote_status['weight'];
        
        // 验证签名
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($_G['uid']);
        if (!$this->verify_vote_signature($binding['dna'], $proposal_id, $choice, $signature)) {
            showmessage('签名验证失败，请使用正确的DNA私钥签名');
        }
        
        // 记录投票
        $vote_data = array(
            'proposal_id' => $proposal_id,
            'uid' => $_G['uid'],
            'dna' => $binding['dna'],
            'choice' => $choice,
            'weight' => $weight,
            'signature' => $signature,
            'voted_at' => TIMESTAMP,
            'synced' => 0
        );
        
        C::t('#cnsh#cnsh_votes')->insert($vote_data);
        
        // 更新提案统计
        $this->update_proposal_stats($proposal_id);
        
        // 同步到CNSH链
        $this->sync_vote_to_cnsh($vote_data);
        
        showmessage('投票成功', 'plugin.php?id=cnsh:governance&action=view&pid=' . $proposal_id);
    }
    
    /**
     * 统计投票结果
     */
    function tally_votes($proposal_id) {
        $votes = C::t('#cnsh#cnsh_votes')->fetch_all_by_proposal($proposal_id);
        
        $total_weight = 0;
        $support_weight = 0;
        $opposition_weight = 0;
        $voter_count = count($votes);
        
        foreach ($votes as $vote) {
            $total_weight += $vote['weight'];
            if ($vote['choice'] == 1) {
                $support_weight += $vote['weight'];
            } else {
                $opposition_weight += $vote['weight'];
            }
        }
        
        // 70%治理规则
        $support_ratio = $total_weight > 0 ? $support_weight / $total_weight : 0;
        $passed = $support_ratio >= 0.7;
        
        return array(
            'total_weight' => round($total_weight, 2),
            'support_weight' => round($support_weight, 2),
            'opposition_weight' => round($opposition_weight, 2),
            'support_ratio' => round($support_ratio * 100, 2),
            'opposition_ratio' => round((1 - $support_ratio) * 100, 2),
            'passed' => $passed,
            'threshold' => 70,
            'voter_count' => $voter_count
        );
    }
    
    /**
     * 更新提案统计
     */
    function update_proposal_stats($proposal_id) {
        $stats = $this->tally_votes($proposal_id);
        
        C::t('#cnsh#cnsh_proposals')->update($proposal_id, array(
            'total_weight' => $stats['total_weight'],
            'support_weight' => $stats['support_weight']
        ));
        
        // 检查是否达到70%通过
        $proposal = C::t('#cnsh#cnsh_proposals')->fetch($proposal_id);
        if ($stats['passed'] && $proposal['status'] == 0) {
            // 自动通过
            C::t('#cnsh#cnsh_proposals')->update($proposal_id, array(
                'status' => 1,
                'executed_at' => TIMESTAMP
            ));
            
            // 执行提案
            $this->execute_proposal($proposal);
        }
    }
    
    /**
     * 执行通过的提案
     */
    function execute_proposal($proposal) {
        // 根据提案类型执行
        switch ($proposal['type']) {
            case 1: // 社区规则
                // 更新规则缓存
                break;
            case 2: // 版主任免
                // 更新版主权限
                break;
            case 3: // 资金分配
                // 执行资金转移
                break;
        }
        
        // 记录执行日志
        $this->log_execution($proposal);
    }
    
    /**
     * 验证投票签名
     */
    function verify_vote_signature($dna, $proposal_id, $choice, $signature) {
        global $_G;
        $shield_api = $_G['cache']['plugin']['cnsh']['shield_api'] ?: 'http://localhost:16384';
        
        $message = "VOTE:{$proposal_id}:{$choice}:" . TIMESTAMP;
        
        $post_data = array(
            'action' => 'verify_signature',
            'dna' => $dna,
            'message' => $message,
            'signature' => $signature
        );
        
        $response = dfsockopen($shield_api . '/api/verify_signature', 0, http_build_query($post_data));
        $result = json_decode($response, true);
        
        return $result && $result['valid'];
    }
    
    /**
     * 同步到CNSH链
     */
    function sync_vote_to_cnsh($vote_data) {
        // 异步同步到链上
        // 实际实现需要调用CNSH护盾API
    }
    
    function sync_proposal_to_cnsh($proposal_id, $data) {
        // 同步提案到链上
    }
    
    /**
     * 记录执行日志
     */
    function log_execution($proposal) {
        $log = array(
            'proposal_id' => $proposal['id'],
            'executed_by' => 'system',
            'executed_at' => TIMESTAMP,
            'result' => 'success'
        );
        C::t('#cnsh#cnsh_execution_log')->insert($log);
    }
}
?>
