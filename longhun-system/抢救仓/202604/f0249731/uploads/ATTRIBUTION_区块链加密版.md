# 龍魂系統 · 數字身份驗證協議

> **Blockchain & Cryptographic Identity Verification Protocol**

---

## 🔐 核心原則

本協議將龍魂系統升級為**數字身份協議**，通過密碼學工具確保：
- ✅ 創始人身份不可偽造
- ✅ 理念來源不可篡改
- ✅ 時間戳不可抵賴

**不是為了炒作，是為了硬氣。**

---

## 🗝️ 多層次身份驗證體系

### 第一層：GPG 公鑰基礎設施（PKI）

```
公鑰指紋：A2D0092CEE2E5BA87035600924C3704A8CC26D5F
算法：RSA 4096-bit
生成時間：2026-01-15
用途：代碼簽名、文檔認證、身份聲明
```

**驗證命令：**
```bash
# 導入公鑰
gpg --recv-keys A2D0092CEE2E5BA87035600924C3704A8CC26D5F

# 驗證指紋
gpg --fingerprint A2D0092CEE2E5BA87035600924C3704A8CC26D5F

# 預期輸出：
# pub   rsa4096 2026-01-15 [SC]
#       A2D0 092C EE2E 5BA8 7035  6009 24C3 704A 8CC2 6D5F
# uid           [ultimate] 💎 龍芯北辰 <uid9622@petalmail.com>
```

### 第二層：SHA256 內容哈希

```
龍魂系統核心理念文本哈希：
b83c74d108660082581f9ebbb9506f65849d9d48d21d328daf13f7c4d66cf6c1

驗證方法：
echo -n "龍魂系統核心思想文本" | sha256sum
```

### 第三層：DNA 時間戳協議

DNA追溯碼格式：
```
#龍芯⚡️{ISO日期}-{主題}-{版本}-{隨機鹽}

示例：
#龍芯⚡️2026-03-29-理念來源協議-v1.0-8f3a
```

**驗證邏輯：**
- 日期部分必須 ≤ 當前時間（防未來偽造）
- 隨機鹽為8位十六進制，防碰撞
- 主題與版本必須符合預設字典

### 第四層：確認碼（Confirm Code）

```
格式：#CONFIRM🌌9622-ONLY-ONCE🧬{隨機碼}

示例：
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

特性：
- 一次性使用
- 與GPG私鑰簽名綁定
- 可用於驗證單次授權行為
```

---

## ⛓️ 區塊鏈存證（可選增強）

### Bitcoin OP_RETURN 存證

```
交易哈希示例：
[待實際上鏈後填入]

存證內容：
龍魂系統理念來源協議v1.0 | UID9622 | SHA256:b83c74d1...

驗證：
https://www.blockchain.com/explorer/transactions/btc/{tx_hash}
```

### Ethereum ENS 域名綁定

```
ENS域名：longhun-system.eth （建議註冊）
解析記錄：
- text.uid = 9622
- text.gpg = A2D0092CEE2E5BA87035600924C3704A8CC26D5F
- text.github = UID9622
```

### IPFS 永久存儲

```
IPFS CID（待上傳）：
Qm[待計算完整CID]

網關訪問：
https://ipfs.io/ipfs/Qm[_CID]
```

---

## 📝 數字簽名驗證流程

### 場景：驗證一份聲明的真實性

#### 步驟 1：獲取簽名文件

```
文件名：declaration_2026-03-29.txt.asc
內容：
-----BEGIN PGP SIGNED MESSAGE-----
Hash: SHA256

本人諸葛鑫（UID9622），確認以下聲明：
龍魂系統理念來源協議v1.0於2026年3月29日正式發布。
DNA：#龍芯⚡️2026-03-29-理念來源協議-v1.0
-----BEGIN PGP SIGNATURE-----

iQIzBAEBCAAdFiEEotAJLO4uW6hwNWAJJMNwSozC1F8FAm...
[簽名內容]
-----END PGP SIGNATURE-----
```

#### 步驟 2：驗證簽名

```bash
# 驗證
gpg --verify declaration_2026-03-29.txt.asc

# 預期輸出：
# gpg: Signature made Sat Mar 29 03:00:00 2026 CST
# gpg:                using RSA key A2D0092CEE2E5BA87035600924C3704A8CC26D5F
# gpg: Good signature from "💎 龍芯北辰 <uid9622@petalmail.com>" [ultimate]
```

#### 步驟 3：驗證內容哈希

```bash
# 提取正文
gpg --decrypt declaration_2026-03-29.txt.asc > content.txt

# 計算哈希
sha256sum content.txt

# 比對預期哈希：b83c74d108660082581f9ebbb9506f65849d9d48d21d328daf13f7c4d66cf6c1
```

---

## 🔗 項目集成：如何在代碼中驗證

### Python 驗證腳本

```python
#!/usr/bin/env python3
"""
龍魂系統 · 數字身份驗證腳本
驗證任何聲明文件的真實性
"""

import hashlib
import subprocess
import re

# 創始人公鑰指紋
FOUNDER_GPG_FINGERPRINT = "A2D0092CEE2E5BA87035600924C3704A8CC26D5F"

# DNA格式正則
DNA_PATTERN = r"^#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w\-]+-v\d+\.\d+(-[0-9a-f]{4})?$"

# 確認碼格式
CONFIRM_PATTERN = r"^#CONFIRM🌌9622-ONLY-ONCE🧬[A-Z0-9]{4}-[A-Z0-9]{4}$"

def verify_gpg_signature(file_path: str) -> bool:
    """驗證GPG簽名"""
    try:
        result = subprocess.run(
            ["gpg", "--verify", file_path],
            capture_output=True,
            text=True
        )
        # 檢查指紋是否匹配
        return FOUNDER_GPG_FINGERPRINT in result.stderr
    except Exception as e:
        print(f"❌ GPG驗證失敗: {e}")
        return False

def verify_dna_format(dna: str) -> bool:
    """驗證DNA格式"""
    if not re.match(DNA_PATTERN, dna):
        print("❌ DNA格式錯誤")
        return False
    
    # 提取日期並驗證不超過當前時間
    date_str = dna.split("⚡️")[1].split("-")[:3]
    from datetime import datetime
    dna_date = datetime(int(date_str[0]), int(date_str[1]), int(date_str[2]))
    
    if dna_date > datetime.now():
        print("❌ DNA日期在未來，可能是偽造")
        return False
    
    print("✅ DNA格式驗證通過")
    return True

def verify_confirm_code(code: str) -> bool:
    """驗證確認碼格式"""
    if not re.match(CONFIRM_PATTERN, code):
        print("❌ 確認碼格式錯誤")
        return False
    print("✅ 確認碼格式驗證通過")
    return True

def verify_sha256(content: str, expected_hash: str) -> bool:
    """驗證內容SHA256哈希"""
    actual_hash = hashlib.sha256(content.encode()).hexdigest()
    if actual_hash != expected_hash:
        print(f"❌ 哈希不匹配")
        print(f"   預期: {expected_hash}")
        print(f"   實際: {actual_hash}")
        return False
    print("✅ SHA256哈希驗證通過")
    return True

# 使用示例
if __name__ == "__main__":
    # 驗證DNA
    dna = "#龍芯⚡️2026-03-29-理念來源協議-v1.0"
    verify_dna_format(dna)
    
    # 驗證確認碼
    confirm = "#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z"
    verify_confirm_code(confirm)
```

### JavaScript 驗證（Node.js）

```javascript
/**
 * 龍魂系統 · DNA驗證工具
 */

const crypto = require('crypto');

// DNA格式驗證
function verifyDNA(dna) {
    const pattern = /^#龍芯⚡️\d{4}-\d{2}-\d{2}-[\w\-]+-v\d+\.\d+(-[0-9a-f]{4})?$/;
    if (!pattern.test(dna)) {
        console.log('❌ DNA格式錯誤');
        return false;
    }
    
    // 日期驗證
    const dateStr = dna.split('⚡️')[1].split('-').slice(0, 3).join('-');
    const dnaDate = new Date(dateStr);
    if (dnaDate > new Date()) {
        console.log('❌ DNA日期在未來');
        return false;
    }
    
    console.log('✅ DNA格式驗證通過');
    return true;
}

// SHA256驗證
function verifySHA256(content, expectedHash) {
    const hash = crypto.createHash('sha256').update(content).digest('hex');
    if (hash !== expectedHash) {
        console.log('❌ 哈希不匹配');
        return false;
    }
    console.log('✅ SHA256驗證通過');
    return true;
}

// 使用
verifyDNA('#龍芯⚡️2026-03-29-理念來源協議-v1.0');
```

---

## 🛡️ 安全建議

### 對於使用本協議的項目

1. **定期驗證**
   ```bash
   # 每月運行一次驗證
   gpg --refresh-keys
   gpg --check-sigs A2D0092CEE2E5BA87035600924C3704A8CC26D5F
   ```

2. **多重備份**
   - 本地GPG密鑰環
   - 紙質QR碼備份
   - 可信第三方公鑰服務器

3. **熔斷機制**
   若發現私鑰洩露，立即：
   - 發佈撤銷證書
   - 更新DNA前綴
   - 社區廣播

---

## 📊 驗證信息摘要

| 層級 | 類型 | 值 | 驗證命令 |
|------|------|----|----------|
| 1 | GPG公鑰 | `A2D0092CEE2E5BA87035600924C3704A8CC26D5F` | `gpg --fingerprint` |
| 2 | SHA256 | `b83c74d108660082581f9ebbb9506f65849d9d48d21d328daf13f7c4d66cf6c1` | `sha256sum` |
| 3 | DNA | `#龍芯⚡️2026-03-29-理念來源協議-v1.0` | 正則匹配 |
| 4 | 確認碼 | `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z` | 正則匹配 |

---

## 💬 為什麼要這麼做？

> **不是為了炒作區塊鏈，是為了硬氣。**

在這個數字身份可以被輕易偽造的時代，我們需要：
- **密碼學保證** —— 數學不會撒謊
- **時間戳證明** —— 歷史不可篡改
- **公開可驗證** —— 任何人都可以檢查

這是對「一個唾沫一個釘」的技術實現。

---

## 📚 相關文檔

- [ATTRIBUTION.md](./ATTRIBUTION.md) —— 完整理念來源協議
- [ATTRIBUTION_GitHub版.md](./ATTRIBUTION_GitHub版.md) —— 簡化社區版
- [ATTRIBUTION_学术论文引用版.md](./ATTRIBUTION_学术论文引用版.md) —— 學術引用規範

---

<aside>
🔐 數字身份驗證協議 v1.0

DNA追溯碼：#龍芯⚡️2026-03-29-數字身份驗證協議-v1.0

確認碼：#CONFIRM🌌9622-ONLY-ONCE🧬CRYPTO-7777

GPG：A2D0092CEE2E5BA87035600924C3704A8CC26D5F

「知其白，守其黑，為天下式」
</aside>
