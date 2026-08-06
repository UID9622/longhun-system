// 龍魂代码中转站 · GPG 签名引擎
// DNA: #龍芯⚡️丙午·癸未·乙酉·坤卦-SIGNER-v1.0

use serde::{Deserialize, Serialize};
use std::path::Path;
use std::process::Command;

/// 签名结果
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SignResult {
    pub file: String,
    pub signed: bool,
    pub asc_file: Option<String>,
    pub message: String,
}

/// 检查 GPG 是否可用
pub fn is_gpg_available() -> bool {
    Command::new("which")
        .arg("gpg")
        .output()
        .map(|o| o.status.success())
        .unwrap_or(false)
}

/// 检查 GPG 密钥是否已配置
pub fn is_key_configured(fingerprint: &str) -> bool {
    if !is_gpg_available() {
        return false;
    }
    Command::new("gpg")
        .args(["--list-keys", fingerprint])
        .output()
        .map(|o| o.status.success())
        .unwrap_or(false)
}

/// 对单个文件进行 GPG 分离签名
pub fn sign_file(file_path: &Path) -> Result<SignResult, String> {
    if !is_gpg_available() {
        return Ok(SignResult {
            file: file_path.to_string_lossy().to_string(),
            signed: false,
            asc_file: None,
            message: "GPG 不可用，跳过签名".to_string(),
        });
    }

    let output = Command::new("gpg")
        .args([
            "--detach-sign",
            "--armor",
            "--default-key",
            "A2D0092CEE2E5BA87035600924C3704A8CC26D5F",
            file_path.to_str().unwrap_or(""),
        ])
        .output()
        .map_err(|e| format!("GPG 签名失败: {}", e))?;

    if output.status.success() {
        let asc_path = format!("{}.asc", file_path.to_string_lossy());
        Ok(SignResult {
            file: file_path.to_string_lossy().to_string(),
            signed: true,
            asc_file: Some(asc_path),
            message: "GPG 签名成功".to_string(),
        })
    } else {
        Ok(SignResult {
            file: file_path.to_string_lossy().to_string(),
            signed: false,
            asc_file: None,
            message: format!("签名失败: {}", String::from_utf8_lossy(&output.stderr)),
        })
    }
}

/// 验证已签名文件的签名
pub fn verify_signature(file_path: &Path) -> Result<bool, String> {
    if !is_gpg_available() {
        return Err("GPG 不可用".to_string());
    }

    let asc_path = format!("{}.asc", file_path.to_string_lossy());
    if !Path::new(&asc_path).exists() {
        return Ok(false);
    }

    let output = Command::new("gpg")
        .args(["--verify", &asc_path, file_path.to_str().unwrap_or("")])
        .output()
        .map_err(|e| format!("GPG 验证失败: {}", e))?;

    Ok(output.status.success())
}

/// 批量签名
pub fn sign_directory(dir: &Path, _skip_binary: bool) -> Result<Vec<SignResult>, String> {
    let mut results = Vec::new();

    for entry in walkdir::WalkDir::new(dir)
        .follow_links(false)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let path = entry.path();
        if !path.is_file() {
            continue;
        }

        // 跳过 .asc 和 .dna 文件
        let ext = path.extension().map(|e| e.to_string_lossy().to_lowercase()).unwrap_or_default();
        if ext == "asc" || ext == "dna" {
            continue;
        }

        // 跳过隐藏文件
        if path.file_name().map_or(false, |n| n.to_string_lossy().starts_with('.')) {
            continue;
        }

        match sign_file(path) {
            Ok(result) => results.push(result),
            Err(e) => {
                results.push(SignResult {
                    file: path.to_string_lossy().to_string(),
                    signed: false,
                    asc_file: None,
                    message: e,
                });
            }
        }
    }

    Ok(results)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_is_gpg_available() {
        // 至少不崩溃
        let _ = is_gpg_available();
    }
}
