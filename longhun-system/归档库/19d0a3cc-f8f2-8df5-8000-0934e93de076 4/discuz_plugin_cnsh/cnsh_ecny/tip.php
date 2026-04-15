<?php
/**
 * CNSH-64 数字人民币打赏模块
 * DNA绑定的点对点支付
 */

if(!defined('IN_DISCUZ')) {
    exit('Access Denied');
}

class plugin_cnsh_ecny {
    
    var $config = array();
    
    function __construct() {
        global $_G;
        $this->config = $_G['cache']['plugin']['cnsh'];
    }
    
    /**
     * 在帖子底部添加打赏按钮
     */
    function viewthread_bottom() {
        global $_G, $post;
        
        // 只显示在楼主帖子
        if ($post['first'] != 1) return '';
        
        $author_uid = $post['authorid'];
        $author_binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($author_uid);
        
        if (!$author_binding || $author_binding['status'] != 1) {
            return '<!-- 作者未绑定DNA，无法接收打赏 -->';
        }
        
        $author_dna = $author_binding['dna'];
        $author_dna_short = substr($author_dna, 0, 10) . '...' . substr($author_dna, -4);
        
        // 获取已收到的打赏总额
        $total_tips = C::t('#cnsh#cnsh_tips')->sum_by_to_dna($author_dna);
        $tip_count = C::t('#cnsh#cnsh_tips')->count_by_to_dna($author_dna);
        
        return <<<HTML
<style>
.cnsh-tip-box {
    background: linear-gradient(135deg, #fff5f5 0%, #ffe0e0 100%);
    border: 2px solid #ff6b6b;
    border-radius: 12px;
    padding: 20px;
    margin: 20px 0;
    text-align: center;
}
.cnsh-tip-box h4 {
    margin: 0 0 10px 0;
    color: #c92a2a;
    font-size: 18px;
}
.cnsh-tip-box .dna-info {
    font-size: 12px;
    color: #666;
    margin-bottom: 15px;
}
.cnsh-tip-box .dna-info code {
    background: #fff;
    padding: 2px 8px;
    border-radius: 4px;
    font-family: monospace;
}
.cnsh-tip-box .stats {
    font-size: 14px;
    color: #666;
    margin-bottom: 15px;
}
.cnsh-tip-box .stats strong {
    color: #c92a2a;
    font-size: 18px;
}
.tip-amounts {
    display: flex;
    justify-content: center;
    gap: 10px;
    flex-wrap: wrap;
}
.tip-amounts button {
    background: linear-gradient(135deg, #ff6b6b 0%, #c92a2a 100%);
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 20px;
    cursor: pointer;
    font-size: 14px;
    font-weight: bold;
    transition: all 0.3s;
}
.tip-amounts button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(255,107,107,0.4);
}
#cnsh-tip-qr {
    margin-top: 15px;
    min-height: 200px;
}
#cnsh-tip-qr img {
    max-width: 200px;
    border-radius: 8px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}
.tip-status {
    margin-top: 10px;
    padding: 10px;
    border-radius: 8px;
    font-size: 14px;
}
.tip-status.success {
    background: #d4edda;
    color: #155724;
}
.tip-status.pending {
    background: #fff3cd;
    color: #856404;
}
</style>
<div class="cnsh-tip-box">
    <h4>💰 数字人民币打赏</h4>
    <div class="dna-info">
        支持作者DNA: <code>{$author_dna_short}</code>
    </div>
    <div class="stats">
        已收到 <strong>¥{$total_tips}</strong> 来自 {$tip_count} 人
    </div>
    <div class="tip-amounts">
        <button onclick="cnshTip({$post['tid']}, '{$author_dna}', 0.1)">¥0.1</button>
        <button onclick="cnshTip({$post['tid']}, '{$author_dna}', 1)">¥1</button>
        <button onclick="cnshTip({$post['tid']}, '{$author_dna}', 10)">¥10</button>
        <button onclick="cnshTip({$post['tid']}, '{$author_dna}', 100)">¥100</button>
    </div>
    <div id="cnsh-tip-qr"></div>
    <div id="cnsh-tip-status"></div>
</div>
<script>
var checkInterval = null;

function cnshTip(tid, toDna, amount) {
    // 清除之前的检查
    if (checkInterval) {
        clearInterval(checkInterval);
    }
    
    document.getElementById('cnsh-tip-qr').innerHTML = '<p>正在生成支付二维码...</p>';
    document.getElementById('cnsh-tip-status').innerHTML = '';
    
    fetch('plugin.php?id=cnsh:ecny&action=create_tip', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: 'tid=' + tid + '&to_dna=' + encodeURIComponent(toDna) + '&amount=' + amount + '&formhash=' + document.querySelector('input[name="formhash"]').value
    })
    .then(r => r.json())
    .then(data => {
        if (data.error) {
            document.getElementById('cnsh-tip-qr').innerHTML = '<p style="color:red">' + data.error + '</p>';
            return;
        }
        
        document.getElementById('cnsh-tip-qr').innerHTML = 
            '<img src="' + data.qr_code + '" alt="扫码支付">' +
            '<p style="font-size:12px;color:#666;margin-top:10px">请使用数字人民币APP扫码支付</p>';
        
        // 开始轮询检查支付状态
        checkInterval = setInterval(function() {
            checkTipStatus(data.tip_id);
        }, 3000);
    })
    .catch(err => {
        document.getElementById('cnsh-tip-qr').innerHTML = '<p style="color:red">请求失败，请重试</p>';
    });
}

function checkTipStatus(tipId) {
    fetch('plugin.php?id=cnsh:ecny&action=check_tip&tip_id=' + tipId)
    .then(r => r.json())
    .then(data => {
        if (data.status === 'success') {
            clearInterval(checkInterval);
            document.getElementById('cnsh-tip-status').innerHTML = 
                '<div class="tip-status success">✓ 打赏成功！感谢您的支持</div>';
            document.getElementById('cnsh-tip-qr').innerHTML = '';
        } else if (data.status === 'failed') {
            clearInterval(checkInterval);
            document.getElementById('cnsh-tip-status').innerHTML = 
                '<div class="tip-status" style="background:#f8d7da;color:#721c24">✗ 支付失败</div>';
        }
    });
}
</script>
HTML;
    }
    
    /**
     * 在用户中心添加钱包入口
     */
    function spacecp_baseinfo_top() {
        global $_G;
        
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($_G['uid']);
        if (!$binding) return '';
        
        // 获取钱包余额
        $balance = $this->get_wallet_balance($binding['dna']);
        $total_received = C::t('#cnsh#cnsh_tips')->sum_by_to_dna($binding['dna']);
        $total_sent = C::t('#cnsh#cnsh_tips')->sum_by_from_dna($binding['dna']);
        
        return <<<HTML
<style>
.cnsh-wallet-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 12px;
    padding: 20px;
    margin: 15px 0;
    color: #fff;
}
.cnsh-wallet-card h3 {
    margin: 0 0 15px 0;
    font-size: 16px;
}
.wallet-balance {
    font-size: 32px;
    font-weight: bold;
    margin-bottom: 15px;
}
.wallet-stats {
    display: flex;
    gap: 20px;
    font-size: 13px;
    opacity: 0.9;
}
.wallet-actions {
    margin-top: 15px;
    display: flex;
    gap: 10px;
}
.wallet-actions a {
    background: rgba(255,255,255,0.2);
    color: #fff;
    padding: 8px 16px;
    border-radius: 6px;
    text-decoration: none;
    font-size: 13px;
}
.wallet-actions a:hover {
    background: rgba(255,255,255,0.3);
}
</style>
<div class="cnsh-wallet-card">
    <h3>💳 数字人民币钱包</h3>
    <div class="wallet-balance">¥{$balance}</div>
    <div class="wallet-stats">
        <span>累计收入: ¥{$total_received}</span>
        <span>累计支出: ¥{$total_sent}</span>
    </div>
    <div class="wallet-actions">
        <a href="plugin.php?id=cnsh:wallet">查看详情</a>
        <a href="plugin.php?id=cnsh:wallet&action=withdraw">提现</a>
    </div>
</div>
HTML;
    }
    
    /**
     * 获取钱包余额
     */
    function get_wallet_balance($dna) {
        global $_G;
        $ecny_api = $_G['cache']['plugin']['cnsh']['ecny_api'] ?: 'http://localhost:16385';
        
        $response = dfsockopen($ecny_api . '/api/balance?dna=' . urlencode($dna));
        $result = json_decode($response, true);
        
        return $result && isset($result['balance']) ? $result['balance'] : '0.00';
    }
}

/**
 * 数字人民币钱包控制器
 */
class cnsh_ecny {
    
    function __construct() {
        global $_G;
        if (!$_G['uid']) {
            showmessage('请先登录', 'member.php?mod=logging&action=login');
        }
    }
    
    /**
     * 钱包首页
     */
    function index() {
        global $_G;
        
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($_G['uid']);
        if (!$binding) {
            showmessage('请先绑定DNA身份', 'plugin.php?id=cnsh:bind');
        }
        
        $plugin = new plugin_cnsh_ecny();
        $balance = $plugin->get_wallet_balance($binding['dna']);
        
        // 获取交易记录
        $page = max(1, intval($_GET['page']));
        $transactions = $this->get_transactions($binding['dna'], $page);
        
        include template('cnsh:wallet');
    }
    
    /**
     * 创建打赏订单
     */
    function create_tip() {
        global $_G;
        
        $tid = intval($_POST['tid']);
        $to_dna = trim($_POST['to_dna']);
        $amount = floatval($_POST['amount']);
        
        // 验证参数
        if ($amount <= 0 || $amount > 1000) {
            echo json_encode(array('error' => '金额必须在0.01-1000元之间'));
            exit;
        }
        
        // 验证发送方DNA
        $from_binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_uid($_G['uid']);
        if (!$from_binding) {
            echo json_encode(array('error' => '请先绑定DNA身份'));
            exit;
        }
        
        // 验证接收方DNA
        $to_binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_dna($to_dna);
        if (!$to_binding) {
            echo json_encode(array('error' => '接收方未绑定DNA'));
            exit;
        }
        
        // 检查频率限制
        if (!$this->check_tip_limit($_G['uid'])) {
            echo json_encode(array('error' => '操作过于频繁，请稍后再试'));
            exit;
        }
        
        // 调用CNSH数字人民币模块创建订单
        $order = $this->create_ecny_order($from_binding['dna'], $to_dna, $amount, $tid);
        
        if (!$order['success']) {
            echo json_encode(array('error' => $order['error'] ?: '创建订单失败'));
            exit;
        }
        
        // 记录打赏
        $tip_id = C::t('#cnsh#cnsh_tips')->insert(array(
            'from_uid' => $_G['uid'],
            'from_dna' => $from_binding['dna'],
            'to_uid' => $to_binding['uid'],
            'to_dna' => $to_dna,
            'amount' => $amount,
            'tid' => $tid,
            'order_id' => $order['order_id'],
            'status' => 2, // 确认中
            'created_at' => TIMESTAMP
        ), true);
        
        echo json_encode(array(
            'success' => true,
            'tip_id' => $tip_id,
            'qr_code' => $order['qr_code'],
            'order_id' => $order['order_id']
        ));
        exit;
    }
    
    /**
     * 检查打赏频率限制
     */
    function check_tip_limit($uid) {
        // 检查最近60秒内是否有打赏
        $recent = C::t('#cnsh#cnsh_tips')->fetch_recent_by_uid($uid, 60);
        if ($recent) return false;
        
        // 检查今日总额
        $today_total = C::t('#cnsh#cnsh_tips')->sum_today_by_uid($uid);
        if ($today_total >= 5000) return false;
        
        return true;
    }
    
    /**
     * 检查打赏状态
     */
    function check_tip() {
        $tip_id = intval($_GET['tip_id']);
        $tip = C::t('#cnsh#cnsh_tips')->fetch($tip_id);
        
        if (!$tip) {
            echo json_encode(array('status' => 'not_found'));
            exit;
        }
        
        // 查询链上状态
        $chain_status = $this->query_ecny_status($tip['order_id']);
        
        if ($chain_status === 'confirmed') {
            // 更新状态
            C::t('#cnsh#cnsh_tips')->update($tip_id, array(
                'status' => 1,
                'tx_hash' => $chain_status['tx_hash'],
                'confirmed_at' => TIMESTAMP
            ));
            
            // 增加双方信誉
            $this->increase_reputation($tip['from_dna'], 0.5, '打赏他人');
            $this->increase_reputation($tip['to_dna'], 1, '收到打赏');
            
            echo json_encode(array('status' => 'success'));
        } else if ($chain_status === 'failed') {
            C::t('#cnsh#cnsh_tips')->update($tip_id, array('status' => 0));
            echo json_encode(array('status' => 'failed'));
        } else {
            echo json_encode(array('status' => 'pending'));
        }
        exit;
    }
    
    /**
     * 创建数字人民币订单
     */
    function create_ecny_order($from_dna, $to_dna, $amount, $tid) {
        global $_G;
        $ecny_api = $_G['cache']['plugin']['cnsh']['ecny_api'] ?: 'http://localhost:16385';
        
        $post_data = array(
            'action' => 'create_tip_order',
            'from_dna' => $from_dna,
            'to_dna' => $to_dna,
            'amount' => $amount,
            'reference' => 'TIP:' . $tid,
            'callback_url' => $_G['siteurl'] . 'plugin.php?id=cnsh:ecny&action=callback'
        );
        
        $response = dfsockopen($ecny_api . '/api/create_order', 0, http_build_query($post_data));
        return json_decode($response, true);
    }
    
    /**
     * 查询支付状态
     */
    function query_ecny_status($order_id) {
        global $_G;
        $ecny_api = $_G['cache']['plugin']['cnsh']['ecny_api'] ?: 'http://localhost:16385';
        
        $response = dfsockopen($ecny_api . '/api/order_status?order_id=' . urlencode($order_id));
        $result = json_decode($response, true);
        
        return $result ? $result['status'] : 'unknown';
    }
    
    /**
     * 增加信誉
     */
    function increase_reputation($dna, $amount, $reason) {
        $binding = C::t('#cnsh#cnsh_dna_binding')->fetch_by_dna($dna);
        if (!$binding) return;
        
        $old_score = floatval($binding['reputation']);
        $new_score = min($old_score + $amount, 100);
        
        C::t('#cnsh#cnsh_dna_binding')->update($binding['id'], array(
            'reputation' => $new_score
        ));
        
        // 记录日志
        C::t('#cnsh#cnsh_reputation_log')->insert(array(
            'dna' => $dna,
            'old_score' => $old_score,
            'new_score' => $new_score,
            'change' => $amount,
            'reason' => $reason,
            'created_at' => TIMESTAMP
        ));
    }
    
    /**
     * 获取交易记录
     */
    function get_transactions($dna, $page) {
        return C::t('#cnsh#cnsh_tips')->fetch_by_dna($dna, $page);
    }
}
?>
