-- CNSH-64 社区系统数据库安装脚本
-- Discuz! X3.5 插件

-- DNA绑定表
DROP TABLE IF EXISTS pre_cnsh_dna_binding;
CREATE TABLE pre_cnsh_dna_binding (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uid INT UNSIGNED NOT NULL COMMENT 'Discuz用户ID',
    dna VARCHAR(66) NOT NULL COMMENT 'CNSH-DNA地址',
    reputation DECIMAL(5,2) DEFAULT 50.00 COMMENT '信誉分(0-100)',
    heart_seed_hash VARCHAR(64) DEFAULT '' COMMENT '心种子哈希',
    bound_at INT UNSIGNED NOT NULL COMMENT '绑定时间',
    last_sync INT UNSIGNED DEFAULT 0 COMMENT '最后同步时间',
    status TINYINT DEFAULT 1 COMMENT '0=解绑,1=正常,2=封禁',
    UNIQUE KEY uk_uid (uid),
    UNIQUE KEY uk_dna (dna),
    KEY idx_reputation (reputation),
    KEY idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='CNSH-DNA绑定表';

-- 治理提案表
DROP TABLE IF EXISTS pre_cnsh_proposals;
CREATE TABLE pre_cnsh_proposals (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL COMMENT '提案标题',
    content TEXT COMMENT '提案内容',
    proposer_uid INT UNSIGNED NOT NULL COMMENT '提案人UID',
    proposer_dna VARCHAR(66) NOT NULL COMMENT '提案人DNA',
    type TINYINT DEFAULT 1 COMMENT '1=社区规则,2=版主任免,3=资金分配',
    status TINYINT DEFAULT 0 COMMENT '0=投票中,1=通过,2=否决,3=执行中,4=已完成',
    start_time INT UNSIGNED NOT NULL COMMENT '开始时间',
    end_time INT UNSIGNED NOT NULL COMMENT '结束时间',
    total_weight DECIMAL(10,2) DEFAULT 0 COMMENT '总投票权重',
    support_weight DECIMAL(10,2) DEFAULT 0 COMMENT '支持权重',
    created_at INT UNSIGNED NOT NULL,
    executed_at INT UNSIGNED DEFAULT 0 COMMENT '执行时间',
    execution_tx VARCHAR(128) DEFAULT '' COMMENT '执行交易哈希',
    KEY idx_status (status),
    KEY idx_type (type),
    KEY idx_time (start_time, end_time),
    KEY idx_proposer (proposer_uid)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='治理提案表';

-- 投票记录表
DROP TABLE IF EXISTS pre_cnsh_votes;
CREATE TABLE pre_cnsh_votes (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    proposal_id INT UNSIGNED NOT NULL COMMENT '提案ID',
    uid INT UNSIGNED NOT NULL COMMENT '投票人UID',
    dna VARCHAR(66) NOT NULL COMMENT '投票人DNA',
    choice TINYINT NOT NULL COMMENT '1=支持,0=反对',
    weight DECIMAL(5,2) NOT NULL COMMENT '投票权重',
    signature VARCHAR(256) NOT NULL COMMENT '投票签名',
    voted_at INT UNSIGNED NOT NULL,
    synced TINYINT DEFAULT 0 COMMENT '是否同步到链上',
    UNIQUE KEY uk_proposal_uid (proposal_id, uid),
    KEY idx_dna (dna),
    KEY idx_proposal (proposal_id),
    KEY idx_voted_at (voted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='治理投票记录表';

-- 数字人民币打赏记录表
DROP TABLE IF EXISTS pre_cnsh_tips;
CREATE TABLE pre_cnsh_tips (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    from_uid INT UNSIGNED NOT NULL COMMENT '发送方UID',
    from_dna VARCHAR(66) NOT NULL COMMENT '发送方DNA',
    to_uid INT UNSIGNED NOT NULL COMMENT '接收方UID',
    to_dna VARCHAR(66) NOT NULL COMMENT '接收方DNA',
    amount DECIMAL(10,2) NOT NULL COMMENT '金额',
    tid INT UNSIGNED DEFAULT 0 COMMENT '关联帖子ID',
    pid INT UNSIGNED DEFAULT 0 COMMENT '关联回复ID',
    order_id VARCHAR(128) DEFAULT '' COMMENT '订单ID',
    tx_hash VARCHAR(128) DEFAULT '' COMMENT '交易哈希',
    status TINYINT DEFAULT 2 COMMENT '0=失败,1=成功,2=确认中',
    created_at INT UNSIGNED NOT NULL,
    confirmed_at INT UNSIGNED DEFAULT 0 COMMENT '确认时间',
    KEY idx_from_dna (from_dna),
    KEY idx_to_dna (to_dna),
    KEY idx_from_uid (from_uid),
    KEY idx_to_uid (to_uid),
    KEY idx_tx (tx_hash),
    KEY idx_order (order_id),
    KEY idx_status (status),
    KEY idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='数字人民币打赏记录表';

-- 信誉历史记录表
DROP TABLE IF EXISTS pre_cnsh_reputation_log;
CREATE TABLE pre_cnsh_reputation_log (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    dna VARCHAR(66) NOT NULL COMMENT 'DNA地址',
    old_score DECIMAL(5,2) NOT NULL COMMENT '原分数',
    new_score DECIMAL(5,2) NOT NULL COMMENT '新分数',
    change DECIMAL(5,2) NOT NULL COMMENT '变化值',
    reason VARCHAR(255) COMMENT '变动原因',
    related_uid INT UNSIGNED DEFAULT 0 COMMENT '相关用户',
    related_tx VARCHAR(128) DEFAULT '' COMMENT '相关交易',
    created_at INT UNSIGNED NOT NULL,
    KEY idx_dna (dna),
    KEY idx_time (created_at),
    KEY idx_related_tx (related_tx)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='信誉变动记录表';

-- DNA绑定日志表
DROP TABLE IF EXISTS pre_cnsh_binding_log;
CREATE TABLE pre_cnsh_binding_log (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    uid INT UNSIGNED NOT NULL COMMENT '用户ID',
    dna VARCHAR(66) NOT NULL COMMENT 'DNA地址',
    action VARCHAR(20) NOT NULL COMMENT 'bind/unbind',
    ip VARCHAR(40) COMMENT 'IP地址',
    created_at INT UNSIGNED NOT NULL,
    KEY idx_uid (uid),
    KEY idx_dna (dna),
    KEY idx_action (action),
    KEY idx_time (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='DNA绑定日志表';

-- 提案执行日志表
DROP TABLE IF EXISTS pre_cnsh_execution_log;
CREATE TABLE pre_cnsh_execution_log (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    proposal_id INT UNSIGNED NOT NULL COMMENT '提案ID',
    executed_by VARCHAR(50) DEFAULT 'system' COMMENT '执行者',
    executed_at INT UNSIGNED NOT NULL,
    result VARCHAR(20) DEFAULT 'success' COMMENT '执行结果',
    details TEXT COMMENT '执行详情',
    KEY idx_proposal (proposal_id),
    KEY idx_time (executed_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='提案执行日志表';

-- DNA封禁日志表
DROP TABLE IF EXISTS pre_cnsh_ban_log;
CREATE TABLE pre_cnsh_ban_log (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    dna VARCHAR(66) NOT NULL COMMENT 'DNA地址',
    reason VARCHAR(255) COMMENT '封禁原因',
    tx_hash VARCHAR(128) COMMENT '链上交易哈希',
    banned_at INT UNSIGNED NOT NULL,
    unbanned_at INT UNSIGNED DEFAULT 0 COMMENT '解封时间',
    unbanned_by INT UNSIGNED DEFAULT 0 COMMENT '解封操作者',
    KEY idx_dna (dna),
    KEY idx_time (banned_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='DNA封禁日志表';

-- 插入默认数据

-- 示例：创建一个测试提案（70%治理演示）
INSERT INTO pre_cnsh_proposals (
    title, content, proposer_uid, proposer_dna, type, status,
    start_time, end_time, created_at
) VALUES (
    '社区治理规则V1.0',
    '本提案确立CNSH社区的70%治理规则：\n1. 所有重大决策需获得70%投票权重支持\n2. 投票权重与DNA信誉分挂钩\n3. 版主任免需社区投票通过',
    1,
    '0x0000000000000000000000000000000000000000',
    1,
    0,
    UNIX_TIMESTAMP(),
    UNIX_TIMESTAMP() + 604800,
    UNIX_TIMESTAMP()
);
