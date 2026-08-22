// 龍魂代码中转站 · 打包输出引擎
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-PACKER-v1.0

use crate::core::dna;
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};

/// 打包文件
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PackedFile {
    pub path: String,
    pub size_bytes: u64,
    pub had_dna: bool,
    pub injected: bool,
    pub signed: bool,
}

/// 转换清单
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Manifest {
    pub station_version: String,
    pub transformed_at: String,
    pub original_path: String,
    pub language: String,
    pub framework: Option<String>,
    pub original_platform: String,
    pub chip_target: String,
    pub total_files: u32,
    pub injected: u32,
    pub compiled: u32,
    pub signed: u32,
    pub dna: String,
    pub security_passed: bool,
    pub r_score: u32,             // 三色审计 R 值 (0-95)
    // 成本分析字段（第七批）
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cost_monthly_cny: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cost_daily_cny: Option<f64>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub data_sovereign_risk: Option<String>,
    #[serde(skip_serializing_if = "Option::is_none")]
    pub cross_border_api_count: Option<u32>,
}

/// 主权 JSON 元数据
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SovereignJSON {
    pub station: String,
    pub version: String,
    pub dna: String,
    pub confirm_code: String,
    pub creator: String,
    pub gpg_fingerprint: String,
    pub transformed_at: String,
    pub original_path: String,
    pub language: String,
    pub platform: String,
    pub chip_target: String,
    pub license_model: String,
    pub jurisdiction: String,
    pub files_count: u32,
}

/// 输出包
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct OutputPackage {
    pub output_dir: String,
    pub files: Vec<PackedFile>,
    pub manifest: Manifest,
    pub sovereign_json: SovereignJSON,
}

/// 生成 SovereignJSON
pub fn generate_sovereign_json(
    original_path: &str,
    language: &str,
    platform: &str,
    chip_target: &str,
    files_count: u32,
) -> SovereignJSON {
    let action_dna = dna::generate_dna("TRANSFORM");
    SovereignJSON {
        station: "龍魂代码中转站".to_string(),
        version: "1.0.0".to_string(),
        dna: action_dna.clone(),
        confirm_code: dna::get_confirm_code(),
        creator: "诸葛鑫（UID9622）".to_string(),
        gpg_fingerprint: dna::get_gpg_fingerprint(),
        transformed_at: chrono::Local::now().format("%Y-%m-%dT%H:%M:%S%z").to_string(),
        original_path: original_path.to_string(),
        language: language.to_string(),
        platform: platform.to_string(),
        chip_target: chip_target.to_string(),
        license_model: "核心思想层: CC BY-NC-SA 4.0 | 工程实现层: MulanPSL v2".to_string(),
        jurisdiction: "中华人民共和国".to_string(),
        files_count,
    }
}

/// 生成 Manifest
pub fn generate_manifest(
    original_path: &str,
    language: &str,
    framework: Option<&str>,
    platform: &str,
    chip_target: &str,
    total_files: u32,
    injected: u32,
    compiled: u32,
    signed: u32,
    security_passed: bool,
    r_score: u32,
) -> Manifest {
    Manifest {
        station_version: "1.0.0".to_string(),
        transformed_at: chrono::Local::now().format("%Y-%m-%dT%H:%M:%S%z").to_string(),
        original_path: original_path.to_string(),
        language: language.to_string(),
        framework: framework.map(|s| s.to_string()),
        original_platform: platform.to_string(),
        chip_target: chip_target.to_string(),
        total_files,
        injected,
        compiled,
        signed,
        dna: dna::generate_dna("TRANSFORM"),
        security_passed,
        r_score,
        cost_monthly_cny: None,
        cost_daily_cny: None,
        data_sovereign_risk: None,
        cross_border_api_count: None,
    }
}

/// 写入输出文件
pub fn write_output_files(
    output_dir: &Path,
    sovereign_json: &SovereignJSON,
    manifest: &Manifest,
) -> Result<(), String> {
    std::fs::create_dir_all(output_dir).map_err(|e| format!("创建输出目录失败: {}", e))?;

    // 写入 .sovereign.json
    let sovereign_path = output_dir.join(".sovereign.json");
    let sovereign_content = serde_json::to_string_pretty(sovereign_json)
        .map_err(|e| format!("序列化 sovereign.json 失败: {}", e))?;
    std::fs::write(&sovereign_path, sovereign_content)
        .map_err(|e| format!("写入 .sovereign.json 失败: {}", e))?;

    // 写入 manifest.json
    let manifest_path = output_dir.join("manifest.json");
    let manifest_content = serde_json::to_string_pretty(manifest)
        .map_err(|e| format!("序列化 manifest.json 失败: {}", e))?;
    std::fs::write(&manifest_path, manifest_content)
        .map_err(|e| format!("写入 manifest.json 失败: {}", e))?;

    // 写入 README.md（输出说明）
    let readme_path = output_dir.join("README-lh-station.md");
    let readme_content = format!(
        "# 🐉 龍魂代码中转站 · 转换输出\n\n\
         > 此目录由龍魂代码中转站 v1.0 自动生成\n\n\
         ## 主权标识\n\
         - DNA: {}\n\
         - 确认码: {}\n\
         - 创建者: 诸葛鑫（UID9622）\n\
         - 协议: 核心思想层 CC BY-NC-SA 4.0 / 工程实现层 MulanPSL v2\n\
         - 司法管辖区: 中华人民共和国\n\n\
         ## 兼容性\n\
         - 所有代码保留原始平台 100% 兼容\n\
         - 主权头作为注释注入，不影响编译/运行\n\
         - .so 编译产物在 libs/ 目录下（如有）\n\n\
         ## 文件说明\n\
         - `manifest.json` — 转换清单（完整记录所有操作）\n\
         - `.sovereign.json` — 主权元数据\n\
         - `*.asc` — GPG 分离签名\n\
         - `*.dna` — 二进制文件主权标识（如有）\n\n\
         ## 核心理念\n\
         > 代码随便用去赚钱，思想名号要授权。\n\
         > 不是要做系统，只是要一个中转站。\n\n\
         中国法律为本代码唯一准绳。\n",
        sovereign_json.dna,
        sovereign_json.confirm_code,
    );
    std::fs::write(&readme_path, readme_content)
        .map_err(|e| format!("写入 README 失败: {}", e))?;

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_generate_sovereign_json() {
        let sj = generate_sovereign_json("/test/project", "Python", "General", "鲲鹏", 5);
        assert!(sj.dna.contains("龍芯"));
        assert_eq!(sj.jurisdiction, "中华人民共和国");
        assert_eq!(sj.files_count, 5);
    }

    #[test]
    fn test_generate_manifest() {
        let m = generate_manifest("/test", "Rust", Some("Cargo"), "Linux", "鲲鹏", 10, 10, 1, 10, true, 95);
        assert_eq!(m.total_files, 10);
        assert_eq!(m.injected, 10);
        assert!(m.security_passed);
    }
}
