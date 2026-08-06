// 龍魂代码中转站 · API 调用成本分析引擎
// 扫描代码外部 API → 分类 → 估算成本 + 数据主权风险
// DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-COST-ANALYZER-v1.0

use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::path::{Path, PathBuf};
use walkdir::WalkDir;

// ═══════════════════════════════════════
// 结构体
// ═══════════════════════════════════════

/// API 服务商分类
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum ApiProvider {
    OpenAPI,
    KnownForeign(String),
    KnownDomestic(String),
    SelfHosted,
    Unknown,
}

impl std::fmt::Display for ApiProvider {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            ApiProvider::OpenAPI => write!(f, "OpenAPI (通用)"),
            ApiProvider::KnownForeign(name) => write!(f, "境外: {}", name),
            ApiProvider::KnownDomestic(name) => write!(f, "国内: {}", name),
            ApiProvider::SelfHosted => write!(f, "内网/自托管"),
            ApiProvider::Unknown => write!(f, "未知"),
        }
    }
}

/// 检测到的 API 调用
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ApiCall {
    pub endpoint: String,
    pub method: String,
    pub frequency_hint: String,
    pub auth_type: Option<String>,
    pub provider: String,
    pub file: String,
    pub line: Option<u32>,
}

/// 数据主权风险等级
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Serialize, Deserialize)]
pub enum RiskLevel {
    Low,
    Medium,
    High,
    Critical,
}

impl std::fmt::Display for RiskLevel {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            RiskLevel::Low => write!(f, "🟢 Low"),
            RiskLevel::Medium => write!(f, "🟡 Medium"),
            RiskLevel::High => write!(f, "🔴 High"),
            RiskLevel::Critical => write!(f, "⚫ Critical"),
        }
    }
}

/// 成本分析报告
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CostReport {
    pub estimated_monthly_cny: f64,
    pub estimated_daily_cny: f64,
    pub data_sovereign_risk: String,
    pub cross_border_apis: Vec<ApiCall>,
    pub domestic_apis: Vec<ApiCall>,
    pub self_hosted_count: u32,
    pub recommendations: Vec<String>,
    pub analysis_time: String,
    pub total_apis_detected: u32,
    pub api_calls: Vec<ApiCall>,
}

// ═══════════════════════════════════════
// 境外服务商域名匹配
// ═══════════════════════════════════════

const FOREIGN_SERVICES: &[(&str, &str, f64)] = &[
    // (域名片段, 服务商名称, 预估单价 CNY/次)
    ("api.openai.com", "OpenAI", 0.15),
    ("api.anthropic.com", "Anthropic", 0.20),
    (".googleapis.com", "Google APIs", 0.05),
    ("generativelanguage.googleapis.com", "Google Gemini", 0.08),
    (".firebaseio.com", "Firebase", 0.03),
    (".amazonaws.com", "AWS", 0.05),
    ("bedrock.", "AWS Bedrock", 0.12),
    (".azure.com", "Azure", 0.06),
    ("azure-api.net", "Azure API", 0.06),
    (".cloudflare.com", "Cloudflare", 0.02),
    (".herokuapp.com", "Heroku", 0.03),
    (".netlify.app", "Netlify", 0.01),
    (".vercel.app", "Vercel", 0.02),
    ("api.github.com", "GitHub API", 0.01),
    ("api.stripe.com", "Stripe", 0.05),
    ("api.twilio.com", "Twilio", 0.10),
    ("api.sendgrid.com", "SendGrid", 0.02),
    ("supabase.co", "Supabase", 0.03),
    ("api.deepseek.com", "DeepSeek", 0.01),
    ("api.mistral.ai", "Mistral", 0.08),
    ("api.together.xyz", "Together AI", 0.05),
    ("api.groq.com", "Groq", 0.03),
    ("api.cohere.ai", "Cohere", 0.08),
];

const DOMESTIC_SERVICES: &[(&str, &str, f64)] = &[
    ("aliyuncs.com", "阿里云", 0.008),
    ("tencentcloudapi.com", "腾讯云", 0.008),
    ("myqcloud.com", "腾讯云", 0.008),
    ("huaweicloud.com", "华为云", 0.008),
    ("baidubce.com", "百度云", 0.005),
    ("baidu.com/api", "百度 API", 0.005),
    ("volcengineapi.com", "火山引擎", 0.008),
    ("jdcloud.com", "京东云", 0.008),
    ("qcloud.com", "腾讯云", 0.008),
    ("apigw.ctyun.cn", "天翼云", 0.005),
    ("uid9622.cn", "鲲鹏(自托管)", 0.0),
    ("longhun888.com", "龍魂(自托管)", 0.0),
];

const SELF_HOSTED_PATTERNS: &[&str] = &[
    "localhost",
    "127.0.0.1",
    "0.0.0.0",
    "192.168.",
    "10.",
];

/// API URL 正则提取用模式（HTTP/HTTPS URL）
fn extract_urls(content: &str) -> Vec<(String, usize)> {
    let mut urls = Vec::new();
    // 匹配 https?:// 开头的 URL
    for (line_num, line) in content.lines().enumerate() {
        let mut search_start = 0usize;
        while let Some(pos) = line[search_start..].find("https://") {
            let abs_pos = search_start + pos;
            let remaining = &line[abs_pos..];
            if let Some(end) = remaining.find(|c: char| {
                c.is_whitespace() || c == '"' || c == '\'' || c == ')' || c == ']' || c == '}' || c == ',' || c == ';'
            }) {
                let url = remaining[..end].to_string();
                if url.len() > 10 {
                    urls.push((url, line_num + 1));
                }
                search_start = abs_pos + end;
            } else {
                // URL 到行尾
                let url = remaining.to_string();
                if url.len() > 10 {
                    urls.push((url, line_num + 1));
                }
                break;
            }
        }
        // 也匹配以 http:// 开头的（较少见但也要检测）
        search_start = 0;
        while let Some(pos) = line[search_start..].find("http://") {
            let abs_pos = search_start + pos;
            let remaining = &line[abs_pos..];
            if let Some(end) = remaining.find(|c: char| {
                c.is_whitespace() || c == '"' || c == '\'' || c == ')' || c == ']' || c == '}' || c == ',' || c == ';'
            }) {
                let url = remaining[..end].to_string();
                if url.len() > 10 {
                    urls.push((url, line_num + 1));
                }
                search_start = abs_pos + end;
            } else {
                let url = remaining.to_string();
                if url.len() > 10 {
                    urls.push((url, line_num + 1));
                }
                break;
            }
        }
    }
    urls
}

/// 从 URL 提取域名
fn extract_domain(url: &str) -> String {
    let without_proto = url
        .trim_start_matches("https://")
        .trim_start_matches("http://");
    let domain = without_proto
        .split('/')
        .next()
        .unwrap_or(without_proto)
        .split(':')
        .next()
        .unwrap_or(without_proto);
    domain.to_lowercase()
}

/// 猜测 HTTP 方法
fn guess_method(url: &str, line: &str) -> String {
    let lower = line.to_lowercase();
    if lower.contains(".post(") || lower.contains("http.post") || lower.contains("requests.post") {
        "POST".to_string()
    } else if lower.contains(".put(") || lower.contains("requests.put") {
        "PUT".to_string()
    } else if lower.contains(".patch(") || lower.contains("requests.patch") {
        "PATCH".to_string()
    } else if lower.contains(".delete(") || lower.contains("requests.delete") {
        "DELETE".to_string()
    } else if url.contains("/chat/completions") || url.contains("/completions") {
        "POST".to_string()
    } else {
        "GET".to_string()
    }
}

/// 检测认证方式
fn guess_auth(line: &str) -> Option<String> {
    let lower = line.to_lowercase();
    if lower.contains("bearer") { return Some("Bearer Token".to_string()); }
    if lower.contains("api_key") || lower.contains("api-key") || lower.contains("apikey") { return Some("API Key".to_string()); }
    if lower.contains("authorization") || lower.contains("auth") { return Some("Authorization Header".to_string()); }
    if lower.contains("x-api-key") { return Some("X-API-Key".to_string()); }
    None
}

/// 分类服务商
fn classify_provider(domain: &str) -> (ApiProvider, f64) {
    // 先检查内网
    for pattern in SELF_HOSTED_PATTERNS {
        if domain.contains(pattern) || domain.starts_with(pattern) {
            return (ApiProvider::SelfHosted, 0.0);
        }
    }

    // 检查国内
    for (pattern, name, price) in DOMESTIC_SERVICES {
        if domain.contains(pattern) {
            return (ApiProvider::KnownDomestic(name.to_string()), *price);
        }
    }

    // 检查境外
    for (pattern, name, price) in FOREIGN_SERVICES {
        if domain.contains(pattern) {
            return (ApiProvider::KnownForeign(name.to_string()), *price);
        }
    }

    // 未识别
    (ApiProvider::Unknown, 0.005) // 默认低单价
}

/// 主分析函数
pub fn analyze(input_path: &Path, output_dir: &Path) -> Result<CostReport, String> {
    let mut detected_calls: Vec<ApiCall> = Vec::new();
    let mut seen_endpoints: HashSet<String> = HashSet::new();

    // ═══ 1. 扫描所有代码文件 ═══
    if input_path.is_file() {
        scan_file(input_path, input_path, &mut detected_calls, &mut seen_endpoints)?;
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

            let path_str = path.to_string_lossy();
            // 跳过常见忽略目录
            if path_str.contains("/.")
                || path_str.contains("target/")
                || path_str.contains("node_modules/")
                || path_str.contains("__pycache__/")
                || path_str.contains(".git/")
                || path_str.contains("dist/")
                || path_str.contains("build/")
                || path_str.contains(".sovereign")
            {
                continue;
            }

            scan_file(path, input_path, &mut detected_calls, &mut seen_endpoints)?;
        }
    }

    // ═══ 2. 分类统计 ═══
    let mut cross_border_apis: Vec<ApiCall> = Vec::new();
    let mut domestic_apis: Vec<ApiCall> = Vec::new();
    let mut self_hosted_count = 0u32;
    let mut total_daily_cny = 0.0;

    for call in &detected_calls {
        let domain = extract_domain(&call.endpoint);
        let (provider, unit_price) = classify_provider(&domain);

        // 每天1000次基准
        let daily_cost = unit_price * 1000.0;
        total_daily_cny += daily_cost;

        match &provider {
            ApiProvider::KnownForeign(_) | ApiProvider::OpenAPI => {
                cross_border_apis.push(call.clone());
            }
            ApiProvider::KnownDomestic(_) => {
                domestic_apis.push(call.clone());
            }
            ApiProvider::SelfHosted => {
                self_hosted_count += 1;
            }
            ApiProvider::Unknown => {
                // 未知服务商 → 归入 cross_border（保守处理）
                cross_border_apis.push(call.clone());
            }
        }
    }

    // ═══ 3. 数据主权风险判定 ═══
    let cross_border_count = cross_border_apis.len();
    let data_sovereign_risk = if cross_border_count == 0 {
        RiskLevel::Low
    } else if cross_border_count <= 2 {
        RiskLevel::Medium
    } else if cross_border_count <= 5 {
        RiskLevel::High
    } else {
        RiskLevel::Critical
    };

    // ═══ 4. 生成建议 ═══
    let mut recommendations: Vec<String> = Vec::new();

    if cross_border_count > 0 {
        recommendations.push(format!(
            "⚠️ 检测到 {} 个跨境 API 端点，数据可能流出中国境内",
            cross_border_count
        ));
        recommendations.push(
            "建议优先使用国内替代服务（阿里云/腾讯云/华为云）".to_string(),
        );
    }

    if data_sovereign_risk >= RiskLevel::High {
        recommendations.push(
            "🔴 高风险：建议对跨境 API 进行数据脱敏处理，必要时端侧加密后传输".to_string(),
        );
    }

    if self_hosted_count > 0 {
        recommendations.push(format!(
            "✅ {} 个自托管/内网服务 — 数据主权安全",
            self_hosted_count
        ));
    }

    if detected_calls.is_empty() {
        recommendations.push("✅ 未检测到外部 API 调用 — 数据主权无风险".to_string());
    }

    // ═══ 5. 估算月度成本 ═══
    let estimated_monthly_cny = total_daily_cny * 30.0;

    let report = CostReport {
        estimated_monthly_cny: (estimated_monthly_cny * 100.0).round() / 100.0,
        estimated_daily_cny: (total_daily_cny * 100.0).round() / 100.0,
        data_sovereign_risk: data_sovereign_risk.to_string(),
        cross_border_apis,
        domestic_apis,
        self_hosted_count,
        recommendations,
        analysis_time: chrono::Local::now().format("%Y-%m-%dT%H:%M:%S%z").to_string(),
        total_apis_detected: detected_calls.len() as u32,
        api_calls: detected_calls,
    };

    // ═══ 6. 写入 .cost-report.json ═══
    std::fs::create_dir_all(output_dir)
        .map_err(|e| format!("创建输出目录失败: {}", e))?;

    let cost_path = output_dir.join(".cost-report.json");
    std::fs::write(&cost_path, serde_json::to_string_pretty(&report)
        .map_err(|e| format!("序列化成本报告失败: {}", e))?)
        .map_err(|e| format!("写入成本报告失败: {}", e))?;
    println!("  成本: {} → {}", report.data_sovereign_risk, cost_path.display());

    Ok(report)
}

/// 扫描单个文件
fn scan_file(
    file_path: &Path,
    base_path: &Path,
    calls: &mut Vec<ApiCall>,
    seen: &mut HashSet<String>,
) -> Result<(), String> {
    // 只扫描代码文件
    let ext = file_path
        .extension()
        .map(|e| e.to_string_lossy().to_lowercase())
        .unwrap_or_default();

    let code_exts = [
        "py", "js", "mjs", "cjs", "ts", "tsx", "jsx",
        "rs", "c", "cpp", "cc", "h", "hpp",
        "go", "java", "kt", "kts", "swift", "ets",
        "sh", "bash", "zsh",
        "yaml", "yml", "toml", "json",
        "html", "htm", "vue", "svelte",
        "rb", "php", "pl", "lua",
    ];

    if !code_exts.iter().any(|e| e == &ext.as_str()) {
        return Ok(());
    }

    let content = match std::fs::read_to_string(file_path) {
        Ok(c) => c,
        Err(_) => return Ok(()),
    };

    let rel_path = file_path
        .strip_prefix(base_path)
        .unwrap_or(file_path)
        .to_string_lossy()
        .to_string();

    let urls = extract_urls(&content);
    let lines: Vec<&str> = content.lines().collect();

    for (url, line_num) in urls {
        // 跳过明显的非 API URL（静态资源等）
        let lower_url = url.to_lowercase();
        if lower_url.ends_with(".js")
            || lower_url.ends_with(".css")
            || lower_url.ends_with(".png")
            || lower_url.ends_with(".jpg")
            || lower_url.ends_with(".svg")
            || lower_url.ends_with(".woff")
            || lower_url.ends_with(".ico")
            || lower_url.ends_with(".map")
            || lower_url.contains("cdn.")
        {
            continue;
        }

        // 幂等去重
        let dedup_key = format!("{}:{}", extract_domain(&url), url.split('?').next().unwrap_or(&url));
        if seen.contains(&dedup_key) {
            continue;
        }
        seen.insert(dedup_key);

        let line_content = if line_num > 0 && line_num <= lines.len() {
            lines[line_num - 1]
        } else {
            ""
        };

        let (provider, _) = classify_provider(&extract_domain(&url));

        calls.push(ApiCall {
            endpoint: url.clone(),
            method: guess_method(&url, line_content),
            frequency_hint: "1000次/天（默认估算基准）".to_string(),
            auth_type: guess_auth(line_content),
            provider: provider.to_string(),
            file: rel_path.clone(),
            line: Some(line_num as u32),
        });
    }

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    #[test]
    fn test_analyze_python_openai() {
        let dir = std::env::temp_dir().join("lh-station-cost-openai");
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::write(
            dir.join("ai_client.py"),
            r#"
import openai
client = openai.OpenAI(api_key="sk-xxx")
response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "hello"}]
)
print(response)
url = "https://api.openai.com/v1/chat/completions"
"#,
        )
        .unwrap();

        let output_dir = dir.join("output");
        std::fs::create_dir_all(&output_dir).unwrap();

        let report = analyze(&dir, &output_dir).unwrap();
        assert!(report.total_apis_detected >= 1);
        assert!(!report.cross_border_apis.is_empty());
        // OpenAI 境外 → risk >= Medium
        assert!(report.data_sovereign_risk.contains("Medium")
            || report.data_sovereign_risk.contains("High")
            || report.data_sovereign_risk.contains("Critical"));
        assert!(report.estimated_monthly_cny > 0.0);
        assert!(output_dir.join(".cost-report.json").exists());

        std::fs::remove_dir_all(&dir).ok();
    }

    #[test]
    fn test_analyze_domestic_only() {
        let dir = std::env::temp_dir().join("lh-station-cost-domestic");
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::write(
            dir.join("cloud.js"),
            r#"
const tencent = require('tencentcloud-sdk-nodejs');
fetch('https://cvm.tencentcloudapi.com/');
fetch('https://ecs.aliyuncs.com/');
"#,
        )
        .unwrap();

        let output_dir = dir.join("output");
        std::fs::create_dir_all(&output_dir).unwrap();

        let report = analyze(&dir, &output_dir).unwrap();
        // 纯国内 → risk = Low
        assert_eq!(report.data_sovereign_risk, "🟢 Low");
        assert!(report.cross_border_apis.is_empty());
        assert!(!report.domestic_apis.is_empty());

        std::fs::remove_dir_all(&dir).ok();
    }

    #[test]
    fn test_analyze_no_api() {
        let dir = std::env::temp_dir().join("lh-station-cost-clean");
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::write(dir.join("main.rs"), "fn main() { println!(\"hello\"); }\n").unwrap();

        let output_dir = dir.join("output");
        std::fs::create_dir_all(&output_dir).unwrap();

        let report = analyze(&dir, &output_dir).unwrap();
        assert_eq!(report.total_apis_detected, 0);
        assert_eq!(report.estimated_monthly_cny, 0.0);
        assert_eq!(report.data_sovereign_risk, "🟢 Low");

        std::fs::remove_dir_all(&dir).ok();
    }

    #[test]
    fn test_classify_self_hosted() {
        let (provider, price) = classify_provider("localhost:8080");
        assert_eq!(provider, ApiProvider::SelfHosted);
        assert_eq!(price, 0.0);

        let (provider, price) = classify_provider("192.168.1.100:3000");
        assert_eq!(provider, ApiProvider::SelfHosted);
        assert_eq!(price, 0.0);
    }

    #[test]
    fn test_extract_domain() {
        assert_eq!(extract_domain("https://api.openai.com/v1/chat"), "api.openai.com");
        assert_eq!(extract_domain("https://cvm.tencentcloudapi.com/"), "cvm.tencentcloudapi.com");
        assert_eq!(extract_domain("http://localhost:8080/api"), "localhost");
    }

    #[test]
    fn test_cost_report_file_output() {
        let dir = std::env::temp_dir().join("lh-station-cost-file");
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::write(
            dir.join("api.py"),
            "requests.post('https://uid9622.cn/api/test')\n",
        )
        .unwrap();

        let output_dir = dir.join("output");
        std::fs::create_dir_all(&output_dir).unwrap();

        let report = analyze(&dir, &output_dir).unwrap();
        // uid9622.cn 是自托管/国内
        assert!(report.cross_border_apis.is_empty());
        assert!(output_dir.join(".cost-report.json").exists());

        // 验证 JSON 可反序列化
        let content = std::fs::read_to_string(output_dir.join(".cost-report.json")).unwrap();
        let parsed: CostReport = serde_json::from_str(&content).unwrap();
        assert_eq!(parsed.total_apis_detected, report.total_apis_detected);

        std::fs::remove_dir_all(&dir).ok();
    }
}
