// 龍魂分层许可 + 中国法合规声明
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-LICENSE-ENGINE-v1.0

/// 许可类型
#[derive(Debug, Clone, PartialEq)]
pub enum LicenseType {
    /// 核心思想层 - CC BY-NC-SA 4.0
    Thought,
    /// 工程实现层 - MulanPSL v2
    Engineering,
}

/// 根据文件扩展名判定许可类型
pub fn detect_license(file_path: &str) -> LicenseType {
    let path_lower = file_path.to_lowercase();
    
    // 工程实现层（代码文件）
    let engineering_exts = [
        ".py", ".js", ".ts", ".html", ".css", ".sh", ".bash",
        ".rs", ".c", ".cpp", ".h", ".hpp", ".go", ".java", ".kt",
        ".swift", ".ets", ".tsx", ".jsx", ".vue", ".svelte",
        ".dockerfile", ".yml", ".yaml", ".toml", ".lock",
        ".makefile", ".cmake", ".gradle", ".xml",
    ];
    
    for ext in &engineering_exts {
        if path_lower.ends_with(ext) {
            return LicenseType::Engineering;
        }
    }
    
    // Dockerfile 特殊处理
    if path_lower.contains("dockerfile") || path_lower.ends_with("dockerfile") {
        return LicenseType::Engineering;
    }
    
    // 核心思想层（文档/协议）
    LicenseType::Thought
}

/// 生成许可声明
pub fn get_license_header(file_path: &str, language: &str) -> String {
    match detect_license(file_path) {
        LicenseType::Thought => {
            format!(
                "> 协议: CC BY-NC-SA 4.0（核心思想层）· 来源链不可切断· 署名-非商业-相同方式共享"
            )
        }
        LicenseType::Engineering => {
            format!(
                "# License: MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)"
            )
        }
    }
}

/// 中国法合规声明
pub fn get_compliance_declaration() -> String {
    "中国法律为本代码唯一准绳·数据不在未经授权下出境·为中国人民服务".to_string()
}

/// 反殖民声明
pub fn get_anti_colonial_declaration() -> String {
    "主权标识: 中華人民共和國·龍魂體系·UID9622·不依附于任何外部平台".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_detect_license_engineering() {
        assert_eq!(detect_license("main.py"), LicenseType::Engineering);
        assert_eq!(detect_license("app.js"), LicenseType::Engineering);
        assert_eq!(detect_license("lib.rs"), LicenseType::Engineering);
        assert_eq!(detect_license("index.ets"), LicenseType::Engineering);
    }

    #[test]
    fn test_detect_license_thought() {
        assert_eq!(detect_license("README.md"), LicenseType::Thought);
        assert_eq!(detect_license("protocol.txt"), LicenseType::Thought);
    }

    #[test]
    fn test_license_headers_not_empty() {
        let eng = get_license_header("main.rs", "Rust");
        assert!(eng.contains("MulanPSL"));
        
        let thought = get_license_header("README.md", "Markdown");
        assert!(thought.contains("CC BY-NC-SA"));
    }
}
