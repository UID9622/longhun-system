# 🐲 龍魂系统 · 阶段4审计报告

## 维权证据 GPG 签章 + Web 老百姓入口落地

**DNA**: #龍芯⚡️丙午·癸未·甲申·庚午·䷙大畜-PHASE4-WITNESS-SIGN-WEB-REPORT-20260804-UID9622  
**确认码**: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z  
**GPG**: A2D0092CEE2E5BA87035600924C3704A8CC26D5F  
**报告日期**: 2026-08-04  
**审计人**: 诸葛鑫（UID9622）  
**三色判定**: 🟢 通过

---

## 1. 目标

在阶段 3（SM4-CBC 加密）基础上，为老百姓维权证据固化增加：
1. **GPG 分离签名**：证明证据内容未被篡改
2. **Agent 审计链**：签名前由 P05/P15/S3 预审
3. **Web 入口**：浏览器点一下就能固化证据，降低使用门槛

---

## 2. 新增能力

### 2.1 CLI：一键签名固化

```bash
# 普通加密固化（阶段3已有）
lh --witness

# 新增：Agent 审计 + GPG 签章 + SM4 加密
lh --witness --sign

# 解密查看
lh --view-witness WITNESS-20260804_144906-da07cc9b2bba8330

# 启动 Web 服务
lh --witness-serve
```

### 2.2 执行流程（签名模式）

```
输入证据
   ↓
Agent 审计链（P05 上帝之眼 + P15 乔前辈 + S3 人民维权助手）
   ↓
生成 witness JSON（含内容 SHA-256）
   ↓
GPG 分离签名 → witness_*.json.asc
   ↓
SM4-CBC 加密 → witness_*.json.enc
   ↓
删除明文 JSON，保留 .enc（密文）和 .asc（签名）
```

### 2.3 Web 入口

| 文件 | 作用 |
|:---|:---|
| `web/witness.html` | 前端页面：输入框 + 签名开关 + 固化按钮 |
| `bin/lh_witness_server.py` | 本地 HTTP 服务，默认 `127.0.0.1:8780` |
| `lh --witness-serve` | CLI 启动入口 |

**Web 流程**：
1. 浏览器访问 `http://127.0.0.1:8780/`
2. 填写证据内容
3. 点击「固化证据」
4. 后端调用 `lh --witness --sign`
5. 返回证据 ID、加密文件路径、签名文件路径

---

## 3. 文件变更清单

| 文件 | 变更 | GPG 签名 |
|:---|:---|:---:|
| `08_BIN/lh.py` | 新增 `--sign` 解析、Agent 审计调用、GPG 签名、SM4 加密；新增 `--witness-serve` | ✅ |
| `08_BIN/lh.py.asc` | 重新签名 | ✅ |
| `05_ENGINES/longhun_agents/__init__.py` | 修复空文件导致 `GrandOrchestrator` 无法导入的 bug | ✅ |
| `bin/lh_witness_server.py` | 新增 Web 后端服务 | ✅ |
| `web/witness.html` | 新增前端页面 | ✅ |
| `audit/PHASE4_WITNESS_SIGN_WEB_REPORT_20260804.md` | 本报告 | ✅ |

---

## 4. 测试记录

### 4.1 CLI --witness --sign

```bash
printf "测试签名证据：平台无故封号\ndone\n" | ./bin/lh --witness --sign
```

**输出关键信息**：
- ✅ Agent 审计链完成（P05、P15、S3 均 ok）
- ✅ GPG 签章完成：`data/witness/witness_20260804_144407.json.asc`
- ✅ 证据已固化并加密：`data/witness/witness_20260804_144407.json.enc`
- 🆔 证据ID：`WITNESS-20260804_144407-2a0ab40d44353aa2`

### 4.2 Web API

```bash
python3 bin/lh_witness_server.py --port 8780
curl -X POST http://127.0.0.1:8780/api/witness \
  -H "Content-Type: application/json" \
  -d '{"content":"Web测试：平台恶意删帖","sign":true}'
```

**返回**：
```json
{
  "sign": true,
  "witness_id": "WITNESS-20260804_144758-481ae0445923f82e",
  "enc_file": "data/witness/witness_20260804_144758.json.enc",
  "asc_file": "data/witness/witness_20260804_144758.json.asc",
  "sha256": "481ae0445923f82e100855c38119b177",
  "audit": "P05→P15→S3"
}
```

### 4.3 CLI --witness-serve

```bash
lh --witness-serve
# 服务启动在 http://127.0.0.1:8780/
```

**验证**：`curl http://127.0.0.1:8780/health` 返回 `{"status":"ok"}`

### 4.4 旧模式兼容

```bash
printf "普通模式测试\ndone\n" | ./bin/lh --witness
```

**结果**：普通加密模式仍然正常工作，无签名文件生成。

---

## 5. 安全说明

| 风险 | 缓解措施 |
|:---|:---|
| Web 服务暴露公网 | 默认只监听 `127.0.0.1`，不对外暴露 |
| 明文证据落盘 | 加密后删除明文 JSON，仅保留 `.enc` 和 `.asc` |
| GPG 签名可验证性 | `.asc` 签名文件公开保留；验证时需先解密 `.enc` 恢复明文 |
| Agent 审计失败 | 审计失败不阻塞签名流程，仅提示警告 |
| 依赖注入 | Web 服务仅调用本地 `lh.py`，不执行用户输入的任何命令 |

---

## 6. 已知限制

1. **GPG 验证需先解密**：`.asc` 是对明文 JSON 的签名，但明文已删除。验证时需先用 `lh --view-witness` 解密到临时文件，再 `gpg --verify`。
2. **Web 服务无认证**：本地原型暂未加登录，后续可接入龍魂身份核验。
3. **大文件输入**：通过命令行参数/JSON 传递，超长内容可能受 shell/HTTP 限制。
4. **Agent 审计是本地 persona**：不产生网络调用，结果是基于规则/模板的评估，不是真人律师意见。

---

## 7. 签名验证

```bash
# 验证代码签名
gpg --verify 08_BIN/lh.py.asc 08_BIN/lh.py
gpg --verify bin/lh_witness_server.py.asc bin/lh_witness_server.py
gpg --verify web/witness.html.asc web/witness.html
```

---

## 8. 三色审计结论

| 审计项 | 状态 | 说明 |
|:---|:---:|:---|
| 签名正确性 | 🟢 | GPG 分离签名生成成功，密钥匹配 UID9622 |
| Agent 审计链 | 🟢 | P05→P15→S3 三步执行无报错 |
| Web 服务可用性 | 🟢 | `/api/witness` 返回正确 JSON |
| 本地安全 | 🟢 | 默认 127.0.0.1，无公网暴露 |
| 旧模式兼容 | 🟢 | `lh --witness` 不加 `--sign` 仍正常工作 |
| 主权锚定 | 🟢 | DNA + GPG + 确认码完整 |
| 验证便捷性 | 🟡 | 需先解密再验证签名，后续可加 `--verify-witness` |

**总体判定**: 🟢 阶段 4 完成，老百姓入口可用。

---

## 9. 下一步建议

1. **阶段 1B：收紧公网暴露面**（推荐）—— 把内部服务从 `0.0.0.0` 改为 `127.0.0.1`
2. **阶段 4.1**：增加 `--verify-witness ID` 命令，一键解密+验证 GPG 签名
3. **阶段 4.2**：给 Web 入口加本地身份核验或简单密码

---

*本报告由龍魂三色审计系统自动生成。*
