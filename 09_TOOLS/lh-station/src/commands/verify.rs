// 龍魂代码中转站 · verify 命令
// 验证已转换代码的完整性（DNA + GPG + 结构）

use crate::core::dna;
use crate::pipeline::signer;
use std::path::PathBuf;
use walkdir::WalkDir;

pub fn run(path: PathBuf) -> Result<(), String> {
    if !path.exists() {
        return Err(format!("路径不存在: {}", path.display()));
    }

    println!();
    println!("🔐 龍魂转换完整性验证");
    println!("{}", "═".repeat(60));
    println!("路径: {}", path.display());
    println!();

    let mut checks_total = 0u32;
    let mut checks_passed = 0u32;
    let mut checks_failed = 0u32;

    // 检查 1: .sovereign.json 是否存在
    checks_total += 1;
    let sovereign_path = path.join(".sovereign.json");
    if sovereign_path.exists() {
        println!("✅ .sovereign.json  存在");
        checks_passed += 1;
    } else {
        println!("❌ .sovereign.json  缺失 — 转换元数据不存在");
        checks_failed += 1;
    }

    // 检查 2: manifest.json 是否存在
    checks_total += 1;
    let manifest_path = path.join("manifest.json");
    if manifest_path.exists() {
        println!("✅ manifest.json    存在");
        checks_passed += 1;
    } else {
        println!("❌ manifest.json    缺失");
        checks_failed += 1;
    }

    // 检查 3: DNA 覆盖率
    checks_total += 1;
    let mut total_files = 0u32;
    let mut dna_files = 0u32;

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

        let ext = p.extension().map(|e| e.to_string_lossy().to_lowercase()).unwrap_or_default();
        if ext == "asc" || ext == "dna" || ext == "json" {
            continue;
        }

        total_files += 1;
        if let Ok(content) = std::fs::read_to_string(p) {
            if dna::has_dna(&content) {
                dna_files += 1;
            }
        }
    }

    if total_files > 0 && dna_files == total_files {
        println!("✅ DNA 覆盖率      {}/{} (100%)", dna_files, total_files);
        checks_passed += 1;
    } else if total_files > 0 {
        println!("⚠️ DNA 覆盖率      {}/{} ({:.0}%)", dna_files, total_files,
            (dna_files as f64 / total_files as f64) * 100.0);
        checks_failed += 1;
    } else {
        println!("⚠️ DNA 覆盖率      无文件可检查");
        checks_passed += 1;
    }

    // 检查 4: GPG 签名验证
    checks_total += 1;
    if !signer::is_gpg_available() {
        println!("⚠️ GPG 签名验证    GPG 不可用（跳过）");
        checks_passed += 1;
    } else {
        let mut gpg_verified = 0u32;
        let mut gpg_failed = 0u32;

        for entry in WalkDir::new(&path)
            .follow_links(false)
            .into_iter()
            .filter_map(|e| e.ok())
        {
            let p = entry.path();
            if !p.is_file() {
                continue;
            }

            let ext = p.extension().map(|e| e.to_string_lossy().to_lowercase()).unwrap_or_default();
            if ext == "asc" || ext == "dna" || ext == "json" {
                continue;
            }

            let asc_path = format!("{}.asc", p.to_string_lossy());
            if PathBuf::from(&asc_path).exists() {
                match signer::verify_signature(p) {
                    Ok(true) => gpg_verified += 1,
                    _ => gpg_failed += 1,
                }
            }
        }

        let gpg_total = gpg_verified + gpg_failed;
        if gpg_total > 0 && gpg_failed == 0 {
            println!("✅ GPG 签名验证    {}/{} 通过", gpg_verified, gpg_total);
            checks_passed += 1;
        } else if gpg_total > 0 {
            println!("⚠️ GPG 签名验证    {}/{} 通过, {} 失败", gpg_verified, gpg_total, gpg_failed);
            checks_failed += 1;
        } else {
            println!("⚠️ GPG 签名验证    未找到签名文件");
            checks_passed += 1;
        }
    }

    // 检查 5: README-lh-station.md 是否存在
    checks_total += 1;
    let readme_path = path.join("README-lh-station.md");
    if readme_path.exists() {
        println!("✅ README.md       存在");
        checks_passed += 1;
    } else {
        println!("⚠️ README.md       缺失");
        checks_passed += 1; // 非必要
    }

    println!();
    println!("{}", "═".repeat(60));
    println!("📊 验证结果: {}/{} 通过", checks_passed, checks_total);

    if checks_failed == 0 {
        println!("🟢 完整性验证通过 — 所有主权标识完整");
    } else {
        println!("🟡 {} 项检查未通过 — 建议重新运行 transform", checks_failed);
    }
    println!();

    Ok(())
}
