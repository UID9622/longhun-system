# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐉 龍魂 · 生态节点数据架构统一建表引擎 v1.0
DNA: #龍芯⚡️丙午·丙申·癸亥·戊午·䷚颐-ECOSYSTEM-SCHEMA-ENGINE-V1.0
创建者: 诸葛鑫（UID9622）
License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)

功能:
  - init   : 按文档 12_DOCS/dragon-soul-open-hub/ECOSYSTEM-NODE-DATA-ARCHITECTURE-v1.0.md
             自动创建全部 30 张表 (16节点 + 横切基础设施)
  - verify : 校验已建表完整性
  - drop   : 冻结所有表（只标记 frozen，不物理删除，符合"不删除只冻结"铁律）
用法:
  python3 lh_ecosystem_schema.py init    # 建库建表
  python3 lh_ecosystem_schema.py verify  # 校验
"""
import os
import sqlite3
import sys
import json
from datetime import datetime, timezone

DB_PATH = os.path.join(os.path.expanduser("~"), ".longhun", "ecosystem.db")
DB_DIR = os.path.dirname(DB_PATH)

# ── 横切基础设施 (5表) ──────────────────────────────
SCHEMA = {}

SCHEMA["dna_registry"] = """
CREATE TABLE IF NOT EXISTS dna_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL UNIQUE,
    node_id VARCHAR(32) NOT NULL,
    entity_type VARCHAR(20) NOT NULL,
    owner_uid VARCHAR(32) NOT NULL,
    parent_dna VARCHAR(64),
    hash8 CHAR(8) NOT NULL,
    gpg_signature VARCHAR(128),
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active'
);
CREATE INDEX IF NOT EXISTS idx_dna_node ON dna_registry(node_id);
CREATE INDEX IF NOT EXISTS idx_dna_owner ON dna_registry(owner_uid);
"""

SCHEMA["audit_logs"] = """
CREATE TABLE IF NOT EXISTS audit_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    node_id VARCHAR(32) NOT NULL,
    operation VARCHAR(50) NOT NULL,
    target_type VARCHAR(20),
    target_id VARCHAR(64),
    operator_uid VARCHAR(32),
    tri_color CHAR(2),
    details TEXT,
    ip_hash VARCHAR(16),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_audit_node ON audit_logs(node_id);
CREATE INDEX IF NOT EXISTS idx_audit_time ON audit_logs(created_at);
"""

SCHEMA["shame_wall"] = """
CREATE TABLE IF NOT EXISTS shame_wall (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    node_id VARCHAR(32),
    reason TEXT NOT NULL,
    severity VARCHAR(10),
    evidence TEXT,
    tri_color CHAR(2) DEFAULT '🔴',
    resolved BOOLEAN DEFAULT FALSE,
    resolved_at TIMESTAMP,
    resolved_by VARCHAR(32),
    resolution_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["skill_registry"] = """
CREATE TABLE IF NOT EXISTS skill_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_id VARCHAR(32) NOT NULL UNIQUE,
    node_id VARCHAR(32) NOT NULL,
    category VARCHAR(20) NOT NULL,
    name VARCHAR(64) NOT NULL,
    entry VARCHAR(128),
    params TEXT,
    output_schema TEXT,
    rate_limit INTEGER DEFAULT 60,
    tri_color CHAR(2) DEFAULT '🟢',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_skill_node ON skill_registry(node_id);
"""

SCHEMA["ecosystem_passports"] = """
CREATE TABLE IF NOT EXISTS ecosystem_passports (
    uid VARCHAR(32) PRIMARY KEY,
    dna_hash VARCHAR(64) NOT NULL,
    member_level VARCHAR(10) NOT NULL,
    eco_role VARCHAR(20) DEFAULT 'free_user',
    status VARCHAR(10) DEFAULT 'active',
    persona_pref VARCHAR(32) DEFAULT 'P00-文心',
    monthly_verify_expire VARCHAR(10),
    first_verify_date VARCHAR(10),
    continuous_months INTEGER DEFAULT 0,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS subscription_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR(32) NOT NULL,
    level VARCHAR(10) NOT NULL,
    start_time VARCHAR(19) NOT NULL,
    expire_time VARCHAR(19) NOT NULL,
    auto_renew BOOLEAN DEFAULT TRUE,
    pay_method VARCHAR(10) DEFAULT 'xpay',
    tx_id VARCHAR(64),
    renew_count INTEGER DEFAULT 0,
    paid_months INTEGER DEFAULT 0,
    tri_color CHAR(2) DEFAULT '🟢'
);
CREATE TABLE IF NOT EXISTS auth_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR(32) NOT NULL,
    auth_time VARCHAR(19) NOT NULL,
    auth_method VARCHAR(20) NOT NULL,
    auth_result VARCHAR(10) NOT NULL,
    challenge_code VARCHAR(32),
    response_hash VARCHAR(32)
);
CREATE TABLE IF NOT EXISTS api_keys (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR(32) NOT NULL,
    key_id VARCHAR(32) NOT NULL,
    key_hash VARCHAR(16) NOT NULL,
    key_prefix VARCHAR(16) NOT NULL,
    purpose VARCHAR(64) DEFAULT '',
    scopes TEXT DEFAULT '[]',
    status VARCHAR(10) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used_at TIMESTAMP
);
"""

# ── free 层 (N01-N05) ──────────────────────────────
SCHEMA["node_n01_compute_guard"] = """
CREATE TABLE IF NOT EXISTS node_n01_health_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    check_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    host VARCHAR(32) NOT NULL,
    service_count INTEGER,
    healthy_count INTEGER,
    failed_services TEXT,
    cpu_percent REAL,
    mem_percent REAL,
    disk_percent REAL,
    auto_healed BOOLEAN DEFAULT FALSE,
    bark_pushed BOOLEAN DEFAULT FALSE,
    tri_color CHAR(2) DEFAULT '🟢'
);
CREATE INDEX IF NOT EXISTS idx_n01_time ON node_n01_health_checks(check_time);
"""

SCHEMA["node_n02_dna"] = """
CREATE TABLE IF NOT EXISTS node_n02_dna_assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL UNIQUE,
    asset_name VARCHAR(128) NOT NULL,
    asset_type VARCHAR(20) NOT NULL,
    asset_path VARCHAR(256),
    size_bytes INTEGER,
    content_hash VARCHAR(16),
    gpg_signed BOOLEAN DEFAULT FALSE,
    gpg_signature_path VARCHAR(256),
    merklet_root VARCHAR(64),
    owner_uid VARCHAR(32) DEFAULT 'UID9622',
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_n02_type ON node_n02_dna_assets(asset_type);
"""

SCHEMA["node_n03_xpay"] = """
CREATE TABLE IF NOT EXISTS node_n03_transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tx_id VARCHAR(64) NOT NULL UNIQUE,
    dna VARCHAR(64) NOT NULL,
    amount REAL NOT NULL,
    currency VARCHAR(8) NOT NULL,
    sender_uid VARCHAR(32) NOT NULL,
    recipient_uid VARCHAR(32) NOT NULL,
    purpose VARCHAR(64),
    memo TEXT,
    processing_fee REAL DEFAULT 0,
    dna_fee REAL DEFAULT 0,
    total_fee REAL DEFAULT 0,
    status VARCHAR(20) NOT NULL,
    settlement_ref VARCHAR(64),
    sovereign_country VARCHAR(4) DEFAULT 'CN',
    gateway_mode VARCHAR(10) DEFAULT 'sandbox',
    hmac_signature VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_n03_uid ON node_n03_transactions(sender_uid);
CREATE TABLE IF NOT EXISTS node_n03_balances (
    uid VARCHAR(32) PRIMARY KEY,
    balance REAL DEFAULT 0,
    locked_balance REAL DEFAULT 0,
    total_in REAL DEFAULT 0,
    total_out REAL DEFAULT 0,
    currency VARCHAR(8) DEFAULT 'CNY',
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["node_n04_tongxinyi"] = """
CREATE TABLE IF NOT EXISTS node_n04_translations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    src_lang VARCHAR(10) NOT NULL,
    dst_lang VARCHAR(10) NOT NULL,
    src_text TEXT NOT NULL,
    dst_text TEXT NOT NULL,
    semantic_score REAL,
    model_used VARCHAR(32),
    embedding TEXT,
    user_uid VARCHAR(32),
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n04_terms (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    term VARCHAR(64) NOT NULL,
    meaning TEXT,
    bridge_code VARCHAR(128),
    category VARCHAR(20),
    glyph_version VARCHAR(8),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(term, category)
);
"""

SCHEMA["node_n05_voice"] = """
CREATE TABLE IF NOT EXISTS node_n05_voices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,
    voice_id VARCHAR(32) NOT NULL UNIQUE,
    voice_name VARCHAR(64),
    voice_file VARCHAR(256),
    voiceprint_hash VARCHAR(64),
    duration_sec REAL,
    sample_rate INTEGER,
    format VARCHAR(10),
    model_id VARCHAR(32),
    status VARCHAR(20) DEFAULT 'active',
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_n05_uid ON node_n05_voices(uid);
"""

# ── basic 层 (N06-N14) ─────────────────────────────
SCHEMA["node_n06_cnsh"] = """
CREATE TABLE IF NOT EXISTS node_n06_cnsh_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    project_id VARCHAR(32) NOT NULL UNIQUE,
    project_name VARCHAR(64) NOT NULL,
    src_code TEXT,
    compiled_code TEXT,
    ast_json TEXT,
    errors TEXT,
    diagnostics TEXT,
    user_uid VARCHAR(32),
    embedding TEXT,
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n06_syntax_errors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    project_id VARCHAR(32),
    error_type VARCHAR(32),
    error_msg TEXT,
    suggestion TEXT,
    model_suggestion TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["node_n07_wishing"] = """
CREATE TABLE IF NOT EXISTS node_n07_wishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    wish_id VARCHAR(32) NOT NULL UNIQUE,
    wish_title VARCHAR(128) NOT NULL,
    wish_desc TEXT,
    wish_type VARCHAR(20),
    creator_uid VARCHAR(32) NOT NULL,
    target_amount REAL,
    current_amount REAL DEFAULT 0,
    supporters INTEGER DEFAULT 0,
    status VARCHAR(20) DEFAULT 'open',
    deadline VARCHAR(19),
    tags TEXT DEFAULT '[]',
    embedding TEXT,
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n07_supports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    wish_id VARCHAR(32) NOT NULL,
    supporter_uid VARCHAR(32) NOT NULL,
    amount REAL NOT NULL,
    message TEXT,
    tx_id VARCHAR(64),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["node_n08_decision"] = """
CREATE TABLE IF NOT EXISTS node_n08_decision_cards (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    hash8 CHAR(8) NOT NULL,
    card_type VARCHAR(20) NOT NULL,
    decision_level VARCHAR(5),
    title VARCHAR(128) NOT NULL,
    trigger_input TEXT,
    selected_option TEXT,
    alternatives TEXT DEFAULT '[]',
    tri_color CHAR(2),
    responsibility_owner VARCHAR(32),
    reversible BOOLEAN DEFAULT FALSE,
    context TEXT,
    reasoning TEXT,
    embedding TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX IF NOT EXISTS idx_n08_hash ON node_n08_decision_cards(hash8);
"""

SCHEMA["node_n09_filter"] = """
CREATE TABLE IF NOT EXISTS node_n09_filter_rules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    rule_id VARCHAR(32) NOT NULL UNIQUE,
    rule_name VARCHAR(64) NOT NULL,
    rule_type VARCHAR(20) NOT NULL,
    pattern TEXT NOT NULL,
    severity VARCHAR(10) NOT NULL,
    action VARCHAR(20) NOT NULL,
    tri_color CHAR(2) DEFAULT '🟢',
    enabled BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n09_filter_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    content_hash VARCHAR(16) NOT NULL,
    matched_rule VARCHAR(32),
    severity VARCHAR(10),
    action_taken VARCHAR(20),
    content_preview TEXT,
    tri_color CHAR(2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["node_n10_lora"] = """
CREATE TABLE IF NOT EXISTS node_n10_lora_models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    model_id VARCHAR(32) NOT NULL UNIQUE,
    model_name VARCHAR(64) NOT NULL,
    base_model VARCHAR(32),
    rank INTEGER,
    alpha INTEGER,
    train_data_count INTEGER,
    val_loss REAL,
    dataset_version VARCHAR(16),
    status VARCHAR(20) DEFAULT 'training',
    artifact_path VARCHAR(256),
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n10_train_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    model_id VARCHAR(32) NOT NULL,
    epoch INTEGER,
    loss REAL,
    lr REAL,
    elapsed_sec REAL,
    metrics TEXT,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    status VARCHAR(20)
);
"""

SCHEMA["node_n11_memory"] = """
CREATE TABLE IF NOT EXISTS node_n11_memory_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    entry_id VARCHAR(36) NOT NULL UNIQUE,
    category VARCHAR(20) NOT NULL,
    title VARCHAR(128) NOT NULL,
    content TEXT NOT NULL,
    keywords TEXT DEFAULT '[]',
    creator VARCHAR(32) NOT NULL,
    collaborator_signature VARCHAR(64),
    source VARCHAR(64),
    priority INTEGER DEFAULT 0,
    embedding TEXT,
    vector TEXT,
    backfilled BOOLEAN DEFAULT FALSE,
    notion_url VARCHAR(256),
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n11_memory_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_id VARCHAR(36) NOT NULL,
    target_id VARCHAR(36) NOT NULL,
    relation VARCHAR(20),
    weight REAL DEFAULT 1.0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["node_n12_persona"] = """
CREATE TABLE IF NOT EXISTS node_n12_personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    persona_id VARCHAR(16) NOT NULL UNIQUE,
    name VARCHAR(32) NOT NULL,
    layer VARCHAR(10) NOT NULL,
    function VARCHAR(64) NOT NULL,
    duty_weight REAL DEFAULT 0,
    engine_path VARCHAR(128),
    config_path VARCHAR(128),
    trigger_keywords TEXT DEFAULT '[]',
    status VARCHAR(20) DEFAULT 'active',
    last_triggered TIMESTAMP,
    trigger_count INTEGER DEFAULT 0,
    lock_until TIMESTAMP,
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n12_routing_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    intent TEXT,
    routed_to VARCHAR(16) NOT NULL,
    confidence REAL,
    co_agents TEXT DEFAULT '[]',
    debounce_locked BOOLEAN DEFAULT FALSE,
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["node_n13_eye"] = """
CREATE TABLE IF NOT EXISTS node_n13_audit_reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    report_id VARCHAR(32) NOT NULL UNIQUE,
    audit_target VARCHAR(128) NOT NULL,
    audit_type VARCHAR(20) NOT NULL,
    gates_passed INTEGER DEFAULT 0,
    gates_total INTEGER DEFAULT 11,
    tri_color CHAR(2) NOT NULL,
    risk_score REAL,
    findings TEXT DEFAULT '[]',
    recommendations TEXT DEFAULT '[]',
    auditor_persona VARCHAR(16),
    co_auditor VARCHAR(16),
    gpg_signature VARCHAR(128),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n13_gate_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    report_id VARCHAR(32) NOT NULL,
    gate_no VARCHAR(8) NOT NULL,
    gate_name VARCHAR(32) NOT NULL,
    result VARCHAR(10) NOT NULL,
    detail TEXT,
    checked_by VARCHAR(16),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["node_n14_executor"] = """
CREATE TABLE IF NOT EXISTS node_n14_tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    task_id VARCHAR(32) NOT NULL UNIQUE,
    task_name VARCHAR(128) NOT NULL,
    task_type VARCHAR(20),
    prompt TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    orchestrator VARCHAR(16),
    agents TEXT DEFAULT '[]',
    steps TEXT DEFAULT '[]',
    progress REAL DEFAULT 0,
    result TEXT,
    error TEXT,
    user_uid VARCHAR(32) DEFAULT 'UID9622',
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    finished_at TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n14_exec_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    task_id VARCHAR(32) NOT NULL,
    step_no INTEGER,
    agent VARCHAR(16),
    action TEXT,
    result TEXT,
    elapsed_ms INTEGER,
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ── pro 层 (N15-N16) ───────────────────────────────
SCHEMA["node_n15_trust"] = """
CREATE TABLE IF NOT EXISTS node_n15_trust_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,
    tech_score REAL DEFAULT 0,
    community_score REAL DEFAULT 0,
    creation_score REAL DEFAULT 0,
    total_score REAL DEFAULT 0,
    bucket_type VARCHAR(20),
    contribution_log TEXT DEFAULT '[]',
    polit_check VARCHAR(20),
    state_own_check VARCHAR(20),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tri_color CHAR(2) DEFAULT '🟢',
    UNIQUE(uid)
);
CREATE TABLE IF NOT EXISTS node_n15_contribution_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    event_desc TEXT,
    score_delta REAL,
    scene_matrix TEXT,
    notarizer VARCHAR(16) DEFAULT 'P20',
    evidence TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SCHEMA["node_n16_daoyin"] = """
CREATE TABLE IF NOT EXISTS node_n16_guidance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,
    guidance_type VARCHAR(20) NOT NULL,
    question TEXT,
    guidance TEXT NOT NULL,
    anchor_chapter VARCHAR(16),
    model_used VARCHAR(32),
    user_feedback INTEGER DEFAULT 0,
    embedding TEXT,
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS node_n16_daodejing_anchors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter_no INTEGER NOT NULL UNIQUE,
    chapter_title VARCHAR(64) NOT NULL,
    original_text TEXT NOT NULL,
    plain_explanation TEXT,
    algorithmic_anchor TEXT,
    philosophic_concept TEXT,
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

# ── founder 层 ─────────────────────────────────────
SCHEMA["node_founder_governance"] = """
CREATE TABLE IF NOT EXISTS node_founder_governance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna VARCHAR(64) NOT NULL,
    uid VARCHAR(32) NOT NULL,
    governance_role VARCHAR(32),
    proposals_submitted INTEGER DEFAULT 0,
    proposals_voted INTEGER DEFAULT 0,
    monthly_verified INTEGER DEFAULT 0,
    continuous_months INTEGER DEFAULT 0,
    contribution_points REAL DEFAULT 0,
    trust_score REAL DEFAULT 0,
    last_verify_date VARCHAR(10),
    status VARCHAR(20) DEFAULT 'active',
    tri_color CHAR(2) DEFAULT '🟢',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""


def _connect():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def cmd_init():
    conn = _connect()
    created = 0
    for name, ddl in SCHEMA.items():
        for stmt in ddl.strip().split(";"):
            stmt = stmt.strip()
            if stmt:
                conn.execute(stmt)
        created += 1
    conn.commit()
    conn.close()
    print(f"✅ 生态库已建: {DB_PATH}")
    print(f"   共创建 {len(SCHEMA)} 组 schema / 30+ 张表")


def cmd_verify():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in cur.fetchall()]
    conn.close()
    expected = []
    for name, ddl in SCHEMA.items():
        for line in ddl.strip().splitlines():
            line = line.strip()
            if line.upper().startswith("CREATE TABLE"):
                expected.append(line.split("(")[0].replace("CREATE TABLE IF NOT EXISTS", "").strip())
    missing = [t for t in expected if t not in tables]
    print(f"已建表: {len(tables)} 张")
    print(f"应有表: {len(expected)} 张")
    if missing:
        print(f"❌ 缺失: {missing}")
        return 1
    print("✅ 全部表已就位")
    return 0


def cmd_freeze():
    """不删除只冻结：标记 shame_wall + 追加冻结审计"""
    conn = _connect()
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO shame_wall (dna, node_id, reason, severity, tri_color) "
        "VALUES (?, ?, ?, ?, ?)",
        (f"#龍芯⚡️{now}-SCHEMA-FREEZE", "system",
         f"生态schema冻结操作 @{now}", "MEDIUM", "🟡"),
    )
    conn.commit()
    conn.close()
    print(f"✅ 已冻结留档（记录入耻辱墙）@{now}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if cmd == "init":
        cmd_init()
    elif cmd == "verify":
        return cmd_verify()
    elif cmd == "freeze":
        cmd_freeze()
    else:
        print(f"用法: {sys.argv[0]} [init|verify|freeze]")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
