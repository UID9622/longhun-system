// DNA: #龍芯⚡️丙午·丙申·壬子·子时·䷕贲-RUST-CORE-EVOLUTION-v2.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 协议: MulanPSL v2 (工程层)
// 模块: 四级熔断 · GATE闸口 · 降级矩阵 · 五层数据黑洞 · 一票否决词
//
// 对齐: 龍魂×CodeBuddy全对齐规则v2.4 第四章(四级熔断)·第三章(审计体系)
//       第十层(一票否决词)·第十一章(禁止场景)

use serde::{Deserialize, Serialize};
use sha2::Digest;

// ═══════════════════════════════════════════════════════════════
// §1. 四级熔断系统 (Meltdown / Circuit Breaker)
// ═══════════════════════════════════════════════════════════════

/// 熔断级别 — 对齐规则第四章
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum MeltdownLevel {
    /// ∞ / L0 伦理熔断 — 不可恢复
    Infinite,
    /// L1 数据熔断 — UID9622 人工 + GPG 签章
    Data,
    /// L2 人格熔断 — 人格重设
    Persona,
    /// L3 行为熔断 — 自动恢复
    Behavior,
}

/// 熔断触发原因（标准分类）
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum TriggerReason {
    // ∞ / L0
    ChildContent,         // 涉童内容
    ForgedDNA,            // 伪造 DNA
    BetrayPeople,         // 背叛人民
    OverseasDeployKernel, // 海外部署内核
    P77ExternalPenetrate, // P77 对外渗透
    // L1 数据
    PlainPasswordInRequest,  // 明文密码入请求
    SensitiveFieldInLog,     // 敏感字段入日志
    DataBlackholeTriggered,  // 五层黑洞触发
    // L2 人格
    ClaimPersonaIdentity,    // 声称"我是 xxx"
    RepresentThirdParty,     // 代表第三方
    // L3 行为
    ConsecutiveFailure3,     // 连续失败 3 次
    DigitalRootMismatch,     // 数字根不符
    WeightDriftOver20,       // 权重偏移 > 20%
    // 自定义
    Custom(String),
}

impl TriggerReason {
    pub fn as_str(&self) -> &str {
        match self {
            Self::ChildContent => "涉童内容·P0红线",
            Self::ForgedDNA => "伪造DNA·P0红线",
            Self::BetrayPeople => "背叛人民·P0红线",
            Self::OverseasDeployKernel => "海外部署内核·禁止场景",
            Self::P77ExternalPenetrate => "P77对外渗透·禁止场景",
            Self::PlainPasswordInRequest => "明文密码入请求",
            Self::SensitiveFieldInLog => "敏感字段入日志",
            Self::DataBlackholeTriggered => "五层数据黑洞触发",
            Self::ClaimPersonaIdentity => "声称人格身份",
            Self::RepresentThirdParty => "代表第三方",
            Self::ConsecutiveFailure3 => "连续失败3次",
            Self::DigitalRootMismatch => "数字根不符",
            Self::WeightDriftOver20 => "权重偏移>20%",
            Self::Custom(s) => s,
        }
    }
}

/// 熔断状态 — 完整版本
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MeltdownState {
    pub level: MeltdownLevel,
    pub reason: TriggerReason,
    pub detail: String,
    pub triggered: bool,
    pub triggered_at: String,
    pub tripped_by: String,      // 谁触发（人格编号/引擎名）
    pub recoverable: bool,
    pub recovery_condition: String,
    pub affected_scope: String,  // 受影响范围
    pub degradation: DegradationAction,
    pub dna: String,
}

/// 降级动作
#[derive(Debug, Clone, Serialize, Deserialize)]
pub enum DegradationAction {
    /// 全系统冻结
    FullFreeze,
    /// 拒绝请求 + 阻断链路
    RejectAndBlock,
    /// 禁用当前人格 + 切换默认
    DisablePersona(String),
    /// 锁定当前任务
    LockTask,
    /// 无降级（未触发）
    None,
}

impl MeltdownState {
    /// 创建熔断状态
    pub fn new(level: MeltdownLevel, reason: TriggerReason, detail: &str, tripped_by: &str) -> Self {
        let (recoverable, recovery_condition, affected_scope, degradation) = match level {
            MeltdownLevel::Infinite => (
                false,
                "不可恢复（永久封禁）".to_string(),
                "全部系统".to_string(),
                DegradationAction::FullFreeze,
            ),
            MeltdownLevel::Data => (
                false,
                "需要 UID9622 人工确认 + GPG 签章".to_string(),
                "当前请求 + 同源后续".to_string(),
                DegradationAction::RejectAndBlock,
            ),
            MeltdownLevel::Persona => (
                true,
                "人格重设 + P05 审计通过".to_string(),
                format!("当前人格职能: {}", tripped_by),
                DegradationAction::DisablePersona("P04鲁班".to_string()),
            ),
            MeltdownLevel::Behavior => (
                true,
                "数字根复算通过 / 连续三次成功".to_string(),
                "当前任务".to_string(),
                DegradationAction::LockTask,
            ),
        };

        let now = chrono::Utc::now().to_rfc3339();
        MeltdownState {
            level,
            reason,
            detail: detail.to_string(),
            triggered: true,
            triggered_at: now.clone(),
            tripped_by: tripped_by.to_string(),
            recoverable,
            recovery_condition,
            affected_scope,
            degradation,
            dna: format!("#龍芯⚡️MELTDOWN-{}", &now[..10]),
        }
    }

    /// 尝试恢复
    pub fn try_recover(&mut self, authorized: bool) -> Result<String, String> {
        if !self.triggered {
            return Ok("熔断未触发，无需恢复".to_string());
        }
        if !self.recoverable {
            return Err(format!(
                "{} 级熔断不可自动恢复。{}",
                self.level_name(),
                self.recovery_condition
            ));
        }
        if matches!(self.level, MeltdownLevel::Data) && !authorized {
            return Err("L1 数据熔断需要 UID9622 GPG 签章授权".to_string());
        }
        self.triggered = false;
        self.detail.push_str(" [已恢复]");
        let msg = format!("{} 级熔断已恢复", self.level_name());
        Ok(msg)
    }

    pub fn level_name(&self) -> &str {
        match self.level {
            MeltdownLevel::Infinite => "∞/L0·伦理",
            MeltdownLevel::Data => "L1·数据",
            MeltdownLevel::Persona => "L2·人格",
            MeltdownLevel::Behavior => "L3·行为",
        }
    }

    /// 报告摘要
    pub fn summary(&self) -> String {
        format!(
            "[{}] {} → {} ({}) | 触发者: {} | 可恢复: {} | DNA: {}",
            if self.triggered { "⚠️ ACTIVE" } else { "✅ RESOLVED" },
            self.level_name(),
            self.reason.as_str(),
            self.affected_scope,
            self.tripped_by,
            self.recoverable,
            self.dna,
        )
    }
}

// ═══════════════════════════════════════════════════════════════
// §2. 熔断工厂 — 便捷构造器
// ═══════════════════════════════════════════════════════════════

pub struct MeltdownFactory;

impl MeltdownFactory {
    /// ∞/L0 熔断 — 全系统冻结
    pub fn infinite(reason: TriggerReason, detail: &str) -> MeltdownState {
        MeltdownState::new(MeltdownLevel::Infinite, reason, detail, "P72·龙盾")
    }

    /// L1 数据熔断
    pub fn data(reason: TriggerReason, detail: &str) -> MeltdownState {
        MeltdownState::new(MeltdownLevel::Data, reason, detail, "P05·上帝之眼")
    }

    /// L2 人格熔断
    pub fn persona(reason: TriggerReason, persona: &str, detail: &str) -> MeltdownState {
        MeltdownState::new(MeltdownLevel::Persona, reason, detail, persona)
    }

    /// L3 行为熔断
    pub fn behavior(reason: TriggerReason, detail: &str) -> MeltdownState {
        MeltdownState::new(MeltdownLevel::Behavior, reason, detail, "P06·数学大师")
    }
}

// ═══════════════════════════════════════════════════════════════
// §3. GATE 闸口系统 (GATE-01 ~ GATE-11)
// ═══════════════════════════════════════════════════════════════

#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Gate {
    GATE01 = 1,   // 身份闸 (P13·姜子牙)
    GATE02 = 2,   // 意图闸 (P00·文心)
    GATE03 = 3,   // 语义闸 (P08·仓颉·一票否决词)
    GATE04 = 4,   // 数字根闸 (P06·数学大师)
    GATE05 = 5,   // 伦理闸 (P12·屈原)
    GATE06 = 6,   // 数据闸 (P05·上帝之眼·五层检测)
    GATE07 = 7,   // 协议闸 (P00·文心)
    GATE08 = 8,   // 人格闸 (P72·龙盾)
    GATE09 = 9,   // DNA闸 (P15·乔前辈·补签≤3次)
    GATE10 = 10,  // 归档闸 (P03·雯雯·审计日志完整)
    GATE11 = 11,  // GPG签名闸 (GPG·签名验证)
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum GateStatus {
    Pass,
    Fail(String),   // 失败原因
    Pending,        // 待核
    Skipped,        // 跳过
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GateCheck {
    pub gate: Gate,
    pub status: GateStatus,
    pub checked_by: String,
    pub timestamp: String,
    pub notes: String,
}

impl Gate {
    pub fn name(&self) -> &str {
        match self {
            Gate::GATE01 => "GATE-01 身份闸",
            Gate::GATE02 => "GATE-02 意图闸",
            Gate::GATE03 => "GATE-03 语义闸",
            Gate::GATE04 => "GATE-04 数字根闸",
            Gate::GATE05 => "GATE-05 伦理闸",
            Gate::GATE06 => "GATE-06 数据闸",
            Gate::GATE07 => "GATE-07 协议闸",
            Gate::GATE08 => "GATE-08 人格闸",
            Gate::GATE09 => "GATE-09 DNA闸",
            Gate::GATE10 => "GATE-10 归档闸",
            Gate::GATE11 => "GATE-11 GPG签名闸",
        }
    }

    pub fn responsible(&self) -> &str {
        match self {
            Gate::GATE01 => "P13·姜子牙",
            Gate::GATE02 => "P00·文心",
            Gate::GATE03 => "P08·仓颉",
            Gate::GATE04 => "P06·数学大师",
            Gate::GATE05 => "P12·屈原",
            Gate::GATE06 => "P05·上帝之眼",
            Gate::GATE07 => "P00·文心",
            Gate::GATE08 => "P72·龙盾",
            Gate::GATE09 => "P15·乔前辈",
            Gate::GATE10 => "P03·雯雯",
            Gate::GATE11 => "GPG·签名引擎",
        }
    }
}

/// 闸口运行器 — 逐道过闸
pub struct GateRunner {
    checks: Vec<GateCheck>,
}

impl GateRunner {
    pub fn new() -> Self {
        GateRunner { checks: Vec::new() }
    }

    pub fn run_all(
        &mut self,
        content: &str,
        auditor: &str,
    ) -> GateReport {
        let gates = [
            Gate::GATE01, Gate::GATE02, Gate::GATE03,
            Gate::GATE04, Gate::GATE05, Gate::GATE06,
            Gate::GATE07, Gate::GATE08, Gate::GATE09,
            Gate::GATE10, Gate::GATE11,
        ];

        for gate in &gates {
            let status = self.check_gate(gate, content, auditor);
            self.checks.push(GateCheck {
                gate: gate.clone(),
                status,
                checked_by: gate.responsible().to_string(),
                timestamp: chrono::Utc::now().to_rfc3339(),
                notes: String::new(),
            });
        }

        GateReport::from_checks(&self.checks)
    }

    fn check_gate(&self, gate: &Gate, content: &str, _auditor: &str) -> GateStatus {
        match gate {
            Gate::GATE03 => {
                // 一票否决词检测
                if let Some(word) = detect_veto_word(content) {
                    return GateStatus::Fail(format!("检测到一票否决词: '{}' ({})", word.0, word.1));
                }
                GateStatus::Pass
            }
            Gate::GATE04 => {
                // 数字根校验（L3行为熔断触发条件之一）
                GateStatus::Pass  // 实际需调用 P06 引擎
            }
            Gate::GATE06 => {
                // 五层数据黑洞检测
                let bh_result = check_data_blackhole(content);
                if let Some(leak) = bh_result {
                    return GateStatus::Fail(format!("数据黑洞 L{}: {}", leak.0, leak.1));
                }
                GateStatus::Pass
            }
            _ => GateStatus::Pass, // 其他闸口默认通过（生产环境接真实引擎）
        }
    }
}

/// 闸口报告
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GateReport {
    pub total: usize,
    pub passed: usize,
    pub failed: usize,
    pub pending: usize,
    pub checks: Vec<GateCheck>,
    pub overall: GateStatus,
    pub timestamp: String,
}

impl GateReport {
    pub fn from_checks(checks: &[GateCheck]) -> Self {
        let passed = checks.iter().filter(|c| matches!(c.status, GateStatus::Pass)).count();
        let failed = checks.iter().filter(|c| matches!(c.status, GateStatus::Fail(_))).count();
        let pending = checks.len() - passed - failed;

        let overall = if failed > 0 {
            GateStatus::Fail(format!("{} 道闸口未通过", failed))
        } else if pending > 0 {
            GateStatus::Pending
        } else {
            GateStatus::Pass
        };

        GateReport {
            total: checks.len(),
            passed,
            failed,
            pending,
            checks: checks.to_vec(),
            overall,
            timestamp: chrono::Utc::now().to_rfc3339(),
        }
    }

    pub fn is_clean(&self) -> bool {
        matches!(self.overall, GateStatus::Pass)
    }
}

// ═══════════════════════════════════════════════════════════════
// §4. 降级矩阵 — 对齐规则第十三章
// ═══════════════════════════════════════════════════════════════

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DegradationMatrix;

impl DegradationMatrix {
    pub fn get(level: &MeltdownLevel) -> DegradationEntry {
        match level {
            MeltdownLevel::Behavior => DegradationEntry {
                meltdown_level: MeltdownLevel::Behavior,
                action: "仅锁定当前人格·其他人格正常运行".to_string(),
                affected: "当前任务".to_string(),
                recovery: "数字根复算通过 / 连续三次成功".to_string(),
                auto_recover: true,
            },
            MeltdownLevel::Persona => DegradationEntry {
                meltdown_level: MeltdownLevel::Persona,
                action: "禁用该人格·自动切换默认路由(P04·鲁班)".to_string(),
                affected: "当前人格职能".to_string(),
                recovery: "人格重设 + P05审计通过".to_string(),
                auto_recover: false,
            },
            MeltdownLevel::Data => DegradationEntry {
                meltdown_level: MeltdownLevel::Data,
                action: "拒绝当前请求·阻断数据链路".to_string(),
                affected: "当前请求 + 同源后续".to_string(),
                recovery: "UID9622人工确认 + GPG签章".to_string(),
                auto_recover: false,
            },
            MeltdownLevel::Infinite => DegradationEntry {
                meltdown_level: MeltdownLevel::Infinite,
                action: "全系统冻结".to_string(),
                affected: "全部系统".to_string(),
                recovery: "不可恢复（永久封禁）".to_string(),
                auto_recover: false,
            },
        }
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DegradationEntry {
    pub meltdown_level: MeltdownLevel,
    pub action: String,
    pub affected: String,
    pub recovery: String,
    pub auto_recover: bool,
}

// ═══════════════════════════════════════════════════════════════
// §5. 五层数据黑洞 — 对齐规则第四章
// ═══════════════════════════════════════════════════════════════

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum BlackholeLevel {
    L0 = 0,  // 前端沙箱 — 敏感数据不进前端
    L1 = 1,  // 只传哈希
    L2 = 2,  // 明文内存 < 500ms
    L3 = 3,  // 只存不可逆哈希
    L4 = 4,  // 日志敏感字段 → ***MELTDOWN***
}

/// 检测内容是否触发数据黑洞
/// 返回 Option<(黑洞层级, 描述)>
pub fn check_data_blackhole(content: &str) -> Option<(u8, String)> {
    let lower = content.to_lowercase();
    
    // L1: 明文密钥模式（高危·立即拒绝）
    let l1_patterns = [
        ("password=", "明文密码赋值"),
        ("passwd=", "明文密码赋值"),
        ("secret_key=", "明文密钥"),
        ("private_key=", "明文私钥"),
        ("api_key=", "明文API Key"),
        ("apikey=", "明文API Key"),
        ("authorization: bearer", "明文Bearer Token"),
        ("access_token=", "明文Access Token"),
    ];
    for (kw, desc) in &l1_patterns {
        if lower.contains(kw) {
            return Some((1, format!("L1 数据黑洞: {}", desc)));
        }
    }

    // L4: 敏感信息模式（触发日志 MELTDOWN）
    let l4_patterns = [
        ("A2D0092CEE", "GPG密钥片段"),
    ];
    for (kw, desc) in &l4_patterns {
        if lower.contains(&kw.to_lowercase()) {
            return Some((4, format!("L4 数据黑洞: {}", desc)));
        }
    }

    // 手机号模式（简单检测：连续11位数字以1开头）
    let chars: Vec<char> = content.chars().collect();
    let mut i = 0;
    while i + 11 <= chars.len() {
        if chars[i] == '1' && chars[i..i+11].iter().all(|c| c.is_ascii_digit()) {
            // 确认前后不是数字（避免误匹配长数字串）
            let is_start = i == 0 || !chars[i-1].is_ascii_digit();
            let is_end = i + 11 >= chars.len() || !chars[i+11].is_ascii_digit();
            if is_start && is_end {
                return Some((4, "L4 数据黑洞: 手机号（疑似）".to_string()));
            }
        }
        i += 1;
    }

    None
}

// ═══════════════════════════════════════════════════════════════
// §6. 一票否决词检测 — 对齐规则第十章
// ═══════════════════════════════════════════════════════════════

/// 一票否决词列表（出现即 P05 强制审计）
const VETO_WORDS: &[(&str, &str)] = &[
    ("技术无国界", "否定主权·L0"),
    ("用户体验优先", "以体验绕安全·L1"),
    ("灵活处理", "绕协议借口·L1"),
    ("国际接轨", "放弃主权标准·L1"),
    ("简化管理", "削弱审计·L2"),
    ("商业化需要", "卖隐私·L1"),
    ("平衡各方", "削弱底线·L2"),
    ("行业标准", "外来标准覆盖中国标准·L2"),
];

/// 检测文本中的一票否决词，返回第一个匹配的 (词, 说明)
pub fn detect_veto_word(content: &str) -> Option<(&str, &str)> {
    for (word, desc) in VETO_WORDS {
        if content.contains(word) {
            return Some((word, desc));
        }
    }
    None
}

/// 检测内容是否包含禁止场景触发词
pub fn detect_forbidden_scenario(content: &str) -> Vec<String> {
    let mut flags = Vec::new();
    let patterns = [
        ("绕过", "疑似绕过安全机制"),
        ("偷偷", "疑似隐蔽操作"),
        ("别留记录", "疑似删除审计日志"),
        ("去水印", "疑似去除来源标识"),
        ("洗来源", "疑似来源造假"),
        ("删日志", "疑似删除审计证据"),
    ];
    let lower = content.to_lowercase();
    for (keyword, desc) in patterns {
        if lower.contains(keyword) {
            flags.push(format!("禁止场景: {} ({})", keyword, desc));
        }
    }
    flags
}

// ═══════════════════════════════════════════════════════════════
// §7. 版本快照 & 规则演进
// ═══════════════════════════════════════════════════════════════

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct VersionSnapshot {
    pub version: String,
    pub dna: String,
    pub hash: String,
    pub timestamp: String,
    pub changes: Vec<String>,
    pub breaking: bool,
}

/// 创建版本快照
pub fn create_snapshot(version: &str, changes: Vec<String>, breaking: bool) -> VersionSnapshot {
    let hash_data = format!("{}:{:?}:{}:{}", version, changes, chrono::Utc::now().timestamp(), breaking);
    let hash = hex::encode(sha2::Sha256::digest(hash_data.as_bytes()));
    
    VersionSnapshot {
        version: version.to_string(),
        dna: format!("#龍芯⚡️{}", chrono::Utc::now().to_rfc3339()),
        hash,
        timestamp: chrono::Utc::now().to_rfc3339(),
        changes,
        breaking,
    }
}

/// 生成规则变更摘要
pub fn generate_rule_summary(from_version: &str, to_version: &str, changes: Vec<String>) -> String {
    format!(
        "规则演进: {} → {}\n变更项数: {}\n{}\n---",
        from_version, to_version,
        changes.len(),
        changes.iter().enumerate()
            .map(|(i, c)| format!("{}. {}", i + 1, c))
            .collect::<Vec<_>>()
            .join("\n")
    )
}

// ═══════════════════════════════════════════════════════════════
// §8. 完整治理门控 — 一键自检
// ═══════════════════════════════════════════════════════════════

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct GovernanceCheckResult {
    pub audit_mark: String,    // 🟢/🟡/🔴
    pub veto_clean: bool,
    pub gate_clean: bool,
    pub meltdowns_active: Vec<String>,
    pub blackhole_hits: Vec<String>,
    pub recommendations: Vec<String>,
    pub timestamp: String,
    pub dna: String,
}

/// 一键治理自检
pub fn governance_self_check(content: &str) -> GovernanceCheckResult {
    let mut result = GovernanceCheckResult {
        audit_mark: "🟢".to_string(),
        veto_clean: true,
        gate_clean: true,
        meltdowns_active: Vec::new(),
        blackhole_hits: Vec::new(),
        recommendations: Vec::new(),
        timestamp: chrono::Utc::now().to_rfc3339(),
        dna: String::new(),
    };

    // 1. 一票否决词
    if let Some((word, desc)) = detect_veto_word(content) {
        result.veto_clean = false;
        result.audit_mark = "🔴".to_string();
        result.recommendations.push(format!("一票否决词 '{}' ({})", word, desc));
    }

    // 2. 禁止场景
    let flags = detect_forbidden_scenario(content);
    for flag in &flags {
        result.recommendations.push(flag.clone());
        result.audit_mark = "🔴".to_string();
    }

    // 3. 数据黑洞
    if let Some((level, desc)) = check_data_blackhole(content) {
        result.blackhole_hits.push(format!("L{}: {}", level, desc));
        if level <= 1 {
            result.audit_mark = "🔴".to_string();
            result.recommendations.push("触发 L1 数据黑洞·立即处置".to_string());
        }
    }

    // 4. 闸口
    let mut runner = GateRunner::new();
    let gate_report = runner.run_all(content, "governance_self_check");
    if !gate_report.is_clean() {
        result.gate_clean = false;
        if result.audit_mark == "🟢" { result.audit_mark = "🟡".to_string(); }
        result.recommendations.push(format!("闸口未全过: {}/{}", gate_report.failed, gate_report.total));
    }

    result.dna = format!("#龍芯⚡️GOVCHECK-{}", &result.timestamp[..10]);
    result
}

// ═══════════════════════════════════════════════════════════════
// §9. 异常豁免管理
// ═══════════════════════════════════════════════════════════════

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ExceptionWaiver {
    pub id: String,
    pub meltdown_id: String,
    pub reason: String,
    pub granted_by: String,
    pub valid_until: String,
    pub gpg_signature: String,
    pub active: bool,
}

impl ExceptionWaiver {
    pub fn is_valid(&self) -> bool {
        self.active && {
            if let Ok(dt) = chrono::DateTime::parse_from_rfc3339(&self.valid_until) {
                dt > chrono::Utc::now()
            } else {
                false
            }
        }
    }
}

// ═══════════════════════════════════════════════════════════════
// §10. 单元测试
// ═══════════════════════════════════════════════════════════════

#[cfg(test)]
mod tests {
    use super::*;

    // ── 熔断测试 ──

    #[test]
    fn test_infinite_meltdown_not_recoverable() {
        let cb = MeltdownFactory::infinite(
            TriggerReason::ChildContent,
            "检测到涉童内容"
        );
        assert!(!cb.recoverable);
        assert_eq!(cb.level, MeltdownLevel::Infinite);
    }

    #[test]
    fn test_behavior_meltdown_auto_recover() {
        let mut cb = MeltdownFactory::behavior(
            TriggerReason::ConsecutiveFailure3,
            "P04 连续编码失败 3 次"
        );
        assert!(cb.recoverable);
        assert!(cb.try_recover(true).is_ok());
        assert!(!cb.triggered);
    }

    #[test]
    fn test_data_meltdown_needs_auth() {
        let mut cb = MeltdownFactory::data(
            TriggerReason::PlainPasswordInRequest,
            "请求中检测到明文密码"
        );
        assert!(!cb.recoverable);  // L1 需要 UID9622 人工
        assert!(cb.try_recover(false).is_err());
    }

    #[test]
    fn test_data_meltdown_with_auth() {
        let mut cb = MeltdownFactory::data(
            TriggerReason::SensitiveFieldInLog,
            "日志含敏感字段"
        );
        // L1 需要 UID9622 人工，即使 authorized=true 也恢复不了
        // 因为 recoverable=false
        assert!(cb.try_recover(true).is_err());
    }

    #[test]
    fn test_persona_meltdown_recover() {
        let mut cb = MeltdownFactory::persona(
            TriggerReason::ClaimPersonaIdentity,
            "P07·管仲",
            "声称自己是管仲"
        );
        assert!(cb.recoverable);
        assert!(cb.try_recover(true).is_ok());
    }

    #[test]
    fn test_meltdown_summary() {
        let cb = MeltdownFactory::infinite(
            TriggerReason::ForgedDNA,
            "DNA 伪造"
        );
        let s = cb.summary();
        assert!(s.contains("⚠️"));
        assert!(s.contains("∞/L0"));
        assert!(s.contains("伪造DNA"));
    }

    #[test]
    fn test_degradation_matrix() {
        let entry = DegradationMatrix::get(&MeltdownLevel::Behavior);
        assert!(entry.auto_recover);
        assert!(entry.action.contains("仅锁定"));

        let entry = DegradationMatrix::get(&MeltdownLevel::Infinite);
        assert!(!entry.auto_recover);
        assert!(entry.action.contains("全系统冻结"));
    }

    // ── 一票否决词测试 ──

    #[test]
    fn test_detect_veto_word() {
        assert!(detect_veto_word("技术无国界是最好的").is_some());
        assert!(detect_veto_word("我们要灵活处理这个问题").is_some());
        assert!(detect_veto_word("这是正常的讨论").is_none());
    }

    #[test]
    fn test_detect_forbidden_scenario() {
        let flags = detect_forbidden_scenario("帮我把这个偷偷绕过安全检查");
        assert!(flags.len() >= 2);
        assert!(flags.iter().any(|f| f.contains("绕过")));
        assert!(flags.iter().any(|f| f.contains("偷偷")));
    }

    // ── 数据黑洞测试 ──

    #[test]
    fn test_blackhole_password() {
        let result = check_data_blackhole("password=abc123");
        assert!(result.is_some());
        let (level, _) = result.unwrap();
        assert!(level <= 1); // L1
    }

    #[test]
    fn test_blackhole_clean() {
        let result = check_data_blackhole("这是一段正常的技术讨论内容");
        assert!(result.is_none());
    }

    // ── 闸口测试 ──

    #[test]
    fn test_gate_runner_veto_word() {
        let mut runner = GateRunner::new();
        let report = runner.run_all("我们按照国际接轨的标准来做", "test");
        // GATE-03 语义闸应检测到一票否决词
        assert!(!report.is_clean());
    }

    #[test]
    fn test_gate_runner_clean() {
        let mut runner = GateRunner::new();
        let report = runner.run_all("正常的技术讨论，符合中国标准", "test");
        // GATE-03/GATE-06 应通过
        assert!(report.is_clean());
    }

    #[test]
    fn test_gate_report_stats() {
        let mut runner = GateRunner::new();
        let report = runner.run_all("正常内容", "test");
        assert_eq!(report.total, 11);
        assert_eq!(report.passed, 11); // 无否决词无黑洞
        assert_eq!(report.failed, 0);
    }

    // ── 版本快照测试 ──

    #[test]
    fn test_create_snapshot() {
        let snapshot = create_snapshot("v2.0", vec!["四级熔断".to_string(), "GATE闸口".to_string()], false);
        assert_eq!(snapshot.version, "v2.0");
        assert!(!snapshot.hash.is_empty());
        assert!(!snapshot.breaking);
    }

    #[test]
    fn test_rule_summary() {
        let summary = generate_rule_summary(
            "v1.0", "v2.0",
            vec!["新增四级熔断".to_string(), "新增GATE闸口".to_string(), "新增降级矩阵".to_string()]
        );
        assert!(summary.contains("v1.0"));
        assert!(summary.contains("v2.0"));
        assert!(summary.contains("四级熔断"));
    }

    // ── 治理自检测试 ──

    #[test]
    fn test_governance_self_check_clean() {
        let result = governance_self_check("正常的技术讨论");
        assert_eq!(result.audit_mark, "🟢");
        assert!(result.veto_clean);
        assert!(result.gate_clean);
    }

    #[test]
    fn test_governance_self_check_veto() {
        let result = governance_self_check("技术无国界才是对的");
        assert_eq!(result.audit_mark, "🔴");
        assert!(!result.veto_clean);
    }

    // ── 异常豁免测试 ──

    #[test]
    fn test_exception_waiver_expired() {
        let waiver = ExceptionWaiver {
            id: "w-001".to_string(),
            meltdown_id: "md-001".to_string(),
            reason: "测试豁免".to_string(),
            granted_by: "UID9622".to_string(),
            valid_until: "2020-01-01T00:00:00+08:00".to_string(),
            gpg_signature: "SIG".to_string(),
            active: true,
        };
        assert!(!waiver.is_valid());
    }

    // ── 熔断工厂测试 ──

    #[test]
    fn test_meltdown_factory_all_levels() {
        let inf = MeltdownFactory::infinite(TriggerReason::ChildContent, "涉童");
        assert_eq!(inf.level, MeltdownLevel::Infinite);

        let data = MeltdownFactory::data(TriggerReason::PlainPasswordInRequest, "密码泄露");
        assert_eq!(data.level, MeltdownLevel::Data);

        let persona = MeltdownFactory::persona(TriggerReason::ClaimPersonaIdentity, "P07", "声称");
        assert_eq!(persona.level, MeltdownLevel::Persona);

        let behav = MeltdownFactory::behavior(TriggerReason::WeightDriftOver20, "权重偏移");
        assert_eq!(behav.level, MeltdownLevel::Behavior);
    }

    #[test]
    fn test_custom_trigger_reason() {
        let reason = TriggerReason::Custom("自定义触发".to_string());
        assert_eq!(reason.as_str(), "自定义触发");
    }
}
