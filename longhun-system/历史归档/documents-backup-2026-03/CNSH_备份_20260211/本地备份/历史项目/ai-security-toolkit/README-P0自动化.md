# UID9622 AI安全工具包 - P0级自动化系统

> 🎯 **确认码**: #UID9622-P0-REALNESS-PROTOCOL-V1.0  
> 🌐 **仓库**: https://gitee.com/uid9622/ai-security-toolkit  
> 🔐 **版本**: UID9622-CONTROL-PLANE-GOVERNANCE-V2.1

---

## 🚀 一条命令自动化

CodeBuddy/CI只需要执行4个命令：

```bash
# 健康检查（不修改任何东西）
make healthcheck

# 生成审计事件 + 日志  
make audit

# 生成整改措施（不直接改代码）
make remediate

# 登记到registry并可选推送到Gitee
make register
```

---

## 📁 仓库结构（复制即可）

```
/dist/                       # 公开产物（脱敏后）
/events/                     # 事件（强制落盘）
/logs/                       # 日志（强制落盘）
/remediation/                # 整改措施（结构化）
/registry/                   # 登记台账（机器可读）
/keys/                       # 公钥（只放公钥）
/scripts/
    healthcheck.py            # 健康检查
    control_plane.py          # 总控台
    updater.py               # 更新器
    register_audit.py        # 登记器
    make_event.py           # 事件生成器
Makefile                    # 入口命令
instance_meta.json           # 实例元数据
```

---

## 🔍 P0事件契约

### 事件命名规范
`event_<instance_id>_<YYYYMMDD>T<HHMMSS><TZOFFSET>_<STATUS>_<ACTION>_<REASON>.json`

### 强制字段
- `evidence.event_file` 必须存在且与实际落盘一致
- 缺失/不一致 = `META_INVALID` + `exit_code=6` + 停机

### 退出码标准
- **0**: OK (允许继续)
- **1**: HEALTHCHECK_FAILED (dist不合格)
- **2**: BLOCK_STARTUP (红色拦截)
- **3**: UPDATE_FAILED (更新失败)
- **4**: SIGNATURE_INVALID (验签失败)
- **5**: HASH_MISMATCH (sha256不匹配)
- **6**: META_INVALID (字段缺失/格式错误)

---

## 📋 登记台账: registry.jsonl

每行一个记录，天然可追加、可diff、可审计：

```json
{"audit_event_file":"events/...","remediation_file":"remediation/...","repo":"https://gitee.com/uid9622/ai-security-toolkit","commit":"...","status":"OPEN","owner":"uid9622-ai-assistant","created_at":"2025-12-24T10:07:54.123456","registered_at":"2025-12-24T10:08:00.654321"}
```

---

## 🔧 整改措施格式

固定4段结构，不给黑箱留空间：

1. **问题是什么** (引用event的reason_code)
2. **影响范围** (影响谁、影响什么)
3. **修复步骤** (最小步骤，不写花活)
4. **验收标准** (如何证明修好了：要出现什么OK事件)

---

## 🎯 CodeBuddy永久执行口令

> **必须先计划再执行；执行必留痕；失败必停机。**

1. **执行前输出**: 将改哪些文件 + 将产出哪些event/log + 回滚点
2. **执行后必须落盘**: `./events/` event（命名按规范）+ `./logs/` 日志
3. **event必须包含** `evidence.event_file`，并与实际落盘一致，否则写FAIL(`META_INVALID`, exit_code=6)并停止
4. **整改不允许直接"偷偷改"**，必须先产出`remediation/*.md`，给出验收标准

---

## 🌍 国内外协作支持

### 协作契约
- **默认义务**: 按24小时窗口更新；不更新即被强制
- **禁止行为**: 反向覆盖母本；绕过三色审计；删日志
- **争议处理**: 以事件与日志为唯一证据

### P0三关口已打通
- ✅ **入口关口**: 只发dist，统一接入流程
- ✅ **签名关口**: Ed25519 + SHA256验证
- ✅ **数据边界关口**: 24小时窗口，跨境合规

---

## 📊 当前状态

- 🟢 **总控台**: 正常运行
- 🟢 **更新器**: 正常运行  
- 🔴 **健康检查**: 发现占位符痕迹需修复
- ✅ **事件系统**: 正常生成事件和日志
- ✅ **登记系统**: 正常登记到registry.jsonl

---

## 🎉 使用示例

```bash
# 初始化仓库结构
make init

# 完整自动化流程
make healthcheck && make audit && make remediate && make register

# 提交到Gitee
git add .
git commit -m "P0自动化执行 - 事件+整改+登记"  
git push origin master
```

---

**透明度**: 📊 所有操作完全公开透明  
**审计**: 🔴 三色P0审计系统已启动  
**追责**: 📋 事件+日志+registry完整证据链  

---
*最后更新: 2025-12-24 10:10 GMT+8*  
*确认码: #UID9622-P0-REALNESS-PROTOCOL-V1.0*