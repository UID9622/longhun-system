---
title: DNA流水線·四步自動化引擎
tags: [流水線, 自動化, Python, 追溯, 執行]
---

# DNA 流水線自動化

**DNA**: #龍芯⚡️20260525|DNA-PIPELINE-AUTOMATION|v1.0
**完成度**: 100% ✅
**代碼行數**: 960+ 行 Python
**工具位置**: `~/longhun-system/tools/DNA追溯流水線_自動化觸發器.py`

---

## 📌 流水線架構

```
發佈 (Step 1)
  ├─ 打水印（embed DNA）
  ├─ 生成簽名
  └─ 自動郵件登記
       ↓
檢測 (Step 2)
  ├─ 掃描水印
  ├─ 識別釣鉤
  └─ 收集證據
       ↓
追溯 (Step 3)
  ├─ 反向追蹤
  ├─ 生成黑名單
  └─ 公開發佈
       ↓
審計 (Step 4)
  ├─ 生成審計日誌
  ├─ 法律時間戳
  └─ 閉環驗證
```

---

## 🔧 核心組件

### 1. Step 1：發佈與嵌入

```python
def step1_prepare_and_register(content, platform, uid):
    # 1. 生成 DNA
    dna = generate_dna(date=today, topic=extract_topic(content))

    # 2. 打水印
    watermarked_content = embed_watermark(content, dna)

    # 3. 生成簽名
    signature = sign_with_key(watermarked_content, uid)

    # 4. 自動郵件登記
    send_registration_email(
        to="longhun2025@petalmail.com",
        subject=f"DNA登記 {dna}",
        body=registration_template(dna, platform, content_hash)
    )

    return {
        "dna": dna,
        "watermarked": watermarked_content,
        "signature": signature,
        "registered": True
    }
```

**觸發條件**：用戶在 CSDN/知乎/掘金 點擊「發佈」

---

### 2. Step 2：檢測與取證

```python
def step2_detect_infringement(page_url, page_html):
    # 1. 掃描水印
    detected_dnas = scan_watermarks(page_html)  # 三層檢測

    # 2. 識別釣鉤
    hooks = detect_hooks(page_html)  # 18+11 類

    # 3. 收集證據
    evidence = {
        "url": page_url,
        "title": extract_title(page_html),
        "dnas_found": detected_dnas,
        "hooks_detected": hooks,
        "screenshot": take_screenshot(page_url),
        "html_snapshot": page_html,
        "timestamp": now(),
        "hash": sha256(page_html)
    }

    # 4. 保存證據包
    evidence_id = save_evidence(evidence)

    return {
        "evidence_id": evidence_id,
        "infringement_score": calculate_score(hooks, detected_dnas),
        "ready_for_report": True
    }
```

**觸發條件**：用戶右鍵菜單「標記侵權」或自動掃描定時任務

---

### 3. Step 3：追溯與發佈

```python
def step3_trace_and_publish(evidence_id, original_dna):
    evidence = load_evidence(evidence_id)

    # 1. 反向追蹤
    trace_result = trace_back_to_origin(
        infringe_url=evidence["url"],
        dna_signature=original_dna
    )

    # 2. 生成黑名單條目
    blacklist_entry = {
        "domain": extract_domain(evidence["url"]),
        "reason": "大量侵權",
        "evidence_id": evidence_id,
        "added_date": now(),
        "violation_count": count_violations_by_domain(evidence["url"])
    }

    # 3. 發佈到 shame wall（公開黑名單）
    publish_to_shame_wall(blacklist_entry)

    # 4. 更新本地黑名單
    add_to_blacklist(blacklist_entry)

    return {
        "trace_id": generate_id(),
        "blacklist_published": True,
        "domains_blacklisted": [blacklist_entry["domain"]]
    }
```

**觸發條件**：檢測到高分侵權（自動或手動確認）

---

### 4. Step 4：審計與閉環

```python
def step4_audit_closure(evidence_id, trace_id):
    # 1. 生成審計日誌
    audit_log = {
        "evidence_id": evidence_id,
        "trace_id": trace_id,
        "step1_timestamp": load_step1_time(evidence_id),
        "step2_timestamp": load_step2_time(evidence_id),
        "step3_timestamp": load_step3_time(evidence_id),
        "step4_timestamp": now(),
        "uid": UID9622,
        "status": "closed"
    }

    # 2. 申請法律時間戳
    legal_timestamp = request_legal_timestamp(
        evidence_package=evidence_id,
        timestamp=now()
    )

    # 3. 驗證完整性
    verification_result = verify_chain_integrity(
        dna_signature=load_dna(evidence_id),
        hash_chain=[step1_hash, step2_hash, step3_hash, step4_hash]
    )

    # 4. 存檔
    save_audit_log(audit_log)
    save_legal_timestamp(legal_timestamp)

    return {
        "audit_id": audit_log["evidence_id"],
        "legal_timestamp": legal_timestamp,
        "chain_verified": verification_result["valid"],
        "closure_status": "complete"
    }
```

**觸發條件**：Step 3 完成後自動執行

---

## 📊 數據庫模式

### SQLite 表結構

```sql
-- 已發佈內容
CREATE TABLE published_content (
  id TEXT PRIMARY KEY,
  dna TEXT UNIQUE,
  platform TEXT,
  title TEXT,
  content_hash TEXT,
  publish_date TIMESTAMP,
  uid TEXT
);

-- 侵權檢測記錄
CREATE TABLE infringement_records (
  id TEXT PRIMARY KEY,
  evidence_id TEXT,
  source_dna TEXT,
  infringe_url TEXT,
  detected_dnas TEXT,  -- JSON array
  hooks_detected TEXT, -- JSON array
  infringement_score FLOAT,
  detection_date TIMESTAMP
);

-- 黑名單
CREATE TABLE blacklist (
  id TEXT PRIMARY KEY,
  domain TEXT UNIQUE,
  violation_count INT,
  added_date TIMESTAMP,
  status TEXT  -- active|removed
);

-- 審計日誌
CREATE TABLE audit_logs (
  id TEXT PRIMARY KEY,
  evidence_id TEXT,
  trace_id TEXT,
  step1_time TIMESTAMP,
  step2_time TIMESTAMP,
  step3_time TIMESTAMP,
  step4_time TIMESTAMP,
  legal_timestamp TEXT,
  chain_verified BOOLEAN
);
```

---

## 🚀 使用示例

### 快速開始

```bash
# 1. 發佈內容時自動觸發 Step 1
python DNA追溯流水線_自動化觸發器.py --step 1 \
  --content "my_article.md" \
  --platform "CSDN"

# 2. 檢測侵權
python DNA追溯流水線_自動化觸發器.py --step 2 \
  --url "https://infringing-site.com/article"

# 3. 追溯發佈
python DNA追溯流水線_自動化觸發器.py --step 3 \
  --evidence-id "abc123" \
  --original-dna "#龍芯⚡️20260525|ARTICLE|v1.0|xxx"

# 4. 審計閉環
python DNA追溯流水線_自動化觸發器.py --step 4 \
  --evidence-id "abc123"
```

---

## 📧 自動郵件系統

### 登記郵件格式

```
收件人: longhun2025@petalmail.com
主題: DNA登記 #龍芯⚡️20260525|...

內容:
---
【DNA 登記】
日期: 2026-05-25
DNA: #龍芯⚡️20260525|ARTICLE-TITLE|v1.0|abc123def4

平台: CSDN
文章標題: [標題]
內容摘要: [前 200 字]
內容哈希: sha256_hash

發佈人: UID9622
確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

此郵件可作為原創時間戳證據。
---
```

---

## ⚙️ 配置文件

位置: `~/longhun-system/config/dna_pipeline.yaml`

```yaml
pipeline:
  step1:
    auto_trigger: true
    platforms: [CSDN, 知乎, 掘金]

  step2:
    scan_interval: 3600  # 每小時掃描一次
    hooks_weight_threshold: 0.5

  step3:
    auto_publish_threshold: 0.8  # 信心度 > 80% 自動發佈
    shame_wall_url: "https://longhun.example.com/blacklist"

  step4:
    legal_timestamp_provider: "http://timestamp.authority.com"
    archive_path: "/path/to/audit/logs"
```

---

## 📈 性能指標

| 指標 | 數值 | 說明 |
|------|------|------|
| Step 1 執行時間 | < 2s | 發佈→登記 |
| Step 2 掃描時間 | 5-30s | 取決於頁面大小 |
| Step 3 發佈時間 | < 1s | 黑名單更新 |
| Step 4 審計時間 | < 5s | 生成日誌 + 時間戳 |
| **完整流水線** | **10-40s** | 從檢測到審計閉環 |

---

## 🔐 安全機制

✅ DNA 簽名驗證
✅ 時間戳不可篡改
✅ 哈希鏈完整性檢查
✅ 審計日誌加密存儲
✅ 郵件確認追蹤

---

## 相關文件

- **完整代碼**: `~/longhun-system/tools/DNA追溯流水線_自動化觸發器.py`
- **快速開始**: `~/longhun-system/tools/DNA流水線_快速開始.md`
- **DNA 系統**: [[DNA追溯系統]]
- **Widget 集成**: [[LongHunWidget 項目]]

---

DNA: `#龍芯⚡️20260525|DNA-PIPELINE-AUTOMATION|v1.0`
責任: UID9622·不免責
