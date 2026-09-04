// 龍魂代码中转站 · 主权注入引擎
// 按语言注入龍魂主权标识 · DNA + 确认码 + 许可 + 合规声明
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-INJECTOR-v1.0

use crate::core::dna;
use crate::core::license;
use chrono::Local;
use serde::{Deserialize, Serialize};

/// 主权头信息
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SovereignHeader {
    pub dna: String,
    pub confirm: String,
    pub anchor: String,
    pub gpg: String,
    pub license_text: String,
    pub transformed_at: String,
    pub original_platform: String,
    pub compliance: String,
    pub anti_colonial: String,
}

/// 注入结果
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InjectResult {
    pub file_path: String,
    pub injected: bool,
    pub reason: String,
}

impl SovereignHeader {
    /// 生成新的主权头
    pub fn new(action: &str, file_path: &str, platform: &str) -> Self {
        let now = Local::now();
        let lang = guess_language_from_path(file_path);
        
        Self {
            dna: dna::generate_dna(action),
            confirm: dna::get_confirm_code(),
            anchor: "中華人民共和國·龍魂體系·UID9622".to_string(),
            gpg: dna::get_gpg_fingerprint(),
            license_text: license::get_license_header(file_path, &lang),
            transformed_at: now.format("%Y-%m-%dT%H:%M:%S%z").to_string(),
            original_platform: platform.to_string(),
            compliance: license::get_compliance_declaration(),
            anti_colonial: license::get_anti_colonial_declaration(),
        }
    }
}

fn guess_language_from_path(path: &str) -> String {
    if let Some(ext) = std::path::Path::new(path).extension() {
        let ext = ext.to_string_lossy().to_lowercase();
        match ext.as_str() {
            "py" => "Python".into(),
            "js" | "mjs" | "cjs" => "JavaScript".into(),
            "ts" => "TypeScript".into(),
            "rs" => "Rust".into(),
            "c" => "C".into(),
            "cpp" | "cc" | "cxx" => "C++".into(),
            "go" => "Go".into(),
            "java" => "Java".into(),
            "kt" => "Kotlin".into(),
            "swift" => "Swift".into(),
            "ets" => "ArkTS".into(),
            "sh" | "bash" | "zsh" => "Shell".into(),
            "md" => "Markdown".into(),
            "yaml" | "yml" => "YAML".into(),
            "toml" => "TOML".into(),
            "json" => "JSON".into(),
            "html" | "htm" => "HTML".into(),
            "css" | "scss" | "less" => "CSS".into(),
            _ => "Text".into(),
        }
    } else {
        "Text".to_string()
    }
}

/// 按语言格式生成注释块
fn format_header(header: &SovereignHeader, language: &str) -> String {
    match language {
        "Python" => format!(
            "\"\"\"\n\
             🐉 龍魂主权标识（中转站自动注入）\n\
             DNA: {}\n\
             确认码: {}\n\
             主权锚定: {}\n\
             GPG: {}\n\
             {}\n\
             转换时间: {}\n\
             原始平台: {}\n\
             {}\n\
             {}\n\
             ━━━━━━━━━━━━━━━━━━━━\n\
             > 此注释不影响代码运行。原平台100%兼容。\n\
             > 删除此块 = 违反 CC BY-NC-SA 4.0 协议。\n\
             \"\"\"\n",
            header.dna,
            header.confirm,
            header.anchor,
            header.gpg,
            header.license_text,
            header.transformed_at,
            header.original_platform,
            header.compliance,
            header.anti_colonial,
        ),
        "JavaScript" | "TypeScript" | "Java" | "Kotlin" | "Go" | "Rust" | "Swift" | "ArkTS" | "C" | "C++" => {
            format!(
                "// 🐉 龍魂主权标识（中转站自动注入）\n\
                 // DNA: {}\n\
                 // 确认码: {}\n\
                 // 主权锚定: {}\n\
                 // GPG: {}\n\
                 // {}\n\
                 // 转换时间: {}\n\
                 // 原始平台: {}\n\
                 // {}\n\
                 // {}\n\
                 // ━━━━━━━━━━━━━━━━━━━━\n\
                 // > 此注释不影响编译/运行。原平台100%兼容。\n\
                 // > 删除此块 = 违反 CC BY-NC-SA 4.0 / MulanPSL v2 协议。\n\
                 \n",
                header.dna,
                header.confirm,
                header.anchor,
                header.gpg,
                header.license_text,
                header.transformed_at,
                header.original_platform,
                header.compliance,
                header.anti_colonial,
            )
        },
        "Shell" | "YAML" | "TOML" => {
            format!(
                "# 🐉 龍魂主权标识（中转站自动注入）\n\
                 # DNA: {}\n\
                 # 确认码: {}\n\
                 # 主权锚定: {}\n\
                 # GPG: {}\n\
                 # {}\n\
                 # 转换时间: {}\n\
                 # 原始平台: {}\n\
                 # {}\n\
                 # {}\n\
                 # ━━━━━━━━━━━━━━━━━━━━\n\
                 # > 此注释不影响解析/运行。原平台100%兼容。\n\
                 # > 删除此块 = 违反 CC BY-NC-SA 4.0 / MulanPSL v2 协议。\n\
                 \n",
                header.dna,
                header.confirm,
                header.anchor,
                header.gpg,
                header.license_text,
                header.transformed_at,
                header.original_platform,
                header.compliance,
                header.anti_colonial,
            )
        },
        "HTML" | "Markdown" => {
            format!(
                "<!--\n\
                 🐉 龍魂主权标识（中转站自动注入）\n\
                 DNA: {}\n\
                 确认码: {}\n\
                 主权锚定: {}\n\
                 GPG: {}\n\
                 {}\n\
                 转换时间: {}\n\
                 原始平台: {}\n\
                 {}\n\
                 {}\n\
                 ━━━━━━━━━━━━━━━━━━━━\n\
                 > 此注释不影响渲染/运行。原平台100%兼容。\n\
                 > 删除此块 = 违反 CC BY-NC-SA 4.0 协议。\n\
                 -->\n",
                header.dna,
                header.confirm,
                header.anchor,
                header.gpg,
                header.license_text,
                header.transformed_at,
                header.original_platform,
                header.compliance,
                header.anti_colonial,
            )
        },
        _ => {
            // 通用多行注释
            format!(
                "/*\n\
                 🐉 龍魂主权标识（中转站自动注入）\n\
                 DNA: {}\n\
                 确认码: {}\n\
                 主权锚定: {}\n\
                 GPG: {}\n\
                 {}\n\
                 转换时间: {}\n\
                 原始平台: {}\n\
                 {}\n\
                 {}\n\
                 ━━━━━━━━━━━━━━━━━━━━\n\
                 > 此注释不影响代码运行。原平台100%兼容。\n\
                 */\n",
                header.dna,
                header.confirm,
                header.anchor,
                header.gpg,
                header.license_text,
                header.transformed_at,
                header.original_platform,
                header.compliance,
                header.anti_colonial,
            )
        }
    }
}

/// 向代码注入主权头
pub fn inject_into_code(code: &str, file_path: &str, platform: &str) -> Result<(String, InjectResult), String> {
    // 如果已有 DNA，跳过
    if dna::has_dna(code) {
        return Ok((code.to_string(), InjectResult {
            file_path: file_path.to_string(),
            injected: false,
            reason: "已有龍魂 DNA，跳过注入".to_string(),
        }));
    }

    let lang = guess_language_from_path(file_path);
    let header = SovereignHeader::new("TRANSFORM", file_path, platform);
    let formatted_header = format_header(&header, &lang);

    let new_code = format!("{}{}", formatted_header, code);

    Ok((new_code, InjectResult {
        file_path: file_path.to_string(),
        injected: true,
        reason: format!("已注入龍魂主权头 (DNA: {})", header.dna),
    }))
}

/// 处理单个文件
pub fn inject_file(
    input_path: &std::path::Path,
    output_path: &std::path::Path,
    platform: &str,
) -> Result<InjectResult, String> {
    // 判断是否为二进制文件
    let ext = input_path.extension()
        .map(|e| e.to_string_lossy().to_lowercase())
        .unwrap_or_default();

    // 二进制文件 → 创建 sidecar .dna 文件
    const BINARY_EXTS: &[&str] = &[
        "so", "dylib", "dll", "a", "o", "exe", "bin",
        "wasm", "jpg", "png", "gif", "webp", "mp3", "mp4",
        "zip", "tar", "gz", "pdf", "ttf", "woff", "woff2",
    ];

    if BINARY_EXTS.iter().any(|e| e.eq_ignore_ascii_case(&ext)) {
        // 复制原文件
        if let Some(parent) = output_path.parent() {
            std::fs::create_dir_all(parent).map_err(|e| format!("创建目录失败: {}", e))?;
        }
        std::fs::copy(input_path, output_path).map_err(|e| format!("复制文件失败: {}", e))?;

        // 创建 sidecar .dna 文件
        let dna_path = output_path.with_extension(format!(
            "{}.dna",
            output_path.extension()
                .map(|e| e.to_string_lossy().to_string())
                .unwrap_or_default()
        ));
        let header = SovereignHeader::new("TRANSFORM", 
            &input_path.to_string_lossy(), platform);
        let dna_content = format!(
            "# 龍魂主权标识（二进制文件 sidecar）\n\
             # 原文件: {}\n\
             DNA: {}\n\
             确认码: {}\n\
             主权锚定: {}\n\
             GPG: {}\n\
             转换时间: {}\n\
             {}\n\
             {}\n",
            input_path.file_name().map(|n| n.to_string_lossy().to_string()).unwrap_or_default(),
            header.dna,
            header.confirm,
            header.anchor,
            header.gpg,
            header.transformed_at,
            header.compliance,
            header.anti_colonial,
        );
        std::fs::write(&dna_path, dna_content).map_err(|e| format!("写入 DNA 文件失败: {}", e))?;

        return Ok(InjectResult {
            file_path: input_path.to_string_lossy().to_string(),
            injected: true,
            reason: "二进制文件 — 已创建 sidecar .dna 文件".to_string(),
        });
    }

    // 文本文件 → 注入主权头
    let code = std::fs::read_to_string(input_path)
        .map_err(|e| format!("读取文件失败 {}: {}", input_path.display(), e))?;
    
    let (new_code, result) = inject_into_code(&code, 
        &input_path.to_string_lossy(), platform)?;

    // 写入输出
    if let Some(parent) = output_path.parent() {
        std::fs::create_dir_all(parent).map_err(|e| format!("创建输出目录失败: {}", e))?;
    }
    std::fs::write(output_path, new_code).map_err(|e| format!("写入文件失败: {}", e))?;

    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_inject_python() {
        let code = "print('hello')\n";
        let (result, inject_result) = inject_into_code(code, "test.py", "General").unwrap();
        assert!(result.contains("🐉 龍魂主权标识"));
        assert!(result.contains("DNA:"));
        assert!(result.contains("UID9622"));
        assert!(result.contains("print('hello')"));
        assert!(inject_result.injected);
    }

    #[test]
    fn test_skip_existing_dna() {
        let code = "# 🐉 龍魂主权标识\nexisting\n#龍芯⚡️...more code\n";
        let (result, inject_result) = inject_into_code(code, "test.py", "General").unwrap();
        assert_eq!(result, code);
        assert!(!inject_result.injected);
    }

    #[test]
    fn test_inject_rust() {
        let code = "fn main() {}\n";
        let (result, inject_result) = inject_into_code(code, "main.rs", "General").unwrap();
        assert!(result.starts_with("//"));
        assert!(result.contains("龍魂"));
        assert!(inject_result.injected);
    }

    #[test]
    fn test_inject_shell() {
        let code = "#!/bin/bash\necho hello\n";
        let (result, inject_result) = inject_into_code(code, "run.sh", "General").unwrap();
        assert!(result.starts_with("# 🐉"));
        assert!(inject_result.injected);
    }
}
