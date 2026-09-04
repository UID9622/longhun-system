**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
# 🐉 lh-station 三色审计迁移 · CodeBuddy 指令

## 目标

将 lh-station 的 security 模块从"殖民评分 + 规则列表"改为
**三色审计标准（R值 + 🟢🟡🔴 + DNA 证据链）**，
CI/CD 报告同步更新。

## 改动 1：security.rs —— 替换殖民评分为三色判定

### 旧逻辑

```rust
struct SecurityReport {
    passed: bool,
    violations: Vec<Violation>,
    colonial_score: f64,    // 0.70/1.0 ← 废弃
    data_exfil_check: bool,
    ...
}
```

### 新逻辑

```rust
/// 三色审计判定结果
#[derive(Debug, Serialize, Deserialize)]
struct TricolorVerdict {
    r_score: u32,                   // R 值 0-95
    status_code: String,            // "GREEN" | "YELLOW" | "RED"
    emoji: String,                  // "🟢" | "🟡" | "🔴"
    disposition: String,            // 处置动作
    triggered_rules: Vec<String>,   // 触发的规则 ID
    dna: String,                    // 证据链 DNA
    evidence_hash: String,          // 证据哈希（SM3优先）
    engine_version: String,         // "tricolor-core/1.1.0"
}

struct SecurityReport {
    passed: bool,
    verdict: TricolorVerdict,       // ← 替换 colonial_score
    violations: Vec<Violation>,     // 保留作为明细
    data_exfil_check: bool,
    ...
}
```

### R值计算（替换殖民评分计算）

```rust
/// 将安全审查结果映射到三色审计六维评分
fn compute_r_score(report: &SecurityReport) -> u32 {
    // 从 violations 反推六维得分
    let has_data_exfil = report.violations.iter().any(|v|
        matches!(v.severity, Severity::Block | Severity::Warn)
        && v.rule.starts_with("DATA_EXFIL"));
    let has_colonial = report.violations.iter().any(|v|
        v.rule.starts_with("COLONIAL"));
    let has_license = report.violations.iter().any(|v|
        v.rule.starts_with("LICENSE"));

    // 六维评分（100 - 扣分）
    let human_welfare = 95;  // 默认高位
    let fairness = if report.license_compliance { 90 } else { 65 };
    let controllability = if has_colonial { 70 } else { 90 };
    let transparency = 85;   // 代码本身透明
    let traceability = if report.passed { 90 } else { 60 };
    let privacy = if has_data_exfil { 55 } else { 90 };

    // 加权公式
    let r = (human_welfare as f64 * 0.20)
          + (fairness as f64 * 0.20)
          + (controllability as f64 * 0.15)
          + (transparency as f64 * 0.15)
          + (traceability as f64 * 0.15)
          + (privacy as f64 * 0.15);
    (r.min(95.0).round() as u32)
}

/// 根据 R 值生成三色判定
fn make_verdict(r_score: u32, violations: &[Violation]) -> TricolorVerdict {
    let (status_code, emoji, disposition) = if r_score >= 85 {
        ("GREEN", "🟢", "自动放行")
    } else if r_score >= 60 {
        ("YELLOW", "🟡", "挂起待复核")
    } else {
        ("RED", "🔴", "立即熔断")
    };

    let triggered_rules: Vec<String> = violations.iter()
        .map(|v| format!("{}-{}", v.rule, v.severity as u8))
        .collect();

    TricolorVerdict {
        r_score,
        status_code: status_code.to_string(),
        emoji: emoji.to_string(),
        disposition: disposition.to_string(),
        triggered_rules,
        dna: generate_tricolor_dna(),
        evidence_hash: sha256_of_violations(violations),
        engine_version: "tricolor-core/1.1.0".to_string(),
    }
}
```

### 修改点

1. `security.rs` — `SecurityReport` 结构体新增 `verdict: TricolorVerdict` 字段
2. `security.rs` — `run_security_check()` 末尾调用 `compute_r_score()` + `make_verdict()`
3. `packer.rs` — `Manifest` 中 `colonial_score` 替换为 `r_score`

### 测试补充

在 `supplement_tests.rs` 中新增：

```rust
// 三色判定测试
#[test]
fn test_tricolor_r_score_green() { /* 高得分 → 🟢 */ }
#[test]
fn test_tricolor_r_score_yellow() { /* 中等得分 → 🟡 */ }
#[test]
fn test_tricolor_r_score_red()    { /* 低得分 → 🔴 */ }
#[test]
fn test_tricolor_dna_format()     { /* DNA 格式校验 */ }
#[test]
fn test_tricolor_verdict_json()   { /* verdict 序列化正确 */ }
```

（共 5 个新增测试）

---

## 改动 2：CI/CD 报告 —— 改用 R 值 + 🟢🟡🔴

### 旧报告（以 colonial_score 为主）

```
殖民评分: 0.70/1.0
```

### 新报告（三色审计格式）

在 `.github/workflows/lh-station.yml` 的 PR Comment / Job Summary 中，原殖民评分替换为：

```markdown
### 🐉 三色审计报告

| 维度 | 值 |
|:---|:---:|
| R 值 | **71** |
| 状态 | **🟡 审查** |
| 处置 | 挂起待复核 |
| DNA | `#龍芯⚡️丙午···-AUDIT-7f3k9x-9622` |

**触发的规则:**
- RULE-PRIVACY-003 · 隐私保护不足（得分55）
- RULE-EXPORT-001 · 数据导出未充分申明

**六维得分:**
```
人类福祉: 82  ██████████████▉
公平公正: 78  █████████████▋
可控可信: 70  ████████████
透明可解释: 65 ███████████▎
责任可追溯: 80 ██████████████
隐私保护: 55  █████████▌
─────────────────────
R = 71 → 🟡 审查
```
```

### GitHub Actions 脚本改动

在 `lh-station.yml` 的 PR Comment 生成脚本中：

```javascript
// 原来
// const colonialScore = manifest.colonial_score || 'N/A';
// body += `| 殖民评分 | ${colonialScore} |\n`;

// 改为
const verdict = JSON.parse(fs.readFileSync('${{ env.LH_OUTPUT }}/.sovereign.json')).verdict;
body += `| R 值 | **${verdict.r_score}** |\n`;
body += `| 三色状态 | **${verdict.emoji} ${verdict.status_code}** |\n`;
body += `| DNA | \`${verdict.dna}\` |\n`;
```

---

## 改动影响

| 文件 | 改动量 | 兼容性 |
|:---|:---:|:---:|
| `security.rs` | ~40 行新增 | `SecurityReport` 新增字段，旧序列化兼容 |
| `packer.rs` | ~5 行 | `colonial_score` → `r_score`（字段名变更） |
| `.github/workflows/lh-station.yml` | ~15 行 | PR Comment 脚本替换 |
| 测试 | +5 个 | 新增，不破坏旧测试 |

---

🐉 丙午 · 癸未 · 乙酉 · 坤卦 · 三色审计迁移 · 🟢
