// 龍魂代码中转站 · 记忆封印引擎
// 转换完成后 → SHA-256 封印 → 归档到 ~/.longhun/memory/seals/
// DNA: #龍芯⚡️丙午·癸未·乙酉·壬午·䷁坤-SEAL-v1.0

use serde::{Deserialize, Serialize};
use sha2::{Sha256, Digest};
use std::path::{Path, PathBuf};

// ═══════════════════════════════════════
// 结构体
// ═══════════════════════════════════════

/// 封印记录 — 一次转换的完整审计快照
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct SealRecord {
    pub dna: String,
    pub station_version: String,
    pub transformed_at: String,
    pub original_path: String,
    pub language: String,
    pub chip_target: String,
    pub total_files: u32,
    pub injected_count: u32,
    pub compiled_count: u32,
    pub signed_count: u32,
    pub security_passed: bool,
    pub security_violations: u32,
    pub r_score: Option<u32>,
    pub cost_monthly: Option<f64>,
    pub cost_risk: Option<String>,
    pub cost_cross_border: Option<u32>,
    pub seal_hash: String,
}

/// 索引条目（写入 index.json）
#[derive(Debug, Clone, Serialize, Deserialize)]
struct IndexEntry {
    dna: String,
    original_path: String,
    language: String,
    transformed_at: String,
    seal_hash: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct SealIndex {
    seals: Vec<IndexEntry>,
    updated_at: String,
}

/// 获取封印目录路径
fn seals_dir() -> PathBuf {
    let home = std::env::var("HOME")
        .unwrap_or_else(|_| "/tmp".to_string());
    PathBuf::from(home).join(".longhun/memory/seals")
}

/// 幂等检查：相同 DNA 是否已存在
pub fn dna_exists(dna: &str) -> bool {
    let seal_path = seals_dir().join(format!("{}.seal.json", dna));
    seal_path.exists()
}

/// 主封印函数
pub fn seal(
    dna: &str,
    station_version: &str,
    transformed_at: &str,
    original_path: &str,
    language: &str,
    chip_target: &str,
    total_files: u32,
    injected_count: u32,
    compiled_count: u32,
    signed_count: u32,
    security_passed: bool,
    security_violations: u32,
    r_score: Option<u32>,
    cost_monthly: Option<f64>,
    cost_risk: Option<String>,
    cost_cross_border: Option<u32>,
    output_dir: &Path,
) -> Result<SealRecord, String> {
    // ═══ 1. 幂等检查 ═══
    if dna_exists(dna) {
        return Err(format!("DNA 已归档，跳过: {}", dna));
    }

    // ═══ 2. 组装 SealRecord ═══
    let partial = SealRecord {
        dna: dna.to_string(),
        station_version: station_version.to_string(),
        transformed_at: transformed_at.to_string(),
        original_path: original_path.to_string(),
        language: language.to_string(),
        chip_target: chip_target.to_string(),
        total_files,
        injected_count,
        compiled_count,
        signed_count,
        security_passed,
        security_violations,
        r_score,
        cost_monthly,
        cost_risk,
        cost_cross_border,
        seal_hash: String::new(), // 待填充
    };

    // ═══ 3. SHA-256 哈希 ═══
    let mut hasher = Sha256::new();
    // 序列化不含 seal_hash 的部分来生成哈希
    let pre_hash_json = serde_json::to_string(&partial)
        .map_err(|e| format!("序列化失败: {}", e))?;
    hasher.update(pre_hash_json.as_bytes());
    let hash_result = hasher.finalize();
    let seal_hash = hex::encode(hash_result);

    let record = SealRecord {
        seal_hash: seal_hash.clone(),
        ..partial
    };

    // ═══ 4. 写入输出目录 .seal-record.json ═══
    let seal_path = output_dir.join(".seal-record.json");
    let seal_json = serde_json::to_string_pretty(&record)
        .map_err(|e| format!("序列化封印记录失败: {}", e))?;
    std::fs::write(&seal_path, &seal_json)
        .map_err(|e| format!("写入封印记录失败: {}", e))?;
    println!("  封印: 🧬 {} → {}", record.dna, seal_path.display());

    // ═══ 5. 归档到 ~/.longhun/memory/seals/ ═══
    let dir = seals_dir();
    if let Err(e) = std::fs::create_dir_all(&dir) {
        eprintln!("⚠️ WARNING: 创建封印目录失败: {}", e);
        return Ok(record); // 不阻塞
    }

    let archive_path = dir.join(format!("{}.seal.json", dna));
    if let Err(e) = std::fs::write(&archive_path, &seal_json) {
        eprintln!("⚠️ WARNING: 写入封印归档失败: {}", e);
        return Ok(record); // 不阻塞
    }

    // ═══ 6. 更新 index.json ═══
    update_index(dna, original_path, language, transformed_at, &seal_hash);

    // ── 桥接龙魂记忆系统 ──────────────────────────
    // 通过 Python CLI 桥接器将封印记录存入 MemoryLifecycle
    let bridge_json = serde_json::to_string(&record)
        .map_err(|e| format!("序列化失败: {}", e))?;
    match std::process::Command::new("python3")
        .args(["-c", &format!(
            "from longhun_bridge import store_seal; import sys; \
             result = store_seal('{}'); \
             print(result)",
            bridge_json.replace('\\', "\\\\").replace('\'', "'\\''")
        )])
        .current_dir(std::env::current_dir().unwrap_or_else(|_| PathBuf::from(".")))
        .output()
    {
        Ok(output) if output.status.success() => {
            let stdout = String::from_utf8_lossy(&output.stdout);
            // 解析桥接器返回，提取 entry_id
            if let Ok(result) = serde_json::from_str::<serde_json::Value>(&stdout) {
                if result.get("status").and_then(|s| s.as_str()) == Some("ok") {
                    let entry_id = result.get("entry_id").and_then(|v| v.as_str()).unwrap_or("?");
                    println!("  记忆: 🧠 已存入龙魂记忆系统 (entry_id: {})", entry_id);
                } else {
                    eprintln!("  ⚠️ 记忆桥接: {}", result.get("reason").and_then(|s| s.as_str()).unwrap_or("未知错误"));
                }
            } else {
                eprintln!("  ⚠️ 记忆桥接: 无法解析返回");
            }
        }
        Ok(output) => {
            let stderr = String::from_utf8_lossy(&output.stderr);
            eprintln!("  ⚠️ 记忆桥接失败: {}", stderr.trim());
        }
        Err(e) => {
            eprintln!("  ⚠️ 记忆桥接启动失败: {} (无 Python3 环境?)", e);
        }
    }

    Ok(record)
}

/// 更新封印索引
fn update_index(dna: &str, original_path: &str, language: &str, transformed_at: &str, seal_hash: &str) {
    let index_path = seals_dir().join("index.json");

    let mut index: SealIndex = if index_path.exists() {
        match std::fs::read_to_string(&index_path) {
            Ok(content) => serde_json::from_str(&content).unwrap_or(SealIndex {
                seals: Vec::new(),
                updated_at: String::new(),
            }),
            Err(_) => SealIndex {
                seals: Vec::new(),
                updated_at: String::new(),
            },
        }
    } else {
        SealIndex {
            seals: Vec::new(),
            updated_at: String::new(),
        }
    };

    // 幂等：不重复添加
    if !index.seals.iter().any(|e| e.dna == dna) {
        index.seals.push(IndexEntry {
            dna: dna.to_string(),
            original_path: original_path.to_string(),
            language: language.to_string(),
            transformed_at: transformed_at.to_string(),
            seal_hash: seal_hash.to_string(),
        });
    }

    index.updated_at = chrono::Local::now()
        .format("%Y-%m-%dT%H:%M:%S%z")
        .to_string();

    if let Ok(json) = serde_json::to_string_pretty(&index) {
        if let Err(e) = std::fs::write(&index_path, json) {
            eprintln!("⚠️ WARNING: 更新封印索引失败: {}", e);
        }
    }
}

/// 读取已有的封印记录
pub fn read_seal(dna: &str) -> Option<SealRecord> {
    let path = seals_dir().join(format!("{}.seal.json", dna));
    if !path.exists() {
        return None;
    }
    let content = std::fs::read_to_string(&path).ok()?;
    serde_json::from_str(&content).ok()
}

/// 列出所有封印记录
pub fn list_seals() -> Vec<SealRecord> {
    let index_path = seals_dir().join("index.json");
    if !index_path.exists() {
        return Vec::new();
    }

    let content = match std::fs::read_to_string(&index_path) {
        Ok(c) => c,
        Err(_) => return Vec::new(),
    };

    let index: SealIndex = match serde_json::from_str(&content) {
        Ok(i) => i,
        Err(_) => return Vec::new(),
    };

    index
        .seals
        .iter()
        .filter_map(|entry| read_seal(&entry.dna))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;

    fn setup_test_dna(suffix: &str) -> String {
        format!(
            "#龍芯⚡️TEST-SEAL-{}-{}",
            chrono::Local::now().timestamp(),
            suffix
        )
    }

    #[test]
    fn test_seal_creates_record() {
        let dna = setup_test_dna("create");
        let tmp = std::env::temp_dir().join(format!("lh-station-seal-{}", chrono::Local::now().timestamp()));
        std::fs::create_dir_all(&tmp).unwrap();

        let result = seal(
            &dna,
            "1.0.0",
            "2026-08-06T12:00:00+08:00",
            "/tmp/test-project",
            "Rust",
            "鲲鹏",
            5,
            5,
            1,
            5,
            true,
            0,
            Some(90),
            Some(0.0),
            Some("🟢 Low".to_string()),
            Some(0),
            &tmp,
        );

        assert!(result.is_ok());
        let record = result.unwrap();

        // 验证 seal_hash 不为空
        assert!(!record.seal_hash.is_empty());
        assert_eq!(record.dna, dna);
        assert!(record.security_passed);

        // 验证 .seal-record.json 存在
        assert!(tmp.join(".seal-record.json").exists());

        // 验证归档文件存在
        let archive = seals_dir().join(format!("{}.seal.json", dna));
        assert!(archive.exists(), "归档文件应存在: {:?}", archive);

        // 验证 index.json
        let index_path = seals_dir().join("index.json");
        assert!(index_path.exists());

        // 清理输出目录
        std::fs::remove_dir_all(&tmp).ok();
        // 清理归档（保留 index 不影响其他测试）
        std::fs::remove_file(&archive).ok();
    }

    #[test]
    fn test_seal_idempotent() {
        let dna = setup_test_dna("idem");
        let tmp = std::env::temp_dir().join(format!("lh-station-seal-idem-{}", chrono::Local::now().timestamp()));
        std::fs::create_dir_all(&tmp).unwrap();

        // 第一次封印
        let r1 = seal(
            &dna, "1.0.0", "2026-08-06T12:00:00+08:00",
            "/tmp/a", "Python", "auto",
            1, 1, 0, 1,
            true, 0, None, None, None, None,
            &tmp,
        );
        assert!(r1.is_ok());

        // 第二次相同 DNA → 应返回 Err（幂等）
        let r2 = seal(
            &dna, "1.0.0", "2026-08-06T12:00:00+08:00",
            "/tmp/b", "Python", "auto",
            1, 1, 0, 1,
            true, 0, None, None, None, None,
            &tmp,
        );
        assert!(r2.is_err(), "相同DNA第二次应失败（幂等）");
        assert!(r2.unwrap_err().contains("已归档"));

        std::fs::remove_dir_all(&tmp).ok();
        let archive = seals_dir().join(format!("{}.seal.json", dna));
        std::fs::remove_file(&archive).ok();
    }

    #[test]
    fn test_seal_hash_consistent() {
        // 相同输入 → 相同 seal_hash
        let dna = setup_test_dna("hash");
        let tmp = std::env::temp_dir().join(format!("lh-station-seal-hash-{}", chrono::Local::now().timestamp()));
        std::fs::create_dir_all(&tmp).unwrap();

        let build = || {
            let _tmp = std::env::temp_dir().join("dummy");
            std::fs::create_dir_all(&_tmp).ok();
            SealRecord {
                dna: dna.clone(),
                station_version: "1.0.0".to_string(),
                transformed_at: "2026-08-06T12:00:00+08:00".to_string(),
                original_path: "/tmp/x".to_string(),
                language: "Rust".to_string(),
                chip_target: "鲲鹏".to_string(),
                total_files: 3,
                injected_count: 3,
                compiled_count: 1,
                signed_count: 3,
                security_passed: true,
                security_violations: 0,
                r_score: Some(95),
                cost_monthly: Some(0.0),
                cost_risk: Some("🟢 Low".to_string()),
                cost_cross_border: Some(0),
                seal_hash: String::new(),
            }
        };

        let mut hasher = Sha256::new();
        let json = serde_json::to_string(&build()).unwrap();
        hasher.update(json.as_bytes());
        let h1 = hex::encode(hasher.finalize());

        let mut hasher = Sha256::new();
        hasher.update(serde_json::to_string(&build()).unwrap().as_bytes());
        let h2 = hex::encode(hasher.finalize());

        assert_eq!(h1, h2, "相同输入应产生相同哈希");

        std::fs::remove_dir_all(&tmp).ok();
    }

    #[test]
    fn test_dna_exists() {
        let dna = setup_test_dna("exists");
        // 先确保不存在
        let path = seals_dir().join(format!("{}.seal.json", dna));
        std::fs::remove_file(&path).ok();
        assert!(!dna_exists(&dna));

        // 创建
        let tmp = std::env::temp_dir().join(format!("lh-station-seal-exists-{}", chrono::Local::now().timestamp()));
        std::fs::create_dir_all(&tmp).unwrap();
        seal(
            &dna, "1.0.0", "2026-08-06T12:00:00+08:00",
            "/tmp/x", "Python", "auto",
            1, 1, 0, 1,
            true, 0, None, None, None, None,
            &tmp,
        )
        .ok();

        assert!(dna_exists(&dna));

        std::fs::remove_dir_all(&tmp).ok();
        std::fs::remove_file(&path).ok();
    }
}
