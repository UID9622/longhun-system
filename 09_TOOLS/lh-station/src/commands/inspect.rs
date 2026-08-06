// 龍魂代码中转站 · inspect 命令
// 检查代码主权状态

use crate::core::dna;
use std::path::PathBuf;
use walkdir::WalkDir;

pub fn run(path: PathBuf) -> Result<(), String> {
    if !path.exists() {
        return Err(format!("路径不存在: {}", path.display()));
    }

    println!();
    println!("🔍 龍魂主权状态检查");
    println!("{}", "═".repeat(60));
    println!("路径: {}", path.display());
    println!();

    let mut total_files = 0u32;
    let mut has_sovereign = 0u32;
    let mut has_gpg_sign = 0u32;
    let mut has_dna_mark = 0u32;
    let mut unknown_files = 0u32;

    let mut files_with_dna: Vec<String> = Vec::new();
    let mut files_without_dna: Vec<String> = Vec::new();

    for entry in WalkDir::new(&path)
        .follow_links(false)
        .into_iter()
        .filter_map(|e| e.ok())
    {
        let p = entry.path();
        if !p.is_file() {
            continue;
        }

        let path_str = p.to_string_lossy();
        if path_str.contains("/.")
            || path_str.contains("target/")
            || path_str.contains("node_modules/")
        {
            continue;
        }

        // 跳过 .asc 和主权元数据文件
        let ext = p.extension().map(|e| e.to_string_lossy().to_lowercase()).unwrap_or_default();
        if ext == "asc" || ext == "dna" {
            if ext == "asc" {
                has_gpg_sign += 1;
            }
            continue;
        }

        total_files += 1;

        if let Ok(content) = std::fs::read_to_string(p) {
            if dna::has_dna(&content) {
                has_dna_mark += 1;
                let rel = p.strip_prefix(&path).unwrap_or(p).to_string_lossy().to_string();
                files_with_dna.push(rel);
            } else {
                let rel = p.strip_prefix(&path).unwrap_or(p).to_string_lossy().to_string();
                files_without_dna.push(rel);
            }
        } else {
            unknown_files += 1;
        }
    }

    // 检查是否有 .sovereign.json
    let sovereign_path = path.join(".sovereign.json");
    if sovereign_path.exists() {
        has_sovereign += 1;
        if let Ok(content) = std::fs::read_to_string(&sovereign_path) {
            if let Ok(sj) = serde_json::from_str::<serde_json::Value>(&content) {
                println!("📋 主权元数据: 已找到");
                if let Some(dna_val) = sj.get("dna") {
                    println!("   DNA: {}", dna_val.as_str().unwrap_or("?"));
                }
                if let Some(date) = sj.get("transformed_at") {
                    println!("   转换时间: {}", date.as_str().unwrap_or("?"));
                }
                if let Some(platform) = sj.get("platform") {
                    println!("   原始平台: {}", platform.as_str().unwrap_or("?"));
                }
            }
        }
    } else {
        println!("📋 主权元数据: 未找到 (无 .sovereign.json)");
    }

    println!();
    println!("📊 统计:");
    println!("   总文件: {}", total_files);
    println!("   有龍魂 DNA: {} ({:.0}%)", has_dna_mark, 
        if total_files > 0 { (has_dna_mark as f64 / total_files as f64) * 100.0 } else { 0.0 });
    println!("   无龍魂 DNA: {}", files_without_dna.len());
    println!("   GPG 签名文件: {}", has_gpg_sign);
    println!("   主权元数据: {} ({} .sovereign.json)", 
        if has_sovereign > 0 { "有" } else { "无" }, has_sovereign);

    if !files_without_dna.is_empty() {
        println!();
        println!("⚠️ 无主权标识的文件 ({} 个):", files_without_dna.len());
        for f in &files_without_dna[..files_without_dna.len().min(20)] {
            println!("   • {}", f);
        }
        if files_without_dna.len() > 20 {
            println!("   ... 还有 {} 个文件", files_without_dna.len() - 20);
        }
        println!();
        println!("💡 运行 'lh-station transform {}' 注入主权标识", path.display());
    }

    if has_dna_mark == total_files && has_sovereign > 0 {
        println!();
        println!("🟢 主权状态: 完整 — 所有文件已标识");
    } else if has_dna_mark > 0 {
        println!();
        println!("🟡 主权状态: 部分 — {}/{} 文件已标识", has_dna_mark, total_files);
    } else {
        println!();
        println!("🔴 主权状态: 未标识 — 建议运行 transform");
    }

    println!();
    Ok(())
}
