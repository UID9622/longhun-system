<?php
/**
 * CNSH-64 DNA绑定模块
 * 虚拟身份与现实身份的锚定点
 */

if(!defined('IN_DISCUZ')) {
    exit('Access Denied');
}

class plugin_cnsh_dna {
    
    var $config = array();
    
    function __construct() {
        global $_G;
        $this->config = $_G['cache']['plugin']['cnsh'];
    }
    
    /**
     * 在用户资料页显示DNA绑定状态
     */
    function profile_baseinfo_top() {
        global $_G;
        $uid = $_G['uid'];
        
        if (!$uid) return '';
        
        // 查询DNA绑定状态
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($uid);
        
        if ($binding && $binding['status'] == 1) {
            // 已绑定，显示DNA信息和信誉
            $dna_short = substr($binding['dna'], 0, 12) . '...' . substr($binding['dna'], -6);
            $reputation = floatval($binding['reputation']);
            $level = $this->get_reputation_level($reputation);
            $level_class = $this->get_level_class($reputation);
            $heart_icon = $this->get_heart_icon($binding['heart_seed_hash']);
            
            return <<<HTML
<style>
.cnsh-dna-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    color: #fff;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.cnsh-dna-card h3 {
    margin: 0 0 15px 0;
    font-size: 16px;
    color: #00d4ff;
    display: flex;
    align-items: center;
    gap: 8px;
}
.dna-info {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 15px;
}
.dna-address {
    font-family: monospace;
    background: rgba(0,212,255,0.1);
    padding: 8px 12px;
    border-radius: 6px;
    font-size: 13px;
    color: #00d4ff;
}
.dna-status {
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
}
.dna-status.verified {
    background: #00c853;
    color: #fff;
}
.reputation-bar {
    height: 8px;
    background: rgba(255,255,255,0.1);
    border-radius: 4px;
    overflow: hidden;
    margin-bottom: 10px;
}
.reputation-fill {
    height: 100%;
    background: linear-gradient(90deg, #ff4757 0%, #ffa502 50%, #00c853 100%);
    border-radius: 4px;
    transition: width 0.5s ease;
}
.reputation-level {
    font-size: 14px;
    color: #aaa;
}
.reputation-level strong {
    color: #fff;
    font-size: 16px;
}
.heart-seed {
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid rgba(255,255,255,0.1);
    font-size: 12px;
    color: #888;
}
</style>
<div class="cnsh-dna-card">
    <h3>🧬 CNSH-DNA身份</h3>
    <div class="dna-info">
        <span class="dna-address">{$dna_short}</span>
        <span class="dna-status verified">✓ 已验证</span>
    </div>
    <div class="reputation-bar">
        <div class="reputation-fill" style="width: {$reputation}%"></div>
    </div>
    <div class="reputation-level">
        信誉等级: <strong class="{$level_class}">{$level}</strong> 
        <span style="color:#666">({$reputation}/100)</span>
    </div>
    <div class="heart-seed">
        {$heart_icon} 心种子: {$binding['heart_seed_hash']}
    </div>
</div>
HTML;
        } else {
            // 未绑定，显示绑定入口
            return <<<HTML
<style>
.cnsh-dna-card.unbound {
    background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    color: #fff;
    text-align: center;
}
.cnsh-dna-card.unbound h3 {
    margin: 0 0 10px 0;
    color: #b2bec3;
}
.cnsh-dna-card.unbound p {
    color: #dfe6e9;
    margin-bottom: 15px;
}
.btn-bind {
    display: inline-block;
    background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
    color: #fff;
    padding: 12px 30px;
    border-radius: 25px;
    text-decoration: none;
    font-weight: bold;
    transition: all 0.3s;
}
.btn-bind:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 20px rgba(0,212,255,0.4);
}
</style>
<div class="cnsh-dna-card unbound">
    <h3>🧬 CNSH-DNA身份</h3>
    <p>尚未绑定DNA身份，绑定后可获得：<br>
    ✓ 信誉体系 ✓ 治理投票权 ✓ 数字人民币钱包</p>
    <a href="plugin.php?id=cnsh:bind" class="btn-bind">立即绑定DNA</a>
</div>
HTML;
        }
    }
    
    /**
     * 根据信誉分计算等级
     */
    function get_reputation_level($score) {
        if ($score >= 90) return '圣心';
        if ($score >= 70) return '明心';
        if ($score >= 50) return '初心';
        if ($score >= 30) return '迷心';
        return '浊心';
    }
    
    /**
     * 获取等级样式类
     */
    function get_level_class($score) {
        if ($score >= 90) return 'level-sage';
        if ($score >= 70) return 'level-clear';
        if ($score >= 50) return 'level-initial';
        if ($score >= 30) return 'level-lost';
        return 'level-turbid';
    }
    
    /**
     * 获取心种子图标
     */
    function get_heart_icon($hash) {
        if (empty($hash)) return '🌱';
        $first_char = substr($hash, 0, 1);
        $icons = array('0'=>'💎','1'=>'🌟','2'=>'🔥','3'=>'💧','4'=>'🌿',
                      '5'=>'⚡','6'=>'🌙','7'=>'☀️','8'=>'🌊','9'=>'🍃',
                      'a'=>'🔮','b'=>'🎯','c'=>'🎪','d'=>'🎨','e'=>'🎭','f'=>'🎪');
        return $icons[$first_char] ?? '🌱';
    }
    
    /**
     * 在帖子作者信息中显示DNA标识
     */
    function viewthread_authorinfo($param) {
        global $post;
        
        $uid = $post['authorid'];
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($uid);
        
        if ($binding && $binding['status'] == 1) {
            $level = $this->get_reputation_level($binding['reputation']);
            return <<<HTML
<span class="cnsh-dna-badge" title="CNSH-DNA已验证: {$binding['dna']}">
    🧬 {$level}
</span>
<style>
.cnsh-dna-badge {
    display: inline-block;
    background: linear-gradient(135deg, #00d4ff 0%, #0099cc 100%);
    color: #fff;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    margin-left: 5px;
}
</style>
HTML;
        }
        return '';
    }
}

/**
 * DNA绑定页面控制器
 */
class cnsh_bind {
    
    function __construct() {
        global $_G;
        if (!$_G['uid']) {
            showmessage('请先登录', 'member.php?mod=logging&action=login');
        }
    }
    
    /**
     * 绑定页面
     */
    function index() {
        global $_G;
        
        $uid = $_G['uid'];
        $existing = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($uid);
        
        if ($existing) {
            showmessage('您已绑定DNA', 'home.php?mod=spacecp&ac=profile');
        }
        
        include template('cnsh:bind');
    }
    
    /**
     * 处理绑定请求
     */
    function do_bind() {
        global $_G;
        
        $uid = $_G['uid'];
        $dna = trim($_GET['dna']);
        $signature = trim($_GET['signature']);
        $timestamp = intval($_GET['timestamp']);
        
        // 验证参数
        if (empty($dna) || empty($signature)) {
            showmessage('参数不完整');
        }
        
        // 验证时间戳（5分钟内有效）
        if (abs(TIMESTAMP - $timestamp) > 300) {
            showmessage('签名已过期，请重新生成');
        }
        
        // 调用CNSH护盾验证
        $verify_result = $this->verify_dna_binding($dna, $uid, $timestamp, $signature);
        
        if (!$verify_result['success']) {
            showmessage('验证失败: ' . $verify_result['error']);
        }
        
        // 检查DNA是否已被封禁
        if ($verify_result['banned']) {
            showmessage('该DNA已被封禁，无法绑定');
        }
        
        // 检查绑定上限
        $existing_bindings = C::t('#cnsh#cnsh_dna_binding')->count_by_dna($dna);
        if ($existing_bindings >= 5) {
            showmessage('该DNA已绑定5个身份，达到上限');
        }
        
        // 创建绑定
        $data = array(
            'uid' => $uid,
            'dna' => $dna,
            'reputation' => $verify_result['reputation'] ?: 50.00,
            'heart_seed_hash' => $verify_result['heart_seed'] ?: '',
            'bound_at' => TIMESTAMP,
            'status' => 1
        );
        
        C::t('#cnsh#cnsh_dna_binding')->insert($data);
        
        // 更新用户组
        $this->update_user_group($uid, $data['reputation']);
        
        // 记录日志
        $this->log_binding($uid, $dna, 'bind');
        
        showmessage('DNA绑定成功！', 'home.php?mod=spacecp&ac=profile', array(), array('showdialog' => 1));
    }
    
    /**
     * 验证DNA绑定
     */
    function verify_dna_binding($dna, $uid, $timestamp, $signature) {
        $shield_api = $this->get_shield_api();
        
        $post_data = array(
            'action' => 'verify_binding',
            'dna' => $dna,
            'uid' => $uid,
            'timestamp' => $timestamp,
            'signature' => $signature
        );
        
        $response = dfsockopen($shield_api . '/api/verify_binding', 0, http_build_query($post_data));
        $result = json_decode($response, true);
        
        return $result ?: array('success' => false, 'error' => '无法连接CNSH护盾');
    }
    
    /**
     * 更新用户组
     */
    function update_user_group($uid, $reputation) {
        // 根据信誉分分配用户组
        $groupid = 10; // 默认
        if ($reputation >= 90) $groupid = 1;  // 管理员级
        elseif ($reputation >= 70) $groupid = 2;  // 超级版主
        elseif ($reputation >= 50) $groupid = 3;  // 版主
        elseif ($reputation >= 30) $groupid = 11; // 正式会员
        
        C::t('common_member')->update($uid, array('groupid' => $groupid));
    }
    
    /**
     * 记录绑定日志
     */
    function log_binding($uid, $dna, $action) {
        $log_data = array(
            'uid' => $uid,
            'dna' => $dna,
            'action' => $action,
            'ip' => getglobal('clientip'),
            'created_at' => TIMESTAMP
        );
        C::t('#cnsh#cnsh_binding_log')->insert($log_data);
    }
    
    /**
     * 获取护盾API地址
     */
    function get_shield_api() {
        global $_G;
        return $_G['cache']['plugin']['cnsh']['shield_api'] ?: 'http://localhost:16384';
    }
}
?>
