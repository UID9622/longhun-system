# lh-station 生态串联方案

> DNA: #龍芯⚡️丙午·丙申·戊申·亥时·䷗复-LH-STATION-INTEGRATION-PLAN-v1.0-C8F3E1A5
> 创建者: 诸葛鑫（UID9622）
> 协议: CC BY-NC-SA 4.0（核心思想层）

---

## 一、定位

`lh-station` 是龍魂体系**主权合规闭环**的第一个环节——**代码主权注入**。

### 在体系中的位置

```
┌─────────────────────────────────────────────────────┐
│                龍魂体系 · 主权合规闭环                │
│                                                     │
│  [lh-station] ──→ [longhun-memory] ──→ [longhun-save]
│   注入DNA+封印       记忆归档           长期版本存储   │
│       │                    │                  │      │
│       └────────┬───────────┴──────────────────┘      │
│                ↓                                     │
│           [lh.py 审计]                               │
│           [lh audit]                                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 数据流

```
外部代码仓库
    │
    ↓
lh-station transform
    ├── DNA 注入 (detector → injector)
    ├── 编译验证 (compiler)
    ├── 安全扫描 (security)
    ├── GPG 签章 (signer)
    ├── 产出打包 (packer) → manifest.json
    ├── 成本核算 (cost_analyzer) → .cost-report.json
    └── 封印存档 (seal) → ~/.longhun/memory/seals/
    │
    ↓
longhun-memory (记忆服务 :8771)
    ├── 封印记录入库
    └── DNA 索引更新
    │
    ↓
longhun-save (存储服务 :8772)
    ├── 交付物版本快照
    └── 历史追溯链
    │
    ↓
lh.py audit (三色审计)
    ├── manifest.json 读取
    ├── 十闸口比对
    └── 🟢/🟡/🔴 判定
    │
    ↓
🟢 → 可部署 (鲲鹏)
🟡 → 待核，人工复查
🔴 → 冻结，禁止发布
```

---

## 二、与各子系统对接

### 2.1 longhun-memory (记忆服务)

**接口**: `POST /api/memory/seal/register`
**触发时机**: `lh-station seal` 步骤完成后
**数据格式**:
```json
{
  "dna": "#龍芯⚡️丙午·䷗复-PROJECT-V1-A7F3C2B1",
  "seal_hash": "e3b0c442...",
  "seal_path": "~/.longhun/memory/seals/龍芯...seal.json",
  "manifest_checksum": "abc123...",
  "timestamp": "2026-08-06T12:00:00+08:00",
  "cost_monthly_cny": 2.37,
  "risk_level": "Low"
}
```

**幂等性**: DNA 已存在 → 返回 409（跳过）
**后续计划**: 封印自动注册到记忆服务（`lh-station seal --register`）

### 2.2 longhun-save (存储服务)

**接口**: `POST /api/save/version`
**触发时机**: 部署前
**数据格式**:
```json
{
  "dna": "#龍芯⚡️丙午·䷗复-PROJECT-V1-A7F3C2B1",
  "manifest": { "..." },
  "files": ["base64..."],
  "gpg_signed": true,
  "audit_mark": "🟢"
}
```

**版本管理**: 每个 DNA 对应一个版本快照，支持回滚。

### 2.3 lh.py (审计控制台)

**接口**: `lh audit --manifest path/to/manifest.json`
**触发时机**: 部署前（P14 + P77 + P05 链路）
**检查项**:
- GATE-01~10 十闸口
- manifest.json 字段完整性
- cost-report.json 风险等级
- GPG 签名验证
- 三色判定输出

### 2.4 鲲鹏部署

**路径**: `deploy/sync-to-kunpeng.sh`
**流程**:
```bash
# 1. 本地 transform
lh-station transform ./my-project/ --output ./lh-output/

# 2. 审计
lh audit --manifest ./lh-output/manifest.json

# 3. 🟢 通过 → 同步
bash deploy/sync-to-kunpeng.sh

# 4. 鲲鹏上运行
ssh root@119.13.90.27 'lh-station verify /opt/longhun/releases/...'
```

---

## 三、CI/CD 流水线串联

### GitHub Actions

```
push → audit(clippy+fmt) → build+test → supplement-tests
                                           ↓
                                     cross-check
                                           ↓
                                     security-scan
                                           ↓
                                     🟢 → deploy (手动)
```

### GitLab CI

```
push → audit → build → test → security
                              ↓
                        🟢 → deploy (manual)
                              ↓
                        鲲鹏 /opt/longhun/bin/lh-station
```

### 本地开发

```bash
# 1. 开发
cd tools/lh-station
cargo build

# 2. 测试
cargo test
cargo test --test supplement_tests -- --nocapture --test-threads=1

# 3. 自检
cargo clippy -- -D warnings
cargo fmt -- --check

# 4. 安全
cargo audit

# 5. 🟢 提交
git add -A && git commit -m "feat(lh-station): ..."
python3 ../../bin/lh_gpg_sign.py sign .
```

---

## 四、测试策略

### 测试分层

| 层级 | 位置 | 覆盖 | 说明 |
|:---|:---|:---|:---|
| 单元测试 | `src/**/*.rs #[cfg(test)]` | 每个模块独立测试 | 30 个（已有） |
| 补充测试 | `tests/supplement_tests.rs` | 跨模块集成 | 14 个（P0+P1） |
| E2E 测试 | CI 矩阵 | 全链路 | GitHub Actions |

### 补充测试分类

| 类别 | 优先级 | 测试数 | 说明 |
|:---|:---:|:---:|:---|
| B-构建 | P0/P1 | 5 | 空项目/B1, 超大文件/B2, 海量文件/B3, 纯二进制/B4, 已有DNA幂等/B5 |
| D-部署 | P1 | 3 | 无GPG/D1, 无Python/D2, 无交叉编译器/D3 |
| S-安全 | P0/P1 | 4 | 主权头完整性/S1, 重放攻击/S2, 注入绕过/S3, 封印篡改/S4 |
| CI-端到端 | P1 | 1 | 全链路八步管线/CI1 |

---

## 五、部署路线图

### Phase 1 (当前) ✅

- [x] 八步管线（detector·injector·compiler·security·signer·packer·cost_analyzer·seal）
- [x] GitHub Actions CI/CD
- [x] GitLab CI/CD
- [x] 补充测试套件（14 个）
- [x] README 用户手册

### Phase 2 (下一步)

- [ ] `lh-station seal --register` → 自动注册到 longhun-memory
- [ ] `lh-station deploy` → 一键部署到鲲鹏
- [ ] 支持 SM2/SM3 国密签名
- [ ] 支持更多芯片架构（申威/昇腾）

### Phase 3 (远期)

- [ ] Web Dashboard 可视化管理
- [ ] 分布式封印链（多节点验证）
- [ ] AI 驱动的安全审计增强

---

## 六、故障排查

### 常见问题

| 问题 | 原因 | 解决 |
|:---|:---|:---|
| `GPG not found` | 未安装 gpg | `brew install gnupg` / `apt install gnupg` |
| `Cross compile failed` | 缺少交叉编译器 | `apt install gcc-aarch64-linux-gnu` |
| `Seal idempotent skip` | DNA 已存在 | 正常行为，不重复封印 |
| `Cost analysis WARNING` | 检测到海外 API | 检查 `data_sovereign_risk` 字段 |

### 日志位置

- 运行日志: `lh-station` stdout
- 封印位置: `~/.longhun/memory/seals/`
- 封印索引: `~/.longhun/memory/seals/index.json`
- 审计日志: `tools/lh-station/logs/`

---

> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
> GPG: A2D0092CEE2E5BA87035600924C3704A8CC26D5F
