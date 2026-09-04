// DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-RUST-CORE-MEMORY-v1.0-UID9622
// 创建者: 诸葛鑫（UID9622）
// 模块: 记忆条目 CRUD · 优先级排序 · P0-P3 生命周期

use serde::{Deserialize, Serialize};

/// 记忆优先级
#[derive(Debug, Clone, PartialEq, PartialOrd, Serialize, Deserialize)]
pub enum MemoryPriority {
    P0 = 0,  // 焊死·永恒（天条·DNA·确认码）
    P1 = 1,  // 核心协议·白皮书·密码
    P2 = 2,  // 技能定义·引擎定义·配置
    P3 = 3,  // 常规记忆·日志·对话记录
}

/// 记忆条目
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemoryEntry {
    pub id: String,              // UUID
    pub priority: MemoryPriority,
    pub content: String,
    pub dna: String,             // DNA 追溯码
    pub tags: Vec<String>,
    pub created_at: String,
    pub updated_at: String,
    pub access_count: u64,
    pub frozen: bool,            // 冻结状态（不删除只冻结）
}

/// 记忆查询结果
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MemoryQueryResult {
    pub entries: Vec<MemoryEntry>,
    pub total: usize,
    pub query_time_ms: f64,
}

// ══════════════════════════════════════════════
// 记忆 CRUD
// ══════════════════════════════════════════════

/// 查询记忆（按关键词匹配）
pub fn query(query_str: &str) -> MemoryQueryResult {
    let start = std::time::Instant::now();
    
    let entries = if query_str.is_empty() {
        get_all_memories()
    } else {
        search_memories(query_str)
    };
    
    let total = entries.len();
    let query_time_ms = start.elapsed().as_secs_f64() * 1000.0;
    
    MemoryQueryResult {
        entries,
        total,
        query_time_ms,
    }
}

/// 获取全部记忆（按优先级排序）
fn get_all_memories() -> Vec<MemoryEntry> {
    let mut entries = memory_store();
    entries.sort_by(|a, b| a.priority.partial_cmp(&b.priority).unwrap());
    entries
}

/// 搜索记忆
fn search_memories(query: &str) -> Vec<MemoryEntry> {
    let q = query.to_lowercase();
    memory_store()
        .into_iter()
        .filter(|e| {
            e.content.to_lowercase().contains(&q) ||
            e.tags.iter().any(|t| t.to_lowercase().contains(&q)) ||
            e.dna.to_lowercase().contains(&q)
        })
        .collect()
}

/// 创建新记忆（P3 默认优先级）
pub fn create_memory(content: &str, tags: Vec<String>) -> MemoryEntry {
    let now = chrono::Utc::now().to_rfc3339();
    MemoryEntry {
        id: uuid_v4(),
        priority: MemoryPriority::P3,
        content: content.to_string(),
        dna: format!("#龍芯⚡️{}", now),
        tags,
        created_at: now.clone(),
        updated_at: now,
        access_count: 0,
        frozen: false,
    }
}

/// 冻结记忆（不删除，只标记 frozen=true）
pub fn freeze_memory(entry: &mut MemoryEntry, reason: &str) {
    entry.frozen = true;
    entry.updated_at = chrono::Utc::now().to_rfc3339();
    entry.tags.push(format!("frozen:{}", reason));
}

/// P0 → P3 生命周期策略
pub fn lifecycle_strategy(priority: &MemoryPriority) -> &'static str {
    match priority {
        MemoryPriority::P0 => "永恒焊死·仅UID9622可修改",
        MemoryPriority::P1 => "协议级·需P05审计+P15签章",
        MemoryPriority::P2 => "工具级·需GPG签名修改",
        MemoryPriority::P3 => "常规·30天未访问冻结·90天归档",
    }
}

// ══════════════════════════════════════════════
// 内部工具
// ══════════════════════════════════════════════

fn uuid_v4() -> String {
    // 简化的 UUIDv4 生成（生产环境用 uuid crate）
    use sha2::Digest;
    let now = std::time::SystemTime::now()
        .duration_since(std::time::UNIX_EPOCH)
        .unwrap()
        .as_nanos();
    let hash = sha2::Sha256::digest(format!("LONGHUN-MEMORY-{}", now));
    format!("{:x}", hash)[..32].to_string()
}

/// 内置焊死记忆（P0/P1 级）
fn memory_store() -> Vec<MemoryEntry> {
    vec![
        MemoryEntry {
            id: "p0-dna-anchor".to_string(),
            priority: MemoryPriority::P0,
            content: "#龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜 · UID9622 · 龍魂系统最高锚点".to_string(),
            dna: "#龍芯⚡️丙午·丙申·庚戌·䷙大畜-DNA-ANCHOR-P0".to_string(),
            tags: vec!["p0".to_string(), "anchor".to_string(), "eternal".to_string()],
            created_at: "2024-12-01T00:00:00+08:00".to_string(),
            updated_at: "2024-12-01T00:00:00+08:00".to_string(),
            access_count: 999,
            frozen: false,
        },
        MemoryEntry {
            id: "p0-confirm-code".to_string(),
            priority: MemoryPriority::P0,
            content: "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z".to_string(),
            dna: "#龍芯⚡️丙午·丙申·庚戌·䷙大畜-CONFIRM-P0".to_string(),
            tags: vec!["p0".to_string(), "confirm".to_string(), "eternal".to_string()],
            created_at: "2024-12-01T00:00:00+08:00".to_string(),
            updated_at: "2024-12-01T00:00:00+08:00".to_string(),
            access_count: 999,
            frozen: false,
        },
    ]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_query_empty_returns_all() {
        let result = query("");
        assert!(result.total > 0);
    }

    #[test]
    fn test_query_dna() {
        let result = query("UID9622");
        assert!(result.total > 0);
    }

    #[test]
    fn test_create_memory() {
        let entry = create_memory("测试记忆", vec!["test".to_string()]);
        assert_eq!(entry.priority, MemoryPriority::P3);
        assert!(!entry.id.is_empty());
    }

    #[test]
    fn test_freeze_memory() {
        let mut entry = create_memory("将被冻结", vec![]);
        freeze_memory(&mut entry, "审计需要");
        assert!(entry.frozen);
        assert!(entry.tags.iter().any(|t| t.contains("frozen")));
    }

    #[test]
    fn test_p0_lifecycle() {
        let strategy = lifecycle_strategy(&MemoryPriority::P0);
        assert!(strategy.contains("永恒"));
    }
}
