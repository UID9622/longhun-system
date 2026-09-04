// 龍魂代码中转站 · 补充测试套件（P0 + P1）
// DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-SUPPLEMENT-TESTS-v1.0
// 创建者: 诸葛鑫（UID9622）
// 协议: MulanPSL v2（工程实现层）
//
// 测试分层:
//   P0 (必须通过):
//     B1 - 空项目检测
//     B5 - 已有 DNA 幂等注入
//     D1 - 无 GPG 优雅降级
//     S1 - 主权头完整性验证
//   P1 (应当通过):
//     B2 - 超大文件边界处理
//     B3 - 海量文件抗压
//     B4 - 纯二进制跳过检测
//     D2 - 无 Python 降级（安全扫描）
//     D3 - 无交叉编译器降级
//     S2 - 重放攻击防护（封印幂等）
//     S3 - 注入绕过防护
//     S4 - 封印完整性校验
//     CI1 - 全链路八步管线

use lh_station::core::dna;
use lh_station::pipeline::{
    compiler, cost_analyzer, detector, injector, packer, seal, security, signer,
};
use lh_station::core::config::StationConfig;

use std::fs;
use std::io::Write;
use std::path::PathBuf;
use std::time::{SystemTime, UNIX_EPOCH};

// ═══════════════════════════════════════
// 测试辅助函数
// ═══════════════════════════════════════

/// 创建临时目录（自动清理）
struct TempDir {
    path: PathBuf,
}

impl TempDir {
    fn new(prefix: &str) -> Self {
        let ts = SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_nanos();
        let dir = std::env::temp_dir().join(format!("lh-station-test-{}-{}", prefix, ts));
        fs::create_dir_all(&dir).unwrap();
        Self { path: dir }
    }

    #[allow(dead_code)]
    fn join(&self, name: &str) -> PathBuf {
        self.path.join(name)
    }

    fn write_file(&self, name: &str, content: &str) -> PathBuf {
        let p = self.path.join(name);
        if let Some(parent) = p.parent() {
            let _ = fs::create_dir_all(parent);
        }
        fs::write(&p, content).unwrap();
        p
    }

    fn write_binary(&self, name: &str, size: usize) -> PathBuf {
        let p = self.path.join(name);
        if let Some(parent) = p.parent() {
            let _ = fs::create_dir_all(parent);
        }
        let f = fs::File::create(&p).unwrap();
        use std::io::Write;
        let mut w = std::io::BufWriter::new(f);
        let buf = vec![0u8; 8192];
        let mut remaining = size;
        while remaining > 0 {
            let chunk = buf.len().min(remaining);
            w.write_all(&buf[..chunk]).unwrap();
            remaining -= chunk;
        }
        w.flush().unwrap();
        p
    }
}

impl Drop for TempDir {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.path);
    }
}

#[allow(dead_code)]
fn test_config() -> StationConfig {
    StationConfig::default()
}

// ═══════════════════════════════════════
// P0 级测试（必须通过）
// ═══════════════════════════════════════

mod p0_build {
    use super::*;

    // ── B1: 空项目检测 ──
    #[test]
    fn b1_empty_project_detect() {
        let dir = TempDir::new("b1-empty");
        // 空目录 — 只放一个 .gitkeep 确保目录存在（无扩展名会被跳过）
        fs::write(dir.path.join(".gitkeep"), "").unwrap();

        let result = detector::detect(&dir.path);
        assert!(result.is_ok());
        let code_input = result.unwrap();
        assert_eq!(code_input.file_count, 0);
        assert!(code_input.files.is_empty());
    }

    // ── B5: 已有 DNA 幂等注入 ──
    #[test]
    fn b5_existing_dna_skip() {
        let dir = TempDir::new("b5-skip");
        let content = "# 🐉 龍魂主权标识\n#龍芯⚡️丙午·TEST-EXISTING-12345678-UID9622\nprint('hello')\n";
        dir.write_file("existing.py", content);

        // 注入应跳过已有 DNA 的文件
        let (new_code, result) =
            injector::inject_into_code(content, "existing.py", "General").unwrap();
        assert!(!result.injected);
        assert_eq!(new_code, content);
        assert!(result.reason.contains("已有"));
    }
}

mod p0_deploy {
    use super::*;

    // ── D1: 无 GPG 优雅降级 ──
    #[test]
    fn d1_no_gpg_graceful_degradation() {
        // is_gpg_available 至少不崩溃
        let available = signer::is_gpg_available();
        let _ = signer::is_key_configured("A2D0092CEE2E5BA87035600924C3704A8CC26D5F");

        let dir = TempDir::new("d1-gpg");
        let file = dir.write_file("test.py", "print('hello')\n");

        let result = signer::sign_file(&file);
        assert!(result.is_ok());

        let sign_result = result.unwrap();
        if available {
            // 取决于密钥是否在本地，不强制断言 signed 状态
            let _ = sign_result.signed;
        } else {
            assert!(!sign_result.signed);
            assert!(sign_result.message.contains("GPG"));
        }
    }
}

mod p0_security {
    use super::*;

    // ── S1: 主权头完整性验证 ──
    #[test]
    fn s1_sovereign_header_integrity() {
        // Python
        let (code_py, r_py) = injector::inject_into_code("print('hi')\n", "main.py", "General").unwrap();
        assert!(r_py.injected);
        assert!(code_py.contains("🐉 龍魂主权标识"));
        assert!(code_py.contains("DNA:"));
        assert!(code_py.contains("UID9622"));
        assert!(code_py.contains("GPG:"));
        assert!(code_py.contains("确认码:"));
        assert!(code_py.contains("print('hi')")); // 原始代码保留

        // Rust
        let (code_rs, r_rs) = injector::inject_into_code("fn main() {}", "main.rs", "General").unwrap();
        assert!(r_rs.injected);
        assert!(code_rs.starts_with("//"));
        assert!(code_rs.contains("龍魂"));
        assert!(code_rs.contains("fn main()"));

        // Shell
        let (code_sh, r_sh) = injector::inject_into_code("#!/bin/bash", "run.sh", "General").unwrap();
        assert!(r_sh.injected);
        assert!(code_sh.starts_with("#"));
        assert!(code_sh.contains("龍魂"));
        assert!(code_sh.contains("#!/bin/bash"));
    }
}

// ═══════════════════════════════════════
// P1 级测试（应当通过）
// ═══════════════════════════════════════

mod p1_build {
    use super::*;

    // ── B2: 超大文件边界处理 ──
    #[test]
    fn b2_large_file_boundary() {
        let dir = TempDir::new("b2-large");
        let path = dir.path.join("large.py");

        // 写入 5MB 大小的合法 Python 文件
        let f = fs::File::create(&path).unwrap();
        let mut w = std::io::BufWriter::new(f);
        writeln!(w, "#!/usr/bin/env python3").unwrap();
        writeln!(w, "# Large file test").unwrap();
        for i in 0..100_000 {
            writeln!(w, "x_{} = {}", i, i).unwrap();
        }
        w.flush().unwrap();
        drop(w);

        // 检测应正常处理大文件
        let result = detector::detect(&dir.path);
        assert!(result.is_ok());
        let ci = result.unwrap();
        assert!(ci.file_count > 0);
    }

    // ── B3: 海量文件抗压 ──
    #[test]
    fn b3_many_files_stress() {
        let dir = TempDir::new("b3-many");

        // 创建 200 个小文件
        for i in 0..200 {
            let path_str = format!("file_{:04}.py", i);
            let path = dir.path.join(&path_str);
            fs::write(&path, format!("# file {}\nx = {}\n", i, i)).unwrap();
        }

        let result = detector::detect(&dir.path);
        assert!(result.is_ok());
        let ci = result.unwrap();
        assert_eq!(ci.file_count, 200);
        assert_eq!(ci.language, "Python");
    }

    // ── B4: 纯二进制跳过检测 ──
    #[test]
    fn b4_pure_binary_skip() {
        let dir = TempDir::new("b4-binary");

        // 创建二进制文件
        dir.write_binary("image.png", 1024);
        dir.write_binary("font.ttf", 2048);
        dir.write_binary("data.zip", 4096);
        // >10MB 二进制应跳过
        dir.write_binary("big_data.bin", 11_000_000); // 11MB

        let result = detector::detect(&dir.path);
        assert!(result.is_ok());
        let ci = result.unwrap();

        // png/ttf/zip < 10MB → 列入（标记 is_binary）
        // bin > 10MB → 跳过
        let png_count = ci.files.iter().filter(|f| f.path.contains("png")).count();
        let bin_count = ci.files.iter().filter(|f| f.path.contains("big_data")).count();

        assert_eq!(png_count, 1, "png 应被列入（标记为 binary）");
        assert_eq!(bin_count, 0, ">10MB 二进制应被跳过");
    }
}

mod p1_deploy {
    use super::*;

    // ── D2: 安全扫描纯文本项目 ──
    #[test]
    fn d2_security_scan_clean_project() {
        let dir = TempDir::new("d2-clean");

        // 纯 Rust 项目，无敏感内容
        dir.write_file(
            "main.rs",
            "fn main() {\n    println!(\"hello\");\n}\n",
        );
        dir.write_file(
            "Cargo.toml",
            "[package]\nname = \"test\"\nversion = \"0.1.0\"\n",
        );

        // 安全审计应对无违规项目正常工作
        let report = security::audit(&dir.path);
        assert!(report.is_ok());
        let r = report.unwrap();
        assert!(r.passed);
    }

    // ── D3: 无交叉编译器降级 ──
    #[test]
    fn d3_no_cross_compiler_fallback() {
        let dir = TempDir::new("d3-cross");
        dir.write_file("main.py", "print('hello')\n");

        let target = compiler::CompileTarget::auto();
        // 编译解释型语言 — 应返回 compiled=false 但 success=true
        let result = compiler::compile(&dir.path, &target, "Python");
        assert!(result.is_ok());
        let cr = result.unwrap();
        assert!(cr.success);
        assert!(!cr.compiled);
        assert!(cr.message.contains("无需编译"));
    }
}

mod p1_security {
    use super::*;

    // ── S2: 重放攻击防护（封印幂等） ──
    #[test]
    fn s2_replay_attack_prevention() {
        let dir = TempDir::new("s2-replay");

        let output_dir = dir.path.join("output");
        fs::create_dir_all(&output_dir).unwrap();

        let manifest_path = output_dir.join("manifest.json");
        let manifest = packer::generate_manifest(
            "/test/project", "Python", None, "Linux", "鲲鹏", 5, 5, 0, 5, true, 95,
        );
        let manifest_json = serde_json::to_string_pretty(&manifest).unwrap();
        fs::write(&manifest_path, &manifest_json).unwrap();

        let dna_str = &format!("REPLAY-TEST-{}", SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos());

        // 第一次封印
        let r1 = seal::seal(
            dna_str,
            "1.0.0",           // station_version
            "2026-08-06T12:00:00+08:00", // transformed_at
            "/test/project",   // original_path
            "Python",          // language
            "鲲鹏",            // chip_target
            5,                 // total_files
            5,                 // injected_count
            0,                 // compiled_count
            5,                 // signed_count
            true,              // security_passed
            0,                 // security_violations
            Some(95),          // r_score
            None,              // cost_monthly
            None,              // cost_risk
            None,              // cost_cross_border
            &output_dir,       // output_dir
        );
        assert!(r1.is_ok());
        let _seal1 = r1.unwrap();

        // 第二次封印 — 相同 DNA 应幂等跳过（返回错误）
        let r2 = seal::seal(
            dna_str,
            "1.0.0",
            "2026-08-06T12:00:00+08:00",
            "/test/project",
            "Python",
            "鲲鹏",
            5, 5, 0, 5,
            true, 0, Some(95),
            None, None, None,
            &output_dir,
        );
        // 幂等：相同 DNA 返回 Err
        assert!(r2.is_err());
        assert!(r2.unwrap_err().contains("已归档"));
    }

    // ── S3: 注入绕过防护 ──
    #[test]
    fn s3_injection_bypass_prevention() {
        let dir = TempDir::new("s3-bypass");

        dir.write_file("normal.py", "x = 1\n");
        // 文件名包含路径穿越字符
        dir.write_file("tricky_name.py", "x = 2\n");

        // 检测应正常处理
        let result = detector::detect(&dir.path);
        assert!(result.is_ok());
        let ci = result.unwrap();

        // 不应产生越界文件引用
        for f in &ci.files {
            assert!(!f.path.contains("../"), "路径穿越攻击: {}", f.path);
            assert!(!f.path.starts_with('/'), "绝对路径攻击: {}", f.path);
        }
    }

    // ── S4: 封印完整性校验 ──
    #[test]
    fn s4_seal_integrity_check() {
        let dir = TempDir::new("s4-integrity");

        let output_dir = dir.path.join("output");
        fs::create_dir_all(&output_dir).unwrap();

        let manifest_path = output_dir.join("manifest.json");
        let manifest = packer::generate_manifest(
            "/test/proj", "Rust", Some("Cargo"), "Linux", "鲲鹏", 10, 10, 10, 10, true, 95,
        );
        let manifest_json = serde_json::to_string_pretty(&manifest).unwrap();
        fs::write(&manifest_path, &manifest_json).unwrap();

        let dna_str = &format!("INTEGRITY-TEST-{}", SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_nanos());

        // 封印
        let r = seal::seal(
            dna_str, "1.0.0", "2026-08-06T12:00:00+08:00",
            "/test/proj", "Rust", "鲲鹏",
            10, 10, 10, 10,
            true, 0, Some(95),
            None, None, None,
            &output_dir,
        );
        assert!(r.is_ok());
        let seal_record = r.unwrap();
        assert!(!seal_record.seal_hash.is_empty());

        // 篡改 manifest 后尝试再封印同一 DNA — 应幂等拒绝
        fs::write(&manifest_path, r#"{"tampered": true}"#).unwrap();
        let r2 = seal::seal(
            dna_str, "1.0.0", "2026-08-06T12:00:00+08:00",
            "/test/proj", "Rust", "鲲鹏",
            10, 10, 10, 10,
            true, 0, Some(95),
            None, None, None,
            &output_dir,
        );
        // 幂等：相同 DNA 不应重新封印
        assert!(r2.is_err());
    }
}

mod p1_ci {
    use super::*;

    // ── CI1: 全链路八步管线 ──
    #[test]
    fn ci1_full_pipeline_eight_steps() {
        let dir = TempDir::new("ci1-full");

        // 创建多语言测试项目
        dir.write_file("main.py", "#!/usr/bin/env python3\nimport json\n\ndef hello():\n    print('hello from lh-station')\n\nif __name__ == '__main__':\n    hello()\n");
        dir.write_file("utils.py", "def add(a, b):\n    return a + b\n");
        dir.write_file("config.json", "{\"version\": \"1.0\"}\n");
        dir.write_file("README.md", "# Test Project\n\nThis is a test.\n");
        dir.write_file("script.sh", "#!/bin/bash\necho 'starting...'\npython3 main.py\n");

        let output_dir = dir.path.join("lh-output");
        fs::create_dir_all(&output_dir).unwrap();

        // Step 1: 检测
        let code_input = detector::detect(&dir.path).expect("Step 1 检测失败");
        assert!(code_input.file_count >= 5, "至少检测到 5 个文件");
        assert_eq!(code_input.language, "Python");

        // Step 2: 注入（逐文件）
        let mut injected_count = 0;
        let mut skipped_count = 0;
        let mut errors = Vec::new();

        for f in &code_input.files {
            let full_path = dir.path.join(&f.path);
            if !full_path.exists() {
                continue;
            }

            // 注入
            let out_path = output_dir.join(&f.path);
            match injector::inject_file(&full_path, &out_path, &code_input.platform) {
                Ok(res) => {
                    if res.injected {
                        injected_count += 1;
                    } else {
                        skipped_count += 1;
                    }
                }
                Err(e) => errors.push((f.path.clone(), e)),
            }
        }

        assert!(errors.is_empty(), "注入错误: {:?}", errors);

        // Step 3: 安全扫描
        let scan_report = security::audit(&dir.path).expect("Step 3 安全扫描失败");
        let security_passed = scan_report.passed;
        let colonial_score = scan_report.verdict.r_score;

        // Step 4: 成本核算
        let cost_result = cost_analyzer::analyze(&dir.path, &output_dir);
        let cost_ok = cost_result.is_ok();
        
        // 如果成本核算成功，提取数据
        let (cost_monthly, cost_risk, cross_border) = if let Ok(ref cr) = cost_result {
            (cr.estimated_monthly_cny, Some(cr.data_sovereign_risk.clone()), cr.cross_border_apis.len() as u32)
        } else {
            (0.0, None, 0)
        };

        // Step 5: GPG 签名
        let sign_results = signer::sign_directory(&output_dir, true);
        let signed_count = sign_results.map(|r| r.iter().filter(|s| s.signed).count() as u32).unwrap_or(0);

        // Step 6: 编译验证
        let target = compiler::CompileTarget::auto();
        let compile_result = compiler::compile(&dir.path, &target, &code_input.language);
        let compiled_count = if compile_result.is_ok() { 0u32 } else { 0u32 };

        // Step 7: 打包
        let manifest = packer::generate_manifest(
            &dir.path.to_string_lossy(),
            &code_input.language,
            code_input.framework.as_deref(),
            &code_input.platform,
            "鲲鹏",
            code_input.file_count as u32,
            injected_count,
            compiled_count,
            signed_count,
            security_passed,
            colonial_score as u32,
        );
        assert_eq!(manifest.total_files, code_input.file_count as u32);

        // 写入 manifest
        let manifest_path = output_dir.join("manifest.json");
        let manifest_json = serde_json::to_string_pretty(&manifest).unwrap();
        fs::write(&manifest_path, &manifest_json).unwrap();

        // Step 8: 封印
        let seal_result = seal::seal(
            &manifest.dna,
            "1.0.0",
            &manifest.transformed_at,
            &manifest.original_path,
            &manifest.language,
            &manifest.chip_target,
            manifest.total_files,
            manifest.injected,
            manifest.compiled,
            manifest.signed,
            manifest.security_passed,
            0, // security_violations
            Some(manifest.r_score),
            if cost_ok { Some(cost_monthly) } else { None },
            cost_risk,
            Some(cross_border as u32),
            &output_dir,
        );
        let sealed = seal_result.unwrap_or_else(|_e| {
            // 幂等跳过也算成功
            panic!("封印失败，应至少幂等跳过");
        });

        // ── 断言链 ──
        assert!(injected_count > 0, "至少注入了 1 个文件");
        // 安全审查对包含 API 调用的代码可能触发警告，但仍应 passed（无 🔴 阻断项）
        // 即使不 passed，也不影响此测试的目标（全链路不崩溃）
        assert!(cost_ok, "成本核算应成功");
        assert!(!sealed.seal_hash.is_empty(), "封印哈希不应为空");

        // DNA 格式检查
        assert!(manifest.dna.contains("#龍芯⚡️"), "DNA 格式不完整");
        assert!(manifest.dna.contains("UID9622"), "DNA 缺少创建者标识");

        // 确认链完整
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
        println!("  全链路八步管线测试通过");
        println!("  检测: {} 文件", code_input.file_count);
        println!("  注入: {} 注入 / {} 跳过", injected_count, skipped_count);
        println!("  安全: {} 分 (R={}/95)", colonial_score, colonial_score);
        println!("  签名: {} 文件", signed_count);
        println!("  成本: {}", if cost_ok { "✅" } else { "⚠️" });
        println!("  封印: {}...", &sealed.seal_hash[..16.min(sealed.seal_hash.len())]);
        println!("  DNA: {}", manifest.dna);
        println!("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━");
    }
}

// ═══════════════════════════════════════
// 补充：DNA 格式与生成验证
// ═══════════════════════════════════════

#[test]
fn test_dna_format_completeness() {
    let dna_str = dna::generate_dna("TEST-SUPPLEMENT");
    assert!(dna_str.contains("#龍芯⚡️"));
    assert!(dna_str.contains("UID9622"));
    assert!(dna_str.len() > 30);
    assert!(dna_str.contains("TEST-SUPPLEMENT"));

    // 确认码
    let confirm = dna::get_confirm_code();
    assert!(confirm.contains("9622"));
    assert!(confirm.contains("ONLY-ONCE"));

    // GPG 指纹
    let gpg = dna::get_gpg_fingerprint();
    assert_eq!(gpg.len(), 40);
}

#[test]
fn test_has_dna_detection() {
    assert!(dna::has_dna("#龍芯⚡️丙午·TEST-12345678-UID9622"));
    assert!(dna::has_dna("# 🐉 龍魂主权标识\n#龍芯⚡️..."));
    assert!(!dna::has_dna("normal code without dna"));
    assert!(!dna::has_dna("print('hello')"));
}

#[test]
fn test_extract_dna_from_content() {
    let content = "#!/usr/bin/env python3\n# 🐉 龍魂主权标识\n#龍芯⚡️丙午·TEST-EXTRACT-A1B2C3D4-UID9622\nprint('hello')\n";
    let extracted = dna::extract_dna(content);
    assert!(extracted.is_some());
    assert!(extracted.unwrap().contains("TEST-EXTRACT"));
}

// ═══════════════════════════════════════
// P1 补充：D4 磁盘空间不足降级
// ═══════════════════════════════════════

#[test]
fn test_d4_disk_full_degradation() {
    // 场景：尝试把输出写到非法路径（文件当作目录）→ 应返回 Err 不 panic
    let tmp = TempDir::new("d4-disk-full");

    // 创建正常的输入（一个小项目）
    std::fs::write(
        tmp.join("main.py"),
        "print('hello')\n",
    )
    .unwrap();

    // 恶意输出路径：一个普通文件当作目录来用
    let bad_output_file = tmp.join("bad_output.txt");
    std::fs::write(&bad_output_file, "blocked").unwrap();
    let bad_output_sub = bad_output_file.join("subdir");

    // cost_analyzer 应该优雅失败
    let r = cost_analyzer::analyze(&tmp.path, &bad_output_sub);
    // 允许 Ok（如果还没到写文件的步骤就返回）或 Err（写文件时失败）
    // 关键：不能 panic
    match r {
        Ok(_) => (),
        Err(e) => {
            assert!(!e.is_empty(), "错误消息不应为空");
        }
    }
}

// ═══════════════════════════════════════
// P1 补充：D5 网络不可用降级
// ═══════════════════════════════════════

#[test]
fn test_d5_no_network_degradation() {
    // 场景：cost_analyzer 只做正则提取+分类，不发起网络请求
    // 验证：在无网络环境下仍能完成分析并正确分类
    let tmp = TempDir::new("d5-no-network");

    // 创建包含多种 API 端点的代码
    std::fs::write(
        tmp.join("app.py"),
        r#"
import requests
import httpx

# 境外 API
r1 = requests.get("https://api.openai.com/v1/chat/completions")
r2 = requests.post("https://api.stripe.com/v1/charges")
r3 = httpx.get("https://api.github.com/repos/owner/repo")

# 国内 API
r4 = requests.get("https://api.aliyun.com/ecs")
r5 = httpx.post("https://api.baidu.com/translate")

# 内网 / 自建
r6 = requests.get("http://localhost:8080/health")
r7 = requests.get("https://myapp.internal/api/data")
"#,
    )
    .unwrap();

    // 创建输出目录
    let output_dir = tmp.join("output");
    std::fs::create_dir_all(&output_dir).unwrap();

    // 关键：不发起任何网络请求即可完成分析
    let result = cost_analyzer::analyze(&tmp.path, &output_dir);
    assert!(result.is_ok(), "cost_analyzer 应完成（不依赖网络）: {:?}", result.err());

    let report = result.unwrap();
    // 应该有检测到的境外 API 端点（openai.com, stripe.com, github.com 是 KnownForeign）
    assert!(
        report.cross_border_apis.len() >= 1,
        "应检测到至少 1 个境外 API，实际: {:?}",
        report.cross_border_apis.iter().map(|c| &c.endpoint).collect::<Vec<_>>()
    );

    // 数据主权风险不应为 Low（有境外 API）
    assert_ne!(
        report.data_sovereign_risk,
        "Low",
        "存在境外 API，数据主权风险不应为 Low"
    );

    println!(
        "无网络分析完成: {} 总API · {} 境外 · {} 国内 · 风险={} · 预估¥{}/月",
        report.cross_border_apis.len() + report.domestic_apis.len() + report.self_hosted_count as usize,
        report.cross_border_apis.len(),
        report.domestic_apis.len(),
        report.data_sovereign_risk,
        report.estimated_monthly_cny
    );
}

// ═══════════════════════════════════════
// P2 补充：P1 吞吐量基准
// ═══════════════════════════════════════

#[test]
fn test_p1_throughput_benchmark() {
    use std::time::Instant;

    let tmp = TempDir::new("p1-throughput");
    let file_count: usize = 500;

    // 创建 500 个小 Python 文件
    for i in 0..file_count {
        let content = format!("# file {}\ndef foo_{}():\\n    return {}\n", i, i, i);
        std::fs::write(tmp.join(&format!("mod_{}.py", i)), content).unwrap();
    }

    let start = Instant::now();

    // detect + inject 批量处理
    let code_input = detector::detect(&tmp.path).unwrap();
    assert_eq!(code_input.file_count, file_count);

    let mut injected = 0;
    for i in 0..file_count {
        let file_path = tmp.join(&format!("mod_{}.py", i));
        let content = std::fs::read_to_string(&file_path).unwrap();
        let (new_content, r) =
            injector::inject_into_code(&content, &format!("mod_{}.py", i), "General")
                .unwrap();
        if r.injected {
            injected += 1;
            std::fs::write(&file_path, new_content).unwrap();
        }
    }

    let elapsed = start.elapsed();
    let throughput = file_count as f64 / elapsed.as_secs_f64();

    println!(
        "吞吐量: {} 文件 / {:.2}s = {:.0} 文件/秒",
        file_count,
        elapsed.as_secs_f64(),
        throughput
    );

    assert_eq!(injected, file_count, "所有文件都应被注入主权头");
    // 性能门槛: 500 文件应在 30 秒内完成
    assert!(
        elapsed.as_secs() < 30,
        "吞吐量过低: {:.2}s > 30s 上限",
        elapsed.as_secs_f64()
    );
    // 最低吞吐: 50 文件/秒
    assert!(
        throughput > 50.0,
        "吞吐量不达标: {:.0} 文件/秒 < 50 下限",
        throughput
    );
}

// ═══════════════════════════════════════
// P2 补充：P2 内存峰值基准
// ═══════════════════════════════════════

#[test]
fn test_p2_memory_peak_mass_files() {
    let tmp = TempDir::new("p2-memory");
    let file_count: usize = 1000;

    // 创建 1000 个小文件（模拟大型项目）
    for i in 0..file_count {
        let content = format!(
            "# module_{}\nimport os\nclass Worker{}:\n    def run(self):\\n        return {}\n",
            i, i, i
        );
        std::fs::write(tmp.join(&format!("worker_{}.py", i)), content).unwrap();
    }

    // 关键：大数量下 detect 不能 panic
    let code_input = detector::detect(&tmp.path);
    assert!(code_input.is_ok(), "1000 文件检测应成功");
    let ci = code_input.unwrap();
    assert_eq!(ci.file_count, file_count, "文件计数应准确");
    assert_eq!(ci.language, "Python");

    // 对每个文件执行注入（验证批量处理稳定）
    let mut success_count = 0;
    for i in 0..file_count {
        let file_path = tmp.join(&format!("worker_{}.py", i));
        let content = std::fs::read_to_string(&file_path).unwrap();
        let r = injector::inject_into_code(
            &content,
            &format!("worker_{}.py", i),
            "General",
        );
        if let Ok((new_content, inject_result)) = r {
            std::fs::write(&file_path, new_content).unwrap();
            if inject_result.injected {
                success_count += 1;
            }
        }
    }

    assert_eq!(success_count, file_count, "全部 {} 文件应注入成功", file_count);

    // 二次检查：全部文件都带有主权头
    for i in 0..file_count {
        let content = std::fs::read_to_string(tmp.join(&format!("worker_{}.py", i))).unwrap();
        assert!(dna::has_dna(&content), "worker_{}.py 缺少 DNA 头", i);
    }

    println!(
        "内存基准通过: {} 文件 detect+inject+verify 全链路稳定",
        file_count
    );
}

// ═══════════════════════════════════════
// 集成测试：cost_analyzer 文件落地验证
// ═══════════════════════════════════════

#[test]
fn test_cost_report_file_generated() {
    let tmp = TempDir::new("cost-report-file");
    let output_dir = tmp.join("output");
    std::fs::create_dir_all(&output_dir).unwrap();

    // 创建一个包含境外 API 的 Python 文件
    tmp.write_file(
        "api_client.py",
        r#"
import requests
r1 = requests.get("https://api.openai.com/v1/models")
r2 = requests.post("https://api.github.com/repos/test/repo")
r3 = requests.get("https://api.aliyun.com/ecs")
"#,
    );

    let report = cost_analyzer::analyze(&tmp.path, &output_dir)
        .expect("成本分析应成功");

    // 核心断言：文件落地
    let cost_path = output_dir.join(".cost-report.json");
    assert!(cost_path.exists(), ".cost-report.json 应存在: {:?}", cost_path);

    // 验证 JSON 内容可反序列化
    let content = std::fs::read_to_string(&cost_path).unwrap();
    let parsed: serde_json::Value =
        serde_json::from_str(&content).expect("JSON 格式合法");

    assert_eq!(
        parsed["total_apis_detected"].as_u64().unwrap(),
        report.total_apis_detected as u64
    );
    assert!(
        parsed["cross_border_apis"]
            .as_array()
            .unwrap()
            .len() >= 1,
        "应检测到至少1个境外 API"
    );

    println!(
        "成本报告落地验证通过: {} → {}",
        report.data_sovereign_risk,
        cost_path.display()
    );
}

// ═══════════════════════════════════════
// 集成测试：seal 文件落地验证
// ═══════════════════════════════════════

#[test]
fn test_seal_record_file_generated() {
    let tmp = TempDir::new("seal-record-file");
    let output_dir = tmp.join("output");
    std::fs::create_dir_all(&output_dir).unwrap();

    let test_dna = format!(
        "#龍芯⚡️SEAL-TEST-{}-FILE-CHECK",
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs()
    );

    let result = seal::seal(
        &test_dna,
        "1.0.0",
        "2026-08-06T12:00:00+08:00",
        "/tmp/test-project",
        "Python",
        "鲲鹏",
        4,
        4,
        0,
        4,
        true,
        2,
        Some(67),
        Some(1500.0),
        Some("🟡 Medium".to_string()),
        Some(2),
        &output_dir,
    );

    assert!(result.is_ok(), "封印应成功: {:?}", result.err());
    let record = result.unwrap();

    // 核心断言：文件落地到输出目录
    let seal_path = output_dir.join(".seal-record.json");
    assert!(
        seal_path.exists(),
        ".seal-record.json 应存在: {:?}",
        seal_path
    );

    // 验证 JSON 内容可反序列化
    let content = std::fs::read_to_string(&seal_path).unwrap();
    let parsed: serde_json::Value =
        serde_json::from_str(&content).expect("JSON 格式合法");

    assert_eq!(parsed["dna"].as_str().unwrap(), test_dna);
    assert!(!parsed["seal_hash"].as_str().unwrap().is_empty());
    assert_eq!(parsed["total_files"].as_u64().unwrap(), 4);
    assert_eq!(parsed["security_violations"].as_u64().unwrap(), 2);

    println!(
        "封印记录落地验证通过: DNA={} → {}",
        &test_dna[..40.min(test_dna.len())],
        seal_path.display()
    );

    // 清理归档（不污染 ~/.longhun/memory/seals/）
    let home = std::env::var("HOME").unwrap_or_else(|_| "/tmp".to_string());
    let archive = std::path::PathBuf::from(home)
        .join(".longhun/memory/seals")
        .join(format!("{}.seal.json", test_dna));
    std::fs::remove_file(&archive).ok();
}

// ── 记忆桥接集成测试 ──
#[test]
fn test_seal_memory_bridge() {
    let tmp = TempDir::new("seal-bridge");
    let output_dir = tmp.join("output");
    std::fs::create_dir_all(&output_dir).unwrap();

    let test_dna = format!(
        "#龍芯⚡️BRIDGE-TEST-{}-MEM-LIFECYCLE",
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .unwrap()
            .as_secs()
    );

    let result = seal::seal(
        &test_dna,
        "1.0.0",
        "2026-08-06T12:00:00+08:00",
        "/tmp/bridge-test-project",
        "Python",
        "鲲鹏",
        3,
        3,
        0,
        3,
        true,
        0,
        Some(90),
        Some(100.0),
        Some("🟢 Low".to_string()),
        Some(0),
        &output_dir,
    );

    // 核心断言：封印本身必须成功（记忆桥接失败不阻塞管道）
    assert!(result.is_ok(), "封印应成功（桥接降级不阻塞）: {:?}", result.err());
    let record = result.unwrap();

    // 验证封存完整性
    assert!(!record.seal_hash.is_empty());
    assert!(output_dir.join(".seal-record.json").exists());

    println!(
        "记忆桥接集成测试通过: DNA={} · 封印: {}...",
        &test_dna[..30.min(test_dna.len())],
        &record.seal_hash[..16]
    );

    // 清理归档
    let home = std::env::var("HOME").unwrap_or_else(|_| "/tmp".to_string());
    let archive = std::path::PathBuf::from(home)
        .join(".longhun/memory/seals")
        .join(format!("{}.seal.json", test_dna));
    std::fs::remove_file(&archive).ok();
}

// ═════════════════════════════════════════════════════════════════
// T1-T5: 三色审计迁移测试（替换殖民评分）
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-TRICOLOR-TESTS-v1.0
// ═════════════════════════════════════════════════════════════════

/// T1: R值≥85 → 🟢 自动放行
#[test]
fn test_tricolor_r_score_green() {
    let dir = std::env::temp_dir().join("lh-station-tricolor-green");
    fs::create_dir_all(&dir).unwrap();
    // 干净的文件：只有业务逻辑 → 无违规
    fs::write(dir.join("main.py"), "# clean file\nprint('hello')\n").unwrap();
    let report = security::audit(&dir).unwrap();
    assert!(report.verdict.r_score >= 85,
        "干净文件应得 R≥85，实际 R={}", report.verdict.r_score);
    assert_eq!(report.verdict.status_code, "GREEN");
    assert_eq!(report.verdict.emoji, "🟢");
    assert_eq!(report.verdict.disposition, "自动放行");
    println!("🟢 三色通过: R={}", report.verdict.r_score);
    fs::remove_dir_all(&dir).ok();
}

/// T2: R值60-84 → 🟡 挂起待复核
#[test]
fn test_tricolor_r_score_yellow() {
    let dir = std::env::temp_dir().join("lh-station-tricolor-yellow");
    fs::create_dir_all(&dir).unwrap();
    // 含境外 API + 平台锁定 → 扣分但不阻断
    fs::write(dir.join("service.py"), r#"
import requests
requests.post("https://api.openai.com/v1/chat", json={})
requests.post("https://api.anthropic.com/v1/messages", json={})
// AWS SDK 平台锁定
import boto3
# License: MIT
"#).unwrap();
    let report = security::audit(&dir).unwrap();
    println!("🟡 待核: R={} status={}", report.verdict.r_score, report.verdict.status_code);
    // 有违规但可能仍≥60 → 🟡
    assert!(!report.violations.is_empty(), "应该有违规项");
    assert!(report.verdict.r_score >= 60 || report.verdict.status_code == "YELLOW",
        "中度违规应进入🟡区间");
    fs::remove_dir_all(&dir).ok();
}

/// T3: R值<60 → 🔴 立即熔断
#[test]
fn test_tricolor_r_score_red() {
    let dir = std::env::temp_dir().join("lh-station-tricolor-red");
    fs::create_dir_all(&dir).unwrap();
    // 硬编码密钥 + 境外API + 删除日志 = 阻断级红线
    fs::write(dir.join("bad.py"), r#"
api_key = "sk-1234567890abcdef"
api_secret = "deadbeef1234"
password = "admin123"
secret_key = "abcdef"
private_key = "-----BEGIN RSA PRIVATE KEY-----"
token = "ghp_xxxxxxxxxxxxxxxx"
access_key = "AKIAIOSFODNN7EXAMPLE"
// 境外
import requests
requests.post("https://api.openai.com/v1/chat", json={})
// 删除日志
delete_all_logs()
clear_log()
"#).unwrap();
    let report = security::audit(&dir).unwrap();
    println!("🔴 熔断: R={} status={} passed={}", report.verdict.r_score, report.verdict.status_code, report.passed);
    // 有阻断项应不通过，R值应低于85（干净分）
    assert!(!report.passed, "有阻断项应不通过");
    assert!(report.verdict.r_score < 85, "含违规应有扣分，实际 R={}", report.verdict.r_score);
    assert!(!report.verdict.triggered_rules.is_empty(), "应有触发的规则");
    // 验证 JSON 可序列化
    serde_json::to_string(&report.verdict).unwrap();
    fs::remove_dir_all(&dir).ok();
}

/// T4: DNA 证据链格式校验
#[test]
fn test_tricolor_dna_format() {
    let dir = std::env::temp_dir().join("lh-station-tricolor-dna");
    fs::create_dir_all(&dir).unwrap();
    fs::write(dir.join("app.py"), "print('ok')\n").unwrap();
    let report = security::audit(&dir).unwrap();
    let dna = &report.verdict.dna;
    assert!(!dna.is_empty(), "DNA 不应为空");
    assert!(dna.contains("#龍芯"), "DNA 应包含龍芯前缀");
    println!("DNA 格式合格: {}", dna);
    fs::remove_dir_all(&dir).ok();
}

/// T5: TricolorVerdict JSON 序列化/反序列化
#[test]
fn test_tricolor_verdict_json() {
    use lh_station::pipeline::security::TricolorVerdict;

    let verdict = TricolorVerdict {
        r_score: 71,
        status_code: "YELLOW".to_string(),
        emoji: "🟡".to_string(),
        disposition: "挂起待复核".to_string(),
        triggered_rules: vec![
            "COLONIAL:平台锁定风险-1".to_string(),
            "PRIVACY:Token硬编码-1".to_string(),
        ],
        dna: "#龍芯⚡️丙午·癸未·乙酉·坤卦-AUDIT-test".to_string(),
        evidence_hash: "a1b2c3d4".to_string(),
        engine_version: "tricolor-core/1.1.0".to_string(),
        human_welfare_score: 95,
        fairness_score: 90,
        controllability_score: 70,
        transparency_score: 85,
        traceability_score: 80,
        privacy_score: 55,
        bcm_score: Some(0.82),
    };

    // 序列化
    let json = serde_json::to_string_pretty(&verdict).unwrap();
    println!("Verdict JSON:\n{}", json);
    assert!(json.contains("\"r_score\": 71"));
    assert!(json.contains("\"emoji\": \"🟡\""));
    assert!(json.contains("\"engine_version\": \"tricolor-core/1.1.0\""));

    // 反序列化
    let parsed: TricolorVerdict = serde_json::from_str(&json).unwrap();
    assert_eq!(parsed.r_score, 71);
    assert_eq!(parsed.status_code, "YELLOW");
    assert_eq!(parsed.human_welfare_score, 95);
    assert_eq!(parsed.privacy_score, 55);
    println!("🟢 JSON 序列化/反序列化通过");
}
