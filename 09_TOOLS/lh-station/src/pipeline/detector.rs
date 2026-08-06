// 龍魂代码中转站 · 代码解析器
// 检测: 语言/框架/目标平台 · 只读无副作用
// DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-DETECTOR-v1.0

use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::path::Path;
use walkdir::WalkDir;

/// 编程语言
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub enum Language {
    Python,
    JavaScript,
    TypeScript,
    Rust,
    C,
    Cpp,
    Go,
    Java,
    Kotlin,
    Swift,
    ArkTS,
    Shell,
    Markdown,
    Yaml,
    Toml,
    Json,
    Html,
    Css,
    Unknown(String),
}

impl std::fmt::Display for Language {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Language::Python => write!(f, "Python"),
            Language::JavaScript => write!(f, "JavaScript"),
            Language::TypeScript => write!(f, "TypeScript"),
            Language::Rust => write!(f, "Rust"),
            Language::C => write!(f, "C"),
            Language::Cpp => write!(f, "C++"),
            Language::Go => write!(f, "Go"),
            Language::Java => write!(f, "Java"),
            Language::Kotlin => write!(f, "Kotlin"),
            Language::Swift => write!(f, "Swift"),
            Language::ArkTS => write!(f, "ArkTS"),
            Language::Shell => write!(f, "Shell"),
            Language::Markdown => write!(f, "Markdown"),
            Language::Yaml => write!(f, "YAML"),
            Language::Toml => write!(f, "TOML"),
            Language::Json => write!(f, "JSON"),
            Language::Html => write!(f, "HTML"),
            Language::Css => write!(f, "CSS"),
            Language::Unknown(s) => write!(f, "Unknown({})", s),
        }
    }
}

/// 目标平台
#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub enum Platform {
    HarmonyOS,
    IOS,
    Android,
    Linux,
    Windows,
    MacOS,
    Web,
    Unknown,
}

impl std::fmt::Display for Platform {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Platform::HarmonyOS => write!(f, "HarmonyOS"),
            Platform::IOS => write!(f, "iOS"),
            Platform::Android => write!(f, "Android"),
            Platform::Linux => write!(f, "Linux"),
            Platform::Windows => write!(f, "Windows"),
            Platform::MacOS => write!(f, "macOS"),
            Platform::Web => write!(f, "Web"),
            Platform::Unknown => write!(f, "General"),
        }
    }
}

/// 代码输入描述
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CodeInput {
    pub path: String,
    pub language: String,
    pub framework: Option<String>,
    pub platform: String,
    pub files: Vec<DetectedFile>,
    pub file_count: usize,
    pub has_docker: bool,
    pub has_ci: bool,
}

/// 单个被检测文件
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct DetectedFile {
    pub path: String,
    pub language: String,
    pub is_binary: bool,
    pub size_bytes: u64,
}

/// 扩展名 → 语言映射
fn ext_to_language(ext: &str) -> Language {
    match ext {
        "py" => Language::Python,
        "js" => Language::JavaScript,
        "mjs" => Language::JavaScript,
        "cjs" => Language::JavaScript,
        "ts" => Language::TypeScript,
        "tsx" => Language::TypeScript,
        "jsx" => Language::JavaScript,
        "rs" => Language::Rust,
        "c" => Language::C,
        "h" => Language::C,
        "cpp" => Language::Cpp,
        "cc" => Language::Cpp,
        "cxx" => Language::Cpp,
        "hpp" => Language::Cpp,
        "go" => Language::Go,
        "java" => Language::Java,
        "kt" => Language::Kotlin,
        "kts" => Language::Kotlin,
        "swift" => Language::Swift,
        "ets" => Language::ArkTS,
        "sh" => Language::Shell,
        "bash" => Language::Shell,
        "zsh" => Language::Shell,
        "md" => Language::Markdown,
        "yaml" => Language::Yaml,
        "yml" => Language::Yaml,
        "toml" => Language::Toml,
        "json" => Language::Json,
        "html" => Language::Html,
        "htm" => Language::Html,
        "css" => Language::Css,
        "scss" => Language::Css,
        "less" => Language::Css,
        _ => Language::Unknown(ext.to_string()),
    }
}

/// 二进制文件扩展名
const BINARY_EXTS: &[&str] = &[
    "so", "dylib", "dll", "a", "o", "obj", "exe", "bin",
    "wasm", "pyc", "pyo", "class", "jar", "war",
    "jpg", "jpeg", "png", "gif", "webp", "svg", "ico",
    "mp3", "mp4", "wav", "flac", "ogg", "avi", "mov",
    "zip", "tar", "gz", "bz2", "xz", "7z", "rar",
    "pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx",
    "ttf", "otf", "woff", "woff2",
    "db", "sqlite", "sqlite3",
    "lock", "sum",
];

fn is_binary_ext(ext: &str) -> bool {
    BINARY_EXTS.iter().any(|e| e.eq_ignore_ascii_case(ext))
}

/// 检测框架
fn detect_framework(files: &[DetectedFile]) -> Option<String> {
    let file_paths: Vec<&str> = files.iter().map(|f| f.path.as_str()).collect();
    
    if file_paths.iter().any(|p| p.contains("build-profile.json5") || p.contains("module.json5")) {
        return Some("HarmonyOS / ArkUI".to_string());
    }
    if file_paths.iter().any(|p| p.contains("pubspec.yaml")) {
        return Some("Flutter".to_string());
    }
    if file_paths.iter().any(|p| p.contains("Cargo.toml")) {
        // 检查是否包含鸿蒙 target
        if file_paths.iter().any(|p| p.contains(".ets")) {
            return Some("Rust + HarmonyOS".to_string());
        }
        return Some("Rust / Cargo".to_string());
    }
    if file_paths.iter().any(|p| p.ends_with("package.json")) {
        if file_paths.iter().any(|p| p.contains("node_modules/react-native")) {
            return Some("React Native".to_string());
        }
        if file_paths.iter().any(|p| p.contains("next.config")) {
            return Some("Next.js".to_string());
        }
        if file_paths.iter().any(|p| p.ends_with("vue.config.js") || p.ends_with("nuxt.config.ts")) {
            return Some("Vue / Nuxt".to_string());
        }
        return Some("Node.js / npm".to_string());
    }
    if file_paths.iter().any(|p| p.contains("go.mod")) {
        return Some("Go Modules".to_string());
    }
    if file_paths.iter().any(|p| p.ends_with("requirements.txt") || p.ends_with("setup.py") || p.ends_with("pyproject.toml")) {
        if file_paths.iter().any(|p| p.contains("Django")) {
            return Some("Django".to_string());
        }
        if file_paths.iter().any(|p| p.contains("FastAPI") || p.contains("fastapi")) {
            return Some("FastAPI".to_string());
        }
        return Some("Python / pip".to_string());
    }
    None
}

/// 检测目标平台
fn detect_platform(files: &[DetectedFile]) -> Platform {
    let file_paths: Vec<&str> = files.iter().map(|f| f.path.as_str()).collect();
    
    // HarmonyOS
    if file_paths.iter().any(|p| p.ends_with(".ets")) 
        && file_paths.iter().any(|p| p.contains("module.json5")) {
        return Platform::HarmonyOS;
    }
    
    // iOS
    if file_paths.iter().any(|p| p.ends_with(".swift"))
        && file_paths.iter().any(|p| p.ends_with(".xcodeproj") || p.contains(".xcodeproj/")) {
        return Platform::IOS;
    }
    
    // Android
    if file_paths.iter().any(|p| p.ends_with(".kt") || p.ends_with(".java"))
        && file_paths.iter().any(|p| p.contains("AndroidManifest.xml")) {
        return Platform::Android;
    }
    
    // Web
    if file_paths.iter().any(|p| p.ends_with(".html") || p.ends_with(".vue") || p.ends_with(".svelte")) {
        return Platform::Web;
    }
    
    Platform::Unknown
}

/// 主检测函数
pub fn detect(input_path: &Path) -> Result<CodeInput, String> {
    if !input_path.exists() {
        return Err(format!("路径不存在: {}", input_path.display()));
    }

    let mut lang_counts: HashMap<Language, usize> = HashMap::new();
    let mut detected_files: Vec<DetectedFile> = Vec::new();
    let mut has_docker = false;
    let mut has_ci = false;

    for entry in WalkDir::new(input_path)
        .follow_links(false)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        
        // 跳过隐藏目录和常见忽略目录
        let path_str = path.to_string_lossy();
        if path_str.contains("/.") 
            || path_str.contains("target/")
            || path_str.contains("node_modules/")
            || path_str.contains("__pycache__/")
            || path_str.contains(".git/")
            || path_str.contains("build/")
            || path_str.contains("dist/")
            || path_str.contains(".sovereign") // 跳过已生成的主权文件
        {
            continue;
        }

        if !path.is_file() {
            continue;
        }

        // 检查 Dockerfile
        if path.file_name().map_or(false, |n| {
            let n = n.to_string_lossy().to_lowercase();
            n == "dockerfile" || n.starts_with("dockerfile.")
        }) {
            has_docker = true;
        }

        // 检查 CI 配置
        if path.file_name().map_or(false, |n| {
            let n = n.to_string_lossy();
            n == ".gitlab-ci.yml" || n.contains("jenkins") 
                || n.starts_with(".github/workflows")
        }) {
            has_ci = true;
        }

        let ext = path.extension()
            .map(|e| e.to_string_lossy().to_lowercase())
            .unwrap_or_default();
        
        let is_binary = is_binary_ext(&ext);
        let file_size = match std::fs::metadata(path) {
            Ok(m) if is_binary => m.len(),
            _ => 0,
        };

        // 跳过太大的二进制文件
        if is_binary && file_size > 10_000_000 {
            continue;
        }

        if !ext.is_empty() {
            let lang = ext_to_language(&ext);
            *lang_counts.entry(lang.clone()).or_insert(0) += 1;

            let rel_path = path.strip_prefix(input_path)
                .unwrap_or(path)
                .to_string_lossy()
                .to_string();

            detected_files.push(DetectedFile {
                path: rel_path,
                language: lang.to_string(),
                is_binary,
                size_bytes: file_size,
            });
        }
    }

    // 取占比最高的语言
    let primary_lang = lang_counts
        .into_iter()
        .max_by_key(|(_, count)| *count)
        .map(|(lang, _)| lang)
        .unwrap_or(Language::Unknown("unknown".to_string()));

    let platform = detect_platform(&detected_files);
    let framework = detect_framework(&detected_files);
    let file_count = detected_files.len();

    Ok(CodeInput {
        path: input_path.to_string_lossy().to_string(),
        language: primary_lang.to_string(),
        framework,
        platform: platform.to_string(),
        files: detected_files,
        file_count,
        has_docker,
        has_ci,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_ext_to_language() {
        assert_eq!(ext_to_language("py"), Language::Python);
        assert_eq!(ext_to_language("rs"), Language::Rust);
        assert_eq!(ext_to_language("js"), Language::JavaScript);
        assert_eq!(ext_to_language("ts"), Language::TypeScript);
        assert_eq!(ext_to_language("ets"), Language::ArkTS);
    }

    #[test]
    fn test_is_binary_ext() {
        assert!(is_binary_ext("so"));
        assert!(is_binary_ext("png"));
        assert!(is_binary_ext("zip"));
        assert!(!is_binary_ext("py"));
        assert!(!is_binary_ext("rs"));
    }

    #[test]
    fn test_detect_nonexistent() {
        let result = detect(Path::new("/nonexistent/path/12345"));
        assert!(result.is_err());
    }
}
