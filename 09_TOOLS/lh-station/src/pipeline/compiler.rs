// 龍魂代码中转站 · 芯片适配编译
// 交叉编译到中国芯片架构 · 鲲鹏/昇腾/飞腾/龙芯/申威
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-COMPILER-v1.0

use crate::core::config::ChipInfo;
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use std::process::Command;

/// 编译目标
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CompileTarget {
    pub chip_name: String,
    pub arch: String,
    pub rust_target: String,
}

/// 编译结果
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct CompileResult {
    pub chip: String,
    pub success: bool,
    pub output_file: Option<String>,
    pub message: String,
    pub compiled: bool,
}

impl CompileTarget {
    pub fn from_chip_info(info: &ChipInfo) -> Self {
        Self {
            chip_name: info.name.clone(),
            arch: info.arch.clone(),
            rust_target: info.rust_target.clone(),
        }
    }

    /// 自动选择最佳目标
    pub fn auto() -> Self {
        // 默认鲲鹏（已验证通过）
        Self {
            chip_name: "鲲鹏".to_string(),
            arch: "aarch64".to_string(),
            rust_target: "aarch64-unknown-linux-gnu".to_string(),
        }
    }
}

/// 检查交叉编译器是否可用
pub fn check_cross_compiler(target: &CompileTarget) -> bool {
    let gcc_name = format!("{}-linux-gnu-gcc", target.arch);
    Command::new("which")
        .arg(&gcc_name)
        .output()
        .map(|o| o.status.success())
        .unwrap_or(false)
}

/// 检查 rust target 是否已安装
pub fn check_rust_target(target: &CompileTarget) -> bool {
    Command::new("rustup")
        .args(["target", "list", "--installed"])
        .output()
        .map(|o| {
            let stdout = String::from_utf8_lossy(&o.stdout);
            stdout.contains(&target.rust_target)
        })
        .unwrap_or(false)
}

/// 安装 rust target
pub fn install_rust_target(target: &CompileTarget) -> Result<(), String> {
    let output = Command::new("rustup")
        .args(["target", "add", &target.rust_target])
        .output()
        .map_err(|e| format!("rustup 执行失败: {}", e))?;
    
    if output.status.success() {
        Ok(())
    } else {
        Err(format!("安装 target {} 失败: {}", 
            target.rust_target,
            String::from_utf8_lossy(&output.stderr)))
    }
}

/// 编译 Rust 项目
pub fn compile_rust(
    project_dir: &Path,
    target: &CompileTarget,
) -> Result<CompileResult, String> {
    // 检查是否有 Cargo.toml
    let cargo_toml = project_dir.join("Cargo.toml");
    if !cargo_toml.exists() {
        return Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: false,
            output_file: None,
            message: "未找到 Cargo.toml，跳过 Rust 编译".to_string(),
            compiled: false,
        });
    }

    // 确保 target 已安装
    if !check_rust_target(target) {
        install_rust_target(target)?;
    }

    // 检查交叉编译器
    if !check_cross_compiler(target) {
        return Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: false,
            output_file: None,
            message: format!("{} 交叉编译器未安装，降级为标记输出", target.arch),
            compiled: false,
        });
    }

    // 执行编译
    let output = Command::new("cargo")
        .current_dir(project_dir)
        .args(["build", "--release", "--target", &target.rust_target])
        .output()
        .map_err(|e| format!("cargo 执行失败: {}", e))?;

    if output.status.success() {
        // 查找编译产物
        let target_dir = project_dir.join("target").join(&target.rust_target).join("release");
        let possible_names = [
            format!("lib{}.so", project_dir.file_name()
                .map(|n| n.to_string_lossy().to_string())
                .unwrap_or_default()),
        ];

        let mut found = None;
        for name in &possible_names {
            let so_path = target_dir.join(name);
            if so_path.exists() {
                found = Some(so_path.to_string_lossy().to_string());
                break;
            }
        }

        // 如果没找到精确名称，搜索所有 .so
        if found.is_none() {
            if let Ok(entries) = std::fs::read_dir(&target_dir) {
                for entry in entries.flatten() {
                    let path = entry.path();
                    if path.extension().map_or(false, |e| e == "so") {
                        found = Some(path.to_string_lossy().to_string());
                        break;
                    }
                }
            }
        }

        Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: true,
            output_file: found,
            message: format!("{} 编译成功", target.chip_name),
            compiled: true,
        })
    } else {
        Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: false,
            output_file: None,
            message: format!("编译失败: {}", String::from_utf8_lossy(&output.stderr)),
            compiled: false,
        })
    }
}

/// 编译 C 项目
pub fn compile_c(
    source_path: &Path,
    target: &CompileTarget,
) -> Result<CompileResult, String> {
    let gcc = format!("{}-linux-gnu-gcc", target.arch);
    
    // 检查编译器
    if !Command::new("which").arg(&gcc).output()
        .map(|o| o.status.success()).unwrap_or(false) 
    {
        return Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: false,
            output_file: None,
            message: format!("{} 未安装，跳过 C 编译", gcc),
            compiled: false,
        });
    }

    let output_path = source_path.with_extension("o");
    let output = Command::new(&gcc)
        .arg("-o")
        .arg(&output_path)
        .arg(source_path)
        .output()
        .map_err(|e| format!("gcc 执行失败: {}", e))?;

    if output.status.success() {
        Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: true,
            output_file: Some(output_path.to_string_lossy().to_string()),
            message: format!("{} C 编译成功", target.chip_name),
            compiled: true,
        })
    } else {
        Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: false,
            output_file: None,
            message: format!("编译失败: {}", String::from_utf8_lossy(&output.stderr)),
            compiled: false,
        })
    }
}

/// 编译 Go 项目
pub fn compile_go(
    project_dir: &Path,
    target: &CompileTarget,
) -> Result<CompileResult, String> {
    let go_mod = project_dir.join("go.mod");
    if !go_mod.exists() {
        return Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: false,
            output_file: None,
            message: "未找到 go.mod，跳过 Go 编译".to_string(),
            compiled: false,
        });
    }

    let goarch = match target.arch.as_str() {
        "aarch64" => "arm64",
        "x86_64" => "amd64",
        "loongarch64" => "loong64",
        other => other,
    };

    let output = Command::new("go")
        .current_dir(project_dir)
        .env("GOOS", "linux")
        .env("GOARCH", goarch)
        .args(["build", "-o", &format!("app-{}", target.chip_name)])
        .output()
        .map_err(|e| format!("go build 失败: {}", e))?;

    if output.status.success() {
        Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: true,
            output_file: Some(format!("app-{}", target.chip_name)),
            message: format!("{} Go 编译成功", target.chip_name),
            compiled: true,
        })
    } else {
        Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: false,
            output_file: None,
            message: format!("编译失败: {}", String::from_utf8_lossy(&output.stderr)),
            compiled: false,
        })
    }
}

/// 主编译入口：按语言决定编译策略
pub fn compile(
    input: &Path,
    target: &CompileTarget,
    language: &str,
) -> Result<CompileResult, String> {
    match language {
        "Rust" => compile_rust(input, target),
        "C" | "C++" => {
            // C/C++ 编译单个文件或整个项目
            if input.is_dir() {
                // 尝试找 Makefile
                let makefile = input.join("Makefile");
                if makefile.exists() {
                    // 尝试 make cross
                    let output = Command::new("make")
                        .current_dir(input)
                        .env("CROSS_COMPILE", &format!("{}-linux-gnu-", target.arch))
                        .arg("cross")
                        .output();
                    
                    match output {
                        Ok(o) if o.status.success() => Ok(CompileResult {
                            chip: target.chip_name.clone(),
                            success: true,
                            output_file: None,
                            message: format!("{} make cross 编译成功", target.chip_name),
                            compiled: true,
                        }),
                        _ => Ok(CompileResult {
                            chip: target.chip_name.clone(),
                            success: false,
                            output_file: None,
                            message: format!("{} make cross 失败，降级标记", target.chip_name),
                            compiled: false,
                        }),
                    }
                } else {
                    compile_c(input, target)
                }
            } else {
                compile_c(input, target)
            }
        }
        "Go" => compile_go(input, target),
        "Python" | "JavaScript" | "TypeScript" | "Shell" | "Markdown" 
        | "YAML" | "TOML" | "JSON" | "HTML" | "CSS" | "ArkTS" => {
            // 解释型语言 / 标记语言 → 无需编译
            Ok(CompileResult {
                chip: target.chip_name.clone(),
                success: true,
                output_file: None,
                message: format!("{} 语言无需编译（解释型/标记型）", language),
                compiled: false,
            })
        }
        _ => Ok(CompileResult {
            chip: target.chip_name.clone(),
            success: false,
            output_file: None,
            message: format!("不支持的语言: {}", language),
            compiled: false,
        }),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_auto_target() {
        let target = CompileTarget::auto();
        assert_eq!(target.chip_name, "鲲鹏");
        assert_eq!(target.rust_target, "aarch64-unknown-linux-gnu");
    }

    #[test]
    fn test_check_rust_target() {
        // 至少确保不崩溃
        let target = CompileTarget::auto();
        let _ = check_rust_target(&target);
    }
}
