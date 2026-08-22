# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# CNSH 命名问题修复建议

**DNA**: `#龍芯⚡️丙午·甲午·丁卯·丙午·䷚颐-CNSH-NAMING-REMEDIATION-v1.0`  
**生成时间**: 2026-06-22  
**扫描范围**: /Users/zuimeidedeyihan/longhun-system  
**扫描文件数**: 3519  
**命名问题文件**: 1686  
**问题条目总数**: 11943  
**CNSH 相关文件**: 1134

---

## 一、核心发现

1. **英文变量名占主导**: 大量代码使用英文变量名/函数名，未按 CNSH L2 语法层规范使用中文命名或 `CNSH_` / 层级前缀。
2. **常量命名混乱**: 大量全大写英文常量（如 `NOTION_TOKEN`、`CONFIG`、`PERSONAS_DATA`）未映射为中文层级前缀（如 `数据_notion_token`、`配置_核心`）。
3. **短变量名过多**: `p`、`s`、`i`、`x`、`y` 等无意义短名不符合可读性要求。
4. **龍字合规**: 未发现 `龍` 字简化问题（已通过繁简体归一确保）。

---

## 二、修复优先级

| 优先级 | 对象 | 修复方式 |
|---|---|---|
| P0 | 核心模块（`cnsh/`、`cnsh-core/`、`control-panel/`） | 优先中文命名改造 |
| P1 | 工具脚本（`bin/`、`agents/`） | 中文命名 + 中文注释 |
| P2 | 文档与配置（`docs/`、`*.md`、`*.json`） | 术语中文化 |
| P3 | 研究/实验代码（`research/`、`experiments/`） | 记录建议，暂缓改造 |
| P4 | 第三方/归档（`_archive/`、依赖目录） | 不修改 |

---

## 三、命名规范速查

```
变量: 纯中文 或 CNSH_前缀 或 层级前缀
      例: 用户列表、数据_配置、CNSH_运行时

函数: 纯中文动词开头
      例: 计算数字根(文本)、验证DNA(链)

类:   大驼峰或纯中文
      例: 龍魂运行时、DNA追溯器

常量: 优先中文命名，必要时层级前缀
      例: 数据_notion_token、配置_根目录
```

---

## 四、高频英文命名 → 中文映射建议

| 英文模式 | 中文映射建议 |
|---|---|
| `config` / `configuration` | `配置` / `数据_配置` |
| `token` | `令牌` / `数据_令牌` |
| `user` | `用户` |
| `data` | `数据` |
| `result` / `results` | `结果` / `数据_结果` |
| `error` | `错误` |
| `message` / `msg` | `消息` |
| `logger` | `日志器` / `记录器` |
| `level` | `层级` / `级别` |
| `mode` | `模式` |
| `status` | `状态` |
| `value` / `val` | `值` |
| `key` | `键` |
| `index` / `idx` | `索引` |
| `count` / `num` | `计数` |
| `size` | `大小` |
| `path` | `路径` |
| `file` | `文件` |
| `dir` / `directory` | `目录` |
| `name` | `名称` |
| `id` | `标识` |
| `type` | `类型` |
| `action` | `动作` |
| `event` | `事件` |
| `handler` | `处理器` |
| `callback` | `回调` |
| `request` / `req` | `请求` |
| `response` / `resp` | `响应` |
| `client` | `客户端` |
| `server` | `服务端` |
| `database` / `db` | `数据库` |
| `table` | `表` |
| `record` | `记录` |
| `query` | `查询` |
| `filter` | `过滤` |
| `sort` | `排序` |
| `validate` | `验证` |
| `parse` | `解析` |
| `render` | `渲染` |
| `execute` / `exec` | `执行` |
| `process` | `处理` |
| `analyze` | `分析` |
| `check` | `检查` |
| `audit` | `审计` |
| `trace` | `追溯` |
| `encrypt` | `加密` |
| `decrypt` | `解密` |
| `sign` | `签名` |
| `verify` | `校验` |

---

## 五、重点文件清单（按问题数量排序）

```
test_audit_integration_v1.py            199 警告
research/riemann_numerical_verification_extended.py   150 警告
research/riemann_perspective_C_proof.py  123 警告
skill-standards.integrated/longhun-standard-calculation-framework.py   105 警告
longhun_mvp_executor_v1.0.py             49 警告
longhun_mvp_setup_integration_v1.0.py    58 警告
brain_notion_sync.py                     87 警告
longhun_self_check_v1.0.py               41 警告
baobao-guardian/backend/app/main.py      40 警告
research/riemann_three_talent_verification.py   73 警告
```

---

## 六、修复原则

1. **不动运行逻辑**: 命名改造只改标识符，不改算法和数据结构。
2. **批量替换前备份**: 每个文件改造前先 git 提交或备份。
3. **按优先级分批**: 先 P0 核心模块，再 P1 工具脚本，最后文档。
4. **测试先行**: 每个模块改造后必须运行单元测试，确保可执行性。
5. **保留英文映射**: 在注释或文档中保留英文原名，便于生态对接。

---

## 七、自动化修复脚本使用

```bash
# 查看完整命名问题 JSON
/tmp/cnsh_scan_report.json

# 查看完整修复建议 JSON
/tmp/cnsh_naming_remediation.json

# 使用 CNSH 运行时检查单个文件
python3 ~/.kimi-code/skills/longhun-cnsh/scripts/CNSH运行时.py --naming-check 目标文件.py
```

---

**数据主权归于人民 · 中文编程自主 · 龍魂文化主权不可侵犯**
