// 龍魂代码中转站 · 安全审查引擎
// 反殖民检测 + 数据外泄检测 + 中国法合规
// DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-SECURITY-v1.0

use serde::{Deserialize, Serialize};
use std::path::Path;
use walkdir::WalkDir;

/// 违规严重级别
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Severity {
    Block,
    Warn,
    Info,
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

/// 安全审查报告
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SecurityReport {
    pub passed: bool,
    pub violations: Vec<Violation>,
    pub data_exfil_check: bool,
    pub colonial_pattern_check: bool,
    pub license_compliance: bool,
    pub anti_colonial_score: f64,
    pub summary: String,
}

impl SecurityReport {
    fn new() -> Self {
        Self {
            passed: true,
            violations: Vec::new(),
            data_exfil_check: true,
            colonial_pattern_check: true,
            license_compliance: true,
            anti_colonial_score: 1.0,
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
                "数据外泄风险",
                &format!("发现境外 API 端点: {}", pattern),
            );
        }
    }

    // 2. 硬编码密钥检测
    let key_patterns = [
        ("api_key", "API 密钥硬编码"),
        ("api_secret", "API 密钥硬编码"),
        ("password", "密码硬编码"),
        ("secret_key", "密钥硬编码"),
        ("private_key", "私钥硬编码"),
        ("token", "Token 硬编码"),
        ("access_key", "Access Key 硬编码"),
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
                "平台锁定风险",
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
            "数据批量操作",
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
            "中国法合规",
            "检测到日志删除功能 — 日志不应可删除，违反中国网络安全法",
        );
    }

    Ok(())
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

    // 反殖民评分
    let total_weight = report.violations.len() as f64;
    let block_count = report.violations.iter()
        .filter(|v| v.severity.contains("🔴")).count() as f64;
    let warn_count = report.violations.iter()
        .filter(|v| v.severity.contains("🟡")).count() as f64;

    if total_weight > 0.0 {
        report.anti_colonial_score = 1.0 - (block_count * 0.2 + warn_count * 0.05);
        report.anti_colonial_score = report.anti_colonial_score.max(0.0);
    }

    // 生成摘要
    if report.passed && report.violations.is_empty() {
        report.summary = "🟢 安全审查通过 · 无违规项 · 反殖民评分 1.0/1.0".to_string();
    } else if report.passed {
        report.summary = format!(
            "🟡 安全审查通过（{} 个注意项）· 反殖民评分 {:.2}/1.0",
            report.violations.len(),
            report.anti_colonial_score,
        );
    } else {
        let blocks: Vec<_> = report.violations.iter()
            .filter(|v| v.severity.contains("🔴")).collect();
        report.summary = format!(
            "🔴 安全审查未通过 · {} 个阻断项 · {} 个注意项 · 反殖民评分 {:.2}/1.0",
            blocks.len(),
            report.violations.len() - blocks.len(),
            report.anti_colonial_score,
        );
    }

    Ok(report)
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
