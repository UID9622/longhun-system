// 龍魂代码中转站 · transform 命令
// 全管道: 检测→注入→编译→审查→成本分析→签名→打包→归档
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-TRANSFORM-CMD-v1.1

use crate::pipeline::detector;
use crate::pipeline::injector;
use crate::pipeline::compiler::{self, CompileTarget};
use crate::pipeline::security;
use crate::pipeline::cost_analyzer;
use crate::pipeline::signer;
use crate::pipeline::packer;
use crate::pipeline::seal;
use crate::core::config::StationConfig;
use std::path::{Path, PathBuf};
use std::io::Write;

pub fn run(
    input: PathBuf,
    output: PathBuf,
    chip: String,
    cross: bool,
    no_sign: bool,
) -> Result<(), String> {
    let config = StationConfig::default();

    println!();
    println!("🐉 龍魂代码中转站 v{}", config.station_version);
    println!("{}", "═".repeat(50));

    // ═══ Step 1: 检测 ═══
    print!("🔍 检测中... ");
    std::io::stdout().flush().unwrap();
    
    let code_input = detector::detect(&input)?;
    
    let framework_str = code_input.framework.as_deref().unwrap_or("无框架");
    println!("{} · {} · {}", code_input.language, framework_str, code_input.platform);
    println!("   共 {} 个文件 · Docker: {} · CI: {}", 
        code_input.file_count,
        if code_input.has_docker { "✓" } else { "✗" },
        if code_input.has_ci { "✓" } else { "✗" },
    );

    // ═══ Step 2: 主权注入 ═══
    println!("💉 注入主权头...");

    let mut total_files = 0u32;
    let mut injected_count = 0u32;

    for detected_file in &code_input.files {
        if detected_file.is_binary {
            // 二进制跳过（后续在 copier 中处理）
            total_files += 1;
            continue;
        }

        let rel_path = &detected_file.path;
        let input_path = input.join(rel_path);
        let output_path = output.join(rel_path);

        match injector::inject_file(&input_path, &output_path, &code_input.platform) {
            Ok(result) => {
                if result.injected {
                    injected_count += 1;
                    println!("   ✓ {}", rel_path);
                }
                total_files += 1;
            }
            Err(e) => {
                eprintln!("   ✗ {} — {}", rel_path, e);
            }
        }
    }

    // ═══ Step 3: 芯片适配编译 ═══
    let target = if chip == "auto" {
        CompileTarget::auto()
    } else if let Some(info) = config.find_chip(&chip) {
        CompileTarget::from_chip_info(info)
    } else {
        CompileTarget::auto()
    };

    println!("🔧 编译目标: {} ({})", target.chip_name, target.rust_target);

    let compile_result = if cross {
        compiler::compile(&input, &target, &code_input.language)?
    } else {
        compiler::CompileResult {
            chip: target.chip_name.clone(),
            success: true,
            output_file: None,
            message: "跳过编译（--cross=false）".to_string(),
            compiled: false,
        }
    };

    println!("   结果: {}", compile_result.message);
    if let Some(ref so_path) = compile_result.output_file {
        // 复制 .so 到输出目录的 libs/
        let libs_dir = output.join("libs").join(&target.arch);
        std::fs::create_dir_all(&libs_dir).map_err(|e| format!("创建 libs 目录失败: {}", e))?;
        
        let so_name = Path::new(so_path).file_name()
            .map(|n| n.to_string_lossy().to_string())
            .unwrap_or_else(|| "liboutput.so".to_string());
        let dest = libs_dir.join(&so_name);
        std::fs::copy(so_path, &dest).map_err(|e| format!("复制 .so 失败: {}", e))?;
        println!("   → {}", dest.display());
    }

    let compiled_count = if compile_result.compiled { 1u32 } else { 0u32 };

    // ═══ Step 4: 安全审查 ═══
    println!("🛡️ 安全审查...");
    let sec_report = security::audit(&input)?;
    
    let status_icon = if sec_report.passed { "🟢" } else { "🔴" };
    let violations_count = sec_report.violations.len();
    println!("   {} {}", status_icon, sec_report.summary);
    
    for v in &sec_report.violations {
        println!("     {} [{}] {} — {}", v.severity, v.file, v.rule, v.detail);
    }

    // ═══ Step 5: API 成本分析（钩子1） ═══
    println!("💰 API 成本分析...");
    let cost_report = match cost_analyzer::analyze(&input, &output) {
        Ok(report) => {
            let risk_icon = match report.data_sovereign_risk.as_str() {
                "🟢 Low" => "🟢",
                "🟡 Medium" => "🟡",
                "🔴 High" => "🔴",
                "⚫ Critical" => "⚫",
                _ => "🟡",
            };
            println!("   {} 检测到 {} 个 API · 预估月成本 ¥{:.2} · 主权风险: {}",
                risk_icon,
                report.total_apis_detected,
                report.estimated_monthly_cny,
                report.data_sovereign_risk,
            );
            
            if report.data_sovereign_risk.contains("Critical") {
                eprintln!("⚫ 严重警告: 检测到大量跨境API调用，数据主权面临严重风险！");
            } else if report.data_sovereign_risk.contains("High") {
                eprintln!("🔴 警告: 存在跨境API调用，数据主权有风险");
            }
            
            for rec in &report.recommendations {
                println!("     {}", rec);
            }
            Some(report)
        }
        Err(e) => {
            eprintln!("   ⚠️ 成本分析失败（不阻塞管道）: {}", e);
            None
        }
    };

    let cost_monthly = cost_report.as_ref().map(|r| r.estimated_monthly_cny);
    let cost_daily = cost_report.as_ref().map(|r| r.estimated_daily_cny);
    let cost_risk = cost_report.as_ref().map(|r| r.data_sovereign_risk.clone());
    let cross_border_count = cost_report.as_ref().map(|r| r.cross_border_apis.len() as u32);

    // ═══ Step 6: GPG 签名 ═══
    let signed_count = if no_sign {
        println!("🔏 GPG 签名: 跳过（--no-sign）");
        0u32
    } else {
        println!("🔏 GPG 签名...");
        let sign_results = signer::sign_directory(&output, true)?;
        let mut sc = 0u32;
        for sr in &sign_results {
            if sr.signed {
                sc += 1;
            }
        }
        println!("   已签名: {} / {} 文件", sc, sign_results.len());
        sc
    };

    // ═══ Step 7: 生成元数据文件 ═══
    println!("📦 生成元数据文件...");
    
    let sovereign_json = packer::generate_sovereign_json(
        &code_input.path,
        &code_input.language,
        &code_input.platform,
        &target.chip_name,
        total_files,
    );

    let mut manifest = packer::generate_manifest(
        &code_input.path,
        &code_input.language,
        code_input.framework.as_deref(),
        &code_input.platform,
        &target.chip_name,
        total_files,
        injected_count,
        compiled_count,
        signed_count,
        sec_report.passed,
        sec_report.verdict.r_score,
    );

    // 注入成本分析字段
    manifest.cost_monthly_cny = cost_monthly;
    manifest.cost_daily_cny = cost_daily;
    manifest.data_sovereign_risk = cost_risk.clone();
    manifest.cross_border_api_count = cross_border_count;

    packer::write_output_files(&output, &sovereign_json, &manifest)?;

    // ═══ Step 8: 记忆封印（钩子2） ═══
    println!("🧬 记忆封印...");
    let transform_time = sovereign_json.transformed_at.clone();
    match seal::seal(
        &manifest.dna,
        &config.station_version,
        &transform_time,
        &code_input.path,
        &code_input.language,
        &target.chip_name,
        total_files,
        injected_count,
        compiled_count,
        signed_count,
        sec_report.passed,
        violations_count as u32,
        Some(sec_report.verdict.r_score),
        cost_monthly,
        cost_risk.clone(),
        cross_border_count,
        &output,
    ) {
        Ok(seal_record) => {
            println!("   ✅ {} -> ~/.longhun/memory/seals/", seal_record.dna);
        }
        Err(e) => {
            if e.contains("已归档") {
                println!("   ⏭️ {} (幂等跳过)", manifest.dna);
            } else {
                eprintln!("   ⚠️ WARNING: 封印写入失败（不阻塞管道）: {}", e);
            }
        }
    }

    // ═══ 完成 ═══
    println!("{}", "═".repeat(50));
    println!("📂 输出: {}", output.display());
    println!("   ├── <原目录结构>    ← 原代码 + 主权头（100% 兼容原平台）");
    if compile_result.compiled {
        println!("   ├── libs/{}/        ← 编译产物", target.arch);
    }
    println!("   ├── .sovereign.json  ← 主权元数据");
    println!("   ├── manifest.json     ← 转换清单");
    if cost_report.is_some() {
        println!("   ├── .cost-report.json ← API成本分析");
    }
    println!("   ├── .seal-record.json ← 封印记录");
    println!("   └── README-lh-station.md");
    println!();
    println!("🧬 DNA: {}", manifest.dna);
    println!("📊 主权状态: {} {} 通过 · {} 注入 · {} 编译 · {} 签名 · 三色审计 R={}/95 ({})",
        status_icon,
        if sec_report.passed { "" } else { " (有阻断项)" },
        injected_count,
        compiled_count,
        signed_count,
        sec_report.verdict.r_score,
        sec_report.verdict.status_code,
    );
    if let Some(c) = cost_monthly {
        println!("💰 预估月API成本: ¥{:.2}", c);
    }

    Ok(())
}
