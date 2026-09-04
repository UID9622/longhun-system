# CNSH 标准库 v1.0

中文原生编程语言 CNSH 的官方标准库 —— **零三方依赖**（M77 零中间层铁律）。

## 模块一览

| 模块 | 功能 | 关键函数 |
|:---|:---|:---|
| `cnsh_std.io` | 文件读写 | `read` `write` `append` `read_json` `write_json` |
| `cnsh_std.http` | 网络请求 | `get` `post` `get_json`（默认禁代理直连） |
| `cnsh_std.crypto` | 哈希/加密 | `sha256` `hmac_sha256` `derive_key` `encrypt/decrypt` |
| `cnsh_std.time` | 时间/干支 | `now_iso` `ganzhi_stamp` `today` |
| `cnsh_std.dna` | DNA 追溯 | `generate` `validate` `extract` |
| `cnsh_std.audit` | 三色审计 | `verdict` `log` `read_log` |
| `cnsh_std.fuse` | P0 熔断 | `trip` `is_triggered` `check` |
| `cnsh_std.topo` | 系统拓扑 | `layers` `engines` `snapshot` |
| `cnsh_std.memorial` | 铭碑记录 | `record` `list_records` `freeze` |

## 安装

```bash
pip install -e packaging/cnsh-stdlib     # 开发安装
# 或直接使用（无需安装）:
import sys; sys.path.insert(0, "packaging/cnsh-stdlib")
from cnsh_std import io, dna, audit
```

## 快速上手

```python
from cnsh_std import dna, crypto, audit, fuse

# DNA 追溯码
code = dna.generate("MY-PACKAGE", "BUILD")
print(code)                      # #龍芯⚡️2026-09-04·MY-PACKAGE-BUILD-xxxxx

# 三色审计
audit.log("./audit.jsonl", {"scope": "发布", "verdict": "pass"})

# 加密（教学级）
tok = crypto.encrypt("机密", "口令")
print(crypto.decrypt(tok, "口令"))

# P0 熔断
fuse.check("正常操作")            # 通过
fuse.check("伪造DNA")            # 抛 PermissionError
```

## 自测

```bash
python3 packaging/cnsh-stdlib/tests/test_all.py
# ✅ CNSH 标准库自测: 通过 9 | 失败 0
```

## 签名

```
DNA:    #龍芯⚡️丙午·丁酉·乙酉·午时·䷾既济-CNSH-STDLIB-v1.0-UID9622
归属名: 诸葛鑫 | UID9622 · 龍芯北辰
GPG:    A2D0092CEE2E5BA87035600924C3704A8CC26D5F
License: MulanPSL v2 (工程实现层) · 核心思想层 CC BY-NC-SA 4.0
```


---

## 💛 支持龍魂（纯自愿 · 零黑箱）

龍魂的一切免费开放。若你认可「让技术为人、为普通人生长」，可自愿支持——款项仅用于服务器与开发成本，不留一分私账。

- **收款方式**: SOL / USDC（Solana）
- **实时地址与二维码**: 见官网 [uid9622.cn](https://uid9622.cn) 底部「支持龍魂」区 — 地址由 `lh wallet` 统一管理（公司账户落地后自动切换 · 以官网为准）

> 龍魂不诱导、不施压、不道德绑架。捐与不捐，开放与尊重不变。

<!-- LH-WALLET-SUPPORT -->
