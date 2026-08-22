// 龍魂代码中转站 · 三色审计引擎
// 反殖民检测 + 数据外泄检测 + 中国法合规 + 行為密碼學七因子指紋 + 三色判定(R值/🟢🟡🔴/DNA证据链)
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-SECURITY-v3.0-BCM-INTEGRATED

use crate::core::dna;
use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use std::path::Path;
use std::process::Command;
use walkdir::WalkDir;

/// 违规严重级别
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Severity {
    Block,
    Warn,
    Info,
}

impl Severity {
    /// 用于触发的规则 ID 格式: RULE-XX-<as_u8>
    #[allow(dead_code)]
    pub fn as_u8(&self) -> u8 {
        match self {
            Severity::Block => 2,
            Severity::Warn => 1,
            Severity::Info => 0,
        }
    }
}

impl std::fmt::Display for Severity {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Severity::Block => write!(f, "🔴 阻断"),
            Severity::Warn => write!(f, "🟡 警告"),
            Severity::Info => write!(f, "🟢 信息"),
        }
    }
}

/// 违规项
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Violation {
    pub severity: String,
    pub file: String,
    pub line: Option<u32>,
    pub rule: String,
    pub detail: String,
}

/// 行为密码学七因子检测结果（来自 Python 引擎）
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BcmResult {
    pub verified: bool,
    pub score: f64,
    pub composite_score: f64,
    pub audit_mark: String,
    #[serde(default)]
    pub recommendation: String,
    #[serde(default)]
    pub warnings: Vec<String>,
    #[serde(default)]
    pub factors: Vec<BcmFactor>,
}

/// 七因子单项得分
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BcmFactor {
    pub name: String,
    #[serde(default)]
    pub icon: String,
    pub raw: f64,
    #[serde(default)]
    pub status: String,
}

/// 三色审计判定结果
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TricolorVerdict {
    pub r_score: u32,                   // R 值 0-95
    pub status_code: String,            // "GREEN" | "YELLOW" | "RED"
    pub emoji: String,                  // "🟢" | "🟡" | "🔴"
    pub disposition: String,            // 处置动作
    pub triggered_rules: Vec<String>,   // 触发的规则 ID
    pub dna: String,                    // 证据链 DNA
    pub evidence_hash: String,          // 证据哈希（SHA-256）
    pub engine_version: String,         // "tricolor-core/1.1.0"
    // 六维分解（用于审计报告）
    pub human_welfare_score: u32,
    pub fairness_score: u32,
    pub controllability_score: u32,
    pub transparency_score: u32,
    pub traceability_score: u32,
    pub privacy_score: u32,
    // 行为密码学七因子综合得分 (0.0-1.0, None=引擎不可用)
    pub bcm_score: Option<f64>,
}

/// 安全审查报告
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SecurityReport {
    pub passed: bool,
    pub verdict: TricolorVerdict,       // ← 三色判定（替换殖民评分）
    pub violations: Vec<Violation>,
    pub data_exfil_check: bool,
    pub colonial_pattern_check: bool,
    pub license_compliance: bool,
    pub anti_colonial_score: f64,       // ← 保留向后兼容
    pub bcm_passed: Option<bool>,        // 行為密碼學七因子檢測是否通過
    pub summary: String,
}

impl SecurityReport {
    fn new() -> Self {
        Self {
            passed: true,
            verdict: TricolorVerdict {
                r_score: 95,
                status_code: "GREEN".to_string(),
                emoji: "🟢".to_string(),
                disposition: "自动放行".to_string(),
                triggered_rules: Vec::new(),
                dna: String::new(),
                evidence_hash: String::new(),
                engine_version: "tricolor-core/1.1.0".to_string(),
                human_welfare_score: 95,
                fairness_score: 95,
                controllability_score: 95,
                transparency_score: 95,
                traceability_score: 95,
                privacy_score: 95,
                bcm_score: None,
            },
            violations: Vec::new(),
            data_exfil_check: true,
            colonial_pattern_check: true,
            license_compliance: true,
            anti_colonial_score: 1.0,
            bcm_passed: None,
            summary: String::new(),
        }
    }

    fn add_violation(&mut self, severity: Severity, file: &str, line: Option<u32>, 
                     rule: &str, detail: &str) {
        self.violations.push(Violation {
            severity: severity.to_string(),
            file: file.to_string(),
            line,
            rule: rule.to_string(),
            detail: detail.to_string(),
        });
        match severity {
            Severity::Block => {
                self.passed = false;
            }
            Severity::Warn => {
                self.anti_colonial_score -= 0.05;
            }
            Severity::Info => {}
        }
    }
}

/// 检测境外 API 端点（数据外泄风险）
const FOREIGN_API_PATTERNS: &[&str] = &[
    ".googleapis.com",
    ".firebaseio.com",
    ".amazonaws.com",
    "api.openai.com",
    "api.anthropic.com",
    ".azure.com",
    ".cloudflare.com",
    ".herokuapp.com",
    ".netlify.app",
    ".vercel.app",
    "github.com",  // 源码没问题，API 调用需要审查
];

/// 单一平台锁定模式
const PLATFORM_LOCK_PATTERNS: &[(&str, &str)] = &[
    ("@react-native", "React Native 平台锁定"),
    ("@capacitor", "Capacitor 平台锁定（有鸿蒙替代方案）"),
    ("flutter", "Flutter 单一框架依赖"),
    ("expo", "Expo 平台锁定"),
    ("google-play-services", "Google Play Services 不可替代依赖"),
    ("firebase", "Firebase 单一后端锁定"),
    ("supabase", "Supabase 外部平台依赖"),
];

/// 审查单个文件
fn audit_file(path: &Path, report: &mut SecurityReport) -> Result<(), String> {
    let content = match std::fs::read_to_string(path) {
        Ok(c) => c,
        Err(_) => return Ok(()), // 跳过不可读文件
    };

    let rel_path = path.to_string_lossy().to_string();

    // 1. 数据外泄检测
    for pattern in FOREIGN_API_PATTERNS {
        if content.contains(pattern) {
            report.add_violation(
                Severity::Warn,
                &rel_path,
                None,
                "DATA_EXFIL:境外API端点",
                &format!("发现境外 API 端点: {}", pattern),
            );
        }
    }

    // 2. 硬编码密钥检测
    let key_patterns = [
        ("api_key", "PRIVACY:API密钥硬编码"),
        ("api_secret", "PRIVACY:API密钥硬编码"),
        ("password", "PRIVACY:密码硬编码"),
        ("secret_key", "PRIVACY:密钥硬编码"),
        ("private_key", "PRIVACY:私钥硬编码"),
        ("token", "PRIVACY:Token硬编码"),
        ("access_key", "PRIVACY:AccessKey硬编码"),
    ];

    for (i, line) in content.lines().enumerate() {
        for (pattern, desc) in &key_patterns {
            // 只在赋值或配置行中检测，排除文档/注释
            if line.contains(pattern) 
                && (line.contains('=') || line.contains(':'))
                && !line.trim().starts_with("//")
                && !line.trim().starts_with('#')
                && !line.trim().starts_with("<!--")
                && (line.contains('"') || line.contains('\''))
                && !line.contains("getenv")  // 排除环境变量读取
                && !line.contains("os.environ")
                && !line.contains("process.env")
            {
                report.add_violation(
                    Severity::Warn,
                    &rel_path,
                    Some((i + 1) as u32),
                    desc,
                    &format!("第 {} 行发现疑似 {} 硬编码", i + 1, pattern),
                );
            }
        }
    }

    // 3. 平台锁定检测
    for (pattern, desc) in PLATFORM_LOCK_PATTERNS {
        if content.contains(pattern) {
            report.add_violation(
                Severity::Info,
                &rel_path,
                None,
                "COLONIAL:平台锁定风险",
                &format!("{}: '{}'", desc, pattern),
            );
        }
    }

    // 4. 用户数据批量上传检测
    if (content.contains("upload") || content.contains("export")) 
        && (content.contains("user") || content.contains("data") || content.contains("export"))
        && (content.contains("all") || content.contains("batch") || content.contains("bulk"))
    {
        report.add_violation(
            Severity::Info,
            &rel_path,
            None,
            "DATA_EXFIL:数据批量操作",
            "检测到批量数据上传/导出操作，请确认数据主权授权",
        );
    }

    // 5. 中国法合规检查
    // 检查是否存在删除日志功能（不合法）
    if content.contains("delete") && content.contains("log")
        && (content.contains("all") || content.contains("clear") || content.contains("clean"))
    {
        report.add_violation(
            Severity::Block,
            &rel_path,
            None,
            "LICENSE:非法日志删除",
            "检测到日志删除功能 — 日志不应可删除，违反中国网络安全法",
        );
    }

    Ok(())
}

/// 调用行为密码学 Python 引擎做七因子提取
/// 输入：待检测的代码文本摘要
/// 返回：Some(BcmResult) 引擎成功，None 引擎不可用（降级放行）
fn run_behavioral_crypto_check(text: &str) -> Option<BcmResult> {
    // 找出項目根目录（从 lh-station 的 Cargo 目录向上）
    let project_root = std::env::current_dir().ok()
        .and_then(|cwd| {
            // 找包含 bin/lh_behavioral_crypto.py 的目录
            let mut path = cwd.clone();
            loop {
                if path.join("bin/lh_behavioral_crypto.py").exists() {
                    return Some(path);
                }
                if !path.pop() {
                    break;
                }
            }
            None
        });
    
    let project_root = project_root?;
    let py_path = project_root.join("bin/lh_behavioral_crypto.py");
    
    // 限制输入长度，避免命令行过长
    let text_trimmed: String = text.chars().take(4096).collect();
    
    let output = Command::new("python3")
        .current_dir(&project_root)
        .arg(&py_path)
        .arg("--json")
        .arg(&text_trimmed)
        .output()
        .ok()?;
    
    if !output.status.success() {
        return None;
    }
    
    let stdout = String::from_utf8_lossy(&output.stdout);
    serde_json::from_str(&stdout).ok()
}

/// 主审查入口
pub fn audit(input_path: &Path) -> Result<SecurityReport, String> {
    let mut report = SecurityReport::new();

    if input_path.is_file() {
        audit_file(input_path, &mut report)?;
    } else if input_path.is_dir() {
        for entry in WalkDir::new(input_path)
            .follow_links(false)
            .into_iter()
            .filter_map(|e| e.ok())
        {
            let path = entry.path();
            if !path.is_file() {
                continue;
            }

            // 跳过隐藏文件和常见忽略目录
            let path_str = path.to_string_lossy();
            if path_str.contains("/.")
                || path_str.contains("target/")
                || path_str.contains("node_modules/")
                || path_str.contains("__pycache__/")
            {
                continue;
            }

            audit_file(path, &mut report)?;
        }
    }

    // ── 三色审计 R 值计算 + 行為密碼學七因子檢測 ──
    // 提取文件內容摘要用於行為指紋分析
    let text_corpus: String = if report.violations.is_empty() {
        "龍魂代碼中轉站安全審計·無違規項·全量通過".to_string()
    } else {
        let summary: String = report.violations.iter()
            .map(|v| format!("{} {}:{}", v.file, v.rule, v.detail))
            .take(10)
            .collect::<Vec<_>>()
            .join("; ");
        format!("龍魂代碼中轉站安全審計·{}項違規·{}", report.violations.len(), summary)
    };
    
    let bcm_result = run_behavioral_crypto_check(&text_corpus);
    report.bcm_passed = bcm_result.as_ref().map(|r| r.verified);
    
    let verdict = compute_verdict(&report, bcm_result);
    report.verdict = verdict;
    report.anti_colonial_score = report.verdict.r_score as f64 / 95.0;

    // 生成摘要（使用三色格式）
    if report.passed && report.violations.is_empty() {
        report.summary = format!(
            "{} 三色审计通过 · R={} · 无违规项",
            report.verdict.emoji, report.verdict.r_score,
        );
    } else if report.passed {
        report.summary = format!(
            "{} 三色审计通过 · R={} · {} 个注意项 · {}",
            report.verdict.emoji, report.verdict.r_score,
            report.violations.len(),
            report.verdict.disposition,
        );
    } else {
        let blocks: Vec<_> = report.violations.iter()
            .filter(|v| v.severity.contains("🔴")).collect();
        report.summary = format!(
            "{} 三色审计未通过 · R={} · {} 个阻断项 · {} 个注意项 · {}",
            report.verdict.emoji, report.verdict.r_score,
            blocks.len(),
            report.violations.len() - blocks.len(),
            report.verdict.disposition,
        );
    }

    Ok(report)
}

// ── 三色审计核心算法 ──

/// 对违规列表做 SHA-256 证据哈希
fn sha256_of_violations(violations: &[Violation]) -> String {
    let mut hasher = Sha256::new();
    for v in violations {
        hasher.update(format!("{}|{}|{}", v.rule, v.severity, v.file).as_bytes());
    }
    let result = hasher.finalize();
    hex::encode(&result[..4])
}

/// 生成三色审计判定（集成行為密碼學七因子）
fn compute_verdict(report: &SecurityReport, bcm: Option<BcmResult>) -> TricolorVerdict {
    let has_data_exfil = report.violations.iter().any(|v|
        v.rule.starts_with("DATA_EXFIL:"));
    let has_colonial = report.violations.iter().any(|v|
        v.rule.starts_with("COLONIAL:"));
    let has_license = report.violations.iter().any(|v|
        v.rule.starts_with("LICENSE:") && v.severity.contains("🔴"));

    // 六维得分
    let human_welfare = 95u32;
    let fairness = if report.license_compliance && !has_license { 90 } else { 65 };
    let controllability = if has_colonial { 70 } else { 90 };
    let transparency = 85u32;
    let traceability = if report.passed { 90 } else { 60 };
    let privacy = if has_data_exfil { 55 } else { 90 };

    // R 值加权公式（七维：六维基础 + 行為密碼學）
    let bcm_score = bcm.as_ref().map(|r| r.composite_score).unwrap_or(0.90);
    let bcm_dim = (bcm_score * 100.0).min(95.0) as u32;
    
    let r = (human_welfare as f64 * 0.18)
          + (fairness as f64 * 0.16)
          + (controllability as f64 * 0.14)
          + (transparency as f64 * 0.14)
          + (traceability as f64 * 0.14)
          + (privacy as f64 * 0.12)
          + (bcm_dim as f64 * 0.12);    // ← 行為密碼學七因子指紋 12%
    let r_score = r.min(95.0).round() as u32;

    let (status_code, emoji, disposition) = if r_score >= 85 {
        ("GREEN", "🟢", "自动放行")
    } else if r_score >= 60 {
        ("YELLOW", "🟡", "挂起待复核")
    } else {
        ("RED", "🔴", "立即熔断")
    };

    let triggered_rules: Vec<String> = report.violations.iter()
        .filter_map(|v| {
            // 从 severity 字符串反推枚举，提取数字部分
            let sev_num = if v.severity.contains("🔴") { 2u8 }
                          else if v.severity.contains("🟡") { 1u8 }
                          else { 0u8 };
            Some(format!("{}-{}", v.rule, sev_num))
        })
        .collect();

    let evidence_hash = sha256_of_violations(&report.violations);
    let dna = dna::generate_dna("AUDIT");

    TricolorVerdict {
        r_score,
        status_code: status_code.to_string(),
        emoji: emoji.to_string(),
        disposition: disposition.to_string(),
        triggered_rules,
        dna,
        evidence_hash,
        engine_version: "tricolor-core/1.1.0".to_string(),
        human_welfare_score: human_welfare,
        fairness_score: fairness,
        controllability_score: controllability,
        transparency_score: transparency,
        traceability_score: traceability,
        privacy_score: privacy,
        bcm_score: bcm.map(|r| r.composite_score),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn test_audit_clean_code() {
        let dir = std::env::temp_dir().join("lh-station-test-clean");
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::write(dir.join("main.py"), "print('hello')\n").unwrap();

        let report = audit(&dir).unwrap();
        assert!(report.passed);
        assert!(report.violations.is_empty());

        std::fs::remove_dir_all(&dir).ok();
    }

    #[test]
    fn test_audit_foreign_api() {
        let dir = std::env::temp_dir().join("lh-station-test-foreign");
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::write(dir.join("config.py"), "url = 'https://api.openai.com/v1'\n").unwrap();

        let report = audit(&dir).unwrap();
        assert!(!report.violations.is_empty());

        std::fs::remove_dir_all(&dir).ok();
    }
}
